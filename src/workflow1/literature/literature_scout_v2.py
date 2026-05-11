"""Generic lightweight literature scout helpers for publication workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class LiteratureRecord:
    """Minimal literature metadata used by publication quality helpers."""

    citation_key: str
    item_type: str
    title: str
    authors: str
    year: str
    venue: str
    doi: str
    url: str
    access_status: str
    peer_reviewed: str
    journal_quartile: str
    venue_note: str
    relevance: str
    topic: str
    paper_use: str
    limitation: str


def scout_publication_literature(goal_text: str = "") -> list[LiteratureRecord]:
    """Return a small generic starter set for dry-run publication planning.

    Real projects should replace these records with verified local PDFs,
    Zotero readback, or authoritative literature searches before formal claims.
    """

    topic = goal_text.strip() or "generic predictive modeling workflow"
    return [
        LiteratureRecord(
            citation_key="DOME2021Reporting",
            item_type="article",
            title="DOME: recommendations for supervised machine learning validation in biology",
            authors="Walsh et al.",
            year="2021",
            venue="Nature Methods",
            doi="10.1038/s41592-021-01205-4",
            url="https://doi.org/10.1038/s41592-021-01205-4",
            access_status="metadata-only",
            peer_reviewed="yes",
            journal_quartile="Q1",
            venue_note="reporting guideline",
            relevance="high",
            topic=topic,
            paper_use="engineering and reporting checklist",
            limitation="metadata-only in the public template",
        ),
        LiteratureRecord(
            citation_key="TRIPODAI2024",
            item_type="guideline",
            title="TRIPOD+AI reporting guideline for prediction models using artificial intelligence",
            authors="Collins et al.",
            year="2024",
            venue="BMJ",
            doi="10.1136/bmj-2023-078378",
            url="https://doi.org/10.1136/bmj-2023-078378",
            access_status="metadata-only",
            peer_reviewed="yes",
            journal_quartile="guideline",
            venue_note="prediction model reporting guideline",
            relevance="high",
            topic=topic,
            paper_use="reporting completeness checklist",
            limitation="metadata-only in the public template",
        ),
    ]


def write_literature_outputs(run_dir: str | Path, records: Iterable[LiteratureRecord]) -> dict[str, Path]:
    """Write generic literature sidecar files inside a run directory."""

    package = Path(run_dir)
    output_dir = package / "literature"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    csv_path = output_dir / "literature_records.csv"
    md_path = output_dir / "literature_records.md"
    pd.DataFrame(rows).to_csv(csv_path, index=False, encoding="utf-8-sig")
    lines = ["# Literature Records", "", "Public-template records are placeholders until verified by a real project.", ""]
    for record in records:
        lines.append(f"- `{record.citation_key}`: {record.title} ({record.year}); access={record.access_status}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"csv": csv_path, "markdown": md_path}
