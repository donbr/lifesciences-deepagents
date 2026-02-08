# Known Issues - Sprint 1 Redesign

## Artifact Generation Not Working (High Priority)

**Status:** Regression from unknown previous working state
**Affects:** persistence_specialist Phase 6 output
**Impact:** `graph.json` and `report.md` not generated in `.deepagents/workspace/`

### Description

The persistence_specialist completes successfully and provides final answers, but does not generate artifact files despite:
- FilesystemBackend configured with `virtual_mode=True`
- Workspace directory created at `.deepagents/workspace/`
- PERSIST_SYSTEM prompt instructing file generation

### Root Cause (Suspected)

FilesystemBackend's `write_file` tool not accessible to persistence_specialist when `tools: []` is set. The automatic tool exposure mechanism from FilesystemBackend may require:
- Explicit tool inclusion in subagent configuration
- Different tools parameter (None vs [] vs explicit list)
- Additional FilesystemBackend configuration

### Reproduction

```bash
python3 test_artifact_generation.py
# Workspace directory exists but remains empty
```

### Workaround

None currently. Agent provides complete answers via UI but artifacts are not persisted to filesystem.

### Investigation Needed

1. Compare to last known working configuration (when did artifacts work?)
2. Review DeepAgents documentation on FilesystemBackend tool exposure
3. Check if explicit `write_file` tool import/configuration required
4. Test with different `tools` parameter values ([], None, explicit list)

### Related Files

- `apps/api/graphs/lifesciences.py` - Line 141 (persistence_specialist configuration)
- `apps/api/shared/prompts.py` - PERSIST_SYSTEM prompt
- `.deepagents/workspace/` - Expected artifact output directory

### Sprint 1 Impact

**Does NOT block Sprint 1 merge:**
- ✅ Progressive disclosure validated and working
- ✅ FilesystemBackend infrastructure in place
- ✅ Non-blocking design (agent works without artifacts)
- ❌ Artifact generation (deferred to follow-up)

---

*Document created: 2026-02-08*
*Branch: feature/sprint1-redesign-with-ui-preservation*
