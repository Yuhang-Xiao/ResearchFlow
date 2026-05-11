"""Generate a minimal cleaning plan without modifying raw data."""

from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

from workflow1.pipelines.runner import PipelineResult
from workflow1.pipelines.validation.runner import run as run_validation
from workflow1.utils.io import ensure_directory


def run(raw_dir: str | Path = "data/01_raw", reports_dir: str | Path = "reports") -> PipelineResult:
    """Create a Chinese cleaning plan from validation summaries only."""

    validation_result = run_validation(raw_dir=raw_dir, reports_dir=reports_dir)
    if validation_result.status != "ok":
        return PipelineResult(
            name="cleaning-plan",
            status=validation_result.status,
            details={
                "message": "Cleaning plan was not generated because validation did not produce usable summaries.",
                "validation_status": validation_result.status,
                "validation_details": validation_result.details,
            },
        )

    dataset_name = str(validation_result.details["dataset_name"])
    reports_path = ensure_directory(reports_dir)
    summary_path = Path(reports_dir) / "tables" / f"validation_summary_{dataset_name}.csv"
    output_path = reports_path / f"cleaning_plan_{dataset_name}.md"
    summary = pd.read_csv(summary_path)
    output_path.write_text(_build_plan(dataset_name, summary), encoding="utf-8")

    return PipelineResult(
        name="cleaning-plan",
        status="ok",
        details={
            "dataset_name": dataset_name,
            "outputs": [str(output_path)],
            "message": "Cleaning plan generated. No raw data was modified.",
        },
    )


def _build_plan(dataset_name: str, summary: pd.DataFrame) -> str:
    lines = [
        f"# Cleaning Plan: {dataset_name}",
        "",
        "本计划由最小 cleaning-plan runner 根据 validation summary 自动生成，只提出清洗建议，不修改 `data/01_raw`，不生成清洗后数据集，也不执行建模或可视化。",
        "",
        "## 总体原则",
        "",
        "- 保留原始字段名，尤其是中文字段名；不要为了美化而盲目翻译字段。",
        "- 所有派生数据应写入 `data/02_intermediate` 或更高层级，不能覆盖 `data/01_raw`。",
        "- 日期字段、唯一键、分类映射和重复值处理在执行前应记录规则和假设。",
        "- 本计划中的“可自动执行”仅表示低风险候选动作；真正执行清洗仍应由后续 cleaning runner 或明确任务触发。",
        "",
        "## 自动可执行候选项",
        "",
    ]
    automatic = _automatic_items(summary)
    lines.extend(f"- {item}" for item in automatic)
    if not automatic:
        lines.append("- 暂无明确低风险自动清洗候选项。")

    lines.extend(["", "## 需要用户确认或任务目标约束的项目", ""])
    confirm = _confirmation_items(summary)
    lines.extend(f"- {item}" for item in confirm)
    if not confirm:
        lines.append("- 暂无明显需要用户确认的清洗风险项。")

    lines.extend(["", "## 字段级建议", ""])
    for _, row in summary.iterrows():
        suggestions = _column_suggestions(row)
        if not suggestions:
            continue
        table_label = row.get("sheet_name", "")
        prefix = f"`{row['column_name']}`"
        if isinstance(table_label, str) and table_label:
            prefix += f"（sheet: `{table_label}`）"
        lines.append(f"### {prefix}")
        lines.extend(f"- {suggestion}" for suggestion in suggestions)
        lines.append("")

    lines.extend(
        [
            "## 后续执行前检查清单",
            "",
            "- 明确研究目标、分析单位、目标变量或主要结局。",
            "- 确认是否存在相关 `references/` 文档，并提取会影响清洗或标签构造的要求。",
            "- 确认唯一键、日期字段和重复值处理规则。",
            "- 确认缺失值处理是否会影响目标变量、关键暴露变量或分组变量。",
            "- 执行清洗后生成 cleaning log，并把输出写入适当的数据层。",
            "",
        ]
    )
    return "\n".join(lines)


def _automatic_items(summary: pd.DataFrame) -> list[str]:
    items: list[str] = []
    if _any_true(summary, "is_unnamed_column"):
        items.append("可将完全由导入产生的 `Unnamed` 列列入删除候选，但删除前需确认不是有效源字段。")
    if _any_true(summary, "is_empty_column"):
        items.append("可将全空列列入删除候选，并在 cleaning log 中记录字段名。")
    if "is_date_name_candidate" in summary and summary["is_date_name_candidate"].fillna(False).any():
        items.append("可将日期名称候选字段列入后续日期解析候选清单；本阶段不解析日期。")
    if "low_cardinality_values" in summary and summary["low_cardinality_values"].fillna("").astype(str).str.len().gt(0).any():
        items.append("可为低基数字段生成类别值清单，供后续标准化、合并或映射使用。")
    return items


def _confirmation_items(summary: pd.DataFrame) -> list[str]:
    items: list[str] = []
    duplicate_rows = int(summary.get("duplicate_row_count", pd.Series([0])).fillna(0).max())
    if duplicate_rows > 0:
        items.append(f"检测到重复行候选（最大重复行数 {duplicate_rows}）；是否删除或合并必须结合业务含义确认。")
    if _any_true(summary, "is_unique_key_candidate"):
        items.append("存在唯一键候选字段；是否作为主键需结合数据来源和研究单位确认。")
    if "missing_rate" in summary and summary["missing_rate"].fillna(0).gt(0.2).any():
        items.append("存在缺失率超过 20% 的字段；删除、填补或保留需结合研究目标确认。")
    if "mixed_type_count" in summary and summary["mixed_type_count"].fillna(0).gt(1).any():
        items.append("存在混合类型候选字段；需确认应转为 numeric、category、date 还是保留 text。")
    return items


def _column_suggestions(row: pd.Series) -> list[str]:
    suggestions: list[str] = []
    if bool(row.get("is_empty_column", False)):
        suggestions.append("全空列：建议列入删除候选，执行前记录字段名和来源。")
    if bool(row.get("is_unnamed_column", False)):
        suggestions.append("Unnamed 列：可能是索引残留或空表头，建议核对源文件。")
    if bool(row.get("is_unique_key_candidate", False)):
        suggestions.append("唯一键候选：可作为主键候选，但需确认是否符合分析单位。")
    if bool(row.get("is_date_name_candidate", False)):
        suggestions.append("日期名称候选：后续可尝试日期解析，但本计划阶段不解析。")
    if int(row.get("mixed_type_count", 0) or 0) > 1:
        suggestions.append("混合类型候选：建议在清洗阶段统一类型，并保留无法转换的原始值。")
    missing_rate = float(row.get("missing_rate", 0) or 0)
    if missing_rate > 0:
        suggestions.append(f"存在缺失值：缺失率约 {missing_rate:.2%}，需根据字段角色决定填补、保留或排除。")
    low_values = str(row.get("low_cardinality_values", "") or "")
    if low_values and low_values.lower() != "nan":
        suggestions.append("低基数字段：建议检查类别拼写、同义值、异常类别和是否需要映射。")
    return suggestions


def _any_true(frame: pd.DataFrame, column: str) -> bool:
    return column in frame and frame[column].fillna(False).astype(bool).any()


def safe_dataset_name(value: str) -> str:
    """Return a filesystem-safe dataset name."""

    return re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", value).strip("_") or "dataset"

