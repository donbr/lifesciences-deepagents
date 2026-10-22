"""Offline fakes for the Temporal host: a message-aware model and a stub MCP tool."""

import asyncio
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, ClassVar

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult


@dataclass
class FakeState:
    tool_calls: Counter = field(default_factory=Counter)
    tool_args: list[tuple[str, dict]] = field(default_factory=list)
    tool_delay: float = 0.0
    # Per-tool scripted outcomes, consumed in order; an exception is raised,
    # a string is returned. Default (empty) is success.
    tool_script: dict[str, list[Exception | str]] = field(default_factory=dict)
    # Per-role ("supervisor" / "subagent") exceptions the model raises, one per
    # call, before replying normally.
    model_script: dict[str, list[Exception]] = field(default_factory=dict)


FAKE_STATE = FakeState()


def reset_fakes() -> None:
    FAKE_STATE.tool_calls.clear()
    FAKE_STATE.tool_args.clear()
    FAKE_STATE.tool_delay = 0.0
    FAKE_STATE.tool_script.clear()
    FAKE_STATE.model_script.clear()
    PolicyModel.calls.clear()


def _call(call_id: str, name: str, args: dict) -> AIMessage:
    return AIMessage(content="", tool_calls=[{"id": call_id, "name": name, "args": args}])


def _task(subagent_type: str, description: str) -> tuple[str, dict]:
    return "task", {"subagent_type": subagent_type, "description": description}


# Supervisor's first delegation per mode. A loop specialist repeats the tool
# named by "Use <tool>." in its task description.
_FIRST_TASKS = {
    "string_loop": [
        _task("expansion_specialist", "Expand NF1. Use string_search_proteins."),
    ],
    # Both specialists have chembl_search_compounds: two branches, one service.
    "parallel": [
        _task("anchor_specialist", "Anchor NF1. Use chembl_search_compounds."),
        _task("traversal_drugs_specialist", "Drugs for NF1. Use chembl_search_compounds."),
    ],
}
_DEFAULT_FIRST_TASK = [_task("anchor_specialist", "Anchor NF1 and doxorubicin to CURIEs.")]
_LOOP_MODES = {"string_loop", "parallel"}
MAX_LOOP_CALLS = 10


class PolicyModel(BaseChatModel):
    """Chooses its reply from the conversation, so call order does not matter."""

    mode: str
    calls: ClassVar[list[dict]] = []

    @property
    def _llm_type(self) -> str:
        return "policy-fake"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "PolicyModel":
        return self

    def _reply(self, messages: list[BaseMessage]) -> tuple[str, AIMessage]:
        system = " ".join(
            str(m.content) for m in messages if isinstance(m, SystemMessage)
        )
        done = Counter(m.name for m in messages if isinstance(m, ToolMessage))
        call_id = f"call-{len(messages)}"
        if "Life Sciences Graph Builder Supervisor" in system:
            if not done["task"]:
                tasks = _FIRST_TASKS.get(self.mode, _DEFAULT_FIRST_TASK)
                return "supervisor", AIMessage(content="", tool_calls=[
                    {"id": f"{call_id}-{i}", "name": name, "args": args}
                    for i, (name, args) in enumerate(tasks)
                ])
            if not done["write_file"]:
                return "supervisor", _call(call_id, "write_file", {
                    "file_path": "/workspace/report.md",
                    "content": "# NF1 report\nHGNC:7765",
                })
            return "supervisor", AIMessage(content="DONE: report written to /workspace/report.md")
        if self.mode in _LOOP_MODES:
            return "subagent", self._loop_reply(messages, call_id)
        if self.mode == "happy" and not done["think_tool"]:
            # think_tool is sync and pure: it runs in the workflow, not as an activity.
            return "subagent", _call(call_id, "think_tool", {"reflection": "Resolve NF1 first."})
        if self.mode == "runaway" or not done["hgnc_search_genes"]:
            return "subagent", _call(call_id, "hgnc_search_genes", {"query": "NF1"})
        return "subagent", AIMessage(content="Anchored NF1 -> HGNC:7765")

    def _loop_reply(self, messages: list[BaseMessage], call_id: str) -> AIMessage:
        """Call the task's tool until it returns a non-error result (max 10 calls)."""
        task = next(str(m.content) for m in messages if isinstance(m, HumanMessage))
        tool = re.search(r"Use (\w+)\.", task).group(1)
        results = [m for m in messages if isinstance(m, ToolMessage) and m.name == tool]
        if any(m.status != "error" for m in results):
            return AIMessage(content=f"{tool} succeeded")
        if len(results) >= MAX_LOOP_CALLS:
            return AIMessage(content=f"{tool} kept failing")
        # The task text as query tells the branches apart in FAKE_STATE.tool_args.
        return _call(call_id, tool, {"query": task})

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        role, message = self._reply(messages)
        script = FAKE_STATE.model_script.get(role)
        if script:
            raise script.pop(0)
        PolicyModel.calls.append({
            "role": role,
            "kwargs": kwargs,
            "tool_results": [
                (m.name, m.status, str(m.content))
                for m in messages
                if isinstance(m, ToolMessage)
            ],
        })
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        return self._generate(messages, **kwargs)


async def fake_call_tool(tool_name: str, arguments: dict, apply_rate_limit: bool = True) -> str:
    FAKE_STATE.tool_calls[tool_name] += 1
    FAKE_STATE.tool_args.append((tool_name, arguments))
    await asyncio.sleep(FAKE_STATE.tool_delay)
    script = FAKE_STATE.tool_script.get(tool_name)
    if script:
        outcome = script.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
    return f"{tool_name}: HGNC:7765 NF1 neurofibromin 1"
