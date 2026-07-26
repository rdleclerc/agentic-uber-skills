# Forward rubric correction

The original Tier 3 case expected `blocked_with_failure_intake`, but its evidence
said canary authorization was absent. Under the typed contract, that requires
`user_decision`; it is not an environmental failure.

- Original rubric SHA-256 chunks: `94f32fdc02bf8c6f` `ffa50ad3f17227e2` `9c92316fd2d6dddc` `3438762a135039d9`
- Corrected rubric SHA-256 chunks: `c59533cd2edaa3b2` `8c83dfd5fa546f1a` `d179a3de07c25233` `c49410dd90a9e8c7`
- First blind receipt: `results/first-blind-holdout-forward.md`

The suite now preserves that authority case and adds a separate unavailable
runtime-gate case, with authorization already present and a filed broker-error
receipt. This directly tests `blocked_with_failure_intake` without conflating
operator authority and external failure.
