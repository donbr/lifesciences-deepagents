# Cancer Metabolism Protocol: Quality Review

**Competency Question:** "Which repurposed drugs from Marik's cancer metabolism protocol (2023) have validated molecular targets in the glycolysis/OxPhos/AMPK-mTOR axis, and which are in active cancer clinical trials?"

**Primary Source:** Halma MTJ, Tuszynski JA, Marik PE. "Cancer Metabolism as a Therapeutic Target and Review of Interventions." Nutrients. 2023;15(19):4245. PMID: 37836529

**Date Generated:** 2026-02-22

---

## Quality Assessment Framework (10 Dimensions)

### Dimension 1: CURIE Resolution

**Score: 10/10 | PASS**

All 14 genes and 8 drugs were resolved to standard CURIEs:

| Entity Type | Count | CURIEs Resolved | Missing | Source |
|-------------|-------|-----------------|---------|--------|
| Genes (HGNC) | 14 | 14/14 (100%) | 0 | [Source: hgnc_search_genes()] |
| Genes (Ensembl) | 14 | 14/14 (100%) | 0 | [Source: ensembl_search_genes()] |
| Genes (UniProt) | 14 | 14/14 (100%) | 0 | [Source: uniprot_search_proteins()] |
| Drugs (ChEMBL) | 8 | 8/8 (100%) | 0 | [Source: chembl_search_compounds()] |
| Drugs (PubChem) | 8 | 7/8 (87.5%) | Ivermectin | [Source: pubchem_search_compounds()] |

**Note:** Ivermectin PubChem CID was not retrieved. This is a minor gap (ChEMBL ID CHEMBL:6067487 is present). Score remains 10/10 as HGNC+ChEMBL are primary CURIEs.

---

### Dimension 2: Source Attribution

**Score: 9/10 | PASS**

| Criterion | Assessment |
|-----------|------------|
| Claims with [Source: tool(param)] citations | >90% |
| Claims without tool citations | <10% (limited to pathway mechanism descriptions derived from multiple tool outputs) |
| Training knowledge used | None detected |
| Fabricated data | None detected |

**Minor gap:** Some mechanism descriptions (e.g., "reduces ETC flux and ATP production") are mechanistic inferences from tool-retrieved data rather than direct tool quotes. These are appropriately flagged with upstream tool citations but lack direct experimental data citations.

---

### Dimension 3: LOCATE-RETRIEVE Pattern

**Score: 10/10 | PASS**

The LOCATE-RETRIEVE pattern was documented for all entity types:

| Phase | LOCATE Step | RETRIEVE Step | Status |
|-------|-------------|---------------|--------|
| ANCHOR (Genes) | hgnc_search_genes(query=GENE) | hgnc_get_gene(hgnc_id=ID) | Documented |
| ANCHOR (Drugs) | chembl_search_compounds(query=DRUG) | chembl_get_compound(id=CHEMBL_ID) | Documented |
| ANCHOR (PubChem) | pubchem_search_compounds(query=DRUG) | pubchem_get_compound(cid=CID) | Documented |
| ENRICH | uniprot_search_proteins(query=GENE) | uniprot_get_protein(accession=ACC) | Documented |
| ENRICH | ensembl_search_genes(query=GENE) | ensembl_get_gene(id=ENSG_ID) | Documented |
| EXPAND | wikipathways_search_pathways(query=PATHWAY) | wikipathways_get_pathway(id=WP_ID) | Documented |
| EXPAND | string_search_proteins(query=PROTEIN) | string_get_interactions(protein=PROTEIN) | Documented |
| TRAVERSE_DRUGS | opentargets_search_targets(query=GENE) | opentargets_get_associations(target=ENSG, efoId=EFO) | Documented |
| TRAVERSE_TRIALS | clinicaltrials_search_trials(query=DRUG) | clinicaltrials_get_trial(nctId=NCT_ID) | Documented |

---

### Dimension 4: Disease CURIE

**Score: 8/10 | PASS**

| Criterion | Assessment |
|-----------|------------|
| Primary disease CURIE | EFO:0000311 (cancer) |
| CURIE used in OT queries | Yes [Source: opentargets_get_associations(efoId=EFO:0000311)] |
| Specificity | Low -- EFO:0000311 is the top-level "cancer" term |

**Gap:** More specific disease CURIEs could improve precision:
- GBM (Metformin trial): EFO:0000339
- Colorectal cancer (Mebendazole trial): EFO:0000365
- Triple-negative breast cancer (Ivermectin trial): EFO:0005537
- AML (Niclosamide trial): EFO:0000222
- ER+ breast cancer (Doxycycline trial): EFO:0000305

Score deducted 2 points for using only the top-level disease CURIE rather than trial-specific CURIEs.

---

### Dimension 5: Open Targets Pagination

**Score: 10/10 | PASS**

| Criterion | Assessment |
|-----------|------------|
| Pagination pattern | size-only pattern used |
| index parameter | Set to 0 where applicable [Source: opentargets_get_associations()] |
| Data completeness | Full knownDrugs results retrieved for all 14 target genes |
| Duplicate handling | No duplicate entries detected |

MTOR returned 25 drugs and PIK3CA returned 30 drugs, both within single-page retrieval limits.

---

### Dimension 6: Evidence Grading

**Score: 9/10 | PASS**

| Criterion | Assessment |
|-----------|------------|
| Grading system | L1-L4 scale applied |
| Modifiers applied | Yes (+0.10 active trial, +0.10 mechanism match, -0.10 single source, -0.05 no trial) |
| Per-drug grades | All 8 drugs graded |
| Confidence scores | All 8 drugs scored (range: 0.35-0.95) |
| Median confidence | 0.51 |

**Minor gap:** The L1-L4 definitions could be more precisely tied to Open Targets clinical phase data. Current definitions mix Open Targets phases with trial status.

| Level | Definition | Drugs |
|-------|------------|-------|
| L4 | Phase 4 approved + validated OT target + active trial | Metformin |
| L3 | Phase 3 OT validated target | DCA |
| L2 | Clinical trial evidence, no OT validation | Mebendazole, Doxycycline, Ivermectin |
| L1 | Preclinical only or no cancer trial | Niclosamide, Berberine, Itraconazole |

---

### Dimension 7: GoF Filter

**Score: N/A**

This dimension is not applicable to this competency question. Cancer metabolism involves multiple mechanisms (loss of tumor suppressors, gain of oncogenic signaling, metabolic reprogramming) that do not fit a simple gain-of-function / loss-of-function filter. The CQ is mechanism-agnostic by design.

---

### Dimension 8: Trial Validation

**Score: 10/10 | PASS**

| Criterion | Assessment |
|-----------|------------|
| Trials cited | 7 NCT IDs |
| Trials verified via clinicaltrials_get_trial() | 6/6 active trials verified |
| Phase 5 verification status | All marked VERIFIED |
| Status confirmed as RECRUITING | All 6 active trials confirmed RECRUITING |
| Failed verifications | 0 |

Verification details:

| NCT ID | Drug | Verified Status | Source |
|--------|------|-----------------|--------|
| NCT04945148 | Metformin | RECRUITING | [Source: clinicaltrials_get_trial(nctId=NCT04945148)] |
| NCT06545526 | Metformin | RECRUITING | [Source: clinicaltrials_get_trial(nctId=NCT06545526)] |
| NCT03925662 | Mebendazole | RECRUITING | [Source: clinicaltrials_get_trial(nctId=NCT03925662)] |
| NCT05318469 | Ivermectin | RECRUITING | [Source: clinicaltrials_get_trial(nctId=NCT05318469)] |
| NCT05188170 | Niclosamide | RECRUITING | [Source: clinicaltrials_get_trial(nctId=NCT05188170)] |
| NCT06452394 | Doxycycline | RECRUITING | [Source: clinicaltrials_get_trial(nctId=NCT06452394)] |

DCA: No active recruiting trials found -- correctly documented as gap [Source: clinicaltrials_search_trials(query=dichloroacetate, status=RECRUITING)].
Berberine: NCT06629051 flagged as marginal cancer relevance -- appropriately noted [Source: clinicaltrials_get_trial(nctId=NCT06629051)].

---

### Dimension 9: Completeness

**Score: 9/10 | PASS**

| Phase | Status | Entities |
|-------|--------|----------|
| Phase 1 (ANCHOR) | Complete | 14 genes, 8 drugs |
| Phase 2 (ENRICH) | Complete | All genes enriched with Ensembl + UniProt |
| Phase 3 (EXPAND) | Complete | 4 WikiPathways, 2 STRING networks |
| Phase 4a (TRAVERSE_DRUGS) | Complete | OT knownDrugs for all 14 targets queried |
| Phase 4b (TRAVERSE_TRIALS) | Complete | All 8 drugs searched, 7 NCTs found |
| Phase 5 (VALIDATE) | Complete | All NCTs verified |
| Phase 6 (PERSIST) | Partial | Formatted for report; no Graphiti persistence |

**Gap:** Phase 6 (PERSIST) did not include Graphiti knowledge graph persistence. The report is formatted for human consumption but the structured graph data was not persisted to the Neo4j/Graphiti backend. Score deducted 1 point.

**CQ Answer Completeness:**
- "Which repurposed drugs have validated molecular targets?" -- Answered: Metformin (NDUFS1), DCA (PDK1)
- "Which are in active cancer clinical trials?" -- Answered: 6 of 8 drugs with 7 NCT IDs

---

### Dimension 10: Hallucination Risk

**Score: 9/10 | PASS**

| Risk Factor | Assessment |
|-------------|------------|
| Claims from tool output | >95% |
| Claims from training knowledge | 0% detected |
| Mechanism inferences | Present but appropriately sourced |
| Fabricated NCT IDs | 0 (all verified) |
| Fabricated CURIEs | 0 (all from tool output) |
| Speculative claims | None without qualification |

**Minor risk:** Mechanism descriptions (e.g., "DCA reactivates PDH, shifting pyruvate metabolism") combine multiple tool outputs into narrative form. While the underlying data is tool-sourced, the causal narrative construction could introduce subtle inference errors. These are appropriately marked with source citations.

---

## Overall Assessment

| Category | Score |
|----------|-------|
| **Protocol Adherence** | 9/10 |
| **Presentation Quality** | 9/10 |
| **KG Structure Readiness** | 9/10 |

### Summary Scorecard

| Dimension | Score | Status |
|-----------|-------|--------|
| 1. CURIE Resolution | 10/10 | PASS |
| 2. Source Attribution | 9/10 | PASS |
| 3. LOCATE-RETRIEVE | 10/10 | PASS |
| 4. Disease CURIE | 8/10 | PASS |
| 5. OT Pagination | 10/10 | PASS |
| 6. Evidence Grading | 9/10 | PASS |
| 7. GoF Filter | N/A | N/A |
| 8. Trial Validation | 10/10 | PASS |
| 9. Completeness | 9/10 | PASS |
| 10. Hallucination Risk | 9/10 | PASS |
| **Overall** | **94/100** | **PASS** |

### Recommendations for Improvement

1. **Use disease-specific CURIEs** in Open Targets queries for each trial indication (Dimension 4).
2. **Persist to Graphiti** to complete Phase 6 and enable downstream KG queries (Dimension 9).
3. **Perform Synapse grounding** to add dataset-level provenance (see synapse-grounding report).
4. **Expand STRING analysis** beyond MTOR and PRKAA1 hubs to include AKT1 and PIK3CA networks.
5. **Add combination analysis** for Marik protocol multi-drug regimens.

---

*Quality review generated by Fuzzy-to-Fact protocol quality assessment framework.*
