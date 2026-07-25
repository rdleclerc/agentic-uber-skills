REQUEST_KEYWORDS = {"please", "can you", "find", "write"}


def is_request(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in REQUEST_KEYWORDS)
