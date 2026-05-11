"""Write reproducible model-setting detail artifacts for manuscripts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


MODEL_DEFAULTS = {
    "DummyMedian": ("baseline", "median response baseline", "none", "reference baseline; no tunable hyperparameters"),
    "RidgeLogTarget": ("interpretable_control", "weather/calendar/location features", "log1p target", "alpha=1.0 unless tuned"),
    "PoissonRegressor": ("count_glm", "non-negative numeric and encoded categorical features", "raw count-like target", "alpha, max_iter"),
    "TweedieRegressor": ("count_glm", "non-negative numeric and encoded categorical features", "raw non-negative target", "power, alpha, link"),
    "RandomForestLogTarget": ("modern_ml", "encoded tabular features", "log1p target", "n_estimators, max_depth, min_samples_leaf"),
    "ExtraTreesLogTarget": ("modern_ml", "encoded tabular features", "log1p target", "n_estimators, max_features, min_samples_leaf"),
    "HistGradientBoostingLogTarget": ("modern_ml", "encoded tabular features", "log1p target", "learning_rate, max_iter, max_leaf_nodes"),
    "TwoStageZeroPositive": ("task_specific", "zero indicator model plus positive-value regressor", "hurdle/positive target", "classifier/regressor settings"),
    "LSTMSequence": ("sequence_candidate", "ordered windows with weather/calendar/location context", "scaled sequence target", "sequence_length, hidden_size, epochs"),
}


def _model_name(row: pd.Series) -> str:
    for key in ["model", "candidate", "Candidate"]:
        if key in row and pd.notna(row[key]):
            return str(row[key])
    return "candidate_model"


def _scenario_features(scenario: str) -> str:
    if "autoregressive" in scenario or "nowcasting" in scenario:
        return "weather, calendar, location, entity identity, lagged target value, rolling target history"
    if "weather_calendar_only" in scenario:
        return "weather and calendar features only"
    return "weather, calendar, location, and pest identity features available before target week"


def write_model_setting_details(
    *,
    run_dir: str | Path,
    candidate_matrix: pd.DataFrame,
    metrics: pd.DataFrame,
    primary_model: dict[str, Any],
) -> dict[str, Path]:
    package = Path(run_dir)
    model_dir = next((p for p in package.iterdir() if p.is_dir() and p.name.startswith("03_")), package / "03_模型实验")
    model_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    candidate_names = {_model_name(row) for _, row in candidate_matrix.iterrows()} if not candidate_matrix.empty else set()
    if not metrics.empty and "model" in metrics.columns:
        candidate_names.update(str(v) for v in metrics["model"].dropna().unique())
    if not candidate_names and primary_model.get("model"):
        candidate_names.add(str(primary_model["model"]))

    metrics_by_model = {str(row.get("model")): row for _, row in metrics.iterrows()} if not metrics.empty and "model" in metrics.columns else {}
    for name in sorted(candidate_names):
        role, features, transform, hyper = MODEL_DEFAULTS.get(
            name,
            ("candidate", "task-appropriate features listed in the candidate matrix", "recorded in modeling pipeline", "recorded if trained; otherwise dependency approval required"),
        )
        metric_row = metrics_by_model.get(name)
        scenario = str(metric_row.get("scenario", "not_trained_or_recorded")) if metric_row is not None else "not_trained_or_recorded"
        rows.append(
            {
                "model": name,
                "task_role": role,
                "applicability_reason": "Included because the target structure and validation setting make this family scientifically plausible.",
                "literature_basis": "model_method_literature_map / references.bib",
                "input_features": _scenario_features(scenario) if scenario != "not_trained_or_recorded" else features,
                "target_transformation": transform,
                "hyperparameters_or_search_space": hyper,
                "validation_strategy": "time holdout with multi-metric regression diagnostics",
                "training_status": str(metric_row.get("status", "candidate_only")) if metric_row is not None else "candidate_only",
                "failure_or_nontraining_reason": "" if metric_row is not None else "not trained in the controlled lightweight run or awaiting dependency approval",
                "eligible_for_main_conclusion": "yes" if name == str(primary_model.get("model")) else "no",
            }
        )
    detail = pd.DataFrame(rows)
    detail_path = model_dir / "model_setting_detail_table.csv"
    detail.to_csv(detail_path, index=False, encoding="utf-8-sig")

    audit_rows = []
    required = [
        "model",
        "task_role",
        "input_features",
        "target_transformation",
        "hyperparameters_or_search_space",
        "validation_strategy",
        "training_status",
    ]
    for _, row in detail.iterrows():
        missing = [col for col in required if not str(row.get(col, "")).strip()]
        audit_rows.append({"model": row["model"], "missing_fields": "; ".join(missing), "status": "pass" if not missing else "fail"})
    audit_path = model_dir / "model_setting_detail_audit.csv"
    pd.DataFrame(audit_rows).to_csv(audit_path, index=False, encoding="utf-8-sig")

    rationale_path = model_dir / "model_family_rationale.md"
    rationale_path.write_text(
        """# Model Family Rationale

The model set is selected from the inferred task structure rather than from a user-specified algorithm. A complete publication workflow must include transparent baselines, count-aware or distribution-aware controls, flexible nonlinear machine-learning candidates, and time-aware or sequence candidates when the data have temporal structure. The primary model is chosen only after multi-metric validation and pathological-model filtering; algorithm prestige alone is not evidence.
""",
        encoding="utf-8",
    )
    return {"detail": detail_path, "audit": audit_path, "rationale": rationale_path}
