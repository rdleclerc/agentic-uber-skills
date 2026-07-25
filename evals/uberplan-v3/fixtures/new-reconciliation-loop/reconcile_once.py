def reconcile_once(records: list[dict]) -> list[str]:
    return [
        record["id"]
        for record in records
        if record["provider_confirmed"] and record["state"] == "pending"
    ]
