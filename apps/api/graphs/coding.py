import sys
import os
from dotenv import load_dotenv

# Ensure we can import from shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from shared.tools import tavily_search, fetch_webpage_content
from shared.mcp import query_langchain_docs
from shared.prompts import DEVELOPER_SYSTEM_PROMPT

load_dotenv()

WORKSPACE_DIR = "coding_workspace"

def create_coding_graph(model_name: str = "anthropic:claude-sonnet-4-5-20250929"):
    """Create a coding agent graph."""
    
    # Initialize workspace
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)
        
    backend = FilesystemBackend(
        root_dir=WORKSPACE_DIR,
        virtual_mode=True
    )
    
    model = init_chat_model(model_name)

    agent = create_deep_agent(
        model=model,
        backend=backend,
        system_prompt=DEVELOPER_SYSTEM_PROMPT,
        tools=[tavily_search, fetch_webpage_content, query_langchain_docs],
    )

    return agent

# Expose the graph for LangGraph
graph = create_coding_graph()
