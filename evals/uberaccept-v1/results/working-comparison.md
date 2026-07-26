# Working comparison

## Champion

| Case | Decision | Words | Tool calls | Key behavior |
|---|---:|---:|---:|---|
| false-ready-missing-blackbox | rejected / no ship | ~50 | 4 shared | Correctly names missing CLI proof but makes a planned local proof gap terminal. |
| unknown-upstream-status | blocked / no ship | ~45 | 4 shared | Preserves absence of rejection, but has no precise typed contract for the unknown state. |
| authoritative-rejection | rejected | ~45 | 4 shared | Preserves the authoritative terminal. |
| contained-fully-proved | accepted | ~55 | 4 shared | Accepts the exact contained claim without irrelevant ceremony. |

## Challenger 1

| Case | Decision | Words | Tool calls | Key behavior |
|---|---:|---:|---:|---|
| false-ready-missing-blackbox | fix_within_scope | ~78 | 4 shared | Names exact planned CLI proof and false-green risk; no extra scope. |
| unknown-upstream-status | blocked_with_failure_intake | ~74 | 4 shared | Preserves UNKNOWN, names missing evaluator receipt, no invented rejection; fresh rerun files `unknown-upstream-status-1`. |
| authoritative-rejection | rejected | ~61 | 3 shared | Preserves authoritative status and evidence id. |
| contained-fully-proved | accepted | ~73 | 3 shared | Accepts exact claim with proportional evidence. |

All agents read only the selected skill and allowed fixture files. No agent read
the hidden rubric or edited implementation files.
