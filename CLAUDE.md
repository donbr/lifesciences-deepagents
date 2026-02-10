# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Life Sciences Deep Agents Platform - A multi-agent system for biomedical research combining LangGraph-based agents with a shared React UI. The primary agent is:
- **lifesciences**: "Fuzzy-to-Fact" protocol for biological entity resolution (ANCHOR → ENRICH → EXPAND → TRAVERSE_DRUGS → TRAVERSE_TRIALS → VALIDATE → PERSIST)

Legacy agents (`research`, `coding`) exist but are deprecated.

## Commands

### Backend (Python with uv)
```bash
uv sync                    # Install dependencies
uv run langgraph dev       # Start backend on :2024
fuser -k 2024/tcp          # Kill port 2024 if address in use
```

### Frontend (yarn)
```bash
cd apps/web
yarn install               # Install dependencies
yarn dev                   # Dev server with Turbopack on :3000
yarn build                 # Production build
yarn lint                  # ESLint
yarn lint:fix              # ESLint with auto-fix
yarn format                # Prettier format
yarn format:check          # Check formatting
```

### Testing & Verification
```bash
uv run python scripts/verify_mcp_client.py       # Test MCP client connectivity
uv run python scripts/verify_mcp_wrapper.py       # Test MCP tool wrappers
uv run python scripts/verify_pubmed.py            # Test PubMed stdio adapter
uv run python scripts/inspect_mcp_capabilities.py # List available MCP tools
uv run python scripts/test_lifesciences_agent.py  # End-to-end agent test
```

## Architecture

### Directory Layout
- `apps/api/graphs/` — Agent definitions (`lifesciences.py`)
- `apps/api/shared/mcp.py` — `HTTPMCPClient` + `StdioMCPClient` + all MCP tool wrappers + rate limiter
- `apps/api/shared/tools.py` — `tavily_search`, `fetch_webpage_content`, `think_tool`
- `apps/api/shared/prompts.py` — System prompts for supervisor + all 7 phase specialists
- `apps/web/src/app/hooks/useChat.ts` — Core chat state, streaming, interrupt handling
- `apps/web/src/providers/` — `ClientProvider` (LangGraph SDK client), `ChatProvider` (state context)

### DeepAgents Pattern

All agents use `create_deep_agent()` from the `deepagents` library. This creates a **supervisor** that delegates to **specialist subagents** via `task()` tool calls. The supervisor has no tools itself — it only routes. Default model: `openai:gpt-4o` (lifesciences.py:38).

The lifesciences agent has 7 specialists (one per Fuzzy-to-Fact phase). Each specialist gets only the tools it needs (tool isolation):

| Specialist | Phase | Tools |
|------------|-------|-------|
| `anchor_specialist` | 1 ANCHOR | `query_lifesciences`, `query_pubmed`, `think_tool` |
| `enrichment_specialist` | 2 ENRICH | `query_lifesciences`, `query_pubmed`, `think_tool` |
| `expansion_specialist` | 3 EXPAND | `query_lifesciences`, `think_tool` |
| `traversal_drugs_specialist` | 4a TRAVERSE_DRUGS | `query_lifesciences`, `query_api_direct`, `think_tool` |
| `traversal_trials_specialist` | 4b TRAVERSE_TRIALS | `query_lifesciences`, `query_api_direct`, `think_tool` |
| `validation_specialist` | 5 VALIDATE | `query_lifesciences`, `query_pubmed`, `think_tool` |
| `persistence_specialist` | 6 PERSIST | (none — formats and summarizes) |

The library's `SubAgentMiddleware` automatically gives each subagent: `TodoListMiddleware`, `FilesystemMiddleware`, `SummarizationMiddleware`, `AnthropicPromptCachingMiddleware`, and a built-in general-purpose agent.

### MCP Integration

`shared/mcp.py` provides two MCP client types (`HTTPMCPClient` for remote JSON-RPC, `StdioMCPClient` for local npx servers). Five tool wrappers bridge to APIs:

| Tool | Connection | Timeout | Purpose |
|------|------------|---------|---------|
| `query_lifesciences` | HTTP → `lifesciences-research.fastmcp.app/mcp` | 120s | ChEMBL, HGNC, UniProt, STRING, BioGRID, ClinicalTrials.gov, Open Targets, PubChem, WikiPathways, Ensembl, Entrez, IUPHAR |
| `query_pubmed` | Stdio → `npx @cyanheads/pubmed-mcp-server` | — | PubMed article search, metadata, and full text |
| `query_langchain_docs` | HTTP → `docs.langchain.com/mcp` | 30s | LangChain/LangGraph documentation |
| `query_api_direct` | Direct HTTP to arbitrary URL | 30s | Direct HTTP GET/POST fallback (e.g., Open Targets GraphQL) |
| `persist_to_graphiti` | HTTP → `localhost:8000/mcp` | 30s | Save knowledge graph as JSON episodes to Graphiti |

`query_lifesciences` accepts a `tool_args` parameter for full API control: `tool_args={"gene_symbol": "TP53"}`.

**PubMed adapter note**: `query_pubmed` remaps tool names and arguments for the `@cyanheads/pubmed-mcp-server` (e.g., `search_articles` → `pubmed_search_articles`, `query` → `queryTerm`, `max_results` → `maxResults`). See mcp.py:278-283.

**Rate limits**: STRING 1 req/s, ChEMBL 0.5s, PubMed 0.34s, BioGrid 0.5s, Open Targets 0.2s.

### API Reliability

- **ChEMBL frequently returns 500 errors.** Use Open Targets `knownDrugs` GraphQL as fallback (returns drugs + mechanisms + phases in one call).
- **HGNC is fastest/most reliable** for gene resolution — always start ANCHOR phase there.
- **STRING batch queries** return protein names; single queries don't.
- **Open Targets GraphQL** requires explicit `index: 0` in pagination.
- **ClinicalTrials.gov v2 API** is stable and returns structured JSON.

### Frontend Data Flow

UI settings (`ConfigDialog`) → `assistantId` stored in localStorage → `useChat` hook creates `@langchain/langgraph-sdk` client → streams from LangGraph backend on `:2024`. Thread ID is a URL query parameter (via `nuqs`). The hook supports tool approval interrupts via `resumeInterrupt(value)`.

## Configuration

| File | Purpose |
|------|---------|
| `langgraph.json` | Graph entry points mapping agent names to Python files |
| `.mcp.json` | MCP server registry (graphiti-aura, neo4j Docker/Aura) |
| `pyproject.toml` | Python dependencies (uv-managed) |
| `apps/web/package.json` | Frontend dependencies (yarn-managed) |

## Environment Variables

Required in `.env` (see `.env.example`):
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
- `LANGSMITH_API_KEY`, `LANGSMITH_TRACING`, `LANGSMITH_PROJECT`
- `BIOGRID_API_KEY`, `NCBI_API_KEY`
- `OPENAI_API_KEY` (in `.env.example`)
- `TAVILY_API_KEY`, `ANTHROPIC_API_KEY` (loaded at runtime, not in `.env.example`)

## Code Conventions

- Python: Type hints (TypedDict, Annotated), async/await for I/O, docstrings on tools (`parse_docstring=True`)
- TypeScript: `"use client"` directives, hook-based state, path aliasing (`@/*`)
- MCP tool timeouts vary by API reliability: 120s for ChEMBL, 60s for PubMed, 30s default

## Reference Materials

- `reference/competency_questions/` — Competency questions catalog and guidance for evaluating agent quality
- `reference/deepagents/` — DeepAgents library examples (content-builder, deep-research, text-to-sql, ralph-mode)
- `reference/prior-art-api-patterns.md` — Prior art patterns for life sciences API integration
- `reference/deep-agents-ui/` — Reference UI implementation (hooks, providers, components)
