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


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class DeepRcaPackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_metadata_declares_implicit_utility_trigger(self) -> None:
        meta = (ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", meta)
        self.assertIn("$deep-rca", meta)
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
            copy = Path(tmp) / "deep-rca"
            shutil.copytree(ROOT, copy)
            (copy / "README.md").write_text("# duplicate docs\n")
            result = subprocess.run([sys.executable, str(copy / "scripts" / "lint_skill_package.py"), str(copy)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("README.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
