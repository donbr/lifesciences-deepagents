"""
Side-effect-free construction of the Life Sciences supervisor agent.

Split out of ``lifesciences.py`` so two hosts can share one agent definition:

- the LangGraph server (``lifesciences.py:graph``), which resolves config from the
  local filesystem and builds the agent at import time;
- a Temporal workflow (``apps/temporal``), which receives the resolved config as a
  workflow argument and must not do I/O, read the clock or the environment while
  building the agent.

Everything that touches disk, env or the clock lives in ``resolve_agent_config``.
``build_lifesciences_agent`` only assembles objects, and takes hooks so the
Temporal host can route tools and the filesystem backend through activities.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware, ToolCallRequest
from langchain_core.messages import ToolMessage
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend

from shared import mcp
from shared.tools import think_tool
from shared.prompts import (
    ANCHOR_SYSTEM,
    ENRICH_SYSTEM,
    EXPAND_SYSTEM,
    TRAVERSE_DRUGS_SYSTEM,
    TRAVERSE_TRIALS_SYSTEM,
    VALIDATE_SYSTEM,
    PERSIST_SYSTEM,
)

DEFAULT_MODEL = "anthropic:claude-sonnet-4-5-20250929"

ALLOWED_LIFESCIENCES_SUBAGENTS = {
    "anchor_specialist",
    "enrichment_specialist",
    "expansion_specialist",
    "traversal_drugs_specialist",
    "traversal_trials_specialist",
    "validation_specialist",
    "persistence_specialist",
}

# Tools whose bodies do network or subprocess I/O. Everything here must run as an
# activity under Temporal; think_tool is pure and stays in the agent loop.
IO_TOOL_NAMES = (
    "query_api_direct",
    "persist_to_graphiti",
    "query_pubmed",
    *mcp.LIFESCIENCES_ALIAS_TOOL_NAMES,
)

SUBAGENT_TOOL_NAMES: dict[str, tuple[str, ...]] = {
    "anchor_specialist": (
        "hgnc_search_genes",
        "ensembl_search_genes",
        "entrez_search_genes",
        "uniprot_search_proteins",
        "chembl_search_compounds",
        "pubchem_search_compounds",
        "iuphar_search_ligands",
        "iuphar_search_targets",
        "wikipathways_search_pathways",
        "clinicaltrials_search_trials",
        "query_pubmed",
        "think_tool",
    ),
    "enrichment_specialist": (
        "hgnc_get_gene",
        "ensembl_search_genes",
        "ensembl_get_gene",
        "ensembl_get_transcript",
        "entrez_get_gene",
        "entrez_get_pubmed_links",
        "uniprot_search_proteins",
        "uniprot_get_protein",
        "chembl_get_compound",
        "chembl_get_compounds_batch",
        "pubchem_get_compound",
        "iuphar_get_ligand",
        "iuphar_get_target",
        "opentargets_get_associations",
        "query_pubmed",
        "think_tool",
    ),
    "expansion_specialist": (
        "string_search_proteins",
        "string_get_interactions",
        "string_get_network_image_url",
        "wikipathways_get_pathways_for_gene",
        "wikipathways_get_pathway_components",
        "wikipathways_get_pathway",
        "biogrid_search_genes",
        "biogrid_get_interactions",
        "think_tool",
    ),
    "traversal_drugs_specialist": (
        "chembl_search_compounds",
        "chembl_get_compound",
        "pubchem_search_compounds",
        "pubchem_get_compound",
        "iuphar_search_ligands",
        "iuphar_get_ligand",
        "opentargets_search_targets",
        "opentargets_get_target",
        "opentargets_get_associations",
        "query_api_direct",
        "think_tool",
    ),
    "traversal_trials_specialist": (
        "clinicaltrials_search_trials",
        "clinicaltrials_get_trial",
        "clinicaltrials_get_trial_locations",
        "query_api_direct",
        "think_tool",
    ),
    "validation_specialist": (
        "clinicaltrials_get_trial",
        "pubchem_get_compound",
        "chembl_get_compound",
        "ensembl_get_gene",
        "query_pubmed",
        "think_tool",
    ),
    "persistence_specialist": ("persist_to_graphiti",),
}

SUBAGENT_DESCRIPTIONS = {
    "anchor_specialist": "PHASE 1: Resolves fuzzy terms to canonical CURIEs (HGNC, CHEMBL, NCT). Use for identifying genes, drugs, and diseases. Can also search literature via PubMed.",
    "enrichment_specialist": "PHASE 2: Fetches detailed metadata for CURIEs. Gets UniProt/Ensembl IDs for genes, functions for proteins, Max Phase for drugs.",
    "expansion_specialist": "PHASE 3: Finds biological connections. Gets STRING interactions, WikiPathways, BioGrid genetic interactions.",
    "traversal_drugs_specialist": "PHASE 4a: Identifies therapeutic targets and finds drugs that target them. Searches for approved drugs and inhibitors. Has fallback to Open Targets if ChEMBL fails.",
    "traversal_trials_specialist": "PHASE 4b: Finds Clinical Trials for identified drugs. Combines drug names with disease context. Can use ClinicalTrials.gov v2 API directly.",
    "validation_specialist": "PHASE 5: Verifies facts to prevent hallucinations. Validates NCT IDs and drug mechanisms. Can verify claims against PubMed literature.",
    "persistence_specialist": "PHASE 6: Formats validated knowledge graph and provides final summary.",
}

SUBAGENT_PROMPTS = {
    "anchor_specialist": ANCHOR_SYSTEM,
    "enrichment_specialist": ENRICH_SYSTEM,
    "expansion_specialist": EXPAND_SYSTEM,
    "traversal_drugs_specialist": TRAVERSE_DRUGS_SYSTEM,
    "traversal_trials_specialist": TRAVERSE_TRIALS_SYSTEM,
    "validation_specialist": VALIDATE_SYSTEM,
    "persistence_specialist": PERSIST_SYSTEM,
}

# Subagent order matches the protocol phases (and the original file).
SUBAGENT_ORDER = tuple(SUBAGENT_TOOL_NAMES)


def all_tools() -> dict[str, Any]:
    """Every tool any specialist can use, keyed by tool name."""
    tools = {name: getattr(mcp, name) for name in IO_TOOL_NAMES}
    tools["think_tool"] = think_tool
    return tools


class LifesciencesSubagentGuardMiddleware(AgentMiddleware):
    """Reject missing/unknown task() subagent types."""

    def _validate(self, request: ToolCallRequest) -> ToolMessage | None:
        if request.tool_call.get("name") != "task":
            return None

        tool_call_id = request.tool_call.get("id", "subagent-guard")
        args = request.tool_call.get("args", {})
        if not isinstance(args, dict):
            return ToolMessage(
                content="Rejected task call: arguments must be an object.",
                tool_call_id=tool_call_id,
                status="error",
            )

        subagent_type = str(args.get("subagent_type", "")).strip()
        if not subagent_type:
            return ToolMessage(
                content="Rejected task call: missing `subagent_type`.",
                tool_call_id=tool_call_id,
                status="error",
            )

        if subagent_type not in ALLOWED_LIFESCIENCES_SUBAGENTS:
            allowed = ", ".join(sorted(ALLOWED_LIFESCIENCES_SUBAGENTS))
            return ToolMessage(
                content=(
                    f"Rejected unknown subagent `{subagent_type}`. Allowed: {allowed}."
                ),
                tool_call_id=tool_call_id,
                status="error",
            )

        return None

    def wrap_tool_call(self, request: ToolCallRequest, handler):
        rejection = self._validate(request)
        if rejection is not None:
            return rejection
        return handler(request)

    async def awrap_tool_call(self, request: ToolCallRequest, handler):
        rejection = self._validate(request)
        if rejection is not None:
            return rejection
        return await handler(request)


@dataclass
class AgentConfig:
    """Everything the agent build needs from the host environment.

    Serializable, so a Temporal workflow can receive it as an argument instead
    of reading disk, env or the clock itself.
    """

    model_name: str
    runtime_root: str
    current_date: str
    memory_paths: list[str] = field(default_factory=list)
    skills_source: list[str] = field(default_factory=list)


def resolve_agent_config(model_name: str = DEFAULT_MODEL) -> AgentConfig:
    """Resolve runtime paths, skills and the date. Does I/O; host-side only."""
    configured = os.getenv("LIFESCIENCES_RUNTIME_ROOT")
    if configured:
        runtime_root = Path(configured).expanduser().resolve()
    else:
        repo_root = Path(__file__).resolve().parents[2]
        runtime_root = (repo_root / ".deepagents").resolve()
    runtime_root.mkdir(parents=True, exist_ok=True)
    (runtime_root / "workspace").mkdir(parents=True, exist_ok=True)

    skills_root = runtime_root / "skills"
    has_skills = skills_root.exists() and any(
        entry.is_dir() and (entry / "SKILL.md").exists()
        for entry in skills_root.iterdir()
    )

    # SkillsMiddleware expects parent-directory paths (e.g., "/skills/") so it can
    # scan child directories for SKILL.md files. Passing individual skill paths
    # like "/skills/lifesciences-graph-builder" causes _alist_skills to find only
    # SKILL.md (a file, not a directory), resulting in skill_dirs=[] and no skills
    # being injected into agent system prompts.
    #
    # We pass ["/skills/"] as the single source for all agents. Tool isolation is
    # enforced via the tools list on each specialist, not via skill visibility.
    return AgentConfig(
        model_name=model_name,
        runtime_root=str(runtime_root),
        current_date=datetime.now().strftime("%Y-%m-%d"),
        memory_paths=["/AGENTS.md"] if (runtime_root / "AGENTS.md").exists() else [],
        skills_source=["/skills/"] if has_skills else [],
    )


def supervisor_prompt(current_date: str) -> str:
    return f"""You are the Life Sciences Graph Builder Supervisor.
Your goal is to orchestrate the 'Fuzzy-to-Fact' protocol to answer user questions about biology and medicine.

You delegate work to specialist subagents using the task() tool. Each invocation is stateless — the specialist only sees the description you provide. Include ALL context the specialist needs.

Protocol Phases (execute sequentially unless noted):
1. ANCHOR: Identify entities and get CURIEs → delegate to anchor_specialist
2. ENRICH: Get metadata for those entities → delegate to enrichment_specialist
3. EXPAND: Find connections (interactions, pathways) → delegate to expansion_specialist
4. TRAVERSE_DRUGS + TRAVERSE_TRIALS: These two CAN run in parallel since they are independent.
   - TRAVERSE_DRUGS: Find drugs matching targets → delegate to traversal_drugs_specialist
   - TRAVERSE_TRIALS: Find clinical trials for the disease → delegate to traversal_trials_specialist
   To run in parallel, call both task() tools in a single message.
5. VALIDATE: Verify facts (IDs, mechanisms) → delegate to validation_specialist
6. PERSIST: Summarize and finalize → delegate to persistence_specialist

DATA PASSING BETWEEN PHASES:
- Each specialist returns structured results. You MUST include the relevant output in the description for the next specialist.
- Example: After ANCHOR returns CURIEs, pass them to ENRICH: "Enrich the following entities: HGNC:171 (ACVR1), MONDO:0018875 (FOP). Get UniProt IDs, Ensembl IDs, and functional descriptions."
- After ENRICH returns Ensembl IDs, pass them to TRAVERSE_DRUGS: "Find drugs targeting ACVR1 (Ensembl: ENSG00000115170). Try ChEMBL first, fall back to Open Targets."
- Include the disease context from the original query in ALL phase descriptions.

IMPORTANT:
- Do not skip phases. If a phase returns no results, note this and continue.
- After all phases complete, relay the persistence_specialist's summary to the user.

Today's date is {current_date}.

STRICT ROUTING RULES:
- NEVER invent new subagents (like 'research-analyst').
- Always start with 'anchor_specialist' for new queries.
- If the user asks a research question, map it to the 'anchor_specialist' first to identify the key entities."""


def build_lifesciences_agent(
    config: AgentConfig,
    *,
    model: Any = None,
    tools: dict[str, Any] | None = None,
    filesystem_backend: Any = None,
    agent_factory: Callable[..., Any] = create_deep_agent,
    supervisor_middleware: Sequence[AgentMiddleware] = (),
    subagent_middleware: Callable[[], Sequence[AgentMiddleware]] | None = None,
) -> Any:
    """Assemble the supervisor and its seven specialists. No I/O.

    Args:
        config: Output of ``resolve_agent_config``.
        model: Supervisor model; defaults to ``config.model_name``.
        tools: Tool objects by name; defaults to ``all_tools()``. A Temporal host
            passes activity-wrapped tools here.
        filesystem_backend: Backend for persistent paths (AGENTS.md, skills);
            defaults to a local ``FilesystemBackend``. A Temporal host passes a
            ``TemporalBackend`` here.
        agent_factory: ``create_deep_agent`` or a compatible wrapper.
        supervisor_middleware: Added after the subagent guard.
        subagent_middleware: Called once per specialist, so stateful middleware
            (call limits) is not shared between specialists.
    """
    tools = tools if tools is not None else all_tools()
    if filesystem_backend is None:
        filesystem_backend = FilesystemBackend(
            root_dir=config.runtime_root, virtual_mode=True
        )

    # Backend configuration for workspace isolation:
    # - /workspace/ → StateBackend (ephemeral, thread-scoped)
    # - Everything else → FilesystemBackend (persistent: AGENTS.md, skills)
    backend = CompositeBackend(
        default=filesystem_backend,
        routes={"/workspace/": StateBackend()},
    )

    subagents = []
    for name in SUBAGENT_ORDER:
        spec: dict[str, Any] = {
            "name": name,
            "description": SUBAGENT_DESCRIPTIONS[name],
            "system_prompt": SUBAGENT_PROMPTS[name],
            "model": config.model_name,
            "skills": list(config.skills_source),
            "tools": [tools[t] for t in SUBAGENT_TOOL_NAMES[name]],
        }
        if subagent_middleware is not None:
            spec["middleware"] = list(subagent_middleware())
        subagents.append(spec)

    return agent_factory(
        model=model if model is not None else config.model_name,
        tools=[],  # Supervisor delegates, doesn't call tools directly
        system_prompt=supervisor_prompt(config.current_date),
        middleware=[LifesciencesSubagentGuardMiddleware(), *supervisor_middleware],
        backend=backend,
        memory=config.memory_paths or None,
        skills=config.skills_source or None,
        subagents=subagents,
    )
