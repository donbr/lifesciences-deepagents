# NF1 doxorubicin rerun, 2026-10-21

Question (verbatim, as submitted in Feb 2026):
> What known genes or pathways are implicated in minimizing Doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?

Code: branch `chore/oct21-validation` from `568dfe0`, three changes: model `anthropic:claude-sonnet-4-5-20250929`
(`apps/api/lifesciences.py:228`), tools server `https://biosciences-mcp.fastmcp.app/mcp` (`apps/api/shared/mcp.py:192`),
Graphiti `http://localhost:8002/mcp` (`apps/api/shared/mcp.py:583`). `uv.lock` unchanged. LangSmith project `lifesciences-deepagents`.

| Folder | What | Trace / source | Cost | Result |
|---|---|---|---|---|
| (not saved) | LangGraph, old endpoint `lifesciences-research.fastmcp.app` | `01a15fe4-e931-72c0-92c3-150ff8669c63` | $2.91 (API key) | Killed ~19:42Z: every STRING/BioGRID call returned `-32603`; server hung on shutdown |
| `run-1952/` | LangGraph via web UI, thread `98fa7f44-d6c9-408b-9320-3cadb2e0c229`, 19:52-20:16Z | `01a16005-fb2e-7921-858f-49fe27513aa6` | $2.75 (API key) | 25 nodes / 33 edges. Files exported from thread state (`thread-state.json`) |
| `run-2043/` | LangGraph via web UI, thread `28d32a78-904a-4935-9a23-2c2fdbb66435`, 20:43-21:11Z | `01a16034-54de-7a60-83c1-f3d0f21d3307` | $3.41 (API key) | 43 nodes / 68 edges. Ran with the `/workspace/` state route disabled (since reverted), so files were written to `.deepagents/workspace/` and copied here; thread state not exported (server stopped; full history in LangSmith) |
| `plugin-ob-interactive/` | Claude Code + open-biosciences `bio-research` plugin (`/bio-research:ob-research`, `/bio-research:ob-report`, review), Don's session | session `75db85fa-dc3d-4a5c-a9f4-b4980677d931` | Max subscription | 19 nodes / 15 edges after review fixes; review verdict PARTIAL |

Not saved here: the headless plugin run (session `7cc16163-54f7-4da4-a849-ec411f3a0808`) wrote
`output/cqs/doxorubicin-nf1-toxicity-2026-10-21/knowledge-graph.json`; its location is undecided.

Known issues to weigh before comparing with the deck:
- Same inputs, different results: run-1952 and run-2043 differ in size (25/33 vs 43/68) and content.
- run-2043's validation specialist marked BioGRID synthetic-lethality citations INVALID because the PMIDs did not appear in keyword searches. Both papers are real synthetic-lethality screens (PMID 27453043, doi:10.1016/j.molcel.2016.06.022; PMID 19490893, doi:10.1016/j.cell.2009.05.006). The evidence is screen-level and weak, not invalid; the report's "INVALID" wording is wrong.
- Graphiti persistence was never called in either completed run; nothing was written to graphiti-docker.
- Stage 2 (publication pipeline: Synapse grounding, /40 quality review) has not been run, so deck claims C8 and C10 are not yet testable.
