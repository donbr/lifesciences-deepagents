"""scripts/temporal_run_report.py counts tool failures from history, not result strings."""

import importlib.util
import json
import uuid
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest
from temporalio.api.common.v1 import ActivityType, Payload, Payloads
from temporalio.api.enums.v1 import EventType
from temporalio.api.history.v1 import (
    ActivityTaskCompletedEventAttributes,
    ActivityTaskScheduledEventAttributes,
    ActivityTaskStartedEventAttributes,
    HistoryEvent,
)
from temporalio.client import WorkflowFailureError

from agent_factory import resolve_agent_config
from apps.temporal.workflow import LifesciencesResearchWorkflow, LoopLimits, ResearchInput
from shared.mcp import MCPCallError

from .conftest import _worker
from .fakes import FAKE_STATE

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "temporal_run_report.py"
_spec = importlib.util.spec_from_file_location("temporal_run_report", _SCRIPT)
report = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(report)


async def test_counts_retries_final_failures_and_workflow_failure(client):
    """A real offline run: one retried attempt, three final failures, fail-fast."""
    FAKE_STATE.tool_script["string_search_proteins"] = [
        MCPCallError("HTTP 503 from MCP tool", service="string", retryable=True),
        *[MCPCallError("HTTP 400 from MCP tool", service="string", retryable=False)] * 5,
    ]
    task_queue = f"lifesciences-test-{uuid.uuid4()}"
    config = replace(resolve_agent_config(), model_name="anthropic:string_loop")
    async with _worker(client, task_queue):
        handle = await client.start_workflow(
            LifesciencesResearchWorkflow.run,
            ResearchInput(question="NF1", config=config, limits=LoopLimits()),
            id=task_queue,
            task_queue=task_queue,
            execution_timeout=timedelta(seconds=60),
        )
        with pytest.raises(WorkflowFailureError):
            await handle.result()

    tally = report.RunTally()
    async for event in handle.fetch_history_events():
        tally.add(event)

    assert tally.tools == {"string_search_proteins": 3}
    assert tally.tool_retries == {"string_search_proteins": 1}
    assert tally.tool_failures == {"string_search_proteins": 3}
    assert tally.tool_failure_types == {"string_search_proteins: MCPCallError": 3}
    assert tally.tool_error_results == {}
    assert tally.workflow_failure == (
        "MCPServiceUnavailable: MCP service string unavailable after 3 consecutive failures"
    )


def _payloads(obj) -> Payloads:
    return Payloads(payloads=[Payload(data=json.dumps(obj).encode())])


def test_counts_completed_results_with_error_status():
    """Fallback: a tool that handled its own error completes with status="error"."""
    tally = report.RunTally()
    tally.add(HistoryEvent(
        event_id=5,
        event_type=EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED,
        activity_task_scheduled_event_attributes=ActivityTaskScheduledEventAttributes(
            activity_type=ActivityType(name="deepagents.invoke_tool"),
            input=_payloads({"tool_name": "hgnc_search_genes", "args": {}}),
        ),
    ))
    tally.add(HistoryEvent(
        event_id=6,
        event_type=EventType.EVENT_TYPE_ACTIVITY_TASK_STARTED,
        activity_task_started_event_attributes=ActivityTaskStartedEventAttributes(
            scheduled_event_id=5, attempt=1
        ),
    ))
    tally.add(HistoryEvent(
        event_id=7,
        event_type=EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED,
        activity_task_completed_event_attributes=ActivityTaskCompletedEventAttributes(
            scheduled_event_id=5,
            result=_payloads({"message": {"kwargs": {"content": "x", "status": "error"}}}),
        ),
    ))
    assert tally.tools == {"hgnc_search_genes": 1}
    assert tally.tool_error_results == {"hgnc_search_genes": 1}
    assert tally.tool_failures == {}
    assert tally.tool_retries == {}
