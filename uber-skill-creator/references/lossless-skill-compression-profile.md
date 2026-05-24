# Lossless Skill / Plan Compression Profile

Use this when improving a skill, skill pack, or durable plan artifact without changing behavior. Goal: reduce token load while preserving triggers, safety, output contracts, validators, and evidence expectations.

## Preserve exactly unless tests change

- YAML frontmatter `name` and core trigger meaning in `description`
- router-sensitive phrases such as `Do not auto-trigger from task similarity`
- validator-required headings, field labels, enum values, and table columns
- safety prohibitions, approval gates, side-effect boundaries, and blocker language
- output contracts, terminal states, receipt fields, and acceptance gates
- examples/evals/fixtures that prove behavior

## Compress first

- delete repeated rationale after the rule is stated once
- move detailed examples, variants, and long layouts into `references/`
- replace prose lists with tight bullets or tables
- collapse duplicate definitions into one canonical reference plus a pointer
- shorten local wording only when validator tests and trigger intent stay unchanged
- split giant hierarchical plans into root/child/ledger/receipt files instead of one long file

## Microcopy policy

Contractions such as `do not` → `don't` are optional and usually tiny savings. Do **not** change them in frontmatter, metadata, tests, validator-required phrases, or hard safety rules unless the matching tests are updated intentionally. Prefer deleting duplicate prose over contraction sweeps.

## Plan artifacts

Run the same pass on large plans before final presentation:

1. preserve Operational Outcome Contract, terminal states, pseudocode, status ledger, risk/evidence map, and acceptance rubric;
2. move long child details into child plan files when a plan tree is present;
3. keep the root plan as an index/control plane;
4. record what was compressed or split so future agents do not recreate the giant file.

## Proof of no loss

After compression, run package validators/tests, compare required headings/phrases, and update evals only when intentionally changing behavior. If a compression cannot be proven lossless, report it as an advisory candidate, not a patch.
