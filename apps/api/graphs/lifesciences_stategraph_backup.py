from typing import Annotated, TypedDict, List, Dict, Any, Union
import json
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from apps.api.shared.mcp import query_lifesciences

# --- State Definition ---

class GraphState(TypedDict):
    """
    State for the Life Sciences Graph Builder Agent.
    Tracks the progression through the 5-phase 'Fuzzy-to-Fact' protocol.
    """
    messages: Annotated[List[BaseMessage], operator.add]
    question: str
    
    # Phase Results (Accumulated State)
    anchor_results: Dict[str, Any]      # Phase 1: Canonical CURIEs (HGNC:1100, CHEMBL:25)
    enrichment_data: Dict[str, Any]     # Phase 2: Metadata (UniProt Function, Targets)
    expansion_graph: Dict[str, Any]     # Phase 3: Interactions (STRING edges, Pathways)
    traversal_paths: Dict[str, Any]     # Phase 4: Druggable Targets / Indications
    validation_report: Dict[str, Any]   # Phase 5: Error checks (NCT IDs, Mechanisms)
    
    current_phase: str
    errors: List[str]

# --- Tools Setup ---

# We only have one "meta-tool" that bridges to the FastMCP server.
# The agent will call this with specific 'tool_name' arguments.
tools = [query_lifesciences]

# LLM Setup
llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# --- Prompts ---

ANCHOR_SYSTEM = """You are the ANCHOR specialist of the Life Sciences Graph Builder.
Goal: Resolve all biological entities (Genes, Drugs, Diseases) in the user's question to canonical CURIEs.

Protocol (Fuzzy-to-Fact Phase 1):
1. Identify every gene, drug, or disease mentioned.
2. Use `query_lifesciences` to search for them:
   - Genes: Use tool `hgnc_search_genes` (or `search_genes`)
   - Drugs: Use tool `chembl_search_compounds` (or `search_compounds`)
   - Trials: Use tool `clinicaltrials_search_trials`
3. Select the best matching CURIE (e.g., HGNC:11998, CHEMBL:25).

Your final answer must be a JSON summary of the resolved entities.
"""

ENRICH_SYSTEM = """You are the ENRICHMENT specialist.
Goal: Fetch detailed metadata for the CURIEs identified in the Anchor phase.

Protocol (Phase 2):
1. For each Gene CURIE (HGNC:...), call `hgnc_get_gene` to get UniProt/Ensembl IDs.
2. For each Protein (UniProt:...), call `uniprot_get_protein` to get function/subcellular location.
3. For each Drug (CHEMBL:...), call `chembl_get_compound` to get Max Phase and indications.
"""

EXPAND_SYSTEM = """You are the NETWORK EXPANSION specialist.
Goal: Find biological connections (interactions, pathways) for the enriched nodes.

Protocol (Phase 3):
1. For Proteins: First resolve to STRING ID if needed using `string_search_proteins` with the gene symbol. Then use `string_get_interactions` with the STRING ID (e.g., '9606.ENSP...'). 
   - DO NOT pass a gene name to `string_get_interactions`. You must find the ID first.
2. For Pathways: Use `wikipathways_get_pathways_for_gene` with the HGNC ID or Gene Symbol.
3. For Genetic Interactions: Use `biogrid_get_interactions`.
   - ARGUMENTS: `tool_name="biogrid_get_interactions"`, `tool_args={"gene_symbol": "TP53"}`
   - DO NOT use "query". The key inside tool_args MUST be "gene_symbol".
"""

TRAVERSE_DRUGS_SYSTEM = """You are the TRAVERSAL (DRUGS) specialist.
Goal: Identify therapeutic targets and find drugs that target them.

Protocol (Phase 4a):
1. Identify the key targets from the expanded graph (Phase 3).
2. For each target, search for approved drugs or inhibitors using `chembl_search_compounds` (search for 'inhibitor of [target]') or by looking up the target's cross-references if available.
3. Return a list of specific drug names found (e.g., 'Crizotinib', 'Pemetrexed').
"""

TRAVERSE_TRIALS_SYSTEM = """You are the TRAVERSAL (TRIALS) specialist.
Goal: Find Clinical Trials using the specific drug names identified in the previous phase.

Protocol (Phase 4b):
1. Use the specific drug names found in Phase 4a (Traverse Drugs).
2. Search for Clinical Trials (`clinicaltrials_search_trials`) combining the Drug Name + Disease Context (from the original question).
   - "Pemetrexed AND NSCLC"
   - "Crizotinib AND ALK-positive"
3. Do NOT use broad terms like "Inhibitor" in the search; use the specific drug names.
"""

# ... (Validation and Persist prompts remain similar)

VALIDATE_SYSTEM = """You are the VALIDATION specialist.
Goal: Verify specific facts to prevent hallucinations.

Protocol (Phase 5):
1. Verify every NCT ID found using `clinicaltrials_get_trial`. If it returns 'Entity Not Found', it is an error.
2. Check if the drugs found actually have the mechanism claimed.
"""

PERSIST_SYSTEM = """You are the PERSISTENCE specialist.
Goal: Format the validated graph and save it.

Protocol (Phase 6):
1. Summarize the answer seamlessly.
2. explicitly list the VALIDATED facts (e.g., "Validated Trial: NCT12345").
"""

# --- Nodes Implementation ---

def _call_model(state: GraphState, system_prompt: str, phase_name: str):
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system_prompt)] + messages
    else:
        # Update system prompt for the new phase
        messages[0] = SystemMessage(content=system_prompt)
    
    response = llm.invoke(messages)
    return {
        "messages": [response],
        "current_phase": phase_name
    }

def anchor_node(state: GraphState):
    return _call_model(state, ANCHOR_SYSTEM, "ANCHOR")

def enrich_node(state: GraphState):
    return _call_model(state, ENRICH_SYSTEM, "ENRICH")

def expand_node(state: GraphState):
    return _call_model(state, EXPAND_SYSTEM, "EXPAND")

def traverse_drugs_node(state: GraphState):
    return _call_model(state, TRAVERSE_DRUGS_SYSTEM, "TRAVERSE_DRUGS")

def traverse_trials_node(state: GraphState):
    return _call_model(state, TRAVERSE_TRIALS_SYSTEM, "TRAVERSE_TRIALS")

def validate_node(state: GraphState):
    return _call_model(state, VALIDATE_SYSTEM, "VALIDATE")

def persist_node(state: GraphState):
    return _call_model(state, PERSIST_SYSTEM, "PERSIST")

# --- Routing Logic ---

def should_continue(state: GraphState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "next_phase"

def get_next_phase(phase):
    order = ["ANCHOR", "ENRICH", "EXPAND", "TRAVERSE_DRUGS", "TRAVERSE_TRIALS", "VALIDATE", "PERSIST", END]
    try:
        idx = order.index(phase)
        return order[idx + 1].lower() if idx + 1 < len(order) else END
    except ValueError:
        return END

def router(state: GraphState):
    if state["messages"][-1].tool_calls:
        return "tools"
    
    current = state.get("current_phase", "ANCHOR")
    if current == "ANCHOR": return "enrich"
    if current == "ENRICH": return "expand"
    if current == "EXPAND": return "traverse_drugs"
    if current == "TRAVERSE_DRUGS": return "traverse_trials"
    if current == "TRAVERSE_TRIALS": return "validate"
    if current == "VALIDATE": return "persist"
    return END

# --- Graph Construction ---

graph_builder = StateGraph(GraphState)

graph_builder.add_node("anchor", anchor_node)
graph_builder.add_node("enrich", enrich_node)
graph_builder.add_node("expand", expand_node)
graph_builder.add_node("traverse_drugs", traverse_drugs_node)
graph_builder.add_node("traverse_trials", traverse_trials_node)
graph_builder.add_node("validate", validate_node)
graph_builder.add_node("persist", persist_node)
graph_builder.add_node("tools", ToolNode(tools))

# Edges
graph_builder.add_edge(START, "anchor")

# For each node, either go to tools or next phase
for node in ["anchor", "enrich", "expand", "traverse_drugs", "traverse_trials", "validate"]:
    graph_builder.add_conditional_edges(
        node,
        should_continue,
        {
            "tools": "tools",
            "next_phase": get_next_phase(node.upper())
        }
    )

def return_to_sender(state: GraphState):
    phase = state.get("current_phase", "ANCHOR").lower()
    return phase

graph_builder.add_conditional_edges(
    "tools",
    return_to_sender,
    {
        "anchor": "anchor",
        "enrich": "enrich",
        "expand": "expand",
        "traverse_drugs": "traverse_drugs",
        "traverse_trials": "traverse_trials",
        "validate": "validate",
        "persist": "persist" 
    }
)

graph_builder.add_edge("persist", END)

# Compile
graph = graph_builder.compile()
