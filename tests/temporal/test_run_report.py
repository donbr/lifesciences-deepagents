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


async def test_counts_retries_final_failures_and_workflow_failure(client, fast_tool_retries):
    """A real offline run: a retried call that ends in a permanent error (not
    counted by fail-fast), then three calls that exhaust their 3 attempts."""
    FAKE_STATE.tool_script["string_search_proteins"] = [
        MCPCallError("HTTP 503 from MCP tool", service="string", retryable=True),
        MCPCallError("HTTP 400 from MCP tool", service="string", retryable=False),
        *[MCPCallError("HTTP 503 from MCP tool", service="string", retryable=True)] * 9,
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

    assert tally.tools == {"string_search_proteins": 4}
    assert tally.tool_retries == {"string_search_proteins": 1 + 3 * 2}
    assert tally.tool_failures == {"string_search_proteins": 4}
    assert tally.tool_failure_types == {"string_search_proteins: MCPCallError": 4}
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


def test_sums_cache_tokens_and_prices_them():
    """input_tokens includes cached tokens; cost discounts reads and surcharges writes."""
    tally = report.RunTally()
    for i, (inp, out, read, create) in enumerate([(1000, 100, 0, 600), (1000, 50, 600, 200)]):
        sid = 10 * i + 1
        tally.add(HistoryEvent(
            event_id=sid,
            event_type=EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED,
            activity_task_scheduled_event_attributes=ActivityTaskScheduledEventAttributes(
                activity_type=ActivityType(name="deepagents.invoke_model"),
                input=_payloads({}),
            ),
        ))
        tally.add(HistoryEvent(
            event_id=sid + 1,
            event_type=EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED,
            activity_task_completed_event_attributes=ActivityTaskCompletedEventAttributes(
                scheduled_event_id=sid,
                result=_payloads({"message": {"kwargs": {"usage_metadata": {
                    "input_tokens": inp,
                    "output_tokens": out,
                    "input_token_details": (
                        {"cache_read": read, "cache_creation": create}
                        if i == 0
                        # TTL-split form: cache_creation is 0, the write is in ephemeral_5m
                        else {"cache_read": read, "cache_creation": 0, "ephemeral_5m_input_tokens": create}
                    ),
                }}}}),
            ),
        ))
    assert (tally.tokens_in, tally.tokens_out) == (2000, 150)
    assert (tally.cache_read, tally.cache_creation) == (600, 800)
    assert tally.cache_read_share == pytest.approx(0.3)
    # uncached 600 * 3 + 800 * 3.75 + 600 * 0.30 + 150 * 15, per million
    assert tally.cache_aware_cost == pytest.approx((1800 + 3000 + 180 + 2250) / 1e6)
    assert tally.list_cost == pytest.approx((6000 + 2250) / 1e6)
