# End-to-End Validation Runbook

## Instructions for the Evaluation Team

You are validating the life sciences graph-builder skill after a major rewrite. The skills now use MCP tools as the primary method (not curl), enforce LOCATE→RETRIEVE discipline, and include grounding rules to prevent hallucinations. Your job is to run the test cases, score the results, and write a retrospective.

**Pre-requisites**: The `lifesciences-research` MCP server must be available. Verify by running:
```
Use ToolSearch to find "hgnc_search_genes". If it appears, the MCP is connected.
If not, run: claude mcp add --scope local --transport http lifesciences-research https://lifesciences-research.fastmcp.app/mcp
Then restart the session.
```

---

## Task 1: Run the 3 Test Protocol Cases

Run each test case using the `/lifesciences-graph-builder` skill. For each one, record the results in a markdown file.

### Test Case 1: TP53 Pathway

Run this command:
```
/lifesciences-graph-builder "What drugs target TP53 and its interactors in cancer?"
```

**Gold-standard entities to check for:**
- Gene: TP53 → HGNC:11998
- Protein: p53 → UniProtKB:P04637
- Ensembl: ENSG00000141510
- Interactors found via STRING: MDM2, BCL2, ATM, SIRT1

**Gold-standard drugs:**
| Drug | Phase | Mechanism | Target |
|------|-------|-----------|--------|
| Venetoclax | 4 (approved) | BCL2 inhibitor | BCL2 |
| Navitoclax | 3 | BCL2/BCL-XL inhibitor | BCL2, BCL2L1 |
| APR-246 (Eprenetapopt) | 3 | p53 reactivator | TP53 |
| Idasanutlin | 3 | MDM2 antagonist | MDM2 |

**Gold-standard trials:**
- NCT00461032 (Venetoclax CLL)
- NCT02993523 (APR-246 MDS)

Save results to: `docs/evaluations/results/tc1-tp53-pathway.md`

---

### Test Case 2: ACVR1/FOP (Gain-of-Function)

Run this command:
```
/lifesciences-graph-builder "What drugs target the ACVR1 pathway in fibrodysplasia ossificans progressiva (FOP)?"
```

**Gold-standard entities:**
- Gene: ACVR1 (ALK2) → HGNC:171
- Protein: Activin receptor type-1 → UniProtKB:Q04771
- Ensembl: ENSG00000115170
- Disease: FOP → MONDO:0018875

**Critical anti-pattern — these MUST be EXCLUDED:**
- Eptotermin Alfa (BMP agonist — worsens FOP)
- Dibotermin Alfa (BMP agonist — worsens FOP)

**Gold-standard drugs (inhibitors/antagonists only):**
| Drug | Phase | Mechanism |
|------|-------|-----------|
| Palovarotene | 3 (completed) | RARγ agonist — blocks downstream chondrogenesis |
| Garetosmab | 3 (active) | Anti-activin A antibody — blocks ACVR1 ligand |
| Fidrisertib (IPN60130) | 2 | Direct ALK2 kinase inhibitor |
| Saracatinib (AZD0530) | 2 | Src kinase inhibitor — blocks BMP-induced HO |
| Zilurgisertib (INCB000928) | 2 | Direct ALK2 kinase inhibitor |

**Gold-standard trials:**
- NCT03312634 (Palovarotene Phase 3)
- NCT05394116 (Garetosmab Phase 3)
- NCT05039515 (Fidrisertib Phase 2)
- NCT04307953 (Saracatinib Phase 2)
- NCT05090891 (Zilurgisertib Phase 2)

Save results to: `docs/evaluations/results/tc2-acvr1-fop.md`

---

### Test Case 3: BRCA1 Breast Cancer

Run this command:
```
/lifesciences-graph-builder "What PARP inhibitors are used for BRCA1-mutant breast cancer?"
```

**Gold-standard entities:**
- Gene: BRCA1 → HGNC:1100
- Protein: BRCA1 → UniProtKB:P38398
- Ensembl: ENSG00000012048

**Gold-standard drugs:**
| Drug | Phase | Mechanism |
|------|-------|-----------|
| Olaparib | 4 (FDA approved) | PARP1/2 inhibitor |
| Talazoparib | 4 (FDA approved) | PARP1/2 inhibitor (PARP trapper) |
| Niraparib | 4 (FDA approved) | PARP1/2 inhibitor |
| Rucaparib | 4 (FDA approved) | PARP1/2/3 inhibitor |

**Gold-standard trials:**
- NCT02000622 (OlympiAD — Olaparib)
- NCT01945775 (EMBRACA — Talazoparib)

Save results to: `docs/evaluations/results/tc3-brca1-parp.md`

---

## Task 2: Score Each Test Case

For each test case, score using this rubric (5 criteria × 0-4 points = 20 max):

| Criterion | 0 | 1 | 2 | 3 | 4 |
|-----------|---|---|---|---|---|
| **Tool Usage** | No tools called | Some tools, no pattern | LOCATE→RETRIEVE for some | LOCATE→RETRIEVE for most | All entities follow LOCATE→RETRIEVE |
| **Grounding** | All from parametric knowledge | Mostly parametric, some tools | Mixed | Mostly grounded in tool results | Fully grounded — every fact traces to a tool call |
| **CURIEs** | No identifiers | Names only | Some CURIEs | Most entities have CURIEs | All entities have correct CURIEs |
| **Drug Accuracy** | All wrong or hallucinated | 1 correct drug found | 2 correct drugs | 3+ correct drugs | All gold-standard drugs found |
| **Trial Accuracy** | Hallucinated NCT IDs | 1 verified NCT ID | 2+ verified NCT IDs | All NCT IDs verified | All gold-standard trials found + verified |

Record the scores in each results file. Target: **15+/20** for each test case.

---

## Task 3: Run 3 Competency Questions

Select and run these 3 competency questions from `reference/competency_questions/competency-questions-catalog.md`:

### CQ1: FOP Mechanism (DrugMechDB Style)

```
/lifesciences-graph-builder "By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?"
```

**Expected gold-standard path:**
`Drug(Palovarotene/CHEMBL:2105648)` → agonist → `Protein(RARG/HGNC:9866)` → regulates → `Protein(ACVR1/HGNC:171)` → causes → `Disease(FOP/MONDO:0007606)`

**Persist to Graphiti** (if available):
```
Use the graphiti-docker add_memory tool with:
  group_id: "cq1-fop-mechanism"
  name: "Palovarotene mechanism for FOP"
  source: "json"
  episode_body: [the validated graph JSON from the skill output]
```

Save trace to: `docs/competency-validations/cq1-fop-mechanism.md`

---

### CQ11: p53-MDM2-Nutlin Axis (Canonical Pathway)

```
/lifesciences-graph-builder "How does Nutlin-3a inhibit the p53-MDM2 interaction, and what clinical trials test MDM2 inhibitors?"
```

**Expected entities:** TP53 (HGNC:11998), MDM2 (HGNC:6973), Nutlin-3a/Idasanutlin (CHEMBL376859)
**Expected path:** `Drug(Nutlin-3a)` → inhibitor → `Protein(MDM2)` → regulates → `Protein(TP53)` → associated_with → `Disease(AML)`

Save trace to: `docs/competency-validations/cq11-p53-mdm2-nutlin.md`

---

### CQ7: NGLY1 Drug Repurposing (Rare Disease, Multi-API)

```
/lifesciences-graph-builder "What approved drugs could be repurposed for NGLY1 deficiency by targeting pathway neighbors?"
```

**Why this is hard:** NGLY1 is a rare disease with no approved drugs. The skill must:
1. Resolve NGLY1 (HGNC:17646) via HGNC
2. Find interactors via STRING (ENGase, ERAD pathway members)
3. Search for drugs targeting those interactors
4. Build a 4-hop path: Drug → Neighbor Target → Interaction → NGLY1 → Disease

Save trace to: `docs/competency-validations/cq7-ngly1-repurposing.md`

---

## Task 4: Write the Retrospective

Create `docs/retrospectives/skills-rewrite-validation-retrospective.md` with these sections:

### Section 1: Executive Summary
- Date of validation
- Who ran it
- Overall scores for TC1, TC2, TC3
- Pass/fail summary

### Section 2: Before/After Comparison

The **pre-rewrite baseline** is documented in `docs/retrospectives/acvr1-fop-fuzzy-to-fact-retrospective.md`. Key failures:
- Returned BMP agonists for FOP (FAIL)
- Hallucinated NCT ID from prompt example (FAIL)
- Used curl exclusively (no MCP tools)
- No LOCATE→RETRIEVE discipline
- Estimated score: ~5/24

Compare against your TC2 results. Document the delta.

### Section 3: What Changed (Reference)
- `.mcp.json` now includes `lifesciences-research` MCP server (34 tools)
- All 6 skills rewritten: MCP tools primary, curl fallback
- LOCATE→RETRIEVE discipline enforced in all skills
- Gain-of-function disease filter added to graph-builder and pharmacology skills
- Grounding rules added to prevent parametric knowledge leakage

### Section 4: Remaining Issues
Document any issues you encounter. Known issues to watch for:
- **Open Targets GraphQL pagination**: The `knownDrugs` query may fail on first attempt with `cursor` vs `page` syntax. The skill falls back to curl for this — is that acceptable?
- **ChEMBL timeouts**: Detail endpoints (`chembl_get_compound`) often return 500 errors. Search endpoints are reliable. Document which ones fail.
- **Graphiti persistence**: `persist_to_graphiti` is NOT wired in the production agent (`apps/api/graphs/lifesciences.py:132` has `tools=[]`). This only affects the LangGraph backend, not Claude Code skill execution. Note whether you were able to persist to Graphiti via the `graphiti-docker` MCP.
- **Test protocol syntax**: The test protocol references `query_lifesciences(tool_name="hgnc_search_genes")` (production wrapper syntax) but the skills now call `hgnc_search_genes` directly via MCP. Note this mismatch and update the test protocol if time permits.

### Section 5: Recommendations
Based on your findings, prioritize next steps:
- P1 (Critical): What must be fixed before the next demo?
- P2 (Important): What should be addressed this sprint?
- P3 (Enhancement): What goes to the backlog?

---

## Task 5: Commit Results

Stage and commit all validation results:

```
git checkout feature/skills-evaluation-rewrite
git add docs/evaluations/results/ docs/competency-validations/ docs/retrospectives/skills-rewrite-validation-retrospective.md
git commit -m "Add E2E validation results and post-rewrite retrospective

- Run 3 test protocol cases (TC1 TP53, TC2 ACVR1/FOP, TC3 BRCA1/PARP)
- Score each against rubric (target: 15+/20)
- Run 3 competency questions (CQ1, CQ7, CQ11)
- Document before/after improvement and remaining gaps

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Directory Structure (create as needed)

```
docs/
├── evaluations/
│   ├── test-protocol.md                    # Already exists
│   ├── skills-evaluation-report.md         # Already exists
│   ├── behavioral-audit.md                 # Already exists
│   ├── consistency-analysis.md             # Already exists
│   └── results/                            # NEW — create this
│       ├── tc1-tp53-pathway.md
│       ├── tc2-acvr1-fop.md
│       └── tc3-brca1-parp.md
├── competency-validations/                 # NEW — create this
│   ├── cq1-fop-mechanism.md
│   ├── cq7-ngly1-repurposing.md
│   └── cq11-p53-mdm2-nutlin.md
└── retrospectives/
    ├── acvr1-fop-fuzzy-to-fact-retrospective.md  # Already exists (pre-rewrite)
    └── skills-rewrite-validation-retrospective.md # NEW — write this
```

## Success Criteria

The validation is complete when:
- [ ] All 3 test cases scored ≥15/20
- [ ] Agonist filtering confirmed working in TC2 (no Eptotermin Alfa or Dibotermin Alfa)
- [ ] All NCT IDs in output verified via `clinicaltrials_get_trial` MCP tool
- [ ] At least 3 competency questions have execution traces
- [ ] Retrospective documents the before/after scoring delta
- [ ] All results committed to `feature/skills-evaluation-rewrite` branch
