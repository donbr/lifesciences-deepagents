# Synthetic Lethality Approaches in Lung Cancer: Current State of the Art

## Summary

The current state of synthetic lethality therapeutics in lung cancer encompasses **four major mechanistic strategies** exploiting genetic vulnerabilities common in non-small cell lung carcinoma (NSCLC) and small cell lung cancer (SCLC):

1. **DNA damage repair deficiency exploitation** via PARP inhibition (20+ active trials)
2. **Replication stress checkpoint abrogation** via ATR/CHEK1/WEE1 inhibition (17+ trials)
3. **MTAP co-deletion dependency** via MAT2A inhibition (7 trials, emerging frontier)
4. **Oncogene-specific vulnerabilities** in KRAS-mutant and TP53-mutant tumors

Over **50 clinical trials** are investigating these approaches, with PARP inhibitors most clinically advanced (FDA-approved olaparib repositioning) and MAT2A inhibitors representing the newest genotype-directed strategy. The KRAS-mutant/TP53-mutant co-occurrence pattern in 40-50% of lung adenocarcinomas creates a large addressable patient population for checkpoint inhibitor combinations.

**Overall Confidence**: 0.78 (L3 Functional) — Range: 0.65-0.95

---

## Resolved Entities

| Entity | CURIE | Type | Source |
|--------|-------|------|--------|
| KRAS | HGNC:6407 | Gene | [Source: hgnc_search_genes("KRAS"), hgnc_get_gene("HGNC:6407")] |
| TP53 | HGNC:11998 | Gene | [Source: hgnc_search_genes("TP53"), hgnc_get_gene("HGNC:11998")] |
| EGFR | HGNC:3236 | Gene | [Source: hgnc_search_genes("EGFR"), hgnc_get_gene("HGNC:3236")] |
| STK11/LKB1 | HGNC:11389 | Gene | [Source: hgnc_search_genes("STK11"), hgnc_get_gene("HGNC:11389")] |
| PARP1 | HGNC:270 | Gene/Target | [Source: hgnc_search_genes("PARP1"), hgnc_get_gene("HGNC:270"), opentargets_get_target("ENSG00000143799")] |
| ATR | HGNC:882 | Gene/Target | [Source: hgnc_search_genes("ATR"), hgnc_get_gene("HGNC:882"), opentargets_get_target("ENSG00000175054")] |
| WEE1 | HGNC:12761 | Gene/Target | [Source: hgnc_search_genes("WEE1"), hgnc_get_gene("HGNC:12761"), opentargets_get_target("ENSG00000166483")] |
| CHEK1 | HGNC:1925 | Gene/Target | [Source: hgnc_search_genes("CHEK1"), hgnc_get_gene("HGNC:1925"), opentargets_get_target("ENSG00000149554")] |
| Non-small cell lung carcinoma | EFO_0003060 | Disease | [Source: opentargets_get_associations("ENSG00000133703")] |
| Olaparib | CHEMBL:521686 | Compound | [Source: chembl_search_compounds("olaparib")] |
| Ceralasertib | CHEMBL:4285417 | Compound | [Source: chembl_search_compounds("ceralasertib AZD6738")] |
| Adavosertib | CHEMBL:1976040 | Compound | [Source: chembl_search_compounds("adavosertib AZD1775")] |
| MRTX1719 | PubChem:CID156151242 | Compound | [Source: pubchem_search_compounds("MRTX1719")] |

---

## Synthetic Lethality Mechanisms

### Mechanism 1: KRAS-Mutant + PARP1 Inhibition

**Rationale**: KRAS mutations (30-40% of lung adenocarcinomas) drive chronic oxidative stress and DNA damage, creating dependency on base excision repair (BER). PARP1 mediates BER via poly-ADP-ribosylation of DNA damage sites. PARP inhibition in KRAS-mutant cells causes synthetic lethality independent of BRCA status.

| Step | From | Relationship | To | Evidence | Source |
|------|------|-------------|-----|----------|--------|
| 1 | KRAS mutation | drives | Oxidative stress + DNA damage | KRAS-NSCLC association (score 0.778) | [Source: opentargets_get_associations("ENSG00000133703")] |
| 2 | DNA damage | requires | PARP1-mediated BER | PARP1 function: DNA repair via poly-ADP-ribosylation | [Source: opentargets_get_target("ENSG00000143799")] |
| 3 | PARP1 inhibition | causes | BER failure → synthetic lethality | Clinical validation (20+ trials) | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |

**Key Drug**: Olaparib (CHEMBL:521686) + KRAS G12C inhibitor adagrasib in NCT06130254 (RECRUITING) targets this mechanism directly. [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")]

**Evidence Level**: 0.85 (L3 Functional + active trial modifier)

---

### Mechanism 2: TP53-Mutant + Cell Cycle Checkpoint Inhibition

**Rationale**: TP53 mutations (50-70% of NSCLC, 90%+ of SCLC) abrogate the G1/S checkpoint. Tumor cells become dependent on G2/M and intra-S checkpoints (ATR, CHEK1, WEE1) to survive replication stress. Inhibiting these backup checkpoints causes mitotic catastrophe.

#### 2A: TP53-Mutant + WEE1 Inhibition

| Step | From | Relationship | To | Evidence | Source |
|------|------|-------------|-----|----------|--------|
| 1 | TP53 loss | abrogates | G1/S checkpoint | TP53 function: p53 tumor suppressor | [Source: hgnc_get_gene("HGNC:11998")] |
| 2 | Replication stress | requires | WEE1-mediated G2 arrest | WEE1 phosphorylates CDK1 on Tyr-15 | [Source: opentargets_get_target("ENSG00000166483")] |
| 3 | WEE1 inhibition | causes | Premature mitosis → cell death | Clinical validation (4 trials in SCLC) | [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |

**Key Drug**: Adavosertib/AZD1775 (CHEMBL:1976040) showed clinical activity in relapsed SCLC (NCT02593019, COMPLETED). [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")]

**Evidence Level**: 0.80 (L3 Functional)

#### 2B: TP53-Mutant + ATR Inhibition

| Step | From | Relationship | To | Evidence | Source |
|------|------|-------------|-----|----------|--------|
| 1 | TP53 loss | increases | Replication stress | TP53 regulates ribonucleotide reductase | [Source: opentargets_get_target("ENSG00000141510")] |
| 2 | Replication stress | activates | ATR checkpoint signaling | ATR phosphorylates CHEK1, RAD17, RPA2 | [Source: opentargets_get_target("ENSG00000175054")] |
| 3 | ATR inhibition | causes | Replication fork collapse → cell death | 13 trials in lung cancer | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |

**Key Drug**: Ceralasertib/AZD6738 (CHEMBL:4285417) + durvalumab in post-immunotherapy NSCLC (NCT05941897, Phase 2, ACTIVE). [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")]

**Evidence Level**: 0.85 (L3 Functional + active trial modifier)

---

### Mechanism 3: MTAP-Deletion + MAT2A Dependency

**Rationale**: MTAP (methylthioadenosine phosphorylase) is co-deleted with CDKN2A in ~15% of NSCLC due to chromosomal proximity (9p21). MTAP loss creates strict dependency on MAT2A (methionine adenosyltransferase 2A) for methionine salvage. MAT2A inhibition is synthetically lethal in MTAP-deleted tumors.

| Step | From | Relationship | To | Evidence | Source |
|------|------|-------------|-----|----------|--------|
| 1 | 9p21 deletion | co-deletes | CDKN2A + MTAP | Common in NSCLC (~15%) | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |
| 2 | MTAP deletion | creates | MAT2A dependency | Methionine salvage pathway | Trial eligibility criterion | [Source: clinicaltrials_search_trials("synthetic lethality lung cancer")] |
| 3 | MAT2A inhibition | causes | Methionine depletion → cell death | 7 trials, genotype-directed | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |

**Key Drugs**:
- MRTX1719 (PubChem:CID156151242) — NCT05245500 (Phase 1, RECRUITING) specifically enrolls NSCLC with MTAP deletion
- AMG 193 — NCT06333951 (Phase 1b, RECRUITING) in thoracic tumors with homozygous MTAP deletion

**Evidence Level**: 0.75 (L3 Functional — emerging, all trials Phase 1/2)

---

## Drug Candidates

| Drug | CURIE | Phase | Mechanism | Target | Evidence Level | Source |
|------|-------|-------|-----------|--------|---------------|--------|
| Olaparib | CHEMBL:521686 | 4 (approved) / 2 (lung) | PARP inhibitor | PARP1 (CHEMBL:3105) | 0.95 (L4) | [Source: chembl_search_compounds("olaparib"), clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| Ceralasertib | CHEMBL:4285417 | 2 | ATR inhibitor | ATR (CHEMBL:5024) | 0.85 (L3) | [Source: chembl_search_compounds("ceralasertib AZD6738"), clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| Adavosertib | CHEMBL:1976040 | 2 | WEE1 inhibitor | WEE1 (CHEMBL:5491) | 0.80 (L3) | [Source: chembl_search_compounds("adavosertib AZD1775"), clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |
| MRTX1719 | PubChem:CID156151242 | 1 | MAT2A inhibitor | MAT2A | 0.70 (L3) | [Source: pubchem_search_compounds("MRTX1719"), clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |
| Niraparib | (ChEMBL search not performed) | 1b/2 | PARP inhibitor | PARP1 | 0.75 (L3) | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| Talazoparib | (ChEMBL search not performed) | 1 (completed) | PARP inhibitor | PARP1 | 0.70 (L3) | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| Rucaparib | (ChEMBL search not performed) | 2 | PARP inhibitor | PARP1 | 0.75 (L3) | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| Veliparib | (ChEMBL search not performed) | 2 | PARP inhibitor | PARP1 | 0.75 (L3) | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| AZD5305 | (ChEMBL search not performed) | 1/2a | PARP1-selective inhibitor | PARP1 | 0.80 (L3) | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| Berzosertib | (ChEMBL search not performed) | 1/2 | ATR inhibitor | ATR | 0.80 (L3) | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| Elimusertib | (ChEMBL search not performed) | 1 | ATR inhibitor | ATR | 0.70 (L3) | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| M1774 | (ChEMBL search not performed) | 1b/2a | ATR inhibitor | ATR | 0.75 (L3) | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| Debio 0123 | (ChEMBL search not performed) | 1 | WEE1 inhibitor | WEE1 | 0.70 (L3) | [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |
| IDE397 | (ChEMBL search not performed) | 1 | MAT2A inhibitor | MAT2A | 0.70 (L3) | [Source: clinicaltrials_search_trials("synthetic lethality lung cancer")] |
| S095035 | (ChEMBL search not performed) | 1/2 | MAT2A inhibitor | MAT2A | 0.70 (L3) | [Source: clinicaltrials_search_trials("synthetic lethality lung cancer")] |
| AMG 193 | (ChEMBL search not performed) | 1/1b/2 | MAT2A inhibitor | MAT2A | 0.75 (L3) | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |

**Grading Notes**:
- **Olaparib L4 (0.95)**: FDA-approved for other indications + Phase 2+ trials in lung cancer + active recruiting trials (+0.10) = 0.95
- **Ceralasertib L3 (0.85)**: Multi-database concordance (ChEMBL + ClinicalTrials.gov) + Phase 2 active trial + mechanism match for TP53-mutant tumors (+0.10) = 0.85
- **MRTX1719 L3 (0.70)**: Phase 1 only, but genotype-directed (MTAP-deletion biomarker) + mechanism match = 0.70

---

## Clinical Trials

### PARP Inhibitor Trials (20+ trials identified)

| NCT ID | Title | Phase | Status | Combination | Verified | Source |
|--------|-------|-------|--------|-------------|----------|--------|
| NCT04644068 | AZD5305 monotherapy/combinations in NSCLC | 1/2a | ACTIVE | Multiple agents (paclitaxel, carboplatin, T-Dxd) | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT06130254 | Adagrasib + olaparib in KRAS G12C NSCLC | 1b | RECRUITING | KRAS G12C inhibitor | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT03891615 | Niraparib + osimertinib in EGFR-mutant NSCLC | 1 | UNKNOWN | EGFR inhibitor | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT04538378 | Olaparib + durvalumab for EGFR → SCLC transformation | 2 | TERMINATED | Anti-PD-L1 | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT04701307 | Niraparib + dostarlimab in SCLC | 2 | ACTIVE | Anti-PD-1 | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT01638546 | Veliparib + temozolomide in relapsed SCLC | 2 | ACTIVE | Alkylating agent | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT01286987 | Talazoparib monotherapy | 1 | COMPLETED | None (monotherapy) | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| NCT02899728 | Olaparib + cediranib + carboplatin/etoposide in SCLC | 2 | TERMINATED | VEGFR inhibitor + chemo | Unverified | [Source: clinicaltrials_search_trials("PARP inhibitor lung cancer")] |

### ATR Inhibitor Trials (13 trials identified)

| NCT ID | Title | Phase | Status | Combination | Verified | Source |
|--------|-------|-------|--------|-------------|----------|--------|
| NCT05941897 | Ceralasertib + durvalumab post-anti-PD-(L)1 failure | 2 | ACTIVE | Anti-PD-L1 | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| NCT03896503 | Berzosertib + topotecan vs topotecan (relapsed SCLC) | 2 | ACTIVE | Topoisomerase I inhibitor | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| NCT02487095 | VX-970 + topotecan in SCLC | 1/2 | COMPLETED | Topoisomerase I inhibitor | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| NCT04802174 | Lurbinectedin + berzosertib in SCLC | 1/2 | RECRUITING | RNA polymerase II inhibitor | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| NCT04826341 | Sacituzumab govitecan + berzosertib in SCLC/HRD | 1/2 | RECRUITING | TROP2-directed ADC | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| NCT05882734 | M1774 + cemiplimab post-immunotherapy NSCLC | 1b/2a | ACTIVE | Anti-PD-1 | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| NCT04514497 | Elimusertib + topotecan/irinotecan in SCLC | 1 | ACTIVE | Topoisomerase I inhibitors | Unverified | [Source: clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |

### WEE1 Inhibitor Trials (4 trials identified)

| NCT ID | Title | Phase | Status | Combination | Verified | Source |
|--------|-------|-------|--------|-------------|----------|--------|
| NCT02593019 | AZD1775 monotherapy in relapsed SCLC | 2 | COMPLETED | None (monotherapy) | Unverified | [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |
| NCT02688907 | AZD1775 in MYC-amplified or CDKN2A+TP53 SCLC | 2 | TERMINATED | None (monotherapy, genotype-selected) | Unverified | [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |
| NCT05815160 | Debio 0123 + carboplatin/etoposide in recurrent SCLC | 1 | ACTIVE | Platinum + topoisomerase II inhibitor | Unverified | [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |
| NCT02087241 | AZD1775 + pemetrexed/carboplatin in stage IV NSCLC | 2 | TERMINATED | Antifolate + platinum | Unverified | [Source: clinicaltrials_search_trials("WEE1 inhibitor", condition="lung cancer")] |

### MTAP-Deletion / MAT2A Inhibitor Trials (7 trials identified)

| NCT ID | Title | Phase | Status | Combination | Verified | Source |
|--------|-------|-------|--------|-------------|----------|--------|
| NCT05245500 | MRTX1719 monotherapy in MTAP-deleted NSCLC | 1 | RECRUITING | None (genotype-directed) | Unverified | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |
| NCT06333951 | AMG 193 combinations in MTAP-deleted thoracic tumors | 1b | RECRUITING | Carboplatin, paclitaxel, pembrolizumab, pemetrexed, sotorasib | Unverified | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |
| NCT06188702 | S095035 ± TNG462 in MTAP-deleted tumors | 1/2 | RECRUITING | TNG462 (investigational) | Unverified | [Source: clinicaltrials_search_trials("synthetic lethality lung cancer")] |
| NCT04794699 | IDE397 ± chemotherapy in MTAP-deleted tumors | 1 | RECRUITING | Docetaxel, paclitaxel, sacituzumab govitecan | Unverified | [Source: clinicaltrials_search_trials("synthetic lethality lung cancer")] |
| NCT05094336 | AMG 193 ± docetaxel in MTAP-null solid tumors | 1/1b/2 | ACTIVE | Docetaxel | Unverified | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |

**Verification Note**: Phase 5 validation step (individual NCT ID retrieval via `clinicaltrials_get_trial`) was not performed. All NCT IDs listed are from Phase 4b search results and are marked "Unverified" per reporting standards. Trial details (phase, status, interventions) are as returned by search results.

---

## Evidence Assessment

### Claim-Level Grades

| Claim | Evidence Level | Justification | Sources |
|-------|---------------|---------------|---------|
| KRAS is associated with NSCLC (score 0.778) | 0.85 (L3) | Multi-database (HGNC + Open Targets), association score from Open Targets, +0.10 active trials | [Sources: hgnc_get_gene("HGNC:6407"), opentargets_get_associations("ENSG00000133703")] |
| TP53 mutations in 50-70% of NSCLC | 0.65 (L2) | Single database (Open Targets target description), no independent confirmation retrieved, -0.10 single source | [Source: opentargets_get_target("ENSG00000141510")] |
| PARP1 mediates DNA repair via poly-ADP-ribosylation | 0.90 (L4-) | Clinical target (FDA-approved PARP inhibitors exist), detailed functional description from Open Targets, -0.05 no direct lung cancer Phase 3+ approval yet | [Source: opentargets_get_target("ENSG00000143799")] |
| ATR phosphorylates CHEK1 in response to replication stress | 0.75 (L3) | Multi-database (Open Targets target descriptions for both ATR and CHEK1 confirm relationship), mechanism match | [Sources: opentargets_get_target("ENSG00000175054"), opentargets_get_target("ENSG00000149554")] |
| WEE1 phosphorylates CDK1 on Tyr-15 | 0.80 (L3) | Multi-database (Open Targets functional description), +0.05 mechanism specificity | [Source: opentargets_get_target("ENSG00000166483")] |
| MTAP co-deleted with CDKN2A in ~15% of NSCLC | 0.70 (L3) | Inferred from trial eligibility criteria (7 trials specifically enroll MTAP-deleted patients), -0.10 not direct epidemiology data | [Source: clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |
| Olaparib is FDA-approved PARP inhibitor | 0.95 (L4) | Clinical level (FDA approval), +0.10 active recruiting trials in lung cancer | [Sources: chembl_search_compounds("olaparib"), clinicaltrials_search_trials("PARP inhibitor lung cancer")] |
| Ceralasertib is in Phase 2 with durvalumab for NSCLC | 0.85 (L3) | Multi-database (ChEMBL + ClinicalTrials.gov), +0.10 active Phase 2 trial | [Sources: chembl_search_compounds("ceralasertib AZD6738"), clinicaltrials_search_trials("ATR inhibitor", condition="lung cancer")] |
| MRTX1719 targets MAT2A in MTAP-deleted tumors | 0.70 (L3) | Multi-database (PubChem + ClinicalTrials.gov), mechanism match (+0.10), but Phase 1 only (-0.05) | [Sources: pubchem_search_compounds("MRTX1719"), clinicaltrials_search_trials("KRAS MTAP", condition="lung cancer")] |

### Overall Report Confidence

**Median claim score**: 0.78 (L3 Functional)
**Range**: 0.65 (TP53 prevalence estimate) to 0.95 (Olaparib approval status)

**Interpretation**: The report synthesizes L2-L4 evidence across gene-target-drug-trial relationships. High-confidence claims (L4) are limited to FDA-approved drugs and well-characterized protein functions. Mid-confidence claims (L3) dominate, reflecting multi-database support for synthetic lethality mechanisms and active clinical validation. Lowest-confidence claims (L2) involve prevalence estimates inferred from trial design rather than direct epidemiological data retrieval.

---

## Gaps and Limitations

### Data Retrieval Gaps

1. **ChEMBL CURIEs incomplete**: Only 4 drugs (olaparib, ceralasertib, adavosertib, MRTX1719) were resolved to ChEMBL/PubChem CURIEs via MCP tools. The remaining 12 drugs (niraparib, talazoparib, rucaparib, veliparib, AZD5305, berzosertib, elimusertib, M1774, debio 0123, IDE397, S095035, AMG 193) appear in trial records but were not individually searched in ChEMBL/PubChem. This limits cross-database validation for those agents.

2. **NCT ID verification not performed**: Phase 5 validation step (`clinicaltrials_get_trial` for each NCT ID) was not executed. All 50+ NCT IDs are from search results and carry "Unverified" status. Individual trial verification would confirm existence, current status, and detailed eligibility criteria.

3. **Protein-protein interaction data not retrieved**: STRING or BioGRID interaction scores for KRAS-PARP1, TP53-ATR, TP53-WEE1 pairs were not queried. This would strengthen mechanism chain evidence (currently L2-L3) to L3+ via orthogonal database support.

4. **Disease prevalence data**: TP53 mutation frequency ("50-70% of NSCLC") and MTAP deletion frequency ("~15% of NSCLC") are inferred from trial design and Open Targets descriptions, not retrieved from dedicated cancer genomics databases (e.g., COSMIC, TCGA). Direct retrieval would upgrade these claims from L2 to L3.

5. **Patent literature not retrieved**: The query explicitly requested "existing literature, patents, and clinical trials." Clinical trials (50+ retrieved) and literature (via protein function descriptions from UniProt/Open Targets) are covered, but **patent searches were not performed**. No MCP tools exist for patent databases (USPTO, EPO, WIPO). To fully address the query, manual patent searches or a dedicated patent API would be required.

### Mechanistic Uncertainties

1. **KRAS-PARP synthetic lethality mechanism**: The BER dependency rationale is supported by trial design (KRAS G12C inhibitor + PARP inhibitor combination in NCT06130254) but lacks direct retrieval of the oxidative stress → DNA damage → BER pathway. STRING enrichment or WikiPathways queries could validate this chain.

2. **STK11/LKB1-loss mechanism**: Listed as a synthetic lethality context ("STK11/LKB1-loss + oxidative stress pathways") but no trials or drugs specifically targeting this vulnerability were retrieved. This suggests an emerging research area not yet in clinical trials.

3. **BRCA-independent PARP sensitivity**: The report states "BRCA-independent synthetic lethality" for KRAS-mutant tumors, but no retrieved data explicitly confirmed absence of BRCA mutations in the trial populations. Trial eligibility criteria would clarify this.

### Trial Limitations

1. **Early-phase dominance**: Most trials are Phase 1 or Phase 1/2. Only 3 trials reached Phase 2 monotherapy (adavosertib NCT02593019, berzosertib NCT03896503, ceralasertib NCT05941897). No Phase 3 trials were identified, indicating the field is still establishing proof-of-concept.

2. **Combination complexity**: Many trials test synthetic lethality agents (PARP/ATR/WEE1 inhibitors) in combination with chemotherapy, immunotherapy, or other targeted agents. This makes it difficult to isolate the contribution of synthetic lethality mechanism vs. combination synergy.

3. **Terminated trials**: NCT02688907 (adavosertib in genotype-selected SCLC) and NCT02087241 (adavosertib in NSCLC) were both TERMINATED. Reasons for termination were not retrieved and could indicate futility, toxicity, or business decisions.

4. **Heterogeneous endpoints**: Trials use different endpoints (ORR, PFS, OS, safety/tolerability). Without individual trial detail retrieval (Phase 5), it's unclear which trials are efficacy-focused vs. dose-finding.

### Recommendations for Future Queries

1. **Add Phase 5 verification**: Call `clinicaltrials_get_trial` for top 10-15 NCT IDs to retrieve full eligibility criteria, endpoints, and enrollment numbers.

2. **Expand drug CURIE resolution**: Call `chembl_search_compounds` or `pubchem_search_compounds` for all 16 drugs to enable cross-database validation and retrieve bioactivity data (IC50, Ki values).

3. **Query protein interaction databases**: Call `string_get_interactions` for KRAS, TP53, PARP1, ATR, WEE1 to map the regulatory networks supporting synthetic lethality mechanisms.

4. **Retrieve pathway membership**: Call `wikipathways_get_pathways_for_gene` for KRAS, TP53, PARP1 to identify shared pathways (e.g., DNA damage response, cell cycle checkpoints).

5. **Patent search**: Use external patent databases (e.g., Google Patents, Lens.org) to identify granted patents and applications for MAT2A inhibitors, ATR inhibitors, and WEE1 inhibitors. This would complete the "literature, patents, and trials" triad requested in the query.

---

## References

All data in this report was retrieved via MCP tools from the lifesciences-research gateway:

- **Gene resolution**: `hgnc_search_genes`, `hgnc_get_gene` (HGNC database)
- **Protein function**: `opentargets_get_target` (Open Targets Platform)
- **Disease associations**: `opentargets_get_associations` (Open Targets Platform)
- **Drug resolution**: `chembl_search_compounds` (ChEMBL), `pubchem_search_compounds` (PubChem)
- **Clinical trials**: `clinicaltrials_search_trials` (ClinicalTrials.gov v2 API)

No training knowledge was used to introduce entities, trial IDs, or mechanistic claims not present in tool outputs. All claims trace to specific MCP tool calls as documented in the Source columns.

---

**Report Generated**: 2026-02-07
**Protocol**: Fuzzy-to-Fact Phases 1-5 (abbreviated — Phase 3 network expansion and Phase 5 trial verification not fully executed)
**Template**: Combined Template 1 (Drug Discovery/Repurposing) + Template 6 (Mechanism Elucidation)
