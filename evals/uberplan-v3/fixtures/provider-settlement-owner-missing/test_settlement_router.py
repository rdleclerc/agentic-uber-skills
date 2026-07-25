import pytest

from settlement_router import route_settlement


class NoOwner:
    def owner_for(self, payment_id):
        return None


def test_missing_settlement_owner_fails_explicitly():
    with pytest.raises(RuntimeError, match="settlement owner is unavailable"):
        route_settlement("pay-1", NoOwner(), NoOwner(), NoOwner())
