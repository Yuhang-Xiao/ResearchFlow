---
name: workflow-self-improvement-scout
description: Scan workflow1 gaps and search GitHub/open-source projects for safe workflow upgrades. Trigger phrases include: optimize workflow, upgrade workflow, let Codex find useful skills, search GitHub for workflow improvements, expand automated research capability, self-improve workflow, workflow upgrade, skill scout, one-line research workflow
---

# workflow-self-improvement-scout

## Trigger Phrases

- optimize workflow
- upgrade workflow
- let Codex find useful skills
- search GitHub for workflow improvements
- expand automated research capability
- 优化工作流
- 升级工作流
- 让 Codex 寻找可用技能
- 搜索 GitHub 改进工作流
- 扩展自动科研能力
- self-improve workflow
- workflow upgrade
- skill scout
- one-line research workflow

## When To Use

Use when workflow1 needs capability-gap scanning, GitHub/open-source scouting, safe local skill adaptation, upgrade planning, approval queue management, or self-review after durable tasks.

## When Not To Use

Do not use to install external code, start MCP servers, write Zotero databases, call API keys, train models, run DQN, modify raw data, delete unique files, or change formal model parameters without explicit user confirmation.

## Inputs

- Current run package.
- `framework/workflow_improvement/` policies.
- Local `.agents/skills/`, `framework/workflow_recipes/`, `framework/model_registry/`, `src/workflow1/`, `project_state/`.
- GitHub/open-source candidate summaries.

## Outputs

- Candidate matrix and upgrade action plan.
- Local SKILL.md/recipe/stub patches when safe.
- Approval queue entries for high-risk upgrades.
- Improvement ledger rows.
- Project state updates.

## Required Checks

- Confirm no raw data or formal config is modified.
- Check license/documentation before adapting external ideas.
- Prefer local lightweight adaptation over code copying.
- Run dry-run and skills-doctor after changes.

## Safety Boundaries

Follow `framework/workflow_improvement/safe_patch_policy.yaml`.

## Auto-Allowed Actions

Add local skills, recipes, registry entries, lightweight stubs, reports, ledgers, approval plans, and dry-run validation.

## Approval-Required Actions

Installing MCP/plugins, using API keys, writing Zotero, dependency installation, long-running services, executing third-party scripts, formal model parameter changes.

## Project State Updates

Update `project_state/current_focus.md`, `next_step.md`, `decision_log.md`, `changelog.md`, `lessons_learned.md`, `conversation_handoff.md`, `project_memory.md`, and `run_protocol.md` when durable.

## Run Package Outputs

Write scout reports, gap tables, evaluation matrices, applied upgrade logs, approval queue snapshots, and dry-run results to the active run package.
