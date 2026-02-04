import sys
import os
from dotenv import load_dotenv

# Ensure we can import from shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from shared.tools import tavily_search, think_tool
from shared.mcp import query_langchain_docs, query_lifesciences
from shared.prompts import RESEARCHER_INSTRUCTIONS

load_dotenv()

def create_research_graph(model_name: str = "openai:gpt-4.1-mini"):
    """Create a deep research agent graph."""
    
    model = init_chat_model(model_name)
    current_date = datetime.now().strftime("%Y-%m-%d")

    agent = create_deep_agent(
        model=model,
        tools=[],
        system_prompt=f"""You are a deep research agent. Your job is to:

1. Break down complex research queries into sub-questions
2. Search for information on each sub-question
3. Synthesize findings into a comprehensive report
4. Cite your sources

You have a team of specialists to help you.
Today's date is {current_date}.""",
        subagents=[
            {
                "name": "search_specialist",
                "description": "Primary researcher. Executing 'tavily_search' for web results AND 'query_lifesciences' for direct API access to ClinicalTrials.gov, ChEMBL, and WikiPathways. Prefer asking for 'database queries' for medical topics.",
                "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
                "model": model_name,
                "tools": [tavily_search, think_tool, query_langchain_docs, query_lifesciences]
            },
            {
                "name": "synthesizer",
                "description": "Combines information from multiple sources into coherent summaries",
                "system_prompt": "You synthesize information clearly and cite sources. Review the markdown content provided by the search specialist and extract the key facts.",
                "model": model_name
            }
        ]
    )

    return agent

# Expose the graph for LangGraph
graph = create_research_graph()
