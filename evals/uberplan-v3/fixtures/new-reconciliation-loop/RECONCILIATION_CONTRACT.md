# Reconciliation contract

`reconcile_once` is the canonical single-pass calculation. It returns candidate
record IDs and does not mutate providers. A loop runner may checkpoint verified
record IDs and submit an already-approved record once. Unapproved candidates
remain pending for human review.

The loop must expose its run ID, cursor, attempted count, verified count,
deferred count, and terminal reason.
