"""Gate: baseline and multi-model comparison are present."""

from __future__ import annotations

from workflow1.quality_gates.base import QualityGate


class ModelComparisonGate(QualityGate):
    gate_name = "ModelComparisonGate"

    def run(self, context: dict[str, object]):
        models = list(context.get("models", []))
        has_baseline = any("baseline" in str(m).lower() or "dummy" in str(m).lower() for m in models)
        if len(models) < 2 or not has_baseline:
            return self.fail(["baseline_or_multi_model_comparison_missing"], ["train_baseline_and_compare_models"])
        return self.pass_()
