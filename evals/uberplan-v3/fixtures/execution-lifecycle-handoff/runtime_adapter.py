from lifecycle import final_status, required_acceptance_sections, tier_two_review


def execution_contract(report):
    return {
        "tier_two_review": tier_two_review(),
        "acceptance_sections": required_acceptance_sections(),
        "terminal_status": final_status(report),
    }
