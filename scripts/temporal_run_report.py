"""Summarize one LifesciencesResearchWorkflow run from its Temporal history.

    uv run python scripts/temporal_run_report.py <workflow-id> [--out DIR]

Reports duration, history size, activity counts and retries, token usage (from
the usage_metadata on model activity results), MCP tool results that are error
strings (shared.mcp returns errors as text), and the graph.json size. With
--out, writes the answer and every /workspace/ file to DIR.
"""

import argparse
import asyncio
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from temporalio.api.enums.v1 import EventType
from temporalio.client import Client

from apps.temporal.durable import make_plugin
from apps.temporal.workflow import LifesciencesResearchWorkflow

ERROR_MARKERS = (
    "Error calling tool",
    "HTTP Connection Error",
    "Error from MCP server",
    "Stdio Connection Error",
    "No valid content found",
)
# Sonnet 4.5 list prices, USD per million tokens.
PRICE_IN, PRICE_OUT = 3.0, 15.0


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


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_id")
    parser.add_argument("--out")
    args = parser.parse_args()

    client = await Client.connect(
        os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"), plugins=[make_plugin()]
    )
    handle = client.get_workflow_handle(args.workflow_id)
    desc = await handle.describe()

    events = 0
    history_bytes = 0
    largest_payload = 0
    scheduled: dict[int, tuple[str, str]] = {}
    activities: Counter = Counter()
    extra_attempts: Counter = Counter()
    failed: Counter = Counter()
    tools: Counter = Counter()
    tool_errors: Counter = Counter()
    tokens_in = tokens_out = 0

    async for e in handle.fetch_history_events():
        events += 1
        history_bytes += e.ByteSize()
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED:
            a = e.activity_task_scheduled_event_attributes
            name = a.activity_type.name
            tool = ""
            if name == "deepagents.invoke_tool":
                tool = next(iter(_find(_payload_json(a.input), "tool_name")), "?")
                tools[tool] += 1
            scheduled[e.event_id] = (name, tool)
            activities[name] += 1
            largest_payload = max(largest_payload, a.input.ByteSize())
        elif e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_STARTED:
            a = e.activity_task_started_event_attributes
            extra_attempts[scheduled[a.scheduled_event_id][0]] += a.attempt - 1
        elif e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED:
            a = e.activity_task_completed_event_attributes
            name, tool = scheduled[a.scheduled_event_id]
            largest_payload = max(largest_payload, a.result.ByteSize())
            body = _payload_json(a.result)
            if name == "deepagents.invoke_model":
                for usage in _find(body, "usage_metadata"):
                    if isinstance(usage, dict):
                        tokens_in += usage.get("input_tokens", 0)
                        tokens_out += usage.get("output_tokens", 0)
            elif name == "deepagents.invoke_tool":
                text = json.dumps(body)
                if any(m in text for m in ERROR_MARKERS):
                    tool_errors[tool] += 1
        elif e.event_type in (
            EventType.EVENT_TYPE_ACTIVITY_TASK_FAILED,
            EventType.EVENT_TYPE_ACTIVITY_TASK_TIMED_OUT,
        ):
            attrs = (
                e.activity_task_failed_event_attributes
                if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_FAILED
                else e.activity_task_timed_out_event_attributes
            )
            failed[scheduled[attrs.scheduled_event_id][0]] += 1

    duration = (
        (desc.close_time - desc.start_time).total_seconds() / 60
        if desc.close_time
        else None
    )
    print(f"workflow: {args.workflow_id}  status: {desc.status.name}")
    print(f"duration: {duration and round(duration, 1)} min")
    print(f"history: {events} events, {history_bytes / 1e6:.2f} MB; largest payload {largest_payload / 1e3:.0f} KB")
    print(f"activities: {dict(activities)}")
    print(f"extra attempts: {dict(+extra_attempts)}  failed/timed out: {dict(failed)}")
    cost = tokens_in / 1e6 * PRICE_IN + tokens_out / 1e6 * PRICE_OUT
    print(f"tokens: in {tokens_in:,} out {tokens_out:,}  ~${cost:.2f} at list price, no cache discount")
    print(f"MCP tool calls: {sum(tools.values())}  error-string results: {dict(tool_errors)}")
    print(f"top tools: {tools.most_common(10)}")

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
