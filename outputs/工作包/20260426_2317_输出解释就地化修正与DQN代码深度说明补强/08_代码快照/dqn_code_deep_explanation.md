# DQN 代码深度说明

    ## 总体流程

    `run_recommended_delete_and_dqn_revised.py` 同时承担缓存清理、环境核验、上游数据检查、DQN 修正版 experimental training、多模型比较、图表生成、报告生成、论文 Results 草稿和索引更新。它不是 formal DQN 训练脚本，而是一次 experimental workflow orchestration。

    ## State 构建

    `build_mapping()` 负责识别状态表字段；`prepare_model_data()` 将 canonical PEANUT belief-MDP/MOE-EDI 特征转换为模型输入，包括 state matrix、risk score、uncertainty、month/group key。对应论文 Method 的 state representation。当前 state 仍依赖已有 feature table，formal 前需确认所有字段含义、单位和缺失处理。

    ## Action 定义

    `ACTION_VALUES = [0, 1, 3, 5, 10]` 是粗粒度抽检加码动作。`build_valid_actions()` 把动作档位和容量上限结合为 action mask。高维二元 action 未训练，仍需 hierarchical/factorized/combinatorial 方案。

    ## Reward 计算

    `build_reward_matrix()` 是核心 reward function：risk reward 与 information gain 为正项，sampling cost、opportunity penalty、constraint penalty 为惩罚项，并用 robust scale + `tanh` 重标度。该函数对应论文 Method 的 reward decomposition。所有权重仍是 experimental，formal 前必须确认。

    ## Constraint 处理

    `build_capacity()`、`capacity_for_row()`、`build_valid_actions()` 和 `evaluate_policy()` 共同处理约束。`evaluate_policy()` 还会在 monthly remaining budget 与 capacity 下调整不可行动作，并统计 constraint violation / adjustment。当前所有策略违约为 0，但这依赖 action mask 和预算容量设定。

    ## DQN 训练

    `QNet` 定义 Q-network；`train_dqn()` 负责 model/target network、epsilon-greedy、batch update、target update、epsilon decay、training log、early stopping 相关逻辑。该训练是 experimental，不允许直接作为 formal policy optimizer。

    ## Q-learning 与 heuristic baseline

    `train_qlearning()` 用聚合状态构建 Q-learning baseline；`build_baseline_actions()` 生成 uniform、historical、risk-ranking top-k、random、threshold/greedy uncertainty 等 baseline。`evaluate_policy()` 使用统一 protocol 比较所有策略。

    ## 输出、图表与 Word

    `model_outputs()` 组织训练和比较；`generate_charts()` 生成 PNG 主图；`create_reports()` 写训练/审计/质量报告；`create_results_draft()` 写 experimental Results draft 和 DOCX；`sync_outputs()` 同步必要 canonical 副本。

    ## 与论文 Method / Results 的关系

    - Method：state/action/reward/constraint/training/baseline/evaluation 由代码函数和配置共同支撑。
    - Results：multi-model comparison、reward curve、constraint summary、policy table、quality gates 和 evidence table 支撑 Results 草稿。
    - Discussion：局限性来自 experimental boundary、reward 权重、transition 近似、约束确认和外部验证缺口。
