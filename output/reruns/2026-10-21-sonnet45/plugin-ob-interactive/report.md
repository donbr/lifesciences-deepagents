# Decoupling Doxorubicin Toxicity from Anti-Tumor Efficacy in NF1

**Competency question**: What known genes or pathways are implicated in minimizing Doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?

**Source catalog**: `biosciences-research/docs/competency-questions-paul.md` cq3 (Focus Area 1), user-scoped to NF1. Not present in `open-biosciences/biosciences-competency-questions-sample`; no gold-standard path exists.

**Templates applied**: Template 7 (Safety / Off-Target, primary) + Template 2 (Gene / Protein Network, secondary), with the Clinical Trials section from Template 1.

**Pipeline input**: `.ob-cq/cq-nf1-dox-toxicity-efficacy/results.json` — 17 nodes, 15 edges. The `metadata` block carries `tools_used`, `failures`, and aggregate counts but **no `phases_completed` field**; phase coverage is inferred from the conversation record (Phases 1-5 run, 6a persisted to local files only, not to Graphiti).

**Overall confidence: 0.50 (L1/L2 boundary), range 0.25-0.80.** Median of 12 graded claims.

> Synthesis disclaimer: mechanism descriptions paraphrase UniProt function text, Open Targets mechanism records, and PubMed abstracts. All synthesis is grounded in cited tool calls; no entities, CURIEs, or quantitative values are introduced from training knowledge.

---

## Summary

The toxicity and the efficacy of doxorubicin are carried by **two different topoisomerase II isoforms**, and that asymmetry is the entire answer to this question.

Doxorubicin's only recorded mechanism is inhibition of **TOP2A** (DNA topoisomerase II alpha), the anti-tumor axis [Source: curl OpenTargets/graphql(drug(CHEMBL53463).mechanismsOfAction)]. Cardiotoxicity, by contrast, is mediated by the paralogue **TOP2B** in cardiomyocytes: cardiomyocyte-specific *Top2b* deletion protects mice from doxorubicin-induced DNA double-strand breaks, defective mitochondrial biogenesis, ROS formation, and progressive heart failure [Source: pubmed get_article_metadata(23104132)]. CRISPR screen data support the asymmetry at the tumor end — TOP2A scores as a hit in **883** ORCS screens versus **24** for TOP2B [Sources: get_orcs_essentiality(7153), get_orcs_essentiality(7155)]. **TOP2A/TOP2B isoform selectivity is therefore the canonical therapeutic-window lever**, and it is NF1-independent.

NF1 changes the *efficacy* side only. Three NF1-specific resistance nodes were retrieved, all from single publications:

1. **BCL2L1 (Bcl-xL)** — the most directly on-question gene. NF1 deficiency upregulates Bcl-xL through activated Erk1/2 in MPNST-derived Schwann cells, causing doxorubicin resistance; Bcl-xL knockdown restores doxorubicin-induced apoptosis, and very low-dose ABT-737 plus doxorubicin is synergistic [Source: pubmed get_article_metadata(23292448)].
2. **AXL** and **NFKB1** — strongly activated at 2 and 21 days after doxorubicin in NF1-MPNST tumorgrafts, tightly correlated regardless of treatment or genomic context; proposed as resistance-mitigation targets [Source: pubmed get_article_metadata(32245042)].
3. **BRD4** and **EZH2** — co-investigated with TOP2A as therapeutic targets in human NF1-derived MPNSTs [Source: pubmed search_articles(title query) -> PMID 28813519].

The clinical instantiation of the question already exists: **NCT02584309**, a completed non-inferiority study of doxorubicin with upfront dexrazoxane in advanced soft tissue sarcoma, with progression-free survival as the primary endpoint and cardiac endpoints secondary, and MPNST an eligible histology [Source: clinicaltrials_get_trial(NCT:02584309)].

**No evidence was retrieved that NF1 status modulates anthracycline cardiotoxicity itself.** Every NF1-specific finding sits on the tumor side.

---

## Resolved Entities

| Entity | CURIE | Type | Role in this question | Source |
|--------|-------|------|----------------------|--------|
| NF1 | HGNC:7765 | Gene | Ras GAP; loss drives the resistance axis | [Sources: hgnc_search_genes("NF1"), hgnc_get_gene(HGNC:7765)] |
| Neurofibromin | UniProtKB:P21359 | Protein | "Stimulates the GTPase activity of Ras" | [Source: uniprot_get_protein(UniProtKB:P21359)] |
| TOP2A | HGNC:11989 | Gene | Doxorubicin anti-tumor target | [Sources: hgnc_search_genes("TOP2A"), hgnc_get_gene(HGNC:11989)] |
| TOP2B | HGNC:11990 | Gene | Cardiotoxicity mediator | [Sources: hgnc_search_genes("TOP2B"), hgnc_get_gene(HGNC:11990)] |
| BCL2L1 | HGNC:992 | Gene | NF1-loss-driven resistance node | [Sources: hgnc_search_genes("BCL2L1"), curl HGNC/fetch(hgnc_id/992)] |
| AXL | HGNC:905 | Gene | Post-doxorubicin kinome adaptation | [Sources: hgnc_search_genes("AXL"), curl HGNC/fetch(hgnc_id/905)] |
| NFKB1 | HGNC:7794 | Gene | Post-doxorubicin kinome adaptation | [Sources: hgnc_search_genes("NFKB1"), curl HGNC/fetch(hgnc_id/7794)] |
| BRD4 | HGNC:13575 | Gene | Combination target in NF1-MPNST | [Sources: hgnc_search_genes("BRD4"), curl HGNC/fetch(hgnc_id/13575)] |
| EZH2 | HGNC:3527 | Gene | Combination target in NF1-MPNST | [Sources: hgnc_search_genes("EZH2"), curl HGNC/fetch(hgnc_id/3527)] |
| MCL1 | HGNC:6943 | Gene | BCL2-family context node | [Sources: hgnc_search_genes("MCL1"), curl HGNC/fetch(hgnc_id/6943)] |
| KRAS | HGNC:6407 | Gene | NF1 GAP substrate (partial node) | [Source: string_get_interactions(STRING:9606.ENSP00000351015)] |
| DOXORUBICIN | CHEMBL:53463 | Compound | Index compound | [Source: chembl_search_compounds("doxorubicin")] |
| DEXRAZOXANE | CHEMBL:1738 | Compound | Cardioprotection candidate | [Source: chembl_search_compounds("dexrazoxane")] |
| Neurofibromatosis type 1 | MONDO:0018975 | Disease | Germline context | [Source: opentargets_get_associations(ENSG00000196712)] |
| Malignant peripheral nerve sheath tumor | MONDO:0017827 | Disease | Treated indication | [Source: opentargets_get_associations(ENSG00000196712)] |

Gene cross-references (Ensembl, UniProt, locus) for all ten gene nodes are in `entities.json`. KRAS is the one incomplete node: it was discovered during Phase 3 EXPAND and not enriched via `hgnc_get_gene`.

---

## Index Compound Profile

| Property | Value | Source |
|----------|-------|--------|
| Drug name | DOXORUBICIN | [Source: chembl_search_compounds("doxorubicin")] |
| CURIE | CHEMBL:53463 | [Source: chembl_search_compounds("doxorubicin")] |
| Primary target | TOP2A (ENSG00000131747) | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).mechanismsOfAction)] |
| Mechanism | DNA topoisomerase II alpha inhibitor (INHIBITOR) | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).mechanismsOfAction)] |
| Maximum clinical stage | APPROVAL | [Source: curl OpenTargets/graphql(drug(CHEMBL53463))] |
| Molecular formula | Not returned | [No data: chembl_get_compound(CHEMBL:53463) returned name only, molecular_formula null] |
| Mechanism (ChEMBL) | Not available | [No data: get_mechanism(CHEMBL:53463) returned ENTITY_NOT_FOUND; curl ChEMBL/mechanism.json(CHEMBL53463) returned 0 mechanisms] |

---

## Toxicity Axis: Isoform-Resolved Off-Target

| Toxicity target | Gene CURIE | Evidence of mediation | Tumor essentiality (ORCS hit screens) | Source |
|-----------------|-----------|----------------------|--------------------------------------|--------|
| TOP2B (topoisomerase II beta) | HGNC:11990 | Cardiomyocyte-specific *Top2b* deletion protects mice from doxorubicin-induced DSBs, defective mitochondrial biogenesis, ROS, and progressive heart failure | 24 | [Sources: pubmed get_article_metadata(23104132), get_orcs_essentiality(7155)] |
| TOP2A (topoisomerase II alpha) | HGNC:11989 | Not a toxicity mediator in retrieved data; the efficacy target | 883 | [Sources: curl OpenTargets/graphql(drug(CHEMBL53463).mechanismsOfAction), get_orcs_essentiality(7153)] |

The two isoforms are distinct loci and distinct proteins: TOP2A at 17q21.2 / UniProtKB:P11388, TOP2B at 3p24.2 / UniProtKB:Q02880 [Sources: hgnc_get_gene(HGNC:11989), hgnc_get_gene(HGNC:11990)].

### Safety Signals (pharmacovigilance)

| Signal | logLR | Reports | Rank among 21 AE terms | Source |
|--------|-------|---------|------------------------|--------|
| Febrile neutropenia | 9262.78 | 4246 | 1 | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).adverseEvents)] |
| Neutropenia | 3269.59 | 2928 | 2 | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).adverseEvents)] |
| Mucosal inflammation | 1497.72 | 990 | 3 | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).adverseEvents)] |
| **Cardiotoxicity** | **1400.85** | **618** | **4** | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).adverseEvents)] |
| Thrombocytopenia | 1158.44 | 1630 | 6 | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).adverseEvents)] |
| Haematotoxicity | 1122.58 | 561 | 7 | [Source: curl OpenTargets/graphql(drug(CHEMBL53463).adverseEvents)] |

Cardiotoxicity is the highest-ranked non-haematological, non-mucosal signal. Myelosuppression dominates by report volume but has no isoform-resolved mechanism in the retrieved data, so it is not addressable by the TOP2A/TOP2B lever.

### Pharmacological Mitigation

| Agent | CURIE | Mechanism(s) | Max phase | Source |
|-------|-------|--------------|-----------|--------|
| Dexrazoxane | CHEMBL:1738 | Iron sequestering agent (SEQUESTERING AGENT, target CHEMBL2363058); DNA topoisomerase II inhibitor (INHIBITOR, target CHEMBL2094255) | 4 | [Source: get_mechanism(CHEMBL:1738)] |

**Isoform caveat**: the ChEMBL record names "DNA topoisomerase II inhibitor" against target CHEMBL2094255 **without disambiguating alpha from beta**. A dexrazoxane-to-TOP2B edge is therefore *inferred*, not asserted by any tool call, and is graded Insufficient Evidence below.

---

## Efficacy Axis: NF1-Specific Resistance Network

### Interaction and regulatory edges

| From | Relationship | To | Quantitative | Source |
|------|-------------|-----|-------------|--------|
| NF1 | interacts with (GAP substrate) | KRAS | STRING 0.998 | [Source: string_get_interactions(STRING:9606.ENSP00000351015)] |
| NF1 | interacts with | RRAS2 | STRING 0.939 | [Source: string_get_interactions(STRING:9606.ENSP00000351015)] |
| NF1 | interacts with | RRAS | STRING 0.940 | [Source: string_get_interactions(STRING:9606.ENSP00000351015)] |
| NF1 | interacts with | TMEM127 | STRING 0.879 | [Source: string_get_interactions(STRING:9606.ENSP00000351015)] |
| NF1 loss | upregulates (via Erk1/2) | BCL2L1 (Bcl-xL) | Not quantified in abstract | [Source: pubmed get_article_metadata(23292448)] |
| BCL2L1 | confers resistance to | DOXORUBICIN | Reversed by siRNA knockdown; ABT-737 synergy at "very low dose" | [Source: pubmed get_article_metadata(23292448)] |
| DOXORUBICIN | induces adaptation in | AXL | Activated at 2 d and 21 d | [Source: pubmed get_article_metadata(32245042)] |
| DOXORUBICIN | induces adaptation in | NFKB1 | Activated at 2 d and 21 d, correlated with AXL | [Source: pubmed get_article_metadata(32245042)] |

15 interactions were returned at `required_score=700`; the four NF1-incident edges above are the ones relevant here. The remaining 11 are RAS-pathway edges not incident on NF1 (KRAS-EGFR 0.999, KRAS-BRAF 0.999, KRAS-NRAS 0.999, KRAS-HRAS 0.999, KRAS-TP53 0.954, KRAS-PTEN 0.925, KRAS-AKT1 0.902, KRAS-SPRED1 0.733, RRAS-RRAS2 0.959, RRAS-BRAF 0.942, RRAS2-BRAF 0.937) [Source: string_get_interactions(STRING:9606.ENSP00000351015)].

### Disease associations

| Disease | CURIE | Score | Source |
|---------|-------|-------|--------|
| Neurofibromatosis type 1 | MONDO:0018975 | 0.89 | [Source: opentargets_get_associations(ENSG00000196712)] |
| Neurofibromatosis-Noonan syndrome | MONDO:0011035 | 0.84 | [Source: opentargets_get_associations(ENSG00000196712)] |
| Neurofibromatosis | MONDO:0021061 | 0.82 | [Source: opentargets_get_associations(ENSG00000196712)] |
| Juvenile myelomonocytic leukemia | MONDO:0011908 | 0.77 | [Source: opentargets_get_associations(ENSG00000196712)] |
| Malignant peripheral nerve sheath tumor | MONDO:0017827 | 0.69 | [Source: opentargets_get_associations(ENSG00000196712)] |

3078 associations total; the top 10 were retrieved. **Every row returned `evidence_count: 0` and an empty `evidence_sources` array**, so the scores are usable but their provenance is not inspectable through this tool [Source: opentargets_get_associations(ENSG00000196712)].

### Pathway membership

**No data retrieved.** `wikipathways_get_pathways_for_gene` returned 0 results for TOP2B by both symbol and Entrez ID [No data: wikipathways_get_pathways_for_gene("TOP2B"), wikipathways_get_pathways_for_gene("7155")]. No pathway membership is asserted for the topoisomerase axis. Template 2 requires this section; it is empty by tool outcome, not by omission.

### Network properties

- Nodes persisted: 17 (10 Gene, 2 Compound, 2 Disease, 3 Trial)
- Edges persisted: 15
- STRING interactions returned at threshold 700: 15; NF1-incident: 4
- Mean STRING score of NF1-incident edges: 0.94
- Regulatory vs physical: the four NF1-incident STRING edges are scored associations without direction; the directional edges (NF1-to-BCL2L1, doxorubicin-to-AXL/NFKB1) come from PubMed abstracts, not interaction databases

---

## Clinical Trials

| NCT ID | Title | Design | Status | MPNST eligible | Verified | Source |
|--------|-------|--------|--------|----------------|----------|--------|
| NCT02584309 | A Non-Inferiority Study of Doxorubicin With Upfront Dexrazoxane for the Treatment of Advanced or Metastatic Soft Tissue Sarcoma | Interventional, non-randomized, parallel, no masking; doxorubicin 75 mg/m2; PFS primary, cardiac-related mortality and CTRCD rate secondary; Washington University School of Medicine; 2016-02-22 to 2022-07-17 | COMPLETED | Yes (listed histology) | Yes | [Source: clinicaltrials_get_trial(NCT:02584309)] |
| NCT05858710 | Study of DPPG2-TSL-DOX Combined With Hyperthermia in Soft Tissue Sarcoma | Interventions: DPPG2-TSL-DOX, dexrazoxane | COMPLETED | Not listed | Search only | [Source: clinicaltrials_search_trials("dexrazoxane cardioprotection sarcoma doxorubicin")] |
| NCT06849986 | IO Combined With AI as First-line Treatment for Patients With Soft Tissue Sarcoma (TAIS) | Tislelizumab + liposomal doxorubicin + ifosfamide | RECRUITING | Yes | Search only | [Source: clinicaltrials_search_trials("doxorubicin malignant peripheral nerve sheath tumor")] |
| NCT06277154 | MASCT-I Combined With Doxorubicin and Ifosfamide for First-line Treatment of Advanced Soft Tissue Sarcoma | MASCT-I + doxorubicin + ifosfamide | RECRUITING | Yes | Search only | [Source: clinicaltrials_search_trials("doxorubicin malignant peripheral nerve sheath tumor")] |

26 MPNST-and-doxorubicin trials exist in total; 8 were retrieved [Source: clinicaltrials_search_trials("doxorubicin malignant peripheral nerve sheath tumor")].

**NCT02584309 carries the exact logic of this competency question** — efficacy as the primary endpoint, cardiac toxicity as secondary, under upfront cardioprotection. **Its results were not retrieved.** The registry record gives the design only; whether non-inferiority was met is unknown from this pipeline.

---

## Evidence Assessment

| # | Claim | Base | Modifiers | Final | Level |
|---|-------|------|-----------|-------|-------|
| 1 | Doxorubicin's recorded mechanism is TOP2A inhibition | L2 0.55 (Open Targets + PubMed 28813519 concordance) | mechanism match +0.10, literature support +0.05, ChEMBL returned 0 mechanisms (absence, not conflict) +0.00, single-DB penalty not applied | **0.72** | L3 Functional |
| 2 | TOP2B mediates doxorubicin cardiotoxicity in cardiomyocytes | L1 0.45 (one publication) | literature support +0.05 | **0.50** | L1/L2 boundary |
| 3 | Cardiotoxicity is a top-4 doxorubicin FAERS signal | L1 0.45 (Open Targets adverseEvents) | literature support +0.05 (PMID 23104132 independently characterises dose-dependent cardiotoxicity) | **0.50** | L1/L2 boundary |
| 4 | Dexrazoxane is a max-phase-4 agent with iron-sequestering and topo II inhibitor mechanisms | L4 0.90 (approved, max_phase 4) | single source -0.10 (ChEMBL only) | **0.80** | L3 Functional |
| 5 | Dexrazoxane acts selectively on TOP2B | L1 0.40 | unverified ID -0.15 (CHEMBL2094255 isoform not disambiguated) | **0.25** | **Insufficient Evidence** |
| 6 | NF1 is a Ras GAP | L2 0.55 (UniProt function + STRING) | high STRING score +0.05 (KRAS 0.998) | **0.60** | L2 Multi-DB |
| 7 | NF1 loss upregulates BCL2L1 via Erk1/2, causing doxorubicin resistance reversible by ABT-737 | L1 0.45 (one publication) | literature support +0.05 | **0.50** | L1/L2 boundary |
| 8 | AXL and NFKB1 are activated after doxorubicin in NF1-MPNST | L1 0.45 (one publication) | none | **0.45** | L1 Single-DB |
| 9 | BRD4, EZH2 and TOP2A are expressed in human NF1-derived MPNSTs | L1 0.45 (one publication) | none | **0.45** | L1 Single-DB |
| 10 | TOP2A is far more CRISPR-essential than TOP2B (883 vs 24 hit screens) | L1 0.45 (BioGRID ORCS) | single source -0.05 (cell_line, phenotype and scoring_method returned null) | **0.40** | L1 Single-DB |
| 11 | NF1 is associated with NF1 disease (0.89) and MPNST (0.69) | L1 0.45 (Open Targets) | evidence_sources empty -0.10 | **0.35** | L1 Single-DB |
| 12 | NCT02584309 tests doxorubicin + upfront dexrazoxane with PFS primary and cardiac endpoints secondary, MPNST eligible | L3 0.70 (authoritative registry, Phase 5 verified via get_trial) | none; results not retrieved | **0.70** | L3 Functional |

**Median: 0.50. Range: 0.25-0.80.** One claim (#5) falls below L1 and is flagged Insufficient Evidence.

The confidence is held down by a structural feature of the evidence, not by sloppy retrieval: **every NF1-specific claim rests on a single publication**. The isoform-selectivity claims (#1, #4) are the best-supported; the NF1-specific resistance claims (#7, #8, #9) are each one paper deep. Note also that the rubric scores by source count, not experimental strength — claim #2 is a causal cardiomyocyte-specific knockout in *Nature Medicine* and scores 0.50 purely because no second database corroborates it.

---

## Gaps and Limitations

**Tool failures and empty results**

- `get_mechanism(CHEMBL:53463)` returned `ENTITY_NOT_FOUND`; the `curl ChEMBL/mechanism.json` fallback returned 0 mechanisms. The TOP2A mechanism rests on Open Targets alone.
- `chembl_get_compound(CHEMBL:53463)` returned name only, `molecular_formula: null`. No physicochemical profile.
- `wikipathways_get_pathways_for_gene` returned 0 results for TOP2B by symbol and by Entrez ID. **No pathway membership is asserted anywhere in this report.**
- All `opentargets_get_associations` rows returned `evidence_count: 0` with empty `evidence_sources`.
- ORCS `slim` responses returned `cell_line`, `phenotype` and `scoring_method` as null, so the 883-vs-24 essentiality contrast **cannot be attributed to NF1-mutant lines specifically**.

**Not retrieved**

- **Results for NCT02584309.** The question's own clinical test completed in 2022 and its outcome is unknown from this pipeline. This is the single highest-value gap.
- Dexrazoxane's TOP2A-versus-TOP2B selectivity ratio. No IC50 or Ki values were retrieved for either isoform, so the Selectivity Comparison section of Template 7 cannot be populated.
- Liposomal doxorubicin formulation data, despite two retrieved trials using it (NCT06849986, NCT05858710).
- MCL1 is persisted as a node with no retrieved edge; it is context, not a finding.
- KRAS is a partial node (symbol and STRING score only), not enriched via `hgnc_get_gene`.

**Scope boundaries**

- **No evidence was retrieved that NF1 status modulates anthracycline cardiotoxicity.** The TOP2B cardioprotection axis is general oncology, not NF1-specific; the NF1-specific findings are all tumor-side resistance. Any claim of NF1-specific cardioprotection would be unsupported.
- The ABT-737 / low-dose doxorubicin synergy (claim #7) is cell-line work in sNF96.2; no in vivo or clinical confirmation was retrieved.
- No gold-standard path exists for this question, so no gold-standard validation score is reported. Validation was evidence-level only.
- Phase 6a persisted to local JSON files; **nothing was written to Graphiti**.

---

## Appendix: Tools Used

| Phase | Tool | Purpose | Outcome |
|-------|------|---------|---------|
| 1 ANCHOR | `hgnc_search_genes` x7 | Resolve NF1, TOP2A, TOP2B, BCL2L1, AXL, NFKB1, BRD4, EZH2, MCL1 | All resolved |
| 1 ANCHOR | `chembl_search_compounds` x2 | Resolve doxorubicin, dexrazoxane | CHEMBL:53463, CHEMBL:1738 |
| 1 ANCHOR | `opentargets_search_targets` | Resolve NF1 to Ensembl | ENSG00000196712 |
| 2 ENRICH | `hgnc_get_gene` x4, `curl HGNC/fetch` x6 | Cross-references for all gene nodes | Complete for 9 of 10 |
| 2 ENRICH | `uniprot_get_protein` | Neurofibromin function text | Retrieved |
| 2 ENRICH | `opentargets_get_associations` | NF1 disease anchors | Scores retrieved, evidence empty |
| 3 EXPAND | `string_search_proteins`, `string_get_interactions` | NF1 network at score 700 | 15 interactions |
| 3 EXPAND | `wikipathways_get_pathways_for_gene` x2 | TOP2B pathway membership | 0 results |
| 3 EXPAND | `get_orcs_essentiality` x2 | TOP2A/TOP2B CRISPR essentiality | 883 / 24 hit screens |
| 4a DRUGS | `curl OpenTargets/graphql` | Doxorubicin mechanism + adverse events | TOP2A inhibitor, 21 AE terms |
| 4a DRUGS | `get_mechanism`, `curl ChEMBL/mechanism` | Doxorubicin, dexrazoxane mechanisms | Failed for doxorubicin; 2 mechanisms for dexrazoxane |
| 4b TRIALS | `clinicaltrials_search_trials` x2 | MPNST + doxorubicin, dexrazoxane cardioprotection | 26 and 4 total |
| 5 VALIDATE | `clinicaltrials_get_trial` | Verify NCT02584309 | Verified, full design |
| 5 VALIDATE | `pubmed search_articles` x7, `get_article_metadata` x3 | Literature grounding | 4 papers cited |
| 6a PERSIST | local file write | results/entities/edges/validation JSON | Written; Graphiti not used |

## Appendix: Literature Cited

All literature retrieved from PubMed.

- Zhang S, et al. Identification of the molecular basis of doxorubicin-induced cardiotoxicity. *Nat Med* 2012;18(11):1639-42. PMID 23104132. [DOI](https://doi.org/10.1038/nm.2919)
- Park HJ, et al. NF1 deficiency causes Bcl-xL upregulation in Schwann cells derived from neurofibromatosis type 1-associated malignant peripheral nerve sheath tumors. *Int J Oncol* 2013;42(2):657-66. PMID 23292448. [DOI](https://doi.org/10.3892/ijo.2012.1751)
- Grit JL, et al. Kinome Profiling of NF1-Related MPNSTs in Response to Kinase Inhibition and Doxorubicin Reveals Therapeutic Vulnerabilities. *Genes (Basel)* 2020;11(3):331. PMID 32245042. [DOI](https://doi.org/10.3390/genes11030331)
- Expression and inhibition of BRD4, EZH2 and TOP2A in neurofibromas and malignant peripheral nerve sheath tumors. *PLoS One* 2017. PMID 28813519. [DOI](https://doi.org/10.1371/journal.pone.0183155)
- A High-Throughput Screening Platform Identifies Novel Combination Treatments for Malignant Peripheral Nerve Sheath Tumors. *Mol Cancer Ther* 2022. PMID 35511749. [DOI](https://doi.org/10.1158/1535-7163.MCT-21-0947)
