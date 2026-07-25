from reconcile_once import reconcile_once


def test_returns_only_confirmed_pending_records():
    records = [
        {"id": "a", "provider_confirmed": True, "state": "pending"},
        {"id": "b", "provider_confirmed": False, "state": "pending"},
        {"id": "c", "provider_confirmed": True, "state": "complete"},
    ]
    assert reconcile_once(records) == ["a"]
