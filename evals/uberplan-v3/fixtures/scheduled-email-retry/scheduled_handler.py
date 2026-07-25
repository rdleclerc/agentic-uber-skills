from delivery_ledger import DeliveryLedger, RetryDecision


def handle_failed_send(attempt: int, max_attempts: int) -> RetryDecision:
    ledger = DeliveryLedger()
    return ledger.classify_failure(attempt=attempt, max_attempts=max_attempts)
