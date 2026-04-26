# Results Draft (experimental results draft)

本节为 PEANUT 项目 DQN 修正版 **experimental results draft**。所有数值均来自本轮 CSV 输出；由于预算、成本、capacity、reward 权重和 transition 假设仍未作为 formal DQN 参数由用户逐项确认，以下结果不得解释为正式监管政策结论。

## 训练收敛与策略覆盖

DQN 修正版在 myenv1 + torch GPU 环境下完成 281 个 episode 的实验训练，策略表覆盖 1710 个省份-年月-供应链环节状态。最终 moving average reward 为 474.810668，最终 mean loss 为 0.128869。

## 多模型对比

本轮共比较 7 类策略。按 total reward 排序，最佳 experimental 策略为 `Q-learning`，total reward = 471.529095。DQN 修正版 total reward = 469.858674，rank = 2；Q-learning total reward = 471.529095，rank = 1。

## 约束与图表质量

DQN 修正版 constraint violation rate = 0.000000。本轮主图全部输出为 PNG；图表审计通过 9/9，并采用 `Microsoft YaHei` 作为中文字体。

## 结果边界

这些结果可用于评估 reward 重标度、动作空间可行性、多模型对比协议和科研质量门控，但不能作为 formal DQN 训练结论、政策建议或最终论文 Results。formal DQN 仍需用户确认动作空间、预算、成本、capacity、reward 权重、transition 与训练超参数。
