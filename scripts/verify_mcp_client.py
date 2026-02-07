
import asyncio
try:
    from mcp.client.sse import sse_client
    from mcp import ClientSession, InitializeRequest, ClientCapabilities
    print("mcp imported successfully")
except ImportError as e:
    print(f"Failed to import mcp: {e}")
    exit(1)

async def main():
    url = "https://pubmed.mcp.claude.com/mcp"
    print(f"Connecting to {url}...")
    try:
        async with sse_client(url) as (read, write):
            print("SSE connected.")
            async with ClientSession(read, write) as session:
                print("Session created. Initializing...")
                await session.initialize()
                print("Initialized!")
                
                print("Calling tool search_articles...")
                result = await session.call_tool("search_articles", {"query": "FOP", "max_results": 1})
                print("Result:", result)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
