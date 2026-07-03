# V3 subprocess reference-following probe — PASS (2026-07-03)

Fresh `codex exec` (gpt-5.5, medium, read-only sandbox, stdin closed) given a throwaway skill whose SKILL.md points at references/policy-data.md containing sentinel SENTINEL-KESTREL-4471.

Result: sentinel returned verbatim → unattended Codex subprocesses DO follow SKILL.md→reference pointers on demand.

Gate consequence: R5 may delete the 5 inlined adversary-block copies (each skill keeps its ≤3 unique questions + one pointer line). Evidence trail: probe skill + result in session scratchpad; verbatim output below.

```
SENTINEL-KESTREL-4471 — deployments allowed only between 02:00 and 04:00 UTC on Tuesdays.```

Operational lesson (R12): codex exec blocks forever on open non-TTY stdin — dispatch contract gains 'always redirect stdin explicitly (< /dev/null or - < file)'. First run hung 4m and was killed; retry with stdin closed succeeded.
