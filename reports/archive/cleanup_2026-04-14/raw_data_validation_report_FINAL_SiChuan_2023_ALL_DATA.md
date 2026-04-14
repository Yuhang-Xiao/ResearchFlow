# 原始数据 Validation Report：FINAL_SiChuan_2023_ALL_DATA

日期：2026-04-14

范围：基于既有 validation proposal 对 active raw dataset 执行 read-only raw data validation audit。本报告只记录验证发现；未执行 cleaning、transformation、date parsing、type conversion、column dropping、deduplication、recoding、imputation、formal analysis 或 modeling。

Active raw dataset：`F:\DESK\workflow1\data\01_raw\FINAL_SiChuan_2023_ALL_DATA.xlsx`

输出汇总表：`reports/tables/raw_data_validation_summary_FINAL_SiChuan_2023_ALL_DATA.csv`

## 验证结论概览

- 文件身份验证通过：active input 为 `FINAL_SiChuan_2023_ALL_DATA.xlsx`，文件类型为 Excel workbook (`.xlsx`)，大小为 17,081,452 bytes。
- Workbook 结构验证通过：sheet names 为 `Sheet1`；`Sheet1` 的 header row 为 1，data rows 为 102,130，columns 为 33。
- Expected columns 验证通过：观察到的 33 个字段与当前 inventory 一致，未发现 missing expected columns 或 extra columns，字段顺序一致。
- Row identity 验证通过：`序号` 完整且唯一，non-null=102,130，missing=0，unique=102,130，duplicate_count=0。
- Empty columns 验证通过：`Unnamed: 28` 与 `Unnamed: 29` 均为全空字段。
- Date-like fields 需要后续审批决策：`生产日期` 与 `通报时间` 仍仅做 raw string format profiling，未进行 parsing。
- Mixed-type fields 需要后续审批决策：`检测数值` 与 `法规限制` 存在 mixed type 表现，未进行 type conversion。
- High-missingness fields 需要后续审批决策：`不合格项目分类`, `不合格项目`, `不合格规范列`, `检测数值`, `法规限制`, `商标`, `措施`, `伙伴网链接`, `检验项目`, `标准`, `备注`, `Unnamed: 28`, `Unnamed: 29`。

## 字段级 Validation Summary

| 字段名 | Non-null | Missing | Missing rate | Unique values | Python raw type counts |
|---|---:|---:|---:|---:|---|
| `序号` | 102,130 | 0 | 0.00% | 102,130 | {'int': 102130} |
| `产品分类` | 102,130 | 0 | 0.00% | 215 | {'str': 102130} |
| `产品名称` | 102,130 | 0 | 0.00% | 28,466 | {'str': 102130} |
| `判定结果` | 102,130 | 0 | 0.00% | 2 | {'str': 102130} |
| `不合格项目分类` | 4,245 | 97,885 | 95.84% | 40 | {'str': 4245} |
| `不合格项目` | 4,257 | 97,873 | 95.83% | 318 | {'str': 4257} |
| `不合格规范列` | 4,391 | 97,739 | 95.70% | 243 | {'str': 4391} |
| `检测数值` | 4,045 | 98,085 | 96.04% | 2,859 | {'float': 140, 'str': 3876, 'int': 29} |
| `法规限制` | 3,045 | 99,085 | 97.02% | 317 | {'str': 3044, 'int': 1} |
| `规格型号` | 100,964 | 1,166 | 1.14% | 5,416 | {'str': 100964} |
| `商标` | 39,246 | 62,884 | 61.57% | 1,075 | {'str': 39246} |
| `生产日期` | 99,705 | 2,425 | 2.37% | 1,437 | {'str': 99705} |
| `生产企业名称` | 102,096 | 34 | 0.03% | 18,115 | {'str': 102096} |
| `生产企业地址` | 102,052 | 78 | 0.08% | 18,931 | {'str': 102052} |
| `生产省份` | 102,130 | 0 | 0.00% | 33 | {'str': 102130} |
| `抽样单位名称` | 102,121 | 9 | 0.01% | 36,033 | {'str': 102121} |
| `抽样单位地址` | 83,248 | 18,882 | 18.49% | 6,255 | {'str': 83248} |
| `通报时间` | 102,130 | 0 | 0.00% | 127 | {'str': 102130} |
| `通报文号` | 102,130 | 0 | 0.00% | 159 | {'str': 102130} |
| `通报单位` | 102,130 | 0 | 0.00% | 39 | {'str': 102130} |
| `措施` | 1,720 | 100,410 | 98.32% | 61 | {'str': 1720} |
| `伙伴网链接` | 31,625 | 70,505 | 69.03% | 38 | {'str': 31625} |
| `来源链接` | 102,130 | 0 | 0.00% | 247 | {'str': 102130} |
| `检验项目` | 266 | 101,864 | 99.74% | 59 | {'str': 266} |
| `抽检级别` | 102,130 | 0 | 0.00% | 3 | {'str': 102130} |
| `检验机构` | 67,072 | 35,058 | 34.33% | 119 | {'str': 67072} |
| `标准` | 3,952 | 98,178 | 96.13% | 53 | {'str': 3952} |
| `备注` | 693 | 101,437 | 99.32% | 211 | {'str': 693} |
| `Unnamed: 28` | 0 | 102,130 | 100.00% | 0 | {} |
| `Unnamed: 29` | 0 | 102,130 | 100.00% | 0 | {} |
| `抽样环节` | 102,130 | 0 | 0.00% | 3 | {'str': 102130} |
| `是否网抽` | 52,878 | 49,252 | 48.22% | 2 | {'str': 52878} |
| `_export_file` | 102,130 | 0 | 0.00% | 6,662 | {'str': 102130} |

## 文件与结构检查

| 检查项 | 结果 |
|---|---|
| 文件路径 | `F:\DESK\workflow1\data\01_raw\FINAL_SiChuan_2023_ALL_DATA.xlsx` |
| 文件类型 | Excel workbook (`.xlsx`) |
| Sheet names | `['Sheet1']` |
| `Sheet1` rows | 102,130 data rows |
| `Sheet1` columns | 33 columns |
| Header row | 1 |
| Expected columns | PASS；33 个字段完全匹配当前 inventory |

## Row Identity 检查

`序号` 是当前唯一 standalone candidate key，验证结果为 PASS：字段完整、唯一，未发现 duplicate values。此发现只说明当前 raw file 中 `序号` 可作为候选 row identifier；如果要据此执行 deduplication、merge key 设计或下游 cleaned dataset 规则，仍需要用户审批。

## Empty Columns 检查

- `Unnamed: 28`：non-null=0，missing=102,130。
- `Unnamed: 29`：non-null=0，missing=102,130。

这两个字段看起来像 export artifacts，但删除字段属于 approval-required action，本次没有执行。

## Date-like Raw Format Profile

未进行 date parsing；以下仅为原始值格式分类：

- `生产日期`：`YYYY-M-D_like`=99,705；`missing`=2,425。
- `通报时间`：`YYYY-M-D_like`=102,130。

## Mixed-type Fields 检查

- `检测数值`：type_counts={'float': 140, 'str': 3876, 'int': 29}；non-null=4,045；missing=98,085。
- `法规限制`：type_counts={'str': 3044, 'int': 1}；non-null=3,045；missing=99,085。

本次没有进行 numeric conversion、unit parsing 或 recoding。

## Low-cardinality Fields 检查

以下仅统计原始取值，不进行 recoding 或翻译：

- `判定结果`：`合格`=97,873；`不合格`=4,257。
- `抽检级别`：`市抽`=70,493；`省抽`=31,624；`国抽`=13。
- `抽样环节`：`流通环节`=80,360；`餐饮环节`=15,950；`生产环节`=5,820。
- `是否网抽`：`否`=52,829；`是`=49。

## Provenance Fields 检查

- `来源链接`：non-null=102,130；missing=0；unique=247。
- `伙伴网链接`：non-null=31,625；missing=70,505；unique=38。
- `_export_file`：non-null=102,130；missing=0；unique=6,662。

本次没有执行 link validation、web access 或 provenance-based filtering。

## Recommended Cleaning Actions

以下为建议动作，不是已执行动作：

- 确认是否保留 `Unnamed: 28` 与 `Unnamed: 29`，或将其作为空 export artifact 删除。
- 为 `生产日期` 与 `通报时间` 制定 date parsing 规则，并明确无法解析值的处理方式。
- 为 `检测数值` 与 `法规限制` 制定 mixed-type handling 规则，包括是否保留原始字符串、是否拆分数值/单位/限定符、以及是否创建派生字段。
- 判断 high-missingness fields 的缺失是否为结构性缺失，尤其是 `不合格项目分类`、`不合格项目`、`不合格规范列`、`检测数值`、`法规限制`、`商标`、`措施`、`伙伴网链接`、`检验项目`、`标准` 和 `备注`。
- 确认 `判定结果`、`抽检级别`、`抽样环节` 与 `是否网抽` 的允许取值集合，再决定是否需要 category mapping 或 recoding。
- 确认 `序号` 是否可作为后续 cleaned dataset 的 row identifier，或是否需要设计 composite key。

## Approval-required Actions

在用户明确审批前，不应执行以下动作：

- 删除任何字段，包括 `Unnamed: 28` 与 `Unnamed: 29`。
- Parsing `生产日期` 或 `通报时间`。
- Converting `检测数值` 或 `法规限制`。
- Imputing missing values 或基于 missingness 过滤记录/字段。
- Recoding `判定结果`、`抽检级别`、`抽样环节` 或 `是否网抽`。
- Deduplication 或基于 `序号`/composite key 的记录合并。
- 创建 cleaned analysis-ready dataset。
- 运行 formal EDA、statistical analysis 或 modeling。
