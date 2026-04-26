# DQN Code Method Notes

    本代码对应 Method 写作时应拆成：数据与 state features、action space、reward decomposition、constraints/action mask、DQN training、Q-learning baseline、heuristic baselines、evaluation protocol、quality gates、experimental boundary。

    不应把代码写成“自动得到最优监管政策”。准确表述应为：在本地 PEANUT belief-MDP/MOE-EDI 特征和 experimental reward/constraint 设置下，训练并比较 DQN、Q-learning 与多种 heuristic baseline。
