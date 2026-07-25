from delivery_ledger import DeliveryLedger
from scheduled_handler import handle_failed_send


def test_last_allowed_attempt_is_terminal():
    decision = DeliveryLedger().classify_failure(attempt=3, max_attempts=3)
    assert decision.retry is False
    assert decision.delay_seconds is None


def test_handler_delegates_retry_classification():
    assert handle_failed_send(attempt=2, max_attempts=3).retry is True
