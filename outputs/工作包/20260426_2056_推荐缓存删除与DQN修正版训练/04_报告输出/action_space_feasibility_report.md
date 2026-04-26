# 动作空间可行性报告

本轮状态数为 1710，月份数为 24。高维二元动作空间的组合规模约为 `2^1710`，不适合在当前 experimental run 中直接训练。

## 结论

本轮采用粗粒度 `[0, 1, 3, 5, 10]` 档位动作空间，并用 action mask、月度预算和 capacity 约束保证可行性。中等粒度 top-k 分配适合作为下一步升级；高维二元动作空间应先转化为 factorized action、hierarchical RL 或预算约束下的组合优化后处理，再进入训练。

详见 `02_表格输出/action_space_options.csv`。
