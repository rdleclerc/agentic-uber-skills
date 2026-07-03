Implemented the R16a Gaia runtime seed under the requested paths only. I did not run any git commands.

**Files Created**
- `evals/failures/README.md`
- `evals/failures/INDEX.md`
- `evals/failures/cases/{gmail-silent-lane-12d,hermes-overseer-dead-9w,silent-nonresponse-class,false-apology-fix-of-fix,human-owned-blocker-grind,op-hang-under-launchd,pg-null-upsert-dup,post-upgrade-silent-breakage,library-silent-truncation}.md`
- `scripts/run_twice_idempotency_check.sh` executable skeleton

**Validator Output**
```text
PASS: validated 9 failure case file(s)
```

**Case Dates/Status**
```text
false-apology-fix-of-fix | 2026-07-02 | seed
gmail-silent-lane-12d | 2026-06-19 | seed
hermes-overseer-dead-9w | 2026-05-04 | seed
human-owned-blocker-grind | 2026-06-24 | seed
library-silent-truncation | 2026-07-03 | seed
op-hang-under-launchd | 2026-07-03 | seed
pg-null-upsert-dup | 2026-07-03 | seed
post-upgrade-silent-breakage | 2026-04-29 | seed
silent-nonresponse-class | 2026-06-11 | seed
```

**Checks**
- Pack validator passed.
- `bash -n scripts/run_twice_idempotency_check.sh` passed.
- Helper smoke passed with a constant probe: second run inserted `0` rows.
- Runtime README is 25 lines.
- Index marks 12 process-canonical cases with `canonical: agentic-uber-skills/evals/failures/`.

**Flags**
- `op-hang-under-launchd`: repo evidence anchor is from 2026-07-02, but the catalog/dispatch says to seed it as a 2026-07-03 standing lesson. I kept `2026-07-03` and noted that.
- `pg-null-upsert-dup`: I found no repo-specific RCA receipt in this worktree; seeded from the catalog, `GAIA_TESTING.md`, and the new helper.
- `library-silent-truncation`: only a lightweight repo anchor exists in `knowledge/agent-followups.md`; I kept the catalog’s broader markdownify/html2text class and did not overclaim stronger repo evidence.

High-tier Claude review was not reachable: local Claude is logged out, and `type0` / `agclaw` SSH aliases do not resolve. This is locally verified only. 

