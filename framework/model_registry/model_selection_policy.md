# Model Selection Policy

workflow1 must infer the task type from the research goal, target column, data profile, temporal/group/spatial structure, imbalance, zero inflation, and available dependencies. The user does not need to name a model.

Selection order:

1. Confirm target and task type.
2. Load `task_to_model_map.yaml`, metrics, validation, explainability, figure/table, literature, failure, and repair maps.
3. Always include a transparent baseline.
4. Add at least one interpretable control and one stronger candidate when dependencies allow.
5. Treat AutoML as a benchmark/candidate generator, not as a replacement for scientific reasoning.
6. If a dependency is missing, write an approval plan and use local fallback.
7. Never use GitHub/HF/OpenML as academic evidence; they are engineering references only.
8. Failed gates create repair actions before final product packaging.
