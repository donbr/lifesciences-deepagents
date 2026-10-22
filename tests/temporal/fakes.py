"""Offline fakes for the Temporal host: a message-aware model and a stub MCP tool."""

import asyncio
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, ClassVar

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult


@dataclass
class FakeState:
    tool_calls: Counter = field(default_factory=Counter)
    tool_delay: float = 0.0
    # Per-tool scripted outcomes, consumed in order; an exception is raised,
    # a string is returned. Default (empty) is success.
    tool_script: dict[str, list[Exception | str]] = field(default_factory=dict)


FAKE_STATE = FakeState()


def reset_fakes() -> None:
    FAKE_STATE.tool_calls.clear()
    FAKE_STATE.tool_delay = 0.0
    FAKE_STATE.tool_script.clear()
    PolicyModel.calls.clear()


def _call(call_id: str, name: str, args: dict) -> AIMessage:
    return AIMessage(content="", tool_calls=[{"id": call_id, "name": name, "args": args}])


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
                return "supervisor", _call(call_id, "task", {
                    "subagent_type": "anchor_specialist",
                    "description": "Anchor NF1 and doxorubicin to CURIEs.",
                })
            if not done["write_file"]:
                return "supervisor", _call(call_id, "write_file", {
                    "file_path": "/workspace/report.md",
                    "content": "# NF1 report\nHGNC:7765",
                })
            return "supervisor", AIMessage(content="DONE: report written to /workspace/report.md")
        if self.mode == "happy" and not done["think_tool"]:
            # think_tool is sync and pure: it runs in the workflow, not as an activity.
            return "subagent", _call(call_id, "think_tool", {"reflection": "Resolve NF1 first."})
        if self.mode == "runaway" or not done["hgnc_search_genes"]:
            return "subagent", _call(call_id, "hgnc_search_genes", {"query": "NF1"})
        return "subagent", AIMessage(content="Anchored NF1 -> HGNC:7765")

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        role, message = self._reply(messages)
        PolicyModel.calls.append({"role": role, "kwargs": kwargs})
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        return self._generate(messages, **kwargs)


async def fake_call_tool(tool_name: str, arguments: dict, apply_rate_limit: bool = True) -> str:
    FAKE_STATE.tool_calls[tool_name] += 1
    await asyncio.sleep(FAKE_STATE.tool_delay)
    script = FAKE_STATE.tool_script.get(tool_name)
    if script:
        outcome = script.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
    return f"{tool_name}: HGNC:7765 NF1 neurofibromin 1"
