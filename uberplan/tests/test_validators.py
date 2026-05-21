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

    def test_tier2_requires_prd_checklist(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Product / PRD checklist")
        end = text.index("## Task map / implementation graph")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_prd_checklist.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_task_map_mermaid(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Task map / implementation graph")
        end = text.index("## Tier decision")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_task_map.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_verifiable_subgoals(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Verifiable subgoals and metrics")
        end = text.index("## Parallelization plan")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_subgoals.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_parallelization_plan(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Parallelization plan")
        end = text.index("## Testing adaptation gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_parallelization.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_testing_adaptation_gate(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Testing adaptation gate")
        end = text.index("## Tier decision")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_testing_adaptation.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_goal_execution_posture(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Goal execution posture and delivery")
        end = text.index("## Product / PRD checklist")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_goal_execution_posture.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_user_expectation_surprise_assessment(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## User expectation / surprise assessment")
        end = text.index("## Product / PRD checklist")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_user_expectation.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_target_file_tree(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Target architecture / file tree")
        end = text.index("## Repository topology / package seam")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_target_file_tree.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_dead_code_tool_plan(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Code-health / dead-code tool plan")
        end = text.index("## Risk-to-evidence map")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_dead_code_plan.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_decision_tradeoff_register(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Decision / tradeoff / surprise register")
        end = text.index("## Pre-presentation over-orchestration review")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_decision_register.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_over_orchestration_review(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Pre-presentation over-orchestration review")
        end = text.index("## Plan acceptance gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_over_orchestration_review.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_plan_acceptance_gate(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Plan acceptance gate")
        end = text.index("## Pre-launch confidence gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_plan_acceptance.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_thin_harness_rubric(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Thin harness / fat agent design rubric")
        end = text.index("## Source-convention check")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_thin_harness.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_agent_execution_proof_ladder(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Agent execution proof ladder")
        end = text.index("## Source-convention check")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_agent_execution_proof_ladder.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_source_convention_check(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Source-convention check")
        end = text.index("## Agent Boundary Contract")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_source_convention.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_repository_topology(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_repository_topology_plan.md"), "--tier", "2", "--agent-behavior")

    def test_existing_file_plan_can_mark_topology_not_applicable(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace("the added validator fixture", "the validator fixture")
        text = text.replace("one small validator fixture", "the small validator fixture")
        text = text.replace("adding validator fixture coverage", "updating validator fixture coverage")
        text = text.replace("New validator/test files stay inside the existing skill package", "Existing validator/test files stay inside the existing skill package")
        text = text.replace("Add validator and fixture coverage", "Update validator and fixture coverage")
        text = text.replace("Add deterministic harness validation", "Update deterministic harness validation")
        text = text.replace("root-level", "top-level")
        text = text.replace("refactor", "cleanup")
        text = text.replace("Refactor", "Cleanup")
        start = text.index("## Target architecture / file tree")
        end = text.index("## Architecture classification")
        replacement = """## Target architecture / file tree

Not applicable because this plan only edits existing files inside their current owning package and does not add or relocate files, create root-level modules, restructure package boundaries, or change import/dependency seams.

## Repository topology / package seam

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
        self.assertIn("agentic_system_plan_requires_prd_task_map_and_thin_harness", ids)
        self.assertIn("long_running_goal_not_uberslice", ids)
        self.assertIn("agentic_plan_requires_codex_to_openclaw_proof_ladder", ids)
        self.assertIn("plan_self_reviews_over_orchestration_before_presentation", ids)
        self.assertIn("repeated_testing_failures_require_rca_replan", ids)
        self.assertIn("plan_requires_user_expectation_surprise_assessment", ids)
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
            "templates/plan-contract.md",
        ]:
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
