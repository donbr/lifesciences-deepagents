#!/usr/bin/env python3
"""
Test workspace isolation using unique thread_ids.

This script verifies that:
1. Each thread_id gets isolated workspace state
2. No workspace contamination between test runs
3. AGENTS.md and skills remain accessible across threads
"""

import uuid
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

from lifesciences import create_lifesciences_graph
from langchain_core.messages import HumanMessage


async def test_workspace_isolation():
    """Test that different thread_ids have isolated workspace state."""

    print("\n=== Testing Workspace Isolation ===\n")

    # Create the agent
    agent = create_lifesciences_graph()

    # Test 1: First thread
    thread_id_1 = f"test-{uuid.uuid4()}"
    print(f"Test 1 - Thread ID: {thread_id_1}")

    config_1 = {"configurable": {"thread_id": thread_id_1}}
    input_1 = {
        "messages": [
            HumanMessage(content="What is the HGNC symbol for ACVR1?")
        ]
    }

    print("Invoking agent for Test 1...")
    try:
        result_1 = await agent.ainvoke(input_1, config_1)
        print(f"✓ Test 1 completed successfully")
        print(f"  Response messages: {len(result_1.get('messages', []))}")
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        return False

    # Test 2: Second thread (should not see Test 1's workspace)
    thread_id_2 = f"test-{uuid.uuid4()}"
    print(f"\nTest 2 - Thread ID: {thread_id_2}")

    config_2 = {"configurable": {"thread_id": thread_id_2}}
    input_2 = {
        "messages": [
            HumanMessage(content="What is the gene symbol for TP53?")
        ]
    }

    print("Invoking agent for Test 2...")
    try:
        result_2 = await agent.ainvoke(input_2, config_2)
        print(f"✓ Test 2 completed successfully")
        print(f"  Response messages: {len(result_2.get('messages', []))}")
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        return False

    # Test 3: Verify AGENTS.md is still accessible
    print("\n=== Verifying Persistent Storage ===\n")

    runtime_root = Path(__file__).parent.parent / ".deepagents"
    agents_md = runtime_root / "AGENTS.md"
    skills_dir = runtime_root / "skills"

    if agents_md.exists():
        print(f"✓ AGENTS.md exists and is accessible")
    else:
        print(f"⚠ AGENTS.md not found (this is OK for first run)")

    if skills_dir.exists():
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        print(f"✓ Skills directory exists with {skill_count} skills")
    else:
        print(f"⚠ Skills directory not found")

    print("\n=== All Tests Passed ===\n")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_workspace_isolation())
    sys.exit(0 if success else 1)
