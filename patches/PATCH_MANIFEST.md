# ImHex MCP Plugin Patches

Apply in numerical order to [WerWolv/ImHex](https://github.com/WerWolv/ImHex) commit `63d111d`.

```powershell
cd ImHex
..\apply-patches.ps1   # Windows
# or
../apply-patches.sh     # Unix
```

## Patch Order

| # | Patch | Files | Purpose |
|---|-------|-------|---------|
| 01 | `01-builtin-library-plugin.patch` | `plugins/builtin/CMakeLists.txt` | Add `LIBRARY_PLUGIN` flag so MCP plugin can link against builtin |
| 02 | `02-fileprovider-public-open.patch` | `plugins/builtin/include/.../file_provider.hpp` | Make `open(bool)` public so MCP plugin can call it |
| 03 | `03-fileprovider-graceful-settings.patch` | `plugins/builtin/source/.../file_provider.cpp` | Try-catch in `open()` and `loadSettings()` for programmatic use |
| 04 | `04-provider-graceful-settings.patch` | `lib/libimhex/source/providers/provider.cpp` | Try-catch in `Provider::loadSettings()` for missing settings |
| 05 | `05-appleclang-build-helpers.patch` | `cmake/build_helpers.cmake` | Add AppleClang 15.0.0 as supported compiler |
| 0007 | `0007-...patch` | `plugins/mcp/CMakeLists.txt`, `plugin_mcp.cpp` | **Creates the MCP plugin** with all endpoints |
| 0008 | `0008-...patch` | `plugin_mcp.cpp` | Improve disassembly/diff error handling |
| 0009 | `0009-...patch` | `plugin_mcp.cpp` | TaskManager-based diff analysis |
| 0010 | `0010-...patch` | `plugin_mcp.cpp` | Add batch/open_directory endpoint |
| 0011 | `0011-...patch` | `plugin_mcp.cpp` | Add batch/search endpoint |
| 0012 | `0012-...patch` | `plugin_mcp.cpp` | Add batch/hash endpoint |
| 0013 | `0013-...patch` | `plugin_mcp.cpp` | Fix glob pattern matching |
| 0014 | `0014-...patch` | `plugin_mcp.cpp` | Fix glob pattern escaping |
| 06 | `06-mcp-api-compatibility.patch` | `plugin_mcp.cpp`, `test_list_providers.py` | Adapt to `OpenResult`, `setPickedPath()`, `shared_ptr` API |
| 0001 | `0001-...patch` | `plugin_mcp.cpp` | Queue-based file opening (async) |

## Key Changes

- **Builtin as shared library**: Exported as `.hexpluglib` so MCP plugin can link against it
- **FileProvider API**: `open(bool)` returns `OpenResult` — use `.isFailure()` / `.getErrorMessage()`
- **Path handling**: Use `setPickedPath()` (not `setPath()`) from Provider base class
- **Provider::add()**: Takes `std::shared_ptr<prv::Provider>`, not `unique_ptr`
