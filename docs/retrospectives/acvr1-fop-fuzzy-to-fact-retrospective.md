# Retrospective: ACVR1/FOP Fuzzy-to-Fact Protocol Execution

**Query**: "What drugs target the ACVR1 pathway in FOP?"
**Date**: 2026-02-07
**Execution Time**: ~3.5 minutes (01:16:49 — 01:20:15 UTC)
**Model**: openai:gpt-4o (lifesciences.py:38)
**Trace**: `traces/65888641-a6f7-4d44-9a7c-09e9e9a292fa.json`

---

## 1. Executive Summary

The ACVR1/FOP execution exposed **systemic issues** across the Fuzzy-to-Fact pipeline — not isolated tool failures, but architectural gaps in inter-phase data passing, tool assignment, CURIE format standardization, and error recovery. Of seven phases, only one (ANCHOR) produced partially correct output. The execution missed both gold-standard drug candidates (Palovarotene, Garetosmab) and instead returned clinically inappropriate agonists (Eptotermin Alfa, Dibotermin Alfa) that would *worsen* FOP. No knowledge graph was persisted to Graphiti due to a tool wiring bug.

**Root causes** (ordered by impact):
1. **Supervisor data passing failure** — CURIEs not relayed between phases; subagents received natural language summaries instead of structured IDs
2. **persist_to_graphiti never assigned** to any specialist (`lifesciences.py:132`, `tools: []`)
3. **CURIE format inconsistencies** across prompts, mcp.py, and SKILL.md
4. **No error recovery routing** — supervisor marches through all phases regardless of upstream failures
5. **No output format compliance** — zero specialists returned structured JSON as specified

**P1 fixes** (3 code changes) would address issues #1, #2, and #4. Estimated effort: <2 hours.

---

## 2. Phase-by-Phase Execution Audit

### Phase 1: ANCHOR — Entity Resolution
**Rating**: PARTIAL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[query_lifesciences, query_pubmed, think_tool]` — correct |
| Prompt-Tool Alignment | Good — references correct tool names |
| ID Format | Correct — uses bare strings for search, outputs CURIEs |

**What happened**: Resolved ACVR1 to `HGNC:171` correctly via `hgnc_search_genes`. However, the specialist overreached by also resolving Saracatinib (`CHEMBL:217092`) and clinical trial IDs — scope that belongs to TRAVERSE_DRUGS (Phase 4a). The supervisor then passed entity *names* (not CURIEs) to the ENRICH specialist, violating the data-passing instructions at `lifesciences.py:62-64`.

**Evidence**: Trace line 126 shows supervisor task description: *"Enrich the identified entities (ACVR1, Fibrodysplasia Ossificans Progressiva, Saracatinib)..."* — names only, no CURIEs.

### Phase 2: ENRICH — Metadata Enrichment
**Rating**: PARTIAL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[query_lifesciences, query_pubmed, think_tool]` — correct |
| Prompt-Tool Alignment | Good but CURIE format issue (see Section 4) |
| ID Format | `uniprot_id: "Q04771"` — bare ID, inconsistent with SKILL.md |

**What happened**: Instead of calling `hgnc_get_gene` (to get UniProt/Ensembl cross-references) and `uniprot_get_protein` (for functional descriptions), the specialist relied on `query_pubmed` for literature-based enrichment. This returned narrative text about FOP pathophysiology but **failed to extract** the Ensembl ID (`ENSG00000115170`) needed by TRAVERSE_DRUGS for Open Targets queries.

**Impact**: Downstream phases were starved of the Ensembl ID. The TRAVERSE_DRUGS specialist could not construct the precise Open Targets GraphQL query.

### Phase 3: EXPAND — Network Expansion
**Rating**: PARTIAL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[query_lifesciences, think_tool]` — correct |
| Prompt-Tool Alignment | Good — STRING, WikiPathways, BioGRID all accessible |
| ID Format | Consistent (bare STRING IDs match mcp.py) |

**What happened**: WikiPathways returned 3 pathways (WP2857 Mesodermal Commitment, WP3931, WP5473). BioGRID returned genetic interactions. However, STRING interaction partners were not fully retrieved — the specialist noted "specific interaction partners from STRING weren't retrieved." **WikiPathways `get_pathways_for_gene`** was called but `get_pathway_components` was **not**, meaning BMP pathway member genes (SMAD1, BMPR1A) were never enumerated for drug targeting.

### Phase 4a: TRAVERSE_DRUGS — Drug Discovery
**Rating**: FAIL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[query_lifesciences, query_api_direct, think_tool]` — correct |
| Prompt-Tool Alignment | Good — ChEMBL + Open Targets fallback documented |
| ID Format | Correct for Open Targets GraphQL |

**What happened**: Used Open Targets `knownDrugs` via `query_api_direct` (correct fallback pattern). Returned **Eptotermin Alfa** and **Dibotermin Alfa** — both ACVR1 *agonists* used for bone healing. These ACTIVATE the ACVR1/BMP pathway, which is the pathological mechanism in FOP. FOP requires pathway *inhibition*, not activation. The specialist failed to distinguish agonist vs antagonist mechanisms in the disease context.

**Gold standard drugs missed**: Palovarotene (RARgamma agonist, FDA-approved for FOP), Garetosmab (anti-Activin A antibody, Phase 2/3), LDN-193189 (ACVR1 inhibitor, preclinical).

**Additional issue**: Phases 4a and 4b ran sequentially despite the supervisor prompt (`lifesciences.py:54-57`) explicitly allowing parallel execution.

### Phase 4b: TRAVERSE_TRIALS — Clinical Trial Discovery
**Rating**: FAIL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[query_lifesciences, query_api_direct, think_tool]` — correct |
| Cascading failure | Searched for wrong drugs from Phase 4a |

**What happened**: Searched for trials of Eptotermin Alfa and Dibotermin Alfa in FOP — found zero results (correct, as these drugs are not studied for FOP). The specialist did not attempt a disease-only search (`query_lifesciences(query="fibrodysplasia ossificans progressiva", tool_name="clinicaltrials_search_trials")`) which would have found Palovarotene Phase 3 trials (NCT03312634, NCT02190747).

### Phase 5: VALIDATE — Fact Verification
**Rating**: FAIL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[query_lifesciences, query_pubmed, think_tool]` — correct |
| Hallucination injection | Introduced entities not from upstream |

**What happened**: The validator tested `NCT03312634` and `CHEMBL1234` — IDs not present in any upstream phase output. `CHEMBL1234` is a placeholder from the prompt example. The specialist also introduced "Palovarotene" from its own parametric knowledge, not from pipeline data. Found PubMed confirmation (PMID:39451784) that Palovarotene is approved for FOP, but this was a hallucination-injection rather than validation of upstream claims.

### Phase 6: PERSIST — Graph Persistence
**Rating**: FAIL

| Aspect | Assessment |
|--------|-----------|
| Tools Assigned | `[]` (empty) — **BUG** (`lifesciences.py:132`) |
| Prompt-Tool Mismatch | `PERSIST_SYSTEM` references `persist_to_graphiti` (prompts.py:473-479) |

**What happened**: The specialist attempted to call Graphiti but had no tools available. Returned: *"There seems to be a persistent issue with connecting to Graphiti."* This error message is misleading — it suggests a connectivity problem, not a configuration bug. The **supervisor** then generated the final summary itself (trace line 399), violating the architecture principle that the supervisor only routes.

**Root cause**: `persist_to_graphiti` is imported at `lifesciences.py:24` but never added to any specialist's tool list.

---

## 3. Tier Discipline Analysis

The architecture defines three tiers (SKILL.md:13-35, prior-art-api-patterns.md:291-318):

| Tier | Purpose | Implementation | Status |
|------|---------|---------------|--------|
| **Tier 1: MCP Tools** | Verified node retrieval | `query_lifesciences` | UNDERUTILIZED — ENRICH fell back to PubMed narrative |
| **Tier 2: Direct API** | Relationship edges / fallback | `query_api_direct` | CORRECTLY USED — Open Targets GraphQL worked |
| **Tier 3: Graphiti** | Knowledge graph persistence | `persist_to_graphiti` | BROKEN — tool not wired to any specialist |

### Discipline Violations

1. **ANCHOR scope creep**: Resolved drugs and trial IDs in Phase 1 (belongs in Phases 4a/4b)
2. **ENRICH tier demotion**: Used Tier 2 (PubMed literature) instead of Tier 1 (structured MCP `hgnc_get_gene` + `uniprot_get_protein`) for metadata enrichment
3. **Supervisor synthesized output**: Generated final answer instead of routing to persistence_specialist — broke the "supervisor delegates only" principle
4. **No output format compliance**: All seven specialists returned free-form text, not the structured JSON specified in their `<output_format>` sections

---

## 4. CURIE Format & ID Resolution Patterns

Three documentation layers define ID formats, and they contradict each other:

| Tool | mcp.py Docstring | prompts.py Example | SKILL.md Example | Consistent? |
|------|------------------|-------------------|------------------|-------------|
| `hgnc_get_gene` | `"HGNC:..."` | `"HGNC:171"` | `"HGNC:11998"` | YES |
| `uniprot_get_protein` | `"P12345"` (bare) | `"Q04771"` (bare) | `"UniProtKB:P04637"` (CURIE) | **NO** |
| `chembl_get_compound` | `"CHEMBL..."` (bare) | `"CHEMBL25"` (bare) | `"CHEMBL:3137309"` (CURIE) | **NO** |
| `string_get_interactions` | `"..."` (unspecified) | `"9606.ENSP..."` (bare) | `"STRING:9606.ENSP..."` / bare (both) | **NO** |
| `ensembl_get_gene` | `"ENSG..."` (bare) | `"ENSG00000115170"` (bare) | `"ENSG00000141510"` (bare) | YES |
| `pubchem_get_compound` | `"PubChem:CID..."` | (none) | (none) | INDETERMINATE |
| `entrez_get_gene` | `"NCBIGene:..."` | (none) | (none) | INDETERMINATE |
| `biogrid_get_interactions` | `"TP53"` (symbol) | `"ACVR1"` (symbol) | (none) | YES |

**Root cause**: Conflation of two contexts — API call arguments (what the FastMCP server accepts) vs graph node IDs (canonical CURIEs for Graphiti persistence). The W3C CURIE standard (prior-art-api-patterns.md:157-159) defines `PREFIX:LOCAL_ID`, but FastMCP passes arguments as raw dictionaries without CURIE validation (confirmed via Context7 FastMCP docs).

**SKILL.md self-contradiction**: STRING ID format appears as both `"STRING:9606.ENSP00000269305"` (SKILL.md:67) and `"9606.ENSP00000269305"` (SKILL.md:174) within the same document.

---

## 5. API Reliability & Fallback Patterns

### Reliability Reassessment

| API | Documented | Observed | Reassessment |
|-----|-----------|----------|-------------|
| ChEMBL search | "Frequently 500s" | `chembl_search_compounds` succeeded | **Overstated** — search endpoints use Elasticsearch (resilient); detail endpoints hit primary DB (prone to 500s) |
| ChEMBL detail | "Frequently 500s" | Not tested in this execution | Remains valid for `chembl_get_compound` |
| Open Targets | "Reliable" | `knownDrugs` returned results correctly | **Confirmed** reliable |
| STRING | "Batch returns names; single doesn't" | Single query lacked partner names | **Confirmed** |
| ClinicalTrials.gov | "Stable" | MCP search worked; `filter.studyType` returned 400 | **filter.studyType is NOT a valid v2 parameter** |

### Documented vs Missing Fallbacks

| Primary | Documented Fallback | Status |
|---------|-------------------|--------|
| ChEMBL | Open Targets `knownDrugs` | DOCUMENTED, TESTED |
| STRING | (none) | **MISSING** — BioGRID + Open Targets `associatedTargets` could substitute |
| UniProt | (none) | **MISSING** — Ensembl xrefs + PubMed could partially substitute |
| WikiPathways | (none) | **MISSING** — STRING enrichment endpoint could substitute |

### ClinicalTrials.gov v2 Filter Fix

The `filter.studyType=INTERVENTIONAL` parameter does not exist in the v2 API. Valid parameters found in the codebase (SKILL.md:117, 173, 193):
- `query.cond`, `query.intr`, `query.term` — search parameters
- `filter.overallStatus` — status filter (e.g., `RECRUITING`)
- `pageSize`, `format` — pagination/format

To filter by study type, use: `query.term=AREA[StudyType]INTERVENTIONAL`

---

## 6. Tool Assignment Gap Analysis

### Tool Assignment Matrix

| Specialist | Assigned Tools | Missing Tools | Unused Imports | Evidence |
|------------|---------------|---------------|----------------|----------|
| anchor_specialist | `query_lifesciences`, `query_pubmed`, `think_tool` | — | — | Correct |
| enrichment_specialist | `query_lifesciences`, `query_pubmed`, `think_tool` | — | — | Correct (tools adequate, but specialist used wrong ones) |
| expansion_specialist | `query_lifesciences`, `think_tool` | `query_pubmed` (backup) | — | Literature fallback would help when STRING returns <3 interactions |
| traversal_drugs_specialist | `query_lifesciences`, `query_api_direct`, `think_tool` | — | — | Correct |
| traversal_trials_specialist | `query_lifesciences`, `query_api_direct`, `think_tool` | — | — | Correct |
| validation_specialist | `query_lifesciences`, `query_pubmed`, `think_tool` | — | — | Correct |
| persistence_specialist | `[]` (empty) | **`persist_to_graphiti`** | — | **BUG**: imported at `lifesciences.py:24`, never assigned |

### Imported but Unused

`persist_to_graphiti` is imported at `lifesciences.py:24`:
```python
from shared.mcp import query_lifesciences, query_api_direct, persist_to_graphiti, query_pubmed
```
It is never referenced in any subagent's `tools` list. This is the only unused import.

---

## 7. Prompt Engineering Assessment

### Structural Quality

All seven specialist prompts use a consistent five-tag XML schema: `<role>`, `<protocol>`, `<pitfalls>`, `<reasoning>`, `<output_format>`. This aligns with Anthropic's guidance to use consistent, semantic XML tag names (platform-docs: "Use XML tags to structure prompts").

**Gaps identified**:
1. **Supervisor prompt uses NO XML tags** (`lifesciences.py:45-77`) — plain text with Markdown headers, inconsistent with specialist design
2. **No multishot examples** — Anthropic recommends 3-5 diverse examples per prompt; current prompts have zero worked examples showing multi-step tool invocation sequences
3. **No error recovery section** — supervisor lacks guidance for handling partial results, cross-phase dependency failures, or circuit-breaker logic
4. **No formal JSON schema** — `<output_format>` sections use informal JSON examples rather than validated schemas

### Pitfall Documentation Quality

The `<pitfalls>` sections are among the strongest prompt features. Each contains operationally specific guidance from real API behavior. The TRAVERSE_DRUGS pitfalls section is exemplary: *"Do NOT retry more than once — switch to Open Targets fallback"* with a concrete cutoff.

**Key gap**: No pitfall addresses the agonist/antagonist distinction critical for gain-of-function diseases like FOP.

---

## 8. Architecture Alignment with Prior Art

### BTE-RAG Pattern (Callaghan et al., 2023; Xu et al., 2025)

BTE-RAG achieves 75.8% accuracy by federating 61 biomedical APIs with semantic annotations for API chaining. The Fuzzy-to-Fact protocol aligns well with BTE-RAG's core principle — structured API access outperforms unstructured text retrieval (prior-art-api-patterns.md:399-402).

**Gap**: BTE-RAG's ID-to-object translation automatically handles CURIE transformations between APIs. The lifesciences agent relies on the LLM to manually manage ID formats across phases, which proved unreliable.

### TRAPI Standard (NCATS Translator)

TRAPI requires CURIEs for all identifiers and structured JSON responses (prior-art-api-patterns.md:110-118). The lifesciences agent partially aligns:
- CURIE output format is defined but inconsistently enforced (see Section 4)
- Structured JSON responses are specified in `<output_format>` but never produced by the LLM
- No formal `ErrorEnvelope` with recovery hints at the subagent level

### DeepAgents Pattern Alignment

The reference implementation at `reference/deepagents/examples/deep_research/agent.py` confirms the pattern used in `lifesciences.py` — `create_deep_agent()` with `model`, `tools`, `system_prompt`, and `subagents`. Key divergences:

1. **Reference uses `FilesystemBackend`** (content-builder-agent, line 173) for persistent file I/O; lifesciences agent does not
2. **Reference gives supervisor its own tools** (deep_research/agent.py:56: `tools=[tavily_search, think_tool]`); lifesciences supervisor has `tools=[]`
3. **Reference limits concurrency** (agent.py:21: `max_concurrent_research_units = 3`); lifesciences agent has no concurrency limits

The DeepAgents `FilesystemMiddleware` provides `write_file`/`read_file` to every subagent automatically. The lifesciences agent could use this for inter-phase data passing — e.g., ANCHOR writes CURIEs to `/anchor_output.json`, supervisor tells ENRICH to `read_file("/anchor_output.json")`. This would solve the structured data passing problem without relying on the supervisor to faithfully relay CURIEs.

### Competency Question Fit

**cq1: FOP Mechanism** — *"By what mechanism does Palovarotene treat FOP?"*
- Gold standard path: `Drug(Palovarotene)` → `Protein(RARG)` → `Protein(ACVR1)` → `Disease(FOP)`
- Execution result: Palovarotene was never identified by TRAVERSE_DRUGS. RARG was never resolved. The validator hallucinated Palovarotene from parametric knowledge.
- **0/4 edges discovered through API grounding**

**cq2: FOP Drug Repurposing** — *"What drugs targeting BMP pathway could be repurposed for FOP?"*
- Gold standard: ACVR1 → BMP Pathway (WP:WP2760) → Member Genes (SMAD1, BMPR1A) → LDN-193189, Dorsomorphin
- Execution result: WikiPathways returned 3 pathways but `get_pathway_components` was never called. LDN-193189 and Dorsomorphin were never identified.
- **1/4 steps completed** (pathway identification only, no component enumeration)

---

## 9. Prioritized Recommendations

### P1 — Critical (fix before next execution)

**P1.1: Wire persist_to_graphiti to persistence_specialist**
- File: `lifesciences.py:132`
- Change: `"tools": []` → `"tools": [persist_to_graphiti]`
- Impact: Enables Tier 3 persistence; tool has built-in graceful fallback if Graphiti is down (mcp.py:410-413)
- Effort: 1 line change
- Source: Agent 1 audit, Agent 3 tool gap analysis

**P1.2: Add filesystem-based inter-phase data passing**
- File: `lifesciences.py:45-77` (supervisor prompt)
- Change: Add instruction for specialists to write structured output to files:
  ```
  CRITICAL DATA PASSING RULE:
  - After each specialist returns, extract CURIEs and structured IDs from the response
  - Include ALL CURIEs explicitly in the next specialist's task description
  - Example: "Enrich HGNC:171 (ACVR1). Get UniProt ID and Ensembl ID. The Ensembl ID is needed for Phase 4a."
  ```
- Impact: Prevents the cascading failure observed when supervisor passed names instead of IDs
- Effort: Prompt edit (~15 min)
- Source: Agent 1 audit (supervisor data passing deficiency), DeepAgents FilesystemMiddleware docs

**P1.3: Add error recovery routing to supervisor**
- File: `lifesciences.py:45-77` (supervisor prompt)
- Change: Add `<error_recovery>` section:
  ```
  ERROR RECOVERY:
  - If ENRICH fails to return an Ensembl ID, delegate to anchor_specialist with: "Resolve ACVR1 Ensembl ID via ensembl_search_genes"
  - If TRAVERSE_DRUGS returns only agonists for a gain-of-function disease, re-delegate with: "Find INHIBITORS of ACVR1, not agonists"
  - If 3+ phases return no results, skip to persistence_specialist with partial data
  ```
- Impact: Prevents blind march through failing phases; enables self-correction
- Effort: Prompt edit (~30 min)
- Source: Agent 3 Anthropic patterns analysis, platform-docs hallucination reduction guide

### P2 — Important (fix within 1 week)

**P2.1: Standardize CURIE formats across all documentation layers**
- Files: `mcp.py:221-234`, `prompts.py:226-234`, `SKILL.md:193-217`
- Change: Synchronize all three layers. Decision: mcp.py and prompts.py should match (since they're the runtime interface); SKILL.md should match them. For UniProt: standardize on bare accession (`"Q04771"`) since that's what the FastMCP server accepts, and add a comment explaining the API-vs-persistence format difference.
- Impact: Eliminates confusion about whether to send `UniProtKB:Q04771` or `Q04771`
- Effort: ~1 hour across 3 files
- Source: Agent 2 CURIE analysis, W3C CURIE Syntax 1.0 (prior-art-api-patterns.md:157)

**P2.2: Add agonist/antagonist distinction to TRAVERSE_DRUGS prompt**
- File: `prompts.py:316-360`
- Change: Add to `<pitfalls>`:
  ```
  - For GAIN-OF-FUNCTION diseases (e.g., FOP caused by constitutive ACVR1 activation), you need INHIBITORS or ANTAGONISTS.
    Do NOT return agonists — they would worsen the disease.
  - Check the "mechanismOfAction" field from Open Targets: filter for "inhibitor", "antagonist", "negative modulator".
  ```
- Impact: Prevents returning clinically inappropriate drugs
- Effort: Prompt edit (~15 min)
- Source: Agent 1 TRAVERSE_DRUGS audit, cq1/cq2 gold standard comparison

**P2.3: Add multishot examples to specialist prompts**
- Files: `prompts.py` (all 7 specialist prompts)
- Change: Add one worked `<example>` per specialist showing complete tool invocation → think_tool → output sequence
- Impact: Significantly improves output format compliance and tool usage patterns (Anthropic guidance: "3-5 diverse examples")
- Effort: ~2 hours for all 7 prompts
- Source: Agent 3 Anthropic patterns analysis, platform-docs multishot prompting guide

**P2.4: Add XML tags to supervisor prompt**
- File: `lifesciences.py:45-77`
- Change: Wrap sections in `<phases>`, `<data_passing>`, `<routing_rules>`, `<error_recovery>`
- Impact: Consistency with specialist prompts; reduces misinterpretation risk
- Effort: ~30 min
- Source: Agent 3 structural quality assessment

### P3 — Enhancement (backlog)

**P3.1: Add missing API fallback patterns**
- File: `prompts.py` (EXPAND, ENRICH prompts)
- Change: Document STRING → BioGRID fallback, UniProt → Ensembl xrefs fallback, WikiPathways → STRING enrichment fallback
- Source: Agent 2 fallback pattern recommendations

**P3.2: Add query_pubmed to expansion_specialist**
- File: `lifesciences.py:104`
- Change: `"tools": [query_lifesciences, think_tool]` → `"tools": [query_lifesciences, query_pubmed, think_tool]`
- Plus: Add PubMed fallback step to `EXPAND_SYSTEM` prompt
- Source: Agent 3 tool gap analysis

**P3.3: Fix ClinicalTrials.gov filter documentation**
- File: `prompts.py:362-404`
- Change: Add explicit list of valid v2 API parameters; note that `filter.studyType` is invalid
- Source: Agent 2 API reliability reassessment

**P3.4: Enforce structured JSON output with formal schemas**
- Files: All specialist prompts in `prompts.py`
- Change: Add `// required` field annotations, include partial-failure examples in `<output_format>`
- Source: Agent 3 Anthropic structured outputs analysis

**P3.5: Differentiate ChEMBL search vs detail reliability in documentation**
- Files: `CLAUDE.md`, `MEMORY.md`, `prompts.py`
- Change: Replace "ChEMBL frequently returns 500 errors" with "ChEMBL detail endpoints (`chembl_get_compound`) frequently return 500s; search endpoints (`chembl_search_compounds`) are generally reliable"
- Source: Agent 2 API reliability reassessment

---

## 10. Appendix: MCP Tool Call Trace

Reconstructed from `traces/65888641-a6f7-4d44-9a7c-09e9e9a292fa.json`:

| Phase | Specialist | Tool Call | Result |
|-------|-----------|----------|--------|
| 1 ANCHOR | anchor_specialist | `hgnc_search_genes("ACVR1")` | HGNC:171 resolved |
| 1 ANCHOR | anchor_specialist | `chembl_search_compounds("Saracatinib")` | CHEMBL:217092 (scope violation) |
| 2 ENRICH | enrichment_specialist | `query_pubmed(search_articles, "ACVR1 FOP")` | Literature text (should have used hgnc_get_gene) |
| 3 EXPAND | expansion_specialist | `wikipathways_get_pathways_for_gene("ACVR1")` | WP2857, WP3931, WP5473 |
| 3 EXPAND | expansion_specialist | `biogrid_get_interactions("ACVR1")` | Genetic interactions returned |
| 3 EXPAND | expansion_specialist | `string_search_proteins("ACVR1")` | STRING ID resolved but interactions incomplete |
| 4a TRAVERSE | traversal_drugs_specialist | Open Targets GraphQL via `query_api_direct` | Eptotermin Alfa, Dibotermin Alfa (agonists — wrong) |
| 4b TRAVERSE | traversal_trials_specialist | `clinicaltrials_search_trials(...)` | Zero results (searched for wrong drugs) |
| 5 VALIDATE | validation_specialist | `clinicaltrials_get_trial("NCT03312634")` | Tested hallucinated ID |
| 6 PERSIST | persistence_specialist | (no tools available) | Failed — tools=[] |

---

## 11. Appendix: Grounding Sources

### MCP Documentation Queries (9 total)

| # | MCP Server | Query | Key Finding |
|---|-----------|-------|-------------|
| 1 | docs-langchain | "DeepAgents create_deep_agent SubAgentMiddleware tool isolation" | Confirmed subagents are stateless; task description is only input |
| 2 | docs-langchain | "LangGraph supervisor routing stateless delegation pattern" | FilesystemMiddleware available for inter-phase data; not used |
| 3 | docs-langchain | "DeepAgents middleware stack FilesystemMiddleware TodoListMiddleware" | Auto-attached to all subagents; can write/read files for data passing |
| 4 | platform-docs | "tool use best practices structured outputs" (Anthropic) | Detailed tool descriptions are "most important factor"; multishot examples recommended |
| 5 | platform-docs | "agent error handling recovery retry patterns" (Anthropic) | "Allow Claude to say I don't know" reduces hallucination; is_error flag for tool errors |
| 6 | platform-docs | "FastMCP tool parameter validation input types" | FastMCP supports Pydantic Field validation but uses flexible mode by default |
| 7 | platform-docs | "structured output JSON format prompting" (LangChain) | Formal JSON schemas more reliable than informal examples |
| 8 | Context7 | FastMCP → "tool argument validation CURIE format" | Arguments passed as raw dicts; no built-in CURIE validation; strict mode available |
| 9 | Context7 | LangGraph → "subgraph tool assignment agent routing" | Supervisor pattern with tool isolation confirmed as standard |

### Code References

| Issue | File:Line | Evidence |
|-------|-----------|----------|
| `persist_to_graphiti` not in persistence_specialist tools | `lifesciences.py:132` | `tools: []` but PERSIST_SYSTEM references the tool |
| `persist_to_graphiti` imported but unused | `lifesciences.py:24` | `from shared.mcp import ... persist_to_graphiti ...` |
| UniProt CURIE format inconsistency | `prompts.py:230` vs `SKILL.md:57` | `"Q04771"` (bare) vs `"UniProtKB:P04637"` (CURIE) |
| ChEMBL CURIE format inconsistency | `mcp.py:223` vs `SKILL.md:199` | `"CHEMBL..."` (bare) vs `"CHEMBL:3137309"` (CURIE) |
| STRING self-contradiction in SKILL.md | `SKILL.md:67` vs `SKILL.md:174` | `"STRING:9606.ENSP..."` vs `"9606.ENSP..."` |
| No XML tags in supervisor prompt | `lifesciences.py:45-77` | Plain text with Markdown headers |
| No error recovery in supervisor | `lifesciences.py:45-77` | Only guidance: "If a phase returns no results, note this and continue" |
| ClinicalTrials.gov invalid filter | conversation trace | `filter.studyType=INTERVENTIONAL` returns HTTP 400 |
| Parallel execution not used | conversation trace | Phases 4a and 4b ran sequentially |

### Prior Art References

- W3C CURIE Syntax 1.0 (prior-art-api-patterns.md:157-159)
- BTE-RAG accuracy improvement: 51% → 75.8% for GPT-4o mini with structured APIs (prior-art-api-patterns.md:399)
- TRAPI CURIE requirements (prior-art-api-patterns.md:110-118)
- BioThings Explorer ID-to-object translation (prior-art-api-patterns.md:181-183)
- Competency questions cq1 and cq2 gold standards (competency-questions-catalog.md:33-119)
