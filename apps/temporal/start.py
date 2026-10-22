"""Start one research run and print the answer.

    uv run python -m apps.temporal.start "What genes ... NF1?"

Config (runtime root, skills, today's date) is resolved here, client-side, and
passed to the workflow so the workflow never reads disk, env or the clock.
"""

import asyncio
import os
import sys
import uuid

from dotenv import load_dotenv
from temporalio.client import Client

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from agent_factory import resolve_agent_config
from apps.temporal.durable import make_plugin
from apps.temporal.storage import payload_storage_from_env
from apps.temporal.workflow import LifesciencesResearchWorkflow, ResearchInput
from apps.temporal.worker import TASK_QUEUE


async def main() -> None:
    load_dotenv()
    question = " ".join(sys.argv[1:]) or (
        "What known genes or pathways are implicated in minimizing Doxorubicin "
        "toxicity while preserving its anti-tumor efficacy for NF1?"
    )
    # With storage configured, use the same plugin and storage as the worker so large
    # payloads decode (see storage.py); otherwise the plain client, as before.
    async with payload_storage_from_env(os.environ) as converter:
        client = await Client.connect(
            os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
            plugins=[make_plugin(data_converter=converter)] if converter else [],
        )
        workflow_id = f"lifesciences-{uuid.uuid4()}"
        print(f"Workflow: {workflow_id}")
        result = await client.execute_workflow(
            LifesciencesResearchWorkflow.run,
            ResearchInput(question=question, config=resolve_agent_config()),
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )
    print(result.answer)
    for path in sorted(result.workspace_files):
        print(f"  {path}")


if __name__ == "__main__":
    asyncio.run(main())
