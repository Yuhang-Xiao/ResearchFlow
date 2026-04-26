# DQN 文献增强建模方案与参数确认报告

## 1. 本轮结论

本轮未运行正式 DQN。基于用户研究计划、当前 PEANUT 数据结构、MOE/EDI 风险特征、belief-MDP 状态表、Zotero 审计与联网补充文献，当前最合适的正式表述是：**MOE/EDI 风险驱动的 belief-MDP / constrained MDP 抽检资源配置问题**。DQN 只能作为近似求解器之一，不能替代用户对动作、预算、成本、产能、reward 权重和训练参数的确认。

正式训练状态：**blocked**。原因是动作空间、预算、单位抽检成本、产能、最低覆盖、处置/召回损失、reward 权重、DQN 网络结构和训练超参数仍未确认。

## 2. 文档优先抽取

用户研究计划已经明确：真实污染/风险水平不可直接观测；抽检结果是观测信号；Beta-Binomial 信念更新与遗忘传播构成 belief-MDP；风险模块应接入 AFB1 浓度、EDI/MOE、人口/消费量/BMDL；动作是预算与产能约束下跨省份和供应链环节的整数抽检资源配置；reward 应综合暴露风险、抽检成本、处置/召回损失和信息价值。

## 3. 当前数据基础

- 清洗分析表：94,556 行。
- 浓度清洗表：1,978 行，最终采用浓度可用 766 行，未发现负浓度。
- count panel：1,710 行。
- Beta-Binomial belief states：1,710 行，与 count panel 行数一致。
- MOE/EDI 扩展 belief-MDP state features：1,710 行，120 列。
- EDI/MOE risk table：766 行。

仍需注意：消费量对 2023-2024 使用最近年份回退，人口有 71 个状态单元未匹配，BMDL 情景仍是 prototype 来源，正式风险 reward 前应确认。

## 4. 文献增强后的建模结构

### 状态 State

建议状态由四组组成，但需要用户确认特征白名单与标准化方式：

1. 信念模块：Beta posterior alpha/beta、后验均值、后验方差、后验强度、风险等级、不确定性等级。
2. 风险模块：AFB1 浓度分布、EDI、MOE、低于 MOE cutoff 比例、MOE 风险惩罚项。
3. 规模权重模块：人口权重、消费量、供应链环节、地区与时间特征。
4. 资源与惯性模块：上一期抽检量、覆盖强度、浓度可用率、预算剩余、产能剩余。

### 动作 Action

正式动作不应由 Codex 定稿。建议确认以下两种表达之一：

- 方案 A：对每个候选省份×环节给出整数抽检批次数，使用 action mask 保证预算/产能/整数约束。
- 方案 B：先按风险与不确定性筛选 top-K 候选单元，再从离散档位中分配增量抽检批次数，降低动作维度。

### Reward

建议拆解为可审计线性或 Lagrangian 形式：

`reward_t = w_risk * 风险下降 + w_info * 信息价值 - w_sample * 抽检成本 - w_disposal * 处置/召回损失 - w_violation * 约束违约`

其中所有权重、成本和损失都必须由用户确认；当前只能作为公式结构。

### 约束 Constraints

硬约束优先进入 action mask：总预算、环节/地区/实验室产能、整数抽检批次、最低覆盖、不可抽检对象屏蔽。若使用软约束或 Lagrangian penalty，需要单独确认惩罚权重和可接受违约容忍度。

### 算法候选

- Baselines：随机抽检、历史比例抽检、风险排序优先、MOE风险优先、信息价值优先、成本效果贪心。
- DQN 候选：基础 DQN、Double DQN、Dueling Double DQN。文献上 Double DQN 可降低 Q 过估计，建议作为正式候选，但最终 variant 需确认。

## 5. 文献依据如何进入模型

- Mnih et al. (2015): 支持 DQN 的 replay buffer 与 target network 机制。
- van Hasselt et al. (2016): 支持 Double DQN 作为降低过估计的候选。
- Altman (1999) 与 safe RL 约束综述：支持 CMDP/action masking/约束惩罚的建模语言。
- van Asselt et al. (2021)、FAO、Wang et al. (2020)、Focker et al. (2023): 支持 risk-based monitoring、资源有限条件下的抽检优先级和健康风险降低目标。
- EFSA/JECFA/IARC: 支持 AFB1 危害背景与 MOE/EDI 风险表征，但不能替代本项目 BMDL/消费量/人口参数确认。

## 6. 参数确认表

正式参数确认表已生成：`02_表格输出/dqn_parameter_confirmation_table.csv`，并同步为 canonical：`project_state/dqn_parameter_confirmation_table.csv`。

## 7. Readiness 判断

当前 readiness：**不可训练，只可继续参数确认与方案修订**。

必须确认后才能进入正式 DQN：动作空间、预算、成本、产能、最低覆盖、处置/召回损失、信息价值定义、reward 权重、transition/仿真假设、episode、baseline、DQN variant、网络结构、learning rate、gamma、epsilon、replay buffer、batch size、target update、训练/验证切分和评价指标。
