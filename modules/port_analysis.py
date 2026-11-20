"""Bounded TCP connect checks; no payloads or exploitation."""
from __future__ import annotations

import socket


def check_tcp_port(host: str, port: int, timeout: float = 0.6) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        return sock.connect_ex((host, port)) == 0
    except OSError:
        return False
    finally:
        sock.close()


def scan_tcp_ports(host: str, ports: list[int]) -> list[dict[str, int | bool]]:
    return [{"port": port, "open": check_tcp_port(host, port)} for port in ports]
