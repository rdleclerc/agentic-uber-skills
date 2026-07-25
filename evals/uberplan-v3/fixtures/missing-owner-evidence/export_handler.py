def reconcile_export(export_id: str, handler, provider, ledger):
    owner = handler.owner_for(export_id)
    if owner is None:
        owner = provider.owner_for(export_id)
    if owner is None:
        owner = ledger.owner_for(export_id)
    if owner is None:
        raise RuntimeError("export owner is not available")
    return owner.reconcile(export_id)
