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
        "common_quality_gates": [
            "data/01_raw remains read-only",
            "schema/metadata before full data loading",
            "upstream outputs verified before downstream modeling",
            "formal parameters require user confirmation",
            "outputs routed to run package",
        ],
    }


def route_goal(goal: str) -> dict[str, Any]:
    """Return a structured dry-run plan for a one-line research command."""

    text = goal.lower()
    details = _base_details(goal)

    if "优化" in goal or "升级" in goal or "workflow" in text or "skill" in text:
        details.update(
            intent="workflow_self_improvement",
            mode="safe_dry_run",
            required_skills=[
                "workflow-self-improvement-scout",
                "workflow-gap-analyzer",
                "github-skill-scout-and-adapter",
                "safe-workflow-upgrade-planner",
                "external-plugin-approval-manager",
            ],
            planned_stages=[
                "create run package",
                "scan local capabilities",
                "search watchlist/GitHub if needed",
                "apply low-risk local upgrades",
                "write approval queue",
                "run skills-doctor",
                "update project_state",
            ],
            approval_required=["MCP/plugin install", "API keys", "Zotero database writes", "large dependency installation"],
            executable_now=True,
        )
        return details

    if "dqn" in text and ("正式" in goal or "confirmed" in text):
        details.update(
            intent="formal_dqn_guarded_plan",
            mode="formal_confirmed_required",
            required_skills=[
                "document-governed-modeling",
                "zotero-literature-auditor",
                "environment-auditor",
                "dqn-readiness-auditor",
                "upstream-output-auditor",
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
            intent="literature_method_update",
            mode="planning_only",
            required_skills=["zotero-literature-auditor", "reference-document-reader", "project-memory-updater"],
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
            intent="cleaning_and_label_engineering",
            mode="planning_only",
            required_skills=[
                "data-schema-profiler",
                "data-cleaning-matching",
                "concentration-cleaning-auditor",
                "upstream-output-auditor",
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

    if "监督" in goal or "分类" in goal or "回归" in goal or "模型比较" in goal:
        details.update(
            intent="supervised_model_comparison",
            mode="prototype_plan",
            required_skills=["ml-problem-framer", "method-selector", "baseline-trainer", "upstream-output-auditor"],
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

    if "论文" in goal or "结果部分" in goal or "报告" in goal:
        details.update(
            intent="paper_result_writer",
            mode="planning_only",
            required_skills=["upstream-output-auditor", "zotero-literature-auditor", "project-memory-updater"],
            planned_stages=[
                "verify report-vs-data consistency",
                "check figure/table completeness",
                "check citation completeness",
                "draft Chinese results section",
                "record limitations and non-formal/prototype status",
            ],
            executable_now=True,
            approval_required=["formal conclusion sign-off if policy/model claims are made"],
        )
        return details

    if "peanut" in text or "花生" in goal or "食品安全" in goal or "风险监管" in goal:
        details.update(
            intent="peanut_food_safety_full_workflow",
            mode="guarded_dry_run",
            required_skills=[
                "goal-driven-research-orchestrator",
                "upstream-output-auditor",
                "concentration-cleaning-auditor",
                "zotero-literature-auditor",
                "document-governed-modeling",
                "dqn-readiness-auditor",
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

    if "prototype" in text or "自动选择模型" in goal:
        details.update(
            intent="model_selection_prototype_plan",
            mode="prototype_plan",
            required_skills=["ml-problem-framer", "method-selector", "baseline-trainer", "dqn-readiness-auditor"],
            planned_stages=[
                "inspect current research objective",
                "classify task family",
                "choose transparent baseline first",
                "generate prototype-only execution plan",
                "write metric contract and quality gates",
            ],
            executable_now=False,
            block_reason="This acceptance task forbids executing prototype models; plan only.",
        )
        return details

    details.update(
        intent="generic_full_research_workflow",
        mode="guarded_dry_run",
        required_skills=[
            "goal-driven-research-orchestrator",
            "data-schema-profiler",
            "data-cleaning-matching",
            "zotero-literature-auditor",
            "method-selector",
            "upstream-output-auditor",
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
