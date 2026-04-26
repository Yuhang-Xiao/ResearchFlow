# Model Output Explanations


    ## 多模型比较输出

    total_reward 越高表示在当前 reward decomposition 与 rescaling 下综合表现越好；sampling_cost_total 越高表示抽检成本更高；constraint_violation_rate 越高表示违反预算或容量约束的风险更高。

    - `Q-learning`：total_reward=471.529，mean_reward=0.2757，risk_reward_total=437.080，sampling_cost_total=108.306，constraint_violation_rate=0.000，rank=1。
- `DQN修正版`：total_reward=469.859，mean_reward=0.2748，risk_reward_total=429.850，sampling_cost_total=112.662，constraint_violation_rate=0.000，rank=2。
- `threshold/greedy uncertainty`：total_reward=468.917，mean_reward=0.2742，risk_reward_total=484.704，sampling_cost_total=135.612，constraint_violation_rate=0.000，rank=3。
- `risk-ranking top-k`：total_reward=441.661，mean_reward=0.2583，risk_reward_total=422.675，sampling_cost_total=82.350，constraint_violation_rate=0.000，rank=4。
- `uniform allocation`：total_reward=417.275，mean_reward=0.2440，risk_reward_total=348.015，sampling_cost_total=90.972，constraint_violation_rate=0.000，rank=5。
- `historical allocation`：total_reward=305.568，mean_reward=0.1787，risk_reward_total=435.415，sampling_cost_total=219.906，constraint_violation_rate=0.000，rank=6。
- `random policy`：total_reward=247.134，mean_reward=0.1445，risk_reward_total=283.677，sampling_cost_total=108.252，constraint_violation_rate=0.000，rank=7。

    ## 解释边界

    这些数值来自同一 experimental comparison protocol，但 reward 权重、预算、容量和动作空间尚未被用户确认为 formal，因此只支持探索性 Results 草稿。Q-learning 领先 DQN 说明当前状态聚合/训练轮次/奖励尺度下，表格型对照策略可能更稳定；不能据此断言 DQN 在真实监管中劣于 Q-learning。
