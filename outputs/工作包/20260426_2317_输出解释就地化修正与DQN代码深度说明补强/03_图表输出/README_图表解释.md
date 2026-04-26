# 图表输出解释

本目录说明：包含 DQN 训练曲线、策略比较、约束解释性图和图表 QA 相关 PNG。

## 文件说明
- `dqn_revised_action_distribution.png`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_revised_constraint_summary.png`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_revised_constraint_summary_explained.png`：解释性约束图，说明全 0 违约率是约束满足而非缺失。
- `dqn_revised_convergence_diagnosis.png`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_revised_moving_average_reward.png`：DQN 修正版移动平均 reward 曲线。
- `dqn_revised_policy_comparison.png`：DQN 与 baseline 策略 total reward 对比图。
- `dqn_revised_reward_curve.png`：DQN 修正版训练 reward 曲线。
- `dqn_revised_top_priority_risk.png`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_revised_training_curve.png`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `multi_model_comparison.png`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。

## 阅读规则

1. 本目录 README 是就地解释，不需要先跳到 `10_输出解释与索引/` 才能读懂。
2. 关键 artifact 均尽量配套同名 `.explanation.md`。
3. DQN 相关输出全部保持 experimental；不能作为 formal 监管政策结论。
4. 用户下一步应优先阅读本目录 README、关键同名 explanation、再回到总索引查看跨目录关系。
