def public_status(job_id: str, pending_ids: set[str], committed_ids: set[str]) -> str:
    if job_id in committed_ids:
        return "complete"
    if job_id in pending_ids:
        return "accepted"
    return "accepted"
