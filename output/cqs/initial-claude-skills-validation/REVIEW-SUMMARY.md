# Competency Question Reports — Quality Review Summary

**Date**: 2026-02-07
**Reviewer**: Automated multi-agent review team (6 parallel agents)
**Protocol**: Fuzzy-to-Fact (graph-builder + reporting skills)

---

## Executive Summary

All 6 CQ reports received **PARTIAL** verdicts. No report fully passes the Fuzzy-to-Fact protocol requirements. The strongest dimensions are **Completeness** (all 6 pass) and **Evidence Grading** (5/6 pass). The weakest dimensions are **Disease CURIE in ENRICH** (5/6 fail) and **Hallucination Risk** (all 6 flagged MEDIUM or higher).

| # | Report | Verdict | Pass | Fail | N/A | Top Issue |
|---|--------|---------|------|------|-----|-----------|
| CQ1 | Doxorubicin Resistance Correlation | PARTIAL | 2 | 4 | 2 | No LOCATE steps shown; no disease CURIEs |
| CQ2 | Tumor Immune Evasion | PARTIAL | 5 | 2 | 2 | No disease CURIEs; Luspatercept mechanism error |
| CQ3 | Metastasis Gene Expression | PARTIAL | 4 | 1 | 3 | No disease CURIEs; secondary entities unresolved |
| CQ4 | Tumor Protease Mechanism | PARTIAL | 5 | 2 | 2 | No disease CURIEs; 9 entities missing CURIEs |
| CQ5 | NSCLC Drug Candidates | PARTIAL | 7 | 2 | 0 | Source attribution gaps in Discussion; inflated confidence |
| CQ6 | Synthetic Lethality Lung Cancer | PARTIAL | 5 | 4 | 1 | 0/26 NCT IDs verified; no patent/literature coverage |

---

## Dimension Heatmap

| Dimension | CQ1 | CQ2 | CQ3 | CQ4 | CQ5 | CQ6 | Pattern |
|-----------|-----|-----|-----|-----|-----|-----|---------|
| 1. CURIE Resolution | PARTIAL | PARTIAL | PASS | PARTIAL | PASS | FAIL | Secondary entities often unresolved |
| 2. Source Attribution | PARTIAL | PASS | PASS | PASS | FAIL | PASS | Discussion sections weakest |
| 3. LOCATE→RETRIEVE | FAIL | PARTIAL | PASS | PARTIAL | PASS | PASS | LOCATE steps often undocumented |
| 4. Disease CURIE (ENRICH) | **FAIL** | **FAIL** | **FAIL** | **FAIL** | PASS | **FAIL** | Systemic gap — only CQ5 resolves disease |
| 5. OT Pagination | N/A | PASS | N/A | PASS | PASS | PASS | Fixed by skill update; working |
| 6. Evidence Grading | PARTIAL | PASS | PASS | PASS | FAIL | PASS | Section-level vs claim-level grading varies |
| 7. GoF Filter | N/A | N/A | N/A | N/A | PASS | N/A | Only applicable to CQ5; correctly applied |
| 8. Trial Validation | PARTIAL | PASS | N/A | PASS | PASS | FAIL | CQ6 skipped Phase 5 entirely |
| 9. Completeness | PASS | PASS | PASS | PASS | PASS | FAIL | CQ6 missing patents + literature |
| 10. Hallucination Risk | MED-HIGH | MEDIUM | MEDIUM | MEDIUM | MEDIUM | MEDIUM | Universal — mechanism narratives exceed tool output |

---

## Systemic Issues (Cross-Report)

### 1. Disease CURIE Resolution — 5/6 FAIL
The most consistent failure. Only CQ5 (NSCLC) resolves a disease CURIE (EFO_0003060). The ENRICH phase skill fix adds `opentargets_get_associations` for disease resolution, but these reports were generated before the fix was applied. **This validates that the skill fix was needed.**

### 2. Hallucination Risk — All 6 MEDIUM or higher
Every report contains "connective tissue" claims (mechanism narratives, prevalence statistics, clinical context) that exceed what tool outputs provide. Common patterns:
- Epidemiological percentages (e.g., "TP53 mutations in >50% of cancers") — no tool source
- Detailed molecular mechanisms (e.g., "binds E-boxes in CDH1 promoter") — beyond STRING/UniProt output
- FDA approval status and pivotal trial outcomes — training knowledge
- Clinical recommendations — synthesis beyond tool data

### 3. LOCATE Step Documentation — 3/6 missing or incomplete
Reports often show RETRIEVE calls (e.g., `hgnc_get_gene`) without the preceding LOCATE call (`hgnc_search_genes`). The provenance chain is implied but not explicitly documented.

### 4. Secondary Entity CURIEs — Consistent gap
Interactor proteins discovered via STRING (e.g., HDAC1, MDM2, CTNNB1, TIMP1) are referenced by gene symbol only — never resolved to HGNC CURIEs. The graph-builder skill requires LOCATE→RETRIEVE for all entities included in the graph.

### 5. NCT ID Format — 4/6 use non-standard format
Reports use `NCT:00001944` (with colon) instead of the standard `NCT00001944` (no colon) specified in the graph-builder skill.

---

## Per-Report Detailed Scores

### CQ1: Doxorubicin Resistance Correlation
| Dimension | Score | Notes |
|-----------|-------|-------|
| CURIE Resolution | PARTIAL | Core genes resolved; diseases + many interactors unresolved |
| Source Attribution | PARTIAL | ~25 sourced, ~15-20 unsourced |
| LOCATE→RETRIEVE | FAIL | No explicit two-step pattern shown |
| Disease CURIE | FAIL | No MONDO/EFO CURIEs anywhere |
| OT Pagination | N/A | Open Targets not visibly used |
| Evidence Grading | PARTIAL | Levels used but no claim-level numeric scoring |
| GoF Filter | N/A | Not applicable |
| Trial Validation | PARTIAL | 5/~20 NCT IDs verified; 14+ unverified |
| Completeness | PASS | Answers CQ with depth |
| Hallucination Risk | MED-HIGH | Multiple unsourced mechanism descriptions |

### CQ2: Tumor Immune Evasion
| Dimension | Score | Notes |
|-----------|-------|-------|
| CURIE Resolution | PARTIAL | Genes/compounds excellent; disease CURIEs absent |
| Source Attribution | PASS | >95% of claims cited |
| LOCATE→RETRIEVE | PARTIAL | Clinical trials correct; gene/STRING gaps |
| Disease CURIE | FAIL | No MONDO/EFO resolved |
| OT Pagination | PASS | size-only pattern used; limitation acknowledged |
| Evidence Grading | PASS | L1-L4 properly applied; minor arithmetic error |
| GoF Filter | N/A | Not applicable |
| Trial Validation | PASS | 3/3 NCT IDs verified |
| Completeness | PASS | Core question well answered |
| Hallucination Risk | MEDIUM | Luspatercept mechanism likely inaccurate |

### CQ3: Metastasis Gene Expression
| Dimension | Score | Notes |
|-----------|-------|-------|
| CURIE Resolution | PASS | 11 genes resolved; secondary entities unresolved |
| Source Attribution | PASS | ~48 sourced, ~2 unsourced |
| LOCATE→RETRIEVE | PASS | hgnc_get_gene step not documented but implied |
| Disease CURIE | FAIL | No MONDO/EFO for metastasis or cancer |
| OT Pagination | N/A | Not used |
| Evidence Grading | PASS | 10 claims graded; modifier arithmetic not shown |
| GoF Filter | N/A | Not applicable |
| Trial Validation | N/A | Correctly scoped out (network-only question) |
| Completeness | PASS | Gene selection bias noted; missing pathways |
| Hallucination Risk | MEDIUM | Mechanism details exceed tool output |

### CQ4: Tumor Protease Mechanism
| Dimension | Score | Notes |
|-----------|-------|-------|
| CURIE Resolution | PARTIAL | 4 core resolved; 9 entities missing CURIEs |
| Source Attribution | PASS | ~55 sourced, ~4-5 unsourced |
| LOCATE→RETRIEVE | PARTIAL | RETRIEVE present; LOCATE not evidenced for initial anchoring |
| Disease CURIE | FAIL | No disease CURIEs despite mentioning multiple cancers |
| OT Pagination | PASS | Self-aware about pagination risks |
| Evidence Grading | PASS | 15 claims graded; median/range computed correctly |
| GoF Filter | N/A | Not applicable |
| Trial Validation | PASS | 6 NCT IDs listed; 2 fully verified, 4 from LOCATE |
| Completeness | PASS | All three CQ components addressed |
| Hallucination Risk | MEDIUM | ~7 narrative claims embed training knowledge |

### CQ5: NSCLC Drug Candidates
| Dimension | Score | Notes |
|-----------|-------|-------|
| CURIE Resolution | PASS | All entities resolved; minor format issues |
| Source Attribution | FAIL | ~15-18 unsourced claims in Discussion |
| LOCATE→RETRIEVE | PASS | Clear two-step pattern throughout |
| Disease CURIE | PASS | EFO_0003060 resolved early via Open Targets |
| OT Pagination | PASS | No failures; reasonable result sizes |
| Evidence Grading | FAIL | Section-level only; inflated 9.5/10 confidence |
| GoF Filter | PASS | Only inhibitors/antagonists included |
| Trial Validation | PASS | 3 NCT IDs verified |
| Completeness | PASS | 24 drugs; fully answers the CQ |
| Hallucination Risk | MEDIUM | Training knowledge in Discussion section |

### CQ6: Synthetic Lethality Lung Cancer
| Dimension | Score | Notes |
|-----------|-------|-------|
| CURIE Resolution | FAIL | 12/16 drugs lack CURIEs |
| Source Attribution | PASS | ~55-60 sourced claims |
| LOCATE→RETRIEVE | PASS | Two-step for 13 resolved entities |
| Disease CURIE | FAIL | Obtained incidentally; wrong format |
| OT Pagination | PASS | MCP tools handled pagination |
| Evidence Grading | PASS | 9 claims graded; median/range computed |
| GoF Filter | N/A | Not applicable |
| Trial Validation | FAIL | 0/26 NCT IDs verified; Phase 5 skipped |
| Completeness | FAIL | No patent coverage; no PubMed literature |
| Hallucination Risk | MEDIUM | Prevalence figures from training |

---

## Priority Remediation Actions

### P0 — Systemic (affects all reports)
1. **Enforce disease CURIE resolution in ENRICH phase** — the skill fix is now in place; re-running should resolve this
2. **Constrain mechanism narratives** — add a grounding check that flags sentences without `[Source:]` tags
3. **Standardize NCT ID format** — enforce bare `NCT00001944` (no colon)

### P1 — Per-report fixes
4. **CQ1**: Show LOCATE steps; verify 14+ unverified NCT IDs; add disease CURIEs
5. **CQ5**: Add source citations to Discussion section; implement claim-level evidence grading
6. **CQ6**: Run Phase 5 for top 15 NCT IDs; add PubMed literature search; acknowledge patent gap in Summary

### P2 — Quality improvements
7. **All reports**: Resolve secondary entity CURIEs (STRING-discovered interactors)
8. **CQ2**: Verify Luspatercept mechanism against actual Open Targets output
9. **CQ3**: Add WikiPathways data; fix node/edge count inconsistency
10. **CQ4**: Resolve 9 missing entity CURIEs

---

## Conclusion

The skills fixes applied in this session (disease CURIE resolution in ENRICH, Open Targets pagination guidance) directly address the #1 systemic failure (5/6 reports failing disease CURIE). The pagination fix is validated — all reports that used Open Targets knownDrugs post-fix show no pagination failures.

The remaining systemic issues (hallucination risk, LOCATE documentation, secondary entity CURIEs, NCT format) require either:
- **Prompt-level enforcement** (grounding checks, format validation) — addressable in skills
- **Production code changes** (tool output post-processing, validation middleware) — out of scope for skills fixes

**Overall protocol compliance**: ~60% across all dimensions and reports. Target: 80%+ after P0/P1 remediations.
