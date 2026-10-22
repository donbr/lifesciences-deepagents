"""Worker tracing configuration (offline: plain dicts, no Temporal server)."""

from apps.temporal.worker import configure_tracing


def test_tracing_disabled_by_default():
    env = {"LANGSMITH_TRACING": "true"}
    assert configure_tracing(env) is False
    assert env["LANGSMITH_TRACING"] == "false"
    assert env["LANGCHAIN_TRACING_V2"] == "false"


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
    ls_utils.get_env_var.cache_clear()
    try:
        assert ls_utils.tracing_is_enabled()  # primes the cache with True
        assert configure_tracing(os.environ) is False
        assert not ls_utils.tracing_is_enabled()
        assert not _tracing_v2_is_enabled()
    finally:
        monkeypatch.undo()
        ls_utils.get_env_var.cache_clear()
