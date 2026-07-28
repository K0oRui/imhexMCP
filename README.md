<div align="center">
    <img width="400" src="https://raw.githubusercontent.com/WerWolv/ImHex/master/resources/dist/common/logo/ImHexLogoSVGBG.svg" alt="imhex">
    </br>
</div>

<div align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--2.0-blue?style=for-the-badge" alt="license" /></a>
    <img src="https://img.shields.io/badge/tools-77-success?style=for-the-badge" alt="tools" />
    <img src="https://img.shields.io/badge/C++%20endpoints-36-success?style=for-the-badge" alt="endpoints" />
</div>


# ImHex MCP Server


> **Fork** — this repository provides an MCP (Model Context Protocol) server that exposes ImHex hex editor capabilities to AI assistants. It consists of a Python MCP server and a C++ ImHex plugin communicating via TCP (port 31337).
>
> ## Modernization
> - **Server refactored** — monolithic `server.py` (~2465 lines) split into modular `tools/` package with 7 modules; each tool is a `Tool()` definition with a dedicated handler function. Server entry point reduced to ~60 lines.
> - **Client extracted** — standalone `ImHexClient` class in `client.py` handles TCP connect/disconnect/send/receive with retry logic.
> - **Tool count expanded** — from 27 tools to 77 tools (50 new), organized into `file_ops.py`, `analysis.py`, `search.py`, `bookmarks.py`, `batch.py`, `extra.py`.
> - **C++ plugin extended** — from 30 endpoints to 36 endpoints (6 new): `file/create`, `mem/new_provider`, `bookmark/edit`, `patch/export`, `selection/get`, `selection/set`.
> - **Stale files removed** — 170+ files cleaned up: old test files, benchmark scripts, unused `lib/` directory (async client, cache, batching, etc.), `docs/` directory (consolidated), Hypothesis cache.
>
> ## Fixes
> - **`file/create` crash** — `createProvider("hex.builtin.provider.file")` required a file path and crashed on the empty provider. Replaced with `MemoryProvider`.
> - **`mem/new_provider` size bug** — `bytes.size()` was read after `std::move(bytes)`, returning 0. Fixed by saving size before the move.
> - **`selection/get` and `selection/set` missing endpoints** — Python handlers referenced C++ endpoints that were never registered. Added both endpoints with `ImHexApi::HexEditor` API.
> - **`analyze` always scanned 10MB** — entropy/stats used a hardcoded 10MB instead of actual file size.
> - **`constants_search` crash** — referenced undefined `handle_search` function.
> - **`batch_search` wrong parameter** — sent `"patterns"` array instead of single `"pattern"` string.
> - **`batch_search_single` missing default** — `provider_ids` required when it should default to `"all"`.
> - **`multi_search` wrong response key** — read nonexistent `"patterns"` key instead of `"results"`.
> - **`batch_open_directory` unusable** — C++ endpoint never worked; rewritten in pure Python.
> - **`histogram` list vs dict** — distribution data is JSON array, handler tried `.items()` on it.
> - **`bookmark_edit` color type** — color string (`"FF0000FF"`) passed directly to C++ endpoint expecting `u32`. Python handler now converts via `int(color, 16)`.
> - **Plugin build errors** — ImHex API had breaking changes (`markDirty` → `markDataDirty`, `isDirty` → `isDataDirty`/`isMetadataDirty`, `IntervalTree::StoredInterval` API change, `MemoryProvider` namespace, `Patches::fromProvider` pointer fix). All resolved against ImHex `v1.39.0.WIP`.
>
> ## New Tools (50)
>
> `list_providers` `save_file` `undo` `redo` `undo_status` `create_file` `mem_new_provider` `patch_export` `bookmark_edit` `entropy` `magic` `strings` `statistics` `disassemble` `highlight_add` `highlight_remove` `selection_get` `selection_set` `data_insert` `data_remove` `data_find_replace` `analyze` `section_headers` `constants_search` `search_multi` `export_search` `add_bookmark` `list_bookmarks` `batch_search_single` `batch_hash_range` `decode_data` `diff_analyze` `disassemble_bytes` `read_chunked` `file_list` `read_data` `write_data` `hexdump` `disassemble_x64` `disassemble_x86` `disassemble_arm` `disassemble_arm64` `shutdown` `pattern_execute` `goto` `encode_data` `list_architectures` `data_encode` `histogram` `list_all_tools`
>
> ## Infrastructure
> - **Patches** (`patches/`) — 7 ImHex build patches for API compatibility plus 14 historical MCP feature patches.
> - **Plugin rebuilt** — `mcp.hexplug` compiled against ImHex `v1.39.0.WIP` headers with `-Werror` compatibility fixes.
> - **Plugin build tree** — sources need to be synced to `ImHex/plugins/mcp/source/` before building; cmake builds from the ImHex workspace.

## What the Server Does

ImHex MCP Server exposes the ImHex hex editor to AI assistants via the Model Context Protocol. The AI can:
- Open, create, and switch between file/memory providers
- Read/write hex data, search for patterns, extract strings
- Analyze entropy, byte frequency, and file type magic
- Disassemble code (x86, x86-64, ARM, ARM64, MIPS, PowerPC, RISC-V)
- Manage bookmarks and highlights
- Run batch operations across multiple files
- Export patches in IPS/IPS32 format
- Execute ImHex pattern language code

## Architecture

```
AI Assistant ──MCP──→ Python server (server.py) ──TCP (31337)──→ ImHex (mcp.hexplug plugin)
                              │
                              ├── tools/file_ops.py — file I/O, providers
                              ├── tools/analysis.py — entropy, statistics, magic
                              ├── tools/search.py — pattern search, multi‑search
                              ├── tools/bookmarks.py — bookmarks CRUD
                              ├── tools/batch.py — multi‑file batch operations
                              └── tools/extra.py — encode, disasm, hexdump, histogram
```

## Quick Start

```bash
pip install mcp>=1.3.0

# Start with existing ImHex instance (Network Interface enabled on port 31337)
python mcp-server/server.py

# Or auto‑launch ImHex on Windows:
python mcp-server/server.py --auto-launch
```

Configure in `opencode.json`:

```json
"imhex": {
    "type": "local",
    "command": ["python", "path\\to\\mcp-server\\server.py", "--auto-launch"],
    "enabled": true,
    "timeout": 120000
}
```

## Windows Notes

- `--auto-launch` finds ImHex in `dist/bin/imhex-gui.exe` or common install paths
- Full path support (backslashes, drive letters) in all file operations

## Requirements

- Python 3.10+
- `mcp` package (`pip install mcp`)
- ImHex with Network Interface enabled (Settings → General) or `--auto-launch`
- C++ plugin rebuild requires: CMake 3.16+, MinGW (MSYS2), ImHex build tree

## Project Structure

```
imhexMCP/
├── mcp-server/
│   ├── server.py          # MCP server entry point (~60 lines)
│   ├── client.py          # TCP client for ImHex communication
│   │
│   ├── tools/
│   │   ├── __init__.py    # Aggregates TOOLS/HANDLERS from all modules
│   │   ├── file_ops.py    # File I/O, provider management, undo/redo
│   │   ├── analysis.py    # Entropy, statistics, magic, diff, patterns
│   │   ├── search.py      # Pattern search, multi-search, export
│   │   ├── bookmarks.py   # Bookmark CRUD
│   │   ├── batch.py       # Batch operations across multiple files
│   │   └── extra.py       # Disassembly, encode, hexdump, histogram
│   │
│   └── tests/             # Python client/server tests
│
├── plugin/
│   ├── source/
│   │   └── plugin_mcp.cpp # C++ ImHex plugin (36 network endpoints)
│   └── CMakeLists.txt     # Plugin build definition
│
├── patches/               # ImHex build patches for API compatibility
│   ├── PATCH_MANIFEST.md  # Patch descriptions and status
│   ├── 01-*.patch         # 7 build-line patches
│   └── 0001-*.patch       # 14 historical MCP feature patches
│
├── dist/bin/
│   ├── imhex-gui.exe      # Built ImHex binary
│   └── plugins/mcp.hexplug # Compiled C++ plugin
│
├── .opencode/             # opencode configuration
└── opencode.json          # MCP server registration
```

## Legal

```
ImHex MCP Server — Copyright (C) 2025 ImHex MCP Integration Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

ImHex Copyright (C) 2020-2024 WerWolv — https://github.com/WerWolv/ImHex
```


## Thanks

Thanks to WerWolv for creating [ImHex](https://github.com/WerWolv/ImHex), the best hex editor available.


## Compiling the Plugin

**Requirements:**
- CMake 3.16+
- MinGW (MSYS2) with g++ 16+
- ImHex build tree (included as `ImHex/` subdirectory)

**Build commands:**
```powershell
# Copy source to ImHex build tree
Copy-Item plugin\source\plugin_mcp.cpp -Destination ImHex\plugins\mcp\source\

# Build from ImHex workspace
cd ImHex\build
cmake --build . --target mcp -j

# Copy output to dist
Copy-Item plugins\mcp.hexplug -Destination ..\dist\bin\plugins\
Copy-Item plugins\mcp.hexplug -Destination ..\dist\bin\
```

**Notes:**
- Source must be synced to `ImHex/plugins/mcp/source/` before building — the cmake build reads from there.
- The plugin is compiled as `mcp.hexplug` and loaded by ImHex at startup.
- After rebuilding, restart ImHex to pick up the new plugin.


## Contributing

- Keep `tools/` module structure — add new tools to the appropriate module
- C++ endpoints go in `plugin/source/plugin_mcp.cpp` in the `registerNetworkEndpoint` block
- Both a Python Tool definition (`TOOLS`) and handler (`HANDLERS`) must be registered
- Verify with `python -c "from tools import TOOLS, HANDLERS; print(f'{len(TOOLS)} tools, {len(HANDLERS)} handlers')"` before committing
