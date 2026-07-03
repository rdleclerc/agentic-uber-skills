# Wave 2 — Dispatch 3: R5 pack-internal dedup (uberplan, uberaccept, uberassess, uberrca, uberskillevolver)

You are Codex, implementer. Pack repo only; NO git commands. P1 absolute: every deleted block → named home, receipt-mapped, verified present there. Entry gates satisfied: canonical homes exist (references/claude-adversary.md; references/operational-states.md; spine Review ladder; uberplan owns TUR + Gall's-Law planning bias), and the V3 subprocess probe PASSED (coordination/process-rearchitecture-202607/wave2-v3-probe.md) — reference-following is proven for both runtimes.

Read first: the five SKILL.md files; references/claude-adversary.md; references/operational-states.md; ubergoal/SKILL.md (the shape to match: pointer lines + unique content only); wave2-d2-deletion-receipt.md (receipt format).

## Per-skill dedup (uberplan 3,706w · uberaccept 2,641w · uberassess 2,100w · uberrca 1,684w · uberskillevolver 2,058w)

1. **Inlined Claude-adversary blocks (4 copies)**: in uberplan, uberaccept, uberassess, uberrca — replace each ~400-500-word block with: the skill's OWN "ask exactly" questions (keep verbatim, they are unique per skill) + ONE line: "Contract: `../references/claude-adversary.md` (opt-in only on explicit request; reconciliation + frame-independence rules there)." Delete everything else of the block (trigger phrases list, reconciliation taxonomy, frame-independence paragraph, scope-fidelity-packet mechanics — all present in the reference; verify each is truly there before deleting, add to the reference if genuinely missing rather than losing it).
2. **Blocked-state machine / topology / parent-child copies** in uberplan, uberaccept, uberskillevolver → one pointer line each to `../references/operational-states.md`. Verify the reference covers what each copy says; missing nuances get merged INTO the reference (single home), not kept locally.
3. **Gall's-Law / Basic-Spine-First restatements** (4 places): uberplan keeps ONE canonical statement (it is the planning skill); uberaccept/ubergoal/others get a pointer line or rely on uberplan routing. (ubergoal already handled.)
4. **Loop-engineering summaries** in uberplan/uberaccept/uberskillevolver: compress each to ≤1 line pointing at `../references/loop-engineering.md` (its own header says keep essentials local because references may not auto-load — that rationale is now DISPROVEN by the probe; update that header sentence in loop-engineering.md to cite the probe).
5. **Type0/product residue**: any remaining project-specific examples in these five skills → delete (receipt row) or genericize in place if load-bearing.
6. Keep each skill's frontmatter description untouched. Keep all validator/template references intact (uberaccept's 19-section report + validators are R8's business, NOT yours — do not restructure output contracts, only dedup shared-rule prose).

## Word budgets (standing, add to SKILL_WORD_BUDGETS in scripts/lint_pack_contract.py)

Set each of the five skills' budget to its post-dedup count + 10% headroom (round up to nearest 50). Report the numbers.

## Receipt + verification

- `coordination/process-rearchitecture-202607/wave2-d3-deletion-receipt.md`: same table format as d2 (removed block | words | invariant | new home | verified).
- Run: pack tests + lint (budgets included), per-skill lints/tests for all five, quick_validate for all five, drift report (no regressions on existing MATCHes).
- Print: per-skill before/after word counts + total pack SKILL.md word count (baseline 19,176; after R6 ubergoal=786; report the new total), the deletion receipt inline, and FLAG anything you could not preserve losslessly.
