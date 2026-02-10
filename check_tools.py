#!/usr/bin/env python3
"""Check what tools are actually available to subagents."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from apps.api.lifesciences import graph

print("Checking lifesciences agent configuration...\n")

# Get the agent configuration
config = graph.get_graph()

print(f"Graph nodes: {list(config.nodes.keys())}\n")

# Try to inspect the subagents
for node_name in config.nodes:
    print(f"Node: {node_name}")

print("\n" + "="*70)
print("Checking subagent configurations from source...")

# Read the source to see what tools each subagent has
with open('apps/api/lifesciences.py') as f:
    lines = f.readlines()
    in_subagent = False
    current_agent = None

    for i, line in enumerate(lines, 1):
        if '"name":' in line and 'specialist' in line:
            current_agent = line.strip().split('"')[3]
            in_subagent = True
            print(f"\n{current_agent}:")

        if in_subagent and '"tools":' in line:
            # Get the tools list
            tools_line = line.strip()
            print(f"  Line {i}: {tools_line}")

            if tools_line == '"tools": []':
                print(f"  ❌ NO TOOLS")
            else:
                print(f"  ✓ HAS TOOLS")

            in_subagent = False
