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
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertTrue(case.get("required_behavior"))


if __name__ == "__main__":
    unittest.main()
