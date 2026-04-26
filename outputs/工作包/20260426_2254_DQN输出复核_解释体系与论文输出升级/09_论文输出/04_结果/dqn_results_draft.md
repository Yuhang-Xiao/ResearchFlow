# DQN 修正版实验结果（experimental results draft）

## 结果边界

本节仅报告 PEANUT 风险监管 DQN 修正版的 experimental run。奖励权重、约束参数、动作空间和真实监管转移机制尚未完成 formal 确认，因此下述结果不能作为最终监管政策结论。

## 多模型比较

| policy | total_reward | risk_reward_total | information_gain_total | sampling_cost_total | constraint_violation_rate | rank |
| --- | --- | --- | --- | --- | --- | --- |
| Q-learning | 471.5291 | 437.0804 | 87.2321 | 108.3060 | 0.0000 | 1 |
| DQN修正版 | 469.8587 | 429.8497 | 80.3900 | 112.6620 | 0.0000 | 2 |
| threshold/greedy uncertainty | 468.9167 | 484.7041 | 105.3355 | 135.6120 | 0.0000 | 3 |
| risk-ranking top-k | 441.6613 | 422.6748 | 94.8814 | 82.3500 | 0.0000 | 4 |
| uniform allocation | 417.2752 | 348.0154 | 77.6811 | 90.9720 | 0.0000 | 5 |
| historical allocation | 305.5678 | 435.4147 | 68.7857 | 219.9060 | 0.0000 | 6 |
| random policy | 247.1343 | 283.6766 | 56.9349 | 108.2520 | 0.0000 | 7 |

在相同预算、动作约束、容量约束和评价指标下，`Q-learning` 取得最高 total_reward（471.529）。`DQN修正版` 位列第 2（total_reward=469.859），说明修正版 DQN 已能产生接近最优对照的策略输出，但当前并未超过 Q-learning。


    ## 约束与质量核验

    `constraint_violation_summary.csv` 显示所有比较策略的违约率为 0。该结果应解释为在当前 experimental action mask 与预算/容量配置下约束被满足，而不是数据缺失。图 `dqn_revised_constraint_summary_explained.png` 已将全 0 图转换为解释性 PNG。

    ## 图表引用

    - 图 1：`dqn_revised_policy_comparison.png`，展示各策略 total_reward 对比。
    - 图 2：`dqn_revised_reward_curve.png` 与 `dqn_revised_moving_average_reward.png`，展示训练回报和移动平均回报。
    - 图 3：`dqn_revised_constraint_summary_explained.png`，说明约束违约为 0 的语义。

    ## 文献依据

    DQN 训练机制参考 DQN、Double DQN/Dueling DQN 的方法谱系 [Mnih2015DQN; VanHasselt2016DoubleDQN; Wang2016DuelingDQN]；约束与安全强化学习解释参考 constrained RL/CMDP 文献 [Achiam2017CPO; Altman1999CMDP]；风险导向抽检逻辑参考 risk-based inspection 与 food safety monitoring 文献 [Wang2020RiskBasedSampling; VanAsselt2021RiskBasedInspections]。本轮仅建立 evidence map，不声称所有文献已完成全文形式核验。

    ## 不能过度解释的地方

    当前结果不能说明真实监管中 DQN 必然优于或劣于其他策略，也不能说明现有 reward 权重已经最优。formal DQN 需要进一步确认状态定义、动作空间、成本/预算/容量参数、约束强度、转移近似、敏感性分析和外部验证。
