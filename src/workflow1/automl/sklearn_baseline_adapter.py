"""Local sklearn baseline adapter used even when external AutoML is unavailable."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import importlib.util
import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    mean_absolute_error,
    mean_squared_error,
    median_absolute_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from workflow1.automl.automl_adapter_base import AutoMLAdapter, AutoMLRunResult


class SklearnBaselineAdapter(AutoMLAdapter):
    adapter_name = "sklearn_baseline"
    optional_dependency = "scikit-learn"

    def is_available(self) -> bool:
        return True

    def fit_predict(
        self,
        df: pd.DataFrame,
        target_column: str,
        task_type: str,
        output_dir: str | Path | None = None,
        random_state: int = 42,
    ) -> AutoMLRunResult:
        y = df[target_column]
        x = df.drop(columns=[target_column])
        numeric = [c for c in x.columns if pd.api.types.is_numeric_dtype(x[c])]
        categorical = [c for c in x.columns if c not in numeric]
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
                ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
            ],
            remainder="drop",
        )
        classification = task_type in {"binary_classification", "multiclass_classification", "imbalanced_classification"}
        stratify = y if classification and y.nunique() > 1 and y.value_counts().min() >= 2 else None
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=random_state, stratify=stratify)
        if classification:
            baseline = Pipeline([("prep", preprocessor), ("model", DummyClassifier(strategy="most_frequent"))])
            model = Pipeline([("prep", preprocessor), ("model", LogisticRegression(max_iter=1000))])
            fallback = Pipeline([("prep", preprocessor), ("model", RandomForestClassifier(n_estimators=50, random_state=random_state))])
        else:
            baseline = Pipeline([("prep", preprocessor), ("model", DummyRegressor(strategy="median"))])
            model = Pipeline([("prep", preprocessor), ("model", Ridge())])
            fallback = Pipeline([("prep", preprocessor), ("model", RandomForestRegressor(n_estimators=50, random_state=random_state))])
        baseline.fit(x_train, y_train)
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        pred_proba = model.predict_proba(x_test) if classification and hasattr(model, "predict_proba") else None
        baseline_pred = baseline.predict(x_test)
        baseline_proba = baseline.predict_proba(x_test) if classification and hasattr(baseline, "predict_proba") else None
        metrics = (
            self._classification_metrics(y_test, pred, pred_proba)
            if classification
            else self._regression_metrics(y_test, pred)
        )
        baseline_metrics = {
            f"baseline_{k}": v
            for k, v in (
                self._classification_metrics(y_test, baseline_pred, baseline_proba)
                if classification
                else self._regression_metrics(y_test, baseline_pred)
            ).items()
            if not str(k).endswith("_not_applicable_reason")
        }
        metrics.update(baseline_metrics)
        output = Path(output_dir) if output_dir else None
        artifacts: dict[str, str] = {}
        if output:
            output.mkdir(parents=True, exist_ok=True)
            pd.DataFrame({"actual": y_test, "predicted": pred}).to_csv(output / "sklearn_baseline_predictions.csv", index=False, encoding="utf-8-sig")
            artifacts["predictions"] = str(output / "sklearn_baseline_predictions.csv")
            if classification:
                cm = confusion_matrix(y_test, pred)
                labels = sorted(pd.Series(y_test).dropna().unique())
                pd.DataFrame(cm, index=[f"actual_{x}" for x in labels], columns=[f"pred_{x}" for x in labels]).to_csv(
                    output / "confusion_matrix.csv", encoding="utf-8-sig"
                )
                artifacts["confusion_matrix"] = str(output / "confusion_matrix.csv")
            else:
                residuals = pd.Series(y_test).reset_index(drop=True) - pd.Series(pred).reset_index(drop=True)
                residual_df = pd.DataFrame(
                    {
                        "actual": list(y_test),
                        "predicted": list(pred),
                        "residual": residuals,
                        "absolute_error": residuals.abs(),
                    }
                )
                residual_df.to_csv(output / "residual_diagnostics.csv", index=False, encoding="utf-8-sig")
                residual_df.nlargest(max(1, min(10, len(residual_df))), "absolute_error").to_csv(
                    output / "extreme_error_cases.csv", index=False, encoding="utf-8-sig"
                )
                artifacts["residual_diagnostics"] = str(output / "residual_diagnostics.csv")
                artifacts["extreme_error_cases"] = str(output / "extreme_error_cases.csv")
            shap_artifacts = self._write_shap_or_fallback(
                model=model,
                x_train=x_train,
                x_test=x_test,
                output=output,
                classification=classification,
            )
            artifacts.update(shap_artifacts)
        return AutoMLRunResult(
            adapter_name=self.adapter_name,
            status="ok",
            task_type=task_type,
            metrics=metrics,
            model_summary=f"baseline=Dummy, primary={model.named_steps['model'].__class__.__name__}, fallback={fallback.named_steps['model'].__class__.__name__}",
            warnings=[],
            artifacts=artifacts,
        )

    def _classification_metrics(self, y_true: pd.Series, y_pred: Any, pred_proba: Any | None) -> dict[str, Any]:
        labels = sorted(pd.Series(y_true).dropna().unique())
        average = "binary" if len(labels) == 2 else "macro"
        pos_label = labels[-1] if len(labels) == 2 else 1
        metrics: dict[str, Any] = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, average=average, pos_label=pos_label, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, average=average, pos_label=pos_label, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, average=average, pos_label=pos_label, zero_division=0)),
            "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
            "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "mcc": float(matthews_corrcoef(y_true, y_pred)),
            "confusion_matrix": json.dumps(confusion_matrix(y_true, y_pred).tolist(), ensure_ascii=False),
        }
        if pred_proba is not None and len(labels) == 2:
            positive_scores = pred_proba[:, 1]
            metrics["roc_auc"] = float(roc_auc_score(y_true, positive_scores))
            metrics["pr_auc"] = float(average_precision_score(y_true, positive_scores, pos_label=pos_label))
        elif pred_proba is not None and len(labels) > 2:
            try:
                metrics["roc_auc"] = float(roc_auc_score(y_true, pred_proba, multi_class="ovr", average="macro"))
            except Exception as exc:
                metrics["roc_auc_not_applicable_reason"] = f"multiclass ROC-AUC unavailable: {exc}"
            metrics["pr_auc_not_applicable_reason"] = "PR-AUC is not part of the default multiclass metric contract."
        else:
            metrics["roc_auc_not_applicable_reason"] = "predict_proba unavailable for selected model."
            metrics["pr_auc_not_applicable_reason"] = "predict_proba unavailable for selected model."
        return metrics

    def _regression_metrics(self, y_true: pd.Series, y_pred: Any) -> dict[str, Any]:
        actual = np.asarray(y_true, dtype=float)
        predicted = np.asarray(y_pred, dtype=float)
        residual = actual - predicted
        absolute_error = np.abs(residual)
        metrics: dict[str, Any] = {
            "mae": float(mean_absolute_error(actual, predicted)),
            "rmse": float(mean_squared_error(actual, predicted) ** 0.5),
            "r2": float(r2_score(actual, predicted)),
            "median_ae": float(median_absolute_error(actual, predicted)),
            "residual_analysis": json.dumps(
                {
                    "residual_mean": float(np.mean(residual)),
                    "residual_std": float(np.std(residual)),
                    "mean_absolute_residual": float(np.mean(absolute_error)),
                },
                ensure_ascii=False,
            ),
            "extreme_value_error": float(np.mean(np.sort(absolute_error)[-max(1, int(np.ceil(len(absolute_error) * 0.1))):])),
        }
        if np.min(actual) >= 0 and np.min(predicted) >= 0:
            metrics["rmsle"] = float(mean_squared_error(np.log1p(actual), np.log1p(predicted)) ** 0.5)
        else:
            metrics["rmsle_not_applicable_reason"] = "RMSLE requires non-negative actual and predicted values."
        return metrics

    def _write_shap_or_fallback(
        self,
        model: Pipeline,
        x_train: pd.DataFrame,
        x_test: pd.DataFrame,
        output: Path,
        classification: bool,
    ) -> dict[str, str]:
        explain_dir = output / "explainability_outputs"
        explain_dir.mkdir(parents=True, exist_ok=True)
        audit_path = output / "shap_availability_audit.csv"
        decision_path = output / "shap_or_fallback_decision.csv"
        artifacts = {
            "shap_availability_audit": str(audit_path),
            "shap_or_fallback_decision": str(decision_path),
        }
        shap_available = importlib.util.find_spec("shap") is not None
        audit_row = {"tool": "shap", "available": shap_available, "model_compatible": False, "status": "not_run", "reason": ""}
        decision_row = {"method": "fallback", "status": "planned", "reason": "SHAP unavailable or incompatible"}
        if shap_available:
            try:
                import shap

                transformed_train = model.named_steps["prep"].transform(x_train)
                transformed_test = model.named_steps["prep"].transform(x_test)
                if hasattr(transformed_train, "toarray"):
                    transformed_train = transformed_train.toarray()
                if hasattr(transformed_test, "toarray"):
                    transformed_test = transformed_test.toarray()
                transformed_train = np.asarray(transformed_train, dtype=float)[:50]
                transformed_test = np.asarray(transformed_test, dtype=float)[:20]
                estimator = model.named_steps["model"]
                explainer = shap.Explainer(estimator, transformed_train)
                values = explainer(transformed_test)
                raw_values = np.asarray(values.values)
                if raw_values.ndim == 3:
                    importance = np.abs(raw_values).mean(axis=(0, 2))
                else:
                    importance = np.abs(raw_values).mean(axis=0)
                try:
                    feature_names = list(model.named_steps["prep"].get_feature_names_out())
                except Exception:
                    feature_names = [f"feature_{i}" for i in range(len(importance))]
                shap_df = pd.DataFrame({"feature": feature_names[: len(importance)], "mean_abs_shap": importance})
                shap_df.sort_values("mean_abs_shap", ascending=False).to_csv(
                    explain_dir / "shap_feature_importance.csv", index=False, encoding="utf-8-sig"
                )
                artifacts["shap_feature_importance"] = str(explain_dir / "shap_feature_importance.csv")
                audit_row.update({"model_compatible": True, "status": "ok", "reason": f"SHAP {shap.__version__} ran on transformed sklearn pipeline."})
                decision_row = {"method": "SHAP", "status": "ok", "reason": "SHAP installed and compatible with selected sklearn model."}
            except Exception as exc:
                audit_row.update({"status": "fallback", "reason": str(exc)})
                decision_row = {
                    "method": "fallback",
                    "status": "planned",
                    "reason": "SHAP installed but failed on selected model; use permutation importance/PDP/local explanation fallback.",
                }
        else:
            audit_row.update({"reason": "SHAP is not installed in the active Python environment."})
        pd.DataFrame([audit_row]).to_csv(audit_path, index=False, encoding="utf-8-sig")
        pd.DataFrame([decision_row]).to_csv(decision_path, index=False, encoding="utf-8-sig")
        (explain_dir / "README_解释输出.md").write_text(
            "# 解释输出\n\n"
            "本目录保存 SHAP 或替代解释产物。解释只支持 predictive association，不作为因果机制证明。\n",
            encoding="utf-8",
        )
        return artifacts
