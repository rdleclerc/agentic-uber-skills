from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = "python3"


class ValidatorTests(unittest.TestCase):
    def run_ok(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([PY, *args], cwd=ROOT, text=True, capture_output=True, check=True)

    def run_fail(self, *args: str) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run([PY, *args], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def test_learning_record_valid(self):
        self.run_ok("scripts/validate_learning_record.py", "tests/fixtures/valid/learning_record.md")

    def test_learning_record_requires_evidence_and_decision(self):
        proc = self.run_fail("scripts/validate_learning_record.py", "tests/fixtures/invalid/learning_record_missing_evidence.md")
        self.assertIn("Evidence links", proc.stderr)
        self.assertIn("Promotion decision", proc.stderr)

    def test_promotion_batch_valid(self):
        self.run_ok("scripts/validate_promotion_batch.py", "tests/fixtures/valid/promotion_batch.md")

    def test_promotion_batch_rejects_auto_mutation(self):
        proc = self.run_fail("scripts/validate_promotion_batch.py", "tests/fixtures/invalid/promotion_batch_auto_mutation.md")
        self.assertIn("forbidden", proc.stderr)

    def test_lint_skill_package(self):
        self.run_ok("scripts/lint_skill_package.py", str(ROOT))

    def test_new_learning_record_creates_timestamped_template(self):
        with tempfile.TemporaryDirectory() as td:
            proc = self.run_ok(
                "scripts/new_learning_record.py",
                "--root", td,
                "--skill", "UberGoal",
                "--run-slug", "Big Plan!",
                "--timestamp", "20260509T090000",
            )
            path = Path(proc.stdout.strip())
            self.assertTrue(path.exists())
            self.assertIn("ubergoal/20260509T090000-big-plan/post-run-learning.md", str(path))
            text = path.read_text()
            self.assertIn("- Skill(s): UberGoal", text)
            self.assertIn("- Run slug: big-plan", text)


if __name__ == "__main__":
    unittest.main()
