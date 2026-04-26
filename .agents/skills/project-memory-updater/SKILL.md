---
name: project-memory-updater
description: Update workflow1 project memory, lessons learned, conversation handoff, next step, changelog, and decision log after each durable task.
---

# Project Memory Updater

## When To Use

Use this skill at the end of any task that changes durable project understanding, workflow rules, data decisions, modeling decisions, reference guidance, outputs, or next steps.

## Responsibilities

- Check whether `project_state/project_memory.md` needs durable updates.
- Write new data, cleaning, modeling, literature, visualization, or workflow lessons to `project_state/lessons_learned.md`.
- Update `project_state/conversation_handoff.md` for complex work or likely context transitions.
- Keep `project_state/next_step.md` short and actionable.
- Append notable changes to `project_state/changelog.md`.
- Append durable decisions and rationale to `project_state/decision_log.md`.

## Rules

- Do not rewrite history casually.
- Append dated entries unless the user requests cleanup.
- Keep long-term memory concise and reusable.
- Do not store secrets, private identifiers, or unnecessary raw-data details in memory files.

## Run Package And Cleanup Requirement

任务开始前调用 `run-package-manager` 创建任务工作包；任务结束后调用 `whole-workspace-organizer` 做全目录整理检查。以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。

## Document-Governed DQN Memory Rule

After any DQN, POMDP, belief-MDP, constrained RL, or safe RL preparation task, record in project state whether:

- user research documents were fully read;
- Zotero notes and PDFs were audited, including any `?????` encoding problems;
- Python and `torch` availability were checked in the requested interpreter, not only the default Python;
- formal DQN is blocked or allowed;
- the parameter confirmation table has been generated and which parameters still need user confirmation.

Do not mark formal DQN as ready until the user has confirmed state, action, reward, constraints, transition assumptions, training hyperparameters, and the formal Python interpreter.
