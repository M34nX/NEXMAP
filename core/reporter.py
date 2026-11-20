"""Minimal JSON report writer."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def save_report(data: dict[str, Any]) -> str:
    report_dir = Path(__file__).resolve().parents[1] / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = report_dir / f"nexmap-{timestamp}.json"
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), **data}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)
