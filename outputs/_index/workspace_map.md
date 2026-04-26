# Workspace Map

## 主查看入口

- `outputs/工作包/`：按 `YYYYMMDD_HHMM_中文任务名` 组织的任务工作包。
- `outputs/_index/`：全局任务索引、run manifest、canonical 输出索引和删除日志。
- `outputs/_待复核/`：无法自动判断归属但唯一的文件。

## 标准目录职责

- `data/01_raw/`：不可修改原始数据。
- `data/03_primary/`：项目级 canonical 清洗主表。
- `data/04_feature/`：pipeline 必须直接读取的 canonical 特征。
- `reports/项目级索引与摘要/`：项目级摘要和入口报告。
- `experiments/`：项目级实验入口和 canonical 实验索引。
- `references/`：研究计划、文献、标准、方法和笔记。
- `archive/`：历史、旧目录和已迁移辅助体系。
