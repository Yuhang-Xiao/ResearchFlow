# 输入说明

本轮未修改 `data/01_raw`。

## 上游输入

- `data/03_primary/peanut_cleaned_analysis_ready.csv`
- `data/04_feature/peanut_concentration_clean_table.csv`
- `data/04_feature/peanut_count_panel.csv`
- `data/04_feature/peanut_beta_binomial_belief_states.csv`
- `data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`
- `data/04_feature/peanut_edi_moe_risk_table.csv`
- `references/processed_summaries/peanut_research_plan_summary.md`
- `reports/项目级索引与摘要/peanut_pre_dqn_readiness_after_moe_edi.md`
- `D:/桌面/codex/zotero/data/deepreads/20260420_A Survey of Constraint Formulations in Safe Reinforcement Learning.md`
- `D:/桌面/codex/zotero/data/deepreads/20260425_Human-level control through deep reinforcement learning.md`

## 降级说明

本环境未安装 `torch`，因此本轮未运行 PyTorch DQN，而是使用 `sklearn.MLPRegressor` 实现 Fitted Q iteration 作为轻量 DQN-style 函数逼近烟测。
