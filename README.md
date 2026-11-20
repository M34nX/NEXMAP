# NEXMAP
**Next Generation Network Mapping** — *Discover. Analyze. Secure.*

NEXMAP is a lightweight Python CLI for conservative network visibility on Termux and Linux. It uses only the Python standard library.

## Current status — v1.0.0 Stage 2
Implemented:
- CLI commands: `info`, `discover`, and `ports`.
- Local IPv4 and interface subnet detection using the OS routing table and Linux interface metadata (no data payload is sent).
- Private RFC1918 IPv4 target validation; public IP targets and IPv6 are rejected.
- Discovery auto-detects the local subnet where supported, or accepts an explicit CIDR that must contain the device's local IPv4 address.
- Discovery subnet limit: no more than 256 addresses; TCP ports 80 and 443 only; maximum 16 concurrent workers.
- Single-host TCP checks accept at most 32 explicitly selected ports.
- Explicit confirmation is required before every active check.
- Optional JSON reports for port-check results.

Not implemented yet: UDP scanning, OS fingerprinting, broad service fingerprinting, vulnerability exploitation, credential checks, or stealth features. A host that does not answer on TCP 80/443 may still be online.

## Install on Termux
```bash
pkg update
pkg install python git
git clone https://github.com/M34nX/NEXMAP.git
cd NEXMAP
git checkout v1.0.0-stage-2
python main.py --help
```

No pip packages and no root access are required.

## Usage
Show the detected local IPv4 and subnet:
```bash
python main.py info
```

Discover responsive web endpoints on the detected local subnet:
```bash
python main.py discover
```
If automatic subnet detection is unavailable, provide the private CIDR manually:
```bash
python main.py discover --target 192.168.1.0/24
```
The subnet must contain this device's detected local IPv4 address and may contain at most 256 addresses. Type `DISCOVER` at the prompt to confirm authorization.

Check selected TCP ports on one private host:
```bash
python main.py ports --target 192.168.1.1 --ports 22,53,80,443
```
Type `SCAN` at the prompt to confirm authorization. Add `--save` to write a JSON report to `reports/`.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Safety
Use only on devices and networks you own or have explicit permission to assess. NEXMAP rejects targets outside RFC1918 private ranges, limits discovery scope and concurrency, and requires an explicit confirmation phrase. TCP connect results can be affected by firewalls and filtering; they are not proof that a device is offline or vulnerable.

## License
MIT — see [LICENSE](LICENSE).
