---
name: goal-driven-research-orchestrator
description: Route one-line research launch commands into workflow1 using project memory, references, raw inventory, registries, recipes, and relevant skills.
---

# Goal-driven Research Orchestrator

## When To Trigger

Use this skill when the user provides raw data plus a research goal, asks to continue a previous workflow, or gives a one-line command that implies data cleaning, modeling, visualization, reporting, simulation, optimization, or project continuation.

## First Files To Read

1. `START_HERE.md`
2. `project_state/project_memory.md`
3. `project_state/run_protocol.md`
4. `project_state/current_focus.md`
5. `project_state/next_step.md`
6. `project_state/decision_log.md`
7. `project_state/lessons_learned.md`
8. `project_state/conversation_handoff.md`
9. `references/processed_summaries/`
10. raw data inventory from `data/01_raw`
11. relevant files under `references/`
12. relevant skills under `.agents/skills/`

## Default Flow

Reference reading, intake, validation, cleaning plan, cleaning, label engineering, EDA, model framing, baseline modeling, tuning/comparison, simulation or optimization feasibility, visualization, report generation, project memory update, and conversation handoff.

Only execute stages that are appropriate, implemented, and requested by the user goal. Do not treat planning as actual cleaning.

## Safety

Verify upstream data before downstream modeling. Stop for missing raw data, non-operational goals, unidentifiable core fields, destructive raw-data actions, secrets, external authorization, or sensitive-data decisions.
