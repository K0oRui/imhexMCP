import json
import logging
import socket
from typing import Any

logger = logging.getLogger("imhex-mcp")


class ImHexError(Exception):
    pass


class ImHexClient:
    def __init__(self, host: str = "localhost", port: int = 31337, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: socket.socket | None = None

    @property
    def is_connected(self) -> bool:
        return self._sock is not None

    def connect(self):
        if self._sock:
            try:
                self._sock.sendall(b"\n")
                return
            except Exception:
                self.disconnect()
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        self._sock.settimeout(self.timeout)

    def disconnect(self):
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def send_command(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        for attempt in range(2):
            try:
                if not self._sock:
                    self.connect()
                payload = json.dumps({"endpoint": endpoint, "data": data or {}}) + "\n"
                self._sock.sendall(payload.encode())
                resp = b""
                while True:
                    chunk = self._sock.recv(65536)
                    if not chunk:
                        break
                    resp += chunk
                    if b"\n" in resp:
                        break
                result = json.loads(resp.decode().strip())
                if result.get("status") == "error":
                    msg = result.get("data", {}).get("error", "Unknown error")
                    raise ImHexError(msg)
                return result
            except (socket.timeout, ConnectionError, OSError):
                self.disconnect()
                if attempt == 1:
                    raise ImHexError("Connection lost")
            except json.JSONDecodeError as e:
                self.disconnect()
                raise ImHexError(f"Invalid JSON: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()
