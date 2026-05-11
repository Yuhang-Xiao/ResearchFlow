"""Executable Research OS chain for acceptance-scale workflows."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import pandas as pd

from workflow1.automl.sklearn_baseline_adapter import SklearnBaselineAdapter
from workflow1.model_registry import load_model_registry
from workflow1.model_registry.explainability_selector import select_explainability
from workflow1.model_registry.figure_table_selector import select_figure_table_plan
from workflow1.model_registry.literature_need_selector import select_literature_needs
from workflow1.model_registry.metric_selection_engine import select_metrics
from workflow1.model_registry.model_repair_strategy_selector import select_repair_strategies
from workflow1.model_registry.model_selection_engine import select_models
from workflow1.model_registry.task_inference_engine import infer_task_from_dataframe, load_table
from workflow1.model_registry.validation_strategy_selector import select_validation_strategy
from workflow1.orchestration.action_queue import build_default_action_queue
from workflow1.orchestration.repair_decision_engine import decide_repairs
from workflow1.orchestration.research_plan import ResearchPlan
from workflow1.quality_gates.metric_completeness_gate import MetricCompletenessGate
from workflow1.quality_gates.model_registry_gate import ModelRegistryGate


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_sidecar_explanation(path: Path, purpose: str, status: str = "draft/minimal executable product") -> Path:
    sidecar = path.with_name(path.name + ".explanation.md")
    write_text(
        sidecar,
        "# Artifact Explanation\n\n"
        f"- artifact: `{path.name}`\n"
        f"- purpose: {purpose}\n"
        f"- status: {status}\n"
        "- evidence boundary: This artifact supports workflow execution and audit. It is not a formal paper claim by itself.\n",
    )
    return sidecar


def write_directory_readmes(output: Path) -> None:
    readme_by_dir = {
        output: ("# Minimal Research Product Package\n\nThis directory contains the executable Research OS outputs for one data-goal task.\n"),
        output / "models": ("# Model Outputs\n\nPredictions, metrics support tables, and explainability artifacts from the local sklearn baseline live here.\n"),
        output / "models" / "explainability_outputs": ("# Explainability Outputs\n\nSHAP outputs or documented fallback explanation artifacts. These describe predictive associations, not causal mechanisms.\n"),
        output / "04_报告输出": ("# Report Outputs\n\nMinimal paper/report skeletons and research cards. Draft status is explicit.\n"),
        output / "07_日志与错误": ("# Logs And Repair Records\n\nQuality-gate failures, repair decisions, and remaining issues are recorded here.\n"),
        output / "10_输出解释与索引": ("# Explanation Navigation\n\nCentral navigation for explanations. Local directory README files and same-name sidecars remain the source of artifact-level explanations.\n"),
    }
    for directory, text in readme_by_dir.items():
        directory.mkdir(parents=True, exist_ok=True)
        write_text(directory / "README.md", text)


def write_repair_logs(output: Path, gate_results: list[dict[str, object]], repair_decision: dict[str, object]) -> dict[str, str]:
    log_dir = output / "07_日志与错误"
    log_dir.mkdir(parents=True, exist_ok=True)
    failed = [g for g in gate_results if g.get("status") != "pass"]
    failed_rows = []
    for gate in failed:
        failed_rows.append(
            {
                "gate_name": gate.get("gate_name"),
                "status": gate.get("status"),
                "severity": gate.get("severity"),
                "failed_items": json.dumps(gate.get("failed_items", []), ensure_ascii=False),
                "repair_suggestions": json.dumps(gate.get("repair_suggestions", []), ensure_ascii=False),
                "requires_human_authorization": gate.get("requires_human_authorization", False),
            }
        )
    pd.DataFrame(
        [
            {
                "round": "round_1_initial_execution",
                "failed_gate_count": len(failed),
                "repair_status": repair_decision.get("status"),
                "reason": repair_decision.get("reason"),
            }
        ]
    ).to_csv(log_dir / "redo_log.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(failed_rows).to_csv(log_dir / "failed_gate_summary.csv", index=False, encoding="utf-8-sig")
    write_text(
        log_dir / "failed_gate_summary.md",
        "# Failed Gate Summary\n\n"
        + ("\n".join(f"- {row['gate_name']}: {row['failed_items']}" for row in failed_rows) if failed_rows else "All executable gates passed.\n"),
    )
    repaired_items = repair_decision.get("repair_actions", []) if not repair_decision.get("requires_human_authorization") else []
    pd.DataFrame(repaired_items).to_csv(log_dir / "repaired_items.csv", index=False, encoding="utf-8-sig")
    remaining_rows = failed_rows if repair_decision.get("requires_human_authorization") else []
    pd.DataFrame(remaining_rows).to_csv(log_dir / "remaining_issues.csv", index=False, encoding="utf-8-sig")
    return {
        "redo_log": str(log_dir / "redo_log.csv"),
        "failed_gate_summary": str(log_dir / "failed_gate_summary.md"),
        "repaired_items": str(log_dir / "repaired_items.csv"),
        "remaining_issues": str(log_dir / "remaining_issues.csv"),
    }


def write_minimal_product_skeleton(output: Path, plan: ResearchPlan, gate_results: list[dict[str, object]]) -> dict[str, str]:
    report_dir = output / "04_报告输出"
    report_dir.mkdir(parents=True, exist_ok=True)
    gate_status = "pass" if all(g.get("status") == "pass" for g in gate_results) else "needs_repair"
    full_paper = report_dir / "full_paper.md"
    write_text(
        full_paper,
        "# Minimal Research Product Draft\n\n"
        "Status: draft/minimal executable product. This is a scaffold generated by workflow1, not a final manuscript.\n\n"
        "## Title\n\nTBD from research goal.\n\n"
        "## Abstract\n\nPending full evidence chain and complete product-mode execution.\n\n"
        "## Keywords\n\nworkflow1; machine learning; reproducibility\n\n"
        "## Introduction\n\nDraft placeholder pending literature evidence.\n\n"
        "## Literature Review\n\nRequires verified full-text or abstract-level evidence mapping.\n\n"
        "## Method\n\n"
        f"Task type: `{plan.task_type}`. Target: `{plan.target_variable}`. Baselines: `{', '.join(plan.baseline_models)}`.\n\n"
        "## Results\n\nExecutable baseline metrics and gate status are stored beside this file.\n\n"
        "## Discussion\n\nInterpretation must remain predictive and non-causal unless later evidence supports causal claims.\n\n"
        "## Conclusion\n\nPending complete quality gates.\n\n"
        "## References\n\nPending citation verification.\n\n"
        "## Appendix\n\nSee manifest and local artifact explanations.\n",
    )
    cards = {
        "data_card.md": "# Data Card\n\nMinimal data profile is recorded in `task_inference.json`.\n",
        "model_card.md": f"# Model Card\n\nTask type: `{plan.task_type}`. Baselines: `{', '.join(plan.baseline_models)}`. Candidate families: `{', '.join(plan.candidate_models)}`.\n",
        "experiment_card.md": f"# Experiment Card\n\nGate status: `{gate_status}`. Random seed: `42`.\n",
        "evidence_card.md": "# Evidence Card\n\nLiterature and external engineering references are planned but not treated as formal claims until verified.\n",
    }
    artifacts = {"full_paper": str(full_paper)}
    write_sidecar_explanation(full_paper, "Minimal full-paper scaffold for product-mode completeness checks.")
    for name, text in cards.items():
        path = report_dir / name
        write_text(path, text)
        write_sidecar_explanation(path, f"Research card: {name}.")
        artifacts[name[:-3]] = str(path)
    return artifacts


def write_explanation_coverage(output: Path, key_artifacts: list[Path]) -> dict[str, str]:
    explain_dir = output / "10_输出解释与索引"
    explain_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    missing = []
    for directory in sorted([p for p in output.rglob("*") if p.is_dir()] + [output]):
        readme = directory / "README.md"
        rows.append({"path": str(directory), "type": "directory", "local_explanation": str(readme), "present": readme.exists()})
        if not readme.exists():
            missing.append({"path": str(directory), "missing": "README.md"})
    for artifact in key_artifacts:
        sidecar = artifact.with_name(artifact.name + ".explanation.md")
        rows.append({"path": str(artifact), "type": "artifact", "local_explanation": str(sidecar), "present": sidecar.exists()})
        if not sidecar.exists():
            missing.append({"path": str(artifact), "missing": sidecar.name})
    coverage = explain_dir / "local_explanation_coverage_matrix.csv"
    missing_path = explain_dir / "missing_local_explanations.csv"
    pd.DataFrame(rows).to_csv(coverage, index=False, encoding="utf-8-sig")
    pd.DataFrame(missing).to_csv(missing_path, index=False, encoding="utf-8-sig")
    write_text(
        explain_dir / "artifact_explanation_index.md",
        "# Artifact Explanation Index\n\n"
        "This is a navigation layer only. Read each directory README and same-name `.explanation.md` file for local context.\n",
    )
    return {"local_explanation_coverage_matrix": str(coverage), "missing_local_explanations": str(missing_path)}


def execute_research_os_minimal(
    data_file: str,
    research_goal: str,
    output_dir: str,
    target_column: str | None = None,
) -> dict[str, object]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    df = load_table(data_file)
    inference = infer_task_from_dataframe(df, research_goal, target_column)
    registry = load_model_registry()
    model_decision = select_models(inference.task_type, registry)
    metrics = select_metrics(inference.task_type, registry)
    validation = select_validation_strategy(inference.task_type, inference.profile, registry)
    explainability = select_explainability(inference.task_type, shap_available=importlib.util.find_spec("shap") is not None, registry=registry)
    figure_table = select_figure_table_plan(inference.task_type, registry)
    literature = select_literature_needs(inference.task_type, registry)
    repairs = select_repair_strategies(inference.task_type, registry=registry)
    action_queue = build_default_action_queue()
    plan = ResearchPlan(
        task_type=inference.task_type,
        target_variable=inference.target_column,
        baseline_models=model_decision.baseline_models,
        candidate_models=model_decision.candidate_model_families,
        metrics=metrics,
        validation_strategy=validation,
        explainability_plan=explainability,
        figure_table_plan=figure_table,
        literature_needs=literature,
        repair_strategies=repairs,
        actions=action_queue.to_rows(),
        notes=inference.reasons,
    )
    model_result = None
    if inference.target_column:
        model_result = SklearnBaselineAdapter().fit_predict(df, inference.target_column, inference.task_type, output / "models").to_dict()
        pd.DataFrame([model_result["metrics"]]).to_csv(output / "model_metrics.csv", index=False, encoding="utf-8-sig")
    gate_results = [
        MetricCompletenessGate().run({"task_type": inference.task_type, "metrics": model_result["metrics"] if model_result else {}, "registry": registry}).to_dict(),
        ModelRegistryGate().run({"registry": registry}).to_dict(),
    ]
    repair_decision = decide_repairs(gate_results).to_dict()
    write_directory_readmes(output)
    written_artifacts: dict[str, str] = {}
    for name, data, purpose in [
        ("research_plan.json", plan.to_dict(), "Registry-derived research plan with models, metrics, validation, explainability, figures, literature needs, and repair actions."),
        ("task_inference.json", inference.to_dict(), "Task and target inference result from the data profile and research goal."),
        ("model_decision.json", model_decision.to_dict(), "Model family and baseline decision selected from the Model & Method Registry."),
        ("gate_results.json", gate_results, "Executable quality-gate results."),
        ("repair_decision.json", repair_decision, "Auto-repair decision derived from failed quality gates."),
    ]:
        path = output / name
        write_json(path, data)
        write_sidecar_explanation(path, purpose)
        written_artifacts[name] = str(path)
    (output / "reproducibility_README.md").write_text(
        "# Reproducibility\n\n"
        f"- data_file: `{data_file}`\n"
        f"- research_goal: {research_goal}\n"
        "- random_seed: 42\n"
        "- executor: workflow1 Research OS minimal executable chain\n",
        encoding="utf-8",
    )
    pd.DataFrame(action_queue.to_rows()).to_csv(output / "action_queue.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(gate_results).to_csv(output / "gate_results.csv", index=False, encoding="utf-8-sig")
    for path, purpose in [
        (output / "model_metrics.csv", "Task-appropriate metric table for the local baseline."),
        (output / "action_queue.csv", "Default action queue and repair-oriented next actions."),
        (output / "gate_results.csv", "CSV copy of executable quality-gate results."),
        (output / "reproducibility_README.md", "Reproducibility summary for this minimal run."),
    ]:
        if path.exists():
            write_sidecar_explanation(path, purpose)
            written_artifacts[path.name] = str(path)
    written_artifacts.update(write_repair_logs(output, gate_results, repair_decision))
    written_artifacts.update(write_minimal_product_skeleton(output, plan, gate_results))
    key_paths = [Path(p) for p in written_artifacts.values() if Path(p).exists()]
    written_artifacts.update(write_explanation_coverage(output, key_paths))
    pd.DataFrame([{"artifact": p.name, "path": str(p)} for p in sorted(output.rglob("*")) if p.is_file()]).to_csv(
        output / "manifest.csv", index=False, encoding="utf-8-sig"
    )
    write_sidecar_explanation(output / "manifest.csv", "Complete file manifest for this minimal research product package.")
    return {
        "status": "ok",
        "plan": plan.to_dict(),
        "inference": inference.to_dict(),
        "model_result": model_result,
        "gate_results": gate_results,
        "repair_decision": repair_decision,
        "output_dir": str(output),
    }
