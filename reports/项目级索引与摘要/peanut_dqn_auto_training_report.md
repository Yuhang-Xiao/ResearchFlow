# PEANUT DQN 自动训练报告

任务性质：自动合成参数 DQN 实验版 / self-synthesized DQN experimental run

## 训练结论

- 状态数：1710
- 状态维度：15
- 动作空间：[0, 1, 3, 5, 10]
- 训练 episodes：120
- 设备：cuda / NVIDIA GeForce RTX 4060 Ti
- 最终 episode reward：-256.108393
- 最终 mean loss：0.001326

## baseline 对比

DQN policy total reward = 28.241472；最佳非 DQN baseline 为 `risk_ranking_top_k`，total reward = -249.171999。

## 解释边界

本结果可以用于 workflow 闭环验收、prototype 方法探索和参数敏感性设计，不能作为正式监管政策结论、论文最终核心结论或用户确认参数后的 formal DQN 结果。


## 审计补充

第三次重训后采用人口风险 P95 归一化。DQN total reward = 28.241；最佳非 DQN baseline = risk_ranking_top_k (-249.172)；策略覆盖 1710 个状态，约束违约率 0。
