"""Structured placeholders for reference summaries."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from workflow1.references.reader import ReferenceReadResult


@dataclass(frozen=True)
class ReferenceSummary:
    """A lightweight Chinese-first summary placeholder."""

    source_path: Path
    status: str
    summary: str
    actionable_requirements: tuple[str, ...] = ()
    potential_conflicts: tuple[str, ...] = ()
    recommended_use: str = ""
    warnings: tuple[str, ...] = field(default_factory=tuple)


def summarize_reference(result: ReferenceReadResult) -> ReferenceSummary:
    """Return a structured placeholder summary for future workflow use."""

    if result.status != "ok":
        return ReferenceSummary(
            source_path=result.document.path,
            status=result.status,
            summary="参考文件未能完整读取，暂不能提取可靠的方法要求。",
            potential_conflicts=("需要人工确认文件是否可读、是否为扫描版 PDF、是否加密或是否需要 OCR。",),
            recommended_use="在后续工作流中仅记录该参考文件存在，不应自动套用其内容。",
            warnings=result.warnings,
        )

    preview = " ".join(result.text.split())[:500]
    return ReferenceSummary(
        source_path=result.document.path,
        status=result.status,
        summary=f"已提取参考文件文本。当前轻量 summarizer 仅返回预览，正式任务中应基于全文生成中文方法摘要。预览：{preview}",
        actionable_requirements=(
            "在实际清洗、建模、仿真、优化、可视化或报告任务前，结合用户目标与数据证据提取可执行要求。",
            "不要将参考文件建议自动覆盖用户明确指令或实际数据证据。",
        ),
        recommended_use="将该文件作为后续任务的方法参考，并在 workflow summaries 中按路径引用。",
        warnings=result.warnings,
    )

