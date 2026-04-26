# DQN 初步运行报告

## 结论

- 已完成上游核验和 DQN-style 沙盒初跑。
- 本轮结果只能作为管线烟测和参数缺口定位，不能作为正式监管策略。
- 正式 DQN 仍被阻断：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束惩罚参数尚未确认。

## 上游核验

- PASS: 10
- WARN: 0
- FAIL: 0

## 沙盒模型设置

- 算法: Fitted Q iteration with sklearn MLPRegressor as a lightweight DQN-style function approximator; torch is not installed.
- 动作档位: 0=维持/不加码, 1=常规加密抽检, 2=重点专项抽检
- gamma: 0.85
- FQI iterations: 12

## 动作分布

|   recommended_action | recommended_action_name   |   状态单元数 |   平均风险proxy |   平均不确定性proxy |
|---------------------:|:--------------------------|-------------:|----------------:|--------------------:|
|                    0 | 维持/不加码               |          188 |        0.276162 |            0.155938 |
|                    1 | 常规加密抽检              |         1322 |        0.341222 |            0.57953  |
|                    2 | 重点专项抽检              |          200 |        0.844432 |            0.300225 |

## 正式 DQN 缺口

- 正式动作空间未确认：省份-环节抽检批次数、复检、召回/处置触发档位尚未参数化。
- 缺少正式预算、单次抽检成本、检测产能上限和区域最低覆盖约束。
- 缺少处置/召回损失、信息价值权重、约束违约惩罚权重。
- BMDL 与消费量高分位等毒理/暴露参数仍有 prototype 或待复核字段。
- 当前历史数据没有真实干预动作与动作后状态转移，无法做因果意义上的 off-policy DQN 评估。

## 输出文件

- 上游核验表: `D:\桌面\codex\workflow1\outputs\工作包\20260425_1132_DQN初步运行\02_表格输出\peanut_dqn_upstream_audit_findings.csv`
- prototype policy: `D:\桌面\codex\workflow1\outputs\工作包\20260425_1132_DQN初步运行\01_数据输出\peanut_dqn_prototype_policy.csv`
- 高优先级状态: `D:\桌面\codex\workflow1\outputs\工作包\20260425_1132_DQN初步运行\02_表格输出\peanut_dqn_top_priority_states.csv`
- 动作汇总: `D:\桌面\codex\workflow1\outputs\工作包\20260425_1132_DQN初步运行\02_表格输出\peanut_dqn_action_summary.csv`
