"""Optional S3 External Storage for large agent payloads.

Temporal rejects payloads over 2 MB by default and histories over 50 MB; a real
run produced ~10 MB of history. With External Storage, payloads above a size
threshold are written to S3 and history keeps only a small reference.

Enabled by env ``TEMPORAL_PAYLOAD_S3_BUCKET`` (optional
``TEMPORAL_PAYLOAD_S3_ENDPOINT`` for a local moto/minio endpoint). Read host-side
only, never in workflow code. Unset, nothing changes and ``aioboto3`` is not
imported (install it with ``uv sync --group external-storage``).

EVERY client that reads a run's history or result (worker, start, report script)
must use the same storage, or it cannot decode the payloads.
"""

from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from dataclasses import replace

from temporalio.converter import DataConverter, ExternalStorage

BUCKET_ENV = "TEMPORAL_PAYLOAD_S3_BUCKET"
ENDPOINT_ENV = "TEMPORAL_PAYLOAD_S3_ENDPOINT"
_LOCAL_HOSTS = ("localhost", "127.0.0.1", "[::1]")


def _is_local(endpoint: str) -> bool:
    host = endpoint.split("://", 1)[-1].split("/", 1)[0].rsplit(":", 1)[0]
    return host in _LOCAL_HOSTS or host.strip("[]") == "::1"


@asynccontextmanager
async def payload_storage(endpoint: str | None, bucket: str) -> AsyncIterator[DataConverter]:
    """Yield a DataConverter with S3 External Storage.

    The S3 client must stay open while Temporal reads and writes payloads, so keep
    the ``async with`` around the client and worker. With ``endpoint`` None this is
    real S3 using the normal AWS credential chain. A custom endpoint is accepted
    only on localhost (moto/minio); it uses throwaway test credentials unless
    ``AWS_ACCESS_KEY_ID`` is already set.
    """
    if endpoint is not None and not _is_local(endpoint):
        raise ValueError(f"custom S3 endpoint must be local (localhost); got {endpoint!r}")

    import os

    import aioboto3
    from temporalio.contrib.aws.s3driver import S3StorageDriver
    from temporalio.contrib.aws.s3driver.aioboto3 import new_aioboto3_client

    kwargs: dict = {}
    if endpoint is not None:
        kwargs["endpoint_url"] = endpoint
        if not os.environ.get("AWS_ACCESS_KEY_ID"):
            kwargs.update(
                aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1"
            )
    async with aioboto3.Session().client("s3", **kwargs) as s3_client:
        driver = S3StorageDriver(client=new_aioboto3_client(s3_client), bucket=bucket)
        storage = ExternalStorage(drivers=[driver])
        yield replace(DataConverter.default, external_storage=storage)


@asynccontextmanager
async def payload_storage_from_env(env: Mapping[str, str]) -> AsyncIterator[DataConverter | None]:
    """``payload_storage`` per the env vars above; yields None when unset (disabled)."""
    bucket = env.get(BUCKET_ENV)
    if not bucket:
        yield None
        return
    async with payload_storage(env.get(ENDPOINT_ENV) or None, bucket) as converter:
        yield converter
