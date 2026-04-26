---
name: dqn-readiness-auditor
description: Audit readiness before formal DQN or constrained DQN. Use to check state, observation, action, masks, budget, capacity, cost, reward, transitions, belief update, episodes, training hyperparameters, baselines, metrics, and required user confirmations.
---

# DQN Readiness Auditor

Formal DQN cannot run until state, observation, action, action mask, budget, capacity, cost, reward, transition, belief update, episode, network, exploration, replay, baseline, metric, and stopping rules are specified or confirmed by the user.

If anything is missing, write a readiness report and parameter confirmation table instead of training.
