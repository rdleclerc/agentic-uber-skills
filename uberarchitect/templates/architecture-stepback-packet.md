# Architecture Stepback Packet

## Plain-English diagnosis

Explain the problem in human language before jargon.

## System class

Name the architectural class and why it applies.

## Normal industry architecture

Describe how this class of problem is usually solved. Include prior-art pattern names, not vendor worship.

## Fresh-start architecture

If a senior architect built this today from scratch, what would the shape be?

## Current mismatch

How does the current implementation fight that normal shape?

## Symptom patches demoted

Which local fixes may still help but are not the root architecture?

## Smallest transition path

- Stabilizer:
- Target architecture move:
- Deferred complexity:

## Scope revision required

Yes / no. If yes, state the revised implementation scope and do not approve the original local-patch plan until the operator or plan owner accepts that scope change.

## Proof gate

- Experiment:
- Metrics:
- Pass threshold:
- Falsifier:

## Human counterfactual / agent affordance gap

Would a competent senior human with the same facts likely miss this? If not, what context/tool/skill/feedback/gate did the agent lack?

## Recommendation

Adopt / watch / reject / needs research. State implementation approval boundary.
