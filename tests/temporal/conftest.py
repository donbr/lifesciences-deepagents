import asyncio
import uuid
from collections import Counter
from dataclasses import replace
from datetime import timedelta

import pytest
import pytest_asyncio
from temporalio.api.enums.v1 import EventType
from temporalio.client import Client
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from agent_factory import resolve_agent_config
from apps.temporal.durable import make_plugin
from apps.temporal.workflow import (
    LifesciencesResearchWorkflow,
    LoopLimits,
    ResearchInput,
    ResearchResult,
)
from shared import mcp

from .fakes import FAKE_STATE, PolicyModel, fake_call_tool, reset_fakes


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def env():
    async with await WorkflowEnvironment.start_local() as environment:
        yield environment


@pytest_asyncio.fixture
async def client(env, monkeypatch):
    reset_fakes()
    monkeypatch.setattr(mcp.lifesciences_client, "call_tool", fake_call_tool)
    return await Client.connect(
        env.client.service_client.config.target_host,
        namespace=env.client.namespace,
        plugins=[make_plugin(model_provider=lambda name: PolicyModel(mode=name.split(":", 1)[1]))],
    )


async def _history(handle) -> Counter:
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


def _worker(client: Client, task_queue: str) -> Worker:
    return Worker(
        client,
        task_queue=task_queue,
        workflows=[LifesciencesResearchWorkflow],
        max_cached_workflows=0,
    )


async def run_agent(
    client: Client,
    mode: str,
    limits: LoopLimits,
    *,
    crash_after_tool_calls: int | None = None,
    model_name: str | None = None,
) -> tuple[ResearchResult, Counter]:
    """Run the workflow to completion; return its result and history counts.

    With crash_after_tool_calls, the worker is shut down once that many real
    tool calls have happened and a fresh worker finishes the run. model_name
    overrides the default ``anthropic:<mode>``; the fake provider parses the
    mode from the part after ':'.
    """
    task_queue = f"lifesciences-test-{uuid.uuid4()}"
    config = replace(resolve_agent_config(), model_name=model_name or f"anthropic:{mode}")
    request = ResearchInput(question="NF1 doxorubicin toxicity", config=config, limits=limits)
    if crash_after_tool_calls is None:
        async with _worker(client, task_queue):
            handle = await client.start_workflow(
                LifesciencesResearchWorkflow.run,
                request,
                id=task_queue,
                task_queue=task_queue,
                execution_timeout=timedelta(seconds=60),
            )
            result = await handle.result()
        return result, await _history(handle)

    FAKE_STATE.tool_delay = 0.3
    first = _worker(client, task_queue)
    running = asyncio.create_task(first.run())
    handle = await client.start_workflow(
        LifesciencesResearchWorkflow.run,
        request,
        id=task_queue,
        task_queue=task_queue,
        execution_timeout=timedelta(seconds=90),
    )
    while sum(FAKE_STATE.tool_calls.values()) < crash_after_tool_calls:
        await asyncio.sleep(0.05)
    await first.shutdown()
    await running
    async with _worker(client, task_queue):
        result = await handle.result()
    FAKE_STATE.tool_delay = 0.0
    return result, await _history(handle)
