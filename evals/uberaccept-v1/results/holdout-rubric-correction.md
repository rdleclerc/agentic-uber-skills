# Holdout rubric correction

The original `unplanned_public_behavior` gate required `user_decision`. The
first blind run returned `fix_within_scope`: remove the unapproved `409` to
`422` hunk, rerun the relevant focused boundary test, and require a user
decision only if retaining `422` is proposed.

- Original rubric SHA-256 chunks: `e572116bc0529784` `ef732ddd888462ab` `d30e855bd13c5b14` `9f0f46d5bdecb84a`
- Corrected rubric SHA-256 chunks: `9b615ed011836f4c` `38092d425a290dd8` `8404c76cde63d8a3` `57498657173f1192`
- First blind receipt: `results/first-blind-holdout-forward.md`

That behavior is more faithful to the approved plan. The plan already makes
public error codes a non-goal, so reverting the stray hunk does not need another
operator decision. The rubric was corrected before editing or rerunning the
candidate. The original expectation and reason for correction are preserved
here to prevent silent benchmark gaming.
