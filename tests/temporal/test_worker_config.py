"""Worker configuration: tracing, activity options (offline, no Temporal server)."""

from datetime import timedelta

import pytest
from temporalio.common import RetryPolicy

from apps.temporal.durable import BACKEND_ACTIVITY_OPTIONS, MODEL_ACTIVITY_OPTIONS
from apps.temporal.worker import configure_tracing


def test_tracing_disabled_by_default():
    env = {"LANGSMITH_TRACING": "true"}
    assert configure_tracing(env) is False
    assert env["LANGSMITH_TRACING"] == "false"
    assert env["LANGCHAIN_TRACING_V2"] == "false"
    assert env["LANGSMITH_TRACING_V2"] == "false"
    assert env["LANGCHAIN_TRACING"] == "false"


def test_tracing_opt_in_leaves_env_untouched():
    env = {"LIFESCIENCES_TEMPORAL_TRACE": "1", "LANGSMITH_TRACING": "true"}
    before = dict(env)
    assert configure_tracing(env) is True
    assert env == before


def test_opt_in_requires_exact_value():
    env = {"LIFESCIENCES_TEMPORAL_TRACE": "0", "LANGSMITH_TRACING": "true"}
    assert configure_tracing(env) is False
    assert env["LANGSMITH_TRACING"] == "false"


def test_override_takes_effect_despite_langsmith_env_cache(monkeypatch):
    """langsmith caches env lookups; the override must clear that cache."""
    import os

    from langchain_core.tracers.context import _tracing_v2_is_enabled
    from langsmith import utils as ls_utils

    monkeypatch.delenv("LIFESCIENCES_TEMPORAL_TRACE", raising=False)
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")
    # langsmith reads LANGSMITH_TRACING_V2 before LANGSMITH_TRACING.
    monkeypatch.setenv("LANGSMITH_TRACING_V2", "true")
    ls_utils.get_env_var.cache_clear()
    try:
        assert ls_utils.tracing_is_enabled()  # primes the cache with True
        assert configure_tracing(os.environ) is False
        assert not ls_utils.tracing_is_enabled()
        assert not _tracing_v2_is_enabled()
    finally:
        monkeypatch.undo()
        ls_utils.get_env_var.cache_clear()


def test_model_retry_budget_outlasts_a_sustained_overload():
    # ~6 minutes of backoff across 10 attempts (5, 10, 20, 40, then 60s x5) before a model call fails.
    assert MODEL_ACTIVITY_OPTIONS == {
        "start_to_close_timeout": timedelta(minutes=5),
        "retry_policy": RetryPolicy(
            initial_interval=timedelta(seconds=5),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=10,
        ),
    }


def test_backend_activities_have_bounded_retries():
    """A deterministic backend exception must not retry forever."""
    assert BACKEND_ACTIVITY_OPTIONS["retry_policy"].maximum_attempts == 3
    assert BACKEND_ACTIVITY_OPTIONS["start_to_close_timeout"] == timedelta(seconds=30)


async def test_payload_storage_disabled_without_bucket_env():
    from apps.temporal.storage import payload_storage_from_env

    async with payload_storage_from_env({}) as converter:
        assert converter is None


async def test_payload_storage_rejects_remote_custom_endpoint():
    from apps.temporal.storage import payload_storage

    with pytest.raises(ValueError, match="local"):
        async with payload_storage("https://s3.example.com", "bucket"):
            pass
