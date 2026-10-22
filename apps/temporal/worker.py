"""Run a worker for the Life Sciences research workflow.

    uv run python -m apps.temporal.worker
"""

import asyncio
import os

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker

from apps.temporal.durable import make_plugin
from apps.temporal.workflow import LifesciencesResearchWorkflow

TASK_QUEUE = "lifesciences-research"


async def main() -> None:
    load_dotenv()
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
