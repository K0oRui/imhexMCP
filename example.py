#!/usr/bin/env python3
"""Minimal example using the ImHex MCP client."""
import sys
sys.path.insert(0, "mcp-server")
from client import ImHexClient

with ImHexClient() as client:
    caps = client.send_command("imhex/capabilities")
    print("Capabilities:", caps)

    client.send_command("file/open", {"path": "/path/to/file.bin"})
    info = client.send_command("provider/info")
    print("Provider:", info)

    data = client.send_command("data/read", {"offset": 0, "length": 64})
    print("First 64 bytes hex:", data.get("data", {}).get("data", ""))
