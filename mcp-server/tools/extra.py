from client import ImHexClient
from mcp.types import Tool

TOOLS = [
    Tool(
        name="decode_data",
        description="Decode hex/base64/ascii data to readable format",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Data string to decode"},
                "encoding": {
                    "type": "string",
                    "enum": ["hex", "base64", "ascii", "text", "binary"],
                    "description": "Source encoding",
                },
            },
            "required": ["data", "encoding"],
        },
    ),
    Tool(
        name="diff_analyze",
        description="Analyze diff between two providers with optional algorithm",
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
                "algorithm": {
                    "type": "string",
                    "enum": ["simple", "myers"],
                    "description": "Diff algorithm",
                },
            },
            "required": ["provider_id_1", "provider_id_2"],
        },
    ),
    Tool(
        name="disassemble_bytes",
        description="Disassemble raw bytes at an offset with explicit architecture",
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
                    "description": "Bytes to disassemble",
                    "minimum": 1,
                    "maximum": 4096,
                },
                "architecture": {
                    "type": "string",
                    "description": "CPU architecture (e.g. x86_64, arm)",
                    "default": "x86_64",
                },
                "base_address": {
                    "type": "integer",
                    "description": "Base address",
                    "minimum": 0,
                },
            },
        },
    ),
    Tool(
        name="read_chunked",
        description="Read data in chunks from a file for streaming large data",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Start offset",
                    "minimum": 0,
                },
                "length": {"type": "integer", "description": "Total bytes to read"},
                "chunk_size": {
                    "type": "integer",
                    "description": "Chunk size in bytes",
                    "default": 1048576,
                },
                "chunk_index": {
                    "type": "integer",
                    "description": "Chunk index to fetch",
                    "minimum": 0,
                },
                "encoding": {
                    "type": "string",
                    "enum": ["hex", "base64"],
                    "description": "Output encoding",
                },
            },
            "required": ["offset", "length"],
        },
    ),
    Tool(
        name="file_list",
        description="Alias for list_files",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="read_data",
        description="Alias for read_hex",
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
        name="write_data",
        description="Alias for write_hex",
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
        name="hexdump",
        description="Pretty hex dump with offset, hex bytes, and ASCII sidebar",
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
                    "description": "Bytes to dump",
                    "minimum": 1,
                    "maximum": 65536,
                },
                "width": {
                    "type": "integer",
                    "description": "Bytes per line (default: 16)",
                    "default": 16,
                },
            },
            "required": ["offset", "length"],
        },
    ),
    Tool(
        name="disassemble_x64",
        description="Disassemble x86-64 code at given offset",
        inputSchema={
            "type": "object",
            "properties": {
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
                "base_address": {
                    "type": "integer",
                    "description": "Base address",
                    "minimum": 0,
                },
            },
            "required": ["offset"],
        },
    ),
    Tool(
        name="disassemble_x86",
        description="Disassemble x86 (32-bit) code at given offset",
        inputSchema={
            "type": "object",
            "properties": {
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
                "base_address": {
                    "type": "integer",
                    "description": "Base address",
                    "minimum": 0,
                },
            },
            "required": ["offset"],
        },
    ),
    Tool(
        name="disassemble_arm",
        description="Disassemble ARM (32-bit) code at given offset",
        inputSchema={
            "type": "object",
            "properties": {
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
                "base_address": {
                    "type": "integer",
                    "description": "Base address",
                    "minimum": 0,
                },
            },
            "required": ["offset"],
        },
    ),
    Tool(
        name="disassemble_arm64",
        description="Disassemble ARM64 (AArch64) code at given offset",
        inputSchema={
            "type": "object",
            "properties": {
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
                "base_address": {
                    "type": "integer",
                    "description": "Base address",
                    "minimum": 0,
                },
            },
            "required": ["offset"],
        },
    ),
    Tool(
        name="shutdown",
        description="Shutdown ImHex process",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="pattern_execute",
        description="Execute ImHex pattern language code on the current file",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Pattern language code to execute",
                }
            },
            "required": ["code"],
        },
    ),
    Tool(
        name="goto",
        description="Jump to a specific offset in the file",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {
                    "type": "integer",
                    "description": "Offset to jump to",
                    "minimum": 0,
                }
            },
            "required": ["offset"],
        },
    ),
    Tool(
        name="encode_data",
        description="Encode data to hex/base64 format",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Raw string data to encode"},
                "encoding": {
                    "type": "string",
                    "enum": ["hex", "base64"],
                    "description": "Target encoding",
                },
            },
            "required": ["data", "encoding"],
        },
    ),
    Tool(
        name="list_architectures",
        description="List supported CPU architectures for disassembly",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="data_encode",
        description="Apply encoding transform (xor/rot/not) to a data region",
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
                    "description": "Bytes to transform",
                    "minimum": 1,
                },
                "type": {
                    "type": "string",
                    "enum": ["xor", "rot", "not"],
                    "description": "Transform type",
                },
                "key": {
                    "type": "integer",
                    "description": "XOR key or ROT value",
                    "minimum": 0,
                    "maximum": 255,
                },
            },
            "required": ["offset", "size", "type"],
        },
    ),
    Tool(
        name="histogram",
        description="Show byte frequency distribution as ASCII bar chart",
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
                    "description": "Bytes to analyze",
                    "minimum": 1,
                    "maximum": 10485760,
                },
                "top": {
                    "type": "integer",
                    "description": "Top N bytes to show (default: 16)",
                    "minimum": 1,
                    "maximum": 256,
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="list_all_tools",
        description="List all available ImHex MCP commands with descriptions",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
]


def handle_decode_data(client: ImHexClient, args: dict) -> str:
    d = client.send_command("data/decode", args).get("data", {})
    return f"Decoded ({args['encoding']}): {d.get('decoded', '')}"


def handle_diff_analyze(client: ImHexClient, args: dict) -> str:
    return str(client.send_command("diff/analyze", args).get("data", {}))


def handle_disassemble_bytes(client: ImHexClient, args: dict) -> str:
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


def handle_read_chunked(client: ImHexClient, args: dict) -> str:
    d = client.send_command(
        "data/read", {"offset": args["offset"], "length": args["length"]}
    ).get("data", {})
    return f"Offset: 0x{args['offset']:X}  Length: {args['length']} bytes\nHex:\n{d.get('data', '')}"


def handle_file_list(client: ImHexClient, _args: dict) -> str:
    from .file_ops import handle_list_files

    return handle_list_files(client, {})


def handle_read_data(client: ImHexClient, args: dict) -> str:
    from .analysis import handle_read_hex

    return handle_read_hex(client, args)


def handle_write_data(client: ImHexClient, args: dict) -> str:
    from .analysis import handle_write_hex

    return handle_write_hex(client, args)


def handle_hexdump(client: ImHexClient, args: dict) -> str:
    width = args.get("width", 16)
    d = client.send_command(
        "data/read", {"offset": args["offset"], "length": args["length"]}
    ).get("data", {})
    hex_str = d.get("data", "")
    raw = bytes.fromhex(hex_str) if hex_str else b""
    lines = [f"Hex dump at 0x{args['offset']:X} ({len(raw)} bytes):"]
    for i in range(0, len(raw), width):
        chunk = raw[i : i + width]
        hex_part = " ".join(f"{b:02X}" for b in chunk)
        hex_part = hex_part.ljust(width * 3 - 1)
        ascii_part = "".join(chr(b) if 0x20 <= b < 0x7F else "." for b in chunk)
        addr = args["offset"] + i
        lines.append(f"  {addr:08X}  {hex_part}  |{ascii_part}|")
    return "\n".join(lines)


def _disassemble_with(client: ImHexClient, args: dict, arch: str) -> str:
    params = {
        "provider_id": args.get("provider_id", 0),
        "offset": args["offset"],
        "size": args.get("size", 64),
        "architecture": arch,
        "base_address": args.get("base_address", 0),
    }
    d = client.send_command("data/disassemble", params).get("data", {})
    if "error" in d:
        return f"Error: {d['error']}"
    instrs = d.get("instructions", [])
    lines = [f"Architecture: {arch}  Instructions: {len(instrs)}"]
    for i in instrs:
        lines.append(
            f"  {i.get('address', ''):16s} {i.get('bytes', ''):24s} {i.get('mnemonic', '')} {i.get('operands', '')}"
        )
    return "\n".join(lines)


def handle_disassemble_x64(client: ImHexClient, args: dict) -> str:
    return _disassemble_with(client, args, "x86_64")


def handle_disassemble_x86(client: ImHexClient, args: dict) -> str:
    return _disassemble_with(client, args, "x86_32")


def handle_disassemble_arm(client: ImHexClient, args: dict) -> str:
    return _disassemble_with(client, args, "ARM")


def handle_disassemble_arm64(client: ImHexClient, args: dict) -> str:
    return _disassemble_with(client, args, "ARM64")


def handle_shutdown(client: ImHexClient, _args: dict) -> str:
    client.disconnect()
    return "Shutting down ImHex"


def handle_pattern_execute(client: ImHexClient, args: dict) -> str:
    d = client.send_command("pattern/execute", {"code": args["code"]}).get("data", {})
    lines = []
    if d.get("success"):
        lines.append(
            f"Pattern executed successfully ({d.get('pattern_count', 0)} patterns, {d.get('running_time', 0):.3f}s)"
        )
        for p in d.get("patterns", []):
            lines.append(
                f"  {p.get('type', '?')} {p.get('name', '?')} @ 0x{p.get('offset', 0):X} ({p.get('size', 0)} bytes)"
            )
    else:
        lines.append(f"Pattern execution failed (code: {d.get('return_code')})")
        for e in d.get("compile_errors", []):
            lines.append(f"  Line {e.get('line')}: {e.get('message')}")
        if d.get("eval_error"):
            lines.append(f"  Runtime: {d['eval_error']}")
    for msg in d.get("log", []):
        lines.append(f"  [log] {msg}")
    return "\n".join(lines) if lines else "(no output)"


def handle_goto(client: ImHexClient, args: dict) -> str:
    from .analysis import handle_selection_set

    return handle_selection_set(client, {"offset": args["offset"], "size": 1})


def handle_encode_data(client: ImHexClient, _args: dict) -> str:
    import base64

    data = _args["data"].encode() if isinstance(_args["data"], str) else _args["data"]
    if _args["encoding"] == "hex":
        return f"Encoded (hex): {data.hex().upper()}"
    elif _args["encoding"] == "base64":
        return f"Encoded (base64): {base64.b64encode(data).decode()}"
    return "Unknown encoding"


def handle_list_architectures(client: ImHexClient, _args: dict) -> str:
    archs = [
        "x86_16  - Intel 16-bit x86",
        "x86_32  - Intel 32-bit x86 (IA-32)",
        "x86_64  - Intel 64-bit x86 (AMD64/EM64T)",
        "ARM     - ARM 32-bit",
        "ARM64   - ARM 64-bit (AArch64)",
        "MIPS    - MIPS (big/little endian)",
        "PowerPC - PowerPC 32-bit",
        "RISCV   - RISC-V (32/64-bit)",
    ]
    return "Supported architectures:\n" + "\n".join(archs)


def handle_data_encode(client: ImHexClient, args: dict) -> str:
    offset = args["offset"]
    size = args["size"]
    enc_type = args["type"]
    key = args.get("key", 0)
    d = client.send_command("data/read", {"offset": offset, "length": size}).get(
        "data", {}
    )
    hex_str = d.get("data", "")
    if not hex_str:
        return "Failed to read data"
    raw = bytes.fromhex(hex_str)
    if enc_type == "xor":
        transformed = bytes(b ^ key for b in raw)
    elif enc_type == "rot":
        transformed = bytes((b + key) & 0xFF for b in raw)
    elif enc_type == "not":
        transformed = bytes(~b & 0xFF for b in raw)
    else:
        return f"Unknown transform: {enc_type}"
    client.send_command("data/write", {"offset": offset, "data": transformed.hex()})
    return f"{enc_type.upper()} transform applied to {size} bytes at 0x{offset:X} with key=0x{key:X}"


def handle_list_all_tools(_client: ImHexClient, _args: dict) -> str:
    from tools import TOOLS

    lines = [f"ImHex MCP - {len(TOOLS)} tools available", ""]
    for t in TOOLS:
        props = t.inputSchema.get("properties", {})
        params = ", ".join(props.keys()) if props else "(none)"
        lines.append(f"  {t.name}({params})")
        if t.description:
            lines.append(f"    {t.description}")
    return "\n".join(lines)


def handle_histogram(client: ImHexClient, args: dict) -> str:
    offset = args.get("offset", 0)
    size = args.get("size", 0)
    top = args.get("top", 16)
    if size == 0:
        info = client.send_command("provider/info").get("data", {})
        if info.get("valid"):
            size = info.get("size", 0)
    d = client.send_command(
        "data/statistics",
        {"offset": offset, "size": min(size, 10485760), "include_distribution": True},
    ).get("data", {})
    distribution = d.get("distribution")
    if not distribution or not isinstance(distribution, list):
        return "No distribution data available"
    sorted_bytes = sorted(distribution, key=lambda x: int(x["count"]), reverse=True)[
        :top
    ]
    max_count = max(int(e["count"]) for e in sorted_bytes)
    bar_width = 40
    lines = [
        f"Byte distribution (top {len(sorted_bytes)} of {d.get('unique_bytes', 0)} unique bytes):"
    ]
    for entry in sorted_bytes:
        bv = int(entry["byte"])
        count = int(entry["count"])
        bar_len = max(1, count * bar_width // max_count) if max_count else 1
        bar = chr(0x2588) * bar_len
        char = chr(bv) if 0x20 <= bv < 0x7F else " "
        lines.append(
            f"  0x{bv:02X} ({char}) |{bar} {count:,} ({count * 100.0 / size:.1f}%)"
        )
    return "\n".join(lines)


HANDLERS = {
    "decode_data": handle_decode_data,
    "diff_analyze": handle_diff_analyze,
    "disassemble_bytes": handle_disassemble_bytes,
    "read_chunked": handle_read_chunked,
    "file_list": handle_file_list,
    "read_data": handle_read_data,
    "write_data": handle_write_data,
    "hexdump": handle_hexdump,
    "disassemble_x64": handle_disassemble_x64,
    "disassemble_x86": handle_disassemble_x86,
    "disassemble_arm": handle_disassemble_arm,
    "disassemble_arm64": handle_disassemble_arm64,
    "shutdown": handle_shutdown,
    "pattern_execute": handle_pattern_execute,
    "goto": handle_goto,
    "encode_data": handle_encode_data,
    "list_architectures": handle_list_architectures,
    "data_encode": handle_data_encode,
    "histogram": handle_histogram,
    "list_all_tools": handle_list_all_tools,
}
