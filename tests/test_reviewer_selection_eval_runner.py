from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "evals" / "reviewer-selection" / "run_eval.py"
SPEC = importlib.util.spec_from_file_location("reviewer_selection_eval", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


SUBJECT_OUTPUTS = {
    "generic-cross-model": {
        "case_id": "generic-cross-model", "decision": "stop", "authorized_route": None,
        "selected_model": None, "selected_effort": None, "attempted_model_route": None,
        "invocation_attempted": False, "approval_or_stop": "stopped",
        "reason": "Generic cross-model wording names no route; stop rather than guess Claude.", "failures": [],
    },
    "required-sol-ultra-unavailable": {
        "case_id": "required-sol-ultra-unavailable", "decision": "stop", "authorized_route": None,
        "selected_model": None, "selected_effort": None, "attempted_model_route": None,
        "invocation_attempted": False, "approval_or_stop": "stopped",
        "reason": "The exact Sol Ultra binding is unavailable; no downgrade or Claude fallback.", "failures": [],
    },
    "explicit-claude-by-name": {
        "case_id": "explicit-claude-by-name", "decision": "authorize", "authorized_route": "claude",
        "selected_model": "claude", "selected_effort": None, "attempted_model_route": None,
        "invocation_attempted": False, "approval_or_stop": "authorized_not_invoked",
        "reason": "Rob explicitly named Claude; the route is authorized but not invoked.", "failures": [],
    },
    "gaia-adversarial-review": {
        "case_id": "gaia-adversarial-review", "decision": "select", "authorized_route": "gpt-5.6-sol",
        "selected_model": "gpt-5.6-sol", "selected_effort": "ultra", "attempted_model_route": None,
        "invocation_attempted": False, "approval_or_stop": "approved_not_invoked",
        "reason": "Gaia binds a fresh isolated gpt-5.6-sol reviewer at ultra; no Claude fallback.", "failures": [],
    },
}


def write_fake(path: Path, mode: str = "pass", repo: Path | None = None) -> Path:
    outputs = copy.deepcopy(SUBJECT_OUTPUTS)
    if mode == "generic_wrong":
        outputs["generic-cross-model"].update(
            decision="authorize", authorized_route="claude", selected_model="claude",
            approval_or_stop="authorized_not_invoked",
        )
    if mode == "bad_stop_token":
        outputs["generic-cross-model"]["approval_or_stop"] = "stop_pending_choice"
    if mode == "bad_stop_route":
        outputs["generic-cross-model"]["authorized_route"] = "gpt-5.6-sol at ultra only"
    if mode == "attempted_route":
        outputs["generic-cross-model"]["attempted_model_route"] = "gpt-5.6-sol"
    script = f"""#!/usr/bin/env python3
import json, os, pathlib, sys, time, uuid
MODE = {mode!r}
REPO = pathlib.Path({str(repo)!r}) if {repo is not None!r} else None
OUTPUTS = json.loads({json.dumps(outputs)!r})
prompt = sys.stdin.read()
payload = json.loads(prompt.split("INPUT_JSON=", 1)[1])
files = {{item["path"]: item["content"] for item in payload["files"]}}
phase = payload["phase"]
home = pathlib.Path(os.environ["CODEX_HOME"])
if any(item.name != "auth.json" for item in home.iterdir()) or (REPO and pathlib.Path.cwd().is_relative_to(REPO)):
    sys.exit(9)
if MODE == "timeout_write_repo":
    (REPO / "unexpected.txt").write_text("mutation")
if MODE in ("timeout", "timeout_write_repo"):
    time.sleep(2)
if MODE == "nonzero":
    sys.exit(7)
if MODE == "missing":
    sys.exit(0)
if MODE == "malformed_trace":
    print("not-json")
    sys.exit(0)
if MODE == "write_bundle":
    pathlib.Path("unexpected.txt").write_text("mutation")
if MODE == "write_repo":
    (REPO / "unexpected.txt").write_text("mutation")
if phase == "subject":
    case = json.loads(files["case.json"])
    output = OUTPUTS[case["case_id"]]
else:
    rubric = json.loads(files["rubric.json"])
    subject = json.loads(files["subject-output.json"])
    failures = [key for key, value in rubric["expected"].items() if subject.get(key) != value]
    output = {{"case_id": rubric["case_id"], "passed": not failures, "failures": failures, "evidence": ["field comparison"]}}
thread_id = "duplicate-runtime-id" if MODE == "duplicate_thread" else str(uuid.uuid4())
print(json.dumps({{"type": "thread.started", "thread_id": thread_id}}))
if MODE == "error_item":
    print(json.dumps({{"type": "item.completed", "item": {{"type": "error", "message": "synthetic process failure"}}}}))
if MODE == "tool":
    print(json.dumps({{"type": "item.started", "item": {{"type": "command_execution", "command": "forbidden"}}}}))
text = "not-json-output" if MODE == "malformed_output" else json.dumps(output)
print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": text}}}}))
print(json.dumps({{"type": "turn.completed", "usage": {{"input_tokens": 1, "output_tokens": 1}}}}))
"""
    path.write_text(script, encoding="utf-8")
    path.chmod(0o755)
    return path


class RunnerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        suite_source = ROOT / "evals" / "reviewer-selection"
        suite_target = self.repo / "evals" / "reviewer-selection"
        shutil.copytree(suite_source, suite_target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for relative in [
            "AGENTS.md", "ubergoal/SKILL.md", "uberaccept/SKILL.md", "uberplan/SKILL.md",
            "references/claude-adversary.md", "references/drift-fingerprints.toml",
        ]:
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.suite_path = suite_target / "suite.json"

    def fixed_snapshot(self) -> dict[str, str]:
        return RUNNER.tree_snapshot(self.repo, {".uberlearn-local", "results"})

    def trim_cases(self, *case_ids: str) -> None:
        suite = RUNNER.load_json(self.suite_path)
        suite["cases"] = [f"cases/{case_id}.json" for case_id in case_ids]
        suite["rubrics"] = {case_id: suite["rubrics"][case_id] for case_id in case_ids}
        RUNNER.write_json(self.suite_path, suite)

    def run_fake(self, mode: str = "pass") -> dict:
        fake = write_fake(self.root / f"fake-{mode}", mode, self.repo)
        return RUNNER.run_suite(
            self.repo, self.suite_path, str(fake), "gpt-5.6-sol", "ultra", test_runner=True,
        )


class StaticContractTests(RunnerTestCase):
    def test_base_status_and_four_targeted_cases_are_frozen(self) -> None:
        base = RUNNER.load_json(self.suite_path.parent / "base.json")
        suite = RUNNER.load_json(self.suite_path)
        status = RUNNER.load_json(self.suite_path.parent / suite["current_evaluation_status"])
        self.assertEqual("commit 4c5135c55cbddb6db775652eb835465ed2d95e0d", base["base_commit"])
        self.assertTrue(base["recorded_before_source_edits"])
        self.assertEqual(4, len(suite["cases"]))
        self.assertEqual({"uberaccept", "ubergoal", "uberplan"}, set(status["skills"]))
        for skill in status["skills"].values():
            self.assertEqual("fresh_eval_required", skill["evaluation_state"])
            self.assertEqual("not_promoted", skill["promotion_state"])

    def test_command_is_no_shell_ephemeral_sol_ultra_read_only(self) -> None:
        cmd = RUNNER.command("codex", "gpt-5.6-sol", "ultra", Path("/bundle"))
        self.assertEqual("codex", cmd[0])
        self.assertIn("--ephemeral", cmd)
        self.assertIn("--ignore-user-config", cmd)
        self.assertIn("--ignore-rules", cmd)
        self.assertIn("read-only", cmd)
        self.assertIn("gpt-5.6-sol", cmd)
        self.assertIn('model_reasoning_effort="ultra"', cmd)
        self.assertIn('web_search="disabled"', cmd)
        self.assertEqual(len(RUNNER.DISABLED_FEATURES), cmd.count("--disable"))
        self.assertIn("shell_tool", cmd)
        self.assertIn("unified_exec", cmd)
        self.assertIn("plugins", cmd)
        self.assertIn("skill_search", cmd)
        self.assertNotIn("sh", cmd)

    def test_subject_bundle_is_exact_allowlist_and_rubric_is_secret(self) -> None:
        case_path = self.suite_path.parent / "cases" / "generic-cross-model.json"
        bundle = self.root / "bundle"
        case, bindings = RUNNER.copy_subject_bundle(self.repo, case_path, bundle)
        prompt, prompt_bindings = RUNNER.inline_payload(bundle, "subject")
        expected = set(case["context_files"]) | {"case.json"}
        self.assertEqual(expected, set(RUNNER.tree_snapshot(bundle)))
        self.assertEqual(expected, {item["path"] for item in bindings})
        self.assertEqual(expected, {item["path"] for item in prompt_bindings})
        rubric = RUNNER.load_json(self.suite_path.parent / "rubrics" / "generic-cross-model.hidden.json")
        self.assertNotIn(rubric["secrecy_marker"], prompt)
        self.assertNotIn("reason_requirements", prompt)
        self.assertNotIn("explicit-claude-by-name", prompt)

    def test_committed_targeted_evidence_is_hash_bound_and_not_promoted(self) -> None:
        results = self.suite_path.parent / "results"
        summary = RUNNER.load_json(results / "targeted-evidence.json")
        claimed_manifest = summary.pop("manifest_hash")
        self.assertEqual(claimed_manifest, RUNNER.sha(RUNNER.packed(summary)))
        self.assertEqual({"subject": 4, "grader": 4}, summary["evidence_call_count"])
        self.assertEqual({"subject": 5, "grader": 4}, summary["total_call_count"])
        self.assertEqual("failed_closed", summary["case_results"]["explicit-claude-by-name"])
        self.assertEqual(0, summary["claude_invocation_count"])
        self.assertEqual({summary["runner_sha256_at_evidence"]}, {item["runner_sha256"] for item in summary["case_receipts"]})
        self.assertEqual({summary["harness_sha256_at_evidence"]}, {item["harness_sha256"] for item in summary["case_receipts"]})
        self.assertFalse((results / "last-failure.json").exists())
        runtime_ids = set()
        for receipt in summary["case_receipts"]:
            claimed = receipt.pop("receipt_hash")
            self.assertEqual(claimed, RUNNER.sha(RUNNER.packed(receipt)))
            self.assertEqual("fresh_eval_required", receipt["evaluation_state"])
            self.assertEqual("not_promoted", receipt["promotion_state"])
            for trace in receipt["process"].values():
                self.assertEqual(["agent_message"], trace["item_types"])
                self.assertEqual([], trace["tool_choices"])
                runtime_ids.add(trace["runtime_thread_id"])
        self.assertEqual(8, len(runtime_ids))
        explicit = next(item for item in summary["case_receipts"] if item["case_id"] == "explicit-claude-by-name")
        self.assertEqual("claude", explicit["process"]["subject"]["output"]["authorized_route"])
        self.assertFalse(explicit["process"]["subject"]["output"]["invocation_attempted"])


class SuccessfulRunTests(RunnerTestCase):
    def test_four_fresh_subject_and_grader_calls_bind_traces_and_cleanup(self) -> None:
        before = self.fixed_snapshot()
        first = self.run_fake()
        second = self.run_fake()
        self.assertNotEqual(first["run_id"], second["run_id"])
        self.assertEqual({"subject": 4, "grader": 4}, first["call_count"])
        self.assertEqual({"subject": 4, "grader": 4}, second["call_count"])
        self.assertEqual(before, self.fixed_snapshot())
        self.assertEqual(2, len(list((self.repo / ".uberlearn-local" / "reviewer-selection-v1").iterdir())))
        self.assertFalse(list((self.repo / ".uberlearn-local").rglob("case.json")))
        runtime_ids = set()
        expected_harness_sha256 = RUNNER.sha(RUNNER.HARNESS_PATH.read_bytes())
        for case_id in SUBJECT_OUTPUTS:
            receipt = RUNNER.load_json(self.suite_path.parent / "results" / f"{case_id}.receipt.json")
            claimed = receipt.pop("run_hash")
            self.assertEqual(claimed, RUNNER.sha(RUNNER.packed(receipt)))
            self.assertEqual(claimed, second["receipt_hashes"][case_id])
            self.assertEqual("fresh_eval_required", receipt["evaluation_state"])
            self.assertEqual("not_promoted", receipt["promotion_state"])
            self.assertEqual(expected_harness_sha256, receipt["harness_sha256"])
            self.assertEqual(expected_harness_sha256, first["harness_sha256"])
            self.assertEqual(receipt["harness_sha256"], first["harness_sha256"])
            for phase in ("subject", "grader"):
                trace = receipt["process"][phase]
                self.assertEqual(1, trace["schema_version"])
                self.assertEqual([], trace["tool_choices"])
                self.assertEqual([], trace["side_effects"])
                self.assertEqual([], trace["files_read"])
                self.assertTrue(trace["delivered_context_files"])
                self.assertTrue(trace["isolated_codex_home"])
                self.assertEqual("gpt-5.6-sol", trace["model"])
                self.assertEqual("ultra", trace["reasoning_effort"])
                runtime_ids.add(trace["runtime_thread_id"])
            tampered = copy.deepcopy(receipt)
            tampered["binding"]["model"] = "other"
            self.assertNotEqual(claimed, RUNNER.sha(RUNNER.packed(tampered)))
            tampered = copy.deepcopy(receipt)
            tampered["harness_sha256"] = "sha256:" + "0" * 64
            self.assertNotEqual(claimed, RUNNER.sha(RUNNER.packed(tampered)))
        self.assertEqual(8, len(runtime_ids))

    def test_raw_traces_are_local_and_gitignored(self) -> None:
        self.trim_cases("generic-cross-model")
        summary = self.run_fake()
        raw = self.repo / ".uberlearn-local" / "reviewer-selection-v1" / summary["run_id"]
        self.assertTrue((raw / "generic-cross-model" / "subject.stdout.jsonl").is_file())
        self.assertTrue((raw / "generic-cross-model" / "grader.stdout.jsonl").is_file())
        self.assertIn(".uberlearn-local/", (ROOT / ".gitignore").read_text())


class FailureTests(RunnerTestCase):
    def assert_failure(self, mode: str, phrase: str) -> None:
        self.trim_cases("generic-cross-model")
        suite = RUNNER.load_json(self.suite_path)
        if mode in {"timeout", "timeout_write_repo"}:
            suite["timeout_seconds"] = 1
            RUNNER.write_json(self.suite_path, suite)
        with self.assertRaises(RUNNER.EvalFailure):
            self.run_fake(mode)
        failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
        self.assertEqual("generic-cross-model", failure["case_id"])
        self.assertEqual("subject", failure["phase"])
        self.assertEqual("gpt-5.6-sol", failure["model"])
        self.assertEqual("ultra", failure["reasoning_effort"])
        self.assertIn(phrase, failure["reason"])
        self.assertEqual("failed_closed", failure["status"])
        self.assertFalse(list((self.repo / ".uberlearn-local").rglob("case.json")))

    def test_timeout_nonzero_missing_and_malformed_fail_closed(self) -> None:
        for mode, phrase in [
            ("timeout", "timeout after 1s"), ("nonzero", "nonzero exit 7"),
            ("missing", "missing trace"), ("malformed_trace", "malformed trace line"),
            ("malformed_output", "malformed final output"), ("tool", "tool execution attempted"),
            ("error_item", "process trace error"),
            ("bad_stop_token", "invalid decision or approval_or_stop"),
            ("bad_stop_route", "invalid route, model, or effort"),
            ("attempted_route", "model-route attempt is forbidden"),
            ("write_bundle", "unexpected write in disposable bundle"),
            ("write_repo", "unexpected repository write"),
            ("timeout_write_repo", "unexpected repository write"),
        ]:
            with self.subTest(mode=mode):
                with self.setUpSubTestRepo():
                    self.assert_failure(mode, phrase)

    def test_duplicate_runtime_context_fails_closed(self) -> None:
        self.trim_cases("generic-cross-model")
        with self.assertRaises(RUNNER.EvalFailure):
            self.run_fake("duplicate_thread")
        failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
        self.assertEqual("grader", failure["phase"])
        self.assertIn("runtime context id was reused", failure["reason"])

    def test_failed_rerun_removes_all_prior_success_artifacts(self) -> None:
        self.run_fake()
        with self.assertRaises(RUNNER.EvalFailure):
            self.run_fake("generic_wrong")
        results = self.suite_path.parent / "results"
        self.assertFalse((results / "targeted-run.json").exists())
        self.assertFalse([path for path in results.glob("*.receipt.json")])

    def setUpSubTestRepo(self):
        outer = self

        class Reset:
            def __enter__(self):
                outer.setUp()
                return self

            def __exit__(self, *_args):
                outer.temp.cleanup()

        return Reset()

    def test_model_or_effort_mismatch_has_exact_preflight_receipt(self) -> None:
        self.run_fake()
        with self.assertRaises(RUNNER.EvalFailure):
            RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "xhigh")
        results = self.suite_path.parent / "results"
        failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
        self.assertEqual("preflight", failure["case_id"])
        self.assertEqual("preflight", failure["phase"])
        self.assertIn("model binding mismatch", failure["reason"])
        self.assertEqual({"subject": 0, "grader": 0}, failure["call_count"])
        self.assertFalse((results / "targeted-run.json").exists())
        self.assertFalse(list(results.glob("*.receipt.json")))

    def test_malformed_suite_performs_no_output_writes(self) -> None:
        self.run_fake()
        results = self.suite_path.parent / "results"
        prior_summary = (results / "targeted-run.json").read_bytes()
        self.suite_path.write_text("{", encoding="utf-8")
        with self.assertRaises(ValueError):
            RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "ultra", test_runner=True)
        self.assertEqual(prior_summary, (results / "targeted-run.json").read_bytes())
        self.assertFalse((results / "last-failure.json").exists())

    def test_fixed_output_path_drift_cannot_touch_victim_or_results(self) -> None:
        suite = RUNNER.load_json(self.suite_path)
        victim = self.repo / "unrelated-receipts"
        victim.mkdir()
        marker = victim / "targeted-run.json"
        marker.write_text("keep", encoding="utf-8")
        canonical_results = self.suite_path.parent / "results"
        before = RUNNER.tree_snapshot(canonical_results)
        for field, value in (
            ("result_dir", "unrelated-receipts"),
            ("raw_artifact_root", "evals/reviewer-selection/raw-not-ignored"),
        ):
            with self.subTest(field=field):
                candidate = dict(suite)
                candidate[field] = value
                RUNNER.write_json(self.suite_path, candidate)
                with self.assertRaises(RUNNER.EvalFailure):
                    RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "ultra", test_runner=True)
                self.assertEqual("keep", marker.read_text(encoding="utf-8"))
                self.assertEqual(before, RUNNER.tree_snapshot(canonical_results))
        RUNNER.write_json(self.suite_path, suite)

    def test_canonical_mode_accepts_current_manifest_with_fake_codex(self) -> None:
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        fake = write_fake(bin_dir / "codex", "pass", self.repo)
        with mock.patch.dict(os.environ, {"PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", "")}):
            summary = RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "ultra")
        self.assertEqual(RUNNER.EXPECTED_INPUT_MANIFEST_SHA256, summary["input_manifest_sha256"])
        self.assertEqual(RUNNER.sha(fake.read_bytes()), summary["runner_sha256"])
        self.assertEqual(RUNNER.sha(RUNNER.HARNESS_PATH.read_bytes()), summary["harness_sha256"])

    def test_canonical_mode_rejects_each_of_five_policy_input_drifts_before_calls(self) -> None:
        self.assertEqual(5, len(RUNNER.EXPECTED_POLICY_INPUT_PATHS))
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        marker = self.root / "codex-invoked"
        fake = bin_dir / "codex"
        fake.write_text(f"#!/bin/sh\nprintf invoked > {marker}\nexit 99\n", encoding="utf-8")
        fake.chmod(0o755)
        env = {"PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", "")}
        for relative in sorted(RUNNER.EXPECTED_POLICY_INPUT_PATHS):
            with self.subTest(relative=relative):
                path = self.repo / relative
                original = path.read_bytes()
                path.write_bytes(original + b"\n")
                try:
                    with mock.patch.dict(os.environ, env):
                        with self.assertRaises(RUNNER.EvalFailure):
                            RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "ultra")
                    self.assertFalse(marker.exists())
                    failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
                    self.assertIn("case, rubric, or context manifest digest mismatch", failure["reason"])
                    self.assertEqual({"subject": 0, "grader": 0}, failure["call_count"])
                finally:
                    path.write_bytes(original)

    def test_canonical_mode_rejects_suite_digest_or_case_set_drift(self) -> None:
        suite = RUNNER.load_json(self.suite_path)
        suite["cases"] = suite["cases"][:1]
        suite["rubrics"] = {"generic-cross-model": suite["rubrics"]["generic-cross-model"]}
        RUNNER.write_json(self.suite_path, suite)
        with self.assertRaises(RUNNER.EvalFailure):
            RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "ultra")
        failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
        self.assertIn("suite or base manifest digest mismatch", failure["reason"])

    def test_canonical_mode_rejects_referenced_input_drift(self) -> None:
        case_path = self.suite_path.parent / "cases" / "generic-cross-model.json"
        case = RUNNER.load_json(case_path)
        case["operator_prompt"] += " tampered"
        RUNNER.write_json(case_path, case)
        with self.assertRaises(RUNNER.EvalFailure):
            RUNNER.run_suite(self.repo, self.suite_path, "codex", "gpt-5.6-sol", "ultra")
        failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
        self.assertIn("case, rubric, or context manifest digest mismatch", failure["reason"])

    def test_success_receipt_marks_fake_runner_and_binds_executable(self) -> None:
        self.trim_cases("generic-cross-model")
        fake = write_fake(self.root / "fake-pass", "pass", self.repo)
        summary = RUNNER.run_suite(self.repo, self.suite_path, str(fake), "gpt-5.6-sol", "ultra", test_runner=True)
        receipt = RUNNER.load_json(self.suite_path.parent / "results" / "generic-cross-model.receipt.json")
        self.assertEqual("test_runner", receipt["runner_mode"])
        self.assertEqual(RUNNER.sha(fake.read_bytes()), receipt["runner_sha256"])
        self.assertEqual(RUNNER.sha(RUNNER.HARNESS_PATH.read_bytes()), receipt["harness_sha256"])
        self.assertEqual("test_runner", summary["runner_mode"])


class BlackBoxRoutingTests(RunnerTestCase):
    def run_cli(self, fake: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(RUNNER_PATH), "--repo", str(self.repo), "--suite", str(self.suite_path),
             "--codex-bin", str(fake), "--allow-test-runner"],
            text=True, capture_output=True, env=env, timeout=20,
        )

    def claude_sentinel(self) -> tuple[dict[str, str], Path]:
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        marker = self.root / "claude-launched"
        claude = bin_dir / "claude"
        claude.write_text(f"#!/bin/sh\nprintf launched > {marker}\n", encoding="utf-8")
        claude.chmod(0o755)
        env = {**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", "")}
        return env, marker

    def test_generic_cross_model_cannot_pass_as_claude_route(self) -> None:
        self.trim_cases("generic-cross-model")
        fake = write_fake(self.root / "fake-wrong", "generic_wrong", self.repo)
        env, marker = self.claude_sentinel()
        proc = self.run_cli(fake, env)
        self.assertNotEqual(0, proc.returncode, proc.stdout)
        self.assertFalse(marker.exists())
        failure = RUNNER.load_json(self.suite_path.parent / "results" / "last-failure.json")
        self.assertEqual("subject", failure["phase"])
        self.assertEqual({"subject": 1, "grader": 0}, failure["call_count"])

    def test_explicit_claude_name_authorizes_without_launch(self) -> None:
        self.trim_cases("explicit-claude-by-name")
        fake = write_fake(self.root / "fake-pass", "pass", self.repo)
        env, marker = self.claude_sentinel()
        proc = self.run_cli(fake, env)
        self.assertEqual(0, proc.returncode, proc.stderr + proc.stdout)
        self.assertFalse(marker.exists())
        summary = json.loads(proc.stdout)
        self.assertEqual({"subject": 1, "grader": 1}, summary["call_count"])
        raw = self.repo / ".uberlearn-local" / "reviewer-selection-v1" / summary["run_id"]
        trace = (raw / "explicit-claude-by-name" / "subject.stdout.jsonl").read_text()
        self.assertIn('\\"authorized_route\\": \\"claude\\"', trace)


if __name__ == "__main__":
    unittest.main()
