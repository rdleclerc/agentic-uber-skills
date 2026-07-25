from request_router import is_request


def dispatch(message: str, agent):
    if not is_request(message):
        return None
    return agent.respond(raw_message=message, candidate_signal="keyword_match")
