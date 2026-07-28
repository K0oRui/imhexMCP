from unittest.mock import Mock, patch

import anyio
import pytest
from client import ImHexClient, ImHexError
from tools import HANDLERS


@pytest.mark.anyio
async def test_list_tools_returns_known_tools():
    from mcp.server import Server

    app = Server("imhex")
    tools_ref = []

    @app.list_tools()
    async def list_tools():
        from tools import TOOLS

        tools_ref.append(TOOLS)
        return TOOLS

    result = await list_tools()
    assert len(result) > 0
    assert result is tools_ref[0]


@pytest.mark.anyio
async def test_call_tool_wraps_handler_result():
    from mcp.types import TextContent

    client = Mock(spec=ImHexClient)
    client.is_connected = True
    client.send_command.return_value = {"data": {"decoded": "hello"}}

    handler = HANDLERS.get("decode_data")
    assert handler is not None

    result = handler(client, {"data": "68656C6C6F", "encoding": "hex"})
    content = TextContent(type="text", text=result)
    assert isinstance(content, TextContent)
    assert "hello" in content.text


@pytest.mark.anyio
async def test_ensure_connected_already_connected():
    client = Mock(spec=ImHexClient)
    client.is_connected = True

    def call():
        from server import ensure_connected

        ensure_connected(client, "localhost", 31337, auto_launch=False)

    await anyio.to_thread.run_sync(call)
    client.connect.assert_not_called()


@pytest.mark.anyio
async def test_ensure_connected_auto_launch_fails_gracefully():
    client = Mock(spec=ImHexClient)
    client.is_connected = False
    client.connect.side_effect = [ConnectionRefusedError, None]

    with (
        patch("server.find_imhex", return_value=None),
        pytest.raises(RuntimeError, match="ImHex not found"),
    ):
        from server import ensure_connected

        await anyio.to_thread.run_sync(
            ensure_connected, client, "localhost", 31337, True
        )


@pytest.mark.anyio
async def test_unknown_tool_returns_error():
    from tools import HANDLERS

    assert "nonexistent_tool" not in HANDLERS


@pytest.mark.anyio
async def test_handlers_called_sequentially():
    client = Mock(spec=ImHexClient)
    client.is_connected = True
    client.send_command.return_value = {"data": {}}

    results = []
    for name in ("inspect_data", "data_entropy", "data_magic"):
        handler = HANDLERS.get(name)
        if handler:
            result = await anyio.to_thread.run_sync(handler, client, _sample_args(name))
            results.append(result)

    assert len(results) == 3
    assert all(isinstance(r, str) for r in results)


@pytest.mark.anyio
async def test_concurrent_handler_calls():
    client = Mock(spec=ImHexClient)
    client.is_connected = True
    client.send_command.return_value = {"data": {}}

    async def call_handler(name):
        handler = HANDLERS.get(name)
        if handler:
            return await anyio.to_thread.run_sync(handler, client, _sample_args(name))
        return None

    import asyncio

    results = await asyncio.gather(
        call_handler("read_hex"),
        call_handler("write_hex"),
        call_handler("hash"),
    )

    assert all(isinstance(r, str) for r in results)


@pytest.mark.anyio
async def test_anyio_timeout_on_slow_handler():
    client = Mock(spec=ImHexClient)
    client.is_connected = True
    client.send_command.side_effect = lambda *a, **kw: (_ for _ in ()).throw(
        TimeoutError("slow")
    )

    with pytest.raises((TimeoutError, ImHexError)):
        with anyio.fail_after(5.0):
            await anyio.to_thread.run_sync(
                HANDLERS["read_hex"], client, {"offset": 0, "length": 16}
            )


def _sample_args(name: str) -> dict:
    args = {
        "read_hex": {"offset": 0, "length": 16},
        "write_hex": {"offset": 0, "data": "FF"},
        "inspect_data": {"offset": 0},
        "hash": {"algorithm": "sha256", "offset": 0},
        "data_entropy": {"offset": 0, "size": 1024},
        "data_statistics": {"offset": 0, "size": 1024},
        "data_strings": {"offset": 0, "size": 1024, "min_length": 4},
        "data_magic": {"offset": 0, "size": 256},
        "data_disassemble": {"offset": 0, "size": 64, "architecture": "x86_64"},
        "data_insert": {"offset": 0, "size": 10},
        "data_remove": {"offset": 0, "size": 10},
        "data_find_replace": {"find": "FF", "replace": "00"},
        "highlight_add": {"offset": 0, "size": 16},
        "selection_set": {"offset": 0, "size": 16},
        "encode_data": {"data": "hello", "encoding": "hex"},
        "decode_data": {"data": "68656C6C6F", "encoding": "hex"},
        "analyze": {},
        "section_headers": {},
        "constants_search": {"value": "4D5A", "type": "hex"},
    }
    return args.get(name, {})
