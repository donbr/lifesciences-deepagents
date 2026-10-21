# Sage deck rerun (NF1 case study): design

**Date:** 2026-10-21
**Owner:** Don
**Status:** Stage 1 run 2026-10-21 (see Run log); stage 2 not yet run

## Intent

The Sage BioNetworks collaboration deck
(`biosciences-program/docs/presentations/proposed-sage-collaboration-deck.pdf`, shared 2026-03-05)
presents a case study on page 8, "Doxorubicin Cardiotoxicity in NF1", based on a February 2026 run.
Don wants to rerun that question with this codebase and check whether the case study's claims still
hold. The rerun must be traceable: every new output records exactly what produced it, and the
February code and outputs stay untouched as the baseline.

Don is the reader. The question he answers with the results is: "Do the new results still support
what the deck says?"

**Guiding rule (Don): change as little as possible.** Every deviation from February is listed in
this document and recorded in the run's provenance.

## Scope

- **In:** the NF1 doxorubicin case study (deck page 8, claims C6–C10 below).
- **Deferred to a separate job:** deck page 7, "Production Results" (5 reports, 9.3/10 median,
  9.7/10 protocol execution, 0 hallucinations, 100% NCT verification). Those five questions (FOP,
  ARID1A, TP53, NGLY1, BMP) were run separately on 2026-02-07, most likely with Claude Code skills
  (commit `35870a2`; reports cite direct `curl` calls; reviewed on the 10-dimension /10 scale).
  They share no data with the NF1 run.

## Success

The bar is the case study's **headline claims**, not identical text. The model, the live databases
and the clinical trial landscape have all moved since February.

| # | Claim (deck page 8) | February source (`output/cqs/doxorubicin-nf1-toxicity/`) |
|---|---|---|
| C6 | KG: 18 nodes (11 genes, 3 compounds, 3 pathways, 2 diseases), 20 edges | `-knowledge-graph.json` |
| C7 | Three cardioprotective axes: TOP2B/dexrazoxane (L4), NRF2/KEAP1 (L2), MEK/selumetinib (L4) | `-report.md` |
| C8 | 8 Synapse datasets; 56% node coverage (10/18); 35% edge coverage (7/20); key datasets syn200548, syn44222814, syn61259950 | `-synapse-grounding.md` |
| C9 | 6 verified clinical trials; all 3 drugs FDA-approved | `-report.md`, `-quality-review.md` |
| C10 | Quality score 35/40 PASS | `-quality-review.md` |

The comparison records "holds", "differs" (with the new value) or "not produced" for each row.
Tolerances are Don's decision, to be set before the comparison is written (see Open decisions).

Known legacy inconsistency to note in the comparison, not fix: C6's node breakdown sums to 19
(11 + 3 + 3 + 2), not 18.

## Goals

- Rerun the NF1 question with the smallest possible change to the February code.
- Capture every new output with a provenance record.
- Produce one comparison of claims C6–C10 against the new results.

## Non-goals

- Improving the pipeline, prompts, skills or dependencies.
- Deck page 7 and anything else in the deck beyond C6–C10.
- Migrating to `biosciences-deepagents` or `biosciences-mcp`.

## Anti-goals (failure even if it technically works)

- Any edit to February outputs (`output/cqs/**`) or to February code beyond the three changes listed
  under "Code changes".
- A dependency upgrade: `uv.lock` must stay byte-identical to the baseline.
- A secret in the public repo: no `.env`, no key values; keys are identified by last 4 characters only.
- A result whose model, commit, endpoint or Graphiti namespace cannot be determined afterwards.

## Baseline

- Repo: `donbr/lifesciences-deepagents` (public). Working clone:
  `~/open-biosciences/lifesciences-deepagents`, on `main` at `568dfe0` (merge of PR #9, which put
  the February run history under version control). The clone is in the Open Biosciences VS Code
  workspace.
- Tag `568dfe0` as `baseline/2026-02-sage-deck` and push the tag.
- Known gap: the NF1 v1 folder was committed only on 2026-10-21 (`3193232`), so the exact code
  state that produced it in February is not recorded. `568dfe0` is the closest available and is
  accepted as the baseline (Don); the comparison states this.

## How it was made in February (as found)

1. **Stage 1, research (Fuzzy-to-Fact phases 1–6):** the LangGraph app, graph `lifesciences`
   (`langgraph.json` → `apps/api/lifesciences.py:graph`), served by `uv run langgraph dev` and
   driven from the web UI (assistant id `lifesciences`). Model `openai:gpt-4o` (default argument at
   `apps/api/lifesciences.py:228`; stamped in the NF1 v4 bioRxiv draft and the FOP retrospective).
   Tools come from `https://lifesciences-research.fastmcp.app/mcp`, authenticated with
   `BIOSCIENCES_API_KEY` (`apps/api/shared/mcp.py:192-197`). The agent's `/workspace/` is
   thread-scoped, so stage-1 output exists only in thread state and LangSmith.
   Graphiti persistence (`persist_to_graphiti`, `apps/api/shared/mcp.py:583-634`) targets
   `http://localhost:8000/mcp` (unchanged since the first commit). The local graphiti-docker
   Neo4j has February episodes for other questions but none for NF1 doxorubicin, so NF1 most
   likely did not persist.
2. **Stage 2, publication (report, KG JSON, Synapse grounding, quality review, bioRxiv draft):**
   the `lifesciences-publication-pipeline` skill in Claude Code (`.claude/skills/`), with the
   Synapse MCP server from `.mcp.json`. The model used was not recorded.

## The rerun

### Decided by Don

- **Model:** Claude Sonnet 4.5, `claude-sonnet-4-5-20250929`, for both stages. A deliberate change
  from February's stage-1 model (`gpt-4o`), recorded as such. Sonnet 4.5 is still active, the
  baseline lock supports it, and it was already used in this repo.
- **Billing and telemetry:** stage 1 uses the Anthropic API key in `.env` (fingerprint `…PwAA`), so
  it has full LangSmith telemetry. Stage 2 runs in Claude Code on Don's subscription (no
  `ANTHROPIC_API_KEY` exported). Rule: work that benefits from telemetry uses the API key;
  everything else uses the Claude Code subscription.
- **Graphiti:** stage 1 writes to the graphiti-docker MCP endpoint (`http://localhost:8002/mcp`,
  container `docker-graphiti-mcp-1`, Neo4j `docker-neo4j-1`), with the code's default group id
  `lifesciences-default` unchanged. That group does not exist yet. Provenance records the group id
  actually used (the agent may choose another).
- **Scope:** NF1 only; page 7 deferred.
- **Baseline:** `568dfe0`, with the drift noted.
- **Location:** the clone at `~/open-biosciences/lifesciences-deepagents`.

### Input (verbatim from the February run)

> What known genes or pathways are implicated in minimizing Doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?

Slug: `doxorubicin-nf1-toxicity`. Verified against the February LangGraph run state (`.langgraph_api/.langgraph_ops.pckl` in the legacy worktree): this exact string, capital D, was submitted 9 times. It is Paul Zamora's cq3 (`reference/competency_questions/competency-questions-paul.md:13`) with "for NF1" added. Stakeholder: Sasha Scott (Sage Bionetworks, NF-OSI); her pain points and the CQ16–CQ25 proposals are in the graphiti-docker groups `sasha-scott-research-2026` and `sage-cq-prioritized-2026` (2026-02-16).

### Code changes (the complete list)

On branch `chore/oct21-validation`, created from the baseline tag:

1. `apps/api/lifesciences.py:228`: default `model_name` `"openai:gpt-4o"` →
   `"anthropic:claude-sonnet-4-5-20250929"`.
2. `apps/api/shared/mcp.py:583`: `GRAPHITI_MCP_URL` `"http://localhost:8000/mcp"` →
   `"http://localhost:8002/mcp"` (no trailing slash: `/mcp/` returns a 307 redirect, which the app's httpx client does not follow).
3. `apps/api/shared/mcp.py:192`: `LIFESCIENCES_MCP_URL` `"https://lifesciences-research.fastmcp.app/mcp"` →
   `"https://biosciences-mcp.fastmcp.app/mcp"` (Don, 2026-10-21). Reason: the first rerun attempt (trace
   `01a15fe4-e931-72c0-92c3-150ff8669c63`) got `-32603 Server returned an error response` on every STRING and
   BioGRID call from the old endpoint, while the February NF1 run (trace `019c6cb3-3a73-7dc2-9279-b3d4d3a229f7`,
   2026-02-17, same question) got data from both. The new endpoint accepts the same `BIOSCIENCES_API_KEY` Bearer
   auth and serves all 34 tool names the app calls. Known limit (Don): the app does not use the
   `biosciences-mcp-edge` endpoints (e.g. ORCS essentiality, mechanism of action) that the current Cowork
   plugin uses, so BioGRID/edge discovery will be weaker than the plugin's.
4. New files only, outside `apps/`: a run script and the provenance writer (location left to the
   builder, e.g. `scripts/rerun/`).

No other edit under `apps/`, `.claude/`, `.deepagents/`. Environment: `uv sync --frozen` against
the baseline `uv.lock`. If anything needs a package not in the lock, stop and ask Don.

### Stage 1: research

- Start `uv run langgraph dev` from the clone, as in February.
- Submit the question to assistant `lifesciences` through the LangGraph SDK against the local
  server (my call: headless instead of the web UI, so the run is scripted and repeatable; same graph
  and server the UI used).
- Save the thread's final state and message history to the run folder, and record the LangSmith
  trace id (project from `.env`, `LANGSMITH_PROJECT=lifesciences-deepagents`) and the Graphiti
  `add_memory` result and group id.

### Stage 2: publication

- Don starts Claude Code in the clone with `--model claude-sonnet-4-5-20250929`. This step is
  interactive, because the Synapse MCP server signs in through a browser.
- Run the `lifesciences-publication-pipeline` skill on the stage-1 output saved in the run folder.
  It produces its five files into the run folder.
- Copy the Claude Code session transcript (the session `.jsonl` under `~/.claude/projects/`) into
  the run folder as stage-2 provenance (my call, to make up for the lack of LangSmith telemetry on
  the subscription). Record the Claude Code version and the model it reports. OpenTelemetry export
  to Don's otel stack is optional and not required.

### Output layout

```
output/reruns/<YYYY-MM-DD>-sonnet45/
  provenance.json             # run-level record
  comparison.md               # C6-C10 vs baseline
  doxorubicin-nf1-toxicity/
    provenance.json           # per-stage detail
    stage1-thread.json        # final state + messages
    stage2-claude-session.jsonl
    doxorubicin-nf1-toxicity-report.md
    doxorubicin-nf1-toxicity-knowledge-graph.json
    doxorubicin-nf1-toxicity-synapse-grounding.md
    doxorubicin-nf1-toxicity-quality-review.md
    doxorubicin-nf1-toxicity-biorxiv-draft.md
```

Nothing is written under `output/cqs/`. Before committing, scan the run folder (especially the
session transcript) for `.env` values, key patterns and email addresses; the repo is public.

### Provenance record (minimum fields)

- Git: run commit SHA, baseline tag and SHA, `git diff --stat baseline..HEAD`, clean/dirty flag.
- Environment: `uv.lock` SHA-256 (must equal baseline), Python version, versions of `deepagents`,
  `langchain`, `langchain-anthropic`, `anthropic`; Claude Code version.
- Model: id requested, id reported in responses, per stage.
- Endpoints: MCP URL (and server version if exposed), Synapse MCP URL, Graphiti URL and group id.
- Keys: name and last 4 characters only, for each key used; billing account per stage
  (API key / Claude subscription).
- Run: question text, slug, start/end UTC timestamps, LangGraph thread id, LangSmith trace id(s),
  exit status, any refusal or retry.

### Preflight (before the run)

1. The clone is clean and on the run branch; `uv.lock` hash equals baseline.
2. `https://lifesciences-research.fastmcp.app/mcp` answers a tool list with the current
   `BIOSCIENCES_API_KEY`. Risk: in Aug 2026 `biosciences-deepagents` moved to `biosciences-mcp`
   with a different auth header, so this server may be gone or changed. If it fails, stop and ask
   Don; do not repoint the code.
3. The Anthropic key accepts a minimal request to `claude-sonnet-4-5-20250929`.
4. graphiti-docker (`localhost:8002`) answers; record whether group `lifesciences-default` already
   exists.
5. LangSmith key is valid and the project exists.

### Comparison

`comparison.md`: one row per claim C6–C10 with deck value, February file value, new value, verdict
and a link to the new file. A short header gives the provenance summary (model, commit, date,
endpoints), the two code changes, the baseline gap and the C6 inconsistency.

## Constraints

- The repo is public: all committed content is published.
- Costs: Anthropic API usage for stage 1; Claude subscription usage for stage 2. One run unless Don
  asks for repeats.
- Runs commit to `chore/oct21-validation` and reach `main` only through a PR Don reviews and merges.

## Run log (2026-10-21)

Details, trace ids and costs: `output/reruns/2026-10-21-sonnet45/PROVENANCE.md`.

- Runs were started from the web UI (`apps/web`, `yarn dev`, assistant `lifesciences`), not the headless
  SDK runner described under Stage 1; no runner script was written.
- Attempt 1 on the old endpoint failed every STRING/BioGRID call (`-32603`) and was killed; this led to code change 3.
- Two completed stage-1 runs on identical inputs differed materially (25 nodes / 33 edges vs 43 / 68), so one
  run is one sample, not a stable measurement.
- The second run's validation specialist rejected real BioGRID synthetic-lethality citations as INVALID
  (method: PMID absent from keyword searches). Treat that verdict as an error when comparing.
- Graphiti persistence was never called, so code change 2 is untested.
- Agent files live in thread state (`/workspace/` → `StateBackend`, `apps/api/lifesciences.py:295`); export them
  from the server after each run. A temporary change that wrote them to disk was reverted (Don, 2026-10-21).
- API spend on stage 1: $9.07.

## Open decisions (Don's)

- Tolerances per claim (e.g. node/edge counts within ±N; quality score at or above 35/40).
- Whether to repeat stage 1 (and how many times) given the run-to-run variation.
- Location of the headless plugin run's `output/cqs/doxorubicin-nf1-toxicity-2026-10-21/knowledge-graph.json`.

## Left to the builder

- Run script and provenance-writer implementation and language.
- Retry and timeout handling (each retry recorded).
- How the stage-1 output is handed to the stage-2 skill, as long as the handed-over file is in the
  run folder.
