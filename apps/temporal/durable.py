"""Worker-side wiring: activity-wrapped tools, the filesystem backend factory, the plugin.

``tool_as_activity`` registers each tool in a process-wide registry that the
``deepagents.invoke_tool`` activity resolves by name, so the wrapping must happen
at import on every worker process, not only inside the workflow. The workflow
imports ``DURABLE_TOOLS`` from here (passed through the sandbox) and the worker
imports this module before it starts.
"""

from datetime import timedelta
from typing import Any

from deepagents.backends import FilesystemBackend
from langchain_core.tools import BaseTool, StructuredTool
from temporalio.common import RetryPolicy
from temporalio.deepagents import DeepAgentsPlugin, tool_as_activity
from temporalio.exceptions import ApplicationError

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from agent_factory import IO_TOOL_NAMES, all_tools
from shared.mcp import MCPCallError

FILESYSTEM_BACKEND = "lifesciences_fs"

MODEL_ACTIVITY_OPTIONS: dict[str, Any] = {
    "start_to_close_timeout": timedelta(minutes=5),
    "retry_policy": RetryPolicy(maximum_attempts=3, initial_interval=timedelta(seconds=5)),
}

# ChEMBL calls use a 120s HTTP timeout in shared.mcp; leave headroom.
# Retryable MCPCallErrors (timeouts, transport errors, 429, 5xx) use these
# attempts; permanent ones fail the activity at once (see _raise_for_activity).
TOOL_ACTIVITY_OPTIONS: dict[str, Any] = {
    "retry_policy": RetryPolicy(maximum_attempts=3, initial_interval=timedelta(seconds=2)),
}
TOOL_TIMEOUT = timedelta(minutes=3)

BACKEND_ACTIVITY_OPTIONS: dict[str, Any] = {
    "start_to_close_timeout": timedelta(seconds=30),
}


def _async_in_workflow(tool: StructuredTool) -> StructuredTool:
    """Give a pure sync tool a coroutine.

    LangChain runs a sync-only tool's ``ainvoke`` via ``run_in_executor``, which
    the workflow event loop rejects (``NotImplementedError``). Pure tools stay in
    the workflow, so they need an async body instead.
    """
    func = tool.func

    async def _arun(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return StructuredTool(
        name=tool.name,
        description=tool.description,
        args_schema=tool.args_schema,
        func=func,
        coroutine=_arun,
    )


def _raise_for_activity(tool: BaseTool) -> StructuredTool:
    """Same tool, but a permanent MCPCallError stops the activity's retries.

    A retryable MCPCallError propagates unchanged and is retried per
    ``TOOL_ACTIVITY_OPTIONS``. This copy is what ``tool_as_activity`` registers,
    so it is the body the ``deepagents.invoke_tool`` activity runs.
    """
    coroutine = tool.coroutine

    async def _arun(*args: Any, **kwargs: Any) -> Any:
        try:
            return await coroutine(*args, **kwargs)
        except MCPCallError as e:
            if e.retryable:
                raise
            raise ApplicationError(str(e), type="MCPCallError", non_retryable=True) from e

    return StructuredTool(
        name=tool.name,
        description=tool.description,
        args_schema=tool.args_schema,
        coroutine=_arun,
    )


def _durable_tools() -> dict[str, Any]:
    # Tools raise on failure; ToolFailureMiddleware turns the activity's final
    # failure into an error message for the agent.
    tools = all_tools(errors_as_content=False)
    for name, tool in tools.items():
        if name in IO_TOOL_NAMES:
            tools[name] = tool_as_activity(
                _raise_for_activity(tool),
                start_to_close_timeout=TOOL_TIMEOUT,
                activity_options=TOOL_ACTIVITY_OPTIONS,
            )
        elif getattr(tool, "coroutine", None) is None:
            tools[name] = _async_in_workflow(tool)
    return tools


DURABLE_TOOLS = _durable_tools()


def filesystem_backend(root_dir: str) -> FilesystemBackend:
    """Named backend factory; runs worker-side for every backend activity."""
    return FilesystemBackend(root_dir=root_dir, virtual_mode=True)


def make_plugin(**kwargs: Any) -> DeepAgentsPlugin:
    """The plugin with this app's backend factory and model defaults.

    Subagent ``model="..."`` strings are routed through the plugin's patched
    ``resolve_model``, so they use these plugin-wide model options.
    """
    kwargs.setdefault("model_activity_options", MODEL_ACTIVITY_OPTIONS)
    return DeepAgentsPlugin(
        backends={FILESYSTEM_BACKEND: filesystem_backend},
        **kwargs,
    )
