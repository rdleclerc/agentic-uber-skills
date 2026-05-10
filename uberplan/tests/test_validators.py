from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "scripts" / "validate_plan_contract.py"
LINT = ROOT / "scripts" / "lint_skill_package.py"
FIX = ROOT / "tests" / "fixtures"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class PlanValidatorTests(unittest.TestCase):
    def assertPasses(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def assertFails(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)

    def test_tier0_plan_stays_lightweight(self) -> None:
        self.assertPasses(str(PLAN), str(FIX / "valid" / "tier0_plan.md"), "--tier", "0")

    def test_tier2_agent_plan_passes_with_agent_behavior(self) -> None:
        self.assertPasses(str(PLAN), str(FIX / "valid" / "tier2_agent_plan.md"), "--tier", "2", "--agent-behavior")

    def test_hollow_tier3_plan_fails(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "hollow_tier3_plan.md"), "--tier", "3", "--agent-behavior")

    def test_agent_behavior_requires_advocate(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_agent_advocate_plan.md"), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_repository_topology(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_repository_topology_plan.md"), "--tier", "2", "--agent-behavior")

    def test_templates_need_allow_template_mode(self) -> None:
        self.assertFails(str(PLAN), str(ROOT / "templates" / "plan-contract.md"), "--tier", "2")
        self.assertPasses(str(PLAN), str(ROOT / "templates" / "plan-contract.md"), "--tier", "2", "--allow-template")


class PackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("agent_error_triggers_advocate", ids)
        self.assertIn("complex_codebase_exploration_trail", ids)
        self.assertIn("complexity_blocked_without_benefit_gap", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertIn("expected_tier", case)
            self.assertTrue(case.get("required_behavior") or case.get("required_lanes"))

    def test_key_templates_exist(self) -> None:
        for rel in [
            "templates/plan-contract.md",
            "templates/confidence-gate.md",
            "templates/exploration-trail.md",
            "templates/first-principles-simplifier-report.md",
        ]:
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
