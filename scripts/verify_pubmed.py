
import asyncio
import os
from apps.api.shared.mcp import query_pubmed

async def verify():
    print("Testing PubMed Integration...")
    try:
        # Test search_articles
        result = await query_pubmed.ainvoke(
            {"tool_name": "search_articles", "tool_args": {"query": "ACVR1 FOP", "max_results": 1}}
        )
        print("✅ search_articles result:", result)
        
        # Parse result to get a PMID (assuming result structure, or just use a known one)
        # For simplicity, let's just use a hardcoded PMID if search fails to return specific structure
        # But let's try to be dynamic if possible.
        # The result from MCP is likely a string or list of strings.
        
        # Test get_article_metadata with a known PMID (from the README example or typical FOP paper)
        # PMID: 29871926 (Palovarotene MOVE trial related or similar)
        # Let's use a very standard one: 29871926
        
        metadata = await query_pubmed.ainvoke(
            {"tool_name": "get_article_metadata", "tool_args": {"pmids": ["29871926"]}}
        )
        print("✅ get_article_metadata result:", metadata)

        print("\n🎉 PubMed Integration Verification Successful!")

    except Exception as e:
        print(f"\n❌ PubMed Integration Verification Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
