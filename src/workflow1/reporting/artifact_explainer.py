"""Artifact explanation helpers.

These helpers are intentionally lightweight. They create structured rows that
task scripts can write to Markdown/CSV explanation indexes.
"""

from __future__ import annotations

from pathlib import Path


def explain_artifact(
    path: Path,
    *,
    purpose: str,
    source: str,
    method: str,
    reading_guide: str,
    paper_section: str,
    formal_status: str = "experimental_or_not_formal_until_verified",
    limitations: str = "",
) -> dict[str, str]:
    """Return a standard artifact explanation row."""

    return {
        "file_path": str(path),
        "file_type": path.suffix.lower().lstrip(".") or "no_ext",
        "purpose": purpose,
        "input_source": source,
        "generation_method": method,
        "how_to_read": reading_guide,
        "paper_section": paper_section,
        "formal_status": formal_status,
        "limitations": limitations,
    }


def unable_to_verify(path: Path, reason: str) -> dict[str, str]:
    """Create a standardized unable-to-verify explanation row."""

    return explain_artifact(
        path,
        purpose="unable_to_verify",
        source="unknown",
        method="not generated or not readable",
        reading_guide=f"Do not use this artifact for claims. Reason: {reason}",
        paper_section="none",
        formal_status="not_usable",
        limitations=reason,
    )
