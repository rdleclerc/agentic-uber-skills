# Export delivery contract

Ingress may report `accepted` only after the queue has durably admitted a job.
A job may leave the queue only after its result is durably committed. Worker
crashes must cause safe redelivery, and duplicate execution must not produce
duplicate exports. When durable capacity is exhausted, ingress must refuse or
defer work explicitly rather than buffer without limit.

The queue owns durable admission and redelivery. The worker owns result commit
and idempotency. The status projection must derive public state from durable
queue and result records.
