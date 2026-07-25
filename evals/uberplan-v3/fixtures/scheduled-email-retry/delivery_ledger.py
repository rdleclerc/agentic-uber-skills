from dataclasses import dataclass


@dataclass(frozen=True)
class RetryDecision:
    retry: bool
    delay_seconds: int | None


class DeliveryLedger:
    def classify_failure(self, *, attempt: int, max_attempts: int) -> RetryDecision:
        """Attempts are one-indexed; max_attempts is the total allowed sends."""
        if attempt <= max_attempts:
            return RetryDecision(retry=True, delay_seconds=60 * (2 ** (attempt - 1)))
        return RetryDecision(retry=False, delay_seconds=None)
