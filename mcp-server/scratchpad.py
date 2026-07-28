"""
Quick-start:  ipython -i scratchpad.py

You get a repl with the client and handlers loaded.
Mock client.send_command to test handler logic without ImHex.
"""

from unittest.mock import Mock

from client import ImHexClient
from tools import HANDLERS, TOOLS

print(f"ImHex MCP scratchpad — {len(TOOLS)} tools, {len(HANDLERS)} handlers")

client = Mock(spec=ImHexClient)
client.is_connected = True
client.send_command.return_value = {"data": {}}


def test(name, **overrides):
    handler = HANDLERS[name]
    args = _defaults.get(name, {}) | overrides
    print(f"\n--- {name} ---")
    print(handler(client, args))


_defaults = {
    "inspect_data": {"offset": 0},
    "hash": {"algorithm": "sha256", "offset": 0},
    "data_entropy": {"offset": 0, "size": 1024},
    "data_strings": {"offset": 0, "size": 1024, "min_length": 4},
    "data_magic": {"offset": 0, "size": 256},
    "decode_data": {"data": "48656C6C6F", "encoding": "hex"},
    "encode_data": {"data": "Hello", "encoding": "hex"},
}

print("\nReady. Try:  test('decode_data')")
print("Or mock a real response:")
print("  client.send_command.return_value = {'data': {'decoded': 'world'}}")
print("  test('decode_data')")
