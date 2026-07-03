# Sample Routing Answers - Pass

## R01
case_id: R01
tier: Tier 0
artifact: no durable artifact beyond inline note
routing: tier 0
gates: no review; tier0 trailer

## R02
case_id: R02
tier: Tier 1
artifact: micro-intent
routing: tier 1
gates: exact-diff review pass; acceptance criteria and verification command

## R03
case_id: R03
tier: Tier 3
artifact: full uberplan using uberplan/templates/plan-tier3.md
routing: tier 3 with live gate
gates: plan review, exact-diff review, adversarial review, acceptance

## R04
case_id: R04
tier: Tier 2
artifact: uberplan with source/approval boundaries
routing: tier 2 source approval
gates: exact-diff review, independent adversarial lane, scope-fidelity verdict

## R05
case_id: R05
tier: Tier 1 + loop_mode
artifact: Loop Contract inside uberplan
routing: Tier 1 loop_mode
gates: no-progress rule and failure cap; uberrca on same-family failure

## R06
case_id: R06
tier: Tier 2
artifact: scope artifact plus plan
routing: Tier 2 doctrine
gates: drift-registry update, exact-diff review, independent adversarial lane, scope-fidelity verdict

## R07
case_id: R07
tier: Tier 1
artifact: deletion receipt plus micro-intent
routing: Tier 1 dead module
gates: exact-diff review, dead-code proof, rollback note

## R08
case_id: R08
tier: Tier 2
artifact: uberplan for behavior surface
routing: Tier 2 behavior surface
gates: exact-diff review, independent adversarial lane, scope-fidelity verdict

## R09
case_id: R09
tier: no goal; assessment route
artifact: uberassess assessment packet
routing: no goal assessment route
gates: source authority, approval boundary, no implementation

## R10
case_id: R10
tier: Tier 3
artifact: uberplan plan tree
routing: Tier 3 production
gates: 4-phase ladder, safe-predecessor approval, live proof

## R11
case_id: R11
tier: Tier 3
artifact: uberplan with provider risk surfaced
routing: Tier 3 provider routing
gates: 4-phase ladder and reject under-tiered routing

## R12
case_id: R12
tier: Tier 3
artifact: scope artifact plus full plan
routing: Tier 3 live-injected
gates: live-injected rider, GAIA_TESTING live-proof gate, 4-phase ladder
