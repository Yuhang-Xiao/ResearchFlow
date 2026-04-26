# DQN 自动训练结果审计报告

任务性质：自动合成参数 DQN 实验版 / self-synthesized DQN experimental run

## 审计结论

训练完成，策略覆盖 1710 / 1710 个状态；DQN policy total reward = 28.241，优于最佳非 DQN baseline `risk_ranking_top_k`（-249.172）。约束违约率为 0。

## 数值审计

- 最终 episode reward：-256.108
- 最终 mean loss：0.001326
- 最终 epsilon：0.548
- 最大动作占比：0.842
- 推荐动作集合：0, 1, 3, 5

## 自动修复记录

1. 首次报告阶段缺少 `tabulate`，已改用 CSV 文本报告。
2. 第二次训练发现 reward/Q/loss 数量级异常，原因是人口加权风险 proxy 未归一化；已用 P95 归一化后重训。
3. Matplotlib SVG 输出存在 CJK 字体缺字 warning；图表文件已生成，核心数值不受影响，后续可配置中文字体改善显示。

## 边界

本轮结果可用于 workflow 闭环验收、方法探索和 prototype 分析，不能作为最终监管政策结论、论文核心结论或 formal DQN 结果。
