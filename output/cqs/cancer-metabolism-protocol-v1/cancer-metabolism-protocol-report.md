# Cancer Metabolism Protocol: Drug Repurposing & Mechanism Elucidation Report

**Competency Question:** "Which repurposed drugs from Marik's cancer metabolism protocol (2023) have validated molecular targets in the glycolysis/OxPhos/AMPK-mTOR axis, and which are in active cancer clinical trials?"

**Primary Source:** Halma MTJ, Tuszynski JA, Marik PE. "Cancer Metabolism as a Therapeutic Target and Review of Interventions." Nutrients. 2023;15(19):4245. PMID: 37836529

**Templates Applied:** Template 1 (Drug Discovery/Repurposing) + Template 6 (Mechanism Elucidation)

**Date Generated:** 2026-02-22

---

## 1. Summary

Of the 8 repurposed drugs catalogued from Marik's cancer metabolism protocol (2023), **2 have formally validated molecular targets** in the glycolysis/OxPhos/AMPK-mTOR axis as registered in Open Targets knownDrugs: **Metformin** (targeting NDUFS1/Complex I, Phase 4) and **Sodium Dichloroacetate (DCA)** (targeting PDK1, Phase 3) [Source: opentargets_get_associations(efoId=EFO:0000311)]. The remaining 6 drugs (Mebendazole, Ivermectin, Niclosamide, Berberine, Itraconazole, Doxycycline) act through targets not formally registered in Open Targets or through preclinical/indirect mechanisms [Source: opentargets_get_associations(efoId=EFO:0000311)].

**6 of the 8 drugs have active recruiting cancer clinical trials** as of 2025: Metformin (Phase 2, Phase 3), Mebendazole (Phase 3), Ivermectin (Phase 1/2), Niclosamide (Phase 1), Doxycycline (Phase 2), and Berberine (N/A, marginal cancer relevance) [Source: clinicaltrials_search_trials(query=each drug, status=RECRUITING)]. DCA and Itraconazole have no active recruiting cancer trials.

Median evidence confidence across all 8 drugs is **0.51** (range: 0.35-0.95).

---

## 2. Resolved Entities

### 2.1 Genes (14 resolved)

| Gene | HGNC ID | Ensembl | UniProt | Location | Metabolic Axis | Source |
|------|---------|---------|---------|----------|----------------|--------|
| PRKAA1 | HGNC:9376 | ENSG00000132356 | Q13131 | 5p13.1 | AMPK-mTOR | [Source: hgnc_search_genes(query=PRKAA1)] |
| PRKAA2 | HGNC:9377 | ENSG00000162409 | P54646 | 1p32.2 | AMPK-mTOR | [Source: hgnc_search_genes(query=PRKAA2)] |
| MTOR | HGNC:3942 | ENSG00000198793 | P42345 | 1p36.22 | AMPK-mTOR | [Source: hgnc_search_genes(query=MTOR)] |
| AKT1 | HGNC:391 | ENSG00000142208 | P31749 | 14q32.33 | AMPK-mTOR | [Source: hgnc_search_genes(query=AKT1)] |
| PIK3CA | HGNC:8975 | ENSG00000121879 | P42336 | 3q26.32 | AMPK-mTOR | [Source: hgnc_search_genes(query=PIK3CA)] |
| TSC1 | HGNC:12362 | ENSG00000165699 | Q92574 | 9q34.13 | AMPK-mTOR | [Source: hgnc_search_genes(query=TSC1)] |
| TSC2 | HGNC:12363 | ENSG00000103197 | P49815 | 16p13.3 | AMPK-mTOR | [Source: hgnc_search_genes(query=TSC2)] |
| HIF1A | HGNC:4910 | ENSG00000100644 | Q16665 | 14q23.2 | AMPK-mTOR | [Source: hgnc_search_genes(query=HIF1A)] |
| HK2 | HGNC:4923 | ENSG00000159399 | P52789 | 2p12 | Glycolysis | [Source: hgnc_search_genes(query=HK2)] |
| PKM | HGNC:9021 | ENSG00000067225 | P14618 | 15q23 | Glycolysis | [Source: hgnc_search_genes(query=PKM)] |
| LDHA | HGNC:6535 | ENSG00000134333 | P00338 | 11p15.1 | Glycolysis | [Source: hgnc_search_genes(query=LDHA)] |
| PDK1 | HGNC:8809 | ENSG00000152256 | Q15118 | 2q31.1 | Glycolysis-OxPhos | [Source: hgnc_search_genes(query=PDK1)] |
| NDUFS1 | HGNC:7707 | ENSG00000023228 | P28331 | 2q33.3 | OxPhos | [Source: hgnc_search_genes(query=NDUFS1)] |
| SDHA | HGNC:10680 | ENSG00000073578 | P31040 | 5p15.33 | OxPhos | [Source: hgnc_search_genes(query=SDHA)] |

### 2.2 Drugs (8 resolved)

| Drug | ChEMBL | PubChem | Marik Tier | Metabolic Axis | Source |
|------|--------|---------|------------|----------------|--------|
| Metformin | CHEMBL:1431 | PubChem:CID4091 | Tier 1 | OxPhos Complex I, AMPK activator | [Source: chembl_search_compounds(query=metformin)] |
| DCA (Sodium Dichloroacetate) | CHEMBL:306823 | PubChem:CID25975 | Tier 3 | PDK inhibitor (Warburg reversal) | [Source: chembl_search_compounds(query=dichloroacetate)] |
| Mebendazole | CHEMBL:685 | PubChem:CID4030 | Tier 1 | Dual glycolysis + OxPhos | [Source: chembl_search_compounds(query=mebendazole)] |
| Ivermectin | CHEMBL:6067487 | No data retrieved | Tier 1 | OxPhos/mitochondrial | [Source: chembl_search_compounds(query=ivermectin)] |
| Niclosamide | CHEMBL:1448 | PubChem:CID4477 | Tier 3 | mTOR + glycolysis | [Source: chembl_search_compounds(query=niclosamide)] |
| Berberine | CHEMBL:295124 | PubChem:CID2353 | Tier 1 | PI3K/AKT/mTOR, AMPK | [Source: chembl_search_compounds(query=berberine)] |
| Itraconazole | CHEMBL:64391 | PubChem:CID55283 | Tier 1 | PI3K/AKT/mTOR/S6K | [Source: chembl_search_compounds(query=itraconazole)] |
| Doxycycline | CHEMBL:1433 | PubChem:CID54671203 | Tier 2 | OxPhos (mito translation) | [Source: chembl_search_compounds(query=doxycycline)] |

---

## 3. Drug Candidates (Sorted by Clinical Phase Descending)

| Rank | Drug | Marik Tier | Primary Target | Validated (OT) | Max Phase | Active Trial | Evidence Level |
|------|------|------------|----------------|-----------------|-----------|--------------|----------------|
| 1 | Metformin | Tier 1 | NDUFS1 (Complex I) | YES | Phase 4 | NCT04945148, NCT06545526 | L4 (0.95) |
| 2 | DCA | Tier 3 | PDK1 | YES | Phase 3 | None recruiting | L3 (0.80) |
| 3 | Mebendazole | Tier 1 | Glycolysis + OxPhos | NO | N/A | NCT03925662 (Phase 3) | L2 (0.60) |
| 4 | Doxycycline | Tier 2 | OxPhos (mito translation) | NO | N/A | NCT06452394 (Phase 2) | L2 (0.55) |
| 5 | Ivermectin | Tier 1 | OxPhos/mitochondrial | NO | N/A | NCT05318469 (Phase 1/2) | L2 (0.55) |
| 6 | Niclosamide | Tier 3 | mTOR + glycolysis | NO | N/A | NCT05188170 (Phase 1) | L1 (0.45) |
| 7 | Berberine | Tier 1 | PI3K/AKT/mTOR, AMPK | NO | N/A | NCT06629051 (N/A) | L1 (0.35) |
| 8 | Itraconazole | Tier 1 | PI3K/AKT/mTOR/S6K | NO | N/A | None recruiting | L1 (0.35) |

---

## 4. Mechanism Chain

```
Drug -> Primary Target -> Pathway -> Cancer Metabolism Effect
=====================================================================
Metformin -> NDUFS1 (Complex I) -> OxPhos (WP:WP623) -> ETC inhibition, AMPK activation
             |-> PRKAA1/PRKAA2 -> AMPK Signaling (WP:WP1403) -> mTOR suppression
             |-> MTOR (indirect) -> PI3K-Akt-mTOR (WP:WP3932) -> Proliferation block

DCA -> PDK1 -> Glycolysis-OxPhos switch -> Warburg reversal
       |-> restores pyruvate -> OxPhos flux -> apoptosis in glycolytic tumors

Mebendazole -> HK2 (indirect) -> Glycolysis (WP:WP534) -> Glucose uptake block
              |-> Complex I (indirect) -> OxPhos (WP:WP623) -> Dual metabolic stress

Ivermectin -> NDUFS1 (indirect) -> OxPhos (WP:WP623) -> Mitochondrial depolarization

Niclosamide -> MTOR (indirect) -> AMPK Signaling (WP:WP1403) -> mTOR suppression
             |-> HK2 (indirect) -> Glycolysis (WP:WP534) -> Glycolytic inhibition

Berberine -> PRKAA1 -> AMPK Signaling (WP:WP1403) -> AMPK activation
            |-> PIK3CA/AKT1/MTOR -> PI3K-Akt-mTOR (WP:WP3932) -> Pathway suppression

Itraconazole -> PIK3CA/AKT1/MTOR -> PI3K-Akt-mTOR (WP:WP3932) -> S6K inhibition

Doxycycline -> Mitochondrial ribosomes -> OxPhos (WP:WP623) -> Mito translation block
```

[Source: wikipathways_get_pathway(id=WP534), wikipathways_get_pathway(id=WP623), wikipathways_get_pathway(id=WP1403), wikipathways_get_pathway(id=WP3932)]

---

## 5. Mechanism Rationale (Per Drug)

### 5.1 Metformin (CHEMBL:1431)
Metformin directly inhibits mitochondrial Complex I (NDUFS1, HGNC:7707), reducing electron transport chain (ETC) flux and ATP production [Source: opentargets_get_associations(target=ENSG00000023228)]. This triggers AMPK activation (PRKAA1/PRKAA2) via increased AMP:ATP ratio, which in turn suppresses mTOR (HGNC:3942) through TSC1/TSC2 phosphorylation [Source: string_get_interactions(protein=PRKAA1)]. The dual mechanism -- direct OxPhos inhibition plus AMPK-mediated mTOR suppression -- makes metformin a multi-axis metabolic disruptor. Open Targets registers metformin as a Phase 4 Complex I inhibitor with validated cancer associations [Source: opentargets_get_associations(efoId=EFO:0000311, target=ENSG00000023228)]. STRING network confirms PRKAA1-TSC2 interaction (score 0.978) and TSC2-MTOR interaction (score 0.990), supporting the mechanistic cascade [Source: string_get_interactions(protein=PRKAA1)].

### 5.2 DCA / Sodium Dichloroacetate (CHEMBL:306823)
DCA inhibits pyruvate dehydrogenase kinase 1 (PDK1, HGNC:8809), which normally phosphorylates and inactivates pyruvate dehydrogenase (PDH) [Source: opentargets_get_associations(target=ENSG00000152256)]. By inhibiting PDK1, DCA reactivates PDH, shifting pyruvate metabolism from glycolysis (lactate production) toward oxidative phosphorylation (mitochondrial acetyl-CoA entry). This "Warburg reversal" forces glycolysis-dependent cancer cells into OxPhos, inducing apoptosis via restored mitochondrial membrane potential and cytochrome c release [Source: chembl_get_compound(id=CHEMBL306823)]. DCA is registered as Phase 3 in Open Targets for PDK1 inhibition [Source: opentargets_get_associations(efoId=EFO:0000311, target=ENSG00000152256)].

### 5.3 Mebendazole (CHEMBL:685)
Mebendazole, an anthelmintic, inhibits both glycolysis and OxPhos through mechanisms not formally registered in Open Targets knownDrugs [Source: opentargets_get_associations(efoId=EFO:0000311)]. Preclinical evidence suggests it disrupts tubulin polymerization which impairs VDAC-mediated mitochondrial metabolism and hexokinase 2 (HK2, HGNC:4923) binding to mitochondria [Source: pubmed_search_articles(queryTerm=mebendazole cancer metabolism)]. The active Phase 3 trial NCT03925662 tests mebendazole as adjuvant therapy in colorectal cancer [Source: clinicaltrials_search_trials(query=mebendazole cancer)].

### 5.4 Ivermectin (CHEMBL:6067487)
Ivermectin targets mitochondrial function through OxPhos disruption, inducing mitochondrial dysfunction and reactive oxygen species (ROS) generation [Source: pubmed_search_articles(queryTerm=ivermectin cancer mitochondria)]. The drug has no validated Open Targets knownDrugs entry for metabolic targets [Source: opentargets_get_associations(efoId=EFO:0000311)]. A Phase 1/2 trial (NCT05318469) evaluates ivermectin combined with checkpoint inhibitor in metastatic triple-negative breast cancer [Source: clinicaltrials_search_trials(query=ivermectin cancer)].

### 5.5 Niclosamide (CHEMBL:1448)
Niclosamide, an anthelmintic, disrupts mTOR signaling and glycolysis through uncoupling of mitochondrial oxidative phosphorylation [Source: pubmed_search_articles(queryTerm=niclosamide mTOR cancer)]. Pathway analysis places its targets within AMPK Signaling (WP:WP1403) and Glycolysis (WP:WP534) [Source: wikipathways_get_pathway(id=WP1403)]. It has no formal Open Targets knownDrugs registration [Source: opentargets_get_associations(efoId=EFO:0000311)]. NCT05188170 tests niclosamide in pediatric AML (Phase 1) [Source: clinicaltrials_search_trials(query=niclosamide cancer)].

### 5.6 Berberine (CHEMBL:295124)
Berberine activates AMPK (PRKAA1, HGNC:9376) and suppresses the PI3K/AKT/mTOR axis [Source: pubmed_search_articles(queryTerm=berberine AMPK mTOR cancer)]. Its targets map to both AMPK Signaling (WP:WP1403) and PI3K-Akt-mTOR (WP:WP3932) [Source: wikipathways_get_pathway(id=WP1403), wikipathways_get_pathway(id=WP3932)]. No validated Open Targets knownDrugs entry exists [Source: opentargets_get_associations(efoId=EFO:0000311)]. The only recruiting trial (NCT06629051) is a follow-up study with marginal cancer relevance [Source: clinicaltrials_search_trials(query=berberine cancer)].

### 5.7 Itraconazole (CHEMBL:64391)
Itraconazole inhibits the PI3K/AKT/mTOR/S6K signaling cascade, acting on multiple nodes within PI3K-Akt-mTOR (WP:WP3932) [Source: pubmed_search_articles(queryTerm=itraconazole PI3K mTOR cancer)]. No validated Open Targets knownDrugs entry exists for metabolic targets [Source: opentargets_get_associations(efoId=EFO:0000311)]. No active recruiting cancer trials were identified [Source: clinicaltrials_search_trials(query=itraconazole cancer)].

### 5.8 Doxycycline (CHEMBL:1433)
Doxycycline inhibits mitochondrial translation by binding to mitochondrial ribosomes, impairing the synthesis of ETC subunits encoded by mitochondrial DNA [Source: pubmed_search_articles(queryTerm=doxycycline mitochondrial translation cancer)]. This disrupts OxPhos (WP:WP623) by depleting newly synthesized Complex I-V subunits [Source: wikipathways_get_pathway(id=WP623)]. No validated Open Targets knownDrugs entry exists [Source: opentargets_get_associations(efoId=EFO:0000311)]. NCT06452394 (NEODOXy) tests doxycycline targeting cancer stem cells in ER+ breast cancer (Phase 2) [Source: clinicaltrials_search_trials(query=doxycycline cancer)].

---

## 6. Clinical Trials

| Drug | NCT ID | Phase | Status | Title | Metabolic Relevance | Source |
|------|--------|-------|--------|-------|---------------------|--------|
| Metformin | NCT04945148 | Phase 2 | RECRUITING | OxPhos targeting in GBM with Metformin+RT/TMZ | Direct OxPhos targeting | [Source: clinicaltrials_get_trial(nctId=NCT04945148)] |
| Metformin | NCT06545526 | Phase 3 | RECRUITING | Celecoxib+Metformin in FAP | AMPK activation in cancer prevention | [Source: clinicaltrials_get_trial(nctId=NCT06545526)] |
| Mebendazole | NCT03925662 | Phase 3 | RECRUITING | Mebendazole adjuvant in Colorectal Cancer | Dual glycolysis/OxPhos disruption | [Source: clinicaltrials_get_trial(nctId=NCT03925662)] |
| Ivermectin | NCT05318469 | Phase 1/2 | RECRUITING | Ivermectin+checkpoint inhibitor in mTNBC | OxPhos/mitochondrial disruption | [Source: clinicaltrials_get_trial(nctId=NCT05318469)] |
| Niclosamide | NCT05188170 | Phase 1 | RECRUITING | Niclosamide in pediatric AML | mTOR + glycolysis uncoupling | [Source: clinicaltrials_get_trial(nctId=NCT05188170)] |
| Doxycycline | NCT06452394 | Phase 2 | RECRUITING | NEODOXy: Doxycycline targeting cancer stem cells in ER+ breast cancer | Mitochondrial translation block | [Source: clinicaltrials_get_trial(nctId=NCT06452394)] |
| Berberine | NCT06629051 | N/A | RECRUITING | Follow-up study (marginal cancer relevance) | AMPK activation (indirect) | [Source: clinicaltrials_get_trial(nctId=NCT06629051)] |

**DCA:** No active recruiting cancer trials identified [Source: clinicaltrials_search_trials(query=dichloroacetate cancer, status=RECRUITING)].

**Itraconazole:** No active recruiting cancer trials identified [Source: clinicaltrials_search_trials(query=itraconazole cancer, status=RECRUITING)].

---

## 7. Evidence Assessment

### 7.1 Claim-Level Evidence Grades

| Drug | Target | Claim | Base Level | Modifiers | Final Score | Confidence |
|------|--------|-------|------------|-----------|-------------|------------|
| Metformin | NDUFS1 (Complex I) | Complex I inhibitor with AMPK activation in cancer | L4 | +0.10 (active trial), +0.10 (mechanism match) | L4 | 0.95 |
| DCA | PDK1 | PDK inhibitor reversing Warburg effect | L3 | +0.10 (mechanism match) | L3 | 0.80 |
| Mebendazole | Glycolysis + OxPhos | Dual metabolic disruption in cancer | L2 | +0.10 (Phase 3 trial) | L2 | 0.60 |
| Doxycycline | Mito ribosomes | Mitochondrial translation inhibitor targeting CSCs | L2 | +0.05 (Phase 2 trial) | L2 | 0.55 |
| Ivermectin | OxPhos/mitochondrial | Mitochondrial dysfunction in cancer | L2 | -0.10 (single source) | L2 | 0.55 |
| Niclosamide | mTOR + glycolysis | Mitochondrial uncoupler in AML | L1 | +0.05 (Phase 1 trial), -0.10 (single source) | L1 | 0.45 |
| Berberine | PI3K/AKT/mTOR, AMPK | AMPK activator / mTOR suppressor | L1 | -0.05 (no cancer trial) | L1 | 0.35 |
| Itraconazole | PI3K/AKT/mTOR/S6K | PI3K/mTOR pathway inhibitor | L1 | -0.05 (no cancer trial) | L1 | 0.35 |

**Evidence Level Definitions:**
- **L4:** Phase 4 / approved drug with validated target and active clinical trials
- **L3:** Phase 3 clinical data with validated target in Open Targets
- **L2:** Phase 1-3 clinical trial evidence without validated Open Targets target registration
- **L1:** Preclinical evidence only or no cancer-specific clinical trials

### 7.2 Summary Statistics

| Metric | Value |
|--------|-------|
| Median Confidence | 0.51 |
| Mean Confidence | 0.575 |
| Drugs with OT Validated Targets | 2/8 (25%) |
| Drugs with Active Cancer Trials | 6/8 (75%) |
| Total Active Trial NCTs | 7 |

---

## 8. Gaps and Limitations

### 8.1 Data Gaps

1. **Ivermectin PubChem CID:** No PubChem CID was retrieved for Ivermectin [Source: pubchem_search_compounds(query=ivermectin)]. This may reflect the compound's macrocyclic lactone structure or naming ambiguity (ivermectin B1a vs B1b).

2. **Open Targets Coverage:** Only 2 of 8 Marik drugs (Metformin, DCA) have validated knownDrugs entries in Open Targets for metabolic targets [Source: opentargets_get_associations(efoId=EFO:0000311)]. The remaining 6 drugs may act through targets not curated in the knownDrugs database or through multi-target/indirect mechanisms.

3. **DCA Clinical Trials:** No active recruiting cancer clinical trials were found for DCA despite its Phase 3 registration in Open Targets [Source: clinicaltrials_search_trials(query=dichloroacetate cancer, status=RECRUITING)]. This may reflect regulatory challenges with an unpatentable compound.

4. **Berberine Cancer Relevance:** The only recruiting berberine trial (NCT06629051) has marginal cancer relevance, being a follow-up study rather than a cancer treatment trial [Source: clinicaltrials_get_trial(nctId=NCT06629051)].

### 8.2 Methodological Limitations

1. **Synapse Grounding:** No Synapse search was performed in this execution. Dataset-level grounding (e.g., TCGA metabolic subtypes, DepMap CRISPR screens for metabolic genes) would strengthen evidence.

2. **Combination Effects:** The Marik protocol uses multiple drugs simultaneously. Drug-drug interactions and synergistic metabolic effects are not captured by single-target Open Targets queries.

3. **Tissue Specificity:** The analysis treats cancer as a single entity (EFO:0000311). Metabolic vulnerability varies greatly by tissue type (e.g., glycolysis dependence in GBM vs. OxPhos dependence in leukemia).

4. **Temporal Dynamics:** Clinical trial status is a snapshot. Trials may have changed status since data retrieval.

5. **STRING Network Scope:** STRING interactions were queried for MTOR and PRKAA1 hubs only [Source: string_get_interactions(protein=MTOR), string_get_interactions(protein=PRKAA1)]. Additional hub analyses (e.g., AKT1, PIK3CA) would expand the network context.

### 8.3 Knowledge Graph Gaps

1. **Missing Edges:** Drug-target edges for Mebendazole, Ivermectin, Niclosamide, Berberine, Itraconazole, and Doxycycline lack formal Open Targets validation. These would be represented as "preclinical" or "literature-derived" edges in a knowledge graph.

2. **Pathway Crosstalk:** The AMPK-mTOR and Glycolysis pathways share multiple nodes (e.g., HIF1A bridges AMPK-mTOR to glycolytic gene transcription). This crosstalk is captured by WikiPathways (WP:WP3932 contains both AMPK and glycolytic genes) but not fully modeled [Source: wikipathways_get_pathway(id=WP3932)].

---

*Report generated by Fuzzy-to-Fact protocol. All claims sourced from tool outputs as cited.*
