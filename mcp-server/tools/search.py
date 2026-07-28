from client import ImHexClient
from mcp.types import Tool

TOOLS = [
    Tool(
        name="search",
        description="Search for a hex/text/regex pattern in the currently open file",
        inputSchema={
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Pattern to search for"},
                "type": {
                    "type": "string",
                    "enum": ["hex", "text", "regex"],
                    "description": "Search type",
                },
                "offset": {
                    "type": "integer",
                    "description": "Result offset for pagination",
                    "minimum": 0,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results",
                    "minimum": 1,
                    "maximum": 100000,
                },
            },
            "required": ["pattern", "type"],
        },
    ),
    Tool(
        name="multi_search",
        description="Search for multiple patterns simultaneously",
        inputSchema={
            "type": "object",
            "properties": {
                "patterns": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "type": {"type": "string", "enum": ["hex", "text"]},
                        },
                        "required": ["pattern", "type"],
                    },
                    "minItems": 1,
                    "maxItems": 20,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results per pattern",
                    "minimum": 1,
                    "maximum": 100000,
                },
            },
            "required": ["patterns"],
        },
    ),
    Tool(
        name="export_search_results",
        description="Export search matches to JSON or CSV",
        inputSchema={
            "type": "object",
            "properties": {
                "matches": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Array of match offsets",
                },
                "output_path": {"type": "string", "description": "Output file path"},
                "format": {
                    "type": "string",
                    "enum": ["json", "csv"],
                    "description": "Export format",
                },
                "context_bytes": {
                    "type": "integer",
                    "description": "Context bytes per match",
                    "minimum": 0,
                    "maximum": 256,
                },
            },
            "required": ["matches", "output_path"],
        },
    ),
]


def handle_search(client: ImHexClient, args: dict) -> str:
    params = {"pattern": args["pattern"], "type": args["type"]}
    if args.get("offset"):
        params["offset"] = args["offset"]
    if args.get("limit"):
        params["limit"] = args["limit"]
    d = client.send_command("search/find", params).get("data", {})
    matches = d.get("matches", [])
    total = d.get("total_matches", len(matches))
    offset = args.get("offset", 0)
    lines = [
        f"Pattern: '{args['pattern']}' ({args['type']})  Total: {total}  Showing: {len(matches)}"
    ]
    for i, m in enumerate(matches[:100], 1):
        lines.append(f"  {offset + i}. 0x{m:X}")
    if d.get("has_more"):
        lines.append(f"Use offset={offset + len(matches)} for more")
    return "\n".join(lines)


def handle_multi_search(client: ImHexClient, args: dict) -> str:
    params = {"patterns": args["patterns"]}
    if args.get("limit"):
        params["limit"] = args["limit"]
    d = client.send_command("search/multi", params).get("data", {})
    results = d.get("results", [])
    lines = [f"Multi-pattern search ({d.get('patterns_searched', 0)} patterns):"]
    for i, p in enumerate(results, 1):
        lines.append(
            f"  [{i}] '{p.get('pattern', '')}' ({p.get('type', '')}) - {p.get('count', 0)} matches"
        )
        for j, m in enumerate(p.get("matches", [])[:5], 1):
            lines.append(f"       {j}. 0x{m:X}")
    return "\n".join(lines)


def handle_export_search_results(client: ImHexClient, args: dict) -> str:
    d = client.send_command("search/export", args).get("data", {})
    return f"Exported {d.get('match_count', 0)} matches to {d.get('output_path', args['output_path'])}"


HANDLERS = {
    "search": handle_search,
    "multi_search": handle_multi_search,
    "export_search_results": handle_export_search_results,
    "search_multi": handle_multi_search,
    "export_search": handle_export_search_results,
}
