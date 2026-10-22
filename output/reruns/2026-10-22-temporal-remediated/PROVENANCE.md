# NF1 doxorubicin rerun under Temporal after remediation (Tasks 2-6), 2026-10-22

Same question as `../2026-10-21-sonnet45/temporal-0.7/PROVENANCE.md` (default NF1 doxorubicin question). Code: branch
`spike/temporal-wrap`, commit `954755f` (includes the run-report cache fix `2cc381e`..`954755f`; the run itself used the
code as of `2cc381e`, the later commit only touches the report script and its test). Model `anthropic:claude-sonnet-4-5` (alias).
Local dev server, namespace `default`, no payload offload (`TEMPORAL_PAYLOAD_S3_BUCKET` unset), LangSmith tracing off.

| Item | Value | temporal-0.7 |
|---|---|---|
| Workflow | `lifesciences-3c228875-1d5e-44d7-a218-014e7f928642` | `lifesciences-1b1b5d83-...` |
| Started / duration | 2026-10-22T05:16:17Z, 32.3 min, no worker restart, 0 failed workflow tasks | 21.1 min |
| Model calls | 67 `deepagents.invoke_model` | 63 |
| Tool calls | 56 MCP tool activities, 20 filesystem `backend_op` | 71 MCP, 49 backend_op |
| Tokens | 1,283,842 in / 118,145 out | 1,203,641 in / 71,608 out |
| Prompt cache | 953,007 read (74.2% of input), 330,447 written | 0 read |
| Cost | ~$3.30 cache-aware; ~$5.62 at list price with no cache discount | ~$4.69 list |
| History | 847 events, 8.45 MB, largest payload 254 KB | 9.99 MB, 715 KB |
| Graph | 44 nodes / 56 edges (`files/graph.json`) | 39 / 52 |

Cost formula: uncached input x $3 + cache writes x $3.75 + cache reads x $0.30 + output x $15, per million
(`input_tokens` already includes cached tokens). Output is the largest component (118k tokens = $1.77).

## Acceptance

| Criterion | Result |
|---|---|
| Cache reads >= 70% of input tokens | PASS: 74.2% |
| Cache-aware cost <= $2.50 | MISS: $3.30 (output tokens 1.65x temporal-0.7; run was longer, 67 model calls) |
| Tool failures listed and explained; 0 error strings recorded as successes | PASS: see below; `status=error` results = 0 |
| History < 10 MB | PASS: 8.45 MB |
| LangSmith traces for the run = 0 | PASS: 0 runs in `lifesciences-deepagents` since 04:55Z (workflow started 05:16Z) |
| Output files under `/workspace/` (agent state) | PASS: 11 files in `workspace_files`, incl. `graph.json` and `report.md`; nothing new in `.deepagents/tmp/` |
| Graph vs run-1952 (25/33), run-2043 (43/68), temporal-0.7 (39/52) | 44 / 56 (recorded) |

Tool failures (4 final failures, 4 retried attempts, all surfaced as failed activities, none as success strings):
- `query_pubmed` x2, `MCPCallError`: `Stdio Connection Error calling pubmed_fetch_contents: ExceptionGroup` on
  `get_article_metadata` calls. Retryable, 3 attempts each (4 extra attempts). Cause is the same local PubMed stdio
  server fault seen in temporal-0.7 (there it was recorded as a success string; now it fails and retries). Not
  investigated further; the agent continued without those abstracts.
- `query_api_direct` x2, `MCPCallError`: `HTTP 400` from the Open Targets GraphQL API, `Cannot query field
  'knownDrugs' on type 'Target'`. Non-retryable, 1 attempt each. Explained: the agent wrote a query using a field
  the Open Targets v4 schema no longer has (agent error, not infrastructure).

## Files

`answer.md` is the workflow result; `files/` holds the 11 files in the result's `workspace_files` (agent state).
Report script output: `.superpowers/sdd/2026-10-21-temporal-spike-remediation/task-7-report-output.txt` (not committed).

## Known issues
- Cost target missed ($3.30 vs $2.50). Cache hits are healthy (74%), but 330k tokens were written to the cache
  (billed at $3.75/M) and output tokens are $1.77 alone.
- LangChain reports cache writes in `input_token_details.ephemeral_5m_input_tokens` with `cache_creation` = 0, so a
  naive sum shows no writes. The report script now counts them (first cache-aware figure, $3.05, undercounted).
- The worker log does not show the `LangSmith tracing: OFF` line (only sandbox import warnings); tracing-off is
  inferred from 0 LangSmith runs.
- `answer.md` opens with chat-style preamble ("Perfect! Now let me provide...") and emoji; it is the model's final message.
