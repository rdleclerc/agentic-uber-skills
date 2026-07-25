# Promotion tool contract

Release promotion is an external write. The caller must supply a scoped
approval token and stable idempotency key. The tool returns a durable receipt
containing release ID, idempotency key, provider operation ID, and terminal
state. Missing approval fails before the provider call. Duplicate keys return
the existing receipt. Provider failures propagate as `PromotionError`; the
tool must not retry silently.
