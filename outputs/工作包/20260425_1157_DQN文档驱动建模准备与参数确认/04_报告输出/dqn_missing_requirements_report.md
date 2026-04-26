# DQN 正式建模缺失项与参数确认报告

## 结论

当前不允许运行正式 DQN。原因不是上游数据完全不可用，而是正式决策参数尚未由用户确认；尤其是动作空间、预算、成本、产能、损失与 reward 权重。

- 需要用户确认的参数项：29
- 已生成参数确认表：`02_表格输出/dqn_parameter_confirmation_table.csv`

## 当前 canonical 数据可用性

- cleaned_dataset：存在=是；行数估计=103509；路径=`D:\桌面\codex\workflow1\data\03_primary\peanut_cleaned_analysis_ready.csv`
- count_panel：存在=是；行数估计=1710；路径=`D:\桌面\codex\workflow1\data\04_feature\peanut_count_panel.csv`
- concentration_table：存在=是；行数估计=1983；路径=`D:\桌面\codex\workflow1\data\04_feature\peanut_concentration_clean_table.csv`
- beta_binomial_states：存在=是；行数估计=1710；路径=`D:\桌面\codex\workflow1\data\04_feature\peanut_beta_binomial_belief_states.csv`
- belief_mdp_features：存在=是；行数估计=1710；路径=`D:\桌面\codex\workflow1\data\04_feature\peanut_belief_mdp_state_features.csv`
- belief_mdp_features_with_moe_edi：存在=是；行数估计=1710；路径=`D:\桌面\codex\workflow1\data\04_feature\peanut_belief_mdp_state_features_with_moe_edi.csv`
- edi_moe_risk_table：存在=是；行数估计=770；路径=`D:\桌面\codex\workflow1\data\04_feature\peanut_edi_moe_risk_table.csv`

## 必须确认的关键参数

- state 定义：partially_specified；建议=使用文档提到的 belief + MOE/EDI + 覆盖/不确定性特征作为候选，不作为正式定稿；formal=否，待确认
- observation 定义：partially_specified；建议=抽检批次/不合格/AFB1不合格/浓度作为候选；formal=否，待确认
- 动作空间：conceptual_only；建议=建议由用户确认动作档位和每档批次数；formal=否
- action mask：not_specified；建议=按预算、产能、最低覆盖生成 mask，待确认；formal=否
- 每期预算：not_specified；建议=建议值待用户提供；formal=否
- 产能上限：not_specified；建议=建议值待用户提供；formal=否
- 单批次抽检成本：conceptual_only；建议=建议按环节分别给成本；formal=否
- 区域/环节最低覆盖约束：conceptual_only；建议=建议用户给最低覆盖阈值；formal=否
- inspection allocation rule：conceptual_only；建议=候选：按风险、人口权重、不确定性联合排序；formal=否
- recall / disposal loss：conceptual_only；建议=由用户提供或指定情景值；formal=否
- risk loss：partially_specified；建议=用 MOE风险惩罚作为候选，权重待确认；formal=否
- information value weight：conceptual_only；建议=建议用不确定性下降 proxy，权重待确认；formal=否
- reward function：conceptual_only；建议=仅列候选公式，不定正式权重；formal=否
- transition logic：partially_specified；建议=沿用文档的 belief update；动作影响转移需确认；formal=否
- belief update：partially_specified；建议=prior/forgetting factor 需确认是否正式；formal=否，待确认
- time step：partially_specified；建议=建议月度；formal=否，待确认
- episode definition：not_specified；建议=建议按省份-环节时序或全局月度 episode，待确认；formal=否
- baseline policies：not_specified；建议=候选：历史分配、随机、风险贪心、均匀覆盖；formal=否
- DQN 网络结构：not_specified；建议=建议值待确认；formal=否
- learning rate：not_specified；建议=建议值待确认；formal=否
- gamma：not_specified；建议=建议值待确认；formal=否
- epsilon 策略：not_specified；建议=建议值待确认；formal=否
- replay buffer 大小：not_specified；建议=建议值待确认；formal=否
- batch size：not_specified；建议=建议值待确认；formal=否
- episode 数：not_specified；建议=建议值待确认；formal=否
- 训练/验证划分：not_specified；建议=建议时间外推验证，待确认；formal=否
- evaluation metrics：not_specified；建议=候选：风险损失、预算违约、覆盖率、MOE改善、不确定性下降；formal=否
- visualization outputs：not_specified；建议=建议策略地图、预算-风险曲线、约束违约图；formal=否
- formal stopping conditions：not_specified；建议=建议用户确认：参数未确认/上游核验失败/torch不可用时停止；formal=否

## 本轮禁止事项执行情况

- 未运行正式 DQN。
- 未使用 sklearn 替代正式 DQN。
- 未修改 `data/01_raw`。
- 未把 `20260425_1132_DQN初步运行` 的 sandbox 设定作为正式依据。
