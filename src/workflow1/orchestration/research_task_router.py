"""Research task routing for auto research product mode."""

from __future__ import annotations


def infer_research_product_tasks(research_goal: str) -> tuple[str, ...]:
    """Infer product-mode task families from a research goal.

    The router intentionally returns task families, not one hard-coded model.
    Concrete model choices are left to downstream planners after schema and
    target-structure profiling.
    """

    text = research_goal.lower()
    tasks: list[str] = [
        "input_contract",
        "schema_profile",
        "raw_validation",
        "target_structure_inference",
        "literature_first_evidence_chain",
        "data_lineage_manifest",
    ]
    if any(k in text for k in ["predict", "预测", "classification", "分类", "regression", "回归", "risk", "风险"]):
        tasks.extend(["multi_task_modeling", "model_comparison", "metric_completeness"])
    if any(k in text for k in ["time", "year", "week", "month", "时间", "年份", "周", "月份"]):
        tasks.append("time_aware_validation")
    if any(k in text for k in ["group", "location", "region", "地区", "空间", "分组", "地点"]):
        tasks.append("group_or_spatial_validation")
    if any(k in text for k in ["zero", "count", "extreme", "极端", "长尾", "零膨胀", "事件"]):
        tasks.extend(["event_classification", "risk_level_classification", "extreme_event_modeling"])
    tasks.extend(
        [
            "explainability_gate",
            "figure_table_product_gate",
            "full_paper_product_gate",
            "word_render_gate",
            "quality_gate_orchestration",
            "auto_repair_loop",
            "reproducibility_packaging",
            "zotero_sidecar_evidence_pack",
        ]
    )
    return tuple(dict.fromkeys(tasks))


def required_skills_for_tasks(tasks: tuple[str, ...]) -> tuple[str, ...]:
    """Map task families to local skills."""

    mapping = {
        "target_structure_inference": "target-structure-inference-agent",
        "multi_task_modeling": "multi-task-modeling-planner",
        "model_comparison": "model-comparison-orchestrator",
        "metric_completeness": "metric-completeness-auditor",
        "explainability_gate": "shap-explainability-runner",
        "figure_table_product_gate": "figure-table-product-builder",
        "literature_first_evidence_chain": "literature-evidence-chain-builder",
        "full_paper_product_gate": "full-paper-product-writer",
        "word_render_gate": "word-docx-render-auditor",
        "quality_gate_orchestration": "research-quality-orchestrator",
        "auto_repair_loop": "auto-repair-loop-agent",
        "reproducibility_packaging": "reproducibility-auditor",
        "zotero_sidecar_evidence_pack": "zotero-safe-writeback-manager",
    }
    skills = [mapping[task] for task in tasks if task in mapping]
    skills.extend(["paper-completeness-auditor", "academic-section-integrator", "reference-integrity-checker"])
    return tuple(dict.fromkeys(skills))
