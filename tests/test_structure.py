"""Project structure and safety-default tests."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_required_directories_exist(self):
        for directory in ("config", "core", "modules", "interface", "reports", "utils", "tests"):
            self.assertTrue((ROOT / directory).is_dir(), directory)

    def test_required_entry_files_exist(self):
        for filename in ("main.py", "README.md", "LICENSE", "requirements.txt"):
            self.assertTrue((ROOT / filename).is_file(), filename)

    def test_settings_are_valid_json_and_safe_by_default(self):
        settings = json.loads((ROOT / "config" / "settings.json").read_text(encoding="utf-8"))
        safety = settings["safety"]
        self.assertTrue(safety["require_explicit_target_confirmation"])
        self.assertFalse(safety["allow_public_ip_targets"])
        self.assertLessEqual(safety["max_hosts_per_discovery"], 256)


if __name__ == "__main__":
    unittest.main()
