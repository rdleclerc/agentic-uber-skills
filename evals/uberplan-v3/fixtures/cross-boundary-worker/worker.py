from queue import JobQueue


def run_once(queue: JobQueue, result_store) -> bool:
    job = queue.take()
    if job is None:
        return False
    result = build_export(job)
    result_store.commit(job["id"], result)
    return True


def build_export(job: dict) -> str:
    return f"export:{job['id']}"
