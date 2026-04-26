---
name: document-governed-modeling
description: Enforce user-document-first modeling for DQN, POMDP, belief-MDP, reinforcement learning, optimization, or other formal modeling tasks. Use before setting model state, action, reward, constraints, transitions, or training hyperparameters.
---

# Document-Governed Modeling

## When To Trigger

Use before any DQN, POMDP, belief-MDP, reinforcement learning, optimization, simulation, or formal model setup task.

## Required Inputs

Read user-provided research plans, model specification documents, processed summaries, project memory, and relevant Zotero/deepread notes before proposing model settings.

## Rules

- User documents outrank Codex defaults, generic ML experience, external papers, and previous sandbox prototypes.
- Do not convert a sandbox/prototype assumption into a formal setting without explicit user confirmation.
- Do not invent formal state, action, reward, constraint, transition, or training hyperparameter values.
- If a document gives only conceptual guidance, record it as `conceptual_only` and list the missing value for user confirmation.
- If a document gives an exact value, cite the document evidence and still flag whether the user wants to treat it as formal.

## Outputs

Write a model-spec extraction report, a machine-readable YAML/JSON spec, and a parameter confirmation table before any formal modeling.
