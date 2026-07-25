from config_guard import require_delete_actor


def delete_environment(
    environment: str, actor_id: str | None, configured_actors: set[str]
) -> str:
    authorized_actor = require_delete_actor(actor_id, configured_actors)
    return f"delete:{environment}:authorized-by:{authorized_actor}"
