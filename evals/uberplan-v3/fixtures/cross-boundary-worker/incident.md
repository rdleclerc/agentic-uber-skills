# Production delivery incident

At 10:04, ingress accepted 18,200 export jobs while all workers were saturated.
At 10:07, a worker crashed after dequeuing and before committing its result.
The dequeued job never reappeared. The status API continued to report both the
lost job and newly admitted jobs as `accepted`. Operators could not distinguish
durable work from requests only held in process memory.

The queue depth grew until the process was killed. Restarting recovered none of
the dequeued or in-memory jobs.
