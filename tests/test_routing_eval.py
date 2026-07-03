from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "evals" / "routing" / "run_routing_eval.py"
PASS_FIXTURE = ROOT / "evals" / "routing" / "fixtures" / "sample_answers_pass.md"
FAIL_FIXTURE = ROOT / "evals" / "routing" / "fixtures" / "sample_answers_under_tier_fail.md"


class RoutingEvalTests(unittest.TestCase):
    def run_harness(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(HARNESS), *args], cwd=ROOT, text=True, capture_output=True)

    def test_packet_generation_is_fresh_agent_contract(self) -> None:
        proc = self.run_harness("--case-id", "R11")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("MUST-ESCALATE", proc.stdout)
        self.assertIn("Read ONLY `ubergoal/SKILL.md`", proc.stdout)
        self.assertIn("Do not implement", proc.stdout)
        self.assertIn("provider routing", proc.stdout)

    def test_grader_accepts_pass_fixture(self) -> None:
        proc = self.run_harness("--grade", str(PASS_FIXTURE))
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("SUMMARY passed=12 failed=0 total=12", proc.stdout)
        self.assertIn("PASS R11 MUST_ESCALATE", proc.stdout)
        self.assertIn("PASS R12 MUST_ESCALATE", proc.stdout)

    def test_grader_rejects_under_tier_fixture(self) -> None:
        proc = self.run_harness("--grade", str(FAIL_FIXTURE))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL R11 MUST_ESCALATE", proc.stdout)
        self.assertIn("FAIL R12 MUST_ESCALATE", proc.stdout)
        self.assertIn("tier expected='Tier 3' actual='Tier 1'", proc.stdout)


if __name__ == "__main__":
    unittest.main()
