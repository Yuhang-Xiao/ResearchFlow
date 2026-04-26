# DQN 初步运行工作包

创建时间：2026-04-25 11:32

## 任务目标

根据 workflow1 当前花生/AFB1 风险监管项目状态，在进入正式 DQN 前完成上游核验，并在缺少正式动作、预算、成本和约束参数的情况下运行一个可复现的 DQN-style 沙盒 prototype。

## 关键结论

- 上游数据核验通过：cleaned dataset、浓度清洗表、count panel、Beta-Binomial belief states、belief-MDP+MOE/EDI 特征和 EDI/MOE 表均可读取并通过本轮一致性检查。
- 沙盒初跑成功：使用 `sklearn.MLPRegressor` 做 Fitted Q iteration 近似，因为本环境未安装 `torch`。
- 正式 DQN 仍未 ready：缺少动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束惩罚参数。
- 已补充 DQN 核心方法文献 Mnih et al. 2015 到 Zotero Web API，item key 为 `NHMM33QB`。

## 主要输出

- `04_报告输出/peanut_dqn_prototype_report.md`
- `02_表格输出/peanut_dqn_upstream_audit_findings.csv`
- `01_数据输出/peanut_dqn_prototype_policy.csv`
- `02_表格输出/peanut_dqn_top_priority_states.csv`
- `02_表格输出/peanut_dqn_action_summary.csv`
- `06_配置参数/peanut_dqn_prototype_assumptions.json`
- `07_日志与错误/peanut_dqn_prototype_run_summary.json`
- `08_代码快照/run_dqn_prototype.py`

## Zotero 文献

- 文献：Mnih et al. (2015), *Human-level control through deep reinforcement learning*, Nature, DOI `10.1038/nature14236`
- Zotero item key：`NHMM33QB`
- Zotero note key：`KZBVG5H5`
- 本地精读：`D:/桌面/codex/zotero/data/deepreads/20260425_Human-level control through deep reinforcement learning.md`
- 入库日志：`D:/桌面/codex/zotero/logs/20260425_dqn_methods_zotero_import.md`
