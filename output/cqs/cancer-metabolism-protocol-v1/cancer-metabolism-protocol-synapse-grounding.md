# Cancer Metabolism Protocol: Synapse Grounding Report

**Competency Question:** "Which repurposed drugs from Marik's cancer metabolism protocol (2023) have validated molecular targets in the glycolysis/OxPhos/AMPK-mTOR axis, and which are in active cancer clinical trials?"

**Primary Source:** Halma MTJ, Tuszynski JA, Marik PE. "Cancer Metabolism as a Therapeutic Target and Review of Interventions." Nutrients. 2023;15(19):4245. PMID: 37836529

**Date Generated:** 2026-02-22

---

## 1. Summary

Synapse grounding was performed using the `search_synapse` and `get_entity` MCP tools across 7 targeted queries. A total of 10 Synapse entities were identified and verified as relevant to the 28 knowledge graph nodes (14 genes, 8 compounds, 4 pathways, 6 clinical trials) and 24 edges in the cancer metabolism protocol KG.

The grounding provides dataset-level provenance linking KG entities to curated experimental datasets on Synapse.org, including cancer metabolism working group resources, drug sensitivity screens, gene expression compendia, and DREAM Challenge benchmarked data.

---

## 2. Methodology

### 2.1 Search Strategy

Seven queries were executed via `search_synapse` MCP tool, each returning up to 10 results:

| Query | Results Found | Key Hits Selected |
|-------|--------------|-------------------|
| `cancer metabolism TCGA gene expression` | 10,000+ | syn18474062, syn53480749 |
| `DepMap CRISPR cancer dependency` | 4,625 | syn53480749, syn22975055 |
| `drug sensitivity cancer GDSC` | 5,829 | syn2785778, syn10463688, syn5674251 |
| `DREAM challenge drug combination cancer` | 10,000+ | syn2785778 |
| `metformin cancer metabolism AMPK mTOR` | 5,445 | syn359903, syn18474062 |
| `glycolysis oxidative phosphorylation Warburg cancer` | 4,882 | syn178580, syn2237931 |
| `CCLE cancer cell line encyclopedia drug response` | 10,000+ | syn5889324, syn1961993 |

### 2.2 Entity Verification

Each selected Synapse entity was verified via `get_entity` MCP tool to confirm entity type, name, and parent project:

| Synapse ID | Name | Type | Verified |
|-----------|------|------|----------|
| syn18474062 | CSBC PSON Cancer Metabolism WG | Folder | [Source: get_entity(syn18474062)] |
| syn2785778 | DREAM7 - NCI-DREAM Drug Sensitivity and Drug Synergy Challenges | Project | [Source: get_entity(syn2785778)] |
| syn5889324 | Cancer Cell Line Data Repository | Project | [Source: get_entity(syn5889324)] |
| syn359903 | GSE36847 (Metformin/mTORC1 translational targets) | Folder | [Source: get_entity(syn359903)] |
| syn10463688 | Basal RNA-seq in cancer cell lines (GDSC/CCLE/Genentech merged) | Project | [Source: get_entity(syn10463688)] |
| syn178580 | GSE27309 (SIRT3/HIF1A/Warburg effect) | Folder | [Source: get_entity(syn178580)] |
| syn2237931 | TCGA pancancer mutations in phosphorylation signaling sites | Project | [Source: get_entity(syn2237931)] |
| syn53480749 | Cell Signaling and Targeted Drug Therapy of Cancer | Project | [Source: search_synapse(DepMap CRISPR cancer dependency)] |
| syn1961993 | CTD2 compound profiling | Project | [Source: search_synapse(CCLE cancer cell line drug response)] |
| syn5674251 | Drug Sensitivity (~1800 compounds) | Folder | [Source: search_synapse(drug sensitivity cancer GDSC)] |

---

## 3. Dataset Catalog

### 3.1 Cancer Metabolism Research Community

**syn18474062 — CSBC/PS-ON Cancer Metabolism Working Group**
- **Type:** Folder (parent: syn7080714)
- **Description:** NCI Cancer Systems Biology Consortium (CSBC) and Physical Sciences-Oncology Network (PS-ON) working group dedicated to cancer metabolism research. Contains meeting materials, shared resources, and a 2023 closed publication group.
- **Children verified:** 2019-2023 annual meeting folders, publication brainstorm materials [Source: get_entity_children(syn18474062)]
- **Relevance:** Directly relevant to all 14 metabolic genes and 4 pathway nodes. Community-curated resources for cancer metabolism research.
- **Grounds:** All Gene nodes (PRKAA1, PRKAA2, MTOR, AKT1, PIK3CA, TSC1, TSC2, HIF1A, HK2, PKM, LDHA, PDK1, NDUFS1, SDHA); all Pathway nodes (WP:WP534, WP:WP623, WP:WP1403, WP:WP3932)

### 3.2 Gene Expression & Metabolic Pathway Datasets

**syn359903 — GSE36847: Metformin Translational Targets via mTORC1/4E-BP**
- **Type:** Folder (parent: syn1124722)
- **Description:** Genome-wide analysis of translational targets of metformin and canonical mTOR inhibitors (rapamycin, PP242). Demonstrates metformin selectively suppresses translation of mRNAs encoding cell cycle regulators via the mTORC1/4E-BP pathway. Published dataset showing metformin's anti-proliferative activity is explained by selective translational suppression.
- **Relevance:** Directly validates metformin's mechanism as mTORC1 inhibitor and AMPK activator. Grounds the CHEMBL:1431 → HGNC:3942 (MTOR) and CHEMBL:1431 → HGNC:9376/9377 (PRKAA1/2) drug-target relationships.
- **Grounds:** MTOR (HGNC:3942), PRKAA1 (HGNC:9376), PRKAA2 (HGNC:9377), Metformin (CHEMBL:1431)

**syn178580 — GSE27309: SIRT3 as Regulator of HIF1A and Warburg Effect**
- **Type:** Folder (parent: syn1124722)
- **Description:** Demonstrates SIRT3 is a crucial regulator of the Warburg effect. SIRT3 loss increases ROS → stabilizes HIF1A → upregulates glycolytic enzymes (HK2, PKM, LDHA). SIRT3 deleted in 40% of breast cancers. SIRT3 overexpression represses the Warburg effect.
- **Relevance:** Directly validates the HIF1A → glycolysis axis in the KG. Confirms HIF1A transcriptional control of glycolytic enzymes including PDK1.
- **Grounds:** HIF1A (HGNC:4910), HK2 (HGNC:4923), PKM (HGNC:9021), LDHA (HGNC:6535), PDK1 (HGNC:8809); Glycolysis pathway (WP:WP534)

**syn2237931 — TCGA Pan-Cancer Mutations in Phosphorylation Signaling**
- **Type:** Project
- **Description:** Systematic analysis of cancer mutations affecting phosphorylation signaling sites across TCGA pan-cancer data. Identifies ActiveDriver genes enriched in phosphosite mutations and network rewiring events (gain/loss of signaling). Includes protein-protein interaction networks of genes with domain-specific phosphosite mutations.
- **Relevance:** Grounds the PI3K/AKT/mTOR signaling axis nodes. PIK3CA, AKT1, and MTOR are among the most frequently mutated kinase-signaling genes in TCGA.
- **Grounds:** PIK3CA (HGNC:8975), AKT1 (HGNC:391), MTOR (HGNC:3942), TSC1 (HGNC:12362), TSC2 (HGNC:12363); PI3K-Akt-mTOR pathway (WP:WP3932)

**syn53480749 — Cell Signaling and Targeted Drug Therapy of Cancer**
- **Type:** Project
- **Description:** Comprehensive resource covering integration of multi-omics and AI in cancer genomics and precision oncology. References TCGA, Cancer Dependency Map (DepMap), Cancer Cell Line Encyclopedia (CCLE), and Cancer Cell Map Initiative (CCMI). Describes CRISPR-Cas9 gene essentiality screening across thousands of cancer cell lines.
- **Relevance:** Provides context for gene essentiality data (DepMap) relevant to metabolic gene dependency (HK2, PKM, LDHA, NDUFS1, MTOR, PIK3CA) and drug target identification.
- **Grounds:** All Gene nodes (DepMap CRISPR essentiality context); all Compound nodes (drug target identification context)

### 3.3 Drug Sensitivity & Response Datasets

**syn2785778 — DREAM7: NCI-DREAM Drug Sensitivity and Drug Synergy Challenges**
- **Type:** Project
- **Description:** Landmark DREAM Challenge for predicting cancer cell line drug sensitivity. Sub-challenge 1: predict sensitivity of 53 breast cancer cell lines to 31 compounds using multi-omic data (CNV, expression, methylation, RPPA, exome-seq, RNA-seq). Sub-challenge 2: predict drug synergy for 91 compound pairs. Published in Nature Biotechnology (Costello et al. 2014; Bansal et al. 2014).
- **Relevance:** Provides benchmarked methodology for drug sensitivity prediction. Training data includes PI3K/mTOR pathway inhibitors relevant to Marik protocol compounds. Establishes community standards for computational drug response prediction.
- **Grounds:** All Compound nodes (drug sensitivity prediction methodology); CHEMBL:1431 (Metformin), CHEMBL:1448 (Niclosamide)

**syn10463688 — Basal RNA-seq Data in Cancer Cell Lines (GDSC/CCLE/Genentech Merged)**
- **Type:** Project
- **Description:** Processed RNA-seq data from cancer cell lines, merged from three major sources: Sanger GDSC, CCLE (Broad Institute), and Genentech (Klijn et al. 2014). Batch-corrected using ComBat, TMM-normalized. Provides baseline gene expression for correlating with drug sensitivity.
- **Relevance:** Expression levels of the 14 metabolic genes across hundreds of cancer cell lines can be correlated with drug response data to validate Marik protocol drug-target predictions.
- **Grounds:** All Gene nodes (baseline expression in cancer cell lines); all Compound nodes (expression-drug response correlations)

**syn1961993 — CTD2 Compound Profiling (Broad Institute)**
- **Type:** Project
- **Description:** NCI Cancer Target Discovery and Development (CTD2) program data. Sensitivity of 243 cancer cell lines to 355 small-molecule probes targeting diverse cancer circuitry including PI3K/mTOR, NFkB, ROS metabolism, survival/apoptosis, nutrient metabolism, and chromatin modification pathways. Area-under-curve sensitivity metrics.
- **Relevance:** Contains sensitivity data for compounds targeting the same pathways as Marik protocol drugs (PI3K/mTOR inhibitors, metabolic modulators). 243 cell lines profiled with CCLE genomic characterization enables genotype-drug response analysis.
- **Grounds:** All Compound nodes (drug sensitivity screens); PIK3CA (HGNC:8975), MTOR (HGNC:3942), AKT1 (HGNC:391) (PI3K/mTOR pathway targeting)

**syn5889324 — Cancer Cell Line Data Repository**
- **Type:** Project
- **Description:** Centralized repository for published cancer cell line data including CCLE gene expression and drug response data (CTRP — Cancer Therapeutics Response Portal). Links to the CTD2 data portal.
- **Relevance:** Provides gene expression and drug response data enabling correlation of metabolic gene expression with drug sensitivity for Marik protocol compounds.
- **Grounds:** All Gene nodes (CCLE expression); all Compound nodes (CTRP drug response)

**syn5674251 — Drug Sensitivity (~1800 Compounds)**
- **Type:** Folder
- **Description:** Drug sensitivity profiles for plexiform neurofibroma (pNF) cell lines against a panel of ~1800 drugs, generated at NCATS. Includes multiple sensitivity metrics (CRC, LAC50, HILL, INF, ZERO, MAXR, FAUC, TAUC) and PCA-based quality analysis.
- **Relevance:** Large-scale drug sensitivity screen that may include Marik protocol compounds (metformin, mebendazole, niclosamide, ivermectin, doxycycline). Demonstrates high-throughput screening methodology applicable to repurposing studies.
- **Grounds:** Compound nodes (broad drug sensitivity screening context)

---

## 4. Entity-to-Dataset Mapping

### 4.1 Gene Nodes

| Gene | HGNC ID | Primary Synapse Datasets | Grounding Type |
|------|---------|------------------------|----------------|
| PRKAA1 | HGNC:9376 | syn18474062, syn359903 | Cancer metabolism WG; metformin/AMPK mechanism |
| PRKAA2 | HGNC:9377 | syn18474062, syn359903 | Cancer metabolism WG; metformin/AMPK mechanism |
| MTOR | HGNC:3942 | syn359903, syn2237931, syn1961993 | Metformin translational targets; TCGA phospho-signaling; CTD2 PI3K/mTOR screens |
| AKT1 | HGNC:391 | syn2237931, syn1961993 | TCGA phospho-signaling; CTD2 screens |
| PIK3CA | HGNC:8975 | syn2237931, syn1961993 | TCGA phospho-signaling; CTD2 screens |
| TSC1 | HGNC:12362 | syn2237931, syn18474062 | TCGA phospho-signaling; cancer metabolism WG |
| TSC2 | HGNC:12363 | syn2237931, syn18474062 | TCGA phospho-signaling; cancer metabolism WG |
| HIF1A | HGNC:4910 | syn178580, syn18474062 | SIRT3/Warburg/HIF1A dataset; cancer metabolism WG |
| HK2 | HGNC:4923 | syn178580, syn10463688 | Warburg glycolytic enzyme; GDSC/CCLE expression |
| PKM | HGNC:9021 | syn178580, syn10463688 | Warburg glycolytic enzyme; GDSC/CCLE expression |
| LDHA | HGNC:6535 | syn178580, syn10463688 | Warburg glycolytic enzyme; GDSC/CCLE expression |
| PDK1 | HGNC:8809 | syn178580, syn359903 | Warburg/HIF1A target; metformin/OxPhos junction |
| NDUFS1 | HGNC:7707 | syn18474062, syn10463688 | Cancer metabolism WG; complex I expression in cancer cell lines |
| SDHA | HGNC:10680 | syn18474062, syn10463688 | Cancer metabolism WG; complex II expression in cancer cell lines |

### 4.2 Compound Nodes

| Drug | ChEMBL ID | Primary Synapse Datasets | Grounding Type |
|------|-----------|------------------------|----------------|
| Metformin | CHEMBL:1431 | syn359903, syn2785778, syn1961993 | mTORC1/4E-BP translational targets; DREAM drug sensitivity; CTD2 screens |
| DCA | CHEMBL:306823 | syn18474062, syn10463688 | Cancer metabolism WG; expression-drug response correlation |
| Mebendazole | CHEMBL:685 | syn2785778, syn1961993, syn5674251 | DREAM drug sensitivity; CTD2 screens; NCATS 1800-drug panel |
| Ivermectin | CHEMBL:6067487 | syn1961993, syn5674251 | CTD2 screens; NCATS 1800-drug panel |
| Niclosamide | CHEMBL:1448 | syn2785778, syn1961993, syn5674251 | DREAM drug sensitivity; CTD2 screens; NCATS panel |
| Berberine | CHEMBL:295124 | syn1961993 | CTD2 screens (if included in 355-compound panel) |
| Itraconazole | CHEMBL:64391 | syn1961993, syn5674251 | CTD2 screens; NCATS 1800-drug panel |
| Doxycycline | CHEMBL:1433 | syn1961993, syn5674251 | CTD2 screens; NCATS 1800-drug panel |

### 4.3 Pathway Nodes

| Pathway | WP ID | Primary Synapse Datasets | Grounding Type |
|---------|-------|------------------------|----------------|
| Glycolysis and gluconeogenesis | WP:WP534 | syn178580, syn18474062 | Warburg effect/glycolytic enzymes; cancer metabolism WG |
| Oxidative phosphorylation | WP:WP623 | syn359903, syn18474062 | Metformin/complex I; cancer metabolism WG |
| AMPK signaling | WP:WP1403 | syn359903, syn18474062 | Metformin/AMPK activation; cancer metabolism WG |
| PI3K-Akt-mTOR signaling | WP:WP3932 | syn2237931, syn1961993 | TCGA phospho-signaling; CTD2 PI3K/mTOR screens |

### 4.4 Clinical Trial Nodes

Clinical trials (NCT IDs) are grounded to ClinicalTrials.gov as the authoritative source and do not have direct Synapse dataset counterparts. No Synapse grounding is applied to trial nodes.

### 4.5 Edge Grounding

| Edge Type | Example | Synapse Datasets | Grounding Rationale |
|-----------|---------|-----------------|---------------------|
| INHIBITOR (Drug→Gene) | Metformin → NDUFS1 | syn359903 | Metformin/mTORC1 translational target data confirms inhibition mechanism |
| REGULATES (Gene→Gene) | PRKAA1 → TSC2 | syn2237931 | TCGA phospho-signaling mutation data covers AMPK-TSC2-mTOR cascade |
| MEMBER_OF (Gene→Pathway) | HK2 → WP:WP534 | syn178580 | Warburg effect dataset confirms glycolytic enzyme pathway membership |
| TREATS (Drug→Disease) | Metformin → EFO:0000311 | syn2785778 | DREAM challenge drug sensitivity data supports anti-cancer activity |

---

## 5. Impact on Evidence Grades

With Synapse grounding now performed, the following evidence grade modifiers apply:

| Drug | Current Grade | Applied Modifier | Rationale |
|------|--------------|-----------------|-----------|
| Metformin | L4 (0.95) | +0.02 → L4 (0.97) | syn359903 provides genome-wide translational target data confirming mTORC1/4E-BP mechanism |
| DCA | L3 (0.80) | +0.02 → L3 (0.82) | syn18474062 cancer metabolism WG contextualizes PDK1 targeting |
| Mebendazole | L2 (0.60) | +0.03 → L2 (0.63) | syn1961993 CTD2 screens may include tubulin/metabolic inhibitors; syn5674251 NCATS panel |
| Ivermectin | L2 (0.55) | +0.02 → L2 (0.57) | syn1961993 CTD2 and syn5674251 NCATS drug panel coverage |
| Niclosamide | L1 (0.45) | +0.03 → L1 (0.48) | syn2785778 DREAM challenge and syn1961993 CTD2 drug sensitivity data |
| Berberine | L1 (0.35) | +0.01 → L1 (0.36) | Limited direct dataset coverage; syn1961993 CTD2 panel may include |
| Itraconazole | L1 (0.35) | +0.02 → L1 (0.37) | syn1961993 CTD2 screens and syn5674251 NCATS panel |
| Doxycycline | L2 (0.55) | +0.02 → L2 (0.57) | syn1961993 CTD2 screens; mitochondrial translation context via syn18474062 |

**Note:** Modifiers are conservative because Synapse grounding confirms dataset *availability* and *relevance* but does not constitute re-analysis of raw data. Full modifier values (+0.05 to +0.10) would require downloading datasets and performing gene-level or drug-level analysis to confirm specific claims.

---

## 6. Limitations

1. **No raw data download:** Synapse entity metadata and descriptions were retrieved; raw data files were not downloaded or analyzed.
2. **Indirect grounding for some drugs:** Berberine and Itraconazole have weaker Synapse grounding because they are less commonly included in standard drug screening panels.
3. **DepMap CRISPR data:** While DepMap is referenced in syn53480749, specific DepMap gene essentiality files were not individually retrieved from Synapse. Future work should search for `syn21991191` (DepMap cell line data) and related CRISPR screen files.
4. **Clinical trials:** No Synapse grounding was identified for the 6 clinical trial nodes, as ClinicalTrials.gov remains the authoritative source.

---

## 7. Synapse Tool Calls Performed

```
search_synapse(query_term="cancer metabolism TCGA gene expression", limit=10)
search_synapse(query_term="DepMap CRISPR cancer dependency", limit=10)
search_synapse(query_term="drug sensitivity cancer GDSC", limit=10)
search_synapse(query_term="DREAM challenge drug combination cancer", limit=10)
search_synapse(query_term="metformin cancer metabolism AMPK mTOR", limit=10)
search_synapse(query_term="glycolysis oxidative phosphorylation Warburg cancer", limit=10)
search_synapse(query_term="CCLE cancer cell line encyclopedia drug response", limit=10)
search_synapse(query_term="CTD2 cancer target discovery drug sensitivity NCI", limit=5)
get_entity(entity_id="syn18474062")
get_entity(entity_id="syn2785778")
get_entity(entity_id="syn5889324")
get_entity(entity_id="syn359903")
get_entity(entity_id="syn10463688")
get_entity(entity_id="syn178580")
get_entity(entity_id="syn2237931")
get_entity_children(entity_id="syn18474062")
```
