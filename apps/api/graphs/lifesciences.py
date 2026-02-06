"""
Life Sciences Graph Builder Agent - DeepAgents Pattern

Implements the 'Fuzzy-to-Fact' protocol using a supervisor with 7 specialist subagents:
1. ANCHOR: Resolve entities to CURIEs
2. ENRICH: Fetch metadata
3. EXPAND: Find connections/pathways
4. TRAVERSE_DRUGS: Find drugs matching targets
5. TRAVERSE_TRIALS: Find clinical trials
6. VALIDATE: Verify NCT IDs/mechanisms
7. PERSIST: Format final output
"""

import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Ensure we can import from shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from shared.mcp import query_lifesciences, query_api_direct, persist_to_graphiti, query_pubmed
from shared.tools import think_tool
from shared.prompts import (
    ANCHOR_SYSTEM,
    ENRICH_SYSTEM,
    EXPAND_SYSTEM,
    TRAVERSE_DRUGS_SYSTEM,
    TRAVERSE_TRIALS_SYSTEM,
    VALIDATE_SYSTEM,
    PERSIST_SYSTEM
)

load_dotenv()

def create_lifesciences_graph(model_name: str = "openai:gpt-4o"):
    """Create a life sciences deep agent graph using the Fuzzy-to-Fact protocol."""

    model = init_chat_model(model_name)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Supervisor system prompt with phase orchestration
    supervisor_system = f"""You are the Life Sciences Graph Builder Supervisor.
Your goal is to orchestrate the 'Fuzzy-to-Fact' protocol to answer user questions about biology and medicine.

Protocol Phases (execute sequentially):
1. ANCHOR: Identify entities and get CURIEs - delegate to anchor_specialist
2. ENRICH: Get metadata for those entities - delegate to enrichment_specialist
3. EXPAND: Find connections (interactions, pathways) - delegate to expansion_specialist
4. TRAVERSE_DRUGS: Find drugs matching targets - delegate to traversal_drugs_specialist
5. TRAVERSE_TRIALS: Find clinical trials for those drugs - delegate to traversal_trials_specialist
6. VALIDATE: Verify facts (IDs, mechanisms) - delegate to validation_specialist
7. PERSIST: Summarize and finalize - delegate to persistence_specialist

IMPORTANT: You MUST execute phases in order. Each phase builds on the previous phase's results.
- Pass the results from each phase to the next specialist
- Do not skip phases
- If a phase returns no results, note this and continue to the next phase

After all phases complete, provide a final summary to the user with:
- Resolved entities (CURIEs)
- Key metadata
- Interactions and pathways found
- Drug candidates
- Relevant clinical trials
- Validation status

Today's date is {current_date}.

STRICT ROUTING RULES:
- You must ONLY delegate to the subagents listed above.
- NEVER invent new subagents (like 'research-analyst' or 'general-purpose').
- Always start with 'anchor_specialist' for new queries.
- If the user asks a research question, map it to the 'anchor_specialist' first to identify the key entities."""

    # Note: We append think_tool to complex specialists
    agent = create_deep_agent(
        model=model,
        tools=[],  # Supervisor delegates, doesn't call tools directly
        system_prompt=supervisor_system,
        subagents=[
            {
                "name": "anchor_specialist",
                "description": "PHASE 1: Resolves fuzzy terms to canonical CURIEs (HGNC, CHEMBL, NCT). Use for identifying genes, drugs, and diseases. Can also search literature via PubMed.",
                "system_prompt": ANCHOR_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_pubmed, think_tool]
            },
            {
                "name": "enrichment_specialist",
                "description": "PHASE 2: Fetches detailed metadata for CURIEs. Gets UniProt/Ensembl IDs for genes, functions for proteins, Max Phase for drugs.",
                "system_prompt": ENRICH_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_pubmed, think_tool]
            },
            {
                "name": "expansion_specialist",
                "description": "PHASE 3: Finds biological connections. Gets STRING interactions, WikiPathways, BioGrid genetic interactions.",
                "system_prompt": EXPAND_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, think_tool]
            },
            {
                "name": "traversal_drugs_specialist",
                "description": "PHASE 4a: Identifies therapeutic targets and finds drugs that target them. Searches for approved drugs and inhibitors. Has fallback to Open Targets if ChEMBL fails.",
                "system_prompt": TRAVERSE_DRUGS_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_api_direct, think_tool]
            },
            {
                "name": "traversal_trials_specialist",
                "description": "PHASE 4b: Finds Clinical Trials for identified drugs. Combines drug names with disease context. Can use ClinicalTrials.gov v2 API directly.",
                "system_prompt": TRAVERSE_TRIALS_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_api_direct, think_tool]
            },
            {
                "name": "validation_specialist",
                "description": "PHASE 5: Verifies facts to prevent hallucinations. Validates NCT IDs and drug mechanisms. Can verify claims against PubMed literature.",
                "system_prompt": VALIDATE_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_pubmed, think_tool]
            },
            {
                "name": "persistence_specialist",
                "description": "PHASE 6: Formats validated knowledge graph, persists to Graphiti, and provides final summary.",
                "system_prompt": PERSIST_SYSTEM,
                "model": model_name,
                "tools": [persist_to_graphiti]
            }
        ]
    )

    return agent


# Expose the graph for LangGraph (langgraph.json compatibility)
graph = create_lifesciences_graph()
