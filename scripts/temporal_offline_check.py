"""Offline validation of the Temporal host: no LLM key, no MCP network calls.

    uv run python scripts/temporal_offline_check.py

A message-aware fake model plays the supervisor and the anchor specialist, and
the Life Sciences MCP HTTP client is stubbed in-process. Every worker runs with
max_cached_workflows=0, so each workflow task replays the full history and any
nondeterminism in agent construction or middleware fails the run.

Scenarios:
  happy     supervisor -> task(anchor) -> think_tool -> hgnc tool -> write /workspace file -> done
  runaway   the anchor specialist calls tools forever; the per-subagent model
            call limit must stop it and hand control back to the supervisor
  crash     the worker is shut down mid-run and a fresh one finishes it; no
            completed model or tool call may run twice
"""

import asyncio
import os
import sys
import uuid
from collections import Counter
from dataclasses import replace
from datetime import timedelta
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from temporalio.api.enums.v1 import EventType
from temporalio.client import Client
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

import apps.temporal  # noqa: F401
from agent_factory import resolve_agent_config
from apps.temporal.durable import make_plugin
from apps.temporal.workflow import (
    LifesciencesResearchWorkflow,
    LoopLimits,
    ResearchInput,
)
from shared import mcp

MODEL_CALLS: Counter = Counter()
TOOL_CALLS: Counter = Counter()
TOOL_DELAY = {"seconds": 0.0}


class PolicyModel(BaseChatModel):
    """Chooses its reply from the conversation, so call order does not matter."""

    mode: str

    @property
    def _llm_type(self) -> str:
        return "policy-fake"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "PolicyModel":
        return self

    def _reply(self, messages: list[BaseMessage]) -> AIMessage:
        system = " ".join(
            str(m.content) for m in messages if isinstance(m, SystemMessage)
        )
        done = Counter(m.name for m in messages if isinstance(m, ToolMessage))
        call_id = f"call-{len(messages)}"
        if "Life Sciences Graph Builder Supervisor" in system:
            MODEL_CALLS["supervisor"] += 1
            if not done["task"]:
                return _call(call_id, "task", {
                    "subagent_type": "anchor_specialist",
                    "description": "Anchor NF1 and doxorubicin to CURIEs.",
                })
            if not done["write_file"]:
                return _call(call_id, "write_file", {
                    "file_path": "/workspace/report.md",
                    "content": "# NF1 report\nHGNC:7765",
                })
            return AIMessage(content="DONE: report written to /workspace/report.md")
        MODEL_CALLS["subagent"] += 1
        if self.mode == "happy" and not done["think_tool"]:
            # think_tool is sync and pure: it runs in the workflow, not as an activity.
            return _call(call_id, "think_tool", {"reflection": "Resolve NF1 first."})
        if self.mode == "runaway" or not done["hgnc_search_genes"]:
            return _call(call_id, "hgnc_search_genes", {"query": "NF1"})
        return AIMessage(content="Anchored NF1 -> HGNC:7765")

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=self._reply(messages))])

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        return self._generate(messages)


def _call(call_id: str, name: str, args: dict) -> AIMessage:
    return AIMessage(content="", tool_calls=[{"id": call_id, "name": name, "args": args}])


def model_provider(model_name: str) -> PolicyModel:
    return PolicyModel(mode=model_name.split(":", 1)[1])


async def fake_call_tool(tool_name: str, arguments: dict, apply_rate_limit: bool = True) -> str:
    TOOL_CALLS[tool_name] += 1
    await asyncio.sleep(TOOL_DELAY["seconds"])
    return f"{tool_name}: HGNC:7765 NF1 neurofibromin 1"


async def history(handle) -> Counter:
    counts: Counter = Counter()
    scheduled: dict[int, str] = {}
    async for e in handle.fetch_history_events():
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED:
            name = e.activity_task_scheduled_event_attributes.activity_type.name
            scheduled[e.event_id] = name
            counts[name] += 1
        elif e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_STARTED:
            # Attempts beyond the first: an activity that was in flight when its
            # worker died runs again (at-least-once), and history records it.
            attrs = e.activity_task_started_event_attributes
            counts[f"{scheduled[attrs.scheduled_event_id]}.extra_attempts"] += attrs.attempt - 1
        elif e.event_type == EventType.EVENT_TYPE_WORKFLOW_TASK_FAILED:
            counts["WORKFLOW_TASK_FAILED"] += 1
    return counts


def worker(client: Client, task_queue: str) -> Worker:
    return Worker(
        client,
        task_queue=task_queue,
        workflows=[LifesciencesResearchWorkflow],
        max_cached_workflows=0,
    )


def reset() -> None:
    MODEL_CALLS.clear()
    TOOL_CALLS.clear()


def report(name: str, result: Any, hist: Counter) -> None:
    print(f"\n[{name}]")
    print(f"  answer: {result.answer}")
    print(f"  workspace files: {sorted(result.workspace_files)}")
    print(f"  history: {dict(hist)}")
    print(f"  real model calls: {dict(MODEL_CALLS)}  real MCP calls: {dict(TOOL_CALLS)}")


async def run_once(client: Client, mode: str, limits: LoopLimits) -> tuple[Any, Counter]:
    reset()
    task_queue = f"lifesciences-check-{uuid.uuid4()}"
    config = replace(resolve_agent_config(), model_name=f"fake:{mode}")
    async with worker(client, task_queue):
        handle = await client.start_workflow(
            LifesciencesResearchWorkflow.run,
            ResearchInput(question="NF1 doxorubicin toxicity", config=config, limits=limits),
            id=task_queue,
            task_queue=task_queue,
            execution_timeout=timedelta(seconds=60),
        )
        result = await handle.result()
    return result, await history(handle)


async def crash(client: Client) -> tuple[Any, Counter]:
    reset()
    TOOL_DELAY["seconds"] = 0.3
    task_queue = f"lifesciences-crash-{uuid.uuid4()}"
    config = replace(resolve_agent_config(), model_name="fake:runaway")
    first = worker(client, task_queue)
    running = asyncio.create_task(first.run())
    handle = await client.start_workflow(
        LifesciencesResearchWorkflow.run,
        ResearchInput(
            question="NF1 doxorubicin toxicity",
            config=config,
            limits=LoopLimits(subagent_model_calls=8),
        ),
        id=task_queue,
        task_queue=task_queue,
        execution_timeout=timedelta(seconds=90),
    )
    while TOOL_CALLS["hgnc_search_genes"] < 3:
        await asyncio.sleep(0.05)
    await first.shutdown()
    await running
    print(f"\n[crash] first worker stopped after {dict(MODEL_CALLS)} model / {dict(TOOL_CALLS)} MCP calls")
    async with worker(client, task_queue):
        result = await handle.result()
    TOOL_DELAY["seconds"] = 0.0
    return result, await history(handle)


async def main() -> None:
    mcp.lifesciences_client.call_tool = fake_call_tool  # activities run in this process
    async with await WorkflowEnvironment.start_local() as env:
        client = await Client.connect(
            env.client.service_client.config.target_host,
            namespace=env.client.namespace,
            plugins=[make_plugin(model_provider=model_provider)],
        )

        result, hist = await run_once(client, "happy", LoopLimits())
        report("happy", result, hist)
        assert result.answer.startswith("DONE"), result.answer
        assert "/workspace/report.md" in result.workspace_files
        assert hist["deepagents.invoke_model"] == MODEL_CALLS.total() == 6, hist
        assert hist["deepagents.invoke_tool"] == TOOL_CALLS.total() == 1, hist
        assert hist["deepagents.backend_op"] > 0, "AGENTS.md/skills reads should be activities"
        assert hist["WORKFLOW_TASK_FAILED"] == 0, hist

        result, hist = await run_once(client, "runaway", LoopLimits(subagent_model_calls=6))
        report("runaway (subagent limit 6)", result, hist)
        assert MODEL_CALLS["subagent"] == 6, MODEL_CALLS
        assert result.answer.startswith("DONE"), result.answer
        assert hist["WORKFLOW_TASK_FAILED"] == 0, hist

        result, hist = await crash(client)
        report("crash (subagent limit 8)", result, hist)
        assert MODEL_CALLS["subagent"] == 8, MODEL_CALLS
        # Completed calls never re-run; only the attempt in flight at shutdown may.
        assert MODEL_CALLS.total() == (
            hist["deepagents.invoke_model"] + hist["deepagents.invoke_model.extra_attempts"]
        ), (hist, MODEL_CALLS)
        assert TOOL_CALLS.total() == (
            hist["deepagents.invoke_tool"] + hist["deepagents.invoke_tool.extra_attempts"]
        ), (hist, TOOL_CALLS)
        assert hist["deepagents.invoke_tool.extra_attempts"] + hist[
            "deepagents.invoke_model.extra_attempts"
        ] <= 1, hist

    print("\nall checks passed")


if __name__ == "__main__":
    asyncio.run(main())
