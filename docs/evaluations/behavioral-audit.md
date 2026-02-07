# Behavioral Audit: Life Sciences Skills

## Audit Methodology

This audit analyzes what Claude Code *actually does* when each skill is invoked, compared to what the SKILL.md instructs. Analysis is based on:
1. The ACVR1/FOP execution trace (2026-02-07 retrospective)
2. Structural analysis of each SKILL.md for behavioral triggers
3. Known Claude Code behavioral patterns with MCP tools vs parametric knowledge

## Test Case: TP53 Pathway (Test Case #1)

### Skill 1: lifesciences-genomics

**Expected behavior**: Use HGNC curl to search for TP53, then fetch by HGNC ID. Use Ensembl for cross-references.

**Predicted actual behavior**:
| Step | Expected (SKILL.md) | Likely Actual | Issue |
|------|---------------------|---------------|-------|
| Gene search | `curl HGNC /search/symbol/TP53` | May answer "TP53 is HGNC:11998" from memory | **No LOCATE enforcement** — skill shows curl examples but doesn't mandate their use before answering |
| Gene metadata | `curl Ensembl /lookup/id/ENSG00000141510` | May skip if already "knows" chromosome 17p13.1 | **No RETRIEVE mandate** — skill is a reference, not a workflow |
| Cross-references | `curl Ensembl /xrefs/id/ENSG00000141510` | Likely skipped entirely | Skill lists the command but doesn't require it |

**Key finding**: The genomics skill is structured as a **reference card** (API endpoint catalog) rather than a **workflow**. It provides curl examples but never says "you MUST call this before answering." Claude Code can satisfy user queries from parametric knowledge without ever touching the APIs.

**LOCATE→RETRIEVE discipline**: ABSENT — no explicit two-step pattern defined.

**CURIE output**: Not required — skill shows `jq` filters that extract bare IDs (e.g., `{hgnc_id, symbol, name}`), not full CURIEs.

---

### Skill 2: lifesciences-proteomics

**Expected behavior**: Search UniProt for TP53 protein, get protein details, query STRING for interactions.

**Predicted actual behavior**:
| Step | Expected (SKILL.md) | Likely Actual | Issue |
|------|---------------------|---------------|-------|
| Protein search | `curl UniProt /search?query=gene:TP53` | May state "P04637 is the TP53 protein" from memory | **No LOCATE enforcement** |
| Protein details | `curl UniProt /P04637.json` | Might call this OR might summarize from knowledge | Depends on whether user asks for specific fields |
| STRING interactions | `curl STRING /network?identifiers=TP53` | More likely to call this (novel data) | STRING data is less likely to be memorized |
| BioGRID interactions | `curl BioGRID /interactions?geneList=TP53` | Likely called if STRING fails | Requires API key — may fail silently |

**Key finding**: Like genomics, this is a reference card. The "ID Resolution Patterns" section (lines 112-121) shows a useful LOCATE→RETRIEVE pattern (gene symbol → STRING ID → UniProt) but doesn't label it as mandatory.

**LOCATE→RETRIEVE discipline**: IMPLICIT — pattern exists in examples but is not named or enforced.

**CURIE output**: Inconsistent — UniProt examples return bare accessions (`P04637`), STRING returns bare IDs (`9606.ENSP00000269305`). No CURIE formatting guidance.

---

### Skill 3: lifesciences-pharmacology

**Expected behavior**: Search ChEMBL for compounds, get mechanisms, find bioactivity data.

**Predicted actual behavior**:
| Step | Expected (SKILL.md) | Likely Actual | Issue |
|------|---------------------|---------------|-------|
| Compound search | `curl ChEMBL /molecule/search?q=venetoclax` | May state "Venetoclax is CHEMBL3137309" from memory | **No LOCATE enforcement** |
| Drug mechanism | `curl ChEMBL /mechanism?molecule_chembl_id=CHEMBL3137309` | Likely called — mechanism details are novel | Good: this is a RETRIEVE step |
| Drug indications | `curl ChEMBL /drug_indication?...` | Likely called if mechanisms succeeded | |
| Open Targets fallback | Not documented | **MISSING** — skill doesn't mention Open Targets | Critical gap from production code |

**Key finding**: The pharmacology skill has the **best workflow example** (lines 149-163: "Drug Repurposing" pattern) but it assumes you already know the ChEMBL ID. There is no guidance on what to do when ChEMBL returns 500 errors — the production code uses Open Targets as fallback, but this skill doesn't document it.

**LOCATE→RETRIEVE discipline**: PARTIAL — "Drug Repurposing" workflow shows a 3-step pattern (find target → find drugs → get indications) but doesn't use LOCATE/RETRIEVE terminology.

**CURIE output**: Bare ChEMBL IDs only (e.g., `CHEMBL3137309`, not `CHEMBL:3137309`).

---

### Skill 4: lifesciences-clinical

**Expected behavior**: Query Open Targets for target-disease associations, search ClinicalTrials.gov for trials.

**Predicted actual behavior**:
| Step | Expected (SKILL.md) | Likely Actual | Issue |
|------|---------------------|---------------|-------|
| Target-disease | Open Targets GraphQL | Likely called — GraphQL is specific enough | Good: requires Ensembl ID (forces prior resolution) |
| Known drugs | Open Targets `knownDrugs` | Likely called | Good: structured data, hard to guess |
| Trial search | ClinicalTrials.gov v2 API | Likely called | API is specific enough to force tool use |
| Trial details | ClinicalTrials.gov by NCT ID | Likely called for verification | Good |

**Key finding**: This skill has the **strongest tool-use incentives** because Open Targets GraphQL requires specific Ensembl IDs and ClinicalTrials.gov returns structured JSON that Claude can't easily fabricate. However, it has a **filter documentation bug**: `filter.advanced=AREA[Phase]PHASE3` on line 121 — the correct v2 syntax is not well-documented.

**LOCATE→RETRIEVE discipline**: IMPLICIT — the "Disease → Targets → Drugs → Trials" workflow (lines 177-195) is a 3-step chain but doesn't label steps as LOCATE/RETRIEVE.

**CURIE output**: Uses Ensembl IDs for targets, EFO IDs for diseases — good. NCT IDs returned as bare strings.

**Bug**: `knownDrugs` query on line 50 is missing `index: 0` in pagination: `page: {size: 5}` should be `page: {size: 5, index: 0}`. This may cause errors.

---

### Skill 5: lifesciences-crispr

**Expected behavior**: Resolve gene to Entrez ID via HGNC, then query BioGRID ORCS for essentiality data.

**Predicted actual behavior**:
| Step | Expected (SKILL.md) | Likely Actual | Issue |
|------|---------------------|---------------|-------|
| Gene resolution | HGNC MCP → Entrez ID | Likely called — skill mandates this step | **Best LOCATE example** in all skills |
| ORCS essential screens | `curl orcsws.thebiogrid.org/gene/{id}?hit=yes` | Likely called — data is too specific to guess | Good |
| Screen annotations | `curl orcsws.thebiogrid.org/screens/` | Likely called — second step of workflow | Good |

**Key finding**: The CRISPR skill has the **strongest workflow discipline** of all 6 skills. Phase 1 explicitly says "Resolve Gene Identifiers" and Phase 2 says "Query ORCS for Essential Screens Only". The `hit=yes` parameter is emphasized as critical. However, it doesn't use LOCATE/RETRIEVE terminology.

**LOCATE→RETRIEVE discipline**: PRESENT but unnamed — Phases 1-5 form a clear sequential pipeline.

**CURIE output**: Uses Entrez IDs (bare, e.g., `7298`). No CURIE formatting.

---

### Skill 6: lifesciences-graph-builder (Orchestrator)

**Expected behavior**: Execute 7-phase Fuzzy-to-Fact protocol using MCP tools for nodes and curl for edges.

**Predicted actual behavior** (based on ACVR1 trace):
| Phase | Expected (SKILL.md) | Observed (Retrospective) | Issue |
|-------|---------------------|--------------------------|-------|
| 1 ANCHOR | HGNC search → get gene | HGNC search worked; over-resolved drugs | Scope creep into Phase 4a |
| 2 ENRICH | UniProt get protein | Used PubMed instead of structured APIs | **Tier demotion**: narrative text instead of structured IDs |
| 3 EXPAND | STRING interactions, WikiPathways | Partial — WikiPathways found paths but didn't enumerate components | Incomplete RETRIEVE step |
| 4a DRUGS | ChEMBL/Open Targets | Open Targets returned agonists (wrong drugs for FOP) | **No mechanism filtering** for gain-of-function diseases |
| 4b TRIALS | ClinicalTrials.gov | Searched for wrong drugs → zero results | Cascading failure from Phase 4a |
| 5 VALIDATE | Verify NCT IDs, mechanisms | Hallucinated NCT ID from prompt example | **Hallucination injection** from parametric knowledge |
| 6 PERSIST | Graphiti add_memory | Failed — no tools wired | **BUG**: `tools=[]` |

**Key finding**: The graph-builder skill's **architecture diagram** (lines 12-35) correctly defines the three-tier pattern, but the **workflow section** (lines 37-191) doesn't enforce mandatory tool calls. Each phase shows code examples with `# MCP:` comments, but these are treated as suggestions, not requirements. The validator hallucinated entities not from upstream, proving the **external knowledge restriction** is missing.

**LOCATE→RETRIEVE discipline**: IMPLICIT — Phase 1 shows search→get pattern but doesn't enforce it or label it.

**CURIE output**: Defined in "Node Types" table (lines 193-204) but not enforced in workflow steps.

---

## Cross-Skill Behavioral Summary

### Pattern: Parametric Knowledge Override

All 6 skills share a common vulnerability: **Claude Code can satisfy most user queries from parametric knowledge without calling any tools.** The skills provide tool examples but never say:

> "You MUST call this tool before providing any answer. If the tool returns no results, say 'No results found' — do NOT fill in from memory."

This is the single most impactful gap. Per Anthropic's hallucination reduction guidance: *"Explicitly instruct Claude to only use information from provided documents [tools] and not its general knowledge."*

### Pattern: Reference Card vs Workflow

| Skill | Structure | LOCATE→RETRIEVE | Enforcement |
|-------|-----------|-----------------|-------------|
| genomics | Reference card | ABSENT | None |
| proteomics | Reference card | IMPLICIT | None |
| pharmacology | Reference card + workflow | PARTIAL | Weak (examples only) |
| clinical | Reference card + workflow | IMPLICIT | Medium (requires specific IDs) |
| crispr | 5-phase workflow | PRESENT (unnamed) | Strong (pipeline structure) |
| graph-builder | 7-phase workflow | IMPLICIT | Weak (code comments only) |

### Pattern: CURIE Inconsistency

No skill produces consistent CURIEs:
- Genomics: Bare HGNC IDs, bare Ensembl IDs
- Proteomics: Bare UniProt accessions, bare STRING IDs
- Pharmacology: Bare ChEMBL IDs
- Clinical: Ensembl IDs for targets, EFO IDs for diseases, bare NCT IDs
- CRISPR: Bare Entrez IDs
- Graph-builder: CURIEs defined in table but not enforced in workflow

### Hallucination Risk Assessment

| Skill | Risk Level | Reason |
|-------|------------|--------|
| genomics | HIGH | All facts available in parametric knowledge; no tool-use mandate |
| proteomics | HIGH | Common proteins well-known; interactions less so |
| pharmacology | HIGH | Drug names/mechanisms widely known; no fallback docs |
| clinical | MEDIUM | GraphQL requires specific IDs (forces some tool use) |
| crispr | LOW | ORCS data is obscure enough to force API calls |
| graph-builder | HIGH | Orchestrator — amplifies upstream hallucination risks |

---

## Recommendations

1. **Add external knowledge restriction** to ALL skills (mandatory, per Anthropic guidance)
2. **Convert reference cards to workflows** — genomics, proteomics, pharmacology need LOCATE→RETRIEVE structure
3. **Label and enforce LOCATE→RETRIEVE** — use explicit two-step terminology
4. **Standardize CURIE output** — define API context (bare IDs) vs graph context (full CURIEs) distinction
5. **Add Open Targets fallback** to pharmacology skill
6. **Fix `knownDrugs` pagination** — add `index: 0` to clinical skill
7. **Add mechanism filtering** for gain-of-function diseases in graph-builder
