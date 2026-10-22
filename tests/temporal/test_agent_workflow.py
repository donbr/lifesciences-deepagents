"""Offline validation of the Temporal host: no LLM key, no MCP network calls.

Every worker runs with max_cached_workflows=0, so each workflow task replays
the full history and any nondeterminism in agent construction or middleware
fails the run.
"""

from deepagents.backends import FilesystemBackend

from apps.temporal.workflow import LoopLimits

from .conftest import run_agent
from .fakes import FAKE_STATE, PolicyModel


def _real_model_calls(role: str | None = None) -> int:
    return sum(1 for c in PolicyModel.calls if role is None or c["role"] == role)


async def test_happy_path(client):
    """supervisor -> task(anchor) -> think_tool -> hgnc tool -> write /workspace file -> done"""
    result, hist = await run_agent(client, "happy", LoopLimits())
    assert result.answer.startswith("DONE"), result.answer
    assert "/workspace/report.md" in result.workspace_files
    assert hist["deepagents.invoke_model"] == _real_model_calls() == 6, hist
    assert hist["deepagents.invoke_tool"] == FAKE_STATE.tool_calls.total() == 1, hist
    assert hist["deepagents.backend_op"] > 0, "AGENTS.md/skills reads should be activities"
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_runaway_specialist_is_capped(client):
    """The per-subagent model call limit stops a specialist that calls tools forever."""
    result, hist = await run_agent(client, "runaway", LoopLimits(subagent_model_calls=6))
    assert _real_model_calls("subagent") == 6, PolicyModel.calls
    assert result.answer.startswith("DONE"), result.answer
    assert hist["WORKFLOW_TASK_FAILED"] == 0, hist


async def test_crash_does_not_repeat_completed_calls(client):
    """A worker shut down mid-run is replaced; no completed call may run twice."""
    result, hist = await run_agent(
        client, "runaway", LoopLimits(subagent_model_calls=8), crash_after_tool_calls=3
    )
    assert _real_model_calls("subagent") == 8, PolicyModel.calls
    # Completed calls never re-run; only the attempt in flight at shutdown may.
    assert _real_model_calls() == (
        hist["deepagents.invoke_model"] + hist["deepagents.invoke_model.extra_attempts"]
    ), (hist, PolicyModel.calls)
    assert FAKE_STATE.tool_calls.total() == (
        hist["deepagents.invoke_tool"] + hist["deepagents.invoke_tool.extra_attempts"]
    ), (hist, FAKE_STATE.tool_calls)
    assert hist["deepagents.invoke_tool.extra_attempts"] + hist[
        "deepagents.invoke_model.extra_attempts"
    ] <= 1, hist


async def test_workspace_writes_land_in_agent_state(client, monkeypatch):
    """/workspace/ writes (here by the supervisor) stay in agent state, not a backend activity."""
    fs_writes: list[str] = []
    for name in ("write", "awrite"):
        original = getattr(FilesystemBackend, name)

        def spy(self, file_path, *a, _o=original, **kw):
            fs_writes.append(file_path)
            return _o(self, file_path, *a, **kw)

        monkeypatch.setattr(FilesystemBackend, name, spy)

    result, hist = await run_agent(client, "happy", LoopLimits())
    assert result.workspace_files["/workspace/graph.json"].startswith("{"), result.workspace_files
    assert "/workspace/report.md" in result.workspace_files
    assert not [p for p in fs_writes if "graph.json" in p or "report.md" in p], fs_writes
    assert hist["deepagents.backend_op"] > 0  # AGENTS.md/skills reads still cross the boundary
