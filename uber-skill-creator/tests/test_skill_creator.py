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
QUALITY = ROOT / "scripts" / "evaluate_skill_quality.py"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class SkillCreatorPackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_uber_skill_creator_declares_target_profiles_and_alias_boundary(self) -> None:
        body = (ROOT / "SKILL.md").read_text()
        meta = (ROOT / "agents" / "openai.yaml").read_text()
        combined = body + "\n" + meta

        self.assertIn("Choose the target profile first", body)
        self.assertIn("Portable Codex/Claude-compatible skill", body)
        self.assertIn("Uber-family skill", body)
        self.assertIn("OpenClaw/Gaia/Type0/Soho-specific skill", body)
        self.assertIn("openclaw-agentic-skill-creator", combined)
        self.assertIn("skill-creator-pro", combined)
        self.assertIn("deprecation shim", body)
        self.assertIn("Use `uberskillevolver` after substantial or surprising runs", body)
        self.assertIn("use uberskillevolver after real runs", meta)

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

    def test_quality_evaluator_flags_vague_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "vague-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                """---
name: vague-skill
description: Helpful skill.
---

# Vague Skill

Do things for the user.
"""
            )
            result = run_cmd(str(QUALITY), str(skill))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            data = json.loads(result.stdout)

        [record] = data["skills"]
        categories = set(record["issue_categories"])
        self.assertLess(record["score"], 75)
        self.assertIn("triggering", categories)
        self.assertIn("verification", categories)
        self.assertIn("eval_coverage", categories)

    def test_quality_evaluator_rewards_production_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "solid-skill"
            (skill / "scripts").mkdir(parents=True)
            (skill / "evals").mkdir()
            (skill / "agents").mkdir()
            (skill / "scripts" / "check.py").write_text("print('ok')\n")
            (skill / "evals" / "golden_skill_invocations.json").write_text("[]\n")
            (skill / "agents" / "openai.yaml").write_text("policy:\n  allow_implicit_invocation: true\n")
            (skill / "SKILL.md").write_text(
                """---
name: solid-skill
description: Use when Codex needs to evaluate a portable skill with read-only checks, proof requirements, and bounded recommendations.
---

# Solid Skill

Use `scripts/check.py` for deterministic validation and `evals/` for golden prompts.

Do not mutate the target skill during evaluation. Verify outputs with evidence before recommending changes.
"""
            )
            result = run_cmd(str(QUALITY), str(skill))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            data = json.loads(result.stdout)

        [record] = data["skills"]
        self.assertGreaterEqual(record["score"], 90)
        self.assertEqual(record["issue_count"], 0)

    def test_quality_evaluator_parses_folded_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "folded-skill"
            (skill / "agents").mkdir(parents=True)
            (skill / "agents" / "openai.yaml").write_text("policy:\n  allow_implicit_invocation: true\n")
            (skill / "SKILL.md").write_text(
                """---
name: folded-skill
description: >-
  Use when adding, modifying, reviewing, or debugging an agent-facing tool
  whose schema, side effects, source authority, errors, traces, or eval cases
  need to be clear enough for a coding agent to call safely.
---

# Folded Skill

Verify the tool contract with evidence and add eval cases for misuse, errors, and side effects.
Do not mutate live systems during review.
"""
            )
            result = run_cmd(str(QUALITY), str(skill))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            data = json.loads(result.stdout)

        [record] = data["skills"]
        self.assertGreaterEqual(record["description_chars"], 170)
        self.assertNotIn("triggering", set(record["issue_categories"]))

    def test_quality_evaluator_reports_pack_markdown_and_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ["alpha-skill", "beta-skill"]:
                skill = root / name
                skill.mkdir()
                (skill / "SKILL.md").write_text(
                    f"""---
name: {name}
description: Use when Codex needs a portable release review checklist with verification evidence and approval boundaries.
---

# {name}

Do not publish without approval. Verify with tests and evidence.
"""
                )
            result = run_cmd(str(QUALITY), str(root), "--format", "markdown")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

        self.assertIn("# Skill Quality Report", result.stdout)
        self.assertIn("Overlap candidates", result.stdout)


if __name__ == "__main__":
    unittest.main()
