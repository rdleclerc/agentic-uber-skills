# Shared Learning Inbox

This directory is for **sanitized, safe-to-commit learning packets** that should be shared across machines.

Do not commit raw traces, private prompts, credentials, customer data, full logs, or proprietary source dumps. Keep raw records local/private and share only distilled lessons with enough evidence to review.

Suggested flow:

1. On each machine, keep raw records outside the repo, for example:
   - `~/.agentic-uber-learnings/macbook/...`
   - `~/.agentic-uber-learnings/desktop/...`
2. When a lesson should travel, create a sanitized packet under:
   - `learning/inbox/<machine-id>/<YYYYMMDDTHHMMSS>-<slug>/post-run-learning.md`
3. Validate the packet with `uberskillevolver/scripts/validate_learning_record.py`.
4. Commit and push the packet.
5. Other machines pull and periodically review inbox packets with `uberskillevolver`.
6. Promote only high-value/repeated lessons into skill changes, evals, validators, templates, or deletions.

Shared packets are evidence, not automatic rules.
