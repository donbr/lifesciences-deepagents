# Report Quality Review: Metastasis vs. Local Tumor Gene Expression

## Verdict: **PARTIAL**

The report demonstrates strong template selection (Template 2: Gene/Protein Network), good source attribution discipline, and solid evidence grading. However, it fails on disease CURIE resolution, lacks clinical trial validation (by design for this question type), and shows moderate hallucination risk in mechanistic detail claims that go beyond what tool outputs would typically provide.

---

## Dimension Scores

### 1. CURIE Resolution -- **PASS (with minor gaps)**

**Score: 8/10**

All 11 primary genes are resolved to HGNC CURIEs with proper `[Source: hgnc_search_genes("...")]` citations:

| Gene | CURIE | Correctly Formatted |
|------|-------|---------------------|
| SNAI1 | HGNC:11128 | Yes |
| TWIST1 | HGNC:12428 | Yes |
| ZEB1 | HGNC:11642 | Yes |
| MMP9 | HGNC:7176 | Yes |
| CDH1 | HGNC:1748 | Yes |
| VEGFA | HGNC:12680 | Yes |
| MYC | HGNC:7553 | Yes |
| TP53 | HGNC:11998 | Yes |
| CCND1 | HGNC:1582 | Yes |
| CDK4 | HGNC:1773 | Yes |
| RB1 | HGNC:9884 | Yes |

UniProt CURIEs are used in the body text with `UniProtKB:` prefix (e.g., `UniProtKB:O95863`, `UniProtKB:P12830`), which follows the Graph Node ID convention in the skill.

**Gaps identified:**
- Secondary interactors discovered via STRING (HDAC1, KDM1A, EZH2, RCOR1, TIMP1, THBS1, CTNNB1, CTNNA1, VCL, KAT2A, TRRAP, MDM2, SIRT1, ATM, etc.) are referenced by gene symbol only -- no HGNC CURIEs resolved for them. The skill's LOCATE-RETRIEVE discipline would require resolving these newly-discovered entities if they are included in the graph. Since they appear in the "Hub Genes" and interaction tables (and in the "Graph statistics: 11 nodes, 10 edges" note at line 247), this is a minor gap -- the report claims 11 nodes but names far more than 11 entities.
- No CHEMBL CURIEs, which is expected since no drug discovery phase was executed.

---

### 2. Source Attribution -- **PASS**

**Score: 9/10**

The report demonstrates excellent source attribution discipline. I performed a systematic count:

| Section | Claims with Source | Claims without Source | Notes |
|---------|-------------------|---------------------|-------|
| Summary | 1 | 0 | Multi-source citation present |
| Resolved Entities table | 11 | 0 | All rows cite `hgnc_search_genes` |
| Metastasis Network tables | 11 | 0 | All cite `string_get_interactions` with STRING protein IDs |
| Local Tumor Network tables | 7 | 1 | Row at line 70 cites "UniProt function annotation P24385" (non-standard format) |
| Hub Genes tables | 5 | 0 | All cite STRING |
| Functional Programs | 9 | 1 | Line 124 ("No Migration Program") has no source -- this is an absence claim, arguable |
| Interpretation section | 4 | 0 | All cited |

**Totals: ~48 sourced claims, ~2 unsourced claims**

The unsourced claims:
1. Line 70: `[Source: UniProt function annotation P24385]` -- uses a non-standard format. Should be `[Source: uniprot_get_protein(UniProtKB:P24385)]`.
2. Line 124: "No Migration Program" -- an absence assertion with no tool citation. Could cite something like `[No data: string_get_interactions returned no EMT factors for MYC/CCND1/CDK4/RB1]`.

Overall, source attribution is strong and follows the `[Source: tool(param)]` convention consistently.

---

### 3. LOCATE then RETRIEVE Discipline -- **PASS**

**Score: 8/10**

Evidence of LOCATE-RETRIEVE pattern:
- **LOCATE**: All 11 genes went through `hgnc_search_genes("GENE_NAME")` -- the search/LOCATE step.
- **RETRIEVE**: UniProt protein details retrieved via `uniprot_get_protein(UniProtKB:...)` for multiple entities (O95863/SNAI1, P37275/ZEB1, P12830/CDH1, P14780/MMP9, P15692/VEGFA, P01106/MYC, P24385/CCND1, P11802/CDK4, P04637/TP53, P06400/RB1).
- **RETRIEVE**: STRING interactions retrieved via `string_get_interactions(9606.ENSP...)` for multiple proteins.

**Gap**: There is no explicit `hgnc_get_gene` RETRIEVE step shown after the LOCATE step. The report jumps from `hgnc_search_genes` directly to `uniprot_get_protein`. The skill requires LOCATE (search) then RETRIEVE (get by ID). While the UniProt retrieval implies the HGNC LOCATE returned cross-references, the intermediate `hgnc_get_gene` step is not cited. This is a minor protocol gap -- the data pipeline likely did execute it, but the report does not document it.

Additionally, the secondary entities (HDAC1, KDM1A, CTNNB1, etc.) discovered via STRING were never LOCATEd through HGNC. They appear in the report based solely on STRING output names.

---

### 4. Disease CURIE in ENRICH Phase -- **FAIL**

**Score: 2/10**

This is a significant gap. The competency question concerns "metastasis" and "localized tumor" -- both are disease concepts that should be resolved to CURIEs:

- **Metastasis**: No disease CURIE resolved. Should have `EFO:0009708` (metastasis) or similar from Open Targets/MONDO.
- **Cancer (general)**: No disease CURIE. Could be `MONDO:0004992` (cancer) or `EFO:0000311` (cancer).
- **Localized tumor**: No disease CURIE.

The ENRICH phase skill (line 217-238 of the graph-builder skill) explicitly requires: "LOCATE disease CURIE (use Ensembl ID from HGNC cross-references above) ... Call `opentargets_get_associations`... Record disease CURIE for Phase 4a/4b."

No `opentargets_get_associations` or `opentargets_search_targets` calls are cited anywhere in the report. The Gaps section (lines 188-191) acknowledges this: "Open Targets `associatedDiseases` not queried for all genes. Cannot quantify which genes are more strongly associated with metastatic vs. localized cancer subtypes." This is honest self-reporting, but it remains a protocol failure.

---

### 5. Open Targets Pagination -- **N/A**

**Score: N/A**

Open Targets `knownDrugs` was not used in this report. The report scope explicitly excludes drug discovery (line 194-195: "No Phase 4a/4b drug or trial discovery performed"). This is appropriate for the competency question, which asks about gene expression differences, not therapeutics.

No pagination issues to evaluate.

---

### 6. Evidence Grading -- **PASS**

**Score: 8/10**

The report includes a comprehensive evidence assessment section (lines 148-177) with:

- **Three tiers**: High-Confidence (L3: 0.70-0.85), Moderate-Confidence (L2: 0.60-0.65), Lower-Confidence (L1: 0.45)
- **10 individually graded claims** with justifications
- **Overall confidence**: Median 0.75 (L3 Functional), Range 0.45-0.85
- **Median-based calculation**: Correctly uses median (not mean) per the reporting skill specification

**Strengths**:
- Claim-level granularity is correct
- Justifications reference actual data (STRING scores, UniProt annotations)
- The L1 assignment for TWIST1-SNAI1 (STRING 0.901 "but limited functional detail") shows proper rigor

**Gaps**:
- Modifier application is not explicitly shown. The reporting skill specifies modifiers (+0.05 for high STRING score, +0.05 for literature support, etc.) but the report does not show the arithmetic. For example, SNAI1-CDH1 at L3/0.85 should show: Base L3 (0.70) + High STRING (+0.05) + UniProt annotation (+0.05) + multi-DB (+0.05) = 0.85.
- No claims are scored below 0.30 ("Insufficient Evidence"), which is good, but also no claims are flagged as unverifiable.

---

### 7. Gain-of-Function Filter -- **N/A**

**Score: N/A**

The competency question does not involve a gain-of-function disease. It asks about metastasis vs. localized tumor gene expression, which is a comparison of biological programs, not a drug-targeting scenario. No agonist/antagonist filtering was required or expected.

---

### 8. Clinical Trial Validation -- **N/A (by design)**

**Score: N/A**

The report explicitly scopes out clinical trials (line 194-195: "No Phase 4a/4b drug or trial discovery performed. Report focuses on biological networks, not therapeutic interventions."). This is the correct decision for a Template 2 (Gene/Protein Network) question. The Gaps section properly notes this and directs users to Template 1 for drug-focused follow-up.

No NCT IDs are present, so none need validation.

---

### 9. Completeness -- **PASS (with caveats)**

**Score: 7/10**

The report does answer the competency question. It contrasts:

- **Metastasis-driving genes**: SNAI1, TWIST1, ZEB1, MMP9, VEGFA -- operating on migration/invasion/EMT machinery
- **Localized tumor genes**: MYC, TP53, CCND1, CDK4, RB1 -- operating on proliferation/cell cycle machinery
- **The switch mechanism**: CDH1 repression as the molecular gatekeeper

The "Functional Programs: Key Distinctions" section (lines 102-126) directly addresses the CQ with a clear contrast between the two programs. The "Interpretation" section (lines 208-227) provides a thoughtful synthesis.

**Caveats**:
1. **Gene selection bias**: The report pre-selected "canonical" metastasis and local tumor genes rather than discovering them through unbiased queries. A truly data-driven approach would query Open Targets or STRING for genes associated with metastatic cancer vs. localized cancer and let the data determine the gene lists. The current approach risks confirming textbook knowledge rather than discovering novel insights.

2. **Missing Pathway Membership**: The report acknowledges (line 183-186) that WikiPathways was not queried. Template 2 includes a "Pathway Membership" section that is absent from this report.

3. **Missing Disease Associations**: No Open Targets disease association data to quantify which genes are specifically associated with metastatic vs. localized subtypes (acknowledged in Gaps).

4. **Network Properties section**: Present (lines 129-143) and well-formatted, matching Template 2 requirements. However, the claim "11 nodes, 10 edges" at line 247 conflicts with the Network Properties section which reports 6 nodes + 18 edges (metastasis) and 5 nodes + 12 edges (local tumor) -- that is 11 nodes total and 30 edges total, not 10.

---

### 10. Hallucination Risk -- **MEDIUM**

**Score: Medium risk**

Several claims in the report contain mechanistic detail that likely exceeds what the cited tool calls would have returned:

**Likely hallucinated or training-knowledge-augmented details:**

1. **Line 33**: "SNAI1 binds E-boxes in CDH1 promoter, recruits KDM1A histone demethylase" -- STRING `string_get_interactions` returns interaction scores and partner names, but does NOT return detailed molecular mechanisms like "binds E-boxes" or "recruits KDM1A histone demethylase." This mechanistic narrative likely comes from training knowledge, though it is attributed to STRING.

2. **Line 35**: "Chromatin remodeling complex for gene silencing" -- STRING does not provide functional annotations in this format. This is interpretive text from training knowledge.

3. **Line 106**: "SNAI1, TWIST1, and ZEB1 directly repress E-cadherin (CDH1) by binding E-box elements in its promoter" -- UniProt function text may mention E-box binding for SNAI1, but the claim that all three "directly repress CDH1 by binding E-box elements" is a synthesis that extends beyond what two UniProt records would state.

4. **Line 118**: "MYC activates growth-related genes via CAC[GA]TG motifs, regulates PKM splicing for Warburg effect" -- The PKM splicing and Warburg effect detail is specific molecular biology knowledge. UniProt function text for MYC may mention DNA binding motifs but is unlikely to discuss PKM splicing regulation in the exact terms used.

5. **Line 124**: "No Migration Program: Local tumor genes focus on proliferation WITHOUT activating EMT factors or matrix degradation enzymes" -- This is an absence claim based on the fact that STRING interactions for MYC/CCND1/CDK4/RB1 did not return EMT factors. However, absence of evidence in a specific STRING query is not evidence of absence. This claim is presented more strongly than the data supports.

**Mitigating factors:**
- All primary entities have tool-call sources
- The report does not fabricate drug names, NCT IDs, or CURIE identifiers
- Interaction scores are plausible STRING output values
- The "Key Mechanism" column in interaction tables appears to blend tool output with training knowledge -- this is the primary risk area

**Assessment**: The mechanistic narrative is largely consistent with established biology, reducing the risk of outright falsehoods. However, the Fuzzy-to-Fact protocol's Critical Grounding Rule states: "ALL factual claims MUST come from MCP tool results or curl command output." The detailed molecular mechanism descriptions in the "Key Mechanism" columns almost certainly exceed what STRING and UniProt tool calls return verbatim. This is a **protocol violation** even if the biology is correct.

---

## Summary Table

| Dimension | Score | Status |
|-----------|-------|--------|
| 1. CURIE Resolution | 8/10 | **PASS** (secondary entities unresolved) |
| 2. Source Attribution | 9/10 | **PASS** (48 sourced, 2 unsourced) |
| 3. LOCATE-RETRIEVE Discipline | 8/10 | **PASS** (hgnc_get_gene step not documented) |
| 4. Disease CURIE in ENRICH | 2/10 | **FAIL** (no MONDO/EFO resolved for metastasis or cancer) |
| 5. Open Targets Pagination | N/A | **N/A** (not used) |
| 6. Evidence Grading | 8/10 | **PASS** (modifier arithmetic not shown) |
| 7. Gain-of-Function Filter | N/A | **N/A** (not applicable to this CQ) |
| 8. Clinical Trial Validation | N/A | **N/A** (correctly scoped out) |
| 9. Completeness | 7/10 | **PASS** (gene selection bias, missing pathways, node/edge count inconsistency) |
| 10. Hallucination Risk | Medium | **CAUTION** (mechanism details exceed tool output) |

## Actionable Recommendations

1. **Resolve disease CURIEs**: Add a Phase 2 ENRICH step that calls `opentargets_get_associations` for key genes to obtain disease CURIEs for metastasis (e.g., `EFO:0009708`) and cancer generally. This would also enable the missing disease stratification analysis.

2. **Resolve secondary entity CURIEs**: The 15+ interactors discovered via STRING (HDAC1, KDM1A, CTNNB1, etc.) should be LOCATEd through `hgnc_search_genes` to obtain HGNC CURIEs, or explicitly marked as "STRING-discovered, CURIE unresolved."

3. **Constrain "Key Mechanism" columns**: Replace free-text mechanism descriptions with verbatim tool output excerpts or mark interpretive text with a qualifier like "[Interpreted from UniProt function text]". The current format makes it impossible to distinguish tool output from training knowledge.

4. **Show modifier arithmetic**: In the Evidence Assessment section, explicitly show the base level + modifiers = final score calculation for at least the first 2-3 claims, per the reporting skill's worked example format.

5. **Fix node/edge count**: The footer claims "11 nodes, 10 edges" but the Network Properties section reports 11 nodes and 30 combined edges. Reconcile these numbers.

6. **Add WikiPathways data**: Execute `wikipathways_get_pathways_for_gene` for the 11 core genes to fill the missing Pathway Membership section required by Template 2.
