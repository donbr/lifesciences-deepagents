import os
from pathlib import Path

import pytest
from temporalio.testing import ActivityEnvironment

from agent_factory import DEFAULT_MODEL, supervisor_prompt
from apps.temporal.workflow import LoopLimits

from .conftest import run_agent
from .fakes import PolicyModel


async def test_cache_control_reaches_every_model_activity(client):
    await run_agent(client, "happy", LoopLimits())
    assert PolicyModel.calls, "no model calls recorded"
    for call in PolicyModel.calls:
        assert call["kwargs"].get("cache_control", {}).get("type") == "ephemeral", call["role"]


async def test_non_anthropic_model_gets_no_cache_control(client):
    await run_agent(client, "happy", LoopLimits(), model_name="openai:happy")
    assert PolicyModel.calls, "no model calls recorded"
    assert all("cache_control" not in c["kwargs"] for c in PolicyModel.calls)


@pytest.mark.live
async def test_live_second_call_reads_cache():
    """Cost: two Sonnet calls, ~2.5k cached input tokens, well under $0.05."""
    from dotenv import load_dotenv
    from langchain_core.load import dumpd
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain.chat_models import init_chat_model
    from temporalio.deepagents._activity import DeepAgentActivities, ModelActivityInput
    from temporalio.deepagents import _serde

    if not os.environ.get("ANTHROPIC_API_KEY"):
        load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set")

    system = supervisor_prompt("2026-10-21")
    while len(system) < 16_000:  # ~4k tokens, above the 2,048-token minimum
        system += "\n\n" + supervisor_prompt("2026-10-21")
    activities = DeepAgentActivities()
    env = ActivityEnvironment()

    async def call():
        out = await env.run(
            activities.invoke_model,
            ModelActivityInput(
                model_name=DEFAULT_MODEL,
                messages=[dumpd(SystemMessage(content=system)), dumpd(HumanMessage(content="Reply with the single word: ok"))],
                bind_kwargs={"cache_control": {"type": "ephemeral"}, "max_tokens": 16},
            ),
        )
        return _serde.load_messages([out.message])[0]

    await call()
    second = await call()
    details = second.usage_metadata["input_token_details"]
    print("second call input_token_details:", details)
    assert details["cache_read"] > 0
