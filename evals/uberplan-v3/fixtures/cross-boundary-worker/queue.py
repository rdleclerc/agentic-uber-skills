class JobQueue:
    def __init__(self, jobs: list[dict]):
        self.jobs = list(jobs)

    def take(self) -> dict | None:
        if not self.jobs:
            return None
        return self.jobs.pop(0)

    def depth(self) -> int:
        return len(self.jobs)
