# Scheduled email retries

Several call sites invoke delivery retry behavior. Add a `RetryCoordinator`
between scheduled handlers and the delivery ledger so retry policy has one
owner. The coordinator should own attempt state, backoff, and terminal failure.

Production symptom: messages configured for three attempts receive a fourth
send.
