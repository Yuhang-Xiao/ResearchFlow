from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    if text.strip() not in existing:
        path.write_text(existing.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def policy_yaml(name: str, title: str, gates: list[str]) -> str:
    checks = "\n".join(f"  - id: {name}_{i:02d}\n    check: {gate}\n    severity: high\n    required: true" for i, gate in enumerate(gates, 1))
    return f"""name: {name}
title: {title}
version: 1
created_at: "{NOW}"
scope: workflow1 scientific research quality assurance
default_language: zh-CN
principles:
  - data_first: every result must be traceable to validated data, model output, figure/table, or literature evidence
  - prototype_guard: prototype and experimental results must not be written as formal policy conclusions
  - benchmark_first: major methods, figures, tables, and paper sections must be checked against top-journal exemplars
  - safe_adaptation: external tools may inspire local rules, but installation, services, APIs, MCP, and database writes require approval
required_checks:
{checks}
stop_conditions:
  - missing required input or lineage
  - unresolved core data validation error
  - formal DQN/RL parameters not confirmed by user
  - citation cannot be verified but is needed for a formal claim
  - result claim is stronger than available evidence
outputs:
  - quality_gate_table
  - issue_log
  - repair_log
  - approval_queue_entry_when_needed
"""


def build_research_quality() -> None:
    rq = ROOT / "research_quality"
    common = [
        "输入数据、派生数据、表格、图表、模型输出和论文论断必须具有 lineage 或 evidence map",
        "报告中的数字必须能回查到 CSV/XLSX/模型日志，不允许手工漂移",
        "正式结论必须通过 result claim guard；experimental/prototype 必须显式标注",
        "引用必须核验 DOI、题名、作者、年份、期刊或 URL 元数据",
        "高风险外部插件、MCP、API key、大型依赖、Zotero 数据库写入必须进入 approval queue",
    ]
    files = {
        "research_quality_policy.yaml": common + ["每次科研任务结束后必须执行质量核验和自我改进复盘"],
        "data_validation_policy.yaml": ["生成前检查输入 schema、row count、column count、key fields", "生成后检查缺失、重复、异常、单位、字段映射", "不得修改 data/01_raw"],
        "derived_data_validation_policy.yaml": ["每个派生文件必须记录输入来源、转换规则、输出摘要", "每个任务包必须生成 data_lineage_manifest.csv", "自动修复写 repair log，无法修复写 issue log"],
        "model_comparison_policy.yaml": ["每次模型运行至少包含一个 simple baseline", "高级模型必须与可解释启发式比较", "所有模型使用一致 split、预算、约束和指标"],
        "model_validation_policy.yaml": ["训练前检查 leakage、split、target、unit of analysis", "训练后检查 metric、uncertainty、calibration、segment performance", "模型输出必须区分可用于论文、prototype、blocked"],
        "top_journal_benchmark_policy.yaml": ["方法、图表、结果、论文段落生成前后必须对标高质量论文", "无法全文读取时标记 abstract-only 或 metadata-only", "记录可借鉴点和不可直接套用点"],
        "result_claim_guard_policy.yaml": ["每个结果论断必须映射到数据、模型、图表或文献依据", "未收敛模型不能写成有效策略", "baseline 不公平时不能声称优于 baseline"],
        "chart_table_qa_policy.yaml": ["图表必须检查空图、坐标轴、中文字体、PNG/SVG 输出和数据来源", "表格必须检查 row/column count、主键、单位和报告数字一致性"],
        "citation_verification_policy.yaml": ["引用必须用 DOI/CrossRef/OpenAlex/Semantic Scholar 或本地 PDF 元数据核验", "核验失败引用不得支持 formal claim", "每段论文输出附 citation evidence table"],
        "paper_section_review_policy.yaml": ["论文部分生成必须先有 outline、evidence map、citation table、claim guard、Reviewer 2 audit", "DOCX 输出必须保留对应 Markdown/CSV 证据"],
        "adversarial_review_policy.yaml": ["对方法、数据、论断、图表、引用执行 adversarial/reviewer2 风格质疑", "记录 major/minor issues、修订建议和是否阻断论文写入"],
        "reproducibility_policy.yaml": ["记录 code version、input hash、config、random seed、environment、runtime", "实验可复现性不足时只能标记 prototype"],
    }
    write(rq / "README.md", """# 科研质量核验总体系

本目录定义 workflow1 的研究质量总闸门。后续数据生成、派生数据、模型训练、图表、表格、引用、论文段落和工作流自我升级都必须先经过对应 policy。

核心原则：先核验、再建模；先对标、再写作；先 evidence map、再 conclusion；prototype 不冒充 formal。
""")
    for fn, gates in files.items():
        write(rq / fn, policy_yaml(fn.removesuffix(".yaml"), fn.removesuffix(".yaml").replace("_", " ").title(), gates))
    checklist = {
        "checklist": [
            "pre_generation_data_validation",
            "post_generation_data_validation",
            "derived_data_lineage",
            "table_result_consistency",
            "chart_nonblank_and_font_check",
            "model_preflight_validation",
            "model_postrun_diagnostics",
            "multi_model_fair_comparison",
            "baseline_fairness",
            "reward_convergence_constraint_audit",
            "result_claim_guard",
            "literature_support_check",
            "citation_verification",
            "top_journal_benchmark",
            "reviewer2_audit",
            "reproducibility_record",
            "approval_required_items",
        ]
    }
    write(rq / "research_quality_checklist.yaml", json.dumps(checklist, ensure_ascii=False, indent=2))


def build_quality_modules() -> None:
    quality = ROOT / "src" / "workflow1" / "quality"
    write(quality / "__init__.py", '"""Lightweight research quality guards for workflow1."""\n')
    modules = {
        "evidence_strength_classifier.py": '''"""Classify evidence strength for research claims."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceStrength:
    level: str
    can_support_results: bool
    can_support_formal_claim: bool
    reason: str


def classify_evidence(evidence: dict) -> EvidenceStrength:
    kind = str(evidence.get("kind", "")).lower()
    verified = bool(evidence.get("verified", False))
    formal = bool(evidence.get("formal_parameters_confirmed", False))
    converged = evidence.get("converged", True)
    if kind in {"validated_data", "verified_table", "verified_model"} and verified and formal and converged:
        return EvidenceStrength("formal_ready", True, True, "validated and confirmed evidence")
    if kind in {"validated_data", "verified_table", "verified_model", "peer_reviewed_literature"} and verified:
        return EvidenceStrength("evidence_supported", True, False, "usable evidence, but not formal-policy ready")
    if kind in {"prototype_model", "synthetic_parameter", "abstract_only_literature"}:
        return EvidenceStrength("prototype_only", False, False, "prototype or limited evidence")
    return EvidenceStrength("insufficient", False, False, "missing or unverified evidence")
''',
        "claim_to_evidence_mapper.py": '''"""Map result claims to evidence records."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimEvidenceLink:
    claim_id: str
    claim: str
    evidence_id: str
    evidence_kind: str
    status: str
    note: str


def map_claims_to_evidence(claims: list[dict], evidence: list[dict]) -> list[ClaimEvidenceLink]:
    by_id = {str(item.get("evidence_id")): item for item in evidence}
    links: list[ClaimEvidenceLink] = []
    for idx, claim in enumerate(claims, 1):
        evidence_id = str(claim.get("evidence_id", ""))
        item = by_id.get(evidence_id)
        if not item:
            links.append(ClaimEvidenceLink(str(claim.get("claim_id", idx)), str(claim.get("claim", "")), evidence_id, "", "missing_evidence", "claim has no matching evidence"))
            continue
        links.append(ClaimEvidenceLink(str(claim.get("claim_id", idx)), str(claim.get("claim", "")), evidence_id, str(item.get("kind", "")), "mapped", "evidence found"))
    return links
''',
        "result_claim_guard.py": '''"""Guard research result claims against overstatement."""
from __future__ import annotations

from dataclasses import asdict

from workflow1.quality.claim_to_evidence_mapper import map_claims_to_evidence
from workflow1.quality.evidence_strength_classifier import classify_evidence


FORBIDDEN_ESCALATIONS = [
    ("experimental", "formal"),
    ("prototype", "policy recommendation"),
    ("synthetic parameter", "confirmed parameter"),
    ("unconverged", "effective strategy"),
]


def audit_claims(claims: list[dict], evidence: list[dict]) -> dict:
    links = map_claims_to_evidence(claims, evidence)
    evidence_by_id = {str(item.get("evidence_id")): item for item in evidence}
    findings = []
    for link in links:
        item = evidence_by_id.get(link.evidence_id, {})
        strength = classify_evidence(item)
        claim_text = link.claim.lower()
        status = "pass"
        reason = strength.reason
        if link.status == "missing_evidence":
            status = "block"
            reason = link.note
        elif any(src in claim_text and dst in claim_text for src, dst in FORBIDDEN_ESCALATIONS):
            status = "block"
            reason = "claim contains forbidden escalation"
        elif "formal" in claim_text and not strength.can_support_formal_claim:
            status = "block"
            reason = "formal claim requires confirmed, validated, converged evidence"
        elif not strength.can_support_results:
            status = "revise"
            reason = strength.reason
        findings.append({**asdict(link), "evidence_strength": strength.level, "guard_status": status, "reason": reason})
    return {"status": "pass" if all(f["guard_status"] == "pass" for f in findings) else "needs_revision_or_blocked", "findings": findings}
''',
        "data_generation_validator.py": '''"""Lightweight data generation validation utilities."""
from __future__ import annotations

import csv
from pathlib import Path


def summarize_table(path: str | Path, key_fields: list[str] | None = None) -> dict:
    p = Path(path)
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []
    return {
        "path": str(p),
        "row_count": len(rows),
        "column_count": len(fields),
        "key_fields": key_fields or [],
        "missing_key_fields": [k for k in (key_fields or []) if k not in fields],
        "status": "pass" if fields else "fail_no_columns",
    }


def validate_generated_output(path: str | Path, source_paths: list[str], key_fields: list[str] | None = None) -> dict:
    summary = summarize_table(path, key_fields)
    summary["source_paths"] = source_paths
    summary["has_lineage"] = bool(source_paths)
    if not summary["has_lineage"]:
        summary["status"] = "fail_missing_lineage"
    return summary
''',
        "derived_data_lineage.py": '''"""Derived data lineage manifest helpers."""
from __future__ import annotations

import csv
from pathlib import Path


def write_lineage_manifest(path: str | Path, records: list[dict]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fields = ["output_path", "source_paths", "transform", "row_count", "column_count", "status", "notes"]
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})
''',
        "table_consistency_checker.py": '''"""Check consistency between report claims and table values."""
from __future__ import annotations


def compare_report_numbers(report_numbers: dict[str, float], table_numbers: dict[str, float], tolerance: float = 1e-9) -> list[dict]:
    findings = []
    for key, report_value in report_numbers.items():
        table_value = table_numbers.get(key)
        if table_value is None:
            findings.append({"metric": key, "status": "missing_in_table", "report_value": report_value, "table_value": ""})
        elif abs(float(report_value) - float(table_value)) > tolerance:
            findings.append({"metric": key, "status": "mismatch", "report_value": report_value, "table_value": table_value})
        else:
            findings.append({"metric": key, "status": "pass", "report_value": report_value, "table_value": table_value})
    return findings
''',
        "chart_data_consistency_checker.py": '''"""Lightweight chart QA and data-source consistency checks."""
from __future__ import annotations

from pathlib import Path


def audit_chart_file(chart_path: str | Path, data_path: str | Path | None = None) -> dict:
    chart = Path(chart_path)
    exists = chart.exists()
    size = chart.stat().st_size if exists else 0
    status = "pass" if exists and size > 512 else "fail_blank_or_missing"
    return {
        "chart_path": str(chart),
        "data_path": str(data_path) if data_path else "",
        "chart_exists": exists,
        "chart_size_bytes": size,
        "has_data_source": data_path is not None,
        "status": status if data_path else "fail_missing_data_source",
    }
''',
        "model_validation.py": '''"""Model validation and comparison guards."""
from __future__ import annotations


def audit_model_comparison(rows: list[dict]) -> dict:
    baselines = [r for r in rows if str(r.get("model_role", "")).lower() == "baseline"]
    comparable = all(r.get("split_id") == rows[0].get("split_id") for r in rows) if rows else False
    required = ["primary_metric", "secondary_metrics", "uncertainty", "runtime", "parameter_count", "interpretability", "paper_usable"]
    missing = sorted({field for r in rows for field in required if field not in r or r.get(field) in {"", None}})
    status = "pass" if rows and baselines and comparable and not missing else "fail"
    return {"status": status, "baseline_count": len(baselines), "same_split": comparable, "missing_fields": missing}
''',
    }
    for fn, text in modules.items():
        write(quality / fn, text)

    reporting = ROOT / "src" / "workflow1" / "reporting"
    write(reporting / "__init__.py", '"""Paper reporting orchestration helpers."""\n')
    reporting_modules = {
        "section_evidence_mapper.py": '''"""Build evidence maps for paper sections."""
from __future__ import annotations


def build_section_evidence_map(section: str, claims: list[dict], citations: list[dict]) -> dict:
    return {"section": section, "claims": claims, "citations": citations, "requires_claim_guard": True, "requires_citation_verification": True}
''',
        "paper_quality_auditor.py": '''"""Paper section quality gates."""
from __future__ import annotations


def audit_paper_section(section_map: dict) -> dict:
    claims = section_map.get("claims", [])
    citations = section_map.get("citations", [])
    findings = []
    if not claims:
        findings.append("missing_claims")
    if not citations:
        findings.append("missing_citations")
    if not section_map.get("top_journal_benchmark"):
        findings.append("missing_top_journal_benchmark")
    return {"status": "pass" if not findings else "needs_revision", "findings": findings}
''',
        "docx_exporter.py": '''"""Safe DOCX export wrapper.

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
''',
        "paper_section_orchestrator.py": '''"""Orchestrate safe paper section generation QA."""
from __future__ import annotations

from workflow1.reporting.paper_quality_auditor import audit_paper_section
from workflow1.reporting.section_evidence_mapper import build_section_evidence_map


def plan_paper_section(section: str, claims: list[dict], citations: list[dict], benchmark: str | None = None) -> dict:
    evidence_map = build_section_evidence_map(section, claims, citations)
    evidence_map["top_journal_benchmark"] = benchmark
    audit = audit_paper_section(evidence_map)
    return {"section": section, "outline_required": True, "evidence_map": evidence_map, "quality_audit": audit, "docx_export_required": True}
''',
    }
    for fn, text in reporting_modules.items():
        write(reporting / fn, text)


def build_skills() -> None:
    specs = [
        ("research-quality-orchestrator", "核验结果, quality gate, 科研质量核验, result claim guard"),
        ("top-journal-benchmark-scout", "顶级期刊对标, top journal benchmark, 高质量论文检索"),
        ("top-journal-method-comparator", "方法对标, 模型设定对标, top journal method comparator"),
        ("literature-coverage-auditor", "文献覆盖, literature coverage, 文献质量检查"),
        ("citation-and-reference-verifier", "citation verification, 引用核验, DOI核验"),
        ("data-generation-validator", "数据生成核验, generated data validation, 数据输出检查"),
        ("derived-data-lineage-auditor", "派生数据核验, lineage audit, data_lineage_manifest"),
        ("table-result-consistency-checker", "表格和报告数字核对, table consistency"),
        ("chart-quality-auditor", "图表 QA, 空图检测, 中文字体, PNG 输出"),
        ("model-comparison-auditor", "模型对比, 多模型比较, model comparison"),
        ("baseline-fairness-auditor", "baseline fairness, baseline 公平性, 可解释对照"),
        ("model-validation-and-diagnostics-runner", "模型验证, diagnostics, drift, leakage"),
        ("reward-convergence-constraint-auditor", "reward audit, convergence check, constraint violation"),
        ("result-claim-guard", "result claim guard, 论文论断保护, 过度推断"),
        ("adversarial-reviewer", "adversarial reviewer, 对抗式审稿, robust audit"),
        ("reviewer2-style-auditor", "reviewer 2 audit, Reviewer 2 风格自审"),
        ("reproducibility-auditor", "reproducibility, 可复现实验, seed/config/hash"),
        ("paper-section-quality-reviewer", "论文质量检查, paper section review, Word 输出前核验"),
        ("zotero-writeback-and-note-validator", "Zotero 写入计划, 无乱码中文笔记, citation verification"),
        ("workflow-quality-memory-updater", "任务结束质量复盘, project memory, workflow improvement backlog"),
    ]
    base_body = """---
name: {name}
description: Use when the task mentions {triggers}. It enforces workflow1 research quality gates and produces Chinese-first audit outputs.
---

# {title}

## Trigger Phrases

{trigger_list}

## When To Use

Use for scientific workflow tasks that need research-quality validation, top-journal benchmarking, citation checking, model comparison, paper section QA, or workflow-quality memory updates.

## When Not To Use

- Do not use to run formal DQN/RL training without user-confirmed parameters.
- Do not use to modify `data/01_raw`.
- Do not install external tools, MCP servers, APIs, large dependencies, or write Zotero databases without approval.

## Inputs

- Current task run package.
- Relevant `research_quality/*.yaml` policy files.
- Source data, derived tables, model logs, charts, paper drafts, or citation metadata as applicable.
- `project_state/` and latest `outputs/_index/` files.

## Outputs

- Chinese audit report in the task package.
- CSV quality gate table or issue log.
- Repair log when auto-repair is safe.
- Approval queue entries for high-risk external integrations.

## Required Checks

- Verify lineage/evidence before accepting results.
- Distinguish prototype, experimental, evidence-supported, and formal-ready outputs.
- Check table/report/chart/model/citation consistency according to the matching policy.
- Record stop conditions and next step in `project_state`.

## Stop Conditions

- Missing critical input.
- Unresolved data lineage or citation failure needed for a formal claim.
- User confirmation required for formal DQN/RL parameters, policy conclusions, Zotero database writes, MCP/plugin/API installation, or large dependency installation.

## Project State Updates

Update `project_state/project_memory.md`, `lessons_learned.md`, `conversation_handoff.md`, `next_step.md`, `changelog.md`, and `decision_log.md` when the audit creates durable rules, blockers, or outputs.
"""
    rows = []
    for name, triggers in specs:
        trigger_list = "\n".join(f"- {x.strip()}" for x in triggers.split(","))
        content = base_body.format(name=name, title=name.replace("-", " ").title(), triggers=triggers, trigger_list=trigger_list)
        for base in [ROOT / "skills", ROOT / ".agents" / "skills"]:
            write(base / name / "SKILL.md", content)
        rows.append({"skill": name, "triggers": triggers, "synced_to_skills": "true", "synced_to_agents": "true", "status": "new_or_upgraded"})
    write_csv(RUN / "02_表格输出" / "new_or_upgraded_quality_skills.csv", rows)

    writer_skills = ["academic-writing-and-results-writer", "paper-result-writer", "literature-review-writer", "introduction-writer", "method-writer", "discussion-writer", "word-exporter-docx"]
    for name in writer_skills:
        content = base_body.format(name=name, title=name.replace("-", " ").title(), triggers="论文质量检查, evidence map, citation verification, result claim guard, Word DOCX 输出", trigger_list="- 论文质量检查\n- evidence map\n- citation verification\n- result claim guard\n- Word DOCX 输出")
        for base in [ROOT / "skills", ROOT / ".agents" / "skills"]:
            write(base / name / "SKILL.md", content)


def build_benchmark_and_registries() -> None:
    bench = ROOT / "references" / "top_journal_benchmark"
    write(bench / "README.md", """# 顶级期刊文章对标机制

本目录长期维护 workflow1 的高质量论文对标库。任何模型、图表、结果或论文段落生成前后，都应读取相关 registry，并标记全文读取状态：full-text、abstract-only 或 metadata-only。
""")
    papers = [
        ("Human-level control through deep reinforcement learning", "Mnih et al.", "2015", "Nature", "10.1038/nature14236", "DQN/RL 文献", "full-text-local-note", "DQN baseline and training reporting"),
        ("Deepchecks: A Library for Testing and Validating Machine Learning Models and Data", "Gordeev et al.", "2022", "JMLR", "https://jmlr.org/papers/v23/22-0281.html", "模型验证", "metadata-only", "data/model validation suites"),
        ("Optuna: A Next-generation Hyperparameter Optimization Framework", "Akiba et al.", "2019", "KDD", "10.1145/3292500.3330701", "实验设计/调参", "metadata-only", "reproducible optimization"),
        ("Curie: Toward Rigorous and Automated Scientific Experimentation with AI Agents", "Kon et al.", "2025", "arXiv", "https://arxiv.org/abs/2502.16069", "自动科研 benchmark", "metadata-only", "rigor modules and experiment QA"),
        ("OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts", "Priem et al.", "2022", "arXiv", "https://arxiv.org/abs/2205.01833", "引用核验", "metadata-only", "open bibliographic verification"),
    ]
    rows = []
    for title, authors, year, venue, doi, category, read_status, support in papers:
        rows.append({
            "title": title,
            "authors": authors,
            "year": year,
            "journal_or_conference": venue,
            "doi_or_url": doi,
            "full_text_status": read_status,
            "is_top_or_high_quality": "yes",
            "category": category,
            "supports_workflow1": support,
            "method_setting": "to_extract_in_future_full_read",
            "data_structure": "to_extract",
            "model_comparison": "required_if_model_paper",
            "metrics": "to_extract",
            "figures_tables": "to_extract",
            "limitations": "must_record",
            "adaptable_points": support,
            "non_transferable_points": "do_not_directly_copy_without domain validation",
            "workflow1_requirements": "benchmark before formal reporting",
        })
    for fn in ["top_journal_benchmark_registry.csv", "method_benchmark_matrix.csv", "result_reporting_benchmark_matrix.csv", "figure_table_benchmark_matrix.csv", "writing_style_benchmark_matrix.csv"]:
        write_csv(bench / fn, rows)
    write_csv(RUN / "02_表格输出" / "top_journal_benchmark_initial_registry.csv", rows)

    mc = ROOT / "model_registry"
    protocols = {
        "model_comparison_protocol.yaml": "all model experiments require baseline, same split, same budget/constraints, uncertainty, runtime, parameter_count, interpretability, paper_usable",
        "baseline_policy_registry.yaml": "simple baselines include random, historical, heuristic, risk-ranking, logistic/regression/tree, naive/seasonal-naive",
        "rl_comparison_protocol.yaml": "RL/DQN must compare heuristic, Q-learning, random, historical, risk-ranking under same constraints and budget",
        "supervised_model_comparison_protocol.yaml": "supervised learning must compare logistic/regression/tree baseline and leakage-safe splits",
        "simulation_comparison_protocol.yaml": "simulation must compare status quo, random, heuristic, sensitivity and uncertainty scenarios",
    }
    for fn, desc in protocols.items():
        write(mc / fn, f"""name: {fn.removesuffix('.yaml')}
version: 1
created_at: "{NOW}"
description: "{desc}"
required_fields:
  - model_name
  - model_role
  - split_id
  - primary_metric
  - secondary_metrics
  - uncertainty
  - runtime
  - parameter_count
  - interpretability
  - constraints
  - paper_usable
quality_gates:
  - at_least_one_simple_baseline
  - same_data_split_budget_constraints_metrics
  - advanced_model_compared_to_interpretable_control
  - formal_claims_require_user_confirmation
""")
    baseline_rows = [
        {"task_family": "RL/DQN", "required_baselines": "random; historical; heuristic; risk-ranking; Q-learning", "notes": "same budget/capacity/constraints"},
        {"task_family": "supervised_classification", "required_baselines": "majority; logistic; decision tree", "notes": "same split and leakage-safe features"},
        {"task_family": "regression", "required_baselines": "mean/median; linear regression; tree", "notes": "include uncertainty"},
        {"task_family": "time_series", "required_baselines": "naive; seasonal naive", "notes": "temporal split only"},
        {"task_family": "causal_inference", "required_baselines": "balance; robustness; placebo", "notes": "do not rely on prediction metric only"},
    ]
    write_csv(RUN / "02_表格输出" / "model_comparison_required_baselines.csv", baseline_rows)


def build_tool_reports() -> None:
    candidates = [
        ("OpenAI Codex Skills", "https://github.com/openai/skills", "official skill catalog", "skill packaging conventions", 4, "safe_adapt", "use SKILL.md layout only"),
        ("ComposioHQ/awesome-codex-skills", "https://github.com/ComposioHQ/awesome-codex-skills", "Codex skills collection", "trigger phrase and folder conventions", 4, "safe_adapt", "do not install"),
        ("K-Dense-AI/scientific-agent-skills", "https://github.com/K-Dense-AI/scientific-agent-skills", "scientific skills", "domain skill structure and scientific QA breadth", 4, "safe_adapt", "dependencies require approval"),
        ("Curie", "https://github.com/Just-Curieous/Curie", "rigorous automated experimentation", "rigor modules, experiment knowledge, reporting", 5, "concept_adapt", "Docker/execution requires approval"),
        ("karpathy/autoresearch", "https://github.com/karpathy/autoresearch", "auto experiment loop", "experiment ledger and keep/discard based on metric", 4, "concept_adapt", "do not run overnight experiments"),
        ("ResearchClawBench", "https://github.com/InternScience/ResearchClawBench", "AI research benchmark", "benchmark-style task evaluation", 4, "concept_adapt", "external benchmark execution requires approval"),
        ("Deepchecks", "https://github.com/deepchecks/deepchecks", "data/model validation and drift", "validation suite ideas", 5, "approval_queue_for_install", "dependency install needed"),
        ("Great Expectations", "https://docs.greatexpectations.io/", "data quality expectations", "expectation suite and data docs idea", 5, "approval_queue_for_install", "dependency setup needed"),
        ("Pandera", "https://pandera.readthedocs.io/", "DataFrame schema validation", "schema/check contracts", 5, "approval_queue_for_install", "dependency install optional"),
        ("Evidently", "https://github.com/evidentlyai/evidently", "drift and monitoring", "data/model drift metrics", 4, "approval_queue_for_install", "dependency/server optional"),
        ("MLflow", "https://mlflow.org/docs/latest/ml/tracking/", "experiment tracking", "run tracking and model registry schema", 5, "approval_queue_for_install", "tracking server requires approval"),
        ("DVC", "https://dvc.org/doc", "data/model versioning", "reproducible data lineage", 4, "approval_queue_for_install", "data remote setup requires approval"),
        ("Optuna", "https://github.com/optuna/optuna", "hyperparameter optimization", "trial ledger and pruning concepts", 4, "approval_queue_for_install", "dependency install needed"),
        ("markrussinovich/refchecker", "https://github.com/markrussinovich/refchecker", "academic reference validation", "reference verification workflow", 4, "approval_queue_for_api", "LLM/provider/API use requires approval"),
        ("amazon-science/RefChecker", "https://github.com/amazon-science/RefChecker", "claim/reference hallucination checker", "claim-triplet evidence checking", 4, "concept_adapt", "heavy model dependencies not installed"),
        ("Zotero MCP servers", "https://github.com/swairshah/zotero-mcp-server", "Zotero MCP", "library read/search workflow", 3, "approval_queue", "MCP/database/API risks"),
        ("OpenAlex/CrossRef/Semantic Scholar", "https://api.crossref.org/", "citation metadata APIs", "deterministic DOI metadata checks", 5, "safe_plan", "API/network use only, no keys by default"),
    ]
    rows = [{
        "candidate": c[0], "url": c[1], "category": c[2], "useful_for": c[3], "score_1_5": str(c[4]), "adoption_mode": c[5], "risk_or_condition": c[6]
    } for c in candidates]
    for fn in ["quality_validation_skill_candidates.csv", "quality_validation_tool_evaluation_matrix.csv", "validation_skill_search_results.csv"]:
        write_csv(RUN / "02_表格输出" / fn, rows)
    safe_rows = [r for r in rows if r["adoption_mode"] in {"safe_adapt", "concept_adapt", "safe_plan"}]
    write_csv(RUN / "02_表格输出" / "quality_validation_safe_adaptation_plan.csv", safe_rows)
    approval_rows = [r for r in rows if "approval" in r["adoption_mode"]]
    for fn in ["external_validation_plugin_approval_queue.csv", "approval_required_external_tools.csv", "approval_required_external_tools.csv"]:
        write_csv(RUN / "02_表格输出" / fn, approval_rows)
    write_csv(RUN / "02_表格输出" / "quality_validation_tool_evaluation_matrix.csv", rows)
    write_csv(RUN / "02_表格输出" / "citation_verification_tool_candidates.csv", [r for r in rows if "citation" in r["category"] or "reference" in r["category"] or "metadata" in r["category"] or "Zotero" in r["candidate"]])
    write_csv(RUN / "02_表格输出" / "zotero_writeback_safe_plan.csv", [
        {"step": "scan_local_zotero_workspace", "action": "read files only", "approval_required": "no"},
        {"step": "detect_garbled_notes", "action": "write issue CSV and sidecar notes", "approval_required": "no"},
        {"step": "export_bibtex_ris_csv", "action": "write sidecar export files under workflow1 run package", "approval_required": "no"},
        {"step": "write_to_zotero_database", "action": "blocked until explicit user confirmation", "approval_required": "yes"},
        {"step": "install_zotero_mcp", "action": "approval queue", "approval_required": "yes"},
    ])
    write_csv(RUN / "02_表格输出" / "result_claim_guard_rules.csv", [
        {"rule": "claim_requires_evidence", "block_if_failed": "yes"},
        {"rule": "experimental_not_formal", "block_if_failed": "yes"},
        {"rule": "prototype_not_policy_recommendation", "block_if_failed": "yes"},
        {"rule": "synthetic_parameters_must_be_labeled", "block_if_failed": "yes"},
        {"rule": "unconverged_model_no_effective_strategy_claim", "block_if_failed": "yes"},
        {"rule": "unfair_baseline_no_superiority_claim", "block_if_failed": "yes"},
        {"rule": "literature_insufficient_no_mainstream_claim", "block_if_failed": "yes"},
        {"rule": "quality_gate_required_for_results", "block_if_failed": "yes"},
    ])
    write_csv(RUN / "02_表格输出" / "data_validation_rule_registry.csv", [
        {"rule": "lineage_required", "scope": "derived_data", "severity": "high"},
        {"rule": "row_column_key_summary_required", "scope": "every_output_table", "severity": "high"},
        {"rule": "chart_data_source_required", "scope": "figures", "severity": "high"},
        {"rule": "report_numbers_match_tables", "scope": "reports", "severity": "high"},
        {"rule": "repair_or_issue_log_required", "scope": "auto_repair", "severity": "medium"},
    ])
    write_csv(RUN / "02_表格输出" / "paper_section_quality_gates.csv", [
        {"gate": "top_journal_benchmark_read", "required": "yes"},
        {"gate": "section_outline", "required": "yes"},
        {"gate": "evidence_map", "required": "yes"},
        {"gate": "citation_table", "required": "yes"},
        {"gate": "citation_verification", "required": "yes"},
        {"gate": "result_claim_guard", "required": "yes"},
        {"gate": "reviewer2_audit", "required": "yes"},
        {"gate": "docx_export_or_fallback", "required": "yes"},
    ])
    write_csv(RUN / "02_表格输出" / "workflow_quality_improvement_backlog.csv", [
        {"id": "quality_gate_after_each_task", "status": "active", "priority": "high"},
        {"id": "citation_verification_api_stub", "status": "active", "priority": "high"},
        {"id": "zotero_mcp_review", "status": "approval_required", "priority": "medium"},
        {"id": "deepchecks_pandera_evidently_optional_integrations", "status": "approval_required", "priority": "medium"},
    ])


def build_reports() -> None:
    reports = {
        "quality_validation_skill_scout_report.md": "联网 scout 评估了 Codex skills、scientific skills、Curie、AutoResearch、ResearchClawBench、Deepchecks、Great Expectations、Pandera、Evidently、MLflow、DVC、Optuna、RefChecker、Zotero MCP、OpenAlex/CrossRef/Semantic Scholar。采用方式：只吸收本地 policy/skill/recipe/stub，不安装外部项目。",
        "top_journal_benchmark_system_report.md": "已建立 `references/top_journal_benchmark/` 长期机制。当前初始 registry 包含 DQN、模型验证、实验优化、自动科研、开放引用元数据等高质量文献；未全文读取者明确标记 metadata-only 或 abstract-only。",
        "result_claim_guard_upgrade_report.md": "已新增 result claim guard、evidence strength classifier、claim-to-evidence mapper。规则阻止 experimental 写成 formal、prototype 写成政策建议、未收敛模型写成有效策略、baseline 不公平时声称优越。",
        "model_comparison_protocol_upgrade_report.md": "已新增多模型公平比较协议。RL/DQN 必须比较 heuristic、Q-learning、random、historical、risk-ranking；监督学习、时间序列、因果推断分别有 baseline 和 robustness 要求。",
        "data_generation_validation_system_report.md": "已新增数据生成与派生数据核验 stub，要求 lineage、row/column/key 摘要、图表数据来源、报告数字一致性、repair/issue log。",
        "zotero_writeback_and_citation_verification_upgrade_report.md": "已建立安全 Zotero 方案：只扫描本地工作流目录、生成 sidecar notes 和导出表；不直接改 Zotero SQLite。引用核验优先 DOI、题名、作者、年份、期刊。",
        "paper_quality_workflow_upgrade_report.md": "已新增论文部分 orchestration stub：top journal benchmark、outline、evidence map、中文正文、DOCX/fallback、citation table、citation verification、claim guard、Reviewer 2 audit、revision checklist。",
        "workflow_self_improvement_quality_upgrade_report.md": "已强化任务结束后自我复盘：错误、图表、模型、文献、论断、外部工具、AGENTS、skill、recipe、project_memory、approval queue 均进入检查清单。",
        "research_quality_system_upgrade_report.md": "本轮建立科研质量总体系，覆盖数据、派生数据、模型、多模型比较、RL reward/convergence/constraint、图表表格、引用、论文和 Reviewer 2 风格自审。",
        "top_journal_benchmarking_upgrade_report.md": "顶级期刊对标机制已落地，并要求后续模型、图表、结果、论文段落生成前后均读取 benchmark registry。",
        "model_comparison_and_validation_upgrade_report.md": "多模型比较和模型验证机制已落地；formal 结果必须通过 baseline fairness、diagnostics、uncertainty 和 reproducibility gate。",
        "data_lineage_and_validation_upgrade_report.md": "数据 lineage 与核验机制已落地；每个任务包必须生成 data_lineage_manifest.csv 或说明不适用。",
        "paper_and_citation_quality_upgrade_report.md": "论文输出体系升级为 evidence-first；引用核验和 Zotero sidecar 写入计划已建立。",
        "workflow_memory_and_agent_optimization_report.md": "AGENTS、skills、recipes、model registry、workflow_improvement 和 project_state 已纳入质量门控升级计划。",
    }
    for fn, body in reports.items():
        write(RUN / "04_报告输出" / fn, f"# {fn.removesuffix('.md')}\n\n{body}\n\n## Sources\n\n- OpenAI skills catalog: https://github.com/openai/skills\n- Composio Codex skills: https://github.com/ComposioHQ/awesome-codex-skills\n- K-Dense Scientific Agent Skills: https://github.com/K-Dense-AI/scientific-agent-skills\n- Curie: https://github.com/Just-Curieous/Curie\n- Deepchecks: https://github.com/deepchecks/deepchecks\n- Pandera: https://pandera.readthedocs.io/\n- Great Expectations: https://docs.greatexpectations.io/\n- Evidently: https://github.com/evidentlyai/evidently\n- MLflow: https://mlflow.org/docs/latest/ml/tracking/\n- Zotero MCP example: https://github.com/swairshah/zotero-mcp-server\n")


def update_workflow_improvement() -> None:
    append(ROOT / "workflow_improvement" / "periodic_self_review_protocol.md", """## Research Quality Addendum (2026-04-26)

After every durable scientific task, run a quality self-review covering: new errors, repeated errors, chart/table QA, model comparison, baseline fairness, reward/convergence/constraint audit, literature gaps, citation failures, result overclaiming, external tools that may improve workflow1, AGENTS updates, new skills, recipes, project memory, and approval queue items.
""")
    append(ROOT / "workflow_improvement" / "upgrade_backlog.yaml", """
- id: research_quality_gate_after_each_task
  title: Run research quality gates and workflow improvement review after every durable scientific task.
  status: active
  priority: high
- id: optional_validation_tool_integrations
  title: Evaluate Deepchecks, Great Expectations, Pandera, Evidently, MLflow, DVC, Optuna, RefChecker, and Zotero MCP before any installation.
  status: approval_required
  priority: medium
""")
    append(ROOT / "workflow_improvement" / "external_plugin_approval_queue.yaml", """
- candidate: Deepchecks / Great Expectations / Pandera / Evidently
  reason: Optional validation dependencies may improve QA but require installation.
  approval_required_for: [install_dependencies, run_third_party_code]
  status: waiting_user_confirmation
- candidate: MLflow / DVC / Optuna
  reason: Experiment tracking and optimization tools may require dependency setup, services, or data remotes.
  approval_required_for: [install_dependencies, start_service, configure_remote]
  status: waiting_user_confirmation
- candidate: Zotero MCP / RefChecker with LLM provider
  reason: MCP/API/database/provider interactions are high risk.
  approval_required_for: [install_mcp, api_key, write_zotero_database, run_third_party_code]
  status: waiting_user_confirmation
""")
    append(ROOT / "workflow_improvement" / "source_watchlist.yaml", """
- name: Deepchecks
  url: https://github.com/deepchecks/deepchecks
  category: data_model_validation
- name: Great Expectations
  url: https://docs.greatexpectations.io/
  category: data_quality
- name: Pandera
  url: https://pandera.readthedocs.io/
  category: dataframe_validation
- name: Evidently
  url: https://github.com/evidentlyai/evidently
  category: drift_monitoring
- name: RefChecker
  url: https://github.com/markrussinovich/refchecker
  category: citation_verification
""")
    append(ROOT / "workflow_improvement" / "capability_taxonomy.yaml", """
research_quality:
  - data_generation_validation
  - derived_data_lineage
  - table_chart_qa
  - model_comparison
  - baseline_fairness
  - reward_convergence_constraint_audit
  - citation_verification
  - top_journal_benchmark
  - result_claim_guard
  - reviewer2_audit
  - reproducibility_audit
""")
    ledger = ROOT / "workflow_improvement" / "improvement_ledger.csv"
    if not ledger.exists():
        write(ledger, "timestamp,task,component,status,notes\n")
    append(ledger, f'{NOW},research_quality_system_upgrade,research_quality_and_quality_skills,completed,"Added quality policies, skills, stubs, benchmark registry, comparison protocols, and approval queue entries."')


def update_agents_and_state() -> None:
    agents_addendum = """## Research Quality Gate Policy

After every durable scientific task, Codex must run or plan research quality gates covering data generation and derived-data lineage, table/report consistency, chart QA, model validation, multi-model comparison, baseline fairness, reward/convergence/constraint audit, citation verification, top-journal benchmarking, result claim guard, Reviewer 2 style self-audit, reproducibility, and workflow self-improvement review.

## Top-Journal Benchmarking Policy

Before and after generating methods, model settings, figures, tables, result interpretation, or paper sections, Codex must consult `references/top_journal_benchmark/`. If a paper was not read in full, mark it as `metadata-only` or `abstract-only`; never pretend full-text support exists.

## Literature Coverage and Citation Verification Policy

Every paper section must include a citation evidence table. DOI, title, authors, year, journal/conference, and URL must be verified where possible. Citation failures cannot support formal claims.

## Data Generation and Lineage Validation Policy

Every derived output must record input sources, transformation intent, row count, column count, key fields, units, missingness/anomaly/duplicate checks, and repair or issue logs. Each task package should include `data_lineage_manifest.csv` when data outputs are generated.

## Model Comparison and Baseline Fairness Policy

Every model run must include at least one simple baseline. Advanced models must compare against an interpretable control. RL/DQN must compare heuristic, Q-learning, random, historical, and risk-ranking baselines when applicable. All models must use consistent splits, budgets, constraints, and metrics.

## Reward-Convergence-Constraint Audit Policy

RL/DQN outputs must audit reward scaling, convergence, constraint violations, budget/capacity/minimum coverage assumptions, and whether parameters were user-confirmed. Unconfirmed or unconverged results remain prototype/experimental only.

## Chart/Table QA and PNG Output Policy

Every chart must have a source data table, nonblank output check, readable axes/labels, Chinese font handling when needed, and PNG/SVG output status. Every table must be checked against report numbers.

## Paper Section Evidence and DOCX Export Policy

Paper section generation must follow: benchmark -> outline -> evidence map -> Chinese draft -> DOCX/fallback export -> citation table -> citation verification -> result claim guard -> Reviewer 2 audit -> revision checklist.

## Result Claim Guard Policy

Every result claim must map to data, model, figure/table, or literature evidence. Experimental must not become formal; prototype must not become policy recommendation; synthetic parameters must be labeled; unverified literature cannot imply mainstream consensus; only quality-gate-passing results can enter paper Results.

## Reviewer-2 Style Self-Audit Policy

Before a result, figure, table, or paper section is treated as reportable, Codex must produce a critical audit of likely reviewer objections, missing controls, overclaiming, weak citations, and reproducibility gaps.

## Workflow Self-Improvement After Every Task Policy

At the end of each scientific task, Codex must consider whether errors, repeated frictions, chart/model/literature/citation/claim gaps, or new external tools justify updating AGENTS, skills, recipes, model registry, project memory, or approval queue. Codex should proactively search for useful skills/tools, but must not install high-risk plugins, MCP servers, APIs, large dependencies, or write Zotero databases without user confirmation.
"""
    append(ROOT / "AGENTS.md", agents_addendum)
    long_memory = "后续所有科研任务都必须执行科研质量核验：数据生成与派生数据核验、多模型对比、baseline 公平性、reward/收敛/约束审计、图表和表格 QA、顶级期刊文献对标、引用核验、论文论断保护、Reviewer 2 风格自审。发现缺口时，Codex 应通过 workflow-self-improvement-scout 搜索并安全吸收相关 skill 或工具，高风险项进入 approval queue。"
    append(ROOT / "project_state" / "project_memory.md", f"## 2026-04-26 Research Quality Long-Term Memory\n\n{long_memory}")
    append(ROOT / "project_state" / "lessons_learned.md", "## 2026-04-26 Research Quality Lessons\n\n- 后续科研结果必须 evidence-first；所有模型、图表、表格、论文段落和引用都要通过对应质量门。\n- 多模型比较、baseline fairness、reward/convergence/constraint audit 是正式模型结果进入论文前的硬性条件。\n- 外部验证工具可作为方法来源，但安装、MCP、API、Zotero 数据库写入和大型依赖必须进入 approval queue。")
    write(ROOT / "project_state" / "current_focus.md", f"# Current Focus\n\n当前完成：科研级质量核验、顶级文献对标、多模型比较与 workflow1 自我强化体系建设。\n\n工作包：`{RUN.relative_to(ROOT)}`。\n\n边界：本轮未运行正式 DQN，未生成 formal 政策结论，未修改 `data/01_raw`。\n")
    write(ROOT / "project_state" / "next_step.md", "# Next Step\n\n下一步建议：用一句话触发“核验当前模型结果并与顶级期刊对标”，对最近 experimental DQN 输出执行完整质量 gate；若用户确认 formal DQN 参数，再另建 formal config 并重新训练。\n")
    append(ROOT / "project_state" / "changelog.md", f"## {NOW}\n\n- 新增 research_quality policy 总体系、20 个质量核验 skills、顶级期刊 benchmark registry、多模型比较协议、结果论断保护和论文质量输出 stub。\n- 更新 workflow_improvement、model_registry、AGENTS.md 和 project memory。\n")
    append(ROOT / "project_state" / "decision_log.md", f"## {NOW} Research Quality System Upgrade\n\nDecision: 将科研质量核验设为后续所有科研任务的默认硬闸门。\n\nRationale: 最近 DQN experimental run 已证明流程能跑通，但 formal 科研输出还需要多模型比较、baseline fairness、数据/图表/表格/引用核验和顶刊对标。\n\nImpact: 高风险外部工具进入 approval queue；低风险能力转化为本地 policy、skill、recipe、registry 和 stub。\n")
    write(ROOT / "project_state" / "conversation_handoff.md", f"# Conversation Handoff\n\n{NOW} 完成“科研质量核验、顶级文献对标、多模型比较与工作流强化”。\n\n主工作包：`{RUN.relative_to(ROOT)}`。\n\n关键升级：`research_quality/`、`references/top_journal_benchmark/`、`model_registry/*comparison_protocol.yaml`、`src/workflow1/quality/`、`src/workflow1/reporting/`、20 个质量 skills、AGENTS 研究质量政策、workflow_improvement 复盘机制。\n\n约束：未运行正式 DQN；未生成 formal 政策结论；未修改 `data/01_raw`。\n")
    append(ROOT / "project_state" / "run_protocol.md", "## Research Quality Protocol\n\n每次 durable 科研任务结束前必须执行科研质量核验与 workflow self-improvement review。dry-run 必须返回 matched intent、selected recipe、skills、required inputs、quality gates、expected outputs、stop conditions 和 approval-required items。")
    write(ROOT / "project_state" / "workflow_execution_state.yaml", f"""workflow_self_improvement:
  status: active
  latest_run_package: {RUN.relative_to(ROOT).as_posix()}
  approval_queue: workflow_improvement/external_plugin_approval_queue.yaml
  ledger: workflow_improvement/improvement_ledger.csv
research_quality_system:
  status: active
  latest_run_package: {RUN.relative_to(ROOT).as_posix()}
  policy_root: research_quality
  top_journal_benchmark_root: references/top_journal_benchmark
  result_claim_guard: src/workflow1/quality/result_claim_guard.py
  after_each_task_required: true
latest_dqn_auto_experimental_run:
  status: completed_not_formal
  formal_dqn_status: still_requires_user_confirmed_parameters
""")


def update_run_indexes() -> None:
    rel = RUN.relative_to(ROOT).as_posix()
    append(ROOT / "outputs" / "_index" / "run_index.md", f"## {RUN.name}\n- 路径：`{rel}`\n- 结论：已建立科研质量核验、顶级期刊对标、多模型比较、论文/citation 质量和 workflow self-improvement after-task 机制；dry-run 待执行。\n")
    manifest = ROOT / "outputs" / "_index" / "run_manifest.csv"
    if not manifest.exists():
        write(manifest, "任务包路径,任务名称,任务开始时间,任务类型,输入文件,主要输出,是否完成,是否有错误,是否影响后续 pipeline,README 路径\n")
    append(manifest, f"{rel},{RUN.name},20260426_1857,research_quality_system_upgrade,AGENTS.md; project_state; workflow_improvement; model_registry; skills,research_quality; top_journal_benchmark; quality skills; dry-run reports,True,False,True,{rel}/README.md")
    write(ROOT / "outputs" / "_index" / "latest_canonical_outputs.yaml", f"""latest_run_package: {rel}
research_quality_policy_root: research_quality
top_journal_benchmark_root: references/top_journal_benchmark
model_comparison_protocol: model_registry/model_comparison_protocol.yaml
result_claim_guard: src/workflow1/quality/result_claim_guard.py
paper_section_orchestrator: src/workflow1/reporting/paper_section_orchestrator.py
workflow_self_improvement_ledger: workflow_improvement/improvement_ledger.csv
latest_dqn_status: experimental_completed_not_formal
""")


def build_zotero_sidecars() -> None:
    sidecar = RUN / "09_论文输出" / "zotero_sidecar_notes"
    write(sidecar / "README.md", "# Zotero sidecar notes\n\n本目录用于保存待写入 Zotero 的无乱码中文笔记草稿。未直接修改 Zotero SQLite 数据库。\n")
    write(sidecar / "research_quality_note.md", "# 待写入 Zotero 笔记：科研质量核验体系\n\n本笔记总结 workflow1 后续论文写作必须执行 citation verification、evidence map、result claim guard、Reviewer 2 audit。\n")
    write(RUN / "09_论文输出" / "citation_export_stub.bib", "@misc{workflow1_quality_2026,\n  title={workflow1 Research Quality Gate System},\n  year={2026},\n  note={Local workflow sidecar; not written to Zotero database}\n}\n")
    write(RUN / "09_论文输出" / "citation_export_stub.ris", "TY  - GEN\nTI  - workflow1 Research Quality Gate System\nPY  - 2026\nER  - \n")


def snapshot_policy() -> None:
    text = (ROOT / "research_quality" / "research_quality_policy.yaml").read_text(encoding="utf-8")
    write(RUN / "06_配置参数" / "research_quality_policy_snapshot.yaml", text)


def write_manifest() -> None:
    records = []
    for p in sorted(RUN.rglob("*")):
        if p.is_file():
            records.append({"path": str(p.relative_to(RUN)), "type": p.suffix.lstrip(".") or "file", "description": "generated by research quality upgrade", "created_at": NOW, "sha256": sha256(p)})
    write_csv(RUN / "manifest.csv", records)


def main() -> None:
    build_research_quality()
    build_quality_modules()
    build_skills()
    build_benchmark_and_registries()
    build_tool_reports()
    build_reports()
    update_workflow_improvement()
    update_agents_and_state()
    update_run_indexes()
    build_zotero_sidecars()
    snapshot_policy()
    write_manifest()


if __name__ == "__main__":
    main()
