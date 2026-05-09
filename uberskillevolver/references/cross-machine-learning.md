# Cross-Machine Learning

Use this when the same skill pack is used on multiple machines and you want `uberskillevolver` lessons to combine safely.

## Principle

Synchronize **sanitized lesson packets**, not raw agent memory. Git is the merge layer; human-reviewed promotion is the learning layer.

## Recommended layout

- Raw/private records: `~/.agentic-uber-learnings/<machine-id>/<skill>/<timestamp>-<run>/post-run-learning.md`
- Shared/sanitized packets in this repo: `learning/inbox/<machine-id>/<timestamp>-<run>/post-run-learning.md`
- Processed packets: `learning/processed/...` after promotion/rejection, or leave in inbox with a linked promotion batch if the team prefers an append-only inbox.

## Per-run workflow

1. Create a local record:

```bash
uberskillevolver/scripts/new_learning_record.py \
  --root ~/.agentic-uber-learnings/$(hostname -s) \
  --skill ubergoal \
  --run-slug my-run
```

2. Fill it in and validate it:

```bash
uberskillevolver/scripts/validate_learning_record.py \
  ~/.agentic-uber-learnings/$(hostname -s)/ubergoal/<timestamp>-my-run/post-run-learning.md
```

3. If it contains a lesson worth sharing, copy a sanitized version into the repo inbox:

```bash
mkdir -p learning/inbox/$(hostname -s)/<timestamp>-my-run
cp ~/.agentic-uber-learnings/$(hostname -s)/ubergoal/<timestamp>-my-run/post-run-learning.md \
  learning/inbox/$(hostname -s)/<timestamp>-my-run/post-run-learning.md
```

4. Re-check `Privacy and redaction` says `Safe to commit? yes`, then commit and push.

## Periodic merge workflow

Before changing the skill pack, review the inbox:

```text
Use $uberskillevolver to review learning/inbox across machines. Group repeated lessons, reject weak/noisy lessons, and propose a promotion batch with benefit >> cost for each change.
```

Promotion targets:

- eval seed or regression case
- validator/check
- template tweak
- script/tool change
- deletion/simplification
- no-change/defer note

## Guardrails

- Do not commit secrets, private traces, credentials, raw prompts/responses, or large logs.
- Do not promote a one-off annoyance into permanent process without a strong benefit >> cost case.
- Do not let two machines silently fork the skill pack. Pull before adding packets; push small learning commits frequently.
- If two packets disagree, preserve both as evidence and decide in a promotion batch.
