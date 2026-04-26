# DQN 联网补充文献方法支持报告

联网文献仅用于补充方法背景，不覆盖用户研究计划。若外部文献与用户文档冲突，以用户文档为准。

## 候选文献

- **Human-level control through deep reinforcement learning** (2015, Nature): 说明 DQN 以 neural network 近似 Q(s,a)，但不替代用户文档中的状态、动作和奖励设定。 URL: https://www.nature.com/articles/nature14236
- **A Survey of Constraint Formulations in Safe Reinforcement Learning** (2024, IJCAI): 支持把预算、产能、覆盖和风险红线写为约束或约束惩罚；不覆盖用户文档设定。 URL: https://www.ijcai.org/proceedings/2024/913
- **State of the Art - A Survey of Partially Observable Markov Decision Processes** (1982, Management Science): 支持在不可直接观测污染状态时使用 belief state；具体 belief 构造以项目文档为准。 URL: https://pubsonline.informs.org/doi/10.1287/mnsc.28.1.1
- **Modeling cost-effective monitoring schemes for food safety contaminants: Case study for dioxins in the dairy supply chain** (2021, Food Research International): 支持预算受限食品安全监测优化的建模思想；正式动作和成本仍需用户确认。 URL: https://www.sciencedirect.com/science/article/pii/S0963996921000077
- **Application of the Margin of Exposure (MOE) approach to substances in food that are genotoxic and carcinogenic: Example: Aflatoxin B1** (2010, Food and Chemical Toxicology): 支持 AFB1 作为 MOE 风险度量场景；BMDL 和暴露参数不得由 Codex 擅自定为正式值。 URL: https://www.sciencedirect.com/science/article/pii/S0278691509004980
- **Margin of Exposure** (current topic page, European Food Safety Authority): 支持 MOE 的监管解释；项目正式阈值和惩罚映射仍需用户确认。 URL: https://www.efsa.europa.eu/en/topics/topic/margin-exposure

## 对本项目的边界

- DQN 原始文献只说明 Q-learning + 深度网络函数逼近的算法基础，不定义本项目动作、预算和 reward。
- safe/constrained RL 文献支持把预算、产能、安全阈值作为约束，但具体阈值必须由用户确认。
- 食品安全监测优化文献支持预算受限监测设计，但不提供本项目可直接套用的抽检成本和召回损失。
- MOE/AFB1 文献支持风险度量方向，但正式 BMDL、消费量高分位和风险惩罚映射仍需确认。
