# Data Schema Profiler

## When To Use

Use this skill when new data files are added, when a dataset needs inventorying, or before cleaning, matching, validation, EDA, or modeling.

## Inputs

- File paths or folder paths, usually under `data/01_raw`.
- Optional data dictionary or metadata.
- Optional expected schema.

## Outputs

- File inventory.
- Column names and inferred types.
- Missingness summary.
- Key candidate notes.
- Schema risks and validation recommendations.

## Recommended Workflow

1. Inventory files without modifying them.
2. Inspect metadata, headers, row counts, and sample records before loading full files.
3. Identify candidate keys, date fields, categorical fields, numeric fields, and free-text fields.
4. Compare observed schema to any expected schema.
5. Save reusable schema notes under `src/workflow1/schemas` or a report artifact when requested.
6. Update `project_state/next_step.md` with the recommended follow-up.
