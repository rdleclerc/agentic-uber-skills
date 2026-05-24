from __future__ import annotations

import subprocess
import tempfile
import unittest
import json
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

    def test_learning_record_requires_completion_claim_regression_check(self):
        text = (ROOT / "tests" / "fixtures" / "valid" / "learning_record.md").read_text()
        start = text.index("## Completion-claim regression check")
        end = text.index("## Promotion decision")
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "missing_completion_claim_check.md"
            path.write_text(text[:start] + text[end:])
            proc = self.run_fail("scripts/validate_learning_record.py", str(path))
            self.assertIn("Completion-claim regression check", proc.stderr)

    def test_learning_record_requires_runtime_topology_lesson(self):
        text = (ROOT / "tests" / "fixtures" / "valid" / "learning_record.md").read_text()
        start = text.index("## Runtime topology lesson")
        end = text.index("## Lesson candidates")
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "missing_runtime_topology_lesson.md"
            path.write_text(text[:start] + text[end:])
            proc = self.run_fail("scripts/validate_learning_record.py", str(path))
            self.assertIn("Runtime topology lesson", proc.stderr)

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

    def test_golden_eval_schema_mentions_completion_claim_regression(self):
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("learning_promotes_completion_claim_regression", ids)
        self.assertIn("giant_plan_failure_promotes_plan_tree_layout", ids)
        self.assertIn("learning_captures_runtime_topology_lessons", ids)
        self.assertIn("learning_promotes_expensive_proof_plan_tree_validator", ids)


if __name__ == "__main__":
    unittest.main()
