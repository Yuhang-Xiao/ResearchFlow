# Code Explanations

## outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/08_代码快照/run_recommended_delete_and_dqn_revised.py

- 用途：记录或生成 DQN experimental run、质量复核、解释索引和论文草稿。
- 输入文件：最新 DQN run package、项目索引、配置、CSV、图表和文献清单。
- 输出文件：本轮任务包中的报告、表格、图表修复、DOCX 和解释索引。
- 依赖库：from __future__ import annotations; import csv; import hashlib; import json; import math; import os; import random; import shutil。
- 核心函数：rel; safe_read_text; write_text; append_text; write_csv; write_df; sha256_file; make_run_package; read_csv_rows; is_relative_to; is_cache_or_temp; is_protected_path。
- 方法逻辑：先定位输入与历史输出，再执行质量核验、解释生成、文献映射和论文输出；不修改 raw data 或 Zotero SQLite。
- 如何运行：本轮脚本使用 myenv1 Python；历史快照仅作为证据，不建议直接运行覆盖。
- 常见错误：中文路径、字体缺失、DOCX 渲染表格过宽、历史文件为空。
- 与论文关系：代码说明进入 Method/Appendix，可支撑可复现性说明。
- 人工确认：formal DQN 参数、约束和政策结论仍需用户确认。

## tools/run_dqn_output_explanation_upgrade.py

- 用途：记录或生成 DQN experimental run、质量复核、解释索引和论文草稿。
- 输入文件：最新 DQN run package、项目索引、配置、CSV、图表和文献清单。
- 输出文件：本轮任务包中的报告、表格、图表修复、DOCX 和解释索引。
- 依赖库：from __future__ import annotations; import csv; import hashlib; import json; import math; import os; import shutil; import subprocess。
- 核心函数：now_stamp; write_text; safe_read; rel; sha256_file; init_run_package; inventory_package; load_core_tables; audit_issues; choose_font; render_repair_charts。
- 方法逻辑：先定位输入与历史输出，再执行质量核验、解释生成、文献映射和论文输出；不修改 raw data 或 Zotero SQLite。
- 如何运行：本轮脚本使用 myenv1 Python；历史快照仅作为证据，不建议直接运行覆盖。
- 常见错误：中文路径、字体缺失、DOCX 渲染表格过宽、历史文件为空。
- 与论文关系：代码说明进入 Method/Appendix，可支撑可复现性说明。
- 人工确认：formal DQN 参数、约束和政策结论仍需用户确认。
