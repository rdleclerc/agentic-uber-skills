# Approved Tier 2 plan r7

Preserve the deletion trust boundary in `delete_guard.py`.

1. Refuse deletion when `actor` is empty.
2. Preserve the configured actor.
3. Run both tests in `test_delete_guard.py`.
4. Use exactly one independent safety reviewer for the exact diff, scope, and proof.
