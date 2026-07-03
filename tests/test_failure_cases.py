from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_failure_case.py"
FIXTURES = ROOT / "tests" / "fixtures" / "failure_cases"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)], cwd=ROOT, text=True, capture_output=True)


class FailureCaseValidatorTests(unittest.TestCase):
    def test_pack_process_cases_validate(self) -> None:
        result = run_validator(ROOT / "evals" / "failures" / "cases")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("validated 12 failure case", result.stdout)

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

    def test_pointer_without_canonical_repo_fails(self) -> None:
        result = run_validator(FIXTURES / "invalid" / "pointer-missing-canonical-repo.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pointer file must name canonical repo path", result.stderr)


if __name__ == "__main__":
    unittest.main()
