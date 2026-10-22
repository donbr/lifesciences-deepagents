# NF1 doxorubicin rerun under Temporal (spike), 2026-10-21

Same question as `../PROVENANCE.md`. Code: branch `spike/temporal-wrap` (worktree), uncommitted, based on
`1782cd3`. Changes from that commit: deepagents 0.3.12 -> 0.7.30 (forced by `temporalio-deepagents` 0.0.3),
agent definition split into `apps/api/agent_factory.py`, Temporal host in `apps/temporal/`.

| Item | Value |
|---|---|
| Workflow | `lifesciences-1b1b5d83-551e-4c55-8f90-d0fc4724a51a` (local dev server, namespace `default`) |
| Started / duration | 2026-10-22T03:06:52Z, 21.1 min (includes one worker restart, see below) |
| Model calls | 63 `deepagents.invoke_model` activities |
| Tool calls | 71 MCP tool activities, 49 filesystem `backend_op` activities, 0 failed, 0 retried |
| Tokens | 1,203,641 in / 71,608 out, **0 cache reads** |
| Cost | ~$4.69 at list price (no cache discount applies; see Known issues) |
| History | 1,057 events, 9.99 MB, largest payload 715 KB |
| Graph | 39 nodes / 52 edges (`files/graph.json`) |

Files: `answer.md` is the workflow result; `files/` holds what the agent wrote. The agent wrote to
`/tmp/workspace/`, not `/workspace/`, so the files went through the filesystem backend to
`.deepagents/tmp/workspace/` on disk instead of agent state; they were copied here from there.

Known issues:
- Prompt caching is off under the plugin. `AnthropicPromptCachingMiddleware` only applies to `ChatAnthropic`
  instances (`langchain_anthropic/middleware/prompt_caching.py:118`) and deepagents sets it to ignore other
  models; the plugin's `TemporalModel` is not one. run-1952 read 1,720,862 of 1,978,672 prompt tokens from cache.
- `think_tool` (sync) failed the first workflow tasks (`NotImplementedError` from `run_in_executor` in the
  workflow loop). Fixed by giving it a coroutine; the worker was restarted and the run resumed from history at
  event 137 without repeating completed model or tool calls.
- Two tool results were error strings recorded as successes, so no retry ran: `query_pubmed`
  (`Stdio Connection Error`) and `persist_to_graphiti` (`400 Bad Request` from `localhost:8002/mcp`; nothing
  was written to Graphiti).
- deepagents 0.7 no longer adds `write_todos`; the 0.3 runs spent 36-41 tool calls on it.
- LangSmith: the run produced ~250 separate traces (one per activity, plus the in-workflow graph) instead of one.
