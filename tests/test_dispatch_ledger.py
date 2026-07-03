from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_dispatch_ledger.py"
FIXTURES = ROOT / "tests" / "fixtures" / "dispatch_ledger"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)], cwd=ROOT, text=True, capture_output=True)


class DispatchLedgerValidatorTests(unittest.TestCase):
    def test_valid_dispatch_ledger_passes(self) -> None:
        result = run_validator(FIXTURES / "valid.md")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS: dispatch ledger", result.stdout)

    def test_duplicate_non_retry_work_item_fails(self) -> None:
        result = run_validator(FIXTURES / "duplicate_non_retry.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate non-retry work_item", result.stderr)


if __name__ == "__main__":
    unittest.main()
