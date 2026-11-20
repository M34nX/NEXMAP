"""NEXMAP application entry point.

Version 1.0.0 is currently at Stage 1: project scaffold only.
The interactive interface and network features will be implemented in
subsequent development stages.
"""
from __future__ import annotations

VERSION = "1.0.0"
PROJECT_NAME = "NEXMAP"


def main() -> int:
    """Report the current development status."""
    print(f"{PROJECT_NAME} {VERSION}")
    print("Stage 1 scaffold is in place.")
    print("Network and CLI features are not implemented yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
