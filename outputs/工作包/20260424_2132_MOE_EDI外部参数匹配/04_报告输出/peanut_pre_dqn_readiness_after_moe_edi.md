# DQN 前置状态判断：MOE/EDI 外部参数接入后

1. 消费量数据是否读取成功：成功，文件 `Concentration_and_Consumption pEANUT.xlsx`，共 `240` 行。
2. 人口数据是否读取成功：成功，文件 `population_long_clean.xlsx`，共 `310` 行。
3. 消费量匹配质量：任意规则成功 `1710/1710`；同省同年 `0/1710`；因年份回退或默认值建议复核 `1710` 个状态单元。
4. 人口匹配质量：成功 `1639/1710`；未匹配 `71`。
5. EDI 是否可计算：可计算，输出 `D:/桌面/codex/workflow1/data/04_feature/peanut_edi_moe_risk_table.csv`，记录数 `766`。
6. MOE 是否可计算：可计算，已按 5 个 BMDL 情景生成 MOE。
7. BMDL lognormal 或情景参数是否已配置：已配置，见 `D:/桌面/codex/workflow1/data/04_feature/peanut_bmdl_parameter_config.json`；lognormal 为 prototype 近似，不作最终毒理学结论。
8. belief-MDP 状态特征是否已加入 MOE/EDI：已加入，见 `D:/桌面/codex/workflow1/data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`。
9. 当前是否可以进入最小 DQN prototype：暂不建议正式进入；若仅做 sandbox prototype，可基于新增风险 proxy 设计环境，但仍缺关键动作、成本、预算和约束参数。
10. 如果仍不能进入，缺什么：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重，以及正式 BMDL 文献来源/消费量高分位参数确认。
11. 如果未来进入 DQN prototype，建议：
    - 状态：belief posterior、覆盖强度、浓度可用率、EDI/MOE 汇总、低于 cutoff 比例、人口加权风险 proxy、MOE 惩罚 proxy。
    - 动作：省份-环节抽检强度档位、专项抽检投放、复检/召回触发档位。
    - reward：风险下降收益 - 抽检成本 - 处置成本 - 约束违约惩罚。
    - 约束：预算、检测能力、区域最低覆盖、重点风险区域优先级。
