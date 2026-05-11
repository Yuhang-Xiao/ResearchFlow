---
name: metric-completeness-auditor
description: Check task-appropriate metrics and require not-applicable reasons for omitted metrics.
---

# metric-completeness-auditor

## Classification Metrics

Accuracy, Precision, Recall, F1, Macro-F1, Weighted-F1, Balanced Accuracy, MCC, ROC-AUC, PR-AUC, confusion matrix.

## Regression Metrics

MAE, RMSE, R2, RMSLE, MedianAE, residual analysis, extreme value error.

## Gate Rule

An omitted metric is acceptable only when `not_applicable_reason` is recorded. Silent omission fails the gate and triggers repair.

## Outputs

- `metric_completeness_audit.csv`
- `complete_metric_table.csv`
