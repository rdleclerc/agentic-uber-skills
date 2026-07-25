from promotion_tool import promote_release


def run_promote(release_id: str, provider) -> dict:
    return promote_release(release_id, provider)
