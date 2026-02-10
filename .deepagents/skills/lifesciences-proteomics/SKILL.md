---
name: lifesciences-proteomics
description: "Queries protein databases (UniProt, STRING, BioGRID) via MCP tools for protein lookups, protein-protein interactions, functional enrichment analysis, and cross-database ID mapping. Falls back to query_api_direct when MCP is unavailable. This skill should be used when the user asks to \"find protein interactions\", \"analyze interaction networks\", \"perform GO enrichment\", \"map protein IDs\", or mentions PPI networks, UniProt accessions, STRING scores, BioGRID interactions, or protein ID conversion between databases."
---


## Runtime constraints (DeepAgents)
- Prefer MCP tools first; use query_api_direct for HTTP fallbacks.
- Do not run shell curl in this runtime.
- Use relative file paths under `workspace/`.
- Graphiti persistence is optional/best-effort.

# Proteomics API Skills

Query protein databases via MCP tools (primary) or query_api_direct (fallback).

## Grounding Rule

All protein names, interaction partners, and scores MUST come from API results. Do NOT list protein interactions from training knowledge. If a query returns no results, report "No results found."

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

### UniProt: Protein Search & Retrieval

**LOCATE**: Search for protein by gene name

PRIMARY (MCP tool):
```
Call `uniprot_search_proteins` with: {"query": "TP53", "organism": "9606"}
→ Returns protein accessions, names, gene names
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://rest.uniprot.org/uniprotkb/search?query=gene:TP53+AND+organism_id:9606&format=json&size=3", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get protein by accession (function text is most valuable output)

PRIMARY (MCP tool):
```
Call `uniprot_get_protein` with: {"uniprot_id": "P04637"}
→ Returns: accession, gene, function text, cross-references
→ Parse function text for interactor mentions and pathway clues
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://rest.uniprot.org/uniprotkb/P04637.json", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get protein sequence (FASTA) — query_api_direct fallback
```bash
query_api_direct(url="https://rest.uniprot.org/uniprotkb/P04637.fasta", method="GET")  # runtime fallback (no shell)
```

### UniProt: Batch ID Mapping (Async) — query_api_direct fallback

**LOCATE** + **RETRIEVE** (two-step async pattern):
```bash
# Step 1: Submit ID mapping job
query_api_direct(url="https://rest.uniprot.org/idmapping/run", method="GET")  # runtime fallback (no shell)

# Step 2: Check status then get results
query_api_direct(url="https://rest.uniprot.org/idmapping/status/$JOB_ID", method="GET")  # runtime fallback (no shell)
query_api_direct(url="https://rest.uniprot.org/idmapping/results/$JOB_ID", method="GET")  # runtime fallback (no shell)
```

### STRING: Protein-Protein Interactions

**LOCATE**: Resolve gene symbol to STRING ID

PRIMARY (MCP tool):
```
Call `string_search_proteins` with: {"query": "TP53", "species": 9606}
→ Returns: 9606.ENSP00000269305
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://string-db.org/api/json/get_string_ids?identifiers=TP53&species=9606", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Get interaction network

PRIMARY (MCP tool):
```
Call `string_get_interactions` with: {"string_id": "9606.ENSP00000269305", "species": 9606, "required_score": 700}
→ Returns: interaction partners with confidence scores
```

FALLBACK (query_api_direct):
```bash
query_api_direct(url="https://string-db.org/api/json/network?identifiers=TP53&species=9606&required_score=700&limit=10", method="GET")  # runtime fallback (no shell)
```

**RETRIEVE**: Network for multiple proteins (batch — returns protein names in response)
```bash
query_api_direct(url="https://string-db.org/api/json/network?identifiers=TP53%0dMDM2%0dATM&species=9606", method="GET")  # runtime fallback (no shell)
```

### STRING: Functional Enrichment — query_api_direct fallback

**RETRIEVE**: GO/KEGG/Reactome enrichment for protein set
```bash
query_api_direct(url="https://string-db.org/api/json/enrichment?identifiers=9606.ENSP00000269305%0d9606.ENSP00000258149%0d9606.ENSP00000278616&species=9606", method="GET")  # runtime fallback (no shell)
```

### STRING: Network Visualization

PRIMARY (MCP tool):
```
Call `string_get_network_image_url` with: {"identifiers": ["TP53", "MDM2", "ATM"], "species": 9606}
→ Returns URL for network image
```

FALLBACK (query_api_direct):
```bash
echo "https://string-db.org/api/highres_image/network?identifiers=TP53%0dMDM2%0dATM&species=9606&network_flavor=confidence"
```

### BioGRID: Genetic & Physical Interactions

**LOCATE**: Search for gene interactions

PRIMARY (MCP tool):
```
Call `biogrid_search_genes` with: {"query": "TP53"}
→ Returns BioGRID gene entries
```

**RETRIEVE**: Get interactions for gene

PRIMARY (MCP tool):
```
Call `biogrid_get_interactions` with: {"gene_id": "TP53", "organism": 9606}
→ Returns: interaction partners, experimental systems
```

FALLBACK (query_api_direct — requires API key):
```bash
query_api_direct(url="https://webservice.thebiogrid.org/interactions?geneList=TP53&taxId=9606&format=json&accesskey=${BIOGRID_API_KEY}", method="GET")  # runtime fallback (no shell)
```

## ID Resolution Patterns

### Gene Symbol → STRING ID → UniProt (LOCATE chain)

```
# Step 1: Gene symbol → STRING ID (MCP LOCATE)
Call `string_search_proteins` with: {"query": "TP53", "species": 9606}
→ "9606.ENSP00000269305"

query_api_direct(url="<set-url>", method="GET")  # runtime fallback (no shell)
query_api_direct(url="https://rest.ensembl.org/xrefs/id/ENSP00000269305?content-type=application/json", method="GET")  # runtime fallback (no shell)
```

## Quick Reference

| Task | Pattern | MCP Tool (primary) | Curl Endpoint (fallback) |
|------|---------|-------------------|--------------------------|
| Search proteins | LOCATE | `uniprot_search_proteins` | UniProt `/uniprotkb/search` |
| Get protein details | RETRIEVE | `uniprot_get_protein` | UniProt `/uniprotkb/{accession}` |
| Batch ID mapping | LOCATE+RETRIEVE | (query_api_direct fallback) | UniProt `/idmapping/run` |
| Resolve to STRING ID | LOCATE | `string_search_proteins` | STRING `/get_string_ids` |
| Protein interactions | RETRIEVE | `string_get_interactions` | STRING `/network` |
| Functional enrichment | RETRIEVE | (query_api_direct fallback) | STRING `/enrichment` |
| Gene interactions | RETRIEVE | `biogrid_get_interactions` | BioGRID `/interactions` |

## ID Format Reference

| Database | API Argument (bare) | Graph CURIE | Example |
|----------|---------------------|-------------|---------|
| UniProt | `P04637` | `UniProtKB:P04637` | Bare accession for API |
| STRING | `9606.ENSP00000269305` | `STRING:9606.ENSP00000269305` | Species prefix + Ensembl protein |
| BioGRID | `TP53` (gene symbol) | N/A | Uses gene symbols directly |

## Rate Limits

| API | Limit | Auth Required |
|-----|-------|---------------|
| UniProt | 100 req/s | No |
| STRING | 1 req/s | No |
| BioGRID | 10 req/s | Yes (API key) |

## Pitfalls

- **STRING batch queries** (multiple proteins, separated by `%0d`) return protein names in response; **single-protein queries may NOT include names**.
- **STRING rate limit is 1 req/s** — don't make rapid sequential calls.
- **BioGRID requires `BIOGRID_API_KEY`** — check with `grep BIOGRID_API_KEY .env`.
- **UniProt function text** is the most valuable enrichment output — parse it for interactor mentions and pathway clues.

## Fallback Patterns

| Primary | Fallback | When |
|---------|----------|------|
| STRING `string_get_interactions` | BioGRID `biogrid_get_interactions` | <3 interactions returned from STRING |
| UniProt `uniprot_get_protein` | Ensembl xrefs + NCBI gene summary | UniProt down or no results |

## See Also

- **lifesciences-graph-builder**: Orchestrator for full Fuzzy-to-Fact protocol
- **lifesciences-genomics**: HGNC, Ensembl, NCBI gene resolution endpoints
