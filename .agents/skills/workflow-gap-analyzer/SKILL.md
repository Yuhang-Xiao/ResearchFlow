---
name: workflow-gap-analyzer
description: Analyze local workflow capability gaps across skills, recipes, registries, CLI, project state, and references. Trigger phrases include: workflow-gap-analyzer, workflow upgrade, skill scout
---

# workflow-gap-analyzer

## Trigger Phrases

- workflow-gap-analyzer
- workflow upgrade
- skill scout

## When To Use

Use when workflow1 needs capability-gap scanning, GitHub/open-source scouting, safe local skill adaptation, upgrade planning, approval queue management, or self-review after durable tasks.

## When Not To Use

Do not use to install external code, start MCP servers, write Zotero databases, call API keys, train models, run DQN, modify raw data, delete unique files, or change formal model parameters without explicit user confirmation.

## Inputs

- Current run package.
- `workflow_improvement/` policies.
- Local `.agents/skills/`, `workflow_recipes/`, `model_registry/`, `src/workflow1/`, `project_state/`.
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

Follow `workflow_improvement/safe_patch_policy.yaml`.

## Auto-Allowed Actions

Add local skills, recipes, registry entries, lightweight stubs, reports, ledgers, approval plans, and dry-run validation.

## Approval-Required Actions

Installing MCP/plugins, using API keys, writing Zotero, dependency installation, long-running services, executing third-party scripts, formal model parameter changes.

## Project State Updates

Update `project_state/current_focus.md`, `next_step.md`, `decision_log.md`, `changelog.md`, `lessons_learned.md`, `conversation_handoff.md`, `project_memory.md`, and `run_protocol.md` when durable.

## Run Package Outputs

Write scout reports, gap tables, evaluation matrices, applied upgrade logs, approval queue snapshots, and dry-run results to the active run package.
