"""Minimal raw data validation runner."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any

import pandas as pd

from workflow1.pipelines.intake.runner import SUPPORTED_RAW_EXTENSIONS
from workflow1.pipelines.runner import PipelineResult
from workflow1.utils.io import ensure_directory


DATE_NAME_HINTS = ("date", "time", "year", "month", "day", "日期", "时间", "年份", "年度", "月份")


@dataclass(frozen=True)
class ColumnValidation:
    """Validation summary for one column."""

    dataset_name: str
    file_path: str
    file_type: str
    sheet_name: str
    column_name: str
    row_count: int
    missing_count: int
    missing_rate: float
    unique_count: int
    is_empty_column: bool
    is_unnamed_column: bool
    is_unique_key_candidate: bool
    is_date_name_candidate: bool
    mixed_type_count: int
    low_cardinality_values: str = ""


@dataclass(frozen=True)
class TableValidation:
    """Validation summary for one table."""

    dataset_name: str
    file_path: str
    file_type: str
    sheet_name: str
    row_count: int
    column_count: int
    duplicate_row_count: int
    columns: tuple[ColumnValidation, ...] = field(default_factory=tuple)


def run(raw_dir: str | Path = "data/01_raw", reports_dir: str | Path = "reports") -> PipelineResult:
    """Run lightweight validation checks and write reports."""

    raw_path = Path(raw_dir)
    reports_path = Path(reports_dir)
    tables_path = ensure_directory(reports_path / "tables")
    ensure_directory(reports_path)

    raw_files = _list_raw_files(raw_path)
    if not raw_files:
        return PipelineResult(
            name="validation",
            status="no_raw_data",
            details={
                "message": f"No supported raw files found in {raw_path}. Add .csv or .xlsx files before validation.",
                "raw_dir": str(raw_path),
                "supported_extensions": sorted(SUPPORTED_RAW_EXTENSIONS),
            },
        )

    validations: list[TableValidation] = []
    warnings: list[str] = []
    for file_path in raw_files:
        try:
            validations.extend(_validate_file(file_path))
        except Exception as exc:  # pragma: no cover - defensive boundary for user files.
            warnings.append(f"{file_path}: {exc}")

    if not validations:
        return PipelineResult(
            name="validation",
            status="error",
            details={"message": "Raw files were found, but validation summaries could not be created.", "warnings": warnings},
        )

    dataset_name = _dataset_name(raw_files)
    markdown_path = reports_path / f"validation_report_{dataset_name}.md"
    csv_path = tables_path / f"validation_summary_{dataset_name}.csv"
    _write_validation_markdown(markdown_path, validations, warnings)
    _write_validation_csv(csv_path, validations)

    return PipelineResult(
        name="validation",
        status="ok",
        details={
            "dataset_name": dataset_name,
            "files": len(raw_files),
            "tables": len(validations),
            "outputs": [str(markdown_path), str(csv_path)],
            "warnings": warnings,
        },
    )


def _list_raw_files(raw_path: Path) -> list[Path]:
    if not raw_path.exists():
        return []
    return sorted(
        path
        for path in raw_path.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_RAW_EXTENSIONS and not path.name.startswith("~$")
    )


def _validate_file(file_path: Path) -> list[TableValidation]:
    suffix = file_path.suffix.lower()
    if suffix == ".xlsx":
        workbook = pd.ExcelFile(file_path)
        return [_validate_frame(pd.read_excel(workbook, sheet_name=sheet), file_path, "xlsx", sheet) for sheet in workbook.sheet_names]
    if suffix == ".csv":
        return [_validate_frame(_read_csv(file_path), file_path, "csv", "")]
    return []


def _read_csv(file_path: Path) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
    if last_error:
        raise last_error
    return pd.read_csv(file_path)


def _validate_frame(df: pd.DataFrame, file_path: Path, file_type: str, sheet_name: str) -> TableValidation:
    row_count = int(len(df))
    duplicate_row_count = int(df.duplicated().sum()) if row_count else 0
    columns = tuple(_validate_column(df, column, file_path, file_type, sheet_name) for column in df.columns)
    return TableValidation(
        dataset_name=file_path.stem,
        file_path=str(file_path),
        file_type=file_type,
        sheet_name=sheet_name,
        row_count=row_count,
        column_count=int(len(df.columns)),
        duplicate_row_count=duplicate_row_count,
        columns=columns,
    )


def _validate_column(
    df: pd.DataFrame,
    column: Any,
    file_path: Path,
    file_type: str,
    sheet_name: str,
) -> ColumnValidation:
    series = df[column]
    row_count = int(len(series))
    missing_count = int(series.isna().sum())
    non_missing = series.dropna()
    unique_count = int(non_missing.nunique(dropna=True))
    mixed_type_count = _mixed_type_count(non_missing)
    low_cardinality_values = _low_cardinality_values(non_missing, row_count)
    column_name = str(column)
    return ColumnValidation(
        dataset_name=file_path.stem,
        file_path=str(file_path),
        file_type=file_type,
        sheet_name=sheet_name,
        column_name=column_name,
        row_count=row_count,
        missing_count=missing_count,
        missing_rate=(missing_count / row_count) if row_count else 0.0,
        unique_count=unique_count,
        is_empty_column=missing_count == row_count,
        is_unnamed_column=column_name.startswith("Unnamed") or column_name.strip() == "",
        is_unique_key_candidate=row_count > 0 and missing_count == 0 and unique_count == row_count,
        is_date_name_candidate=_is_date_name_candidate(column_name),
        mixed_type_count=mixed_type_count,
        low_cardinality_values=low_cardinality_values,
    )


def _mixed_type_count(series: pd.Series) -> int:
    if series.empty:
        return 0
    type_names = {type(value).__name__ for value in series.head(1000)}
    return len(type_names)


def _low_cardinality_values(series: pd.Series, row_count: int) -> str:
    if series.empty or row_count == 0:
        return ""
    unique_count = int(series.nunique(dropna=True))
    if unique_count <= 20 or unique_count / max(row_count, 1) <= 0.05:
        counts = series.astype(str).value_counts(dropna=True).head(10)
        return " | ".join(f"{idx}:{count}" for idx, count in counts.items())
    return ""


def _is_date_name_candidate(column_name: str) -> bool:
    lowered = column_name.lower()
    return any(hint in lowered for hint in DATE_NAME_HINTS)


def _dataset_name(raw_files: list[Path]) -> str:
    if len(raw_files) == 1:
        return _safe_name(raw_files[0].stem)
    return "raw_validation"


def _safe_name(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", value).strip("_") or "dataset"


def _write_validation_csv(path: Path, validations: list[TableValidation]) -> None:
    rows = []
    for table in validations:
        for column in table.columns:
            rows.append(column.__dict__ | {"duplicate_row_count": table.duplicate_row_count})
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")


def _write_validation_markdown(path: Path, validations: list[TableValidation], warnings: list[str]) -> None:
    lines = [
        "# 原始数据 Validation Report",
        "",
        "本报告由最小 validation runner 生成，仅做缺失值、重复行、候选键、空列、Unnamed 列、日期名称候选、混合类型和低基数字段检查；未执行清洗、建模或可视化。",
        "",
        "| dataset_name | file_type | sheet_name | rows | columns | duplicate_rows |",
        "|---|---|---|---:|---:|---:|",
    ]
    for table in validations:
        lines.append(
            f"| `{table.dataset_name}` | `{table.file_type}` | `{table.sheet_name}` | {table.row_count} | {table.column_count} | {table.duplicate_row_count} |"
        )
    for table in validations:
        title = table.dataset_name if not table.sheet_name else f"{table.dataset_name} / {table.sheet_name}"
        lines.extend(["", f"## {title}", ""])
        key_candidates = [column.column_name for column in table.columns if column.is_unique_key_candidate]
        empty_columns = [column.column_name for column in table.columns if column.is_empty_column]
        unnamed_columns = [column.column_name for column in table.columns if column.is_unnamed_column]
        date_candidates = [column.column_name for column in table.columns if column.is_date_name_candidate]
        mixed_columns = [column.column_name for column in table.columns if column.mixed_type_count > 1]
        low_cardinality = [column for column in table.columns if column.low_cardinality_values]
        lines.extend(
            [
                f"- 重复行数：{table.duplicate_row_count}",
                f"- 唯一键候选：{', '.join(f'`{name}`' for name in key_candidates) if key_candidates else '无'}",
                f"- 空列：{', '.join(f'`{name}`' for name in empty_columns) if empty_columns else '无'}",
                f"- Unnamed 列：{', '.join(f'`{name}`' for name in unnamed_columns) if unnamed_columns else '无'}",
                f"- 日期名称候选字段：{', '.join(f'`{name}`' for name in date_candidates) if date_candidates else '无'}",
                f"- 混合类型候选字段：{', '.join(f'`{name}`' for name in mixed_columns) if mixed_columns else '无'}",
                "",
                "### 字段缺失概览",
                "",
                "| column | missing | missing_rate | unique | low_cardinality_values |",
                "|---|---:|---:|---:|---|",
            ]
        )
        for column in table.columns:
            lines.append(
                f"| `{column.column_name}` | {column.missing_count} | {column.missing_rate:.2%} | {column.unique_count} | `{column.low_cardinality_values}` |"
            )
    if warnings:
        lines.extend(["", "## 读取警告", ""])
        lines.extend(f"- {warning}" for warning in warnings)
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

