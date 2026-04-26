# DQN 输出复核、解释体系与论文输出升级

        ## 任务目标

        系统复核当前 DQN、Q-learning、heuristic、图表、表格、模型输出、代码、论文输出和文献/Zotero 工作流，并把解释、图表 QA、代码说明、模型说明、论文 section 输出和 workflow self-improvement 固化到长期规则。

        ## 输入来源

        - 最新 DQN 修正版 experimental 包：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练`
        - 历史对照 DQN 自动参数训练包：`outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`
        - 项目索引：`outputs/_index/`
        - 项目状态：`project_state/`
        - references / Zotero sidecar 目录

        ## 主要输出

        - deep audit：`04_报告输出/deep_dqn_output_audit_report.md`
        - 解释索引：`10_输出解释与索引/`
        - 图表 QA 与修复：`02_表格输出/chart_quality_audit.csv`、`03_图表输出/*explained.png`
        - DQN 设置与结果解读：`04_报告输出/dqn_model_setting_detail_report.md`、`dqn_result_interpretation_report.md`
        - 文献/Zotero 安全侧车：`dqn_core_literature.bib`、`dqn_core_literature.ris`、`zotero_writeback_or_import_plan.csv`
        - 论文级 Results：`09_论文输出/04_结果/dqn_results_draft.md`、`09_论文输出/09_word导出/dqn_results_draft.docx`

        ## 尚未解决问题

        当前 DQN 仍为 experimental。formal DQN 仍需确认状态、动作、reward 权重、预算、容量、约束、transition、训练轮次、外部验证和敏感性分析。

        ## 下一步建议

        先由用户确认 formal DQN 参数表，再生成 Method / Introduction / Literature Review / Discussion 的论文级 section。
