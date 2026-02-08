#!/usr/bin/env python3
"""Test artifact generation with persistence_specialist."""

import requests
import json
import time
import os
from pathlib import Path

# LangGraph API endpoint
API_BASE = "http://localhost:2024"
ASSISTANT_ID = "lifesciences"

def test_artifact_generation():
    """Test that persistence_specialist generates graph.json artifact."""

    print("🧪 Testing artifact generation with lifesciences assistant\n")

    # 1. Create a thread
    print("1️⃣ Creating thread...")
    response = requests.post(f"{API_BASE}/threads", json={})
    thread_id = response.json()["thread_id"]
    print(f"   ✓ Thread created: {thread_id}\n")

    # 2. Submit test query
    print("2️⃣ Submitting test query...")
    query = "What is the mechanism of Palovarotene for FOP?"

    response = requests.post(
        f"{API_BASE}/threads/{thread_id}/runs",
        json={
            "assistant_id": ASSISTANT_ID,
            "input": {"messages": [{"role": "user", "content": query}]},
            "stream_mode": "values"
        },
        stream=True
    )

    print(f"   Query: {query}")
    print(f"   Waiting for agent to complete...\n")

    # 3. Stream response and look for completion
    last_message = None
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode('utf-8').replace('data: ', ''))
                if 'messages' in data:
                    last_message = data['messages'][-1] if data['messages'] else None
            except:
                pass

    print("   ✓ Agent completed\n")

    # 4. Check for artifacts
    print("3️⃣ Checking for generated artifacts...")
    workspace_dir = Path(".deepagents/workspace")

    if not workspace_dir.exists():
        print(f"   ❌ Workspace directory does not exist: {workspace_dir}")
        return False

    print(f"   ✓ Workspace exists: {workspace_dir}")

    # List all files in workspace
    files = list(workspace_dir.glob("*"))
    if not files:
        print(f"   ❌ No files found in workspace")
        return False

    print(f"   📁 Files found ({len(files)}):")
    for f in files:
        size = f.stat().st_size
        print(f"      - {f.name} ({size} bytes)")

    # Check for graph.json specifically
    graph_json = workspace_dir / "graph.json"
    if graph_json.exists():
        print(f"\n   ✅ graph.json generated successfully!")
        print(f"      Size: {graph_json.stat().st_size} bytes")

        # Validate it's valid JSON
        try:
            with open(graph_json) as f:
                data = json.load(f)
            print(f"      Valid JSON: ✓")

            if 'nodes' in data:
                print(f"      Nodes: {len(data['nodes'])}")
            if 'edges' in data:
                print(f"      Edges: {len(data['edges'])}")

            return True
        except json.JSONDecodeError as e:
            print(f"      ❌ Invalid JSON: {e}")
            return False
    else:
        print(f"\n   ❌ graph.json NOT found")
        print(f"      Expected: {graph_json}")
        return False

if __name__ == "__main__":
    success = test_artifact_generation()

    print("\n" + "="*70)
    if success:
        print("✅ TEST PASSED: Artifact generation working")
    else:
        print("❌ TEST FAILED: No artifacts generated")
    print("="*70)

    exit(0 if success else 1)
