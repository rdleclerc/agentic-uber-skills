import json
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "evals" / "uberplan-v3" / "working-inputs.json"
RUBRIC = ROOT / "evals" / "uberplan-v3" / "working-rubric.hidden.json"
HOLDOUT_INPUTS = ROOT / "evals" / "uberplan-v3" / "holdout-inputs.json"
HOLDOUT_RUBRIC = ROOT / "evals" / "uberplan-v3" / "holdout-rubric.hidden.json"
FORWARD_INPUTS = ROOT / "evals" / "uberplan-v3" / "forward-inputs.json"
FORWARD_RUBRIC = ROOT / "evals" / "uberplan-v3" / "forward-rubric.hidden.json"
TRANSFER_INPUTS = ROOT / "evals" / "uberplan-v3" / "transfer-inputs.json"
TRANSFER_RUBRIC = ROOT / "evals" / "uberplan-v3" / "transfer-rubric.hidden.json"
SUITE_MANIFEST = ROOT / "evals" / "uberplan-v3" / "suite.json"
BASELINES = ROOT / "evals" / "uberplan-v3" / "baselines"

GRADER_ONLY_KEYS = {
    "expected",
    "expected_decision",
    "causal_requirements",
    "protection_requirements",
    "handoff_requirements",
    "scope_requirements",
    "source_requirements",
    "forbidden_shortcuts",
    "size_target_words",
    "promotion_gate",
    "rubric",
    "shallow_failure",
}


def all_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from all_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_keys(child)


class UberplanV3EvalBoundaryTest(unittest.TestCase):
    def test_agent_inputs_do_not_contain_grader_fields(self):
        for path in (INPUTS, HOLDOUT_INPUTS, FORWARD_INPUTS, TRANSFER_INPUTS):
            inputs = json.loads(path.read_text())
            leaked = GRADER_ONLY_KEYS.intersection(all_keys(inputs))
            self.assertEqual(set(), leaked, path.name)

    def test_working_cases_and_hidden_rubric_match(self):
        inputs = json.loads(INPUTS.read_text())
        rubric = json.loads(RUBRIC.read_text())
        input_ids = [case["id"] for case in inputs["cases"]]
        rubric_ids = [case["id"] for case in rubric["cases"]]
        self.assertEqual(4, len(input_ids))
        self.assertEqual(input_ids, rubric_ids)
        self.assertEqual(len(input_ids), len(set(input_ids)))

    def test_agent_workspaces_exist_and_hide_grader_data(self):
        for input_path in (INPUTS, HOLDOUT_INPUTS, FORWARD_INPUTS, TRANSFER_INPUTS):
            inputs = json.loads(input_path.read_text())
            for case in inputs["cases"]:
                workspace = ROOT / case["workspace"]
                self.assertTrue(workspace.is_dir(), case["id"])
                hidden = [
                    path
                    for path in workspace.rglob("*")
                    if path.is_file()
                    and any(token in path.name.lower() for token in ("rubric", "answer", "expected"))
                ]
                self.assertEqual([], hidden, case["id"])

    def test_holdout_cases_and_hidden_rubric_match(self):
        inputs = json.loads(HOLDOUT_INPUTS.read_text())
        rubric = json.loads(HOLDOUT_RUBRIC.read_text())
        input_ids = [case["id"] for case in inputs["cases"]]
        rubric_ids = [case["id"] for case in rubric["cases"]]
        self.assertEqual(2, len(input_ids))
        self.assertEqual(input_ids, rubric_ids)
        self.assertEqual(len(input_ids), len(set(input_ids)))

    def test_forward_cases_and_hidden_rubric_match(self):
        inputs = json.loads(FORWARD_INPUTS.read_text())
        rubric = json.loads(FORWARD_RUBRIC.read_text())
        input_ids = [case["id"] for case in inputs["cases"]]
        rubric_ids = [case["id"] for case in rubric["cases"]]
        self.assertEqual(3, len(input_ids))
        self.assertEqual(input_ids, rubric_ids)
        self.assertEqual(len(input_ids), len(set(input_ids)))

    def test_transfer_case_and_hidden_rubric_match(self):
        inputs = json.loads(TRANSFER_INPUTS.read_text())
        rubric = json.loads(TRANSFER_RUBRIC.read_text())
        manifest = json.loads(SUITE_MANIFEST.read_text())
        input_ids = [case["id"] for case in inputs["cases"]]
        rubric_ids = [case["id"] for case in rubric["cases"]]
        self.assertEqual(1, len(input_ids))
        self.assertEqual(input_ids, rubric_ids)
        transfer_group = next(
            group for group in manifest["groups"] if group["id"] == "transfer"
        )
        self.assertEqual(
            ["execution_handoff_integrity"],
            transfer_group["additional_hard_gates"],
        )

    def test_suite_manifest_resolves_every_group(self):
        manifest = json.loads(SUITE_MANIFEST.read_text())
        self.assertEqual("uberplan-behavioral-conformance-v1", manifest["suite_id"])
        expected = {
            "working": (INPUTS, RUBRIC),
            "holdout": (HOLDOUT_INPUTS, HOLDOUT_RUBRIC),
            "forward": (FORWARD_INPUTS, FORWARD_RUBRIC),
            "transfer": (TRANSFER_INPUTS, TRANSFER_RUBRIC),
        }
        seen_case_ids = set()
        for group in manifest["groups"]:
            input_path, rubric_path = expected[group["id"]]
            self.assertEqual(input_path.name, group["inputs"])
            self.assertEqual(rubric_path.name, group["rubric"])
            inputs = json.loads(input_path.read_text())
            self.assertEqual(group["case_count"], len(inputs["cases"]))
            for case in inputs["cases"]:
                self.assertNotIn(case["id"], seen_case_ids)
                seen_case_ids.add(case["id"])
        self.assertEqual(set(expected), {group["id"] for group in manifest["groups"]})
        subject_bundle = manifest["subject_bundle"]
        self.assertIn("uberplan/SKILL.md", subject_bundle["include"])
        self.assertIn("<selected_case_workspace>/**", subject_bundle["include"])
        self.assertFalse(
            any(
                "rubric" in item or "*-inputs.json" in item
                for item in subject_bundle["include"]
            )
        )
        self.assertTrue(any("rubric" in item for item in subject_bundle["exclude"]))
        self.assertIn("uberplan/evals/**", subject_bundle["exclude"])

    def test_sanitized_baselines_reference_valid_suite_groups(self):
        baseline_paths = sorted(BASELINES.glob("*.json"))
        self.assertTrue(baseline_paths)
        manifest = json.loads(SUITE_MANIFEST.read_text())
        groups_by_id = {group["id"]: group for group in manifest["groups"]}
        for path in baseline_paths:
            baseline = json.loads(path.read_text())
            self.assertEqual(
                "uberplan-behavioral-conformance-v1", baseline["suite_id"], path.name
            )
            self.assertEqual("historical_composite", baseline["receipt_kind"])
            for chunks in baseline["skill_revisions"].values():
                self.assertEqual(4, len(chunks))
                self.assertTrue(all(len(chunk) == 16 for chunk in chunks))
            metric_names = set(manifest["diagnostic_metrics"])
            self.assertTrue(baseline["results"])
            self.assertEqual(
                set(baseline["coverage_scope"]),
                set(baseline["results"]),
                path.name,
            )
            self.assertLessEqual(
                set(baseline["coverage_scope"]), set(groups_by_id), path.name
            )
            for group_id, result in baseline["results"].items():
                group = groups_by_id[group_id]
                inputs = json.loads(
                    (SUITE_MANIFEST.parent / group["inputs"]).read_text()
                )
                self.assertEqual(
                    [case["id"] for case in inputs["cases"]],
                    [case["id"] for case in result["cases"]],
                )
                for case in result["cases"]:
                    self.assertEqual("pass", case["candidate_substantive_verdict"])
                    self.assertEqual(
                        metric_names,
                        set(case["candidate"]),
                        (path.name, group_id, case["id"]),
                    )
                    self.assertTrue(
                        all(value > 0 for value in case["candidate"].values())
                    )
            self.assertEqual(
                "APPROVE_CANDIDATE",
                baseline["independent_review"]["verdict"],
                path.name,
            )

    def test_current_promotion_receipt_covers_every_group(self):
        manifest = json.loads(SUITE_MANIFEST.read_text())
        self.assertIn(
            "results/current-promotion.json", manifest["promotion_receipts"]
        )
        receipt = json.loads(
            (SUITE_MANIFEST.parent / "results" / "current-promotion.json").read_text()
        )
        self.assertEqual(
            hashlib.sha256((ROOT / "uberplan" / "SKILL.md").read_bytes()).hexdigest(),
            "".join(receipt["skill_sha256_chunks"]),
        )
        raw = receipt["raw_trace_receipt"]
        self.assertFalse(raw["committed"])
        self.assertEqual("rerun_committed_suite", raw["portable_reproduction"])
        self.assertEqual(
            ["working", "holdout", "forward", "transfer"], raw["coverage"]
        )
        self.assertEqual(
            {"working", "holdout_forward", "transfer"},
            set(raw["artifact_sha256_chunks"]),
        )
        self.assertTrue(
            all(
                len(chunks) == 4 and all(len(chunk) == 16 for chunk in chunks)
                for chunks in raw["artifact_sha256_chunks"].values()
            )
        )
        groups = {group["id"]: group for group in manifest["groups"]}
        self.assertEqual(set(groups), set(receipt["groups"]))
        for group_id, group in groups.items():
            inputs = json.loads(
                (SUITE_MANIFEST.parent / group["inputs"]).read_text()
            )
            self.assertEqual(
                [case["id"] for case in inputs["cases"]],
                [case["id"] for case in receipt["groups"][group_id]],
            )
            self.assertTrue(
                all(
                    case["verdict"] == "pass"
                    for case in receipt["groups"][group_id]
                )
            )


if __name__ == "__main__":
    unittest.main()
