"""Method scouting for publication-grade research products.

The scout builds a candidate-method matrix from task structure, registry hints,
local dependency availability, and external workflow lessons. It does not run
third-party code or install dependencies.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.util
from typing import Iterable


@dataclass
class MethodCandidate:
    model_family: str
    candidate_method: str
    role: str
    task_fit: str
    minimum_data_condition: str
    optional_dependencies: str
    dependency_status: str
    literature_topics: str
    engineering_reference: str
    validation_requirement: str
    explanation_requirement: str
    common_failure_modes: str
    training_decision: str
    not_trained_reason: str
    eligible_for_main_claim: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _available(package: str) -> bool:
    return importlib.util.find_spec(package) is not None


def dependency_status(dependencies: Iterable[str]) -> str:
    deps = [d for d in dependencies if d]
    if not deps:
        return "available:standard_or_sklearn"
    missing = [dep for dep in deps if not _available(dep)]
    if missing:
        return "missing:" + ";".join(missing)
    return "available:" + ";".join(deps)


def _candidate(
    model_family: str,
    candidate_method: str,
    role: str,
    task_fit: str,
    minimum_data_condition: str,
    dependencies: list[str],
    literature_topics: list[str],
    engineering_reference: str,
    validation_requirement: str,
    explanation_requirement: str,
    common_failure_modes: list[str],
    training_decision: str,
    not_trained_reason: str = "",
    eligible_for_main_claim: str = "yes_if_quality_gates_pass",
) -> MethodCandidate:
    return MethodCandidate(
        model_family=model_family,
        candidate_method=candidate_method,
        role=role,
        task_fit=task_fit,
        minimum_data_condition=minimum_data_condition,
        optional_dependencies=";".join(dependencies) or "none",
        dependency_status=dependency_status(dependencies),
        literature_topics=";".join(literature_topics),
        engineering_reference=engineering_reference,
        validation_requirement=validation_requirement,
        explanation_requirement=explanation_requirement,
        common_failure_modes=";".join(common_failure_modes),
        training_decision=training_decision,
        not_trained_reason=not_trained_reason,
        eligible_for_main_claim=eligible_for_main_claim,
    )


def scout_methods(task_signals: dict[str, object]) -> list[dict[str, str]]:
    """Return a publication-oriented method candidate matrix.

    Parameters in ``task_signals`` are intentionally simple so callers can build
    them from any dataset profiler: ``is_time_ordered``, ``is_count_like``,
    ``zero_rate``, ``has_groups``, ``has_location``, ``n_rows``.
    """

    is_time = bool(task_signals.get("is_time_ordered"))
    is_count = bool(task_signals.get("is_count_like"))
    zero_rate = float(task_signals.get("zero_rate") or 0.0)
    has_groups = bool(task_signals.get("has_groups"))
    has_location = bool(task_signals.get("has_location"))
    n_rows = int(task_signals.get("n_rows") or 0)
    enough_sequence = is_time and n_rows >= 500

    candidates: list[MethodCandidate] = [
        _candidate(
            "simple_baseline",
            "DummyMedian / seasonal naive / rolling mean",
            "baseline",
            "Minimum comparator for regression, count, and forecasting tasks.",
            "Target column available; time index required for seasonal naive.",
            [],
            ["baseline forecasting", "model comparison"],
            "scikit-learn DummyRegressor; forecasting textbook patterns",
            "Same chronological or grouped split as all advanced models.",
            "Report baseline residuals and error distribution.",
            ["baseline omitted", "unfair split"],
            "train",
        ),
        _candidate(
            "generalized_linear_model",
            "Ridge/ElasticNet and Poisson/Tweedie GLM",
            "interpretable_control",
            "Transparent control for numeric and count-like targets.",
            "Sufficient numeric/categorical features after encoding.",
            ["sklearn"],
            ["generalized linear models", "count regression"],
            "scikit-learn linear_model",
            "Chronological/group-aware split; inspect overdispersion.",
            "Coefficients or permutation importance.",
            ["misspecified link", "overdispersion", "zero inflation"],
            "train",
        ),
        _candidate(
            "zero_inflated_or_two_part",
            "Two-stage zero/positive model",
            "task_specific",
            "Required candidate when the target has substantial zeros.",
            "Zero rate above 0.2 and enough positive cases.",
            ["sklearn"],
            ["zero-inflated models", "hurdle models"],
            "workflow1 local two-stage pattern",
            "Evaluate zero-vs-positive and positive-value errors separately.",
            "Feature importance for classifier and regressor parts.",
            ["error propagation", "rare positive instability"],
            "train" if zero_rate >= 0.2 else "not_applicable",
            "" if zero_rate >= 0.2 else "Target is not materially zero-inflated.",
        ),
        _candidate(
            "tree_ensemble",
            "RandomForest / ExtraTrees",
            "modern_ml",
            "Robust nonlinear tabular baseline for mixed feature types.",
            "Enough rows for chronological or grouped holdout.",
            ["sklearn"],
            ["ensemble learning", "tabular machine learning"],
            "scikit-learn ensemble",
            "Same split as baselines; compare to interpretable controls.",
            "Permutation importance and residual subgroup analysis.",
            ["leakage through lag features", "poor extrapolation"],
            "train",
        ),
        _candidate(
            "gradient_boosting",
            "HistGradientBoosting / Poisson-style boosting",
            "modern_ml",
            "Strong tabular candidate for nonlinear and count-like prediction.",
            "Enough rows and no invalid leakage features in ex-ante setting.",
            ["sklearn"],
            ["gradient boosting", "Poisson regression for counts"],
            "scikit-learn HistGradientBoosting",
            "Chronological/group-aware split; compare log/Poisson variants.",
            "SHAP if compatible; otherwise permutation importance.",
            ["tail underprediction", "calibration drift"],
            "train",
        ),
    ]

    if is_time:
        candidates.extend(
            [
                _candidate(
                    "classical_forecasting",
                    "ARIMA/SARIMAX/state-space",
                    "task_specific",
                    "Classical time-series comparator for ordered weekly data.",
                    "Regular time index; preferably one series or clean panel aggregation.",
                    ["statsmodels"],
                    ["forecasting backtesting", "state space models"],
                    "statsmodels SARIMAX",
                    "Rolling-origin backtest; no random split.",
                    "Forecast residuals and seasonal components.",
                    ["irregular panel", "missing weeks", "dependency missing"],
                    "dependency_approval_or_fallback",
                    "statsmodels is not currently installed in the controlled environment.",
                    "no_until_dependency_available",
                ),
                _candidate(
                    "machine_learning_forecaster",
                    "GBDT with lag/rolling features",
                    "task_specific",
                    "Strong supervised forecaster when panel time order is available.",
                    "Lag features can be constructed without future leakage.",
                    ["sklearn"],
                    ["machine learning forecasting", "rolling-origin validation"],
                    "sklearn pipeline with lag features",
                    "Rolling-origin or time-external split.",
                    "Permutation importance; lag feature sensitivity.",
                    ["future leakage", "lag unavailable at deployment"],
                    "train",
                ),
                _candidate(
                    "deep_sequence",
                    "Automatically scouted GRU/LSTM/TCN/Transformer-style sequence baseline",
                    "optional_advanced_candidate",
                    "Sequence candidate for panel/weekly tasks; selected from task structure, not user request.",
                    "At least 500 rows, ordered time index, sequence window available.",
                    ["torch"],
                    ["deep sequence forecasting", "temporal neural networks"],
                    "PyTorch local implementation only; no unknown third-party code",
                    "Chronological split; compare to seasonal naive and GBDT-lag.",
                    "Ablation, residual analysis, and no causal interpretation.",
                    ["overfitting", "small data", "unstable training", "weak interpretability"],
                    "train" if enough_sequence and _available("torch") else "not_trained",
                    "" if enough_sequence and _available("torch") else "Torch unavailable or sequence conditions not met.",
                    "yes_if_outperforms_baselines_and_documented",
                ),
                _candidate(
                    "automated_forecasting",
                    "Prophet / NeuralProphet / AutoML forecasting",
                    "optional_external_candidate",
                    "External forecasting benchmark when dependencies and license are approved.",
                    "Regular time index and approved installation.",
                    ["prophet"],
                    ["automated forecasting", "additive time-series models"],
                    "Prophet official package",
                    "Rolling-origin backtest.",
                    "Trend/seasonality components.",
                    ["dependency missing", "model not fit for irregular panel"],
                    "dependency_approval_or_fallback",
                    "Prophet is not installed; large/optional dependency requires approval.",
                    "no_until_dependency_available",
                ),
            ]
        )

    if has_groups or has_location:
        candidates.append(
            _candidate(
                "grouped_or_spatial_validation",
                "Leave-location/group-out validation and hierarchical/mixed-effects candidate",
                "validation_and_generalization",
                "Required when observations are grouped by location or source.",
                "At least two groups and sufficient rows per group.",
                ["sklearn"],
                ["grouped validation", "spatial generalization"],
                "GroupKFold / leave-group-out patterns",
                "Group-aware split reported separately from random or chronological split.",
                "Group error plots and subgroup residuals.",
                ["group leakage", "unseen group failure"],
                "train_or_evaluate",
            )
        )

    if is_count:
        candidates.append(
            _candidate(
                "tail_or_extreme_model",
                "Quantile / top-k risk-ranking / extreme-error audit",
                "risk_and_tail_candidate",
                "Count targets often have long tails where average metrics hide warning failures.",
                "Positive tail cases available.",
                ["sklearn"],
                ["extreme event prediction", "quantile loss"],
                "scikit-learn quantile losses where available",
                "Report tail metrics and extreme-case table.",
                "Extreme-case explanations and residual diagnostics.",
                ["rare tail instability", "threshold arbitrariness"],
                "train_or_audit",
            )
        )

    return [candidate.to_dict() for candidate in candidates]


def external_workflow_lessons() -> list[dict[str, str]]:
    """Curated read-only lessons from mature automated-research workflows."""

    return [
        {
            "source": "data-to-paper",
            "url": "https://github.com/Technion-Kishony-lab/data-to-paper",
            "lesson": "Every paper claim should be backward-traceable to code, data, and generated artifacts.",
            "workflow1_adaptation": "Generate claim_to_citation_map.csv, artifact_to_evidence_map.csv, and source-data sidecars.",
        },
        {
            "source": "The AI Scientist",
            "url": "https://arxiv.org/abs/2408.06292",
            "lesson": "Automated research needs idea/method generation, experiments, visualization, paper writing, and review loops.",
            "workflow1_adaptation": "Add method_scout, figure density gates, LaTeX exporter, and reviewer-style rejection-risk gate.",
        },
        {
            "source": "Agent Laboratory",
            "url": "https://arxiv.org/abs/2501.04227",
            "lesson": "Literature review, experimentation, and report writing should be staged, with human review improving final quality.",
            "workflow1_adaptation": "Separate literature-first evidence selection, experiment cards, and target-journal/domain-review limits.",
        },
    ]
