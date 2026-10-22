"""Tool failures under Temporal: activity retries, error messages, per-service fail-fast.

Scripted MCPCallErrors are raised by the stub that replaces the lifesciences MCP
client, so they travel the same path as real ones: alias tool -> durable
wrapper -> deepagents.invoke_tool activity -> ToolFailureMiddleware.
"""

import anthropic
import httpx
import httpx2
import pytest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from temporalio.exceptions import ActivityError, ApplicationError, RetryState

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from apps.temporal.tool_errors import ToolFailureMiddleware, service_for_tool
from apps.temporal.workflow import LoopLimits
from shared.mcp import HTTPMCPClient, MCPCallError

from .conftest import run_agent
from .fakes import FAKE_STATE, PolicyModel


def _permanent(n: int = 1) -> list[Exception]:
    return [
        MCPCallError("HTTP 400 from MCP tool: bad arguments", service="x", retryable=False)
        for _ in range(n)
    ]


def _transient(n: int) -> list[Exception]:
    """``n`` failed attempts; a call uses 3 (TOOL_ACTIVITY_OPTIONS) before it fails."""
    return [
        MCPCallError("HTTP 503 from MCP tool: unavailable", service="x", retryable=True)
        for _ in range(n)
    ]


TRANSIENT_TEXT = "HTTP 503 from MCP tool: unavailable"


def _results_seen(tool: str) -> list[tuple[str, str]]:
    """(status, content) of every result for ``tool`` that a model call saw, in order."""
    seen: list[tuple[str, str]] = []
    for call in PolicyModel.calls:
        for name, status, content in call["tool_results"]:
            if name == tool and (status, content) not in seen:
                seen.append((status, content))
    return seen


# --- Workflow tests ------------------------------------------------------------


async def test_transient_error_is_retried(client):
    FAKE_STATE.tool_script["hgnc_search_genes"] = [
        MCPCallError("HTTP 503 from MCP tool", service="default", retryable=True),
        "ok",
    ]
    result, hist = await run_agent(client, "happy", LoopLimits())
    assert result.answer.startswith("DONE"), result.answer
    assert hist["deepagents.invoke_tool"] == 1, hist
    assert hist["deepagents.invoke_tool.extra_attempts"] == 1, hist
    assert FAKE_STATE.tool_calls["hgnc_search_genes"] == 2
    assert _results_seen("hgnc_search_genes") == [("success", "ok")]
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_permanent_error_reaches_agent_once(client):
    FAKE_STATE.tool_script["hgnc_search_genes"] = _permanent()
    result, hist = await run_agent(client, "happy", LoopLimits())
    assert result.answer.startswith("DONE"), result.answer
    assert hist["deepagents.invoke_tool"] == 1, hist
    assert hist["deepagents.invoke_tool.extra_attempts"] == 0, hist
    assert FAKE_STATE.tool_calls["hgnc_search_genes"] == 1
    assert _results_seen("hgnc_search_genes") == [
        ("error", "Tool error (hgnc_search_genes): HTTP 400 from MCP tool: bad arguments")
    ]
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def _real_client_error(handler) -> MCPCallError:
    """The exception the real HTTP client raises: chained ``from`` the httpx error."""
    mcp_client = HTTPMCPClient("https://mcp.test/mcp", transport=httpx.MockTransport(handler))
    with pytest.raises(MCPCallError) as err:
        await mcp_client.call_tool("hgnc_search_genes", {"query": "NF1"}, apply_rate_limit=False)
    assert isinstance(err.value.__cause__, httpx.HTTPError)
    return err.value


def _timeout(request):
    raise httpx.ReadTimeout("timed out", request=request)


@pytest.mark.parametrize(
    "handler, attempts, curated",
    [
        pytest.param(
            lambda r: httpx.Response(400, json={"detail": "query must be a gene symbol"}),
            1,
            'HTTP 400 from MCP tool hgnc_search_genes: {"detail":"query must be a gene symbol"}',
            id="permanent",
        ),
        pytest.param(
            _timeout,
            3,
            "ReadTimeout calling MCP tool hgnc_search_genes: timed out",
            id="retryable-exhausted",
        ),
    ],
)
async def test_agent_sees_curated_text_of_chained_error(client, handler, attempts, curated):
    """Temporal keeps the __cause__ chain; the agent must get the MCPCallError
    text, not the httpx exception underneath it."""
    FAKE_STATE.tool_script["hgnc_search_genes"] = [
        await _real_client_error(handler) for _ in range(attempts)
    ]
    result, hist = await run_agent(client, "happy", LoopLimits())
    assert result.answer.startswith("DONE"), result.answer
    assert FAKE_STATE.tool_calls["hgnc_search_genes"] == attempts
    assert _results_seen("hgnc_search_genes") == [
        ("error", f"Tool error (hgnc_search_genes): {curated}")
    ]


async def test_dead_service_fails_fast(client, fast_tool_retries):
    """Three calls in a row exhaust their retries on transient errors: stop the run."""
    for tool in ("string_search_proteins", "string_get_interactions"):
        FAKE_STATE.tool_script[tool] = _transient(30)
    error, hist = await run_agent(client, "string_loop", LoopLimits(), expect_failure=True)
    assert error.type == "MCPServiceUnavailable"
    assert error.non_retryable
    assert error.message == "MCP service string unavailable after 3 consecutive failures"
    assert hist["deepagents.invoke_tool"] == 3, hist
    assert hist["deepagents.invoke_tool.extra_attempts"] == 6, hist
    assert FAKE_STATE.tool_calls["string_search_proteins"] == 9
    # The first two failures reached the specialist as error messages.
    assert [s for s, _ in _results_seen("string_search_proteins")] == ["error"]
    assert PolicyModel.calls[-1]["tool_results"].count(
        ("string_search_proteins", "error", f"Tool error (string_search_proteins): {TRANSIENT_TEXT}")
    ) == 2
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_permanent_failures_do_not_stop_the_run(client):
    """An error the agent caused (HTTP 400, invalid params) says nothing about the
    service being down: it reaches the agent, but never counts toward fail-fast."""
    FAKE_STATE.tool_script["string_search_proteins"] = _permanent(3)
    result, hist = await run_agent(client, "string_loop", LoopLimits())
    assert result.answer.startswith("DONE"), result.answer
    assert hist["deepagents.invoke_tool"] == 4, hist
    assert hist["deepagents.invoke_tool.extra_attempts"] == 0, hist
    assert FAKE_STATE.tool_calls["string_search_proteins"] == 4
    last = [c for c in PolicyModel.calls if c["role"] == "subagent"][-1]["tool_results"]
    assert [s for n, s, _ in last if n == "string_search_proteins"] == [
        "error", "error", "error", "success"
    ]
    assert last.count(
        ("string_search_proteins", "error",
         "Tool error (string_search_proteins): HTTP 400 from MCP tool: bad arguments")
    ) == 3
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_parallel_failures_count_deterministically(client, fast_tool_retries):
    """Two specialists fail on the same service in parallel; one shared count stops the run.

    The supervisor runs anchor_specialist and traversal_drugs_specialist at
    once; both loop on chembl_search_compounds, which always fails.

    Determinism rests on the WORKFLOW_TASK_FAILED cause assertion: every
    workflow task replays the full history (max_cached_workflows=0), so a
    count that depended on anything but history would fail a task with a
    nondeterminism error. The only cause allowed is UNHANDLED_COMMAND: the
    workflow tried to fail while the other branch's activity was completing,
    and the worker replayed with the new event. That depends on timing and
    says nothing about determinism.

    Why the activity count is 3 or 4, not exactly 3: each branch has at most
    one chembl call in flight. When the 3rd failure (from either branch) hits
    the limit, the other branch may already have scheduled its next call, so
    one extra activity can exist. It cannot add to the count: the run has
    already failed. The 0.2s tool delay makes both branches' first calls
    overlap, so both feed the one count.

    Each call exhausts its 3 attempts (2 extra per counted call); attempts of
    a possible 4th call add to that before the run closes.
    """
    FAKE_STATE.tool_delay = 0.2
    FAKE_STATE.tool_script["chembl_search_compounds"] = _transient(60)
    error, hist = await run_agent(client, "parallel", LoopLimits(), expect_failure=True)
    assert hist["WORKFLOW_TASK_FAILED"] == hist["WORKFLOW_TASK_FAILED.UNHANDLED_COMMAND"], hist
    assert error.type == "MCPServiceUnavailable"
    assert error.message == "MCP service chembl unavailable after 3 consecutive failures"
    assert set(FAKE_STATE.tool_calls) == {"chembl_search_compounds"}, FAKE_STATE.tool_calls
    assert hist["deepagents.invoke_tool"] in (3, 4), hist
    assert 6 <= hist["deepagents.invoke_tool.extra_attempts"] <= 8, hist
    # Both branches contributed calls to the one chembl count.
    queries = {args["query"] for _, args in FAKE_STATE.tool_args}
    assert queries == {
        "Anchor NF1. Use chembl_search_compounds.",
        "Drugs for NF1. Use chembl_search_compounds.",
    }, FAKE_STATE.tool_args


async def test_failure_counts_survive_worker_restart(client, fast_tool_retries):
    """The worker dies after two failed calls, while the 3rd call's first attempt
    is in flight.

    Each failed call is 3 attempts, so the crash comes at attempt 7. The new
    worker rebuilds the count (2) from history; the 3rd call's remaining
    attempts fail and stop the run. A reset count would allow two more calls.
    """
    FAKE_STATE.tool_script["string_search_proteins"] = _transient(30)
    error, hist = await run_agent(
        client, "string_loop", LoopLimits(), crash_after_tool_calls=7, expect_failure=True
    )
    assert error.type == "MCPServiceUnavailable"
    assert error.message == "MCP service string unavailable after 3 consecutive failures"
    assert hist["deepagents.invoke_tool"] == 3, hist
    # The interrupted attempt counts as one of the 3rd call's 3 attempts; the
    # new worker runs the other two (at-least-once).
    assert hist["deepagents.invoke_tool.extra_attempts"] == 6, hist
    assert FAKE_STATE.tool_calls["string_search_proteins"] == 9
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_model_rate_limit_is_retried(client):
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
    FAKE_STATE.model_script["supervisor"] = [
        anthropic.RateLimitError(
            "rate limited",
            # retry-after-ms becomes the activity's next retry delay.
            response=httpx2.Response(429, headers={"retry-after-ms": "10"}, request=request),
            body=None,
        )
    ]
    result, hist = await run_agent(client, "happy", LoopLimits())
    assert FAKE_STATE.model_script["supervisor"] == [], "the 429 was never raised"
    assert result.answer.startswith("DONE"), result.answer
    assert hist["deepagents.invoke_model.extra_attempts"] == 1, hist
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


@pytest.mark.parametrize("overloads", [2, 9])
async def test_model_overload_is_retried(client, overloads):
    """A sustained 529 must not end a long run: up to 10 attempts per model call."""
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
    FAKE_STATE.model_script["supervisor"] = [
        anthropic.OverloadedError(
            "overloaded",
            response=httpx2.Response(529, headers={"retry-after-ms": "10"}, request=request),
            body=None,
        )
        for _ in range(overloads)
    ]
    result, hist = await run_agent(client, "happy", LoopLimits())
    assert FAKE_STATE.model_script["supervisor"] == [], "not every 529 was raised"
    assert result.answer.startswith("DONE"), result.answer
    assert hist["deepagents.invoke_model.extra_attempts"] == overloads, hist
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


# --- ToolFailureMiddleware unit tests -------------------------------------------


def _request(tool: str, call_id: str = "call-1", args: dict | None = None) -> ToolCallRequest:
    return ToolCallRequest(
        tool_call={"name": tool, "args": args or {}, "id": call_id, "type": "tool_call"},
        tool=None,
        state={},
        runtime=None,
    )


def _activity_error(
    message: str = "bad arguments",
    activity_type: str = "deepagents.invoke_tool",
    retry_state: RetryState = RetryState.MAXIMUM_ATTEMPTS_REACHED,
) -> ActivityError:
    """A failed tool activity. The default retried transient errors until it ran
    out of attempts; NON_RETRYABLE_FAILURE is a permanent (agent-caused) error."""
    error = ActivityError(
        "Activity task failed",
        scheduled_event_id=1,
        started_event_id=2,
        identity="worker",
        activity_type=activity_type,
        activity_id="1",
        retry_state=retry_state,
    )
    error.__cause__ = ApplicationError(
        message,
        type="MCPCallError",
        non_retryable=retry_state == RetryState.NON_RETRYABLE_FAILURE,
    )
    return error


def _permanent_error(message: str = "bad arguments") -> ActivityError:
    return _activity_error(message, retry_state=RetryState.NON_RETRYABLE_FAILURE)


def _ok(request: ToolCallRequest) -> ToolMessage:
    return ToolMessage(content="ok", tool_call_id=request.tool_call["id"])


def _failing(error: Exception):
    def handler(request):
        raise error

    return handler


def _async(handler):
    async def ahandler(request):
        return handler(request)

    return ahandler


async def test_middleware_turns_tool_activity_error_into_error_message():
    middleware = ToolFailureMiddleware()
    message = await middleware.awrap_tool_call(
        _request("string_search_proteins"), _async(_failing(_activity_error()))
    )
    assert isinstance(message, ToolMessage)
    assert message.status == "error"
    assert message.name == "string_search_proteins"
    assert message.tool_call_id == "call-1"
    assert message.content == "Tool error (string_search_proteins): bad arguments"


async def test_middleware_fails_fast_per_service_and_resets_on_success():
    middleware = ToolFailureMiddleware(max_consecutive_failures=3)
    fail = _async(_failing(_activity_error()))
    await middleware.awrap_tool_call(_request("string_search_proteins"), fail)
    await middleware.awrap_tool_call(_request("string_get_interactions"), fail)
    # A success for the service resets its count; other services are separate.
    await middleware.awrap_tool_call(_request("string_search_proteins"), _async(_ok))
    await middleware.awrap_tool_call(_request("chembl_get_compound"), fail)
    await middleware.awrap_tool_call(_request("chembl_get_compound"), fail)
    await middleware.awrap_tool_call(_request("string_search_proteins"), fail)
    await middleware.awrap_tool_call(_request("string_search_proteins"), fail)
    with pytest.raises(ApplicationError) as err:
        await middleware.awrap_tool_call(_request("string_get_interactions"), fail)
    assert err.value.type == "MCPServiceUnavailable"
    assert err.value.non_retryable
    assert err.value.message == "MCP service string unavailable after 3 consecutive failures"


async def test_middleware_stays_tripped_with_the_same_message():
    """After the limit, a racing failure and any new call for the service raise
    the same error; the handler of a new call never runs."""
    middleware = ToolFailureMiddleware(max_consecutive_failures=2)
    fail = _async(_failing(_activity_error()))
    await middleware.awrap_tool_call(_request("chembl_get_compound"), fail)
    messages = set()
    for _ in range(2):  # the tripping failure, then one already in flight
        with pytest.raises(ApplicationError) as err:
            await middleware.awrap_tool_call(_request("chembl_get_compound"), fail)
        messages.add(err.value.message)
    assert messages == {"MCP service chembl unavailable after 2 consecutive failures"}

    async def must_not_run(request):
        raise AssertionError("a tripped service must not be called")

    with pytest.raises(ApplicationError, match="chembl unavailable after 2"):
        await middleware.awrap_tool_call(_request("chembl_search_compounds"), must_not_run)
    # Other services are unaffected.
    ok = await middleware.awrap_tool_call(_request("string_search_proteins"), _async(_ok))
    assert ok.content == "ok"


def test_middleware_sync_path_matches_async():
    middleware = ToolFailureMiddleware(max_consecutive_failures=2)
    fail = _failing(_activity_error())
    message = middleware.wrap_tool_call(_request("string_search_proteins"), fail)
    assert message.status == "error"
    with pytest.raises(ApplicationError, match="MCP service string unavailable after 2"):
        middleware.wrap_tool_call(_request("string_search_proteins"), fail)


async def test_middleware_leaves_other_errors_alone():
    """Only a failed tool activity is a tool error; a subagent's failed model
    activity surfacing through task() must still fail the run."""
    middleware = ToolFailureMiddleware()
    model_error = _activity_error(activity_type="deepagents.invoke_model")
    with pytest.raises(ActivityError):
        await middleware.awrap_tool_call(_request("task"), _async(_failing(model_error)))
    with pytest.raises(ValueError):
        await middleware.awrap_tool_call(
            _request("string_search_proteins"), _async(_failing(ValueError("bug")))
        )


@pytest.mark.parametrize(
    "retry_state", [RetryState.MAXIMUM_ATTEMPTS_REACHED, RetryState.TIMEOUT]
)
async def test_middleware_counts_failures_that_exhausted_retries(retry_state):
    middleware = ToolFailureMiddleware(max_consecutive_failures=1)
    with pytest.raises(ApplicationError, match="string unavailable after 1"):
        await middleware.awrap_tool_call(
            _request("string_search_proteins"),
            _async(_failing(_activity_error(retry_state=retry_state))),
        )


async def test_middleware_permanent_failures_neither_count_nor_reset():
    """A permanent failure still reaches the agent as an error message, but it
    neither adds to the service's count nor clears it (it is no evidence that
    the service is up or down)."""
    middleware = ToolFailureMiddleware(max_consecutive_failures=2)
    exhausted = _async(_failing(_activity_error()))
    permanent = _async(_failing(_permanent_error()))
    await middleware.awrap_tool_call(_request("string_search_proteins"), exhausted)
    for _ in range(5):
        message = await middleware.awrap_tool_call(_request("string_search_proteins"), permanent)
        assert message.status == "error"
        assert message.content == "Tool error (string_search_proteins): bad arguments"
    with pytest.raises(ApplicationError, match="string unavailable after 2"):
        await middleware.awrap_tool_call(_request("string_get_interactions"), exhausted)


def test_middleware_permanent_failures_sync_path():
    middleware = ToolFailureMiddleware(max_consecutive_failures=1)
    message = middleware.wrap_tool_call(
        _request("string_search_proteins"), _failing(_permanent_error())
    )
    assert message.status == "error"


OPEN_TARGETS = "https://api.platform.opentargets.org/api/v4/graphql"
HGNC_REST = "https://rest.genenames.org/fetch/symbol/NF1"


async def test_query_api_direct_hosts_do_not_share_a_count():
    middleware = ToolFailureMiddleware(max_consecutive_failures=2)
    fail = _async(_failing(_activity_error()))
    open_targets = _request("query_api_direct", args={"url": OPEN_TARGETS, "method": "POST"})
    hgnc = _request("query_api_direct", args={"url": HGNC_REST})
    await middleware.awrap_tool_call(open_targets, fail)
    message = await middleware.awrap_tool_call(hgnc, fail)
    assert message.status == "error"  # one failure per host: neither is tripped
    with pytest.raises(
        ApplicationError,
        match="query_api_direct:api.platform.opentargets.org unavailable after 2",
    ):
        await middleware.awrap_tool_call(open_targets, fail)
    ok = await middleware.awrap_tool_call(hgnc, _async(_ok))
    assert ok.content == "ok"


def test_service_for_query_api_direct_is_keyed_by_host():
    assert (
        service_for_tool("query_api_direct", {"url": OPEN_TARGETS})
        == "query_api_direct:api.platform.opentargets.org"
    )
    assert (
        service_for_tool("query_api_direct", {"url": "https://REST.genenames.org:443/x"})
        == "query_api_direct:rest.genenames.org"
    )
    # No usable URL: one shared fallback key.
    assert service_for_tool("query_api_direct") == "query_api_direct"
    assert service_for_tool("query_api_direct", {}) == "query_api_direct"
    assert service_for_tool("query_api_direct", {"url": "not a url"}) == "query_api_direct"
    assert service_for_tool("query_api_direct", {"url": "http://[::1"}) == "query_api_direct"
    assert service_for_tool("query_api_direct", {"url": 42}) == "query_api_direct"
    # Only query_api_direct looks at its arguments.
    assert service_for_tool("hgnc_search_genes", {"url": OPEN_TARGETS}) == "hgnc"


def test_service_for_tool():
    assert service_for_tool("string_search_proteins") == "string"
    assert service_for_tool("chembl_get_compound") == "chembl"
    # rate_limiter lumps these into "default"; fail-fast keeps them apart.
    assert service_for_tool("hgnc_search_genes") == "hgnc"
    assert service_for_tool("wikipathways_get_pathway") == "wikipathways"
    assert service_for_tool("query_pubmed") == "pubmed"
    assert service_for_tool("query_api_direct") == "query_api_direct"
