"""Public orchestration facade for scan modules."""
from modules.discovery import discover_hosts
from modules.port_analysis import scan_tcp_ports

__all__ = ["discover_hosts", "scan_tcp_ports"]
