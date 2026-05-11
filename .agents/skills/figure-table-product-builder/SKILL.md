---
name: figure-table-product-builder
description: Build paper-grade figures/tables with source data, captions, QA, explanations, and paper-use status.
---

# figure-table-product-builder

## Required Products

Create the figure/table set implied by the task: target distribution, time/group patterns, missingness, feature associations, model comparison, observed-vs-predicted, residuals, confusion/ROC/PR when applicable, SHAP/fallback explanations, robustness, literature map, model settings, complete metrics, and appendix tables.

## Gate Rules

- Main figures are PNG-first and nonblank.
- Chinese labels must render or fallback font status must be recorded.
- Every figure/table has source data, caption, explanation, and paper body reference.
- Failed chart/table QA triggers repair.
