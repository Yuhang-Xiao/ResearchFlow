# Method Selector

## When To Use

Use this skill after the problem is framed and before implementing modeling, statistical analysis, matching, or evaluation methods. In goal-driven autonomous mode, select appropriate baseline and advanced methods when the objective and data constraints are clear enough.

## Inputs

- Problem framing notes.
- Data shape and schema summary.
- Evaluation criteria.
- Constraints such as interpretability, compute, sample size, time ordering, or missingness.

## Outputs

- Shortlist of candidate methods.
- Recommended baseline method.
- Reasoning for including or excluding methods.
- Minimum validation plan.

## Recommended Workflow

1. Confirm the task type and metric.
2. Review data constraints and risks.
3. Start with the simplest credible baseline.
4. Add advanced candidates only when they address a real need.
5. Define how methods will be compared.
6. Proceed automatically unless the method choice is blocked by ambiguity, missing data, or a risky irreversible action.
7. Record durable method choices and assumptions in `project_state/decision_log.md`.
