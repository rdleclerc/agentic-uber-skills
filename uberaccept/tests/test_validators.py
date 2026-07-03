from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPT = ROOT / "scripts" / "validate_acceptance_report.py"
ARCH = ROOT / "scripts" / "validate_architecture_steward_report.py"
LINT = ROOT / "scripts" / "lint_skill_package.py"
FIX = ROOT / "tests" / "fixtures"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class AcceptanceValidatorTests(unittest.TestCase):
    def assertPasses(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def assertFails(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)

    def test_valid_acceptance_passes(self) -> None:
        self.assertPasses(str(ACCEPT), str(FIX / "valid" / "final_acceptance.md"), "--agent-behavior")

    def test_accepted_status_passes(self) -> None:
        self.assertPasses(str(ACCEPT), str(FIX / "valid" / "final_acceptance.md"), "--agent-behavior")

    def test_rejected_with_intake_passes(self) -> None:
        self.assertPasses(str(ACCEPT), str(FIX / "valid" / "rejected_with_intake.md"))

    def test_blocked_with_failure_intake_passes(self) -> None:
        self.assertPasses(str(ACCEPT), str(FIX / "valid" / "blocked_with_failure_intake.md"))

    def test_blocked_with_not_applicable_intake_fails(self) -> None:
        result = run_cmd(str(ACCEPT), str(FIX / "invalid" / "blocked_with_na_intake.md"))
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("blocked_with_failure_intake requires failure_case_id or case_updated", result.stderr)

    def test_invalid_acceptance_status_string_fails(self) -> None:
        result = run_cmd(str(ACCEPT), str(FIX / "invalid" / "invalid_status_string.md"))
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("invalid acceptance_status", result.stderr)

    def test_cases_dir_warns_for_missing_failure_case_id(self) -> None:
        result = run_cmd(
            str(ACCEPT),
            str(FIX / "valid" / "blocked_with_failure_intake.md"),
            "--cases-dir",
            str(ROOT / "tests" / "fixtures" / "empty-cases"),
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("warning: failure_case_id has no case file", result.stdout)

    def test_rejected_without_intake_fails(self) -> None:
        result = run_cmd(str(ACCEPT), str(FIX / "invalid" / "rejected_without_intake.md"))
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("failure intake requires exactly one", result.stderr)

    def test_accepted_with_unresolved_blockers_fails(self) -> None:
        result = run_cmd(str(ACCEPT), str(FIX / "invalid" / "accepted_with_unresolved_blockers.md"))
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("Material blockers is not clear", result.stderr)

    def test_acceptance_requires_scope_fidelity_verdict(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## Scope fidelity verdict")
        end = text.index("## Rubric scores")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_scope_fidelity_verdict.md"
            report.write_text(text[:start] + text[end:])
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("scope fidelity verdict", result.stderr)

    def test_blank_acceptance_fails(self) -> None:
        self.assertFails(str(ACCEPT), str(FIX / "invalid" / "blank_acceptance.md"), "--agent-behavior")

    def test_decorated_zero_score_fails(self) -> None:
        self.assertFails(str(ACCEPT), str(FIX / "invalid" / "decorated_zero_acceptance.md"), "--agent-behavior")

    def test_code_acceptance_requires_repository_topology(self) -> None:
        self.assertFails(str(ACCEPT), str(FIX / "invalid" / "no_repository_topology_acceptance.md"), "--agent-behavior")

    def test_agent_behavior_requires_boundary_final_check(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## Agent Boundary Contract final check")
        end = text.index("## Architecture Steward final check")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_boundary_final_check.md"
            report.write_text(text[:start] + text[end:])
            self.assertFails(str(ACCEPT), str(report), "--agent-behavior")

    def test_agent_behavior_requires_regex_keyword_final_check(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## Regex / keyword semantic gate final check")
        end = text.index("## Architecture Steward final check")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_regex_keyword_final_check.md"
            report.write_text(text[:start] + text[end:])
            self.assertFails(str(ACCEPT), str(report), "--agent-behavior")

    def test_acceptance_requires_user_expectation_surprise_delta(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## User expectation / surprise delta")
        end = text.index("## Agent Advocate final check")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_user_expectation_delta.md"
            report.write_text(text[:start] + text[end:])
            self.assertFails(str(ACCEPT), str(report), "--agent-behavior")

    def test_acceptance_requires_claim_state_ledger(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## Claim-state ledger")
        end = text.index("## Planning review reconciliation")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_claim_state_ledger.md"
            report.write_text(text[:start] + text[end:])
            self.assertFails(str(ACCEPT), str(report), "--agent-behavior")

    def test_acceptance_requires_spec_fidelity_and_standards_review(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## Spec fidelity and standards review")
        end = text.index("## Runtime agent topology acceptance")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_spec_fidelity_standards.md"
            report.write_text(text[:start] + text[end:])
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("spec fidelity and standards review", result.stderr)

    def test_acceptance_requires_spec_fidelity_verdict_field(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace("- Spec fidelity verdict: pass, implemented validator/template/eval hardening matches the plan fixture.\n", "")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_spec_fidelity_verdict.md"
            report.write_text(text)
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("Spec fidelity verdict", result.stderr)

    def test_agent_behavior_requires_runtime_agent_topology_acceptance(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        start = text.index("## Runtime agent topology acceptance")
        end = text.index("## Claim-state ledger")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_runtime_topology_acceptance.md"
            report.write_text(text[:start] + text[end:])
            self.assertFails(str(ACCEPT), str(report), "--agent-behavior")

    def test_expensive_proof_requires_acceptance_section(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace(
            "## Implementation summary",
            "## Implementation summary\n\nThis Tier 3 expensive-proof production replacement proof is ready for final proof.",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_expensive_proof_acceptance.md"
            report.write_text(text)
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("expensive-proof", result.stderr)

    def test_expensive_proof_acceptance_section_passes(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace(
            "## Implementation summary",
            "## Implementation summary\n\nThis Tier 3 expensive-proof production replacement proof passed the burn-in gate and final proof acceptance checks.",
            1,
        )
        text = text.replace(
            "| Runtime agent topology | 3 | standard_6_2 policy recorded; no depth-3 escalation; child-agent depth policy checked | none |",
            "| Runtime agent topology | 3 | standard_6_2 policy recorded; no depth-3 escalation; child-agent depth policy checked | none |\n| Tier 3 expensive-proof | 3 | validator result, risk inventory, observability telemetry, phase-boundary contract-fuzz, burn-in/final proof separation, stop/replan, and child status ledger inspected | none |",
        )
        section = """## Tier 3 expensive-proof acceptance

- Expensive-proof scope applies? yes, Tier 3 expensive-proof production replacement final proof.
- Plan validator command/result: `validate_plan_contract.py plan.md --tier 3 --agent-behavior` passed.
- Risk/failure-class inventory inspected: risk inventory covers receipt failure, contract boundary failure, telemetry blind spot failure.
- Observability / telemetry preflight evidence: observability telemetry preflight passed with trace/log/metric/receipt smoke evidence.
- Phase-boundary / contract-fuzz preflight evidence: phase-boundary contract-fuzz preflight passed malformed/truncated/missing-field negative fixtures.
- Burn-in vs final-proof separation evidence: burn-in and final proof were separate gates; burn-in artifacts were not reused as final proof.
- Stop/replan evidence: stop and replan rules were inspected and RCA child-plan path was used for failures.
- Child-plan/status-ledger evidence: child plan status ledger lists observability, contract-fuzz, burn-in, and final-proof children.
- Flat-plan exception / bypass approval: no bypass; child/status ledger evidence exists.
- Expensive-proof acceptance verdict: pass/accept within scope.

"""
        insertion = text.index("## Claim-state ledger")
        text = text[:insertion] + section + text[insertion:]
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "expensive_proof_acceptance.md"
            report.write_text(text)
            self.assertPasses(str(ACCEPT), str(report), "--agent-behavior")

    def test_acceptance_rejects_shared_spine_parent_completion(self) -> None:
        result = run_cmd(str(ACCEPT), str(FIX / "invalid" / "shared_spine_parent_completion_acceptance.md"), "--agent-behavior")
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("proof-only/shared-spine", result.stderr)

    def test_production_active_blocker_rejects_parent_completion(self) -> None:
        result = run_cmd(str(ACCEPT), str(FIX / "invalid" / "production_active_blocker_acceptance.md"), "--agent-behavior")
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("runnable safe next actions", result.stderr)
        self.assertIn("Safe-work exhaustion", result.stderr)

    def test_production_hard_blocked_after_exhaustion_passes(self) -> None:
        self.assertPasses(str(ACCEPT), str(FIX / "valid" / "production_hard_blocked_acceptance.md"), "--agent-behavior")

    def test_production_completion_requires_safe_work_exhaustion_review(self) -> None:
        text = (FIX / "valid" / "production_hard_blocked_acceptance.md").read_text()
        start = text.index("## Safe-work exhaustion adversarial review")
        end = text.index("## Claim-state ledger")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_safe_work_exhaustion_review.md"
            report.write_text(text[:start] + text[end:])
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("Safe-work exhaustion adversarial review", result.stderr)

    def test_existing_file_acceptance_can_mark_topology_not_applicable(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace(
            "| Repository topology | 3 | package topology/dependency evidence: changed validator scripts stayed inside the existing skill package; package lint and validator tests passed | none |",
            "| Repository topology | 2 | not applicable; existing package files changed in place; file layout and package layout unchanged | no topology gate required |",
        )
        text = text.replace(
            "| topology/dependency | package-local validator scripts plus scripts/lint_skill_package.py . | pass |",
            "| topology/dependency | not applicable; existing package layout unchanged | pass |",
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "existing_file_acceptance.md"
            report.write_text(text)
            self.assertPasses(str(ACCEPT), str(report), "--agent-behavior")

    def test_defect_fix_claim_requires_reproduced_red_or_no_repro_reason(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace(
            "Hardened validators, metadata, templates, package lint, and golden eval fixtures for the skill package.",
            "Hardened validators, metadata, templates, package lint, and golden eval fixtures for the skill package. This fixes a regression in the acceptance validator.",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_reproduced_red.md"
            report.write_text(text)
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("defect-fix claim requires reproduced_red", result.stderr)

    def test_defect_fix_claim_accepts_no_repro_reason(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace(
            "Hardened validators, metadata, templates, package lint, and golden eval fixtures for the skill package.",
            "Hardened validators, metadata, templates, package lint, and golden eval fixtures for the skill package. This fixes a regression in documentation-only acceptance wording.",
            1,
        )
        text = text.replace(
            "- not_applicable_with_reason: no failure observed",
            "- not_applicable_with_reason: no failure observed\n- no_repro_reason: documentation-only regression; no executable baseline existed.",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "no_repro_reason.md"
            report.write_text(text)
            self.assertPasses(str(ACCEPT), str(report), "--agent-behavior")

    def test_external_mock_requires_interface_shape_receipt(self) -> None:
        text = (FIX / "valid" / "final_acceptance.md").read_text()
        text = text.replace(
            "Hardened validators, metadata, templates, package lint, and golden eval fixtures for the skill package.",
            "Hardened validators, metadata, templates, package lint, and golden eval fixtures for the skill package. A mock external provider stood in for the real interface.",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "missing_interface_shape_receipt.md"
            report.write_text(text)
            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("interface_shape_receipt", result.stderr)

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

    def test_architecture_steward_requires_repository_topology_dimension(self) -> None:
        self.assertFails(str(ARCH), str(FIX / "invalid" / "missing_repository_topology_architecture_report.md"))

    def test_architecture_template_needs_allow_template_mode(self) -> None:
        self.assertFails(str(ARCH), str(ROOT / "templates" / "architecture-steward-report.md"))
        self.assertPasses(str(ARCH), str(ROOT / "templates" / "architecture-steward-report.md"), "--allow-template")


class PackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("final_acceptance_blocks_missing_tests", ids)
        self.assertIn("agentic_change_requires_advocate_final_check", ids)
        self.assertIn("complexity_final_pass_deletes_or_defers", ids)
        self.assertIn("skill_change_triggers_evolver", ids)
        self.assertIn("flat_module_acceptance_requires_topology_evidence", ids)
        self.assertIn("agent_boundary_contract_acceptance_blocks_generic_reliability", ids)
        self.assertIn("semantic_regex_gate_acceptance_blocks_keyword_router", ids)
        self.assertIn("final_acceptance_checks_user_expectation_delta", ids)
        self.assertIn("acceptance_rejects_shared_safe_spine_completion", ids)
        self.assertIn("acceptance_reads_plan_tree_child_receipts", ids)
        self.assertIn("acceptance_rejects_missing_runtime_topology", ids)
        self.assertIn("acceptance_rejects_flat_expensive_proof", ids)
        self.assertIn("acceptance_rejects_production_active_blocker_completion", ids)
        self.assertIn("acceptance_requires_safe_work_exhaustion_adversarial_review", ids)
        self.assertIn("acceptance_separates_spec_fidelity_from_repo_standards", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertTrue(case.get("required_behavior"))


if __name__ == "__main__":
    unittest.main()
