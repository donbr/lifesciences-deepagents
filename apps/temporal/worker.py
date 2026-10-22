"""Run a worker for the Life Sciences research workflow.

    uv run python -m apps.temporal.worker

Under Temporal every model/tool activity would become its own LangSmith trace
(hundreds per run), so the worker disables LangSmith tracing by default.
Temporal history (and ``scripts/temporal_run_report.py``) is the record of a
run. Set ``LIFESCIENCES_TEMPORAL_TRACE=1`` to trace anyway.
"""

import asyncio
import os
from collections.abc import MutableMapping

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker

from apps.temporal.durable import make_plugin
from apps.temporal.workflow import LifesciencesResearchWorkflow

TASK_QUEUE = "lifesciences-research"


def configure_tracing(env: MutableMapping[str, str]) -> bool:
    """Turn LangSmith tracing off unless LIFESCIENCES_TEMPORAL_TRACE=1.

    Returns True if tracing settings were left as the operator configured them.
    """
    if env.get("LIFESCIENCES_TEMPORAL_TRACE") == "1":
        return True
    env["LANGSMITH_TRACING"] = "false"
    env["LANGCHAIN_TRACING_V2"] = "false"
    return False


async def main() -> None:
    load_dotenv()
    if configure_tracing(os.environ):
        print("LangSmith tracing: ON (LIFESCIENCES_TEMPORAL_TRACE=1); expect one trace per activity.")
    else:
        print("LangSmith tracing: OFF for this worker (set LIFESCIENCES_TEMPORAL_TRACE=1 to enable).")
    client = await Client.connect(
        os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
        plugins=[make_plugin()],
    )
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[LifesciencesResearchWorkflow],
    )
    print(f"Worker started on {TASK_QUEUE}. Ctrl+C to exit.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
