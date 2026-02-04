# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Life Sciences Deep Agents Platform - A multi-agent system for biomedical research combining LangGraph-based agents with a shared React UI. Three specialized agents:
- **research**: Deep Research pattern with main agent + subagents
- **coding**: File-based workspace with virtual filesystem
- **lifesciences**: "Fuzzy-to-Fact" protocol for biological entity resolution (ANCHOR → ENRICH → EXPAND → TRAVERSE_DRUGS → TRAVERSE_TRIALS → VALIDATE → PERSIST)

## Commands

### Backend (Python with uv)
```bash
uv sync                    # Install dependencies
uv run langgraph dev       # Start backend on :2024
```

### Frontend (Node)
```bash
cd apps/web
npm install                # Install dependencies (or yarn)
npm run dev                # Dev server with Turbopack on :3000
npm run build              # Production build
npm run lint               # ESLint
npm run lint:fix           # ESLint with auto-fix
npm run format             # Prettier format
npm run format:check       # Check formatting
```

### Troubleshooting
```bash
fuser -k 2024/tcp          # Kill process on port 2024 if address in use
```

## Architecture

```
apps/
├── api/                   # LangGraph backend
│   ├── graphs/            # Agent definitions (research.py, coding.py, lifesciences.py)
│   └── shared/            # Shared modules
│       ├── mcp.py         # HTTP MCP Client for external APIs
│       ├── tools.py       # tavily_search, fetch_webpage_content, think_tool
│       └── prompts.py     # System prompts
└── web/                   # Next.js 16 frontend
    ├── components/        # React components (ChatInterface, ThreadList, ConfigDialog)
    ├── providers/         # ClientProvider (LangGraph), ChatProvider (state)
    └── lib/               # Utilities
```

### Key Patterns

**DeepAgents Pattern**: All three agents (research, coding, lifesciences) use `create_deep_agent()` with supervisor + subagents architecture. The lifesciences agent has 7 specialist subagents implementing the Fuzzy-to-Fact protocol phases.

**MCP Integration**: HTTPMCPClient uses JSON-RPC protocol. Two main bridges:
- `query_langchain_docs`: LangChain/LangGraph documentation
- `query_lifesciences`: ChEMBL, ClinicalTrials.gov, WikiPathways, HGNC, UniProt, STRING, BioGrid

**Agent Switching**: UI settings → Assistant ID field → set to `research`, `coding`, or `lifesciences`

## Configuration Files

| File | Purpose |
|------|---------|
| `langgraph.json` | Defines graph entry points (`research`, `coding`, `lifesciences`) |
| `.mcp.json` | MCP server registry (graphiti-aura, neo4j servers) |
| `pyproject.toml` | Python dependencies (uv-managed) |
| `apps/web/package.json` | Frontend dependencies and scripts |

## Environment Variables

Required in `.env` (see `.env.example`):
- NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
- TAVILY_API_KEY
- LANGSMITH_API_KEY
- ANTHROPIC_API_KEY, OPENAI_API_KEY

## Code Conventions

- Python: Type hints throughout (TypedDict, Annotated), async/await for I/O, docstrings on tools (parse_docstring=True)
- TypeScript: "use client" directives, hook-based state, type-safe props, path aliasing (@/*)
- Tools: Long timeouts for heavy operations (120s for ChEMBL queries)
