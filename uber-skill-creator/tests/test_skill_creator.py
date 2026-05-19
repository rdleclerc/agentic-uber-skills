from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINT = ROOT / "scripts" / "lint_skill_package.py"
REPORT = ROOT / "scripts" / "generate_eval_report.py"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class SkillCreatorPackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_eval_report_escapes_and_summarizes(self) -> None:
        payload = {
            "skill_name": "demo <skill>",
            "iteration": "iteration-1",
            "summary": "Summary & evidence",
            "cases": [
                {
                    "id": "eval-1",
                    "prompt": "Create <x>",
                    "expected": "Use structured output",
                    "with_skill": "pass",
                    "without_skill": "missed contract",
                    "verdict": "pass",
                    "notes": "Looks <safe>",
                },
                {
                    "id": "eval-2",
                    "prompt": "Near miss",
                    "expected": "Do not trigger",
                    "with_skill": "partial",
                    "without_skill": "partial",
                    "verdict": "partial",
                    "notes": "needs tuning",
                },
            ],
            "description_tuning": {
                "old": "old",
                "new": "new",
                "held_out_examples": ["trigger", "non-trigger"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "report.json"
            out = Path(tmp) / "report.html"
            src.write_text(json.dumps(payload))
            result = run_cmd(str(REPORT), str(src), str(out))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            html = out.read_text()

        self.assertIn("demo &lt;skill&gt; Eval Report", html)
        self.assertIn("pass: 1", html)
        self.assertIn("partial: 1", html)
        self.assertIn("Looks &lt;safe&gt;", html)
        self.assertNotIn("Create <x>", html)


if __name__ == "__main__":
    unittest.main()
