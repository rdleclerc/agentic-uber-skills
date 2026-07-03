from __future__ import annotations

import subprocess
import sys
import unittest
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_failure_case.py"
FIXTURES = ROOT / "tests" / "fixtures" / "failure_cases"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)], cwd=ROOT, text=True, capture_output=True)


def run_validator_args(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), *args], cwd=ROOT, text=True, capture_output=True)


class FailureCaseValidatorTests(unittest.TestCase):
    def test_pack_process_cases_validate(self) -> None:
        result = run_validator(ROOT / "evals" / "failures" / "cases")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("validated 15 failure case", result.stdout)

    def test_pack_failure_index_matches_local_cases(self) -> None:
        result = run_validator_args(
            "--index",
            str(ROOT / "evals" / "failures" / "INDEX.md"),
            "--cases",
            str(ROOT / "evals" / "failures" / "cases"),
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("matches cases", result.stdout)

    def test_valid_pointer_fixture_validates(self) -> None:
        result = run_validator(FIXTURES / "valid" / "runtime-pointer.md")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_missing_required_field_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "missing-required.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required field: eval_check", result.stderr)

    def test_invalid_enum_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "invalid-enum.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid eval_type", result.stderr)

    def test_unsanitized_user_path_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "unsanitized-user-path.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsanitized user path", result.stderr)

    def test_nonexistent_target_fails_cleanly(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "does-not-exist.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: failure case validation failed", result.stderr)
        self.assertIn("cannot read case file", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_unsanitized_title_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "unsanitized-title.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("title contains unsanitized user path", result.stderr)

    def test_unsanitized_cost_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "unsanitized-cost.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cost contains unsanitized user path", result.stderr)

    def test_unsanitized_body_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "unsanitized-body.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("body contains unsanitized user path", result.stderr)

    def test_machine_path_elsewhere_on_parameterized_line_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "parameterized-default-plus-user-path.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("/Users/other/secret", result.stderr)

    def test_pointer_without_canonical_repo_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "pointer-missing-canonical-repo.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pointer file must name canonical repo path", result.stderr)

    def test_index_id_mismatch_fails(self) -> None:
        base = FIXTURES / "index" / "id_mismatch"
        result = run_validator_args("--index", str(base / "INDEX.md"), "--cases", str(base / "cases"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("case file missing from local index", result.stderr)
        self.assertIn("local index id has no case file", result.stderr)

    def test_index_status_mismatch_fails(self) -> None:
        base = FIXTURES / "index" / "status_mismatch"
        result = run_validator_args("--index", str(base / "INDEX.md"), "--cases", str(base / "cases"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("status mismatch", result.stderr)

    def test_gaia_dialect_index_fixture_passes(self) -> None:
        base = FIXTURES / "index" / "gaia_dialect"
        result = run_validator_args("--index", str(base / "INDEX.md"), "--cases", str(base / "cases"))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("matches cases", result.stdout)

    def test_cross_index_detects_shared_status_drift(self) -> None:
        base = FIXTURES / "index" / "cross_index_drift"
        result = run_validator_args("--index", str(base / "left_INDEX.md"), "--cross-index", str(base / "right_INDEX.md"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shared-id status mismatch", result.stderr)

    def test_cross_index_matches_gaia_checkout_when_present(self) -> None:
        gaia_root = Path(os.environ.get("GAIA_ROOT", str(Path.home() / "repos" / "agfunder-gaia"))).expanduser()
        gaia_index = gaia_root / "evals" / "failures" / "INDEX.md"
        if not gaia_index.exists():
            self.skipTest(f"LOUD SKIP: Gaia checkout absent at {gaia_root}; cross-index live check not run")
        result = run_validator_args("--index", str(ROOT / "evals" / "failures" / "INDEX.md"), "--cross-index", str(gaia_index))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
