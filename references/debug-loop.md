# Debug Loop Reference

Use this for ordinary defects and bug fixes. It is deliberately lighter than `$uberrca`; it keeps daily debugging reproducible without turning every bug into an incident review.

## Loop

1. Reproduce the failure on the real path or record `no_repro_reason`.
2. Capture the reproduced-red receipt: failing command, relevant output, input or fixture, and environment assumptions needed to rerun it.
3. Hypothesize the smallest plausible cause that explains the red result.
4. Bisect or narrow until the suspected cause is tied to code, state, config, data, or tool output.
5. Fix the smallest layer that can make the reproduced red turn green.
6. Verify by rerunning the original red command or fixture and recording the now-green output.
7. Exit with exactly one P4 intake field: `failure_case_id`, `case_updated`, or `not_applicable_with_reason`.

## Escalation

Escalate to `$uberrca` on the second occurrence of the same failure class, on repeated same-class test failures during implementation, or when symptoms are architecture-shaped: concurrency, queues, workers, orchestration, long-running jobs, gateway stalls, workflow durability, backpressure, repeated timeouts, or repeated symptom patches.

When escalating, carry the reproduced-red receipt into `$uberrca` and require `class_invariant` plus `surface_enumeration`. The goal is to name the missing invariant, not to relabel ordinary debugging as RCA.

## Boundary

This loop is the default for everyday defects. `$uberrca` is the class-level and incident authority, and it never auto-triggers from ordinary bug similarity.
