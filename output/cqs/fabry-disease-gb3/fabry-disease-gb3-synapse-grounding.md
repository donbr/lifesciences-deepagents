# Fabry Disease Gb3 Knowledge Graph -- Synapse Dataset Grounding Report

**Generated**: 2026-02-27
**KG Source**: `fabry-disease-gb3-knowledge-graph-v2.json`
**Slug**: `fabry-disease-gb3`

---

## 1. Summary

| Metric | Value |
|--------|-------|
| Total KG nodes | 19 |
| Total KG edges | 24 |
| MEMBER_OF edges (excluded) | 3 |
| Groundable edges | 21 |
| Synapse searches executed | 14 |
| Unique datasets assessed | 12 |
| Datasets with grounding relevance | 8 |
| Nodes grounded (direct or contextual) | 10 / 19 (52.6%) |
| Edges grounded (direct or contextual) | 7 / 21 (33.3%) |

**Key finding**: Synapse does not host any datasets that directly study Fabry disease GLA mutations, Gb3 accumulation, or agalsidase/migalastat treatment. The "Fabry Disease" project (syn52229845) contains only clinical image files, not omics data. All grounding is therefore **indirect**, drawn from analogous lysosomal storage disorder datasets (Sandhoff, Gaucher, Pompe, prosaposin deficiency) and sphingolipid pathway profiling studies. No dataset IDs have been fabricated; all IDs below were returned by the Synapse search API and confirmed via `get_entity` and `get_entity_annotations`.

---

## 2. Dataset-to-Graph Mapping Table

| # | Synapse ID | Name | Type | Nodes Grounded | Edges Grounded | Evidence Type | Species | Samples | Grounding Strength |
|---|-----------|------|------|---------------|---------------|---------------|---------|---------|-------------------|
| 1 | syn52229845 | Fabry Disease | Project | Fabry disease (MONDO:0010526) | -- | Clinical images only | H. sapiens | 3 files | Weak |
| 2 | syn351270 | GSE19641 (Sandhoff disease Hexb-/- thymus) | Folder/GEO | HEXB, Fabry disease (LSD context) | GLA-HEXB INTERACTS_WITH (pathway context) | Microarray, gene KO | M. musculus | 2 | Moderate |
| 3 | syn353567 | GSE18745 (S1P lyase KO, sphingolipid metabolism) | Folder/GEO | Sphingolipid pathway (WP4153, WP2788) | GLA MEMBER_OF WP4153 (pathway context) | Microarray, gene KO | M. musculus | 6 | Moderate |
| 4 | syn209100 | GSE23086 (Gaucher disease type 1, GBA1 KO) | Folder/GEO | Fabry disease (LSD context), lysosomal accumulation | Gb3 ACCUMULATES_IN (analogous mechanism) | Microarray, conditional KO | M. musculus | 7 | Moderate |
| 5 | syn178276 | GSE23408 (Gaucher disease, GCase mutant mice) | Folder/GEO | Sphingolipid pathway, lysosomal accumulation | Gb3 ACCUMULATES_IN (analogous) | Microarray, point mutants | M. musculus | 39 | Moderate |
| 6 | syn205075 | GSE8307 (Prosaposin deficiency, glycosphingolipid hydrolases) | Folder/GEO | GLA (saposin activator context), sphingolipid pathway | Alpha-gal A HYDROLYZES Gb3 (activator context) | Microarray, multiple KO models | M. musculus | 68 | Moderate |
| 7 | syn25610190 | Progranulin KO Aging Mouse (GRN-/-, lysosomal proteomics) | Project | HEXB (elevated in KO), lysosomal dysfunction | GLA-HEXB INTERACTS_WITH (co-expression) | TMT mass spectrometry | M. musculus | Multi-batch | Weak |
| 8 | syn58605953 | Pompe ERT + Miglustat (Anding et al. 2023) | Project | ERT mechanism, lysosomal targeting | Drug REPLACES enzyme (analogous ERT) | Preclinical drug study | M. musculus | Multi-group | Weak |
| 9 | syn32846042 | CAGI-ARSA (Arylsulfatase A variant prediction) | Project | ARSA (variant effects) | GLA-ARSA INTERACTS_WITH (functional context) | Computational challenge, variant data | H. sapiens | Challenge | Weak |
| 10 | syn233529 | GSE21899 (Gaucher disease Types I & III, patient blood) | Folder/GEO | Fabry disease (LSD context) | -- | Microarray, human patients | H. sapiens | 14 | Weak |
| 11 | syn256935 | GSE27280 (Pompe disease, acid alpha-glucosidase) | Folder/GEO | ERT mechanism (lysosomal enzyme replacement) | Drug REPLACES enzyme (analogous) | Microarray, human | H. sapiens | 12 | Weak |
| 12 | syn2596750 | WP1424 Globo Sphingolipid Metabolism pathway analysis | File | Gb3 (globo sphingolipid pathway) | Gb3 pathway context | Pathway visualization | -- | -- | Weak |

---

## 3. Node Grounding Coverage

### Grounded Nodes (10/19)

| Node ID | Label | Type | Grounding Datasets | Strength |
|---------|-------|------|-------------------|----------|
| HGNC:4296 | GLA | Gene | syn205075 (prosaposin/saposin context), syn2596750 (globo sphingolipid pathway) | Weak -- no direct GLA profiling |
| UniProtKB:P06280 | Alpha-galactosidase A | Protein | syn205075 (glycosphingolipid hydrolase activator studies) | Weak |
| PubChem:CID66616222 | Globotriaosylceramide (Gb3) | Metabolite | syn2596750 (WP1424 Globo Sphingolipid Metabolism) | Weak |
| MONDO:0010526 | Fabry disease | Disease | syn52229845 (project exists, images only); syn209100, syn178276, syn233529, syn256935 (analogous LSDs) | Moderate (by analogy) |
| HGNC:4879 | HEXB | Gene | syn351270 (GSE19641 Hexb-/- KO), syn25610190 (Hexb elevated in GRN-/- proteomics) | Strong |
| HGNC:4878 | HEXA | Gene | syn351270 (GSE19641, Sandhoff/hexosaminidase context) | Moderate |
| HGNC:713 | ARSA | Gene | syn32846042 (CAGI-ARSA variant challenge) | Moderate |
| WP:WP4153 | Sphingolipid degradation pathway | Pathway | syn353567 (GSE18745 sphingolipid metabolism), syn205075 (GSE8307 prosaposin/saposin) | Moderate |
| WP:WP2788 | Sphingolipid metabolism | Pathway | syn353567 (GSE18745) | Moderate |
| WP:WP5292 | Glycosphingolipid metabolism | Pathway | syn2596750 (WP1424 Globo Sphingolipid) | Weak |

### Ungrounded Nodes (9/19)

| Node ID | Label | Type | Notes |
|---------|-------|------|-------|
| HGNC:7758 | NEU1 | Gene | No Synapse datasets for neuraminidase 1 / sialidosis. Search for "neuraminidase NEU1 sialidosis" returned 2 results, both unrelated (influenza glycomics). |
| CHEMBL:2108214 | Agalsidase Alfa | Drug | No Synapse datasets for Replagal. Search "agalsidase Fabry" returned only the syn52229845 image project and unrelated cell characterization projects. |
| CHEMBL:2108888 | Agalsidase Beta | Drug | No Synapse datasets for Fabrazyme. |
| CHEMBL:110458 | Migalastat | Drug | No Synapse datasets. Search "migalastat Fabry" returned only the same unrelated hits. |
| CHEMBL:4297801 | Pegunigalsidase Alfa | Drug | No Synapse datasets for Elfabrio/PRX-102. |
| CHEMBL:1086997 | Lucerastat | Drug | No Synapse datasets. "Substrate reduction therapy glucosylceramide synthase" returned only Pompe disease results. |
| NCT02795676 | BALANCE trial (PRX-102) | ClinicalTrial | No Synapse datasets. Clinical trials are not typically deposited on Synapse. |
| NCT01218659 | ATTRACT trial (Migalastat) | ClinicalTrial | No Synapse datasets. |
| NCT03425539 | MODIFY trial (Lucerastat) | ClinicalTrial | No Synapse datasets. |

---

## 4. Edge Grounding Coverage

### Grounded Edges (7/21)

| # | Edge | Type | Grounding Dataset(s) | Strength | Justification |
|---|------|------|---------------------|----------|---------------|
| 1 | GLA -> HEXB | INTERACTS_WITH | syn351270 (Hexb-/- KO with glycolipid accumulation), syn25610190 (Hexb elevated in lysosomal KO proteomics) | Moderate | Hexb-/- mouse model shows glycolipid accumulation and gene expression changes in lysosomal pathway shared with GLA. HEXB protein elevated in lysosomal dysfunction model. |
| 2 | GLA -> HEXA | INTERACTS_WITH | syn351270 (Sandhoff disease involves both HEXA/HEXB subunits in hexosaminidase complex) | Weak | The GSE19641 dataset studies Sandhoff disease (HEXB deficiency) which functionally involves both hex subunits; HEXA is not directly profiled. |
| 3 | GLA -> ARSA | INTERACTS_WITH | syn32846042 (CAGI-ARSA variant prediction challenge with functional assay data) | Weak | ARSA variant effects studied computationally; co-pathway membership with GLA in sphingolipid degradation provides contextual support. |
| 4 | Gb3 ACCUMULATES_IN Fabry disease | ACCUMULATES_IN | syn209100 (Gaucher GBA1 KO, analogous lysosomal accumulation), syn178276 (Gaucher GCase mutants, analogous glycolipid accumulation) | Moderate | Both Gaucher disease datasets demonstrate the same lysosomal glycolipid accumulation mechanism caused by lysosomal enzyme deficiency -- directly analogous to GLA deficiency causing Gb3 accumulation. |
| 5 | Alpha-gal A HYDROLYZES Gb3 | HYDROLYZES | syn205075 (prosaposin deficiency -- studies saposin activators of glycosphingolipid hydrolases including GLA) | Weak | Prosaposin encodes saposin B, which activates alpha-galactosidase A for Gb3 hydrolysis. This dataset profiles consequences of saposin loss on glycosphingolipid metabolism. |
| 6 | GLA ASSOCIATED_WITH Fabry disease | ASSOCIATED_WITH | syn52229845 (Fabry Disease project exists on Synapse), syn209100/syn178276/syn233529 (analogous LSD gene-disease associations) | Weak | The existence of a Fabry Disease project on Synapse, plus multiple analogous LSD gene-disease datasets, provides contextual grounding. |
| 7 | GLA ENCODES Alpha-gal A | ENCODES | syn205075 (prosaposin studies reference glycosphingolipid hydrolases by gene/protein) | Weak | Contextual only -- the relationship is established fact, and the prosaposin dataset references the GLA gene product functionally. |

### Ungrounded Edges (11/21)

| # | Edge | Type | Notes |
|---|------|------|-------|
| 1 | GLA -> NEU1 | INTERACTS_WITH | No NEU1-related datasets found on Synapse. |
| 2 | Agalsidase Alfa TREATS Fabry disease | TREATS | No Fabry ERT trial data on Synapse. syn58605953 (Pompe ERT) provides only analogous ERT mechanism. |
| 3 | Agalsidase Alfa REPLACES Alpha-gal A | REPLACES | No datasets. |
| 4 | Agalsidase Beta TREATS Fabry disease | TREATS | No datasets. |
| 5 | Agalsidase Beta REPLACES Alpha-gal A | REPLACES | No datasets. |
| 6 | Migalastat TREATS Fabry disease | TREATS | No datasets. |
| 7 | Migalastat CHAPERONES Alpha-gal A | CHAPERONES | No datasets. |
| 8 | Pegunigalsidase Alfa TREATS Fabry disease | TREATS | No datasets. |
| 9 | Pegunigalsidase Alfa REPLACES Alpha-gal A | REPLACES | No datasets. |
| 10 | Lucerastat TREATS Fabry disease | TREATS | No datasets. |
| 11 | Lucerastat REDUCES_SUBSTRATE Gb3 | REDUCES_SUBSTRATE | No datasets. |

### Trial EVALUATES Edges (3/21 -- Ungrounded)

| # | Edge | Type | Notes |
|---|------|------|-------|
| 1 | NCT02795676 EVALUATES Pegunigalsidase Alfa | EVALUATES | Clinical trial data not on Synapse. |
| 2 | NCT01218659 EVALUATES Migalastat | EVALUATES | Clinical trial data not on Synapse. |
| 3 | NCT03425539 EVALUATES Lucerastat | EVALUATES | Clinical trial data not on Synapse. |

### MEMBER_OF Edges (3/24 -- Ontological, Not Groundable)

| Edge | Type | Rationale |
|------|------|-----------|
| GLA -> WP4153 (Sphingolipid degradation) | MEMBER_OF | Ontological classification from WikiPathways. Pathway membership is a curated assertion, not an experimental claim requiring dataset grounding. |
| GLA -> WP2788 (Sphingolipid metabolism) | MEMBER_OF | Same rationale. |
| GLA -> WP5292 (Glycosphingolipid metabolism) | MEMBER_OF | Same rationale. |

---

## 5. Evidence Level Upgrades

The KG edges already carry database-level evidence (HGNC, UniProt, Open Targets, STRING, ClinicalTrials.gov). Synapse dataset grounding can upgrade evidence levels where experimental data directly tests the mechanistic claim.

| Edge | Original Evidence Level | Synapse Upgrade | New Level | Justification |
|------|------------------------|-----------------|-----------|---------------|
| GLA -> HEXB INTERACTS_WITH | L2 (STRING score 0.941 + text mining) | L2+ | L2 -> L2+ | syn351270 (Hexb-/- KO microarray, 2 samples) and syn25610190 (Hexb elevated in lysosomal KO proteomics by TMT-MS) provide experimental evidence for co-regulation in lysosomal pathways, supporting the STRING interaction. |
| Gb3 ACCUMULATES_IN Fabry disease | L2 (UniProt + Entrez annotation) | L2+ | L2 -> L2+ | syn209100 and syn178276 (Gaucher disease models) demonstrate the same lysosomal glycolipid accumulation mechanism with microarray profiling, providing experimental analogy. |
| GLA -> HEXA INTERACTS_WITH | L2 (STRING score 0.939) | No upgrade | L2 | syn351270 provides only indirect support (Sandhoff disease context). |
| All drug/trial edges | L1-L2 (Open Targets, ClinicalTrials.gov) | No upgrade | L1-L2 | No Fabry-specific drug datasets on Synapse. |

---

## 6. Grounding Confidence Matrix

| Claim | Supporting Datasets | Strength | Justification |
|-------|-------------------|----------|---------------|
| GLA loss-of-function causes Fabry disease | syn52229845 (project existence) | Weak | Project contains only clinical images; no omics data. No GLA mutation profiling datasets found. |
| Alpha-galactosidase A hydrolyzes Gb3 | syn205075 (prosaposin/saposin activator studies) | Weak | Indirect -- prosaposin encodes saposin B which activates alpha-gal A, but the dataset studies prosaposin deficiency, not GLA directly. |
| Gb3 accumulates in lysosomes in Fabry disease | syn209100, syn178276 (Gaucher disease analogs) | Moderate | Strong mechanistic analogy: both are lysosomal enzyme deficiencies causing glycolipid accumulation. However, Gb3-specific accumulation is not directly measured. |
| GLA interacts with HEXB in sphingolipid degradation | syn351270 (Hexb-/- KO), syn25610190 (GRN-/- proteomics with Hexb elevation) | Moderate | Hexb-/- KO shows glycolipid accumulation in a shared pathway; GRN-/- proteomics shows Hexb co-upregulation with other lysosomal enzymes. |
| GLA interacts with ARSA in sphingolipid degradation | syn32846042 (CAGI-ARSA variant challenge) | Weak | Computational variant prediction, not direct protein-protein interaction data. Co-pathway membership is the primary basis. |
| Agalsidase/Migalastat treat Fabry disease | None directly; syn58605953 (Pompe ERT analogy) | Weak | Pompe ERT study provides analogous ERT mechanism evidence (lysosomal enzyme targeting via M6P receptor), but studies a different enzyme and disease. |
| Lucerastat reduces Gb3 via SRT | None | Ungrounded | No substrate reduction therapy datasets found on Synapse for Fabry disease. |
| Clinical trials evaluate Fabry drugs | None | Ungrounded | Clinical trial data is not typically deposited on Synapse. |
| Sphingolipid pathway membership | syn353567 (S1P lyase KO sphingolipid profiling) | Moderate | Demonstrates sphingolipid pathway disruption with gene expression consequences, supporting pathway biology relevant to GLA. |

---

## 7. Methodology

### Tools Used
- **mcp__synapse__search_synapse**: Keyword search across all Synapse entities (projects, folders, files, datasets)
- **mcp__synapse__get_entity**: Retrieve full metadata (name, type, creation date, parent) for each hit
- **mcp__synapse__get_entity_annotations**: Retrieve structured annotations (species, platform, numSamples, repository, tissueType, disease)
- **mcp__synapse__get_entity_children**: Explore container contents

### Search Queries Executed

| # | Query | Hits Found | Relevant Hits |
|---|-------|-----------|---------------|
| 1 | "Fabry disease GLA" | 3,425 | 2 (syn52229845, syn52229903) |
| 2 | "globotriaosylceramide Gb3" | 0 | 0 |
| 3 | "alpha-galactosidase" | 567 | 0 (all beta-galactosidase or alpha-diversity hits) |
| 4 | "lysosomal storage sphingolipid" | 236 | 4 (syn353567, syn351270, syn52504936, syn25610190) |
| 5 | "agalsidase Fabry" | 5 | 1 (syn52229845 -- images only) |
| 6 | "migalastat Fabry" | 5 | 1 (syn52229845 -- images only) |
| 7 | "ARSA HEXB HEXA lysosomal" | 43 | 3 (syn351270, syn32846042, syn25610190) |
| 8 | "Fabry disease enzyme replacement" | 3,657 | 2 (syn58605953 Pompe ERT, syn52229845) |
| 9 | "GLA gene mutation lysosomal" | 10,000+ | 0 (all generic gene/mutation hits) |
| 10 | "Sandhoff disease Hexb knockout" | 3,894 | 2 (syn351270, syn351271) |
| 11 | "sphingolipid degradation pathway ceramide glycolipid" | 1,435 | 2 (syn353567, syn205075) |
| 12 | "Gaucher disease glucocerebrosidase sphingolipid" | 3,435 | 4 (syn178276, syn209100, syn233529, syn205075) |
| 13 | "neuraminidase NEU1 sialidosis" | 2 | 0 (both influenza-related) |
| 14 | "substrate reduction therapy glucosylceramide synthase" | 1,316 | 1 (syn58605953 -- Pompe, not Fabry) |

### Matching Criteria
- **Direct match**: Dataset explicitly studies the KG entity (gene, protein, disease, drug, or trial)
- **Analogous match**: Dataset studies the same biological mechanism in a related disease (e.g., Gaucher glycolipid accumulation as analog for Fabry Gb3 accumulation)
- **Pathway match**: Dataset profiles a pathway that includes the KG entity

### MEMBER_OF Edge Exclusion Rationale
MEMBER_OF edges encode ontological relationships (gene membership in a curated pathway from WikiPathways). These are definitional assertions, not experimental claims. A dataset cannot "ground" the fact that GLA is a member of WP4153; it can only confirm that the pathway exists and functions as described. Therefore, MEMBER_OF edges are excluded from the grounding denominator. The 3 MEMBER_OF edges (GLA -> WP4153, GLA -> WP2788, GLA -> WP5292) reduce the groundable edge count from 24 to 21.

---

## 8. Limitations

### Coverage Gaps
1. **No Fabry-specific omics datasets on Synapse**: The syn52229845 "Fabry Disease" project contains only clinical images (JPGs), not gene expression, proteomics, or metabolomics data. This is the most significant limitation.
2. **No drug treatment datasets**: None of the 5 drugs in the KG (agalsidase alfa/beta, migalastat, pegunigalsidase alfa, lucerastat) have treatment datasets on Synapse. Fabry ERT and chaperone therapy data may exist in other repositories (GEO, dbGaP, EGA).
3. **No clinical trial data**: Clinical trial datasets are typically deposited in clinicaltrials.gov, dbGaP, or sponsor portals -- not Synapse.
4. **NEU1 gap**: No datasets for neuraminidase 1 / sialidosis found on Synapse. The GLA-NEU1 interaction edge remains ungrounded.

### Cross-Species Issues
- All grounding datasets with direct experimental evidence are murine (M. musculus), not human. While lysosomal storage disease mechanisms are well-conserved across species, species-specific differences in glycosphingolipid metabolism, enzyme kinetics, and tissue distribution exist.
- Human datasets found (syn233529 GSE21899, syn256935 GSE27280) are for Gaucher/Pompe disease, not Fabry disease.

### Platform Age
- Most GEO datasets mirrored on Synapse use legacy microarray platforms (Affymetrix Mouse430_2, HGU133A2) from 2012 era. Modern RNA-seq or single-cell data for lysosomal storage diseases may exist on GEO/SRA but are not indexed on Synapse.

### Specificity Gaps
- **Gb3-specific measurement**: No dataset directly measures Gb3 (globotriaosylceramide) levels. The glycosphingolipid pathway datasets measure other sphingolipids (ceramide, sphingomyelin, S1P).
- **GLA enzyme activity**: No datasets with alpha-galactosidase A enzyme activity assays found on Synapse.
- **Pharmacological chaperone mechanism**: Migalastat's chaperone mechanism (stabilizing misfolded GLA mutants) is not testable with any available Synapse dataset.

### Recommendations for Improved Grounding
1. Search GEO directly for "Fabry disease" microarray/RNA-seq studies (likely GSE datasets not mirrored on Synapse)
2. Search dbGaP for Fabry disease patient cohort genomics data
3. Search EGA for European Fabry disease registries
4. Search Metabolomics Workbench for Gb3/lyso-Gb3 metabolomics datasets
5. The CAGI-ARSA project (syn32846042) suggests the CAGI framework could be extended to GLA variant prediction, which would provide direct grounding for the GLA-Fabry association

---

*Report generated by Synapse MCP tool-assisted search. All Synapse entity IDs verified via `get_entity` and `get_entity_annotations` API calls. No dataset IDs were fabricated.*
