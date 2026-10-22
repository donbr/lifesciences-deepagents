"""How a failed tool activity reaches the agent under Temporal.

An I/O tool runs as a ``deepagents.invoke_tool`` activity. A transient failure
is retried by the activity's retry policy; a permanent failure, or a transient
one that exhausts its retries, surfaces in the workflow as ``ActivityError``.
LangGraph's ToolNode re-raises that, which would abort the whole run, so
``ToolFailureMiddleware`` turns it into an error ``ToolMessage`` the agent can
react to, and stops the run once one service has failed several times in a row.

The failure counts live on the middleware instance, which the workflow builds
inside ``run``. They are therefore rebuilt from history on every replay: a
crashed or evicted worker resumes with the same counts, never with zeros.
"""

from collections import Counter
from collections.abc import Awaitable, Callable
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware, ToolCallRequest
from langchain_core.messages import ToolMessage
from temporalio.deepagents._activity import INVOKE_TOOL
from temporalio.exceptions import ActivityError, ApplicationError, FailureError

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from shared.mcp import LIFESCIENCES_ALIAS_TOOL_NAMES, rate_limiter


def service_for_tool(tool_name: str) -> str:
    """The upstream service a tool depends on, for counting failures.

    Starts from ``rate_limiter.get_service_from_tool`` (the service an
    ``MCPCallError`` names), but splits its catch-all ``"default"`` bucket:
    an HGNC outage says nothing about WikiPathways.
    """
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

    Use one instance per workflow run, shared by the supervisor and every
    specialist, so failures of one service count across agents.
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

    def _before_call(self, request: ToolCallRequest) -> None:
        # Once tripped, a service stays down for the rest of the run: no new
        # calls to it, only the same error.
        service = service_for_tool(request.tool_call["name"])
        if self._tripped(service):
            raise self._unavailable(service)

    def _on_result(self, request: ToolCallRequest, result: Any) -> None:
        # An error message here never reached the service (e.g. ToolNode
        # rejected the arguments), so it is not evidence the service is up.
        if isinstance(result, ToolMessage) and result.status == "error":
            return
        service = service_for_tool(request.tool_call["name"])
        if not self._tripped(service):
            self._failures.pop(service, None)

    def _on_failure(self, request: ToolCallRequest, error: ActivityError) -> ToolMessage:
        name = request.tool_call["name"]
        service = service_for_tool(name)
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
