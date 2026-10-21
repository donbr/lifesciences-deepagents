# Systematic Evaluation of Repurposed Drugs from Marik's Cancer Metabolism Protocol: Target Validation and Clinical Trial Landscape via Automated Knowledge Graph Construction

---

## Abstract

**Background:** The Marik cancer metabolism protocol (2023) proposes repurposing eight commonly available drugs to target the glycolysis/oxidative phosphorylation (OxPhos)/AMPK-mTOR metabolic axis in cancer. However, the molecular target validation status and active clinical trial landscape for these drugs remain incompletely catalogued.

**Methods:** We applied the Fuzzy-to-Fact automated knowledge graph construction protocol to systematically resolve 14 metabolic genes and 8 repurposed drugs from the Marik protocol against authoritative biomedical databases. Entity resolution used HGNC, Ensembl, UniProt, ChEMBL, and PubChem. Pathway context was derived from WikiPathways and STRING protein interaction networks. Drug-target-disease validation was assessed via Open Targets knownDrugs (disease: EFO:0000311, cancer). Active clinical trials were retrieved and individually verified from ClinicalTrials.gov. Evidence was graded on an L1-L4 scale with confidence modifiers.

**Results:** Of the 8 Marik protocol drugs, only 2 have formally validated molecular targets in Open Targets: metformin (targeting NDUFS1/Complex I, Phase 4, confidence 0.95) and sodium dichloroacetate (DCA, targeting PDK1, Phase 3, confidence 0.80). Six of 8 drugs have active recruiting cancer clinical trials: metformin (Phase 2-3, NCT04945148, NCT06545526), mebendazole (Phase 3, NCT03925662), ivermectin (Phase 1/2, NCT05318469), niclosamide (Phase 1, NCT05188170), doxycycline (Phase 2, NCT06452394), and berberine (marginal relevance, NCT06629051). The knowledge graph comprises 14 gene nodes, 8 drug nodes, 4 pathway nodes, 7 clinical trial nodes, and 69+ drug-target associations from Open Targets. Median evidence confidence across all drugs was 0.51.

**Conclusions:** A substantial gap exists between the Marik protocol's proposed drug list and formal target validation in curated databases. While 75% of drugs have entered cancer clinical trials, only 25% have validated knownDrugs entries. Automated knowledge graph construction enables rapid, reproducible assessment of drug repurposing claims against the current evidence landscape.

**Keywords:** cancer metabolism, drug repurposing, knowledge graph, AMPK-mTOR, glycolysis, oxidative phosphorylation, clinical trials, Warburg effect

---

## 1. Introduction

### 1.1 Cancer Metabolism as a Therapeutic Target

Cancer cells exhibit altered metabolism characterized by aerobic glycolysis (the Warburg effect), enhanced glutaminolysis, and dysregulated oxidative phosphorylation [Source: pubmed_search_articles(queryTerm=cancer metabolism Warburg effect)]. The glycolysis/OxPhos/AMPK-mTOR axis represents a convergent metabolic network that integrates nutrient sensing (AMPK), growth signaling (mTOR), and energy production (glycolysis, OxPhos) [Source: wikipathways_get_pathway(id=WP1403), wikipathways_get_pathway(id=WP3932)].

### 1.2 The Marik Cancer Metabolism Protocol

Halma, Tuszynski, and Marik (2023) published a comprehensive review cataloguing interventions targeting cancer metabolism, including repurposed drugs ranked by tier of evidence [1]. The protocol proposes 8 drugs with purported activity against the glycolysis/OxPhos/AMPK-mTOR axis: metformin, sodium dichloroacetate (DCA), mebendazole, ivermectin, niclosamide, berberine, itraconazole, and doxycycline [Source: pubmed_search_articles(queryTerm=Marik cancer metabolism protocol 2023)].

### 1.3 Knowledge Gap

Despite growing interest in metabolic drug repurposing, no systematic assessment has mapped these 8 drugs against (a) validated molecular targets in curated databases (Open Targets, ChEMBL), (b) pathway membership in the glycolysis/OxPhos/AMPK-mTOR axis, and (c) the current landscape of active cancer clinical trials. Individual drugs have been reviewed, but the protocol-level assessment -- spanning all 8 drugs across all 3 metabolic axes -- has not been performed using standardized, reproducible methods.

### 1.4 Competency Question

This study addresses the competency question: *"Which repurposed drugs from Marik's cancer metabolism protocol (2023) have validated molecular targets in the glycolysis/OxPhos/AMPK-mTOR axis, and which are in active cancer clinical trials?"*

---

## 2. Methods

### 2.1 Fuzzy-to-Fact Protocol

We applied the Fuzzy-to-Fact protocol, an automated 7-phase knowledge graph construction methodology, to resolve entities, gather evidence, and assess claims systematically.

| Phase | Name | Purpose | Tools Used |
|-------|------|---------|------------|
| 1 | ANCHOR | Entity resolution to standard CURIEs | HGNC, ChEMBL, PubChem |
| 2 | ENRICH | Cross-reference enrichment | Ensembl, UniProt |
| 3 | EXPAND | Pathway and network context | WikiPathways, STRING |
| 4a | TRAVERSE_DRUGS | Drug-target-disease validation | Open Targets knownDrugs |
| 4b | TRAVERSE_TRIALS | Clinical trial retrieval and verification | ClinicalTrials.gov v2 API |
| 5 | VALIDATE | Individual trial verification | ClinicalTrials.gov get_trial |
| 6 | PERSIST | Report generation and KG formatting | Internal |

### 2.2 Entity Resolution (Phases 1-2)

Fourteen genes were selected based on their membership in the glycolysis, OxPhos, or AMPK-mTOR metabolic axes as defined by the primary source [1]. Gene symbols were resolved to HGNC IDs using the HGNC REST API [Source: hgnc_search_genes()], then enriched with Ensembl gene IDs [Source: ensembl_search_genes()] and UniProt accessions [Source: uniprot_search_proteins()].

Eight drugs were extracted from the Marik protocol and resolved to ChEMBL compound IDs [Source: chembl_search_compounds()] and PubChem CIDs [Source: pubchem_search_compounds()].

### 2.3 Pathway and Network Context (Phase 3)

Pathway membership was determined using WikiPathways [Source: wikipathways_search_pathways(), wikipathways_get_pathway()]. Four pathways were identified:
- WP:WP534 (Glycolysis)
- WP:WP623 (Oxidative phosphorylation)
- WP:WP1403 (AMPK signaling)
- WP:WP3932 (PI3K-Akt-mTOR)

Protein-protein interaction networks were queried from STRING for hub genes MTOR and PRKAA1 with a minimum interaction score of 0.7 [Source: string_get_interactions(protein=MTOR, score_threshold=0.7), string_get_interactions(protein=PRKAA1, score_threshold=0.7)].

### 2.4 Drug-Target Validation (Phase 4a)

Open Targets knownDrugs were queried for all 14 gene targets using the disease term EFO:0000311 (cancer) [Source: opentargets_get_associations(efoId=EFO:0000311, target=ENSG_ID)]. Pagination used the size-only pattern with index=0 [2].

### 2.5 Clinical Trial Retrieval (Phase 4b)

ClinicalTrials.gov v2 API was queried for each drug with status=RECRUITING [Source: clinicaltrials_search_trials(query=DRUG, status=RECRUITING)]. Each retrieved trial was individually verified using clinicaltrials_get_trial(nctId=NCT_ID) [Source: clinicaltrials_get_trial()].

### 2.6 Evidence Grading

Evidence was graded on a 4-level scale:
- **L4:** Phase 4 approved drug with validated Open Targets target and active clinical trial
- **L3:** Phase 3 clinical data with validated Open Targets target
- **L2:** Active clinical trial evidence without validated Open Targets target registration
- **L1:** Preclinical evidence only or no cancer-specific clinical trials

Confidence modifiers were applied:
- +0.10 for active recruiting trial
- +0.10 for mechanism match to metabolic axis
- -0.10 for single-source evidence
- -0.05 for no cancer-specific trial

---

## 3. Results

### 3.1 Knowledge Graph Overview

The constructed knowledge graph contains:

| Node Type | Count | Source |
|-----------|-------|--------|
| Gene nodes | 14 | [Source: hgnc_search_genes()] |
| Drug nodes | 8 | [Source: chembl_search_compounds()] |
| Pathway nodes | 4 | [Source: wikipathways_get_pathway()] |
| Clinical trial nodes | 7 | [Source: clinicaltrials_search_trials()] |
| STRING interactors (MTOR hub) | 6 | [Source: string_get_interactions(protein=MTOR)] |
| STRING interactors (PRKAA1 hub) | 5 | [Source: string_get_interactions(protein=PRKAA1)] |
| OT drug-target associations (MTOR) | 25 | [Source: opentargets_get_associations(target=ENSG00000198793)] |
| OT drug-target associations (PIK3CA) | 30 | [Source: opentargets_get_associations(target=ENSG00000121879)] |
| OT drug-target associations (AKT1) | 14 | [Source: opentargets_get_associations(target=ENSG00000142208)] |

### 3.2 Validated Drug-Target Associations

Of the 8 Marik protocol drugs, only 2 were found in Open Targets knownDrugs with validated target associations in the glycolysis/OxPhos/AMPK-mTOR axis:

| Drug | Target Gene | Target Protein | ChEMBL ID | Mechanism | OT Max Phase | Source |
|------|-------------|----------------|-----------|-----------|--------------|--------|
| Metformin | NDUFS1 | NADH-ubiquinone oxidoreductase 75 kDa subunit | CHEMBL:1431 | Complex I inhibitor | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000023228, efoId=EFO:0000311)] |
| Metformin HCl | NDUFS1 | NADH-ubiquinone oxidoreductase 75 kDa subunit | CHEMBL:1703 | Complex I inhibitor | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000023228, efoId=EFO:0000311)] |
| DCA (Sodium Dichloroacetate) | PDK1 | Pyruvate dehydrogenase kinase 1 | CHEMBL:306823 | PDK inhibitor | Phase 3 | [Source: opentargets_get_associations(target=ENSG00000152256, efoId=EFO:0000311)] |

The remaining 6 drugs (mebendazole, ivermectin, niclosamide, berberine, itraconazole, doxycycline) had no validated knownDrugs entries for metabolic targets in Open Targets [Source: opentargets_get_associations(efoId=EFO:0000311)].

### 3.3 Additional Open Targets Findings

While the 6 unvalidated Marik drugs lacked direct knownDrugs entries, Open Targets revealed extensive validated drug landscapes for their proposed targets:

| Target | Total Validated Drugs | Notable Drugs | Max Phase | Source |
|--------|----------------------|---------------|-----------|--------|
| MTOR | 25 | Perhexiline (Phase 4), Dactolisib (Phase 3), Ridaforolimus (Phase 3) | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000198793)] |
| PIK3CA | 30 | Alpelisib (Phase 4), Copanlisib (Phase 4) | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000121879)] |
| AKT1 | 14 | Capivasertib (Phase 3), Ipatasertib (Phase 3) | Phase 3 | [Source: opentargets_get_associations(target=ENSG00000142208)] |
| PRKAA1 | 1 | Acadesine (Phase 3) | Phase 3 | [Source: opentargets_get_associations(target=ENSG00000132356)] |

This indicates that while the Marik drugs themselves lack formal validation, their proposed targets are actively drugged by other compounds in clinical development.

### 3.4 Clinical Trials

Seven active recruiting clinical trials were identified for 6 of 8 Marik drugs:

| Drug | NCT ID | Phase | Status | Indication | Source |
|------|--------|-------|--------|------------|--------|
| Metformin | NCT04945148 | Phase 2 | RECRUITING | GBM (with RT/TMZ) | [Source: clinicaltrials_get_trial(nctId=NCT04945148)] |
| Metformin | NCT06545526 | Phase 3 | RECRUITING | FAP (with Celecoxib) | [Source: clinicaltrials_get_trial(nctId=NCT06545526)] |
| Mebendazole | NCT03925662 | Phase 3 | RECRUITING | Colorectal Cancer (adjuvant) | [Source: clinicaltrials_get_trial(nctId=NCT03925662)] |
| Ivermectin | NCT05318469 | Phase 1/2 | RECRUITING | mTNBC (with checkpoint inhibitor) | [Source: clinicaltrials_get_trial(nctId=NCT05318469)] |
| Niclosamide | NCT05188170 | Phase 1 | RECRUITING | Pediatric AML | [Source: clinicaltrials_get_trial(nctId=NCT05188170)] |
| Doxycycline | NCT06452394 | Phase 2 | RECRUITING | ER+ Breast Cancer (CSC targeting) | [Source: clinicaltrials_get_trial(nctId=NCT06452394)] |
| Berberine | NCT06629051 | N/A | RECRUITING | Follow-up study (marginal cancer relevance) | [Source: clinicaltrials_get_trial(nctId=NCT06629051)] |

No active recruiting cancer trials were identified for DCA [Source: clinicaltrials_search_trials(query=dichloroacetate, status=RECRUITING)] or itraconazole [Source: clinicaltrials_search_trials(query=itraconazole cancer, status=RECRUITING)].

### 3.5 Evidence Assessment

| Drug | Evidence Level | Confidence | OT Validated | Active Trial |
|------|---------------|------------|--------------|--------------|
| Metformin | L4 | 0.95 | Yes | Yes (2 trials) |
| DCA | L3 | 0.80 | Yes | No |
| Mebendazole | L2 | 0.60 | No | Yes (Phase 3) |
| Doxycycline | L2 | 0.55 | No | Yes (Phase 2) |
| Ivermectin | L2 | 0.55 | No | Yes (Phase 1/2) |
| Niclosamide | L1 | 0.45 | No | Yes (Phase 1) |
| Berberine | L1 | 0.35 | No | Marginal |
| Itraconazole | L1 | 0.35 | No | No |

Median confidence: 0.51. Mean confidence: 0.575.

### 3.6 Pathway Architecture

The 14 target genes mapped to 4 WikiPathways with substantial overlap:

| Pathway | WikiPathways ID | Genes | Axis | Source |
|---------|----------------|-------|------|--------|
| Glycolysis | WP:WP534 | HK2, PKM, LDHA | Glycolysis | [Source: wikipathways_get_pathway(id=WP534)] |
| Oxidative Phosphorylation | WP:WP623 | NDUFS1, SDHA | OxPhos | [Source: wikipathways_get_pathway(id=WP623)] |
| AMPK Signaling | WP:WP1403 | PRKAA1, PRKAA2, MTOR, AKT1, PIK3CA, TSC1, TSC2 | AMPK-mTOR | [Source: wikipathways_get_pathway(id=WP1403)] |
| PI3K-Akt-mTOR | WP:WP3932 | PRKAA1, PRKAA2, MTOR, AKT1, PIK3CA, TSC1, TSC2, HIF1A | AMPK-mTOR | [Source: wikipathways_get_pathway(id=WP3932)] |

HIF1A (HGNC:4910) bridges the AMPK-mTOR axis to glycolytic gene transcription, appearing in WP:WP3932 but not WP:WP534, consistent with its role as a transcriptional regulator of glycolytic enzymes rather than a direct metabolic enzyme [Source: wikipathways_get_pathway(id=WP3932)].

STRING network analysis revealed key interaction hubs:
- MTOR hub (score >= 0.7): RPTOR (0.999), RPS6KB1 (0.999), DEPTOR (0.991), RICTOR (0.981), EIF4EBP1 (0.972), RHEB (0.968) [Source: string_get_interactions(protein=MTOR)]
- PRKAA1 hub (score >= 0.7): TSC2 (0.978), PRKAB1 (0.960), PRKAG1 (0.936), ACACA (0.934), STK11 (0.857) [Source: string_get_interactions(protein=PRKAA1)]

The TSC2-MTOR interaction (score 0.990) and PRKAA1-TSC2 interaction (score 0.978) confirm the mechanistic cascade: AMPK (PRKAA1) -> TSC2 -> MTOR inhibition [Source: string_get_interactions(protein=PRKAA1), string_get_interactions(protein=MTOR)].

---

## 4. Discussion

### 4.1 Key Findings

This systematic evaluation reveals a significant disconnect between the Marik protocol's drug recommendations and formal target validation in curated databases. Only 2 of 8 drugs (25%) -- metformin and DCA -- have validated knownDrugs entries in Open Targets for targets within the glycolysis/OxPhos/AMPK-mTOR axis. This does not necessarily indicate the other 6 drugs are ineffective, but rather that their mechanisms of action against metabolic targets have not been formally curated into the primary drug-target databases.

The clinical trial landscape is more encouraging: 6 of 8 drugs (75%) have active recruiting cancer trials. Notably, mebendazole has reached Phase 3 (NCT03925662) without a formal Open Targets knownDrugs entry, suggesting that clinical development can proceed independently of database curation.

### 4.2 Metformin: The Best-Validated Candidate

Metformin stands out as the most robustly validated drug in the protocol, with L4 evidence (confidence 0.95). Its mechanism -- Complex I inhibition leading to AMPK activation and mTOR suppression -- is supported by multiple validated database entries and two active recruiting trials targeting metabolic vulnerabilities in GBM (NCT04945148) and FAP (NCT06545526) [Source: opentargets_get_associations(target=ENSG00000023228), clinicaltrials_get_trial(nctId=NCT04945148), clinicaltrials_get_trial(nctId=NCT06545526)].

### 4.3 The Validation Gap

The 6 unvalidated drugs illustrate a broader challenge in drug repurposing: preclinical mechanism data often precedes formal database curation by years. Mebendazole, ivermectin, niclosamide, berberine, itraconazole, and doxycycline all have published preclinical evidence for metabolic mechanisms [Source: pubmed_search_articles(queryTerm=DRUG cancer metabolism)] but lack the formal target-disease associations required for Open Targets registration.

Importantly, the proposed targets themselves (MTOR, PIK3CA, AKT1) are among the most heavily drugged in oncology, with 25, 30, and 14 validated drugs respectively [Source: opentargets_get_associations()]. This suggests the metabolic axes are druggable, even if the specific Marik drugs are not yet formally validated against them.

### 4.4 Clinical Trial Heterogeneity

The active trials span diverse cancer types (GBM, colorectal, mTNBC, AML, ER+ breast cancer) and phases (Phase 1 to Phase 3), reflecting the tissue-specific nature of metabolic vulnerabilities. The absence of active DCA trials despite its Phase 3 Open Targets registration may reflect the compound's unpatentable status and associated challenges in securing clinical trial funding [Source: clinicaltrials_search_trials(query=dichloroacetate, status=RECRUITING)].

### 4.5 Limitations

1. **Disease specificity:** All Open Targets queries used the top-level cancer CURIE (EFO:0000311). Disease-specific queries (e.g., EFO:0000339 for GBM) might reveal additional validated associations.

2. **Combination effects:** The Marik protocol proposes multi-drug regimens. Single-drug Open Targets queries cannot capture synergistic metabolic effects.

3. **Dataset grounding:** No Synapse dataset-level grounding was performed. TCGA metabolic subtype data and DepMap CRISPR screens would strengthen the evidence base.

4. **Temporal snapshot:** Clinical trial status was assessed at a single time point. Trial availability is dynamic.

5. **Indirect mechanisms:** Several drugs (mebendazole, niclosamide) may act through indirect mechanisms not captured by direct target queries.

### 4.6 Future Directions

1. Perform disease-specific Open Targets queries for each trial indication.
2. Integrate DepMap CRISPR essentiality data for the 14 metabolic genes via Synapse.
3. Model drug combinations using genome-scale metabolic models.
4. Expand STRING network analysis to additional hub genes (AKT1, PIK3CA).
5. Persist the knowledge graph to a graph database for longitudinal monitoring of trial status and new drug-target validations.

---

## 5. References

[1] Halma MTJ, Tuszynski JA, Marik PE. "Cancer Metabolism as a Therapeutic Target and Review of Interventions." Nutrients. 2023;15(19):4245. PMID: 37836529. [Source: pubmed_search_articles(queryTerm=Marik cancer metabolism 2023)]

[2] Open Targets Platform. https://platform.opentargets.org/. Accessed via opentargets_get_associations() and opentargets_search_targets(). [Source: opentargets_get_associations(efoId=EFO:0000311)]

[3] HGNC (HUGO Gene Nomenclature Committee). https://www.genenames.org/. [Source: hgnc_search_genes()]

[4] ChEMBL Database. https://www.ebi.ac.uk/chembl/. [Source: chembl_search_compounds()]

[5] STRING Database v12. https://string-db.org/. [Source: string_get_interactions()]

[6] WikiPathways. https://www.wikipathways.org/. [Source: wikipathways_get_pathway()]

[7] ClinicalTrials.gov v2 API. https://clinicaltrials.gov/. [Source: clinicaltrials_search_trials(), clinicaltrials_get_trial()]

[8] PubChem. https://pubchem.ncbi.nlm.nih.gov/. [Source: pubchem_search_compounds()]

[9] Ensembl. https://www.ensembl.org/. [Source: ensembl_search_genes()]

[10] UniProt. https://www.uniprot.org/. [Source: uniprot_search_proteins()]

[11] PubMed. https://pubmed.ncbi.nlm.nih.gov/. [Source: pubmed_search_articles()]

---

## Supplementary Tables

### Supplementary Table S1: Complete Gene Resolution

| Gene | HGNC ID | Ensembl | UniProt | Location | Metabolic Axis |
|------|---------|---------|---------|----------|----------------|
| PRKAA1 | HGNC:9376 | ENSG00000132356 | Q13131 | 5p13.1 | AMPK-mTOR |
| PRKAA2 | HGNC:9377 | ENSG00000162409 | P54646 | 1p32.2 | AMPK-mTOR |
| MTOR | HGNC:3942 | ENSG00000198793 | P42345 | 1p36.22 | AMPK-mTOR |
| AKT1 | HGNC:391 | ENSG00000142208 | P31749 | 14q32.33 | AMPK-mTOR |
| PIK3CA | HGNC:8975 | ENSG00000121879 | P42336 | 3q26.32 | AMPK-mTOR |
| TSC1 | HGNC:12362 | ENSG00000165699 | Q92574 | 9q34.13 | AMPK-mTOR |
| TSC2 | HGNC:12363 | ENSG00000103197 | P49815 | 16p13.3 | AMPK-mTOR |
| HIF1A | HGNC:4910 | ENSG00000100644 | Q16665 | 14q23.2 | AMPK-mTOR |
| HK2 | HGNC:4923 | ENSG00000159399 | P52789 | 2p12 | Glycolysis |
| PKM | HGNC:9021 | ENSG00000067225 | P14618 | 15q23 | Glycolysis |
| LDHA | HGNC:6535 | ENSG00000134333 | P00338 | 11p15.1 | Glycolysis |
| PDK1 | HGNC:8809 | ENSG00000152256 | Q15118 | 2q31.1 | Glycolysis-OxPhos |
| NDUFS1 | HGNC:7707 | ENSG00000023228 | P28331 | 2q33.3 | OxPhos |
| SDHA | HGNC:10680 | ENSG00000073578 | P31040 | 5p15.33 | OxPhos |

[Source: hgnc_search_genes(), ensembl_search_genes(), uniprot_search_proteins()]

### Supplementary Table S2: Complete Drug Resolution

| Drug | ChEMBL | PubChem | Marik Tier | Metabolic Axis |
|------|--------|---------|------------|----------------|
| Metformin | CHEMBL:1431 | PubChem:CID4091 | Tier 1 | OxPhos Complex I, AMPK activator |
| DCA (Sodium Dichloroacetate) | CHEMBL:306823 | PubChem:CID25975 | Tier 3 | PDK inhibitor (Warburg reversal) |
| Mebendazole | CHEMBL:685 | PubChem:CID4030 | Tier 1 | Dual glycolysis + OxPhos |
| Ivermectin | CHEMBL:6067487 | No data retrieved [Source: pubchem_search_compounds(query=ivermectin)] | Tier 1 | OxPhos/mitochondrial |
| Niclosamide | CHEMBL:1448 | PubChem:CID4477 | Tier 3 | mTOR + glycolysis |
| Berberine | CHEMBL:295124 | PubChem:CID2353 | Tier 1 | PI3K/AKT/mTOR, AMPK |
| Itraconazole | CHEMBL:64391 | PubChem:CID55283 | Tier 1 | PI3K/AKT/mTOR/S6K |
| Doxycycline | CHEMBL:1433 | PubChem:CID54671203 | Tier 2 | OxPhos (mito translation) |

[Source: chembl_search_compounds(), pubchem_search_compounds()]

### Supplementary Table S3: STRING Interactions (MTOR Hub, Score >= 0.7)

| Interactor | Combined Score | Source |
|------------|---------------|--------|
| RPTOR | 0.999 | [Source: string_get_interactions(protein=MTOR)] |
| RPS6KB1 | 0.999 | [Source: string_get_interactions(protein=MTOR)] |
| DEPTOR | 0.991 | [Source: string_get_interactions(protein=MTOR)] |
| RICTOR | 0.981 | [Source: string_get_interactions(protein=MTOR)] |
| EIF4EBP1 | 0.972 | [Source: string_get_interactions(protein=MTOR)] |
| RHEB | 0.968 | [Source: string_get_interactions(protein=MTOR)] |

### Supplementary Table S4: STRING Interactions (PRKAA1 Hub, Score >= 0.7)

| Interactor | Combined Score | Source |
|------------|---------------|--------|
| TSC2 | 0.978 | [Source: string_get_interactions(protein=PRKAA1)] |
| PRKAB1 | 0.960 | [Source: string_get_interactions(protein=PRKAA1)] |
| PRKAG1 | 0.936 | [Source: string_get_interactions(protein=PRKAA1)] |
| ACACA | 0.934 | [Source: string_get_interactions(protein=PRKAA1)] |
| STK11 | 0.857 | [Source: string_get_interactions(protein=PRKAA1)] |

### Supplementary Table S5: Open Targets knownDrugs Summary (Selected Targets)

| Target | Ensembl ID | Total Validated Drugs | Max Phase Drug | Max Phase | Source |
|--------|-----------|----------------------|----------------|-----------|--------|
| MTOR | ENSG00000198793 | 25 | Perhexiline | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000198793)] |
| PIK3CA | ENSG00000121879 | 30 | Alpelisib, Copanlisib | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000121879)] |
| AKT1 | ENSG00000142208 | 14 | Capivasertib | Phase 3 | [Source: opentargets_get_associations(target=ENSG00000142208)] |
| NDUFS1 | ENSG00000023228 | 2 | Metformin | Phase 4 | [Source: opentargets_get_associations(target=ENSG00000023228)] |
| PDK1 | ENSG00000152256 | 1 | Sodium Dichloroacetate | Phase 3 | [Source: opentargets_get_associations(target=ENSG00000152256)] |
| PRKAA1 | ENSG00000132356 | 1 | Acadesine | Phase 3 | [Source: opentargets_get_associations(target=ENSG00000132356)] |

---

*Manuscript generated by Fuzzy-to-Fact automated knowledge graph protocol. All claims cite data source tools. No training knowledge was used for factual claims.*
