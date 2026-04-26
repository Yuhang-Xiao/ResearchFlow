# DQN 自动参数合成报告

任务性质：自动合成参数 DQN 实验版 / self-synthesized DQN experimental run

本轮所有 DQN 参数均由 Codex 在用户明确授权 experimental run 的前提下自动合成。它们不是用户确认参数，也不能转写为 formal config。

## 关键参数

- 动作空间：[0, 1, 3, 5, 10]
- 月预算：4567（历史每月抽检总批次数 P75）
- 局部产能：省份 × 供应链环节历史 P90
- 成本：unit_sampling_cost = 1.0
- reward：risk_reward_weight * risk_coverage_gain + info_gain_weight * information_gain - cost_weight * sampling_cost - constraint_penalty_weight * constraint_violation
- transition：historical replay + Beta-Binomial uncertainty proxy
- 网络：MLP [128, 64]
- 训练：episodes=120, lr=0.001, gamma=0.95, batch_size=64

正式版本仍需用户确认 action、budget、capacity、minimum coverage、cost、reward weights、transition、baseline、network 与训练超参数。

## 自动修复补充

质量门控发现人口加权风险 proxy 未归一化会导致 reward/Q/loss 数量级异常；已在 reward 与策略 risk_score_proxy 中按 P95 归一化，保持 experimental 参数含义但提升数值可审计性。

