# DQN 修正版结果审计报告

任务性质：DQN修正版 experimental run / revised DQN experimental run; not formal policy conclusion

## 核心审计结论

- 数据完整性：通过，上游 6 个 canonical 特征/风险表均存在且非空。
- 策略覆盖：DQN 修正版覆盖 1710 个状态。
- 训练环境：myenv1 + torch GPU，GPU 为 NVIDIA GeForce RTX 4060 Ti。
- PNG 图表：9/9 通过非空检查，中文字体为 `Microsoft YaHei`。
- 多模型对比：最佳策略为 `Q-learning`，total reward = 471.529095；DQN 修正版 rank = 2。
- Q-learning：已完成聚合状态 Q-learning baseline，total reward = 471.529095。
- 启发式策略：最佳启发式 baseline 为 `threshold/greedy uncertainty`，total reward = 468.916699。
- policy collapse：未见明显 collapse。
- reward hacking：未见通过违约或单纯规避成本获得异常高分的证据；仍需 formal 参数确认。
- 质量门控警告数：0。

## 解释边界

本轮结果只能作为 experimental run、workflow 闭环和参数敏感性设计参考。预算、成本、capacity、reward 权重、transition 仍未由用户作为 formal DQN 参数逐项确认，因此不得写成正式监管政策结论或论文最终核心结论。
