# Explanation Simplification Report

        ## 为什么 08_代码快照和其他目录有很多 md

        上一轮为了满足“就地解释”和“同名 explanation”要求，机械地给几乎每个 CSV/PNG/MD/DOCX 生成 `.explanation.md`，还给每个目录生成 `_local.md`。这导致解释文件数量膨胀，读者需要在说明文件之间来回跳转，反而降低可读性。

        ## 本轮处理原则

        - 保留目录 README：让用户在目录内知道看什么。
        - 保留核心 DQN 代码说明：`README_DQN代码总览.md`、`dqn_code_deep_explanation.md`、`dqn_code_to_model_setting_map.csv`、`dqn_code_to_outputs_map.csv`。
        - 删除批量生成的同名 `.explanation.md` 和重复 `_local.md`。
        - 不删除核心数据、最新 DQN 训练包、project_state、raw data 或 canonical outputs。

        ## 删除概况

        - 删除记录数：1
        - 释放空间：0.03 MB
        - 删除日志：`02_表格输出/deleted_redundant_outputs_log.csv`

        ## Word 升级

        新 Word：`outputs/工作包/20260426_2336_输出解释精简_项目存档与Word学术升级/09_论文输出/09_word导出/dqn_results_academic_with_figures.docx`，包含多模型比较表和核心 PNG 图表，写法调整为学术 Results 草稿，但仍明确标注 experimental。

        ## 项目存档

        存档：`archive/project_snapshots/workflow1_curated_project_snapshot_20260426_2336.zip`。
