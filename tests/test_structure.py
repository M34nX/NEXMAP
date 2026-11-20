"""Basic checks for the Stage 1 project scaffold."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_required_directories_exist(self) -> None:
        for directory in ("config", "core", "modules", "interface", "reports", "utils"):
            with self.subTest(directory=directory):
                self.assertTrue((ROOT / directory).is_dir())

    def test_required_entry_files_exist(self) -> None:
        for filename in ("main.py", "README.md", "LICENSE", "requirements.txt"):
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / filename).is_file())

    def test_settings_are_valid_json_and_safe_by_default(self) -> None:
        settings = json.loads((ROOT / "config" / "settings.json").read_text(encoding="utf-8"))
        safety = settings["safety"]
        self.assertTrue(safety["require_explicit_target_confirmation"])
        self.assertFalse(safety["allow_public_ip_targets"])
        self.assertGreater(safety["max_hosts_per_discovery"], 0)
        self.assertGreater(safety["max_tcp_ports_per_run"], 0)


if __name__ == "__main__":
    unittest.main()
