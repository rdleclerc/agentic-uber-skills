# Ubercampaign Profile

Use this cold-loaded `ubergoal` profile when the user says `ubercampaign`, campaign, product campaign, multi-feature campaign, feature-list campaign, plan-tree campaign, or asks to “boil the ocean, assess every item, plan each one, then execute.”

`ubercampaign` is not a new skill. It is a named `ubergoal` campaign shape for multi-item, multi-phase work where each item needs assessment, planning, execution, evidence, and terminal status.

## Campaign contract

A campaign is a root goal with item-by-item children. The root may coordinate and summarize, but it cannot complete children by sharing one proof layer.

Allowed child terminal states:

- `operational` — the child reached its Operational Outcome Contract with target-system proof.
- `blocked` — exact external blocker, evidence, owner/prerequisite, and next unblock action recorded.
- `re_scoped_with_approval` — the user approved a smaller target before completion; original target remains visible as deferred.

Do not count root demos, shared safe proof spines, registries, readiness gates, plans, local-only proofs, or shadow-only proofs as child completion unless the child contract explicitly scoped that artifact as the final outcome.

## Runtime topology and escalation

Plan-tree depth and spawned-agent depth are different. A campaign may have many nested plan files while the runtime uses a bounded subagent tree.

Default local Codex campaign topology:

- config preset: `max_threads=6`, `max_depth=2`;
- role shape: L0 root orchestrator → L1 workstream/feature orchestrator → L2 bounded worker or reviewer;
- L2 workers do not spawn further in default mode.

If the campaign appears to require L0→L1→L2→L3 delegation, stop and ask before changing config. Use this prompt shape:

```text
This campaign appears to need deep-campaign mode. Current local default is max_threads=6, max_depth=2. Switch temporarily to max_threads=8, max_depth=3 and restore 6/2 after the campaign?
```

`max_threads=10`, `max_depth=3` is only for unusually wide/deep campaigns and requires separate explicit approval. Record approval, selected preset, config backup path, restore target, and restore proof/blocker in `status-ledger.md`. Never silently raise thread/depth limits.

## Required file tree

Prefer a campaign artifact directory, not one giant file:

```text
campaigns/<campaign-slug>/
├── index.md                         # root objective, scope, phases, approval gates
├── status-ledger.md                 # one row per item/child/subchild
├── assessments/
│   ├── index.md                     # assessment summary and decisions
│   └── <item-slug>.md               # per-item uberassess packet or summary
├── plans/
│   ├── index.md                     # plan queue and dependencies
│   └── <item-slug>/
│       ├── index.md                 # feature/item plan root
│       ├── child-<n>.md             # optional subplans
│       └── status-ledger.md
├── receipts/
│   └── <item-slug>.md               # child acceptance/implementation receipt
└── final-acceptance.md              # root uberaccept result
```

Keep root files short and navigational. Put deep work in child files. Each continuation should start by reading `index.md`, `status-ledger.md`, and the current child file only.

## Phase 0 — campaign launch

1. Create or bind the root platform goal when available.
2. Create the campaign artifact tree.
3. Record the feature/item inventory with stable IDs and slugs.
4. Name approval gates: assessment gate, planning gate, execution gate, root acceptance gate.
5. Define root success: every adopted item has a terminal state and evidence.
6. Record runtime topology: configured/reportable `max_threads`, `max_depth`, role shape, depth-3 escalation approval if any, and restore target.
7. If the campaign may run for days/week, set a checkpoint cadence: update `status-ledger.md` after every child and at least once per work session.

## Phase 1 — boil-the-ocean assessment

Run a root `uberassess` over the whole list first:

```text
root_assessment = uberassess(full_item_list, mode="deep research / boil the ocean")
```

Then assess every item enough to decide its lane:

```text
FOR item IN campaign_items:
    item_assessment = uberassess(item)
    decision = adopt | reject | watch | eval_only | needs_more_research
    write assessments/<item>.md
    update assessments/index.md and status-ledger.md
END
```

Do not deeply plan rejected/watch/eval-only items. For `needs_more_research`, either run the missing assessment work or mark the item `blocked` until the prerequisite is available.

**Approval gate:** stop for user approval before planning implementation for adopted items unless the user already explicitly authorized the full campaign.

## Phase 2 — plan-tree generation

For each adopted item:

```text
FOR adopted_item IN adopted_items:
    item_plan = uberplan(item_assessment)
    IF item_plan contains multiple operational outcomes OR depth risk:
        create plans/<item>/index.md + child plan files + status-ledger.md
    validate item_plan has:
        Operational Outcome Contract
        Recursive / Hierarchical Execution Pseudocode when child plans exist
        Plan Tree Artifact Layout
        child terminal-state ledger
        evidence gates and rollback/stop conditions
        confidence gate after trying to falsify the plan
END
```

Plans may iterate. A plan is not ready until it names what would make the item operational, what evidence proves it, and what does not count.

**Approval/confidence gate:** stop before execution if plans are not confidence-gated, if the campaign scope changed materially, or if the user has not approved implementation.

## Phase 3 — execution loop

Execute approved plans child by child, not as one blob:

```text
FOR item_plan IN approved_plan_queue ORDERED BY dependencies:
    read campaign index + status-ledger + item plan root
    WHILE item_plan has unfinished child plans:
        child = next unblocked child
        execute child under ubergoal/worker scope
        run tests/evals/proofs named by child OOC
        IF repeated/material unexpected failure:
            stop, run uberrca, revise with uberplan, merge scope change, update ledger
        run child acceptance
        record terminal state operational | blocked | re_scoped_with_approval
        write receipts/<item-or-child>.md
        update item and root ledgers
    END
    run item-level uberaccept before marking item terminal
END
```

Do not let later leaves become superficial. Every leaf must have one of:

- its own Operational Outcome Contract and evidence;
- an explicit pointer to the parent contract proving why no separate evidence is needed;
- a `blocked` or `re_scoped_with_approval` state.

## Phase 4 — root acceptance

Run root `uberaccept` only after every adopted item has a terminal state.

Root final acceptance must include:

- item-by-item terminal-state table;
- evidence path for every operational item;
- blockers and next unblock actions;
- re-scopes and approval evidence;
- user expectation / surprise delta;
- Skills invoked summary;
- campaign run receipt;
- explicit statement that shared proof was not used to complete children.

## Week-long / multi-day durability rules

For campaigns expected to last days or a week:

- Keep `status-ledger.md` as the resume source of truth.
- At each session start, read only root index, root ledger, current item plan, and relevant receipt; do not reload the whole campaign tree.
- At each session end, write: current item, last evidence, next command/action, blockers, dirty repos, and whether user approval is needed.
- Use stable item IDs in every assessment, plan, branch, receipt, and final report.
- Never rely on chat memory alone for campaign state.
- If context gets large, summarize completed children in the ledger and continue from the current child file.
- If child depth exceeds the stated campaign budget, stop and ask or mark the branch `blocked` / `re_scoped_with_approval`.

## Anti-bloat policy

`ubercampaign` is a profile, not a harness. Do not build a hidden queue, semantic judge, scheduler, or orchestration framework inside the skill. Use files, ledgers, skills, typed tools, tests, and acceptance receipts. Add runtime machinery only through a separately approved implementation plan with benefit >> cost.
