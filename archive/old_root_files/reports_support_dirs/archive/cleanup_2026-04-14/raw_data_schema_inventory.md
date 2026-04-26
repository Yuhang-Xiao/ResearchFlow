# Raw Data Schema Inventory

Date: 2026-04-13

Scope: schema inventory only for files under `data/01_raw`. No cleaning, transformation, modeling, or downstream analysis was performed.

Skill used: `skills/data-schema-profiler`.

## File Inventory

| File | Type | Size | Sheets |
|---|---:|---:|---|
| `data/01_raw/MERGED_2023-01-01_to_2023-12-31__hege2__kwNONE__provinces1.xlsx` | Excel workbook | 901,805 bytes | `Sheet1` |

## Workbook: `MERGED_2023-01-01_to_2023-12-31__hege2__kwNONE__provinces1.xlsx`

| Sheet | Header row | Data rows | Columns |
|---|---:|---:|---:|
| `Sheet1` | 1 | 4,290 | 33 |

## Sheet `Sheet1` Columns

| Column | Inferred type | Non-null | Missing | Unique values | Notes |
|---|---:|---:|---:|---:|---|
| `序号` | integer | 4,290 | 0 | 639 | Not unique; not a row-level key. |
| `产品分类` | text | 4,290 | 0 | 119 | Product category. |
| `产品名称` | text | 4,290 | 0 | 1,241 | Product name. |
| `判定结果` | text | 4,290 | 0 | 1 | Target-like outcome column by name, but single observed value. |
| `不合格项目分类` | text | 4,278 | 12 | 40 | Quality issue category. |
| `不合格项目` | text | 4,290 | 0 | 318 | Quality issue item. |
| `不合格规范列` | text | 4,290 | 0 | 242 | Quality issue standard/specification text. |
| `检测数值` | mixed | 4,078 | 212 | 2,859 | Mixed integers, floats, and text. |
| `法规限制` | mixed | 3,078 | 1,212 | 317 | Mostly text with one integer-like value. |
| `规格型号` | text | 4,227 | 63 | 292 | Specification/model. |
| `商标` | text | 4,229 | 61 | 242 | Trademark/brand. |
| `生产日期` | text | 4,191 | 99 | 512 | Likely date/time field stored as text. |
| `生产企业名称` | text | 4,290 | 0 | 451 | Producer name. |
| `生产企业地址` | text | 4,290 | 0 | 435 | Producer address. |
| `生产省份` | text | 4,290 | 0 | 20 | Producer province. |
| `抽样单位名称` | text | 4,289 | 1 | 3,673 | High-cardinality sampling unit name; not unique. |
| `抽样单位地址` | text | 4,231 | 59 | 3,440 | High-cardinality sampling unit address; not unique. |
| `通报时间` | text | 4,290 | 0 | 109 | Likely date/time field stored as text. |
| `通报文号` | text | 4,290 | 0 | 104 | Notice/document number; not unique. |
| `通报单位` | text | 4,290 | 0 | 22 | Reporting unit. |
| `措施` | text | 1,723 | 2,567 | 61 | High missingness. |
| `伙伴网链接` | text | 679 | 3,611 | 32 | High missingness. |
| `来源链接` | text | 4,290 | 0 | 166 | Source URL; not unique. |
| `检验项目` | empty | 0 | 4,290 | 0 | Empty in this sheet. |
| `抽检级别` | text | 4,290 | 0 | 3 | Low-cardinality category. |
| `检验机构` | text | 2,336 | 1,954 | 81 | High missingness. |
| `标准` | text | 3,982 | 308 | 53 | Standard text. |
| `备注` | text | 280 | 4,010 | 160 | Very high missingness. |
| `Unnamed: 28` | empty | 0 | 4,290 | 0 | Unnamed empty column. |
| `Unnamed: 29` | empty | 0 | 4,290 | 0 | Unnamed empty column. |
| `抽样环节` | text | 4,290 | 0 | 3 | Low-cardinality category. |
| `是否网抽` | text | 2,252 | 2,038 | 1 | Binary-like by name, but only one observed non-null value. |
| `_export_file` | text | 4,290 | 0 | 109 | Provenance/source export marker. |

## Candidate Keys

No obvious row-level unique key was identified.

Key notes:

- `序号` is not unique: 639 unique values across 4,290 rows.
- High-cardinality fields such as `抽样单位名称`, `抽样单位地址`, and `检测数值` are not suitable standalone keys.
- A future cleaning or validation step should test composite keys, likely involving source/provenance, notice fields, product fields, production fields, and issue fields.

## Likely Date/Time Fields

- `生产日期`: likely production date; currently inferred as text.
- `通报时间`: likely notice/reporting time; currently inferred as text.
- `_export_file`: provenance field that may encode source/export timing, but it should not be treated as a date field until inspected.

## Likely Target Columns

- `判定结果`: most target-like column by name. However, it has only one observed value in this raw file, so it is not currently useful as a supervised modeling target without broader or differently scoped data.
- `是否网抽`: possible binary indicator by name, but it has one observed non-null value and many missing values. Treat as a feature or metadata candidate only after validation.

## Obvious Schema Risks

- No obvious unique row identifier.
- Date/time-like fields are stored as text and need parsing rules before analysis.
- `检测数值` mixes integers, floats, and text, which may require unit-aware parsing later.
- `法规限制` is mostly text but includes a numeric-looking value, indicating mixed representation.
- Entirely empty columns: `检验项目`, `Unnamed: 28`, `Unnamed: 29`.
- High-missingness columns: `备注`, `伙伴网链接`, `措施`, `是否网抽`, `检验机构`, and `法规限制`.
- Target-like column `判定结果` has only one observed class in this file.
- `Unnamed: 28` and `Unnamed: 29` suggest extra blank columns or export artifacts.

## Recommended Next Action

Define validation rules before cleaning. Start with checks for row identity, expected columns, date parsing for `生产日期` and `通报时间`, missingness thresholds, mixed-type handling for `检测数值` and `法规限制`, and whether `判定结果` is expected to contain more than one class in the intended dataset.
