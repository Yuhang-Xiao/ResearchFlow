# Result Interpretation Guide

    ## 阅读顺序

    1. 先读 `dqn_model_setting_detail_report.md`，确认 state、action、reward、constraint 和 training 都来自本地配置或被标记为 experimental assumption。
    2. 再读 `multi_model_policy_comparison.csv` 和 `dqn_result_interpretation_report.md`，理解 DQN、Q-learning 与 heuristic 的比较。
    3. 图表只作为解释辅助，必须回到源 CSV。
    4. Word Results 草稿只能作为 `experimental results draft`。

    ## 本轮核心结果边界

    - 当前排序最高策略：Q-learning，total_reward=471.5290948939492。
    - DQN 修正版：total_reward=469.8586740235132，排名=2。
    - 由于参数、约束、奖励权重尚未用户确认为 formal，不能写成正式监管政策建议。
