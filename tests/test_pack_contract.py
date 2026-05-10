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

    def test_root_agent_contract_declares_rca_authority(self) -> None:
        text = (ROOT / "AGENTS.md").read_text()
        self.assertIn("deep-rca` = general incident/root-cause authority", text)
        self.assertIn("Agent Advocate = agent-behavior-specific RCA lens", text)
        self.assertIn("use the `deep-rca` ladder for depth", text)

    def test_install_docs_include_full_pack(self) -> None:
        text = (ROOT / "README.md").read_text()
        loop = "for s in deep-rca ubergoal uberplan uberaccept uberskillevolver ubersimplify uberassess; do"
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
