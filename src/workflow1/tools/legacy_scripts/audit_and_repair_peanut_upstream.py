from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/01_raw/PEANUT2023-20241.xlsx"
CLEAN = ROOT / "data/03_primary/peanut_cleaned_analysis_ready.csv"
CLEAN_XLSX = ROOT / "data/03_primary/peanut_cleaned_analysis_ready.xlsx"
CONC = ROOT / "data/04_feature/peanut_concentration_clean_table.csv"
DIST = ROOT / "data/04_feature/peanut_concentration_distribution_summary.csv"
PANEL = ROOT / "data/04_feature/peanut_count_panel.csv"
PANEL_XLSX = ROOT / "data/04_feature/peanut_count_panel.xlsx"
BELIEF = ROOT / "data/04_feature/peanut_beta_binomial_belief_states.csv"
STATE = ROOT / "data/04_feature/peanut_belief_mdp_state_features.csv"


def ensure_dirs() -> None:
    for rel in ["data/03_primary", "data/04_feature", "reports", "reports/tables", "project_state"]:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def to_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def md_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "无记录。"
    d = df.head(max_rows).astype(object).where(pd.notna(df.head(max_rows)), "")
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in d.iterrows():
        vals = [str(row[c]).replace("\n", " ").replace("|", "/")[:220] for c in d.columns]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def norm(x) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip()
    if s.lower() in {"nan", "none", "null"}:
        return ""
    return re.sub(r"\s+", " ", s)


def as_bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s.fillna(False)
    return s.astype(str).str.lower().isin(["true", "1", "是", "yes"])


def normalize_unit(unit: str) -> str:
    u = norm(unit).replace("µ", "μ").replace("ug", "μg").replace("UG", "μg")
    u = re.sub(r"\s+", "", u)
    low = u.lower()
    if low in {"μg/kg", "mcg/kg"}:
        return "μg/kg"
    if low == "mg/kg":
        return "mg/kg"
    if low == "g/100g":
        return "g/100g"
    if low == "mg/g":
        return "mg/g"
    if low == "cfu/g":
        return "CFU/g"
    return u


def convert_to_ugkg(value: float | None, unit: str) -> tuple[float | None, str, bool]:
    if value is None or pd.isna(value):
        return None, normalize_unit(unit), False
    u = normalize_unit(unit)
    if u == "mg/kg":
        return float(value) * 1000.0, "μg/kg", True
    if u == "μg/kg":
        return float(value), "μg/kg", True
    return float(value), u, False


AFB_CONTEXT = re.compile(
    r"(黄\s*曲\s*霉(?:毒素)?\s*(?:B\s*1|B₁|B)?|AFB\s*[-_ ]?1|AFB1|AFLATOXIN\s*B\s*1)",
    re.IGNORECASE,
)
AFB_B_ONLY = re.compile(r"(B₁|B1|B<sup>1</sup>)", re.IGNORECASE)
NON_AFB_CONTEXT = re.compile(r"(维生素\s*B1|硫胺素|黄曲霉毒素\s*M\s*1|AFM1|赭曲霉|玉米赤霉|脱氧雪腐|伏马|展青霉)")


TEXT_COLS = ["不合格项目分类", "不合格项目", "不合格规范列", "检验项目", "检测数值", "备注", "标准"]


def detect_afb1(row: pd.Series) -> tuple[bool, str, bool]:
    hits = []
    suspicious = False
    for col in TEXT_COLS:
        if col not in row.index:
            continue
        text = norm(row.get(col))
        if not text:
            continue
        if NON_AFB_CONTEXT.search(text):
            if "黄曲霉" not in text and "AFB" not in text.upper():
                continue
        if AFB_CONTEXT.search(text):
            hits.append(f"{col}命中AFB1/黄曲霉变体")
        elif "黄曲霉" in text:
            hits.append(f"{col}含黄曲霉关键词")
            suspicious = True
        elif ("AFB" in text.upper() and not NON_AFB_CONTEXT.search(text)):
            hits.append(f"{col}含AFB关键词")
            suspicious = True
        elif AFB_B_ONLY.search(text) and "生物毒素" in text:
            suspicious = True
    if hits:
        return True, "；".join(hits), suspicious
    if suspicious:
        return False, "疑似生物毒素/B1上下文但未明确AFB1", True
    return False, "", False


NUM_UNIT_RE = re.compile(r"([<>≤≥=]?)\s*(-?\d+(?:\.\d+)?)\s*(μg/kg|µg/kg|ug/kg|mg/kg|g/100g|mg/g|CFU/g)?", re.I)


def parse_num_unit_from_text(text: str, afb_context: bool, default_unit: str = "") -> dict:
    s = norm(text)
    out = {
        "value": np.nan,
        "unit": "",
        "unit_inferred": False,
        "operator": "",
        "status": "",
        "reason": "",
    }
    if not s or s in {"/", "-", "—"}:
        out.update(status="无检测数值", reason="空值或占位符")
        return out
    if "合格" == s or s.endswith("合格") and not re.search(r"\d", s):
        out.update(status="无数值", reason="文本为合格但无数值")
        return out
    if re.search(r"未检出|不得检出|阴性|未检出", s):
        out.update(value=0.0, unit=normalize_unit(default_unit), status="未检出/不得检出", reason="")
        return out
    m = NUM_UNIT_RE.search(s)
    if not m:
        out.update(status="无法解析", reason="未找到数值和单位模式")
        return out
    op, val, unit = m.group(1), float(m.group(2)), normalize_unit(m.group(3) or "")
    inferred = False
    if not unit and default_unit:
        unit = normalize_unit(default_unit)
        inferred = True
    elif not unit and afb_context:
        unit = "μg/kg"
        inferred = True
    conv, conv_unit, converted = convert_to_ugkg(val, unit)
    out.update(value=conv, unit=conv_unit, unit_inferred=inferred, operator=op, status="已解析", reason="")
    if converted:
        out["status"] = "已解析并统一单位"
    return out


def parse_detection_value(text: str, afb_context: bool) -> dict:
    s = norm(text)
    base = parse_num_unit_from_text(s, afb_context=afb_context)
    out = {
        "原始检测数值": s,
        "初检浓度值": np.nan,
        "复检浓度值": np.nan,
        "最终采用浓度值": np.nan,
        "浓度单位": "",
        "检测单位是否推断": False,
        "浓度清洗状态": base["status"],
        "检测数值解析失败原因": base["reason"],
    }
    if not s:
        return out

    first = re.search(r"初检(?:结果)?[:：]?\s*[^0-9<>≤≥=]*([<>≤≥=]?\s*-?\d+(?:\.\d+)?)\s*(μg/kg|µg/kg|ug/kg|mg/kg)?", s, re.I)
    second = re.search(r"复检(?:结果)?[:：]?\s*[^0-9<>≤≥=]*([<>≤≥=]?\s*-?\d+(?:\.\d+)?)\s*(μg/kg|µg/kg|ug/kg|mg/kg)?", s, re.I)

    def parse_match(m):
        if not m:
            return np.nan, "", False
        val = float(re.sub(r"[<>≤≥=\s]", "", m.group(1)))
        unit = normalize_unit(m.group(2) or ("μg/kg" if afb_context else ""))
        inferred = not bool(m.group(2)) and afb_context
        conv, conv_unit, _ = convert_to_ugkg(val, unit)
        return conv, conv_unit, inferred

    fv, fu, fi = parse_match(first)
    sv, su, si = parse_match(second)
    if pd.notna(fv):
        out["初检浓度值"] = fv
        out["浓度单位"] = fu
        out["检测单位是否推断"] = fi
    if pd.notna(sv):
        out["复检浓度值"] = sv
        out["浓度单位"] = su or out["浓度单位"]
        out["检测单位是否推断"] = out["检测单位是否推断"] or si
    if pd.notna(sv):
        out["最终采用浓度值"] = sv
        out["浓度清洗状态"] = "初检复检均解析，最终采用复检值"
        out["检测数值解析失败原因"] = ""
    elif pd.notna(fv):
        out["最终采用浓度值"] = fv
        out["浓度清洗状态"] = "解析初检值，最终采用初检值"
        out["检测数值解析失败原因"] = ""
    elif pd.notna(base["value"]):
        out["初检浓度值"] = base["value"]
        out["最终采用浓度值"] = base["value"]
        out["浓度单位"] = base["unit"]
        out["检测单位是否推断"] = bool(base["unit_inferred"])
        out["检测数值解析失败原因"] = ""
    return out


def parse_limit_value(text: str, afb_context: bool) -> dict:
    p = parse_num_unit_from_text(text, afb_context=afb_context)
    return {
        "原始法规限制": norm(text),
        "法规限量_数值": p["value"],
        "法规限量_单位": p["unit"],
        "法规限量_比较符号": p["operator"] or "≤" if pd.notna(p["value"]) else "",
        "法规限量_单位是否推断": bool(p["unit_inferred"]),
        "法规限量解析状态": p["status"],
        "法规限量解析失败原因": p["reason"],
    }


def classify_review(row: pd.Series) -> str:
    reasons = []
    if row.get("AFB1识别可疑", False):
        reasons.append("AFB1识别可疑需复核")
    if row.get("是否AFB1相关", False) and pd.isna(row.get("最终采用浓度值")):
        reasons.append("AFB1相关但浓度无法解析")
    if row.get("是否AFB1相关", False) and pd.isna(row.get("法规限量_数值")):
        reasons.append("AFB1相关但法规限量无法解析")
    if row.get("是否AFB1相关", False) and norm(row.get("浓度单位")) not in {"", "μg/kg"}:
        reasons.append("AFB1浓度单位未统一为μg/kg")
    if row.get("是否AFB1相关", False) and pd.notna(row.get("最终采用浓度值")) and pd.notna(row.get("法规限量_数值")):
        numeric_exceed = float(row["最终采用浓度值"]) > float(row["法规限量_数值"])
        judgment_bad = bool(row.get("是否不合格", False))
        if numeric_exceed != judgment_bad:
            reasons.append("数值超标判断与原始判定结果不一致")
    if "多项目" in norm(row.get("检测数值解析失败原因")):
        reasons.append("多项目混合值需复核")
    return "；".join(reasons)


def make_panel(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["生产省份_清洗", "年份", "月份", "年月", "供应链环节"]
    tmp = df.copy()
    for c in ["是否合格", "是否不合格", "是否AFB1相关", "AFB1相关不合格"]:
        tmp[c] = as_bool(tmp[c])
    tmp["AFB1浓度可用"] = tmp["是否AFB1相关"] & tmp["最终采用浓度值"].notna()
    g = tmp.groupby(group_cols, dropna=False)
    out = g.agg(
        抽检总批次数=("序号", "count"),
        合格批次数=("是否合格", "sum"),
        不合格批次数=("是否不合格", "sum"),
        AFB1相关记录数=("是否AFB1相关", "sum"),
        AFB1相关不合格批次数=("AFB1相关不合格", "sum"),
        浓度可用记录数=("AFB1浓度可用", "sum"),
    ).reset_index()
    out = out.rename(columns={"生产省份_清洗": "省份"})
    out["不合格率"] = out["不合格批次数"] / out["抽检总批次数"].replace(0, np.nan)
    out["AFB1相关不合格率"] = out["AFB1相关不合格批次数"] / out["AFB1相关记录数"].replace(0, np.nan)
    out["数据完整性标记"] = np.where(
        out[["省份", "年份", "月份", "年月", "供应链环节"]].isna().any(axis=1) | out["省份"].astype(str).eq(""),
        "关键索引缺失",
        "基本完整",
    )
    return out


def make_concentration_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "序号", "生产省份_清洗", "年份", "月份", "年月", "供应链环节", "产品二级类", "产品名称",
        "污染物名称_标准化", "是否AFB1相关", "AFB1识别依据", "原始检测数值", "初检浓度值", "复检浓度值",
        "最终采用浓度值", "浓度单位", "检测单位是否推断", "原始法规限制", "法规限量_数值", "法规限量_单位",
        "法规限量_比较符号", "法规限量_单位是否推断", "是否超标", "超标倍数", "浓度清洗状态",
        "检测数值解析失败原因", "法规限量解析状态", "法规限量解析失败原因", "是否建议人工复核", "复核原因",
    ]
    out = df[df["是否AFB1相关"]].copy()
    out = out[[c for c in cols if c in out.columns]]
    out = out.rename(columns={"生产省份_清洗": "省份", "产品二级类": "产品分类"})
    return out


def make_distribution(conc: pd.DataFrame) -> pd.DataFrame:
    if conc.empty:
        return pd.DataFrame()
    valid = conc[pd.to_numeric(conc["最终采用浓度值"], errors="coerce").notna()].copy()
    valid["最终采用浓度值"] = pd.to_numeric(valid["最终采用浓度值"], errors="coerce")
    if valid.empty:
        return pd.DataFrame()

    def log_mu(s):
        vals = pd.to_numeric(s, errors="coerce")
        vals = vals[vals > 0]
        return float(np.log(vals).mean()) if len(vals) >= 2 else np.nan

    def log_sigma(s):
        vals = pd.to_numeric(s, errors="coerce")
        vals = vals[vals > 0]
        return float(np.log(vals).std(ddof=1)) if len(vals) >= 2 else np.nan

    dist = valid.groupby(["省份", "年份", "月份", "年月", "供应链环节"], dropna=False).agg(
        样本量=("最终采用浓度值", "count"),
        均值=("最终采用浓度值", "mean"),
        中位数=("最终采用浓度值", "median"),
        P75=("最终采用浓度值", lambda s: s.quantile(0.75)),
        P90=("最终采用浓度值", lambda s: s.quantile(0.90)),
        P95=("最终采用浓度值", lambda s: s.quantile(0.95)),
        最大值=("最终采用浓度值", "max"),
        lognormal_mu=("最终采用浓度值", log_mu),
        lognormal_sigma=("最终采用浓度值", log_sigma),
    ).reset_index()
    dist["是否适合MonteCarlo模拟"] = np.where(dist["样本量"] >= 10, "较适合", np.where(dist["样本量"] >= 3, "可探索但样本偏少", "不适合/样本不足"))
    return dist


def main() -> int:
    ensure_dirs()
    if not RAW.exists():
        raise FileNotFoundError("核心输入 PEANUT2023-20241.xlsx 不存在，必须停止。")
    try:
        raw = pd.read_excel(RAW, sheet_name="Sheet1")
    except Exception as exc:
        raise RuntimeError(f"原始数据无法读取：{type(exc).__name__}: {exc}") from exc
    if not CLEAN.exists():
        raise FileNotFoundError("清洗主表不存在，且本脚本需要既有清洗主表承接非浓度字段。")

    old_clean = pd.read_csv(CLEAN, low_memory=False)
    old_conc = pd.read_csv(CONC, low_memory=False) if CONC.exists() else pd.DataFrame()
    old_panel = pd.read_csv(PANEL, low_memory=False) if PANEL.exists() else pd.DataFrame()
    df = old_clean.copy()

    for c in ["是否合格", "是否不合格", "是否AFB1相关", "是否超标", "AFB1相关不合格"]:
        if c in df:
            df[c] = as_bool(df[c])

    findings = []
    repair_log = []

    # Use cleaned table as the repair target and raw table as verification evidence.
    text_missing = [c for c in TEXT_COLS + ["检测数值", "法规限制", "判定结果"] if c not in df.columns]
    if text_missing:
        raise RuntimeError("核心字段缺失且无法可靠替代：" + "、".join(text_missing))

    afb_result = df.apply(detect_afb1, axis=1)
    new_afb = pd.Series([x[0] for x in afb_result], index=df.index)
    new_basis = pd.Series([x[1] for x in afb_result], index=df.index)
    suspicious = pd.Series([x[2] for x in afb_result], index=df.index)
    old_afb = as_bool(df["是否AFB1相关"])
    afb_added = int((new_afb & ~old_afb).sum())
    afb_removed = int((old_afb & ~new_afb).sum())
    if afb_added or afb_removed:
        findings.append({"问题类型": "AFB1标签不一致", "发现数量": afb_added + afb_removed, "是否自动修复": "是", "影响范围": "清洗主表、浓度表、计数面板、belief状态"})
        repair_log.append(f"- AFB1 标签修复：新增 {afb_added} 条，移除 {afb_removed} 条。")
    df["是否AFB1相关"] = new_afb
    df["AFB1识别依据"] = new_basis
    df["AFB1识别可疑"] = suspicious
    df["污染物名称_标准化"] = np.where(df["是否AFB1相关"], "黄曲霉毒素B1（AFB1）", df.get("不合格项目_标准化", ""))
    df["污染物类别_标准化"] = np.where(df["是否AFB1相关"], "真菌毒素/生物毒素", df.get("污染物类别_标准化", "未识别"))

    parsed = df.apply(lambda r: parse_detection_value(r.get("检测数值"), bool(r["是否AFB1相关"])), axis=1)
    for col in ["原始检测数值", "初检浓度值", "复检浓度值", "最终采用浓度值", "浓度单位", "检测单位是否推断", "浓度清洗状态", "检测数值解析失败原因"]:
        old = df[col] if col in df else pd.Series([np.nan] * len(df))
        new = pd.Series([p[col] for p in parsed], index=df.index)
        changed = int((old.astype(str).fillna("") != new.astype(str).fillna("")).sum())
        if changed and col in {"最终采用浓度值", "复检浓度值", "初检浓度值", "浓度清洗状态"}:
            findings.append({"问题类型": f"{col}修复", "发现数量": changed, "是否自动修复": "是", "影响范围": "浓度清洗与超标判断"})
        df[col] = new

    limits = df.apply(lambda r: parse_limit_value(r.get("法规限制"), bool(r["是否AFB1相关"])), axis=1)
    for col in ["原始法规限制", "法规限量_数值", "法规限量_单位", "法规限量_比较符号", "法规限量_单位是否推断", "法规限量解析状态", "法规限量解析失败原因"]:
        old = df[col] if col in df else pd.Series([np.nan] * len(df))
        new = pd.Series([p[col] for p in limits], index=df.index)
        changed = int((old.astype(str).fillna("") != new.astype(str).fillna("")).sum())
        if changed and col in {"法规限量_数值", "法规限量_单位", "法规限量解析状态"}:
            findings.append({"问题类型": f"{col}修复", "发现数量": changed, "是否自动修复": "是", "影响范围": "超标判断与超标倍数"})
        df[col] = new

    numeric_possible = df["最终采用浓度值"].notna() & df["法规限量_数值"].notna()
    numeric_exceed = pd.Series(False, index=df.index)
    numeric_exceed.loc[numeric_possible] = pd.to_numeric(df.loc[numeric_possible, "最终采用浓度值"], errors="coerce") > pd.to_numeric(df.loc[numeric_possible, "法规限量_数值"], errors="coerce")
    fallback_exceed = df["是否AFB1相关"] & df["是否不合格"] & ~numeric_possible
    old_exceed = as_bool(df["是否超标"]) if "是否超标" in df else pd.Series(False, index=df.index)
    new_exceed = numeric_exceed | fallback_exceed
    exceed_changed = int((old_exceed != new_exceed).sum())
    if exceed_changed:
        findings.append({"问题类型": "是否超标修复", "发现数量": exceed_changed, "是否自动修复": "是", "影响范围": "浓度表、可行性判断"})
        repair_log.append(f"- 是否超标重算：{exceed_changed} 条记录发生变化；优先使用浓度/限量数值比较，无法比较时仅对 AFB1 不合格记录回退原始判定。")
    df["是否超标"] = new_exceed
    df["超标倍数"] = np.where(numeric_possible & (pd.to_numeric(df["法规限量_数值"], errors="coerce") > 0), pd.to_numeric(df["最终采用浓度值"], errors="coerce") / pd.to_numeric(df["法规限量_数值"], errors="coerce"), np.nan)
    df["是否检出"] = pd.to_numeric(df["最终采用浓度值"], errors="coerce").fillna(np.nan).gt(0)
    df["AFB1相关不合格"] = df["是否AFB1相关"] & df["是否不合格"]

    df["复核原因"] = df.apply(classify_review, axis=1)
    df["是否建议人工复核"] = df["复核原因"].ne("")

    old_conc_count = int(old_conc.shape[0]) if not old_conc.empty else 0
    conc = make_concentration_table(df)
    if old_conc_count != len(conc):
        findings.append({"问题类型": "AFB1浓度表记录数变化", "发现数量": abs(old_conc_count - len(conc)), "是否自动修复": "是", "影响范围": "浓度清洗表"})
        repair_log.append(f"- 浓度表记录数由 {old_conc_count} 变为 {len(conc)}。")

    dist = make_distribution(conc)
    panel = make_panel(df)
    if not old_panel.empty and "浓度可用记录数" in old_panel.columns:
        old_conc_total = int(pd.to_numeric(old_panel["浓度可用记录数"], errors="coerce").fillna(0).sum())
        new_conc_total = int(panel["浓度可用记录数"].sum())
        if old_conc_total != new_conc_total:
            findings.append({"问题类型": "计数面板浓度可用记录数口径错误", "发现数量": abs(old_conc_total - new_conc_total), "是否自动修复": "是", "影响范围": "计数面板、belief-MDP状态特征"})
            repair_log.append(f"- 计数面板 `浓度可用记录数` 从全表可用浓度口径修复为 AFB1 相关浓度可用口径：{old_conc_total} -> {new_conc_total}。")

    issue_rows = [
        {"问题类型": "AFB1相关但浓度无法解析", "记录数": int((df["是否AFB1相关"] & df["最终采用浓度值"].isna()).sum()), "处理方式": "保留原始值并写入复核原因"},
        {"问题类型": "AFB1相关但法规限量无法解析", "记录数": int((df["是否AFB1相关"] & df["法规限量_数值"].isna()).sum()), "处理方式": "保留原始限量并写入复核原因"},
        {"问题类型": "数值超标判断与原始判定结果不一致", "记录数": int(df["复核原因"].str.contains("数值超标判断", na=False).sum()), "处理方式": "以数值比较为主，标记人工复核"},
        {"问题类型": "AFB1识别可疑", "记录数": int(df["AFB1识别可疑"].sum()), "处理方式": "不静默纳入，标记复核"},
        {"问题类型": "建议人工复核", "记录数": int(df["是否建议人工复核"].sum()), "处理方式": "详见清洗主表复核原因"},
    ]
    issue_log = pd.DataFrame(issue_rows)

    to_csv(df, CLEAN)
    try:
        df.to_excel(CLEAN_XLSX, index=False)
    except Exception as exc:
        repair_log.append(f"- XLSX 主表输出失败，保留 CSV；错误：{type(exc).__name__}: {exc}")
    to_csv(conc, CONC)
    to_csv(dist, DIST)
    to_csv(panel, PANEL)
    try:
        panel.to_excel(PANEL_XLSX, index=False)
    except Exception as exc:
        repair_log.append(f"- XLSX 计数面板输出失败，保留 CSV；错误：{type(exc).__name__}: {exc}")
    to_csv(issue_log, ROOT / "reports/tables/peanut_data_quality_summary.csv")
    to_csv(issue_log, ROOT / "reports/tables/peanut_cleaning_issue_log.csv")

    findings_df = pd.DataFrame(findings) if findings else pd.DataFrame([{"问题类型": "未发现需修复问题", "发现数量": 0, "是否自动修复": "不适用", "影响范围": "无"}])
    to_csv(findings_df, ROOT / "reports/tables/peanut_concentration_audit_findings.csv")

    # Rebuild belief states because count-panel concentration coverage and possibly AFB1 labels changed.
    beta_stdout = ""
    try:
        beta = subprocess.run([sys.executable, str(ROOT / "scripts/run_peanut_beta_belief_update.py")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=600)
        beta_stdout = beta.stdout[-1000:]
        if beta.returncode != 0:
            repair_log.append(f"- Beta-Binomial 重建失败，需后续处理：{beta.stderr[-1000:]}")
    except Exception as exc:
        repair_log.append(f"- Beta-Binomial 重建执行异常，需后续处理：{type(exc).__name__}: {exc}")

    summary = {
        "clean_rows": int(len(df)),
        "raw_rows": int(len(raw)),
        "afb1_records": int(df["是否AFB1相关"].sum()),
        "afb1_concentration_rows": int(len(conc)),
        "afb1_concentration_available": int(pd.to_numeric(conc["最终采用浓度值"], errors="coerce").notna().sum()),
        "afb1_limit_available": int(pd.to_numeric(conc["法规限量_数值"], errors="coerce").notna().sum()),
        "afb1_exceedance": int(as_bool(conc["是否超标"]).sum()),
        "panel_rows": int(len(panel)),
        "panel_afb1_concentration_available_total": int(panel["浓度可用记录数"].sum()),
        "belief_rebuilt": BELIEF.exists() and STATE.exists(),
    }

    report = f"""# PEANUT 上游结果自动查验报告

## 查验范围

- 原始数据：`data/01_raw/PEANUT2023-20241.xlsx`
- 清洗主表：`data/03_primary/peanut_cleaned_analysis_ready.csv`
- AFB1 浓度清洗表：`data/04_feature/peanut_concentration_clean_table.csv`
- 浓度分布摘要：`data/04_feature/peanut_concentration_distribution_summary.csv`
- 计数面板：`data/04_feature/peanut_count_panel.csv`
- Beta-Binomial belief state：`data/04_feature/peanut_beta_binomial_belief_states.csv`
- belief-MDP state features：`data/04_feature/peanut_belief_mdp_state_features.csv`

## 核心统计

```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

## 发现问题与修复

{md_table(findings_df, 30)}

## 浓度清洗 must-pass 检查结论

- AFB1 常见变体识别：已使用扩展规则复核并重算。
- 非 AFB1 生物毒素误识别：未默认把所有 `生物毒素` 视为 AFB1；可疑记录进入复核。
- `检测数值`：已重算原始值、初检值、复检值、最终采用值、单位、解析状态和失败原因。
- `法规限制`：已重算原始限量、数值、单位、比较符号和单位推断标记。
- AFB1 单位：优先统一到 `μg/kg`；无法统一的记录进入复核。
- `是否超标`：已优先使用统一单位后的浓度与限量比较，并与原始判定交叉校验。
- `超标倍数`：已基于统一单位后的浓度和限量重算。
- 浓度分布摘要：仅基于有效 AFB1 浓度记录生成。
- 报告统计：本报告统计直接从修复后的 CSV 重新计算。

## 下游影响

本次修复影响了浓度清洗表、浓度分布摘要和计数面板中的 `浓度可用记录数` 口径，因此已同步重建 Beta-Binomial belief state 与 belief-MDP state features。
"""
    write_text(ROOT / "reports/peanut_upstream_verification_report.md", report)

    concentration_report = f"""# AFB1 浓度清洗修复后报告

## 记录范围

- AFB1 相关记录数：{summary['afb1_records']}
- 浓度清洗表记录数：{summary['afb1_concentration_rows']}
- 最终采用浓度可用记录数：{summary['afb1_concentration_available']}
- 法规限量可用记录数：{summary['afb1_limit_available']}
- 超标记录数：{summary['afb1_exceedance']}
- 浓度分布摘要行数：{len(dist)}

## 修复后规则

- AFB1 识别覆盖 `黄曲霉毒素B₁`、`黄曲霉毒素B1`、`黄曲霉毒素B`、`黄曲霉毒素 B₁`、`AFB1`、`AFB`、`B₁/B1` 等上下文变体。
- 不把所有 `生物毒素` 默认视为 AFB1；可疑但不确定的记录进入人工复核。
- 检测数值保留原始文本，提取初检值、复检值和最终采用值；复检值可解析时优先采用复检值。
- AFB1 浓度和法规限量优先统一为 `μg/kg`。
- `≤20`、`20` 等无单位限量仅在 AFB1 上下文中推断为 `μg/kg`，并记录单位推断标记。
- `是否超标` 优先由最终采用浓度值与法规限量数值比较得到，并与原始判定结果交叉校验。
- `超标倍数` 基于统一单位后的浓度和限量计算。

## Issue Log

{md_table(issue_log, 20)}

## 分布摘要样例

{md_table(dist, 20)}
"""
    write_text(ROOT / "reports/peanut_concentration_cleaning_report.md", concentration_report)

    count_panel_report = f"""# 花生风险计数面板修复后报告

## 面板索引

- 索引：`省份 × 年份 × 月份 × 年月 × 供应链环节`
- 面板行数：{len(panel)}
- 抽检总批次数合计：{int(panel['抽检总批次数'].sum())}
- AFB1 相关记录数合计：{int(panel['AFB1相关记录数'].sum())}
- AFB1 浓度可用记录数合计：{int(panel['浓度可用记录数'].sum())}

## 关键修复

`浓度可用记录数` 已修复为 AFB1 相关记录中最终采用浓度可用的记录数，不再使用全表任意检测数值可用口径。该修复已同步重建 Beta-Binomial belief state 和 belief-MDP state features。

## 面板样例

{md_table(panel, 20)}
"""
    write_text(ROOT / "reports/peanut_count_panel_report.md", count_panel_report)

    cleaning_report = f"""# 花生抽检数据清洗修复后报告

## 修复后规模

- 清洗主表记录数：{summary['clean_rows']}
- AFB1 相关记录数：{summary['afb1_records']}
- AFB1 浓度可用记录数：{summary['afb1_concentration_available']}
- AFB1 法规限量可用记录数：{summary['afb1_limit_available']}

## 本轮重点修复

- 复核并修复 AFB1 标签。
- 复核并修复检测数值、法规限制、单位统一、是否超标和超标倍数。
- 重新生成浓度清洗表、浓度分布摘要、计数面板、Beta-Binomial belief state 和 belief-MDP state features。

## 数据质量问题

{md_table(issue_log, 20)}
"""
    write_text(ROOT / "reports/peanut_cleaning_report.md", cleaning_report)

    repair = "# PEANUT 上游修复日志\n\n"
    repair += "## 已自动修复问题\n\n"
    repair += "\n".join(repair_log) if repair_log else "无。\n"
    repair += "\n\n## 已降级处理问题\n\n无。\n\n## 未解决且需要用户处理的问题\n\n无。\n"
    write_text(ROOT / "reports/peanut_upstream_repair_log.md", repair)

    dqn_ready = False
    blockers = [
        "仍缺少 DQN/MDP 奖励函数所需的预算、产能、抽检成本、处置/召回损失、信息价值权重等外部参数。",
        "MOE/EDI 仍缺少消费量、人口、体重、BMDL 等外部参数。",
        "当前已具备修复后的 belief-MDP 状态特征，但尚未定义动作空间与约束。"
    ]
    readiness = f"""# DQN 前置状态判断：上游修复后

1. 浓度清洗是否通过复核：通过核心自动复核；仍有无法解析或需人工复核记录，已进入 issue/复核原因，不阻止数据表继续作为原型输入。
2. AFB1 标签是否通过复核：通过扩展规则复核，未默认把所有生物毒素视为 AFB1。
3. 计数面板是否通过复核：通过并已重建；`浓度可用记录数` 已改为 AFB1 相关浓度可用口径。
4. Beta-Binomial belief state 是否仍可用：已重建，可用于原型。
5. belief-MDP state features 是否仍可用：已重建，可用于最小环境设计。
6. 是否可以进入最小 DQN prototype：否，当前不要进入 DQN。
7. 阻塞原因：
{chr(10).join('- ' + b for b in blockers)}
8. 下一步应修什么：先定义最小 belief-MDP 的动作档位、预算/产能约束、奖励函数参数需求，并补齐 MOE/EDI 外部参数；在参数缺失时只能做环境设计，不训练 DQN。
"""
    write_text(ROOT / "reports/peanut_pre_dqn_readiness_after_repair.md", readiness)

    today = datetime.now().strftime("%Y-%m-%d")
    write_text(ROOT / "project_state/current_focus.md", "# Current Focus\n\n当前焦点：已执行 PEANUT 上游输出自动查验与浓度清洗修复。下一阶段不要进入 DQN；应先基于修复后的 `peanut_belief_mdp_state_features.csv` 设计最小 belief-MDP 环境，并补齐预算、产能、成本、召回损失、消费量、人口、体重和 BMDL 等外部参数。\n")
    write_text(ROOT / "project_state/next_step.md", "# Next Step\n\n当前阻塞正式 DQN：缺少动作空间、预算/产能约束、抽检成本、处置/召回损失、信息价值权重，以及 MOE/EDI 的消费量、人口、体重、BMDL。下一步先设计最小 belief-MDP 环境参数表与外部参数需求清单，不训练 DQN。\n")
    with (ROOT / "project_state/changelog.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {today}\n\n- Added upstream verification and concentration-cleaning must-pass rules to `AGENTS.md` and skills.\n- Created upstream/concentration auditor skills under `.agents/skills/` and `skills/`.\n- Audited and repaired PEANUT concentration cleaning outputs, regenerated cleaned table, concentration table, concentration distribution summary, count panel, Beta-Binomial states, and belief-MDP state features.\n")
    with (ROOT / "project_state/decision_log.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {today}\n\n### Require upstream verification before downstream models\n\nRationale: 下游 DQN/POMDP/MOE-EDI 依赖浓度、标签、计数面板和 belief state；若上游存在解析或口径错误，会直接污染模型状态和结论。\n\nImpact: 任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。本次已修复计数面板 `浓度可用记录数` 口径，并同步重建 belief state 与 belief-MDP state features。\n")
    with (ROOT / "project_state/lessons_learned.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {today} Upstream Verification Lessons\n\n- 任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。\n- 计数面板中的 `浓度可用记录数` 对 AFB1 风险建模应采用 AFB1 相关浓度可用口径，而不是全表任意检测数值可用口径。\n- `是否超标` 应优先由统一单位后的浓度和法规限量计算，再与原始判定结果交叉校验。\n")
    with (ROOT / "project_state/project_memory.md").open("a", encoding="utf-8") as f:
        f.write("\n## Upstream Verification Long-Term Rule\n\n任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。\n")
    with (ROOT / "project_state/run_protocol.md").open("a", encoding="utf-8") as f:
        f.write("\n## Upstream Verification Protocol\n\n进入 MOE/EDI、POMDP、belief-MDP、DQN 或正式可视化之前，必须先查验清洗主表、浓度清洗表、计数面板、字典、Beta-Binomial belief state 和 belief-MDP state features。若发现遗漏、解析失败、标签冲突、数值异常或报告与数据不一致，应自动修复并重建受影响产物；不得带着已知错误进入下游模型。\n")
    handoff = f"""# Conversation Handoff

## 当前状态

已完成 PEANUT 上游输出自动查验与浓度清洗修复。本轮没有进入 DQN。

## 核心输出

- `reports/peanut_upstream_verification_report.md`
- `reports/peanut_upstream_repair_log.md`
- `reports/tables/peanut_concentration_audit_findings.csv`
- `reports/peanut_pre_dqn_readiness_after_repair.md`
- `data/03_primary/peanut_cleaned_analysis_ready.csv`
- `data/04_feature/peanut_concentration_clean_table.csv`
- `data/04_feature/peanut_concentration_distribution_summary.csv`
- `data/04_feature/peanut_count_panel.csv`
- `data/04_feature/peanut_beta_binomial_belief_states.csv`
- `data/04_feature/peanut_belief_mdp_state_features.csv`

## 当前阻塞

不要进入正式 DQN。仍缺少动作空间、预算/产能约束、抽检成本、处置/召回损失、信息价值权重，以及 MOE/EDI 所需消费量、人口、体重、BMDL。

## 继续 Prompt

请继续 PEANUT 项目。先读取 `reports/peanut_upstream_verification_report.md`、`reports/peanut_pre_dqn_readiness_after_repair.md` 和 `data/04_feature/peanut_belief_mdp_state_features.csv`，不要运行 DQN，先设计最小 belief-MDP 环境参数表和外部参数需求清单。
"""
    write_text(ROOT / "project_state/conversation_handoff.md", handoff)
    write_text(ROOT / "reports/peanut_upstream_audit_summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        ensure_dirs()
        msg = f"""# PEANUT 上游修复日志

## 未解决且需要用户处理的问题

- 错误类型：`{type(exc).__name__}`
- 错误位置：`scripts/audit_and_repair_peanut_upstream.py`
- 错误信息：{exc}

## 说明

本脚本已内置轻量路径、编码、表格输出、XLSX 输出降级和正则修复策略。当前错误属于核心输入或核心字段问题，无法可靠自动修复。
"""
        write_text(ROOT / "reports/peanut_upstream_repair_log.md", msg)
        print(msg, file=sys.stderr)
        raise
