# 原始数据 Validation Proposal：FINAL_SiChuan_2023_ALL_DATA

日期：2026-04-14

范围：仅提出 active raw dataset 的 validation proposal。本文件不应用 cleaning rules，不进行 date parsing，不创建 cleaned datasets，不运行 formal analysis，也不做 modeling decisions。

Active raw dataset：`F:\DESK\workflow1\data\01_raw\FINAL_SiChuan_2023_ALL_DATA.xlsx`

Sheet names：`Sheet1`

## Proposed Validation Checks

| 检查范围 | Proposed check | 原因 | Expected output | 风险或假设 |
|---|---|---|---|---|
| 文件身份 | 确认 active input 仍为 `FINAL_SiChuan_2023_ALL_DATA.xlsx`。 | 避免误用此前的 raw datasets。 | 记录 active input path 与 file type 的 validation note。 | 假设该 basename 唯一标识当前目标数据集。 |
| Workbook 结构 | 确认 `Sheet1` 存在，且 header row 为一行。 | 避免 sheet name 或 header offset 错误。 | 包含 row count 与 column count 的 sheet inventory。 | 假设第 1 行是预期 header row。 |
| Expected columns | 将当前 inventory 中观察到的 33 个 source columns 作为参照进行检查。 | 检测文件版本是否意外变化。 | expected、missing、extra columns 的 pass/fail list。 | 必须严格保留原始中文字段名。 |
| Row identity | 检查 `序号` 的完整性与唯一性。 | `序号` 是 schema inventory 中唯一的 standalone candidate key。 | 包含 duplicate count 与 missing count 的 key validation summary。 | 这不能证明 `序号` 在未来文件中也具有语义稳定性。 |
| Empty columns | 确认 `Unnamed: 28` 和 `Unnamed: 29` 仍为空。 | 识别 export artifacts，但不删除字段。 | Empty-column validation summary。 | Dropping columns 不包含在此步骤中，且需要审批。 |
| Date-like fields | 仅 profile `生产日期` 和 `通报时间` 的 raw string formats，不进行 parsing。 | 为未来 approval-gated date parsing decision 做准备。 | 未解析原始格式的 format-frequency summary 和 examples。 | 此 validation step 不应进行 date parsing 或 coercion。 |
| Mixed-type fields | Profile `检测数值` 和 `法规限制` 的 raw type categories。 | 这些字段包含 mixed numeric and text representations。 | Raw type-count 与 representative-format summary。 | 不进行 numeric conversion、unit parsing 或 recoding。 |
| Missingness | 汇总所有字段的 missingness，并标记 high-missingness fields。 | 识别结构性缺失候选与数据质量风险。 | 按 source column 输出的 missingness table。 | 不包含 missingness interpretation。 |
| Low-cardinality fields | 汇总 `判定结果`、`抽检级别`、`抽样环节` 和 `是否网抽` 的 unique counts。 | 为后续 category values 验证做准备。 | 使用原始值的 category-count summary。 | 不进行 recoding 或翻译原始取值。 |
| Provenance fields | 汇总 `来源链接`、`伙伴网链接` 和 `_export_file` 的完整性与唯一性。 | 支持 traceability checks。 | Provenance-field completeness and uniqueness summary。 | 不包含 link validation 或 web access。 |

## Auto-Allowed Scope

该 validation step 只能产生 lightweight technical summaries：

- File and sheet validation summary。
- Expected-column check summary。
- `序号` 的 candidate-key validation summary。
- Missingness summary。
- `生产日期`、`通报时间`、`检测数值` 和 `法规限制` 的 raw format summaries。
- 使用原始 source values 的 category-count summaries。

## Explicitly Out of Scope Until Approval

- 应用 cleaning rules。
- 删除 `Unnamed: 28`、`Unnamed: 29` 或任何其他字段。
- Parsing `生产日期` 或 `通报时间`。
- Converting `检测数值` 或 `法规限制`。
- Imputing missing values。
- Recoding `判定结果`、`抽检级别`、`抽样环节` 或 `是否网抽`。
- 创建 cleaned analysis-ready datasets。
- 运行 formal EDA、statistical analysis 或 modeling。
- 解释结果或起草 research report。

## First Approval-Required Step After Review

在用户 review 此 proposal 之后，第一个 approval-required step 将是任何 validation-driven changes 的执行决策，例如 date parsing、type conversion、column dropping、recoding、imputation、deduplication，或创建 cleaned analysis-ready dataset。
