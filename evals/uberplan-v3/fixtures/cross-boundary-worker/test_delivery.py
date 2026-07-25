from queue import JobQueue
from status import public_status


def test_taken_job_is_not_redelivered_after_crash():
    queue = JobQueue([{"id": "job-1"}])
    assert queue.take()["id"] == "job-1"
    assert queue.take() is None


def test_unknown_job_is_reported_as_accepted():
    assert public_status("lost", set(), set()) == "accepted"
