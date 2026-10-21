# Executive Summary: Skill vs DeepAgents Comparison

**Date**: 2026-02-09
**Query**: By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?
**Comparison**: lifesciences-graph-builder skill vs DeepAgents lifesciences implementation

---

## TL;DR

Both approaches produced **scientifically correct answers**. The skill had **0 errors** vs DeepAgents' 3 errors, but the "missing phase files" issue was a **misdiagnosis** — files exist in LangGraph state, just not on disk.

**Correct fix**: Configure `FilesystemBackend` instead of default `StateBackend` to write files to disk.

---

## Answer Quality: Both Correct ✓

### Skill Answer
**Mechanism**: Palovarotene (RARγ agonist) → proteasome-mediated degradation of phosphorylated SMAD1/5/8 → inhibits BMP signaling → reduces heterotopic ossification

**Strengths**:
- More mechanistic detail (proteasome degradation)
- Detailed BMP pathway explanation
- Web search for mechanism (not in MCP tools)

### DeepAgents Answer
**Mechanism**: Palovarotene (RARγ agonist) → SMAD1-RARγ complex degradation → inhibits BMP signaling → reduces heterotopic ossification

**Strengths**:
- More clinical breadth (24 trials vs 8)
- Explicit gap disclosure
- Structured phase files (when backend configured correctly)

**Verdict**: Both scientifically accurate, different presentation styles.

---

## Execution Metrics

| Metric | Skill | DeepAgents |
|--------|-------|------------|
| **Tool calls** | 22 (19 MCP + 2 Bash + 1 WebSearch) | ~15-20 (via wrappers) |
| **Errors** | 0 | 3 (ChEMBL 500, Open Targets format, file creation) |
| **Phase files** | 0/8 (not required) | 4/8 (50% — files in state, not disk) |
| **Execution time** | ~15 min | ~20 min |
| **ChEMBL success** | ✓ (no 500 error) | ✗ (500 error) |

---

## The "Missing Files" Issue — CORRECTED

### Original Diagnosis (WRONG)
> "Specialists lack `write_file` tool. Fix: Add `write_file` to specialist tool lists."

### Correct Diagnosis (from LangChain docs)
**Specialists ALREADY HAVE `write_file` tool** because:
1. `create_deep_agent()` automatically includes `FilesystemMiddleware`
2. `FilesystemMiddleware` automatically provides `write_file`, `read_file`, `ls`, `edit_file`
3. Subagents automatically inherit these tools

**The real issue**:
- Default backend is `StateBackend` (ephemeral, in LangGraph state)
- `StateBackend` stores files in state, **NOT on disk**
- Files exist in thread state, just not at `.deepagents/workspace/`

### The Correct Fix

**Option 1: Write to disk (for development)**
```python
# In apps/api/lifesciences.py
from deepagents.backends import FilesystemBackend

lifesciences_graph = create_deep_agent(
    name="lifesciences",
    backend=FilesystemBackend(root_dir=".deepagents/workspace", virtual_mode=True),
    # ... rest of config
)
```

**Option 2: Keep StateBackend (for production)**
```python
# Default behavior — files in state (secure, thread-scoped)
lifesciences_graph = create_deep_agent(
    name="lifesciences",
    # backend defaults to StateBackend
    # ... rest of config
)
```

**Option 3: Hybrid (CompositeBackend)**
```python
from deepagents.backends import CompositeBackend, StateBackend, FilesystemBackend

lifesciences_graph = create_deep_agent(
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/workspace/": FilesystemBackend(root_dir=".deepagents/workspace", virtual_mode=True)}
    ),
    # ... rest of config
)
```

---

## When to Use Which Approach

### Use Skill When:
- ✓ Exploratory queries (no fixed workflow)
- ✓ Interactive chat (conversational output)
- ✓ Simple queries (1-3 phases)
- ✓ Fast iteration needed
- ✓ Budget-conscious (fewer LLM calls)

**Example**: "What is the function of TP53?" → Skill (2-3 tool calls vs 7 specialist invocations)

### Use DeepAgents When:
- ✓ Fixed workflow (same phases every time)
- ✓ Batch processing (1000s of queries)
- ✓ Machine-readable output (JSON, graph)
- ✓ Audit requirements (compliance, provenance)
- ✓ Complex queries (all 6 phases)
- ✓ Parallel execution (Phases 4a/4b)

**Example**: Clinical trial matching, knowledge graph construction, FDA submission

---

## Recommendations by Scenario

| Scenario | Recommendation | Backend |
|----------|----------------|---------|
| **Academic research** | Skill | N/A |
| **Production pipeline** | DeepAgents | StateBackend (default) |
| **Local development** | DeepAgents | FilesystemBackend |
| **Interactive platform** | Skill | N/A |
| **Knowledge graph** | DeepAgents | CompositeBackend |
| **FDA submission** | DeepAgents | StateBackend + audit logging |

---

## Comparison Highlights

### Maintainability
**Skill wins**: Single SKILL.md file (850 lines) vs 8 files (lifesciences.py + prompts.py, 1300 lines)

### Reliability
**Skill wins (this execution)**: 0 errors vs 3 errors

**But** DeepAgents showed impressive resilience — produced correct answer despite 50% file failures.

### Transparency
**DeepAgents wins**: Structured phase files, explicit delegation, better observability

**But** Skill's single conversation thread is easier to read end-to-end.

### Flexibility
**Skill wins**: All 34 MCP tools available, can pivot mid-query, flexible fallbacks (curl, web search)

**DeepAgents**: Tool isolation (security), enforced phases (safety), parallel execution (performance)

---

## Key Learnings

1. **File creation was never broken** — files were in state, not disk
2. **Specialists already have write_file** — FilesystemMiddleware is automatic
3. **StateBackend vs FilesystemBackend** is the key distinction:
   - StateBackend: Thread-scoped, secure, ephemeral (production default)
   - FilesystemBackend: Persistent on disk, for development/debugging
4. **Both approaches are valid** — serve different purposes
5. **Don't assume based on symptoms** — verify against docs

---

## Next Steps

### Immediate (if you want files on disk)
1. Apply FilesystemBackend fix to `apps/api/lifesciences.py`
2. Re-run FOP query
3. Verify 8 files appear in `.deepagents/workspace/`

### Short-term
1. Update CLAUDE.md with backend configuration guidance
2. Add environment variable for backend selection (dev vs prod)
3. Test both StateBackend and FilesystemBackend

### Long-term
1. Add CompositeBackend for hybrid workflows
2. Implement metrics for file creation success rate
3. Add LangSmith dashboards for phase completion tracking

---

## Deliverables Created

All files in `comparison-reports/`:

1. ✓ `SKILL-VS-DEEPAGENTS.md` (450 lines) — Side-by-side comparison
2. ✓ `ANALYSIS.md` (588 lines) — Critical analysis, scenario recommendations
3. ✓ `CORRECTED-FIX.md` (200 lines) — Correct diagnosis based on LangChain docs
4. ✓ `EXECUTIVE-SUMMARY.md` (this file) — TL;DR for stakeholders

All files in `skill-execution/`:

1. ✓ `fop-skill-transcript.md` (174 lines) — Full execution log
2. ✓ `tool-calls.txt` (100 lines) — 22 tool call sequence
3. ✓ `answer.md` (91 lines) — Mechanism with evidence

---

## Conclusion

**The skill vs DeepAgents comparison revealed complementary strengths, not a winner.**

- **Skill**: Simple, fast, flexible — ideal for research and development
- **DeepAgents**: Structured, auditable, production-ready — ideal for pipelines

**The "missing files" issue was a misunderstanding** — files exist in state, just need `FilesystemBackend` to write to disk.

**Both approaches produced correct scientific answers** — the choice depends on your use case, not quality.

**Final recommendation**: Keep both. Use Skill for CLI/chat, DeepAgents for API/batch. Share the same MCP tools and Fuzzy-to-Fact protocol.
