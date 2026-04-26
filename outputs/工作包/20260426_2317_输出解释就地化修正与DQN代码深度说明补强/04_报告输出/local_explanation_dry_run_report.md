# Local Explanation Dry-run Report

## 为每个输出目录生成本地解释

- 状态：pass

```text
 'no_real_data_processing': True, 'no_model_training': True, 'no_dqn_execution': True, 'run_package_required': True, 'project_state_update_required': True, 'selected_recipe': 'workflow_recipes/local_explanation_colocation_workflow.yaml', 'required_inputs': ['AGENTS.md', 'START_HERE.md', 'project_state/', 'outputs/_index/', 'research_quality/', 'workflow_recipes/', 'model_registry/', 'workflow_improvement/', 'skills/', '.agents/skills/'], 'common_quality_gates': ['data/01_raw remains read-only', 'schema/metadata before full data loading', 'upstream outputs verified before downstream modeling', 'formal parameters require user confirmation', 'outputs routed to run package', 'result claims mapped to evidence', 'tables/charts checked against source data', 'citations verified before paper use'], 'expected_outputs': ['*/README_*����.md', '*/local_explanation*.md', 'local_explanation_coverage_matrix.csv'], 'stop_conditions': ['missing critical input', 'unresolved data lineage or table/chart mismatch', 'formal claim without verified evidence', 'external plugin/MCP/API/Zotero write/large dependency required', 'formal DQN/RL parameters not user-confirmed'], 'approval_required': [], 'matched_i
```

## 为关键 artifact 生成同名解释文件

- 状态：pass

```text
r_model_execution': True, 'one_line_plan': {'goal': 'Ϊ�ؼ� artifact ����ͬ�������ļ�', 'dry_run_only': True, 'no_real_data_processing': True, 'no_model_training': True, 'no_dqn_execution': True, 'run_package_required': True, 'project_state_update_required': True, 'selected_recipe': 'workflow_recipes/local_explanation_colocation_workflow.yaml', 'required_inputs': ['AGENTS.md', 'START_HERE.md', 'project_state/', 'outputs/_index/', 'research_quality/', 'workflow_recipes/', 'model_registry/', 'workflow_improvement/', 'skills/', '.agents/skills/'], 'common_quality_gates': ['data/01_raw remains read-only', 'schema/metadata before full data loading', 'upstream outputs verified before downstream modeling', 'formal parameters require user confirmation', 'outputs routed to run package', 'result claims mapped to evidence', 'tables/charts checked against source data', 'citations verified before paper use'], 'expected_outputs': ['*.explanation.md', 'missing_local_explanations.csv'], 'stop_conditions': ['missing critical input', 'unresolved data lineage or table/chart mismatch', 'formal claim without verified evidence', 'external plugin/MCP/API/Zotero write/large dependency required', 'formal DQN/R
```

## 为 DQN 代码生成深度解释

- 状态：pass

```text
ion': True, 'run_package_required': True, 'project_state_update_required': True, 'selected_recipe': 'workflow_recipes/dqn_code_deep_explanation_workflow.yaml', 'required_inputs': ['AGENTS.md', 'START_HERE.md', 'project_state/', 'outputs/_index/', 'research_quality/', 'workflow_recipes/', 'model_registry/', 'workflow_improvement/', 'skills/', '.agents/skills/'], 'common_quality_gates': ['data/01_raw remains read-only', 'schema/metadata before full data loading', 'upstream outputs verified before downstream modeling', 'formal parameters require user confirmation', 'outputs routed to run package', 'result claims mapped to evidence', 'tables/charts checked against source data', 'citations verified before paper use'], 'expected_outputs': ['README_DQN��������.md', 'dqn_code_deep_explanation.md', 'dqn_code_method_notes.md', 'dqn_code_reproducibility_notes.md'], 'stop_conditions': ['missing critical input', 'unresolved data lineage or table/chart mismatch', 'formal claim without verified evidence', 'external plugin/MCP/API/Zotero write/large dependency required', 'formal DQN/RL parameters not user-confirmed'], 'approval_required': [], 'matched_intent': 'dqn_code_deep_explanation', 'intent'
```

## 生成 DQN 代码到模型设置映射

- 状态：pass

```text
y-run', 'status': 'ok', 'details': {'goal': '���� DQN ���뵽ģ������ӳ��', 'safe_only': False, 'route': 'dqn_code_to_model_setting_map', 'review_status': 'ok', 'no_real_data_or_model_execution': True, 'one_line_plan': {'goal': '���� DQN ���뵽ģ������ӳ��', 'dry_run_only': True, 'no_real_data_processing': True, 'no_model_training': True, 'no_dqn_execution': True, 'run_package_required': True, 'project_state_update_required': True, 'selected_recipe': 'workflow_recipes/dqn_code_deep_explanation_workflow.yaml', 'required_inputs': ['AGENTS.md', 'START_HERE.md', 'project_state/', 'outputs/_index/', 'research_quality/', 'workflow_recipes/', 'model_registry/', 'workflow_improvement/', 'skills/', '.agents/skills/'], 'common_quality_gates': ['data/01_raw remains read-only', 'schema/metadata before full data loading', 'upstream outputs verified before downstream modeling', 'formal parameters require user confirmation', 'outputs routed to run package', 'result claims mapped to evidence', 'tables/charts checked against source data', 'citations verified before paper use'], 'expected_outputs': ['dqn_code_to_model_setting_map.csv'], 'stop_conditions': ['missing critical input', 'unresolved data lineage o
```

## 生成 DQN 代码到输出文件映射

- 状态：pass

```text
stage': 'dry-run', 'status': 'ok', 'details': {'goal': '���� DQN ���뵽����ļ�ӳ��', 'safe_only': False, 'route': 'dqn_code_to_outputs_map', 'review_status': 'ok', 'no_real_data_or_model_execution': True, 'one_line_plan': {'goal': '���� DQN ���뵽����ļ�ӳ��', 'dry_run_only': True, 'no_real_data_processing': True, 'no_model_training': True, 'no_dqn_execution': True, 'run_package_required': True, 'project_state_update_required': True, 'selected_recipe': 'workflow_recipes/dqn_code_deep_explanation_workflow.yaml', 'required_inputs': ['AGENTS.md', 'START_HERE.md', 'project_state/', 'outputs/_index/', 'research_quality/', 'workflow_recipes/', 'model_registry/', 'workflow_improvement/', 'skills/', '.agents/skills/'], 'common_quality_gates': ['data/01_raw remains read-only', 'schema/metadata before full data loading', 'upstream outputs verified before downstream modeling', 'formal parameters require user confirmation', 'outputs routed to run package', 'result claims mapped to evidence', 'tables/charts checked against source data', 'citations verified before paper use'], 'expected_outputs': ['dqn_code_to_outputs_map.csv'], 'stop_conditions': ['missing critical input', 'unresolved data lineage or t
```

## 检查解释是否只存在于总索引而没有就地解释

- 状态：pass

```text
 'no_real_data_processing': True, 'no_model_training': True, 'no_dqn_execution': True, 'run_package_required': True, 'project_state_update_required': True, 'selected_recipe': 'workflow_recipes/local_explanation_colocation_workflow.yaml', 'required_inputs': ['AGENTS.md', 'START_HERE.md', 'project_state/', 'outputs/_index/', 'research_quality/', 'workflow_recipes/', 'model_registry/', 'workflow_improvement/', 'skills/', '.agents/skills/'], 'common_quality_gates': ['data/01_raw remains read-only', 'schema/metadata before full data loading', 'upstream outputs verified before downstream modeling', 'formal parameters require user confirmation', 'outputs routed to run package', 'result claims mapped to evidence', 'tables/charts checked against source data', 'citations verified before paper use'], 'expected_outputs': ['*/README_*����.md', '*/local_explanation*.md', 'local_explanation_coverage_matrix.csv'], 'stop_conditions': ['missing critical input', 'unresolved data lineage or table/chart mismatch', 'formal claim without verified evidence', 'external plugin/MCP/API/Zotero write/large dependency required', 'formal DQN/RL parameters not user-confirmed'], 'approval_required': [], 'matched_i
```
