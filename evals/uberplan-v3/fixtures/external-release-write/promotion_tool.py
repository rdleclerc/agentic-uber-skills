class PromotionError(Exception):
    pass


def promote_release(release_id: str, provider) -> dict:
    try:
        return provider.promote(release_id)
    except Exception as exc:
        raise PromotionError(str(exc)) from exc
