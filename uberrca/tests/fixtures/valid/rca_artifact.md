# RCA Artifact

- class_invariant: Dispatch must not mark a child terminal until exit code and expected output artifact are both observed.
- failure_case_id: subprocess-dies-without-terminal-state

## Surface enumeration

- Dispatch wrapper exit code.
- Expected output artifact.
- Child ledger terminal state.

## RCA ladder

- Symptom: child run disappeared without terminal output.
- Immediate failure: wrapper accepted missing artifact.
- Enabling condition: no terminal contract.
- Failed guard/invariant: terminality was not tied to exit code plus output artifact.
- Upstream admission failure: dispatch launched without a receipt contract.
- Recovery/detection gap: retry was manual.
- Class-level cause: dispatch path lacked terminal-state invariant.

## Durable fix plan

- Lowest enforceable layer: dispatch wrapper.
- Tests/evals/monitors: exit-code plus expected-output fixture.
