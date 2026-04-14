# Raw Data Validation Proposal: FINAL_SiChuan_2023_ALL_DATA

Date: 2026-04-14

Scope: proposal only for validating the active raw dataset. This document does not apply cleaning rules, parse dates, create cleaned datasets, run formal analysis, or make modeling decisions.

Active raw dataset: `F:\DESK\workflow1\data\01_raw\FINAL_SiChuan_2023_ALL_DATA.xlsx`

Sheet names: `Sheet1`

## Proposed Validation Checks

| Check area | Proposed check | Reason | Expected output | Risk or assumption |
|---|---|---|---|---|
| File identity | Confirm the active input remains `FINAL_SiChuan_2023_ALL_DATA.xlsx`. | Prevent accidental reuse of older raw datasets. | Validation note confirming the active input path and file type. | Assumes the basename uniquely identifies the intended dataset. |
| Workbook structure | Confirm `Sheet1` exists and has one header row. | Prevent sheet-name or header-offset errors. | Sheet inventory with row and column counts. | Assumes row 1 is the intended header row. |
| Expected columns | Check the observed 33 source columns against the current inventory. | Detect accidental file version changes. | Pass/fail list of expected, missing, and extra columns. | Requires preserving original Chinese column names exactly. |
| Row identity | Check `序号` for completeness and uniqueness. | `序号` is the only standalone candidate key from the schema inventory. | Key validation summary with duplicate and missing counts. | Does not prove `序号` is semantically stable across future files. |
| Empty columns | Confirm `Unnamed: 28` and `Unnamed: 29` remain empty. | Identify export artifacts without dropping them. | Empty-column validation summary. | Dropping columns is not included and would require approval. |
| Date-like fields | Profile raw string formats in `生产日期` and `通报时间` without parsing. | Prepare for a future approval-gated date parsing decision. | Format-frequency summary and examples of unparsed raw formats. | No date parsing or coercion should occur in this validation step. |
| Mixed-type fields | Profile raw type categories for `检测数值` and `法规限制`. | These fields contain mixed numeric and text representations. | Raw type-count and representative-format summary. | No numeric conversion, unit parsing, or recoding should occur. |
| Missingness | Summarize missingness for all columns, with flags for high-missingness fields. | Identify structural missingness candidates and quality risks. | Missingness table by source column. | Missingness interpretation is not included. |
| Low-cardinality fields | Summarize unique counts for `判定结果`, `抽检级别`, `抽样环节`, and `是否网抽`. | Prepare for later validation of category values. | Category-count summary using original values. | Recoding or translating values is not included. |
| Provenance fields | Summarize completeness and uniqueness for `来源链接`, `伙伴网链接`, and `_export_file`. | Support traceability checks. | Provenance-field completeness and uniqueness summary. | Link validation or web access is not included. |

## Auto-Allowed Scope

The validation step may produce lightweight technical summaries only:

- File and sheet validation summary.
- Expected-column check summary.
- Candidate-key validation summary for `序号`.
- Missingness summary.
- Raw format summaries for `生产日期`, `通报时间`, `检测数值`, and `法规限制`.
- Category-count summaries using original source values.

## Explicitly Out of Scope Until Approval

- Applying cleaning rules.
- Dropping `Unnamed: 28`, `Unnamed: 29`, or any other columns.
- Parsing `生产日期` or `通报时间`.
- Converting `检测数值` or `法规限制`.
- Imputing missing values.
- Recoding `判定结果`, `抽检级别`, `抽样环节`, or `是否网抽`.
- Creating cleaned analysis-ready datasets.
- Running formal EDA, statistical analysis, or modeling.
- Interpreting results or drafting a research report.

## First Approval-Required Step After Review

After this proposal is reviewed, the first approval-required step will be any decision to apply validation-driven changes, such as date parsing, type conversion, column dropping, recoding, imputation, deduplication, or creation of a cleaned analysis-ready dataset.
