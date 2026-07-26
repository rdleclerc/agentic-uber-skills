# UberAccept lifecycle eval

This suite preserves the champion/challenger evidence used to tune UberAccept.
Working cases gate ordinary decision quality; holdouts test authority and scope;
forward cases test risk-scaled proof. Rubrics are frozen before candidate edits.

Run agents in fresh context. Give each agent the selected `SKILL.md` plus only
the named fixture files. Agents must not edit the fixture or implementation.
Record decision, causal completeness, scope, files read, output size, and tool
calls. A hard-gate failure cannot be offset by a shorter answer.
