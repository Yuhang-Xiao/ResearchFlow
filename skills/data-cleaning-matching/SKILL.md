# Data Cleaning and Matching

## When To Use

Use this skill when preparing raw or intermediate data for validation, EDA, feature engineering, or modeling.

## Inputs

- Source files or intermediate tables.
- Schema profiling notes.
- Cleaning rules or expected formats.
- Matching keys, blocking rules, or join requirements.

## Outputs

- Cleaned or matched dataset in the appropriate `data` layer.
- Cleaning rule summary.
- Matching diagnostics, such as unmatched records and duplicate keys.
- Validation recommendations.

## Recommended Workflow

1. Preserve raw inputs unchanged.
2. Define cleaning rules before applying them.
3. Normalize types, names, dates, categories, and identifiers.
4. Check key uniqueness before joins or matching.
5. Track unmatched, ambiguous, and duplicate records.
6. Write outputs to `data/02_intermediate` or `data/03_primary`.
7. Update project state with assumptions and next steps.
