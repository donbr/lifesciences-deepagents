# Baseline UI Progressive Disclosure - Capture Summary

**Date**: 2026-02-08
**Commit**: 35870a2 (last known good state before Sprint 1)
**Test Query**: "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"

---

## ✅ Baseline Restoration Complete

### Actions Taken:
1. ✅ Backed up Sprint 1 work to `/tmp/sprint1-backup/`
2. ✅ Hard reset to commit 35870a2
3. ✅ Cleaned Sprint 1 untracked files
4. ✅ Verified servers running (backend: 2024, frontend: 3000)
5. ✅ Captured 10 baseline screenshots
6. ✅ Fetched LangSmith trace

---

## 📸 Baseline Screenshots Captured

All screenshots saved to: `baseline-screenshots/`

| File | Phase | Description |
|------|-------|-------------|
| `00-initial.png` | Initial | Empty UI before query submission |
| `01-query-submitted.png` | Submitted | Query entered, waiting for first phase |
| `02-anchor_specialist.png` | Phase 1: ANCHOR | Entity resolution (Palovarotene, FOP CURIEs) |
| `03-enrichment_specialist.png` | Phase 2: ENRICH | Metadata enrichment (UniProt, Ensembl IDs) |
| `04-expansion_specialist.png` | Phase 3: EXPAND | Network expansion (protein interactions) |
| `05-traversal_drugs_specialist.png` | Phase 4a: TRAVERSE_DRUGS | Drug mechanism discovery |
| `06-traversal_trials_specialist.png` | Phase 4b: TRAVERSE_TRIALS | Clinical trial discovery |
| `07-validation_specialist.png` | Phase 5: VALIDATE | Fact validation |
| `08-persistence_specialist.png` | Phase 6: PERSIST | Final summary and graph formatting |
| `99-final-complete.png` | Complete | All phases done, final answer displayed |

**Total Size**: 776K (10 screenshots)
**Phases Captured**: 7/7 completed phases ✓

---

## 📊 LangSmith Trace

**Trace ID**: `019c3c9a-4db1-76a2-bc67-cafeb0899a20`
**Location**: `baseline-traces/019c3c9a-4db1-76a2-bc67-cafeb0899a20.json`
**Messages**: 15 total

This trace contains the complete execution flow showing:
- Supervisor delegations via `task()` tool calls
- All 7 specialist subagent executions
- Tool calls to MCP services (query_lifesciences, query_pubmed)
- Streaming message flow to frontend

---

## 🎯 Key Baseline Observations

### UI Progressive Disclosure Pattern (Working):
1. **SubAgentIndicator Components**: Each phase appears as a collapsible section
2. **Status Transitions**: Blue pulsing dot (running) → Green dot (completed)
3. **Collapsible Sections**: User can expand/collapse each phase
4. **Sequential Execution**: All 7 phases execute in order
5. **Iterative Graph Building**: Users see knowledge being built step-by-step

### Backend-Frontend Integration:
- Supervisor delegates to specialists via `task()` tool
- `subagent_type` parameter identifies phase (e.g., "anchor_specialist")
- UI extracts `task()` calls from streaming messages
- ChatMessage component renders SubAgentIndicator for each task
- Status updates flow through WebSocket streaming

### File Locations (Working Baseline):
- **Backend**: `apps/api/graphs/lifesciences.py` (commit 35870a2)
- **Frontend**: `apps/web/src/app/components/ChatMessage.tsx` (SubAgent extraction)
- **UI Component**: `apps/web/src/app/components/SubAgentIndicator.tsx` (status display)

---

## 🔍 Next Steps

Now that we have baseline artifacts, we can:

1. **Create Feature Branch**: `git checkout -b feature/sprint1-redesign-with-ui-preservation`

2. **Redesign Sprint 1** with these principles:
   - Preserve `task()` tool delegation pattern (UI depends on it)
   - FilesystemBackend as non-blocking enhancement
   - Artifacts generated best-effort (don't break phases)
   - Test after each incremental change

3. **Incremental Implementation** with validation:
   - Change 1: Add FilesystemBackend with virtual_mode → Run Playwright → Compare screenshots
   - Change 2: Update PERSIST_SYSTEM for optional file writes → Run Playwright → Compare
   - Change 3: Add schema validation (standalone) → Run Playwright → Compare
   - Change 4: Wire schema into persistence if all tests pass

4. **Acceptance Criteria**:
   - All 7 phases still execute and appear in UI
   - Screenshots match baseline (same progressive disclosure)
   - No permission errors in traces
   - Bonus: graph.json and report.md generated in workspace

---

## 📁 Files Created

### Scripts:
- `capture_baseline_ui.py` - Playwright Python script for baseline capture
- `inspect_ui.py` - UI reconnaissance script

### Data:
- `baseline-screenshots/` - 10 PNG screenshots (776K total)
- `baseline-traces/` - LangSmith trace JSON

### Documentation:
- `BASELINE-CAPTURE-SUMMARY.md` - This file

---

## ⚠️ Sprint 1 Issues Documented

### Root Cause:
- Absolute paths (`/phase1_anchor.json`) interpreted as system root paths
- FilesystemBackend without `virtual_mode=True` allowed unsafe path resolution
- Permission denied writing to `/` (root filesystem)

### Breaking Changes:
- Added FilesystemBackend integration
- Modified supervisor prompt with filesystem handoff instructions
- Updated PERSIST_SYSTEM to require file writes
- No incremental testing or UI validation

### Lessons Learned:
1. Always capture baseline before infrastructure changes
2. Use feature branches for experimental work
3. Validate UI behavior after each change
4. Test end-to-end, not just unit tests
5. Document working patterns before modifying them

---

**Status**: ✅ Baseline captured and documented
**Ready for**: Sprint 1 redesign with UI preservation
