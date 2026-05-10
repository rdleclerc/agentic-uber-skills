from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
EXPECTED_TEMPLATES = [
    "simplify-plan.md",
    "complexity-inventory.md",
    "modularity-audit.md",
    "dead-code-audit.md",
    "test-confidence.md",
    "simplification-candidates.md",
    "patch-log.md",
    "final-simplification-report.md",
]


class UbersimplifyTests(unittest.TestCase):
    def run_ok(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([PY, *args], cwd=ROOT, text=True, capture_output=True, check=True)

    def run_fail(self, *args: str) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run([PY, *args], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def test_package_lint(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        self.run_ok("scripts/lint_skill_package.py", str(ROOT))

    def test_template_report_allow_template(self) -> None:
        self.run_ok("scripts/validate_simplify_report.py", "templates/final-simplification-report.md", "--allow-template")

    def test_valid_report_passes(self) -> None:
        self.run_ok("scripts/validate_simplify_report.py", "tests/fixtures/valid/final_simplification_report.md")

    def test_valid_patch_report_passes(self) -> None:
        self.run_ok("scripts/validate_simplify_report.py", "tests/fixtures/valid/final_simplification_report_patch.md")

    def test_weak_report_fails(self) -> None:
        proc = self.run_fail("scripts/validate_simplify_report.py", "tests/fixtures/invalid/final_simplification_report_weak.md")
        self.assertIn("section lacks completed substance", proc.stderr)

    def test_patch_no_tests_fails(self) -> None:
        proc = self.run_fail("scripts/validate_simplify_report.py", "tests/fixtures/invalid/patch_no_tests.md")
        self.assertIn("concrete post-patch test/eval/static command", proc.stderr)

    def test_patch_no_authorization_fails(self) -> None:
        proc = self.run_fail("scripts/validate_simplify_report.py", "tests/fixtures/invalid/patch_no_authorization.md")
        self.assertIn("explicit Patch authorization", proc.stderr)

    def test_dynamic_refs_not_checked_fails(self) -> None:
        proc = self.run_fail("scripts/validate_simplify_report.py", "tests/fixtures/invalid/dynamic_refs_not_checked.md")
        self.assertIn("dynamic-reference safeguard details", proc.stderr)

    def test_ready_yes_no_placeholder_fails(self) -> None:
        proc = self.run_fail("scripts/validate_simplify_report.py", "tests/fixtures/invalid/ready_yes_no_placeholder.md")
        self.assertIn("Ready to accept? must be exactly yes or no", proc.stderr)

    def test_rollback_vague_fails(self) -> None:
        proc = self.run_fail("scripts/validate_simplify_report.py", "tests/fixtures/invalid/rollback_vague.md")
        self.assertIn("concrete rollback/backout plan", proc.stderr)

    def test_new_simplify_run_creates_full_trail(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc = self.run_ok(
                "scripts/new_simplify_run.py",
                "--root", td,
                "--run-slug", "My Complex Refactor",
                "--mode", "audit",
                "--timestamp", "20260509T101500Z",
            )
            out = Path(proc.stdout.strip())
            for name in EXPECTED_TEMPLATES:
                self.assertTrue((out / name).exists(), name)
            self.assertIn("20260509T101500Z-my-complex-refactor", str(out))
            self.assertIn("- Mode: audit", (out / "simplify-plan.md").read_text())
            self.assertIn("- Mode: audit", (out / "final-simplification-report.md").read_text())
            self.assertIn(f"- Trail path: {out}", (out / "final-simplification-report.md").read_text())

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("audit_mode_default_no_deletion", ids)
        self.assertIn("weak_tests_block_patch_mode", ids)
        self.assertIn("modularity_fail_fast_opportunity", ids)
        self.assertIn("conflict_no_artifacts_over_trail", ids)
        self.assertIn("grep_only_does_not_delete_dynamic_code", ids)
        self.assertIn("patch_mode_requires_authorization", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertTrue(case.get("expected_behavior"))
            self.assertNotIn("required_behavior", case)


if __name__ == "__main__":
    unittest.main()
