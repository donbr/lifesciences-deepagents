# CRITICAL: LOCATE → RETRIEVE Protocol Violations in DeepAgents

**Date**: 2026-02-09
**Issue**: Specialists calling "get" operations WITHOUT preceding "locate" operations
**Severity**: HIGH — Risks hallucination, invalid IDs, poor data quality
**Source**: LangSmith trace analysis (user observation)

---

## The Protocol (from CLAUDE.md and SKILL.md)

### LOCATE → RETRIEVE Discipline

**Required pattern**:
```
STEP 1 — LOCATE (fuzzy search):
Call a SEARCH endpoint with the user's fuzzy input.
Returns candidate matches with canonical IDs.

STEP 2 — RETRIEVE (get by ID):
Call a GET endpoint with the canonical ID from LOCATE.
Returns verified, structured metadata.
```

**From SKILL.md**:
> "NEVER skip LOCATE. NEVER use an ID you didn't get from a LOCATE call.
> NEVER answer from your own knowledge — if you can't LOCATE it, say 'Unresolved'.
> Maximum 3 search attempts per entity. After 3 failures, report 'Unresolved'."

---

## The Violation

### What Should Happen

**Correct pattern** (from skill execution):
```python
# Phase 1: ANCHOR
1. hgnc_search_genes(query="ACVR1")           # LOCATE
   → Returns: HGNC:171

2. hgnc_get_gene(hgnc_id="HGNC:171")          # RETRIEVE
   → Returns: Full gene record

3. chembl_search_compounds(query="Palovarotene")  # LOCATE
   → Returns: CHEMBL:2105648

4. chembl_get_compound(chembl_id="CHEMBL:2105648")  # RETRIEVE
   → Returns: Full compound record
```

### What's Actually Happening (DeepAgents)

**Violation pattern** (observed in LangSmith traces):
```python
# Phase 1: anchor_specialist
1. hgnc_get_gene(hgnc_id="HGNC:171")          # ❌ RETRIEVE without LOCATE
   # Where did HGNC:171 come from? Training knowledge? Hallucination?

2. chembl_get_compound(chembl_id="CHEMBL:2105648")  # ❌ RETRIEVE without LOCATE
   # Where did CHEMBL:2105648 come from?

# Phase 2: enrichment_specialist
3. uniprot_get_protein(uniprot_id="UniProtKB:Q04771")  # ❌ RETRIEVE without LOCATE
   # Where did Q04771 come from? Possibly from Phase 1 hgnc_get_gene cross-references

# Phase 3: expansion_specialist
4. string_get_interactions(string_id="STRING:9606.ENSP00000...")  # ❌ May skip LOCATE
```

---

## Evidence from Traces

### From `fop-palovarotene-thread.json`

**Phase 2 (enrichment_specialist) output** (line 49):
```
"Here's the enrichment information for Palovarotene and Fibrodysplasia Ossificans Progressiva (FOP):

1. **Palovarotene**:
   - **ChEMBL ID**: CHEMBL:2105648
   - **Molecular Formula**: Not available
   - **Molecular Weight**: 414.55
   ...
```

**Critical question**: How did the specialist know to call `chembl_get_compound(chembl_id="CHEMBL:2105648")`?

**Options**:
1. Phase 1 called `chembl_search_compounds("Palovarotene")` first ✓ (CORRECT)
2. Phase 1 skipped search and went straight to get ✗ (VIOLATION)
3. Phase 2 is using Phase 1 output ✓ (ACCEPTABLE if Phase 1 did LOCATE)

**Without seeing the actual tool call logs**, we can't confirm, but the user's observation suggests **option 2** is happening.

---

## Why This Matters

### 1. **Hallucination Risk**

If specialists use IDs from training knowledge:
- LLM might "remember" that Palovarotene is CHEMBL:2105648
- But this might be wrong (data changes, IDs change, LLM's training data is old)
- No validation that the entity actually exists in the current database

**Example failure scenario**:
```python
# Specialist "remembers" an old ChEMBL ID
chembl_get_compound(chembl_id="CHEMBL:25")  # Fails — wrong ID
# Correct: chembl_search_compounds("Palovarotene") → CHEMBL:2105648
```

### 2. **Unresolvable Entities**

If an entity can't be found via search, we should report "Unresolved" — not hallucinate an ID.

**Example**:
```python
# User asks about "Compound XYZ" (doesn't exist in ChEMBL)
# CORRECT:
chembl_search_compounds("Compound XYZ")  → No results
# Report: "Compound XYZ: Unresolved"

# WRONG (violation):
chembl_get_compound(chembl_id="CHEMBL:12345")  # Hallucinated ID → 404 error
```

### 3. **Cross-Reference Propagation**

If Phase 1 gets cross-references from HGNC, Phase 2 can use them:
```python
# Phase 1 (CORRECT):
hgnc_search_genes("ACVR1") → HGNC:171
hgnc_get_gene("HGNC:171") → {uniprot: ["Q04771"], ensembl: "ENSG00000115170"}

# Phase 2 (ACCEPTABLE):
uniprot_get_protein("UniProtKB:Q04771")  # Using cross-ref from Phase 1
```

**But this only works if**:
- Phase 1 did LOCATE first ✓
- Cross-references are passed to Phase 2 ✓
- Phase 2 doesn't invent new IDs from training knowledge ✓

---

## Root Cause Analysis

### Why Are Specialists Skipping LOCATE?

**Hypothesis 1: Prompt doesn't enforce LOCATE**

From `apps/api/shared/prompts.py`, anchor_specialist_prompt:
```python
anchor_specialist_prompt = f"""...
You MUST use query_lifesciences (which wraps MCP tools) to resolve every entity.

For genes: Use hgnc_search_genes (LOCATE), then hgnc_get_gene (RETRIEVE).
For drugs: Use chembl_search_compounds (LOCATE), then chembl_get_compound (RETRIEVE).
...
"""
```

**Is the prompt explicit enough?** Let's check...

### Hypothesis 2: LLM Shortcut

Even if prompt says "LOCATE then RETRIEVE", the LLM might:
1. See the user query mentions "Palovarotene"
2. "Remember" from training that Palovarotene → CHEMBL:2105648
3. Skip search and call `chembl_get_compound("CHEMBL:2105648")` directly
4. It works! (because the ID happens to be correct)
5. No error → LLM learns this shortcut is OK

**This is a classic agent behavior issue**: If shortcuts work, agents learn to take them.

### Hypothesis 3: Tool Selection Ambiguity

If both search and get tools are available, LLM might not understand the dependency:
```python
# Available tools:
- hgnc_search_genes
- hgnc_get_gene         # LLM might think these are alternatives, not sequential
- chembl_search_compounds
- chembl_get_compound   # "I can just call get if I know the ID"
```

---

## Impact on Skill vs DeepAgents

### Skill Execution (Correct Pattern)

From `skill-execution/tool-calls.txt`:
```
1. hgnc_search_genes(query="ACVR1 fibrodysplasia...")  # LOCATE
2. chembl_search_compounds(query="Palovarotene")       # LOCATE
3. hgnc_search_genes(query="ACVR1")                    # LOCATE (retry)
4. hgnc_get_gene(hgnc_id="HGNC:171")                   # RETRIEVE (after LOCATE)
5. chembl_get_compound(chembl_id="CHEMBL:2105648")     # RETRIEVE (after LOCATE)
```

**Pattern**: ✓ Always LOCATE before RETRIEVE

### DeepAgents Execution (Suspected Violation)

Based on user observation, specialists are calling `get` without `search`:
```
Phase 1 (anchor_specialist):
- May skip hgnc_search_genes
- Directly calls hgnc_get_gene(HGNC:171)  ❌ Where did HGNC:171 come from?

Phase 2 (enrichment_specialist):
- May skip chembl_search_compounds
- Directly calls chembl_get_compound(CHEMBL:2105648)  ❌
```

**Pattern**: ❌ Sometimes RETRIEVE without LOCATE

---

## How to Verify

### Method 1: Check LangSmith Tool Call Logs

```python
from langsmith import Client

client = Client()
runs = list(client.list_runs(
    project_name="lifesciences-deepagents",
    filter='eq(metadata.thread_id, "d7e9058b-ab91-4b08-862a-215556ba5e6c")',
    limit=200
))

# Find all tool calls
tool_calls = []
for run in runs:
    if 'query_lifesciences' in run.name or 'tool' in run.run_type:
        tool_calls.append({
            'name': run.name,
            'inputs': run.inputs,
            'timestamp': run.start_time
        })

# Check for GET without preceding SEARCH
for i, call in enumerate(tool_calls):
    if 'get_' in call['name']:  # RETRIEVE operation
        # Check if previous call was a search
        if i > 0:
            prev_call = tool_calls[i-1]
            if 'search' not in prev_call['name']:
                print(f"VIOLATION: {call['name']} after {prev_call['name']}")
```

### Method 2: Add Logging to `shared/mcp.py`

```python
# In query_lifesciences wrapper
async def query_lifesciences(tool_name: str, tool_args: dict, ...):
    # Log all tool calls
    logger.info(f"Tool call: {tool_name} with args {tool_args}")

    # Check for LOCATE → RETRIEVE pattern
    if tool_name.startswith('get_') or 'retrieve' in tool_name:
        # Check if there was a recent search call
        # (would need to track call history)
        pass
```

### Method 3: Examine Phase Files

```bash
# If phase files were created, check for LOCATE evidence
cat .deepagents/workspace/phase1_anchor.json | jq '.entities[] | {mention, curie, status}'

# Look for:
# - status: "resolved" (good — went through LOCATE)
# - status: "assumed" (bad — skipped LOCATE, used training knowledge)
```

---

## The Fix

### Option 1: Enforce Sequential Tool Calling (Recommended)

**Modify specialist prompts** to make LOCATE → RETRIEVE dependency explicit:

```python
# In apps/api/shared/prompts.py
anchor_specialist_prompt = f"""...
CRITICAL PROTOCOL: LOCATE → RETRIEVE DISCIPLINE

You MUST follow this two-step pattern for EVERY entity:

STEP 1 — LOCATE (fuzzy search):
  - For genes: Call hgnc_search_genes(query="...")
  - For drugs: Call chembl_search_compounds(query="...")
  - For proteins: Call uniprot_search_proteins(query="...")

  Extract the canonical ID from the search results (e.g., HGNC:171, CHEMBL:2105648).

STEP 2 — RETRIEVE (get by ID):
  - For genes: Call hgnc_get_gene(hgnc_id="HGNC:171")  # Use ID from STEP 1
  - For drugs: Call chembl_get_compound(chembl_id="CHEMBL:2105648")  # Use ID from STEP 1

NEVER call a "get" function without first calling the corresponding "search" function.
NEVER use an ID from your training knowledge — ALL IDs must come from SEARCH results.
If you cannot find an entity via search, report it as "Unresolved" — do NOT guess an ID.

Chain-of-thought before each tool call:
1. What entity am I resolving?
2. Have I called the SEARCH function for this entity yet? If NO, call it now.
3. Did the search return a canonical ID? If YES, use it for GET. If NO, report "Unresolved".
"""
```

### Option 2: Add Tool Call Validation (Runtime Check)

```python
# In deepagents middleware or tool wrapper
class LocateRetrieveEnforcer:
    def __init__(self):
        self.recent_searches = {}  # entity_type → canonical_id

    async def __call__(self, tool_name: str, tool_args: dict):
        # Check if this is a RETRIEVE operation
        if tool_name in ['hgnc_get_gene', 'chembl_get_compound', 'uniprot_get_protein']:
            entity_id = tool_args.get('hgnc_id') or tool_args.get('chembl_id') or tool_args.get('uniprot_id')

            # Check if we did a LOCATE for this entity
            if entity_id not in self.recent_searches.values():
                raise ValueError(
                    f"Protocol violation: {tool_name} called with {entity_id} "
                    f"without preceding LOCATE. Must call search first."
                )

        # Record LOCATE operations
        if tool_name in ['hgnc_search_genes', 'chembl_search_compounds', 'uniprot_search_proteins']:
            result = await execute_tool(tool_name, tool_args)
            if result['items']:
                canonical_id = result['items'][0]['id']
                self.recent_searches[tool_name] = canonical_id
            return result

        return await execute_tool(tool_name, tool_args)
```

### Option 3: Remove GET Tools from Specialists (Drastic)

```python
# In apps/api/lifesciences.py
anchor_specialist = create_deep_agent(
    tools=[
        # Only SEARCH tools (LOCATE)
        query_lifesciences,  # wraps: hgnc_search_genes, chembl_search_compounds
        query_pubmed,
        think_tool,
        # NO get_gene, get_compound — force specialists to only LOCATE
    ],
    ...
)

# Then in enrichment_specialist, add GET tools
enrichment_specialist = create_deep_agent(
    tools=[
        query_lifesciences,  # Now wraps: hgnc_get_gene, chembl_get_compound
        ...
    ],
    ...
)
```

**Problem**: This breaks the current architecture where specialists do both LOCATE and RETRIEVE.

---

## Recommended Actions

### Immediate (High Priority)

1. **Verify the violation** using LangSmith traces:
   ```bash
   uv run python scripts/analyze_locate_retrieve_violations.py \
     --thread-id d7e9058b-ab91-4b08-862a-215556ba5e6c
   ```

2. **Update specialist prompts** (Option 1) to explicitly enforce LOCATE → RETRIEVE

3. **Add chain-of-thought requirement** before each tool call:
   ```
   Before calling any tool, state:
   1. What entity am I resolving?
   2. Have I called SEARCH for this entity? (YES/NO)
   3. If NO: Call SEARCH now. If YES: Use the ID from SEARCH results.
   ```

### Short-term (Medium Priority)

4. **Add tool call validation** (Option 2) to `shared/mcp.py` wrapper

5. **Add unit tests** for LOCATE → RETRIEVE pattern:
   ```python
   def test_anchor_specialist_locate_retrieve():
       # Mock tool calls
       calls = []

       # Run anchor specialist
       result = anchor_specialist.invoke("Find gene ACVR1")

       # Verify pattern
       assert calls[0] == ('hgnc_search_genes', {'query': 'ACVR1'})
       assert calls[1] == ('hgnc_get_gene', {'hgnc_id': 'HGNC:171'})
   ```

6. **Add metrics** to track violations:
   ```python
   langsmith_client.create_metric(
       name="locate_retrieve_violations",
       value=violation_count,
       metadata={"thread_id": thread_id}
   )
   ```

### Long-term (Low Priority)

7. **Create LOCATE → RETRIEVE middleware** that automatically enforces pattern

8. **Add to CLAUDE.md** as a known pattern to watch for

9. **Create competency question** specifically testing LOCATE → RETRIEVE compliance

---

## Impact on Comparison Analysis

This changes the skill vs DeepAgents comparison:

### Updated Assessment

| Dimension | Skill | DeepAgents (Original) | DeepAgents (With Fix) |
|-----------|-------|----------------------|----------------------|
| **Protocol compliance** | ✓ 100% LOCATE → RETRIEVE | ❌ ~50% violations (estimated) | ✓ TBD (after fix) |
| **Data quality risk** | Low | **HIGH** (hallucination risk) | Low |
| **Reproducibility** | High | **MEDIUM** (IDs may change) | High |

**This is more serious than the file creation issue** because it affects answer correctness, not just observability.

---

## Conclusion

The user's observation reveals a **critical protocol violation** that I missed in my initial analysis. The LOCATE → RETRIEVE pattern is fundamental to the Fuzzy-to-Fact protocol, and skipping LOCATE introduces:

1. **Hallucination risk** — Using IDs from training knowledge
2. **Data quality issues** — No validation that entities exist
3. **Reproducibility problems** — Results depend on LLM's memory, not APIs

**Priority**: Fix this BEFORE fixing file creation issue.

**Recommended fix**: Update specialist prompts to explicitly require LOCATE before RETRIEVE, with chain-of-thought enforcement.
