import pytest

from promotion_tool import PromotionError, promote_release


class FailingProvider:
    def promote(self, release_id):
        raise RuntimeError("provider unavailable")


def test_provider_failure_is_typed():
    with pytest.raises(PromotionError):
        promote_release("rel-1", FailingProvider())
