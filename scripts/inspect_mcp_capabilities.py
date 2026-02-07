
import asyncio
import httpx
import json

MCP_URL = "https://lifesciences-research.fastmcp.app/mcp"

async def list_tools():
    print(f"Connecting to {MCP_URL}...")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 1
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(MCP_URL, json=payload, headers=headers)
            response.raise_for_status()
            text = response.text
            
            # Simple SSE Parser
            data = None
            for line in text.split('\n'):
                if line.startswith("data: "):
                    try:
                        data = json.loads(line[6:].strip())
                        break
                    except:
                        continue
            
            if not data:
                 try:
                     data = json.loads(text)
                 except:
                     print("Failed to parse response:", text[:200])
                     return

            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
                print(f"\nFound {len(tools)} tools:")
                for tool in tools:
                    print(f"- {tool['name']}")
            else:
                print("Invalid response format:", data)
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(list_tools())
