#!/usr/bin/env python3
"""Test with detailed logging to see what persistence_specialist is doing."""

import requests
import json

API_BASE = "http://localhost:2024"
ASSISTANT_ID = "lifesciences"

# Create thread
response = requests.post(f"{API_BASE}/threads", json={})
thread_id = response.json()["thread_id"]
print(f"Thread: {thread_id}\n")

# Submit query
query = "What drugs target BRAF for melanoma?"
print(f"Query: {query}\n")

response = requests.post(
    f"{API_BASE}/threads/{thread_id}/runs",
    json={
        "assistant_id": ASSISTANT_ID,
        "input": {"messages": [{"role": "user", "content": query}]},
        "stream_mode": "messages"
    },
    stream=True
)

print("Streaming response...\n")
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode('utf-8').replace('data: ', ''))
            if isinstance(data, list) and len(data) > 0:
                msg = data[0]
                if 'content' in msg:
                    # Look for persistence_specialist activity
                    content_str = str(msg['content'])
                    if 'persistence' in content_str.lower():
                        print(f"\n🔍 Persistence specialist activity:")
                        print(json.dumps(msg, indent=2)[:500])

                    # Look for write_file tool calls
                    if 'write_file' in content_str.lower():
                        print(f"\n📝 write_file tool call detected!")
                        print(json.dumps(msg, indent=2))

                    # Look for tool calls in general
                    if 'tool_calls' in msg:
                        for tc in msg['tool_calls']:
                            print(f"\n🔧 Tool: {tc.get('name', 'unknown')}")
                            if tc.get('name') == 'write_file':
                                print(f"   Args: {tc.get('args', {})}")
        except:
            pass

print("\n\nDone. Check .deepagents/workspace/ for files.")
