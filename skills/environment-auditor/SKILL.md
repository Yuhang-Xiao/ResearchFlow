---
name: environment-auditor
description: Check Python, torch, CUDA, and required packages before DQN or other model execution. Use when a task mentions environments, torch, Python interpreters, or model training readiness.
---

# Environment Auditor

Check default Python and the exact user-specified interpreter. If the specified path is missing, record that fact and any nearby candidate environment separately. Do not silently substitute interpreters or downgrade formal DQN to sklearn.
