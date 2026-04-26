# DQN 模型设置详细说明

    > 状态：experimental setting documentation。以下内容只来自本地配置、代码快照和输出表；无法从本地文件核验的内容标为 `未核验` 或 `experimental assumption`。

    ## 1. 科研问题

    本轮 DQN 试图在 PEANUT/AFB1 风险监管场景中，为不同状态单元选择抽检加码动作，使风险覆盖、信息增益、成本和约束满足之间取得可解释的 experimental trade-off。该输出不是 formal 监管政策结论。

    ## 2. MDP / belief-MDP 近似

    - 状态来自 `data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv` 与相关 belief-state / MOE-EDI 特征。
    - transition 在当前输出中主要是基于状态序列和抽检动作的 experimental approximation；没有核验到经用户正式确认的真实监管动态转移方程。
    - belief update 使用 Beta-Binomial belief-state 作为输入证据，但本轮训练没有证明其可替代真实监管反馈闭环。

    ## 3. State

    当前配置路径：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/06_配置参数/dqn_revised_experimental_config.yaml`。状态特征来源：`data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`。状态应解释为地区、环节、风险、posterior mean/uncertainty、MOE/EDI 等信息的组合，具体字段需结合 canonical feature table 和 `state_feature_missing_summary.csv` 阅读。

    ## 4. Action

    实际训练动作空间：`coarse_discrete_action_space_with_action_mask`；动作档位：`[0, 1, 3, 5, 10]`。

    动作空间可行性：高维二元动作没有训练；配置中标记为 `not trained in this run; requires factorized/hierarchical/combinatorial method`。本轮推荐继续使用粗粒度动作空间做实验，并把高维动作留给 hierarchical RL / factorized action / combinatorial optimization。

    ## 5. Reward

    Reward decomposition：['risk_reward', 'information_gain', 'sampling_cost', 'opportunity_penalty', 'constraint_penalty']。

    - risk reward weight：2.4
    - information gain weight：0.85
    - cost weight：0.18
    - constraint penalty weight：5.0
    - rescaling：raw reward divided by robust P90 absolute valid reward then tanh

    解释风险：reward 权重仍为 experimental；formal 前必须确认成本、预算、容量、惩罚强度和风险收益尺度。

    ## 6. Constraint

    约束包括 monthly budget、local/stage/global capacity 和 action mask。当前 monthly_budget=4567。约束违约表显示本轮比较策略均无违约，但这依赖当前 action mask 与预算容量设定。

    ## 7. Training

    训练参数：episodes=300，learning_rate=0.001，gamma=0.9，batch_size=256，epsilon_start=1.0，epsilon_min=0.05，epsilon_decay=0.986，target_update_frequency=10，early_stopping=True。

    机制说明：DQN 使用 replay buffer、target network、epsilon-greedy、mini-batch update 等强化学习机制；这些机制需要结合代码快照和 training log 复核。模型 artifact 存在，但本轮不重新训练。

    ## 8. Baseline 与评价

    Baseline：DQN修正版, Q-learning, uniform allocation, historical allocation, risk-ranking top-k, random policy, threshold/greedy uncertainty。比较必须共用 state set、budget、action constraints、capacity constraints 和 metrics。核心指标包括 total_reward、risk_reward_total、information_gain_total、sampling_cost_total、constraint_violation_rate、state_coverage、rank。

    ## 9. Quality gates

    本轮新增图表 QA、表格解释、模型输出解释、代码说明、文献映射和 Results claim guard。所有结果仍标记为 experimental。
