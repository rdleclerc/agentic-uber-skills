import pytest

from config_guard import AuthorizationError, require_delete_actor


def test_missing_actor_is_rejected():
    with pytest.raises(AuthorizationError):
        require_delete_actor(None, {"alice"})


def test_configured_actor_is_preserved():
    assert require_delete_actor("alice", {"alice"}) == "alice"


def test_unknown_actor_keeps_typed_error():
    with pytest.raises(AuthorizationError):
        require_delete_actor("mallory", {"alice"})
