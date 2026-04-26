# Run Package Policy Snapshot

## Run Package First Policy

1. 每次实质性科研任务开始前，必须先创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
2. 本轮任务产生的所有文件必须优先写入该任务工作包。
3. 标准目录只保存 canonical/latest 和 pipeline 必需文件。
4. 不允许把任务结果直接散落到 `reports/`、`data/04_feature/`、`experiments/` 根目录。
5. 如果某个结果需要被后续流程读取，可以同时复制到标准目录作为 canonical 文件。
6. 每个任务工作包必须包含 README 和 manifest。
7. 每次任务完成后必须更新 run index、run manifest、latest canonical outputs、artifact index 和 workspace structure。
8. 无法归属但唯一的文件进入 `outputs/_待复核/`。
9. hash 完全重复的文件应删除重复副本并记录。
10. 新对话继续任务时，应先读取最新 `outputs/_index/run_index.md` 和 `project_state/conversation_handoff.md`。

长期规则：以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。
