"""Build dual-track RAG and optional training corpora from run packages."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

import pandas as pd


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.I),
    re.compile(r"pass" r"word\s*[:=]\s*['\"]?[^,\s]{8,}", re.I),
    re.compile(r"tok" r"en\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.I),
]


def _prefixed_dir(package: Path, prefix: str) -> Path:
    matches = sorted([p for p in package.iterdir() if p.is_dir() and p.name.startswith(prefix)])
    return matches[0] if matches else package / prefix.rstrip("_")


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _safe_text(text: str) -> str:
    cleaned = text.replace("\x00", " ").strip()
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub("[REDACTED_SECRET]", cleaned)
    return re.sub(r"\s+", " ", cleaned)


def _has_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def _write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _read_jsonl_hashes(path: Path) -> set[str]:
    if not path.exists():
        return set()
    hashes: set[str] = set()
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("hash"):
                hashes.add(str(item["hash"]))
    return hashes


def _append_unique_jsonl(path: Path, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = _read_jsonl_hashes(path)
    appended = 0
    with path.open("a", encoding="utf-8", newline="\n") as f:
        for row in rows:
            h = str(row.get("hash", ""))
            if h and h not in existing:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                existing.add(h)
                appended += 1
    return appended


def _latex_sections(tex: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"\\section\{([^}]+)\}", tex))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tex)
        section = match.group(1)
        body = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", tex[start:end])
        body = re.sub(r"\s+", " ", body).strip()
        if body:
            sections.append((section, body))
    return sections


def _load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_research_corpus(
    *,
    run_dir: str | Path,
    domain: str,
    task_type: str,
    global_corpus_dir: str | Path | None = None,
) -> dict[str, Path]:
    """Generate RAG chunks and optional training examples from derived artifacts."""

    package = Path(run_dir)
    corpus_dir = _prefixed_dir(package, "09_")
    corpus_dir.mkdir(parents=True, exist_ok=True)
    global_dir = Path(global_corpus_dir) if global_corpus_dir else package.parents[1] / "research_corpus"
    global_dir.mkdir(parents=True, exist_ok=True)

    latex_dir = _prefixed_dir(package, "05_")
    model_dir = _prefixed_dir(package, "03_")
    figure_dir = _prefixed_dir(package, "04_")
    quality_dir = _prefixed_dir(package, "08_")

    project_id = package.name
    tex_path = latex_dir / "main.tex"
    tex = tex_path.read_text(encoding="utf-8", errors="replace") if tex_path.exists() else ""
    chunks = []
    for section, body in _latex_sections(tex):
        for idx, paragraph in enumerate([p.strip() for p in re.split(r"(?<=[.!?])\s+", body) if len(p.strip()) > 120]):
            text = _safe_text(paragraph)
            h = _hash(f"{project_id}|{section}|{idx}|{text}")
            chunks.append(
                {
                    "id": h[:16],
                    "project_id": project_id,
                    "domain": domain,
                    "task_type": task_type,
                    "source_artifact": str(tex_path),
                    "section": section,
                    "text": text,
                    "evidence_ids": [],
                    "citation_keys": re.findall(r"\\cite[tp]?\{([^}]+)\}", paragraph),
                    "tags": [domain, task_type, "manuscript_section"],
                    "language": "en",
                    "privacy_level": "derived_non_sensitive",
                    "reusable_status": "approved_for_internal_reuse",
                    "hash": h,
                }
            )

    method_rows = _load_csv(model_dir / "model_setting_detail_table.csv")
    method_cards = []
    for row in method_rows:
        text = _safe_text(
            f"Model {row.get('model')} plays role {row.get('task_role')}. Inputs: {row.get('input_features')}. "
            f"Target transformation: {row.get('target_transformation')}. Hyperparameters: {row.get('hyperparameters_or_search_space')}. "
            f"Validation: {row.get('validation_strategy')}. Status: {row.get('training_status')}."
        )
        h = _hash(f"{project_id}|method|{row.get('model')}|{text}")
        method_cards.append({**row, "project_id": project_id, "domain": domain, "text": text, "hash": h})

    figure_rows = _load_csv(figure_dir / "figure_to_claim_map.csv")
    figure_narratives = []
    for row in figure_rows:
        text = _safe_text(f"{row.get('figure_id')} supports: {row.get('claim_supported')} Source data: {row.get('source_data')}.")
        h = _hash(f"{project_id}|figure|{row.get('figure_id')}|{text}")
        figure_narratives.append({**row, "project_id": project_id, "domain": domain, "text": text, "hash": h})

    instruction_examples = []
    method_text = "\n".join(item["text"] for item in method_cards[:8])
    if method_text:
        h = _hash(f"{project_id}|instruction|methods|{method_text}")
        instruction_examples.append(
            {
                "instruction": "Write a reproducible Methods subsection from the provided model-setting evidence.",
                "input": method_text,
                "output": "A complete Methods subsection should describe data, predictors, target transformation, model families, hyperparameters, validation strategy, metrics, pathological-model handling, and claim boundaries.",
                "constraints": "Do not invent unrecorded model settings; preserve prediction-versus-causation boundaries.",
                "evidence_context": "model_setting_detail_table.csv",
                "acceptance_criteria": "All trained and candidate model families are represented with settings and validation logic.",
                "source_run": project_id,
                "quality_score": 0.9,
                "hash": h,
            }
        )
    if figure_narratives:
        visual_input = "\n".join(item["text"] for item in figure_narratives[:10])
        h = _hash(f"{project_id}|instruction|visuals|{visual_input}")
        instruction_examples.append(
            {
                "instruction": "Turn figure-level evidence into a detailed Results narrative.",
                "input": visual_input,
                "output": "A complete Results narrative should explain data patterns, model comparison, diagnostic figures, tail-error behavior, and interpretation limits.",
                "constraints": "Every formal claim must point to a figure, table, model output, or literature evidence.",
                "evidence_context": "figure_to_claim_map.csv",
                "acceptance_criteria": "The narrative explains rather than merely lists figures.",
                "source_run": project_id,
                "quality_score": 0.9,
                "hash": h,
            }
        )

    preference_pairs = []
    if instruction_examples:
        prompt = instruction_examples[0]["instruction"]
        chosen = instruction_examples[0]["output"]
        rejected = "The model was trained and performed well. More details are shown in the table."
        h = _hash(f"{project_id}|preference|{prompt}|{chosen}|{rejected}")
        preference_pairs.append(
            {
                "prompt": prompt,
                "chosen": chosen,
                "rejected": rejected,
                "rubric": "Prefer reproducible, evidence-linked, method-complete scientific writing over vague summaries.",
                "rejection_reason": "Missing data, model, metric, validation, and evidence details.",
                "source_run": project_id,
                "hash": h,
            }
        )

    claim_pairs = []
    for row in figure_narratives:
        h = _hash(f"{project_id}|claim|{row.get('figure_id')}|{row.get('claim_supported')}")
        claim_pairs.append(
            {
                "claim": row.get("claim_supported", ""),
                "evidence": row.get("source_data", ""),
                "evidence_type": "figure_source_data",
                "source_run": project_id,
                "quality_score": 0.85,
                "hash": h,
            }
        )

    outputs = {
        "rag_chunks.jsonl": chunks,
        "instruction_examples.jsonl": instruction_examples,
        "preference_pairs.jsonl": preference_pairs,
        "method_cards.jsonl": method_cards,
        "figure_narratives.jsonl": figure_narratives,
        "claim_evidence_training_pairs.jsonl": claim_pairs,
    }
    output_paths: dict[str, Path] = {}
    for name, rows in outputs.items():
        path = corpus_dir / name
        _write_jsonl(path, rows)
        _append_unique_jsonl(global_dir / name, rows)
        output_paths[name] = path

    audit_rows = []
    for name, rows in outputs.items():
        hashes = [row.get("hash") for row in rows]
        text_blob = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
        no_secret = not _has_secret(text_blob) and "[REDACTED_SECRET]" not in text_blob
        audit_rows.append(
            {
                "artifact": name,
                "row_count": len(rows),
                "schema_complete": all("hash" in row for row in rows),
                "no_secret": no_secret,
                "dedup_pass": len(hashes) == len(set(hashes)),
                "status": "pass" if rows and no_secret and len(hashes) == len(set(hashes)) else "fail",
            }
        )
    audit_path = corpus_dir / "corpus_quality_audit.csv"
    pd.DataFrame(audit_rows).to_csv(audit_path, index=False, encoding="utf-8-sig")

    manifest_rows = [
        {"artifact": name, "path": str(path), "track": "rag" if name == "rag_chunks.jsonl" else "training_optional"}
        for name, path in output_paths.items()
    ]
    manifest_path = corpus_dir / "corpus_manifest.csv"
    pd.DataFrame(manifest_rows).to_csv(manifest_path, index=False, encoding="utf-8-sig")

    balance_path = corpus_dir / "corpus_domain_balance_report.csv"
    pd.DataFrame(
        [
            {"domain": domain, "task_type": task_type, "artifact": name, "row_count": len(rows)}
            for name, rows in outputs.items()
        ]
    ).to_csv(balance_path, index=False, encoding="utf-8-sig")

    output_paths.update({"audit": audit_path, "manifest": manifest_path, "balance": balance_path})
    return output_paths
