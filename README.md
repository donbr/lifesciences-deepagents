# DeepAgents Platform

A unified platform for running multiple Deep Agents (Research, Coding) with a shared React UI.

## Directory Structure

- **apps/api**: The LangGraph backend server.
  - `graphs/`: Definitions for different agents (`research.py`, `coding.py`).
  - `shared/`: Shared tools (VFS, Search) and prompts.
- **apps/web**: The Next.js Agent Chat UI.
  - Adapted to support dynamic switching between agents.

## Quickstart

### 1. Start the Backend API

**Best Practice**: Use `uv run` to ensure you are using the correct dependencies, ignoring any globally active virtual environments.

```bash
# Install dependencies
uv sync

# Start the server (handles virtual env automatically)
uv run langgraph dev
```
This serves the API at `http://localhost:2024`.

> **Note on Warnings**: If you see `warning: VIRTUAL_ENV=... does not match`, it just means you have a different virtual env active in your shell. `uv run` will safely ignore it and use the project's correct environment.

### 2. Start the Frontend UI

```bash
cd apps/web
npm install
npm run dev
```
Open `http://localhost:3000`.

## How to Switch Agents

In the UI:
1. Click the **Settings** icon.
2. In **Agent config**, set the **Assistant ID** (or Graph ID) to:
   - `research` (for the Deep Research Agent)
   - `coding` (for the Coding Agent)
   - `lifesciences` (for the Life Sciences Graph Builder)
3. Click Save.

## Troubleshooting

### "Server not running" or Port Conflicts
If `langgraph dev` fails saying address in use:
```bash
# Kill whatever is on port 2024
fuser -k 2024/tcp
# Restart
uv run langgraph dev
```
