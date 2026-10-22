"""The Life Sciences supervisor agent as a Temporal workflow.

The agent loop (supervisor, task() delegation, subagent loops, middleware) runs
in the workflow and replays deterministically. Every model call, every I/O tool
call and every persistent-filesystem operation is an activity. ``/workspace/``
stays on ``StateBackend``, i.e. in agent state inside the workflow.

Loop limits are LangChain middleware; Temporal's part is that the counters are
rebuilt from history on replay, so a crash cannot reset a run's budget. The
same holds for tool failure counts (``tool_errors.ToolFailureMiddleware``).
"""

from dataclasses import dataclass, field
from functools import partial
from typing import Any

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from deepagents.backends import FilesystemBackend
    from langchain.agents.middleware import ModelCallLimitMiddleware
    from langgraph.errors import GraphRecursionError
    from temporalio.deepagents import TemporalBackend, create_temporal_deep_agent

    from agent_factory import AgentConfig, build_lifesciences_agent
    from apps.temporal.caching import TemporalAnthropicPromptCachingMiddleware
    from apps.temporal.durable import (
        BACKEND_ACTIVITY_OPTIONS,
        DURABLE_TOOLS,
        FILESYSTEM_BACKEND,
        MODEL_ACTIVITY_OPTIONS,
    )
    from apps.temporal.tool_errors import ToolFailureMiddleware


@dataclass
class LoopLimits:
    """Model-call caps. Observed in the 2026-10-21 runs: supervisor <= 21, any
    one specialist invocation <= 29. Defaults leave roughly 2x headroom."""

    supervisor_model_calls: int = 40
    subagent_model_calls: int = 50


@dataclass
class ResearchInput:
    question: str
    config: AgentConfig
    limits: LoopLimits = field(default_factory=LoopLimits)


@dataclass
class ResearchResult:
    answer: str
    workspace_files: dict[str, str]


def _text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        )
    return str(content)


def _agent_middleware(limit: int, tool_failures: ToolFailureMiddleware) -> list[Any]:
    """Middleware for one agent (the supervisor or one specialist).

    The call limit and caching middleware are new per agent; ``tool_failures``
    is the run's single instance, so failures of a service count across agents.
    """
    return [
        ModelCallLimitMiddleware(run_limit=limit, exit_behavior="end"),
        TemporalAnthropicPromptCachingMiddleware(),
        tool_failures,
    ]


@workflow.defn(failure_exception_types=[GraphRecursionError])
class LifesciencesResearchWorkflow:
    @workflow.run
    async def run(self, input: ResearchInput) -> ResearchResult:
        filesystem = TemporalBackend(
            FILESYSTEM_BACKEND,
            factory_argument=input.config.runtime_root,
            backend_type=FilesystemBackend,
            activity_options=BACKEND_ACTIVITY_OPTIONS,
        )
        # Built here, not at import: its failure counts are rebuilt from history
        # on replay, so a worker restart does not reset them.
        tool_failures = ToolFailureMiddleware()
        agent = build_lifesciences_agent(
            input.config,
            tools=DURABLE_TOOLS,
            filesystem_backend=filesystem,
            agent_factory=partial(
                create_temporal_deep_agent, activity_options=MODEL_ACTIVITY_OPTIONS
            ),
            supervisor_middleware=_agent_middleware(
                input.limits.supervisor_model_calls, tool_failures
            ),
            subagent_middleware=partial(
                _agent_middleware, input.limits.subagent_model_calls, tool_failures
            ),
        )
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": input.question}]}
        )
        # CompositeBackend strips the route prefix before writing to state, so
        # state keys are "/report.md"; report the path the agent wrote to.
        files = {
            f"/workspace{path}": _text(
                data.get("content", "") if isinstance(data, dict) else data
            )
            for path, data in (result.get("files") or {}).items()
        }
        return ResearchResult(
            answer=_text(result["messages"][-1].content),
            workspace_files=files,
        )
