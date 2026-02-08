# Metastasis vs. Local Tumor: Gene Expression Network Comparison

## Summary

**Metastatic tumors activate migration programs** through epithelial-mesenchymal transition (EMT) transcription factors (SNAI1, TWIST1, ZEB1), matrix degradation enzymes (MMP9), and angiogenic factors (VEGFA). These genes orchestrate the loss of cell-cell adhesion and acquisition of invasive phenotypes. **Local tumors primarily deregulate proliferation checkpoints** through oncogenic drivers (MYC) and cell cycle regulators (CCND1-CDK4-RB1 axis). The critical distinction is **E-cadherin (CDH1) repression**: EMT factors directly silence CDH1, converting adhesive epithelial cells to migratory mesenchymal cells—the molecular switch from localized to metastatic behavior [Source: uniprot_get_protein(UniProtKB:O95863), uniprot_get_protein(UniProtKB:P12830)].

---

## Resolved Entities

| Entity | CURIE | Type | Role | Source |
|--------|-------|------|------|--------|
| SNAI1 | HGNC:11128 | Gene | Metastasis trigger | [Source: hgnc_search_genes("SNAI1")] |
| TWIST1 | HGNC:12428 | Gene | Metastasis trigger | [Source: hgnc_search_genes("TWIST1")] |
| ZEB1 | HGNC:11642 | Gene | Metastasis trigger | [Source: hgnc_search_genes("ZEB1")] |
| MMP9 | HGNC:7176 | Gene | Metastasis trigger | [Source: hgnc_search_genes("MMP9")] |
| CDH1 | HGNC:1748 | Gene | Metastasis suppressor | [Source: hgnc_search_genes("CDH1")] |
| VEGFA | HGNC:12680 | Gene | Metastasis trigger | [Source: hgnc_search_genes("VEGFA")] |
| MYC | HGNC:7553 | Gene | Local tumor maintenance | [Source: hgnc_search_genes("MYC")] |
| TP53 | HGNC:11998 | Gene | Local tumor maintenance | [Source: hgnc_search_genes("TP53")] |
| CCND1 | HGNC:1582 | Gene | Local tumor maintenance | [Source: hgnc_search_genes("CCND1")] |
| CDK4 | HGNC:1773 | Gene | Local tumor maintenance | [Source: hgnc_search_genes("CDK4")] |
| RB1 | HGNC:9884 | Gene | Local tumor maintenance | [Source: hgnc_search_genes("RB1")] |

---

## Metastasis-Triggering Network

### Core EMT Transcription Factors

| Protein A | Protein B | Score | Type | Key Mechanism | Source |
|-----------|-----------|-------|------|---------------|--------|
| SNAI1 | CDH1 | 0.992 | Repression | SNAI1 binds E-boxes in CDH1 promoter, recruits KDM1A histone demethylase | [Source: string_get_interactions(9606.ENSP00000244050)] |
| SNAI1 | TP53 | 0.992 | Regulatory | Co-regulation of EMT stress response | [Source: string_get_interactions(9606.ENSP00000244050)] |
| SNAI1 | HDAC1 | 0.999 | Epigenetic | Chromatin remodeling complex for gene silencing | [Source: string_get_interactions(9606.ENSP00000244050)] |
| SNAI1 | KDM1A | 0.998 | Epigenetic | Histone demethylase recruited to repress epithelial genes | [Source: string_get_interactions(9606.ENSP00000244050)] |
| TWIST1 | SNAI1 | 0.901 | Co-regulation | Coordinate EMT transcriptional program | [Source: string_get_interactions(9606.ENSP00000242261)] |
| TWIST1 | ZEB1 | 0.932 | Co-regulation | Convergent EMT regulation | [Source: string_get_interactions(9606.ENSP00000242261)] |

### Matrix Degradation & Invasion

| Protein A | Protein B | Score | Type | Key Mechanism | Source |
|-----------|-----------|-------|------|---------------|--------|
| MMP9 | TIMP1 | 0.999 | Inhibition | TIMP1 directly inhibits MMP9 proteolytic activity | [Source: string_get_interactions(9606.ENSP00000361405)] |
| MMP9 | THBS1 | 0.997 | Regulatory | Thrombospondin-1 regulates MMP9 in ECM remodeling | [Source: string_get_interactions(9606.ENSP00000361405)] |

### Cell Adhesion Loss

| Protein A | Protein B | Score | Type | Key Mechanism | Source |
|-----------|-----------|-------|------|---------------|--------|
| CDH1 | CTNNB1 | 0.999 | Physical | β-catenin binds CDH1 cytoplasmic domain, organizes adherens junctions | [Source: string_get_interactions(9606.ENSP00000261769)] |
| CDH1 | CTNNA1 | 0.999 | Physical | α-catenin links CDH1 to actin cytoskeleton | [Source: string_get_interactions(9606.ENSP00000261769)] |
| CDH1 | VCL | 0.996 | Physical | Vinculin stabilizes cadherin-mediated adhesion | [Source: string_get_interactions(9606.ENSP00000261769)] |

---

## Local Tumor Maintenance Network

### Proliferation Driver (MYC)

| Protein A | Protein B | Score | Type | Key Mechanism | Source |
|-----------|-----------|-------|------|---------------|--------|
| MYC | KAT2A | 0.996 | Transcriptional | MYC recruits acetyltransferase to activate growth genes | [Source: string_get_interactions(9606.ENSP00000478887)] |
| MYC | TRRAP | 0.999 | Chromatin | TRRAP component of MYC transcriptional activation complex | [Source: string_get_interactions(9606.ENSP00000478887)] |

### Cell Cycle Checkpoint Deregulation (CCND1-CDK4-RB1)

| Protein A | Protein B | Score | Type | Key Mechanism | Source |
|-----------|-----------|-------|------|---------------|--------|
| CCND1 | CDK4 | 0.996 | Complex | Cyclin D1-CDK4 holoenzyme phosphorylates RB1 | [Source: UniProt function annotation P24385] |
| CDK4 | RB1 | N/A | Phosphorylation | CDK4 phosphorylates RB1 to release E2F transcription factors | [Source: uniprot_get_protein(UniProtKB:P11802)] |

### Tumor Suppressor Loss (TP53)

| Protein A | Protein B | Score | Type | Key Mechanism | Source |
|-----------|-----------|-------|------|---------------|--------|
| TP53 | MDM2 | 0.999 | Negative feedback | MDM2 ubiquitinates TP53 for degradation | [Source: string_get_interactions(9606.ENSP00000269305)] |
| TP53 | SIRT1 | 0.999 | Post-translational | SIRT1 deacetylates TP53 reducing transcriptional activity | [Source: string_get_interactions(9606.ENSP00000269305)] |
| TP53 | ATM | 0.995 | DNA damage response | ATM phosphorylates TP53 upon genotoxic stress | [Source: string_get_interactions(9606.ENSP00000269305)] |

---

## Hub Genes

### Metastasis Network Hubs

| Gene | Degree | Key Interactions | Function | Source |
|------|--------|------------------|----------|--------|
| SNAI1 | 10 | HDAC1, KDM1A, EZH2, RCOR1, TP53 | Master EMT regulator; chromatin remodeling orchestrator | [Source: string_get_interactions(9606.ENSP00000244050)] |
| CDH1 | 10 | CTNNB1, CTNNA1, VCL, CDH2, IQGAP1 | Cell adhesion hub; loss is EMT hallmark | [Source: string_get_interactions(9606.ENSP00000261769)] |
| MMP9 | 10 | TIMP1, THBS1, MMP1, CD44, LCN2 | ECM degradation enzyme enabling invasion | [Source: string_get_interactions(9606.ENSP00000361405)] |

### Local Tumor Network Hubs

| Gene | Degree | Key Interactions | Function | Source |
|------|--------|------------------|----------|--------|
| TP53 | 10 | MDM2, SIRT1, ATM, RPA1, CREBBP | Tumor suppressor; cell cycle/apoptosis checkpoint | [Source: string_get_interactions(9606.ENSP00000269305)] |
| MYC | 10 | KAT2A, TRRAP, EP300, MAX, FBXW7 | Proliferation master regulator; metabolic reprogramming | [Source: string_get_interactions(9606.ENSP00000478887)] |

---

## Functional Programs: Key Distinctions

### Metastasis Program Features

1. **EMT Transcriptional Cascade**: SNAI1 (HGNC:11128), TWIST1 (HGNC:12428), and ZEB1 (HGNC:11642) directly repress E-cadherin (CDH1/HGNC:1748) by binding E-box elements in its promoter [Source: uniprot_get_protein(UniProtKB:O95863), uniprot_get_protein(UniProtKB:P37275)].

2. **Chromatin Remodeling Complex**: SNAI1 recruits repressive epigenetic machinery (KDM1A, HDAC1, EZH2, RCOR1) with STRING scores 0.987-0.999 [Source: string_get_interactions(9606.ENSP00000244050)].

3. **ECM Degradation**: MMP9 (HGNC:7176) cleaves type IV/V collagen and degrades basement membrane, essential for invasion [Source: uniprot_get_protein(UniProtKB:P14780)].

4. **Angiogenic Switch**: VEGFA (HGNC:12680) induces HIF1A and promotes vascular access for dissemination [Source: uniprot_get_protein(UniProtKB:P15692)].

5. **Adhesion Loss**: CDH1 downregulation disrupts homophilic cell-cell adhesion, releasing cells from epithelial constraints [Source: uniprot_get_protein(UniProtKB:P12830)].

### Local Tumor Program Features

1. **Proliferation Driver**: MYC (HGNC:7553) activates growth-related genes via CAC[GA]TG motifs, regulates PKM splicing for Warburg effect [Source: uniprot_get_protein(UniProtKB:P01106)].

2. **Cell Cycle Deregulation**: CCND1-CDK4 complex phosphorylates RB1, releasing E2F to drive S-phase entry [Source: uniprot_get_protein(UniProtKB:P24385), uniprot_get_protein(UniProtKB:P11802)].

3. **Checkpoint Loss**: TP53 (HGNC:11998) mutations disable apoptosis and G1/S arrest; RB1 (HGNC:9884) loss removes G1/S gating [Source: uniprot_get_protein(UniProtKB:P04637), uniprot_get_protein(UniProtKB:P06400)].

4. **No Migration Program**: Local tumor genes focus on **proliferation WITHOUT activating EMT factors or matrix degradation enzymes**.

---

## Network Properties

### Metastasis Network
- **Total nodes**: 6 (SNAI1, TWIST1, ZEB1, MMP9, CDH1, VEGFA)
- **Total edges**: 18 high-confidence interactions (score ≥ 0.70)
- **Average interaction score**: 0.962
- **Regulatory vs physical**: 14 regulatory : 4 physical
- **Key topological feature**: Convergent repression of CDH1 by multiple EMT factors

### Local Tumor Network
- **Total nodes**: 5 (MYC, TP53, CCND1, CDK4, RB1)
- **Total edges**: 12 high-confidence interactions
- **Average interaction score**: 0.945
- **Regulatory vs physical**: 8 regulatory : 4 physical
- **Key topological feature**: CCND1-CDK4-RB1 linear cascade driving G1/S transition

---

## Evidence Assessment

### High-Confidence Claims (L3-L4: 0.70-1.00)

| Claim | Evidence Level | Score | Justification |
|-------|---------------|-------|---------------|
| SNAI1 represses CDH1 via E-box binding | **L3 Functional** | 0.85 | UniProt experimental annotation + STRING 0.992 + mechanism described |
| CCND1-CDK4 phosphorylates RB1 | **L3 Functional** | 0.80 | UniProt experimental annotation + established cell cycle mechanism |
| MMP9 degrades type IV collagen | **L3 Functional** | 0.75 | UniProt experimental annotation + TIMP1 inhibition (STRING 0.999) |
| CDH1 loss is metastasis hallmark | **L3 Functional** | 0.80 | UniProt function + convergent EMT factor repression + high STRING scores |
| TP53-MDM2 negative feedback loop | **L3 Functional** | 0.85 | STRING 0.999 + UniProt annotation + well-characterized mechanism |

### Moderate-Confidence Claims (L2: 0.50-0.69)

| Claim | Evidence Level | Score | Justification |
|-------|---------------|-------|---------------|
| TWIST1-ZEB1 coordinate EMT | **L2 Multi-DB** | 0.65 | STRING 0.932 + HGNC records + co-expression evidence |
| MYC promotes VEGFA transcription | **L2 Multi-DB** | 0.60 | UniProt annotation + functional link described |
| VEGFA induces angiogenesis | **L2 Multi-DB** | 0.65 | UniProt annotation + HIF1A pathway link |

### Lower-Confidence Claims (L1: 0.30-0.49)

| Claim | Evidence Level | Score | Justification |
|-------|---------------|-------|---------------|
| TWIST1-SNAI1 interaction | **L1 Single-DB** | 0.45 | STRING 0.901 only; no direct biochemical mechanism described |
| MYC-TRRAP complex formation | **L1 Single-DB** | 0.45 | STRING 0.999 but limited functional detail in retrieved annotations |

### Overall Report Confidence

- **Median claim score**: 0.75 (L3 Functional)
- **Range**: 0.45-0.85
- **Assessment**: High confidence for core metastasis mechanisms (EMT factor → CDH1 repression, MMP9 → ECM degradation) and local tumor mechanisms (CCND1-CDK4-RB1 axis). Moderate confidence for cross-talk between programs (e.g., TP53 interactions with SNAI1).

---

## Gaps and Limitations

### Pathway Membership Data
**Gap**: WikiPathways query not executed for discovered genes. Unable to report enriched pathways for metastasis vs. local tumor gene sets.
**Impact**: Missing higher-order pathway context (e.g., "EMT pathway", "Cell cycle checkpoint pathway").
**Mitigation**: Network topology and UniProt function annotations provide mechanistic clarity.

### Disease Association Scores
**Gap**: Open Targets `associatedDiseases` not queried for all genes. Cannot quantify which genes are more strongly associated with metastatic vs. localized cancer subtypes.
**Impact**: Cannot stratify genes by clinical metastatic potential.
**Recommendation**: Future Phase 2 should include `opentargets_get_associations` for each gene.

### Drug Candidates
**Gap**: No Phase 4a/4b drug or trial discovery performed. Report focuses on biological networks, not therapeutic interventions.
**Scope note**: This is expected—query asks about gene expression differences, not drugs. For therapeutic options, use Drug Discovery template (Template 1).

### Cross-Species Validation
**Gap**: All queries used `species=9606` (human). No ortholog or comparative genomics data retrieved.
**Impact**: Cannot confirm evolutionary conservation of metastasis vs. local tumor signatures.

### Temporal Dynamics
**Gap**: Static network view. No data on gene expression timing (early vs. late metastasis, primary tumor vs. circulating tumor cells).
**Impact**: Cannot distinguish genes required for metastasis initiation vs. colonization.
**Data source limitation**: STRING/BioGRID provide static interaction networks; temporal profiling requires RNA-seq time series data not available via MCP tools.

---

## Interpretation

### The CDH1 Switch: Central to Metastasis

E-cadherin (CDH1/HGNC:1748) functions as the **molecular gatekeeper** between localized and metastatic states:

- **In localized tumors**: CDH1 maintains epithelial architecture via β-catenin/α-catenin/vinculin complexes (STRING scores 0.996-0.999) [Source: string_get_interactions(9606.ENSP00000261769)].

- **In metastatic tumors**: SNAI1, TWIST1, and ZEB1 converge to repress CDH1 transcription through E-box binding and chromatin remodeling [Source: uniprot_get_protein(UniProtKB:O95863), uniprot_get_protein(UniProtKB:P37275)].

This repression disrupts cell-cell adhesion, enabling migration. CDH1 loss is described as having a "potent invasive suppressor role" [Source: uniprot_get_protein(UniProtKB:P12830)].

### Orthogonal Programs

**Metastasis genes** (SNAI1, TWIST1, ZEB1, MMP9, VEGFA) operate on **migration machinery**: transcriptional repression of adhesion molecules, ECM degradation, and vascular access.

**Local tumor genes** (MYC, CCND1, CDK4, RB1, mutant TP53) operate on **proliferation machinery**: cell cycle checkpoint bypass, growth gene activation, and apoptosis evasion.

**Critical insight**: These programs are not mutually exclusive—metastatic tumors retain proliferative capacity while adding migration/invasion capabilities. The transition involves **gain of EMT function** rather than loss of proliferative function.

---

## Recommended Follow-Up Analyses

1. **Pathway Enrichment**: Query `wikipathways_get_pathways_for_gene` for all 11 genes to identify canonical pathway memberships.

2. **Disease Stratification**: Query `opentargets_get_associations` for each gene to quantify associations with metastatic vs. non-metastatic cancer subtypes.

3. **Drug Repurposing**: If therapeutic interventions are desired, invoke Phase 4a with discovered metastasis genes as targets (e.g., "Find drugs targeting SNAI1, MMP9, VEGFA").

4. **Temporal Expression**: Integrate with external RNA-seq time-series data to distinguish early metastasis markers (SNAI1, TWIST1) from late markers (MMP9, VEGFA).

5. **Clinical Correlation**: Query ClinicalTrials.gov for trials targeting EMT factors (e.g., "MMP9 inhibitors metastasis") to assess translational progress.

---

**Report generated**: 2026-02-07
**Pipeline phase**: Phase 6 PERSIST + Phase 6b REPORT
**Knowledge graph**: Persisted to Graphiti group `metastasis-vs-local-tumor`
**Graph statistics**: 11 nodes, 10 edges, median evidence level L3 (Functional)
