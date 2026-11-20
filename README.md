# NEXMAP
**Next Generation Network Mapping**  
*Discover. Analyze. Secure.*

NEXMAP is a lightweight, modular Python network visibility and security-assessment project for Termux (Android) and Linux.

> **Development status:** Version 1.0.0 is being developed in stages. This branch completes **Stage 1 (project scaffold)** only. Network discovery, port analysis, service identification, diagnostics, security assessment, and reporting are not implemented yet.

## Project goals
- Provide useful, evidence-based network visibility for systems and networks the operator is authorized to assess.
- Run without assuming root privileges.
- Keep dependencies and resource use low for Termux and Linux.
- Separate interface, network operations, analysis, validation, and reporting.
- Use conservative limits, explicit target confirmation, and safe defaults.
- Never claim a vulnerability based on insufficient evidence.

## Architecture
```text
NEXMAP/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── config/settings.json
├── core/{__init__.py, scanner.py, network.py, analyzer.py, reporter.py}
├── modules/{__init__.py, discovery.py, port_analysis.py, service_detection.py, security_audit.py}
├── interface/{__init__.py, banner.py, menu.py}
├── reports/.gitkeep
├── tests/{__init__.py, test_structure.py}
└── utils/{__init__.py, validators.py, logger.py}
```

## Development stages
1. **Stage 1 — Project structure:** package layout, configuration baseline, documentation, and scaffold test.
2. **Stage 2 — Terminal interface:** consistent CLI, banner, menu, and input handling.
3. **Stage 3 — Network diagnostics:** interfaces, addresses, DNS, and connectivity information.
4. **Stage 4 — Authorized discovery:** conservative discovery on explicitly authorized local networks.
5. **Stage 5 — Port and service analysis:** bounded TCP checks and evidence-based service identification.
6. **Stage 6 — Security assessment:** explainable configuration checks and recommendations.
7. **Stage 7 — Reporting:** timestamped TXT and JSON reports.
8. **Stage 8 — Validation and optimization:** automated tests and Termux/Linux compatibility checks.

## Requirements
- Python 3.10 or newer (target baseline; compatibility will be verified during implementation).
- Stage 1 uses only the Python standard library.
- No root access is required for the project scaffold.

## Installation
### Termux
```bash
pkg update
pkg install python git
git clone https://github.com/M34nX/NEXMAP.git
cd NEXMAP
git checkout v1.0.0-stage-1
python main.py
```

### Linux
```bash
sudo apt update
sudo apt install python3 git
git clone https://github.com/M34nX/NEXMAP.git
cd NEXMAP
git checkout v1.0.0-stage-1
python3 main.py
```

The current entry point intentionally reports that implementation is pending. It is not a working scanner yet.

## Tests
Run from the repository root:
```bash
python -m unittest discover -s tests -v
```

## Authorization and safe use
Future active network checks are intended only for systems and networks for which the operator has explicit permission. The implementation must reject public-range targets by default, require clear confirmation, apply conservative limits, and avoid exploitation, credential theft, persistence, stealth, and evasion.

## License
MIT. See [LICENSE](LICENSE).
