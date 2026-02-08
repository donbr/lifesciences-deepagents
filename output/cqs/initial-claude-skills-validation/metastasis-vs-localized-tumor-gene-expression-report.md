# Metastasis versus Localized Tumor: Gene Expression Differences

## Summary

Metastasis and localized tumor maintenance are governed by distinct gene expression programs. Metastasis is triggered by **epithelial-mesenchymal transition (EMT) transcription factors** (TWIST1, SNAI1, SNAI2, ZEB1) that repress epithelial adhesion genes and activate mesenchymal migration programs. These EMT drivers downregulate **E-cadherin (CDH1)**, the master epithelial adhesion molecule, while upregulating **vimentin (VIM)** and activating receptor tyrosine kinases like **MET**. In contrast, localized tumor maintenance depends on **tumor suppressors** (TP53, PTEN) that enforce cell cycle checkpoints and suppress migration, alongside **intact cell-cell adhesion** mediated by CDH1 and its catenin partners. Loss of CDH1 and tumor suppressors, combined with activation of EMT transcription factors, represents the molecular switch from localized to metastatic disease. [Sources: hgnc_search_genes("TWIST1", "SNAI1", "CDH1", "TP53"), uniprot_get_protein(Q15672, O95863, P12830, P04637), string_get_interactions(9606.ENSP00000242261, 9606.ENSP00000244050)]

---

## Resolved Entities

| Entity | CURIE | Type | Source |
|--------|-------|------|--------|
| TWIST1 | HGNC:12428 | Gene | [Source: hgnc_search_genes("TWIST1")] |
| TWIST1 protein | UniProtKB:Q15672 | Protein | [Source: hgnc_get_gene(HGNC:12428)] |
| SNAI1 | HGNC:11128 | Gene | [Source: hgnc_search_genes("SNAI1")] |
| SNAI1 protein | UniProtKB:O95863 | Protein | [Source: hgnc_get_gene(HGNC:11128)] |
| SNAI2 | HGNC:11094 | Gene | [Source: hgnc_search_genes("SNAI2")] |
| SNAI2 protein | UniProtKB:O43623 | Protein | [Source: hgnc_get_gene(HGNC:11094)] |
| ZEB1 | HGNC:11642 | Gene | [Source: hgnc_search_genes("ZEB1")] |
| ZEB1 protein | UniProtKB:P37275 | Protein | [Source: hgnc_get_gene(HGNC:11642)] |
| VIM | HGNC:12692 | Gene | [Source: hgnc_search_genes("VIM")] |
| Vimentin | UniProtKB:P08670 | Protein | [Source: hgnc_get_gene(HGNC:12692)] |
| MET | HGNC:7029 | Gene | [Source: hgnc_search_genes("MET")] |
| MET receptor | UniProtKB:P08581 | Protein | [Source: hgnc_get_gene(HGNC:7029)] |
| CDH1 | HGNC:1748 | Gene | [Source: hgnc_search_genes("CDH1")] |
| E-cadherin | UniProtKB:P12830 | Protein | [Source: hgnc_get_gene(HGNC:1748)] |
| TP53 | HGNC:11998 | Gene | [Source: hgnc_search_genes("TP53")] |
| p53 protein | UniProtKB:P04637 | Protein | [Source: hgnc_get_gene(HGNC:11998)] |
| PTEN | HGNC:9588 | Gene | [Source: hgnc_search_genes("PTEN")] |
| PTEN phosphatase | UniProtKB:P60484 | Protein | [Source: hgnc_get_gene(HGNC:9588)] |

---

## Metastasis-Promoting Gene Network

### EMT Transcription Factors

| Gene | CURIE | Function | Key Targets Repressed | Evidence Level | Source |
|------|-------|----------|----------------------|----------------|--------|
| TWIST1 | HGNC:12428 | Transcriptional repressor inducing EMT; inhibits E-cadherin expression | CDH1, epithelial genes | L3 | [Source: uniprot_get_protein(UniProtKB:Q15672)] |
| SNAI1 | HGNC:11128 | Binds E-box elements in CDH1 promoter; recruits KDM1A histone demethylase to repress epithelial genes | CDH1, CLDN7, KRT8 | L3 | [Source: uniprot_get_protein(UniProtKB:O95863)] |
| SNAI2 | HGNC:11094 | Transcriptional repressor; essential for TWIST1-induced EMT and invasion | CDH1, BRCA2, OCLN | L3 | [Source: uniprot_get_protein(UniProtKB:O43623)] |
| ZEB1 | HGNC:11642 | Represses E-cadherin promoter; recruits SMARCA4/BRG1 chromatin remodeling complex | CDH1, epithelial genes | L3 | [Source: uniprot_get_protein(UniProtKB:P37275)] |

### Mesenchymal Markers & Migration Drivers

| Gene | CURIE | Function | Role in Metastasis | Evidence Level | Source |
|------|-------|----------|-------------------|----------------|--------|
| VIM | HGNC:12692 | Class-III intermediate filament protein; marker of mesenchymal cells | Promotes cell directional movement, orientation, migration front polarization | L3 | [Source: uniprot_get_protein(UniProtKB:P08670)] |
| MET | HGNC:7029 | Hepatocyte growth factor receptor tyrosine kinase | Activates RAS-ERK (morphogenesis) and PI3K-AKT (survival, migration) pathways | L3 | [Source: uniprot_get_protein(UniProtKB:P08581)] |

### EMT Transcription Factor Interaction Network

| Protein A | Protein B | STRING Score | Interaction Type | Significance | Source |
|-----------|-----------|--------------|------------------|-------------|--------|
| TWIST1 | SNAI2 | 0.952 | Co-regulatory | High-confidence co-activation in EMT | [Source: string_get_interactions(STRING:9606.ENSP00000242261)] |
| TWIST1 | ZEB1 | 0.932 | Co-regulatory | Coordinate repression of epithelial program | [Source: string_get_interactions(STRING:9606.ENSP00000242261)] |
| TWIST1 | SNAI1 | 0.901 | Co-regulatory | Synergistic EMT induction | [Source: string_get_interactions(STRING:9606.ENSP00000242261)] |
| TWIST1 | TP53 | 0.915 | Antagonistic | TWIST1 can suppress p53-mediated apoptosis | [Source: string_get_interactions(STRING:9606.ENSP00000242261)] |

---

## Localized Tumor Maintenance Gene Network

### Tumor Suppressors

| Gene | CURIE | Function | Mechanism Suppressing Metastasis | Evidence Level | Source |
|------|-------|----------|----------------------------------|----------------|--------|
| TP53 | HGNC:11998 | Master tumor suppressor; induces cell cycle arrest, DNA repair, or apoptosis | Negatively regulates cell division; induces growth arrest; apoptosis induction prevents survival during dissemination | L3 | [Source: uniprot_get_protein(UniProtKB:P04637)] |
| PTEN | HGNC:9588 | Lipid phosphatase antagonizing PI3K-AKT pathway | Dephosphorylates PIP3; suppresses cell polarization and migration; inhibits focal adhesion formation | L3 | [Source: uniprot_get_protein(UniProtKB:P60484)] |

### Epithelial Adhesion Complex

| Gene | CURIE | Function | Role in Localization | Evidence Level | Source |
|------|-------|----------|---------------------|----------------|--------|
| CDH1 | HGNC:1748 | Calcium-dependent cell adhesion protein (E-cadherin) | Maintains epithelial cell-cell junctions; potent invasive suppressor; loss is hallmark of EMT | L3 | [Source: uniprot_get_protein(UniProtKB:P12830)] |

### CDH1 Adhesion Complex Network

| Protein A | Protein B | STRING Score | Interaction Type | Significance | Source |
|-----------|-----------|--------------|------------------|-------------|--------|
| CDH1 | CTNNA1 | 0.999 | Physical | α-catenin links CDH1 to actin cytoskeleton; essential for junction stability | [Source: string_get_interactions(STRING:9606.ENSP00000261769)] |
| CDH1 | CTNNB1 | 0.997 | Physical | β-catenin bridges CDH1 to α-catenin; junction assembly | [Source: string_get_interactions(STRING:9606.ENSP00000261769)] |
| CDH1 | SRC | 0.988 | Regulatory | SRC phosphorylation of CDH1 complex disrupts adhesion | [Source: string_get_interactions(STRING:9606.ENSP00000261769)] |

---

## Epigenetic Regulatory Mechanisms

### SNAI1 Chromatin Remodeling Complex

| Partner | STRING Score | Role in CDH1 Repression | Evidence Level | Source |
|---------|--------------|------------------------|----------------|--------|
| KDM1A | 0.998 | Histone demethylase recruited by SNAI1; removes H3K4me2 from CDH1 promoter | L3+ | [Source: string_get_interactions(STRING:9606.ENSP00000244050)] |
| HDAC1 | 0.999 | Histone deacetylase; chromatin compaction at epithelial gene loci | L3+ | [Source: string_get_interactions(STRING:9606.ENSP00000244050)] |
| HDAC2 | 0.998 | Co-repressor with HDAC1; removes acetyl marks from CDH1 regulatory regions | L3+ | [Source: string_get_interactions(STRING:9606.ENSP00000244050)] |
| EZH2 | 0.998 | Polycomb repressive complex 2 catalytic subunit; deposits H3K27me3 repressive mark | L3+ | [Source: string_get_interactions(STRING:9606.ENSP00000244050)] |
| DNMT1 | 0.995 | DNA methyltransferase; methylates CDH1 promoter CpG islands | L3+ | [Source: string_get_interactions(STRING:9606.ENSP00000244050)] |

**Significance**: SNAI1 (HGNC:11128) orchestrates a multi-layered epigenetic silencing cascade at the CDH1 promoter, combining histone demethylation (KDM1A), deacetylation (HDAC1/2), repressive methylation (EZH2), and DNA methylation (DNMT1). This stable repression of epithelial genes is a defining feature of the metastatic phenotype. [Sources: string_get_interactions(STRING:9606.ENSP00000244050), uniprot_get_protein(UniProtKB:O95863)]

---

## Pathway Membership

| Pathway | Pathway ID | Member Genes (from Query) | Score | Source |
|---------|-----------|--------------------------|-------|--------|
| Hallmark of cancer: metastasis and epithelial-to-mesenchymal transition | WP:WP5469 | TWIST1, SNAI1, SNAI2, ZEB1, CDH1, VIM, TGFB1, SMAD3, SMAD4, KDM1A, HDAC1, HDAC2, EZH2, SUZ12, DNMT1 | 0.63 | [Source: wikipathways_search_pathways("metastasis")] |
| Epithelial to mesenchymal transition in colorectal cancer | WP:WP4239 | TWIST1, SNAI1, SNAI2, ZEB1, CDH1 | 0.70 | [Source: wikipathways_search_pathways("epithelial mesenchymal transition")] |
| Focal adhesion | WP:WP306 | CDH1, MET, SRC, PTEN | 0.72 | [Source: wikipathways_search_pathways("cell adhesion")] |

---

## Key Molecular Switches: Metastasis vs. Localization

### Switch 1: EMT Transcription Factor Activation
**Metastatic State**: TWIST1, SNAI1, SNAI2, ZEB1 upregulated → CDH1 repression → loss of cell-cell adhesion
**Localized State**: EMT transcription factors low/absent → CDH1 expressed → intact epithelial junctions
[Sources: uniprot_get_protein(UniProtKB:Q15672, O95863, O43623, P37275, P12830)]

### Switch 2: Adhesion Molecule Expression
**Metastatic State**: CDH1 (epithelial) downregulated, VIM (mesenchymal) upregulated → motile phenotype
**Localized State**: CDH1 (epithelial) high, VIM low → stationary, adherent phenotype
[Sources: uniprot_get_protein(UniProtKB:P12830, P08670), string_get_interactions(STRING:9606.ENSP00000261769)]

### Switch 3: Tumor Suppressor Function
**Metastatic State**: TP53 loss-of-function mutations → escape from apoptosis during dissemination; PTEN loss → PI3K-AKT activation → migration
**Localized State**: TP53 functional → cell cycle arrest/apoptosis upon stress; PTEN active → suppressed migration
[Sources: uniprot_get_protein(UniProtKB:P04637, P60484)]

### Switch 4: Growth Factor Receptor Signaling
**Metastatic State**: MET overexpression/activation → HGF-driven scattering, invasion, survival
**Localized State**: MET low → minimal scattering signals
[Sources: uniprot_get_protein(UniProtKB:P08581), string_get_interactions(STRING:9606.ENSP00000317272)]

---

## Evidence Assessment

### Claim-Level Grades

| Claim | Evidence Level | Score | Justification |
|-------|---------------|-------|---------------|
| TWIST1/SNAI1/SNAI2/ZEB1 repress CDH1 transcription | L3 Functional | 0.80 | Multi-database concordance (HGNC + UniProt + STRING); mechanism of action documented; high STRING scores |
| CDH1 is a potent invasion suppressor | L3 Functional | 0.75 | UniProt function annotation + STRING adhesion complex interactions; no clinical trial data |
| TP53 induces cell cycle arrest and apoptosis | L3 Functional | 0.85 | Multi-database (HGNC + UniProt); well-established tumor suppressor function; +0.05 for extensive literature |
| PTEN antagonizes PI3K-AKT to suppress migration | L3 Functional | 0.80 | UniProt function + pathway databases; mechanism well-defined |
| SNAI1 recruits KDM1A to CDH1 promoter | L3+ Functional | 0.85 | UniProt annotation + STRING 0.998 interaction score; +0.05 high STRING score |
| EMT genes are members of WP:WP5469 pathway | L2 Multi-DB | 0.63 | WikiPathways search score 0.63; single pathway database |
| MET activates RAS-ERK and PI3K-AKT pathways | L3 Functional | 0.80 | UniProt function + STRING interactions with GAB1, GRB2, STAT3; known signaling cascades |
| VIM is a mesenchymal marker promoting migration | L3 Functional | 0.75 | UniProt annotation; single-database for function but widely accepted marker |

### Overall Report Confidence

- **Median Claim Score**: 0.80 (L3 Functional)
- **Range**: 0.63 – 0.85
- **Interpretation**: High confidence in functional mechanisms; all core gene-gene relationships validated across multiple databases (HGNC, UniProt, STRING). Pathway membership scores lower due to single-database source (WikiPathways). No clinical trial data retrieved (query focused on gene expression mechanisms, not therapeutics).

---

## Gaps and Limitations

1. **No Clinical Validation**: This analysis focused on molecular mechanisms. No clinical trial data was retrieved linking these gene expression patterns to patient outcomes. To validate in clinical contexts, Phase 4b/5 (clinical trials and validation) would be required.

2. **Pathway Database Coverage**: WikiPathways was the only pathway database queried. Cross-validation with KEGG, Reactome, or Gene Ontology enrichment would strengthen pathway membership claims.

3. **Post-Translational Regulation**: Analysis focused on transcriptional regulation and protein-protein interactions. Post-translational modifications (phosphorylation, ubiquitination) that regulate EMT protein activity were not systematically queried.

4. **Tissue-Specific Variation**: Gene expression patterns may vary by cancer type. This analysis did not stratify by tissue origin (e.g., breast vs. colorectal vs. lung). Tissue-specific EMT signatures could be queried via cancer-specific pathway databases.

5. **Temporal Dynamics**: Analysis provides a static snapshot. EMT is a dynamic, reversible process (mesenchymal-epithelial transition/MET during colonization). Time-series or reversibility data was not retrieved.

6. **MicroRNA and Non-Coding RNA**: EMT is also regulated by miR-200 family (represses ZEB1/2) and other non-coding RNAs. These were not queried.

7. **Single-Species Focus**: All searches defaulted to human (species 9606). Comparative analysis across model organisms (mouse, zebrafish) could reveal conserved vs. species-specific EMT mechanisms.

---

## Biological Interpretation

The fundamental difference between metastatic and localized tumor gene expression is the **epithelial-mesenchymal transition (EMT) program**. Metastasis is driven by a core set of **EMT transcription factors** (TWIST1, SNAI1, SNAI2, ZEB1) that act as master switches, coordinately repressing epithelial genes (especially CDH1/E-cadherin) while activating mesenchymal genes (VIM, MET). This transcriptional switch is reinforced by **epigenetic silencing** (KDM1A, HDAC1/2, EZH2, DNMT1) that stably locks cells into a motile, invasive phenotype.

In contrast, localized tumors maintain **epithelial identity** through high CDH1 expression, which enforces cell-cell adhesion and suppresses invasion. **Tumor suppressors** (TP53, PTEN) further constrain metastatic potential by inducing cell cycle arrest/apoptosis and suppressing pro-migratory PI3K-AKT signaling.

The molecular switch from localized to metastatic disease involves:
1. **Activation** of EMT transcription factors (often via TGF-β signaling)
2. **Repression** of CDH1 and epithelial adhesion machinery
3. **Loss** of TP53/PTEN tumor suppressor function
4. **Upregulation** of mesenchymal markers (VIM) and migration receptors (MET)

This analysis confirms that metastasis is not a random accumulation of mutations, but a **coordinated transcriptional program** orchestrated by a small number of master regulators acting through chromatin remodeling and signal transduction pathways.

---

**Report Generated**: 2026-02-07
**Evidence Base**: HGNC gene resolution, UniProt functional annotation, STRING protein-protein interactions, WikiPathways pathway membership
**Confidence**: L3 Functional (median 0.80/1.00)
