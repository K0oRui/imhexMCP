from tools import HANDLERS, TOOLS

KNOWN_ALIASES = {
    "entropy",
    "magic",
    "strings",
    "statistics",
    "disassemble",
    "search_multi",
    "export_search",
    "add_bookmark",
    "file_list",
    "read_data",
    "write_data",
}


def test_tools_registered():
    assert len(TOOLS) > 0


def test_handlers_match_tools():
    tool_names = {t.name for t in TOOLS}
    handler_names = set(HANDLERS.keys())
    missing_tools = handler_names - tool_names - KNOWN_ALIASES
    assert not missing_tools, f"Handlers with no tool: {missing_tools}"
    missing_handlers = tool_names - handler_names
    assert not missing_handlers, f"Tools with no handler: {missing_handlers}"


def test_each_tool_has_schema():
    for tool in TOOLS:
        assert tool.inputSchema is not None
        assert "type" in tool.inputSchema
        assert "properties" in tool.inputSchema
