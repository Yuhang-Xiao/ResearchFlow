"""Gate: result claims are not over-stated."""

from __future__ import annotations

from workflow1.quality_gates.base import QualityGate


class ClaimGuardGate(QualityGate):
    gate_name = "ClaimGuardGate"
    risky_terms = ["prove causality", "causal effect", "政策证明", "因果证明", "必然", "完全解决"]

    def run(self, context: dict[str, object]):
        text = str(context.get("paper_text", ""))
        risky = [term for term in self.risky_terms if term.lower() in text.lower()]
        if risky:
            return self.fail(risky, ["downgrade_claims_to_association_or_exploratory"])
        return self.pass_()
