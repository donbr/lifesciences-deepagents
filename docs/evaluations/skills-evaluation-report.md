# Life Sciences Skills — Evaluation Report

**Date**: 2026-02-07
**Scope**: All 6 `.claude/skills/lifesciences-*` skill definitions
**Baseline**: ACVR1/FOP retrospective + production code analysis

---

## 1. Executive Summary

The life sciences Claude Code skills underwent a comprehensive 3-agent evaluation:
1. **Behavioral Audit** analyzed what Claude actually does vs what skills instruct
2. **Consistency Analysis** compared skills against the production `apps/api/` implementation
3. **Skills Rewrite** applied findings to improve all 6 skills

**Core finding**: Claude Code frequently ignores the directive to use MCP tools for entity resolution, instead answering from parametric knowledge. This leads to hallucinated entities, inconsistent CURIEs, and ungrounded claims. The root cause is that skills were structured as **reference cards** (API endpoint catalogs) rather than **enforced workflows** with mandatory tool-use gates.

**Changes made**: All 6 skills were rewritten to enforce a disciplined LOCATE → RETRIEVE pattern with explicit grounding rules, aligned with Anthropic's official guidance on hallucination reduction, skill authoring, and tool use.

---

## 2. Behavioral Audit Results

### Key Findings

**Pattern 1 — Parametric Knowledge Override**: All 6 skills were vulnerable to Claude answering from training knowledge instead of calling tools. The skills provided curl examples but never said "you MUST call this before answering."

**Pattern 2 — Reference Card vs Workflow**: 4 of 6 skills (genomics, proteomics, pharmacology, clinical) were structured as reference cards with no workflow enforcement. Only CRISPR had a strong 5-phase pipeline.

**Pattern 3 — CURIE Inconsistency**: No skill produced consistent CURIEs. Formats varied between bare IDs and full CURIEs within the same document.

### Hallucination Risk Before Changes

| Skill | Risk Level | Reason |
|-------|------------|--------|
| genomics | HIGH | All facts available in parametric knowledge |
| proteomics | HIGH | Common proteins well-known |
| pharmacology | HIGH | Drug names/mechanisms widely known |
| clinical | MEDIUM | GraphQL requires specific IDs (forces some tool use) |
| crispr | LOW | ORCS data is obscure enough to force API calls |
| graph-builder | HIGH | Amplifies upstream hallucination risks |

### ACVR1/FOP Trace Analysis (Observed Failures)

| Phase | Expected | Observed | Root Cause |
|-------|----------|----------|------------|
| ANCHOR | HGNC LOCATE → RETRIEVE | Partial — over-resolved drugs | No scope boundaries |
| ENRICH | UniProt RETRIEVE | Used PubMed narrative instead | No mandatory tool-use gate |
| EXPAND | STRING RETRIEVE | Incomplete — missed pathway components | No RETRIEVE verification |
| DRUGS | Open Targets LOCATE | Returned agonists (wrong drugs for FOP) | No mechanism filter |
| TRIALS | ClinicalTrials.gov LOCATE | Searched wrong drugs → zero results | Cascading from DRUGS |
| VALIDATE | NCT ID RETRIEVE | Hallucinated NCT ID from prompt example | No grounding enforcement |
| PERSIST | Graphiti add_memory | Failed — tools=[] | Production bug (unrelated) |

Full audit: `docs/evaluations/behavioral-audit.md`

---

## 3. Consistency Analysis Results

### Skills ↔ Production Alignment (Before Changes)

| Dimension | Score (0-4) | Notes |
|-----------|------------|-------|
| Phase naming | 4 | Near-perfect match |
| Tool invocation syntax | 1 | Skills used dot notation; production uses `query_lifesciences()` |
| CURIE format | 1 | Systematic disagreement on 5 of 9 entity types |
| Workflow steps | 2 | Phase mapping exists but skills span multiple production phases |
| Fallback patterns | 1 | Critical Open Targets fallback missing from skills |
| Error recovery | 0 | Absent from both |
| Rate limits | 2 | Some match, some significantly different |
| Tool assignment | 3 | Production has correct tools per specialist |

**Overall**: 14/32 (44%) alignment

### Critical Gaps Found

1. **Pharmacology skill had NO Open Targets fallback** — the primary drug discovery mechanism in production
2. **UniProt CURIE format disagreement**: Skill used `UniProtKB:P04637`, production used `P04637` (bare)
3. **ChEMBL CURIE format disagreement**: Skill used `CHEMBL:3137309`, production used `CHEMBL3137309` (bare)
4. **ChEMBL rate limit**: Skill said 100 req/s; production throttles to ~2 req/s
5. **ClinicalTrials.gov**: `filter.studyType` documented in skills but invalid in v2 API
6. **Open Targets pagination**: Missing `index: 0` in several skill examples

Full analysis: `docs/evaluations/consistency-analysis.md`

---

## 4. Changes Made

### Change 1: Grounding Rule (All 6 Skills)

Added explicit external knowledge restriction per [Anthropic hallucination reduction guidance](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations):

```
All [entity type] MUST come from API results. Do NOT provide [entity type]
from training knowledge. If a query returns no results, report "No results found."
```

**Rationale**: Anthropic's guidance states: *"Explicitly instruct Claude to only use information from provided documents [tools] and not its general knowledge."*

### Change 2: LOCATE → RETRIEVE Discipline (All 6 Skills)

Converted reference cards to workflows with explicit two-step SOA terminology:

- **LOCATE**: Fuzzy search to find candidate IDs
- **RETRIEVE**: Get full record by canonical ID

Every curl example and API call is now labeled as either LOCATE or RETRIEVE.

**Rationale**: Per [Anthropic tool use guidance](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview): *"Before calling a tool, do some analysis. First, think about which tool is relevant..."*

### Change 3: Chain-of-Thought Tool Selection (Graph-Builder)

Added mandatory pre-tool reasoning to the orchestrator skill:

```
Before each tool call, briefly state:
1. What information I need
2. Which tool will provide it (LOCATE or RETRIEVE)
3. What parameters I'll use
4. What I expect to get back
```

**Rationale**: Anthropic recommends chain-of-thought prompting before tool calls to prevent incorrect tool selection.

### Change 4: Checklist Workflow (Graph-Builder)

Replaced implicit phase descriptions with a checklist per [Anthropic skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

```
## Fuzzy-to-Fact Execution Checklist
- [ ] Phase 1 ANCHOR: LOCATE gene/drug/disease → RETRIEVE canonical CURIEs
- [ ] Phase 2 ENRICH: RETRIEVE metadata for each CURIE
...
```

### Change 5: CURIE Format Conventions (Graph-Builder + All Domain Skills)

Introduced explicit two-context rule:
- **API arguments**: Bare IDs matching what the MCP server/API accepts
- **Graph node IDs**: Full CURIEs for Graphiti persistence

Added "ID Format Reference" tables to all 6 skills showing both formats.

### Change 6: Open Targets Fallback (Pharmacology)

Added Open Targets `knownDrugs` GraphQL as the PRIMARY drug discovery mechanism, with ChEMBL as secondary. This matches the production architecture.

### Change 7: API Reliability & Fallback Tables (Graph-Builder, Pharmacology)

Added explicit fallback patterns:
| Primary | Fallback | When |
|---------|----------|------|
| ChEMBL detail | Open Targets `knownDrugs` | On 500 error |
| STRING network | BioGRID interactions | <3 interactions |
| Drug+disease trial search | Disease-only search | Zero results |

### Change 8: ClinicalTrials.gov v2 Fixes (Clinical)

- Documented that `filter.studyType` is NOT valid in v2 API
- Added correct syntax: `query.term=AREA[StudyType]INTERVENTIONAL`
- Added valid parameters table

### Change 9: Gain-of-Function Disease Filter (Graph-Builder, Pharmacology)

Added mechanism filtering guidance for diseases caused by protein overactivation:
- INCLUDE: inhibitors, antagonists, negative modulators
- EXCLUDE: agonists, positive modulators, activators

This directly addresses the ACVR1/FOP failure where agonists were returned.

---

## 5. Before/After Comparison

### Graph-Builder SKILL.md

| Aspect | Before | After |
|--------|--------|-------|
| Grounding rule | None | Explicit external knowledge restriction |
| LOCATE→RETRIEVE | Implicit (code comments) | Explicit two-step discipline with labels |
| Chain-of-thought | None | Mandatory pre-tool reasoning |
| Workflow structure | Phase descriptions | Checklist with checkboxes |
| CURIE format | Defined but contradictory | Two-context rule (API args vs graph IDs) |
| Fallback patterns | Open Targets mentioned | Formal fallback table |
| Mechanism filtering | None | Gain-of-function disease filter |
| Tool invocation syntax | Dot notation (`hgnc.search_genes`) | `query_lifesciences()` wrapper syntax |

### Domain Skills (Genomics, Proteomics, Pharmacology, Clinical, CRISPR)

| Aspect | Before | After |
|--------|--------|-------|
| Structure | Reference card | Workflow with LOCATE/RETRIEVE labels |
| Grounding rule | None | Per-skill external knowledge restriction |
| ID format documentation | Inconsistent/missing | ID Format Reference tables |
| Fallback patterns | None | Explicit fallback tables (where applicable) |
| Rate limits | Some incorrect | Aligned with production |
| ClinicalTrials.gov filters | Included invalid params | Fixed with valid v2 parameters |

---

## 6. Estimated Improvement (ACVR1/FOP Regression Test)

Based on the changes, here's how the ACVR1/FOP test case would likely score:

| Phase | Before Score | After Score (Expected) | Key Change |
|-------|-------------|------------------------|------------|
| ANCHOR | 2/4 | 3/4 | Grounding rule prevents scope creep |
| ENRICH | 1/4 | 3/4 | Mandatory RETRIEVE steps for structured metadata |
| EXPAND | 2/4 | 3/4 | RETRIEVE labels for pathway components |
| DRUGS | 0/4 | 3/4 | Mechanism filter + Open Targets as primary |
| TRIALS | 0/4 | 2/4 | Disease-only fallback search |
| VALIDATE | 0/4 | 3/4 | Grounding rule prevents hallucination injection |
| PERSIST | 0/4 | N/A | Requires production bug fix (tools=[]) |
| **Total** | **5/24** | **17/24** | **+12 points** |

---

## 7. Remaining Gaps & Next Steps

### Not Addressed in This Round

1. **Production code changes**: The `persist_to_graphiti` bug (`lifesciences.py:132, tools=[]`) requires a production code fix, not a skill change
2. **Multishot examples**: Anthropic recommends 3-5 worked examples per prompt; skills currently have 0-1. Adding these would further improve tool-use compliance
3. **Formal JSON schemas**: `<output_format>` sections in production prompts use informal JSON; formal schemas would improve output compliance
4. **Error recovery in production supervisor**: The supervisor prompt (`lifesciences.py:45-77`) still lacks error recovery routing
5. **Inter-phase data passing**: Production supervisor still relies on the LLM to relay CURIEs between phases; filesystem-based passing would be more reliable

### Recommended Next Steps

1. **Fix production bug**: `lifesciences.py:132` → `"tools": [persist_to_graphiti]`
2. **Add multishot examples** to all specialist prompts in `prompts.py`
3. **Run all 3 test cases** from `docs/evaluations/test-protocol.md` and record scores
4. **Add error recovery** to supervisor prompt for cascading failures
5. **Consider filesystem-based data passing** for inter-phase CURIEs

---

## 8. Sources

### Anthropic Official Documentation
- [Reduce Hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) — "Explicitly instruct Claude to only use information from provided documents and not its general knowledge"
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Workflow checklists, feedback loops, consistent terminology, progressive disclosure, keep SKILL.md under 500 lines
- [Tool Use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — Chain-of-thought tool selection, tool_choice parameter
- [Multishot Prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting) — "3-5 diverse examples = better performance"

### Project Documentation
- ACVR1/FOP Retrospective: `docs/retrospectives/acvr1-fop-fuzzy-to-fact-retrospective.md`
- Prior Art Patterns: `reference/prior-art-api-patterns.md` (BTE-RAG, TRAPI, W3C CURIE Syntax)
- Production Code: `apps/api/shared/prompts.py`, `apps/api/graphs/lifesciences.py`

### Evaluation Artifacts
- Test Protocol: `docs/evaluations/test-protocol.md`
- Behavioral Audit: `docs/evaluations/behavioral-audit.md`
- Consistency Analysis: `docs/evaluations/consistency-analysis.md`
