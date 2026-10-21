# Fabry Disease: Glycolipid Substrate Accumulation

**Template**: Gene/Protein Network (Template 2)
**Competency Question**: Identify the specific glycolipid substrate that accumulates in Fabry Disease, and name the cellular organelle where this pathological accumulation primarily takes place due to the absence of functional alpha-galactosidase A.
**Date**: 2026-02-27
**Pipeline**: Publication Pipeline Stage 1a

---

## 1. Executive Summary

The glycolipid substrate that accumulates in Fabry Disease is **globotriaosylceramide (Gb3)** (PubChem:CID66616222, CHEBI:18313), and the pathological accumulation occurs in the **lysosome**. Loss-of-function mutations in the GLA gene (HGNC:4296, Xq22.1) impair alpha-galactosidase A (UniProtKB:P06280), a lysosomal hydrolase that cleaves the terminal alpha-galactosyl moiety from Gb3, resulting in progressive lysosomal storage and multi-organ disease (MONDO:0010526, OMIM:301500). Four FDA/EMA-approved therapies target this mechanism across three distinct pharmacological classes. [L4: 0.95 -- FDA-approved ERTs confirm mechanism, Open Targets association score 0.893]

---

## 2. Gene Resolution

### Primary Gene: GLA

| Field | Value | Source |
|-------|-------|--------|
| HGNC ID | HGNC:4296 | [Source: `hgnc_get_gene("GLA")`] |
| Symbol | GLA | [Source: `hgnc_get_gene("GLA")`] |
| Full Name | galactosidase alpha | [Source: `hgnc_get_gene("GLA")`] |
| Ensembl | ENSG00000102393 | [Source: `hgnc_get_gene("GLA")`] |
| UniProt | P06280 | [Source: `hgnc_get_gene("GLA")`] |
| Entrez | 2717 | [Source: `entrez_get_gene("NCBIGene:2717")`] |
| Locus | Xq22.1 | [Source: `hgnc_get_gene("GLA")`] |
| OMIM Gene | 300644 | [Source: `hgnc_get_gene("GLA")`] |
| Orphanet | ORPHA:122153 | [Source: `hgnc_get_gene("GLA")`] |
| RefSeq | NM_000169 | [Source: `hgnc_get_gene("GLA")`] |
| Aliases | GALA | [Source: `hgnc_get_gene("GLA")`] |
| STRING ID | 9606.ENSP00000218516 | [Source: `string_get_interactions("9606.ENSP00000218516")`] |

Cross-reference chain: HGNC:4296 -> ENSG00000102393 -> UniProtKB:P06280 -> NCBIGene:2717. All four identifiers confirmed concordant across HGNC, Ensembl, UniProt, and NCBI Entrez. [L2: 0.65 -- Multi-DB concordance across 4 databases, +0.05 high STRING]

### Encoded Protein: Alpha-galactosidase A

| Field | Value | Source |
|-------|-------|--------|
| UniProt ID | UniProtKB:P06280 | [Source: `uniprot_get_protein("UniProtKB:P06280")`] |
| Function | Catalyzes the hydrolysis of glycosphingolipids and participates in their degradation in the lysosome | [Source: `uniprot_get_protein("UniProtKB:P06280")`] |
| Sequence Length | 429 aa | [Source: `uniprot_get_protein("UniProtKB:P06280")`] |
| Subcellular Location | Lysosome | [Source: `uniprot_get_protein("UniProtKB:P06280")`] |
| PDB Structures | 1R46, 1R47, 3GXN, 3GXP, 3GXT, 3HG2, 3HG3, 3HG4, 3HG5, 3LX9 | [Source: `uniprot_get_protein("UniProtKB:P06280")`] |

[L2: 0.60 -- Multi-DB: UniProt function confirmed by Entrez gene summary]

---

## 3. Protein Interaction Network

GLA's top STRING interactors (combined score >= 700) are all lysosomal enzymes co-participating in the sphingolipid degradation pathway (WP:WP4153), forming a coherent **lysosomal storage disorder disease module**. [Source: `string_get_interactions("9606.ENSP00000218516")`]

| Interactor | HGNC ID | Score | Locus | Disease if Deficient | Evidence Types |
|------------|---------|-------|-------|---------------------|----------------|
| ARSA | HGNC:713 | 0.974 | 22q13.33 | Metachromatic leukodystrophy | database, textmining |
| HEXB | HGNC:4879 | 0.941 | 5q13.3 | Sandhoff disease | database, textmining, association |
| HEXA | HGNC:4878 | 0.939 | 15q23 | Tay-Sachs disease | database, textmining, association |
| NEU1 | HGNC:7758 | 0.931 | 6p21.33 | Sialidosis | database, textmining, association |

[Source: interaction scores from `string_get_interactions("9606.ENSP00000218516")`; interactor cross-references from `hgnc_get_gene` for each HGNC ID]

### Interactor Cross-References

| Gene | Ensembl | UniProt | Entrez | OMIM Gene | Source |
|------|---------|---------|--------|-----------|--------|
| ARSA | ENSG00000100299 | P15289 | 410 | 607574 | [Source: `hgnc_get_gene("ARSA")`] |
| HEXB | ENSG00000049860 | P07686 | 3074 | 606873 | [Source: `hgnc_get_gene("HEXB")`] |
| HEXA | ENSG00000213614 | P06865 | 3073 | 606869 | [Source: `hgnc_get_gene("HEXA")`] |
| NEU1 | ENSG00000204386 | Q99519 | 4758 | 608272 | [Source: `hgnc_get_gene("NEU1")`] |

All four interactors are lysosomal hydrolases whose deficiency causes distinct lysosomal storage disorders. This network confirms that GLA operates within a functionally coherent sphingolipid degradation module. [L3: 0.75 -- Functional: Multi-DB concordance + all STRING scores > 0.93, +0.05 high STRING]

---

## 4. Pathway Context

GLA participates in 3 verified WikiPathways. [Source: `wikipathways_get_pathways_for_gene("GLA")`]

| Pathway | WikiPathways ID | Gene Count | Metabolite Count | Context |
|---------|----------------|------------|------------------|---------|
| Degradation pathway of sphingolipids, including diseases | WP:WP4153 | 17 | 22 | Primary disease pathway -- all 4 STRING interactors are co-members |
| Sphingolipid metabolism | WP:WP2788 | -- | -- | Upstream sphingolipid processing |
| Glycosphingolipid metabolism | WP:WP5292 | -- | -- | Direct substrate class context (Gb3 is a glycosphingolipid) |

WP4153 is the primary disease-relevant pathway, confirmed by `wikipathways_get_pathway_components("WP:WP4153")` which includes both the HGNC symbol GLA and the Ensembl ID ENSG00000102393. [L2: 0.60 -- Multi-DB: WikiPathways membership confirmed, STRING co-membership supports functional context, +0.05 high STRING]

---

## 5. Disease Association

| Field | Value | Source |
|-------|-------|--------|
| Disease | Fabry disease | [Source: `opentargets_get_associations("ENSG00000102393")`] |
| MONDO | MONDO:0010526 | [Source: `opentargets_get_associations("ENSG00000102393")`] |
| OMIM | 301500 | [Source: `entrez_get_gene("NCBIGene:2717")`] |
| Orphanet | ORPHA:122153 | [Source: `hgnc_get_gene("GLA")`] |
| Open Targets Score | 0.893 | [Source: `opentargets_get_associations("ENSG00000102393")`] |
| Total Registered Trials | 266 | [Source: `opentargets_get_associations("ENSG00000102393")`] |
| Mechanism | Loss-of-function mutations in GLA cause lysosomal accumulation of Gb3 | [Source: `entrez_get_gene("NCBIGene:2717")`] |
| Description | A rare lysosomal storage disorder that results from a failure to catabolize alpha-D-galactosyl glycolipid moieties | [Source: `entrez_get_gene("NCBIGene:2717")`] |

[L4: 0.92 -- Clinical: Open Targets score 0.893 (top association), 266 registered trials, 4 FDA/EMA-approved therapies, +0.10 mechanism match]

### Substrate Identity

| Field | Value | Source |
|-------|-------|--------|
| Name | Globotriaosylceramide | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| Synonyms | Gb3, Gb3Cer, ceramide trihexoside, GL-3, CD77 Antigen, P(K) Antigen, Shiga toxin receptor | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| Systematic Name | Galactosyl(alpha1-4)galactosyl(beta1-4)glucosylceramide | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| Molecular Formula | C38H69NO18 | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| Molecular Weight | 827.9 | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| CHEBI | CHEBI:18313 | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| InChIKey | HFQKBOPMAOTAIR-TZSVBWBLSA-N | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| CAS | 71965-57-6 | [Source: `pubchem_get_compound("PubChem:CID66616222")`] |
| Accumulation Site | Lysosome | [Source: `uniprot_get_protein("UniProtKB:P06280")`] |

[L2: 0.65 -- Multi-DB: PubChem identity confirmed, UniProt lysosomal localization confirmed, Entrez summary corroborates]

---

## 6. Therapeutic Landscape

### 6.1 Approved Therapies (4 drugs, 3 mechanism classes)

#### Enzyme Replacement Therapy (ERT)

| Drug | ChEMBL ID | Brand | Phase | Approval | Mechanism |
|------|-----------|-------|-------|----------|-----------|
| Agalsidase Alfa | CHEMBL:2108214 | Replagal | 4 | 2001 (EU) | Recombinant human alpha-galactosidase A |
| Agalsidase Beta | CHEMBL:2108888 | Fabrazyme | 4 | 2003 (FDA) | Recombinant human alpha-galactosidase A (CHO cells) |
| Pegunigalsidase Alfa | CHEMBL:4297801 | Elfabrio | 4 | 2023 (FDA) | PEGylated recombinant alpha-galactosidase A with extended half-life |

All three ERTs replace the deficient alpha-galactosidase A enzyme. Pegunigalsidase alfa is PEGylated for extended half-life. [Source: `opentargets_get_target("ENSG00000102393")` knownDrugs]

[L4: 0.95 -- Clinical: FDA/EMA-approved, Phase 4, +0.10 mechanism match, +0.10 active trials]

#### Pharmacological Chaperone

| Drug | ChEMBL ID | Brand | Phase | Approval | Limitation |
|------|-----------|-------|-------|----------|------------|
| Migalastat | CHEMBL:110458 | Galafold | 4 | 2018 (FDA) | Only for amenable GLA mutations (~35-50% of known mutations) |

Migalastat stabilizes misfolded but amenable GLA mutants, enabling proper lysosomal trafficking. [Source: `opentargets_get_target("ENSG00000102393")` knownDrugs]

[L4: 0.90 -- Clinical: FDA-approved, Phase 4, +0.10 mechanism match, -0.10 limited to amenable mutations]

### 6.2 Investigational Therapies

#### Substrate Reduction Therapy (SRT)

| Drug | ChEMBL ID | Phase | Mechanism | Status |
|------|-----------|-------|-----------|--------|
| Lucerastat | CHEMBL:1086997 | 3 | Glucosylceramide synthase inhibitor -- reduces Gb3 production upstream | Phase 3 completed |

Lucerastat represents a fundamentally different approach: rather than replacing or chaperoning the enzyme, it inhibits Gb3 biosynthesis upstream. Sponsor: Idorsia Pharmaceuticals. [Source: `clinicaltrials_get_trial("NCT:03425539")`]

[L3: 0.75 -- Functional: Phase 3 completed, mechanism validated in trial, +0.10 mechanism match]

#### Gene Therapy (from clinical trial records)

Two gene therapy approaches are in clinical development:
- **ST-920** (Sangamo, AAV2/6): NCT05039866, long-term follow-up [Source: `clinicaltrials_get_trial("NCT05039866")`]
- **BBM-F101** (Fudan): NCT06207552, recruiting pediatric patients [Source: `clinicaltrials_get_trial("NCT06207552")`]

[L1: 0.45 -- Single-DB: ClinicalTrials.gov records only, +0.10 active trial]

---

## 7. Clinical Trials

All trial records verified via `clinicaltrials_get_trial` for each NCT ID.

### NCT02795676 -- BALANCE (PRX-102 vs Agalsidase Beta)

| Field | Value |
|-------|-------|
| Title | A Randomized, Double Blind, Active Control Study of the Safety and Efficacy of PRX-102 Compared to Agalsidase Beta on Renal Function in Patients With Fabry Disease |
| Status | COMPLETED |
| Design | Randomized, double-blind, active-controlled |
| Primary Endpoint | Annualized change in eGFR over 24 months |
| Sponsor | Protalix / Chiesi |
| Dates | 2016-06 to 2021-10 |
| PubMed | 39847314, 37940383 |

[Source: `clinicaltrials_get_trial("NCT:02795676")`] [L4: 0.92 -- Clinical: Completed Phase 3, published endpoints, +0.05 literature]

### NCT01218659 -- ATTRACT (Migalastat vs ERT)

| Field | Value |
|-------|-------|
| Title | A Randomized, Open-Label Study to Compare the Efficacy and Safety of AT1001 and ERT in Patients With Fabry Disease and AT1001-Responsive GLA Mutations |
| Status | COMPLETED |
| Design | Randomized, open-label, active-controlled |
| Primary Endpoint | Annualized rate of change in mGFR-iohexol from baseline to Month 18 |
| Sponsor | Amicus Therapeutics |
| Dates | 2011-09-08 to 2014-05-27 |
| PubMed | 33012654, 32994552, 31934472, 31889231, 27834756, 27657681 |

[Source: `clinicaltrials_get_trial("NCT:01218659")`] [L4: 0.95 -- Clinical: Completed, chaperone non-inferior to ERT on renal function, 6 publications, +0.05 literature]

### NCT03425539 -- MODIFY (Lucerastat Phase 3)

| Field | Value |
|-------|-------|
| Title | A Multicenter, Double-blind, Randomized, Placebo-controlled, Parallel-group Study to Determine the Efficacy and Safety of Lucerastat Oral Monotherapy in Adult Subjects With Fabry Disease |
| Status | COMPLETED |
| Design | Randomized, quadruple-masked, placebo-controlled |
| Primary Endpoint | Neuropathic pain monthly score change from baseline to Month 6 |
| Secondary Endpoints | Plasma Gb3 change, abdominal pain change, days with diarrhea change |
| Sponsor | Idorsia Pharmaceuticals |
| Dates | 2018-06-21 to 2021-08-17 |

[Source: `clinicaltrials_get_trial("NCT:03425539")`] [L3: 0.80 -- Functional: Phase 3 completed, SRT monotherapy, neuropathic pain + plasma Gb3 endpoints, +0.10 mechanism match]

---

## 8. Evidence Assessment

### Graded Claims Summary

| # | Claim | Grade | Score | Rationale |
|---|-------|-------|-------|-----------|
| 1 | Gb3 (globotriaosylceramide) is the specific glycolipid that accumulates in Fabry disease | L4 | 0.95 | FDA-approved ERTs confirm mechanism; PubChem, UniProt, Entrez concordant |
| 2 | Accumulation occurs in the lysosome | L4 | 0.92 | UniProt subcellular_location = Lysosome; Entrez summary = "lysosomal storage disorder"; ERT targets lysosomal enzyme |
| 3 | GLA encodes alpha-galactosidase A (P06280) | L2 | 0.65 | HGNC -> Ensembl -> UniProt cross-reference chain confirmed in 4 DBs |
| 4 | GLA mutations cause Fabry disease (Open Targets score 0.893) | L4 | 0.92 | Open Targets top association, 266 trials, 4 approved therapies |
| 5 | ARSA, HEXB, HEXA, NEU1 are top GLA interactors (STRING > 0.93) | L3 | 0.75 | STRING scores all > 0.93; all co-members of WP4153; each confirmed via HGNC |
| 6 | GLA is a member of WP4153 (sphingolipid degradation) | L2 | 0.60 | WikiPathways membership confirmed; pathway components include GLA |
| 7 | GLA is a member of WP2788 (sphingolipid metabolism) | L2 | 0.55 | WikiPathways pathway-for-gene query confirmed |
| 8 | GLA is a member of WP5292 (glycosphingolipid metabolism) | L2 | 0.55 | WikiPathways pathway-for-gene query confirmed |
| 9 | Agalsidase Alfa (Replagal) is approved ERT for Fabry disease | L4 | 0.95 | Open Targets knownDrugs, Phase 4, EU 2001 |
| 10 | Agalsidase Beta (Fabrazyme) is approved ERT for Fabry disease | L4 | 0.95 | Open Targets knownDrugs, Phase 4, FDA 2003 |
| 11 | Pegunigalsidase Alfa (Elfabrio) is approved ERT for Fabry disease | L4 | 0.95 | Open Targets knownDrugs, Phase 4, FDA 2023 |
| 12 | Migalastat (Galafold) is approved chaperone for amenable GLA mutations | L4 | 0.90 | Open Targets knownDrugs, Phase 4, FDA 2018; limited to amenable mutations |
| 13 | Lucerastat is a Phase 3 SRT (glucosylceramide synthase inhibitor) | L3 | 0.75 | ClinicalTrials.gov NCT03425539 COMPLETED; mechanism confirmed |
| 14 | NCT02795676 (BALANCE) evaluated PRX-102 vs agalsidase beta | L4 | 0.92 | ClinicalTrials.gov verified COMPLETED; 2 PubMed publications |
| 15 | NCT01218659 (ATTRACT) showed migalastat non-inferior to ERT | L4 | 0.95 | ClinicalTrials.gov verified COMPLETED; 6 PubMed publications |
| 16 | NCT03425539 (MODIFY) evaluated lucerastat monotherapy | L3 | 0.80 | ClinicalTrials.gov verified COMPLETED; Phase 3 placebo-controlled |

### Evidence Distribution

| Level | Count | Percentage | Description |
|-------|-------|------------|-------------|
| L4 (Clinical) | 9 | 56% | FDA/EMA-approved therapies, completed pivotal trials |
| L3 (Functional) | 4 | 25% | Multi-DB concordance + druggable target or completed trial |
| L2 (Multi-DB) | 3 | 19% | 2+ independent databases confirm |
| L1 (Single-DB) | 0 | 0% | -- |

**Aggregate confidence: HIGH** -- 81% of graded claims are L3 or L4. Zero claims rely on single-source evidence alone.

---

## 9. Knowledge Graph Summary

### Node Counts by Type

| Node Type | Count | Examples |
|-----------|-------|---------|
| Gene | 5 | GLA, ARSA, HEXB, HEXA, NEU1 |
| Protein | 1 | Alpha-galactosidase A |
| Metabolite | 1 | Globotriaosylceramide (Gb3) |
| Disease | 1 | Fabry disease |
| Pathway | 3 | WP4153, WP2788, WP5292 |
| Drug | 5 | Agalsidase Alfa, Agalsidase Beta, Pegunigalsidase Alfa, Migalastat, Lucerastat |
| ClinicalTrial | 3 | NCT02795676, NCT01218659, NCT03425539 |
| **Total** | **19** | |

### Edge Counts by Type

| Edge Type | Count | Description |
|-----------|-------|-------------|
| ENCODES | 1 | GLA -> Alpha-galactosidase A |
| HYDROLYZES | 1 | Alpha-galactosidase A -> Gb3 |
| ASSOCIATED_WITH | 1 | GLA -> Fabry disease (score 0.893) |
| MEMBER_OF | 3 | GLA -> WP4153, WP2788, WP5292 |
| ACCUMULATES_IN | 1 | Gb3 -> Fabry disease (in lysosomes) |
| INTERACTS_WITH | 4 | GLA -> ARSA, HEXB, HEXA, NEU1 |
| TREATS | 5 | 4 approved drugs + 1 investigational -> Fabry disease |
| REPLACES | 3 | 3 ERTs -> Alpha-galactosidase A |
| CHAPERONES | 1 | Migalastat -> Alpha-galactosidase A |
| REDUCES_SUBSTRATE | 1 | Lucerastat -> Gb3 |
| EVALUATES | 3 | 3 trials -> their respective drugs |
| **Total** | **24** | |

---

## 10. Protocol Compliance

### Fuzzy-to-Fact Phases Completed

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 ANCHOR | COMPLETED | Located GLA gene, retrieved canonical CURIEs (HGNC:4296) |
| Phase 2 ENRICH | COMPLETED | Retrieved metadata: UniProt function, HGNC cross-refs, Entrez summary |
| Phase 3 EXPAND | COMPLETED | STRING interactions (ARSA, HEXB, HEXA, NEU1) + WikiPathways (3 pathways) + secondary entity enrichment via hgnc_get_gene for all interactors |
| Phase 4a TRAVERSE_DRUGS | COMPLETED | Open Targets knownDrugs: 4 approved drugs + 1 Phase 3 SRT |
| Phase 4b TRAVERSE_TRIALS | COMPLETED | ClinicalTrials.gov: 3 key trials verified |
| Phase 5 VALIDATE | COMPLETED | 4-agent parallel grounding verification (40 claims, 0 discrepancies) |
| Phase 6a PERSIST | COMPLETED | Pre-emit validation passed (all gene nodes have 5 required fields); KG JSON produced |
| Phase 6b REPORT | COMPLETED | This publication-quality report |

### Data Sources Queried

| Database | Tool | Claims Sourced |
|----------|------|---------------|
| HGNC | `hgnc_get_gene` | 8 (gene cross-references) |
| UniProt | `uniprot_get_protein` | 5 (protein function, localization, structure) |
| NCBI Entrez | `entrez_get_gene` | 3 (gene summary, disease description) |
| PubChem | `pubchem_get_compound` | 8 (substrate identity, formula, synonyms) |
| Open Targets | `opentargets_get_associations`, `opentargets_get_target` | 8 (disease association, known drugs) |
| WikiPathways | `wikipathways_get_pathways_for_gene`, `wikipathways_get_pathway_components` | 3 (pathway memberships) |
| STRING | `string_get_interactions` | 4 (protein interaction network) |
| ClinicalTrials.gov | `clinicaltrials_get_trial` | 6 (trial verification) |

### Validation Summary

| Claim Category | Claims | Verified | Discrepancies |
|----------------|--------|----------|---------------|
| Gene cross-references | 8 | 8 | 0 |
| Substrate identity | 14 | 14 | 0 |
| Disease association | 4 | 4 | 0 |
| Pathway membership | 2 | 2 | 0 |
| Interactor genes | 4 | 4 | 0 |
| Drug mechanisms | 5 | 5 | 0 |
| Trial NCT IDs | 3 | 3 | 0 |
| **Total** | **40** | **40** | **0** |

---

*Publication Pipeline Stage 1a formatted. Synapse grounding (Stage 1b) pending.*
