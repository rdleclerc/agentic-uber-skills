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
- For Tier 2/3, did the V0 plan premortem run after the first concrete plan, and did every material failure mode receive either a plan revision or explicit accepted-risk rationale?
- Did the premortem challenge overengineering/code-bloat, proposed new files/modules/abstractions, what can be deleted/merged/avoided, and the 80/50 alternative?
- Has the Simplifier found a smaller/elegant path that should replace this plan?
- Has the Codebase Scout checked existing patterns/tests/claims when the repo is nontrivial?
- Has the OpenClaw/Platform Steward checked local policy when OpenClaw/Type0/runtime is touched?
- Has the Architecture Steward participated early enough to shape the plan, not just approve it afterward?
- Are architecture guidelines satisfied?
- Are source authority/truth boundaries clear?
- Is rollback/adoption state clear?
- Is the rubric measurable rather than aspirational?
- Did the steward challenge unnecessary complexity, subagent cost, and over-tiering?

## Final Value Adversary / cautious-theater gate

For Tier 2/3, run one fresh-context independent review of the final plan immediately before acceptance. Give the reviewer only the operator instruction, final plan, and decisive evidence. Require `BLOCK` or `APPROVE`, not another open-ended review round.

The review must return:

- **Strictly necessary now:** each retained material slice/mechanism and the explicit requirement or named failure it protects.
- **Evidence-contingent:** work removed from the initial plan, with the exact trigger that would justify restoring it.
- **Cautious theater:** ceremony, speculative generalization, redundant proof/review, or machinery not tied to an evidenced risk; delete it.
- **Smallest linear alternative:** the least-branched plan that preserves the operational outcome.
- **Reduction:** slices, files, agents/reviews, production surface, and operator steps removed.
- **First valuable checkpoint:** the earliest result useful even if later work stops.

Block acceptance when cautious-theater work remains, evidence-contingent work is scheduled before its trigger, or generic caution is the only justification. Do not classify explicit requirements, trust-boundary validation, data-loss protection, security, source authority, or irreversible side-effect gates as theater.

Verdict:

```text
Confidence verdict:
- 100% confident within scope? yes/no
- Value Adversary verdict: APPROVE/BLOCK
- Strictly necessary now:
- Evidence-contingent and trigger:
- Cautious theater deleted:
- Smallest linear plan / reduction:
- First valuable checkpoint:
- Scope:
- Material blockers:
- Non-blocking residual risks:
- Required revisions:
- Evidence required before completion:
```
