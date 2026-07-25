PENDING: list[dict] = []


def accept_export(job: dict) -> dict:
    PENDING.append(job)
    return {"job_id": job["id"], "status": "accepted"}
