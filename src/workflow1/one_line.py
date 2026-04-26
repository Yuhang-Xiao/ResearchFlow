"""One-line research dry-run routing.

This module deliberately produces plans only. It does not read full datasets,
clean data, train models, run DQN, or write Zotero databases.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _exists(path: str) -> bool:
    return Path(path).exists()


def _base_details(goal: str) -> dict[str, Any]:
    return {
        "goal": goal,
        "dry_run_only": True,
        "no_real_data_processing": True,
        "no_model_training": True,
        "no_dqn_execution": True,
        "run_package_required": True,
        "project_state_update_required": True,
        "selected_recipe": "workflow_recipes/one_line_research_dry_run.yaml",
        "required_inputs": [
            "AGENTS.md",
            "START_HERE.md",
            "project_state/",
            "outputs/_index/",
            "research_quality/",
            "workflow_recipes/",
            "model_registry/",
            "workflow_improvement/",
            "skills/",
            ".agents/skills/",
        ],
        "common_quality_gates": [
            "data/01_raw remains read-only",
            "schema/metadata before full data loading",
            "upstream outputs verified before downstream modeling",
            "formal parameters require user confirmation",
            "outputs routed to run package",
            "result claims mapped to evidence",
            "tables/charts checked against source data",
            "citations verified before paper use",
        ],
        "expected_outputs": [
            "task run package",
            "quality gate table",
            "issue/repair log when applicable",
            "project_state updates after durable work",
        ],
        "stop_conditions": [
            "missing critical input",
            "unresolved data lineage or table/chart mismatch",
            "formal claim without verified evidence",
            "external plugin/MCP/API/Zotero write/large dependency required",
            "formal DQN/RL parameters not user-confirmed",
        ],
        "approval_required": [],
    }


def route_goal(goal: str) -> dict[str, Any]:
    """Return a structured dry-run plan for a one-line research command."""

    text = goal.lower()
    details = _base_details(goal)

    if "解释当前任务的所有输出" in goal or "输出解释" in goal or "artifact explanation" in text:
        details.update(
            matched_intent="artifact_output_explanation",
            intent="artifact_output_explanation",
            mode="explanation_dry_run",
            selected_recipe="workflow_recipes/output_explanation_workflow.yaml",
            required_skills=[
                "artifact-explanation-generator",
                "chart-quality-auditor",
                "table-result-consistency-checker",
                "result-claim-guard",
            ],
            planned_stages=[
                "locate latest run package from outputs/_index",
                "inventory figures, tables, model outputs, code, reports, and DOCX files",
                "generate artifact_explanation_index.md",
                "generate artifact_to_evidence_map.csv",
                "flag experimental/formal status for every claim-supporting output",
            ],
            quality_gates=[
                "each artifact has purpose, source, method, interpretation, limitation, and paper-use status",
                "no formal claim from experimental-only output",
                "missing or unreadable artifacts are recorded as unable to verify",
            ],
            expected_outputs=[
                "artifact_explanation_index.md",
                "artifact_to_evidence_map.csv",
                "result_interpretation_guide.md",
            ],
            executable_now=True,
        )
        return details

    if "解释所有图表和表格" in goal or "图表和表格" in goal or "figure/table explanation" in text:
        details.update(
            matched_intent="figure_table_explanation_and_chart_repair",
            intent="figure_table_explanation_and_chart_repair",
            mode="chart_table_explanation_dry_run",
            selected_recipe="workflow_recipes/output_explanation_workflow.yaml",
            required_skills=[
                "chart-quality-auditor",
                "table-result-consistency-checker",
                "artifact-explanation-generator",
                "result-claim-guard",
            ],
            planned_stages=[
                "scan figures and source tables",
                "detect blank, all-zero, near-blank, no-difference, and Chinese-font issues",
                "generate explanatory PNG or table replacement when visualization is semantically blank",
                "write figure_explanations.md and table_explanations.md",
            ],
            quality_gates=[
                "PNG preferred for main figures",
                "Chinese labels render correctly or fallback font recorded",
                "all-zero charts explain whether zero means no violation or missing data",
                "every table has field/unit/source/interpretation notes",
            ],
            expected_outputs=[
                "chart_quality_audit.csv",
                "chart_system_repair_report.md",
                "figure_explanations.md",
                "table_explanations.md",
            ],
            executable_now=True,
        )
        return details

    if "为当前代码生成方法说明" in goal or "代码生成方法说明" in goal or "code explanation" in text:
        details.update(
            matched_intent="code_method_explanation",
            intent="code_method_explanation",
            mode="code_explanation_dry_run",
            selected_recipe="workflow_recipes/output_explanation_workflow.yaml",
            required_skills=[
                "code-explanation-auditor",
                "artifact-explanation-generator",
                "reproducibility-auditor",
            ],
            planned_stages=[
                "inventory scripts in the latest run package and src/tools",
                "identify inputs, outputs, dependencies, core functions, and method logic",
                "write code_inventory.csv and code_explanations.md",
                "flag scripts that need human confirmation before formal reuse",
            ],
            quality_gates=[
                "each key script has purpose, inputs, outputs, dependency, workflow, method logic, run command, and reproducibility status",
                "code outputs are mapped to figures/tables/model results where possible",
            ],
            expected_outputs=[
                "code_inventory.csv",
                "code_explanations.md",
                "code_method_explanation_report.md",
            ],
            executable_now=True,
        )
        return details

    if "为当前模型生成详细方法说明" in goal or "模型生成详细方法说明" in goal or "model setting" in text:
        details.update(
            matched_intent="model_setting_documentation",
            intent="model_setting_documentation",
            mode="model_documentation_dry_run",
            selected_recipe="workflow_recipes/model_documentation_workflow.yaml",
            required_skills=[
                "model-setting-documenter",
                "document-governed-modeling",
                "reward-convergence-constraint-auditor",
                "literature-coverage-auditor",
            ],
            planned_stages=[
                "read config, training log, state/action/reward/constraint outputs, and model registry",
                "document features/state/target/action/reward/parameters/training/evaluation/baselines",
                "map components to data evidence and literature status",
                "preserve experimental boundary for unconfirmed settings",
            ],
            quality_gates=[
                "model settings come from local config/code/output evidence",
                "unverified items are marked as experimental assumption or unable to verify",
                "formal DQN remains blocked without user-confirmed parameters",
            ],
            expected_outputs=[
                "dqn_model_setting_detail_report.md",
                "model_output_explanations.md",
                "dqn_model_component_literature_map.csv",
            ],
            executable_now=True,
        )
        return details

    if "为当前模型结果生成详细解读" in goal or "模型结果生成详细解读" in goal or "result interpretation" in text:
        details.update(
            matched_intent="model_result_interpretation",
            intent="model_result_interpretation",
            mode="interpretation_dry_run",
            selected_recipe="workflow_recipes/model_result_interpretation_workflow.yaml",
            required_skills=[
                "result-interpretation-writer",
                "model-comparison-auditor",
                "baseline-fairness-auditor",
                "reward-convergence-constraint-auditor",
                "result-claim-guard",
            ],
            planned_stages=[
                "read multi-model comparison and diagnostics tables",
                "explain each metric and direction of improvement",
                "assess stability, reward hacking, convergence, and constraint risks",
                "separate paper-usable experimental results from formal conclusions",
            ],
            quality_gates=[
                "no metric-only CSV without interpretation",
                "all claims map to source table or chart",
                "experimental boundary retained",
            ],
            expected_outputs=[
                "dqn_result_interpretation_report.md",
                "model_output_explanations.md",
                "result_interpretation_guide.md",
            ],
            executable_now=True,
        )
        return details

    if "补充模型文献依据并写入 zotero" in goal.lower() or (
        "模型文献依据" in goal and "zotero" in text
    ):
        details.update(
            matched_intent="literature_grounded_modeling_zotero_sidecar",
            intent="literature_grounded_modeling_zotero_sidecar",
            mode="safe_zotero_sidecar_dry_run",
            selected_recipe="workflow_recipes/literature_grounded_modeling_zotero.yaml",
            required_skills=[
                "literature-coverage-auditor",
                "citation-and-reference-verifier",
                "zotero-writeback-and-note-validator",
                "model-setting-documenter",
            ],
            planned_stages=[
                "scan local references and Zotero workspace read-only",
                "build candidate literature pool and selected core literature table",
                "map model components to literature evidence",
                "generate sidecar notes, BibTeX, RIS, CSV, and import plan",
                "block direct Zotero SQLite write",
            ],
            quality_gates=[
                "read status is explicit: full-text, abstract-level, metadata-only, or not accessible",
                "garbled notes cannot support formal claims",
                "no Zotero database write without user approval",
            ],
            expected_outputs=[
                "dqn_literature_candidate_pool.csv",
                "dqn_core_literature_selected.csv",
                "dqn_model_component_literature_map.csv",
                "dqn_core_literature.bib",
                "dqn_core_literature.ris",
                "zotero_writeback_or_import_plan.csv",
            ],
            executable_now=True,
            approval_required=["Zotero database write", "MCP/plugin installation", "API key"],
        )
        return details

    if "生成论文 results 部分并导出 word" in goal.lower() or (
        "results" in text and "word" in text
    ):
        details.update(
            matched_intent="paper_results_docx_export",
            intent="paper_results_docx_export",
            mode="paper_results_docx_dry_run",
            selected_recipe="workflow_recipes/paper_section_docx_workflow.yaml",
            required_skills=[
                "paper-result-writer",
                "word-exporter-docx",
                "citation-and-reference-verifier",
                "result-claim-guard",
                "reviewer2-style-auditor",
            ],
            planned_stages=[
                "read verified tables, figures, quality gates, and literature map",
                "draft Results as academic Chinese prose with experimental boundary",
                "insert compact tables and figure references",
                "export DOCX and run render QA",
            ],
            quality_gates=[
                "every numeric claim comes from CSV",
                "evidence table accompanies section draft",
                "DOCX render checked",
                "experimental is not promoted to formal policy conclusion",
            ],
            expected_outputs=[
                "dqn_results_draft.md",
                "dqn_results_evidence_table.csv",
                "dqn_results_draft.docx",
                "docx_render_qa.md",
            ],
            executable_now=True,
            approval_required=["formal policy conclusion sign-off"],
        )
        return details

    if "检查图表是否为空并修复" in goal or "空图" in goal or "empty chart" in text:
        details.update(
            matched_intent="empty_chart_audit_and_repair",
            intent="empty_chart_audit_and_repair",
            mode="empty_chart_repair_dry_run",
            selected_recipe="workflow_recipes/chart_empty_repair_workflow.yaml",
            required_skills=[
                "chart-quality-auditor",
                "artifact-explanation-generator",
                "result-claim-guard",
            ],
            planned_stages=[
                "scan PNG/SVG/PDF chart artifacts",
                "detect blank, near-blank, all-zero, and no-difference charts",
                "repair by explanatory PNG, replacement table, or documented omission",
                "update figure explanations and chart QA",
            ],
            quality_gates=[
                "no blank axes-only main chart",
                "all-zero charts explain the scientific meaning of zero",
                "missing data is explicitly displayed and logged",
            ],
            expected_outputs=[
                "chart_quality_audit.csv",
                "chart_system_repair_report.md",
                "figure_explanations.md",
            ],
            executable_now=True,
        )
        return details

    if "搜索并创建缺失的解释类 skill" in goal or "解释类 skill" in goal:
        details.update(
            matched_intent="explanation_skill_scout",
            intent="explanation_skill_scout",
            mode="safe_skill_scout_dry_run",
            selected_recipe="workflow_recipes/workflow_self_improvement.yaml",
            required_skills=[
                "workflow-self-improvement-scout",
                "skill-scout-and-upgrader",
                "local-skill-adapter",
                "safe-workflow-upgrade-planner",
            ],
            planned_stages=[
                "scan current explanation/reporting gaps",
                "search open-source README/docs/checklists",
                "adapt safe ideas into local skills and recipes",
                "place risky tools in approval queue",
                "run dry-run validation",
            ],
            quality_gates=[
                "no unknown third-party code execution",
                "license/documentation status recorded",
                "local lightweight adaptation only unless approved",
            ],
            expected_outputs=[
                "explanation_and_reporting_skill_scout_report.md",
                "explanation_reporting_skill_candidates.csv",
                "new_or_upgraded_explanation_skills.csv",
            ],
            executable_now=True,
            approval_required=["external plugin/MCP installation", "large dependency installation", "API key"],
        )
        return details

    if "为每个输出目录生成本地解释" in goal or "本地解释" in goal or "就地解释" in goal:
        details.update(
            matched_intent="local_directory_explanation",
            intent="local_directory_explanation",
            mode="local_explanation_dry_run",
            selected_recipe="workflow_recipes/local_explanation_colocation_workflow.yaml",
            required_skills=[
                "artifact-explanation-generator",
                "code-explanation-auditor",
                "result-claim-guard",
            ],
            planned_stages=[
                "create or identify active run package",
                "scan each output directory",
                "create directory README and local explanation files",
                "update total index as navigation only",
            ],
            quality_gates=[
                "each result directory has README/local explanation",
                "10_输出解释与索引 is navigation only",
                "experimental status appears in local explanations",
            ],
            expected_outputs=[
                "*/README_*解释.md",
                "*/local_explanation*.md",
                "local_explanation_coverage_matrix.csv",
            ],
            executable_now=True,
        )
        return details

    if "为关键 artifact 生成同名解释文件" in goal or "同名解释" in goal:
        details.update(
            matched_intent="same_name_artifact_explanation",
            intent="same_name_artifact_explanation",
            mode="same_name_explanation_dry_run",
            selected_recipe="workflow_recipes/local_explanation_colocation_workflow.yaml",
            required_skills=["artifact-explanation-generator", "result-claim-guard"],
            planned_stages=[
                "identify core figures, tables, reports, code, config, and DOCX",
                "write <artifact>.explanation.md beside each core artifact",
                "record missing explanations",
            ],
            quality_gates=[
                "core artifacts have same-name explanation files",
                "support artifacts are listed in directory README",
            ],
            expected_outputs=[
                "*.explanation.md",
                "missing_local_explanations.csv",
            ],
            executable_now=True,
        )
        return details

    if "为 dqn 代码生成深度解释" in goal.lower() or "dqn 代码生成深度解释" in goal:
        details.update(
            matched_intent="dqn_code_deep_explanation",
            intent="dqn_code_deep_explanation",
            mode="dqn_code_explanation_dry_run",
            selected_recipe="workflow_recipes/dqn_code_deep_explanation_workflow.yaml",
            required_skills=[
                "code-explanation-auditor",
                "model-setting-documenter",
                "result-interpretation-writer",
            ],
            planned_stages=[
                "inspect DQN code snapshots and src modules",
                "extract functions/classes and model responsibilities",
                "explain state/action/reward/constraint/training/evaluation/baselines",
                "map code to Method and Results sections",
            ],
            quality_gates=[
                "DQN code explanation covers model logic, not only filenames",
                "formal TODOs are explicit",
                "no core code logic is changed without need",
            ],
            expected_outputs=[
                "README_DQN代码总览.md",
                "dqn_code_deep_explanation.md",
                "dqn_code_method_notes.md",
                "dqn_code_reproducibility_notes.md",
            ],
            executable_now=True,
        )
        return details

    if "生成 dqn 代码到模型设置映射" in goal.lower():
        details.update(
            matched_intent="dqn_code_to_model_setting_map",
            intent="dqn_code_to_model_setting_map",
            mode="dqn_code_mapping_dry_run",
            selected_recipe="workflow_recipes/dqn_code_deep_explanation_workflow.yaml",
            required_skills=["code-explanation-auditor", "model-setting-documenter"],
            planned_stages=[
                "map functions/classes to state, action, reward, constraint, training, baseline, evaluation",
                "flag unverified or experimental assumptions",
            ],
            expected_outputs=["dqn_code_to_model_setting_map.csv"],
            executable_now=True,
        )
        return details

    if "生成 dqn 代码到输出文件映射" in goal.lower():
        details.update(
            matched_intent="dqn_code_to_outputs_map",
            intent="dqn_code_to_outputs_map",
            mode="dqn_code_output_mapping_dry_run",
            selected_recipe="workflow_recipes/dqn_code_deep_explanation_workflow.yaml",
            required_skills=["code-explanation-auditor", "artifact-explanation-generator"],
            planned_stages=[
                "map code units to generated tables, figures, reports, configs, model artifacts, and Word outputs",
                "check each output has local explanation",
            ],
            expected_outputs=["dqn_code_to_outputs_map.csv"],
            executable_now=True,
        )
        return details

    if "检查解释是否只存在于总索引" in goal or "只有总索引" in goal:
        details.update(
            matched_intent="central_index_only_explanation_audit",
            intent="central_index_only_explanation_audit",
            mode="local_explanation_gap_audit_dry_run",
            selected_recipe="workflow_recipes/local_explanation_colocation_workflow.yaml",
            required_skills=["artifact-explanation-generator", "research-quality-orchestrator"],
            planned_stages=[
                "scan output directories for README/local explanations",
                "scan core artifacts for same-name .explanation.md",
                "write missing_local_explanations.csv",
            ],
            quality_gates=[
                "central index cannot be the only explanation",
                "missing local explanations are explicitly listed",
            ],
            expected_outputs=[
                "local_explanation_coverage_matrix.csv",
                "missing_local_explanations.csv",
            ],
            executable_now=True,
        )
        return details

    if (
        "核验" in goal
        or "质量" in goal
        or "quality gate" in text
        or "顶级期刊" in goal
        or "top journal" in text
    ) and not ("多模型" in goal or "模型对比" in goal or "model comparison" in text):
        details.update(
            matched_intent="research_quality_and_top_journal_audit",
            intent="research_quality_and_top_journal_audit",
            mode="quality_dry_run",
            selected_recipe="workflow_recipes/research_quality_audit.yaml",
            required_skills=[
                "research-quality-orchestrator",
                "data-generation-validator",
                "derived-data-lineage-auditor",
                "table-result-consistency-checker",
                "chart-quality-auditor",
                "model-comparison-auditor",
                "baseline-fairness-auditor",
                "reward-convergence-constraint-auditor",
                "top-journal-benchmark-scout",
                "top-journal-method-comparator",
                "citation-and-reference-verifier",
                "result-claim-guard",
                "reviewer2-style-auditor",
                "workflow-quality-memory-updater",
            ],
            planned_stages=[
                "create run package",
                "read latest canonical outputs and recent run packages",
                "build data and derived-output lineage manifest",
                "audit tables and charts against source tables",
                "audit model comparison, baseline fairness, reward, convergence, and constraints",
                "benchmark methods/results/figures against top-journal registry",
                "run result claim guard and Reviewer 2 audit",
                "write quality reports and update project_state",
            ],
            quality_gates=[
                "data lineage present",
                "table/report numbers match",
                "charts nonblank and source-linked",
                "at least one baseline for model claims",
                "reward/convergence/constraint audit present for RL/DQN",
                "top-journal benchmark status recorded",
                "formal conclusions blocked unless user-confirmed",
            ],
            expected_outputs=[
                "data_lineage_manifest.csv",
                "quality_gate_results.csv",
                "top_journal_benchmark_audit.md",
                "model_comparison_audit.csv",
                "result_claim_guard_findings.csv",
                "reviewer2_audit.md",
            ],
            executable_now=True,
            approval_required=["formal policy conclusion", "external validation tool installation"],
        )
        return details

    if "多模型" in goal or "模型对比" in goal or "model comparison" in text:
        details.update(
            matched_intent="multi_model_comparison_quality_audit",
            intent="multi_model_comparison_quality_audit",
            mode="comparison_dry_run",
            selected_recipe="workflow_recipes/model_comparison_quality_audit.yaml",
            required_skills=[
                "model-comparison-auditor",
                "baseline-fairness-auditor",
                "model-validation-and-diagnostics-runner",
                "reward-convergence-constraint-auditor",
                "result-claim-guard",
                "reproducibility-auditor",
            ],
            planned_stages=[
                "verify model input and split contract",
                "select required baselines from model_registry",
                "compare advanced models to interpretable controls",
                "audit metrics, uncertainty, runtime, parameter count, interpretability",
                "decide paper usable/prototype/blocked status",
            ],
            quality_gates=[
                "at least one simple baseline",
                "same split/budget/constraints/metrics",
                "baseline fairness passed",
                "uncertainty and runtime recorded",
                "claim guard passed before paper use",
            ],
            expected_outputs=[
                "model_comparison_required_baselines.csv",
                "model_comparison_quality_audit_report.md",
                "baseline_fairness_findings.csv",
            ],
            executable_now=False,
            block_reason="Dry-run only: no model training or formal DQN execution.",
            approval_required=["formal model run", "large dependency installation"],
        )
        return details

    if "word" in text or "docx" in text or "论文结果" in goal or "结果部分" in goal or "论文" in goal:
        details.update(
            matched_intent="paper_section_quality_and_word_export",
            intent="paper_section_quality_and_word_export",
            mode="paper_section_dry_run",
            selected_recipe="workflow_recipes/paper_section_quality_workflow.yaml",
            required_skills=[
                "top-journal-benchmark-scout",
                "paper-section-quality-reviewer",
                "citation-and-reference-verifier",
                "result-claim-guard",
                "reviewer2-style-auditor",
                "word-exporter-docx",
            ],
            planned_stages=[
                "read top-journal benchmark registry",
                "generate section outline",
                "generate evidence map and citation table",
                "draft Chinese section",
                "export DOCX or Markdown fallback",
                "run citation verification, result claim guard, and Reviewer 2 audit",
            ],
            quality_gates=[
                "benchmark read status recorded",
                "evidence map complete",
                "citation verification passed or limitations recorded",
                "prototype/formal status preserved",
                "DOCX/fallback output verified",
            ],
            expected_outputs=[
                "section_outline.md",
                "section_evidence_map.csv",
                "citation_evidence_table.csv",
                "paper_section.docx or fallback markdown",
                "reviewer2_revision_checklist.md",
            ],
            executable_now=True,
            approval_required=["formal conclusion sign-off", "Zotero database write"],
        )
        return details

    if "zotero" in text and ("写入" in goal or "笔记" in goal or "note" in text):
        details.update(
            matched_intent="literature_expansion_zotero_sidecar_plan",
            intent="literature_expansion_zotero_sidecar_plan",
            mode="safe_zotero_dry_run",
            selected_recipe="workflow_recipes/literature_citation_zotero_quality.yaml",
            required_skills=[
                "literature-coverage-auditor",
                "citation-and-reference-verifier",
                "zotero-writeback-and-note-validator",
                "workflow-quality-memory-updater",
            ],
            planned_stages=[
                "scan local Zotero workspace read-only",
                "detect garbled notes",
                "search metadata gaps if needed",
                "generate clean Chinese sidecar notes",
                "generate BibTeX/RIS/CSV sidecar exports",
                "block direct Zotero database writes until approval",
            ],
            quality_gates=[
                "no Zotero SQLite write",
                "garbled notes flagged",
                "DOI/title/authors/year/venue metadata checked",
                "sidecar notes generated in run package",
            ],
            expected_outputs=[
                "citation_verification_tool_candidates.csv",
                "zotero_writeback_safe_plan.csv",
                "sidecar_notes/",
                "citation_evidence_table.csv",
            ],
            executable_now=True,
            approval_required=["Zotero database write", "Zotero MCP installation", "API key"],
        )
        return details

    if "优化" in goal or "升级" in goal or "workflow" in text or "skill" in text:
        details.update(
            matched_intent="workflow_self_improvement",
            intent="workflow_self_improvement",
            mode="safe_dry_run",
            selected_recipe="workflow_recipes/workflow_self_improvement.yaml",
            required_skills=[
                "workflow-self-improvement-scout",
                "workflow-gap-analyzer",
                "github-skill-scout-and-adapter",
                "safe-workflow-upgrade-planner",
                "external-plugin-approval-manager",
                "workflow-quality-memory-updater",
            ],
            planned_stages=[
                "create run package",
                "scan local capabilities",
                "search watchlist/GitHub if needed",
                "check research-quality gaps from the latest task",
                "apply low-risk local upgrades",
                "write approval queue",
                "run skills-doctor",
                "update project_state",
            ],
            quality_gates=[
                "safe-only adaptation",
                "no third-party code execution",
                "approval queue for MCP/API/dependencies/Zotero write",
                "ledger and project_state updated",
            ],
            expected_outputs=[
                "workflow_quality_improvement_backlog.csv",
                "approval_required_external_tools.csv",
                "workflow_self_improvement_quality_upgrade_report.md",
            ],
            approval_required=["MCP/plugin install", "API keys", "Zotero database writes", "large dependency installation"],
            executable_now=True,
        )
        return details

    if "dqn" in text and ("正式" in goal or "confirmed" in text):
        details.update(
            matched_intent="formal_dqn_guarded_plan",
            intent="formal_dqn_guarded_plan",
            mode="formal_confirmed_required",
            required_skills=[
                "document-governed-modeling",
                "zotero-literature-auditor",
                "environment-auditor",
                "dqn-readiness-auditor",
                "upstream-output-auditor",
                "reward-convergence-constraint-auditor",
            ],
            planned_stages=[
                "read confirmed DQN parameter table",
                "verify no DRAFT config is used",
                "verify myenv1 torch/CUDA",
                "verify upstream belief-MDP/MOE-EDI state features",
                "block training unless every required parameter is confirmed",
            ],
            executable_now=False,
            block_reason="Formal DQN requires explicit confirmed parameters; dry-run only in this task.",
            approval_required=["formal DQN parameter confirmation", "training permission"],
        )
        return details

    if "文献" in goal or "zotero" in text or "方法" in goal:
        details.update(
            matched_intent="literature_method_update",
            intent="literature_method_update",
            mode="planning_only",
            required_skills=[
                "literature-coverage-auditor",
                "citation-and-reference-verifier",
                "zotero-literature-auditor",
                "reference-document-reader",
                "project-memory-updater",
            ],
            planned_stages=[
                "inspect references/processed_summaries",
                "scan Zotero deepreads/PDF inventory",
                "flag garbled notes",
                "summarize method evidence",
                "write method summary and project_state update",
            ],
            executable_now=True,
            approval_required=["Zotero database write", "MCP installation"],
        )
        return details

    if "清洗" in goal or "标签" in goal:
        details.update(
            matched_intent="cleaning_and_label_engineering",
            intent="cleaning_and_label_engineering",
            mode="planning_only",
            required_skills=[
                "data-schema-profiler",
                "data-cleaning-matching",
                "concentration-cleaning-auditor",
                "upstream-output-auditor",
                "data-generation-validator",
            ],
            planned_stages=[
                "raw metadata/schema inventory",
                "validation summary",
                "cleaning plan",
                "label dictionary plan",
                "manual confirmation if cleaning choices affect conclusions",
            ],
            executable_now=False,
            block_reason="This acceptance task forbids real cleaning; plan only.",
        )
        return details

    if "监督" in goal or "分类" in goal or "回归" in goal:
        details.update(
            matched_intent="supervised_model_comparison",
            intent="supervised_model_comparison",
            mode="prototype_plan",
            required_skills=[
                "ml-problem-framer",
                "method-selector",
                "baseline-trainer",
                "upstream-output-auditor",
                "model-comparison-auditor",
                "baseline-fairness-auditor",
            ],
            planned_stages=[
                "verify cleaned/model input exists",
                "identify target/unit/leakage risks",
                "choose baseline models",
                "define metric contract",
                "produce comparison plan",
            ],
            executable_now=False,
            block_reason="This acceptance task forbids model training; prototype plan only.",
        )
        return details

    if "peanut" in text or "花生" in goal or "食品安全" in goal or "风险监管" in goal:
        details.update(
            matched_intent="peanut_food_safety_full_workflow",
            intent="peanut_food_safety_full_workflow",
            mode="guarded_dry_run",
            required_skills=[
                "goal-driven-research-orchestrator",
                "upstream-output-auditor",
                "concentration-cleaning-auditor",
                "zotero-literature-auditor",
                "document-governed-modeling",
                "dqn-readiness-auditor",
                "research-quality-orchestrator",
            ],
            planned_stages=[
                "read PEANUT project memory and research plan",
                "verify canonical cleaned/risk/belief outputs",
                "audit concentration and MOE/EDI readiness",
                "select allowed prototype/model-planning path",
                "block formal DQN until parameter confirmation",
                "plan visualization and Chinese report",
            ],
            data_assets={
                "cleaned_table": _exists("data/03_primary/peanut_cleaned_analysis_ready.csv"),
                "belief_mdp_moe_edi": _exists("data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv"),
                "dqn_parameter_table": _exists("project_state/dqn_parameter_confirmation_table.csv"),
            },
            executable_now=True,
            approval_required=["formal DQN", "formal policy optimization", "unconfirmed external parameters"],
        )
        return details

    details.update(
        matched_intent="generic_full_research_workflow",
        intent="generic_full_research_workflow",
        mode="guarded_dry_run",
        required_skills=[
            "goal-driven-research-orchestrator",
            "data-schema-profiler",
            "data-cleaning-matching",
            "zotero-literature-auditor",
            "method-selector",
            "upstream-output-auditor",
            "research-quality-orchestrator",
            "project-memory-updater",
        ],
        planned_stages=[
            "read project state and run index",
            "identify raw data inventory without full processing",
            "plan schema validation and cleaning",
            "plan label engineering",
            "plan literature/Zotero audit",
            "plan model family selection",
            "plan visualization and Chinese report",
            "route all outputs to run package",
        ],
        executable_now=True,
        approval_required=["formal model parameters", "external plugins", "database writes"],
    )
    return details
