def route_settlement(payment_id: str, adapter, ledger, handler):
    for candidate in (adapter, ledger, handler):
        owner = candidate.owner_for(payment_id)
        if owner is not None:
            return owner.reconcile(payment_id)
    raise RuntimeError("settlement owner is unavailable")
