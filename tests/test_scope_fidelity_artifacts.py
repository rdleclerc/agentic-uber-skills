from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_scope_fidelity_artifacts.py"
FIX = ROOT / "tests" / "fixtures" / "scope_fidelity"


def run_check(case: str, *, missing_scope: bool = False) -> subprocess.CompletedProcess[str]:
    case_dir = FIX / case
    scope = case_dir / ("missing-scope.md" if missing_scope else "scope.md")
    return subprocess.run(
        [
            sys.executable,
            str(CHECK),
            "--scope",
            str(scope),
            "--plan",
            str(case_dir / "plan.md"),
            "--acceptance",
            str(case_dir / "final.md"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class ScopeFidelityArtifactTests(unittest.TestCase):
    def test_missing_scope_file_fails(self) -> None:
        result = run_check("approved_narrowing", missing_scope=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scope.md missing", result.stderr)

    def test_unapproved_slack_only_narrowing_fails(self) -> None:
        result = run_check("unapproved_narrowing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Narrowing? yes lacks non-empty approval citation", result.stderr)

    def test_operator_approved_narrowing_passes(self) -> None:
        result = run_check("approved_narrowing")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_ship_before_scope_verdict_fails(self) -> None:
        result = run_check("ship_before_verdict")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("appears before scope-fidelity verdict", result.stderr)


if __name__ == "__main__":
    unittest.main()
