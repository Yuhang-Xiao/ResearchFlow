"""Top-level orchestration for auto research product mode."""

from __future__ import annotations

from workflow1.orchestration.auto_repair_loop import plan_auto_repair_loop
from workflow1.orchestration.final_product_packager import package_verdict
from workflow1.orchestration.quality_gate_runner import GATE_CONTRACTS
from workflow1.orchestration.research_executor import execute_research_os_minimal
from workflow1.orchestration.research_task_router import infer_research_product_tasks, required_skills_for_tasks


def build_product_orchestration_dry_run(
    goal: str,
    data_file: str = "XXX",
    constraints: tuple[str, ...] = (),
) -> dict[str, object]:
    """Build a structured product-mode dry-run plan."""

    tasks = infer_research_product_tasks(goal)
    return {
        "mode": "auto_research_product",
        "input_contract": {
            "data_file": data_file,
            "research_goal": goal,
            "optional_constraints": list(constraints),
            "minimal_user_input": "启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。",
        },
        "tasks": list(tasks),
        "required_skills": list(required_skills_for_tasks(tasks)),
        "recipes": [
            "workflow_recipes/auto_research_product_orchestrator.yaml",
            "workflow_recipes/one_sentence_to_research_product.yaml",
            "workflow_recipes/literature_first_research_workflow.yaml",
            "workflow_recipes/multi_task_modeling_planner.yaml",
            "workflow_recipes/metric_completeness_gate.yaml",
            "workflow_recipes/model_comparison_gate.yaml",
            "workflow_recipes/explainability_gate.yaml",
            "workflow_recipes/figure_table_product_gate.yaml",
            "workflow_recipes/full_paper_product_gate.yaml",
            "workflow_recipes/paper_product_generation_orchestrator.yaml",
            "workflow_recipes/research_quality_gate_orchestrator.yaml",
            "workflow_recipes/auto_repair_loop.yaml",
        ],
        "quality_gates": list(GATE_CONTRACTS),
        "auto_repair": plan_auto_repair_loop(),
        "final_packaging_verdict_contract": package_verdict(),
        "approval_required": [
            "Zotero database write",
            "paid or institution-only full text",
            "external MCP/plugin installation",
            "API key use",
            "large dependency or model/data download",
            "running unknown third-party code",
        ],
        "dry_run_only": True,
    }


def run_auto_research_product(
    goal: str,
    data_file: str,
    output_dir: str,
    constraints: tuple[str, ...] = (),
    target_column: str | None = None,
) -> dict[str, object]:
    """Run the executable Research OS chain used by product mode.

    This function is intentionally conservative: it performs local data profiling,
    target/task inference, registry-based model/metric/validation/explainability
    selection, a local sklearn baseline, executable gates, repair-action creation,
    and final reproducibility packaging. Literature, Zotero writes, external
    AutoML dependencies, and third-party code execution remain guarded actions.
    """

    result = execute_research_os_minimal(
        data_file=data_file,
        research_goal=goal,
        output_dir=output_dir,
        target_column=target_column,
    )
    result["mode"] = "auto_research_product"
    result["constraints"] = list(constraints)
    result["approval_required"] = [
        "Zotero database write",
        "API key use",
        "large external dependency installation",
        "running unknown third-party code",
        "paid full text",
    ]
    return result
