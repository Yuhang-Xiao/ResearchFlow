# DQN 结果解读报告

## 1. 整体比较

| policy | total_reward | risk_reward_total | information_gain_total | sampling_cost_total | constraint_violation_rate | rank |
| --- | --- | --- | --- | --- | --- | --- |
| Q-learning | 471.5291 | 437.0804 | 87.2321 | 108.3060 | 0.0000 | 1 |
| DQN修正版 | 469.8587 | 429.8497 | 80.3900 | 112.6620 | 0.0000 | 2 |
| threshold/greedy uncertainty | 468.9167 | 484.7041 | 105.3355 | 135.6120 | 0.0000 | 3 |
| risk-ranking top-k | 441.6613 | 422.6748 | 94.8814 | 82.3500 | 0.0000 | 4 |
| uniform allocation | 417.2752 | 348.0154 | 77.6811 | 90.9720 | 0.0000 | 5 |
| historical allocation | 305.5678 | 435.4147 | 68.7857 | 219.9060 | 0.0000 | 6 |
| random policy | 247.1343 | 283.6766 | 56.9349 | 108.2520 | 0.0000 | 7 |

当前 experimental 比较中，`Q-learning` total_reward 最高（471.529），`DQN修正版` 排名 2（total_reward=469.859）。这说明 DQN 在修正版 reward 与约束设定下已经可运行且接近最优对照，但并未超过 Q-learning。


    ## 2. 指标含义

    - total_reward：综合风险收益、信息增益、成本和惩罚后的总目标值；越高表示当前实验目标下越优。
    - risk_reward_total：覆盖风险状态带来的收益；越高说明策略更关注高风险单元。
    - information_gain_total：对不确定状态抽检带来的信息收益；越高说明策略更偏向学习。
    - sampling_cost_total：抽检成本；越高不必然更差，需要与风险收益共同看。
    - constraint_violation_rate：约束违约率；当前为 0，表示 action mask 和容量预算约束有效，但不能替代 formal 约束确认。

    ## 3. 稳定性、reward hacking 与收敛

    当前 training log 支持基本趋势审查，但本轮未重新训练；因此只能说上一轮 DQN 修正版“可运行且有收敛诊断输出”。reward hacking 未发现直接证据，但仍存在权重设定驱动策略的风险。若 formal 化，需要敏感性分析、外部验证和用户确认约束。

    ## 4. 食品安全监管启发

    Experimental 结果提示：在预算和容量约束下，风险收益、信息增益和成本之间可以形成可解释的策略比较框架；但当前输出不能直接转化为监管政策，只能作为方法探索、论文 Results 草稿和后续 formal DQN 参数确认的依据。
