"""Structural decisions for the deepagents 0.7 parity (see the remediation plan, Task 6)."""

import re

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from agent_factory import DEFAULT_MODEL, build_lifesciences_agent, resolve_agent_config, supervisor_prompt
from shared import prompts
from tests.temporal.fakes import PolicyModel


def test_prompt_workspace_paths_are_absolute():
    texts = {
        name: value
        for name, value in vars(prompts).items()
        if isinstance(value, str) and name.isupper()
    }
    texts["supervisor_prompt"] = supervisor_prompt("2026-10-21")
    for name, text in texts.items():
        relative = re.findall(r"(?<!/)workspace/", text)
        assert not relative, f"{name} has a relative workspace/ path"
    assert "/workspace/" in prompts.PERSIST_SYSTEM
    assert "/workspace/" in texts["supervisor_prompt"]


def test_supervisor_has_no_write_todos():
    # Decision R4 (plan Task 6, 6a): write_todos stays out; re-adding must be deliberate.
    agent = build_lifesciences_agent(resolve_agent_config(), model=PolicyModel(mode="happy"))
    assert "write_todos" not in agent.nodes["tools"].bound.tools_by_name


def test_default_model_is_the_alias():
    assert DEFAULT_MODEL == "anthropic:claude-sonnet-4-5"
