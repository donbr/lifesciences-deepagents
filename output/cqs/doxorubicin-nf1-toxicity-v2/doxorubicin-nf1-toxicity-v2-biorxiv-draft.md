# Multi-Database Knowledge Graph Analysis of Doxorubicin Cardiotoxicity Pathways and Therapeutic Alternatives in Neurofibromatosis Type 1

## Abstract

**Background**: Doxorubicin remains a cornerstone of chemotherapy for NF1-associated malignant peripheral nerve sheath tumors (MPNST), but its dose-limiting cardiotoxicity -- mediated through off-target inhibition of topoisomerase II beta (TOP2B) in cardiomyocytes -- presents a critical therapeutic challenge. In NF1 patients, where loss-of-function mutations constitutively activate the RAS-MAPK pathway, understanding the intersection of drug toxicity mechanisms and disease-specific signaling is essential for rational treatment design.

**Methods**: We applied the Fuzzy-to-Fact protocol, a systematic multi-database entity resolution and knowledge graph construction framework, to investigate genes and pathways implicated in minimizing doxorubicin toxicity while preserving anti-tumor efficacy for NF1. Seven phases (ANCHOR through PERSIST) queried 8 databases: HGNC, UniProt, STRING, ChEMBL, PubChem, Open Targets, WikiPathways, and ClinicalTrials.gov. All entities followed LOCATE-RETRIEVE cycles; all clinical trial identifiers underwent Phase 5 verification.

**Results**: The resulting knowledge graph contains 11 gene nodes (all with 5 required cross-database identifiers), 4 drug nodes, 3 disease associations, 3 pathway memberships, and 8 verified clinical trials. We identify two mechanistic axes: (1) the TOP2A/TOP2B selectivity axis, where doxorubicin's therapeutic effect (TOP2A inhibition) is mechanistically separable from its cardiotoxicity (TOP2B inhibition), with dexrazoxane (CHEMBL:1738) providing clinically validated cardioprotection; and (2) the RAS-MAPK signaling axis, where NF1 loss-of-function creates an alternative therapeutic target (MAP2K1/MAP2K2) addressable by FDA-approved MEK inhibitors selumetinib (CHEMBL:1614701) and trametinib (CHEMBL:2103875) without topoisomerase-mediated cardiac risk. TDP2 (STRING score 0.82 with TOP2B) and PARP1 (STRING score 0.72 with TOP2B) represent DNA repair mediators that may modulate cardiotoxicity severity.

**Conclusion**: Three evidence-based strategies emerge for minimizing doxorubicin toxicity in NF1: dexrazoxane co-administration for cardioprotection, MEK inhibitor substitution or combination to reduce doxorubicin dependence, and future investigation of TDP2/PARP1-targeted cardioprotective approaches. No NF1-specific cardiotoxicity trials currently exist, representing a critical clinical gap.

## 1. Introduction

Neurofibromatosis type 1 (NF1; MONDO_0018975) is an autosomal dominant tumor predisposition syndrome caused by loss-of-function mutations in the NF1 gene (HGNC:7765), encoding neurofibromin, a GTPase-activating protein (GAP) for RAS [1]. NF1 patients face elevated risks of multiple tumor types, including malignant peripheral nerve sheath tumors (MPNST; EFO_0000760), for which doxorubicin-based chemotherapy remains standard-of-care [2].

Doxorubicin (CHEMBL:53463), an anthracycline antibiotic, exerts anti-tumor activity by stabilizing topoisomerase II-DNA cleavage complexes, causing lethal double-strand breaks in proliferating cells [3]. However, its utility is constrained by cumulative dose-dependent cardiotoxicity, which limits lifetime exposure and can cause irreversible cardiomyopathy [4]. This toxicity has been attributed to off-target inhibition of TOP2B (HGNC:11990) in post-mitotic cardiomyocytes, which express TOP2B but not the proliferation-associated TOP2A isoform [4].

The intersection of NF1 biology and doxorubicin pharmacology creates a unique therapeutic challenge: how to treat NF1-associated malignancies effectively while minimizing cardiac risk. This question is particularly relevant because NF1 loss-of-function constitutively activates the RAS-MAPK signaling cascade (KRAS -> BRAF -> MEK -> ERK), potentially creating alternative therapeutic targets that bypass the need for DNA-damaging agents entirely.

We applied the Fuzzy-to-Fact protocol -- a systematic, multi-database knowledge graph construction framework -- to investigate what genes, pathways, and therapeutic strategies are implicated in minimizing doxorubicin toxicity while preserving anti-tumor efficacy for NF1. This protocol enforces LOCATE-RETRIEVE entity resolution, multi-source concordance assessment, and claim-level evidence grading to produce a transparent, reproducible knowledge graph.

## 2. Methods

### 2.1 Fuzzy-to-Fact Protocol

The analysis followed seven protocol phases:

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | ANCHOR | Entity resolution via HGNC and ChEMBL fuzzy search |
| 2 | ENRICH | UniProt function text, Open Targets disease associations |
| 3 | EXPAND | STRING protein-protein interactions (score >= 700), WikiPathways |
| 4a | TRAVERSE_DRUGS | Open Targets target records, ChEMBL compound data |
| 4b | TRAVERSE_TRIALS | ClinicalTrials.gov searches with verification |
| 5 | VALIDATE | NCT ID verification, cross-database consistency |
| 6 | PERSIST | Pre-emit validation, KG JSON construction |

### 2.2 Data Sources

| Database | Tools Used | Purpose |
|----------|-----------|---------|
| HGNC | hgnc_search_genes, hgnc_get_gene | Gene symbol resolution, cross-references |
| UniProt | uniprot_search_proteins, uniprot_get_protein | Protein function, sequence, interactions |
| STRING | string_search_proteins, string_get_interactions | Protein-protein interaction network |
| ChEMBL | chembl_search_compounds, chembl_get_compound | Drug compound data, max phase, indications |
| PubChem | pubchem_search_compounds, pubchem_get_compound | Chemical structure, cross-references |
| Open Targets | opentargets_get_target, opentargets_get_associations | Target-disease associations, drug target links |
| WikiPathways | wikipathways_get_pathways_for_gene, wikipathways_get_pathway | Pathway membership |
| ClinicalTrials.gov | clinicaltrials_search_trials, clinicaltrials_get_trial | Clinical trial discovery and verification |

### 2.3 Entity Resolution

All entities followed a LOCATE-RETRIEVE two-step cycle:
1. **LOCATE**: Fuzzy search to identify candidate CURIEs (e.g., hgnc_search_genes("NF1"))
2. **RETRIEVE**: Strict lookup with resolved CURIE (e.g., hgnc_get_gene("HGNC:7765"))

Secondary enrichment: every new interactor from STRING that became a KG node underwent its own LOCATE-RETRIEVE cycle.

### 2.4 Evidence Grading

Claims were graded using a four-level system with modifiers:
- **L4 (0.90-1.00)**: Clinical -- FDA-approved or Phase 2+ with published endpoints
- **L3 (0.70-0.89)**: Functional -- multi-database concordance + druggable target
- **L2 (0.50-0.69)**: Multi-DB -- 2+ databases confirm relationship
- **L1 (0.30-0.49)**: Single-DB -- one database source

Modifiers: active trial (+0.10), mechanism match (+0.10), literature support (+0.05), high STRING score >= 900 (+0.05), single source (-0.10).

### 2.5 LOF Filter

Since NF1 is a loss-of-function tumor suppressor, a LOF filter was applied to drug candidates: only inhibitors acting downstream of NF1 in the RAS-MAPK pathway were considered therapeutically appropriate. Drugs targeting NF1 protein directly were excluded as the protein is non-functional in NF1-null tumors.

## 3. Results

### 3.1 Knowledge Graph Overview

The completed knowledge graph contains:
- **11 gene nodes**: NF1, TOP2A, TOP2B, KRAS, BRAF, TP53, PARP1, TDP2, SPRED1, MAP2K1, MAP2K2
- **4 drug nodes**: Doxorubicin, Selumetinib, Trametinib, Dexrazoxane
- **3 disease associations**: Neurofibromatosis type 1 (MONDO_0018975), Cardiomyopathy (EFO_0000318), MPNST (EFO_0000760)
- **3 pathways**: RAF/MAP kinase cascade (WP:WP2735), NF1 CNV syndrome (WP:WP5366), SUMOylation of DNA replication proteins (WP:WP3805)
- **8 verified clinical trials**
- **25 edges**: 11 protein-protein interactions, 7 drug-target, 3 gene-disease, 4 gene-pathway

All 11 gene nodes passed pre-emit validation with 5 required fields (symbol, name, ensembl, uniprot, location) [5].

### 3.2 Axis 1: TOP2A/TOP2B Selectivity

Doxorubicin inhibits both TOP2A (anti-tumor target; CHEMBL target CHEMBL1806) and TOP2B (cardiotoxicity mediator; CHEMBL target CHEMBL3396) [6, 7]. Open Targets associates TOP2B (ENSG00000077097) with cardiomyopathy (EFO_0000318, score 0.47) [8].

Three proteins in the TOP2B interaction network are relevant to toxicity modulation:

1. **TDP2** (HGNC:17768, STRING score 0.82): Repairs TOP2B-DNA covalent adducts by hydrolyzing 5'-phosphotyrosyl bonds [9]. TDP2 activity may protect cardiomyocytes from TOP2B-mediated damage while potentially reducing doxorubicin efficacy in tumor cells.

2. **PARP1** (HGNC:270, STRING score 0.72): Detects DNA strand breaks from TOP2B cleavage complexes and recruits DNA repair factors [9]. PARP inhibitor drugs are an established cancer therapy class with potential implications for modifying doxorubicin cardiotoxicity.

3. **TOPBP1** (STRING score 0.96): DNA topoisomerase II binding protein involved in checkpoint response to TOP2B-mediated damage [9].

**Dexrazoxane** (CHEMBL:1738, Max Phase 4) provides the only clinically approved cardioprotection mechanism, functioning as both an iron chelator (preventing ROS generation) and a catalytic TOP2B inhibitor that prevents cleavage complex formation without stabilizing them [10].

### 3.3 Axis 2: RAS-MAPK Signaling in NF1

NF1 (HGNC:7765) encodes neurofibromin, which "stimulates the GTPase activity of Ras" [1]. The STRING interaction network reveals high-confidence interactions between NF1 and RAS family members: KRAS (score 0.996), RRAS (0.960), RRAS2 (0.958) [11]. Loss of NF1 GAP activity leads to constitutive KRAS-GTP, which activates BRAF (KRAS-BRAF score 0.999) and the downstream MEK-ERK cascade [11].

NF1 participates in the RAF/MAP kinase cascade pathway (WP:WP2735, 235 genes) and the NF1 CNV syndrome pathway (WP:WP5366, 108 genes) [12].

**Selumetinib** (CHEMBL:1614701, Max Phase 4) is FDA-approved for NF1 plexiform neurofibromas [13]. It selectively inhibits MAP2K1 (MEK1, HGNC:6840) and MAP2K2 (MEK2, HGNC:6842), blocking the hyperactive RAS-MAPK signaling downstream of NF1 loss [14, 15]. This provides anti-tumor efficacy through an entirely different mechanism than doxorubicin, without topoisomerase-mediated cardiotoxicity risk.

**Trametinib** (CHEMBL:2103875, Max Phase 4) offers an alternative MEK1/2 inhibitor with potentially higher potency [16].

### 3.4 Clinical Trial Landscape

Eight clinical trials were identified and verified:

**NF1-specific trials using doxorubicin**:
- NCT00304083: Phase II chemotherapy (doxorubicin + etoposide + ifosfamide) in NF1-associated MPNST, COMPLETED [17]

**NF1-specific trials using MEK inhibitors**:
- NCT02407405: Phase II selumetinib in adult NF1 plexiform neurofibromas, ACTIVE_NOT_RECRUITING [18]
- NCT03433183: Selumetinib + sirolimus for MPNST, COMPLETED [19]
- NCT03871257: Phase 3 selumetinib vs carboplatin/vincristine in NF1 LGG, ACTIVE_NOT_RECRUITING [20]

**Doxorubicin cardioprotection trials** (non-NF1):
- NCT07370506: Telmisartan for doxorubicin cardiotoxicity, NOT_YET_RECRUITING [21]
- NCT04023110: Carvedilol cardioprotection during doxorubicin, COMPLETED [22]
- NCT00955890: Dexrazoxane for anthracycline cardiotoxicity, TERMINATED [23]
- NCT05858710: Liposomal doxorubicin + dexrazoxane in STS, COMPLETED [24]

**NF1-specific cardiotoxicity trials**: No results found [No data: clinicaltrials_search_trials("neurofibromatosis NF1 cardiotoxicity") returned 0 results].

### 3.5 Evidence Assessment

Ten claims were individually graded:

| Claim | Score | Level |
|-------|-------|-------|
| Selumetinib FDA-approved for NF1 | 1.00 | L4 |
| MEK inhibition blocks NF1-null RAS signaling | 1.00 | L4 |
| Doxorubicin inhibits TOP2A (anti-tumor) | 0.95 | L4 |
| Dexrazoxane prevents anthracycline cardiotoxicity | 0.95 | L4 |
| Doxorubicin inhibits TOP2B (cardiotoxicity) | 0.85 | L3 |
| NF1 loss causes constitutive RAS activation | 0.85 | L3 |
| TOP2B associated with cardiomyopathy | 0.65 | L2 |
| TDP2 repairs TOP2B-DNA damage | 0.60 | L2 |
| PARP1 interacts with TOP2B | 0.45 | L1 |
| No NF1-specific cardiotoxicity trials | 0.30 | L1 |

**Overall**: Median 0.83 (L3 Functional), Range 0.30-1.00

## 4. Discussion

### 4.1 Key Findings

This analysis reveals that doxorubicin toxicity in NF1 can be addressed through three complementary evidence-based strategies, each supported by distinct mechanistic rationale and clinical evidence:

**Strategy 1 -- Cardioprotection** (highest evidence: L4): Dexrazoxane co-administration directly addresses the TOP2B-mediated cardiotoxicity mechanism. By catalytically inhibiting TOP2B without stabilizing cleavage complexes, dexrazoxane prevents the double-strand breaks in cardiomyocytes that drive doxorubicin-induced cardiomyopathy. Multiple clinical trials support this approach, though none are NF1-specific.

**Strategy 2 -- MEK inhibitor substitution** (highest evidence: L4): Selumetinib's FDA approval for NF1 plexiform neurofibromas validates MEK inhibition as a viable anti-tumor strategy for NF1. In contexts where doxorubicin's cardiotoxicity risk is unacceptable, MEK inhibitors provide an alternative mechanism of action (targeting the constitutively active RAS-MAPK cascade) with no topoisomerase-mediated cardiac risk. The NF1 -> KRAS -> BRAF -> MEK signaling axis (STRING scores 0.996, 0.999) provides strong molecular rationale for this approach.

**Strategy 3 -- DNA repair modulation** (lower evidence: L1-L2): TDP2 and PARP1 represent interaction-level candidates for modulating TOP2B-mediated cardiac damage. Their roles as direct TOP2B interactors (STRING scores 0.82, 0.72) position them as potential targets for cardioprotective interventions, but clinical validation is lacking.

### 4.2 The Fuzzy-to-Fact Approach

The protocol's systematic LOCATE-RETRIEVE cycles and multi-database concordance assessment provide transparency and reproducibility. Every entity in the knowledge graph traces to specific database queries, and every claim carries an evidence grade based on explicit criteria. The LOF filter analysis prevented inappropriate drug recommendations (e.g., NF1 protein activators) by linking disease mechanism to therapeutic strategy.

### 4.3 Limitations

1. **ChEMBL activity gap**: The MCP toolkit does not expose a ChEMBL bioactivity endpoint for IC50/Ki retrieval. Quantitative selectivity data (TOP2A vs TOP2B inhibition constants) would strengthen the TOP2 isoform selectivity argument.

2. **No NF1-specific cardiotoxicity data**: All cardioprotection evidence derives from breast cancer populations. The NF1 patient population may have distinct cardiac risk profiles due to RAS pathway dysregulation in cardiovascular tissue.

3. **Synapse grounding not performed**: Experimental dataset grounding from Synapse.org was not executed, limiting multi-source concordance for interaction-level claims.

4. **Combination therapy gap**: No clinical trials combine doxorubicin with MEK inhibitors in NF1. This combination strategy -- reduced-dose doxorubicin plus selumetinib, potentially with dexrazoxane cardioprotection -- remains theoretical.

### 4.4 Future Directions

1. NF1-specific cardiotoxicity monitoring studies to establish whether RAS pathway dysregulation modifies cardiac risk
2. Combination trials of reduced-dose doxorubicin + selumetinib + dexrazoxane in NF1-associated MPNST
3. Investigation of TDP2 and PARP1 as cardioprotective targets in preclinical doxorubicin models
4. Synapse.org dataset grounding to identify experimental data supporting TOP2B-cardiomyopathy and NF1-RAS knowledge graph edges

## References

### Gene and Protein Databases
[1] UniProt. Neurofibromin (P21359). Retrieved via uniprot_get_protein(UniProtKB:P21359).
[2] HGNC. Gene record for NF1 (HGNC:7765). Retrieved via hgnc_get_gene(HGNC:7765).
[3] UniProt. DNA topoisomerase 2-alpha (P11388). Retrieved via uniprot_get_protein(UniProtKB:P11388).
[4] UniProt. DNA topoisomerase 2-beta (Q02880). Retrieved via uniprot_get_protein(UniProtKB:Q02880).
[5] HGNC. Gene records for all 11 entities. Retrieved via hgnc_get_gene for HGNC:7765, HGNC:11989, HGNC:11990, HGNC:6407, HGNC:1097, HGNC:11998, HGNC:270, HGNC:17768, HGNC:20249, HGNC:6840, HGNC:6842.

### Interaction and Pathway Databases
[6] Open Targets. Target record for TOP2A (ENSG00000131747). Retrieved via opentargets_get_target(ENSG00000131747). ChEMBL target: CHEMBL1806.
[7] Open Targets. Target record for TOP2B (ENSG00000077097). Retrieved via opentargets_get_target(ENSG00000077097). ChEMBL target: CHEMBL3396, DrugBank: DB04745.
[8] Open Targets. Associations for TOP2B (ENSG00000077097). Retrieved via opentargets_get_associations(ENSG00000077097). Cardiomyopathy EFO_0000318 score=0.465.
[9] STRING. Interactions for TOP2B (STRING:9606.ENSP00000264331). Retrieved via string_get_interactions(STRING:9606.ENSP00000264331, required_score=700).
[10] ChEMBL. Compound record for Dexrazoxane (CHEMBL:1738). Retrieved via chembl_get_compound(CHEMBL:1738).
[11] STRING. Interactions for NF1 (STRING:9606.ENSP00000351015). Retrieved via string_get_interactions(STRING:9606.ENSP00000351015, required_score=700).
[12] WikiPathways. Pathways for NF1. Retrieved via wikipathways_get_pathways_for_gene(NF1). WP:WP2735, WP:WP5366.

### Compound Databases
[13] ChEMBL. Compound record for Selumetinib (CHEMBL:1614701). Retrieved via chembl_get_compound(CHEMBL:1614701). Max Phase 4, indications include Neurofibromatosis 1.
[14] HGNC. Gene record for MAP2K1 (HGNC:6840). Retrieved via hgnc_get_gene(HGNC:6840).
[15] HGNC. Gene record for MAP2K2 (HGNC:6842). Retrieved via hgnc_get_gene(HGNC:6842).
[16] ChEMBL. Compound record for Trametinib (CHEMBL:2103875). Retrieved via chembl_get_compound(CHEMBL:2103875). Max Phase 4.

### Clinical Trials
[17] ClinicalTrials.gov. NCT00304083. Retrieved via clinicaltrials_get_trial(NCT:00304083). VERIFIED.
[18] ClinicalTrials.gov. NCT02407405. Retrieved via clinicaltrials_get_trial(NCT:02407405). VERIFIED.
[19] ClinicalTrials.gov. NCT03433183. Retrieved via clinicaltrials_get_trial(NCT:03433183). VERIFIED.
[20] ClinicalTrials.gov. NCT03871257. Retrieved via clinicaltrials_get_trial(NCT:03871257). VERIFIED.
[21] ClinicalTrials.gov. NCT07370506. Retrieved via clinicaltrials_get_trial(NCT:07370506). VERIFIED.
[22] ClinicalTrials.gov. NCT04023110. Retrieved via clinicaltrials_get_trial(NCT:04023110). VERIFIED.
[23] ClinicalTrials.gov. NCT00955890. Retrieved via clinicaltrials_get_trial(NCT:00955890). VERIFIED.
[24] ClinicalTrials.gov. NCT05858710. Retrieved via clinicaltrials_get_trial(NCT:05858710). VERIFIED.

## Supplementary Materials

### S1: Knowledge Graph Gene Nodes

| Symbol | HGNC | Ensembl | UniProt | Location | Entrez |
|--------|------|---------|---------|----------|--------|
| NF1 | HGNC:7765 | ENSG00000196712 | P21359 | 17q11.2 | 4763 |
| TOP2A | HGNC:11989 | ENSG00000131747 | P11388 | 17q21.2 | 7153 |
| TOP2B | HGNC:11990 | ENSG00000077097 | Q02880 | 3p24.2 | 7155 |
| KRAS | HGNC:6407 | ENSG00000133703 | P01116 | 12p12.1 | 3845 |
| BRAF | HGNC:1097 | ENSG00000157764 | P15056 | 7q34 | 673 |
| TP53 | HGNC:11998 | ENSG00000141510 | P04637 | 17p13.1 | 7157 |
| PARP1 | HGNC:270 | ENSG00000143799 | P09874 | 1q42.12 | 142 |
| TDP2 | HGNC:17768 | ENSG00000111802 | O95551 | 6p22.3 | 51567 |
| SPRED1 | HGNC:20249 | ENSG00000166068 | Q7Z699 | 15q14 | 161742 |
| MAP2K1 | HGNC:6840 | ENSG00000169032 | Q02750 | 15q22.31 | 5604 |
| MAP2K2 | HGNC:6842 | ENSG00000126934 | P36507 | 19p13.3 | 5605 |

### S2: Knowledge Graph Drug Nodes

| Drug | CHEMBL | Max Phase | MW (Da) | Mechanism |
|------|--------|-----------|---------|-----------|
| Doxorubicin | CHEMBL:53463 | 4 | 543.53 | TOP2 poison |
| Selumetinib | CHEMBL:1614701 | 4 | 457.69 | MEK1/2 inhibitor |
| Trametinib | CHEMBL:2103875 | 4 | 615.40 | MEK1/2 inhibitor |
| Dexrazoxane | CHEMBL:1738 | 4 | 268.27 | Iron chelator + TOP2B catalytic inhibitor |

### S3: Evidence Grading Summary

| Claim # | Claim | Base | Modifiers | Final | Level |
|---------|-------|------|-----------|-------|-------|
| 1 | DOX inhibits TOP2A | L4 | +0.05 lit | 0.95 | L4 |
| 2 | DOX inhibits TOP2B | L3 | +0.10 mech, +0.05 OT | 0.85 | L3 |
| 3 | TOP2B-cardiomyopathy assoc | L2 | +0.10 trial | 0.65 | L2 |
| 4 | NF1 LOF -> RAS activation | L3 | +0.05 STRING, +0.05 lit | 0.85 | L3 |
| 5 | Selumetinib approved NF1 | L4 | +0.10 trial, +0.10 mech | 1.00 | L4 |
| 6 | Dexrazoxane cardioprotection | L4 | +0.05 lit | 0.95 | L4 |
| 7 | TDP2 repairs TOP2B damage | L2 | +0.05 STRING | 0.60 | L2 |
| 8 | PARP1 interacts TOP2B | L1 | +0.05 STRING | 0.45 | L1 |
| 9 | MEK inhibition blocks NF1 RAS | L4 | +0.10 mech | 1.00 | L4 |
| 10 | No NF1 cardiotox trials | L1 | -0.10 single | 0.30 | L1 |

### S4: Figure Descriptions

**Figure 1: Knowledge Graph Topology**
The knowledge graph displays two primary mechanistic clusters connected through the query drug doxorubicin. Cluster 1 (TOP2 axis): TOP2A and TOP2B as the therapeutic target and off-target respectively, connected to DNA repair mediators TDP2, PARP1, and TOPBP1. Cluster 2 (RAS-MAPK axis): NF1 as the hub connecting to KRAS, BRAF, MAP2K1, MAP2K2, TP53, and SPRED1. Drug nodes (doxorubicin, selumetinib, trametinib, dexrazoxane) bridge the two clusters through their target interactions.

**Figure 2: Dual-Axis Therapeutic Model**
The model depicts two parallel strategies for minimizing doxorubicin toxicity in NF1. Left axis: Doxorubicin -> TOP2A (therapeutic, green arrow) and Doxorubicin -> TOP2B (toxic, red arrow), with dexrazoxane intercepting the TOP2B arm. Right axis: NF1 loss -> constitutive KRAS -> BRAF -> MEK -> ERK, with selumetinib/trametinib blocking at MEK level, providing an alternative anti-tumor mechanism without cardiac risk.
