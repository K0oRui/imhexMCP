from client import ImHexClient
from mcp.types import Tool

TOOLS = [
    Tool(
        name="read_hex",
        description="Read hex data from the currently open file",
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
                    "description": "Bytes to read",
                    "minimum": 1,
                    "maximum": 1048576,
                },
            },
            "required": ["offset", "length"],
        },
    ),
    Tool(
        name="write_hex",
        description="Write hex data to the currently open file",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "data": {
                    "type": "string",
                    "description": "Hex data to write (e.g. '0A1B2C3D')",
                    "pattern": "^[0-9A-Fa-f]+$",
                },
            },
            "required": ["offset", "data"],
        },
    ),
    Tool(
        name="inspect_data",
        description="Inspect data at an offset (show various type interpretations)",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Offset to inspect",
                    "minimum": 0,
                }
            },
            "required": ["offset"],
        },
    ),
    Tool(
        name="hash",
        description="Calculate hash of data in the currently open file",
        inputSchema={
            "type": "object",
            "properties": {
                "algorithm": {
                    "type": "string",
                    "enum": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],
                    "description": "Hash algorithm",
                },
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "length": {
                    "type": "integer",
                    "description": "Bytes to hash (default: entire file)",
                    "minimum": 1,
                },
            },
            "required": ["algorithm"],
        },
    ),
    Tool(
        name="data_entropy",
        description="Calculate Shannon entropy for a region of data (0-8 bits/byte)",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID (0 = current)",
                    "minimum": 0,
                },
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Bytes to analyze",
                    "minimum": 1,
                    "maximum": 10485760,
                },
            },
        },
    ),
    Tool(
        name="data_statistics",
        description="Calculate byte frequency statistics for a region of data",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID (0 = current)",
                    "minimum": 0,
                },
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Bytes to analyze",
                    "minimum": 1,
                    "maximum": 10485760,
                },
                "include_distribution": {
                    "type": "boolean",
                    "description": "Include full byte distribution",
                },
            },
        },
    ),
    Tool(
        name="data_strings",
        description="Extract ASCII/UTF-16 strings from binary data",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID (0 = current)",
                    "minimum": 0,
                },
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Bytes to scan (0 = entire file)",
                    "minimum": 0,
                    "maximum": 104857600,
                },
                "min_length": {
                    "type": "integer",
                    "description": "Minimum string length",
                    "minimum": 1,
                },
                "type": {
                    "type": "string",
                    "enum": ["ascii", "utf16le", "all"],
                    "description": "String type",
                },
                "max_strings": {
                    "type": "integer",
                    "description": "Max strings to return",
                    "minimum": 1,
                    "maximum": 10000,
                },
            },
        },
    ),
    Tool(
        name="data_magic",
        description="Detect file type using magic number signatures",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID (0 = current)",
                    "minimum": 0,
                },
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Bytes to scan",
                    "minimum": 8,
                    "maximum": 4096,
                },
            },
        },
    ),
    Tool(
        name="data_disassemble",
        description="Disassemble machine code into assembly instructions",
        inputSchema={
            "type": "object",
            "properties": {
                "provider_id": {
                    "type": "integer",
                    "description": "Provider ID (0 = current)",
                    "minimum": 0,
                },
                "offset": {
                    "type": "integer",
                    "description": "Code offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Bytes to disassemble",
                    "minimum": 1,
                    "maximum": 4096,
                },
                "architecture": {
                    "type": "string",
                    "description": "CPU architecture (e.g. x86_64, arm)",
                },
                "base_address": {
                    "type": "integer",
                    "description": "Base address for instruction addresses",
                    "minimum": 0,
                },
            },
        },
    ),
    Tool(
        name="highlight_add",
        description="Add a colored highlight to a region",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {"type": "integer", "description": "Region size", "minimum": 1},
                "color": {
                    "type": "string",
                    "description": "RGBA hex color (e.g. FF0000FF)",
                    "pattern": "^[0-9A-Fa-f]{8}$",
                },
            },
            "required": ["offset", "size"],
        },
    ),
    Tool(
        name="highlight_remove",
        description="Remove a highlight by ID",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Highlight ID to remove",
                    "minimum": 0,
                }
            },
            "required": ["id"],
        },
    ),
    Tool(
        name="selection_get",
        description="Get the current selection range",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="selection_set",
        description="Set the selection range",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Selection size",
                    "minimum": 1,
                },
            },
            "required": ["offset", "size"],
        },
    ),
    Tool(
        name="data_insert",
        description="Insert bytes at offset (shifts data)",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Insert position",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Number of bytes to insert",
                    "minimum": 1,
                },
            },
            "required": ["offset", "size"],
        },
    ),
    Tool(
        name="data_remove",
        description="Remove bytes at offset (shifts data)",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Number of bytes to remove",
                    "minimum": 1,
                },
            },
            "required": ["offset", "size"],
        },
    ),
    Tool(
        name="data_find_replace",
        description="Find and replace a hex pattern",
        inputSchema={
            "type": "object",
            "properties": {
                "find": {"type": "string", "description": "Hex pattern to find"},
                "replace": {"type": "string", "description": "Hex replacement"},
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "length": {
                    "type": "integer",
                    "description": "Length to search",
                    "minimum": 1,
                },
            },
            "required": ["find", "replace"],
        },
    ),
    Tool(
        name="analyze",
        description="One-shot: detect file type, entropy, strings, and hash",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "size": {
                    "type": "integer",
                    "description": "Bytes to analyze (0 = entire file)",
                    "minimum": 0,
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="section_headers",
        description="Parse PE/ELF/Mach-O section headers via pattern language",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="constants_search",
        description="Search file for known constants/magic values",
        inputSchema={
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "Hex value to search for (e.g. '4D5A', '00000001')",
                },
                "type": {
                    "type": "string",
                    "enum": ["hex", "text"],
                    "description": "Search type",
                },
            },
            "required": ["value", "type"],
        },
    ),
]


def handle_read_hex(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/read", args).get("data", {})
    return f"Offset: 0x{args['offset']:X}  Length: {args['length']} bytes\nHex:\n{d.get('data', '')}"


def handle_write_hex(client: ImHexClient, args: dict) -> str:
    client.send_command("data/write", args)
    return f"Wrote {len(args['data']) // 2} bytes at offset 0x{args['offset']:X}"


def handle_inspect_data(client: ImHexClient, args: dict) -> str:
    types_data = (
        client.send_command("data/inspect", args).get("data", {}).get("types", {})
    )
    lines = [f"Data at offset 0x{args['offset']:X}:"]
    for k, v in types_data.items():
        lines.append(f"  {k:12s}: {v}")
    return "\n".join(lines)


def handle_hash(client: ImHexClient, args: dict) -> str:
    params = {"algorithm": args["algorithm"], "offset": args.get("offset", 0)}
    if "length" in args:
        params["length"] = args["length"]
    d = client.send_command("hash/calculate", params).get("data", {})
    if "error" in d:
        return f"Hash error: {d['error']}"
    return f"{args['algorithm'].upper()}: {d.get('hash', '')}"


def handle_data_entropy(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/entropy", args).get("data", {})
    if "error" in d:
        return f"Entropy error: {d['error']}"
    return (
        f"Entropy: {d.get('entropy', 0):.4f} bits/byte  {d.get('interpretation', '')}"
    )


def handle_data_statistics(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/statistics", args).get("data", {})
    if "error" in d:
        return f"Statistics error: {d['error']}"
    lines = [
        f"Unique bytes: {d.get('unique_bytes', 0)}/256",
        f"Most common: 0x{d.get('most_common_byte', 0):02X} ({d.get('most_common_count', 0):,})",
        f"Null bytes: {d.get('null_bytes', 0):,} ({d.get('null_percentage', 0):.1f}%)",
        f"Printable: {d.get('printable_chars', 0):,} ({d.get('printable_percentage', 0):.1f}%)",
    ]
    if args.get("include_distribution") and d.get("distribution"):
        lines.append("Byte distribution (top 10):")
        for bv, cnt in sorted(
            d["distribution"].items(), key=lambda x: int(x[1]), reverse=True
        )[:10]:
            lines.append(f"  0x{int(bv):02X}: {cnt:,}")
    return "\n".join(lines)


def handle_data_strings(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/strings", args).get("data", {})
    if "error" in d:
        return f"Strings error: {d['error']}"
    strings = d.get("strings", [])
    lines = [f"Found {d.get('count', 0)} strings:"]
    for s in strings[:50]:
        v = s.get("value", "")
        if len(v) > 80:
            v = v[:77] + "..."
        lines.append(f'  0x{s.get("offset", 0):08X} [{s.get("type", "")}] "{v}"')
    if d.get("count", 0) > 50:
        lines.append(f"... and {d['count'] - 50} more")
    return "\n".join(lines)


def handle_data_magic(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/magic", args).get("data", {})
    if "error" in d:
        return f"Magic error: {d['error']}"
    matches = d.get("matches", [])
    if not matches:
        return "No known file type signatures detected"
    lines = [f"Matches ({d.get('match_count', 0)}):"]
    for m in matches:
        lines.append(
            f"  {m.get('type', '')} - {m.get('description', '')}  [{m.get('confidence', '')}]"
        )
    return "\n".join(lines)


def handle_data_disassemble(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/disassemble", args).get("data", {})
    if "error" in d:
        result = f"Error: {d['error']}"
        if d.get("available_architectures"):
            result += "\nAvailable: " + ", ".join(d["available_architectures"])
        return result
    instrs = d.get("instructions", [])
    arch = d.get("architecture", args.get("architecture", "x86_64"))
    lines = [f"Architecture: {arch}  Instructions: {len(instrs)}"]
    for i in instrs:
        lines.append(
            f"  {i.get('address', ''):16s} {i.get('bytes', ''):24s} {i.get('mnemonic', '')} {i.get('operands', '')}"
        )
    return "\n".join(lines)


def handle_highlight_add(client: ImHexClient, args: dict) -> str:
    d = client.send_command("highlight/add", args).get("data", {})
    if "error" in d:
        return f"Highlight error: {d['error']}"
    return f"Highlight added: ID {d.get('id')} at 0x{d.get('offset', 0):X} ({d.get('size', 0)} bytes)"


def handle_highlight_remove(client: ImHexClient, args: dict) -> str:
    client.send_command("highlight/remove", {"id": args["id"]}).get("data", {})
    return f"Highlight removed (ID: {args['id']})"


def handle_selection_get(client: ImHexClient, _args: dict) -> str:
    d = client.send_command("selection/get").get("data", {})
    if d.get("valid"):
        return f"Selection: 0x{d.get('offset', 0):X} - 0x{d.get('end', 0):X}  ({d.get('size', 0)} bytes)"
    return "No selection"


def handle_selection_set(client: ImHexClient, args: dict) -> str:
    d = client.send_command("selection/set", args).get("data", {})
    if "error" in d:
        return f"Selection error: {d['error']}"
    return f"Selection set: 0x{d.get('offset', 0):X} ({d.get('size', 0)} bytes)"


def handle_data_insert(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/insert", args).get("data", {})
    if "error" in d:
        return f"Insert error: {d['error']}"
    return f"Inserted {args['size']} bytes at 0x{args['offset']:X}. New size: {d.get('new_size', 0):,}"


def handle_data_remove(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/remove", args).get("data", {})
    if "error" in d:
        return f"Remove error: {d['error']}"
    return f"Removed {args['size']} bytes at 0x{args['offset']:X}. New size: {d.get('new_size', 0):,}"


def handle_data_find_replace(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/find_replace", args).get("data", {})
    if "error" in d:
        return f"Find/replace error: {d['error']}"
    return f"Found {d.get('matches_found', 0)} matches, replaced {d.get('replaced', 0)}"


def handle_analyze(client: ImHexClient, args: dict) -> str:
    offset = args.get("offset", 0)
    size = args.get("size", 0)
    if size == 0:
        info = client.send_command("provider/info").get("data", {})
        if info.get("valid"):
            size = info.get("size", 0)
    lines = []
    magic = client.send_command(
        "data/magic", {"offset": offset, "size": min(size, 4096)}
    ).get("data", {})
    for m in magic.get("matches", []):
        lines.append(f"Type: {m.get('type', '')} - {m.get('description', '')}")
    if not magic.get("matches"):
        lines.append("Type: unknown")
    scan_size = min(size, 10485760)
    ent = client.send_command(
        "data/entropy", {"offset": offset, "size": scan_size}
    ).get("data", {})
    lines.append(
        f"Entropy: {ent.get('entropy', 0):.4f} bits/byte  ({ent.get('interpretation', '')})"
    )
    stats = client.send_command(
        "data/statistics",
        {"offset": offset, "size": scan_size, "include_distribution": False},
    ).get("data", {})
    lines.append(
        f"Unique bytes: {stats.get('unique_bytes', 0)}/256  Null: {stats.get('null_bytes', 0):,} ({stats.get('null_percentage', 0):.1f}%)"
    )
    return "\n".join(lines)


def handle_section_headers(client: ImHexClient, _args: dict) -> str:
    d = client.send_command(
        "pattern/execute",
        {
            "code": """
u16 e_magic @ 0x00;
u32 e_lfanew @ 0x3C;
u16 e_machine @ 0x100;
u16 e_sections @ 0x102;
u32 e_symtab @ 0x104;
u32 e_symcnt @ 0x108;
u16 e_opthdr @ 0x10C;
u16 e_characteristics @ 0x10E;
u16 e_magic_pe @ 0x118;
u16 e_machine_pe @ 0x11C;
u16 e_sections_pe @ 0x120;
u32 e_timedate @ 0x124;
"""
        },
    ).get("data", {})
    if d.get("success"):
        lines = [f"Section headers ({d.get('pattern_count', 0)} fields):"]
        for p in d.get("patterns", []):
            lines.append(
                f"  {p.get('name', '?')} ({p.get('type', '?')}) @ 0x{p.get('offset', 0):X} = {p.get('size', 0)} bytes"
            )
        return "\n".join(lines)
    return f"Failed: {d.get('eval_error', 'unknown')}"


def handle_constants_search(client: ImHexClient, args: dict) -> str:
    limit = args.get("limit", 20)
    d = client.send_command(
        "search/find", {"pattern": args["value"], "type": args["type"], "limit": limit}
    ).get("data", {})
    matches = d.get("matches", [])
    total = d.get("total_matches", len(matches))
    lines = [
        f"Pattern: '{args['value']}' ({args['type']})  Total: {total}  Showing: {len(matches)}"
    ]
    for i, m in enumerate(matches[:limit], 1):
        lines.append(f"  {i}. 0x{m:X}")
    return "\n".join(lines)


HANDLERS = {
    "read_hex": handle_read_hex,
    "write_hex": handle_write_hex,
    "inspect_data": handle_inspect_data,
    "hash": handle_hash,
    "data_entropy": handle_data_entropy,
    "data_statistics": handle_data_statistics,
    "data_strings": handle_data_strings,
    "data_magic": handle_data_magic,
    "data_disassemble": handle_data_disassemble,
    "entropy": handle_data_entropy,
    "magic": handle_data_magic,
    "strings": handle_data_strings,
    "statistics": handle_data_statistics,
    "disassemble": handle_data_disassemble,
    "highlight_add": handle_highlight_add,
    "highlight_remove": handle_highlight_remove,
    "selection_get": handle_selection_get,
    "selection_set": handle_selection_set,
    "data_insert": handle_data_insert,
    "data_remove": handle_data_remove,
    "data_find_replace": handle_data_find_replace,
    "analyze": handle_analyze,
    "section_headers": handle_section_headers,
    "constants_search": handle_constants_search,
}
