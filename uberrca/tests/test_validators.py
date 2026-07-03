from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINT = ROOT / "scripts" / "lint_skill_package.py"
RCA = ROOT / "scripts" / "validate_rca_artifact.py"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class UberRcaPackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_metadata_declares_implicit_utility_trigger(self) -> None:
        meta = (ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", meta)
        self.assertIn("$uberrca", meta)
        self.assertIn("proximate cause", meta)

    def test_golden_eval_schema_and_trigger_mix(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        self.assertGreaterEqual(len(cases), 4)
        self.assertTrue(any(case["should_trigger"] for case in cases))
        self.assertTrue(any(not case["should_trigger"] for case in cases))
        ids = {case["id"] for case in cases}
        self.assertIn("repeated_agent_patch_requires_class_rca", ids)
        self.assertIn("five_repeated_test_failures_trigger_rca", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertIn("required_behavior", case)
            self.assertIsInstance(case["should_trigger"], bool)

    def test_lint_rejects_auxiliary_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "uberrca"
            shutil.copytree(ROOT, copy)
            (copy / "README.md").write_text("# duplicate docs\n")
            result = subprocess.run([sys.executable, str(copy / "scripts" / "lint_skill_package.py"), str(copy)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("README.md", result.stderr)

    def test_rca_artifact_validator(self) -> None:
        self.assertEqual(run_cmd(str(RCA), str(ROOT / "templates" / "rca-artifact.md"), "--allow-template").returncode, 0)
        valid = run_cmd(str(RCA), str(ROOT / "tests" / "fixtures" / "valid" / "rca_artifact.md"))
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)

        missing_invariant = run_cmd(str(RCA), str(ROOT / "tests" / "fixtures" / "invalid" / "rca_artifact_missing_invariant.md"))
        self.assertNotEqual(missing_invariant.returncode, 0)
        self.assertIn("class_invariant", missing_invariant.stderr)

        missing_surface = run_cmd(str(RCA), str(ROOT / "tests" / "fixtures" / "invalid" / "rca_artifact_missing_surface.md"))
        self.assertNotEqual(missing_surface.returncode, 0)
        self.assertIn("surface enumeration", missing_surface.stderr)

        placeholder_surface = run_cmd(str(RCA), str(ROOT / "tests" / "fixtures" / "invalid" / "rca_artifact_placeholder_surface.md"))
        self.assertNotEqual(placeholder_surface.returncode, 0)
        self.assertIn("surface_enumeration", placeholder_surface.stderr)

        missing_intake = run_cmd(str(RCA), str(ROOT / "tests" / "fixtures" / "invalid" / "rca_artifact_missing_intake.md"))
        self.assertNotEqual(missing_intake.returncode, 0)
        self.assertIn("failure intake requires exactly one", missing_intake.stderr)


if __name__ == "__main__":
    unittest.main()
