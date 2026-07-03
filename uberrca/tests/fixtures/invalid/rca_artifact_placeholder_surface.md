# RCA Artifact

- class_invariant: Dispatch must not mark a child terminal until exit code and expected output artifact are both observed.
- failure_case_id: subprocess-dies-without-terminal-state

## Surface enumeration

- tbd

## RCA ladder

- Symptom: child run disappeared without terminal output.

## Durable fix plan

- Lowest enforceable layer: dispatch wrapper.
