import json
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals" / "uberaccept-v1"


class UberAcceptEvalBoundaryTests(unittest.TestCase):
    def test_suite_references_exist(self) -> None:
        suite = json.loads((EVAL / "suite.json").read_text())
        for key in ("working", "working_rubric", "holdouts", "holdout_rubric", "forward", "forward_rubric"):
            self.assertTrue((EVAL / suite[key]).is_file(), key)
        self.assertTrue((EVAL / suite["promotion_receipt"]).is_file())

    def test_inputs_have_unique_ids_and_fixtures(self) -> None:
        ids = []
        for name in ("inputs.json", "holdout-inputs.json", "forward-inputs.json"):
            for case in json.loads((EVAL / name).read_text()):
                ids.append(case["id"])
                fixture = EVAL / case["fixture"]
                self.assertTrue(fixture.is_dir(), case["id"])
                self.assertTrue((fixture / "APPROVED_PLAN.md").is_file(), case["id"])
                self.assertTrue((fixture / "EVIDENCE.md").is_file(), case["id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_rubric_ids_match_inputs(self) -> None:
        pairs = [
            ("inputs.json", "rubric.hidden.json"),
            ("holdout-inputs.json", "holdout-rubric.hidden.json"),
            ("forward-inputs.json", "forward-rubric.hidden.json"),
        ]
        for inputs_name, rubric_name in pairs:
            input_ids = {case["id"] for case in json.loads((EVAL / inputs_name).read_text())}
            rubric_ids = set(json.loads((EVAL / rubric_name).read_text())["hard_gates"])
            self.assertEqual(input_ids, rubric_ids)

    def test_current_promotion_receipt_is_hash_bound_and_complete(self) -> None:
        suite = json.loads((EVAL / "suite.json").read_text())
        receipt = json.loads((EVAL / suite["promotion_receipt"]).read_text())
        self.assertEqual(
            hashlib.sha256((ROOT / "uberaccept" / "SKILL.md").read_bytes()).hexdigest(),
            "".join(receipt["skill_sha256_chunks"]),
        )
        expected = {
            "working": "inputs.json",
            "holdout": "holdout-inputs.json",
            "forward": "forward-inputs.json",
        }
        self.assertEqual(set(expected), set(receipt["groups"]))
        for group, inputs_name in expected.items():
            inputs = json.loads((EVAL / inputs_name).read_text())
            self.assertEqual(
                [case["id"] for case in inputs],
                [case["id"] for case in receipt["groups"][group]],
            )
            self.assertTrue(all(case["verdict"] == "pass" for case in receipt["groups"][group]))


if __name__ == "__main__":
    unittest.main()
