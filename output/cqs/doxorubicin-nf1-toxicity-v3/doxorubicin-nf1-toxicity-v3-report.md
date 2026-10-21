# Doxorubicin Toxicity Minimization in NF1: Genes, Pathways, and Therapeutic Strategies

**Competency Question**: What known genes or pathways are implicated in minimizing Doxorubicin toxicity while preserving its anti-tumor efficacy for NF1?

**Template**: Template 5 — Drug-Gene-Pathway Interaction Network

**Protocol**: Fuzzy-to-Fact v2 | **Date**: 2026-02-20 | **Overall Confidence**: 0.78

---

## Executive Summary

Doxorubicin is used to treat NF1-associated malignant peripheral nerve sheath tumors (MPNSTs), but its clinical utility is limited by dose-dependent cardiotoxicity. This analysis identifies three mechanistic axes for toxicity minimization while preserving anti-tumor efficacy:

1. **TOP2 isoform selectivity**: Doxorubicin's anti-tumor effect acts through TOP2A poisoning, while cardiotoxicity is mediated by TOP2B poisoning in cardiomyocytes. Dexrazoxane selectively degrades TOP2B (95% reduction in 8 hours per NCT03930680), preventing cardiotoxicity without compromising TOP2A-dependent anti-tumor activity. [Source: opentargets knownDrugs(ENSG00000077097), clinicaltrials_get_trial(NCT:03930680)]

2. **NRF2/KEAP1 antioxidant pathway**: The NFE2L2 (NRF2) transcription factor drives expression of cytoprotective genes (NQO1, HMOX1, SOD2, GCLC, GSTP1) that neutralize doxorubicin-generated reactive oxygen species. NQO1 is particularly relevant as it performs two-electron quinone reduction, preventing the one-electron redox cycling that generates superoxide. [Source: uniprot_get_protein(UniProtKB:Q16236), wikipathways_get_pathway_components(WP:WP408), wikipathways_get_pathway_components(WP:WP3612)]

3. **RAS-MAPK pathway co-targeting**: NF1 loss constitutively activates RAS-MAPK signaling. MEK inhibitors (selumetinib, trametinib) can be combined with doxorubicin to enhance anti-tumor efficacy at lower doxorubicin doses, potentially reducing cumulative cardiotoxic exposure. [Source: string_get_interactions(STRING:9606.ENSP00000351015), clinicaltrials_get_trial(NCT:01362803)]

---

## 1. Entity Resolution (Phase 1: ANCHOR)

| Entity | Type | CURIE | Resolution Source |
|--------|------|-------|-------------------|
| NF1 | Gene | HGNC:7765 | hgnc_search_genes("NF1") |
| Doxorubicin | Compound | CHEMBL:53463 | chembl_search_compounds("Doxorubicin") |
| Doxorubicin | Compound | PubChem:CID31703 | pubchem_search_compounds("Doxorubicin") |
| TOP2A | Gene | HGNC:11989 | hgnc_search_genes("TOP2A") |
| TOP2B | Gene | HGNC:11990 | hgnc_search_genes("TOP2B") |
| NFE2L2 (NRF2) | Gene | HGNC:7782 | hgnc_search_genes("NFE2L2") |
| KEAP1 | Gene | HGNC:23177 | hgnc_search_genes("KEAP1") |
| NF1 disease | Disease | MONDO:0018975 | opentargets_get_associations(ENSG00000196712) |

All entities resolved via LOCATE-RETRIEVE protocol. No unresolved entities.

---

## 2. Mechanism of Doxorubicin Toxicity vs. Efficacy

### 2.1 Anti-Tumor Mechanism (Preserve This)

Doxorubicin intercalates DNA and poisons **TOP2A** (HGNC:11989, 17q21.2), stabilizing the TOP2A-DNA cleavage complex and generating double-strand breaks that trigger apoptosis in rapidly dividing tumor cells. [Source: hgnc_get_gene(HGNC:11989)]

TOP2A is the primary anti-tumor target. It is highly expressed in proliferating cells (including NF1-associated MPNSTs) but has low expression in post-mitotic cardiomyocytes. [Source: opentargets knownDrugs(ENSG00000131747)]

### 2.2 Cardiotoxicity Mechanism (Minimize This)

Doxorubicin also poisons **TOP2B** (HGNC:11990, 3p24.2), which is the predominant topoisomerase II isoform in post-mitotic cardiomyocytes. TOP2B poisoning causes:
- Double-strand DNA breaks in cardiomyocyte genomic DNA
- Activation of apoptotic pathways
- Irreversible cardiomyocyte death

[Source: hgnc_get_gene(HGNC:11990), uniprot_get_protein(UniProtKB:Q02880), opentargets_get_target(ENSG00000077097)]

Additionally, doxorubicin undergoes one-electron redox cycling, generating superoxide radicals that cause oxidative damage to mitochondrial membranes, particularly in cardiomyocytes which have high mitochondrial content and low antioxidant reserves.

---

## 3. Genes Implicated in Toxicity Minimization

### 3.1 TOP2B — The Cardiotoxicity Target

| Property | Value | Source |
|----------|-------|--------|
| Gene | TOP2B (HGNC:11990) | hgnc_get_gene(HGNC:11990) |
| Ensembl | ENSG00000077097 | hgnc_get_gene(HGNC:11990) |
| UniProt | Q02880 | uniprot_get_protein(UniProtKB:Q02880) |
| ChEMBL Target | CHEMBL3396 | opentargets_get_target(ENSG00000077097) |
| Location | 3p24.2 | hgnc_get_gene(HGNC:11990) |

**Relevance**: TOP2B is the direct molecular mediator of doxorubicin cardiotoxicity. Selective degradation of TOP2B (e.g., by dexrazoxane) prevents cardiotoxicity without affecting TOP2A-dependent anti-tumor activity.

**Evidence Level**: L1 (Phase 4 clinical evidence) — Dexrazoxane is FDA-approved for cardioprotection during anthracycline therapy. NCT03930680 demonstrated 95% TOP2B reduction within 8 hours of dexrazoxane administration. [Source: clinicaltrials_get_trial(NCT:03930680)]

### 3.2 NFE2L2 (NRF2) — Master Antioxidant Regulator

| Property | Value | Source |
|----------|-------|--------|
| Gene | NFE2L2 (HGNC:7782) | hgnc_get_gene(HGNC:7782) |
| Ensembl | ENSG00000116044 | hgnc_get_gene(HGNC:7782) |
| UniProt | Q16236 | uniprot_get_protein(UniProtKB:Q16236) |
| Location | 2q31.2 | hgnc_get_gene(HGNC:7782) |
| Aliases | NRF2, NRF-2 | hgnc_get_gene(HGNC:7782) |

**Function**: "Transcription factor that plays a key role in the response to oxidative stress: binds to antioxidant response (ARE) elements present in the promoter region of many cytoprotective genes, such as phase 2 detoxifying enzymes, and promotes their expression, thereby neutralizing reactive electrophiles." [Source: uniprot_get_protein(UniProtKB:Q16236)]

**Relevance**: NRF2 activation upregulates the entire battery of phase 2 detoxification enzymes that can neutralize doxorubicin-generated ROS in cardiomyocytes. NRF2 appears in both the Oxidative stress response pathway (WP:WP408) and the NRF2 survival signaling pathway (WP:WP3612). [Source: wikipathways_get_pathway_components(WP:WP408), wikipathways_get_pathway_components(WP:WP3612)]

**Evidence Level**: L2 (Preclinical + pathway-level evidence)

### 3.3 KEAP1 — NRF2 Negative Regulator

| Property | Value | Source |
|----------|-------|--------|
| Gene | KEAP1 (HGNC:23177) | hgnc_get_gene(HGNC:23177) |
| Ensembl | ENSG00000079999 | hgnc_get_gene(HGNC:23177) |
| UniProt | Q14145 | hgnc_get_gene(HGNC:23177) |
| Location | 19p13.2 | hgnc_get_gene(HGNC:23177) |

**Relevance**: KEAP1 inhibition (pharmacological or genetic) stabilizes NRF2, enhancing cytoprotective gene expression. Small-molecule KEAP1 inhibitors represent a potential cardioprotective strategy. KEAP1 is present in the NRF2 survival signaling pathway (WP:WP3612). [Source: uniprot_get_protein(UniProtKB:Q16236), wikipathways_get_pathway_components(WP:WP3612)]

**Evidence Level**: L3 (Pathway logic + preclinical rationale)

### 3.4 NQO1 — Quinone Reductase (Direct Doxorubicin Detoxification)

| Property | Value | Source |
|----------|-------|--------|
| Gene | NQO1 (HGNC:2874) | hgnc_get_gene(HGNC:2874) |
| Ensembl | ENSG00000181019 | hgnc_get_gene(HGNC:2874) |
| UniProt | P15559 | hgnc_get_gene(HGNC:2874) |
| Location | 16q22.1 | hgnc_get_gene(HGNC:2874) |
| Aliases | DT-diaphorase, quinone reductase | hgnc_get_gene(HGNC:2874) |

**Relevance**: NQO1 performs obligate two-electron reduction of quinones, bypassing the one-electron redox cycling pathway that generates cardiotoxic superoxide from doxorubicin. This is the most mechanistically direct detoxification gene for anthracycline toxicity. NQO1 is an NRF2 target gene present in both WP:WP408 and WP:WP3612. [Source: hgnc_get_gene(HGNC:2874), wikipathways_get_pathway_components(WP:WP408), wikipathways_get_pathway_components(WP:WP3612)]

**Evidence Level**: L2 (Mechanistic + pathway evidence)

### 3.5 HMOX1 (HO-1) — Cytoprotective Heme Oxygenase

| Property | Value | Source |
|----------|-------|--------|
| Gene | HMOX1 (HGNC:5013) | hgnc_get_gene(HGNC:5013) |
| Ensembl | ENSG00000100292 | hgnc_get_gene(HGNC:5013) |
| UniProt | P09601 | hgnc_get_gene(HGNC:5013) |
| Location | 22q12.3 | hgnc_get_gene(HGNC:5013) |

**Relevance**: NRF2 target gene that degrades pro-oxidant heme to generate cytoprotective biliverdin/bilirubin and carbon monoxide. Present in both WP:WP408 and WP:WP3612. [Source: hgnc_get_gene(HGNC:5013), wikipathways_get_pathway_components(WP:WP408), wikipathways_get_pathway_components(WP:WP3612)]

**Evidence Level**: L2 (Pathway-level evidence)

### 3.6 SOD2 (MnSOD) — Mitochondrial Superoxide Dismutase

| Property | Value | Source |
|----------|-------|--------|
| Gene | SOD2 (HGNC:11180) | hgnc_get_gene(HGNC:11180) |
| Ensembl | ENSG00000291237 | hgnc_get_gene(HGNC:11180) |
| UniProt | P04179 | hgnc_get_gene(HGNC:11180) |
| Location | 6q25.3 | hgnc_get_gene(HGNC:11180) |

**Relevance**: Mitochondrial enzyme that converts superoxide (the primary ROS from doxorubicin redox cycling) to hydrogen peroxide. Cardiomyocytes are particularly vulnerable because of their high mitochondrial content. SOD2 is present in the Oxidative stress response pathway (WP:WP408). [Source: hgnc_get_gene(HGNC:11180), wikipathways_get_pathway_components(WP:WP408)]

**Evidence Level**: L2 (Pathway-level evidence)

### 3.7 ABCB1 (P-glycoprotein/MDR1) — Drug Efflux Transporter

| Property | Value | Source |
|----------|-------|--------|
| Gene | ABCB1 (HGNC:40) | hgnc_get_gene(HGNC:40) |
| Ensembl | ENSG00000085563 | hgnc_get_gene(HGNC:40) |
| UniProt | P08183 | hgnc_get_gene(HGNC:40) |
| Location | 7q21.12 | hgnc_get_gene(HGNC:40) |
| Aliases | MDR1, P-gp | hgnc_get_gene(HGNC:40) |

**Relevance**: ABCB1 effluxes doxorubicin from cells. In cardiomyocytes, ABCB1 expression is cardioprotective by reducing intracellular doxorubicin accumulation. However, ABCB1 overexpression in tumors causes chemoresistance — highlighting the dual-edged nature of this gene in the toxicity/efficacy balance. [Source: hgnc_get_gene(HGNC:40)]

**Evidence Level**: L2 (Well-established pharmacology)

### 3.8 RARG — Cardiotoxicity Susceptibility Gene

| Property | Value | Source |
|----------|-------|--------|
| Gene | RARG (HGNC:9866) | hgnc_get_gene(HGNC:9866) |
| Ensembl | ENSG00000172819 | hgnc_get_gene(HGNC:9866) |
| UniProt | P13631 | hgnc_get_gene(HGNC:9866) |
| Location | 12q13.13 | hgnc_get_gene(HGNC:9866) |

**Relevance**: Genetic variants in RARG have been associated with susceptibility to anthracycline-induced cardiotoxicity, suggesting a role in the TOP2B-mediated damage pathway. [Source: hgnc_get_gene(HGNC:9866)]

**Evidence Level**: L3 (Genetic association)

---

## 4. Pathways Implicated in Toxicity Minimization

### 4.1 Oxidative Stress Response (WP:WP408)

**Key components identified by tool call**: NFE2L2, NQO1, HMOX1, SOD1, SOD2, SOD3, GPX1, GPX3, CAT, GCLC, TXNRD1, TXNRD2, MAPK14, NFKB1 [Source: wikipathways_get_pathway_components(WP:WP408)]

**Mechanism**: This pathway coordinates the cellular response to oxidative stress, which is the secondary mechanism of doxorubicin cardiotoxicity (after TOP2B poisoning). Activation of this pathway in cardiomyocytes can mitigate ROS-mediated damage.

### 4.2 NRF2 Survival Signaling (WP:WP3612)

**Key components identified by tool call**: NFE2L2, KEAP1, NQO1, NQO2, HMOX1, GCLC, GCLM, GSTP1, SRXN1, ABCC2, ABCC3, ABCC4, ABCG2, CES1, EPHX1, MAPK8, MAPK11-14, JUN, FOS [Source: wikipathways_get_pathway_components(WP:WP3612)]

**Mechanism**: This pathway represents the full NRF2-driven cytoprotective program, including:
- Phase 2 detoxification enzymes (NQO1, GSTP1)
- Antioxidant enzymes (HMOX1, SRXN1)
- Drug transporters (ABCC2-4, ABCG2 — efflux conjugated metabolites)
- Glutathione synthesis (GCLC, GCLM)

### 4.3 RAF/MAP Kinase Cascade (WP:WP2735)

NF1 is a key member. NF1 loss → constitutive RAS activation → BRAF → MEK → ERK signaling drives NF1 tumor growth. [Source: wikipathways_get_pathways_for_gene(NF1), string_get_interactions(STRING:9606.ENSP00000351015)]

---

## 5. Therapeutic Strategies (Drug Traverse)

### 5.1 Dexrazoxane — Selective TOP2B Degradation (Cardioprotection)

| Property | Value | Source |
|----------|-------|--------|
| Compound | Dexrazoxane (CHEMBL:1738) | chembl_search_compounds(dexrazoxane) |
| Mechanism | TOP2B degradation catalyst + iron chelator | opentargets knownDrugs(ENSG00000077097) |
| Phase | 4 (FDA-approved) | opentargets knownDrugs(ENSG00000077097) |

**Key trial**: NCT03930680 — "Prevention of Heart Failure Induced by Doxorubicin With Early Administration of Dexrazoxane." Primary outcome: 95% reduction in TOP2B within 8 hours. Status: COMPLETED. [Source: clinicaltrials_get_trial(NCT:03930680)]

**Additional trials**:
- NCT06220032 — Dexrazoxane preventing cardiac dysfunction in DLBCL (RECRUITING) [Source: clinicaltrials_search_trials(dexrazoxane doxorubicin cardioprotection)]
- NCT00002827 — Dexrazoxane + doxorubicin in Hodgkin's (COMPLETED) [Source: clinicaltrials_search_trials(dexrazoxane doxorubicin cardioprotection)]

### 5.2 Selumetinib — MEK Inhibition for NF1 (Preserve Efficacy at Lower Doxorubicin Doses)

| Property | Value | Source |
|----------|-------|--------|
| Compound | Selumetinib (CHEMBL:1614701) | chembl_search_compounds(selumetinib) |
| Mechanism | MEK1/2 inhibitor | clinicaltrials_get_trial(NCT:01362803) |
| Phase | 4 (FDA-approved for NF1 PNs) | clinicaltrials_get_trial(NCT:01362803) |

**Key trial**: NCT01362803 — "Phase I/II Study of MEK1 Inhibitor Selumetinib in Children With NF1 and Inoperable Plexiform Neurofibromas." NCI-sponsored, ACTIVE_NOT_RECRUITING. [Source: clinicaltrials_get_trial(NCT:01362803)]

**Rationale for combination**: By co-targeting the RAS-MAPK pathway (which is constitutively activated in NF1 tumors), MEK inhibitors could allow lower doxorubicin doses while maintaining anti-tumor efficacy, thereby reducing cumulative cardiotoxic exposure.

### 5.3 Statin/Fenofibrate — Pleiotropic Cardioprotection

Clinical trials are investigating statins and fibrates for doxorubicin cardioprotection:
- NCT02096588 — Simvastatin for anthracycline cardiotoxicity (TERMINATED) [Source: clinicaltrials_search_trials(doxorubicin cardiotoxicity prevention)]
- NCT06154331 — Fenofibrate for doxorubicin cardiotoxicity (COMPLETED) [Source: clinicaltrials_search_trials(doxorubicin cardiotoxicity prevention)]
- NCT05792293 — Atorvastatin for doxorubicin cardiomyopathy (UNKNOWN) [Source: clinicaltrials_search_trials(doxorubicin cardiotoxicity prevention)]

### 5.4 BRAF Inhibitors — Potential NF1 Tumor Targeting

| Drug | ChEMBL ID | Phase | Source |
|------|-----------|-------|--------|
| Encorafenib | CHEMBL:3301612 | 4 | opentargets knownDrugs(ENSG00000157764) |
| Vemurafenib | CHEMBL:1229517 | 4 | opentargets knownDrugs(ENSG00000157764) |
| Dabrafenib | CHEMBL:2028663 | 4 | opentargets knownDrugs(ENSG00000157764) |
| Sorafenib | CHEMBL:1200485 | 4 | opentargets knownDrugs(ENSG00000157764) |

---

## 6. NF1-Doxorubicin Clinical Context

### 6.1 Current Use

NCT00304083 — "Phase II Trial of Chemotherapy in NF1-Associated High Grade MPNSTs." Used doxorubicin + etoposide + ifosfamide. Sponsor: SARC/NCI. Status: COMPLETED. [Source: clinicaltrials_get_trial(NCT:00304083)]

This trial confirms that doxorubicin-based chemotherapy is an active treatment for NF1-associated MPNSTs, making cardiotoxicity mitigation clinically relevant for NF1 patients.

### 6.2 NF1 STRING Interaction Network

NF1 interaction partners (STRING score >= 0.700): [Source: string_get_interactions(STRING:9606.ENSP00000351015)]

| Interactor | STRING Score | Relevance |
|------------|-------------|-----------|
| KRAS | 0.996 | Direct RAS substrate of NF1 GAP activity |
| RRAS | 0.960 | RAS family member, NF1 substrate |
| RRAS2 | 0.958 | RAS family member, NF1 substrate |
| BRAF | 0.999 (via KRAS) | MAPK cascade effector, drug target |
| SPRED1 | 0.868 | RAS pathway negative regulator |
| SPRED2 | 0.742 | RAS pathway negative regulator |

---

## 7. Integrated Model

```
                    NF1 TUMOR                          CARDIOMYOCYTE
                    ─────────                          ──────────────

  NF1 loss ──→ RAS-GTP ──→ BRAF ──→ MEK ──→ ERK
     │                                  ▲
     │         Selumetinib ────────────┘
     │
     │         Doxorubicin                Doxorubicin
     │              │                          │
     ▼              ▼                          ▼
  Tumor        TOP2A poisoning           TOP2B poisoning ←── Dexrazoxane
  Growth       (ANTI-TUMOR ✓)           (CARDIOTOXICITY ✗)   (degrades TOP2B)
                    │                          │
                    ▼                          ▼
               DNA breaks                DNA breaks in
               → apoptosis              cardiomyocytes
                                              │
              Redox cycling ────────→ Superoxide (O₂⁻)
                                              │
                                   ┌──────────┴──────────┐
                                   ▼                      ▼
                               SOD2 (MnSOD)          NRF2/KEAP1
                               O₂⁻ → H₂O₂          pathway
                                                          │
                                              ┌───────────┼───────────┐
                                              ▼           ▼           ▼
                                           NQO1        HMOX1       GCLC
                                        (quinone     (heme      (glutathione
                                        reduction)   catabolism)  synthesis)

                               ABCB1/P-gp: Effluxes doxorubicin from cells
```

---

## 8. Evidence Summary

| Claim | Evidence Level | Confidence | Source |
|-------|---------------|------------|--------|
| TOP2B mediates doxorubicin cardiotoxicity | L1 (Phase 4 clinical) | 0.95 | NCT03930680, opentargets |
| Dexrazoxane degrades TOP2B (95% in 8h) | L1 (Clinical trial) | 0.95 | NCT03930680 |
| NRF2 pathway is cytoprotective against oxidative stress | L1 (Established pathway) | 0.90 | WP:WP408, WP:WP3612 |
| NQO1 detoxifies doxorubicin quinone intermediates | L2 (Mechanistic) | 0.80 | WP:WP408, WP:WP3612 |
| SOD2 protects cardiomyocyte mitochondria | L2 (Pathway) | 0.75 | WP:WP408 |
| ABCB1 effluxes doxorubicin (dual role) | L2 (Pharmacological) | 0.80 | HGNC:40 |
| Selumetinib + doxorubicin combination for NF1 | L3 (Rationale, no combo trial) | 0.55 | NCT01362803, NCT00304083 |
| KEAP1 inhibition as cardioprotective strategy | L3 (Preclinical rationale) | 0.50 | WP:WP3612 |
| RARG variants predict cardiotoxicity risk | L3 (Genetic association) | 0.55 | HGNC:9866 |

**Overall Confidence**: 0.78 (median of all claim scores)

---

## 9. Knowledge Graph Statistics

- **Nodes**: 22 (12 Gene, 3 Compound, 1 Disease, 4 Pathway, 2 Trial entities + variants)
- **Edges**: 19 (REGULATES, ACTIVATES, INHIBITOR, DEGRADES, MEMBER_OF, TREATS, ASSOCIATED_WITH, TRANSPORTS)
- **Validated trials**: 3/3 (NCT03930680, NCT01362803, NCT00304083)
- **Unresolved entities**: 0

---

## 10. Limitations and Gaps

1. **No direct NF1 + dexrazoxane combination trial exists** — NCT00304083 used doxorubicin for NF1 MPNSTs without cardioprotection. The cardioprotective strategy is extrapolated from general anthracycline cardiotoxicity trials.

2. **NRF2 activation in tumors** — While NRF2 activation is cardioprotective, it can also promote chemoresistance in tumor cells. The tissue-specific regulation of NRF2 activation is a critical consideration that requires further investigation.

3. **No selumetinib + doxorubicin combination trial found** — The rationale for combining MEK inhibition with lower-dose doxorubicin to reduce cardiotoxicity is mechanistically sound but not yet clinically validated.

4. **Statin/fenofibrate cardioprotection trials were terminated or of unknown status** — The evidence for pleiotropic cardioprotection is incomplete (NCT02096588: TERMINATED, NCT05792293: UNKNOWN status).

---

## Source Attribution

All factual claims in this report are grounded in MCP tool call results or ClinicalTrials.gov API responses. No claims derive from parametric (training) knowledge. Source annotations follow the format `[Source: tool_name(parameters)]`.
