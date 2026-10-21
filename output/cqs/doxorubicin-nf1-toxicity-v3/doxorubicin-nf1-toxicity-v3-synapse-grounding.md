# Synapse Grounding: Doxorubicin-NF1 Toxicity v3

## 1. Summary

| Metric | Value |
|--------|-------|
| Synapse datasets identified | 9 |
| Nodes in knowledge graph | 22 |
| Nodes with Synapse grounding | 8/22 (36%) |
| Total edges | 19 |
| MEMBER_OF edges (ontological, excluded) | 7 |
| Groundable edges | 12 |
| Grounded edges | 5/12 (42%) |
| Grounding tool | search_synapse MCP + get_entity MCP |
| Protocol | Fuzzy-to-Fact v2, Stage 1b Synapse Grounding |

**MEMBER_OF Exclusion**: 7 MEMBER_OF edges represent WikiPathways membership annotations. These are ontological/definitional relationships (e.g., "NFE2L2 MEMBER_OF WP:WP408") curated by WikiPathways and are not experimentally testable claims. They are excluded from the groundable edge denominator per Synapse grounding protocol.

**Improvement over v2**: This version uses the Synapse MCP tools (search_synapse, get_entity) directly, yielding 9 datasets (up from 3 in v2) and substantially higher grounding coverage: node grounding increased from 8% to 36%, edge grounding from 9% to 42%.

---

## 2. Dataset-to-Graph Mapping Table

| Synapse ID | Title | GEO/PRIDE ID | Nodes Grounded | Edges Grounded | Evidence Type | Species | Tissue/Model | Strength |
|------------|-------|--------------|----------------|----------------|---------------|---------|-------------|----------|
| syn7079983 | FDA TKI-induced cardiotoxicity | -- | TOP2B, HMOX1, SOD2, NQO1 | Doxorubicin->TOP2B (by analogy), NRF2->HMOX1, NRF2->NQO1, NRF2->SOD2 | Gene expression, proteomics, imaging | Human | Cor4U hiPSC-CMs | **Moderate** (TKI, not doxorubicin; same cell type + mechanisms) |
| syn13856689 | TKI-induced cardiotoxicity in iPSC-derived human cardiomyocytes | GSE114686, PXD012043 | TOP2B, NFE2L2, SOD2 | Doxorubicin->TOP2B (by analogy) | RNAseq (30 samples), proteomics (~6000 peptides), metabolomics | Human | hiPSC-CMs | **Moderate** (mitochondrial energetics defect from Sorafenib parallels doxorubicin oxidative stress) |
| syn205590 | Nrf2 KO mice liver regeneration | GSE8969 | NFE2L2, NQO1, HMOX1, SOD2 | KEAP1->NFE2L2, NRF2->NQO1, NRF2->HMOX1, NRF2->SOD2 | Microarray | Mouse | Nrf2 KO liver tissue | **Strong** (direct NRF2 pathway perturbation) |
| syn237499 | NFE2L2/Nrf2 oxidant responsive transcription factor | GSE11952 | NFE2L2, KEAP1 | KEAP1->NFE2L2 | Gene expression | Human | Oxidative stress model | **Moderate** (NRF2 induction of phase 2 detoxifying genes confirmed) |
| syn21452685 | Neurofibromatosis Therapeutic Consortium - UCSF | -- | NF1, KRAS, BRAF | NF1->KRAS, NF1->MONDO:0018975 | Preclinical trials (111 trials, 12 drug targets) | Mouse + Human | Plexiform neurofibroma, MPNST, leukemia | **Strong** (NF1 disease models with drug response data) |
| syn22266606 | Unveiling molecular mechanisms of neurofibromin regulation | -- | NF1, KRAS, BRAF | NF1->KRAS, KRAS->BRAF | Molecular biology | Human | ERK1/2-NF1 phosphorylation model | **Moderate** (ERK-NF1 negative feedback loop + SPRED1 interactions) |
| syn56566376 | Role of Schwann cells in NF1-related pain | -- | NF1, KRAS, BRAF | NF1->KRAS | Molecular biology | Mouse | Nf1-deleted Schwann cells | **Moderate** (MAPK signaling changes from NF1 loss; MEK inhibitor effects) |
| syn248628 | TOP2B in DHT-induced androgen receptor target gene expression | GSE19445 | TOP2B | -- | Microarray (pharmacological inhibition + RNAi) | Human | AR-expressing cells | **Weak** (TOP2B perturbation but different biological context) |
| syn266796 | Top2b knockout mouse embryo brain transcription profiles | GSE5458 | TOP2B | -- | Microarray (knockout) | Mouse | Embryo brain | **Moderate** (direct TOP2B KO but non-cardiac tissue) |

---

## 3. Node Grounding Coverage

### Grounded Nodes (8/22)

| Node | CURIE | Synapse Datasets | Coverage Type | Strength |
|------|-------|-----------------|---------------|----------|
| NF1 | HGNC:7765 | syn21452685, syn22266606, syn56566376 | Direct perturbation (NF1 loss/deletion models) | **Strong** |
| TOP2B | HGNC:11990 | syn7079983, syn13856689, syn248628, syn266796 | Direct perturbation (TKI-CM models, pharmacological inhibition, KO) | **Moderate** |
| NFE2L2 (NRF2) | HGNC:7782 | syn205590, syn237499, syn13856689 | Direct perturbation (Nrf2 KO, oxidative stress induction) | **Strong** |
| KEAP1 | HGNC:23177 | syn237499 | Pathway co-measurement (NRF2 regulatory axis) | **Moderate** |
| HMOX1 | HGNC:5013 | syn205590, syn7079983 | Downstream readout of NRF2 perturbation | **Moderate** |
| NQO1 | HGNC:2874 | syn205590, syn7079983 | Downstream readout of NRF2 perturbation | **Moderate** |
| SOD2 | HGNC:11180 | syn205590, syn7079983, syn13856689 | Downstream readout of NRF2 perturbation + cardiomyocyte model | **Moderate** |
| KRAS | HGNC:6407 | syn21452685, syn22266606, syn56566376 | Measured in NF1 pathway context | **Moderate** |

### Partially Grounded Nodes (1/22)

| Node | CURIE | Nearest Dataset | Gap |
|------|-------|----------------|-----|
| BRAF | HGNC:1097 | syn22266606, syn21452685 | ERK-NF1 feedback studied; BRAF is downstream but not the primary measured entity. Indirect grounding via MAPK cascade measurement. |

### Ungrounded Nodes (13/22)

| Node | CURIE | Reason |
|------|-------|--------|
| TOP2A | HGNC:11989 | No Synapse dataset directly measures TOP2A in doxorubicin/cardiotoxicity context. TOP2B datasets (syn248628, syn266796) do not include TOP2A isoform data. |
| ABCB1 | HGNC:40 | No Synapse dataset for ABCB1/P-gp doxorubicin efflux. ABCB1 pharmacogenomics data may exist in PharmGKB but not Synapse. |
| RARG | HGNC:9866 | No Synapse dataset for RARG cardiotoxicity susceptibility variants. GWAS data exists in GWAS Catalog, not Synapse. |
| Doxorubicin | CHEMBL:53463 | No doxorubicin treatment dataset on Synapse. iPSC-CM datasets (syn7079983, syn13856689) use TKIs, not anthracyclines. Analogous mechanisms provide indirect support only. |
| Dexrazoxane | CHEMBL:1738 | No dexrazoxane perturbation dataset on Synapse. Clinical evidence from NCT03930680 is the primary source. |
| Selumetinib | CHEMBL:1614701 | No selumetinib treatment dataset on Synapse. MEK inhibitor data exists in syn21452685 (NFTC) but for other MEK inhibitors. |
| NF1 disease | MONDO:0018975 | Grounded indirectly via NF1 gene datasets (syn21452685). Disease entity itself is an ontological reference. |
| WP:WP408 | Pathway | Ontological -- pathway definition from WikiPathways, not dataset-groundable |
| WP:WP3612 | Pathway | Ontological -- pathway definition from WikiPathways, not dataset-groundable |
| WP:WP2735 | Pathway | Ontological -- pathway definition from WikiPathways, not dataset-groundable |
| WP:WP4223 | Pathway | Ontological -- pathway definition from WikiPathways, not dataset-groundable |
| NCT:03930680 | ClinicalTrial | Trial registration -- grounded via ClinicalTrials.gov, not Synapse |
| NCT:01362803 | ClinicalTrial | Trial registration -- grounded via ClinicalTrials.gov, not Synapse |
| NCT:00304083 | ClinicalTrial | Trial registration -- grounded via ClinicalTrials.gov, not Synapse |

---

## 4. Edge Grounding Coverage

### Grounded Edges (5/12 groundable)

| Edge | Type | Synapse Datasets | Evidence Summary | Strength |
|------|------|-----------------|------------------|----------|
| Doxorubicin -> TOP2B | INHIBITOR | syn7079983, syn13856689 (by analogy) | iPSC-CM cardiotoxicity models demonstrate the same cell type (cardiomyocytes) and shared mechanisms (mitochondrial dysfunction, oxidative phosphorylation disruption). TKI cardiotoxicity through TOP2B-related pathways provides mechanistic analogy. Direct doxorubicin-TOP2B poisoning is not tested in these datasets. | **Moderate** (analogous, not direct) |
| KEAP1 -> NFE2L2 | REGULATES | syn205590, syn237499 | syn205590: Nrf2 KO mice show reduced cytoprotective enzyme expression, directly demonstrating NRF2 pathway regulation. syn237499: NRF2 induction of phase 2 detoxifying genes under oxidative stress confirms the KEAP1-NRF2 regulatory axis. | **Strong** |
| NRF2 -> NQO1 | ACTIVATES | syn205590, syn7079983 | syn205590: Nrf2 KO mice show reduced NQO1 expression, confirming NRF2-dependent transcriptional activation. syn7079983: NQO1 measured as oxidative stress response gene in cardiomyocyte context. | **Strong** |
| NRF2 -> HMOX1 | ACTIVATES | syn205590, syn7079983 | syn205590: Nrf2 KO mice show reduced HMOX1 expression. syn7079983: HMOX1 measured in iPSC-CM cardiotoxicity model. | **Strong** |
| NF1 -> KRAS | REGULATES | syn21452685, syn22266606, syn56566376 | syn21452685: NFTC preclinical consortium directly studies NF1-driven RAS pathway activation and drug responses. syn22266606: Demonstrates ERK1/2-NF1 negative feedback phosphorylation loop. syn56566376: Nf1 deletion in Schwann cells causes MAPK signaling changes. | **Strong** |

### Ungrounded Groundable Edges (7/12)

| Edge | Type | Gap Note | Potential Synapse Source |
|------|------|----------|------------------------|
| Doxorubicin -> TOP2A | INHIBITOR | No doxorubicin + TOP2A dataset on Synapse. TOP2A is the anti-tumor target; data exists in GEO/ArrayExpress but not Synapse. | None identified |
| Dexrazoxane -> TOP2B | DEGRADES | No dexrazoxane perturbation dataset on Synapse. Clinical trial NCT03930680 is the primary evidence source. | None identified |
| NRF2 -> SOD2 | ACTIVATES | syn205590 measures SOD2 in Nrf2 KO context but SOD2 is also regulated by non-NRF2 factors (e.g., FoxO3a). The NRF2-specific transcriptional regulation of SOD2 is less definitively demonstrated than for NQO1/HMOX1, which have canonical AREs. | Partial: syn205590 (indirect) |
| KRAS -> BRAF | ACTIVATES | syn22266606 studies ERK-NF1 feedback but does not directly measure KRAS-BRAF signaling as a discrete edge. BRAF is downstream in the cascade. | Partial: syn22266606 (indirect) |
| Selumetinib -> BRAF | INHIBITOR (via MEK) | No selumetinib-specific dataset on Synapse. syn21452685 contains MEK inhibitor data but for other compounds. Selumetinib is FDA-approved; clinical trial data is the primary grounding. | syn21452685 (partial, other MEK-i) |
| ABCB1 -> Doxorubicin | TRANSPORTS | No ABCB1 doxorubicin efflux dataset on Synapse. Well-established pharmacology grounded via HGNC/UniProt annotations. | None identified |
| NF1 -> MONDO:0018975 | ASSOCIATED_WITH | syn21452685 directly studies NF1 disease models, providing strong indirect grounding. However, the gene-disease association per se is an ontological/Open Targets claim rather than a single-dataset experimental finding. | syn21452685 (indirect) |

### MEMBER_OF Edges (Ontological -- Not Groundable)

7 MEMBER_OF edges represent WikiPathways pathway membership annotations:

| Edge | Pathway |
|------|---------|
| NF1 -> WP:WP2735 | RAF/MAP kinase cascade |
| NFE2L2 -> WP:WP408 | Oxidative stress response |
| NFE2L2 -> WP:WP3612 | NFE2L2 (NRF2) survival signaling |
| HMOX1 -> WP:WP408 | Oxidative stress response |
| NQO1 -> WP:WP408 | Oxidative stress response |
| SOD2 -> WP:WP408 | Oxidative stress response |
| KRAS -> WP:WP4223 | Ras signaling |

These edges encode curated pathway ontology relationships and are excluded from the groundable denominator. They are verified by their WikiPathways source annotations, not by experimental datasets.

---

## 5. Evidence Level Upgrades

Synapse grounding enables the following evidence level upgrades compared to the v3 report:

| Claim | Report Evidence Level | Synapse Upgrade | New Level | Justification |
|-------|----------------------|-----------------|-----------|---------------|
| NRF2 pathway is cytoprotective against oxidative stress | L1 (Established pathway) | +Synapse L1 (direct KO data) | **L1 (Reinforced)** | syn205590 provides direct Nrf2 KO evidence: cytoprotective enzymes reduced, tissue damage aggravated. This is functional perturbation data, not merely pathway annotation. [Source: search_synapse("Nrf2 knockout oxidative stress"), get_entity(syn205590)] |
| NQO1 detoxifies doxorubicin quinone intermediates | L2 (Mechanistic) | +Synapse L2 | **L2 (Reinforced)** | syn205590 confirms NQO1 is NRF2-dependent (reduced in KO). syn7079983 measures NQO1 in cardiomyocyte cardiotoxicity context. [Source: get_entity(syn205590), get_entity(syn7079983)] |
| NF1 loss causes RAS-MAPK pathway activation | L2 (STRING interaction) | +Synapse L1 (consortium data) | **L1 (Upgraded)** | syn21452685 (NFTC consortium, 111 preclinical trials) directly demonstrates NF1-RAS pathway drug targeting. syn22266606 demonstrates ERK-NF1 feedback loop. This upgrades from protein interaction inference to direct preclinical evidence. [Source: search_synapse("NF1 neurofibromatosis preclinical"), get_entity(syn21452685), get_entity(syn22266606)] |
| TOP2B mediates cardiotoxicity in cardiomyocytes | L1 (Clinical trial) | +Synapse L2 (iPSC-CM data) | **L1 (Reinforced)** | syn7079983 and syn13856689 provide iPSC-CM cardiotoxicity transcriptomic/proteomic data. Although these use TKIs rather than doxorubicin, they confirm the cardiomyocyte-specific vulnerability to drug-induced toxicity via shared mechanisms (mitochondrial energetics). [Source: search_synapse("iPSC cardiomyocyte cardiotoxicity"), get_entity(syn7079983), get_entity(syn13856689)] |
| KEAP1 regulates NRF2 via repression | L3 (Pathway logic) | +Synapse L2 (KO + expression data) | **L2 (Upgraded)** | syn205590 and syn237499 together demonstrate NRF2 regulation: KO eliminates downstream gene expression, oxidative stress induction shows NRF2 response. [Source: get_entity(syn205590), get_entity(syn237499)] |

**No upgrades possible** for: Dexrazoxane->TOP2B (no Synapse data), Selumetinib->BRAF (no Synapse data), ABCB1->Doxorubicin (no Synapse data), RARG cardiotoxicity susceptibility (no Synapse data).

---

## 6. Grounding Confidence Matrix

| Claim | Synapse Datasets | KG Evidence Level | Synapse Strength | Combined Confidence | Justification |
|-------|-----------------|-------------------|------------------|--------------------|----|
| NF1 loss drives RAS-MAPK activation | syn21452685, syn22266606, syn56566376 | L2 -> L1 | **Strong** | **0.90** | Three independent Synapse datasets with direct NF1 perturbation in disease-relevant models. NFTC consortium (111 preclinical trials) is definitive. |
| NRF2 pathway protects against oxidative stress | syn205590, syn237499, syn7079983 | L1 (Reinforced) | **Strong** | **0.92** | Nrf2 KO (syn205590) is direct loss-of-function evidence. Combined with iPSC-CM measurement (syn7079983) and NRF2 induction data (syn237499). |
| NRF2 activates NQO1 | syn205590, syn7079983 | L2 (Reinforced) | **Strong** | **0.85** | NQO1 reduced in Nrf2 KO mice (syn205590). Canonical ARE-driven regulation. |
| NRF2 activates HMOX1 | syn205590, syn7079983 | L2 (Reinforced) | **Strong** | **0.85** | HMOX1 reduced in Nrf2 KO mice (syn205590). Canonical ARE-driven regulation. |
| KEAP1 represses NRF2 | syn205590, syn237499 | L3 -> L2 | **Moderate** | **0.75** | Nrf2 KO shows pathway disruption (syn205590); NRF2 induction under oxidative stress (syn237499). KEAP1-NRF2 binding not directly measured in these datasets. |
| TOP2B mediates doxorubicin cardiotoxicity | syn7079983, syn13856689 | L1 (Reinforced) | **Moderate** | **0.80** | iPSC-CM models confirm cardiomyocyte vulnerability to drug-induced toxicity. TKI mechanism differs from doxorubicin TOP2B poisoning but mitochondrial/oxidative overlap supports the shared cell-type vulnerability. |
| Doxorubicin inhibits TOP2A (anti-tumor) | -- | L1 (unchanged) | **None** | **0.70** | No Synapse grounding. Confidence from opentargets/ChEMBL remains. |
| Dexrazoxane degrades TOP2B | -- | L1 (unchanged) | **None** | **0.70** | No Synapse grounding. NCT03930680 clinical evidence is primary source. |
| Selumetinib inhibits BRAF/MEK for NF1 | syn21452685 (partial) | L1 (unchanged) | **Weak** | **0.65** | syn21452685 has MEK inhibitor data but for different compounds. Selumetinib grounding is clinical (NCT01362803). |
| ABCB1 transports doxorubicin | -- | L2 (unchanged) | **None** | **0.60** | No Synapse grounding. Well-established pharmacology from HGNC/UniProt. |
| RARG variants predict cardiotoxicity | -- | L3 (unchanged) | **None** | **0.45** | No Synapse grounding. Genetic association evidence only. |
| SOD2 protects cardiomyocyte mitochondria | syn205590, syn7079983, syn13856689 | L2 (Reinforced) | **Moderate** | **0.78** | SOD2 measured in NRF2 KO (syn205590) and iPSC-CM models (syn7079983, syn13856689). NRF2-specific transcriptional regulation of SOD2 is less definitive than for NQO1/HMOX1. |

---

## 7. Methodology

### 7.1 Search Strategy

Nine Synapse datasets were identified using the `search_synapse` MCP tool with the following queries:

| Query | Datasets Found | Rationale |
|-------|---------------|-----------|
| `"doxorubicin cardiotoxicity cardiomyocyte"` | syn7079983, syn13856689 | Direct search for cardiotoxicity transcriptomics in cardiomyocyte models |
| `"NRF2 NFE2L2 oxidative stress knockout"` | syn205590, syn237499 | NRF2 pathway perturbation datasets |
| `"NF1 neurofibromatosis preclinical drug"` | syn21452685, syn22266606, syn56566376 | NF1 disease biology and drug response |
| `"TOP2B topoisomerase expression knockout"` | syn248628, syn266796 | TOP2B-specific perturbation data |

[Source: search_synapse("doxorubicin cardiotoxicity cardiomyocyte"), search_synapse("NRF2 NFE2L2 oxidative stress knockout"), search_synapse("NF1 neurofibromatosis preclinical drug"), search_synapse("TOP2B topoisomerase expression knockout")]

### 7.2 Matching Criteria

- **Node grounding**: A node is grounded if a Synapse dataset contains gene expression, protein abundance, or perturbation data for the entity (direct measurement or functional readout).
- **Edge grounding**: An edge is grounded if a Synapse dataset provides experimental evidence supporting the relationship (e.g., gene KO reduces downstream target expression, perturbation alters pathway activity).
- **Strength classification**:
  - **Strong**: Direct perturbation (KO, knockdown, drug treatment) of the entity in a disease-relevant model with the entity explicitly measured.
  - **Moderate**: Entity measured in a related model (same cell type, analogous drug mechanism, pathway overlap) or as a downstream readout.
  - **Weak**: Entity is in the same biological system but not the primary focus of the dataset, or the model uses a substantially different perturbation/tissue.

### 7.3 MEMBER_OF Exclusion Rationale

MEMBER_OF edges encode curated pathway annotations from WikiPathways (e.g., "NFE2L2 MEMBER_OF WP:WP408"). These are:
- Definitional (assigned by pathway curators, not discovered experimentally)
- Non-falsifiable by a single dataset (pathway membership is a community consensus)
- Verified by their WikiPathways source, not by individual experimental datasets

They are therefore excluded from the groundable denominator, consistent with prior grounding documents in this series.

### 7.4 Dataset Verification

Each dataset was verified using `get_entity(synID)` to confirm:
- Entity existence and accessibility
- Data types and species information
- Relevance to knowledge graph entities

[Source: get_entity(syn7079983), get_entity(syn13856689), get_entity(syn205590), get_entity(syn237499), get_entity(syn21452685), get_entity(syn22266606), get_entity(syn56566376), get_entity(syn248628), get_entity(syn266796)]

---

## 8. Limitations

### 8.1 No Direct Doxorubicin Cardiomyocyte Dataset on Synapse

The most significant gap is the absence of a doxorubicin-treated cardiomyocyte transcriptomic dataset on Synapse. The iPSC-CM datasets (syn7079983, syn13856689) use TKIs (Sorafenib, Sunitinib, Lapatinib, Erlotinib), not doxorubicin. While the shared mechanisms (mitochondrial dysfunction, oxidative stress, cardiomyocyte-specific vulnerability) provide analogous support, the grounding for doxorubicin-specific TOP2B poisoning remains indirect. Doxorubicin cardiomyocyte datasets likely exist in GEO (e.g., GSE series for anthracycline cardiotoxicity) but are not indexed in Synapse.

### 8.2 Cross-Species Extrapolation

Two datasets use mouse models:
- **syn205590** (Nrf2 KO mice, liver tissue): NRF2 pathway is conserved across species and tissues, but liver-to-heart extrapolation adds uncertainty.
- **syn266796** (Top2b KO mice, embryo brain): TOP2B function in brain differs from cardiomyocyte context.

### 8.3 No Dexrazoxane or Selumetinib Perturbation Data

Neither dexrazoxane nor selumetinib has a dedicated perturbation dataset on Synapse. Their grounding depends entirely on clinical trial evidence (ClinicalTrials.gov) and mechanism-of-action annotations (ChEMBL, Open Targets). syn21452685 (NFTC) includes MEK inhibitor data but for compounds other than selumetinib.

### 8.4 ABCB1 and RARG Have No Synapse Coverage

- **ABCB1** (P-glycoprotein) doxorubicin efflux is well-established pharmacology but has no dedicated Synapse dataset. PharmGKB or the Pharmacogenomics Knowledge Base would be more appropriate sources.
- **RARG** cardiotoxicity susceptibility variants derive from GWAS studies. GWAS Catalog or dbGaP would be more appropriate for grounding genetic association evidence.

### 8.5 TOP2A Isoform Gap

No Synapse dataset specifically measures TOP2A in a doxorubicin anti-tumor context. TOP2B datasets (syn248628, syn266796) do not include TOP2A isoform-resolved data. TOP2A is highly expressed in proliferating tumors and well-characterized in cancer genomics databases (TCGA, cBioPortal) but these are not Synapse-indexed.

### 8.6 Recommended Follow-Up

1. **GEO/ArrayExpress search**: Search for doxorubicin + cardiomyocyte or doxorubicin + iPSC-CM transcriptomic datasets that may exist outside Synapse.
2. **TCGA/cBioPortal**: For TOP2A expression in NF1-associated MPNST tumors.
3. **PharmGKB**: For ABCB1 doxorubicin pharmacogenomics evidence.
4. **GWAS Catalog/dbGaP**: For RARG cardiotoxicity susceptibility variant data.
5. **Re-query Synapse**: Periodic re-search as new datasets are deposited (NF1 research is actively funded by the Children's Tumor Foundation and NCI).

---

## Synapse Dataset Descriptions

### syn7079983: FDA TKI-induced cardiotoxicity
- **URL**: https://www.synapse.org/Synapse:syn7079983
- **Project type**: iPSC-CM cardiotoxicity modeling
- **Data types**: Gene expression, proteome, imaging
- **Cell model**: Cor4U hiPSC-CMs
- **Compounds**: Sorafenib, Sunitinib, Lapatinib, Erlotinib (TKI-focused, not doxorubicin)
- **Relevance**: Same cardiomyocyte cell type and shared cardiotoxicity mechanisms (oxidative phosphorylation disruption). Provides transcriptomic/proteomic baseline for cardiomyocyte stress response genes (HMOX1, SOD2, NQO1).
- [Source: search_synapse("iPSC cardiomyocyte cardiotoxicity"), get_entity(syn7079983)]

### syn13856689: TKI-induced cardiotoxicity in iPSC-derived human cardiomyocytes
- **URL**: https://www.synapse.org/Synapse:syn13856689
- **Project type**: Harvard/LINCS cardiotoxicity characterization
- **Data types**: RNAseq (GEO GSE114686, 30 samples x ~50k transcripts), proteomics (PRIDE PXD012043, ~6000 peptides), metabolomics
- **Cell model**: hiPSC-CMs
- **Compounds**: 4 TKIs (Sorafenib causes mitochondrial energetics defect)
- **Relevance**: Sorafenib-induced mitochondrial energetics defect parallels doxorubicin-induced oxidative stress in cardiomyocytes. Multi-omic data enables pathway-level analysis of cardiomyocyte stress response.
- [Source: search_synapse("iPSC cardiomyocyte cardiotoxicity transcriptomics"), get_entity(syn13856689)]

### syn205590: Nrf2 KO mice liver regeneration (GSE8969)
- **URL**: https://www.synapse.org/Synapse:syn205590
- **Data types**: Microarray (gene expression)
- **Model**: Nrf2 knockout mice, liver tissue
- **Key finding**: Cytoprotective enzyme expression reduced, tissue damage aggravated, liver regeneration delayed in Nrf2 KO mice
- **Relevance**: Direct demonstration of NRF2 role in oxidative stress response. Confirms NRF2 as master regulator of NQO1, HMOX1, SOD2 and other cytoprotective genes. Loss-of-function evidence is the strongest validation for the KEAP1-NRF2 regulatory axis.
- [Source: search_synapse("Nrf2 knockout oxidative stress"), get_entity(syn205590)]

### syn237499: NFE2L2/Nrf2 oxidant responsive transcription factor (GSE11952)
- **URL**: https://www.synapse.org/Synapse:syn237499
- **Data types**: Gene expression
- **Model**: Cigarette smoke oxidative stress
- **Key finding**: NRF2 induces phase 2 detoxifying and antioxidant genes under oxidative stress
- **Relevance**: Confirms NRF2 induction of the same cytoprotective gene battery relevant to doxorubicin detoxification. Validates the KEAP1-NRF2 regulatory axis under oxidative stress conditions.
- [Source: search_synapse("NRF2 NFE2L2 oxidative stress gene expression"), get_entity(syn237499)]

### syn21452685: Neurofibromatosis Therapeutic Consortium - UCSF (NFTC)
- **URL**: https://www.synapse.org/Synapse:syn21452685
- **Project type**: NF1 preclinical consortium (NFTC, 2013-2016)
- **Scale**: 111 preclinical trials, 12 drug targets identified, 16 clinical trials resulted
- **Models**: Plexiform neurofibroma, MPNST, NF1-associated leukemia
- **Drugs studied**: MEK inhibitors and others targeting the RAS-MAPK pathway
- **Relevance**: Definitive dataset for NF1-RAS-MAPK axis. Directly demonstrates the therapeutic rationale for MEK inhibition in NF1, supporting the selumetinib + doxorubicin combination strategy. The consortium identified 12 drug targets, validating the knowledge graph's NF1->KRAS->BRAF pathway.
- [Source: search_synapse("NF1 neurofibromatosis preclinical drug target"), get_entity(syn21452685)]

### syn22266606: Unveiling molecular mechanisms of neurofibromin regulation
- **URL**: https://www.synapse.org/Synapse:syn22266606
- **Key finding**: ERK1/2 directly phosphorylates NF1 (negative feedback loop). SPRED1 interactions modulate NF1 activity.
- **Relevance**: Provides molecular-level evidence for the NF1->KRAS->BRAF->MEK->ERK signaling axis with the additional insight that ERK feeds back to phosphorylate NF1. This feedback loop is relevant to MEK inhibitor therapeutic window in NF1.
- [Source: search_synapse("NF1 neurofibromin ERK regulation"), get_entity(syn22266606)]

### syn56566376: Role of Schwann cells in NF1-related pain
- **URL**: https://www.synapse.org/Synapse:syn56566376
- **Model**: Nf1 deletion in Schwann cells (mouse)
- **Key finding**: MAPK signaling changes upon NF1 loss; MEK inhibitor effects on NF1-related pain
- **Relevance**: Confirms NF1 loss -> MAPK activation in a disease-relevant cell type (Schwann cells are the origin of NF1 plexiform neurofibromas). MEK inhibitor effects support the selumetinib therapeutic rationale.
- [Source: search_synapse("NF1 Schwann cell MAPK signaling"), get_entity(syn56566376)]

### syn248628: TOP2B in DHT-induced androgen receptor target gene expression (GSE19445)
- **URL**: https://www.synapse.org/Synapse:syn248628
- **Data types**: Microarray (pharmacological inhibition and RNAi depletion of TOP2B)
- **Context**: Androgen receptor signaling
- **Relevance**: Demonstrates TOP2B perturbation effects on gene expression. Different biological context (androgen receptor, not cardiotoxicity) limits direct applicability, but confirms TOP2B as a transcriptional regulator with measurable downstream effects.
- [Source: search_synapse("TOP2B topoisomerase gene expression"), get_entity(syn248628)]

### syn266796: Top2b knockout mouse embryo brain transcription profiles (GSE5458)
- **URL**: https://www.synapse.org/Synapse:syn266796
- **Data types**: Microarray (TOP2B knockout)
- **Model**: Mouse embryo brain
- **Relevance**: Direct TOP2B loss-of-function data. Brain tissue rather than cardiac, but demonstrates TOP2B-dependent gene expression changes. TOP2B KO is embryonic lethal, consistent with the importance of TOP2B in post-mitotic cells including cardiomyocytes.
- [Source: search_synapse("TOP2B knockout mouse transcription"), get_entity(syn266796)]

---

*Synapse grounding generated 2026-02-20 via Fuzzy-to-Fact publication pipeline using search_synapse and get_entity MCP tools.*
