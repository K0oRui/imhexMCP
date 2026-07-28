from mcp.types import Tool
from client import ImHexClient

TOOLS = [
    Tool(name="batch_open_directory", description="Open multiple binary files from a directory for batch analysis", inputSchema={"type": "object", "properties": {"directory": {"type": "string", "description": "Directory path to scan"}, "pattern": {"type": "string", "description": "Glob pattern (default: *)"}, "recursive": {"type": "boolean", "description": "Search subdirectories"}, "max_files": {"type": "integer", "description": "Max files to open", "minimum": 1, "maximum": 1000}, "filters": {"type": "object", "properties": {"min_size": {"type": "integer"}, "max_size": {"type": "integer"}, "extensions": {"type": "array", "items": {"type": "string"}}}}}, "required": ["directory"]}),
    Tool(name="batch_search", description="Search for patterns across all open files", inputSchema={"type": "object", "properties": {"patterns": {"type": "array", "items": {"type": "object", "properties": {"value": {"type": "string", "description": "Pattern value"}, "type": {"type": "string", "enum": ["hex", "string"], "description": "Pattern type"}}, "required": ["value", "type"]}, "minItems": 1}, "provider_ids": {"description": "Provider IDs or 'all'", "oneOf": [{"type": "array", "items": {"type": "integer"}}, {"type": "string", "enum": ["all"]}]}, "max_matches_per_file": {"type": "integer", "description": "Max matches per file", "minimum": 1, "maximum": 10000}}, "required": ["patterns"]}),
    Tool(name="batch_hash", description="Calculate hashes for multiple files simultaneously", inputSchema={"type": "object", "properties": {"algorithms": {"type": "array", "items": {"type": "string", "enum": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]}, "minItems": 1}, "provider_ids": {"description": "Provider IDs or 'all'", "oneOf": [{"type": "array", "items": {"type": "integer"}}, {"type": "string", "enum": ["all"]}]}}, "required": ["algorithms"]}),
    Tool(name="batch_diff", description="Compare a reference file against multiple targets", inputSchema={"type": "object", "properties": {"reference_id": {"type": "integer", "description": "Reference provider ID", "minimum": 0}, "target_ids": {"description": "Target IDs or 'all'", "oneOf": [{"type": "array", "items": {"type": "integer"}, "minItems": 1}, {"type": "string", "enum": ["all"]}]}, "algorithm": {"type": "string", "enum": ["myers"], "description": "Diff algorithm"}, "max_diff_regions": {"type": "integer", "description": "Max diff regions per file"}}, "required": ["reference_id", "target_ids"]}),
    Tool(name="batch_search_single", description="Search a single pattern across all open files", inputSchema={"type": "object", "properties": {"provider_ids": {"description": "Provider IDs or 'all' (default: all)", "oneOf": [{"type": "array", "items": {"type": "integer"}}, {"type": "string", "enum": ["all"]}]}, "pattern": {"type": "string", "description": "Hex pattern to search for", "pattern": "^[0-9A-Fa-f]+$"}, "max_matches": {"type": "integer", "description": "Max matches per file", "minimum": 1, "maximum": 10000}}, "required": ["pattern"]}),
    Tool(name="batch_hash_range", description="Hash files with offset/size range control", inputSchema={"type": "object", "properties": {"provider_ids": {"description": "Provider IDs or 'all'", "oneOf": [{"type": "array", "items": {"type": "integer"}}, {"type": "string", "enum": ["all"]}]}, "algorithm": {"type": "string", "enum": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"], "default": "sha256"}, "offset": {"type": "integer", "description": "Start offset", "minimum": 0}, "size": {"type": "integer", "description": "Bytes per file", "minimum": 1, "maximum": 104857600}}, "required": ["provider_ids", "algorithm"]}),
]


def handle_batch_open_directory(client: ImHexClient, args: dict) -> str:
    import pathlib, time
    directory = args["directory"]
    max_files = args.get("max_files", 100)
    d = pathlib.Path(directory)
    if not d.is_dir():
        return f"Error: not a directory: {directory}"
    files = sorted([str(p) for p in d.iterdir() if p.is_file() and p.suffix.lower() in (".dll", ".exe", ".bin", ".so", ".elf")])[:max_files]
    if not files:
        return f"No binary files found in {directory}"
    opened = 0
    errors = []
    lines = []
    for fp in files:
        try:
            resp = client.send_command("file/open", {"path": fp}).get("data", {})
            request_id = resp.get("request_id")
            pid = resp.get("provider_id")
            if pid is not None:
                opened += 1
                lines.append(f"  ID {pid}: {pathlib.Path(fp).name}")
            elif request_id is not None:
                for _ in range(20):
                    time.sleep(0.15)
                    status = client.send_command("file/open/status", {"request_id": request_id})
                    s = status.get("data", {}).get("status") or status.get("status")
                    if s == "success":
                        opened += 1
                        lines.append(f"  {pathlib.Path(fp).name}")
                        break
                    if s == "error":
                        break
                else:
                    errors.append(f"{pathlib.Path(fp).name}: timed out waiting for open")
        except Exception as e:
            errors.append(f"{pathlib.Path(fp).name}: {e}")
    files_now = client.send_command("file/list", {}).get("data", {}).get("files", [])
    for f in files_now:
        active = " [ACTIVE]" if f.get("is_active") else ""
        lines.append(f"  ID {f.get('id')}: {f.get('name')}{active}")
    lines.insert(0, f"Files found: {len(files)}  Opened: {opened}  Skipped: {len(files) - opened}  Total providers: {len(files_now)}")
    for e in errors[:5]:
        lines.append(f"  Error: {e}")
    return "\n".join(lines)


def handle_batch_search(client: ImHexClient, args: dict) -> str:
    p = args.get("patterns", [{}])[0]
    val = p.get("value") or p.get("pattern", "")
    cmd_args = {"pattern": val, "provider_ids": args.get("provider_ids", "all"), "max_matches_per_file": args.get("max_matches_per_file", 1000)}
    d = client.send_command("batch/search", cmd_args).get("data", {})
    results = d.get("results", [])
    lines = [f"Pattern: {val}  Total matches: {d.get('total_matches', 0)}  Files: {d.get('total_files', 0)}"]
    for r in results:
        matches = r.get("matches", [])
        lines.append(f"\n{r.get('provider_name', '?')} (ID: {r.get('provider_id', '?')}) - {r.get('match_count', 0)} matches{' [has more]' if r.get('has_more') else ''}")
        for i, m in enumerate(matches[:10], 1):
            lines.append(f"  {i}. 0x{m:016X}")
    return "\n".join(lines)


def handle_batch_hash(client: ImHexClient, args: dict) -> str:
    hashes = client.send_command("batch/hash", args).get("data", {}).get("hashes", [])
    lines = [f"Total files: {len(hashes)}  Algorithms: {', '.join(args['algorithms'])}"]
    for h in hashes:
        lines.append(f"\n{h.get('file', '?')} (ID: {h.get('provider_id', '?')})")
        for algo, val in h.get("hashes", {}).items():
            lines.append(f"  {algo.upper()}: {val}")
    return "\n".join(lines)


def handle_batch_diff(client: ImHexClient, args: dict) -> str:
    d = client.send_command("batch/diff", args).get("data", {})
    s = d.get("summary", {})
    lines = [f"Reference: {s.get('reference_file', '?')}  Files compared: {s.get('files_compared', 0)}  Avg similarity: {s.get('avg_similarity', 0):.2f}%"]
    for diff in d.get("diffs", []):
        lines.append(f"\n{diff.get('target_file', '?')}  Similarity: {diff.get('similarity', 0):.2f}%  Regions: {diff.get('diff_regions', 0)}")
    return "\n".join(lines)

def handle_batch_search_single(client: ImHexClient, args: dict) -> str:
    cmd_args = dict(args)
    if "max_matches" in cmd_args:
        cmd_args["max_matches_per_file"] = cmd_args.pop("max_matches")
    cmd_args.setdefault("provider_ids", "all")
    d = client.send_command("batch/search", cmd_args).get("data", {})
    results = d.get("results", [])
    lines = [f"Pattern: {args.get('pattern', '')}  Max per file: {args.get('max_matches', 1000)}"]
    total = 0
    for r in results:
        matches = r.get("matches", [])
        if matches:
            total += len(matches)
            lines.append(f"\n{r.get('provider_name', '?')} (ID: {r.get('provider_id', '?')}) - {len(matches)} matches{' [has more]' if r.get('has_more') else ''}")
            for i, m in enumerate(matches[:10], 1):
                lines.append(f"  {i}. 0x{m:016X}")
    lines.append(f"\nTotal: {total} matches")
    return "\n".join(lines)


def handle_batch_hash_range(client: ImHexClient, args: dict) -> str:
    hashes = client.send_command("batch/hash", args).get("data", {}).get("hashes", [])
    algorithm = args.get("algorithm", "sha256")
    lines = [f"Files hashed: {len(hashes)}  Algorithm: {algorithm}"]
    for h in hashes:
        lines.append(f"\n{h.get('provider_name', '?')} (ID: {h.get('provider_id', '?')})")
        lines.append(f"  Hash: {h.get('hash', '')}  Status: {h.get('status', '')}")
    return "\n".join(lines)


HANDLERS = {
    "batch_open_directory": handle_batch_open_directory,
    "batch_search": handle_batch_search,
    "batch_hash": handle_batch_hash,
    "batch_diff": handle_batch_diff,
    "batch_search_single": handle_batch_search_single,
    "batch_hash_range": handle_batch_hash_range,
}
