# Critical Analysis: Skill vs DeepAgents

**Date**: 2026-02-09
**Analyst**: Claude Code (Sonnet 4.5)
**Context**: Comparison of lifesciences-graph-builder skill vs DeepAgents implementation for FOP/Palovarotene mechanism query

---

## Question 1: Did the skill avoid the missing phase files issue?

**YES, but the answer is nuanced.**

### What happened

**Skill execution**:
- Created 0/8 phase files (0%)
- No file creation failures
- All outputs were conversation-based

**DeepAgents execution** (from VALIDATION-REPORT.md):
- Created 4/8 phase files (50%)
- 50% file creation failure rate
- Missing: phase2_enrich.json, phase4a_drugs.json, phase5_validate.json

### Why the skill "succeeded"

**The skill has no file output requirements.**

From `.claude/skills/lifesciences-graph-builder/SKILL.md`:
- Phase 1-5: No mention of creating JSON files
- Phase 6a PERSIST: "Format validated graph as JSON and persist to Graphiti" (optional, conditional on Graphiti availability)
- Phase 6b REPORT: "Use lifesciences-reporting skill" (separate skill, not executed)

**The skill protocol is conversation-based, not file-based.**

### Why DeepAgents failed

From `apps/api/shared/prompts.py` and ISSUE-REVIEW.md:

**Specialist prompts explicitly require file outputs**:
```python
# Example from anchor_specialist
"Once entities are resolved, persist your findings as phase1_anchor.json with schema..."
```

**But specialists lack the write_file tool**:
```python
# In apps/api/lifesciences.py:307-428
anchor_specialist = create_deep_agent(
    tools=[query_lifesciences, query_pubmed, think_tool],  # NO write_file
    ...
)
```

### Conclusion

**This is NOT a fair comparison.** The skill avoided file failures by not having file requirements, not by solving the underlying issue.

**If the skill were modified to create phase files, it would likely encounter the same issue** (no write_file tool available in skill context).

**The real difference**:
- **Skill**: Protocol guidelines, flexible output format
- **DeepAgents**: Structured output requirements, rigid format

**Both approaches are valid**, just serving different purposes:
- Skill: Exploratory research, human consumption
- DeepAgents: Production pipelines, machine-readable output

---

## Question 2: Which approach is more maintainable?

**Skill wins for simplicity, DeepAgents wins for modularity.**

### Code Maintenance

| Dimension | Skill | DeepAgents | Winner |
|-----------|-------|------------|--------|
| Files to edit | 1 (SKILL.md) | 8+ (lifesciences.py + prompts.py + 7 specialists) | Skill |
| Lines of code | ~850 (SKILL.md) | ~500 (lifesciences.py) + ~800 (prompts.py) = 1300 | Skill |
| Dependency graph | Flat (skill → MCP tools) | Nested (supervisor → specialists → tools) | Skill |
| Testing surface | 1 skill entry point | 1 supervisor + 7 specialists = 8 entry points | Skill |

### Protocol Updates

**Scenario: Add Phase 7 "REFINE" to validate drug targets via literature**

**Skill approach**:
1. Edit SKILL.md
2. Add "## Phase 7: REFINE" section with instructions
3. Update checklist
4. Done (5 minutes)

**DeepAgents approach**:
1. Edit `apps/api/shared/prompts.py` to add `refine_specialist_prompt`
2. Edit `apps/api/lifesciences.py` to create `refine_specialist`
3. Update supervisor prompt to include Phase 7 in delegation logic
4. Add tools to specialist (e.g., `query_pubmed`, `think_tool`)
5. Update `langgraph.json` if needed
6. Test specialist in isolation
7. Test supervisor → specialist delegation
8. Done (30 minutes)

**Winner**: Skill (faster iteration)

### Tool Updates

**Scenario: MCP server adds new tool `query_patents`**

**Skill approach**:
1. MCP server auto-loaded via ToolSearch
2. Skill sees all 35 tools (34 + 1 new)
3. Update SKILL.md to document new tool (optional)
4. Done (0 minutes for availability, 5 minutes for docs)

**DeepAgents approach**:
1. MCP server auto-loaded via `query_lifesciences` wrapper
2. Decide which specialists get access
3. Update specialist tool lists in `lifesciences.py`
4. Update specialist prompts in `prompts.py` to use new tool
5. Test specialists
6. Done (20 minutes)

**Winner**: Skill (automatic tool propagation)

### Bug Fixes

**Scenario: ChEMBL returns 500 errors frequently**

**Skill approach**:
1. Edit SKILL.md Phase 4a section
2. Update instructions to use Open Targets `knownDrugs` as primary, ChEMBL as fallback
3. Done (5 minutes)

**DeepAgents approach**:
1. Edit `traversal_drugs_specialist_prompt` in prompts.py
2. Update fallback logic instructions
3. OR: Edit `shared/mcp.py` to add retry logic to `query_lifesciences` wrapper
4. Test specialist
5. Done (10-20 minutes)

**Winner**: Skill (faster fix)

### Modularity Trade-offs

**DeepAgents advantages**:
- **Specialist reuse**: `anchor_specialist` could be used in other graphs (e.g., drug-repurposing graph)
- **Independent testing**: Each specialist can be tested in isolation with mock inputs
- **Tool isolation**: Easy to audit which specialist uses which tools (security, cost)
- **Parallel evolution**: Specialists can be updated independently without breaking supervisor

**Skill advantages**:
- **Single source of truth**: All protocol logic in one file
- **Easier to understand**: Read top-to-bottom to understand full workflow
- **Faster iteration**: Edit → test cycle is shorter
- **Less coupling**: No supervisor-specialist coordination to manage

### Recommendation

**For rapid prototyping and research**: Use Skill
**For production systems with multiple agents**: Use DeepAgents

**Example**:
- Genomics startup doing exploratory research → Skill
- Pharma company with validated drug discovery pipeline → DeepAgents

---

## Question 3: Which approach is more reliable?

**Skill was more reliable in this specific execution, but DeepAgents' resilience is impressive.**

### Error Rates

| Metric | Skill | DeepAgents |
|--------|-------|------------|
| Tool errors | 0/22 (0%) | 3/~20 (15%) |
| Phase failures | 0/6 (0%) | 2/6 (33%) — Phases 4a, 5 |
| File failures | N/A | 4/8 (50%) |
| Answer correctness | ✓ Correct | ✓ Correct |
| Completion | ✓ 100% | ⚠️ 70% (missing files) but valid answer |

### Error Analysis

**DeepAgents errors**:
1. **ChEMBL 500 error** (Phase 2 or 4a) — upstream API failure
2. **Open Targets format error** (Phase 4a) — `query_api_direct` parsing issue
3. **File creation failures** (Phases 2, 4a, 5) — missing write_file tool

**Skill errors**:
- None

**But**: Skill used web search fallback when MCP tools insufficient (SMAD degradation mechanism). This is flexible but less reproducible than MCP tool calls.

### Graceful Degradation

**DeepAgents** continued despite failures:
- Phase 4a (drugs) failed → still found Palovarotene via Phase 1/2
- Phases 2, 5 file creation failed → still had valid data in conversation
- Produced scientifically correct answer with 70% phase completion

**This is remarkable resilience.** The supervisor + specialist architecture allows failures to be isolated.

**Skill** had no failures to recover from, so graceful degradation wasn't tested.

### Reproducibility

**DeepAgents**:
- ✓ All tool calls logged in LangSmith
- ✓ Phase files provide checkpoints (when they exist)
- ✓ StateBackend allows inspection of intermediate state
- ⚠️ 50% file failure means missing checkpoints

**Skill**:
- ✓ All tool calls logged in LangSmith
- ⚠️ No intermediate checkpoints (conversation only)
- ⚠️ Web search results may vary over time (SMAD mechanism query)

**Winner**: DeepAgents (when file creation works)

### Production Reliability Factors

**Uptime/Availability**:
- Skill depends on: MCP server, LLM API, web search API
- DeepAgents depends on: MCP server, LLM API, StateBackend, LangGraph server
- **Winner**: Skill (fewer dependencies)

**Error recovery**:
- Skill: Flexible (can skip phases, retry, fallback to web search)
- DeepAgents: Structured (specialist retries, but blocked if specialist fails)
- **Winner**: Skill (more flexible)

**Observability**:
- Skill: Conversation trace + LangSmith
- DeepAgents: Conversation trace + LangSmith + phase files + StateBackend
- **Winner**: DeepAgents (more instrumentation)

**Auditability**:
- Skill: Single conversation thread (easy to read, hard to parse)
- DeepAgents: Structured phase files + specialist outputs (easy to parse, verbose)
- **Winner**: DeepAgents

### Recommendation

**For ad-hoc queries**: Skill (simpler, fewer failure modes)
**For production pipelines**: DeepAgents (better observability, auditability) — **after fixing file creation bug**

---

## Question 4: Which approach is more transparent?

**DeepAgents wins on structured transparency, Skill wins on readability.**

### Execution Transparency

**DeepAgents**:
- ✓ Explicit phase transitions (supervisor `task()` calls logged)
- ✓ Specialist inputs/outputs visible in StateBackend
- ✓ Phase files show intermediate results
- ✓ Tool isolation makes it clear which specialist used which tools
- ⚠️ Supervisor decision logic is implicit (LLM decides which specialist to call)

**Skill**:
- ⚠️ Phase transitions implicit (LLM decides when to move to next phase)
- ⚠️ All intermediate results in conversation only (no structured checkpoints)
- ✓ Single conversation thread is easier to read end-to-end
- ⚠️ Tool calls interleaved with reasoning (harder to extract just the tool sequence)

**Winner**: DeepAgents (more structured, easier to audit)

### Debugging Experience

**Scenario: Phase 4a (drugs) returned no results — why?**

**DeepAgents debugging**:
1. Check phase4a_drugs.json — oh, it's missing
2. Check LangSmith trace for `traversal_drugs_specialist`
3. See Open Targets `query_api_direct` error
4. Inspect error message: "GraphQL parsing failed"
5. Fix: Update `shared/mcp.py` to handle Open Targets response format
6. **Time to diagnose**: 5 minutes (phase file revealed issue immediately)

**Skill debugging**:
1. Read full conversation transcript (1000+ lines)
2. Find Phase 4a section
3. See Open Targets curl command
4. See... it succeeded? (because skill used curl fallback correctly)
5. **Time to diagnose**: 15 minutes (had to read full transcript)

**Winner**: DeepAgents (faster debugging with phase files)

### User Transparency

**For end users (scientists using the system)**:

**DeepAgents**:
- Phase-by-phase progress visible in UI
- Phase files can be downloaded for offline review
- Clear separation between "what was found" (phase files) and "how it was found" (specialist logs)

**Skill**:
- Single conversation stream (feels more like chat)
- No progress indicators (just LLM generating text)
- Answer is mixed with tool calls (less structured)

**Winner**: DeepAgents (better user experience for complex queries)

### Developer Transparency

**For developers maintaining the system**:

**DeepAgents**:
- Clear separation of concerns (supervisor vs specialists)
- Tool assignments documented in code (`tools=[...]`)
- Phase logic in specialist prompts (easy to find)
- StateBackend schema is explicit

**Skill**:
- All logic in one SKILL.md file (easy to find, hard to parse)
- No explicit tool assignments (skill has access to all tools)
- Phase logic mixed with instructions (prose, not code)

**Winner**: DeepAgents (better code structure)

### Recommendation

**For research/exploration**: Skill (conversational transparency)
**For production/audit**: DeepAgents (structured transparency)

---

## Question 5: Production recommendation

**Use DeepAgents for production, Skill for development.**

### Detailed Recommendations by Scenario

#### Scenario 1: Drug Repurposing Research (Academic Lab)

**Context**: Professors and postdocs exploring new targets for old drugs.

**Queries**:
- "What drugs target BCL2?"
- "What are the side effects of Venetoclax?"
- "Build pathway from TP53 to apoptosis"

**Characteristics**:
- Ad-hoc queries (1-2 per hour)
- Exploratory (no fixed workflow)
- Users are comfortable with unstructured output
- Budget-conscious (minimize LLM calls)

**Recommendation**: **Skill**

**Reasoning**:
- Fast iteration (no specialist overhead)
- Flexible (can deviate from protocol if needed)
- Simpler deployment (single skill file)
- Lower token cost (fewer LLM calls)

---

#### Scenario 2: Clinical Trial Matching (Pharma Company)

**Context**: Automated system matching patients to trials based on genetic profiles.

**Queries**:
- "Find trials for BRCA1 mutation carriers"
- "What drugs are in Phase 3 for lung cancer?"
- "Validate trial NCT03312634 inclusion criteria"

**Characteristics**:
- Batch processing (1000s of queries per day)
- Fixed workflow (Phase 1 → 4b → 5 every time)
- Users need machine-readable output (JSON)
- Audit requirements (FDA compliance)

**Recommendation**: **DeepAgents (with fixes)**

**Reasoning**:
- Structured output (phase files for audit trail)
- Tool isolation (security: trials specialist can't access drug pricing data)
- Parallel execution (Phase 4a/4b in parallel)
- Observability (LangSmith + phase files + metrics)
- Reproducibility (phase files = checkpoints)

**Required fixes**:
1. Add `write_file` to all specialists
2. Validate phase file writes
3. Add retry logic for ChEMBL, Open Targets
4. Set up monitoring (Datadog, Sentry)

---

#### Scenario 3: Interactive Drug Discovery Platform (Biotech Startup)

**Context**: Scientists using chat interface to explore drug-target interactions.

**Queries**:
- "Explain how Palovarotene works in FOP"
- "Find kinase inhibitors for EGFR"
- "Compare Gefitinib vs Erlotinib"

**Characteristics**:
- Interactive (real-time chat)
- Mixed complexity (simple + complex queries)
- Users want conversational output
- Need to pivot mid-query ("actually, check RARG instead")

**Recommendation**: **Skill**

**Reasoning**:
- Conversational (feels natural in chat UI)
- Flexible (can pivot mid-query)
- Fast (no supervisor overhead)
- Simpler to deploy (single skill file)

**But consider**:
- Add phase progress UI ("Currently in Phase 3: Expansion...")
- Cache MCP tool results (avoid redundant API calls)
- Add "save as report" feature (export conversation to PDF)

---

#### Scenario 4: Knowledge Graph Construction (Data Platform)

**Context**: Batch job building knowledge graph from PubMed + trials + drugs.

**Queries**:
- Process 10,000 PMIDs per night
- Extract gene → drug → disease relationships
- Persist to Neo4j via Graphiti

**Characteristics**:
- Batch processing (overnight jobs)
- Fixed workflow (Phase 1-6 every time)
- Output MUST be persisted (to Neo4j)
- No human in the loop

**Recommendation**: **DeepAgents (with fixes and extensions)**

**Reasoning**:
- Structured output (phase files + Graphiti persistence)
- Parallel execution (critical for 10K PMIDs)
- Checkpointing (resume if job fails mid-batch)
- Tool isolation (prevent LLM from accessing Neo4j credentials)

**Required extensions**:
1. Add batch processing to specialists
2. Implement checkpoint/resume logic
3. Add rate limiting for MCP tools (protect APIs)
4. Add Graphiti persistence to Phase 6

---

#### Scenario 5: Regulatory Submission (FDA NDA)

**Context**: Generating evidence package for FDA submission.

**Queries**:
- "Validate all claims in Section 2.7.3 of NDA"
- "Find supporting trials for efficacy claim X"
- "Cross-reference drug mechanisms across databases"

**Characteristics**:
- Audit trail required (21 CFR Part 11)
- Reproducibility critical (must be able to regenerate exact output)
- No tolerance for errors (every claim must be validated)
- Timestamped, signed outputs

**Recommendation**: **DeepAgents (hardened for compliance)**

**Reasoning**:
- Structured output (phase files with timestamps)
- Audit trail (every tool call logged, signed)
- Reproducibility (phase files = provenance)
- Tool isolation (only approved tools can be used)
- Validation specialist (Phase 5) enforces fact-checking

**Required hardening**:
1. Add digital signatures to phase files
2. Implement role-based access control (only authorized specialists)
3. Add tool call approval workflow (human-in-the-loop)
4. Disable web search (only approved APIs)
5. Add compliance metrics (track source reliability)

---

### Summary Table

| Scenario | Recommendation | Why |
|----------|----------------|-----|
| Academic research | Skill | Flexibility, simplicity, low cost |
| Clinical trial matching | DeepAgents | Structured output, audit trail, batch |
| Interactive platform | Skill | Conversational, fast, flexible |
| Knowledge graph | DeepAgents | Batch, persistence, parallelization |
| FDA submission | DeepAgents (hardened) | Compliance, audit trail, reproducibility |

---

### General Guidelines

**Use Skill when**:
- Exploratory queries (no fixed workflow)
- Interactive users (chat interface)
- Simple queries (1-3 phases)
- Budget-conscious (minimize LLM calls)
- Fast iteration needed (no specialist overhead)

**Use DeepAgents when**:
- Fixed workflow (same phases every time)
- Batch processing (1000s of queries)
- Machine-readable output (JSON, graph)
- Audit requirements (compliance, provenance)
- Complex queries (all 6 phases)

---

## Final Verdict

### The skill avoided file creation failures because it doesn't create files.

**This is true but misses the deeper insight**:

The skill and DeepAgents serve **different purposes**:
- **Skill**: Conversational AI for research (human consumption)
- **DeepAgents**: Structured pipeline for production (machine consumption)

**Both are valid and complementary.**

### Which is "better"?

**There is no universal answer.** It depends on:
1. Use case (exploration vs production)
2. Users (researchers vs systems)
3. Output format (conversation vs JSON)
4. Reliability needs (flexibility vs auditability)

### What should we do next?

**1. Fix DeepAgents file creation bug** (HIGH PRIORITY)
```python
# In apps/api/lifesciences.py
from deepagents.middleware.filesystem import FilesystemMiddleware

# Add to each specialist
anchor_specialist = create_deep_agent(
    tools=[query_lifesciences, query_pubmed, think_tool, write_file],  # ADD write_file
    ...
)
```

**2. Test file creation fix** (CRITICAL)
- Run same FOP query
- Verify all 8 files created
- Check file contents for correctness

**3. Add error handling to DeepAgents** (MEDIUM PRIORITY)
- ChEMBL fallback: Use Open Targets `knownDrugs` as primary
- Open Targets: Add retry logic + format validation
- Specialist failures: Add graceful degradation (continue with partial results)

**4. Add skill-like flexibility to DeepAgents** (LOW PRIORITY)
- Allow specialists to skip phases if not needed
- Add "exploratory mode" where file creation is optional
- Add web search to Phase 5 (validation) for gaps

**5. Add DeepAgents-like structure to Skill** (OPTIONAL)
- Add phase progress indicators
- Add checkpoint file writes (optional)
- Add tool usage metrics

---

## Conclusion

**The comparison revealed complementary strengths**:
- **Skill**: Simple, fast, flexible, conversational
- **DeepAgents**: Structured, parallel, auditable, production-ready

**The 50% file failure in DeepAgents is a bug, not a design flaw.** Once fixed, DeepAgents is the better choice for production pipelines.

**But the skill is still valuable** for exploratory research, interactive chat, and rapid prototyping.

**Recommendation**: Maintain both approaches:
- Use Skill for CLI/chat interface
- Use DeepAgents for API/batch interface
- Share the same MCP tools and protocol logic (Fuzzy-to-Fact)
