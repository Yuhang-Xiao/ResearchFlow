---
name: skill-scout-and-upgrader
description: Search and evaluate open-source skills, agents, workflows, and automation patterns, then propose minimal safe upgrades for workflow1 without blindly copying code.
---

# Skill Scout and Upgrader

## When To Use

Use this skill when existing workflow skills are insufficient for a task, or when the user asks to search GitHub/open-source communities for better skills, agents, research workflows, PDF reading workflows, Zotero automation, machine learning workflows, or reinforcement learning experiment workflows.

## Search Priorities

- Stars and community adoption.
- Recent maintenance activity.
- Clear README and examples.
- Explicit license.
- Fit for food-safety data cleaning, ML, XGBoost, POMDP, reinforcement learning, PDF/deep reading, Zotero automation, visualization, or scientific workflow orchestration.

## Rules

- Prefer primary project repositories and official documentation.
- Do not blindly copy code into this repo.
- Extract design ideas, folder structures, checklist patterns, and reusable workflow concepts.
- If no suitable project exists, create a small local skill with clear scope.
- Record new or modified skills in `project_state/decision_log.md` and `project_state/changelog.md`.

## Outputs

- `reports/skill_scout_report.md`
- Recommended additions or modifications to local `SKILL.md` files.
- A short list of rejected options and reasons when relevant.

