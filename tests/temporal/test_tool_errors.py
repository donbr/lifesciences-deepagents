"""Tool failures under Temporal: activity retries, error messages, per-service fail-fast.

Scripted MCPCallErrors are raised by the stub that replaces the lifesciences MCP
client, so they travel the same path as real ones: alias tool -> durable
wrapper -> deepagents.invoke_tool activity -> ToolFailureMiddleware.
"""

import anthropic
import httpx2
import pytest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from temporalio.exceptions import ActivityError, ApplicationError, RetryState

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from apps.temporal.tool_errors import ToolFailureMiddleware, service_for_tool
from apps.temporal.workflow import LoopLimits
from shared.mcp import MCPCallError

from .conftest import run_agent
from .fakes import FAKE_STATE, PolicyModel


def _permanent(n: int = 1) -> list[Exception]:
    return [
        MCPCallError("HTTP 400 from MCP tool: bad arguments", service="x", retryable=False)
        for _ in range(n)
    ]


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


async def test_dead_service_fails_fast(client):
    for tool in ("string_search_proteins", "string_get_interactions"):
        FAKE_STATE.tool_script[tool] = _permanent(10)
    error, hist = await run_agent(client, "string_loop", LoopLimits(), expect_failure=True)
    assert error.type == "MCPServiceUnavailable"
    assert error.non_retryable
    assert error.message == "MCP service string unavailable after 3 consecutive failures"
    assert hist["deepagents.invoke_tool"] == 3, hist
    assert hist["deepagents.invoke_tool.extra_attempts"] == 0, hist
    assert FAKE_STATE.tool_calls["string_search_proteins"] == 3
    # The first two failures reached the specialist as error messages.
    assert [s for s, _ in _results_seen("string_search_proteins")] == ["error"]
    assert PolicyModel.calls[-1]["tool_results"].count(
        ("string_search_proteins", "error",
         "Tool error (string_search_proteins): HTTP 400 from MCP tool: bad arguments")
    ) == 2
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_parallel_failures_count_deterministically(client):
    """Two specialists run in parallel and share one middleware instance.

    Every workflow task replays the full history (max_cached_workflows=0), so a
    failure count that depended on anything but history would diverge on
    replay and fail a workflow task with a nondeterminism error.

    The one task failure allowed is UNHANDLED_COMMAND: when the workflow tries
    to fail while the other branch's activity is completing, the server rejects
    the completion and the worker replays with the new event. It is timing
    dependent and says nothing about determinism.
    """
    FAKE_STATE.tool_script["string_search_proteins"] = _permanent(10)
    FAKE_STATE.tool_script["chembl_search_compounds"] = _permanent(10)
    error, hist = await run_agent(client, "parallel", LoopLimits(), expect_failure=True)
    assert hist["WORKFLOW_TASK_FAILED"] == hist["WORKFLOW_TASK_FAILED.UNHANDLED_COMMAND"], hist
    assert error.type == "MCPServiceUnavailable"
    assert error.message in {
        "MCP service string unavailable after 3 consecutive failures",
        "MCP service chembl unavailable after 3 consecutive failures",
    }
    dead_tool = "string_search_proteins" if " string " in error.message else "chembl_search_compounds"
    assert FAKE_STATE.tool_calls[dead_tool] == 3, FAKE_STATE.tool_calls
    assert set(FAKE_STATE.tool_calls) == {"string_search_proteins", "chembl_search_compounds"}
    # Both specialists ran; neither service passed the limit.
    assert all(1 <= n <= 3 for n in FAKE_STATE.tool_calls.values()), FAKE_STATE.tool_calls
    assert hist["deepagents.invoke_tool"] == FAKE_STATE.tool_calls.total(), hist


async def test_failure_counts_survive_worker_restart(client):
    """The worker dies after two failed calls, while the 3rd is in flight.

    The new worker rebuilds the count (2) from history; the retried 3rd call
    fails and stops the run. A reset count would allow two more calls.
    """
    FAKE_STATE.tool_script["string_search_proteins"] = _permanent(10)
    error, hist = await run_agent(
        client, "string_loop", LoopLimits(), crash_after_tool_calls=3, expect_failure=True
    )
    assert error.type == "MCPServiceUnavailable"
    assert error.message == "MCP service string unavailable after 3 consecutive failures"
    assert hist["deepagents.invoke_tool"] == 3, hist
    # The in-flight attempt ran again on the new worker (at-least-once).
    assert hist["deepagents.invoke_tool.extra_attempts"] == 1, hist
    assert FAKE_STATE.tool_calls["string_search_proteins"] == 4
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


# --- ToolFailureMiddleware unit tests -------------------------------------------


def _request(tool: str, call_id: str = "call-1") -> ToolCallRequest:
    return ToolCallRequest(
        tool_call={"name": tool, "args": {}, "id": call_id, "type": "tool_call"},
        tool=None,
        state={},
        runtime=None,
    )


def _activity_error(
    message: str = "bad arguments", activity_type: str = "deepagents.invoke_tool"
) -> ActivityError:
    error = ActivityError(
        "Activity task failed",
        scheduled_event_id=1,
        started_event_id=2,
        identity="worker",
        activity_type=activity_type,
        activity_id="1",
        retry_state=RetryState.NON_RETRYABLE_FAILURE,
    )
    error.__cause__ = ApplicationError(message, type="MCPCallError", non_retryable=True)
    return error


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


def test_service_for_tool():
    assert service_for_tool("string_search_proteins") == "string"
    assert service_for_tool("chembl_get_compound") == "chembl"
    # rate_limiter lumps these into "default"; fail-fast keeps them apart.
    assert service_for_tool("hgnc_search_genes") == "hgnc"
    assert service_for_tool("wikipathways_get_pathway") == "wikipathways"
    assert service_for_tool("query_pubmed") == "pubmed"
    assert service_for_tool("query_api_direct") == "query_api_direct"
