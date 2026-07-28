from tools import HANDLERS, TOOLS


def test_tools_registered():
    assert len(TOOLS) > 0


def test_handlers_match_tools():
    tool_names = {t.name for t in TOOLS}
    handler_names = set(HANDLERS.keys())
    assert (
        tool_names == handler_names
    ), f"Mismatch: tools={tool_names - handler_names}, extra_handlers={handler_names - tool_names}"


def test_each_tool_has_schema():
    for tool in TOOLS:
        assert tool.inputSchema is not None
        assert "type" in tool.inputSchema
        assert "properties" in tool.inputSchema
