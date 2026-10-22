# Temporal Spike Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Temporal-hosted Life Sciences agent cost-competitive and failure-honest: prompt caching on, tool errors visible and retried, one LangSmith trace per run, bounded history, then re-baseline.

**Architecture:** Fixes live in the Temporal host (`apps/temporal/`) wherever possible, so the LangGraph-server host keeps working. The one shared change is the tool error contract in `apps/api/shared/mcp.py`: MCP calls raise a typed error; each host decides how errors reach the agent (LangGraph: error `ToolMessage`; Temporal: retried activity, then error `ToolMessage`, then fail-fast per service).

**Tech Stack:** Python 3.13 via uv, temporalio 1.34, temporalio-deepagents 0.0.3, deepagents 0.7.30, langchain 1.4 / langchain-anthropic 1.7.6, pytest + pytest-asyncio, httpx `MockTransport`.

**Spec:** `output/reruns/2026-10-21-sonnet45/temporal-0.7/PROVENANCE.md` (Known issues) and commit `c92a142`. Priorities below come from the measured run: 63 model calls, 1.20M input tokens, 0 cache reads, ~$4.69; run-1952 read 87% of prompt tokens from cache for $2.75.

## Outcome (2026-10-22)

All 7 tasks done and reviewed (branch `spike/temporal-wrap`, draft PR #11). Deviations from the text below, as ruled
during execution: Task 4 took its Step 5 fallback (tracing off on the worker) because `temporalio-langsmith` 0.1.0
caps `langsmith<0.13` while deepagents 0.7 needs `>=0.14.11`; Task 3's fail-fast was changed in the final review to
count only retry-exhausted transient failures (permanent errors neither count nor reset; `query_api_direct` keyed by
host; HTTP 408 retryable); Task 5's acceptance dropped the full-3-MiB-in-context check (deepagents 0.7 evicts large
results); Task 6 decisions below; `persist_to_graphiti` now raises on failure instead of returning a success string.
Task 7: cache reads 74.2% (pass), cost $3.30 vs $2.50 (missed). Results:
`output/reruns/2026-10-22-temporal-remediated/PROVENANCE.md`.

## Priorities

| P | Task | Why this order |
|---|---|---|
| 0 | 1. pytest harness | Every later task is TDD against the offline environment; today's checks are a script |
| 1 | 2. Prompt caching | Largest, cheapest win: ~55-60% cost cut estimated; one-class fix behind a confirmed data path |
| 1 | 3. Tool error contract | Correctness: failures recorded as successes, retries inert, dead endpoints burn whole runs ($2.91 on 2026-10-21) |
| 2 | 4. LangSmith trace consolidation | ~250 traces per run vs 1; blocks batch use on a trace quota |
| 3 | 5. History size via External Storage | 9.99 MB on one question; 50 MB is a hard stop; longer questions will cross it |
| 3 | 6. deepagents 0.7 parity decisions | Behavior drift from the upgrade (no `write_todos`, files under `/tmp/workspace/`); needs Don's call |
| 4 | 7. Re-baseline real run | Acceptance for 2-6; ~$2 expected |
| — | Deferred: `persist_to_graphiti` | Never worked from this app (400: no MCP session handshake); idempotency needed under at-least-once before enabling |

## Global Constraints

- `temporalio-deepagents` 0.0.3 requires `deepagents>=0.7,<0.8`, `langchain>=1.3.14,<2`, `langsmith>=0.10.9,<0.15`.
- `temporalio-langsmith` 0.1.0 requires `langsmith>=0.7.34,<0.13` (conflicts with the installed 0.14.12).
- Default model stays Sonnet 4.5 (`agent_factory.DEFAULT_MODEL`; switched to the alias `anthropic:claude-sonnet-4-5` in Task 6).
- `langgraph.json` → `./apps/api/lifesciences.py:graph` must keep building; `agent_factory` stays free of Temporal imports.
- No workflow code may do I/O, read env, or read the clock (resolve in `resolve_agent_config` / activities).
- Live tests are opt-in markers and must state their cost; default `uv run pytest` makes no network calls.
- Never commit `.env`; `.deepagents/tmp/` and `.deepagents/large_tool_results/` stay uncommitted.

## Review Focus

1. Parallel `task()` calls (drugs + trials in one supervisor message) whose tools fail at the same time: per-service failure counters must stay deterministic on replay — test in Task 3.
2. A non-Anthropic model name (`openai:gpt-4o`, which the file comments still mention): caching must silently not apply, not break the call — test in Task 2.
3. A single tool result larger than Temporal's 2 MB payload limit (largest seen: 715 KB): must not fail the workflow once External Storage is on — test in Task 5.
4. Anthropic 429/overloaded mid-run: the model activity must retry with backoff and the run continue — test in Task 3 (model provider raising once).
5. Worker restart while a run is mid-specialist: caching and error middleware state must rebuild from history (no double-counted failures) — test in Task 3 using the crash scenario.

---

### Task 1: pytest harness for the offline environment

**Files:**
- Create: `tests/__init__.py`, `tests/temporal/__init__.py`, `tests/temporal/conftest.py`, `tests/temporal/fakes.py`, `tests/temporal/test_agent_workflow.py`
- Modify: `pyproject.toml` (dev group + pytest config)
- Delete: `scripts/temporal_offline_check.py` (scenarios move into tests)

**Interfaces:**
- Produces (in `tests/temporal/fakes.py`): `PolicyModel(mode: str)` — the existing message-aware fake, plus `PolicyModel.calls: ClassVar[list[dict]]` recording each `_agenerate` call as `{"role": "supervisor"|"subagent", "kwargs": dict}`; `fake_call_tool(tool_name, arguments, apply_rate_limit=True) -> str`; `FAKE_STATE` with `tool_calls: Counter`, `tool_delay: float`, `tool_script: dict[str, list[Exception | str]]` (per-tool scripted outcomes, consumed in order, default success); `reset_fakes() -> None`.
- Produces (in `conftest.py`): session fixture `env` (`WorkflowEnvironment.start_local()`), function fixture `client` (plugin = `make_plugin(model_provider=lambda name: PolicyModel(mode=name.split(":",1)[1]))`, fakes reset, `shared.mcp.lifesciences_client.call_tool` monkeypatched to `fake_call_tool`), helper `run_agent(client, mode: str, limits: LoopLimits, *, crash_after_tool_calls: int | None = None) -> tuple[ResearchResult, Counter]` returning history counts keyed by activity type plus `"<type>.extra_attempts"` and `"WORKFLOW_TASK_FAILED"`. Workers use `max_cached_workflows=0`.

- [x] **Step 1: Add dev deps and config** — `uv add --dev pytest pytest-asyncio`; in `pyproject.toml` add `[tool.pytest.ini_options]` with `asyncio_mode = "auto"`, `markers = ["live: calls Anthropic (states cost)", "live_langsmith: writes to LangSmith"]`, `addopts = "-m 'not live and not live_langsmith'"`.
- [x] **Step 2: Port the three scenarios as tests** — `test_happy_path`, `test_runaway_specialist_is_capped`, `test_crash_does_not_repeat_completed_calls`, with the exact assertions from `scripts/temporal_offline_check.py` at `c92a142` (happy: `invoke_model == 6`, `invoke_tool == 1`, `backend_op > 0`, `"/workspace/report.md" in workspace_files`; runaway with `subagent_model_calls=6`: 6 subagent calls, answer starts with `DONE`; crash with limit 8: 8 subagent calls, real calls == scheduled + extra attempts, extra attempts ≤ 1).
- [x] **Step 3: Run** — `uv run pytest tests/temporal -q` → `3 passed`.
- [x] **Step 4: Delete the script, run again, commit** — `git commit -m "test: port Temporal offline checks to pytest"`.

---

### Task 2: Prompt caching under the plugin

**Files:**
- Create: `apps/temporal/caching.py`, `tests/temporal/test_caching.py`
- Modify: `apps/temporal/workflow.py` (add the middleware to supervisor and specialists)

**Interfaces:**
- Consumes: `PolicyModel.calls` (Task 1).
- Produces: `class TemporalAnthropicPromptCachingMiddleware(AnthropicPromptCachingMiddleware)` with `_should_apply_caching(self, request: ModelRequest) -> bool` returning `True` when `request.model` is a `TemporalModel` whose `.model` starts with `"anthropic:"`, else delegating to `super()`. Constructed with `unsupported_model_behavior="ignore"`.

Data path (verified): middleware sets `model_settings["cache_control"]` → `create_agent` calls `model.bind_tools(tools, **model_settings)` (`langchain/agents/factory.py:1478`) → `TemporalModel` forwards JSON-able kwargs as `ModelActivityInput.bind_kwargs` → activity calls `model.bind(**bind_kwargs)` on the real `ChatAnthropic` (`temporalio/deepagents/_activity.py:_build_bound_model`). Only the `isinstance(request.model, ChatAnthropic)` gate (`langchain_anthropic/middleware/prompt_caching.py:118`) blocks it today.

- [x] **Step 1: Failing tests**

```python
async def test_cache_control_reaches_every_model_activity(client):
    await run_agent(client, "happy", LoopLimits())
    assert PolicyModel.calls, "no model calls recorded"
    for call in PolicyModel.calls:
        assert call["kwargs"].get("cache_control", {}).get("type") == "ephemeral", call["role"]

async def test_non_anthropic_model_gets_no_cache_control(client):
    await run_agent(client, "happy", LoopLimits(), model_name="openai:happy")
    assert all("cache_control" not in c["kwargs"] for c in PolicyModel.calls)
```

(`run_agent` gains `model_name: str | None = None`, overriding `AgentConfig.model_name`; `PolicyModel` mode parsing uses the part after `:`.)
- [x] **Step 2: Run** — `uv run pytest tests/temporal/test_caching.py -q` → first test FAILS (`cache_control` missing).
- [x] **Step 3: Implement the middleware; append one instance per agent in `workflow.py`** (supervisor list and the per-specialist factory).
- [x] **Step 4: Run** — both pass; full suite still `passed`.
- [x] **Step 5: Live check (marker `live`, cost < $0.05)** — `test_live_second_call_reads_cache`: run the plugin's `invoke_model` activity twice via `ActivityEnvironment` with `model_name=DEFAULT_MODEL`, a system prompt of ≥ 2,048 tokens (repeat `supervisor_prompt("2026-10-21")` until long enough) and `bind_kwargs={"cache_control": {"type": "ephemeral"}}`; assert the second result's `usage_metadata["input_token_details"]["cache_read"] > 0`. Run: `uv run pytest -m live tests/temporal/test_caching.py -q`.
- [x] **Step 6: Commit** — `git commit -m "fix: enable Anthropic prompt caching under the Temporal plugin"`.

---

### Task 3: Tool error contract, retries and per-service fail-fast

**Files:**
- Modify: `apps/api/shared/mcp.py` (raise instead of returning error text), `apps/api/agent_factory.py` (`all_tools`)
- Create: `apps/temporal/tool_errors.py`, `tests/test_mcp_errors.py`, `tests/temporal/test_tool_errors.py`
- Modify: `apps/temporal/durable.py`, `apps/temporal/workflow.py`

**Interfaces:**
- Produces (`shared/mcp.py`): `class MCPCallError(ToolException)` with `__init__(self, message: str, *, service: str, retryable: bool)`. `HTTPMCPClient.call_tool` returns `str` on success and raises `MCPCallError`: `retryable=True` for `httpx.TimeoutException`, `httpx.TransportError`, HTTP 429 and 5xx; `retryable=False` for other 4xx, a JSON-RPC `"error"` in the body, and unparseable bodies (today's "No valid content found"). `StdioMCPClient.call_tool` raises `MCPCallError(retryable=True)` on connection/session errors. `query_api_direct` follows the HTTP rules. `service` = `rate_limiter.get_service_from_tool(tool_name)`.
- Produces (`agent_factory.py`): `all_tools(*, errors_as_content: bool = True) -> dict[str, Any]`. With `True` (LangGraph host) each I/O tool is a copy with `handle_tool_error=True`, so the agent gets a `ToolMessage(status="error")` as before, now marked as an error. The Temporal host passes `False`.
- Produces (`durable.py`): I/O tools are wrapped before `tool_as_activity` so `MCPCallError(retryable=False)` becomes `ApplicationError(str(e), type="MCPCallError", non_retryable=True)` inside the activity; retryable errors propagate and use `TOOL_ACTIVITY_OPTIONS` (3 attempts).
- Produces (`tests/temporal/fakes.py`): two more `PolicyModel` modes — `"string_loop"` (specialist calls `string_search_proteins` until it receives a non-error result, max 10) and `"parallel"` (supervisor's first reply is two `task()` calls, `expansion_specialist` and `traversal_drugs_specialist`, in one message; both specialists behave like `"string_loop"`).
- Produces (`tool_errors.py`): `class ToolFailureMiddleware(AgentMiddleware)` with `__init__(self, max_consecutive_failures: int = 3)` and `awrap_tool_call(request, handler)`: on `ActivityError` returns `ToolMessage(content=f"Tool error ({name}): {root cause message}", tool_call_id=..., status="error")` and increments the failure count for the tool's service; any success for that service resets it; reaching the limit raises `ApplicationError(f"MCP service {service} unavailable after {n} consecutive failures", type="MCPServiceUnavailable", non_retryable=True)`. One instance per workflow run, shared by the supervisor and all specialists.

- [x] **Step 1: Failing unit tests for classification** (`tests/test_mcp_errors.py`, `httpx.MockTransport`): `test_500_is_retryable`, `test_429_is_retryable`, `test_timeout_is_retryable`, `test_400_is_not_retryable`, `test_jsonrpc_error_is_not_retryable` (body `data: {"jsonrpc":"2.0","error":{"code":-32603,"message":"x"}}`), `test_success_returns_text`. Each asserts `pytest.raises(MCPCallError)` and `.retryable`/`.service`, or the returned string.
- [x] **Step 2: Run** — fail (functions return strings). **Step 3: Implement `MCPCallError` and the client changes. Step 4: Run** — pass.
- [x] **Step 5: Failing LangGraph-host test** — `test_langgraph_host_turns_error_into_error_toolmessage`: `all_tools()["hgnc_search_genes"].ainvoke({...}, tool_call_id)` with the client raising `MCPCallError(retryable=False)` returns a `ToolMessage` with `status == "error"` and no exception.
- [x] **Step 6: Failing workflow tests** (`tests/temporal/test_tool_errors.py`, using `FAKE_STATE.tool_script`):
  - `test_transient_error_is_retried`: `hgnc_search_genes` → `[MCPCallError(retryable=True), "ok"]`; assert `invoke_tool.extra_attempts == 1`, run completes, no error `ToolMessage` reached the agent.
  - `test_permanent_error_reaches_agent_once`: `[MCPCallError(retryable=False)]`; assert `invoke_tool.extra_attempts == 0`, the specialist's next model call sees a `ToolMessage` with `status == "error"`, run completes.
  - `test_dead_service_fails_fast`: every `string_*` call non-retryable, specialist mode that calls `string_search_proteins` repeatedly; assert the workflow fails with `ApplicationError` type `MCPServiceUnavailable` after exactly 3 tool activities.
  - `test_parallel_failures_count_deterministically` (Review Focus 1): supervisor issues two `task()` calls in one message whose specialists both hit failing `string_*` tools; with `max_cached_workflows=0` there are no `WORKFLOW_TASK_FAILED` events and the failure is raised once.
  - `test_failure_counts_survive_worker_restart` (Review Focus 5): crash after 2 failing calls; the restarted worker raises `MCPServiceUnavailable` on the 3rd, not the 5th.
  - `test_model_rate_limit_is_retried` (Review Focus 4): provider raises `anthropic.RateLimitError` once for the first supervisor call; assert `invoke_model.extra_attempts == 1` and the run completes.
- [x] **Step 7: Run** — fail. **Step 8: Implement `durable.py` wrapping, `ToolFailureMiddleware`, wire into `workflow.py`. Step 9: Run full suite** — pass.
- [x] **Step 10: Commit** — `git commit -m "fix: typed MCP errors with activity retries and per-service fail-fast"`.

---

### Task 4: One LangSmith trace per run

**Files:**
- Modify: `pyproject.toml` (`langsmith>=0.10.9,<0.13`, add `temporalio-langsmith>=0.1.0`), `apps/temporal/durable.py`
- Create: `tests/temporal/test_tracing.py`

**Interfaces:**
- Produces: `make_plugins(**deepagents_kwargs) -> list[Plugin]` replacing `make_plugin` at call sites (`worker.py`, `start.py`, `scripts/temporal_run_report.py`, tests): returns `[LangSmithPlugin(), DeepAgentsPlugin(...)]` when env `LANGSMITH_TRACING` is `"true"` (read in the worker/starter process, never in workflow code), else `[DeepAgentsPlugin(...)]`. Keep `make_plugin` as the DeepAgents-only builder it calls.

- [ ] (skipped: unsatisfiable dependency, see Outcome) **Step 1: Pin and resolve** — `uv add "langsmith>=0.10.9,<0.13" "temporalio-langsmith>=0.1.0"`; full offline suite must still pass. If resolution fails, stop and record why in the plan; fall back to Step 5.
- [ ] (skipped: unsatisfiable dependency, see Outcome) **Step 2: Failing live test (marker `live_langsmith`, no Anthropic cost)** — `test_happy_run_is_one_trace`: set `LANGSMITH_PROJECT=lifesciences-temporal-test-<uuid4>`, `LANGSMITH_TRACING=true`, run the fake `happy` scenario through `make_plugins`, flush the client, then assert via `langsmith.Client().list_runs(project_name=..., is_root=True)` that there is exactly 1 root run and that the count of `run_type == "llm"` runs equals the history's `invoke_model` count (6). Delete the project afterwards.
- [ ] (skipped: unsatisfiable dependency, see Outcome) **Step 3: Run** — `uv run pytest -m live_langsmith -q` → FAIL (many roots) before wiring.
- [ ] (skipped: unsatisfiable dependency, see Outcome) **Step 4: Implement `make_plugins`; run** — pass.
- [x] **Step 5 (fallback if Steps 1 or 4 fail):** `worker.py` forces `os.environ["LANGSMITH_TRACING"] = "false"` before connecting unless `LIFESCIENCES_TEMPORAL_TRACE=1`; document in `apps/temporal/workflow.py` docstring that Temporal history is the trace of record.
- [x] **Step 6: Commit** — `git commit -m "feat: consolidate LangSmith tracing for Temporal runs"`.

---

### Task 5: Bound history size with External Storage

**Files:**
- Modify: `apps/temporal/durable.py`, `pyproject.toml` (group `external-storage`: `aioboto3>=15.1.0,<15.2`, `moto[server]>=4.0.0`)
- Create: `apps/temporal/storage.py`, `tests/temporal/test_external_storage.py`

**Interfaces:**
- Produces: `async def payload_storage(endpoint: str | None, bucket: str) -> AsyncContextManager[DataConverter | None]` building `replace(DataConverter.default, external_storage=ExternalStorage(drivers=[S3StorageDriver(...)]))` as in `temporal-samples-python/deepagents_plugin/external_storage/client.py`; `make_plugin(data_converter=...)` passes it to `DeepAgentsPlugin(data_converter=...)`. Enabled when env `TEMPORAL_PAYLOAD_S3_BUCKET` is set (read host-side).

- [x] **Step 1: Failing test** — `test_large_tool_result_is_offloaded` (Review Focus 3): moto S3 server fixture on a free port; `hgnc_search_genes` scripted to return 3 MiB of text; assert the run completes, the specialist's next model input contains the full 3 MiB result, and the total history byte size (sum of `event.ByteSize()`) is < 1 MB.
- [x] **Step 2: Run** — FAIL (payload too large / history size). **Step 3: Implement. Step 4: Run** — pass; offline suite unchanged when the env var is unset.
- [x] **Step 5: Commit** — `git commit -m "feat: optional S3 external storage for large agent payloads"`.

---

### Task 6: deepagents 0.7 parity decisions (gated on Don)

Decide before implementing; each choice has a structural test.

- **6a. `write_todos`.** deepagents 0.7 no longer adds `TodoListMiddleware`; the 0.3 runs used it 36-41 times per run. Options: (A) leave it out (fewer calls, unknown quality effect); (B) add `TodoListMiddleware()` to the supervisor in `build_lifesciences_agent`. If B: `test_supervisor_has_write_todos` asserts `"write_todos"` is in the built agent's tool node (`agent.nodes["tools"].bound.tools_by_name`).
- **6b. Output location.** The 0.7 run wrote to `/tmp/workspace/` (filesystem backend, on disk); 0.3 wrote to the `/workspace/` state route. Options: (A) make `/workspace/` explicit in `PERSIST_SYSTEM` and the supervisor prompt; (B) route `/tmp/` to `StateBackend` as well. Test either way: `test_persist_files_land_in_workspace_state` with a fake persistence specialist writing `/tmp/workspace/graph.json` and `/workspace/graph.json`, asserting where each lands.
**Decisions (2026-10-21):**
- **6a = A (leave `write_todos` out).** Rationale: it is the deepagents 0.7 default and means fewer model calls; revisit after Task 7. Guard: `test_supervisor_has_no_write_todos`.
- **6b = A via absolute `/workspace/` prompt paths** (no backend routing change). Root cause: every path in `shared/prompts.py` was relative (`workspace/...`); 0.3 resolved these into the `/workspace/` state route, 0.7 made the model write `/tmp/workspace/...`, which fell through to the on-disk `FilesystemBackend`. Tests: `test_prompt_workspace_paths_are_absolute`, `test_workspace_writes_land_in_agent_state`.
- **Model = alias `anthropic:claude-sonnet-4-5`** (same snapshot as `-20250929`; "latest stable 4.5").
- **Follow-up:** migrate to `claude-sonnet-5-5` before 2026-11-30, when Sonnet 4.5 retires (anthropic SDK deprecation table).

- [x] **Step 1: Record decisions in this file (above). Step 2: TDD each chosen option as above. Step 3: Commit.**

---

### Task 7: Re-baseline the real run

**Files:**
- Create: `output/reruns/<date>-temporal-remediated/` (answer, files, `PROVENANCE.md`)

- [x] **Step 1: Run** — dev server, `uv run python -m apps.temporal.worker`, `uv run python -m apps.temporal.start`; then `uv run python scripts/temporal_run_report.py <id> --out output/reruns/<date>-temporal-remediated`.
- [x] **Step 2: Acceptance** (report output): cache reads ≥ 70% of input tokens; cost ≤ $2.50; error-string tool results with success status = 0; failed/extra attempts listed and each explained; history < 10 MB (or offloaded); LangSmith roots for the run = 1 (if Task 4 landed); graph node/edge counts recorded against run-1952 (25/33), run-2043 (43/68), temporal-0.7 (39/52).
- [x] **Step 3: Write `PROVENANCE.md` in the same format as `temporal-0.7/PROVENANCE.md`; commit.**
