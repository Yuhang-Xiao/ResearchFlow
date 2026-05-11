"""Infer research task type from a data file, target column, and goal text."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re
from typing import Any

import pandas as pd


TARGET_PATTERNS = [
    r"target\s*(?:is|=|:)\s*([\w\-\u4e00-\u9fff]+)",
    r"目标变量(?:是|为|=|:)\s*([\w\-\u4e00-\u9fff]+)",
    r"预测(?:字段|变量|目标)?(?:是|为|=|:)?\s*([\w\-\u4e00-\u9fff]+)",
]


@dataclass
class ColumnProfile:
    name: str
    dtype: str
    missing_rate: float
    unique_count: int
    numeric: bool
    datetime_like: bool


@dataclass
class TaskInference:
    task_type: str
    target_column: str | None
    confidence: float
    reasons: list[str]
    profile: dict[str, Any]
    auxiliary_tasks: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_table(data_file: str | Path) -> pd.DataFrame:
    path = Path(data_file)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def profile_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    columns: list[ColumnProfile] = []
    for col in df.columns:
        series = df[col]
        numeric = pd.api.types.is_numeric_dtype(series)
        col_lower = str(col).lower()
        date_name_hint = (
            col_lower in {"date", "time", "timestamp", "year", "month"}
            or col_lower.endswith(("_date", "_time", "_timestamp", "_year", "_month"))
            or any(k in col_lower for k in ["日期", "时间", "年份", "月份"])
        )
        if not date_name_hint:
            datetime_like = False
        elif numeric and any(k in col_lower for k in ["year", "年份"]):
            datetime_like = bool(series.dropna().between(1900, 2100).mean() >= 0.8)
        else:
            parsed = pd.to_datetime(series.dropna().head(50), errors="coerce")
            datetime_like = bool(len(parsed) and parsed.notna().mean() >= 0.8 and date_name_hint)
        columns.append(
            ColumnProfile(
                name=str(col),
                dtype=str(series.dtype),
                missing_rate=float(series.isna().mean()),
                unique_count=int(series.nunique(dropna=True)),
                numeric=bool(numeric),
                datetime_like=datetime_like,
            )
        )
    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": [asdict(c) for c in columns],
        "datetime_columns": [c.name for c in columns if c.datetime_like],
        "numeric_columns": [c.name for c in columns if c.numeric],
    }


def infer_target_column(df: pd.DataFrame, goal: str, explicit_target: str | None = None) -> str | None:
    if explicit_target and explicit_target in df.columns:
        return explicit_target
    for pattern in TARGET_PATTERNS:
        match = re.search(pattern, goal, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip(" ，。,.;；")
            if candidate in df.columns:
                return candidate
    lowered_goal = goal.lower()
    scored: list[tuple[int, str]] = []
    keywords = ["target", "label", "class", "risk", "value", "count", "rate", "score", "目标", "标签", "风险", "数值", "计数", "发病"]
    for col in df.columns:
        col_text = str(col).lower()
        score = sum(2 for k in keywords if k in col_text) + sum(1 for k in keywords if k in lowered_goal and k in col_text)
        if score:
            scored.append((score, str(col)))
    if scored:
        return sorted(scored, reverse=True)[0][1]
    non_id = [c for c in df.columns if str(c).lower() not in {"id", "index", "编号", "序号"}]
    return str(non_id[-1]) if non_id else None


def infer_task_from_dataframe(
    df: pd.DataFrame,
    goal: str,
    target_column: str | None = None,
) -> TaskInference:
    profile = profile_dataframe(df)
    target = infer_target_column(df, goal, target_column)
    reasons: list[str] = []
    auxiliary: list[str] = []
    text = goal.lower()
    if target is None or target not in df.columns:
        task_type = "clustering" if any(k in text for k in ["cluster", "聚类", "分群"]) else "anomaly_detection"
        return TaskInference(task_type, None, 0.45, ["未识别明确目标变量，转入无监督/异常检测规划"], profile, auxiliary)

    y = df[target].dropna()
    nunique = int(y.nunique())
    numeric = pd.api.types.is_numeric_dtype(y)
    date_present = bool(profile["datetime_columns"])
    group_present = any(str(c).lower() in {"group", "region", "site", "location", "地区", "地点", "分组"} for c in df.columns)
    zero_rate = float((y == 0).mean()) if numeric and len(y) else 0.0

    if date_present and any(k in text for k in ["forecast", "time series", "时间序列", "预测未来", "趋势"]):
        task_type = "time_series_forecasting"
        reasons.append("目标包含时间序列/预测未来语义且数据存在时间字段")
    elif nunique == 2:
        task_type = "binary_classification"
        reasons.append("目标变量只有两个类别，优先按二分类处理")
    elif numeric and y.ge(0).all() and ((y % 1 == 0).all()) and ("count" in text or "计数" in text or zero_rate >= 0.3):
        task_type = "zero_inflated_count" if zero_rate >= 0.3 else "count_regression"
        reasons.append(f"目标为非负整数，zero_rate={zero_rate:.2f}")
    elif not numeric and 2 < nunique <= min(30, max(3, len(y) // 3)):
        task_type = "multiclass_classification"
        reasons.append("目标变量为有限多类别")
    elif numeric and any(k in text for k in ["extreme", "tail", "极端", "长尾", "稀有"]):
        task_type = "extreme_event_prediction"
        auxiliary.append("binary_classification")
        reasons.append("目标为连续值且研究目标强调极端/长尾")
    elif numeric:
        task_type = "regression"
        reasons.append("目标变量为连续数值")
    else:
        task_type = "multiclass_classification"
        reasons.append("目标变量非数值且多类别")

    if group_present:
        auxiliary.append("panel_or_grouped_prediction")
    if date_present and task_type != "time_series_forecasting":
        auxiliary.append("time_aware_validation")
    if numeric and zero_rate >= 0.2 and task_type not in {"zero_inflated_count", "count_regression"}:
        auxiliary.append("extreme_event_prediction")
    return TaskInference(task_type, target, 0.78, reasons, profile, list(dict.fromkeys(auxiliary)))


def infer_task_from_file(data_file: str | Path, goal: str, target_column: str | None = None) -> TaskInference:
    return infer_task_from_dataframe(load_table(data_file), goal, target_column)
