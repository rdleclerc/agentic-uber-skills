import json
import hashlib
import re
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def declared_sha256(value: str) -> str:
    prefix = "sha256:"
    if not value.startswith(prefix):
        raise AssertionError(f"digest is not content-addressed: {value}")
    return value[len(prefix) :]


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

    def test_current_candidate_is_not_promoted_and_historical_chain_is_consistent(self):
        manifest = json.loads(SUITE_MANIFEST.read_text())
        self.assertEqual("results/current-eval-status.json", manifest["current_evaluation_status"])
        self.assertIn("results/current-promotion.json", manifest["historical_promotion_receipts"])
        self.assertIn("results/transfer-selected.md", manifest["historical_promotion_receipts"])
        status = json.loads((SUITE_MANIFEST.parent / manifest["current_evaluation_status"]).read_text())
        current = status["current_candidate"]
        historical = status["historical_evidence"]
        required = status["required_fresh_eval"]
        current_hash = sha256(ROOT / current["skill_path"])
        evaluated_hash = "".join(historical["promoted_skill_sha256_chunks"])

        self.assertEqual("fresh_eval_required", status["evaluation_state"])
        self.assertEqual("not_promoted", status["promotion_state"])
        self.assertFalse(current["fresh_eval_run"])
        self.assertFalse(current["promoted"])
        self.assertIn("proof for the current candidate", historical["legacy_filename_note"])
        self.assertEqual(current_hash, "".join(current["skill_sha256_chunks"]))
        self.assertNotEqual(current_hash, evaluated_hash)
        self.assertEqual("gpt-5.6-sol", required["model"])
        self.assertEqual("ultra", required["reasoning_effort"])
        self.assertIn("generic cross-model", required["coverage_gap"])
        self.assertIn("explicit Claude-by-name", required["coverage_gap"])
        self.assertIn("3 completed calls", historical["historical_metric_gap"])
        self.assertIn("13 total calls", historical["historical_metric_gap"])

        promotion_binding = historical["promotion_receipt"]
        promotion_path = SUITE_MANIFEST.parent / promotion_binding["path"]
        receipt = json.loads(
            promotion_path.read_text()
        )
        self.assertEqual(sha256(promotion_path), declared_sha256(promotion_binding["sha256"]))
        self.assertEqual(evaluated_hash, "".join(receipt["skill_sha256_chunks"]))
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

        replay = historical["replay_binding"]
        replay_path = SUITE_MANIFEST.parent / replay["path"]
        replay_text = replay_path.read_text()
        self.assertEqual(sha256(replay_path), declared_sha256(replay["sha256"]))
        self.assertEqual(evaluated_hash, "".join(replay["skill_sha256_chunks"]))
        self.assertIn(f"`{evaluated_hash}`", replay_text)
        receipt_artifacts = {
            name: "".join(chunks)
            for name, chunks in raw["artifact_sha256_chunks"].items()
        }
        replay_artifacts = {
            name: declared_sha256(value)
            for name, value in replay["raw_artifact_sha256"].items()
        }
        self.assertEqual(receipt_artifacts, replay_artifacts)
        self.assertTrue(all(f"`{digest}`" in replay_text for digest in replay_artifacts.values()))

        local_raw = ROOT / ".uberlearn-local" / "uberplan-v3" / "2026-07-26"
        local_names = {
            "working": "working.md",
            "holdout_forward": "holdout-forward.md",
            "transfer": "transfer.md",
        }
        if local_raw.exists():
            self.assertEqual(sha256(local_raw / "manifest.md"), sha256(replay_path))
            for group, filename in local_names.items():
                self.assertEqual(replay_artifacts[group], sha256(local_raw / filename), group)

        comparison = historical["comparison_binding"]
        comparison_path = SUITE_MANIFEST.parent / comparison["path"]
        comparison_text = comparison_path.read_text()
        self.assertEqual(sha256(comparison_path), declared_sha256(comparison["sha256"]))
        self.assertEqual(evaluated_hash, "".join(comparison["challenger_skill_sha256_chunks"]))
        self.assertEqual(evaluated_hash, "".join(re.findall(r"`([0-9a-f]{16})`", comparison_text)[:4]))

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

        transfer = receipt["groups"]["transfer"][0]
        self.assertEqual("execution_lifecycle_handoff", transfer["id"])
        self.assertEqual(720, transfer["output_words_estimate"])
        self.assertEqual(3, transfer["completed_tool_calls"])
        self.assertEqual("UNKNOWN", transfer["total_tokens"])
        self.assertIn("Case: `execution_lifecycle_handoff`", comparison_text)
        self.assertIn("Output words: approximately 720", comparison_text)
        self.assertIn("Completed tool calls: 3", comparison_text)
        self.assertIn("Total tokens: `UNKNOWN`", comparison_text)
        self.assertIn("Mutation: none", comparison_text)

        pack_binding = historical["pack_acceptance_binding"]
        pack_receipt = SUITE_MANIFEST.parent / pack_binding["path"]
        self.assertEqual(sha256(pack_receipt), declared_sha256(pack_binding["sha256"]))
        self.assertTrue(all(f"`{chunk}`" in pack_receipt.read_text() for chunk in historical["promoted_skill_sha256_chunks"]))


if __name__ == "__main__":
    unittest.main()
