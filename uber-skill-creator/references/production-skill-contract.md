# Production Skill Contract

Use this reference when a skill is meant to be reused by a team, installed across runtimes, released as library infrastructure, or treated as governed behavior. Keep scaffold and one-off work lighter.

## Non-Skill Check

Before creating or expanding a skill, ask what the user really needs:

- **Direct answer:** use when the job is a one-off explanation, summary, translation, or brainstorm.
- **Document or note:** use when the reusable artifact is knowledge, policy, or handoff text with no routed agent execution.
- **Script:** use when the task is deterministic and discoverability/routing is not the hard part.
- **Skill:** use only when the job is recurring, discoverability matters, the workflow needs a boundary, or reusable instructions/checks improve future agent behavior.

If reuse is plausible but unproven, start at `Scaffold` and upgrade after real use.

## Maturity Tiers

| Tier | Use for | Minimum gates |
|---|---|---|
| `Scaffold` | personal or exploratory skill | package validation and resource-boundary check |
| `Production` | reusable team skill | scaffold gates plus trigger evals |
| `Library` | shared infrastructure or multi-client package | production gates plus packaging validation, route-confusion checks, and stronger description tuning |
| `Governed` | critical, meta-level, policy-sensitive, or high-trust skill | library gates plus ownership, review cadence, regression history, promotion policy, and acceptance evidence |

More gates are not automatically better. If a new gate raises context cost without changing a release decision, record it as a future eval idea instead.

## Compact Contract

For `Production` and above, create a small contract section or adjacent JSON/Markdown artifact that names:

- owned recurring job
- trigger description
- should-trigger, should-not-trigger, and near-neighbor examples
- workflow steps, decision points, and expected outputs
- scripts, references, assets, and reports that carry real behavior
- trigger eval plan and output eval plan
- output risk, execution risk, trust boundary, and side-effect boundary
- owner or owning team
- maturity tier, lifecycle status, and review cadence
- target runtimes/platforms and any known semantic loss between them

Leave unknown fields explicit as `missing evidence` or `not yet tested`. Do not invent adapters, telemetry, benchmarks, or target support.

## Review Actions

When evaluation finds a warning or blocker, make it operational. Each action should include:

- `gate_key`: the contract area that failed
- `status`: `warn` or `block`
- `summary`: one sentence
- `why`: user/system risk in plain language
- `source_fix`: smallest file or section to change
- `evidence`: artifact, eval, transcript, or command output proving the issue
- `verification_command`: command or manual check that closes it

Waivers may document accepted warning-level risk, but they do not convert blockers into passes.

## Metadata-Only Drift

For production/library/governed skills, real use should become future evals without storing private raw content. Accept only narrow local metadata such as:

- event type: `skill_activation`, `skill_output`, `script_run`, `review_event`
- skill name and version
- source/client name
- command name without arguments
- outcome: `accepted`, `edited`, `rejected`, `missed`, `failed`, `reviewed`, `unknown`
- failure type: `wrong_trigger`, `under_trigger`, `bad_output`, `missing_resource`, `script_error`, `review_overdue`, `none`
- timestamp

Never collect raw prompts, outputs, transcripts, notes, messages, private files, command arguments, or reviewer comments as telemetry. Convert missed triggers into trigger evals, bad outputs into output eval assertions, and script errors into smoke tests.
