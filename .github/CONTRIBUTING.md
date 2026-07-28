# Contributing to ImHex MCP

## Reporting Bugs

Use the bug report template. Include:
- Clear description and steps to reproduce
- Environment details (OS, architecture, ImHex version)
- Error messages and logs from ImHex console / MCP server

## Suggesting Features

Use the feature request template. Explain the use case, the problem it solves, and any implementation ideas.

## Reporting Patch Failures

If patches fail to apply to a newer ImHex version, use the patch failure template. Include the ImHex commit hash and full error output.

## Development Workflow

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/imhexMCP.git
cd imhexMCP

# Clone ImHex and apply patches
git clone https://github.com/WerWolv/ImHex.git
cd ImHex
git apply ../patches/*.patch
cd ..
```

### Building

```bash
cd ImHex/build
cmake .. -DCMAKE_BUILD_TYPE=Debug -G Ninja
ninja -j$(nproc)
```

### Making Changes

1. **Python server** (`mcp-server/`): Edit `tools/*.py` or `server.py`/`client.py`
2. **C++ plugin** (`plugin/source/plugin_mcp.cpp`): Edit, then sync to `ImHex/plugins/mcp/source/` and rebuild
3. **Patches** (`patches/`): Modify ImHex source, commit, regenerate with `git format-patch`

### Testing

```bash
# Verify tool registration
python -c "from tools import TOOLS, HANDLERS; print(f'{len(TOOLS)} tools, {len(HANDLERS)} handlers')"

# Run tests
cd mcp-server
pip install -r requirements.txt -r dev-requirements.txt
pytest -v
```

## Patch Development

### Creating New Patches

```bash
cd ImHex
git add .
git commit -m "feat: description"
git format-patch origin/master..HEAD -o ../patches/
```

### Naming Convention

```
NN-short-description.patch
```

Example: `06-mcp-api-compatibility.patch`

### Testing Patches

```bash
git clone https://github.com/WerWolv/ImHex.git ImHex-test
cd ImHex-test
git apply --check ../patches/*.patch
git apply ../patches/*.patch
```

## Submitting Changes

1. Create a feature branch
2. Commit with conventional messages (`feat:`, `fix:`, `docs:`, `patch:`)
3. Push and open a Pull Request
4. Fill in the PR template

## Questions?

Open a discussion or issue on GitHub.
