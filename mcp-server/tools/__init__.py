from mcp.types import Tool

from . import file_ops, analysis, search, bookmarks, batch, extra

TOOLS: list[Tool] = []
HANDLERS: dict[str, callable] = {}

for mod in (file_ops, analysis, search, bookmarks, batch, extra):
    TOOLS.extend(mod.TOOLS)
    HANDLERS.update(mod.HANDLERS)
