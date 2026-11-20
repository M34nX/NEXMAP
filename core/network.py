"""Small, dependency-free local network helpers."""
from __future__ import annotations

import socket


def get_local_ipv4() -> str | None:
    """Return the IPv4 address selected for the default route, without sending data."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("192.0.2.1", 80))
        address = sock.getsockname()[0]
        return address if not address.startswith("127.") else None
    except OSError:
        return None
    finally:
        sock.close()
