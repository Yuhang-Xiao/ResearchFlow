---
name: dqn-readiness-auditor
description: Audit readiness before formal DQN or constrained DQN. Use to check state, observation, action, masks, budget, capacity, cost, reward, transitions, belief update, episodes, training hyperparameters, baselines, metrics, and required user confirmations.
---

# DQN Readiness Auditor

## Required Checks

Before formal DQN, verify:

- state and observation definitions
- action space and action mask
- budget and capacity constraints
- unit sampling cost and allocation rule
- recall/disposal loss, risk loss, information value, reward weights
- transition logic and belief update
- time step and episode definition
- baseline policies, network structure, replay buffer, exploration, hyperparameters
- evaluation metrics, visualization outputs, stopping conditions
- user-provided parameters still missing

## Stop Rule

If any formal DQN parameter is missing or only a prototype assumption, do not train. Produce a readiness report and parameter confirmation table.
