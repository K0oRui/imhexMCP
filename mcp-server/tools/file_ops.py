from pathlib import Path

from client import ImHexClient
from mcp.types import Tool

TOOLS = [
    Tool(
        name="get_capabilities",
        description="Get ImHex build version, commit, branch, and available commands",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="set_pattern_code",
        description="Set pattern language code in ImHex for binary data parsing",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Pattern language code"}
            },
            "required": ["code"],
        },
    ),
    Tool(
        name="open_file",
        description="Open a file in ImHex for analysis",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to open"}
            },
            "required": ["path"],
        },
    ),
    Tool(
        name="list_files",
        description="List all currently open files in ImHex",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="switch_file",
        description="Switch the active file/provider in ImHex",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID to switch to",
                    "minimum": 0,
                }
            },
            "required": ["provider_id"],
        },
    ),
    Tool(
        name="close_file",
        description="Close a specific file/provider in ImHex",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID to close",
                    "minimum": 0,
                }
            },
            "required": ["provider_id"],
        },
    ),
    Tool(
        name="compare_files",
        description="Compare two open files at byte level",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id_1": {
                    "type": "integer",
                    "description": "First provider ID",
                    "minimum": 0,
                },
                "provider_id_2": {
                    "type": "integer",
                    "description": "Second provider ID",
                    "minimum": 0,
                },
            },
            "required": ["provider_id_1", "provider_id_2"],
        },
    ),
    Tool(
        name="provider_info",
        description="Get information about the currently open file/provider",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="export_data",
        description="Export a region of data to a file",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "length": {
                    "type": "integer",
                    "description": "Bytes to export",
                    "minimum": 1,
                    "maximum": 104857600,
                },
                "output_path": {"type": "string", "description": "Output file path"},
                "format": {
                    "type": "string",
                    "enum": ["binary", "hex", "base64"],
                    "description": "Export format",
                },
            },
            "required": ["offset", "length", "output_path"],
        },
    ),
    Tool(
        name="list_providers",
        description="List all providers with their IDs",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="save_file",
        description="Save the current file to disk",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Optional path to save as (save-as)",
                }
            },
            "required": [],
        },
    ),
    Tool(
        name="undo",
        description="Undo the last write operation",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="redo",
        description="Redo the last undone operation",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="undo_status",
        description="Check if undo/redo is available",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="create_file",
        description="Create a new empty file provider",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="mem_new_provider",
        description="Create an in-memory provider from hex data",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Hex data to load"},
                "name": {"type": "string", "description": "Optional provider name"},
            },
            "required": ["data"],
        },
    ),
    Tool(
        name="patch_export",
        description="Export patches to IPS format",
        inputSchema={
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["ips", "ips32"],
                    "description": "Patch format",
                    "default": "ips",
                }
            },
            "required": [],
        },
    ),
    Tool(
        name="bookmark_edit",
        description="Edit an existing bookmark by ID",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Bookmark ID to edit"},
                "name": {"type": "string", "description": "New name"},
                "comment": {"type": "string", "description": "New comment"},
                "color": {
                    "type": "string",
                    "description": "New RGBA hex color (e.g. FF0000FF)",
                    "pattern": "^[0-9A-Fa-f]{8}$",
                },
                "offset": {
                    "type": "integer",
                    "description": "New offset",
                    "minimum": 0,
                },
                "size": {"type": "integer", "description": "New size", "minimum": 1},
            },
            "required": ["id"],
        },
    ),
]


def handle_get_capabilities(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("imhex/capabilities").get("data", {})
    return (
        f"ImHex {d.get('version', '?')}  "
        f"Commit: {d.get('commit', '?')}  "
        f"Branch: {d.get('branch', '?')}  "
        f"Commands: {d.get('available_commands', d.get('commands', '?'))}"
    )


def handle_set_pattern_code(client: ImHexClient, args: dict) -> str:
    client.send_command("pattern_editor/set_code", {"code": args["code"]})
    return "Pattern code set successfully"


def handle_open_file(client: ImHexClient, args: dict) -> str:
    fp = Path(args["path"])
    if not fp.exists():
        return f"Error: file not found: {args['path']}"
    client.send_command("file/open", {"path": str(fp.absolute())})
    return f"File open requested: {args['path']}"


def handle_list_files(client: ImHexClient, _args: dict) -> str:
    files = client.send_command("file/list", {}).get("data", {}).get("files", [])
    if not files:
        return "No files open"
    lines = [f"Open files ({len(files)}):"]
    for f in files:
        active = " [ACTIVE]" if f.get("is_active") else ""
        lines.append(
            f"  ID {f.get('id')}: {f.get('name')}{active}  ({f.get('size', 0):,} bytes)"
        )
    return "\n".join(lines)


def handle_switch_file(client: ImHexClient, args: dict) -> str:
    d = client.send_command("file/switch", {"provider_id": args["provider_id"]}).get(
        "data", {}
    )
    return f"Switched to: {d.get('name', '')} (ID {args['provider_id']})  Size: {d.get('size', 0):,} bytes"


def handle_close_file(client: ImHexClient, args: dict) -> str:
    name = (
        client.send_command("file/close", {"provider_id": args["provider_id"]})
        .get("data", {})
        .get("name", "")
    )
    return f"Closed: {name} (ID {args['provider_id']})"


def handle_compare_files(client: ImHexClient, args: dict) -> str:
    d = client.send_command("file/compare", args).get("data", {})
    c = d.get("comparison", {})
    return (
        f"File 1: {d.get('file1', {}).get('name', '?')}  File 2: {d.get('file2', {}).get('name', '?')}\n"
        f"Bytes compared: {c.get('bytes_compared', 0):,}  Differences: {c.get('differences', 0):,}  Similarity: {c.get('similarity_percent', 0):.2f}%"
    )


def handle_provider_info(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("provider/info").get("data", {})
    if not d.get("valid"):
        return "No file is currently open"
    return f"Name: {d.get('name', '?')}  Size: {d.get('size', 0):,} bytes\nWritable: {d.get('writable')}  Readable: {d.get('readable')}  Modified: {d.get('dirty')}"


def handle_export_data(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/export", args).get("data", {})
    return f"Exported {d.get('length', 0):,} bytes to {d.get('output_path', args['output_path'])}"


def handle_list_providers(client: ImHexClient, _args: dict) -> str:
    files = client.send_command("file/list", {}).get("data", {}).get("files", [])
    if not files:
        return "No providers"
    lines = [f"Providers ({len(files)}):"]
    for f in files:
        lines.append(
            f"  ID {f.get('id')}: {f.get('name')}  ({f.get('size', 0):,} bytes)"
        )
    return "\n".join(lines)


def handle_save_file(client: ImHexClient, args: dict) -> str:
    params = {}
    if args.get("path"):
        params["path"] = args["path"]
    d = client.send_command("file/save", params).get("data", {})
    return f"Saved: {d.get('name', '?')}"


def handle_undo(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("undo").get("data", {})
    return f"Undone. Can undo: {d.get('can_undo')}, Can redo: {d.get('can_redo')}"


def handle_redo(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("redo").get("data", {})
    return f"Redone. Can undo: {d.get('can_undo')}, Can redo: {d.get('can_redo')}"


def handle_undo_status(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("undo/status").get("data", {})
    return f"Can undo: {d.get('can_undo')}, Can redo: {d.get('can_redo')}"


def handle_create_file(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("file/create").get("data", {})
    if d.get("success"):
        return f"Created file provider: ID {d.get('provider_id')} - {d.get('name', '')}"
    return "Failed to create file provider"


def handle_mem_new_provider(client: ImHexClient, args: dict) -> str:
    params = {"data": args["data"]}
    if args.get("name"):
        params["name"] = args["name"]
    d = client.send_command("mem/new_provider", params).get("data", {})
    if d.get("success"):
        return f"Created memory provider: {d.get('name')} ({d.get('size')} bytes)"
    return "Failed to create memory provider"


def handle_patch_export(client: ImHexClient, args: dict) -> str:
    d = client.send_command("patch/export", {"format": args.get("format", "ips")}).get(
        "data", {}
    )
    if d.get("success"):
        patch = d.get("patch_data", "")
        size = d.get("patch_size", 0)
        patch_count = d.get("total_patches", 0)
        fmt = d.get("format", "ips")
        lines = [
            f"Patch export ({fmt.upper()}):",
            f"  Total patches: {patch_count}",
            f"  Patch file size: {size} bytes",
            f"  Data: {patch[:128]}{'...' if len(patch) > 128 else ''}",
        ]
        return "\n".join(lines)
    return f"Patch export failed: {d.get('error', 'unknown')}"


def handle_bookmark_edit(client: ImHexClient, args: dict) -> str:
    params = {"id": args["id"]}
    for k in ("name", "comment", "offset", "size"):
        if k in args:
            params[k] = args[k]
    if "color" in args:
        params["color"] = int(args["color"], 16)
    d = client.send_command("bookmark/edit", params).get("data", {})
    if d.get("success"):
        return f"Bookmark {args['id']} edited successfully (new ID: {d.get('new_id', args['id'])})"
    return f"Failed to edit bookmark: {d.get('note', d.get('error', 'unknown'))}"


HANDLERS = {
    "get_capabilities": handle_get_capabilities,
    "set_pattern_code": handle_set_pattern_code,
    "open_file": handle_open_file,
    "list_files": handle_list_files,
    "switch_file": handle_switch_file,
    "close_file": handle_close_file,
    "compare_files": handle_compare_files,
    "provider_info": handle_provider_info,
    "export_data": handle_export_data,
    "list_providers": handle_list_providers,
    "save_file": handle_save_file,
    "undo": handle_undo,
    "redo": handle_redo,
    "undo_status": handle_undo_status,
    "create_file": handle_create_file,
    "mem_new_provider": handle_mem_new_provider,
    "patch_export": handle_patch_export,
    "bookmark_edit": handle_bookmark_edit,
}
