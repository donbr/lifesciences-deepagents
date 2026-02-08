# Life Sciences Skills — Evaluation Test Protocol

## Purpose

This document defines 3 standardized test cases with gold-standard expected outputs for evaluating the life sciences Claude Code skills. Each test case specifies the expected LOCATE (fuzzy search) and RETRIEVE (get-by-ID) tool calls, expected CURIEs, and gold-standard drugs/trials.

## Test Methodology

For each test case, the evaluator should:
1. Invoke the `lifesciences-graph-builder` skill with the input query
2. Record every tool call made (MCP or curl)
3. Check whether LOCATE preceded RETRIEVE for each entity
4. Verify output contains canonical CURIEs (not just names)
5. Compare drugs/trials found against gold standard
6. Note any facts from parametric knowledge (not grounded in tool results)

---

## Test Case 1: TP53 Pathway (Well-Studied Target)

### Input Query
> "What drugs target TP53 and its interactors in cancer?"

### Expected LOCATE Calls (Fuzzy Search)

| Step | Tool | Call | Expected Result |
|------|------|------|-----------------|
| 1.1 | `query_lifesciences` | `tool_name="hgnc_search_genes"`, `query="TP53"` | HGNC:11998 |
| 1.2 | `query_lifesciences` | `tool_name="string_search_proteins"`, `query="TP53"` | 9606.ENSP00000269305 |
| 1.3 | `query_lifesciences` | `tool_name="chembl_search_compounds"`, `query="Venetoclax"` | CHEMBL3137309 |

### Expected RETRIEVE Calls (Get-by-ID)

| Step | Tool | Call | Expected Output |
|------|------|------|-----------------|
| 2.1 | `query_lifesciences` | `tool_name="hgnc_get_gene"`, `tool_args={"hgnc_id": "HGNC:11998"}` | Symbol: TP53, UniProt: P04637, Ensembl: ENSG00000141510 |
| 2.2 | `query_lifesciences` | `tool_name="uniprot_get_protein"`, `tool_args={"uniprot_id": "P04637"}` | Function text mentioning BAX, BCL2, FAS |
| 2.3 | `query_lifesciences` | `tool_name="string_get_interactions"`, `tool_args={"string_id": "9606.ENSP00000269305"}` | MDM2 (0.999), SIRT1, ATM, BCL2 |
| 2.4 | Open Targets GraphQL | `target(ensemblId: "ENSG00000171791") { knownDrugs }` | Venetoclax, Navitoclax |

### Expected CURIEs in Output

| Entity | CURIE | Type |
|--------|-------|------|
| TP53 | HGNC:11998 | Gene |
| BCL2 | HGNC:990 | Gene |
| p53 protein | UniProtKB:P04637 | Protein |
| Venetoclax | CHEMBL:3137309 | Compound |

### Gold-Standard Drugs

| Drug | Phase | Mechanism | Target |
|------|-------|-----------|--------|
| Venetoclax | 4 (approved) | BCL2 inhibitor | BCL2 |
| Navitoclax | 3 | BCL2/BCL-XL inhibitor | BCL2, BCL2L1 |
| APR-246 (Eprenetapopt) | 3 | p53 reactivator | TP53 |
| Idasanutlin | 3 | MDM2 antagonist | MDM2 |

### Gold-Standard Trials

| NCT ID | Drug | Phase | Status |
|--------|------|-------|--------|
| NCT00461032 | Venetoclax (ABT-263 predecessor study) | Phase 1 | Completed |
| NCT02993523 | Venetoclax + rituximab | Phase 3 | Completed |

---

## Test Case 2: ACVR1/FOP (From Retrospective)

### Input Query
> "What drugs target the ACVR1 pathway in FOP?"

### Expected LOCATE Calls

| Step | Tool | Call | Expected Result |
|------|------|------|-----------------|
| 1.1 | `query_lifesciences` | `tool_name="hgnc_search_genes"`, `query="ACVR1"` | HGNC:171 |
| 1.2 | `query_lifesciences` | `tool_name="clinicaltrials_search_trials"`, `query="fibrodysplasia ossificans progressiva"` | Multiple FOP trials |

### Expected RETRIEVE Calls

| Step | Tool | Call | Expected Output |
|------|------|------|-----------------|
| 2.1 | `query_lifesciences` | `tool_name="hgnc_get_gene"`, `tool_args={"hgnc_id": "HGNC:171"}` | UniProt: Q04771, Ensembl: ENSG00000115170 |
| 2.2 | `query_lifesciences` | `tool_name="uniprot_get_protein"`, `tool_args={"uniprot_id": "Q04771"}` | BMP type I receptor serine/threonine kinase |
| 2.3 | Open Targets GraphQL | `target(ensemblId: "ENSG00000115170") { knownDrugs }` | Palovarotene, Garetosmab (must be inhibitors/antagonists) |
| 2.4 | `query_lifesciences` | `tool_name="clinicaltrials_get_trial"`, `tool_args={"nct_id": "NCT03312634"}` | Palovarotene Phase 3 trial |

### Expected CURIEs in Output

| Entity | CURIE | Type |
|--------|-------|------|
| ACVR1 | HGNC:171 | Gene |
| Activin receptor type-1 | UniProtKB:Q04771 | Protein |
| FOP | MONDO:0018875 | Disease |

### Gold-Standard Drugs

| Drug | Phase | Mechanism | Critical Note |
|------|-------|-----------|---------------|
| Palovarotene | 4 (approved) | RARgamma agonist (downstream inhibition of BMP) | FDA-approved for FOP |
| Garetosmab | 2/3 | Anti-Activin A antibody | Upstream pathway blockade |
| LDN-193189 | Preclinical | ACVR1 kinase inhibitor | Direct target inhibitor |

### Critical Anti-Pattern
MUST NOT return: Eptotermin Alfa, Dibotermin Alfa (these are BMP AGONISTS that would worsen FOP). The TRAVERSE_DRUGS phase must filter for inhibitors/antagonists for gain-of-function diseases.

### Gold-Standard Trials

| NCT ID | Drug | Phase | Status |
|--------|------|-------|--------|
| NCT03312634 | Palovarotene | Phase 3 | Completed |
| NCT02190747 | Palovarotene | Phase 2 | Completed |
| NCT05394116 | Garetosmab | Phase 2/3 | Recruiting |

---

## Test Case 3: BRCA1 Breast Cancer (Common Query)

### Input Query
> "What PARP inhibitors are used for BRCA1-mutant breast cancer?"

### Expected LOCATE Calls

| Step | Tool | Call | Expected Result |
|------|------|------|-----------------|
| 1.1 | `query_lifesciences` | `tool_name="hgnc_search_genes"`, `query="BRCA1"` | HGNC:1100 |
| 1.2 | `query_lifesciences` | `tool_name="chembl_search_compounds"`, `query="Olaparib"` | CHEMBL1336 |

### Expected RETRIEVE Calls

| Step | Tool | Call | Expected Output |
|------|------|------|-----------------|
| 2.1 | `query_lifesciences` | `tool_name="hgnc_get_gene"`, `tool_args={"hgnc_id": "HGNC:1100"}` | UniProt: P38398, Ensembl: ENSG00000012048 |
| 2.2 | `query_lifesciences` | `tool_name="uniprot_get_protein"`, `tool_args={"uniprot_id": "P38398"}` | DNA repair, tumor suppressor |
| 2.3 | Open Targets GraphQL | `target(ensemblId: "ENSG00000012048") { knownDrugs }` | PARP inhibitors |
| 2.4 | ClinicalTrials.gov | `query.intr=olaparib&query.cond=breast+cancer` | Multiple trials |

### Expected CURIEs in Output

| Entity | CURIE | Type |
|--------|-------|------|
| BRCA1 | HGNC:1100 | Gene |
| BRCA1 protein | UniProtKB:P38398 | Protein |
| Breast cancer | EFO:0000305 | Disease |
| Olaparib | CHEMBL:1336 | Compound |

### Gold-Standard Drugs

| Drug | Phase | Mechanism | Approval |
|------|-------|-----------|----------|
| Olaparib | 4 (approved) | PARP1/2 inhibitor | FDA-approved for BRCA-mutant breast cancer |
| Talazoparib | 4 (approved) | PARP1/2 inhibitor | FDA-approved for BRCA-mutant breast cancer |
| Niraparib | 4 (approved) | PARP1/2 inhibitor | FDA-approved for ovarian, expanding to breast |
| Rucaparib | 4 (approved) | PARP1/2/3 inhibitor | FDA-approved for BRCA-mutant ovarian |

### Gold-Standard Trials

| NCT ID | Drug | Phase | Status |
|--------|------|-------|--------|
| NCT02000622 | Olaparib (OlympiAD) | Phase 3 | Completed |
| NCT01945775 | Talazoparib (EMBRACA) | Phase 3 | Completed |

---

## Scoring Rubric

### Per-Skill Scoring (0–4 points per criterion)

| Criterion | 0 | 1 | 2 | 3 | 4 |
|-----------|---|---|---|---|---|
| **Tool Usage** | No tools used | Some tools, no pattern | LOCATE used but no RETRIEVE | LOCATE→RETRIEVE for most entities | LOCATE→RETRIEVE for ALL entities |
| **Grounding** | All from parametric knowledge | Mostly parametric with some tools | Mixed — some grounded, some not | Mostly grounded with minor gaps | Fully grounded — every claim from tool results |
| **CURIEs** | No CURIEs in output | Some entity names only | Some CURIEs, inconsistent format | CURIEs for most entities, consistent format | All entities have CURIEs, format matches convention |
| **Drug Accuracy** | No drugs found or all wrong | 1 correct drug | 2 correct drugs | 3+ correct drugs, no harmful errors | All gold-standard drugs found, no inappropriate results |
| **Trial Accuracy** | No trials or hallucinated NCTs | 1 verified trial | 2+ verified trials | All trials verified, correct phases | Gold-standard trials found and verified |

### Overall Score

- **0–4**: Skill needs fundamental redesign
- **5–9**: Significant gaps — LOCATE→RETRIEVE discipline missing
- **10–14**: Functional but inconsistent — needs enforcement
- **15–17**: Good — minor gaps in coverage
- **18–20**: Excellent — fully grounded, accurate results

---

## Evaluation Cadence

- Run all 3 test cases after any SKILL.md modification
- Record results in `docs/evaluations/behavioral-audit.md`
- Compare against previous scores to detect regressions
