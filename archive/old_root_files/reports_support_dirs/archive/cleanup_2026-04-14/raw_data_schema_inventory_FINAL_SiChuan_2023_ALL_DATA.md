# 原始数据 Schema Inventory：FINAL_SiChuan_2023_ALL_DATA

日期：2026-04-14

范围：仅针对当前 active raw dataset 进行 schema inventory。除非明确要求复用，否则忽略之前的原始数据集和此前基于其他数据集得出的技术结论。本文件未执行 cleaning、transformation、date parsing、formal analysis 或 modeling。

使用的 skill：`skills/data-schema-profiler`。

## 已确认的 Active Raw Dataset

| 属性 | 值 |
|---|---|
| 精确文件路径 | `F:\DESK\workflow1\data\01_raw\FINAL_SiChuan_2023_ALL_DATA.xlsx` |
| 相对文件路径 | `data/01_raw/FINAL_SiChuan_2023_ALL_DATA.xlsx` |
| 文件类型 | Excel workbook (`.xlsx`) |
| 文件大小 | 17,081,452 bytes |
| Active sheet names | `Sheet1` |

## Workbook 结构

| Sheet | Header row | Data rows | Columns |
|---|---:|---:|---:|
| `Sheet1` | 1 | 102,130 | 33 |

## `Sheet1` 字段清单

| 字段名 | Inferred type | Non-null | Missing | Unique values | 备注 |
|---|---:|---:|---:|---:|---|
| `序号` | integer | 102,130 | 0 | 102,130 | 候选行级 key；在当前 raw file 中完整且唯一。 |
| `产品分类` | text | 102,130 | 0 | 215 | 产品类别。 |
| `产品名称` | text | 102,130 | 0 | 28,466 | 产品名称；高基数 text field。 |
| `判定结果` | text | 102,130 | 0 | 2 | 从字段名看是 target-like outcome field；是否用于 modeling 需要用户确认。 |
| `不合格项目分类` | text | 4,245 | 97,885 | 40 | Missingness 很高；可能主要在不合格或问题记录中填充。 |
| `不合格项目` | text | 4,257 | 97,873 | 318 | Missingness 很高；可能主要在不合格或问题记录中填充。 |
| `不合格规范列` | text | 4,391 | 97,739 | 243 | Missingness 很高；可能主要在不合格或问题记录中填充。 |
| `检测数值` | mixed | 4,045 | 98,085 | 2,859 | 混合 float、integer 和 text values；missingness 很高。 |
| `法规限制` | mixed | 3,045 | 99,085 | 317 | 主要为 text，包含一个 integer value；missingness 很高。 |
| `规格型号` | text | 100,964 | 1,166 | 5,416 | 规格/型号文本。 |
| `商标` | text | 39,246 | 62,884 | 1,075 | 品牌/商标；missingness 较高。 |
| `生产日期` | text | 99,705 | 2,425 | 1,437 | 从字段名看是 date/time field；未进行 parsing。 |
| `生产企业名称` | text | 102,096 | 34 | 18,115 | 生产企业名称。 |
| `生产企业地址` | text | 102,052 | 78 | 18,931 | 生产企业地址。 |
| `生产省份` | text | 102,130 | 0 | 33 | 生产省份。 |
| `抽样单位名称` | text | 102,121 | 9 | 36,033 | 抽样单位名称；高基数 text field。 |
| `抽样单位地址` | text | 83,248 | 18,882 | 6,255 | 抽样单位地址。 |
| `通报时间` | text | 102,130 | 0 | 127 | 从字段名看是 date/time field；未进行 parsing。 |
| `通报文号` | text | 102,130 | 0 | 159 | 通报/文号字段；不是唯一值。 |
| `通报单位` | text | 102,130 | 0 | 39 | 通报单位。 |
| `措施` | text | 1,720 | 100,410 | 61 | Missingness 极高。 |
| `伙伴网链接` | text | 31,625 | 70,505 | 38 | Missingness 较高；来源/参考链接。 |
| `来源链接` | text | 102,130 | 0 | 247 | 来源链接；不是唯一值。 |
| `检验项目` | text | 266 | 101,864 | 59 | Missingness 极高。 |
| `抽检级别` | text | 102,130 | 0 | 3 | 低基数字段。 |
| `检验机构` | text | 67,072 | 35,058 | 119 | 检验机构；中等 missingness。 |
| `标准` | text | 3,952 | 98,178 | 53 | Missingness 很高。 |
| `备注` | text | 693 | 101,437 | 211 | Missingness 极高。 |
| `Unnamed: 28` | empty | 0 | 102,130 | 0 | 空的 unnamed column。 |
| `Unnamed: 29` | empty | 0 | 102,130 | 0 | 空的 unnamed column。 |
| `抽样环节` | text | 102,130 | 0 | 3 | 低基数字段。 |
| `是否网抽` | text | 52,878 | 49,252 | 2 | 从字段名看是 binary-like indicator；未进行 recoding。 |
| `_export_file` | text | 102,130 | 0 | 6,662 | 来源导出/provenance marker。 |

## Candidate Keys

- `序号` 是当前 raw file 中识别出的唯一 standalone candidate row-level key：102,130 个 non-null values，且 102,130 个 unique values。
- 未测试或选择 composite key。
- `通报文号`、`来源链接` 和 `_export_file` 可能有助于 provenance 或 grouping，但它们不是唯一的 standalone row keys。

## Likely Date/Time Fields

- `生产日期`：从字段名看可能是生产日期字段；当前 inferred type 为 text，未进行 parsing。
- `通报时间`：从字段名看可能是通报/公告时间字段；当前 inferred type 为 text，未进行 parsing。

## Likely Target Columns

- `判定结果`：从字段名看是 target-like outcome field，且有 2 个 unique values。这只是候选判断；任何将其作为 modeling target 的用法都需要经过 approval-gated model-framing decision。
- `是否网抽`：从字段名看是 binary-like indicator，观察到 2 个 non-null values。验证前仅作为候选 metadata 或 feature field；未经审批不得 recode。

## Obvious Schema Risks

- Date/time-like fields `生产日期` 和 `通报时间` 以 text 形式存储；date parsing 属于 approval-required step。
- Mixed-type fields：`检测数值` 和 `法规限制`。
- Empty columns：`Unnamed: 28` 和 `Unnamed: 29`。
- High-missingness columns 包括 `不合格项目分类`、`不合格项目`、`不合格规范列`、`检测数值`、`法规限制`、`商标`、`措施`、`伙伴网链接`、`检验项目`、`标准` 和 `备注`。
- 多个不合格/问题相关字段呈现稀疏填充；在 validation 确认 missingness 是否为结构性缺失前，不应进行解释。
- `判定结果` 看起来是 target-like field，但尚未做出 model framing decision。
