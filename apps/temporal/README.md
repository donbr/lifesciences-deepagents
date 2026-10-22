# Temporal host (spike)

Runs the same Deep Agents supervisor + 7 specialists as the LangGraph server
(`apps/api/agent_factory.py`) as a Temporal workflow, via
`temporalio-deepagents`. The agent loop runs in the workflow; every model call,
I/O tool call and persistent-filesystem operation is an activity. The
LangGraph host (`apps/api/lifesciences.py`, `langgraph.json`) is unchanged.

## Run

```bash
temporal server start-dev                                    # local dev server, localhost:7233
uv run python -m apps.temporal.worker                        # one or more workers
uv run python -m apps.temporal.start "<question>"            # prints the workflow id, then the answer
uv run python scripts/temporal_run_report.py <workflow-id> [--out DIR]   # cost/retry report from history
```

`start.py` sets no execution timeout: a run lasts until it completes or fails
(one question is ~25 minutes and a few dollars). Terminate a stuck run with
`temporal workflow terminate --workflow-id <id>`.

## Environment

| Variable | Default | Meaning |
|---|---|---|
| `TEMPORAL_ADDRESS` | `localhost:7233` | Temporal frontend (worker, starter, report script) |
| `TEMPORAL_PAYLOAD_S3_BUCKET` | unset (storage off) | Enables S3 External Storage for large payloads |
| `TEMPORAL_PAYLOAD_S3_ENDPOINT` | unset (real AWS S3) | Custom S3 endpoint; localhost only (moto/minio) today |
| `LIFESCIENCES_TEMPORAL_TRACE` | unset (tracing off) | `1` keeps LangSmith tracing on in the worker |
| `LIFESCIENCES_RUNTIME_ROOT` | `<repo>/.deepagents` | Filesystem root for the agent's persistent files |

## Payload size and External Storage

Storage is **off by default**, so Temporal's limits apply: 2 MB per payload and
50 MB per workflow history. One NF1 question produced ~8.45 MB of history.
Without storage, a tool result over 2 MB fails its activity and the agent gets
an error message instead of the result.

To turn it on:

- `uv sync --group external-storage` (installs `aioboto3`).
- Set `TEMPORAL_PAYLOAD_S3_BUCKET`; the bucket must already exist. Real S3 uses
  the normal AWS credential chain. A custom `TEMPORAL_PAYLOAD_S3_ENDPOINT` is
  rejected unless it is on localhost.
- The worker, the starter **and** the report script must all use the same
  storage settings, or they cannot decode each other's payloads.
- With storage on, the report script reads raw history payloads: for offloaded
  payloads, the sizes and fallback counts it shows are those of the stored
  references, not of the real content.

## Where files live

`runtime_root` is resolved on the **starter** (`resolve_agent_config`) and
passed to the workflow; the **worker's** filesystem activities use that path,
and large tool results are written to the worker's disk under it. Until that
changes, run the starter and all workers on the same host or on a shared
filesystem. `/workspace/` files live in agent state (workflow history) and are
returned in the result.

## Tracing

Off by default on the worker: under Temporal every model/tool activity becomes
its own LangSmith trace (hundreds per run). Temporal
history and `scripts/temporal_run_report.py` are the record of a run. Set
`LIFESCIENCES_TEMPORAL_TRACE=1` to trace anyway.

## Tool errors

- **Retryable** (timeouts, transport errors, HTTP 408/429/5xx, MCP stdio
  connection errors): retried by the activity, 3 attempts in all.
- **Permanent** (other HTTP 4xx, JSON-RPC errors, unparseable responses):
  fail the activity at once.
- Either way the final failure reaches the agent as an error `ToolMessage`
  with the curated `MCPCallError` text, and the run continues.
- **Fail-fast**: when one service has 3 consecutive calls that exhausted their
  retries on transient errors, the run fails with `MCPServiceUnavailable`
  (non-retryable), so it stops spending money on a dead endpoint. Permanent
  errors (usually a bad query from the agent) do not count; a success resets
  the count. `query_api_direct` is counted per URL host. See
  `tool_errors.py`.
- `persist_to_graphiti` raises a permanent error when Graphiti is
  unreachable (it used to return a success-like note); the graph stays in
  `/workspace/`.

## Model

The model is the alias `anthropic:claude-sonnet-4-5`
(`agent_factory.DEFAULT_MODEL`). Model activities retry up to 10 attempts
(5 s initial, x2 backoff, 60 s cap; a provider `retry-after` overrides).
**Sonnet 4.5 retires on 2026-11-30**: migrating to a newer model is an open
follow-up.
