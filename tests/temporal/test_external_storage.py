"""Large tool results go to S3 External Storage, not workflow history.

Needs moto (dev group) and aioboto3 (``uv sync --group external-storage``);
skipped cleanly without them.
"""

import socket
import uuid
from collections.abc import Iterator
from dataclasses import replace
from datetime import timedelta

import pytest
import pytest_asyncio
boto3 = pytest.importorskip("boto3", reason="needs moto (dev uv group)")
pytest.importorskip("aioboto3", reason="needs the external-storage uv group")
moto_server = pytest.importorskip("moto.server", reason="needs moto (dev uv group)")

from temporalio.api.enums.v1 import EventType
from temporalio.api.sdk.v1 import ExternalStorageReference
from temporalio.client import Client, WorkflowFailureError
from temporalio.converter import DataConverter

from agent_factory import resolve_agent_config
from apps.temporal.durable import make_plugin
from apps.temporal.storage import payload_storage
from apps.temporal.workflow import LifesciencesResearchWorkflow, LoopLimits, ResearchInput
from shared import mcp

from .conftest import _worker
from .fakes import FAKE_STATE, PolicyModel, fake_call_tool, reset_fakes

BUCKET = "test-payloads"
BIG = 3 * 1024 * 1024
INVOKE_TOOL = "deepagents.invoke_tool"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def s3_endpoint() -> Iterator[str]:
    server = moto_server.ThreadedMotoServer(ip_address="127.0.0.1", port=_free_port(), verbose=False)
    server.start()
    try:
        host, port = server.get_host_and_port()
        endpoint = f"http://{host}:{port}"
        boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        ).create_bucket(Bucket=BUCKET)
        yield endpoint
    finally:
        server.stop()


def _plugin(data_converter=None):
    return make_plugin(
        model_provider=lambda name: PolicyModel(mode=name.split(":", 1)[1]),
        data_converter=data_converter,
    )


@pytest_asyncio.fixture
async def stored_client(env, monkeypatch, s3_endpoint):
    reset_fakes()
    monkeypatch.setattr(mcp.lifesciences_client, "call_tool", fake_call_tool)
    async with payload_storage(s3_endpoint, BUCKET) as converter:
        assert converter is not None
        yield await Client.connect(
            env.client.service_client.config.target_host,
            namespace=env.client.namespace,
            plugins=[_plugin(converter)],
        )


async def _start(client: Client):
    task_queue = f"lifesciences-storage-{uuid.uuid4()}"
    config = replace(resolve_agent_config(), model_name="anthropic:happy")
    request = ResearchInput(question="NF1", config=config, limits=LoopLimits())
    handle = await client.start_workflow(
        LifesciencesResearchWorkflow.run,
        request,
        id=task_queue,
        task_queue=task_queue,
        execution_timeout=timedelta(seconds=60),
    )
    return task_queue, handle


async def test_large_tool_result_is_offloaded(stored_client):
    FAKE_STATE.tool_script["hgnc_search_genes"] = ["x" * BIG]
    task_queue, handle = await _start(stored_client)
    async with _worker(stored_client, task_queue):
        result = await handle.result()
    assert result.answer

    events = [e async for e in handle.fetch_history_events()]
    assert sum(e.ByteSize() for e in events) < 1_000_000

    scheduled = {
        e.event_id: e.activity_task_scheduled_event_attributes.activity_type.name
        for e in events
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED
    }
    tool_results = [
        e.activity_task_completed_event_attributes.result.payloads[0]
        for e in events
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED
        and scheduled[e.activity_task_completed_event_attributes.scheduled_event_id] == INVOKE_TOOL
    ]
    references = [
        p
        for p in tool_results
        if isinstance(DataConverter.default.payload_converter.from_payload(p), ExternalStorageReference)
    ]
    assert len(references) == 1, "exactly the 3 MiB tool result is stored externally"
    assert references[0].ByteSize() < 1024
    assert all(p.ByteSize() < 100_000 for p in tool_results if p not in references)
    assert FAKE_STATE.tool_calls["hgnc_search_genes"] == 1


async def test_large_tool_result_without_storage_cannot_be_recorded(client):
    """RED evidence: with no storage, the 3 MiB result exceeds Temporal's 2 MB payload limit.

    The SDK cannot report the activity result (TMPRL1103), so the tool activity
    fails and nothing near 3 MiB is ever recorded in history.
    """
    FAKE_STATE.tool_script["hgnc_search_genes"] = ["x" * BIG] * 10
    task_queue, handle = await _start(client)
    async with _worker(client, task_queue):
        try:
            await handle.result()
        except WorkflowFailureError:
            pass
    events = [e async for e in handle.fetch_history_events()]
    assert max(e.ByteSize() for e in events) < BIG
    scheduled = {
        e.event_id: e.activity_task_scheduled_event_attributes.activity_type.name
        for e in events
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED
    }
    completed = [
        e
        for e in events
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_COMPLETED
        and scheduled[e.activity_task_completed_event_attributes.scheduled_event_id] == INVOKE_TOOL
        and e.activity_task_completed_event_attributes.result.ByteSize() > 1_000_000
    ]
    assert not completed
    failures = [
        e.activity_task_failed_event_attributes.failure.message
        for e in events
        if e.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_FAILED
    ]
    assert any("TMPRL1103" in m for m in failures), failures
    assert FAKE_STATE.tool_calls["hgnc_search_genes"] >= 2, "the tool activity retried"
