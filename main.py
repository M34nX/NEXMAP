"""NEXMAP: conservative, authorized local-network diagnostics."""
from __future__ import annotations

import argparse
import sys

from core.network import get_local_ipv4, get_local_network
from core.reporter import save_report
from modules.discovery import discover_hosts
from modules.port_analysis import scan_tcp_ports
from utils.validators import parse_local_network, parse_private_target, parse_ports

VERSION = "1.0.0"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexmap",
        description="Conservative network visibility for explicitly authorized private networks.",
        epilog="Only scan systems and networks you own or have explicit permission to assess.",
    )
    parser.add_argument("--version", action="version", version=f"NEXMAP {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("info", help="show local IPv4 and detected network information")
    discover = sub.add_parser("discover", help="check a small private local subnet for responsive hosts")
    discover.add_argument("--target", help="optional private IPv4 CIDR; auto-detected if omitted")
    ports = sub.add_parser("ports", help="check selected TCP ports on one private host")
    ports.add_argument("--target", required=True, help="private IPv4 address")
    ports.add_argument("--ports", default="22,53,80,443,445,8080", help="comma-separated TCP ports (max 32)")
    ports.add_argument("--save", action="store_true", help="save a JSON report under reports/")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    local_ip = get_local_ipv4()
    local_network = get_local_network()
    if args.command == "info":
        print(f"NEXMAP {VERSION}")
        print(f"Detected local IPv4: {local_ip or 'unavailable'}")
        print(f"Detected local network: {local_network or 'unavailable'}")
        print("Active scanning: disabled until a command and target are explicitly supplied.")
        return 0

    if not local_ip:
        print("Error: could not determine the device's local IPv4 address. Check Wi-Fi/network connectivity.", file=sys.stderr)
        return 2

    if args.command == "discover":
        requested = args.target or (str(local_network) if local_network else None)
        if not requested:
            print("Error: automatic subnet detection failed. Supply --target with your private local CIDR.", file=sys.stderr)
            return 2
        try:
            network = parse_local_network(requested, local_ip)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2
        print(f"Target: {network} ({network.num_addresses} addresses)")
        print(f"Your device: {local_ip}")
        print("This performs limited TCP connection checks on ports 80 and 443.")
        answer = input("Confirm you own this network or have explicit permission. Type DISCOVER to continue: ").strip()
        if answer != "DISCOVER":
            print("Cancelled.")
            return 1
        results = discover_hosts(network)
        print(f"Responsive hosts: {len(results)}")
        for host in results:
            print(f"  {host['ip']}  open TCP: {','.join(map(str, host['open_ports']))}")
        return 0

    if args.command == "ports":
        try:
            target = parse_private_target(args.target)
            ports = parse_ports(args.ports)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2
        print(f"Target: {target}; TCP ports: {','.join(map(str, ports))}")
        print("Only proceed if you are authorized to assess this device.")
        answer = input("Type SCAN to confirm and continue: ").strip()
        if answer != "SCAN":
            print("Cancelled.")
            return 1
        results = scan_tcp_ports(str(target), ports)
        for item in results:
            state = "open" if item["open"] else "closed|filtered"
            print(f"  {item['port']}/tcp: {state}")
        if args.save:
            path = save_report({"tool": "NEXMAP", "version": VERSION, "target": str(target), "results": results})
            print(f"JSON report: {path}")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
