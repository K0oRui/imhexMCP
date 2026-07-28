from collections.abc import Callable

from mcp.types import Tool

from . import analysis, batch, bookmarks, extra, file_ops, search

TOOLS: list[Tool] = []
HANDLERS: dict[str, Callable] = {}

for mod in (file_ops, analysis, search, bookmarks, batch, extra):
    TOOLS.extend(mod.TOOLS)
    HANDLERS.update(mod.HANDLERS)
