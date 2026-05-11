# Baseline Trainer

## When To Use

Use this skill after the ML problem has been framed, model input data exists, and evaluation metrics and data splits are defined or can be reasonably inferred from the research objective.

## Inputs

- Model input dataset from `data/05_model_input`.
- Target definition.
- Feature list.
- Split strategy.
- Evaluation metric.

## Outputs

- Baseline model artifact or reproducible training script.
- Evaluation metrics.
- Comparison-ready predictions or summaries.
- Notes on limitations and follow-up candidates.

## Recommended Workflow

1. Confirm that target, features, splits, and metrics are defined.
2. Check for leakage and invalid rows before training.
3. Train the simplest credible baseline first.
4. Evaluate on the selected split.
5. Compare against simple heuristics where useful.
6. Save experiment outputs under `experiments/baselines`.
7. Continue to tuning, comparison, or model revision if baseline performance is poor and the objective is clear.
8. Record results, assumptions, and next recommendations in project state.
