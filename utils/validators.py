"""Strict validation for RFC1918 IPv4 targets and bounded TCP port lists."""
from __future__ import annotations

import ipaddress

RFC1918 = tuple(ipaddress.ip_network(value) for value in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))


def _is_rfc1918(address: ipaddress.IPv4Address) -> bool:
    return any(address in network for network in RFC1918)


def parse_private_target(value: str) -> ipaddress.IPv4Address:
    try:
        address = ipaddress.ip_address(value.strip())
    except ValueError as exc:
        raise ValueError("Target must be a valid IPv4 address.") from exc
    if not isinstance(address, ipaddress.IPv4Address) or not _is_rfc1918(address):
        raise ValueError("Only RFC1918 private IPv4 targets are allowed.")
    return address


def parse_local_network(value: str, local_ip: str) -> ipaddress.IPv4Network:
    try:
        network = ipaddress.ip_network(value.strip(), strict=False)
        local = ipaddress.ip_address(local_ip)
    except ValueError as exc:
        raise ValueError("Enter a valid IPv4 CIDR network.") from exc
    if not isinstance(network, ipaddress.IPv4Network) or not isinstance(local, ipaddress.IPv4Address):
        raise ValueError("Only IPv4 networks are supported.")
    if not any(network.subnet_of(private) for private in RFC1918):
        raise ValueError("The target must be inside an RFC1918 private IPv4 range.")
    if network.num_addresses > 256:
        raise ValueError("Network must contain no more than 256 addresses.")
    if not _is_rfc1918(local) or local not in network:
        raise ValueError("The target network must contain this device's detected RFC1918 local IPv4 address.")
    return network


def parse_ports(value: str) -> list[int]:
    try:
        ports = sorted({int(part.strip()) for part in value.split(",") if part.strip()})
    except ValueError as exc:
        raise ValueError("Ports must be comma-separated integers.") from exc
    if not ports or len(ports) > 32 or any(port < 1 or port > 65535 for port in ports):
        raise ValueError("Choose between 1 and 32 TCP ports in the range 1-65535.")
    return ports
