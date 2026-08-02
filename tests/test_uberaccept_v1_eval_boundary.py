import json
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals" / "uberaccept-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def declared_sha256(value: str) -> str:
    prefix = "sha256:"
    if not value.startswith(prefix):
        raise AssertionError(f"digest is not content-addressed: {value}")
    return value[len(prefix) :]


class UberAcceptEvalBoundaryTests(unittest.TestCase):
    def test_suite_references_exist(self) -> None:
        suite = json.loads((EVAL / "suite.json").read_text())
        for key in ("working", "working_rubric", "holdouts", "holdout_rubric", "forward", "forward_rubric"):
            self.assertTrue((EVAL / suite[key]).is_file(), key)
        self.assertTrue((EVAL / suite["current_evaluation_status"]).is_file())
        self.assertTrue((EVAL / suite["historical_promotion_receipt"]).is_file())

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

    def test_current_candidate_is_not_promoted_and_historical_chain_is_consistent(self) -> None:
        suite = json.loads((EVAL / "suite.json").read_text())
        status = json.loads((EVAL / suite["current_evaluation_status"]).read_text())
        current = status["current_candidate"]
        historical = status["historical_evidence"]
        current_hash = sha256(ROOT / current["skill_path"])
        evaluated_hash = "".join(historical["promoted_skill_sha256_chunks"])

        self.assertEqual("fresh_eval_required", status["evaluation_state"])
        self.assertEqual("not_promoted", status["promotion_state"])
        self.assertFalse(current["fresh_eval_run"])
        self.assertFalse(current["promoted"])
        self.assertIn("proof for the current candidate", historical["legacy_filename_note"])
        self.assertEqual(
            current_hash,
            "".join(current["skill_sha256_chunks"]),
        )
        self.assertNotEqual(current_hash, evaluated_hash)
        required = status["required_fresh_eval"]
        self.assertEqual("gpt-5.6-sol", required["model"])
        self.assertEqual("ultra", required["reasoning_effort"])
        self.assertIn("generic cross-model", required["coverage_gap"])
        self.assertIn("explicit Claude-by-name", required["coverage_gap"])

        receipt_binding = historical["promotion_receipt"]
        receipt_path = EVAL / receipt_binding["path"]
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(evaluated_hash, "".join(receipt["skill_sha256_chunks"]))
        self.assertEqual(sha256(receipt_path), declared_sha256(receipt_binding["sha256"]))
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

        replay = historical["replay_binding"]
        self.assertEqual(evaluated_hash, "".join(replay["skill_sha256_chunks"]))
        artifact_paths = set()
        for artifact in replay["artifacts"]:
            path = EVAL / artifact["path"]
            artifact_paths.add(artifact["path"])
            self.assertEqual(sha256(path), declared_sha256(artifact["sha256"]), artifact["path"])
        self.assertIn("results/working-unknown-raw.md", artifact_paths)
        self.assertIn("results/holdout-forward-results.md", artifact_paths)

        comparison = historical["comparison_binding"]
        comparison_path = EVAL / comparison["path"]
        self.assertEqual(evaluated_hash, "".join(comparison["challenger_skill_sha256_chunks"]))
        self.assertEqual(sha256(comparison_path), declared_sha256(comparison["sha256"]))

        for correction in historical["rubric_corrections"]:
            correction_path = EVAL / correction["receipt"]
            correction_text = correction_path.read_text()
            original_hash = sha256(EVAL / correction["original_rubric"])
            corrected_hash = sha256(EVAL / correction["corrected_rubric"])
            self.assertEqual(original_hash, declared_sha256(correction["original_sha256"]))
            self.assertEqual(corrected_hash, declared_sha256(correction["corrected_sha256"]))
            for digest in (original_hash, corrected_hash):
                self.assertTrue(all(f"`{digest[index:index + 16]}`" in correction_text for index in range(0, 64, 16)))
            self.assertEqual(receipt["corrections"]["first_blind_receipt"], correction["first_blind_receipt"])
            self.assertIn(correction["receipt"], receipt["corrections"]["correction_receipts"])

        pack_binding = historical["pack_acceptance_binding"]
        pack_receipt = EVAL / pack_binding["path"]
        self.assertEqual(sha256(pack_receipt), declared_sha256(pack_binding["sha256"]))
        self.assertTrue(all(f"`{chunk}`" in pack_receipt.read_text() for chunk in historical["promoted_skill_sha256_chunks"]))


if __name__ == "__main__":
    unittest.main()
