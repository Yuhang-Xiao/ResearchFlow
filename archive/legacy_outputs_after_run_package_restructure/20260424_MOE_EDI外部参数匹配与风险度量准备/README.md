# MOE_EDI外部参数匹配与风险度量准备

## 任务名称

MOE/EDI 外部参数匹配与风险度量准备

## 执行日期

20260424

## 输入文件

- `D:/桌面/codex/workflow1/data/04_feature/peanut_concentration_clean_table.csv`
- `D:/桌面/codex/workflow1/data/04_feature/peanut_concentration_distribution_summary.csv`
- `D:/桌面/codex/workflow1/data/04_feature/peanut_count_panel.csv`
- `D:/桌面/codex/workflow1/data/04_feature/peanut_beta_binomial_belief_states.csv`
- `D:/桌面/codex/workflow1/data/04_feature/peanut_belief_mdp_state_features.csv`
- `D:/桌面/codex/workflow1/data/01_raw/Concentration_and_Consumption pEANUT.xlsx`
- `D:/桌面/codex/workflow1/data/01_raw/population_long_clean.xlsx`

## 输出文件

- `data/peanut_edi_moe_risk_table.csv`
- `data/peanut_belief_mdp_state_features_with_moe_edi.csv`
- `tables/peanut_consumption_parameter_table.csv`
- `tables/peanut_population_parameter_table.csv`
- `tables/peanut_edi_moe_risk_summary.csv`
- `configs/peanut_bmdl_parameter_config.json`
- `tables/peanut_bmdl_parameter_table.csv`
- `reports/peanut_moe_edi_external_parameter_matching_report.md`
- `reports/peanut_pre_dqn_readiness_after_moe_edi.md`
- `logs/peanut_moe_edi_error_log.md`
- `figures/*.svg`

## 关键参数

- 体重：60.0 kg bw
- BMDL default：0.105 μg/kg bw
- BMDL scenarios：0.050, 0.066, 0.105, 0.158, 0.189 μg/kg bw
- MOE cutoff：3160.0

## 匹配结果

- 消费量任意规则成功匹配：1710/1710
- 消费量同省同年匹配：0/1710
- 人口成功匹配：1639/1710
- 人口未匹配：71/1710

## 未解决问题

- 消费量未覆盖 2023-2024，主要使用同省最近年份回退。
- 消费量文件未提供 P95/高消费量字段。
- BMDL 参数来自用户截图，正式论文需补充可引用来源。
- DQN 仍缺动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

## 下一步建议

补齐 DQN/MDP 外部约束和成本参数，并确认消费量/BMDL prototype 假设是否可作为后续最小环境输入。
