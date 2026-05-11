---
name: environment-auditor
description: Check Python, torch, CUDA, and required packages before DQN or other model execution. Use when a task mentions environments, torch, Python interpreters, or model training readiness.
---

# Environment Auditor

## Required Checks

- Check the default Python interpreter.
- Check any user-specified interpreter exactly as provided.
- If the specified interpreter is missing, search nearby environment directories and record possible spelling/path differences without silently substituting.
- Check `torch`, `torch.cuda.is_available()`, and core packages required by the planned workflow.
- Do not downgrade formal DQN to sklearn just because default Python lacks torch.

## Outputs

Write an environment audit report and a CSV table of commands, return codes, stdout, stderr, and readiness judgment.
