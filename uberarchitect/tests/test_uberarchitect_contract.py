from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UberarchitectContractTests(unittest.TestCase):
    def test_skill_contains_stepback_packet_contract(self) -> None:
        body = (ROOT / "SKILL.md").read_text()
        for phrase in [
            "Do not auto-trigger from task similarity",
            "Architecture Stepback Packet",
            "Plain-English diagnosis",
            "System class",
            "Normal industry architecture",
            "Fresh-start architecture",
            "Current mismatch",
            "Symptom patches demoted",
            "Smallest transition path",
            "Scope revision required",
            "Proof gate",
            "Human counterfactual",
            "producer → durable queue → bounded worker pool → durable state/results → backpressure",
        ]:
            self.assertIn(phrase, body)

    def test_template_contains_required_fields(self) -> None:
        template = (ROOT / "templates" / "architecture-stepback-packet.md").read_text()
        for heading in [
            "## Plain-English diagnosis",
            "## System class",
            "## Normal industry architecture",
            "## Fresh-start architecture",
            "## Current mismatch",
            "## Symptom patches demoted",
            "## Smallest transition path",
            "## Scope revision required",
            "## Proof gate",
            "## Human counterfactual / agent affordance gap",
            "## Recommendation",
        ]:
            self.assertIn(heading, template)

    def test_golden_invocation_examples_cover_type0_failure(self) -> None:
        data = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        trigger_names = {example["name"] for example in data["trigger_examples"]}
        non_trigger_names = {example["name"] for example in data["non_trigger_examples"]}
        self.assertIn("type0_gateway_concurrency", trigger_names)
        self.assertIn("tiny_typo_fix", non_trigger_names)
        type0 = next(example for example in data["trigger_examples"] if example["name"] == "type0_gateway_concurrency")
        for term in ["queue", "worker", "backpressure", "durable state", "symptom patches demoted"]:
            self.assertIn(term, type0["must_surface"])


if __name__ == "__main__":
    unittest.main()
