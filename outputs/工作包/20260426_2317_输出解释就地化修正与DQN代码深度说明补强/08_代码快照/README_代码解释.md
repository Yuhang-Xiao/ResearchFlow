# 代码快照解释

本目录说明：包含 DQN 代码快照、深度代码说明、函数级映射和复现性 notes。

## 文件说明
- `dqn_code_deep_explanation.md`：DQN 代码深度说明。
- `dqn_code_function_inventory.csv`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_code_method_notes.md`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_code_reproducibility_notes.md`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `dqn_code_to_model_setting_map.csv`：代码函数到 state/action/reward/constraint/training/evaluation 的映射。
- `dqn_code_to_outputs_map.csv`：代码函数到输出文件的映射。
- `run_recommended_delete_and_dqn_revised.py`：辅助 artifact；请结合同名 explanation 或 local explanation 阅读。
- `run_recommended_delete_and_dqn_revised_annotated.py`：带文件头说明的 DQN 修正版训练与输出脚本快照。

## 阅读规则

1. 本目录 README 是就地解释，不需要先跳到 `10_输出解释与索引/` 才能读懂。
2. 关键 artifact 均尽量配套同名 `.explanation.md`。
3. DQN 相关输出全部保持 experimental；不能作为 formal 监管政策结论。
4. 用户下一步应优先阅读本目录 README、关键同名 explanation、再回到总索引查看跨目录关系。
