# Raw Data Schema Inventory: FINAL_SiChuan_2023_ALL_DATA

Date: 2026-04-14

Scope: schema inventory only for the active raw dataset. Previous raw datasets and previous dataset-specific technical conclusions are ignored unless explicitly reused. No cleaning, transformation, date parsing, formal analysis, or modeling was performed.

Skill used: `skills/data-schema-profiler`.

## Confirmed Active Raw Dataset

| Attribute | Value |
|---|---|
| Exact file path | `F:\DESK\workflow1\data\01_raw\FINAL_SiChuan_2023_ALL_DATA.xlsx` |
| Relative file path | `data/01_raw/FINAL_SiChuan_2023_ALL_DATA.xlsx` |
| File type | Excel workbook (`.xlsx`) |
| File size | 17,081,452 bytes |
| Active sheet names | `Sheet1` |

## Workbook Structure

| Sheet | Header row | Data rows | Columns |
|---|---:|---:|---:|
| `Sheet1` | 1 | 102,130 | 33 |

## Sheet `Sheet1` Columns

| Column | Inferred type | Non-null | Missing | Unique values | Notes |
|---|---:|---:|---:|---:|---|
| `序号` | integer | 102,130 | 0 | 102,130 | Candidate row-level key; unique and complete in this raw file. |
| `产品分类` | text | 102,130 | 0 | 215 | Product category. |
| `产品名称` | text | 102,130 | 0 | 28,466 | Product name; high-cardinality text field. |
| `判定结果` | text | 102,130 | 0 | 2 | Target-like outcome field by name; requires user confirmation before modeling use. |
| `不合格项目分类` | text | 4,245 | 97,885 | 40 | High missingness; likely populated mainly for failed or issue records. |
| `不合格项目` | text | 4,257 | 97,873 | 318 | High missingness; likely populated mainly for failed or issue records. |
| `不合格规范列` | text | 4,391 | 97,739 | 243 | High missingness; likely populated mainly for failed or issue records. |
| `检测数值` | mixed | 4,045 | 98,085 | 2,859 | Mixed float, integer, and text values; high missingness. |
| `法规限制` | mixed | 3,045 | 99,085 | 317 | Mostly text with one integer value; high missingness. |
| `规格型号` | text | 100,964 | 1,166 | 5,416 | Specification/model text. |
| `商标` | text | 39,246 | 62,884 | 1,075 | Brand/trademark; high missingness. |
| `生产日期` | text | 99,705 | 2,425 | 1,437 | Likely date/time field by name; not parsed. |
| `生产企业名称` | text | 102,096 | 34 | 18,115 | Producer name. |
| `生产企业地址` | text | 102,052 | 78 | 18,931 | Producer address. |
| `生产省份` | text | 102,130 | 0 | 33 | Producer province. |
| `抽样单位名称` | text | 102,121 | 9 | 36,033 | Sampling unit name; high-cardinality text field. |
| `抽样单位地址` | text | 83,248 | 18,882 | 6,255 | Sampling unit address. |
| `通报时间` | text | 102,130 | 0 | 127 | Likely date/time field by name; not parsed. |
| `通报文号` | text | 102,130 | 0 | 159 | Notice/document number; not unique. |
| `通报单位` | text | 102,130 | 0 | 39 | Reporting unit. |
| `措施` | text | 1,720 | 100,410 | 61 | Very high missingness. |
| `伙伴网链接` | text | 31,625 | 70,505 | 38 | High missingness; source/reference link. |
| `来源链接` | text | 102,130 | 0 | 247 | Source link; not unique. |
| `检验项目` | text | 266 | 101,864 | 59 | Very high missingness. |
| `抽检级别` | text | 102,130 | 0 | 3 | Low-cardinality category. |
| `检验机构` | text | 67,072 | 35,058 | 119 | Inspection agency; moderate missingness. |
| `标准` | text | 3,952 | 98,178 | 53 | High missingness. |
| `备注` | text | 693 | 101,437 | 211 | Very high missingness. |
| `Unnamed: 28` | empty | 0 | 102,130 | 0 | Empty unnamed column. |
| `Unnamed: 29` | empty | 0 | 102,130 | 0 | Empty unnamed column. |
| `抽样环节` | text | 102,130 | 0 | 3 | Low-cardinality category. |
| `是否网抽` | text | 52,878 | 49,252 | 2 | Binary-like indicator by name; not recoded. |
| `_export_file` | text | 102,130 | 0 | 6,662 | Source export/provenance marker. |

## Candidate Keys

- `序号` is the only standalone candidate row-level key identified in this raw file: 102,130 non-null values and 102,130 unique values.
- No composite key was tested or selected.
- Fields such as `通报文号`, `来源链接`, and `_export_file` may be useful for provenance or grouping, but they are not unique standalone row keys.

## Likely Date/Time Fields

- `生产日期`: likely production date field by name; stored as text and not parsed.
- `通报时间`: likely reporting/notice time field by name; stored as text and not parsed.

## Likely Target Columns

- `判定结果`: target-like outcome field by name with 2 unique values. This is only a candidate; any use as a modeling target requires an approval-gated model-framing decision.
- `是否网抽`: binary-like indicator by name with 2 observed non-null values. Treat as a candidate metadata or feature field only after validation; do not recode without approval.

## Obvious Schema Risks

- Date/time-like fields `生产日期` and `通报时间` are stored as text; date parsing would be an approval-required step.
- Mixed-type fields: `检测数值` and `法规限制`.
- Empty columns: `Unnamed: 28` and `Unnamed: 29`.
- High-missingness columns include `不合格项目分类`, `不合格项目`, `不合格规范列`, `检测数值`, `法规限制`, `商标`, `措施`, `伙伴网链接`, `检验项目`, `标准`, and `备注`.
- Several issue-related fields appear sparsely populated; interpretation should not proceed until validation confirms whether missingness is structural.
- `判定结果` appears target-like, but no model framing decision has been made.
