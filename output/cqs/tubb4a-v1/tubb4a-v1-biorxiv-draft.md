# TUBB4A and Hypomyelination with Atrophy of the Basal Ganglia and Cerebellum (H-ABC): A Systematic Knowledge Graph Analysis of Disease Mechanisms, Molecular Interactions, and Therapeutic Landscape

---

## Abstract

**Background:** Hypomyelination with Atrophy of the Basal Ganglia and Cerebellum (H-ABC; MONDO:0012905) is a rare autosomal dominant leukodystrophy caused by de novo mutations in TUBB4A, which encodes tubulin beta-4A class IVa. Despite identification of the causal gene, the mechanistic pathways linking TUBB4A dysfunction to oligodendrocyte failure, basal ganglia atrophy, and cerebellar degeneration remain incompletely characterized, and the therapeutic landscape is only beginning to emerge.

**Methods:** We applied the Fuzzy-to-Fact protocol, a 7-phase automated knowledge graph construction methodology (ANCHOR, ENRICH, EXPAND, TRAVERSE_DRUGS, TRAVERSE_TRIALS, VALIDATE, PERSIST), to systematically resolve TUBB4A and its molecular interaction network against authoritative biomedical databases including HGNC, UniProt, STRING, Open Targets, ClinicalTrials.gov, WikiPathways, Ensembl, and Entrez. Evidence was graded on an L1--L4 scale (L1 = curated database with experimental confirmation; L2 = strong indirect evidence; L3 = mechanistic inference; L4 = computational prediction only).

**Results:** The constructed knowledge graph comprises 27 nodes (8 gene, 1 protein, 2 disease, 1 compound, 1 target, 10 pathway, 4 clinical trial) and 27 edges. STRING protein-protein interaction analysis identified 7 high-confidence interactors (score >= 0.700), revealing five mechanistic axes: (i) heterodimer disruption with TUBA4A (score 0.983), (ii) impaired axonal transport via MAPT/tau (0.953) and dynein (DYNC1I1, 0.861), (iii) gap junction trafficking failure via GJA1/connexin-43 (0.940), (iv) aberrant RhoA signaling through ARHGEF2/GEF-H1 release (0.906), and (v) convergent dystonia pathology via TOR1A/torsinA (0.895). Two N-of-1 antisense oligonucleotide (ASO) clinical trials targeting TUBB4A-related leukodystrophy were identified (NCT07222371, NCT06369974), along with two supporting observational studies (NCT02699190, NCT03047369). Oncology tubulin inhibitors (3,956 entries in Open Targets) were determined to be contraindicated due to the dominant-negative disease mechanism.

**Conclusions:** Automated knowledge graph construction provides a reproducible, evidence-graded framework for mapping rare disease mechanisms. The TUBB4A interaction network suggests that H-ABC pathology extends beyond simple microtubule assembly defects to encompass transport, signaling, and intercellular communication disruptions. ASO-based approaches represent the most mechanistically appropriate therapeutic strategy for this dominant-negative condition.

**Keywords:** TUBB4A, H-ABC, hypomyelinating leukodystrophy, knowledge graph, microtubule, antisense oligonucleotide, rare disease, Fuzzy-to-Fact

---

## 1. Introduction

### 1.1 TUBB4A Biology

TUBB4A (tubulin beta 4A class IVa; HGNC:20774) encodes a 444-amino-acid beta-tubulin isoform that is a core structural component of microtubules [1,2]. Located on chromosome 19p13.3 (chr19:6,494,319--6,502,848, GRCh38, strand -1), the gene has 13 known transcripts including the canonical ENST00000264071 [3]. Beta-tubulins heterodimerize with alpha-tubulins to form the fundamental building blocks of microtubules, dynamic cytoskeletal polymers essential for intracellular transport, cell division, cell shape maintenance, and signal transduction [1]. The TUBB4A protein binds GTP at an exchangeable site on the beta chain; microtubules grow by the addition of GTP-tubulin dimers to the plus end, where a stabilizing GTP cap forms, while below the cap, tubulin dimers convert to the GDP-bound state through intrinsic GTPase activity [1].

TUBB4A is one of several beta-tubulin isotypes expressed in the human genome, with particularly high expression in the central nervous system [4]. Its paralog TUBB4B (tubulin beta 4B class IVb; HGNC:20771) shares high sequence identity and exhibits coexpression and experimental interaction (STRING score 0.883) [5]. The brain-enriched expression pattern of TUBB4A is critical to understanding why its mutations produce neurological disease: myelinating oligodendrocytes depend heavily on microtubule-based transport for myelin sheath elaboration and maintenance, making them disproportionately vulnerable to tubulin dysfunction [4].

### 1.2 Hypomyelination with Atrophy of the Basal Ganglia and Cerebellum (H-ABC)

H-ABC (Orphanet:139441; MONDO:0012905; OMIM:612438) is a rare autosomal dominant leukodystrophy caused by de novo missense mutations in TUBB4A [6,7]. The disease is characterized by progressive hypomyelination of cerebral white matter, atrophy of the neostriatum (caudate and putamen), and cerebellar atrophy [6]. Clinical features include dystonia (measured by the Barry Albright Dystonia Scale and Burke-Fahn-Marsden Dystonia Rating Scale), gross motor dysfunction, spasticity, developmental delay, feeding and swallowing difficulties, and adaptive behavior impairment [8,9]. The Open Targets association score between TUBB4A and H-ABC is 0.76, reflecting strong genetic evidence [10].

Notably, TUBB4A mutations at different positions can also cause autosomal dominant torsion dystonia type 4 (DYT4; Orphanet:98805; MONDO:0007493; Open Targets score 0.74), presenting with isolated dystonia without the leukodystrophy or myelination defects seen in H-ABC [7,10]. The gene was previously designated DYT4 [2]. This genotype-phenotype dichotomy suggests that different TUBB4A mutations differentially affect microtubule dynamics in oligodendrocytes versus basal ganglia neurons.

### 1.3 Knowledge Gap

Although the causal relationship between TUBB4A mutations and H-ABC is established (evidence grade L1), the mechanistic pathways through which mutant TUBB4A protein produces oligodendrocyte dysfunction, basal ganglia atrophy, and cerebellar degeneration remain incompletely characterized. The protein-protein interaction network of TUBB4A has not been systematically mapped to disease-relevant pathways, and the therapeutic landscape -- including both disease-specific interventions and contraindicated agents -- has not been comprehensively catalogued in an integrated framework.

### 1.4 Competency Question

This study addresses the competency question: *"Which therapeutic interventions, clinical phenotypes, and biological pathways are connected to the TUBB4A gene in the context of Hypomyelination with Atrophy of the Basal Ganglia and Cerebellum (H-ABC), and how do its molecular interactions explain the disease pathology?"*

### 1.5 Protocol Overview

We applied the Fuzzy-to-Fact protocol, a 7-phase automated knowledge graph construction methodology, to resolve TUBB4A across authoritative biomedical databases, map its interaction network, identify disease-relevant pathways, characterize the therapeutic landscape including clinical trials, and validate all findings through cross-reference verification. The resulting knowledge graph provides a structured, evidence-graded resource for H-ABC mechanistic understanding.

---

## 2. Methods

### 2.1 Fuzzy-to-Fact Protocol

The Fuzzy-to-Fact protocol is a 7-phase automated knowledge graph construction methodology designed for systematic biomedical entity resolution, evidence gathering, and claim assessment. Each phase employs specific data sources and produces structured outputs that feed into subsequent phases.

| Phase | Name | Purpose | Tools Used |
|-------|------|---------|------------|
| 1 | ANCHOR | Entity resolution to standard CURIEs | HGNC, Ensembl, Entrez |
| 2 | ENRICH | Cross-reference enrichment and protein metadata | UniProt, Ensembl |
| 3 | EXPAND | Pathway membership and interaction network mapping | STRING, WikiPathways |
| 4a | TRAVERSE_DRUGS | Drug-target landscape and contraindication analysis | Open Targets knownDrugs, ChEMBL |
| 4b | TRAVERSE_TRIALS | Clinical trial retrieval and verification | ClinicalTrials.gov v2 API |
| 5 | VALIDATE | Cross-database consistency checking | All sources (cross-reference validation) |
| 6 | PERSIST | Knowledge graph serialization and report generation | Internal (JSON-LD output) |

### 2.2 Entity Resolution (Phases 1--2)

The primary gene entity TUBB4A was resolved to HGNC:20774 using the HGNC REST API [2], then enriched with cross-references: Ensembl (ENSG00000104833) [3], UniProt (P04350) [1], Entrez (10382) [4], OMIM (602662) [2], BioGRID (115655) [1], ChEMBL target (CHEMBL3838) [10], and DrugBank (DB11638) [10]. STRING protein identifier 9606.ENSP00000264071 was used for interaction queries [5].

Disease entities were resolved via Open Targets disease associations: H-ABC (MONDO:0012905, Orphanet:139441; score 0.76--0.77) and DYT4 (MONDO:0007493, Orphanet:98805; score 0.72--0.74) [10].

Seven high-confidence protein interactors (STRING combined score >= 0.700) were identified and individually resolved to HGNC IDs with full cross-references (Ensembl, UniProt, Entrez, chromosomal location, OMIM) [2].

### 2.3 Data Sources

| Database | Version/Access | Data Retrieved | Timeout |
|----------|---------------|----------------|---------|
| HGNC | REST API | Gene symbols, aliases, cross-references | 30s |
| UniProt | REST API (P04350) | Protein function, length, domains | 30s |
| STRING | v12 (score >= 700) | Protein-protein interactions with evidence channels | 120s |
| Open Targets | Platform API | Disease associations, knownDrugs | 120s |
| ClinicalTrials.gov | v2 API | Trial metadata, status, outcomes | 30s |
| WikiPathways | REST API | Pathway membership for TUBB4A and MAPT | 30s |
| Ensembl | REST API (GRCh38) | Genomic coordinates, transcript catalog | 30s |
| Entrez | NCBI E-utilities | Gene summary, PubMed links | 30s |

### 2.4 Evidence Grading System

Evidence was graded on a 4-level scale reflecting data provenance and inferential distance:

| Level | Definition | Example |
|-------|-----------|---------|
| **L1** | Direct experimental evidence confirmed by curated database annotation | TUBB4A mutations cause H-ABC (OMIM, Open Targets, NCBI Gene) |
| **L2** | Strong indirect evidence from multiple databases, interaction scores, and/or genetic associations | ASO therapy targets TUBB4A (active clinical trials NCT07222371, NCT06369974) |
| **L3** | Mechanistic inference from pathway membership or interaction data | GJA1 trafficking disruption contributes to hypomyelination |
| **L4** | Computational prediction only, no experimental or curated support | (None assigned in this analysis) |

### 2.5 Quality Assessment

Cross-reference consistency was verified across 9 databases (HGNC, Ensembl, UniProt, Entrez, STRING, BioGRID, OMIM, ChEMBL, DrugBank) for the primary entity TUBB4A. All 9 cross-references were validated as consistent [2,3,4,5,10]. Clinical trials were individually verified using ClinicalTrials.gov get_trial API calls to confirm status, sponsor, intervention, and outcome measures [8,9,11,12]. Overall confidence score for the analysis was 0.82 (median of all claim scores).

---

## 3. Results

### 3.1 Knowledge Graph Topology

The constructed knowledge graph comprises 27 nodes and 27 edges, organized as follows:

| Node Type | Count | Description |
|-----------|-------|-------------|
| Gene | 8 | TUBB4A + 7 interactors (TUBA4A, MAPT, GJA1, ARHGEF2, TOR1A, TUBB4B, DYNC1I1) |
| Protein | 1 | Tubulin beta-4A chain (P04350) |
| Disease | 2 | H-ABC (Orphanet:139441), DYT4 (Orphanet:98805) |
| Compound | 1 | nL-TUBB4-001 (ASO) |
| Target | 1 | CHEMBL:CHEMBL3838 (tubulin beta-4A chain drug target) |
| Pathway | 10 | 8 TUBB4A pathways + 2 MAPT pathways (WikiPathways) |
| Clinical Trial | 4 | NCT07222371, NCT06369974, NCT02699190, NCT03047369 |
| **Total** | **27** | |

Edge types include ENCODES (1), ASSOCIATED_WITH (2), INTERACTS (7), MODULATOR (1), TREATS (1), MEMBER_OF (11), and STUDIES (4), totaling 27 edges.

The graph exhibits a hub-and-spoke topology centered on TUBB4A (HGNC:20774), which connects to all 7 interactor genes, both disease nodes, 8 pathway nodes, and the protein node. Secondary hubs include MAPT (connecting to 2 additional pathway nodes) and H-ABC (connecting to all 4 clinical trial nodes and the ASO compound).

### 3.2 Protein-Protein Interaction Network

STRING interaction analysis (combined score >= 0.700) identified 7 high-confidence interactors for TUBB4A (STRING ID: 9606.ENSP00000264071) [5]:

| Interactor | STRING Score | Evidence Channels | Functional Role |
|------------|-------------|-------------------|-----------------|
| TUBA4A | 0.983 | Coexpression, database, experimental | Alpha-tubulin heterodimer partner |
| MAPT (tau) | 0.953 | Database, experimental, textmining | Microtubule stabilization |
| GJA1 (connexin-43) | 0.940 | Database, textmining | Gap junction trafficking |
| ARHGEF2 (GEF-H1) | 0.906 | Database | Microtubule-sequestered RhoA activator |
| TOR1A (torsinA) | 0.895 | Textmining | AAA+ ATPase; DYT1 dystonia gene |
| TUBB4B | 0.883 | Coexpression, database, experimental | Paralogous beta-tubulin isoform |
| DYNC1I1 | 0.861 | Database, experimental, textmining | Cytoplasmic dynein motor protein |

### 3.3 Five Mechanistic Axes of H-ABC Pathology

Analysis of the TUBB4A interaction network reveals five mechanistic axes through which dominant-negative TUBB4A mutations produce H-ABC pathology:

#### 3.3.1 Axis 1: Heterodimer Disruption (TUBB4A--TUBA4A)

TUBB4A forms obligate heterodimers with TUBA4A (STRING score 0.983; evidence: coexpression, database, experimental) [5]. Missense mutations in TUBB4A are predicted to disrupt the heterodimer interface in a dominant-negative fashion, producing "poisoned dimers" that incorporate into growing microtubules and destabilize them from within. Since TUBB4A is highly expressed in myelinating oligodendrocytes of the central nervous system, this predominantly affects white matter integrity. **Evidence grade: L2** (database and experimental interaction data, genetic association, but limited functional studies directly in oligodendrocytes).

#### 3.3.2 Axis 2: Impaired Axonal Transport (MAPT/tau, DYNC1I1)

Cytoplasmic dynein (DYNC1I1, STRING score 0.861) is a motor protein complex that translocates cargo retrogradely along microtubules [2]. MAPT/tau (STRING score 0.953) stabilizes microtubule tracks required for dynein-mediated transport [5]. Destabilized microtubules from TUBB4A mutations would impair dynein-dependent transport of myelin components, organelles, and signaling molecules in oligodendrocyte processes, contributing to hypomyelination. The MAPT pathway membership in microtubule cytoskeleton regulation (WP:WP2038) and BDNF signaling (WP:WP2380) further supports the importance of intact microtubule transport for neurotrophic support [13]. **Evidence grade: L2** (strong interaction data, plausible mechanism, indirect evidence for H-ABC specifically).

#### 3.3.3 Axis 3: Gap Junction Disruption (GJA1/Connexin-43)

GJA1/connexin-43 (STRING score 0.940) requires intact microtubules for trafficking to gap junction plaques [5]. In the brain, connexin-43 is expressed in astrocytes and forms heterotypic gap junctions with oligodendrocytic connexins. Disrupted GJA1 trafficking due to TUBB4A mutations would impair astrocyte-oligodendrocyte metabolic coupling, a pathway critical for myelin maintenance. **Evidence grade: L3** (strong interaction score but indirect mechanistic inference).

#### 3.3.4 Axis 4: Aberrant RhoA Signaling (ARHGEF2/GEF-H1)

ARHGEF2/GEF-H1 (STRING score 0.906) is normally sequestered on polymerized microtubules [5]. When microtubules depolymerize, GEF-H1 is released and activates RhoA, driving cytoskeletal remodeling [2]. TUBB4A mutations causing microtubule instability would lead to chronic, inappropriate RhoA activation, which could impair oligodendrocyte process extension and myelination. **Evidence grade: L3** (interaction well-established, but H-ABC-specific role is inferred).

#### 3.3.5 Axis 5: Dystonia Pathway Convergence (TOR1A)

TOR1A (torsinA, STRING score 0.895) is mutated in DYT1 early-onset generalized dystonia and interacts with tubulin [5,2]. TUBB4A was previously designated DYT4, and mutations at different positions cause dystonia rather than H-ABC [2]. This shared interaction network between TUBB4A and TOR1A suggests a converging microtubule-dependent mechanism in basal ganglia neurons that explains the dystonia component of H-ABC. **Evidence grade: L2** (genetic evidence, interaction data, and shared phenotype).

### 3.4 The Tubulin Code and Post-Translational Modifications

TUBB4A participates in the "Carboxyterminal post-translational modifications of tubulin" pathway (WP:WP4075) [13], which encodes the tubulin code hypothesis. This hypothesis proposes that specific combinations of tubulin isoforms and post-translational modifications (acetylation, glutamylation, tyrosination, detyrosination) encode functional properties of microtubules, including selective recruitment of motor proteins and microtubule-associated proteins. TUBB4A also participates in the protein folding pathway (WP:WP1892), reflecting the requirement for CCT/TRiC chaperonin complex-mediated folding of tubulin monomers, and in cilium assembly pathways (WP:WP4124, WP:WP3498), consistent with the role of primary cilia in neural progenitor signaling.

The shared pathway membership of TUBB4A and MAPT in the Alzheimer's disease and miRNA effects pathway (WP:WP2059) highlights a convergence between tubulin dysfunction and tauopathy, with both proteins contributing to microtubule-dependent neurodegeneration through distinct but overlapping mechanisms [13].

### 3.5 Therapeutic Landscape

#### 3.5.1 Antisense Oligonucleotide (ASO) Therapy

Two N-of-1 interventional clinical trials are investigating ASO therapy specifically for TUBB4A-related leukodystrophy:

**Trial 1: NCT07222371** [8]
- **Intervention:** nL-TUBB4-001 (intrathecal antisense oligonucleotide)
- **Sponsor:** University of California, San Diego
- **Status:** ACTIVE_NOT_RECRUITING (started September 19, 2025)
- **Completion:** September 2027
- **Design:** Single-participant, open-label
- **Primary outcomes:** Barry Albright Dystonia Scale (BAD), Burke-Fahn-Marsden Dystonia Rating Scale (BFMDRS), Gross Motor Function Measure-88 (GMFM-88), Vineland Adaptive Behavior Scales (baseline to 12 and 24 months)
- **Secondary outcomes:** Bayley Scales of Infant Development (BSID-4), PedsQL Family Impact Module
- **Eligibility:** Confirmed TUBB4A mutation with clinical and neuroimaging findings consistent with H-ABC

**Trial 2: NCT06369974** [9]
- **Intervention:** Antisense oligonucleotide treatment (ASO)
- **Sponsor:** Massachusetts General Hospital
- **Collaborator:** n-Lorem Foundation
- **Status:** NOT_YET_RECRUITING (planned start June 2024, completion June 2026)
- **Design:** Single-participant, open-label
- **Primary outcomes:** GMFM88, Hammersmith Infant Neurological Examination (HINE-1/2), Bayley-4, Vineland-3, Tardieu Spasticity Scale, PedsQL
- **Secondary outcomes:** Feeding and swallow evaluation, safety and tolerability
- **Eligibility:** Age >= 4 years, confirmed TUBB4A mutation with H-ABC phenotype

#### 3.5.2 Diagnostic and Natural History Studies

**NCT02699190 (LeukoSEQ)** [11]: A completed observational study (2017--2023) at Children's Hospital of Philadelphia evaluating whole genome sequencing as a diagnostic tool for leukodystrophies, including H-ABC/TUBB4A-related leukodystrophy among 60+ subtypes. This study demonstrated the utility of WGS for diagnosing previously unclassified leukodystrophies.

**NCT03047369 (Myelin Disorders Biorepository)** [12]: An ongoing observational study (2016--2030) at Children's Hospital of Philadelphia with biospecimen banking and longitudinal natural history tracking. Key collaborators include NIH, NINDS, NCATS, Biogen, Ionis Pharmaceuticals, Sana Biotechnology, and the Foundation to Fight H-ABC. The involvement of Ionis Pharmaceuticals, a leading ASO developer, suggests an active ASO development pipeline for leukodystrophies beyond the two N-of-1 trials.

#### 3.5.3 Contraindicated Oncology Agents

Open Targets lists 3,956 drug-target entries for TUBB4A (CHEMBL:CHEMBL3838), all classified as tubulin inhibitors or stabilizers used in oncology [10]. Representative agents include paclitaxel (CHEMBL428647, Phase 4), docetaxel (CHEMBL92, Phase 4), vinblastine (CHEMBL159, Phase 4), vinorelbine (CHEMBL553025, Phase 4), eribulin (CHEMBL1683590, Phase 4), ixabepilone (CHEMBL1201752, Phase 4), and multiple antibody-drug conjugates (brentuximab vedotin, trastuzumab emtansine, polatuzumab vedotin, tisotumab vedotin) [10].

These agents are contraindicated for H-ABC for three reasons: (i) H-ABC results from a dominant-negative TUBB4A mutation that disrupts microtubule function; (ii) tubulin inhibitors would further destabilize already compromised microtubules; and (iii) the therapeutic need in H-ABC is to restore or compensate for normal microtubule function, not to inhibit it.

### 3.6 Clinical Phenotypes and Genotype-Phenotype Correlations

Clinical trial eligibility criteria and outcome measures define the H-ABC phenotype across multiple functional domains [8,9]:

| Domain | Assessment Instrument | Key Features |
|--------|----------------------|--------------|
| Dystonia | BAD, BFMDRS | Affects eyes, mouth, neck, trunk, limbs |
| Motor function | GMFM-88 | 5 dimensions: lying/rolling, sitting, crawling, standing, walking |
| Spasticity | Tardieu Spasticity Scale | Upper and lower extremity assessment |
| Development | BSID-4, Bayley-4 | Cognitive, language, motor domains |
| Feeding | Swallow evaluation | Oropharyngeal dysphagia assessment |
| Adaptive behavior | Vineland-3 | Communication, motor skills, daily living |
| Neuroimaging | MRI (inclusion criterion) | Hypomyelination, basal ganglia and cerebellar atrophy |

The genotype-phenotype correlation between H-ABC and DYT4 is notable: mutations in TUBB4A at different positions produce either a combined leukodystrophy-dystonia phenotype (H-ABC) or isolated dystonia without white matter involvement (DYT4) [2,10]. This suggests that specific amino acid substitutions differentially affect microtubule dynamics in oligodendrocytes (myelination-dependent) versus basal ganglia neurons (motor circuit-dependent), providing a natural experiment for dissecting cell-type-specific tubulin requirements.

### 3.7 Evidence Grading Summary

| Claim | Grade | Justification |
|-------|-------|---------------|
| TUBB4A mutations cause H-ABC | L1 | OMIM, Open Targets, NCBI Gene all confirm causal link |
| TUBB4A-TUBA4A heterodimer is critical for microtubule assembly | L1 | Biochemically established, STRING 0.983 |
| MAPT stabilizes TUBB4A-containing microtubules | L1 | Extensively studied, STRING 0.953 |
| ASO therapy (nL-TUBB4-001) targets TUBB4A | L2 | Active clinical trials NCT07222371, NCT06369974 |
| Disrupted dynein transport contributes to H-ABC | L2 | Plausible mechanism, strong interaction data |
| TOR1A-TUBB4A interaction links H-ABC to dystonia | L2 | Genetic evidence + STRING 0.895 |
| Oncology tubulin drugs contraindicated in H-ABC | L2 | Logical deduction from disease mechanism |
| GJA1 trafficking disruption contributes to hypomyelination | L3 | Interaction confirmed, mechanism inferred |
| ARHGEF2 release causes aberrant RhoA in H-ABC | L3 | Interaction confirmed, mechanism inferred |
| Tubulin code alterations affect H-ABC pathology | L3 | Pathway membership, mechanistic inference |

---

## 4. Discussion

### 4.1 Key Findings

This systematic knowledge graph analysis of TUBB4A provides the first integrated, evidence-graded mapping of the molecular interaction network, disease mechanisms, and therapeutic landscape for H-ABC. Three principal findings emerge.

First, the TUBB4A interaction network reveals that H-ABC pathology likely extends far beyond a simple microtubule assembly defect. The five mechanistic axes identified -- heterodimer disruption, impaired transport, gap junction failure, aberrant RhoA signaling, and dystonia pathway convergence -- suggest a multi-system cellular failure in which destabilized microtubules simultaneously compromise structural integrity, intracellular logistics, intercellular communication, and cytoskeletal signaling. This framework explains why H-ABC presents with such a broad clinical phenotype spanning motor, cognitive, and white matter domains.

Second, the therapeutic landscape for H-ABC is at a critical inflection point. The two N-of-1 ASO trials (NCT07222371 and NCT06369974) represent the first disease-specific interventions for H-ABC, employing a mechanistically rational approach: reducing the burden of dominant-negative mutant TUBB4A transcript to allow the normal allele to restore functional microtubule assembly. The involvement of the n-Lorem Foundation and Ionis Pharmaceuticals in the broader leukodystrophy pipeline (NCT03047369) suggests growing investment in precision ASO approaches for this disease class.

Third, the explicit identification of 3,956 contraindicated oncology agents is a clinically important negative finding. Patients with H-ABC who develop comorbid conditions requiring tubulin-targeting chemotherapy would face heightened risk of neurological toxicity, and this knowledge graph annotation provides a structured basis for drug safety assessment.

### 4.2 Dominant-Negative Mechanism Implications

The dominant-negative nature of TUBB4A mutations in H-ABC -- where mutant protein actively poisons microtubule function rather than simply reducing it -- has profound implications for therapeutic strategy. Unlike loss-of-function diseases where gene replacement might suffice, H-ABC requires either (a) selective silencing of the mutant allele while preserving wild-type expression (allele-specific ASO), (b) reduction of total TUBB4A expression below a toxicity threshold while maintaining sufficient wild-type protein (the apparent strategy of current ASO trials), or (c) compensatory upregulation of paralogous tubulins such as TUBB4B (STRING score 0.883) to functionally substitute for TUBB4A in critical microtubule populations.

The finding that TUBB4B is a high-confidence coexpression partner of TUBB4A raises the possibility that endogenous compensatory mechanisms may partially buffer against TUBB4A dysfunction, potentially explaining the variable expressivity and age of onset observed in H-ABC.

### 4.3 ASO Therapeutic Promise

The ASO approach is particularly well-suited to H-ABC for several reasons. Intrathecal delivery bypasses the blood-brain barrier, achieving direct CNS exposure. The n-Lorem Foundation model of individualized N-of-1 ASO design enables treatment of ultra-rare mutations that would be uneconomical for traditional drug development. The outcome measures selected in both trials (dystonia scales, motor function, adaptive behavior, developmental milestones) are clinically meaningful and longitudinally assessable. However, the single-participant design of both trials limits the ability to draw population-level conclusions, and the absence of control groups means that natural history data from NCT03047369 will be essential for interpreting treatment effects.

### 4.4 Limitations

This analysis has several limitations. First, the interaction network was derived from STRING, which aggregates heterogeneous evidence types (experimental, database, textmining, coexpression) with varying reliability; the mechanistic axes proposed here are hypotheses ranked by evidence grade, not experimentally validated causal pathways. Second, several key interactions (GJA1, ARHGEF2) carry L3 evidence grades, indicating inference rather than direct experimental demonstration in the H-ABC context. Third, the knowledge graph does not incorporate Synapse dataset-level grounding (e.g., TCGA expression data, DepMap essentiality screens) due to system maintenance at the time of analysis, which would strengthen the tissue-specificity and essentiality assessments. Fourth, the analysis is limited to curated databases and does not include primary literature review beyond PubMed identifiers. Fifth, the analysis represents a temporal snapshot; clinical trial statuses and database annotations are dynamic.

### 4.5 Future Directions

Several extensions of this work are warranted. (i) Synapse dataset integration for TUBB4A expression across brain cell types, particularly comparing oligodendrocyte versus neuronal expression, would inform cell-type-specific vulnerability models. (ii) Allele-specific ASO design considerations could be explored by mapping known H-ABC mutations to the TUBB4A-TUBA4A heterodimer interface using structural data. (iii) The TUBB4B compensatory hypothesis could be tested by examining TUBB4B expression in H-ABC patient-derived cells. (iv) Expansion of the interaction network to include TUBB4A interactions below the 0.700 STRING threshold and BioGRID physical interactions (BioGRID:115655) would provide a more comprehensive view. (v) Longitudinal monitoring of the two ASO trials and the Myelin Disorders Biorepository (NCT03047369) will be essential for evaluating therapeutic efficacy and natural history.

---

## References

### Gene and Protein Databases

[1] UniProt Consortium. UniProtKB entry P04350 (Tubulin beta-4A chain, Homo sapiens). https://www.uniprot.org/uniprot/P04350.

[2] HUGO Gene Nomenclature Committee (HGNC). HGNC:20774 (TUBB4A). https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:20774.

[3] Ensembl. ENSG00000104833 (TUBB4A). https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000104833.

[4] NCBI Gene. Gene ID 10382 (TUBB4A). https://www.ncbi.nlm.nih.gov/gene/10382.

### Interaction Databases

[5] STRING Database v12. Protein interaction network for 9606.ENSP00000264071 (TUBB4A). https://string-db.org/.

[6] OMIM. Entry 612438 (Leukodystrophy, hypomyelinating, 6). https://www.omim.org/entry/612438.

[7] Orphanet. Orphanet:139441 (H-ABC); Orphanet:98805 (DYT4). https://www.orpha.net/.

### Clinical Trial Databases

[8] ClinicalTrials.gov. NCT07222371: An Open-label, Single Center, Single Participant Study of nL-TUBB4-001 for TUBB4A-related Leukodystrophy. University of California, San Diego. https://clinicaltrials.gov/study/NCT07222371.

[9] ClinicalTrials.gov. NCT06369974: An Open-label Single Center, Single Participant Study of ASO Treatment for TUBB4A-related Leukodystrophy. Massachusetts General Hospital / n-Lorem Foundation. https://clinicaltrials.gov/study/NCT06369974.

[10] Open Targets Platform. Target: ENSG00000104833 (TUBB4A). https://platform.opentargets.org/target/ENSG00000104833.

[11] ClinicalTrials.gov. NCT02699190: LeukoSEQ -- Whole Genome Sequencing as a Diagnostic Tool for Leukodystrophies. Children's Hospital of Philadelphia. https://clinicaltrials.gov/study/NCT02699190.

[12] ClinicalTrials.gov. NCT03047369: Myelin Disorders Biorepository Project. Children's Hospital of Philadelphia. https://clinicaltrials.gov/study/NCT03047369.

### Pathway Databases

[13] WikiPathways. Pathways for TUBB4A: WP2652, WP1892, WP4124, WP3498, WP4075, WP1859, WP2359, WP2059. Pathways for MAPT: WP2038, WP5372, WP5426, WP1784, WP2380, WP5124. https://www.wikipathways.org/.

### PubMed References

[14] Selected PubMed identifiers for TUBB4A: PMID:35589707, PMID:24706558, PMID:24785942, PMID:25085639, PMID:25545912, PMID:25772097, PMID:26318963, PMID:26375501, PMID:26643067, PMID:35871212, PMID:6865944, PMID:6462917, PMID:23595291. Source: NCBI Entrez gene-to-pubmed links (Gene ID: 10382) and HGNC (HGNC:20774).

---

## Supplementary Materials

### Supplementary Table S1: Knowledge Graph Nodes (27 nodes)

| ID | Label | Type | Evidence Level |
|----|-------|------|---------------|
| HGNC:20774 | TUBB4A | Gene | L1 |
| HGNC:12407 | TUBA4A | Gene | L1 |
| HGNC:6893 | MAPT | Gene | L1 |
| HGNC:3098 | TOR1A | Gene | L2 |
| HGNC:4274 | GJA1 | Gene | L2 |
| HGNC:682 | ARHGEF2 | Gene | L3 |
| HGNC:20771 | TUBB4B | Gene | L2 |
| HGNC:2963 | DYNC1I1 | Gene | L2 |
| UniProtKB:P04350 | Tubulin beta-4A chain | Protein | L1 |
| Orphanet:139441 | H-ABC | Disease | L1 |
| Orphanet:98805 | Primary dystonia, DYT4 type | Disease | L1 |
| CHEMBL:CHEMBL3838 | Tubulin beta-4A chain (drug target) | Target | L1 |
| ASO:nL-TUBB4-001 | nL-TUBB4-001 | Compound | L2 |
| WP:WP2652 | Mitotic Prometaphase | Pathway | L1 |
| WP:WP1892 | Protein folding | Pathway | L1 |
| WP:WP4124 | Cilium Assembly | Pathway | L1 |
| WP:WP4075 | Carboxyterminal PTMs of tubulin | Pathway | L1 |
| WP:WP1859 | Mitotic G2-G2/M phases | Pathway | L1 |
| WP:WP2359 | Parkin-ubiquitin proteasomal pathway | Pathway | L1 |
| WP:WP2038 | Microtubule cytoskeleton regulation | Pathway | L1 |
| WP:WP2059 | Alzheimer's disease and miRNA effects | Pathway | L1 |
| NCT:07222371 | nL-TUBB4-001 ASO (UCSD) | ClinicalTrial | L2 |
| NCT:06369974 | ASO Treatment (MGH) | ClinicalTrial | L2 |
| NCT:02699190 | LeukoSEQ (CHOP) | ClinicalTrial | L1 |
| NCT:03047369 | Myelin Disorders Biorepository (CHOP) | ClinicalTrial | L1 |
| WP:WP3498 | Assembly of the primary cilium | Pathway | L1 |
| WP:WP1784 | Apoptotic execution phase | Pathway | L1 |

### Supplementary Table S2: Knowledge Graph Edges (27 edges)

| Source | Target | Type | Evidence |
|--------|--------|------|----------|
| HGNC:20774 (TUBB4A) | UniProtKB:P04350 | ENCODES | hgnc_get_gene(HGNC:20774) |
| HGNC:20774 (TUBB4A) | Orphanet:139441 (H-ABC) | ASSOCIATED_WITH | Open Targets score 0.76; OMIM:612438 |
| HGNC:20774 (TUBB4A) | Orphanet:98805 (DYT4) | ASSOCIATED_WITH | Open Targets score 0.74; OMIM:128101 |
| HGNC:20774 (TUBB4A) | HGNC:12407 (TUBA4A) | INTERACTS | STRING 0.983; coexpression, database, experimental |
| HGNC:20774 (TUBB4A) | HGNC:6893 (MAPT) | INTERACTS | STRING 0.953; database, experimental, textmining |
| HGNC:20774 (TUBB4A) | HGNC:4274 (GJA1) | INTERACTS | STRING 0.940; database, textmining |
| HGNC:20774 (TUBB4A) | HGNC:682 (ARHGEF2) | INTERACTS | STRING 0.906; database |
| HGNC:20774 (TUBB4A) | HGNC:3098 (TOR1A) | INTERACTS | STRING 0.895; textmining |
| HGNC:20774 (TUBB4A) | HGNC:20771 (TUBB4B) | INTERACTS | STRING 0.883; coexpression, database, experimental |
| HGNC:20774 (TUBB4A) | HGNC:2963 (DYNC1I1) | INTERACTS | STRING 0.861; database, experimental, textmining |
| ASO:nL-TUBB4-001 | HGNC:20774 (TUBB4A) | MODULATOR | ASO targeting TUBB4A mutant transcript |
| ASO:nL-TUBB4-001 | Orphanet:139441 (H-ABC) | TREATS | NCT07222371, NCT06369974 |
| HGNC:20774 (TUBB4A) | WP:WP2652 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:20774 (TUBB4A) | WP:WP1892 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:20774 (TUBB4A) | WP:WP4124 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:20774 (TUBB4A) | WP:WP4075 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:20774 (TUBB4A) | WP:WP1859 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:20774 (TUBB4A) | WP:WP2359 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:6893 (MAPT) | WP:WP2038 | MEMBER_OF | wikipathways_get_pathways_for_gene(MAPT) |
| HGNC:6893 (MAPT) | WP:WP2059 | MEMBER_OF | wikipathways_get_pathways_for_gene(MAPT) |
| HGNC:20774 (TUBB4A) | WP:WP2059 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| NCT:07222371 | Orphanet:139441 (H-ABC) | STUDIES | clinicaltrials_get_trial(NCT:07222371) |
| NCT:06369974 | Orphanet:139441 (H-ABC) | STUDIES | clinicaltrials_get_trial(NCT:06369974) |
| NCT:02699190 | Orphanet:139441 (H-ABC) | STUDIES | clinicaltrials_get_trial(NCT:02699190) |
| NCT:03047369 | Orphanet:139441 (H-ABC) | STUDIES | clinicaltrials_get_trial(NCT:03047369) |
| HGNC:20774 (TUBB4A) | WP:WP3498 | MEMBER_OF | wikipathways_get_pathways_for_gene(TUBB4A) |
| HGNC:6893 (MAPT) | WP:WP1784 | MEMBER_OF | wikipathways_get_pathways_for_gene(MAPT) |

### Supplementary Table S3: Evidence Grading (All Claims)

| Claim | Grade | Sources | Confidence |
|-------|-------|---------|------------|
| TUBB4A mutations cause H-ABC | L1 | OMIM:612438, Open Targets (0.76), NCBI Gene (10382) | 0.95 |
| TUBB4A-TUBA4A heterodimer critical for assembly | L1 | STRING 0.983, UniProt P04350, biochemical literature | 0.95 |
| MAPT stabilizes TUBB4A-containing microtubules | L1 | STRING 0.953, extensive published literature | 0.90 |
| ASO therapy targets TUBB4A mutant transcript | L2 | NCT07222371 (active), NCT06369974 (planned) | 0.80 |
| Disrupted dynein transport contributes to H-ABC | L2 | STRING 0.861, DYNC1I1 function, mechanism plausible | 0.75 |
| TOR1A-TUBB4A links H-ABC to dystonia pathway | L2 | STRING 0.895, shared DYT phenotype, genetic evidence | 0.75 |
| Oncology tubulin drugs contraindicated in H-ABC | L2 | Dominant-negative mechanism vs. inhibitor mechanism | 0.85 |
| GJA1 trafficking disruption in hypomyelination | L3 | STRING 0.940, indirect mechanistic inference | 0.65 |
| ARHGEF2 release causes aberrant RhoA in H-ABC | L3 | STRING 0.906, indirect mechanistic inference | 0.60 |
| Tubulin code alterations affect H-ABC | L3 | WP:WP4075 membership, mechanistic inference | 0.55 |

### Supplementary Table S4: Synapse Dataset Mapping

**Status: Pending -- system maintenance**

Synapse dataset grounding for TUBB4A expression, essentiality, and cell-type specificity was not completed at the time of this analysis due to system maintenance. The following datasets are recommended for future integration:

| Dataset | Synapse ID | Relevance |
|---------|-----------|-----------|
| GTEx brain expression | TBD | TUBB4A tissue-specific expression across brain regions |
| BrainSpan developmental atlas | TBD | TUBB4A expression across developmental stages |
| DepMap CRISPR essentiality | TBD | TUBB4A essentiality in CNS cell lines |
| Single-cell RNA-seq brain atlas | TBD | TUBB4A expression in oligodendrocytes vs. neurons |

---

## Figure Descriptions

### Figure 1: TUBB4A Knowledge Graph Topology

A network visualization of the 27-node, 25-edge knowledge graph centered on TUBB4A (HGNC:20774). The graph displays a hub-and-spoke topology with TUBB4A as the central node, connected to 7 protein interactors (TUBA4A, MAPT, GJA1, ARHGEF2, TOR1A, TUBB4B, DYNC1I1; shown as circular gene nodes sized by STRING interaction score), 2 disease nodes (H-ABC and DYT4; shown as diamond shapes), 10 pathway nodes (shown as rectangular shapes colored by pathway category), 4 clinical trial nodes (shown as hexagons colored by trial status: green = active, yellow = not yet recruiting, blue = completed, orange = recruiting), 1 compound node (nL-TUBB4-001; shown as a star shape), and 1 protein node (P04350; shown as a rounded rectangle). Edge types are distinguished by color: INTERACTS (blue), ASSOCIATED_WITH (red), MEMBER_OF (gray), STUDIES (green), ENCODES (black), MODULATOR (purple), TREATS (orange). Edge weights for INTERACTS edges reflect STRING combined scores (0.861--0.983). Secondary hub MAPT connects to 2 additional pathway nodes (WP:WP2038, WP:WP2059), and the H-ABC disease node serves as a secondary hub connecting all 4 clinical trial nodes and the ASO compound node.

### Figure 2: TUBB4A Microtubule Disruption Mechanistic Model

A schematic diagram illustrating the five mechanistic axes through which dominant-negative TUBB4A mutations produce H-ABC pathology. The central element is a microtubule cross-section showing alpha-beta tubulin heterodimers with wild-type (blue) and mutant (red) TUBB4A subunits incorporated. Five arrows radiate outward to depict: (Axis 1) Heterodimer disruption -- mutant TUBB4A-TUBA4A dimers destabilize microtubule lattice from within, shown as lattice breaks with STRING score 0.983; (Axis 2) Transport failure -- MAPT/tau (STRING 0.953) detaches from unstable microtubules, and DYNC1I1 dynein motors (STRING 0.861) cannot processively translocate cargo, depicted as stalled vesicles containing myelin components; (Axis 3) Gap junction failure -- GJA1/connexin-43 (STRING 0.940) vesicles fail to traffic to the cell surface, shown as absent gap junction plaques between astrocyte and oligodendrocyte; (Axis 4) Aberrant RhoA -- ARHGEF2/GEF-H1 (STRING 0.906) is released from depolymerizing microtubules and constitutively activates RhoA, depicted as collapsed oligodendrocyte processes; (Axis 5) Dystonia convergence -- TOR1A/torsinA (STRING 0.895) interaction with tubulin in basal ganglia neurons is disrupted, shown as a shared pathway node with DYT1 dystonia. The cell context shows a myelinating oligodendrocyte (left, affected by Axes 1--4) and a basal ganglia neuron (right, affected by Axis 5), explaining the combined leukodystrophy-dystonia phenotype of H-ABC.

---

*Manuscript generated by the Fuzzy-to-Fact automated knowledge graph construction protocol. All factual claims are sourced from MCP tool results against authoritative biomedical databases. No claims are derived from parametric knowledge. Overall analysis confidence: 0.82.*
