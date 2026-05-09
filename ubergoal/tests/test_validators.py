from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "scripts" / "validate_plan_contract.py"
ACCEPT = ROOT / "scripts" / "validate_acceptance_report.py"
ARCH = ROOT / "scripts" / "validate_architecture_steward_report.py"
LINT = ROOT / "scripts" / "lint_skill_package.py"
GOAL = ROOT / "scripts" / "validate_goal_objective.py"
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

    def test_tier2_requires_advocate_even_without_flag(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_agent_advocate_plan.md"), "--tier", "2")

    def test_templates_need_allow_template_mode(self) -> None:
        self.assertFails(str(PLAN), str(ROOT / "templates" / "plan-contract.md"), "--tier", "2")
        self.assertPasses(str(PLAN), str(ROOT / "templates" / "plan-contract.md"), "--tier", "2", "--allow-template")


class AcceptanceValidatorTests(unittest.TestCase):
    def assertPasses(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def assertFails(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)

    def test_valid_acceptance_passes(self) -> None:
        self.assertPasses(str(ACCEPT), str(FIX / "valid" / "final_acceptance.md"), "--agent-behavior")

    def test_blank_acceptance_fails(self) -> None:
        self.assertFails(str(ACCEPT), str(FIX / "invalid" / "blank_acceptance.md"), "--agent-behavior")

    def test_decorated_zero_score_fails(self) -> None:
        self.assertFails(str(ACCEPT), str(FIX / "invalid" / "decorated_zero_acceptance.md"), "--agent-behavior")

    def test_template_needs_allow_template_mode(self) -> None:
        self.assertFails(str(ACCEPT), str(ROOT / "templates" / "final-acceptance.md"))
        self.assertPasses(str(ACCEPT), str(ROOT / "templates" / "final-acceptance.md"), "--allow-template")


class ArchitectureStewardValidatorTests(unittest.TestCase):
    def assertPasses(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def assertFails(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)

    def test_valid_architecture_steward_report_passes(self) -> None:
        self.assertPasses(str(ARCH), str(FIX / "valid" / "architecture_steward_report.md"))

    def test_blank_architecture_steward_report_fails(self) -> None:
        self.assertFails(str(ARCH), str(FIX / "invalid" / "blank_architecture_steward_report.md"))

    def test_architecture_template_needs_allow_template_mode(self) -> None:
        self.assertFails(str(ARCH), str(ROOT / "templates" / "architecture-steward-report.md"))
        self.assertPasses(str(ARCH), str(ROOT / "templates" / "architecture-steward-report.md"), "--allow-template")


class PackageLintAndEvalTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        self.assertGreaterEqual(len(cases), 5)
        ids = {case["id"] for case in cases}
        self.assertIn("tier0_tiny_doc_fix", ids)
        self.assertIn("agent_error_triggers_advocate", ids)
        self.assertIn("openclaw_runtime_triggers_platform_lane", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertIn("expected_tier", case)
            self.assertTrue(case.get("required_behavior") or case.get("required_lanes"))


class GoalObjectiveValidatorTests(unittest.TestCase):
    def test_goal_objective_accepts_compact_goal(self) -> None:
        result = subprocess.run(
            [sys.executable, str(GOAL), "--target-chars", "3400", "--strict-target"],
            cwd=ROOT,
            text=True,
            input="/goal Destination: tests pass. Verification: run unit tests. Done/stop: report evidence.",
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("objective_chars=", result.stdout)

    def test_goal_objective_rejects_near_limit(self) -> None:
        too_long = "/goal " + ("x" * 3800)
        result = subprocess.run(
            [sys.executable, str(GOAL)],
            cwd=ROOT,
            text=True,
            input=too_long,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)


if __name__ == "__main__":
    unittest.main()
