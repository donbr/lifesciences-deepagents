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
from apps.temporal.storage import payload_storage_from_env
from apps.temporal.workflow import LifesciencesResearchWorkflow

TASK_QUEUE = "lifesciences-research"


def configure_tracing(env: MutableMapping[str, str]) -> bool:
    """Turn LangSmith tracing off unless LIFESCIENCES_TEMPORAL_TRACE=1.

    Returns whether tracing is opted in (True) or disabled (False).
    """
    opted_in = env.get("LIFESCIENCES_TEMPORAL_TRACE") == "1"
    if not opted_in:
        env["LANGSMITH_TRACING"] = "false"
        env["LANGCHAIN_TRACING_V2"] = "false"
    # langsmith caches env lookups (populated at import time, before load_dotenv
    # and this override), so drop the cache for the new values to be seen.
    try:
        from langsmith import utils as ls_utils

        ls_utils.get_env_var.cache_clear()
    except (ImportError, AttributeError):
        pass
    return opted_in


async def main() -> None:
    load_dotenv()
    if configure_tracing(os.environ):
        print("LangSmith tracing: ON (LIFESCIENCES_TEMPORAL_TRACE=1); expect one trace per activity.")
    else:
        print("LangSmith tracing: OFF for this worker (set LIFESCIENCES_TEMPORAL_TRACE=1 to enable).")
    # Optional S3 External Storage (TEMPORAL_PAYLOAD_S3_BUCKET); the client that
    # starts runs and the report script must use the same storage.
    async with payload_storage_from_env(os.environ) as converter:
        client = await Client.connect(
            os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
            plugins=[make_plugin(data_converter=converter)],
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
