"""Strict validation for private IPv4 targets and bounded TCP port lists."""
from __future__ import annotations

import ipaddress


def parse_private_target(value: str) -> ipaddress.IPv4Address:
    try:
        address = ipaddress.ip_address(value.strip())
    except ValueError as exc:
        raise ValueError("Target must be a valid IPv4 address.") from exc
    if not isinstance(address, ipaddress.IPv4Address) or not address.is_private or address.is_loopback or address.is_link_local or address.is_multicast or address.is_unspecified:
        raise ValueError("Only private, unicast IPv4 targets are allowed.")
    return address


def parse_local_network(value: str, local_ip: str) -> ipaddress.IPv4Network:
    try:
        network = ipaddress.ip_network(value.strip(), strict=False)
        local = ipaddress.ip_address(local_ip)
    except ValueError as exc:
        raise ValueError("Enter a valid IPv4 CIDR network.") from exc
    if not isinstance(network, ipaddress.IPv4Network) or not isinstance(local, ipaddress.IPv4Address):
        raise ValueError("Only IPv4 networks are supported.")
    if not network.is_private or network.num_addresses > 256:
        raise ValueError("Network must be private and contain no more than 256 addresses.")
    if local not in network:
        raise ValueError("The target network must contain this device's detected local IPv4 address.")
    return network


def parse_ports(value: str) -> list[int]:
    try:
        ports = sorted({int(part.strip()) for part in value.split(",") if part.strip()})
    except ValueError as exc:
        raise ValueError("Ports must be comma-separated integers.") from exc
    if not ports or len(ports) > 32 or any(port < 1 or port > 65535 for port in ports):
        raise ValueError("Choose between 1 and 32 TCP ports in the range 1-65535.")
    return ports
