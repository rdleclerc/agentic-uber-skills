from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackContractTests(unittest.TestCase):
    def test_pack_contract_lint_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/lint_pack_contract.py", "--root", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_only_ubergoal_is_implicit(self) -> None:
        expected = {
            "ubergoal": "allow_implicit_invocation: true",
            "uberplan": "allow_implicit_invocation: false",
            "uberaccept": "allow_implicit_invocation: false",
            "uberskillevolver": "allow_implicit_invocation: false",
            "ubersimplify": "allow_implicit_invocation: false",
            "uberassess": "allow_implicit_invocation: false",
        }
        for skill, phrase in expected.items():
            text = (ROOT / skill / "agents" / "openai.yaml").read_text()
            self.assertIn(phrase, text, skill)
            if skill != "ubergoal":
                body = (ROOT / skill / "SKILL.md").read_text()
                self.assertIn("Do not auto-trigger from task similarity", body, skill)

    def test_ubergoal_owns_platform_goal_by_default(self) -> None:
        body = (ROOT / "ubergoal" / "SKILL.md").read_text()
        meta = (ROOT / "ubergoal" / "agents" / "openai.yaml").read_text()
        evals = (ROOT / "ubergoal" / "evals" / "golden_skill_invocations.json").read_text()
        combined = "\n".join([body, meta, evals])

        self.assertIn("`ubergoal` is a superset of the platform goal primitive", body)
        self.assertIn("If no goal exists and the user explicitly invoked `ubergoal`, call `create_goal`", body)
        self.assertIn("create or bind a Codex/platform goal", meta)

        obsolete_phrases = [
            "Do not create a platform goal merely because this skill is active",
            "do not call create_goal unless",
            "do not create a platform goal without explicit launch instruction",
            "avoid subagents and goal launch",
        ]
        for phrase in obsolete_phrases:
            self.assertNotIn(phrase, combined)

    def test_ubergoal_tier2_requires_specialist_review_board(self) -> None:
        body = (ROOT / "ubergoal" / "SKILL.md").read_text()
        meta = (ROOT / "ubergoal" / "agents" / "openai.yaml").read_text()
        evals = (ROOT / "ubergoal" / "evals" / "golden_skill_invocations.json").read_text()

        self.assertIn("bounded review-board coordinator", body)
        self.assertIn("Tier 2 is valuable because it changes the decision shape", body)
        self.assertIn("launch 2-3 bounded review lanes", body)
        self.assertIn("Codebase/State Scout, Architecture/Contract Steward, and Quality/Eval/Hygiene Auditor", body)
        self.assertIn("specialist review-board agents", meta)
        self.assertIn("run specialist review-board agents or lenses for Tier 2+ work", evals)

    def test_utility_skills_have_task_specific_invocation_policy(self) -> None:
        text = (ROOT / "ubershow" / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", text)
        self.assertIn("browser-first visual artifact", text)
        body = (ROOT / "ubershow" / "SKILL.md").read_text()
        self.assertIn("Do **not** turn every answer into HTML", body)
        self.assertIn("HTML artifacts are generated **views**, not canonical truth", body)

    def test_root_agent_contract_declares_rca_authority(self) -> None:
        text = (ROOT / "AGENTS.md").read_text()
        self.assertIn("deep-rca` = general incident/root-cause authority", text)
        self.assertIn("Agent Advocate = agent-behavior-specific RCA lens", text)
        self.assertIn("use the `deep-rca` ladder for depth", text)

    def test_deep_rca_is_hardened_as_codex_utility_skill(self) -> None:
        self.assertFalse((ROOT / "deep-rca" / "README.md").exists())
        self.assertTrue((ROOT / "deep-rca" / "agents" / "openai.yaml").exists())
        self.assertTrue((ROOT / "deep-rca" / "evals" / "golden_skill_invocations.json").exists())
        self.assertTrue((ROOT / "deep-rca" / "scripts" / "lint_skill_package.py").exists())
        meta = (ROOT / "deep-rca" / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", meta)
        self.assertIn("$deep-rca", meta)

    def test_install_docs_include_full_pack(self) -> None:
        text = (ROOT / "README.md").read_text()
        loop = "for s in deep-rca skill-creator ubergoal uberplan uberaccept uberskillevolver ubersimplify uberassess ubershow; do"
        self.assertEqual(text.count(loop), 3)


if __name__ == "__main__":
    unittest.main()


class UberassessContractTests(unittest.TestCase):
    def test_uberassess_contract_declares_no_implementation_boundary(self) -> None:
        text = (ROOT / "uberassess" / "SKILL.md").read_text()
        self.assertIn("source-grounded recommendations", text)
        self.assertIn("It does not implement", text)
        self.assertIn("Implementation before approval: no", text)
        self.assertIn("benefit >> cost", text)
