# Synthetic Lethality Validation Methods (2026)

Research reference for validating synthetic lethal (SL) gene pairs in the context of the Fuzzy-to-Fact pipeline and knowledge graph construction.

## Overview

Synthetic lethality occurs when simultaneous loss of two genes causes cell death, while loss of either alone is tolerated. This principle enables targeted cancer therapy: if a tumor already has one gene mutated (e.g., TP53), inhibiting its SL partner selectively kills cancer cells while sparing normal tissue.

Validation of SL pairs requires computational screening, experimental confirmation, and clinical translation assessment. This document catalogs the methods available for each stage.

---

## 1. Computational Methods

### 1.1 BioGRID ORCS (Open Repository of CRISPR Screens)

- **URL**: https://orcs.thebiogrid.org
- **Coverage**: 1,800+ genome-wide CRISPR/RNAi screens across 900+ cell lines
- **Query pattern**: Gene symbol or Entrez ID -> essentiality scores per screen
- **MCP access**: `biogrid_search_genes`, `biogrid_get_interactions`
- **Direct API**: `curl "https://orcsws.thebiogrid.org/gene/{ENTREZ_ID}"`

**Interpretation**:
- A gene is "essential" in a screen if its knockout significantly reduces cell fitness
- SL validation: Gene B is essential specifically in screens where Gene A is already mutated
- Look for differential essentiality: high fitness effect in mutant background, low in wild-type

**Limitations**:
- Screen quality varies; some cell lines have complex genotypes
- Context-dependent essentiality can produce false positives
- Not all gene pairs have been tested in appropriate mutant backgrounds

### 1.2 DepMap (Cancer Dependency Map)

- **Source**: Broad Institute (https://depmap.org)
- **Data**: CRISPR (Chronos) and RNAi (DEMETER2) dependency scores
- **Format**: Gene x Cell Line matrices with dependency probability scores
- **Access**: Bulk download CSV; no real-time API in current pipeline

**Key metrics**:
- **CERES score** (legacy): negative = essential; < -0.5 common threshold
- **Chronos score** (current): similar interpretation to CERES but improved algorithm
- **Dependency probability**: 0-1 scale; > 0.5 indicates likely dependency

**SL validation workflow**:
1. Identify cell lines with Gene A mutation (from CCLE annotations)
2. Compare Gene B dependency scores in mutant vs wild-type lines
3. Significant difference indicates potential SL relationship
4. Validate with multiple cell lines from same cancer type

### 1.3 Machine Learning Prediction

**Established approaches**:
- **SynLethDB** (https://synlethdb.sickkids.ca): Curated SL pairs from literature + screens
- **ISLE (In-Silico Lethality Estimation)**: Uses TCGA survival + copy number + mutation data
- **BioPathNet**: Graph neural network on biological pathways for link prediction

**Emerging approaches (2025-2026)**:
- **Temporal knowledge graphs**: Track how SL predictions change with new screen data
- **Multi-modal integration**: Combine CRISPR screens + transcriptomics + drug sensitivity
- **Foundation models**: Protein language models (ESM-2, ProtTrans) for functional similarity scoring

**Reliability hierarchy**:
1. Direct experimental validation (CRISPR screen in correct background) - highest
2. Multi-study computational concordance (3+ databases agree) - high
3. Single computational prediction with biological rationale - moderate
4. ML prediction without experimental support - low

---

## 2. Experimental Validation

### 2.1 CRISPR Knockout Screens

**Gold standard**: Genome-wide CRISPR-Cas9 screen in isogenic cell line pair (Gene A mutant vs wild-type).

**Screen types**:
- **Negative selection (dropout)**: Identify genes whose loss reduces fitness in mutant background
- **Positive selection (enrichment)**: Identify genes whose loss confers resistance
- **Combinatorial CRISPR**: Dual-guide libraries targeting gene pairs simultaneously

**Key datasets**:
- Project Achilles (Broad): 1,000+ cell lines screened
- Sanger DepMap: Independent validation with different library design
- Published focused screens: Gene-specific screens in mutant backgrounds

**Quality indicators**:
- Screen quality metrics: NNMD (null-normalized mean difference), precision-recall
- Replication across cell lines from same cancer type
- Concordance between CRISPR and RNAi approaches

### 2.2 Drug Combination Assays

**Purpose**: Test whether pharmacological inhibition of SL partner kills Gene A-mutant cells.

**Assay types**:
- **Viability assays**: CellTiter-Glo, MTT in isogenic pairs
- **Synergy scoring**: Bliss independence, Loewe additivity, ZIP model
- **Colony formation**: Long-term survival in mutant vs wild-type
- **In vivo xenografts**: Patient-derived xenograft models with known mutations

**Synergy interpretation**:
- Bliss score > 0.1: synergistic (SL supported)
- Bliss score ~ 0: additive (no SL)
- Bliss score < -0.1: antagonistic (SL contradicted)

### 2.3 Patient-Derived Models

- **PDX (Patient-Derived Xenografts)**: Tumor fragments implanted in immunodeficient mice
- **Organoids**: 3D cultures from patient tumor tissue
- **PDC (Patient-Derived Cells)**: 2D cultures with preserved tumor heterogeneity

**Advantages for SL validation**:
- Natural mutational context (not engineered)
- Tumor heterogeneity preserved
- Drug sensitivity testing in clinically relevant models

---

## 3. Clinical Translation

### 3.1 The PARP Inhibitor Paradigm

The most successful SL therapeutic strategy to date:

| Drug | Target | SL Context | Approved Indication | Year |
|------|--------|-----------|-------------------|------|
| Olaparib | PARP1/2 | BRCA1/2 mutation | Ovarian, breast, prostate, pancreatic | 2014 |
| Rucaparib | PARP1/2/3 | BRCA1/2 mutation | Ovarian, prostate | 2016 |
| Niraparib | PARP1/2 | HRD-positive | Ovarian | 2017 |
| Talazoparib | PARP1/2 | BRCA1/2 mutation | Breast | 2018 |

**Lessons for pipeline**:
- Biomarker (BRCA mutation) must be testable and prevalent
- SL mechanism must be robust across cancer types
- Drug must have therapeutic window (PARP inhibitors tolerated in normal cells)
- Resistance mechanisms develop (BRCA reversion mutations)

### 3.2 TP53-Mutation SL Opportunities

TP53 is mutated in ~50% of all cancers, making its SL partners high-value targets.

**Validated SL partners from Feng et al. (2022)**:
| SL Partner | Drug | Mechanism | Trial Status |
|-----------|------|-----------|-------------|
| TYMS | Pemetrexed, 5-FU | Thymidylate synthase inhibition | Multiple Phase 3 |
| WEE1 | Adavosertib (AZD1775) | G2/M checkpoint abrogation | Phase 2 |
| PLK1 | Volasertib | Mitotic kinase inhibition | Phase 3 (AML) |
| CHK1 | Prexasertib | DNA damage checkpoint | Phase 2 |

**Pipeline integration**:
- Use `biogrid_search_genes` to query ORCS for essentiality data
- Cross-reference with `opentargets_get_target` for druggability
- Search `clinicaltrials_search_trials` for "TP53 mutation" + drug name
- Evidence grade: L2 (Multi-DB) minimum for BioGRID + Open Targets concordance

### 3.3 Beyond TP53: Emerging SL Targets

| Mutated Gene | Cancer Context | SL Partner | Drug Class | Evidence |
|-------------|---------------|-----------|-----------|---------|
| ARID1A | Ovarian, gastric | EZH2 | PRC2 inhibitor (Tazemetostat) | Phase 2 |
| ARID1A | Ovarian | ATR | ATR inhibitor | Phase 1 |
| KRAS | Pancreatic, lung | SHP2 | SHP2 inhibitor | Phase 1/2 |
| SMARCB1 | Rhabdoid tumor | EZH2 | PRC2 inhibitor | FDA approved (2020) |
| STK11 | Lung | mTOR | mTOR inhibitor | Preclinical |

---

## 4. Emerging Methods

### 4.1 Temporal Knowledge Graphs

Standard KGs represent static relationships. Temporal KGs track when SL relationships were discovered, validated, or invalidated:

- **Node attributes**: discovery_date, last_validated, validation_method
- **Edge attributes**: first_reported, confidence_trajectory, retraction status
- **Use case**: Identify SL pairs with increasing evidence over time (rising confidence) vs. those failing to replicate (declining confidence)

**Integration with Graphiti**: The temporal metadata in Graphiti facts (valid_at, invalid_at) naturally supports this pattern.

### 4.2 Multi-Omics Integration

Combining data types improves SL prediction accuracy:

| Data Type | Source | Contribution |
|-----------|--------|-------------|
| Genomics | TCGA, ICGC | Mutation co-occurrence patterns |
| Transcriptomics | CCLE, GTEx | Expression-based dependency |
| Proteomics | CPTAC | Protein-level confirmation |
| Metabolomics | HMDB | Pathway activity readout |
| Epigenomics | ENCODE | Regulatory context |

### 4.3 Foundation Models for SL Prediction

Protein language models trained on evolutionary sequences can predict functional relationships:

- **ESM-2** (Meta): Protein embeddings capture functional similarity
- **ProtTrans** (TU Munich): Transformer-based protein representations
- **Application**: Compute embedding similarity between gene pairs; high functional similarity + co-essentiality = SL candidate

### 4.4 Clinical Trial Design Evolution

SL-focused trial designs are maturing:

- **Basket trials**: Test SL drug across multiple cancers with same mutation
- **Umbrella trials**: Test multiple SL drugs in one cancer type
- **Adaptive platform trials**: Dynamically add/remove SL arms based on interim data
- **Biomarker-driven enrollment**: Require mutation testing before randomization

---

## 5. Pipeline Recommendations

### For the Fuzzy-to-Fact Protocol

1. **ANCHOR phase**: Resolve both genes in the SL pair via HGNC
2. **ENRICH phase**: Get UniProt function for both; check for known SL annotations
3. **EXPAND phase**: Query BioGRID ORCS for essentiality in relevant cell lines
4. **TRAVERSE_DRUGS phase**: Search Open Targets for drugs targeting the SL partner
5. **TRAVERSE_TRIALS phase**: Search ClinicalTrials.gov for combination trials
6. **VALIDATE phase**: Cross-reference BioGRID ORCS + DepMap + Open Targets
7. **PERSIST phase**: Use `lifesciences-reporting` Template 1 (Drug Discovery) with SL-specific sections

### Evidence Grading for SL Claims

| Evidence | Level | Example |
|----------|-------|---------|
| FDA-approved SL drug | L4 (Clinical) | Olaparib for BRCA-mutant ovarian |
| Phase 2+ trial targeting SL | L3 (Functional) | Adavosertib for TP53-mutant cancers |
| BioGRID ORCS + DepMap concordance | L2 (Multi-DB) | TYMS essential in TP53-mutant screens |
| Single CRISPR screen | L1 (Single-DB) | One study shows SL in one cell line |

---

## References

- Feng, X., et al. (2022). Sci. Adv. 8, eabm6638. PMC9098673.
- Tsherniak, A., et al. (2017). Cell 170, 564-576. (DepMap/Achilles)
- Behan, F.M., et al. (2019). Nature 568, 511-516. (Sanger DepMap)
- Lord, C.J. & Ashworth, A. (2017). Science 355, 1152-1158. (SL review)
- Ryan, C.J., et al. (2023). Annual Review of Cancer Biology 7, 213-236.
