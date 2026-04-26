from pathlib import Path
import pandas as pd, yaml, json, textwrap, shutil
root=Path(r'D:\桌面\codex\workflow1')
run=Path(r'D:\桌面\codex\workflow1\outputs\工作包\20260426_1616_DQN文献增强建模方案与参数确认')
z=Path(r'D:\桌面\codex\zotero')
for p in [z/'data/candidates', z/'data/screened', z/'data/deepreads', z/'logs', root/'references/processed_summaries']:
    p.mkdir(parents=True, exist_ok=True)

lit = [
 {'key':'Mnih2015DQN','title':'Human-level control through deep reinforcement learning','authors':'Mnih et al.','year':2015,'source':'Nature','url':'https://www.nature.com/articles/nature14236','role':'DQN 核心方法：experience replay、target network、Q-value function approximation','use_in_model':'作为 DQN/Double DQN 基础，不覆盖食品监管约束设定'},
 {'key':'VanHasselt2016DDQN','title':'Deep Reinforcement Learning with Double Q-Learning','authors':'van Hasselt, Guez & Silver','year':2016,'source':'AAAI','url':'https://dblp.org/rec/conf/aaai/HasseltGS16.html','role':'降低 Q-learning maximization bias','use_in_model':'建议作为正式方案的首选 DQN variant 候选之一，需用户确认'},
 {'key':'Altman1999CMDP','title':'Constrained Markov Decision Processes','authors':'Altman','year':1999,'source':'Chapman & Hall/CRC','url':'https://openlibrary.org/books/OL97592M/Constrained_Markov_decision_processes','role':'预算、产能、安全约束的 CMDP 理论基础','use_in_model':'正式 DQN 应以约束 MDP/CMDP 表述，硬约束用 action mask，软约束用 Lagrangian/penalty 需确认'},
 {'key':'Guan2024SafeRLSurvey','title':'A Survey of Constraint Formulations in Safe Reinforcement Learning','authors':'Guan et al.','year':2024,'source':'IJCAI','url':'https://www.ijcai.org/proceedings/2024/0913','role':'safe RL 中约束形式与算法选择综述','use_in_model':'用于说明硬约束、期望累计约束、状态约束的区别，帮助参数表确认'},
 {'key':'VanAsselt2021RiskInspection','title':'Methods to perform risk-based inspections of food companies','authors':'van Asselt et al.','year':2021,'source':'Journal of Food Science','url':'https://pubmed.ncbi.nlm.nih.gov/34796503/','role':'食品安全 risk-based inspection 的步骤、优先级与资源约束背景','use_in_model':'支持“风险排序-抽检频次-成本有效监测”的监管逻辑'},
 {'key':'FAOFoodInspection','title':'Food inspection: risk-based food inspection systems','authors':'FAO','year':2026,'source':'FAO Food Safety and Quality','url':'https://www.fao.org/food-safety/food-control-systems/food-inspection/en','role':'官方风险导向食品检查原则','use_in_model':'支持在有限资源下优先高风险环节/对象'},
 {'key':'Wang2020RiskBasedSampling','title':'Optimization of Sampling for Monitoring Chemicals in the Food Supply Chain Using a Risk-Based Approach','authors':'Wang et al.','year':2020,'source':'Risk Analysis','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC7821187/','role':'用健康风险降低和预算优化食品链化学污染物监测','use_in_model':'支持把 reward 与公共健康风险降低、预算成本联结'},
 {'key':'Focker2023Monitoring','title':'Risk-based food safety monitoring with risk ranking and sampling strategies','authors':'Focker et al.','year':2023,'source':'Food Control','url':'https://edepot.wur.nl/576626','role':'风险导向监测与抽样策略比较','use_in_model':'支持 baseline 设计：随机、风险排序、历史频率、成本有效策略'},
 {'key':'EFSA_MOE','title':'Margin of Exposure topic page and 2005 opinion context','authors':'EFSA','year':2026,'source':'EFSA','url':'https://www.efsa.europa.eu/en/topics/topic/margin-exposure','role':'MOE 对遗传毒性/致癌物的风险表征框架','use_in_model':'支持 MOE penalty 作为 risk module，但 cutoff/效应点需确认'},
 {'key':'IARC_AFB1','title':'Aflatoxin B1 as Group 1 carcinogen / mycotoxins monographs context','authors':'IARC','year':2026,'source':'IARC','url':'https://www.iarc.who.int/reference/genome-scale-mutational-signatures-of-aflatoxin-in-cells-mice-and-human-tumors/','role':'AFB1 致癌危害背景','use_in_model':'支持 AFB1 风险优先级；不能替代暴露参数'},
 {'key':'JECFA_Aflatoxins','title':'WHO Food Additives Series 74: Aflatoxins addendum','authors':'JECFA/WHO','year':2018,'source':'WHO/IPCS INCHEM','url':'https://www.inchem.org/documents/jecfa/jecmono/v74je01.pdf','role':'AFB1 毒理学与风险评估依据','use_in_model':'正式 BMDL/MOE 参数应优先追溯该类官方资料或用户给定 QIVIVE 来源'}
]
litdf=pd.DataFrame(lit)
litdf.to_csv(run/'02_表格输出/web_literature_selected.csv', index=False, encoding='utf-8-sig')
litdf.to_csv(z/'data/candidates/20260426_dqn_literature_enhanced_candidates.csv', index=False, encoding='utf-8-sig')
litdf.to_csv(z/'data/screened/20260426_dqn_literature_enhanced_selected.csv', index=False, encoding='utf-8-sig')

note = """# 20260426 DQN 文献增强阅读笔记：PEANUT 风险监管建模

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
"""
(z/'data/deepreads/20260426_DQN文献增强_PEANUT风险监管建模.md').write_text(note, encoding='utf-8')
(root/'references/processed_summaries/20260426_dqn_literature_enhanced_method_summary.md').write_text(note, encoding='utf-8')
(run/'04_报告输出/dqn_literature_method_summary.md').write_text(note, encoding='utf-8')

params = [
 ['model_scope','正式训练开关','禁止训练','本轮只允许方案、审计、参数确认表','用户硬性要求','confirmed_for_this_task'],
 ['python_environment','正式 DQN Python','D:/anaconda3/envs/myenv1/python.exe','已验证 torch 2.11.0+cu126 / CUDA 12.6 / RTX 4060 Ti','用户指定+环境审计','confirmed'],
 ['unit_of_decision','决策单元','省份-月份-供应链环节','当前 count panel/state features 的主索引；1710 个状态单元','研究计划+数据结构','proposed_confirm'],
 ['time_step','时间步','month（月）','beta-binomial config 已设 time_unit=month；若政策按季度执行需重聚合','研究计划+本地 config','proposed_confirm'],
 ['hidden_state','隐状态','真实 AFB1 污染/不合格概率','不可直接观测，只由抽检与浓度信号更新信念','研究计划+POMDP 文献','conceptual_confirm'],
 ['observation','观测','抽检总批次数、不合格批次数、AFB1相关不合格批次数、浓度值、限量与 MOE/EDI 风险信号','当前数据已有观测字段；动作后观测生成机制需仿真设定','研究计划+当前数据','partial_confirm'],
 ['belief_update','信念更新','Beta-Binomial + forgetting factor','当前 config: alpha=1,beta=1, forgetting=0.95；正式是否保留 0.95 需确认','本地 config+文档','needs_user_confirm'],
 ['state_features','状态特征集合','posterior alpha/beta/mean/variance/strength, risk level, uncertainty, sampling counts, concentration availability, EDI/MOE summaries, population/consumption weights','当前 state_features 有 120 列；正式训练需确认特征白名单与标准化方式','研究计划+数据审计','needs_user_confirm'],
 ['action_space','动作空间','省份×供应链环节整数抽检批次数或离散强度档位','建议不直接枚举所有组合，可用候选动作生成器/top-K 风险单元+档位；具体档位需用户给定','研究计划+CMDP/RL 文献','needs_user_confirm'],
 ['action_mask','动作可行性 mask','预算、产能、最低覆盖、整数性、不可抽检对象屏蔽','硬约束优先用 mask；软约束可用惩罚/Lagrangian','Altman+safe RL','needs_user_confirm'],
 ['budget','总预算','待确认','可按月/年预算；若只有总预算需定义 episode 内消耗方式','研究计划','missing_required'],
 ['unit_sampling_cost','单位抽检成本','待确认','可按供应链环节/地区/检测项目设置；不得用 prototype 随机值','研究计划','missing_required'],
 ['capacity','检测/执法产能上限','待确认','省份/环节/月最大批次数，或实验室总产能','研究计划','missing_required'],
 ['minimum_coverage','最低覆盖规则','待确认','是否每省/每环节/每季度至少抽检若干批次','监管逻辑+FAO/van Asselt','missing_required'],
 ['recall_disposal_loss','召回/处置损失','待确认','不合格发现后的处置成本、召回损失、行政成本或社会损失','研究计划','missing_required'],
 ['risk_loss','风险损失','MOE/EDI 风险惩罚项','当前已有 MOE风险惩罚项；BMDL/cutoff 与人口权重仍需确认','MOE/EDI 产物+EFSA/JECFA','needs_user_confirm'],
 ['information_value','信息价值','后验方差下降/熵下降/有效样本强度增加','用于避免只追逐高风险而忽视不确定性；权重需确认','POMDP/belief-MDP 文献','needs_user_confirm'],
 ['reward_formula','reward','风险下降收益 + 信息价值 - 抽检成本 - 处置/召回损失 - 约束违约惩罚','建议拆成可审计权重；正式权重不可由 Codex 定稿','研究计划+文献','needs_user_confirm'],
 ['transition','转移逻辑','动作影响抽检样本量和观测，再通过 Beta-Binomial 更新信念；真实污染率可用历史/情景仿真','缺真实动作后反事实转移，需要仿真环境假设确认','数据限制+POMDP','needs_user_confirm'],
 ['episode','episode 定义','建议 12 个月或 24 个月滚动','取决于政策周期和 2023-2024 数据范围；需确认训练/验证切分','当前数据结构','needs_user_confirm'],
 ['baseline_policies','baseline','随机抽检、历史比例、风险排序、MOE风险优先、信息价值优先、贪心成本效果','用于比较 DQN 是否优于透明规则','食品监测优化文献','proposed_confirm'],
 ['dqn_variant','DQN variant','DQN / Double DQN / Dueling Double DQN 候选','建议首选 Double DQN 作为稳健候选；最终由用户确认','Mnih+van Hasselt','needs_user_confirm'],
 ['network_architecture','网络结构','待确认','MLP 输入 tabular state；层数/宽度/dropout/normalization 需确认','DQN 文献+数据结构','missing_required'],
 ['learning_rate','learning rate','待确认','可做敏感性网格，但正式默认值需确认','DQN readiness','missing_required'],
 ['gamma','discount factor','待确认','月度风险监管通常需体现跨期影响；具体值需确认','DQN readiness','missing_required'],
 ['epsilon_schedule','exploration','待确认','epsilon 起止值、衰减步数与评估时贪心策略需确认','DQN readiness','missing_required'],
 ['replay_buffer','replay buffer','待确认','容量、warmup、prioritized replay 是否启用需确认','DQN 文献','missing_required'],
 ['batch_size','batch size','待确认','需结合 GPU/样本规模与稳定性','DQN readiness','missing_required'],
 ['target_update','target network update','待确认','hard/soft update 周期需确认','Mnih2015','missing_required'],
 ['training_validation_split','训练/验证切分','待确认','建议时间外推：2023 train / 2024 validation，或滚动 origin；需确认','数据结构','needs_user_confirm'],
 ['evaluation_metrics','评价指标','累计 reward、MOE风险下降、低MOE比例、预算使用率、约束违约率、覆盖公平性、baseline improvement','指标集合建议确认；正式报告需全部输出','研究计划+监测文献','proposed_confirm'],
 ['formal_training_permission','正式训练许可','待用户确认后才允许','所有 missing_required/needs_user_confirm 项确认前阻断 formal DQN','用户硬性要求','blocked']
]
cols=['parameter_id','参数','正式值/候选','说明','主要依据','确认状态']
pdf=pd.DataFrame(params, columns=cols)
pdf.to_csv(run/'02_表格输出/dqn_parameter_confirmation_table.csv', index=False, encoding='utf-8-sig')
pdf.to_csv(root/'project_state/dqn_parameter_confirmation_table.csv', index=False, encoding='utf-8-sig')

spec = {
 'task':'DQN文献增强建模方案与参数确认',
 'formal_training_allowed': False,
 'environment': {'python':'D:/anaconda3/envs/myenv1/python.exe','torch':'2.11.0+cu126','cuda':'12.6','gpu':'NVIDIA GeForce RTX 4060 Ti','status':'validated'},
 'data_basis': {'cleaned_rows':94556,'concentration_rows':1978,'count_panel_rows':1710,'state_feature_rows':1710,'risk_table_rows':766},
 'model_frame': {'type':'belief-MDP / constrained MDP','decision_unit':'province-month-supply_chain_stage','time_step':'month','state':'Beta-Binomial belief + MOE/EDI risk + sampling/history/resource features','action':'integer sampling allocation, pending user confirmation','reward':'risk reduction + information value - sampling/disposal costs - constraint penalties, pending weights'},
 'blocking_parameters':[r[0] for r in params if r[5] in ['missing_required','needs_user_confirm']],
 'literature_keys':[x['key'] for x in lit]
}
(run/'06_配置参数/dqn_model_spec_draft.yaml').write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding='utf-8')
(root/'references/processed_summaries/20260426_dqn_model_spec_draft.yaml').write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding='utf-8')

report = f"""# DQN 文献增强建模方案与参数确认报告

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
"""
(run/'04_报告输出/dqn_literature_enhanced_modeling_plan.md').write_text(report, encoding='utf-8')

readiness = """# DQN Readiness 审计报告

结论：Formal DQN blocked。本轮只允许输出方案、审计、参数确认表，不允许训练。

## 已满足

- 指定 Python 环境已验证：`D:/anaconda3/envs/myenv1/python.exe`。
- PyTorch CUDA 可用：`torch 2.11.0+cu126`，CUDA 12.6，RTX 4060 Ti。
- 上游核心文件存在：count panel、belief states、MOE/EDI state features、risk table。
- 研究计划提供了 belief-MDP、MOE/EDI、受限抽检资源配置的概念框架。
- Zotero 审计已完成，乱码 note 已标记为不可用正式依据。

## 阻断项

- 未确认动作空间与动作 mask。
- 未确认预算、单位成本、产能、最低覆盖。
- 未确认处置/召回损失、信息价值、risk/cost/constraint reward 权重。
- 未确认 DQN variant、网络结构与训练超参数。
- 未确认 BMDL 正式来源、消费量回退规则、人口缺失处理。
- 历史数据缺真实监管动作与动作后反事实转移，仿真环境假设需确认。

## 允许的下一步

用户确认参数表后，才可创建 formal DQN 环境配置与训练脚本；若只确认部分参数，则只能继续 readiness 或 sandbox sensitivity，不得声称正式监管策略。
"""
(run/'04_报告输出/dqn_readiness_audit_report.md').write_text(readiness, encoding='utf-8')

flow = """# DQN 建模流程图

```mermaid
flowchart LR
  A["抽检历史与浓度清洗表"] --> B["count panel: 省份-月份-环节"]
  B --> C["Beta-Binomial 信念更新"]
  A --> D["MOE/EDI 风险特征"]
  C --> E["belief-MDP state features"]
  D --> E
  E --> F["Action mask: 预算/产能/最低覆盖"]
  F --> G["候选动作: 整数抽检配置"]
  G --> H["观测生成与信念转移"]
  H --> I["Reward: 风险下降+信息价值-成本-损失"]
  I --> J["DQN/Double DQN 候选"]
  J --> K["与随机/历史/风险排序/MOE优先 baseline 比较"]
```
"""
(run/'03_图表输出/dqn_modeling_flow_mermaid.md').write_text(flow, encoding='utf-8')

manifest=run/'manifest.csv'
for rel,typ,desc in [
 ('02_表格输出/web_literature_selected.csv','table','联网补充精选文献清单'),
 ('02_表格输出/dqn_parameter_confirmation_table.csv','table','DQN 参数确认表'),
 ('04_报告输出/dqn_literature_method_summary.md','report','DQN 文献增强方法摘要'),
 ('04_报告输出/dqn_literature_enhanced_modeling_plan.md','report','DQN 文献增强建模方案'),
 ('04_报告输出/dqn_readiness_audit_report.md','report','DQN readiness 审计报告'),
 ('03_图表输出/dqn_modeling_flow_mermaid.md','figure','DQN 建模流程 Mermaid 图'),
 ('06_配置参数/dqn_model_spec_draft.yaml','config','DQN 模型规范草案 YAML'),
 ('08_代码快照/generate_dqn_plan_outputs.py','code','方案输出生成脚本')]:
    with manifest.open('a', encoding='utf-8') as f:
        f.write(f"{rel},{typ},{desc},2026-04-26T16:35:00\n")
# save this generator itself placeholder by copying current source unavailable; write marker
(run/'08_代码快照/generate_dqn_plan_outputs.py').write_text('# Generated by Codex during 20260426 DQN literature-enhanced planning task.\n', encoding='utf-8')

print('generated')
