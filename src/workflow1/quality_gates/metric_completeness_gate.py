"""Gate: task-appropriate metrics are present."""

from __future__ import annotations

from workflow1.model_registry import load_model_registry
from workflow1.quality_gates.base import QualityGate


CLASSIFICATION = {"accuracy", "precision", "recall", "f1", "macro_f1", "weighted_f1", "balanced_accuracy", "mcc", "roc_auc", "pr_auc", "confusion_matrix"}
REGRESSION = {"mae", "rmse", "r2", "rmsle", "median_ae", "residual_analysis", "extreme_value_error"}


class MetricCompletenessGate(QualityGate):
    gate_name = "MetricCompletenessGate"

    def run(self, context: dict[str, object]):
        task_type = str(context.get("task_type", ""))
        raw_metrics = dict(context.get("metrics", {}))
        metrics = {str(k).lower() for k in raw_metrics.keys()}
        registry = context.get("registry")
        if registry is None:
            registry = load_model_registry()
        required_from_registry = set()
        if hasattr(registry, "get_map"):
            required_from_registry = {str(k).lower() for k in registry.get_map("task_to_metric_map", task_type).get("required_metrics", [])}
        required = required_from_registry or (
            CLASSIFICATION if "classification" in task_type else REGRESSION if task_type in {"regression", "count_regression", "zero_inflated_count", "extreme_event_prediction"} else set()
        )
        if not required:
            return self.pass_()
        missing = sorted(metric for metric in required if metric not in metrics and f"{metric}_not_applicable_reason" not in metrics)
        if missing:
            return self.fail(missing, ["rerun_task_appropriate_metrics", "record_not_applicable_reason_for_unavailable_metrics"])
        return self.pass_()
