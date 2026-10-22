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
