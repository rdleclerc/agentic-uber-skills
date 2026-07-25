# Delivery ownership

`DeliveryLedger` is the sole owner of durable delivery attempts, retry
classification, backoff, and terminal failure. Callers submit one attempt and
delegate the outcome. Handlers must not implement retry policy or add another
coordinator.

Active source and tests are authoritative. Files under `archive/` describe
discarded designs and must not guide current changes.
