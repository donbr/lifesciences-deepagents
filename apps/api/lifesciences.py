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

LangGraph server entrypoint. The agent definition lives in ``agent_factory`` so
the Temporal host (``apps/temporal``) can build the same agent without I/O.
"""

import os
import sys
import logging

from dotenv import load_dotenv

# Ensure we can import from shared
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain.chat_models import init_chat_model
from agent_factory import DEFAULT_MODEL, build_lifesciences_agent, resolve_agent_config

load_dotenv()
logger = logging.getLogger(__name__)


# anthropic:claude-sonnet-4-5
# openai:gpt-4o"
def create_lifesciences_graph(model_name: str = DEFAULT_MODEL):
    """Create a life sciences deep agent graph using the Fuzzy-to-Fact protocol."""
    config = resolve_agent_config(model_name)
    logger.info(
        "Lifesciences knowledge config: runtime_root=%s memory_enabled=%s skills_source=%s",
        config.runtime_root,
        bool(config.memory_paths),
        config.skills_source,
    )
    return build_lifesciences_agent(config, model=init_chat_model(model_name))


# Expose the graph for LangGraph (langgraph.json compatibility)
graph = create_lifesciences_graph()
