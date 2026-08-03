from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestingStrategyContractTests(unittest.TestCase):
    def test_skill_keeps_the_compact_test_selection_contract(self) -> None:
        text = (ROOT / "SKILL.md").read_text()
        for phrase in [
            "inside or outside\n  `$ubergoal`",
            "not an Uber lifecycle phase",
            "Maturity, owner, targets",
            "test needed: yes/no",
            "one canonical test owner",
            "current checkout",
            "cleanly\n  installed artifact",
            "Table-drive values",
            "authorization, privilege/tenant isolation, source authority",
            "Run the first level that can falsify the changed contract",
            "skipped proof",
            "escalation trigger",
            "without reducing duplicate execution",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_adapter_exposes_the_automatic_utility(self) -> None:
        text = (ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn('display_name: "Testing Strategy"', text)
        self.assertIn("$testing-strategy", text)
        self.assertIn("allow_implicit_invocation: true", text)

    def test_data_only_fixture_covers_triggers_non_triggers_and_outputs(self) -> None:
        evals = ROOT / "evals"
        self.assertEqual(
            sorted(path.name for path in evals.iterdir() if path.is_file()),
            ["golden_skill_invocations.json"],
        )
        data = json.loads((evals / "golden_skill_invocations.json").read_text())
        self.assertEqual(data["schema_version"], 1)

        trigger_ids = {case["id"] for case in data["trigger_examples"]}
        non_trigger_ids = {case["id"] for case in data["non_trigger_examples"]}
        self.assertGreaterEqual(len(trigger_ids), 4)
        self.assertGreaterEqual(len(non_trigger_ids), 4)
        self.assertSetEqual(
            {
                "implementation_only_no_validation_decision",
                "rca_only_no_test_decision",
                "code_review_only_no_test_scope",
                "ordinary_validation_without_test_decision",
                "specified_test_command_only",
            },
            non_trigger_ids,
        )

        for case in data["trigger_examples"]:
            with self.subTest(trigger=case["id"]):
                self.assertTrue(case["should_trigger"])
                self.assertTrue(case["required_behavior"])
                self.assertTrue(case["forbidden_behavior"])
        for case in data["non_trigger_examples"]:
            with self.subTest(non_trigger=case["id"]):
                self.assertFalse(case["should_trigger"])
                self.assertTrue(case["required_behavior"])
                self.assertTrue(case["forbidden_behavior"])

        outputs = data["output_behavior_cases"]
        self.assertGreaterEqual(len(outputs), 4)
        for case in outputs:
            with self.subTest(output=case["id"]):
                self.assertTrue(case["scenario"])
                self.assertTrue(case["must_include"])
                self.assertTrue(case["must_not_include"])


if __name__ == "__main__":
    unittest.main()
