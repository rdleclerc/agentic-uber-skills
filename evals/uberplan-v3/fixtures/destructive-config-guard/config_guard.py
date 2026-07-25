class AuthorizationError(Exception):
    pass


def require_delete_actor(actor_id: str | None, configured_actors: set[str]) -> str:
    if actor_id is None:
        return "system"
    if actor_id not in configured_actors:
        raise AuthorizationError("actor is not allowed to delete environments")
    return actor_id
