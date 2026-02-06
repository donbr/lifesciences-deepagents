
import asyncio
import sys
import os

# Ensure we can import from apps
sys.path.append(os.getcwd())

from apps.api.shared.mcp import query_lifesciences

async def main():
    print("--- Verifying Generic MCP Wrapper ---")
    
    # Test Case: BioGRID Search (verify restored support)
    tool_name = "biogrid_search_genes"
    query = "TP53"
    
    print(f"Calling {tool_name} with query='{query}'...")
    
    try:
        # Note: query_lifesciences is a LangChain Tool, so we must use .ainvoke
        result = await query_lifesciences.ainvoke({"query": query, "tool_name": tool_name})
        print("\n--- Result ---")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        if "TP53" in result or "interaction_count" in result:
             print("\n✅ SUCCESS: Found TP53 in BioGRID")
        else:
             print("\n⚠️ WARNING: Did not find expected ID in output")
             
    except Exception as e:
        print(f"\n❌ FAILURE: {e}")

if __name__ == "__main__":
    asyncio.run(main())
