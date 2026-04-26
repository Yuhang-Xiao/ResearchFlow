# PEANUT MOE/EDI 外部参数匹配与风险度量准备报告

## 1. 本轮任务目的

本轮在不运行 DQN 的前提下，基于修复后的 AFB1 浓度清洗表、计数面板和 belief-MDP 状态特征表，接入消费量、人口、体重和 BMDL prototype 参数，构建 EDI/MOE 风险度量数据基础，并判断是否具备进入最小 belief-MDP / DQN prototype 的条件。

## 2. 输入文件

- 浓度清洗表：`D:/桌面/codex/workflow1/data/04_feature/peanut_concentration_clean_table.csv`
- 浓度分布摘要：`D:/桌面/codex/workflow1/data/04_feature/peanut_concentration_distribution_summary.csv`
- 计数面板：`D:/桌面/codex/workflow1/data/04_feature/peanut_count_panel.csv`
- Beta-Binomial belief states：`D:/桌面/codex/workflow1/data/04_feature/peanut_beta_binomial_belief_states.csv`
- belief-MDP 状态特征：`D:/桌面/codex/workflow1/data/04_feature/peanut_belief_mdp_state_features.csv`
- 上轮 DQN 前置判断：`D:/桌面/codex/workflow1/reports/peanut_pre_dqn_readiness_after_repair.md`
- 消费量文件：`D:/桌面/codex/workflow1/data/01_raw/Concentration_and_Consumption pEANUT.xlsx`
- 人口文件：`D:/桌面/codex/workflow1/data/01_raw/population_long_clean.xlsx`

## 3. 消费量文件读取与字段识别

消费量文件读取成功，共 `240` 行。识别字段包括 `Province`、`MonitorngYear`、`Consumption_g_day`、`BodyWeight (kg)`、`SampleCount`、`Mean_concentration_MP(ug/kg)` 等。原始消费量单位为 `g/day`，已转换为 `kg/day = g/day / 1000`。

原始文件未提供 P95 或高消费量字段，因此本轮消费量参数表保留 P95/高消费量为空，并将该点标记为后续人工复核事项。

## 4. 人口文件读取与字段识别

人口文件读取成功，共 `310` 行。识别字段包括 `Province`、`MonitoringYear`、`population`。该表为长表结构。人口原始值按中国省级人口量级推断为“万人”，并同步生成 `人口数_人 = population * 10000`。

## 5. 匹配规则

消费量匹配规则：

1. 优先按省份规范化名称 + 同年匹配。
2. 若面板年份不在消费量表中，使用同省最近年份。
3. 若省份无法匹配，使用全国中位数默认值，并标记低置信度和人工复核。

人口匹配规则：

1. 优先按省份规范化名称 + 同年匹配。
2. 若年份不完全一致，使用同省最近年份。
3. 若无法匹配，保留缺失并记录清单。

## 6. 匹配质量

- belief-MDP 状态单元总数：`1710`
- 消费量任意规则成功匹配单元数：`1710`
- 消费量同省同年匹配单元数：`0`
- 消费量建议人工复核单元数：`1710`
- 人口成功匹配单元数：`1639`
- 人口未匹配单元数：`71`
- 人口建议人工复核单元数：`71`

人口未匹配省份/年份清单：

| 省份   |   年份 |
|:-------|-------:|
| 不详   |   2023 |
| 不详   |   2024 |
| 台湾   |   2023 |
| 未知   |   2024 |
| 进口   |   2023 |
| 进口   |   2024 |
| 香港   |   2023 |

## 7. 体重参数

体重统一设定为 `60.0` kg bw。

## 8. BMDL 参数

BMDL 来源为用户提供截图中的 QIVIVE predicted BMDL10 based on HCC。本轮仅作为 MOE/EDI prototype 参数，不能作为最终毒理学结论。正式论文需补充可引用文献或原始来源。

情景参数：

- low BMDL：`0.050 μg/kg bw`
- sensitive BMDL：`0.066 μg/kg bw`
- default BMDL：`0.105 μg/kg bw`
- high BMDL：`0.158 μg/kg bw`
- upper BMDL：`0.189 μg/kg bw`
- MOE cutoff：`3160.0`

## 9. BMDL lognormal 或情景参数构建逻辑

以 default BMDL `0.105 μg/kg bw` 作为默认中心值。由于截图中的 P1/P5/P95/P99 与 sensitive/less sensitive 命名方向存在歧义，本轮不强行解释为普通统计分位数；配置文件保留所有情景点，并按低/高端点成对估计 lognormal 的近似 sigma，同时保留五个情景值供敏感性分析。该近似仅供原型风险度量准备。

## 10. EDI 计算逻辑

使用 AFB1 最终采用浓度，优先解释为 `μg/kg food`。消费量已转为 `kg/day`。计算公式：

`EDI = AFB1浓度(μg/kg food) × 消费量(kg/day) / 体重(kg bw)`

输出 EDI 单位为 `μg/kg bw/day`。

## 11. MOE 计算逻辑

`MOE = BMDL / EDI`

已按多个 BMDL 情景计算 `MOE_low_bmdl`、`MOE_sensitive_bmdl`、`MOE_default_bmdl`、`MOE_high_bmdl`、`MOE_upper_bmdl`，并以 cutoff `3160.0` 生成 `是否低于MOE阈值`、`MOE风险等级` 和 `MOE风险惩罚项`。

## 12. 当前结果是否可用于正式论文

当前结果适合作为 PEANUT 风险监管 workflow 的 prototype 数据基础，不建议直接作为正式论文结论。主要原因是消费量年份回退、BMDL 来源仍需正式可引用文献、P95/高消费量字段缺失，以及 reward 所需预算/成本/产能/召回损失等外部参数尚未接入。

## 13. Prototype assumptions

- 体重固定为 60 kg bw。
- 消费量使用平均消费量，缺少高消费量/P95 场景。
- 2023-2024 状态使用消费量同省最近年份回退。
- BMDL 情景值来自用户截图，lognormal 仅为近似。
- 人口单位推断为万人。

## 14. 当前是否可以进入 DQN prototype

当前仍不建议进入正式 DQN。本轮已经具备最小 belief-MDP 状态特征扩展和 EDI/MOE reward proxy 的雏形，但 DQN 仍缺动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

若只做最小 DQN prototype，建议状态可使用：belief posterior 均值/方差、抽检覆盖强度、AFB1 记录覆盖强度、浓度可用率、EDI/MOE 汇总特征、低于 MOE cutoff 比例、人口加权风险 proxy、MOE 风险惩罚 proxy。动作可先设为省份-环节抽检强度档位；reward 可使用风险惩罚下降、人口加权风险下降、抽检成本惩罚的线性组合；约束应至少包括预算和产能。

当前阻塞项：

- 仍存在人口未匹配状态单元，人口加权 reward 需人工复核或补齐。
- 消费量对 2023-2024 采用同省最近年份回退，正式 reward 前需确认可接受性。
- 仍未接入预算、产能、抽检成本、处置/召回损失、动作空间和约束参数。

## 15. 上游核验摘要

```json
{
  "required_files_all_present": true,
  "concentration_rows": 1978,
  "afb1_rows_with_numeric_concentration": 766,
  "count_panel_rows": 1710,
  "state_feature_rows": 1710,
  "count_panel_state_feature_row_match": true,
  "negative_concentration_rows": 0,
  "risk_table_rows": 766,
  "risk_summary_rows": 216
}
```

## 16. 下一步建议

先补齐或确认 DQN/MDP 必需外部参数：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重，并确认消费量最近年份回退和 BMDL 情景参数是否可作为论文前分析假设。
