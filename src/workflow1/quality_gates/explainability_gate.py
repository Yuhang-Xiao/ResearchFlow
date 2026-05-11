"""Gate: SHAP or fallback explainability is present."""

from __future__ import annotations

from workflow1.quality_gates.base import QualityGate


class ExplainabilityGate(QualityGate):
    gate_name = "ExplainabilityGate"

    def run(self, context: dict[str, object]):
        shap_available = bool(context.get("shap_available"))
        ran_shap = bool(context.get("ran_shap"))
        fallback = bool(context.get("fallback_explainability"))
        if shap_available and not ran_shap:
            return self.fail(["shap_available_but_not_run"], ["run_shap_or_fallback"])
        if not shap_available and not fallback:
            return self.fail(["missing_explainability_fallback"], ["run_permutation_importance_pdp_or_ale"])
        return self.pass_()
