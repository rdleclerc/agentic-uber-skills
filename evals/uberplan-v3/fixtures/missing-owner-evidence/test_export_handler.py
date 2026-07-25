import pytest

from export_handler import reconcile_export


class NoOwner:
    def owner_for(self, export_id):
        return None


def test_missing_owner_fails_explicitly():
    with pytest.raises(RuntimeError, match="owner is not available"):
        reconcile_export("exp-1", NoOwner(), NoOwner(), NoOwner())
