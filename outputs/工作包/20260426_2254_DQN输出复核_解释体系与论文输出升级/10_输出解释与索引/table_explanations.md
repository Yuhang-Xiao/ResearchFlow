# Table Explanations

## multi_model_policy_comparison.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/multi_model_policy_comparison.csv`
- 行列规模：7 行，17 列。
- 字段解释：policy, total_reward, mean_reward, risk_reward_total, information_gain_total, sampling_cost_total, opportunity_penalty_total, constraint_penalty_total, constraint_violation_count, constraint_violation_rate, constraint_adjustment_count, mean_action ...。
- 主要发现：共比较 7 个策略；最高 total_reward 策略为 Q-learning。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## multi_model_metric_summary.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/multi_model_metric_summary.csv`
- 行列规模：7 行，17 列。
- 字段解释：policy, total_reward, mean_reward, risk_reward_total, information_gain_total, sampling_cost_total, opportunity_penalty_total, constraint_penalty_total, constraint_violation_count, constraint_violation_rate, constraint_adjustment_count, mean_action ...。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## baseline_fairness_check.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/baseline_fairness_check.csv`
- 行列规模：7 行，8 列。
- 字段解释：policy, same_state_set, same_budget, same_action_constraints, same_capacity_constraints, same_evaluation_metrics, fairness_status, experimental_label。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## reward_component_summary.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/reward_component_summary.csv`
- 行列规模：7 行，9 列。
- 字段解释：policy, risk_reward_total, information_gain_total, sampling_cost_total, opportunity_penalty_total, constraint_penalty_total, rescaled_total_reward, reward_negative, negative_reward_interpretation。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## convergence_diagnosis_summary.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/convergence_diagnosis_summary.csv`
- 行列规模：6 行，3 列。
- 字段解释：metric, value, status。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## constraint_violation_summary.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/constraint_violation_summary.csv`
- 行列规模：7 行，5 列。
- 字段解释：policy, constraint_violation_count, constraint_violation_rate, constraint_adjustment_count, monthly_budget。
- 主要发现：所有策略违约计数为 0；这是约束满足信号，不是缺失。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## chart_quality_audit.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/chart_quality_audit.csv`
- 行列规模：9 行，10 列。
- 字段解释：chart_id, path, source_data, format, exists, size_bytes, nonblank, pixel_std, chinese_font, qa_status。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## research_quality_gate_results.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/research_quality_gate_results.csv`
- 行列规模：14 行，3 列。
- 字段解释：gate, status, evidence。
- 主要发现：质量门控记录 14 项，其中约 14 项显示通过/可用。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## action_space_options.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/02_表格输出/action_space_options.csv`
- 行列规模：3 行，7 列。
- 字段解释：action_space, definition, dimension, trainability, combination_explosion, needs_advanced_method, this_run_recommendation。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## dqn_revised_training_log.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/05_模型与实验/dqn_revised_training_log.csv`
- 行列规模：281 行，10 列。
- 字段解释：episode, total_reward, moving_average_reward, mean_loss, epsilon, mean_action, constraint_violation_rate, device, gpu, elapsed_seconds。
- 主要发现：训练日志包含 281 条记录，用于 reward、loss、epsilon 与收敛诊断。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## qlearning_training_log.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/05_模型与实验/qlearning_training_log.csv`
- 行列规模：300 行，4 列。
- 字段解释：episode, total_reward_proxy, epsilon, state_bins。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。

## experiment_ledger.csv

- 数据来源：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/05_模型与实验/experiment_ledger.csv`
- 行列规模：1 行，10 列。
- 字段解释：experiment_id, created_at, label, status, run_package, policy_csv, model_path, formal_or_experimental, episodes, gpu。
- 主要发现：保存本轮 DQN experimental 输出的结构化证据。
- 局限性：表格仅反映当前 experimental 配置与本地数据输出；正式论文使用前需通过 evidence map 和质量门控。
