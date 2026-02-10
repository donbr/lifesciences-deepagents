---
name: lifesciences-pharmacology
description: "Queries pharmacology databases (ChEMBL, PubChem, IUPHAR, Open Targets) via MCP tools for drug mechanisms, target identification, bioactivity profiling, and indication discovery. Falls back to query_api_direct when MCP is unavailable. This skill should be used when the user asks to \"find drug mechanisms\", \"identify drug targets\", \"analyze bioactivity data\", \"discover drug indications\", or mentions ChEMBL IDs, mechanisms of action, IC50/Ki values, drug-target relationships, or compound similarity searches."
---


## Runtime constraints (DeepAgents)
- Prefer MCP tools first; use query_api_direct for HTTP fallbacks.
- Do not run shell curl in this runtime.
- Use relative file paths under `workspace/`.
- Graphiti persistence is optional/best-effort.

# Pharmacology API Skills

Query pharmacology databases via MCP tools (primary) or query_api_direct (fallback).

## Grounding Rule

All drug names, mechanisms, targets, and bioactivity values MUST come from API results. Do NOT provide drug information from training knowledge. If a query returns no results, report "No results found."

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

### ChEMBL: Compound Search & Details

**LOCATE**: Search compound by name

PRIMARY (MCP tool):
```
Call `chembl_search_compounds` with: {"query": "venetoclax"}
→ Returns: ChEMBL IDs, preferred names, max phase
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/molecule/search?q=venetoclax&format=json", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get compound by ChEMBL ID

PRIMARY (MCP tool):
```
Call `chembl_get_compound` with: {"chembl_id": "CHEMBL3137309"}
→ May return 500 error (common for detail endpoints) — fall back to Open Targets
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL3137309?format=json", method="GET")  # runtime fallback (no shell)
```

### Open Targets: Drug Discovery (PRIMARY — More Reliable Than ChEMBL)

**LOCATE**: Find drugs targeting a protein

PRIMARY (MCP tool):
```
Call `opentargets_get_target` with: {"ensembl_id": "ENSG00000171791"}
→ Returns: knownDrugs with drug name, mechanismOfAction, phase in one call
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://api.platform.opentargets.org/api/v4/graphql", method="GET")  # runtime fallback (no shell)
```

**Open Targets `knownDrugs` Pagination**:
- Use `size` parameter only (e.g., `size: 25`) — this is the reliable pattern
- Do NOT use `page` or `index` — these cause intermittent failures
- For paginated results, use `cursor` (returned in the response) as the continuation token
- If first query fails, retry with `size` only (no other pagination params)

**Note**: Requires Ensembl Gene ID (ENSG...). Get this from HGNC cross-references or Ensembl lookup.

### ChEMBL: Drug Mechanisms (Critical for Graph Edges) — query_api_direct fallback

**RETRIEVE**: Get mechanism for drug (Drug → Target edge)
```bash
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL3137309&format=json", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Find all drugs for target (Target → Drugs edge)
```bash
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/mechanism?target_chembl_id=CHEMBL4860&format=json", method="GET")  # runtime fallback (no shell)
```

### ChEMBL: Drug Indications — query_api_direct fallback

**RETRIEVE**: Get indications for drug (Drug → Disease edge)
```bash
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/drug_indication?molecule_chembl_id=CHEMBL3137309&format=json", method="GET")  # runtime fallback (no shell)
```

### ChEMBL: Bioactivity Data (Potency Metrics) — query_api_direct fallback

**RETRIEVE**: Get activity data (IC50, Ki, EC50)
```bash
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/activity?molecule_chembl_id=CHEMBL3137309&format=json&limit=10", method="GET")  # runtime fallback (no shell)
```

### PubChem: Compound Data

**LOCATE**: Get compound by name

PRIMARY (MCP tool):
```
Call `pubchem_search_compounds` with: {"query": "aspirin"}
→ Returns: CID, molecular formula, properties
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/JSON", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get properties by CID

PRIMARY (MCP tool):
```
Call `pubchem_get_compound` with: {"cid": "2244"}
→ Returns: molecular formula, weight, IUPAC name
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularFormula,MolecularWeight,IUPACName/JSON", method="GET")  # runtime fallback (no shell)
```

### IUPHAR/GtoPdb: Pharmacology

**LOCATE**: Search ligands

PRIMARY (MCP tool):
```
Call `iuphar_search_ligands` with: {"query": "ibuprofen"}
→ Returns: ligand ID, name, type, approved status
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://www.guidetopharmacology.org/services/ligands?name=ibuprofen", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get ligand-target interactions

PRIMARY (MCP tool):
```
Call `iuphar_get_ligand` with: {"ligand_id": "2713"}
→ Returns: target interactions, action types, affinities
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://www.guidetopharmacology.org/services/ligands/2713/interactions", method="GET")  # runtime fallback (no shell)
```

## Drug Repurposing Workflow (LOCATE → RETRIEVE Chain)

```bash
query_api_direct(url="<set-url>", method="GET")  # runtime fallback (no shell)
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL3137309&format=json", method="GET")  # runtime fallback (no shell)

# Step 2: RETRIEVE — Find other drugs for same target
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/mechanism?target_chembl_id=$TARGET&format=json", method="GET")  # runtime fallback (no shell)

# Step 3: RETRIEVE — Get indications for alternative drug
query_api_direct(url="https://www.ebi.ac.uk/chembl/api/data/drug_indication?molecule_chembl_id=CHEMBL2107358&format=json", method="GET")  # runtime fallback (no shell)
```

## Quick Reference

| Task | Pattern | MCP Tool (primary) | Curl Endpoint (fallback) |
|------|---------|-------------------|--------------------------|
| Search compounds | LOCATE | `chembl_search_compounds` | ChEMBL `/molecule/search` |
| Get compound | RETRIEVE | `chembl_get_compound` | ChEMBL `/molecule/{id}` |
| Drug mechanism | RETRIEVE | (query_api_direct fallback) | ChEMBL `/mechanism` |
| Drug indications | RETRIEVE | (query_api_direct fallback) | ChEMBL `/drug_indication` |
| Bioactivity data | RETRIEVE | (query_api_direct fallback) | ChEMBL `/activity` |
| Find drugs for target | LOCATE | `opentargets_get_target` | Open Targets GraphQL `knownDrugs` |
| Compound by name | LOCATE | `pubchem_search_compounds` | PubChem `/compound/name/{name}` |
| Ligand interactions | RETRIEVE | `iuphar_get_ligand` | IUPHAR `/ligands/{id}/interactions` |

## ID Format Reference

| Database | API Argument (bare) | Graph CURIE | Example |
|----------|---------------------|-------------|---------|
| ChEMBL compound | `CHEMBL3137309` | `CHEMBL:3137309` | Bare for API (no colon) |
| ChEMBL target | `CHEMBL4860` | `CHEMBL:4860` | Same pattern |
| PubChem | `2244` (CID) | `PubChem:2244` | Bare numeric for API |

## API Reliability & Fallback Patterns

| Primary | Fallback | When to Switch |
|---------|----------|----------------|
| ChEMBL `chembl_get_compound` (detail) | Open Targets `opentargets_get_target` | On HTTP 500 (common for detail endpoints) |
| ChEMBL `chembl_search_compounds` (search) | (generally reliable — uses Elasticsearch) | Retry once, then report failure |
| ChEMBL `/mechanism` | Open Targets `mechanismOfAction` field | On HTTP 500 |

**Critical**: ChEMBL **detail endpoints** (`/molecule/{id}`) frequently return 500 errors (EBI server issues). ChEMBL **search endpoints** (`/molecule/search?q=...`) are generally reliable because they use Elasticsearch. When detail fails, use Open Targets as primary drug discovery source.

## Rate Limits

| API | Limit | Auth Required | Production Throttle |
|-----|-------|---------------|---------------------|
| ChEMBL | ~2 req/s | No | 0.5s delay in production |
| PubChem | 5 req/s | No | — |
| IUPHAR | 10 req/s | No | — |

## Query Best Practices

### Drug Discovery vs Repurposing
- **Drug repurposing**: Use `max_phase >= 2` filter (want clinical validation, shorter approval path)
- **General discovery**: No phase filter (include preclinical tools, mechanism probes, research reagents)
- **Target validation**: No phase filter needed for mechanism studies

### Gain-of-Function Disease Filter
For diseases caused by protein overactivation (e.g., FOP from constitutive ACVR1):
- INCLUDE: inhibitors, antagonists, negative modulators
- EXCLUDE: agonists, positive modulators, activators
- Check `mechanismOfAction` field from Open Targets or `action_type` from ChEMBL

### Query Efficiency
- Check mechanisms (`/mechanism` endpoint) before bioactivity data
- Use `target_chembl_id` for reverse lookups (find drugs for target)
- Limit activity queries with `&limit=10` for exploration

## See Also

- **lifesciences-graph-builder**: Orchestrator for full Fuzzy-to-Fact protocol
- **lifesciences-clinical**: Open Targets, ClinicalTrials.gov clinical endpoints
