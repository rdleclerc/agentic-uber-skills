from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "scripts" / "validate_assessment_packet.py"
LINT = ROOT / "scripts" / "lint_skill_package.py"
FIX = ROOT / "tests" / "fixtures"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class AssessmentPacketValidatorTests(unittest.TestCase):
    def assertPasses(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def assertFails(self, *args: str) -> subprocess.CompletedProcess[str]:
        result = run_cmd(*args)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        return result

    def test_tier1_assessment_passes(self) -> None:
        self.assertPasses(str(VALIDATE), str(FIX / "valid" / "tier1_assessment.md"), "--tier", "1")

    def test_project_matrix_is_portable_not_type0_required(self) -> None:
        text = (FIX / "valid" / "tier1_assessment.md").read_text()
        replacements = {
            "Type0": "Project Alpha",
            "Gaia": "Project Beta",
            "Soho House": "Project Gamma",
            "OpenClaw / agentic-media": "Shared Platform",
            "Agentic architecture": "Architecture Pack",
            "Uber skills": "Skill Pack",
            "Hermes": "Reflective Memory",
            "Soho ledger": "local ledger",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        with tempfile.TemporaryDirectory() as tmp:
            packet = Path(tmp) / "generic_assessment.md"
            packet.write_text(text)
            self.assertPasses(str(VALIDATE), str(packet), "--tier", "1")

    def test_tier3_agent_assessment_passes(self) -> None:
        self.assertPasses(
            str(VALIDATE),
            str(FIX / "valid" / "tier3_agent_assessment.md"),
            "--tier",
            "3",
            "--agent-system",
            "--implementation-likely",
        )

    def test_missing_source_packet_fails(self) -> None:
        result = self.assertFails(str(VALIDATE), str(FIX / "invalid" / "missing_source_packet.md"), "--tier", "1")
        self.assertIn("Source packet", result.stderr)

    def test_implementation_before_approval_must_be_no(self) -> None:
        result = self.assertFails(str(VALIDATE), str(FIX / "invalid" / "allows_implementation.md"), "--tier", "1")
        self.assertIn("Implementation before approval", result.stderr)

    def test_tier3_requires_agent_advocate(self) -> None:
        result = self.assertFails(str(VALIDATE), str(FIX / "invalid" / "tier3_missing_agent_advocate.md"), "--tier", "3")
        self.assertIn("Agent Advocate", result.stderr)

    def test_template_requires_allow_template(self) -> None:
        self.assertFails(str(VALIDATE), str(ROOT / "templates" / "assessment-packet.md"), "--tier", "1")
        self.assertPasses(str(VALIDATE), str(ROOT / "templates" / "assessment-packet.md"), "--tier", "1", "--allow-template")


class PackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("x_post_routes_to_source_packet_not_implementation", ids)
        self.assertIn("github_repo_requires_benefit_cost_and_prior_art", ids)
        self.assertIn("arxiv_agent_system_requires_agent_advocate", ids)
        self.assertIn("hype_post_can_be_rejected", ids)
        self.assertIn("idea_seed_triggers_deep_research_assessment", ids)
        self.assertIn("plan_artifact_assessment_critiques_plan_before_implementation", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertTrue(case.get("expected_behavior"))


if __name__ == "__main__":
    unittest.main()
