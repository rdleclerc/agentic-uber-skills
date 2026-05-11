from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
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

    def test_agent_behavior_requires_boundary_contract(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Agent Boundary Contract")
        end = text.index("## Source authority and truth boundaries")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_boundary_contract.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agent_behavior_requires_regex_keyword_semantic_gate(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Regex / keyword semantic gate")
        end = text.index("## Source authority and truth boundaries")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_regex_keyword_gate.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_repository_topology(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_repository_topology_plan.md"), "--tier", "2", "--agent-behavior")

    def test_existing_file_plan_can_mark_topology_not_applicable(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace("the added validator fixture", "the validator fixture")
        text = text.replace("one small validator fixture", "the small validator fixture")
        text = text.replace("New validator/test files stay inside the existing skill package", "Existing validator/test files stay inside the existing skill package")
        start = text.index("## Repository topology / package seam")
        end = text.index("## Architecture classification")
        replacement = """## Repository topology / package seam

Not applicable because this plan only edits existing files inside their current owning package and does not add or relocate files, create root-level modules, restructure package boundaries, or change import/dependency seams.

"""
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "existing_file_plan.md"
            plan.write_text(text[:start] + replacement + text[end:])
            self.assertPasses(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

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
        self.assertIn("agent_boundary_contract_blocks_generic_reliability_plan", ids)
        self.assertIn("semantic_regex_gate_blocks_keyword_router_plan", ids)
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
