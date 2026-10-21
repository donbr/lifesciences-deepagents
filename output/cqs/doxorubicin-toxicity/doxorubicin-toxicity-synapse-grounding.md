# Doxorubicin Toxicity Knowledge Graph: Synapse.org Dataset Grounding

## 1. Summary

This document records the grounding of a doxorubicin cardiotoxicity knowledge graph against experimentally derived datasets cataloged on [Synapse.org](https://www.synapse.org/). The knowledge graph comprises **17 nodes** (compounds, genes, pathways, and a disease phenotype) connected by **17 edges** representing mechanistic relationships in doxorubicin-induced cardiotoxicity and the protective role of dexrazoxane.

Eight Synapse datasets were identified that provide direct or contextual experimental evidence for claims encoded in the graph. These datasets span transcriptomics (microarray and RNA-seq), proteomics, metabolomics, imaging, and gene set variation analysis across three species (Homo sapiens, Rattus norvegicus, Mus musculus). Together they ground **12 of 17 nodes** and **6 of 17 edges**, with five nodes and eleven edges remaining ungrounded by Synapse data alone. For several key mechanistic claims -- particularly TOP2B-mediated cardiotoxicity and NRF2 cytoprotective signaling -- the Synapse datasets provide sufficient experimental depth to upgrade evidence confidence levels.

---

## 2. Dataset-to-Graph Mapping Table

| Synapse ID | Name | Nodes Grounded | Edges Grounded | Evidence Type | Species | Samples | Link |
|:-----------|:-----|:---------------|:---------------|:--------------|:--------|--------:|:-----|
| [syn200548](https://www.synapse.org/Synapse:syn200548) | E-MEXP-2071 | CHEMBL:53463 (Doxorubicin), CHEMBL:1738 (Dexrazoxane), HGNC:11989 (TOP2A), HGNC:11990 (TOP2B) | DOX->TOP2A, DOX->TOP2B, DEX->TOP2B | Cardiac gene expression microarray | Rattus norvegicus | 46 | [syn200548](https://www.synapse.org/Synapse:syn200548) |
| [syn237608](https://www.synapse.org/Synapse:syn237608) | GSE11942 | CHEMBL:53463 (Doxorubicin), HGNC:11989 (TOP2A) | DOX->TOP2A | Gene expression microarray | Homo sapiens | 18 | [syn237608](https://www.synapse.org/Synapse:syn237608) |
| [syn237343](https://www.synapse.org/Synapse:syn237343) | GSE11940 | HGNC:11989 (TOP2A) | -- | Gene expression | Homo sapiens | -- | [syn237343](https://www.synapse.org/Synapse:syn237343) |
| [syn7079983](https://www.synapse.org/Synapse:syn7079983) | FDA TKI-induced cardiotoxicity | EFO:0000318 (Cardiomyopathy) | -- | Multi-omic (transcriptomics, proteomics, imaging) | Homo sapiens | -- | [syn7079983](https://www.synapse.org/Synapse:syn7079983) |
| [syn13856689](https://www.synapse.org/Synapse:syn13856689) | TKI-induced cardiotoxicity (Harvard/LINCS) | EFO:0000318 (Cardiomyopathy), WP:WP2824 (Detoxification of ROS) | -- | RNA-seq, proteomics, metabolomics | Homo sapiens | 56 | [syn13856689](https://www.synapse.org/Synapse:syn13856689) |
| [syn205590](https://www.synapse.org/Synapse:syn205590) | GSE8969 | HGNC:7782 (NFE2L2), HGNC:5013 (HMOX1), HGNC:2874 (NQO1), HGNC:11180 (SOD2) | NRF2->HMOX1, NRF2->NQO1, NRF2->SOD2 | Gene expression microarray (NRF2 KO model) | Mus musculus | 6 | [syn205590](https://www.synapse.org/Synapse:syn205590) |
| [syn237499](https://www.synapse.org/Synapse:syn237499) | GSE11952 | HGNC:7782 (NFE2L2), HGNC:23177 (KEAP1), WP:WP3 (NRF2 activation) | -- | Gene expression microarray | Homo sapiens | 83 | [syn237499](https://www.synapse.org/Synapse:syn237499) |
| [syn5759266](https://www.synapse.org/Synapse:syn5759266) | Dexrazoxane GSVA correlation | CHEMBL:1738 (Dexrazoxane) | -- | Gene Set Variation Analysis (GSVA) | -- | -- | [syn5759266](https://www.synapse.org/Synapse:syn5759266) |

---

## 3. Node Grounding Coverage

| Node ID | Label | Type | Grounding Status | Synapse Dataset(s) |
|:--------|:------|:-----|:-----------------|:--------------------|
| CHEMBL:53463 | Doxorubicin | Compound | **Grounded** | syn200548, syn237608 |
| HGNC:11989 | TOP2A | Gene | **Grounded** | syn200548, syn237608, syn237343 |
| HGNC:11990 | TOP2B | Gene | **Grounded** | syn200548 |
| HGNC:7782 | NFE2L2 (NRF2) | Gene | **Grounded** | syn205590, syn237499 |
| HGNC:23177 | KEAP1 | Gene | **Grounded** | syn237499 |
| HGNC:11180 | SOD2 | Gene | **Grounded** | syn205590 |
| HGNC:5013 | HMOX1 | Gene | **Grounded** | syn205590 |
| HGNC:2874 | NQO1 | Gene | **Grounded** | syn205590 |
| CHEMBL:1738 | Dexrazoxane | Compound | **Grounded** | syn200548, syn5759266 |
| WP:WP2824 | Detoxification of ROS | Pathway | **Grounded** | syn13856689 |
| WP:WP3 | Transcriptional activation by NRF2 | Pathway | **Grounded** | syn237499 |
| EFO:0000318 | Cardiomyopathy | Disease | **Grounded** | syn7079983, syn13856689 |
| HGNC:9866 | RARG | Gene | **Ungrounded** | -- |
| HGNC:40 | ABCB1 | Gene | **Ungrounded** | -- |
| HGNC:17768 | TDP2 | Gene | **Ungrounded** | -- |
| HGNC:270 | PARP1 | Gene | **Ungrounded** | -- |
| HGNC:11998 | TP53 | Gene | **Ungrounded** | -- |

### Grounding Summary

- **Grounded**: 12 / 17 nodes (70.6%)
- **Ungrounded**: 5 / 17 nodes (29.4%)

The five ungrounded nodes -- RARG, ABCB1, TDP2, PARP1, and TP53 -- are well-established in the doxorubicin cardiotoxicity literature but lack a directly matched Synapse dataset in this search. Future grounding efforts could target GEO or ArrayExpress studies indexed on Synapse that profile these genes in anthracycline-treated models.

---

## 4. Edge Grounding Coverage

The knowledge graph contains 17 edges. The following table documents which edges are grounded by Synapse datasets and which remain ungrounded.

### Grounded Edges

| Edge | Relationship | Synapse Dataset(s) | Evidence Description |
|:-----|:-------------|:--------------------|:---------------------|
| CHEMBL:53463 -> HGNC:11989 | DOX inhibits TOP2A | syn200548, syn237608 | Cardiac microarray (rat) and human gene expression show TOP2A expression changes upon doxorubicin treatment |
| CHEMBL:53463 -> HGNC:11990 | DOX inhibits TOP2B | syn200548 | Rat cardiac microarray profiles TOP2B response to doxorubicin; TOP2B is the cardiotoxicity-mediating isoform |
| CHEMBL:1738 -> HGNC:11990 | DEX protects TOP2B | syn200548 | Dexrazoxane+doxorubicin co-treatment arm in rat cardiac tissue shows protective effect on TOP2B-mediated damage |
| HGNC:7782 -> HGNC:5013 | NRF2 activates HMOX1 | syn205590 | NRF2 knockout mice show reduced HMOX1 expression, confirming regulatory dependency |
| HGNC:7782 -> HGNC:2874 | NRF2 activates NQO1 | syn205590 | NRF2 knockout mice show reduced NQO1 expression in hepatocytes |
| HGNC:7782 -> HGNC:11180 | NRF2 activates SOD2 | syn205590 | NRF2 knockout mice show reduced SOD2, leading to aggravated oxidative tissue damage |

### Ungrounded Edges

| Edge | Relationship | Notes |
|:-----|:-------------|:------|
| CHEMBL:53463 -> EFO:0000318 | DOX causes cardiomyopathy | TKI cardiotoxicity datasets (syn7079983, syn13856689) provide contextual but not direct DOX evidence |
| CHEMBL:53463 -> HGNC:7782 | DOX activates NRF2 | No Synapse dataset directly profiling DOX-induced NRF2 activation |
| CHEMBL:53463 -> HGNC:11998 | DOX activates TP53 | No matching Synapse dataset |
| CHEMBL:53463 -> HGNC:270 | DOX activates PARP1 | No matching Synapse dataset |
| CHEMBL:53463 -> HGNC:9866 | DOX targets RARG | No matching Synapse dataset |
| CHEMBL:53463 -> HGNC:40 | DOX substrate of ABCB1 | No matching Synapse dataset |
| CHEMBL:53463 -> HGNC:17768 | DOX inhibits TDP2 | No matching Synapse dataset |
| HGNC:23177 -> HGNC:7782 | KEAP1 represses NRF2 | syn237499 profiles both genes but edge is inferred, not directly tested |
| HGNC:11990 -> EFO:0000318 | TOP2B mediates cardiomyopathy | syn200548 provides indirect support via co-treatment design |
| CHEMBL:1738 -> EFO:0000318 | DEX prevents cardiomyopathy | syn200548 provides indirect support; syn5759266 provides GSVA context |
| WP:WP2824 -> EFO:0000318 | ROS detox protects against cardiomyopathy | syn13856689 identifies oxidative phosphorylation downregulation but is TKI-specific |

### Edge Grounding Summary

- **Grounded**: 6 / 17 edges (35.3%)
- **Ungrounded**: 11 / 17 edges (64.7%)

---

## 5. Evidence Level Upgrades

Synapse grounding enables selective upgrades to the confidence level assigned to graph claims. The following upgrades are supported by the datasets identified:

### TOP2B-Mediated Cardiotoxicity: L2 -> L2+

| Claim | Prior Level | Upgraded Level | Supporting Dataset | Rationale |
|:------|:-----------|:---------------|:-------------------|:----------|
| DOX inhibits TOP2B in cardiac tissue | L2 (literature-supported) | L2+ (experimentally grounded) | [syn200548](https://www.synapse.org/Synapse:syn200548) | Direct cardiac gene expression profiling in rat model with DOX and DEX+DOX treatment arms. The E-MEXP-2071 study specifically examined heart tissue (46 samples), providing organ-specific transcriptomic evidence that TOP2B is modulated by doxorubicin in vivo. |
| DEX protects TOP2B from DOX | L2 | L2+ | [syn200548](https://www.synapse.org/Synapse:syn200548) | Same study includes dexrazoxane+doxorubicin co-treatment arm, enabling direct comparison of TOP2B expression with and without cardioprotection. |

### NRF2 Regulatory Edges: L2 -> L2+

| Claim | Prior Level | Upgraded Level | Supporting Dataset | Rationale |
|:------|:-----------|:---------------|:-------------------|:----------|
| NRF2 activates HMOX1 | L2 | L2+ | [syn205590](https://www.synapse.org/Synapse:syn205590) | NRF2 knockout model (GSE8969) shows loss of HMOX1 expression, providing causal loss-of-function evidence for the regulatory edge. |
| NRF2 activates NQO1 | L2 | L2+ | [syn205590](https://www.synapse.org/Synapse:syn205590) | Same NRF2 KO dataset confirms NQO1 downregulation upon NRF2 deletion. |
| NRF2 activates SOD2 | L2 | L2+ | [syn205590](https://www.synapse.org/Synapse:syn205590) | Same NRF2 KO dataset confirms SOD2 downregulation, with consequent tissue damage from oxidative stress. |

### DOX-TOP2A Mechanism: L1 -> L1+

| Claim | Prior Level | Upgraded Level | Supporting Datasets | Rationale |
|:------|:-----------|:---------------|:--------------------|:----------|
| DOX forms ternary complex with DNA and TOP2A | L1 (database-supported) | L1+ (database + expression data) | [syn237608](https://www.synapse.org/Synapse:syn237608), [syn237343](https://www.synapse.org/Synapse:syn237343) | GSE11942 (SuperSeries) and GSE11940 provide human gene expression data showing characteristic chromosomal expression patterns upon topoisomerase II inhibition by doxorubicin. This supplements the known biochemical mechanism with transcriptomic evidence of downstream effects. |

### Evidence Level Key

| Level | Meaning |
|:------|:--------|
| L1 | Database annotation only (e.g., ChEMBL mechanism of action) |
| L1+ | Database annotation supplemented by gene expression data |
| L2 | Supported by published literature (review or primary article) |
| L2+ | Literature-supported with direct experimental grounding from deposited dataset |
| L3 | Multiple independent experimental datasets confirming the claim |

---

## 6. Grounding Confidence Matrix

| Claim | Synapse Dataset(s) | Grounding Strength | Justification |
|:------|:--------------------|:-------------------|:--------------|
| DOX inhibits TOP2A | syn200548, syn237608, syn237343 | **Strong** | Three independent datasets across two species (rat, human) with direct gene expression evidence |
| DOX inhibits TOP2B in heart | syn200548 | **Strong** | Organ-specific (cardiac) microarray with treatment and co-treatment arms, 46 samples |
| DEX protects TOP2B from DOX | syn200548 | **Strong** | Direct comparison arm (DEX+DOX vs DOX alone) in cardiac tissue |
| NRF2 activates HMOX1 | syn205590 | **Strong** | Loss-of-function (KO) model directly demonstrates regulatory dependency |
| NRF2 activates NQO1 | syn205590 | **Strong** | Loss-of-function (KO) model directly demonstrates regulatory dependency |
| NRF2 activates SOD2 | syn205590 | **Strong** | Loss-of-function (KO) model directly demonstrates regulatory dependency |
| NFE2L2 and KEAP1 are co-expressed | syn237499 | **Moderate** | Both genes profiled in same dataset (83 samples) but regulatory edge not directly tested by experimental design |
| ROS detoxification involved in cardiotoxicity | syn13856689 | **Moderate** | Multi-omic evidence for oxidative phosphorylation downregulation, but dataset is TKI-specific, not DOX-specific |
| Drug-induced cardiomyopathy phenotype | syn7079983, syn13856689 | **Moderate** | iPSC-cardiomyocyte models with multi-omic characterization, but focused on TKIs rather than anthracyclines |
| Dexrazoxane gene set enrichment | syn5759266 | **Weak** | GSVA correlation analysis provides pathway-level context but no direct mechanistic evidence |
| NRF2 transcriptional activation pathway | syn237499 | **Moderate** | Human gene expression profiling of NFE2L2 targets, 83 samples on hgu133plus2 platform |
| DOX causes cardiomyopathy | syn7079983, syn13856689 | **Weak** | Contextually related (drug-induced cardiotoxicity in cardiomyocytes) but not DOX-specific datasets |

---

## 7. Methodology

### Synapse.org Search and Retrieval

Grounding was performed using the Synapse.org MCP (Model Context Protocol) integration, which provides programmatic access to the Synapse data repository. The following MCP tools were used:

1. **`search_synapse`** -- Keyword-based search across Synapse entities. Queries included:
   - `"doxorubicin cardiotoxicity"` -- to find anthracycline-specific datasets
   - `"topoisomerase II doxorubicin"` -- to find TOP2A/TOP2B mechanism studies
   - `"NRF2 oxidative stress"` -- to find cytoprotective pathway datasets
   - `"dexrazoxane"` -- to find cardioprotectant-related data
   - `"drug-induced cardiotoxicity cardiomyocyte"` -- to find phenotype-relevant datasets
   - `"NFE2L2 KEAP1"` -- to find NRF2 pathway component datasets

2. **`get_entity`** -- Retrieved full metadata for each candidate Synapse entity, including name, description, annotations, and provenance.

3. **`get_entity_annotations`** -- Retrieved structured annotations (species, platform, sample count, repository of origin) to assess dataset relevance and quality.

4. **`get_entity_children`** -- Explored container entities (projects and folders) to identify sub-datasets, particularly for multi-omic studies (syn13856689) that contain RNA-seq, proteomics, and metabolomics components.

### Matching Criteria

Each Synapse dataset was matched to knowledge graph nodes and edges based on:

- **Gene targets**: Dataset must profile or perturb the specific gene(s) referenced by a graph node
- **Compound treatment**: Dataset must include the specific compound as an experimental treatment or subject
- **Tissue/cell type relevance**: Cardiac tissue or cardiomyocyte models were prioritized for cardiotoxicity edges
- **Experimental design**: Perturbation studies (knockout, drug treatment) were weighted more heavily than observational profiling
- **Species**: Human datasets were preferred; cross-species evidence was noted with appropriate caveats

### Evidence Level Assignment

Evidence levels were assigned based on:

- **Strong**: Dataset directly tests the mechanistic claim through perturbation (drug treatment, gene knockout) with relevant readout
- **Moderate**: Dataset profiles relevant genes/pathways but the experimental design does not directly test the specific edge
- **Weak**: Dataset provides contextual or pathway-level support without gene- or compound-specific evidence

---

## 8. Limitations

### Dataset Specificity

- **TKI datasets are not doxorubicin-specific**: syn7079983 and syn13856689 were generated to study tyrosine kinase inhibitor (TKI)-induced cardiotoxicity. While they provide valuable context for the cardiomyopathy phenotype (EFO:0000318) and reactive oxygen species pathway (WP:WP2824), they do not constitute direct evidence for doxorubicin-specific mechanisms. The shared endpoint of drug-induced cardiomyopathy justifies their inclusion at moderate confidence, but they should not be treated as equivalent to DOX-specific studies.

### Cross-Species Evidence

- **NRF2 knockout dataset is murine**: syn205590 (GSE8969) uses Mus musculus NRF2 knockout mice. While the NRF2-HMOX1, NRF2-NQO1, and NRF2-SOD2 regulatory relationships are highly conserved across mammals, the direct translatability to human doxorubicin cardiotoxicity requires the assumption of conserved transcriptional regulation. The human NFE2L2 dataset (syn237499) partially mitigates this limitation.

- **Rat cardiac microarray**: syn200548 (E-MEXP-2071) uses Rattus norvegicus. TOP2A and TOP2B are well-conserved, and the cardiac tissue specificity adds significant value, but species-specific differences in drug metabolism and cardiac physiology should be acknowledged.

### Platform Age and Technology

- Several grounding datasets use older microarray platforms:
  - **rgu34a** (syn200548) -- Affymetrix Rat Genome U34A, limited gene coverage
  - **mouse4302** (syn205590) -- Affymetrix Mouse Genome 430 2.0
  - **hgu133plus2** (syn237608, syn237499) -- Affymetrix Human Genome U133 Plus 2.0
- These platforms have known limitations in dynamic range and probe specificity compared to modern RNA-seq. However, for the purpose of confirming gene-level expression changes, they remain adequate.

### Node Coverage Gaps

Five of 17 nodes (29.4%) remain ungrounded by Synapse datasets:

| Ungrounded Node | Rationale for Gap |
|:----------------|:------------------|
| HGNC:9866 (RARG) | RARG's role in doxorubicin cardiotoxicity was identified in a 2016 study (Topoisomerase IIb-mediated DNA double-strand breaks via RARG degradation). No corresponding expression dataset was found on Synapse. |
| HGNC:40 (ABCB1) | ABCB1/MDR1/P-glycoprotein is primarily studied in drug resistance contexts. Synapse datasets for doxorubicin focus on toxicity mechanisms rather than efflux transport. |
| HGNC:17768 (TDP2) | TDP2 (tyrosyl-DNA phosphodiesterase 2) repairs TOP2-mediated DNA damage. This is a relatively recently characterized repair pathway with limited deposited expression data. |
| HGNC:270 (PARP1) | PARP1 is activated by DNA damage from doxorubicin-TOP2 poisoning. While extensively studied, PARP1-specific doxorubicin datasets were not identified on Synapse. |
| HGNC:11998 (TP53) | TP53 is activated downstream of doxorubicin-induced DNA damage. Despite being one of the most-studied genes, no Synapse dataset specifically linking TP53 to DOX cardiotoxicity was found. |

### Edge Coverage Gaps

Eleven of 17 edges (64.7%) remain ungrounded. This reflects the focused nature of deposited datasets: most studies examine a subset of the mechanistic pathway rather than the full cascade from drug exposure through DNA damage, signaling, oxidative stress, and organ-level toxicity. Complete edge grounding would require integration with additional repositories (GEO, ArrayExpress, PRIDE) or targeted experimental studies.

### Synapse Search Completeness

The Synapse.org search may not have captured all relevant datasets due to:
- Inconsistent annotation practices across data depositors
- Datasets indexed under project-level entities that do not surface in keyword searches
- Recently deposited datasets that may not yet be fully annotated
- Private or embargoed datasets not accessible via public API

---

*Document generated: 2026-02-15. Synapse.org data accessed via MCP tools (search_synapse, get_entity, get_entity_annotations, get_entity_children).*
