# TUBB4A-v1: Synapse Grounding Report

**Competency Question:** "Which therapeutic interventions, clinical phenotypes, and biological pathways are connected to the TUBB4A gene in the context of Hypomyelination with Atrophy of the Basal ganglia and Cerebellum (H-ABC), and how do its molecular interactions explain the disease pathology?"

**Disease Focus:** Hypomyelination with atrophy of basal ganglia and cerebellum (MONDO:0012905)

**Date Generated:** 2026-02-22

---

> **STATUS: PENDING** -- Synapse.org MCP server unavailable (system maintenance 2026-02-22). This document captures the planned grounding strategy. All `synapse_grounding` arrays in the knowledge graph JSON are empty and will be populated when the Synapse MCP tools become available again.

---

## 1. Summary

Synapse grounding has **not yet been performed** for the TUBB4A-v1 knowledge graph due to Synapse.org MCP server unavailability during system maintenance. This document outlines the planned search strategy, expected coverage targets, and methodology that will be used when the service is restored.

The TUBB4A-v1 knowledge graph contains **27 nodes** (8 genes, 1 protein, 2 diseases, 1 drug target, 1 compound, 10 pathways, 4 clinical trials) and **27 edges** (1 ENCODES, 2 ASSOCIATED_WITH, 7 INTERACTS, 1 MODULATOR, 1 TREATS, 11 MEMBER_OF, 4 STUDIES).

**MEMBER_OF exclusion:** 11 of 27 edges are MEMBER_OF type (gene-to-pathway membership). These represent curated WikiPathways annotations and are not expected to have direct Synapse dataset counterparts. This leaves **16 groundable edges** for Synapse dataset linking.

---

## 2. Planned Search Queries

The following queries will be executed via `search_synapse` MCP tool when the service is restored:

| # | Query | Rationale | Expected Target Nodes |
|---|-------|-----------|----------------------|
| 1 | `TUBB4A leukodystrophy hypomyelination` | Direct disease-gene search for H-ABC datasets | TUBB4A (HGNC:20774), H-ABC (Orphanet:139441) |
| 2 | `tubulin oligodendrocyte myelination` | Oligodendrocyte biology datasets relevant to disease mechanism | TUBB4A, TUBA4A, Tubulin beta-4A chain protein |
| 3 | `microtubule tau brain expression` | Microtubule-associated protein datasets for interaction partners | MAPT (HGNC:6893), TUBB4A, DYNC1I1 |
| 4 | `H-ABC hypomyelination basal ganglia cerebellum MRI` | Neuroimaging or clinical phenotype datasets | H-ABC (Orphanet:139441), DYT4 (Orphanet:98805) |
| 5 | `TUBB4A expression brain single cell RNA-seq` | Brain cell-type expression data for TUBB4A | TUBB4A, TUBB4B (HGNC:20771) |
| 6 | `antisense oligonucleotide ASO leukodystrophy` | ASO therapeutic datasets for rare neurological diseases | nL-TUBB4-001 (ASO:nL-TUBB4-001) |
| 7 | `dystonia DYT tubulin` | Dystonia phenotype datasets linking tubulin mutations | DYT4 (Orphanet:98805), TOR1A (HGNC:3098) |
| 8 | `connexin gap junction microtubule trafficking` | GJA1/connexin-43 microtubule interaction datasets | GJA1 (HGNC:4274) |
| 9 | `tubulin post-translational modifications acetylation` | Tubulin PTM datasets relevant to WP4075 pathway | TUBB4A, Tubulin beta-4A chain protein |
| 10 | `leukodystrophy whole genome sequencing rare disease` | WGS/genomic datasets for leukodystrophies | H-ABC, LeukoSEQ trial context |

---

## 3. Expected Node Coverage

### 3.1 Gene Nodes (8 genes)

| Gene | ID | Expected Synapse Coverage | Search Queries |
|------|----|--------------------------|----------------|
| TUBB4A | HGNC:20774 | HIGH -- primary query target | #1, #2, #5, #9 |
| TUBA4A | HGNC:12407 | MEDIUM -- alpha-tubulin heterodimer partner | #2, #5 |
| MAPT | HGNC:6893 | MEDIUM -- microtubule-associated protein, well-studied | #3 |
| TOR1A | HGNC:3098 | LOW -- dystonia gene, tangential | #7 |
| GJA1 | HGNC:4274 | LOW -- connexin, indirect microtubule link | #8 |
| ARHGEF2 | HGNC:682 | LOW -- microtubule-sequestered GEF, niche | (none planned) |
| TUBB4B | HGNC:20771 | MEDIUM -- paralogous isoform, brain expression | #5 |
| DYNC1I1 | HGNC:2963 | LOW -- dynein motor protein, broad | #3 |

### 3.2 Protein Node (1 protein)

| Protein | ID | Expected Synapse Coverage | Search Queries |
|---------|----|--------------------------|----------------|
| Tubulin beta-4A chain | UniProtKB:P04350 | MEDIUM -- may appear in proteomics datasets | #2, #9 |

### 3.3 Disease Nodes (2 diseases)

| Disease | ID | Expected Synapse Coverage | Search Queries |
|---------|----|--------------------------|----------------|
| H-ABC | Orphanet:139441 | MEDIUM -- rare disease, limited public data | #1, #4, #10 |
| DYT4 | Orphanet:98805 | LOW -- very rare dystonia subtype | #7 |

### 3.4 Target and Compound Nodes

| Entity | ID | Expected Synapse Coverage | Search Queries |
|--------|----|--------------------------|----------------|
| Tubulin beta-4A (drug target) | CHEMBL:CHEMBL3838 | LOW -- broad oncology target, not H-ABC specific | (none planned) |
| nL-TUBB4-001 | ASO:nL-TUBB4-001 | LOW -- N-of-1 investigational compound, unlikely in Synapse | #6 |

### 3.5 Pathway Nodes (8 pathways)

| Pathway | ID | Expected Synapse Coverage | Notes |
|---------|----|--------------------------|-------|
| Mitotic Prometaphase | WP:WP2652 | LOW | Generic cell cycle pathway |
| Protein folding | WP:WP1892 | LOW | Generic chaperone pathway |
| Cilium Assembly | WP:WP4124 | LOW | Ciliopathy datasets possible |
| Carboxyterminal PTMs of tubulin | WP:WP4075 | MEDIUM | Tubulin PTM datasets (#9) |
| Mitotic G2-G2/M phases | WP:WP1859 | LOW | Generic cell cycle pathway |
| Parkin-ubiquitin proteasomal system | WP:WP2359 | LOW | Neurodegeneration datasets possible |
| Microtubule cytoskeleton regulation | WP:WP2038 | MEDIUM | Microtubule biology datasets (#3) |
| Alzheimer's disease and miRNA effects | WP:WP2059 | MEDIUM | AD/tau datasets may cover TUBB4A+MAPT (#3) |

### 3.6 Clinical Trial Nodes (4 trials)

Clinical trials are grounded to ClinicalTrials.gov as the authoritative source and are **not expected** to have direct Synapse dataset counterparts. No Synapse grounding will be applied to trial nodes.

| Trial | ID | Synapse Grounding |
|-------|----|--------------------|
| nL-TUBB4-001 ASO for TUBB4A Leukodystrophy (UCSD) | NCT:07222371 | Not applicable |
| ASO Treatment for TUBB4A Leukodystrophy (MGH) | NCT:06369974 | Not applicable |
| LeukoSEQ: WGS for Leukodystrophies (CHOP) | NCT:02699190 | Not applicable |
| Myelin Disorders Biorepository (CHOP) | NCT:03047369 | Not applicable |

---

## 4. Expected Edge Coverage

### 4.1 Groundable Edges (16 of 25)

| Edge Type | Count | Example | Expected Synapse Relevance |
|-----------|-------|---------|---------------------------|
| ENCODES (Gene to Protein) | 1 | TUBB4A -> Tubulin beta-4A chain | MEDIUM -- proteomics/expression datasets |
| ASSOCIATED_WITH (Gene to Disease) | 2 | TUBB4A -> H-ABC | MEDIUM -- rare disease genomics datasets |
| INTERACTS (Gene to Gene) | 7 | TUBB4A -> TUBA4A (score 0.983) | MEDIUM -- PPI/coexpression datasets |
| MODULATOR (Compound to Gene) | 1 | nL-TUBB4-001 -> TUBB4A | LOW -- N-of-1 ASO, unlikely in Synapse |
| TREATS (Compound to Disease) | 1 | nL-TUBB4-001 -> H-ABC | LOW -- investigational compound |
| STUDIES (Trial to Disease) | 4 | NCT:07222371 -> H-ABC | Not applicable (ClinicalTrials.gov source) |

### 4.2 Excluded Edges: MEMBER_OF (9 of 25)

MEMBER_OF edges represent gene-to-pathway membership from WikiPathways. These are curated annotations and do not require Synapse dataset grounding.

| Source | Target | Type |
|--------|--------|------|
| TUBB4A (HGNC:20774) | Mitotic Prometaphase (WP:WP2652) | MEMBER_OF |
| TUBB4A (HGNC:20774) | Protein folding (WP:WP1892) | MEMBER_OF |
| TUBB4A (HGNC:20774) | Cilium Assembly (WP:WP4124) | MEMBER_OF |
| TUBB4A (HGNC:20774) | Carboxyterminal PTMs of tubulin (WP:WP4075) | MEMBER_OF |
| TUBB4A (HGNC:20774) | Mitotic G2-G2/M phases (WP:WP1859) | MEMBER_OF |
| TUBB4A (HGNC:20774) | Parkin-ubiquitin proteasomal system (WP:WP2359) | MEMBER_OF |
| MAPT (HGNC:6893) | Microtubule cytoskeleton regulation (WP:WP2038) | MEMBER_OF |
| MAPT (HGNC:6893) | Alzheimer's disease and miRNA effects (WP:WP2059) | MEMBER_OF |
| TUBB4A (HGNC:20774) | Alzheimer's disease and miRNA effects (WP:WP2059) | MEMBER_OF |

---

## 5. Methodology

### 5.1 Tools

The following Synapse MCP tools will be used when available:

| Tool | Purpose | Expected Usage |
|------|---------|----------------|
| `search_synapse(query_term, limit)` | Search Synapse.org for datasets matching keyword queries | 10 planned queries (Section 2) |
| `get_entity(entity_id)` | Verify entity metadata (name, type, parent project) | For each selected Synapse ID |
| `get_entity_children(entity_id)` | List child entities within folders/projects | For folders containing relevant sub-datasets |

### 5.2 Selection Criteria

Synapse entities will be selected based on:

1. **Direct relevance** -- Dataset must contain data about one or more KG entities (genes, proteins, diseases, compounds)
2. **Entity type** -- Prefer Projects and Folders with curated experimental data over individual files
3. **Data modality** -- Prioritize transcriptomic (RNA-seq, microarray), genomic (WGS, WES), and proteomic datasets
4. **Disease specificity** -- Datasets specific to leukodystrophies, myelination disorders, or tubulinopathies receive priority over generic datasets
5. **Recency** -- More recent datasets preferred when multiple options exist

### 5.3 Grounding Assignment Rules

- Each node can receive 0-3 Synapse grounding entries
- Each grounding entry includes: `synapse_id`, `name`, and `relevance` (brief rationale)
- Edges inherit grounding from their source/target nodes where the dataset validates the relationship
- Clinical trial nodes are excluded from Synapse grounding (ClinicalTrials.gov is authoritative)
- MEMBER_OF edges are excluded from Synapse grounding (WikiPathways is authoritative)

---

## 6. Expected Challenges

1. **Rare disease data scarcity:** H-ABC (MONDO:0012905) is an ultra-rare disease. Synapse.org may have limited or no datasets specifically focused on H-ABC or TUBB4A leukodystrophy. Brain expression atlases (e.g., Allen Brain Atlas on Synapse, BrainSpan) may provide indirect grounding.

2. **N-of-1 therapeutic:** The nL-TUBB4-001 ASO is an investigational N-of-1 compound from the n-Lorem Foundation. Clinical data from the two active trials is unlikely to be deposited on Synapse during the study period.

3. **Tubulin breadth:** TUBB4A is part of a large tubulin gene family. Synapse searches for "tubulin" may return many oncology-focused datasets (tubulin as a chemotherapy target) that are not relevant to H-ABC disease context.

4. **Interaction partner coverage:** Several interaction partners (ARHGEF2, DYNC1I1, TOR1A) are linked to TUBB4A through STRING protein-protein interactions but may not appear in disease-specific Synapse datasets.

---

## 7. Synapse Tool Calls (Planned)

```
# Primary disease-gene searches
search_synapse(query_term="TUBB4A leukodystrophy hypomyelination", limit=10)
search_synapse(query_term="tubulin oligodendrocyte myelination", limit=10)
search_synapse(query_term="microtubule tau brain expression", limit=10)
search_synapse(query_term="H-ABC hypomyelination basal ganglia cerebellum MRI", limit=10)
search_synapse(query_term="TUBB4A expression brain single cell RNA-seq", limit=10)

# Therapeutic and phenotype searches
search_synapse(query_term="antisense oligonucleotide ASO leukodystrophy", limit=10)
search_synapse(query_term="dystonia DYT tubulin", limit=10)
search_synapse(query_term="connexin gap junction microtubule trafficking", limit=10)

# Pathway-specific searches
search_synapse(query_term="tubulin post-translational modifications acetylation", limit=10)
search_synapse(query_term="leukodystrophy whole genome sequencing rare disease", limit=10)

# Entity verification (to be executed for each selected Synapse ID)
# get_entity(entity_id="syn...")
# get_entity_children(entity_id="syn...")
```
