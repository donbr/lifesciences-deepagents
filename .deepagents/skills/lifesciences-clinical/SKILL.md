---
name: lifesciences-clinical
description: "Queries clinical databases (Open Targets, ClinicalTrials.gov) via MCP tools for target-disease associations, target tractability assessment, and clinical trial discovery. Falls back to query_api_direct when MCP is unavailable. This skill should be used when the user asks to \"validate drug targets\", \"find clinical trials\", \"assess target tractability\", \"discover disease associations\", or mentions Open Targets scores, NCT identifiers, target-disease evidence, druggability assessment, or translational research workflows."
---


## Runtime constraints (DeepAgents)
- Prefer MCP tools first; use query_api_direct for HTTP fallbacks.
- Do not run shell curl in this runtime.
- Use relative file paths under `workspace/`.
- Graphiti persistence is optional/best-effort.

# Clinical & Translational API Skills

Query clinical databases via MCP tools (primary) or query_api_direct (fallback).

## Grounding Rule

All target-disease associations, drug names, trial IDs, and clinical data MUST come from API results. Do NOT provide NCT IDs, trial statuses, or drug-disease associations from training knowledge. If a query returns no results, report "No results found."

## MCP Token Budgeting (`slim` Parameter)

All MCP tools in this skill support a `slim` parameter for token-efficient queries:

**When to use `slim=true`:**
- LOCATE phase: Fast candidate lists (returns ~20 tokens/entity vs ~115-300 tokens)
- Batch operations: Resolving multiple entities in a single turn
- Exploration: Quick overviews without full metadata

**When to use `slim=false` (default):**
- RETRIEVE phase: Need full metadata with cross-references
- Validation: Verifying detailed properties
- Graph persistence: Collecting complete entity records

**Example:**
```
# LOCATE: Find top 10 gene candidates (slim=true for speed)
Call `hgnc_search_genes` with: {"query": "TNF", "slim": true, "page_size": 10}
→ Returns minimal fields: ID, symbol, name only (~20 tokens each)

# RETRIEVE: Get full record for validation (slim=false, default)
Call `hgnc_get_gene` with: {"hgnc_id": "HGNC:11892"}
→ Returns complete metadata with cross-references (~115 tokens)
```

**Impact:** Using `slim=true` during LOCATE enables 5-10x more entities per LLM turn without context overflow.

**Reference:** This token budgeting pattern is detailed in `reference/prior-art-api-patterns.md` (Section 7.1).

## LOCATE → RETRIEVE Patterns

### Open Targets: Target-Disease Associations

**LOCATE**: Search for target or disease

PRIMARY (MCP tool):
```
Call `opentargets_search_targets` with: {"query": "breast cancer"}
→ Returns: target/disease IDs and names
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get diseases associated with target

PRIMARY (MCP tool):
```
Call `opentargets_get_associations` with: {"ensembl_id": "ENSG00000141510"}
→ Returns: associated diseases with scores and evidence types
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
```

### Open Targets: Target Tractability — query_api_direct fallback

**RETRIEVE**: Get druggability assessment
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
```

### Open Targets: Known Drugs for Target

**LOCATE**: Find approved drugs targeting a protein

PRIMARY (MCP tool):
```
Call `opentargets_get_target` with: {"ensembl_id": "ENSG00000171791"}
→ Returns: knownDrugs with drug name, phase, mechanismOfAction
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
```

**Note**: Always include `index: 0` in pagination — omitting it causes errors.

### Open Targets: All-in-One Nested Query — query_api_direct fallback

**RETRIEVE**: Get target + diseases + drugs + tractability in single call
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
    "query": "{
      target(ensemblId: \"ENSG00000141510\") {
        approvedSymbol
        biotype
        tractability { label value }
        knownDrugs(page: {index: 0, size: 3}) {
          rows { drug { name } phase mechanismOfAction }
        }
        associatedDiseases(page: {index: 0, size: 3}) {
          rows { disease { name id } score }
        }
      }
    }"
  }' | jq '.data.target'
```

### Open Targets: Disease-Centric Queries — query_api_direct fallback

**RETRIEVE**: Get targets associated with disease
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
```

## ClinicalTrials.gov API v2

### LOCATE: Search Clinical Trials

**By condition**:

PRIMARY (MCP tool):
```
Call `clinicaltrials_search_trials` with: {"query": "breast cancer"}
→ Returns: NCT IDs, titles, phases, statuses
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://clinicaltrials.gov/api/v2/studies?query.cond=breast+cancer&pageSize=3&format=json", method="GET")  # runtime fallback (no shell)
```

**By intervention (drug)**:

PRIMARY (MCP tool):
```
Call `clinicaltrials_search_trials` with: {"query": "venetoclax"}
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://clinicaltrials.gov/api/v2/studies?query.intr=venetoclax&pageSize=3&format=json", method="GET")  # runtime fallback (no shell)
```

**By status** (query_api_direct fallback — more parameter control):
```bash
query_api_direct(url="https://clinicaltrials.gov/api/v2/studies?filter.overallStatus=RECRUITING&query.cond=leukemia&pageSize=3&format=json", method="GET")  # runtime fallback (no shell)
```

**By study type** (use `query.term` with AREA syntax — `filter.studyType` is NOT valid in v2):
```bash
query_api_direct(url="https://clinicaltrials.gov/api/v2/studies?query.term=AREA[StudyType]INTERVENTIONAL&query.cond=cancer&pageSize=3&format=json", method="GET")  # runtime fallback (no shell)
```

### RETRIEVE: Get Trial Details

**By NCT ID**:

PRIMARY (MCP tool):
```
Call `clinicaltrials_get_trial` with: {"nct_id": "NCT00461032"}
→ Returns: title, status, phase, conditions, interventions
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://clinicaltrials.gov/api/v2/studies/NCT00461032?format=json", method="GET")  # runtime fallback (no shell)
    nct: .protocolSection.identificationModule.nctId,
    title: .protocolSection.identificationModule.briefTitle,
    status: .protocolSection.statusModule.overallStatus,
    phase: .protocolSection.designModule.phases,
    conditions: .protocolSection.conditionsModule.conditions,
    interventions: [.protocolSection.armsInterventionsModule.interventions[]?.name]
  }'
```

### RETRIEVE: Get Trial Locations

PRIMARY (MCP tool):
```
Call `clinicaltrials_get_trial_locations` with: {"nct_id": "NCT00461032"}
→ Returns: trial site locations
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://clinicaltrials.gov/api/v2/studies/NCT00461032?format=json", method="GET")  # runtime fallback (no shell)
```

## Quick Reference

| Task | Pattern | MCP Tool (primary) | Curl Endpoint (fallback) |
|------|---------|-------------------|--------------------------|
| Search diseases | LOCATE | `opentargets_search_targets` | Open Targets GraphQL `search` |
| Target-disease associations | RETRIEVE | `opentargets_get_associations` | Open Targets GraphQL `associatedDiseases` |
| Target tractability | RETRIEVE | (query_api_direct fallback) | Open Targets GraphQL `tractability` |
| Known drugs for target | LOCATE | `opentargets_get_target` | Open Targets GraphQL `knownDrugs` |
| Disease → targets | RETRIEVE | (query_api_direct fallback) | Open Targets GraphQL `associatedTargets` |
| Search trials | LOCATE | `clinicaltrials_search_trials` | ClinicalTrials.gov `/studies?query.*` |
| Get trial details | RETRIEVE | `clinicaltrials_get_trial` | ClinicalTrials.gov `/studies/{NCT}` |

## ClinicalTrials.gov v2 Valid Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `query.cond` | Condition/disease | `breast+cancer` |
| `query.intr` | Intervention/drug | `venetoclax` |
| `query.term` | General search (supports AREA syntax) | `AREA[StudyType]INTERVENTIONAL` |
| `filter.overallStatus` | Status filter | `RECRUITING`, `COMPLETED` |
| `pageSize` | Results per page | `10` |
| `pageToken` | Pagination token | From previous response |
| `format` | Response format | `json` |

**Invalid**: `filter.studyType` does NOT exist in v2 API.

## ID Format Reference

| Database | API Argument | Graph CURIE | Example |
|----------|-------------|-------------|---------|
| Open Targets (target) | `ENSG00000141510` | `ENSG00000141510` | Ensembl gene ID |
| Open Targets (disease) | `EFO_0000305` | `EFO:0000305` | EFO with underscore for API |
| ClinicalTrials.gov | `NCT03312634` | `NCT03312634` | NCT ID (bare) |

## Common Workflows

### Drug Target Validation Pipeline

```
# Step 1: RETRIEVE — Get target-disease association score (MCP)
Call `opentargets_get_associations` with: {"ensembl_id": "ENSG00000171791"}

query_api_direct(url="<set-url>", method="GET")  # runtime fallback (no shell)
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)

# Step 3: LOCATE — Find clinical trials (MCP)
Call `clinicaltrials_search_trials` with: {"query": "BCL2 RECRUITING"}
```

### Disease → Targets → Drugs → Trials (Full Chain)

```
query_api_direct(url="<set-url>", method="GET")  # runtime fallback (no shell)
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)

# Step 2: LOCATE — Get drugs for top target (MCP)
Call `opentargets_get_target` with: {"ensembl_id": "ENSG00000171791"}

# Step 3: LOCATE — Find trials for drug (MCP)
Call `clinicaltrials_search_trials` with: {"query": "venetoclax leukemia RECRUITING"}
```

## Fallback Patterns

| Primary Search | Fallback | When |
|---------------|----------|------|
| Drug + disease trial search | Disease-only search | Zero results for drug+disease combination |
| Specific drug name search | Broader mechanism class search | Drug name not in ClinicalTrials.gov |

## Rate Limits

| API | Limit | Notes |
|-----|-------|-------|
| Open Targets | ~5 req/s (practical) | No auth required; 0.2s delay in production |
query_api_direct(url="<set-url>", method="GET")  # runtime fallback (no shell)

## Pitfalls

- **Open Targets requires Ensembl Gene IDs** (ENSG*) for target queries; use EFO IDs for disease queries.
- **Always include `index: 0`** in Open Targets pagination: `page: {index: 0, size: N}`.
- **ClinicalTrials.gov** uses Cloudflare protection that may block Python httpx clients. Use query_api_direct for reliable access.
- **`filter.studyType` is NOT valid** in v2 API. Use `query.term=AREA[StudyType]INTERVENTIONAL`.

## See Also

- **lifesciences-graph-builder**: Orchestrator for full Fuzzy-to-Fact protocol
- **lifesciences-pharmacology**: ChEMBL, PubChem drug endpoints
