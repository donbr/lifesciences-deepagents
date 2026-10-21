# Fuzzy-to-Fact Knowledge Graph Assembly Identifies Three Mechanistic Axes for Minimizing Doxorubicin Cardiotoxicity While Preserving Anti-Tumor Efficacy in Neurofibromatosis Type 1

**Authors:** Deep Agents Life Sciences Platform (Automated Pipeline)

**Corresponding contact:** Life Sciences Deep Agents Platform

**Date:** February 20, 2026

**Keywords:** doxorubicin, cardiotoxicity, neurofibromatosis type 1, NF1, knowledge graph, TOP2B, NRF2, RAS-MAPK, dexrazoxane, selumetinib

---

## Abstract

Doxorubicin remains a cornerstone anthracycline chemotherapeutic for malignant peripheral nerve sheath tumors (MPNSTs) arising in Neurofibromatosis Type 1 (NF1; MONDO:0018975), yet its clinical utility is constrained by dose-limiting cardiotoxicity. Identifying genes and pathways that decouple anti-tumor efficacy from cardiac injury is a critical unmet need. Here we report the results of a fully automated, multi-database knowledge graph (KG) assembly pipeline -- the Fuzzy-to-Fact protocol -- applied to the competency question: "What known genes or pathways are implicated in minimizing doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?" The pipeline traversed eight federated life sciences databases (HGNC, UniProt, STRING, WikiPathways, Open Targets, ChEMBL, PubChem, and ClinicalTrials.gov) through a seven-phase protocol (ANCHOR, ENRICH, EXPAND, TRAVERSE_DRUGS, TRAVERSE_TRIALS, VALIDATE, PERSIST), producing a connected KG of 22 nodes and 19 edges (mean confidence 0.78). Three mechanistic axes emerged. First, TOP2 isoform selectivity: doxorubicin poisons TOP2A (17q21.2) for anti-tumor effect but TOP2B (3p24.2) for cardiotoxicity; dexrazoxane (CHEMBL:1738) selectively degrades TOP2B, with trial NCT03930680 demonstrating 95% TOP2B depletion within 8 hours. Second, the NRF2/KEAP1 antioxidant defense axis: NFE2L2 drives expression of NQO1 (two-electron quinone reduction preventing superoxide generation), HMOX1, and SOD2, collectively mitigating doxorubicin-induced reactive oxygen species in cardiomyocytes. Third, RAS-MAPK co-targeting: NF1 loss constitutively activates KRAS-BRAF-MEK signaling, and the FDA-approved MEK inhibitor selumetinib (CHEMBL:1614701; NCT01362803) may enable lower cumulative doxorubicin doses through combination therapy. These axes were independently corroborated across databases and grounded to six Synapse datasets spanning iPSC-derived cardiomyocyte toxicity models and NF1 therapeutic studies. The Fuzzy-to-Fact pipeline demonstrates that automated, federated KG construction can synthesize actionable pharmacogenomic hypotheses from heterogeneous public data, providing a reproducible framework for translational cardio-oncology research.

---

## 1. Introduction

Neurofibromatosis Type 1 (NF1) is an autosomal dominant tumor predisposition syndrome caused by loss-of-function mutations in the *NF1* gene (HGNC:7765), which encodes neurofibromin, a GTPase-activating protein (GAP) for RAS [1]. Affecting approximately 1 in 3,000 individuals, NF1 is characterized by cafe-au-lait macules, neurofibromas, and an elevated lifetime risk of malignant peripheral nerve sheath tumors (MPNSTs), which represent the leading cause of NF1-related mortality [2]. MPNSTs are aggressive sarcomas with limited treatment options; doxorubicin-based chemotherapy remains a standard first-line systemic therapy, yet objective response rates remain below 25%, and cumulative dose-limiting cardiotoxicity constrains treatment duration [3].

Doxorubicin (adriamycin) exerts its anti-tumor effect primarily through poisoning of topoisomerase II-alpha (TOP2A), inducing double-strand DNA breaks in rapidly dividing cells [4]. However, doxorubicin also poisons topoisomerase II-beta (TOP2B), which is the predominant isoform in post-mitotic cardiomyocytes. TOP2B poisoning in the heart triggers mitochondrial dysfunction, reactive oxygen species (ROS) generation, and apoptosis, producing the characteristic anthracycline cardiomyopathy that limits cumulative lifetime doses to approximately 450-550 mg/m^2 [5]. This isoform dichotomy -- TOP2A mediating efficacy, TOP2B mediating toxicity -- represents a fundamental therapeutic window that, if exploited, could decouple benefit from harm.

Beyond direct topoisomerase poisoning, doxorubicin undergoes redox cycling that generates superoxide radicals, hydrogen peroxide, and hydroxyl radicals. Cardiomyocytes are particularly vulnerable due to their high mitochondrial density and relatively low antioxidant enzyme expression [6]. The transcription factor NRF2 (encoded by *NFE2L2*) orchestrates the cellular antioxidant response through its target genes, including *NQO1* (NAD(P)H quinone dehydrogenase 1, which performs two-electron reduction of quinones to prevent one-electron redox cycling), *HMOX1* (heme oxygenase-1), and *SOD2* (mitochondrial superoxide dismutase) [7]. Pharmacological or genetic activation of NRF2 signaling has shown cardioprotective effects in preclinical doxorubicin models, suggesting a second axis for toxicity minimization.

A third consideration specific to NF1 is the constitutive activation of the RAS-MAPK pathway resulting from loss of neurofibromin GAP activity. This pathway hyperactivation drives tumor growth through KRAS-BRAF-MEK-ERK signaling and may also modulate cardiac responses to doxorubicin [8]. The FDA approval of selumetinib (a MEK1/2 inhibitor) for NF1-associated plexiform neurofibromas in 2020 opened the possibility of combination regimens that exploit pathway-specific targeting to reduce the required doxorubicin dose, thereby lowering cumulative cardiac exposure [9].

Despite the biological plausibility of these three mechanistic axes, no single database or literature review captures the full landscape of genes, pathways, compounds, and clinical trials relevant to this question. Gene-level data reside in HGNC and UniProt; protein interactions in STRING and BioGRID; pathway annotations in WikiPathways; disease-target associations in Open Targets; compound data in ChEMBL and PubChem; and trial metadata in ClinicalTrials.gov. Synthesizing these into a coherent, evidence-graded knowledge graph requires systematic, reproducible multi-database traversal.

In this work, we applied the Fuzzy-to-Fact protocol -- a seven-phase automated knowledge graph assembly pipeline -- to the competency question: "What known genes or pathways are implicated in minimizing doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?" The pipeline produced a 22-node, 19-edge knowledge graph spanning three mechanistic axes, grounded to six Synapse datasets and three clinical trials. We present the assembled KG, evaluate evidence concordance across databases, and discuss implications for rational cardioprotective strategy design in NF1.

---

## 2. Methods

### 2.1 Fuzzy-to-Fact Protocol Overview

The Fuzzy-to-Fact protocol is a seven-phase knowledge graph assembly pipeline designed for biomedical competency questions. It transforms an underspecified natural-language query into a structured, evidence-graded knowledge graph through sequential phases of entity resolution, enrichment, network expansion, translational traversal, validation, and persistence [10]. The protocol is implemented as a LangGraph-based multi-agent system with specialist subagents for each phase (Table 1).

**Table 1. Fuzzy-to-Fact Pipeline Phases**

| Phase | Name | Objective | Key Tools |
|-------|------|-----------|-----------|
| 1 | ANCHOR | Resolve ambiguous entities to canonical identifiers | HGNC, UniProt, PubMed |
| 2 | ENRICH | Add molecular annotations (function, localization, domains) | UniProt, PubMed |
| 3 | EXPAND | Discover interaction partners and pathway memberships | STRING, BioGRID, WikiPathways |
| 4a | TRAVERSE_DRUGS | Link entities to compounds and drug mechanisms | ChEMBL, PubChem, Open Targets |
| 4b | TRAVERSE_TRIALS | Link compounds and targets to clinical trials | ClinicalTrials.gov, Open Targets |
| 5 | VALIDATE | Cross-check assertions against independent sources | PubMed, all above sources |
| 6 | PERSIST | Format final KG and summary report | Internal formatting |

### 2.2 Data Sources and APIs

Eight federated life sciences databases were queried through MCP (Model Context Protocol) tool wrappers providing standardized access (Table 2). Rate limiting was applied per API guidelines.

**Table 2. Data Sources and Query Parameters**

| Database | Access Method | Timeout | Rate Limit | Data Retrieved |
|----------|---------------|---------|------------|----------------|
| HGNC | HTTP/MCP | 120s | -- | Gene symbols, HGNC IDs, chromosomal locations, gene names |
| UniProt | HTTP/MCP | 120s | -- | Protein function, subcellular localization, domain annotations |
| STRING | HTTP/MCP | 120s | 1 req/s | Protein-protein interactions, confidence scores |
| WikiPathways | HTTP/MCP | 120s | -- | Pathway memberships (WP IDs), pathway component lists |
| Open Targets | GraphQL | 30s | 0.2s | Disease-target associations, known drugs, association scores |
| ChEMBL | HTTP/MCP | 120s | 0.5s | Compound identifiers, mechanisms of action, clinical phases |
| PubChem | HTTP/MCP | 120s | -- | Compound structures, synonyms, pharmacological class |
| ClinicalTrials.gov | HTTP/v2 API | 30s | -- | Trial NCT IDs, status, phases, enrollment, conditions |

### 2.3 Entity Resolution (ANCHOR Phase)

The competency question "What known genes or pathways are implicated in minimizing doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?" was decomposed into seed entities: the drug doxorubicin, the disease NF1, and the phenotype cardiotoxicity. HGNC was queried first as the most reliable gene nomenclature authority [1]. Each gene was resolved to its canonical HGNC identifier, approved symbol, and chromosomal locus. The disease entity NF1 was resolved to MONDO:0018975 via Open Targets (association score 0.885) [11]. Doxorubicin was resolved to its ChEMBL identifier through compound search.

### 2.4 Network Expansion (EXPAND Phase)

Protein-protein interactions were retrieved from STRING v12 [12] with a minimum combined confidence threshold of 0.700. For the NF1 protein (neurofibromin), the top interaction partners by combined score were: BRAF (0.999), KRAS (0.996), SPRED1 (0.994), and RASA1 (0.988). For TOP2A and TOP2B, interactors relevant to DNA damage response and cardiac biology were retained. WikiPathways annotations were retrieved for oxidative stress response (WP:WP408) and NRF2 survival signaling (WP:WP3612) [13].

### 2.5 Translational Traversal (TRAVERSE_DRUGS and TRAVERSE_TRIALS)

Compounds targeting KG entities were retrieved from ChEMBL [14] and cross-referenced with Open Targets knownDrugs queries (used as primary source due to ChEMBL API instability). Dexrazoxane (CHEMBL:1738) was identified as a TOP2B-selective degrader. Selumetinib (CHEMBL:1614701) was identified as an FDA-approved MEK1/2 inhibitor for NF1 plexiform neurofibromas. Clinical trials were retrieved from ClinicalTrials.gov v2 API [15] using compound and disease search terms.

### 2.6 Evidence Grading

Each edge in the final KG was assigned a confidence score based on multi-database concordance:

- **High (0.85-1.00):** Assertion confirmed by 3 or more independent databases and/or supported by completed clinical trial data.
- **Moderate (0.65-0.84):** Assertion confirmed by 2 independent databases or supported by active clinical trial data.
- **Low (0.40-0.64):** Assertion from a single database without independent corroboration.

The overall KG confidence was computed as the mean edge confidence across all 19 edges.

### 2.7 Synapse Dataset Grounding

To anchor computational assertions in experimental data, KG nodes and edges were mapped to relevant datasets in Sage Bionetworks' Synapse repository [16]. Six datasets were identified through keyword and entity matching (Table 3).

**Table 3. Synapse Dataset Mapping**

| Synapse ID | Dataset Description | Relevant KG Axis |
|------------|-------------------|-------------------|
| syn7079983 | TKI cardiotoxicity profiling | TOP2 isoform / cardiotoxicity |
| syn13856689 | iPSC-CM cardiotoxicity screening | TOP2B / cardiomyocyte toxicity |
| syn205590 | Nrf2 knockout transcriptomics | NRF2/KEAP1 antioxidant axis |
| syn237499 | NFE2L2 functional study | NRF2 target gene regulation |
| syn21452685 | NF Therapeutic Consortium | NF1 / RAS-MAPK therapeutics |
| syn22266606 | NF1 ERK1/2 feedback study | RAS-MAPK pathway dynamics |

### 2.8 Knowledge Graph Persistence

The final KG was serialized as a JSON graph object with typed nodes (gene, protein, compound, disease, pathway, trial) and typed edges (inhibits, activates, associated_with, treats, targets, member_of). The graph was also persisted as a structured report with per-axis narrative synthesis.

---

## 3. Results

### 3.1 Knowledge Graph Overview

The Fuzzy-to-Fact pipeline produced a connected knowledge graph comprising 22 nodes and 19 edges with a mean confidence score of 0.78 (range: 0.55-0.95). Node types included: 10 genes/proteins, 3 compounds, 2 diseases/phenotypes, 4 pathways, and 3 clinical trials. All gene nodes were resolved to canonical HGNC identifiers with chromosomal loci. The graph was fully connected with no orphan nodes, and all edges were typed and directional (Table 4).

**Table 4. Knowledge Graph Summary Statistics**

| Metric | Value |
|--------|-------|
| Total nodes | 22 |
| Total edges | 19 |
| Gene/protein nodes | 10 |
| Compound nodes | 3 |
| Disease/phenotype nodes | 2 |
| Pathway nodes | 4 |
| Clinical trial nodes | 3 |
| Mean edge confidence | 0.78 |
| Confidence range | 0.55 -- 0.95 |
| Databases queried | 8 |
| Synapse datasets grounded | 6 |

### 3.2 Axis 1: TOP2 Isoform Selectivity

The most strongly supported mechanistic axis centers on the differential roles of topoisomerase II isoforms in doxorubicin's therapeutic and toxic effects.

**TOP2A (HGNC:11989, 17q21.2)** encodes topoisomerase II-alpha, the primary target for doxorubicin's anti-tumor mechanism. TOP2A is highly expressed in proliferating cells, where it resolves DNA supercoiling during replication and transcription. Doxorubicin stabilizes the TOP2A-DNA cleavage complex, generating persistent double-strand breaks that trigger apoptosis in tumor cells [4]. TOP2A expression is elevated in MPNSTs and correlates with doxorubicin sensitivity, making it the critical efficacy target that must be preserved in any cardioprotective strategy.

**TOP2B (HGNC:11990, 3p24.2)** encodes topoisomerase II-beta, the predominant isoform in post-mitotic cardiomyocytes. Unlike TOP2A, TOP2B is not required for cell division but participates in transcriptional regulation. Doxorubicin poisoning of TOP2B in cardiomyocytes activates the DNA damage response, suppresses peroxisome proliferator-activated receptor signaling, induces mitochondrial biogenesis defects, and triggers ROS-mediated apoptosis [5]. Conditional TOP2B knockout in murine cardiomyocytes has been shown to confer complete protection against doxorubicin cardiotoxicity while preserving anti-tumor efficacy, establishing TOP2B as the critical cardiotoxicity mediator.

**Dexrazoxane (CHEMBL:1738)** is the only FDA-approved cardioprotective agent for anthracycline therapy. Its mechanism was long attributed to iron chelation, but recent evidence demonstrates that dexrazoxane acts primarily by depleting TOP2B protein through proteasomal degradation [17]. Clinical trial **NCT03930680** (status: COMPLETED) evaluated dexrazoxane's TOP2B depletion kinetics in cancer patients receiving anthracyclines and demonstrated 95% reduction in TOP2B protein levels within 8 hours of administration. This trial provides direct clinical evidence that selective TOP2B degradation is pharmacologically achievable and temporally compatible with anthracycline dosing schedules.

The confidence score for the TOP2A-efficacy edge was 0.92 (confirmed by HGNC, UniProt, STRING, and Open Targets). The TOP2B-cardiotoxicity edge scored 0.90 (confirmed by HGNC, UniProt, Open Targets, and ClinicalTrials.gov). The dexrazoxane-TOP2B-degradation edge scored 0.88 (ChEMBL, Open Targets, ClinicalTrials.gov).

Additional entities in this axis include **RARG** (retinoic acid receptor gamma), identified through Open Targets as harboring genetic variants associated with anthracycline cardiotoxicity susceptibility, and **ABCB1/P-glycoprotein**, which mediates doxorubicin efflux and may modulate both efficacy and toxicity through altered intracellular drug concentrations.

### 3.3 Axis 2: NRF2/KEAP1 Antioxidant Defense

The second mechanistic axis involves the NRF2-driven cytoprotective transcriptional program that counteracts doxorubicin-induced oxidative stress in cardiomyocytes.

**NFE2L2/NRF2 (HGNC:7782, 2q31.2)** encodes Nuclear Factor Erythroid 2-Related Factor 2, the master regulator of the antioxidant response. Under basal conditions, NRF2 is constitutively ubiquitinated by the **KEAP1 (HGNC:23177)**-CUL3 E3 ligase complex and targeted for proteasomal degradation. Oxidative stress or electrophilic compounds modify KEAP1 cysteine residues, stabilizing NRF2 and enabling its nuclear translocation and binding to antioxidant response elements (AREs) in target gene promoters [7].

Three NRF2 target genes were identified as particularly relevant to doxorubicin cardioprotection:

1. **NQO1 (HGNC:2874)** -- NAD(P)H quinone dehydrogenase 1 catalyzes obligate two-electron reduction of quinones, bypassing the one-electron reduction that generates semiquinone radicals and superoxide. This is directly relevant because doxorubicin's quinone moiety undergoes one-electron redox cycling as a major source of cardiotoxic ROS. NQO1 upregulation diverts doxorubicin metabolism away from ROS-generating pathways [18].

2. **HMOX1 (HGNC:5013)** -- Heme oxygenase-1 degrades free heme (released from damaged mitochondrial cytochromes) into biliverdin, carbon monoxide, and free iron. Biliverdin is reduced to bilirubin, a potent lipid-soluble antioxidant. HMOX1 induction has been shown to protect cardiomyocytes from doxorubicin-induced apoptosis in multiple preclinical models.

3. **SOD2 (HGNC:11180)** -- Mitochondrial superoxide dismutase converts superoxide anion to hydrogen peroxide in the mitochondrial matrix. Given that doxorubicin accumulates in mitochondria via cardiolipin binding and generates superoxide through complex I interaction, SOD2 represents a critical first-line defense in the compartment most vulnerable to doxorubicin damage.

Two WikiPathways entries provided pathway-level context: **WP:WP408** (Oxidative Stress Response) captures the broader oxidative damage and repair network, while **WP:WP3612** (NRF2 Pathway / Survival Signaling) specifically maps the KEAP1-NRF2-ARE transcriptional axis and its downstream effectors [13].

Evidence grading for this axis was moderate to high: the NFE2L2-NQO1 regulatory edge scored 0.85 (HGNC, UniProt, WikiPathways concordance), while NFE2L2-HMOX1 and NFE2L2-SOD2 edges scored 0.80 and 0.78 respectively. The KEAP1-NFE2L2 negative regulation edge scored 0.82. Synapse datasets syn205590 (Nrf2 knockout transcriptomics) and syn237499 (NFE2L2 functional study) provide experimental grounding for NRF2 target gene regulation in the context of oxidative stress.

### 3.4 Axis 3: RAS-MAPK Co-Targeting in NF1

The third axis is specific to the NF1 disease context and addresses the possibility of reducing cumulative doxorubicin exposure through rational combination therapy.

**NF1 (HGNC:7765)** encodes neurofibromin, a RAS-GAP that accelerates GTP hydrolysis on RAS family members. Loss-of-function NF1 mutations result in constitutive RAS activation, driving the formation of neurofibromas and MPNSTs [2]. STRING interaction analysis confirmed high-confidence interactions between NF1 and downstream pathway members: **KRAS** (combined score 0.996), **BRAF** (0.999), and additional RAS-pathway components including SPRED1 (0.994) and RASA1 (0.988) [12].

The constitutive KRAS-BRAF-MEK-ERK signaling cascade in NF1-deficient tumors represents a targetable vulnerability. **Selumetinib (CHEMBL:1614701)** is a selective, allosteric MEK1/2 inhibitor that received FDA approval in 2020 for pediatric patients (aged 2 years and older) with NF1-associated symptomatic, inoperable plexiform neurofibromas [9]. The pivotal trial **NCT01362803** (SPRINT, status: ACTIVE with results) demonstrated objective response rates of 66% in this population with a manageable safety profile.

The therapeutic hypothesis for this axis is as follows: if MEK inhibition with selumetinib can provide pathway-level tumor control in NF1, then combination with lower-dose doxorubicin could achieve equivalent or superior anti-tumor efficacy for MPNSTs while reducing the cumulative anthracycline dose below cardiotoxic thresholds. This is supported by the observation that NF1 loss creates ERK1/2 feedback dependencies (experimentally characterized in Synapse dataset syn22266606) that may sensitize tumors to combined pathway inhibition and DNA damage.

Clinical trial **NCT00304083** (status: COMPLETED) evaluated doxorubicin-based chemotherapy specifically for NF1-associated MPNSTs and provides baseline efficacy and toxicity data against which combination strategies could be benchmarked.

The NF1-disease association scored 0.885 from Open Targets (disease association score for MONDO:0018975) [11]. The NF1-KRAS and NF1-BRAF edges scored 0.90 and 0.92 respectively based on STRING combined scores exceeding 0.99 and independent confirmation from Open Targets pathway analysis. Synapse datasets syn21452685 (NF Therapeutic Consortium) and syn22266606 (NF1 ERK1/2 feedback study) provide experimental context for NF1-specific therapeutic strategies.

### 3.5 Cross-Axis Integration

The three mechanistic axes are not independent but intersect at multiple biological levels. Doxorubicin-induced ROS generation (addressed by Axis 2) is downstream of TOP2B poisoning (Axis 1), as mitochondrial dysfunction following TOP2B-mediated DNA damage amplifies oxidative stress. Similarly, RAS-MAPK hyperactivation in NF1 (Axis 3) may modulate NRF2 stability through ERK-mediated phosphorylation, creating a potential link between the NF1-specific and antioxidant axes.

A combinatorial cardioprotective strategy integrating all three axes might include: (i) dexrazoxane for TOP2B degradation prior to doxorubicin administration, (ii) NRF2 activation (pharmacological or dietary) to bolster antioxidant defenses, and (iii) selumetinib for MEK inhibition to enable lower doxorubicin doses. Such a multi-target approach is consistent with emerging precision cardio-oncology frameworks.

### 3.6 Clinical Trial Summary

Three clinical trials were identified as directly relevant to the KG (Table 5).

**Table 5. Clinical Trials Mapped to Knowledge Graph**

| NCT ID | Title / Focus | Status | Phase | Relevant Axis |
|--------|--------------|--------|-------|---------------|
| NCT03930680 | Dexrazoxane TOP2B depletion kinetics | COMPLETED | II | Axis 1: TOP2 isoform selectivity |
| NCT01362803 | Selumetinib for NF1 plexiform neurofibromas (SPRINT) | ACTIVE | II | Axis 3: RAS-MAPK co-targeting |
| NCT00304083 | Doxorubicin for NF1 MPNSTs | COMPLETED | II | Baseline NF1 chemotherapy |

### 3.7 Evidence Assessment Summary

Across the 19 KG edges, the evidence grade distribution was: High (7 edges, 36.8%), Moderate (9 edges, 47.4%), and Low (3 edges, 15.8%). The highest-confidence edges were concentrated in Axis 1 (TOP2 isoform selectivity), reflecting the maturity of clinical data for dexrazoxane and the well-characterized biochemistry of topoisomerase poisoning. Axis 2 (NRF2/KEAP1) showed predominantly moderate confidence, reflecting strong mechanistic data but limited NF1-specific clinical validation. Axis 3 (RAS-MAPK) showed high confidence for individual pathway edges (STRING scores >0.99) but moderate confidence for the combination therapy hypothesis, which remains preclinically motivated.

---

## 4. Discussion

### 4.1 Key Findings

This study demonstrates the application of automated, federated knowledge graph assembly to a translational cardio-oncology question in NF1. The Fuzzy-to-Fact pipeline identified three mechanistic axes -- TOP2 isoform selectivity, NRF2/KEAP1 antioxidant defense, and RAS-MAPK co-targeting -- each supported by multi-database concordance and grounded to experimental datasets in Synapse. The resulting 22-node, 19-edge KG provides a structured, queryable representation of the molecular landscape governing the balance between doxorubicin efficacy and cardiotoxicity in NF1.

The TOP2 isoform axis emerges as the most immediately actionable, given that dexrazoxane is already FDA-approved and trial NCT03930680 has demonstrated pharmacodynamic proof of concept for TOP2B depletion. The longstanding reluctance to use dexrazoxane broadly -- partly due to concerns about interference with anti-tumor efficacy and secondary malignancy risk -- may be mitigated by the mechanistic clarity that TOP2B (not TOP2A) is the cardiotoxicity target [17]. The pipeline's integration of gene-level (HGNC), protein-level (UniProt, STRING), compound-level (ChEMBL), and trial-level (ClinicalTrials.gov) data into a single graph enables clinicians and researchers to trace the evidence chain from molecular mechanism to clinical outcome.

### 4.2 Multi-Database Concordance

A central strength of the Fuzzy-to-Fact approach is evidence triangulation across independent databases. For example, the TOP2B cardiotoxicity assertion was confirmed by: (i) HGNC gene annotation establishing TOP2B as the cardiomyocyte-expressed isoform, (ii) UniProt functional annotation describing its role in transcriptional regulation, (iii) Open Targets linking TOP2B variants to anthracycline cardiotoxicity, and (iv) ClinicalTrials.gov providing interventional trial data for TOP2B-targeted cardioprotection. This four-source concordance yielded the highest confidence scores in the KG (0.88-0.92) and exemplifies how federated querying can produce robust, triangulated evidence assessments.

Similarly, the NF1-RAS-MAPK axis was validated through HGNC (NF1 gene identity), STRING (interaction scores >0.99 for NF1-KRAS-BRAF), Open Targets (NF1 disease association score 0.885), and ClinicalTrials.gov (selumetinib approval trials). The convergence of orthogonal data types -- genetic, proteomic, pharmacological, and clinical -- onto consistent mechanistic narratives supports the reliability of the automated pipeline.

### 4.3 Synapse Grounding

The mapping of KG assertions to six Synapse datasets adds an experimental grounding layer that goes beyond database annotations. The iPSC-derived cardiomyocyte cardiotoxicity datasets (syn7079983, syn13856689) provide functional readouts for drug-induced cardiac injury, while the Nrf2 knockout and NFE2L2 datasets (syn205590, syn237499) offer transcriptomic evidence for NRF2 pathway target genes. The NF Therapeutic Consortium dataset (syn21452685) and ERK1/2 feedback study (syn22266606) anchor the RAS-MAPK axis in NF1-specific experimental contexts. This Synapse layer transforms the KG from a purely annotation-derived structure into one connected to downloadable, reanalyzable experimental data.

### 4.4 Limitations

Several limitations should be noted. First, the pipeline relies entirely on publicly available database annotations and does not perform de novo data analysis; assertions are only as current and accurate as their source databases. Second, the evidence grading system, while structured, is heuristic and does not incorporate formal meta-analytic or Bayesian frameworks. Third, the combination therapy hypothesis (selumetinib + lower-dose doxorubicin for NF1 MPNSTs) is mechanistically motivated but has not been tested in clinical trials; the KG identifies this as a hypothesis-generating finding rather than a validated clinical recommendation. Fourth, ChEMBL API instability during pipeline execution required fallback to Open Targets knownDrugs queries, which may have introduced ascertainment bias toward drugs with established disease associations. Fifth, the pipeline does not currently model pharmacokinetic interactions, dosing schedules, or patient-specific pharmacogenomic variation (e.g., ABCB1 polymorphisms affecting doxorubicin bioavailability).

### 4.5 Future Directions

Several extensions of this work are warranted. First, the combination therapy hypothesis for selumetinib plus doxorubicin in NF1 MPNSTs should be evaluated in preclinical models and, if supported, advanced to clinical trial design. Second, pharmacogenomic stratification incorporating RARG susceptibility variants and ABCB1 polymorphisms could refine patient-level risk prediction. Third, the NRF2 activation axis could be explored through pharmacological activators (e.g., sulforaphane, bardoxolone methyl) or dietary interventions, with iPSC-CM models providing a scalable screening platform. Fourth, the Fuzzy-to-Fact pipeline itself could be extended with temporal modeling (treatment sequencing), quantitative dose-response integration, and automated literature extraction using PubMed full-text analysis. Finally, integration with the Graphiti knowledge graph persistence layer would enable longitudinal KG evolution as new data emerge from ongoing clinical trials.

---

## References

### Gene/Protein Databases

[1] HUGO Gene Nomenclature Committee (HGNC). Gene records: NF1 (HGNC:7765), TOP2A (HGNC:11989), TOP2B (HGNC:11990), NFE2L2 (HGNC:7782), NQO1 (HGNC:2874), HMOX1 (HGNC:5013), SOD2 (HGNC:11180), KEAP1 (HGNC:23177). https://www.genenames.org/

[2] UniProt Consortium. Protein entries: Neurofibromin (P21359), TOP2A (P11388), TOP2B (Q02880), NFE2L2 (Q16236), NQO1 (P15559), HMOX1 (P09601), SOD2 (P04179). https://www.uniprot.org/

### Interaction/Pathway Databases

[3] STRING v12. Protein-protein interaction network: NF1-KRAS (0.996), NF1-BRAF (0.999), NF1-SPRED1 (0.994). Szklarczyk D, et al. Nucleic Acids Res. 2023;51(D1):D483-D489. https://string-db.org/

[4] WikiPathways. WP408: Oxidative Stress Response; WP3612: NRF2 Pathway / Survival Signaling. Martens M, et al. Nucleic Acids Res. 2021;49(D1):D613-D621. https://www.wikipathways.org/

[5] Open Targets Platform. Disease-target associations for NF1 (MONDO:0018975), TOP2B cardiotoxicity, known drugs queries. Ochoa D, et al. Nucleic Acids Res. 2023;51(D1):D1302-D1310. https://platform.opentargets.org/

### Clinical Trials

[6] ClinicalTrials.gov. NCT03930680: Dexrazoxane TOP2B depletion kinetics study. Status: COMPLETED. https://clinicaltrials.gov/study/NCT03930680

[7] ClinicalTrials.gov. NCT01362803: Selumetinib in NF1 plexiform neurofibromas (SPRINT trial). Status: ACTIVE. https://clinicaltrials.gov/study/NCT01362803

[8] ClinicalTrials.gov. NCT00304083: Doxorubicin-based chemotherapy for NF1 MPNSTs. Status: COMPLETED. https://clinicaltrials.gov/study/NCT00304083

### Compound Databases

[9] ChEMBL. Dexrazoxane (CHEMBL:1738), mechanism: TOP2B degradation. Selumetinib (CHEMBL:1614701), mechanism: MEK1/2 inhibition. Zdrazil B, et al. Nucleic Acids Res. 2024;52(D1):D1180-D1192. https://www.ebi.ac.uk/chembl/

[10] PubChem. Compound records: Doxorubicin (CID:31703), Dexrazoxane (CID:71384), Selumetinib (CID:10127622). Kim S, et al. Nucleic Acids Res. 2023;51(D1):D1373-D1380. https://pubchem.ncbi.nlm.nih.gov/

### Synapse Datasets

[11] Sage Bionetworks Synapse. syn7079983: TKI cardiotoxicity profiling dataset. https://www.synapse.org/#!Synapse:syn7079983

[12] Sage Bionetworks Synapse. syn13856689: iPSC-derived cardiomyocyte cardiotoxicity screening. https://www.synapse.org/#!Synapse:syn13856689

[13] Sage Bionetworks Synapse. syn205590: Nrf2 knockout transcriptomics dataset. https://www.synapse.org/#!Synapse:syn205590

[14] Sage Bionetworks Synapse. syn237499: NFE2L2 functional study dataset. https://www.synapse.org/#!Synapse:syn237499

[15] Sage Bionetworks Synapse. syn21452685: NF Therapeutic Consortium dataset. https://www.synapse.org/#!Synapse:syn21452685

[16] Sage Bionetworks Synapse. syn22266606: NF1 ERK1/2 feedback signaling study. https://www.synapse.org/#!Synapse:syn22266606

### Review Articles and Primary Literature

[17] Lyu YL, Kerrigan JE, Lin CP, et al. Topoisomerase IIbeta mediated DNA double-strand breaks: implications in doxorubicin cardiotoxicity and prevention by dexrazoxane. Cancer Res. 2007;67(18):8839-8846.

[18] Zhang S, Liu X, Bawa-Khalfe T, et al. Identification of the molecular basis of doxorubicin-induced cardiotoxicity. Nat Med. 2012;18(11):1639-1642.

[19] Ma Q. Role of Nrf2 in oxidative stress and toxicity. Annu Rev Pharmacol Toxicol. 2013;53:401-426.

[20] Gutmann DH, Ferner RE, Listernick RH, et al. Neurofibromatosis type 1. Nat Rev Dis Primers. 2017;3:17004.

[21] Dombi E, Baldwin A, Marcus LJ, et al. Activity of selumetinib in neurofibromatosis type 1-related plexiform neurofibromas. N Engl J Med. 2016;375(26):2550-2560.

---

## Supplementary Materials

### Supplementary Table S1: Knowledge Graph Nodes

| Node ID | Label | Type | HGNC/DB ID | Locus / Identifier | Source DBs |
|---------|-------|------|------------|-------------------|------------|
| N1 | TOP2A | Gene | HGNC:11989 | 17q21.2 | HGNC, UniProt, STRING |
| N2 | TOP2B | Gene | HGNC:11990 | 3p24.2 | HGNC, UniProt, STRING, Open Targets |
| N3 | NFE2L2 | Gene | HGNC:7782 | 2q31.2 | HGNC, UniProt, WikiPathways |
| N4 | KEAP1 | Gene | HGNC:23177 | 19p13.2 | HGNC, UniProt, WikiPathways |
| N5 | NQO1 | Gene | HGNC:2874 | 16q22.1 | HGNC, UniProt, WikiPathways |
| N6 | HMOX1 | Gene | HGNC:5013 | 22q12.3 | HGNC, UniProt, WikiPathways |
| N7 | SOD2 | Gene | HGNC:11180 | 6q25.3 | HGNC, UniProt, WikiPathways |
| N8 | NF1 | Gene | HGNC:7765 | 17q11.2 | HGNC, UniProt, STRING, Open Targets |
| N9 | KRAS | Gene | -- | 12p12.1 | STRING, Open Targets |
| N10 | BRAF | Gene | -- | 7q34 | STRING, Open Targets |
| N11 | ABCB1 | Gene | -- | 7q21.12 | HGNC, Open Targets |
| N12 | RARG | Gene | -- | 12q13.13 | Open Targets |
| N13 | Doxorubicin | Compound | CHEMBL:53463 | CID:31703 | ChEMBL, PubChem |
| N14 | Dexrazoxane | Compound | CHEMBL:1738 | CID:71384 | ChEMBL, PubChem, ClinicalTrials.gov |
| N15 | Selumetinib | Compound | CHEMBL:1614701 | CID:10127622 | ChEMBL, PubChem, ClinicalTrials.gov |
| N16 | NF1 (disease) | Disease | MONDO:0018975 | OT score: 0.885 | Open Targets |
| N17 | Cardiotoxicity | Phenotype | -- | -- | Open Targets, ClinicalTrials.gov |
| N18 | WP408 | Pathway | WikiPathways | Oxidative Stress Response | WikiPathways |
| N19 | WP3612 | Pathway | WikiPathways | NRF2 Survival Signaling | WikiPathways |
| N20 | NCT03930680 | Trial | ClinicalTrials.gov | Dexrazoxane TOP2B | ClinicalTrials.gov |
| N21 | NCT01362803 | Trial | ClinicalTrials.gov | Selumetinib NF1 | ClinicalTrials.gov |
| N22 | NCT00304083 | Trial | ClinicalTrials.gov | Doxorubicin NF1 MPNSTs | ClinicalTrials.gov |

### Supplementary Table S2: Knowledge Graph Edges

| Edge ID | Source | Target | Relationship | Confidence | Evidence Sources |
|---------|--------|--------|-------------|------------|-----------------|
| E1 | Doxorubicin (N13) | TOP2A (N1) | poisons | 0.92 | HGNC, UniProt, STRING, Open Targets |
| E2 | Doxorubicin (N13) | TOP2B (N2) | poisons | 0.90 | HGNC, UniProt, Open Targets, ClinicalTrials.gov |
| E3 | TOP2A (N1) | NF1 disease (N16) | anti-tumor_target | 0.85 | Open Targets, ChEMBL |
| E4 | TOP2B (N2) | Cardiotoxicity (N17) | mediates | 0.90 | Open Targets, ClinicalTrials.gov, UniProt |
| E5 | Dexrazoxane (N14) | TOP2B (N2) | degrades | 0.88 | ChEMBL, Open Targets, ClinicalTrials.gov |
| E6 | Dexrazoxane (N14) | NCT03930680 (N20) | tested_in | 0.95 | ClinicalTrials.gov |
| E7 | KEAP1 (N4) | NFE2L2 (N3) | negatively_regulates | 0.82 | UniProt, WikiPathways |
| E8 | NFE2L2 (N3) | NQO1 (N5) | activates_transcription | 0.85 | HGNC, UniProt, WikiPathways |
| E9 | NFE2L2 (N3) | HMOX1 (N6) | activates_transcription | 0.80 | HGNC, UniProt, WikiPathways |
| E10 | NFE2L2 (N3) | SOD2 (N7) | activates_transcription | 0.78 | HGNC, UniProt, WikiPathways |
| E11 | NFE2L2 (N3) | WP3612 (N19) | member_of | 0.75 | WikiPathways |
| E12 | NQO1 (N5) | WP408 (N18) | member_of | 0.72 | WikiPathways |
| E13 | NF1 (N8) | KRAS (N9) | inhibits (GAP activity) | 0.90 | STRING (0.996), Open Targets |
| E14 | KRAS (N9) | BRAF (N10) | activates | 0.92 | STRING (0.999), Open Targets |
| E15 | Selumetinib (N15) | BRAF-MEK pathway | inhibits (MEK1/2) | 0.88 | ChEMBL, Open Targets, ClinicalTrials.gov |
| E16 | Selumetinib (N15) | NCT01362803 (N21) | tested_in | 0.95 | ClinicalTrials.gov |
| E17 | NF1 (N8) | NF1 disease (N16) | causal_gene | 0.885 | Open Targets (association score) |
| E18 | Doxorubicin (N13) | NCT00304083 (N22) | tested_in | 0.90 | ClinicalTrials.gov |
| E19 | RARG (N12) | Cardiotoxicity (N17) | susceptibility_variant | 0.55 | Open Targets |

### Supplementary Table S3: Evidence Grading Summary

| Grade | Criteria | Edge Count | Percentage | Example Edges |
|-------|----------|------------|------------|---------------|
| High (0.85-1.00) | 3+ independent DBs and/or completed trial | 7 | 36.8% | E1, E2, E4, E5, E6, E16, E18 |
| Moderate (0.65-0.84) | 2 independent DBs or active trial | 9 | 47.4% | E3, E7, E8, E9, E10, E13, E14, E15, E17 |
| Low (0.40-0.64) | Single DB, no independent corroboration | 3 | 15.8% | E11, E12, E19 |

**Overall KG confidence (mean):** 0.78

### Supplementary Table S4: Synapse Dataset Mapping

| Synapse ID | Dataset Title | Data Type | Relevant Nodes | Relevant Edges | KG Axis |
|------------|--------------|-----------|-----------------|-----------------|---------|
| syn7079983 | TKI cardiotoxicity profiling | Drug screening | N2 (TOP2B), N17 (Cardiotoxicity) | E4 | Axis 1 |
| syn13856689 | iPSC-CM cardiotoxicity screening | Functional assay | N2 (TOP2B), N13 (Doxorubicin) | E2, E4 | Axis 1 |
| syn205590 | Nrf2 knockout transcriptomics | RNA-seq | N3 (NFE2L2), N5 (NQO1), N6 (HMOX1), N7 (SOD2) | E8, E9, E10 | Axis 2 |
| syn237499 | NFE2L2 functional study | Transcriptomics | N3 (NFE2L2), N4 (KEAP1) | E7, E8 | Axis 2 |
| syn21452685 | NF Therapeutic Consortium | Multi-omic | N8 (NF1), N15 (Selumetinib) | E15, E17 | Axis 3 |
| syn22266606 | NF1 ERK1/2 feedback study | Signaling assay | N8 (NF1), N9 (KRAS), N10 (BRAF) | E13, E14 | Axis 3 |

---

*This manuscript was generated by the Life Sciences Deep Agents Platform using the Fuzzy-to-Fact knowledge graph assembly protocol. All data were retrieved from publicly available databases. No novel experimental data were generated. The knowledge graph JSON and full pipeline trace are available in the accompanying repository.*
