# DQN 文献与 Zotero 更新

## 已用本地文献

- `A Survey of Constraint Formulations in Safe Reinforcement Learning`：用于确认正式 DQN 应转为 constrained/safe RL 或 CMDP 表述，不能只最大化检测收益。
- `Designing optimal food safety monitoring schemes using Bayesian network and integer programming`：用于说明风险导向监测与预算约束优化的食品安全先例。
- `peanut_research_plan_summary.md`：用于确认本项目的状态、动作、reward 和约束设计方向。

## 本轮新增文献

- Mnih et al. (2015), *Human-level control through deep reinforcement learning*, Nature, DOI `10.1038/nature14236`。
- 用途：作为 DQN 原始方法文献，支撑用 Q-learning + 神经网络函数逼近学习 belief-MDP 动作价值函数。
- Zotero Web API 入库成功：item key `NHMM33QB`，note key `KZBVG5H5`。
- 本地记录：
  - `D:/桌面/codex/zotero/data/candidates/20260425_dqn_methods_candidates.csv`
  - `D:/桌面/codex/zotero/data/screened/20260425_dqn_methods_selected.csv`
  - `D:/桌面/codex/zotero/data/deepreads/20260425_Human-level control through deep reinforcement learning.md`
  - `D:/桌面/codex/zotero/logs/20260425_dqn_methods_zotero_import.md`

## 仍需补充

正式 DQN/受限 DQN 章节建议后续继续补充：

- Constrained DQN / safe RL 在预算、产能和风险阈值约束下的算法实现文献。
- 食品安全抽检资源分配中动作成本、处置成本、召回损失和健康风险损失的参数来源。
