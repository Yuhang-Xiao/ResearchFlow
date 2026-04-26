---
name: artifact-organizer
description: Route workflow1 artifacts into run packages, keep standard directories canonical-only, and trigger whole-workspace cleanup.
---

# Artifact Organizer

所有任务产物必须进入当前任务工作包。标准目录只保存 canonical 和 pipeline 必需文件。任务开始前调用 `run-package-manager`，任务结束后调用 `whole-workspace-organizer`。

长期规则：以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。
