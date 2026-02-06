from langchain_core.tools import tool
import httpx
import json
import logging
import time
import asyncio
from collections import defaultdict
from typing import Optional, Any
import os

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter to prevent API throttling."""

    def __init__(self):
        self.last_call: dict[str, float] = defaultdict(float)
        # Seconds between calls per service
        self.limits = {
            "string": 1.0,      # STRING API: 1 req/s limit
            "chembl": 0.5,      # ChEMBL: be conservative
            "pubmed": 0.34,     # PubMed: ~3 req/s
            "entrez": 0.34,     # NCBI Entrez: 3 req/s
            "iuphar": 0.2,      # IUPHAR: fast
            "opentargets": 0.2, # OpenTargets: fast
            "pubchem": 0.5,     # PubChem: < 5 req/s
            "ensembl": 0.2,     # Ensembl: 15 req/s
            "biogrid": 0.5,     # BioGRID: 2 req/s
            "default": 0.1      # Default: 10 req/s
        }

    async def wait(self, service: str):
        """Wait if needed to respect rate limits."""
        limit = self.limits.get(service, self.limits["default"])
        elapsed = time.time() - self.last_call[service]
        if elapsed < limit:
            await asyncio.sleep(limit - elapsed)
        self.last_call[service] = time.time()

    def get_service_from_tool(self, tool_name: str) -> str:
        """Map tool name to service for rate limiting."""
        if tool_name.startswith("string_"):
            return "string"
        elif tool_name.startswith("chembl_"):
            return "chembl"
        elif tool_name.startswith("mcp_pubmed_") or tool_name.startswith("pubmed_"):
            return "pubmed"
        elif tool_name.startswith("entrez_"):
            return "entrez"
        elif tool_name.startswith("iuphar_"):
            return "iuphar"
        elif tool_name.startswith("opentargets_"):
            return "opentargets"
        elif tool_name.startswith("pubchem_"):
            return "pubchem"
        elif tool_name.startswith("ensembl_"):
            return "ensembl"
        elif tool_name.startswith("biogrid_"):
            return "biogrid"
        return "default"


rate_limiter = RateLimiter()


class HTTPMCPClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

    async def call_tool(self, tool_name: str, arguments: dict, apply_rate_limit: bool = True):
        # Apply rate limiting based on tool name
        if apply_rate_limit:
            service = rate_limiter.get_service_from_tool(tool_name)
            await rate_limiter.wait(service)

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 1
        }

        try:
            # Enable HTTP/2 as some servers (LangChain, FastMCP) prefer it
            async with httpx.AsyncClient(http2=True, verify=True, timeout=self.timeout) as client:
                response = await client.post(self.base_url, json=payload, headers=self.headers)
                response.raise_for_status()

                return self._parse_response(response.text)
        except httpx.HTTPStatusError as e:
            return f"HTTP Connection Error to MCP server: {e}"
        except Exception as e:
            return f"Error calling tool {tool_name}: {e}"

    def _parse_response(self, text: str):
        # Manual SSE Parsing attempt
        # The server might return "event: message\ndata: {...}" body even with json header
        for line in text.split('\n'):
            if line.startswith("data: "):
                json_str = line[6:].strip()
                try:
                    data = json.loads(json_str)
                    
                    # Process the JSON-RPC response
                    if "error" in data:
                        return f"Error from MCP server: {data['error']}"
                    
                    if "result" in data and "content" in data["result"]:
                        text_content = ""
                        for item in data["result"]["content"]:
                            if item.get("type") == "text":
                                text_content += item.get("text", "") + "\n"
                        return text_content.strip()
                        
                except json.JSONDecodeError:
                    continue
        
        # Fallback for standard JSON result
        try:
            data = json.loads(text)
            if "result" in data and "content" in data["result"]:
                text_content = ""
                for item in data["result"]["content"]:
                    if item.get("type") == "text":
                        text_content += item.get("text", "") + "\n"
                return text_content.strip()
        except:
            pass

        return f"No valid content found in response. Raw response start: {text[:200]}"

# --- Docs-LangChain MCP ---
DOCS_MCP_URL = "https://docs.langchain.com/mcp"
docs_client = HTTPMCPClient(DOCS_MCP_URL, timeout=30.0)

@tool
async def query_langchain_docs(query: str):
    """
    Search the official LangChain documentation. 
    Crucial for questions about:
    - LangChain, LangGraph, LangSmith
    - Deep Agents (the library/framework)
    - Middleware, Checkpointing, State Management
    - API references and Usage Guides
    """
    return await docs_client.call_tool("SearchDocsByLangChain", {"query": query})


# --- Life Sciences FastMCP ---
LIFESCIENCES_MCP_URL = "https://lifesciences-research.fastmcp.app/mcp"
# ChEMBL requires longer timeout (120s) as noted in documentation
lifesciences_client = HTTPMCPClient(LIFESCIENCES_MCP_URL, timeout=120.0)

@tool
async def query_lifesciences(
    query: str,
    tool_name: str = "clinicaltrials_search_trials",
    tool_args: Optional[dict[str, Any]] = None
):
    """
    Access biomedical databases via the Life Sciences MCP.
    Acts as a generic wrapper for ANY tool available on the Life Sciences MCP server.

    Common Tools & Argument Patterns:
    
    1. SEARCH Tools (Use 'query' argument or 'tool_args' for complex inputs)
       - clinicaltrials_search_trials: query (str)
       - chembl_search_compounds: query (str)
       - hgnc_search_genes: query (str)
       - uniprot_search_proteins: query (str)
       - string_search_proteins: query (str)
       - pubchem_search_compounds: query (str)
       - wikipathways_search_pathways: query (str)
       - iuphar_search_ligands: query (str)
       - iuphar_search_targets: query (str)
       - opentargets_search_targets: query (str)
       - entrez_search_genes: query (str)
       - ensembl_search_genes: query (str)
       - biogrid_search_genes: query (str)

    2. GET Tools (REQUIRE 'tool_args' with specific ID field)
       - clinicaltrials_get_trial: {"nct_id": "NCT..."}
       - chembl_get_compound: {"chembl_id": "CHEMBL..."}
       - hgnc_get_gene: {"hgnc_id": "HGNC:..."}
       - uniprot_get_protein: {"uniprot_id": "P12345"}
       - string_get_interactions: {"string_id": "...", "species": 9606}
       - pubchem_get_compound: {"pubchem_id": "PubChem:CID..."}
       - wikipathways_get_pathway: {"pathway_id": "WP..."}
       - iuphar_get_ligand: {"iuphar_id": "IUPHAR:..."}
       - iuphar_get_target: {"iuphar_id": "IUPHAR:..."}
       - opentargets_get_target: {"ensembl_id": "ENSG..."}
       - ensembl_get_gene: {"ensembl_id": "ENSG..."}
       - entrez_get_gene: {"entrez_id": "NCBIGene:..."}
       - biogrid_get_interactions: {"gene_symbol": "TP53"}

    Args:
        query: Search query (e.g., "aspirin", "TP53"). Used ONLY if tool_args is None.
        tool_name: The EXACT name of the MCP tool to call (e.g. 'iuphar_search_ligands').
        tool_args: Dictionary of arguments. REQUIRED for 'get_*' tools that don't take a 'query'.
                   Example: {"nct_id": "NCT00001"} OR {"query": "aspirin", "approved_only": True}
    """
    # Use tool_args if provided, otherwise fall back to simple query
    args = tool_args if tool_args else {"query": query}
    return await lifesciences_client.call_tool(tool_name, args)


# --- PubMed MCP ---
PUBMED_MCP_URL = os.environ.get("PUBMED_MCP_URL", "https://pubmed-research.fastmcp.app/mcp")
pubmed_client = HTTPMCPClient(PUBMED_MCP_URL, timeout=60.0)

@tool
async def query_pubmed(
    tool_name: str,
    tool_args: dict[str, Any]
):
    """
    Access biomedical literature via the PubMed MCP.

    Supported tools:
    - mcp_pubmed_search_articles: query (str), max_results (int)
    - mcp_pubmed_get_article_metadata: pmids (list[str])
    - mcp_pubmed_get_full_text_article: pmc_ids (list[str])

    Args:
        tool_name: The MCP tool to call (e.g., 'mcp_pubmed_search_articles')
        tool_args: Dictionary of arguments for the tool
    """
    return await pubmed_client.call_tool(tool_name, tool_args)


# --- Direct API Access (Fallback) ---

@tool
async def query_api_direct(
    url: str,
    method: str = "GET",
    body: Optional[str] = None,
    headers: Optional[dict[str, str]] = None
):
    """
    Direct API access for when MCP tools fail or are unavailable.

    Use this as a fallback when:
    - ChEMBL returns 500 errors (use Open Targets GraphQL instead)
    - You need to access APIs not covered by the MCP
    - You need full control over request parameters

    Common fallback patterns:
    1. Open Targets GraphQL (replaces broken ChEMBL):
       url: "https://api.platform.opentargets.org/api/v4/graphql"
       method: "POST"
       body: '{"query": "{ target(ensemblId: \"ENSG00000115170\") { ... } }"}'

    2. HGNC Gene Resolution:
       url: "https://rest.genenames.org/fetch/symbol/ACVR1"

    3. ClinicalTrials.gov v2:
       url: "https://clinicaltrials.gov/api/v2/studies?query.cond=FOP&pageSize=10&format=json"

    Args:
        url: Full URL to fetch
        method: HTTP method (GET or POST)
        body: Request body for POST requests (JSON string)
        headers: Optional additional headers
    """
    default_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if headers:
        default_headers.update(headers)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method.upper() == "POST":
                response = await client.post(url, content=body, headers=default_headers)
            else:
                response = await client.get(url, headers=default_headers)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        return f"HTTP Error {e.response.status_code}: {e}"
    except Exception as e:
        return f"Error fetching {url}: {e}"


# --- Graphiti Persistence ---

# Graphiti MCP client (connects to local Graphiti server)
GRAPHITI_MCP_URL = "http://localhost:8000/mcp"
graphiti_client = HTTPMCPClient(GRAPHITI_MCP_URL, timeout=30.0)


@tool
async def persist_to_graphiti(
    name: str,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    group_id: str = "lifesciences-default"
):
    """
    Persist validated knowledge graph to Graphiti memory.

    Use this in the PERSIST phase to save the validated knowledge graph.
    Graphiti will extract entities and relationships from the JSON structure.

    Args:
        name: Descriptive name for this episode (e.g., "FOP Drug Repurposing Graph")
        nodes: List of node dicts with keys: id, type, label, properties
               Example: [{"id": "HGNC:171", "type": "Gene", "label": "ACVR1", "properties": {...}}]
        edges: List of edge dicts with keys: source, target, type, properties
               Example: [{"source": "HGNC:171", "target": "CHEMBL:1234", "type": "TARGETS", ...}]
        group_id: Namespace for this graph (default: "lifesciences-default")

    Returns:
        Confirmation message from Graphiti
    """
    episode_body = json.dumps({
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "created_by": "lifesciences-agent",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    })

    try:
        return await graphiti_client.call_tool(
            "add_memory",
            {
                "name": name,
                "episode_body": episode_body,
                "source": "json",
                "source_description": "Life Sciences Graph Builder validated output",
                "group_id": group_id
            },
            apply_rate_limit=False  # Graphiti doesn't need rate limiting
        )
    except Exception as e:
        # Graceful fallback if Graphiti is unavailable
        logger.warning(f"Graphiti persistence failed: {e}")
        return f"Note: Graphiti persistence unavailable ({e}). Graph data preserved in response."
