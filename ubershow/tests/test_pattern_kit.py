from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES = [
    "decision-board.html",
    "implementation-plan.html",
    "code-review-map.html",
    "architecture-map.html",
    "status-timeline.html",
    "questionnaire.html",
    "visual-brief.html",
]


class UbershowPatternKitTests(unittest.TestCase):
    def test_lint_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/lint_skill_package.py", str(SKILL_DIR)],
            cwd=SKILL_DIR,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_required_templates_exist_and_are_self_contained(self) -> None:
        for name in TEMPLATES:
            path = SKILL_DIR / "templates" / name
            text = path.read_text()
            lower = text.lower()
            with self.subTest(template=name):
                self.assertIn("<!doctype html>", lower)
                self.assertIn("data-artifact-kind=", text)
                self.assertIn("data-ubershow-template=", text)
                self.assertIn("<main", lower)
                self.assertIn("<section", lower)
                self.assertIn("<button", lower)
                self.assertIn("decision-receipt", text)
                self.assertIn("copyDecisionReceipt", text)
                self.assertIn("navigator.clipboard.writeText", text)
                self.assertNotIn("<script src=", lower)
                self.assertNotIn("<link ", lower)
                self.assertNotIn("http://", lower)
                self.assertNotIn("https://", lower)

    def test_templates_explain_receipt_registration(self) -> None:
        decision_board = (SKILL_DIR / "templates" / "decision-board.html").read_text()
        self.assertIn("That paste is the registration event.", decision_board)
        self.assertIn("HTML is only the generated view", decision_board)

    def test_decision_board_schema_is_minimal_and_valid(self) -> None:
        schema = json.loads((SKILL_DIR / "schemas" / "decision-board.schema.json").read_text())
        self.assertEqual(schema["title"], "Ubershow Decision Board Input")
        required = set(schema["required"])
        self.assertLessEqual({"artifact_id", "title", "recommendation", "options", "sources", "open_questions"}, required)
        option_props = schema["properties"]["options"]["items"]["properties"]
        self.assertLessEqual({"id", "label", "summary", "pros", "cons", "risk", "reversibility"}, set(option_props))

    def test_skill_mentions_browser_first_and_source_authority(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text()
        self.assertIn("browser-first", text)
        self.assertIn("HTML clicks do not automatically register with the agent", text)
        self.assertIn("copyable decision receipt", text)
        self.assertIn("HTML artifacts are generated **views**, not canonical truth", text)
        self.assertIn("Obsidian/Soho House is optional archive context only", text)


if __name__ == "__main__":
    unittest.main()
