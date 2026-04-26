# PEANUT 上游结果自动查验报告

## 查验范围

- 原始数据：`data/01_raw/PEANUT2023-20241.xlsx`
- 清洗主表：`data/03_primary/peanut_cleaned_analysis_ready.csv`
- AFB1 浓度清洗表：`data/04_feature/peanut_concentration_clean_table.csv`
- 浓度分布摘要：`data/04_feature/peanut_concentration_distribution_summary.csv`
- 计数面板：`data/04_feature/peanut_count_panel.csv`
- Beta-Binomial belief state：`data/04_feature/peanut_beta_binomial_belief_states.csv`
- belief-MDP state features：`data/04_feature/peanut_belief_mdp_state_features.csv`

## 核心统计

```json
{
  "clean_rows": 94556,
  "raw_rows": 94714,
  "afb1_records": 1978,
  "afb1_concentration_rows": 1978,
  "afb1_concentration_available": 766,
  "afb1_limit_available": 754,
  "afb1_exceedance": 805,
  "panel_rows": 1710,
  "panel_afb1_concentration_available_total": 766,
  "belief_rebuilt": true
}
```

## 发现问题与修复

| 问题类型 | 发现数量 | 是否自动修复 | 影响范围 |
| --- | --- | --- | --- |
| AFB1标签不一致 | 2 | 是 | 清洗主表、浓度表、计数面板、belief状态 |
| 浓度清洗状态修复 | 93621 | 是 | 浓度清洗与超标判断 |
| 法规限量_单位修复 | 71 | 是 | 超标判断与超标倍数 |
| 法规限量解析状态修复 | 93756 | 是 | 超标判断与超标倍数 |
| AFB1浓度表记录数变化 | 2 | 是 | 浓度清洗表 |
| 计数面板浓度可用记录数口径错误 | 940 | 是 | 计数面板、belief-MDP状态特征 |

## 浓度清洗 must-pass 检查结论

- AFB1 常见变体识别：已使用扩展规则复核并重算。
- 非 AFB1 生物毒素误识别：未默认把所有 `生物毒素` 视为 AFB1；可疑记录进入复核。
- `检测数值`：已重算原始值、初检值、复检值、最终采用值、单位、解析状态和失败原因。
- `法规限制`：已重算原始限量、数值、单位、比较符号和单位推断标记。
- AFB1 单位：优先统一到 `μg/kg`；无法统一的记录进入复核。
- `是否超标`：已优先使用统一单位后的浓度与限量比较，并与原始判定交叉校验。
- `超标倍数`：已基于统一单位后的浓度和限量重算。
- 浓度分布摘要：仅基于有效 AFB1 浓度记录生成。
- 报告统计：本报告统计直接从修复后的 CSV 重新计算。

## 下游影响

本次修复影响了浓度清洗表、浓度分布摘要和计数面板中的 `浓度可用记录数` 口径，因此已同步重建 Beta-Binomial belief state 与 belief-MDP state features。
