"""Command-line entry point for lightweight workflow routing."""

from __future__ import annotations

import argparse
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
import tomllib
from typing import Any

from workflow1.pipelines.runner import PipelineResult, run_placeholder_pipeline
from workflow1.utils.logging import get_logger


DEFAULT_CONFIG_PATH = Path(".codex/config.toml")


@dataclass(frozen=True)
class WorkflowRunSummary:
    """Structured summary for a lightweight workflow command."""

    config_path: str
    config_loaded: bool
    stage: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)


def load_config(path: str | Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load a TOML config file if it exists."""

    config_path = Path(path)
    if not config_path.exists():
        return {}
    with config_path.open("rb") as handle:
        return tomllib.load(handle)


def route_stage(
    stage: str,
    raw_dir: str | Path = "data/01_raw",
    reports_dir: str | Path = "reports",
    goal: str | None = None,
    safe_only: bool = False,
) -> PipelineResult:
    """Route to a workflow stage."""

    known_stages = {
        "launch",
        "continue",
        "memory-update",
        "skill-scout",
        "intake",
        "validation",
        "cleaning",
        "cleaning-plan",
        "matching",
        "eda",
        "features",
        "modeling",
        "evaluation",
        "postprocess",
        "visualization",
        "orchestration",
        "start-run",
        "finish-run",
        "list-runs",
        "workflow-scout",
        "workflow-upgrade-plan",
        "workflow-upgrade-apply",
        "list-upgrade-candidates",
        "list-approval-queue",
        "skills-doctor",
        "dry-run",
    }
    if stage not in known_stages:
        return PipelineResult(
            name=stage,
            status="unknown_stage",
            details={"message": f"Unknown stage: {stage}"},
        )
    if stage == "start-run":
        from workflow1.run_package import start_run

        return PipelineResult(name=stage, status="ok", details=start_run(os.environ.get("WORKFLOW1_RUN_NAME", "未命名任务")))
    if stage == "finish-run":
        from workflow1.run_package import finish_run

        return PipelineResult(name=stage, status="ok", details=finish_run())
    if stage == "list-runs":
        from workflow1.run_package import list_runs

        return PipelineResult(name=stage, status="ok", details=list_runs())
    if stage in {
        "workflow-scout",
        "workflow-upgrade-plan",
        "workflow-upgrade-apply",
        "list-upgrade-candidates",
        "list-approval-queue",
        "skills-doctor",
        "dry-run",
    }:
        return run_self_improvement_stage(stage=stage, goal=goal, safe_only=safe_only)
    if stage == "intake":
        from workflow1.pipelines.intake import run as run_intake

        return run_intake(raw_dir=raw_dir, reports_dir=reports_dir)
    if stage == "validation":
        from workflow1.pipelines.validation import run as run_validation

        return run_validation(raw_dir=raw_dir, reports_dir=reports_dir)
    if stage == "cleaning-plan":
        from workflow1.pipelines.cleaning import run_cleaning_plan

        return run_cleaning_plan(raw_dir=raw_dir, reports_dir=reports_dir)
    if stage == "launch":
        from workflow1.launch import run_launch

        return run_launch(raw_dir=raw_dir, references_dir="references", mode="launch")
    if stage == "continue":
        from workflow1.launch import run_launch

        return run_launch(raw_dir=raw_dir, references_dir="references", mode="continue")
    if stage == "memory-update":
        from workflow1.launch import run_memory_update_preview

        return run_memory_update_preview()
    if stage == "skill-scout":
        from workflow1.launch import run_skill_scout_preview

        return run_skill_scout_preview()
    return run_placeholder_pipeline(stage)


def run(
    stage: str = "orchestration",
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    raw_dir: str | Path | None = None,
    reports_dir: str | Path | None = None,
    goal: str | None = None,
    safe_only: bool = False,
) -> WorkflowRunSummary:
    """Run the lightweight workflow entry point without business logic."""

    logger = get_logger("workflow1")
    config = load_config(config_path)
    workflow_config = config.get("workflow", {}) if isinstance(config, dict) else {}
    resolved_raw_dir = raw_dir or os.environ.get("WORKFLOW1_RAW_DIR") or workflow_config.get("raw_data_dir", "data/01_raw")
    resolved_reports_dir = reports_dir or os.environ.get("WORKFLOW1_REPORTS_DIR") or workflow_config.get("reports_dir", "reports")
    logger.info("Loaded config: %s", bool(config))
    logger.info("Routing stage: %s", stage)
    result = route_stage(stage, raw_dir=resolved_raw_dir, reports_dir=resolved_reports_dir, goal=goal, safe_only=safe_only)
    if result.status == "not_implemented":
        logger.info("Stage is registered but not implemented yet: %s", stage)
    elif result.status == "unknown_stage":
        logger.warning("Unknown workflow stage requested: %s", stage)
    elif result.status == "no_raw_data":
        logger.info("No supported raw data found for stage: %s", stage)

    return WorkflowRunSummary(
        config_path=str(config_path),
        config_loaded=bool(config),
        stage=result.name,
        status=result.status,
        details=result.details,
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(description="Lightweight workflow1 runner.")
    parser.add_argument(
        "--stage",
        default="orchestration",
        help="Workflow stage to route to. Heavy stage logic is intentionally not implemented yet.",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to the TOML config file.",
    )
    parser.add_argument(
        "--raw-dir",
        default=None,
        help="Raw data directory. Defaults to config workflow.raw_data_dir or WORKFLOW1_RAW_DIR.",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Run package name for --stage start-run.",
    )
    parser.add_argument(
        "--reports-dir",
        default=None,
        help="Reports directory. Defaults to config workflow.reports_dir or WORKFLOW1_REPORTS_DIR.",
    )
    parser.add_argument(
        "--goal",
        default=None,
        help="Natural-language goal for dry-run routing.",
    )
    parser.add_argument(
        "--safe-only",
        action="store_true",
        help="Only apply or preview low-risk local workflow upgrades.",
    )
    return parser


def run_self_improvement_stage(stage: str, goal: str | None = None, safe_only: bool = False) -> PipelineResult:
    """Run lightweight self-improvement stages without external side effects."""

    from workflow1.self_improvement.self_review import run_self_review

    review = run_self_review(Path("."))
    details: dict[str, Any] = {"goal": goal, "safe_only": safe_only}
    if stage == "workflow-scout":
        details.update({"queries": ["Codex skills GitHub", "Zotero MCP GitHub", "AutoML agent GitHub"], "candidates": review["candidates"]})
    elif stage == "workflow-upgrade-plan":
        details.update({"plan": review["plan"]})
    elif stage == "workflow-upgrade-apply":
        details.update({"status": "dry_run_safe_only" if safe_only else "dry_run_requires_safe_only", "plan": review["plan"]})
    elif stage == "list-upgrade-candidates":
        details.update({"candidates": review["candidates"]})
    elif stage == "list-approval-queue":
        details.update({"approval_queue": review["approval_queue"]})
    elif stage == "skills-doctor":
        skill_paths = sorted(str(p) for base in [Path("skills"), Path(".agents/skills")] for p in base.glob("*/SKILL.md"))
        details.update({"skill_count": len(skill_paths), "sample": skill_paths[:20], "status": "ok"})
    elif stage == "dry-run":
        from workflow1.one_line import route_goal

        plan = route_goal(goal or "")
        details.update(
            {
                "route": plan.get("intent", "generic_full_research_workflow"),
                "review_status": review["status"],
                "no_real_data_or_model_execution": True,
                "one_line_plan": plan,
            }
        )
    return PipelineResult(name=stage, status="ok", details=details)


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and print a compact structured summary."""

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.name:
        os.environ["WORKFLOW1_RUN_NAME"] = args.name
    summary = run(
        stage=args.stage,
        config_path=args.config,
        raw_dir=args.raw_dir,
        reports_dir=args.reports_dir,
        goal=args.goal,
        safe_only=args.safe_only,
    )
    print(asdict(summary))
    return 0 if summary.status in {"not_implemented", "unknown_stage"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
