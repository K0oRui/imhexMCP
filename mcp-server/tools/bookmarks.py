from mcp.types import Tool
from client import ImHexClient

TOOLS = [
    Tool(name="bookmark_add", description="Add a bookmark to a specific location in the file", inputSchema={"type": "object", "properties": {"offset": {"type": "integer", "description": "Offset of the bookmark", "minimum": 0}, "size": {"type": "integer", "description": "Size of the bookmarked region", "minimum": 1}, "name": {"type": "string", "description": "Name for the bookmark"}, "color": {"type": "string", "description": "Hex color (e.g. FF0000)", "pattern": "^[0-9A-Fa-f]{6}$"}}, "required": ["offset", "size", "name"]}),
    Tool(name="remove_bookmark", description="Remove a bookmark by its ID", inputSchema={"type": "object", "properties": {"id": {"type": "integer", "description": "Bookmark ID to remove", "minimum": 0}}, "required": ["id"]}),
    Tool(name="add_bookmark", description="Alias for bookmark_add", inputSchema={"type": "object", "properties": {"offset": {"type": "integer", "description": "Offset of the bookmark", "minimum": 0}, "size": {"type": "integer", "description": "Size of the bookmarked region", "minimum": 1}, "name": {"type": "string", "description": "Name for the bookmark"}, "color": {"type": "string", "description": "Hex color (e.g. FF0000)", "pattern": "^[0-9A-Fa-f]{6}$"}}, "required": ["offset", "size", "name"]}),
    Tool(name="list_bookmarks", description="List all bookmarks", inputSchema={"type": "object", "properties": {}, "required": []}),
]


def handle_bookmark_add(client: ImHexClient, args: dict) -> str:
    bid = client.send_command("bookmark/add", args).get("data", {}).get("id", "?")
    return f"Bookmark added: '{args['name']}' at 0x{args['offset']:X} (ID: {bid})"


def handle_remove_bookmark(client: ImHexClient, args: dict) -> str:
    client.send_command("bookmark/remove", {"id": args["id"]})
    return f"Bookmark removed (ID: {args['id']})"


def handle_list_bookmarks(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("bookmark/list").get("data", {})
    bookmarks = d.get("bookmarks", [])
    if not bookmarks:
        return "No bookmarks"
    lines = [f"Bookmarks ({d.get('count', 0)}):"]
    for b in bookmarks:
        lines.append(f"  ID {b.get('id')}: '{b.get('name', '')}' @ 0x{b.get('offset', 0):X} ({b.get('size', 0)} bytes)")
    return "\n".join(lines)


HANDLERS = {
    "bookmark_add": handle_bookmark_add,
    "remove_bookmark": handle_remove_bookmark,
    "add_bookmark": handle_bookmark_add,
    "list_bookmarks": handle_list_bookmarks,
}
