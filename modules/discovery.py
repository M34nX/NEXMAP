"""Conservative TCP-based discovery on a validated private local subnet."""
from __future__ import annotations

import concurrent.futures
import ipaddress

from modules.port_analysis import check_tcp_port

DISCOVERY_PORTS = (80, 443)
MAX_WORKERS = 16


def _probe(address: str) -> dict[str, object] | None:
    open_ports = [port for port in DISCOVERY_PORTS if check_tcp_port(address, port, timeout=0.35)]
    if not open_ports:
        return None
    return {"ip": address, "open_ports": open_ports}


def discover_hosts(network: ipaddress.IPv4Network) -> list[dict[str, object]]:
    """Return hosts accepting TCP on 80/443. Silent hosts may still be online."""
    addresses = [str(ip) for ip in network.hosts()]
    found: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for result in pool.map(_probe, addresses):
            if result is not None:
                found.append(result)
    return found
