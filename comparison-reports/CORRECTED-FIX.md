# CORRECTED FIX: DeepAgents File Creation Issue

**Date**: 2026-02-09
**Source**: LangChain Documentation via docs-langchain MCP server

---

## Original (Incorrect) Diagnosis

**What I initially said** (in SKILL-VS-DEEPAGENTS.md and ANALYSIS.md):

> "Specialists lack `write_file` tool. Fix: Add `write_file` to specialist tool lists in lifesciences.py"

**This was WRONG.**

---

## Correct Diagnosis (from LangChain Docs)

### Key Findings from Documentation

1. **FilesystemMiddleware is automatically included**:
   > "When you create a deep agent with `create_deep_agent`, we **automatically attach** TodoListMiddleware, FilesystemMiddleware, and SubAgentMiddleware to your agent."

   [Source: Agent harness capabilities](https://docs.langchain.com/oss/python/deepagents/harness)

2. **FilesystemMiddleware provides `write_file` tool**:
   > "FilesystemMiddleware from deep agents provides four tools for interacting with both short-term and long-term memory: `ls`, `read_file`, **`write_file`**, `edit_file`"

   [Source: Filesystem middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

3. **Subagents inherit filesystem tools by default**:
   > "Default subagent: 'general-purpose' subagent automatically available. **Has filesystem tools by default**"

   [Source: Task delegation](https://docs.langchain.com/oss/python/deepagents/harness)

**Conclusion**: The specialists **ALREADY HAVE** the `write_file` tool. My original fix was incorrect.

---

## The Real Issue: StateBackend vs FilesystemBackend

### What's Actually Happening

**Default backend** (from docs):
```python
# By default we provide a StateBackend
agent = create_deep_agent()

# Under the hood, it looks like
from deepagents.backends import StateBackend

agent = create_deep_agent(
    backend=(lambda rt: StateBackend(rt))
)
```

[Source: StateBackend](https://docs.langchain.com/oss/python/deepagents/customization)

### StateBackend Behavior

> "An ephemeral filesystem backend stored in langgraph state. **This filesystem only persists for a single thread**."

> "Files live in the agent's state (checkpointed with conversation). **Persists within a thread but not across threads**."

> "By default, these tools write to a local 'filesystem' in your graph state."

[Source: Pluggable storage backends](https://docs.langchain.com/oss/python/deepagents/harness)

**Key insight**: Files ARE being created, but they're stored in **LangGraph state** (in-memory/checkpointed), NOT on the local filesystem at `.deepagents/workspace/`.

---

## Why We Saw "Missing" Files

When we checked:
```bash
ls -la .deepagents/workspace/
# Empty directory
```

**This is EXPECTED behavior** because:
1. The default backend is `StateBackend` (ephemeral, in LangGraph state)
2. `StateBackend` doesn't write to disk — it stores files in agent state
3. Files exist in the thread's checkpoint but not on the filesystem

**The files likely DO exist** — just in LangGraph state, not on disk.

---

## The Correct Fix

### Option 1: Write Files to Disk (FilesystemBackend)

**Use case**: Want persistent files on disk for inspection/debugging

```python
# In apps/api/lifesciences.py
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

# Update the supervisor agent
lifesciences_graph = create_deep_agent(
    name="lifesciences",
    model="openai:gpt-4o",
    backend=FilesystemBackend(
        root_dir=".deepagents/workspace",
        virtual_mode=True  # Security: restricts paths to root_dir
    ),
    system_prompt=supervisor_prompt,
    subagents=[
        anchor_specialist,
        enrichment_specialist,
        expansion_specialist,
        traversal_drugs_specialist,
        traversal_trials_specialist,
        validation_specialist,
        persistence_specialist,
    ],
)
```

**Result**: Phase files will be written to `.deepagents/workspace/phase*.json` on disk.

**Security note** (from docs):
> "Security risks: Agents can read any accessible file, including secrets (API keys, credentials, .env files)"
> "Always use `virtual_mode=True` with `root_dir` to enable path-based access restrictions"

---

### Option 2: Use CompositeBackend (Hybrid)

**Use case**: Ephemeral files in state, but persist important files to disk

```python
from deepagents.backends import CompositeBackend, StateBackend, FilesystemBackend

lifesciences_graph = create_deep_agent(
    name="lifesciences",
    model="openai:gpt-4o",
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),  # Most files in state
        routes={
            "/workspace/": FilesystemBackend(root_dir=".deepagents/workspace", virtual_mode=True),
        }
    ),
    system_prompt=supervisor_prompt,
    subagents=[...],
)
```

**Update specialist prompts** to write to `/workspace/` prefix:
```python
# In apps/api/shared/prompts.py
anchor_specialist_prompt = f"""...
Once entities are resolved, persist your findings as /workspace/phase1_anchor.json with schema...
"""
```

**Result**:
- Files written to `/workspace/phase*.json` → saved to disk
- Other files → stored in state (ephemeral)

---

### Option 3: Keep StateBackend, Query State Programmatically

**Use case**: Files in state are fine, just need to access them programmatically

The files exist in LangGraph state. To read them:

```python
# In your application code
from langgraph_sdk import get_client

client = get_client()
state = client.threads.get_state(thread_id)

# Files are in state['values']['filesystem'] or similar
# (Exact path depends on StateBackend implementation)
```

**This requires no code changes** — files already exist in state.

---

## Verification

After applying Option 1 (FilesystemBackend):

```bash
# Run the FOP query again
# Then check:
ls -la .deepagents/workspace/

# Expected output:
# phase1_anchor.json
# phase2_enrich.json
# phase3_expand.json
# phase4a_drugs.json
# phase4b_trials.json
# phase5_validate.json
# graph.json
# report.md
```

---

## Updated Recommendations

### For Development (Local Testing)
**Use Option 1 (FilesystemBackend)** — easier to inspect files

```python
backend=FilesystemBackend(root_dir=".deepagents/workspace", virtual_mode=True)
```

### For Production (Web Server)
**Use StateBackend (default)** — don't write to disk in production

Files in state are:
- Thread-scoped (isolated between users)
- Checkpointed (survive crashes)
- Secure (no filesystem access)

### For CI/CD Pipelines
**Use Option 2 (CompositeBackend)** — ephemeral files in state, artifacts on disk

```python
backend=lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={"/artifacts/": FilesystemBackend(root_dir="./artifacts", virtual_mode=True)}
)
```

---

## Why My Original Fix Was Wrong

**I assumed**:
- Specialists don't have `write_file` tool
- Need to manually add `write_file` to tool lists

**Reality** (from docs):
- `create_deep_agent()` **automatically** includes `FilesystemMiddleware`
- `FilesystemMiddleware` **automatically** provides `write_file`, `read_file`, `ls`, `edit_file`
- Subagents **automatically** inherit these tools

**The real issue**:
- Files ARE being created (specialists have the tools)
- But default `StateBackend` writes to state, not disk
- To get files on disk, configure `FilesystemBackend`

---

## Sources

All information verified against LangChain documentation:

1. [Agent harness capabilities](https://docs.langchain.com/oss/python/deepagents/harness) — Automatic middleware
2. [Filesystem middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in) — Tools provided
3. [StateBackend](https://docs.langchain.com/oss/python/deepagents/customization) — Default backend behavior
4. [FilesystemBackend](https://docs.langchain.com/oss/python/deepagents/backends) — Disk persistence
5. [Pluggable storage backends](https://docs.langchain.com/oss/python/deepagents/harness) — Backend comparison
6. [Short-term vs. long-term filesystem](https://docs.langchain.com/oss/python/langchain/middleware/built-in) — StateBackend vs StoreBackend

---

## Action Items

1. ✓ **Correct the analysis** — Update SKILL-VS-DEEPAGENTS.md and ANALYSIS.md with correct fix
2. **Test the fix** — Apply FilesystemBackend and run FOP query
3. **Verify files** — Confirm all 8 phase files appear in `.deepagents/workspace/`
4. **Document the fix** — Add to CLAUDE.md for future reference
5. **Update prompts** (optional) — If using CompositeBackend, update paths to `/workspace/` prefix
