"""Small, dependency-free local network helpers for Linux and Termux."""
from __future__ import annotations

import ipaddress
import socket
import struct

try:
    import fcntl
except ImportError:  # pragma: no cover - Linux/Termux is the supported target
    fcntl = None


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


def get_local_network() -> ipaddress.IPv4Network | None:
    """Try to read the selected interface's IPv4 netmask using Linux ioctl."""
    if fcntl is None:
        return None
    local_ip = get_local_ipv4()
    if not local_ip:
        return None
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for _, name in socket.if_nameindex():
            request = struct.pack("256s", name[:15].encode("utf-8"))
            try:
                address_data = fcntl.ioctl(sock.fileno(), 0x8915, request)
                interface_ip = socket.inet_ntoa(address_data[20:24])
                if interface_ip != local_ip:
                    continue
                mask_data = fcntl.ioctl(sock.fileno(), 0x891B, request)
                netmask = socket.inet_ntoa(mask_data[20:24])
                return ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
            except OSError:
                continue
    except OSError:
        return None
    finally:
        sock.close()
    return None
