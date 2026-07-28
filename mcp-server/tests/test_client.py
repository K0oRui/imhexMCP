import json
import socket
import threading

from client import ImHexClient, ImHexError


def test_send_command():
    results = []

    def server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        results.append(port)
        s.listen(1)
        s.settimeout(3)
        conn, _ = s.accept()
        data = conn.recv(4096)
        req = json.loads(data.decode().strip())
        assert req["endpoint"] == "test/ping"
        conn.sendall(
            json.dumps({"status": "ok", "data": {"pong": True}}).encode() + b"\n"
        )
        conn.close()
        s.close()

    t = threading.Thread(target=server, daemon=True)
    t.start()
    port = results[0] if results else None

    # Wait for port
    import time

    time.sleep(0.2)
    port = results[0]

    c = ImHexClient(host="127.0.0.1", port=port, timeout=3)
    resp = c.send_command("test/ping")
    assert resp["data"]["pong"] is True


def test_send_command_error():
    results = []

    def server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        results.append(port)
        s.listen(1)
        s.settimeout(3)
        conn, _ = s.accept()
        conn.recv(4096)
        conn.sendall(
            json.dumps({"status": "error", "data": {"error": "bad stuff"}}).encode()
            + b"\n"
        )
        conn.close()
        s.close()

    threading.Thread(target=server, daemon=True).start()
    import time

    time.sleep(0.2)
    port = results[0]

    c = ImHexClient(host="127.0.0.1", port=port, timeout=3)
    try:
        c.send_command("test/error")
        assert False, "Expected ImHexError"
    except ImHexError as e:
        assert "bad stuff" in str(e)


def test_connection_refused():
    c = ImHexClient(host="127.0.0.1", port=1, timeout=1)
    try:
        c.send_command("test/fail")
        assert False, "Expected error"
    except (ConnectionRefusedError, OSError, ImHexError):
        pass
