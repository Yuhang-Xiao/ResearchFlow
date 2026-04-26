# Zotero 文献审计报告

- 扫描根目录：`D:\桌面\codex\zotero`
- 候选文献/笔记/PDF 数：34
- 乱码或读取问题数：5

## 乱码/读取问题
- `data\candidates\first_round_candidates.csv`: garbled_note (?????=2; replacement=0)
- `data\candidates\master_candidates.csv`: garbled_note (?????=1; replacement=0)
- `data\deepreads\20260425_Human-level control through deep reinforcement learning.md`: garbled_note (?????=40; replacement=0)
- `data\screened\first_round_selected.csv`: garbled_note (?????=2; replacement=0)
- `data\screened\screened_library.csv`: garbled_note (?????=1; replacement=0)

## 可用性原则
含 `?????` 或 replacement character 的 Zotero note 不作为正式 DQN 建模依据；若该文献重要，应追溯 PDF 全文、出版页面或重新生成无乱码中文笔记。

完整清单见 `02_表格输出/zotero_literature_inventory.csv`；问题日志见 `07_日志与错误/zotero_encoding_pdf_issue_log.csv`。