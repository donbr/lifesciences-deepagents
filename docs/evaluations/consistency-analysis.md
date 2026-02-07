# Consistency Analysis: Skills vs Production Implementation

## Purpose

This document compares the `.claude/skills/lifesciences-*` skill definitions against the `apps/api/` production implementation (prompts.py, lifesciences.py, mcp.py) to identify gaps, contradictions, and missing patterns.

---

## 1. Terminology Alignment

### Tool Name Mapping

| Skill Reference | Production Reference (prompts.py/mcp.py) | Match? |
|-----------------|------------------------------------------|--------|
| `hgnc.search_genes` (graph-builder:47) | `query_lifesciences(tool_name="hgnc_search_genes")` (prompts.py:187) | MISMATCH — skills use dot notation; production uses string parameter |
| `uniprot.get_protein` (graph-builder:57) | `query_lifesciences(tool_name="uniprot_get_protein")` (prompts.py:230) | MISMATCH — same dot vs string issue |
| `chembl.search_compounds` (graph-builder:84) | `query_lifesciences(tool_name="chembl_search_compounds")` (prompts.py:323) | MISMATCH — same |
| `string.get_interactions` (graph-builder:67) | `query_lifesciences(tool_name="string_get_interactions")` (prompts.py:278) | MISMATCH — same |
| `graphiti.add_memory` (graph-builder:124) | `persist_to_graphiti(name=..., episode_body=...)` (mcp.py:~400) | MISMATCH — different function signature |

**Impact**: Claude Code uses the skill's dot notation syntax, which doesn't match how tools are actually invoked in the production agent. Users following skill examples would need to translate the syntax.

**Recommendation**: Skills should use the `query_lifesciences(tool_name=..., tool_args={...})` syntax to match production, OR explicitly document the translation.

### Phase Naming

| Skill Phase | Production Specialist | Prompt Constant | Match? |
|-------------|----------------------|-----------------|--------|
| Phase 1: ANCHOR | `anchor_specialist` | `ANCHOR_SYSTEM` | YES |
| Phase 2: ENRICH | `enrichment_specialist` | `ENRICH_SYSTEM` | YES |
| Phase 3: EXPAND | `expansion_specialist` | `EXPAND_SYSTEM` | YES |
| Phase 4a: TRAVERSE_DRUGS | `traversal_drugs_specialist` | `TRAVERSE_DRUGS_SYSTEM` | YES |
| Phase 4b: TRAVERSE_TRIALS | `traversal_trials_specialist` | `TRAVERSE_TRIALS_SYSTEM` | YES |
| Phase 5: VALIDATE | `validation_specialist` | `VALIDATE_SYSTEM` | YES |
| Phase 6: PERSIST | `persistence_specialist` | `PERSIST_SYSTEM` | NUMBERING: skill says "Phase 6", prod says "Phase 7" in some docs |

---

## 2. Workflow Step Mapping

### Genomics Skill ↔ ANCHOR + ENRICH Prompts

| Genomics Skill Step | ANCHOR_SYSTEM (prompts.py:179-217) | ENRICH_SYSTEM (prompts.py:219-266) | Gap? |
|---------------------|-----------------------------------|-------------------------------------|------|
| HGNC search by symbol | `query_lifesciences(query="ACVR1", tool_name="hgnc_search_genes")` | — | Aligned, but syntax differs (curl vs MCP wrapper) |
| HGNC fetch by ID | — | `query_lifesciences(tool_name="hgnc_get_gene", tool_args={"hgnc_id": "HGNC:171"})` | Aligned |
| Ensembl lookup | Curl: `rest.ensembl.org/lookup/id/` | Not in prompts — uses `ensembl_get_gene` MCP | **GAP**: Skill uses curl, production uses MCP |
| Ensembl VEP | Curl: `rest.ensembl.org/vep/` | Not in any production prompt | **GAP**: VEP not used in production |
| NCBI E-utilities | Curl: `eutils.ncbi.nlm.nih.gov/` | `query_lifesciences(tool_name="entrez_search_genes")` in production | Partially aligned — different access method |
| Cross-references | Curl: `rest.ensembl.org/xrefs/id/` | Mentioned in VALIDATE_SYSTEM but not ENRICH | **GAP**: Useful for ENRICH, only documented for VALIDATE |

**Key gaps**:
1. Skill uses raw curl; production uses MCP wrappers — different invocation patterns
2. VEP variant annotation is in the skill but not in any production phase
3. Ensembl cross-references are useful for ENRICH but only documented in VALIDATE

### Proteomics Skill ↔ EXPAND Prompt

| Proteomics Skill Step | EXPAND_SYSTEM (prompts.py:268-314) | Gap? |
|----------------------|-------------------------------------|------|
| UniProt search | Not in EXPAND — belongs in ENRICH | **MISALIGNED**: Skill covers both ENRICH and EXPAND scope |
| UniProt get protein | Not in EXPAND — belongs in ENRICH | Same |
| UniProt batch ID mapping | Not in any production prompt | **GAP**: Not used in production |
| STRING network | `query_lifesciences(tool_name="string_search_proteins")` + `string_get_interactions` | Aligned |
| STRING enrichment | Curl: `string-db.org/api/json/enrichment` | Not in production prompts | **GAP**: Functional enrichment not used |
| BioGRID interactions | `query_lifesciences(tool_name="biogrid_get_interactions")` | Aligned |

**Key gaps**:
1. Proteomics skill spans both ENRICH and EXPAND phases — doesn't map cleanly
2. STRING functional enrichment is in the skill but not used in production
3. UniProt batch ID mapping is in the skill but not used in production

### Pharmacology Skill ↔ TRAVERSE_DRUGS Prompt

| Pharmacology Skill Step | TRAVERSE_DRUGS_SYSTEM (prompts.py:316-360) | Gap? |
|------------------------|---------------------------------------------|------|
| ChEMBL compound search | `query_lifesciences(tool_name="chembl_search_compounds")` | Aligned |
| ChEMBL mechanism | Curl: `/mechanism?molecule_chembl_id=...` | Not in prompts — production uses Open Targets instead | **GAP**: Skill emphasizes ChEMBL mechanisms; production prefers Open Targets |
| ChEMBL drug indication | Curl: `/drug_indication?...` | Not in prompts | **GAP**: Not in production |
| ChEMBL bioactivity | Curl: `/activity?...` | Not in prompts | **GAP**: Not in production |
| Open Targets fallback | Not in skill | `query_api_direct(url="opentargets.org/graphql")` | **CRITICAL GAP**: Skill omits the Open Targets fallback that production relies on |
| PubChem | Curl: `pubchem.ncbi.nlm.nih.gov/rest/pug/` | Not in production | **GAP**: PubChem not used in production |
| IUPHAR/GtoPdb | Curl: `guidetopharmacology.org/services/` | Not in production | **GAP**: IUPHAR not used in production |

**Key gaps**:
1. **CRITICAL**: Pharmacology skill has NO Open Targets fallback — this is the primary drug discovery mechanism in production
2. Skill emphasizes ChEMBL endpoints that frequently fail (500 errors)
3. PubChem and IUPHAR are documented but not used in production

### Clinical Skill ↔ TRAVERSE_TRIALS + VALIDATE Prompts

| Clinical Skill Step | TRAVERSE_TRIALS/VALIDATE (prompts.py:362-456) | Gap? |
|--------------------|------------------------------------------------|------|
| Open Targets target-disease | Not in TRAVERSE_TRIALS prompt (used in EXPAND) | **MISALIGNED**: Skill puts this in clinical; production puts it in EXPAND |
| Open Targets knownDrugs | Referenced in TRAVERSE_DRUGS prompt | **MISALIGNED**: Skill puts in clinical; production in drugs |
| ClinicalTrials.gov search | `query_lifesciences(tool_name="clinicaltrials_search_trials")` | Aligned |
| ClinicalTrials.gov details | `query_lifesciences(tool_name="clinicaltrials_get_trial")` | Aligned |
| Trial verification | VALIDATE_SYSTEM verifies NCT IDs | Aligned |

**Key gaps**:
1. Open Targets is split between clinical skill and drugs/expand in production — confusing mapping
2. Clinical skill's `filter.advanced=AREA[Phase]PHASE3` (line 121) — not well-tested; may not work reliably

### Graph-Builder Skill ↔ Supervisor + All Specialists

| Graph-Builder Feature | lifesciences.py | Gap? |
|----------------------|-----------------|------|
| 7-phase protocol | 7 specialists in `subagents` list | Aligned (skill says 7 phases, code has 7) |
| Tier 1: MCP Tools | `query_lifesciences` wrapper | Aligned conceptually, different syntax |
| Tier 2: Curl Commands | `query_api_direct` for direct HTTP | **GAP**: Skill lists curl commands; production wraps in `query_api_direct` |
| Tier 3: Graphiti | `persist_to_graphiti` | **BUG**: Imported but not wired to persistence_specialist (tools=[]) |
| Parallel Phase 4a/4b | Supervisor prompt allows it (line 54-57) | Aligned in design; observed to run sequentially |
| Data passing | Supervisor prompt mentions CURIEs | **GAP**: Skill doesn't address inter-phase data passing |
| Error recovery | Not in skill | Not in supervisor prompt | **GAP**: Missing in both |

---

## 3. CURIE Format Discrepancies

| Entity Type | Skill (graph-builder) | prompts.py | mcp.py Docstring | Consistent? |
|-------------|----------------------|------------|------------------|-------------|
| Gene (HGNC) | `HGNC:11998` | `HGNC:171` | `"HGNC:..."` | YES — all use HGNC: prefix |
| Protein (UniProt) | `UniProtKB:P04637` | `"Q04771"` (bare) | `"P12345"` (bare) | **NO** — skill uses CURIE, production uses bare |
| Compound (ChEMBL) | `CHEMBL:3137309` | `"CHEMBL25"` (bare) | `"CHEMBL..."` (bare) | **NO** — skill adds colon separator, production doesn't |
| STRING protein | `STRING:9606.ENSP00000269305` AND `9606.ENSP00000269305` | `"9606.ENSP00000263640"` (bare) | Unspecified | **NO** — skill self-contradicts, production uses bare |
| Disease (EFO) | `EFO_0000574` | Not specified | Not in mcp.py | INDETERMINATE |
| Disease (MONDO) | `MONDO_0018875` | `MONDO:0018875` | Not in mcp.py | **NO** — underscore vs colon |
| Trial (NCT) | `NCT:00461032` | `"NCT03312634"` (bare) | Not in mcp.py | **NO** — skill uses CURIE, production uses bare |
| Pathway (WikiPathways) | `WP:WP1742` | Not specified | Not in mcp.py | INDETERMINATE |
| Ensembl gene | `ENSG00000141510` (bare) | `"ENSG00000115170"` (bare) | `"ENSG..."` (bare) | YES — all use bare |

**Root cause**: The skill tries to use W3C CURIE syntax (`PREFIX:LOCAL_ID`) for graph node IDs, but the production code passes bare IDs to MCP tools (which is what the FastMCP server expects). These are two different contexts:
1. **API arguments**: Bare IDs (what the MCP server accepts)
2. **Graph node IDs**: Full CURIEs (for Graphiti persistence)

Neither the skill nor production clearly documents this distinction.

---

## 4. Missing Fallback Patterns

### Documented in Production but Missing from Skills

| Fallback | Production Location | Which Skill Should Document It |
|----------|--------------------|---------------------------------|
| ChEMBL → Open Targets `knownDrugs` | `TRAVERSE_DRUGS_SYSTEM` (prompts.py:325-329) | pharmacology, graph-builder |
| Multiple search attempts (max 3) | `ANCHOR_SYSTEM` (prompts.py:197) | genomics (no retry guidance) |
| Report "Unresolved" for failed resolution | `ANCHOR_SYSTEM` (prompts.py:197) | All skills (none say to report failure) |

### Missing from Both Skills and Production

| Fallback | Why Needed | Recommendation |
|----------|-----------|----------------|
| STRING → BioGRID | When STRING returns <3 interactions | Add to proteomics and graph-builder |
| UniProt → Ensembl xrefs | When UniProt is down | Add to proteomics |
| WikiPathways → STRING enrichment | When WikiPathways has no results for gene | Add to graph-builder |
| Disease-only trial search | When drug-specific search returns zero trials | Add to clinical and graph-builder |

---

## 5. Missing Error Recovery Guidance

### Production Supervisor (lifesciences.py:68-69)
```
- Do not skip phases. If a phase returns no results, note this and continue.
```

This is the **only** error recovery guidance. Missing:
- What to do when ENRICH fails to return Ensembl ID (needed by TRAVERSE_DRUGS)
- What to do when TRAVERSE_DRUGS returns agonists for gain-of-function diseases
- What to do when 3+ phases return no results
- Circuit breaker: when to stop and return partial results

### Skills
None of the 6 skills have any error recovery guidance.

---

## 6. Rate Limit Discrepancies

| API | Skill Documentation | Production (mcp.py) | Match? |
|-----|--------------------|-----------------------|--------|
| HGNC | 10 req/s (genomics:114) | Not rate-limited in mcp.py | MISMATCH — skill overstates restriction |
| Ensembl | 15 req/s (genomics:115) | Not in mcp.py | N/A — skill uses curl directly |
| NCBI | 3 req/s, 10 with key (genomics:116) | Not in mcp.py | N/A — skill uses curl directly |
| UniProt | 100 req/s (proteomics:127) | Not rate-limited in mcp.py | MISMATCH |
| STRING | 1 req/s (proteomics:128) | 1 req/s (mcp.py rate limiter) | MATCH |
| BioGRID | 10 req/s (proteomics:129) | 0.5s delay (mcp.py rate limiter) | APPROXIMATE MATCH |
| ChEMBL | 100 req/s (pharmacology:169) | 0.5s delay (mcp.py rate limiter) | MISMATCH — skill says 100/s; production throttles to 2/s |
| PubChem | 5 req/s (pharmacology:170) | Not in mcp.py | N/A |
| Open Targets | 100 req/s (clinical:199) | 0.2s delay (mcp.py rate limiter) | APPROXIMATE MATCH |
| ClinicalTrials.gov | "Varies" (clinical:200) | Not rate-limited in mcp.py | MISMATCH |

**Key issue**: ChEMBL is rate-limited to ~2 req/s in production but skill says 100 req/s. This mismatch could cause confusion when multiple rapid calls time out.

---

## 7. Alignment Matrix Summary

| Dimension | Alignment Score (0-4) | Notes |
|-----------|----------------------|-------|
| Phase naming | 4 | Near-perfect match |
| Tool invocation syntax | 1 | Skills use dot notation / curl; production uses `query_lifesciences()` wrapper |
| CURIE format | 1 | Systematic disagreement on 5 of 9 entity types |
| Workflow steps | 2 | Phase mapping exists but skills span multiple production phases |
| Fallback patterns | 1 | Critical Open Targets fallback missing from skills |
| Error recovery | 0 | Absent from both (minimal in production supervisor) |
| Rate limits | 2 | Some match, some significantly different |
| Tool assignment | 3 | Production has correct tools per specialist; skill doesn't specify |

**Overall alignment**: 14/32 (44%) — Significant gaps that explain the behavioral failures documented in the retrospective.

---

## 8. Recommendations

### Priority 1: Fix Critical Misalignments

1. **Add Open Targets fallback to pharmacology skill** — this is the #1 missing pattern
2. **Standardize CURIE format** with explicit two-context rule (API args vs graph node IDs)
3. **Align tool invocation syntax** — skills should show `query_lifesciences()` calls, not just curl

### Priority 2: Add Missing Patterns

4. **Add error recovery guidance** to graph-builder skill
5. **Add disease-only trial search fallback** to clinical skill
6. **Add mechanism filtering** (agonist vs antagonist) for gain-of-function diseases
7. **Fix ChEMBL rate limit** documentation to match production (2 req/s, not 100 req/s)

### Priority 3: Structural Improvements

8. **Convert reference cards to workflows** with mandatory LOCATE→RETRIEVE steps
9. **Add external knowledge restriction** per Anthropic hallucination guidance
10. **Clarify skill ↔ production phase mapping** in graph-builder skill
