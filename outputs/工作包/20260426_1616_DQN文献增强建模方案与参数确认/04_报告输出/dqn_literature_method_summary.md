# 20260426 DQN 文献增强阅读笔记：PEANUT 风险监管建模

## 结论

本轮新增文献支持把 PEANUT 抽检资源配置表述为 `belief-MDP / constrained MDP`：状态来自 Beta-Binomial 信念与 MOE/EDI 风险特征；动作是省份×供应链环节的整数抽检资源分配；约束至少包括预算、检测产能、最低覆盖与行动可行性；目标函数应将 MOE/EDI 风险降低、信息价值、抽检成本和处置/召回损失分开参数化。

## 方法依据

- Mnih et al. (2015) 支持使用 DQN 在高维状态上近似 Q 函数，但不提供食品监管参数。
- van Hasselt et al. (2016) 支持用 Double DQN 减少 Q 值过估计，可作为正式训练候选 variant。
- Altman (1999) 与 safe RL 约束综述支持将预算/产能等写成 CMDP 或 action mask/约束惩罚。
- van Asselt et al. (2021)、FAO、Wang et al. (2020)、Focker et al. (2023) 支持 risk-based monitoring、风险排序、成本有效抽样和公共健康风险降低导向。
- EFSA/JECFA/IARC 支持 MOE/EDI 和 AFB1 风险模块，但本项目当前 BMDL 仍是 prototype 来源，正式值必须确认。

## 不可直接定稿的参数

动作档位、预算、单位成本、产能、最低覆盖、处置/召回损失、reward 权重、约束惩罚、DQN 网络结构与训练超参数仍需用户确认。文献只能给出候选范围和建模理由。
