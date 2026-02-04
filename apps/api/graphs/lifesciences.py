"""
Life Sciences Graph Builder Agent - DeepAgents Pattern

Implements the 'Fuzzy-to-Fact' protocol using a supervisor with 7 specialist subagents:
1. ANCHOR: Resolve entities to CURIEs
2. ENRICH: Fetch metadata
3. EXPAND: Find connections/pathways
4. TRAVERSE_DRUGS: Find targeting drugs
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
from shared.mcp import query_lifesciences, query_api_direct, persist_to_graphiti

load_dotenv()

# --- Phase System Prompts ---

ANCHOR_SYSTEM = """You are the ANCHOR specialist of the Life Sciences Graph Builder.
Goal: Resolve all biological entities (Genes, Drugs, Diseases) in the user's question to canonical CURIEs.

Protocol (Fuzzy-to-Fact Phase 1):
1. Identify every gene, drug, or disease mentioned.
2. Use `query_lifesciences` to search for them:
   - Genes: query_lifesciences(query="ACVR1", tool_name="hgnc_search_genes")
   - Drugs: query_lifesciences(query="Imatinib", tool_name="chembl_search_compounds")
   - Trials: query_lifesciences(query="NSCLC", tool_name="clinicaltrials_search_trials")
3. Select the best matching CURIE (e.g., HGNC:171, CHEMBL:25).

IMPORTANT: HGNC is the fastest and most reliable for gene resolution. Start there.

Your final answer must be a JSON summary of the resolved entities.
"""

ENRICH_SYSTEM = """You are the ENRICHMENT specialist.
Goal: Fetch detailed metadata for the CURIEs identified in the Anchor phase.

Protocol (Phase 2):
1. For each Gene CURIE (HGNC:...):
   query_lifesciences(query="", tool_name="hgnc_get_gene", tool_args={"hgnc_id": "HGNC:171"})
   -> Returns UniProt ID, Ensembl ID, gene name

2. For each Protein (UniProt:...):
   query_lifesciences(query="", tool_name="uniprot_get_protein", tool_args={"uniprot_id": "Q04771"})
   -> Returns function, subcellular location, disease associations

3. For each Drug (CHEMBL:...):
   query_lifesciences(query="", tool_name="chembl_get_compound", tool_args={"chembl_id": "CHEMBL25"})
   -> Returns Max Phase, indications, mechanism

IMPORTANT: UniProt function descriptions are highly valuable for understanding target biology.
"""

EXPAND_SYSTEM = """You are the NETWORK EXPANSION specialist.
Goal: Find biological connections (interactions, pathways) for the enriched nodes.

Protocol (Phase 3):

1. For STRING Protein Interactions (PREFERRED - batch queries return protein names):
   # First search for STRING ID
   query_lifesciences(query="ACVR1", tool_name="string_search_proteins", tool_args={"query": "ACVR1", "species": 9606})
   # Then get interactions with the STRING ID
   query_lifesciences(query="", tool_name="string_get_interactions", tool_args={"string_id": "9606.ENSP00000263640", "species": 9606, "required_score": 700})

2. For Pathways:
   query_lifesciences(query="", tool_name="wikipathways_get_pathways_for_gene", tool_args={"gene_id": "ACVR1"})

3. For Genetic Interactions (BioGrid):
   query_lifesciences(query="", tool_name="biogrid_get_interactions", tool_args={"gene_symbol": "ACVR1"})

TIP: STRING batch queries (multiple proteins at once) return protein names; single queries may not.
"""

TRAVERSE_DRUGS_SYSTEM = """You are the TRAVERSAL (DRUGS) specialist.
Goal: Identify therapeutic targets and find drugs that target them.

Protocol (Phase 4a):

1. Try ChEMBL first:
   query_lifesciences(query="ACVR1 inhibitor", tool_name="chembl_search_compounds")

2. If ChEMBL returns errors (500s are common), use Open Targets GraphQL as fallback:
   query_api_direct(
       url="https://api.platform.opentargets.org/api/v4/graphql",
       method="POST",
       body='{"query": "{ target(ensemblId: \\"ENSG00000115170\\") { knownDrugs(size:10) { rows { drug { name } mechanismOfAction phase } } } }"}'
   )

3. Return a list of specific drug names found (e.g., 'Palovarotene', 'Garetosmab').

IMPORTANT: Open Targets is more reliable than ChEMBL and returns drugs + mechanisms + phases in one call.
"""

TRAVERSE_TRIALS_SYSTEM = """You are the TRAVERSAL (TRIALS) specialist.
Goal: Find Clinical Trials using the specific drug names identified in the previous phase.

Protocol (Phase 4b):

1. Using MCP tool:
   query_lifesciences(query="Palovarotene AND fibrodysplasia ossificans progressiva", tool_name="clinicaltrials_search_trials")

2. Or use ClinicalTrials.gov v2 API directly for more control:
   query_api_direct(
       url="https://clinicaltrials.gov/api/v2/studies?query.cond=fibrodysplasia+ossificans+progressiva&query.intr=Palovarotene&pageSize=10&format=json"
   )

3. Combine Drug Name + Disease Context from the original question.
   - "Palovarotene AND FOP"
   - "Garetosmab AND heterotopic ossification"

IMPORTANT: Use specific drug names, NOT broad terms like "inhibitor".
"""

VALIDATE_SYSTEM = """You are the VALIDATION specialist.
Goal: Verify specific facts to prevent hallucinations.

Protocol (Phase 5):

1. Verify every NCT ID found:
   query_lifesciences(query="", tool_name="clinicaltrials_get_trial", tool_args={"nct_id": "NCT03312634"})
   -> If it returns 'Entity Not Found', mark as INVALID

2. Check drug mechanisms match claims:
   query_lifesciences(query="", tool_name="chembl_get_compound", tool_args={"chembl_id": "CHEMBL1234"})
   -> Verify mechanism of action matches what was claimed

3. Mark each fact as VALIDATED or INVALID with reason.
"""

PERSIST_SYSTEM = """You are the PERSISTENCE specialist.
Goal: Format the validated graph, save it to Graphiti, and provide final summary.

Protocol (Phase 6):

1. Structure the validated knowledge as nodes and edges:
   nodes = [
       {"id": "HGNC:171", "type": "Gene", "label": "ACVR1", "properties": {"function": "..."}},
       {"id": "CHEMBL:...", "type": "Drug", "label": "Palovarotene", "properties": {"phase": 3}}
   ]
   edges = [
       {"source": "CHEMBL:...", "target": "HGNC:171", "type": "TARGETS", "properties": {"mechanism": "..."}}
   ]

2. Persist to Graphiti:
   persist_to_graphiti(
       name="FOP Drug Repurposing Graph",
       nodes=nodes,
       edges=edges,
       group_id="fop-drug-repurposing"
   )

3. Summarize the answer with:
   - Resolved entities (CURIEs)
   - Key validated facts
   - Clinical trials with NCT IDs
   - Confidence levels based on validation results
"""


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

Today's date is {current_date}."""

    agent = create_deep_agent(
        model=model,
        tools=[],  # Supervisor delegates, doesn't call tools directly
        system_prompt=supervisor_system,
        subagents=[
            {
                "name": "anchor_specialist",
                "description": "PHASE 1: Resolves fuzzy terms to canonical CURIEs (HGNC, CHEMBL, NCT). Use for identifying genes, drugs, and diseases.",
                "system_prompt": ANCHOR_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences]
            },
            {
                "name": "enrichment_specialist",
                "description": "PHASE 2: Fetches detailed metadata for CURIEs. Gets UniProt/Ensembl IDs for genes, functions for proteins, Max Phase for drugs.",
                "system_prompt": ENRICH_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences]
            },
            {
                "name": "expansion_specialist",
                "description": "PHASE 3: Finds biological connections. Gets STRING interactions, WikiPathways, BioGrid genetic interactions.",
                "system_prompt": EXPAND_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences]
            },
            {
                "name": "traversal_drugs_specialist",
                "description": "PHASE 4a: Identifies therapeutic targets and finds drugs that target them. Searches for approved drugs and inhibitors. Has fallback to Open Targets if ChEMBL fails.",
                "system_prompt": TRAVERSE_DRUGS_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_api_direct]
            },
            {
                "name": "traversal_trials_specialist",
                "description": "PHASE 4b: Finds Clinical Trials for identified drugs. Combines drug names with disease context. Can use ClinicalTrials.gov v2 API directly.",
                "system_prompt": TRAVERSE_TRIALS_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences, query_api_direct]
            },
            {
                "name": "validation_specialist",
                "description": "PHASE 5: Verifies facts to prevent hallucinations. Validates NCT IDs and drug mechanisms.",
                "system_prompt": VALIDATE_SYSTEM,
                "model": model_name,
                "tools": [query_lifesciences]
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
