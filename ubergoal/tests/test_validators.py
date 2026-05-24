from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "scripts" / "validate_goal_objective.py"
RECEIPT = ROOT / "scripts" / "validate_uber_run_receipt.py"
LINT = ROOT / "scripts" / "lint_skill_package.py"


def run_cmd(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, input=input_text, capture_output=True)


class ThinWrapperTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_skill_body_is_thin_and_routes(self) -> None:
        text = (ROOT / "SKILL.md").read_text()
        self.assertLess(len(text.splitlines()), 160)
        self.assertIn("$uberplan", text)
        self.assertIn("$uberaccept", text)
        self.assertIn("$uberskillevolver", text)
        self.assertIn("$ubersimplify", text)
        self.assertIn("$uberassess", text)
        self.assertIn("Implementation effort recommendation", text)
        self.assertIn("`medium`", text)
        self.assertIn("`high`", text)
        self.assertIn("`xhigh`", text)
        self.assertIn("deletion-first pass", text)
        self.assertIn("policy-adherence", text)
        self.assertIn("OpenClaw/agentic architecture", text)
        self.assertIn("no solo self-certification", text)
        self.assertIn("Skills invoked summary", text)
        self.assertIn("Uber run receipt", text)
        self.assertIn("five consecutive failures", text)
        self.assertIn("ubercampaign", text)
        self.assertIn("references/campaign-profile.md", text)
        self.assertIn("user expectation / surprise assessment", text)
        self.assertIn("$deep-rca", text)
        self.assertNotIn("## Planning review board", text)

    def test_monolith_files_are_absent(self) -> None:
        for rel in [
            "templates/plan-contract.md",
            "templates/final-acceptance.md",
            "scripts/validate_plan_contract.py",
            "scripts/validate_acceptance_report.py",
        ]:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_goal_ledger_has_skills_used_summary(self) -> None:
        text = (ROOT / "templates" / "goal-ledger.md").read_text()
        self.assertIn("## Uber run receipt", text)
        self.assertIn("## User expectation / surprise assessment", text)
        self.assertIn("## Skills invoked summary", text)
        for skill in ["ubergoal", "uberassess", "uberplan", "uberaccept", "ubersimplify", "uberskillevolver", "ubershow", "deep-rca", "uber-skill-creator"]:
            self.assertIn(skill, text)

    def test_uber_run_receipt_validator(self) -> None:
        self.assertEqual(run_cmd(str(RECEIPT), str(ROOT / "templates" / "uber-run-receipt.md"), "--allow-template").returncode, 0)
        valid = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "valid" / "uber_run_receipt.md"))
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)
        missing = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "invalid" / "uber_run_receipt_missing_skill.md"))
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("skills invoked table missing skill", missing.stderr)
        failed_gate = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "invalid" / "uber_run_receipt_failed_gate.md"))
        self.assertNotEqual(failed_gate.returncode, 0)
        self.assertIn("expected gate did not pass", failed_gate.stderr)
        shared_spine = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "invalid" / "uber_run_receipt_shared_spine_parent_complete.md"))
        self.assertNotEqual(shared_spine.returncode, 0)
        self.assertIn("shared-spine", shared_spine.stderr)
        missing_terminal = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "invalid" / "uber_run_receipt_missing_child_terminal_states.md"))
        self.assertNotEqual(missing_terminal.returncode, 0)
        self.assertIn("invalid terminal state", missing_terminal.stderr)
        missing_topology = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "invalid" / "uber_run_receipt_missing_runtime_topology.md"))
        self.assertNotEqual(missing_topology.returncode, 0)
        self.assertIn("Runtime agent topology", missing_topology.stderr)
        active_blocker = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "invalid" / "uber_run_receipt_production_active_blocker.md"))
        self.assertNotEqual(active_blocker.returncode, 0)
        self.assertIn("runnable safe next actions", active_blocker.stderr)
        hard_blocked = run_cmd(str(RECEIPT), str(ROOT / "tests" / "fixtures" / "valid" / "uber_run_receipt_production_hard_blocked.md"))
        self.assertEqual(hard_blocked.returncode, 0, hard_blocked.stderr + hard_blocked.stdout)

    def test_uber_run_receipt_validator_accepts_legacy_skill_labels(self) -> None:
        text = (ROOT / "tests" / "fixtures" / "valid" / "uber_run_receipt.md").read_text()
        legacy = (
            text.replace("## Skills invoked", "## Skills used")
            .replace("RCA-driven testing adaptation", "Repeated-test-failure adaptation")
            .replace("Skills invoked summary", "Skills used summary")
            .replace("uber-skill-creator", "skill-creator")
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "legacy_uber_run_receipt.md"
            path.write_text(legacy)
            result = run_cmd(str(RECEIPT), str(path))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("routes_planning_to_uberplan", ids)
        self.assertIn("routes_acceptance_to_uberaccept", ids)
        self.assertIn("skill_change_routes_learning_to_evolver", ids)
        self.assertIn("tiny_task_stays_light", ids)
        self.assertIn("routes_simplification_to_ubersimplify", ids)
        self.assertIn("one_line_refactor_campaign_uses_profile", ids)
        self.assertIn("recurring_refactor_campaign_uses_history", ids)
        self.assertIn("multi_feature_campaign_uses_campaign_profile", ids)
        self.assertIn("routes_source_assessment_to_uberassess", ids)
        self.assertIn("final_policy_adherence_check_reports_surprises", ids)
        self.assertIn("final_handoff_reports_skills_used", ids)
        self.assertIn("uber_run_receipt_enables_skill_evolution", ids)
        self.assertIn("repeated_test_failures_trigger_rca_replan", ids)
        self.assertIn("unexpected_test_failure_triggers_rca_scope_append", ids)
        self.assertIn("user_expectation_surprise_gate", ids)
        self.assertIn("parent_completion_requires_child_terminal_states", ids)
        self.assertIn("executes_uberplan_plan_tree_layout", ids)
        self.assertIn("campaign_depth3_prompts_for_escalation", ids)
        self.assertIn("production_goal_active_blocker_keeps_parent_active", ids)
        route_case = next(case for case in cases if case["id"] == "routes_simplification_to_ubersimplify")
        self.assertTrue(any("ubersimplify" in item for item in route_case.get("expected_behavior", [])))
        refactor_case = next(case for case in cases if case["id"] == "one_line_refactor_campaign_uses_profile")
        self.assertTrue(any("profile" in item for item in refactor_case.get("expected_behavior", [])))
        history_case = next(case for case in cases if case["id"] == "recurring_refactor_campaign_uses_history")
        self.assertTrue(any("history" in item for item in history_case.get("expected_behavior", [])))
        campaign_case = next(case for case in cases if case["id"] == "multi_feature_campaign_uses_campaign_profile")
        self.assertTrue(any("campaign-profile" in item or "ubercampaign" in item for item in campaign_case.get("expected_behavior", [])))
        assess_case = next(case for case in cases if case["id"] == "routes_source_assessment_to_uberassess")
        self.assertTrue(any("uberassess" in item for item in assess_case.get("expected_behavior", [])))
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertTrue(case.get("expected_behavior"))


class GoalObjectiveValidatorTests(unittest.TestCase):
    def test_goal_objective_accepts_compact_goal(self) -> None:
        result = run_cmd(
            str(GOAL),
            "--target-chars", "3400",
            "--strict-target",
            input_text="/goal Destination: tests pass. Verification: run unit tests. Done/stop: report evidence.",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("objective_chars=", result.stdout)

    def test_goal_objective_rejects_near_limit(self) -> None:
        too_long = "/goal " + ("x" * 3800)
        result = run_cmd(str(GOAL), input_text=too_long)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)


if __name__ == "__main__":
    unittest.main()
