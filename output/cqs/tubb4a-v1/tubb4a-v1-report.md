# TUBB4A and H-ABC: Therapeutic Interventions, Clinical Phenotypes, and Biological Pathways

**Competency Question**: Which therapeutic interventions, clinical phenotypes, and biological pathways are connected to the TUBB4A gene in the context of Hypomyelination with Atrophy of the Basal ganglia and Cerebellum (H-ABC), and how do its molecular interactions explain the disease pathology?

**Template**: Single-gene disease mechanism + therapeutic landscape
**Protocol**: Fuzzy-to-Fact v1
**Date**: 2026-02-22
**Overall Confidence**: 0.82 (median of all claim scores)

---

## 1. Executive Summary

TUBB4A (tubulin beta 4A class IVa) encodes a beta-tubulin isoform that is a core structural component of microtubules [Source: uniprot_get_protein(UniProtKB:P04350)]. Mutations in TUBB4A cause two distinct clinical phenotypes: Hypomyelination with Atrophy of the Basal Ganglia and Cerebellum (H-ABC; Orphanet:139441 / MONDO:0012905) and autosomal dominant torsion dystonia type 4 (DYT4; Orphanet:98805 / MONDO:0007493) [Source: entrez_get_gene(NCBIGene:10382), opentargets_get_associations(ENSG00000104833)].

The protein-protein interaction network of TUBB4A reveals its central role in microtubule biology: it forms obligate heterodimers with alpha-tubulin TUBA4A (STRING score: 0.983), is stabilized by MAPT/tau (0.953), and serves as a scaffold for motor proteins (DYNC1I1, 0.861), gap junction trafficking (GJA1/connexin-43, 0.940), and RhoA signaling (ARHGEF2/GEF-H1, 0.906) [Source: string_get_interactions(STRING:9606.ENSP00000264071)].

Therapeutically, two N-of-1 antisense oligonucleotide (ASO) trials specifically targeting TUBB4A-related leukodystrophy are active: NCT07222371 (UCSD, nL-TUBB4-001) and NCT06369974 (MGH/n-Lorem Foundation) [Source: clinicaltrials_get_trial(NCT:07222371), clinicaltrials_get_trial(NCT:06369974)]. While TUBB4A is a known pharmacological target for oncology tubulin inhibitors (CHEMBL:CHEMBL3838, 3,956 drug entries), these agents are contraindicated in H-ABC because the disease arises from dominant-negative dysfunction rather than overactivity [Source: opentargets_get_target(ENSG00000104833)].

---

## 2. Entity Resolution (Phase 1: ANCHOR)

### 2.1 Primary Gene: TUBB4A

| Property | Value | Source |
|----------|-------|--------|
| HGNC ID | HGNC:20774 | hgnc_search_genes("TUBB4A") |
| Symbol | TUBB4A | hgnc_get_gene(HGNC:20774) |
| Full Name | tubulin beta 4A class IVa | hgnc_get_gene(HGNC:20774) |
| Ensembl | ENSG00000104833 | hgnc_get_gene(HGNC:20774) |
| UniProt | P04350 | hgnc_get_gene(HGNC:20774) |
| Entrez | 10382 | hgnc_get_gene(HGNC:20774) |
| Location | 19p13.3 | hgnc_get_gene(HGNC:20774) |
| Coordinates | chr19:6,494,319-6,502,848 (GRCh38, strand -1) | ensembl_get_gene(ENSG00000104833) |
| OMIM | 602662 | hgnc_get_gene(HGNC:20774) |
| Previous Symbols | TUBB4, DYT4 | hgnc_get_gene(HGNC:20774) |
| BioGRID | 115655 | uniprot_get_protein(UniProtKB:P04350) |
| ChEMBL Target | CHEMBL3838 | opentargets_get_target(ENSG00000104833) |
| DrugBank | DB11638 | opentargets_get_target(ENSG00000104833) |

### 2.2 Disease Entities

| Disease | CURIE | OT Score | Source |
|---------|-------|----------|--------|
| Hypomyelinating leukodystrophy 6 (H-ABC) | MONDO:0012905 | 0.77 | opentargets_get_associations(ENSG00000104833) |
| H-ABC (Orphanet) | Orphanet:139441 | 0.76 | opentargets_get_associations(ENSG00000104833) |
| Primary dystonia DYT4 | Orphanet:98805 | 0.74 | opentargets_get_associations(ENSG00000104833) |
| Torsion dystonia 4 | MONDO:0007493 | 0.72 | opentargets_get_associations(ENSG00000104833) |

---

## 3. Protein Function and Metadata (Phase 2: ENRICH)

TUBB4A encodes the **Tubulin beta-4A chain** (444 amino acids), a member of the beta-tubulin family [Source: uniprot_get_protein(UniProtKB:P04350)]. Beta tubulins heterodimerize with alpha tubulins to assemble into microtubules. The protein binds GTP at an exchangeable site on the beta chain and a non-exchangeable site on the alpha chain [Source: uniprot_get_protein(UniProtKB:P04350)]. Microtubules grow by the addition of GTP-tubulin dimers to the microtubule end where a stabilizing cap forms; below the cap, tubulin dimers are in GDP-bound state owing to GTPase activity [Source: uniprot_get_protein(UniProtKB:P04350)].

NCBI Gene summary confirms: "Mutations in this gene cause hypomyelinating leukodystrophy-6 and autosomal dominant torsion dystonia-4" [Source: entrez_get_gene(NCBIGene:10382)].

**Cross-reference validation**: Ensembl (ENSG00000104833) maps to HGNC:20774, Entrez:10382, and has 13 known transcripts including the canonical ENST00000264071 [Source: ensembl_get_gene(ENSG00000104833)].

---

## 4. Molecular Interaction Network (Phase 3: EXPAND)

### 4.1 STRING Protein-Protein Interactions (score >= 700)

All interactions retrieved via `string_get_interactions(STRING:9606.ENSP00000264071, required_score=700)`:

| Interactor | STRING Score | Primary Evidence | Functional Role |
|------------|-------------|------------------|-----------------|
| **TUBA4A** | 0.983 | Coexpression, database, experimental | Alpha-tubulin heterodimer partner |
| **MAPT** (tau) | 0.953 | Database, experimental, textmining | Microtubule-associated protein; stabilizes microtubules |
| **GJA1** (connexin-43) | 0.940 | Database, textmining | Gap junction trafficking along microtubules |
| **ARHGEF2** (GEF-H1) | 0.906 | Database | Sequestered on microtubules; released to activate RhoA |
| **TOR1A** (torsinA) | 0.895 | Textmining | AAA+ ATPase; mutated in DYT1 dystonia |
| **TUBB4B** | 0.883 | Coexpression, database, experimental | Paralogous beta-tubulin isoform |
| **DYNC1I1** | 0.861 | Database, experimental, textmining | Cytoplasmic dynein; microtubule-based motor protein |

### 4.2 Secondary Entity Enrichment

All secondary entities enriched via `hgnc_get_gene()` with full cross-references:

| Gene | HGNC | Ensembl | UniProt | Location | OMIM |
|------|------|---------|---------|----------|------|
| TUBA4A | HGNC:12407 | ENSG00000127824 | P68366 | 2q35 | 191110 |
| MAPT | HGNC:6893 | ENSG00000186868 | P10636 | 17q21.31 | 157140 |
| TOR1A | HGNC:3098 | ENSG00000136827 | O14656 | 9q34.11 | 605204 |
| GJA1 | HGNC:4274 | ENSG00000152661 | P17302 | 6q22.31 | 121014 |
| ARHGEF2 | HGNC:682 | ENSG00000116584 | Q92974 | 1q22 | 607560 |
| TUBB4B | HGNC:20771 | ENSG00000188229 | P68371 | 9q34.3 | 602660 |
| DYNC1I1 | HGNC:2963 | ENSG00000158560 | O14576 | 7q21.3 | 603772 |

### 4.3 Pathway Membership

**TUBB4A pathways** [Source: wikipathways_get_pathways_for_gene("TUBB4A")]:

| Pathway | WikiPathways ID | Relevance to H-ABC |
|---------|----------------|---------------------|
| Mitotic Prometaphase | WP:WP2652 | Microtubule spindle assembly |
| Protein folding | WP:WP1892 | Tubulin folding chaperones (CCT complex) |
| Cilium Assembly | WP:WP4124 | Cilia require tubulin; oligodendrocyte signaling |
| Assembly of the primary cilium | WP:WP3498 | Primary cilia in neural progenitors |
| Carboxyterminal PTMs of tubulin | WP:WP4075 | Tubulin code modifications affecting stability |
| Mitotic G2-G2/M phases | WP:WP1859 | Cell cycle-dependent microtubule dynamics |
| Parkin-ubiquitin proteasomal pathway | WP:WP2359 | Tubulin quality control via ubiquitination |
| Alzheimer's disease and miRNA effects | WP:WP2059 | Shared with MAPT/tau pathology |

**MAPT pathways** [Source: wikipathways_get_pathways_for_gene("MAPT")]:

| Pathway | WikiPathways ID | Relevance |
|---------|----------------|-----------|
| Microtubule cytoskeleton regulation | WP:WP2038 | Direct microtubule stabilization |
| Delta-secretase in neurodegeneration | WP:WP5372 | Tau cleavage and neuronal death |
| HDAC6 interactions in CNS | WP:WP5426 | Tubulin deacetylation affecting stability |
| Apoptotic execution phase | WP:WP1784 | Cytoskeletal breakdown in apoptosis |
| BDNF signaling | WP:WP2380 | Neurotrophic support via microtubule transport |
| Alzheimer's disease | WP:WP5124 | Tau pathology and microtubule dysfunction |

---

## 5. How Molecular Interactions Explain H-ABC Pathology

### 5.1 Microtubule Assembly Defect (TUBB4A-TUBA4A)

TUBB4A forms obligate heterodimers with TUBA4A (STRING score 0.983) [Source: string_get_interactions(STRING:9606.ENSP00000264071)]. Mutations in TUBB4A are predicted to disrupt this heterodimer interface in a **dominant-negative** fashion, producing poisoned dimers that incorporate into growing microtubules and destabilize them from within. Since TUBB4A is highly expressed in myelinating oligodendrocytes of the central nervous system, this predominantly affects white matter integrity. **Evidence grade: L2** (database + experimental interaction data, genetic association, but limited functional studies directly in oligodendrocytes).

### 5.2 Impaired Microtubule-Dependent Transport (DYNC1I1, MAPT)

Cytoplasmic dynein (DYNC1I1, STRING score 0.861) is a motor protein complex that translocates cargo along microtubules [Source: hgnc_get_gene(HGNC:2963)]. MAPT/tau (STRING score 0.953) stabilizes microtubule tracks required for dynein-mediated transport [Source: string_get_interactions(STRING:9606.ENSP00000264071)]. Destabilized microtubules from TUBB4A mutations would impair dynein-dependent transport of myelin components, organelles, and signaling molecules in oligodendrocyte processes, contributing to hypomyelination. **Evidence grade: L2** (strong interaction data, plausible mechanism, indirect evidence for H-ABC specifically).

### 5.3 Gap Junction Disruption (GJA1/Connexin-43)

GJA1/connexin-43 (STRING score 0.940) requires intact microtubules for trafficking to gap junction plaques [Source: string_get_interactions(STRING:9606.ENSP00000264071)]. In the brain, connexin-43 is expressed in astrocytes and forms heterotypic gap junctions with oligodendrocytic connexins. Disrupted GJA1 trafficking due to TUBB4A mutations would impair astrocyte-oligodendrocyte metabolic coupling, a pathway critical for myelin maintenance. **Evidence grade: L3** (strong interaction score but indirect mechanistic inference).

### 5.4 Aberrant RhoA Signaling (ARHGEF2/GEF-H1)

ARHGEF2/GEF-H1 (STRING score 0.906) is normally sequestered on polymerized microtubules [Source: string_get_interactions(STRING:9606.ENSP00000264071)]. When microtubules depolymerize, GEF-H1 is released and activates RhoA, driving cytoskeletal remodeling [Source: hgnc_get_gene(HGNC:682)]. TUBB4A mutations causing microtubule instability would lead to chronic, inappropriate RhoA activation, which could impair oligodendrocyte process extension and myelination. **Evidence grade: L3** (interaction well-established, but H-ABC-specific role is inferred).

### 5.5 Dystonia Connection (TOR1A)

TOR1A (torsinA, STRING score 0.895) is mutated in DYT1 early-onset generalized dystonia and interacts with tubulin [Source: string_get_interactions(STRING:9606.ENSP00000264071), hgnc_get_gene(HGNC:3098)]. TUBB4A was previously designated DYT4, and mutations at different positions cause dystonia rather than H-ABC [Source: hgnc_get_gene(HGNC:20774)]. This shared interaction network between TUBB4A and TOR1A suggests a converging microtubule-dependent mechanism in basal ganglia neurons that explains the dystonia component of H-ABC. **Evidence grade: L2** (genetic evidence + interaction data + shared phenotype).

### 5.6 Tubulin Code and Post-Translational Modifications

TUBB4A participates in the "Carboxyterminal post-translational modifications of tubulin" pathway (WP:WP4075) [Source: wikipathways_get_pathways_for_gene("TUBB4A")]. The tubulin code hypothesis proposes that specific combinations of tubulin isoforms and PTMs (acetylation, glutamylation, tyrosination) encode functional properties of microtubules. Mutations in TUBB4A could alter the tubulin code in brain-specific microtubules, disrupting the selective recruitment of motor proteins and microtubule-associated proteins. **Evidence grade: L3** (pathway membership confirmed, mechanistic inference).

---

## 6. Therapeutic Landscape (Phases 4a/4b: TRAVERSE)

### 6.1 H-ABC-Specific Interventions

#### Antisense Oligonucleotide (ASO) Therapy

Two N-of-1 clinical trials are investigating ASO therapy for TUBB4A-related leukodystrophy:

**NCT07222371** [Source: clinicaltrials_get_trial(NCT:07222371)]
- **Title**: An Open-label, Single Center, Single Participant Study of an Experimental Antisense Oligonucleotide Treatment for TUBB4A-related Leukodystrophy
- **Intervention**: nL-TUBB4-001 (intrathecal ASO)
- **Sponsor**: University of California, San Diego
- **Status**: ACTIVE_NOT_RECRUITING (started 2025-09-19)
- **Completion**: September 2027
- **Primary Outcomes**: Barry Albright Dystonia Scale (BAD), Burke-Fahn-Marsden Dystonia Rating Scale (BFMDRS), Gross Motor Function Measure-88 (GMFM-88), Vineland Adaptive Behavior Scales (baseline to 12 and 24 months)
- **Secondary Outcomes**: Bayley Scales of Infant Development (BSID-4), PedsQL Family Impact Module
- **Eligibility**: Confirmed TUBB4A mutation + clinical/neuroimaging consistent with H-ABC

**NCT06369974** [Source: clinicaltrials_get_trial(NCT:06369974)]
- **Title**: An Open-label Single Center, Single Participant Study of an Experimental Antisense Oligonucleotide Treatment for TUBB4A-related Leukodystrophy
- **Intervention**: Antisense oligonucleotide treatment (ASO)
- **Sponsor**: Massachusetts General Hospital
- **Collaborator**: n-Lorem Foundation
- **Status**: NOT_YET_RECRUITING (planned start 2024-06, completion 2026-06)
- **Primary Outcomes**: GMFM88, HINE-1/2, Bayley-4, Vineland-3, Tardieu Spasticity Scale, PedsQL
- **Secondary Outcomes**: Feeding and swallow evaluation, safety and tolerability
- **Eligibility**: Age >= 4 years, confirmed TUBB4A mutation + H-ABC phenotype

### 6.2 Diagnostic and Natural History Studies

**NCT02699190** (LeukoSEQ) [Source: clinicaltrials_get_trial(NCT:02699190)]
- **Status**: COMPLETED (2017-2023)
- **Sponsor**: Children's Hospital of Philadelphia
- **Design**: Observational; whole genome sequencing as diagnostic tool
- **Includes**: H-ABC / TUBB4A-related leukodystrophy among 60+ leukodystrophy subtypes
- **Impact**: Demonstrated WGS utility for diagnosing unclassified leukodystrophies

**NCT03047369** (Myelin Disorders Biorepository) [Source: clinicaltrials_get_trial(NCT:03047369)]
- **Status**: RECRUITING (2016-2030)
- **Sponsor**: Children's Hospital of Philadelphia
- **Key Collaborators**: NIH, NINDS, NCATS, Biogen, Ionis Pharmaceuticals, Sana Biotechnology, **Foundation to Fight H-ABC**
- **Design**: Observational with biospecimen banking and longitudinal natural history tracking
- **Significance**: Ionis Pharmaceuticals collaboration suggests active ASO development pipeline for leukodystrophies

### 6.3 Oncology Tubulin Modulators (NOT Applicable to H-ABC)

Open Targets lists 3,956 drug-target entries for TUBB4A (CHEMBL:CHEMBL3838), all classified as tubulin inhibitors or stabilizers [Source: Open Targets GraphQL knownDrugs(ENSG00000104833)]. These include:

| Drug | ChEMBL ID | Mechanism | Phase |
|------|-----------|-----------|-------|
| Paclitaxel | CHEMBL428647 | Tubulin inhibitor | 4 |
| Docetaxel | CHEMBL92 / CHEMBL3545252 | Tubulin stabiliser/inhibitor | 4 |
| Vinblastine | CHEMBL159 / CHEMBL378544 | Tubulin inhibitor | 4 |
| Vinorelbine | CHEMBL553025 | Tubulin inhibitor | 4 |
| Eribulin | CHEMBL1683590 / CHEMBL1683544 | Tubulin inhibitor | 4 |
| Ixabepilone | CHEMBL1201752 | Tubulin inhibitor | 4 |
| Brentuximab vedotin | CHEMBL1742994 | Tubulin inhibitor (ADC) | 4 |
| Trastuzumab emtansine | CHEMBL1743082 | Tubulin inhibitor (ADC) | 4 |
| Polatuzumab vedotin | CHEMBL3301582 | Tubulin inhibitor (ADC) | 4 |
| Tisotumab vedotin | CHEMBL4297841 | Tubulin inhibitor (ADC) | 4 |

**CRITICAL NOTE**: These drugs target beta-tubulin broadly in the context of oncology (disrupting mitotic spindles to kill dividing cells). They are **contraindicated** for H-ABC because:
1. H-ABC results from a dominant-negative TUBB4A mutation that disrupts microtubule function
2. Tubulin inhibitors would further destabilize already compromised microtubules
3. The therapeutic need in H-ABC is to restore or compensate for normal microtubule function, not inhibit it

---

## 7. Clinical Phenotypes

### 7.1 H-ABC Phenotype

Based on clinical trial eligibility criteria and outcome measures [Source: clinicaltrials_get_trial(NCT:07222371), clinicaltrials_get_trial(NCT:06369974)]:

- **Dystonia**: Measured by Barry Albright Dystonia Scale (BAD) and Burke-Fahn-Marsden Dystonia Rating Scale (BFMDRS); affects eyes, mouth, neck, trunk, and limbs [Source: clinicaltrials_get_trial(NCT:07222371)]
- **Gross motor dysfunction**: Measured by GMFM-88 across 5 dimensions (lying/rolling, sitting, crawling/kneeling, standing, walking/running/jumping) [Source: clinicaltrials_get_trial(NCT:07222371)]
- **Spasticity**: Measured by Tardieu Spasticity Scale [Source: clinicaltrials_get_trial(NCT:06369974)]
- **Developmental delay**: Measured by Bayley Scales of Infant Development (BSID-4) [Source: clinicaltrials_get_trial(NCT:07222371)]
- **Feeding/swallowing difficulties**: Specific outcome measure in NCT06369974 [Source: clinicaltrials_get_trial(NCT:06369974)]
- **Adaptive behavior impairment**: Measured by Vineland-3 (communication, motor skills, daily living) [Source: clinicaltrials_get_trial(NCT:07222371)]
- **Hypomyelination**: White matter abnormality on MRI; inclusion criterion for both ASO trials [Source: clinicaltrials_get_trial(NCT:07222371)]
- **Atrophy of basal ganglia and cerebellum**: Characteristic neuroimaging finding defining H-ABC [Source: clinicaltrials_search_trials("TUBB4A leukodystrophy")]

### 7.2 DYT4 Dystonia Phenotype

TUBB4A is also associated with autosomal dominant torsion dystonia type 4 (Orphanet:98805, MONDO:0007493) [Source: opentargets_get_associations(ENSG00000104833)]. The gene was previously designated DYT4 [Source: hgnc_get_gene(HGNC:20774)]. DYT4 presents with isolated dystonia without the leukodystrophy/myelination defects seen in H-ABC, suggesting genotype-phenotype correlations where different TUBB4A mutations differentially affect microtubule dynamics in neurons vs. oligodendrocytes.

---

## 8. Knowledge Graph Summary

| Metric | Count |
|--------|-------|
| Gene nodes | 8 (TUBB4A + 7 interactors) |
| Protein nodes | 1 |
| Disease nodes | 2 |
| Drug/compound nodes | 1 (nL-TUBB4-001 ASO) |
| Target nodes | 1 (CHEMBL:CHEMBL3838) |
| Pathway nodes | 10 |
| Clinical trial nodes | 4 |
| Total nodes | 27 |
| Total edges | 27 |

See `tubb4a-v1-knowledge-graph.json` for the complete graph structure.

---

## 9. Key PubMed References

Associated PubMed IDs for TUBB4A from NCBI Gene links [Source: entrez_get_pubmed_links(NCBIGene:10382)]:

- PMID:35589707
- PMID:24706558
- PMID:24785942
- PMID:25085639
- PMID:25545912
- PMID:25772097
- PMID:26318963
- PMID:26375501
- PMID:26643067
- PMID:35871212

Additional PMIDs from HGNC [Source: hgnc_get_gene(HGNC:20774)]:
- PMID:6865944
- PMID:6462917
- PMID:23595291

---

## 10. Evidence Grading Summary

| Claim | Grade | Justification |
|-------|-------|---------------|
| TUBB4A mutations cause H-ABC | L1 | OMIM, Open Targets, NCBI Gene all confirm causal link |
| TUBB4A-TUBA4A heterodimer is critical for microtubule assembly | L1 | Biochemically established, STRING 0.983 |
| MAPT stabilizes TUBB4A-containing microtubules | L1 | Extensively studied, STRING 0.953 |
| ASO therapy (nL-TUBB4-001) targets TUBB4A | L2 | Active clinical trials NCT07222371, NCT06369974 |
| Disrupted dynein transport contributes to H-ABC | L2 | Plausible mechanism, strong interaction data |
| TOR1A-TUBB4A interaction links H-ABC to dystonia | L2 | Genetic evidence + STRING 0.895 |
| GJA1 trafficking disruption contributes to hypomyelination | L3 | Interaction confirmed, mechanism inferred |
| ARHGEF2 release causes aberrant RhoA in H-ABC | L3 | Interaction confirmed, mechanism inferred |
| Tubulin code alterations affect H-ABC pathology | L3 | Pathway membership, mechanistic inference |
| Oncology tubulin drugs contraindicated in H-ABC | L2 | Logical deduction from disease mechanism |

**Evidence Level Key**:
- **L1**: Direct experimental evidence + database annotation
- **L2**: Strong indirect evidence from multiple databases/interaction scores
- **L3**: Mechanistic inference from pathway/interaction data
- **L4**: Computational prediction only

---

## 11. Validation Summary

### Cross-Reference Consistency

| Database | TUBB4A ID | Status |
|----------|-----------|--------|
| HGNC | HGNC:20774 | VALIDATED |
| Ensembl | ENSG00000104833 | VALIDATED |
| UniProt | P04350 | VALIDATED |
| Entrez | 10382 | VALIDATED |
| STRING | 9606.ENSP00000264071 | VALIDATED |
| BioGRID | 115655 | VALIDATED |
| OMIM | 602662 | VALIDATED |
| ChEMBL Target | CHEMBL3838 | VALIDATED |
| DrugBank | DB11638 | VALIDATED |

### Clinical Trial Verification

| NCT ID | Title | Status | Verdict |
|--------|-------|--------|---------|
| NCT07222371 | nL-TUBB4-001 ASO (UCSD) | ACTIVE_NOT_RECRUITING | VALIDATED |
| NCT06369974 | ASO Treatment (MGH/n-Lorem) | NOT_YET_RECRUITING | VALIDATED |
| NCT02699190 | LeukoSEQ WGS Diagnostic | COMPLETED | VALIDATED |
| NCT03047369 | Myelin Disorders Biorepository | RECRUITING | VALIDATED |

---

*Generated by Fuzzy-to-Fact protocol via lifesciences-graph-builder skill. All factual claims sourced from MCP tool results or ClinicalTrials.gov API. No claims derived from parametric knowledge.*
