"""MCP client error contract: failures raise a typed MCPCallError, never return text."""

from contextlib import asynccontextmanager
from functools import partial

import httpx
import pytest
from langchain_core.messages import ToolMessage

import apps.temporal  # noqa: F401  (puts apps/api on sys.path)
from agent_factory import all_tools
from shared import mcp
from shared.mcp import HTTPMCPClient, MCPCallError

URL = "https://mcp.test/mcp"


def _client(handler) -> HTTPMCPClient:
    return HTTPMCPClient(URL, transport=httpx.MockTransport(handler))


async def _call(handler, tool_name: str = "hgnc_search_genes"):
    return await _client(handler).call_tool(
        tool_name, {"query": "NF1"}, apply_rate_limit=False
    )


async def test_500_is_retryable():
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(500), "string_search_proteins")
    assert err.value.retryable is True
    assert err.value.service == "string"


async def test_429_is_retryable():
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(429), "chembl_get_compound")
    assert err.value.retryable is True
    assert err.value.service == "chembl"


async def test_timeout_is_retryable():
    def handler(request):
        raise httpx.ReadTimeout("timed out", request=request)

    with pytest.raises(MCPCallError) as err:
        await _call(handler)
    assert err.value.retryable is True
    assert err.value.service == "default"


async def test_408_is_retryable():
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(408), "string_search_proteins")
    assert err.value.retryable is True


@pytest.mark.parametrize("status", [400, 404, 409, 422])
async def test_other_4xx_is_not_retryable(status):
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(status))
    assert err.value.retryable is False


async def test_400_is_not_retryable():
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(400), "string_get_interactions")
    assert err.value.retryable is False
    assert err.value.service == "string"


async def test_jsonrpc_error_is_not_retryable():
    body = 'data: {"jsonrpc":"2.0","error":{"code":-32603,"message":"x"}}'
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(200, text=body))
    assert err.value.retryable is False
    assert err.value.service == "default"


async def test_unparseable_body_is_not_retryable():
    with pytest.raises(MCPCallError) as err:
        await _call(lambda request: httpx.Response(200, text="<html>gateway</html>"))
    assert err.value.retryable is False


async def test_success_returns_text():
    body = (
        'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"content":'
        '[{"type":"text","text":"HGNC:7765 NF1"}]}}'
    )
    assert await _call(lambda request: httpx.Response(200, text=body)) == "HGNC:7765 NF1"


async def test_query_api_direct_follows_http_rules(monkeypatch):
    monkeypatch.setattr(
        mcp.httpx,
        "AsyncClient",
        partial(httpx.AsyncClient, transport=httpx.MockTransport(lambda r: httpx.Response(503))),
    )
    with pytest.raises(MCPCallError) as err:
        await mcp.query_api_direct.coroutine(url="https://api.test/x")
    assert err.value.retryable is True
    assert err.value.service == "default"


async def test_stdio_connection_error_is_retryable(monkeypatch):
    @asynccontextmanager
    async def broken_stdio_client(params):
        raise OSError("npx not found")
        yield  # pragma: no cover

    monkeypatch.setattr(mcp, "stdio_client", broken_stdio_client)
    with pytest.raises(MCPCallError) as err:
        await mcp.pubmed_client.call_tool("pubmed_search_articles", {"queryTerm": "NF1"})
    assert err.value.retryable is True
    assert err.value.service == "pubmed"


async def test_langgraph_host_turns_error_into_error_toolmessage(monkeypatch):
    async def failing_call_tool(tool_name, arguments, apply_rate_limit=True):
        raise MCPCallError("400 Bad Request", service="default", retryable=False)

    monkeypatch.setattr(mcp.lifesciences_client, "call_tool", failing_call_tool)
    message = await all_tools()["hgnc_search_genes"].ainvoke(
        {
            "name": "hgnc_search_genes",
            "args": {"query": "NF1"},
            "id": "call-1",
            "type": "tool_call",
        }
    )
    assert isinstance(message, ToolMessage)
    assert message.status == "error"
    assert message.tool_call_id == "call-1"
    assert "400 Bad Request" in message.content


async def test_persist_to_graphiti_failure_raises(monkeypatch):
    """A failed persist must not look like success to the agent."""
    async def failing_call_tool(tool_name, arguments, apply_rate_limit=True):
        raise MCPCallError("ConnectError calling Graphiti", service="default", retryable=True)

    monkeypatch.setattr(mcp.graphiti_client, "call_tool", failing_call_tool)
    with pytest.raises(MCPCallError) as err:
        await mcp.persist_to_graphiti.coroutine(name="NF1", nodes=[], edges=[])
    assert err.value.retryable is False
    assert "ConnectError calling Graphiti" in str(err.value)


async def test_langgraph_host_reports_failed_persist_as_error(monkeypatch):
    async def failing_call_tool(tool_name, arguments, apply_rate_limit=True):
        raise MCPCallError("ConnectError calling Graphiti", service="default", retryable=True)

    monkeypatch.setattr(mcp.graphiti_client, "call_tool", failing_call_tool)
    message = await all_tools()["persist_to_graphiti"].ainvoke(
        {
            "name": "persist_to_graphiti",
            "args": {"name": "NF1", "nodes": [], "edges": []},
            "id": "call-1",
            "type": "tool_call",
        }
    )
    assert isinstance(message, ToolMessage)
    assert message.status == "error"
    assert "Graphiti" in message.content


def test_temporal_host_tools_raise():
    tools = all_tools(errors_as_content=False)
    assert tools["hgnc_search_genes"] is mcp.hgnc_search_genes
    assert not tools["hgnc_search_genes"].handle_tool_error
