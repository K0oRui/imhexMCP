#!/usr/bin/env python3
import argparse
import logging
import sys
import subprocess
import time
import os

import shutil
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from client import ImHexClient, ImHexError
from tools import TOOLS, HANDLERS

logger = logging.getLogger("imhex-mcp")

IMHEX_PATHS_WIN = [
    Path(__file__).resolve().parent.parent / "dist" / "bin" / "imhex-gui.exe",
    Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "ImHex" / "imhex.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")) / "ImHex" / "imhex.exe",
    Path.home() / "AppData" / "Local" / "ImHex" / "imhex.exe",
    Path.home() / "scoop" / "imhex" / "current" / "imhex.exe",
]

_imhex_process: subprocess.Popen | None = None


def find_imhex() -> Path | None:
    for p in IMHEX_PATHS_WIN:
        if p.exists():
            return p
    which = shutil.which("imhex")
    return Path(which) if which else None


def launch_imhex(path: Path) -> bool:
    global _imhex_process
    try:
        _imhex_process = subprocess.Popen([str(path)], shell=True)
        return True
    except Exception as e:
        logger.warning("Failed to launch ImHex: %s", e)
        return False


def stop_imhex():
    global _imhex_process
    if _imhex_process:
        try:
            _imhex_process.terminate()
            _imhex_process.wait(timeout=5)
        except Exception:
            try:
                _imhex_process.kill()
                _imhex_process.wait(timeout=3)
            except Exception:
                pass
        _imhex_process = None


def wait_for_imhex(host: str, port: int, timeout: float = 15.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            c = ImHexClient(host=host, port=port, timeout=2)
            c.connect()
            c.disconnect()
            return True
        except Exception:
            time.sleep(0.5)
    return False


def ensure_connected(client: ImHexClient, host: str, port: int, auto_launch: bool):
    if client.is_connected:
        return
    try:
        client.connect()
    except Exception:
        if not auto_launch:
            raise
        logger.info("ImHex not running, launching...")
        imhex_path = find_imhex()
        if not imhex_path:
            raise RuntimeError("ImHex not found")
        if not launch_imhex(imhex_path):
            raise RuntimeError("Failed to launch ImHex")
        logger.info("Waiting for ImHex...")
        if not wait_for_imhex(host, port):
            raise RuntimeError("Timed out waiting for ImHex")
        client.connect()


def parse_args():
    p = argparse.ArgumentParser(description="ImHex MCP Server")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=31337)
    p.add_argument("--timeout", type=float, default=30.0)
    p.add_argument("--debug", action="store_true")
    p.add_argument("--auto-launch", action="store_true", help="Auto-detect and launch ImHex on first tool call")
    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    client = ImHexClient(host=args.host, port=args.port, timeout=args.timeout)

    app = Server("imhex")

    @app.list_tools()
    async def list_tools():
        return TOOLS

    @app.call_tool()
    async def call_tool(name: str, arguments: dict):
        handler = HANDLERS.get(name)
        if not handler:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            if name != "shutdown":
                ensure_connected(client, args.host, args.port, args.auto_launch)
            result = handler(client, arguments)
            if name == "shutdown":
                stop_imhex()
            return [TextContent(type="text", text=result)]
        except ImHexError as e:
            return [TextContent(type="text", text=f"ImHex error: {e}")]
        except Exception as e:
            logger.exception("Tool error")
            return [TextContent(type="text", text=f"Error: {e}")]

    async def run():
        async with stdio_server() as (rs, ws):
            await app.run(rs, ws, app.create_initialization_options())

    try:
        import asyncio
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
        stop_imhex()


if __name__ == "__main__":
    main()
