"""Summarize one LifesciencesResearchWorkflow run from its Temporal history.

    uv run python scripts/temporal_run_report.py <workflow-id> [--out DIR]

Reports duration, history size, activity counts and retries, token usage (from
the usage_metadata on model activity results), tool failures and the graph.json
size. With --out, writes the answer and every /workspace/ file to DIR.

Tool failures: MCP clients raise ``MCPCallError``, so a failed tool call is a
failed ``deepagents.invoke_tool`` activity, not a result string. Per tool, the
report counts retried attempts (attempts beyond the first, whether the call
then succeeded or not) and final failures (ActivityTaskFailed / TimedOut
events: the call's last attempt failed, and the agent got a "Tool error (...)"
message or the run failed fast), broken down by error type. As a fallback it
also counts completed tool results whose ToolMessage has status "error" (a
tool that handles its own errors).
"""

import argparse
import asyncio
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from temporalio.api.enums.v1 import EventType
from temporalio.api.failure.v1 import Failure
from temporalio.api.history.v1 import HistoryEvent
from temporalio.client import Client

from apps.temporal.durable import make_plugin
from apps.temporal.storage import payload_storage_from_env
from apps.temporal.workflow import LifesciencesResearchWorkflow

INVOKE_TOOL = "deepagents.invoke_tool"
INVOKE_MODEL = "deepagents.invoke_model"
# Sonnet 4.5 list prices, USD per million tokens.
PRICE_IN, PRICE_OUT = 3.0, 15.0
# Prompt-cache prices: writes cost 1.25x input, reads 0.1x input.
PRICE_CACHE_WRITE, PRICE_CACHE_READ = 3.75, 0.30


def _payload_json(payloads: Any) -> list[Any]:
    out = []
    for p in payloads.payloads:
        try:
            out.append(json.loads(p.data))
        except ValueError:
            out.append(None)
    return out


def _find(obj: Any, key: str) -> list[Any]:
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                found.append(v)
            found.extend(_find(v, key))
    elif isinstance(obj, list):
        for v in obj:
            found.extend(_find(v, key))
    return found


def _failure_type(failure: Failure) -> str:
    if failure.HasField("application_failure_info"):
        return failure.application_failure_info.type or "ApplicationError"
    if failure.HasField("timeout_failure_info"):
        return "Timeout"
    if failure.HasField("canceled_failure_info"):
        return "Canceled"
    return "Failure"


@dataclass
class RunTally:
    """Counts from one workflow history; feed it every event in order."""

    events: int = 0
    history_bytes: int = 0
    largest_payload: int = 0
    activities: Counter = field(default_factory=Counter)
    extra_attempts: Counter = field(default_factory=Counter)  # by activity type
    failed: Counter = field(default_factory=Counter)  # by activity type
    tools: Counter = field(default_factory=Counter)  # tool activities, by tool
    tool_retries: Counter = field(default_factory=Counter)  # extra attempts, by tool
    tool_failures: Counter = field(default_factory=Counter)  # final failures, by tool
    tool_failure_types: Counter = field(default_factory=Counter)  # by "tool: type"
    tool_error_results: Counter = field(default_factory=Counter)  # status="error" results
    tokens_in: int = 0
    tokens_out: int = 0
    cache_read: int = 0  # subset of tokens_in served from the prompt cache
    cache_creation: int = 0  # subset of tokens_in written to the prompt cache
    workflow_failure: str | None = None
    _scheduled: dict[int, tuple[str, str]] = field(default_factory=dict)

    @property
    def cache_read_share(self) -> float:
        return self.cache_read / self.tokens_in if self.tokens_in else 0.0

    @property
    def list_cost(self) -> float:
        """USD at list price, ignoring the cache."""
        return self.tokens_in / 1e6 * PRICE_IN + self.tokens_out / 1e6 * PRICE_OUT

    @property
    def cache_aware_cost(self) -> float:
        """USD with cache pricing. input_tokens already includes cached tokens."""
        uncached = self.tokens_in - self.cache_read - self.cache_creation
        return (
            uncached * PRICE_IN
            + self.cache_creation * PRICE_CACHE_WRITE
            + self.cache_read * PRICE_CACHE_READ
            + self.tokens_out * PRICE_OUT
        ) / 1e6

    def add(self, e: HistoryEvent) -> None:
        self.events += 1
        self.history_bytes += e.ByteSize()
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED:
            a = e.activity_task_scheduled_event_attributes
            name = a.activity_type.name
            tool = ""
            if name == INVOKE_TOOL:
                tool = next(iter(_find(_payload_json(a.input), "tool_name")), "?")
                self.tools[tool] += 1
            self._scheduled[e.event_id] = (name, tool)
            self.activities[name] += 1
            self.largest_payload = max(self.largest_payload, a.input.ByteSize())
        elif e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_STARTED:
            a = e.activity_task_started_event_attributes
            name, tool = self._scheduled[a.scheduled_event_id]
            self.extra_attempts[name] += a.attempt - 1
            if name == INVOKE_TOOL and a.attempt > 1:
                self.tool_retries[tool] += a.attempt - 1
        elif e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED:
            a = e.activity_task_completed_event_attributes
            name, tool = self._scheduled[a.scheduled_event_id]
            self.largest_payload = max(self.largest_payload, a.result.ByteSize())
            body = _payload_json(a.result)
            if name == INVOKE_MODEL:
                for usage in _find(body, "usage_metadata"):
                    if isinstance(usage, dict):
                        self.tokens_in += usage.get("input_tokens", 0)
                        self.tokens_out += usage.get("output_tokens", 0)
                        details = usage.get("input_token_details") or {}
                        self.cache_read += details.get("cache_read", 0)
                        # Anthropic splits writes by TTL; LangChain then reports
                        # cache_creation=0 and puts them in ephemeral_*_input_tokens.
                        by_ttl = details.get("ephemeral_5m_input_tokens", 0) + details.get(
                            "ephemeral_1h_input_tokens", 0
                        )
                        self.cache_creation += max(details.get("cache_creation", 0), by_ttl)
            elif name == INVOKE_TOOL and "error" in _find(body, "status"):
                self.tool_error_results[tool] += 1
        elif e.event_type in (
            EventType.EVENT_TYPE_ACTIVITY_TASK_FAILED,
            EventType.EVENT_TYPE_ACTIVITY_TASK_TIMED_OUT,
        ):
            attrs = (
                e.activity_task_failed_event_attributes
                if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_FAILED
                else e.activity_task_timed_out_event_attributes
            )
            name, tool = self._scheduled[attrs.scheduled_event_id]
            self.failed[name] += 1
            if name == INVOKE_TOOL:
                self.tool_failures[tool] += 1
                self.tool_failure_types[f"{tool}: {_failure_type(attrs.failure)}"] += 1
        elif e.event_type == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_FAILED:
            failure = e.workflow_execution_failed_event_attributes.failure
            self.workflow_failure = f"{_failure_type(failure)}: {failure.message}"


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_id")
    parser.add_argument("--out")
    args = parser.parse_args()

    # Must match the worker's storage (TEMPORAL_PAYLOAD_S3_BUCKET) to decode payloads.
    async with payload_storage_from_env(os.environ) as converter:
        client = await Client.connect(
            os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
            plugins=[make_plugin(data_converter=converter)],
        )
        handle = client.get_workflow_handle(args.workflow_id)
        desc = await handle.describe()

        t = RunTally()
        async for e in handle.fetch_history_events():
            t.add(e)

        duration = (
            (desc.close_time - desc.start_time).total_seconds() / 60
            if desc.close_time
            else None
        )
        print(f"workflow: {args.workflow_id}  status: {desc.status.name}")
        if t.workflow_failure:
            print(f"workflow failure: {t.workflow_failure}")
        print(f"duration: {duration and round(duration, 1)} min")
        print(f"history: {t.events} events, {t.history_bytes / 1e6:.2f} MB; largest payload {t.largest_payload / 1e3:.0f} KB")
        print(f"activities: {dict(t.activities)}")
        print(f"extra attempts: {dict(+t.extra_attempts)}  failed/timed out: {dict(t.failed)}")
        print(f"tokens: in {t.tokens_in:,} out {t.tokens_out:,}  ~${t.list_cost:.2f} at list price, no cache discount (comparable to earlier runs)")
        print(
            f"cache: read {t.cache_read:,} ({t.cache_read_share:.1%} of input) "
            f"creation {t.cache_creation:,}  cache-aware cost ~${t.cache_aware_cost:.2f}"
        )
        print(f"MCP tool calls: {sum(t.tools.values())}  top: {t.tools.most_common(10)}")
        print(f"tool retried attempts: {dict(t.tool_retries)}")
        print(f"tool final failures (failed/timed out): {dict(t.tool_failures)}")
        print(f"tool failure types: {dict(t.tool_failure_types)}")
        print(f"tool results with status=error (fallback): {dict(t.tool_error_results)}")

        if desc.status.name != "COMPLETED":
            return
        result = await client.get_workflow_handle_for(
            LifesciencesResearchWorkflow.run, args.workflow_id
        ).result()
        graph = result.workspace_files.get("/workspace/graph.json")
        if graph:
            try:
                g = json.loads(graph)
                print(f"graph.json: {len(g.get('nodes', []))} nodes / {len(g.get('edges', []))} edges")
            except ValueError:
                print("graph.json: not valid JSON")
        print(f"workspace files: {sorted(result.workspace_files)}")
        if args.out:
            out = Path(args.out)
            (out / "files").mkdir(parents=True, exist_ok=True)
            (out / "answer.md").write_text(result.answer)
            for path, content in result.workspace_files.items():
                (out / "files" / Path(path).name).write_text(content)
            print(f"wrote {out}")


if __name__ == "__main__":
    asyncio.run(main())
