STATUSES = {
    "accepted",
    "fix_within_scope",
    "replan",
    "user_decision",
    "blocked_with_failure_intake",
    "rejected",
}


def tier_two_review():
    return ["exact_diff", "specialist_review_board"]


def final_status(report):
    return report.get("acceptance_status") or "accepted"


def required_acceptance_sections():
    return [f"section_{index}" for index in range(1, 20)]
