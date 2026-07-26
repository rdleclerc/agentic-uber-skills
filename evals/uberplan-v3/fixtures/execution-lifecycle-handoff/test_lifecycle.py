import unittest

from lifecycle import final_status, required_acceptance_sections, tier_two_review


class LifecycleContractTests(unittest.TestCase):
    def test_current_tier_two_default_is_a_board(self):
        self.assertEqual(["exact_diff", "specialist_review_board"], tier_two_review())

    def test_current_missing_status_fails_open(self):
        self.assertEqual("accepted", final_status({}))

    def test_current_report_is_universal(self):
        self.assertEqual(19, len(required_acceptance_sections()))


if __name__ == "__main__":
    unittest.main()
