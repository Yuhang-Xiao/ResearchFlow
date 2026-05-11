---
name: code-explanation-auditor
description: Audit and explain scripts with purpose, inputs, outputs, dependencies, core functions, process, method logic, run command, errors, reproducibility, and paper relation.
---

# code-explanation-auditor

Use when generated or historical code must be made understandable and reproducible.

## Required Outputs

- `code_inventory.csv`
- `code_explanations.md`
- `code_method_explanation_report.md`

## Per-Script Fields

- script purpose
- input files
- output files
- dependency libraries
- core functions
- main workflow
- model/statistical logic
- how to run
- common errors
- relation to paper/results
- reproducibility status
- human confirmation needed

## Quality Rules

- Do not recommend running historical scripts that may overwrite outputs unless explicitly safe.
- Scripts that affect formal model parameters require user confirmation.
- For model code, explain model logic and function-level responsibilities, not only filenames.
- For DQN/RL code, map code to state, action, reward, constraint, transition/belief assumptions, training, baseline, evaluation, outputs, Method, and Results.
- Generate code-to-model-setting and code-to-output maps when code supports paper or model results.
