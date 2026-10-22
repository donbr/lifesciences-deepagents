"""How a failed tool activity reaches the agent under Temporal.

An I/O tool runs as a ``deepagents.invoke_tool`` activity. A transient failure
is retried by the activity's retry policy; a permanent failure, or a transient
one that exhausts its retries, surfaces in the workflow as ``ActivityError``.
LangGraph's ToolNode re-raises that, which would abort the whole run, so
``ToolFailureMiddleware`` turns it into an error ``ToolMessage`` the agent can
react to, and stops the run once one service has run out of retries on
transient errors several times in a row. A permanent failure (HTTP 400/404,
JSON-RPC invalid params: usually a bad query the agent wrote) reaches the
agent the same way but says nothing about the service being down, so it does
not count.

The failure counts live on the middleware instance, which the workflow builds
inside ``run``. They are therefore rebuilt from history on every replay: a
crashed or evicted worker resumes with the same counts, never with zeros.
"""

from collections import Counter
from collections.abc import Awaitable, Callable, Mapping
from typing import Any
from urllib.parse import urlsplit

from langchain.agents.middleware.types import AgentMiddleware, ToolCallRequest
from langchain_core.messages import ToolMessage
from temporalio.exceptions import ActivityError, ApplicationError, FailureError, RetryState

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from shared.mcp import LIFESCIENCES_ALIAS_TOOL_NAMES, rate_limiter

# The temporalio-deepagents activity name (as in scripts/temporal_run_report.py);
# a literal so we do not import the package's private _activity module.
INVOKE_TOOL = "deepagents.invoke_tool"

# Retry states of a tool activity that ran out of retries on transient errors
# (timeouts, transport errors, 429, 5xx): evidence the service is down. A
# permanent MCPCallError ends as NON_RETRYABLE_FAILURE instead.
_EXHAUSTED_RETRY_STATES = frozenset({RetryState.MAXIMUM_ATTEMPTS_REACHED, RetryState.TIMEOUT})


def _query_api_direct_service(args: Mapping[str, Any] | None) -> str:
    """``query_api_direct:<host>``, or ``query_api_direct`` without a usable URL.

    Pure string parsing of the tool call's ``url`` argument (no I/O), so the
    key is the same on every replay.
    """
    url = args.get("url") if isinstance(args, Mapping) else None
    if isinstance(url, str):
        try:
            host = urlsplit(url).hostname
        except ValueError:
            host = None
        if host:
            return f"query_api_direct:{host}"
    return "query_api_direct"


def service_for_tool(tool_name: str, args: Mapping[str, Any] | None = None) -> str:
    """The upstream service a tool call depends on, for counting failures.

    Starts from ``rate_limiter.get_service_from_tool`` (the service an
    ``MCPCallError`` names), but splits its catch-all ``"default"`` bucket:
    an HGNC outage says nothing about WikiPathways. ``query_api_direct`` is
    keyed by the host of its ``url`` argument: a bad Open Targets query says
    nothing about ClinicalTrials.gov.
    """
    if tool_name == "query_api_direct":
        return _query_api_direct_service(args)
    service = rate_limiter.get_service_from_tool(tool_name)
    if service != "default":
        return service
    if tool_name in LIFESCIENCES_ALIAS_TOOL_NAMES:
        return tool_name.split("_", 1)[0]
    if tool_name == "query_pubmed":
        return "pubmed"
    return tool_name


def _failure_message(error: ActivityError) -> str:
    """The text the agent should see for a failed tool activity.

    Temporal keeps the whole ``__cause__`` chain, and ``MCPCallError`` is
    raised ``from`` the underlying httpx/stdio error, so the deepest cause is
    raw transport text. Use the first ``MCPCallError`` in the chain (the
    curated message); failing that, the activity's own error.
    """
    causes: list[BaseException] = []
    cause = error.__cause__
    while cause is not None:
        causes.append(cause)
        cause = cause.__cause__
    for cause in causes:
        if isinstance(cause, ApplicationError) and cause.type == "MCPCallError":
            return cause.message
    if not causes:
        return error.message
    first = causes[0]
    return first.message if isinstance(first, FailureError) else str(first)


class ToolFailureMiddleware(AgentMiddleware):
    """Failed tool activity -> error ToolMessage; N in a row for a service -> fail the run.

    Only a failure whose retries ran out on transient errors
    (``RetryState.MAXIMUM_ATTEMPTS_REACHED`` or ``TIMEOUT``) adds to the
    service's count. A permanent failure (``NON_RETRYABLE_FAILURE``: the
    ``ApplicationError(type="MCPCallError", non_retryable=True)`` raised for
    HTTP 4xx, JSON-RPC errors, ...) still reaches the agent as an error
    message but neither adds to nor resets the count. A success resets it.

    Use one instance per workflow run, shared by the supervisor and every
    specialist, so failures of one service count across agents.

    Invariant: a trip is sticky (the count is never reset once it reaches the
    limit, and every later call for that service raises the same error). That
    is only safe because the trip error, ``MCPServiceUnavailable``
    (non-retryable), always propagates out of the agent and fails the
    workflow, so no call ever runs after a trip. If the trip error is ever
    caught and the run continues, the service stays blocked for the rest of
    the run.
    """

    def __init__(self, max_consecutive_failures: int = 3) -> None:
        super().__init__()
        self.max_consecutive_failures = max_consecutive_failures
        self._failures: Counter[str] = Counter()

    def _tripped(self, service: str) -> bool:
        return self._failures[service] >= self.max_consecutive_failures

    def _unavailable(self, service: str) -> ApplicationError:
        # Always the limit, not the running count: parallel branches can add a
        # failure after the limit in the same workflow task, and whichever
        # branch's error reaches the workflow first must say the same thing.
        return ApplicationError(
            f"MCP service {service} unavailable after "
            f"{self.max_consecutive_failures} consecutive failures",
            type="MCPServiceUnavailable",
            non_retryable=True,
        )

    @staticmethod
    def _service(request: ToolCallRequest) -> str:
        return service_for_tool(request.tool_call["name"], request.tool_call.get("args"))

    def _before_call(self, request: ToolCallRequest) -> None:
        # Once tripped, a service stays down for the rest of the run: no new
        # calls to it, only the same error.
        service = self._service(request)
        if self._tripped(service):
            raise self._unavailable(service)

    def _on_result(self, request: ToolCallRequest, result: Any) -> None:
        # An error message here never reached the service (e.g. ToolNode
        # rejected the arguments), so it is not evidence the service is up.
        if isinstance(result, ToolMessage) and result.status == "error":
            return
        service = self._service(request)
        if not self._tripped(service):
            self._failures.pop(service, None)

    def _on_failure(self, request: ToolCallRequest, error: ActivityError) -> ToolMessage:
        name = request.tool_call["name"]
        service = self._service(request)
        if error.retry_state in _EXHAUSTED_RETRY_STATES:
            self._failures[service] += 1
        if self._tripped(service):
            raise self._unavailable(service) from error
        return ToolMessage(
            content=f"Tool error ({name}): {_failure_message(error)}",
            name=name,
            tool_call_id=request.tool_call["id"],
            status="error",
        )

    @staticmethod
    def _is_tool_failure(error: ActivityError) -> bool:
        # A subagent's failed model activity also reaches task() as an
        # ActivityError; that is not a tool error and must still fail the run.
        return error.activity_type == INVOKE_TOOL

    def wrap_tool_call(
        self, request: ToolCallRequest, handler: Callable[[ToolCallRequest], Any]
    ) -> Any:
        self._before_call(request)
        try:
            result = handler(request)
        except ActivityError as error:
            if not self._is_tool_failure(error):
                raise
            return self._on_failure(request, error)
        self._on_result(request, result)
        return result

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[Any]],
    ) -> Any:
        self._before_call(request)
        try:
            result = await handler(request)
        except ActivityError as error:
            if not self._is_tool_failure(error):
                raise
            return self._on_failure(request, error)
        self._on_result(request, result)
        return result
