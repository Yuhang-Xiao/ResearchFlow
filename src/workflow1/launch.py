"""Lightweight one-line launch helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from workflow1.pipelines.runner import PipelineResult


STATE_FILES = (
    "project_state/project_memory.md",
    "project_state/run_protocol.md",
    "project_state/current_focus.md",
    "project_state/next_step.md",
    "project_state/decision_log.md",
    "project_state/lessons_learned.md",
    "project_state/conversation_handoff.md",
)


@dataclass(frozen=True)
class LaunchContext:
    """Lightweight context shown before heavy workflow execution."""

    memory_files: tuple[str, ...]
    raw_files: tuple[str, ...]
    reference_files: tuple[str, ...]
    next_step: str
    notes: tuple[str, ...] = field(default_factory=tuple)


def run_launch(
    raw_dir: str | Path = "data/01_raw",
    references_dir: str | Path = "references",
    mode: str = "launch",
) -> PipelineResult:
    """Return a launch context without running heavy tasks."""

    context = build_launch_context(raw_dir=raw_dir, references_dir=references_dir, mode=mode)
    return PipelineResult(
        name=mode,
        status="ok",
        details={
            "message": "One-line launch context prepared. No heavy data processing was started.",
            "memory_files": context.memory_files,
            "raw_files": context.raw_files,
            "reference_files": context.reference_files,
            "next_step": context.next_step,
            "notes": context.notes,
        },
    )


def run_memory_update_preview() -> PipelineResult:
    """Return a memory-update checklist without editing memory files."""

    return PipelineResult(
        name="memory-update",
        status="ok",
        details={
            "message": "Memory update preview only. Update project_state files after durable work.",
            "targets": [
                "project_state/project_memory.md",
                "project_state/lessons_learned.md",
                "project_state/conversation_handoff.md",
                "project_state/next_step.md",
                "project_state/changelog.md",
                "project_state/decision_log.md",
            ],
        },
    )


def run_skill_scout_preview(report_path: str | Path = "reports/skill_scout_report.md") -> PipelineResult:
    """Return the current skill scout report path."""

    path = Path(report_path)
    return PipelineResult(
        name="skill-scout",
        status="ok" if path.exists() else "report_missing",
        details={
            "message": "Skill scout report is available." if path.exists() else "Skill scout report has not been generated yet.",
            "report_path": str(path),
        },
    )


def build_launch_context(
    raw_dir: str | Path = "data/01_raw",
    references_dir: str | Path = "references",
    mode: str = "launch",
) -> LaunchContext:
    """Collect memory, raw file names, and reference file names."""

    memory_files = tuple(path for path in STATE_FILES if Path(path).exists())
    raw_files = tuple(_list_files(raw_dir, {".csv", ".xlsx"}))
    reference_files = tuple(_list_files(references_dir, {".docx", ".pdf", ".md", ".txt", ".csv", ".xlsx"}))
    next_step = _read_next_step()
    notes = [
        "This launcher only prepares context and recommendations.",
        "Use intake/validation/cleaning-plan before actual cleaning.",
    ]
    if mode == "continue":
        notes.append("Continue mode should prioritize project_state/conversation_handoff.md.")
    if not raw_files:
        notes.append("No supported raw files were listed; place .csv or .xlsx files under data/01_raw before data stages.")
    return LaunchContext(
        memory_files=memory_files,
        raw_files=raw_files,
        reference_files=reference_files,
        next_step=next_step,
        notes=tuple(notes),
    )


def _list_files(root: str | Path, suffixes: set[str]) -> list[str]:
    path = Path(root)
    if not path.exists():
        return []
    return sorted(
        str(item)
        for item in path.rglob("*")
        if item.is_file() and item.suffix.lower() in suffixes and not item.name.startswith("~$")
    )


def _read_next_step() -> str:
    path = Path("project_state/next_step.md")
    if not path.exists():
        return "No next_step.md found."
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return text[:1000]

