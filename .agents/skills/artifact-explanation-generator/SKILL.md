---
name: artifact-explanation-generator
description: Generate explanation indexes for every output artifact, including purpose, source, method, reading guide, limitations, paper-use status, and artifact-to-evidence maps.
---

# artifact-explanation-generator

Use when a task produces or audits figures, tables, model outputs, code, reports, Word files, or literature artifacts.

## Required Inputs

- Latest run package from `outputs/_index/latest_canonical_outputs.yaml` or explicit task package.
- Source tables, charts, model artifacts, code snapshots, reports, and quality gate outputs.

## Required Outputs

- `artifact_explanation_index.md`
- `figure_explanations.md`
- `table_explanations.md`
- `model_output_explanations.md`
- `code_explanations.md`
- `result_interpretation_guide.md`
- `artifact_to_evidence_map.csv`

## Required Fields

Each artifact explanation must include:

- file path and type
- purpose
- input source
- generation method
- core fields or visual elements
- main result
- how to read it
- related paper section
- whether it supports Results / Method / Discussion
- formal conclusion status
- limitations
- manual attention needed

## Quality Rules

- Record missing or unreadable artifacts as `unable_to_verify`; do not invent content.
- Experimental outputs must stay experimental.
- Every claim-supporting artifact must map to source evidence.
- Explanations must be co-located with the result directory. `10_输出解释与索引/` is navigation only.
- Key artifacts should have same-name `.explanation.md` sidecars.
- Each result directory should have a README/local explanation that is useful without jumping to the total index.
