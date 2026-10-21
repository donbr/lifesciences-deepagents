# DeepAgents 0.3.12 Spike Baseline (Pre-Step-3)

Date: 2026-02-08
Branch: `feature/deepagents-0312-upgrade-spike`
Worktree: `/home/donbr/ai2026/lifesciences-deepagents-worktrees/deepagents-0312-upgrade-spike`
Local API: `http://127.0.0.1:2224`

## CQ Used
`What drugs target the ACVR1 pathway in fibrodysplasia ossificans progressiva (FOP)?`

## CLI Command Used
```bash
THREAD_ID=$(curl -s -X POST http://127.0.0.1:2224/threads -H 'content-type: application/json' -d '{}' | jq -r '.thread_id')
curl -s -X POST "http://127.0.0.1:2224/threads/${THREAD_ID}/runs/wait" \
  -H 'content-type: application/json' \
  -d '{"assistant_id":"5616883e-18f7-5db6-8adc-14c342741644","input":{"messages":[{"role":"user","content":"What drugs target the ACVR1 pathway in fibrodysplasia ossificans progressiva (FOP)?"}]}}'
```

## Baseline Run
- assistant_id: `5616883e-18f7-5db6-8adc-14c342741644`
- thread_id: `34ca9e5d-2ab7-4146-a3b4-d84c2a8a189c`
- run_id: `019c3f49-bdcd-7971-b4b5-77a51046556b`
- status: `success`

Observed subagent sequence:
- `anchor_specialist`
- `enrichment_specialist`
- `traversal_drugs_specialist`
- `traversal_trials_specialist`
- `enrichment_specialist`
- `traversal_drugs_specialist`

## Regression Signals Captured
- `expansion_specialist` missing.
- repeated phase calls and phase-order drift.
- GOF polarity drift: agonist-only candidates surfaced (`EPTOTERMIN ALFA`, `DIBOTERMIN ALFA`).

## LangSmith Fetch Validation
```bash
uv run langsmith-fetch traces /tmp/lsf-baseline --limit 1 --include-metadata --no-progress --format raw
```
- latest fetched trace_id: `019c3f3d-54ec-7de0-9b0f-78fcef4fce6c`
- fetched evidence includes agonist mentions for ACVR1/FOP flow.

## Notes
This baseline is intentionally captured before Step 3 orchestration stabilization, to compare subsequent incremental gates.
