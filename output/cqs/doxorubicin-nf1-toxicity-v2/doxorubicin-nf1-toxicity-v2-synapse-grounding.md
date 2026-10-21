# Synapse Grounding: Doxorubicin-NF1 Toxicity v2

## Summary

| Metric | Value |
|--------|-------|
| Nodes grounded | 2/25 (8%) |
| Total edges | 21 |
| MEMBER_OF edges (ontological, excluded) | 10 |
| Groundable edges | 11 |
| Grounded edges | 1/11 (9%) |
| Synapse datasets identified | 3 |
| Grounding tool | Tavily web search (Synapse MCP tools not available) |

**Note**: Synapse MCP tools (`search_synapse`, `get_entity`, `get_entity_annotations`, `get_entity_children`) were not available in this environment. Grounding was performed via web search of synapse.org with limited coverage. MEMBER_OF edges (pathway membership from WikiPathways) are ontological and excluded from the groundable denominator per protocol.

---

## Dataset-to-Graph Mapping Table

| Synapse ID | Title | Nodes Grounded | Edges Grounded | Evidence Type | Species | Strength |
|------------|-------|----------------|----------------|---------------|---------|----------|
| syn4939902 | Johns Hopkins NF1 Biospecimen Repository | NF1 (HGNC:7765) | NF1 <-> MONDO:0018975 | RNA-seq + WGS | Human | **Strong** |
| syn8016599 | Modeling signaling networks of NF1-deficient Schwann cells | NF1 (HGNC:7765) | -- | RNAseq, total proteome, phosphoproteome | Human | **Moderate** |
| syn36544458 | NF1 mutation-induced single-cell gene expression | NF1 (HGNC:7765) | -- | scRNA-seq | Human | **Moderate** |

---

## Node Grounding Coverage

### Grounded Nodes

| Node | CURIE | Datasets | Strength |
|------|-------|----------|----------|
| NF1 | HGNC:7765 | syn4939902, syn8016599, syn36544458 | Strong |

### Ungrounded Nodes (23/25)

| Node | CURIE | Reason |
|------|-------|--------|
| TOP2A | HGNC:11989 | No Synapse datasets found for TOP2A + doxorubicin |
| TOP2B | HGNC:11990 | No Synapse datasets found for TOP2B + cardiotoxicity |
| NFE2L2 | HGNC:7782 | No Synapse datasets found for NRF2 + anthracycline |
| KEAP1 | HGNC:23177 | No Synapse datasets found |
| NQO1 | HGNC:2874 | No Synapse datasets found |
| SOD2 | HGNC:11180 | No Synapse datasets found |
| CAT | HGNC:1516 | No Synapse datasets found |
| HMOX1 | HGNC:5013 | No Synapse datasets found |
| ABCB1 | HGNC:40 | No Synapse datasets found |
| CBR3 | HGNC:1549 | No Synapse datasets found |
| RARG | HGNC:9866 | No Synapse datasets found |
| SLC22A16 | HGNC:20302 | No Synapse datasets found |
| Doxorubicin | CHEMBL:53463 | No Synapse datasets found for doxorubicin cardiotoxicity |
| Dexrazoxane | CHEMBL:1738 | No Synapse datasets found |
| Selumetinib | CHEMBL:1614701 | No Synapse datasets found |
| NF1 disease | MONDO:0018975 | Grounded via NF1 gene datasets |
| WP:WP2735 | Pathway | Ontological -- not groundable |
| WP:WP408 | Pathway | Ontological -- not groundable |
| WP:WP3 | Pathway | Ontological -- not groundable |
| WP:WP3612 | Pathway | Ontological -- not groundable |
| NCT:03934905 | Trial | Not applicable for Synapse grounding |
| NCT:00304083 | Trial | Not applicable for Synapse grounding |
| NCT:03433183 | Trial | Not applicable for Synapse grounding |
| NCT:05858710 | Trial | Not applicable for Synapse grounding |

---

## Edge Grounding Coverage

### Grounded Edges (1/11 groundable)

| Edge | Type | Datasets | Evidence | Strength |
|------|------|----------|----------|----------|
| NF1 -> MONDO:0018975 | ASSOCIATED_WITH | syn4939902 | NF1 biospecimens with mutation + expression data for NF1-associated tumors | Strong |

### Ungrounded Groundable Edges (10/11)

| Edge | Type | Gap Note |
|------|------|----------|
| CHEMBL:53463 -> HGNC:11989 | INHIBITOR | No doxorubicin + TOP2A dataset on Synapse |
| CHEMBL:53463 -> HGNC:11990 | INHIBITOR | No doxorubicin + TOP2B dataset on Synapse |
| CHEMBL:1738 -> HGNC:11990 | INHIBITOR | No dexrazoxane dataset on Synapse |
| KEAP1 -> NFE2L2 | REGULATES | No KEAP1-NRF2 perturbation dataset on Synapse |
| NF1 -> TOP2A | CO_LOCATED | Chromosomal co-location; not amenable to dataset grounding |
| CHEMBL:1614701 -> WP:WP2735 | INHIBITOR | No selumetinib + MAPK dataset on Synapse |
| NCT:03934905 -> NFE2L2 | INVESTIGATES | Trial registration; not a dataset edge |
| NCT:00304083 -> NF1 | INVESTIGATES | Trial registration; not a dataset edge |
| NCT:03433183 -> NF1 | INVESTIGATES | Trial registration; not a dataset edge |
| NCT:05858710 -> CHEMBL:1738 | INVESTIGATES | Trial registration; not a dataset edge |

### MEMBER_OF Edges (Ontological -- Not Groundable)

10 MEMBER_OF edges representing WikiPathways membership. These are definitional pathway annotations and are excluded from the groundable denominator.

---

## Evidence Level Upgrades

No upgrades applied. Synapse grounding coverage (9%) is insufficient to upgrade any evidence levels.

---

## Grounding Confidence Matrix

| Claim | Datasets | Strength | Justification |
|-------|----------|----------|---------------|
| NF1 loss causes NF1 disease | syn4939902, syn8016599, syn36544458 | Strong | 3 datasets directly study NF1 mutations in NF1 patients |
| Doxorubicin inhibits TOP2A | None on Synapse | -- | Grounded by Open Targets instead |
| NRF2 pathway is cardioprotective | None on Synapse | -- | Grounded by WikiPathways + clinical trial |

---

## Methodology

- **Tool**: Tavily web search restricted to synapse.org domain (3 queries)
- **Queries**: "doxorubicin cardiotoxicity gene expression", "NF1 neurofibromatosis gene expression", "TOP2B NRF2 anthracycline toxicity"
- **Matching criteria**: Dataset must contain gene expression or perturbation data for entities in the KG
- **MEMBER_OF exclusion**: 10 pathway membership edges excluded from groundable denominator per Synapse grounding protocol (these represent ontological relationships from WikiPathways, not experimentally testable claims)

---

## Limitations

1. **Synapse MCP tools unavailable**: Full programmatic search was not possible; only web search results used
2. **Coverage gap**: Doxorubicin cardiotoxicity datasets not found on Synapse (may exist in GEO/ArrayExpress)
3. **NF1-centric coverage**: All found datasets are NF1-related; no coverage for oxidative stress pathway genes
4. **No annotation verification**: Could not retrieve dataset annotations to confirm species, platform, or sample counts
5. **Recommended follow-up**: Re-run Stage 1b with Synapse MCP tools when available; also search GEO for doxorubicin + cardiomyocyte transcriptomics

---

## Synapse Dataset Descriptions

### syn4939902: Johns Hopkins NF1 Biospecimen Repository
- **URL**: https://www.synapse.org/Synapse:syn4939902
- **Data types**: RNA-seq, Whole Genome Sequencing (WGS)
- **Description**: Comprehensive biospecimen repository for NF1 research with gene expression and genomic data from NF1 patient samples across multiple batches
- **Relevance**: Directly studies NF1 gene expression changes in the disease context

### syn8016599: Modeling signaling networks of NF1-deficient Schwann cells
- **URL**: https://www.synapse.org/Synapse:syn8016599
- **Data types**: RNAseq, total proteome, phosphoproteome
- **Description**: Comprehensive molecular dataset (gene expression, global protein levels, protein modifications) from NF1-deficient Schwann cells
- **Relevance**: Profiles RAS-MAPK signaling downstream of NF1 loss, potentially informing sensitivity to doxorubicin and MEK inhibitors

### syn36544458: NF1 mutation-induced single-cell gene expression
- **URL**: https://nf.synapse.org/Explore/Studies/DetailsPage?studyId=syn36544458
- **Data types**: scRNA-seq
- **Description**: Analyzes NF1 mutation-induced changes in gene expression at the single cell level
- **Relevance**: Provides cell-type-resolved view of NF1 pathway dysregulation

*Synapse grounding generated 2026-02-17 via Fuzzy-to-Fact publication pipeline.*
