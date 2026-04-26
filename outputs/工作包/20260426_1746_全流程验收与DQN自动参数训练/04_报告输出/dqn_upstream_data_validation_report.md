# DQN 上游数据核验报告

任务性质：自动合成参数 DQN 实验版 / self-synthesized DQN experimental run

## 文件可读性

file,exists,readable,rows,columns,issue
data\04_feature\peanut_belief_mdp_state_features.csv,True,True,1710,87,
data\04_feature\peanut_belief_mdp_state_features_with_moe_edi.csv,True,True,1710,120,
data\04_feature\peanut_beta_binomial_belief_states.csv,True,True,1710,87,
data\04_feature\peanut_count_panel.csv,True,True,1710,14,
data\04_feature\peanut_edi_moe_risk_table.csv,True,True,766,26,
data\04_feature\peanut_edi_moe_risk_summary.csv,True,True,216,16,


## 核心状态表

- 使用状态表：`data\04_feature\peanut_belief_mdp_state_features_with_moe_edi.csv`
- 行数：1710
- 列数：120
- 省份字段：`省份`
- 年月字段：`年月`
- 供应链环节字段：`供应链环节`
- posterior mean：`总体不合格_后验均值`
- posterior variance：`总体不合格_后验方差`
- AFB1 posterior：`AFB1全样本不合格_后验均值`, `AFB1全样本不合格_后验方差`
- MOE/EDI：`EDI均值`, `EDI_P95`, `MOE风险惩罚_proxy`
- 人口/人口风险：`人口数_人`, `人口加权风险_proxy`

## 计数面板对齐

merge 结果：{'both': 1710, 'left_only': 0, 'right_only': 0}。

## 缺失处理

MOE/EDI 在无浓度状态存在自然缺失；本轮 experimental DQN 使用 0 或中位数填补并记录，不删除状态。

结论：核心状态特征可构建，适合本轮 experimental DQN 训练；不适合作为 formal DQN 结论。
