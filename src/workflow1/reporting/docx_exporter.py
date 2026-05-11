"""Safe DOCX export wrapper.

Uses python-docx when available. If unavailable, writes a Markdown fallback and
returns a degraded-but-continued status instead of blocking paper QA.
"""
from __future__ import annotations

from pathlib import Path


def export_docx(markdown_text: str, output_path: str | Path) -> dict:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        from docx import Document  # type: ignore
        doc = Document()
        for line in markdown_text.splitlines():
            doc.add_paragraph(line)
        doc.save(out)
        return {"status": "pass", "output_path": str(out), "fallback": False}
    except Exception as exc:  # pragma: no cover - optional dependency fallback
        fallback = out.with_suffix(".md")
        fallback.write_text(markdown_text, encoding="utf-8")
        return {"status": "degraded_markdown_fallback", "output_path": str(fallback), "fallback": True, "error": str(exc)}
