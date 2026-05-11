# Confidence Gate

Before answering, try to prove the plan is unsafe, incomplete, overbroad, under-tested, architecturally weak, too expensive, or impossible to verify.

Check:

- Is this tier too heavy or too light?
- Is the Codex goal necessary, or would ordinary coding be cheaper and sufficient?
- Are subagents explicitly authorized and worth the coordination cost?
- Is each added guardrail tied to a named failure class, or are we building ceremony?
- Is there a smaller change that is also safer because it removes moving parts?
- Are write sets disjoint?
- Are critical tests/evals/audits missing?
- Are real-world fixtures required and available?
- Are external writes/destructive actions gated?
- Did the planning review board run the lanes justified by risk, or explicitly skip them?
- Has the Agent Advocate reconstructed why the agent made/would make the error, rather than treating the agent as random?
- Has the Agent Advocate answered the human counterfactual: would a competent human with normal context/tools have made the error?
- If a human likely would not have erred, does the plan fix the agent's missing context, capability, tool feedback, source clarity, memory/history, state signal, or recovery guidance?
- Does the plan fix the failed context/tool/source/memory/feedback/invariant layer instead of patching a symptom?
- For model-output boundaries, did the plan prove shape, authority, isolation, failure semantics, observability, and replay/eval evidence rather than listing generic reliability words?
- Are regexes, keyword lists, and string matchers limited to mechanical parsing or candidate signals, with no unapproved semantic authority over natural language?
- Has the Loophole Hunter found any unresolved blockers?
- Has the Simplifier found a smaller/elegant path that should replace this plan?
- Has the Codebase Scout checked existing patterns/tests/claims when the repo is nontrivial?
- Has the OpenClaw/Platform Steward checked local policy when OpenClaw/Type0/runtime is touched?
- Has the Architecture Steward participated early enough to shape the plan, not just approve it afterward?
- Are architecture guidelines satisfied?
- Are source authority/truth boundaries clear?
- Is rollback/adoption state clear?
- Is the rubric measurable rather than aspirational?
- Did the steward challenge unnecessary complexity, subagent cost, and over-tiering?

Verdict:

```text
Confidence verdict:
- 100% confident within scope? yes/no
- Scope:
- Material blockers:
- Non-blocking residual risks:
- Required revisions:
- Evidence required before completion:
```
