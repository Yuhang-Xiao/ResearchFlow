---
name: reward-convergence-constraint-auditor
description: Use when the task mentions reward audit, convergence check, constraint violation. It enforces workflow1 research quality gates and produces Chinese-first audit outputs.
---

# Reward Convergence Constraint Auditor

## Trigger Phrases

- reward audit
- convergence check
- constraint violation

## When To Use

Use for scientific workflow tasks that need research-quality validation, top-journal benchmarking, citation checking, model comparison, paper section QA, or workflow-quality memory updates.

## When Not To Use

- Do not use to run formal DQN/RL training without user-confirmed parameters.
- Do not use to modify `data/01_raw`.
- Do not install external tools, MCP servers, APIs, large dependencies, or write Zotero databases without approval.

## Inputs

- Current task run package.
- Relevant `research_quality/*.yaml` policy files.
- Source data, derived tables, model logs, charts, paper drafts, or citation metadata as applicable.
- `project_state/` and latest `outputs/_index/` files.

## Outputs

- Chinese audit report in the task package.
- CSV quality gate table or issue log.
- Repair log when auto-repair is safe.
- Approval queue entries for high-risk external integrations.

## Required Checks

- Verify lineage/evidence before accepting results.
- Distinguish prototype, experimental, evidence-supported, and formal-ready outputs.
- Check table/report/chart/model/citation consistency according to the matching policy.
- Record stop conditions and next step in `project_state`.

## Stop Conditions

- Missing critical input.
- Unresolved data lineage or citation failure needed for a formal claim.
- User confirmation required for formal DQN/RL parameters, policy conclusions, Zotero database writes, MCP/plugin/API installation, or large dependency installation.

## Project State Updates

Update `project_state/project_memory.md`, `lessons_learned.md`, `conversation_handoff.md`, `next_step.md`, `changelog.md`, and `decision_log.md` when the audit creates durable rules, blockers, or outputs.
