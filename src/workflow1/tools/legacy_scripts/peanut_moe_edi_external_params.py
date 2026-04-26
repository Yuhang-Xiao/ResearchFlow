from __future__ import annotations

import json
import math
import re
import shutil
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TASK_NAME = "MOE_EDI外部参数匹配与风险度量准备"
RUN_DATE = date.today().strftime("%Y%m%d")
OUT_DIR = ROOT / "outputs" / f"{RUN_DATE}_{TASK_NAME}"
SUBDIRS = ["data", "reports", "tables", "figures", "logs", "configs"]

FEATURE_DIR = ROOT / "data" / "04_feature"
RAW_DIR = ROOT / "data" / "01_raw"
REPORT_DIR = ROOT / "reports"

BODY_WEIGHT_KG = 60.0
MOE_CUTOFF = 3160.0
BMDL_SCENARIOS = {
    "low_bmdl": 0.050,
    "sensitive_bmdl": 0.066,
    "default_bmdl": 0.105,
    "high_bmdl": 0.158,
    "upper_bmdl": 0.189,
}

EN_TO_CN = {
    "Beijing": "北京",
    "Tianjin": "天津",
    "Hebei": "河北",
    "Shanxi": "山西",
    "Inner Mongolia": "内蒙古",
    "Liaoning": "辽宁",
    "Jilin": "吉林",
    "Heilongjiang": "黑龙江",
    "Shanghai": "上海",
    "Jiangsu": "江苏",
    "Zhejiang": "浙江",
    "Anhui": "安徽",
    "Fujian": "福建",
    "Jiangxi": "江西",
    "Shandong": "山东",
    "Henan": "河南",
    "Hubei": "湖北",
    "Hunan": "湖南",
    "Guangdong": "广东",
    "Guangxi": "广西",
    "Hainan": "海南",
    "Chongqing": "重庆",
    "Sichuan": "四川",
    "Guizhou": "贵州",
    "Yunnan": "云南",
    "Tibet": "西藏",
    "Shaanxi": "陕西",
    "Gansu": "甘肃",
    "Qinghai": "青海",
    "Ningxia": "宁夏",
    "Xinjiang": "新疆",
}


def ensure_dirs() -> None:
    for sub in SUBDIRS:
        (OUT_DIR / sub).mkdir(parents=True, exist_ok=True)
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def find_raw_file(target: str) -> Path:
    target_key = re.sub(r"[^a-z0-9]+", "", target.lower())
    candidates = [p for p in RAW_DIR.iterdir() if p.is_file()]
    scored = []
    for p in candidates:
        key = re.sub(r"[^a-z0-9]+", "", p.stem.lower())
        score = 0
        if target_key == key:
            score = 100
        elif target_key in key or key in target_key:
            score = 80
        else:
            for token in re.findall(r"[a-z0-9]+", target.lower()):
                if token and token in key:
                    score += 10
        if score:
            scored.append((score, p))
    if not scored:
        raise FileNotFoundError(f"无法在 data/01_raw 中识别文件：{target}")
    return sorted(scored, key=lambda x: (-x[0], x[1].name))[0][1]


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in [".xlsx", ".xls"]:
        xls = pd.ExcelFile(path)
        best_sheet = xls.sheet_names[0]
        best_cols = -1
        for sheet in xls.sheet_names:
            preview = pd.read_excel(path, sheet_name=sheet, nrows=10)
            if len(preview.columns) > best_cols:
                best_sheet, best_cols = sheet, len(preview.columns)
        return pd.read_excel(path, sheet_name=best_sheet)
    return pd.read_csv(path, encoding="utf-8-sig")


def normalize_province(value) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan" or text in {"不详", "未知", "NA"}:
        return None
    if text in EN_TO_CN:
        text = EN_TO_CN[text]
    text = re.sub(r"\s+", "", text)
    replacements = [
        "维吾尔自治区",
        "壮族自治区",
        "回族自治区",
        "自治区",
        "省",
        "市",
    ]
    for item in replacements:
        text = text.replace(item, "")
    return text


def to_numeric(s) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def safe_ratio(num, den):
    if den in [0, None] or pd.isna(den):
        return math.nan
    return num / den


def risk_level(moe):
    if pd.isna(moe) or math.isinf(moe):
        return "无法计算"
    if moe < MOE_CUTOFF:
        return "低于阈值/需关注"
    if moe < 10000:
        return "接近阈值/观察"
    return "高于阈值/低关注"


def svg_bar(path: Path, title: str, labels: list[str], values: list[float], x_label: str = "") -> None:
    width, height = 960, 560
    margin_l, margin_r, margin_t, margin_b = 180, 40, 60, 70
    inner_w, inner_h = width - margin_l - margin_r, height - margin_t - margin_b
    finite = [v for v in values if pd.notna(v) and math.isfinite(float(v))]
    max_v = max(finite) if finite else 1
    n = max(1, len(values))
    bar_h = max(8, min(28, inner_h / n * 0.72))
    gap = max(2, (inner_h - bar_h * n) / max(1, n - 1)) if n > 1 else 0
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="20" font-family="Arial, Microsoft YaHei">{title}</text>',
        f'<line x1="{margin_l}" y1="{height-margin_b}" x2="{width-margin_r}" y2="{height-margin_b}" stroke="#333"/>',
    ]
    for i, (lab, val) in enumerate(zip(labels, values)):
        v = 0 if pd.isna(val) or not math.isfinite(float(val)) else float(val)
        y = margin_t + i * (bar_h + gap)
        w = 0 if max_v <= 0 else inner_w * v / max_v
        lines.append(f'<text x="{margin_l-8}" y="{y+bar_h*0.75:.1f}" text-anchor="end" font-size="12" font-family="Arial, Microsoft YaHei">{lab}</text>')
        lines.append(f'<rect x="{margin_l}" y="{y:.1f}" width="{w:.1f}" height="{bar_h:.1f}" fill="#2f6f73"/>')
        lines.append(f'<text x="{margin_l+w+5:.1f}" y="{y+bar_h*0.75:.1f}" font-size="11" font-family="Arial, Microsoft YaHei">{v:.3g}</text>')
    lines.append(f'<text x="{width/2}" y="{height-22}" text-anchor="middle" font-size="13" font-family="Arial, Microsoft YaHei">{x_label}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def svg_hist(path: Path, title: str, values: pd.Series, bins: int = 20, transform=None, x_label: str = "") -> None:
    vals = pd.to_numeric(values, errors="coerce").dropna()
    vals = vals[vals.map(lambda x: math.isfinite(float(x)))]
    if transform:
        vals = vals[vals > 0].map(transform)
    if vals.empty:
        labels, counts = ["无可用值"], [0]
    else:
        counts, edges = pd.cut(vals, bins=bins, retbins=True, include_lowest=True)
        vc = counts.value_counts().sort_index()
        labels = [f"{iv.left:.2g}-{iv.right:.2g}" for iv in vc.index]
        counts = vc.tolist()
    svg_bar(path, title, labels, counts, "频数" if not x_label else x_label)


def build_bmdl_config() -> dict:
    scenario_values = list(BMDL_SCENARIOS.values())
    log_values = [math.log(v) for v in scenario_values if v > 0]
    mu_default = math.log(BMDL_SCENARIOS["default_bmdl"])
    sigma_scenario = float(pd.Series(log_values).std(ddof=1))
    z95 = 1.6448536269514722
    z99 = 2.3263478740408408
    sigma_from_p5_p95_pair = (math.log(0.158) - math.log(0.066)) / (2 * z95)
    sigma_from_p1_p99_pair = (math.log(0.189) - math.log(0.050)) / (2 * z99)
    sigma_paired_approx = float(pd.Series([sigma_from_p5_p95_pair, sigma_from_p1_p99_pair]).mean())
    return {
        "source_note": "用户提供截图中的 QIVIVE predicted BMDL10 based on HCC；当前仅作 MOE/EDI prototype 参数，正式论文需补充可引用文献或原始来源。",
        "unit": "μg/kg bw",
        "moe_cutoff": MOE_CUTOFF,
        "body_weight_kg": BODY_WEIGHT_KG,
        "reported_points": [
            {"label": "general Chinese population", "statistic": "GM", "value": 0.105},
            {"label": "sensitive Chinese population", "statistic": "P95", "value": 0.066},
            {"label": "less sensitive Chinese population", "statistic": "P5", "value": 0.158},
            {"label": "sensitive Chinese population", "statistic": "P99", "value": 0.050},
            {"label": "sensitive Chinese population", "statistic": "P1", "value": 0.189},
        ],
        "ambiguity_note": "P1/P5/P95/P99 与 sensitive/less sensitive 命名方向存在歧义，本配置不强行解释为普通统计分位数；使用情景值和基于情景 log 值的近似 sigma。",
        "scenario_values": BMDL_SCENARIOS,
        "lognormal_approximation": {
            "distribution": "lognormal",
            "center_value_used": "default_bmdl",
            "mu_log": mu_default,
            "sigma_log_primary_paired_endpoint_approx": sigma_paired_approx,
            "sigma_log_from_p5_p95_endpoint_pair": sigma_from_p5_p95_pair,
            "sigma_log_from_p1_p99_endpoint_pair": sigma_from_p1_p99_pair,
            "sigma_log_from_all_scenario_values_descriptive": sigma_scenario,
            "approximation_warning": "因截图中的敏感/不敏感命名与 P1/P5/P95/P99 方向存在歧义，primary sigma 仅按低/高端点成对近似；仅用于原型风险度量准备，不作为最终毒理学分布结论。",
        },
    }


def main() -> None:
    ensure_dirs()
    errors: list[dict] = []
    inputs = {
        "concentration": FEATURE_DIR / "peanut_concentration_clean_table.csv",
        "distribution": FEATURE_DIR / "peanut_concentration_distribution_summary.csv",
        "count_panel": FEATURE_DIR / "peanut_count_panel.csv",
        "belief_states": FEATURE_DIR / "peanut_beta_binomial_belief_states.csv",
        "state_features": FEATURE_DIR / "peanut_belief_mdp_state_features.csv",
        "readiness_after_repair": REPORT_DIR / "peanut_pre_dqn_readiness_after_repair.md",
        "consumption_raw": find_raw_file("Concentration_and_Consumption pEANUT"),
        "population_raw": find_raw_file("population_long_clean"),
    }

    missing = [str(p) for p in inputs.values() if isinstance(p, Path) and not p.exists()]
    if missing:
        raise FileNotFoundError("缺少核心输入文件：" + "; ".join(missing))

    conc = pd.read_csv(inputs["concentration"], encoding="utf-8-sig")
    dist = pd.read_csv(inputs["distribution"], encoding="utf-8-sig")
    count_panel = pd.read_csv(inputs["count_panel"], encoding="utf-8-sig")
    state = pd.read_csv(inputs["state_features"], encoding="utf-8-sig")
    consumption_raw = read_table(inputs["consumption_raw"])
    population_raw = read_table(inputs["population_raw"])

    required_conc = ["省份", "年份", "月份", "年月", "供应链环节", "最终采用浓度值", "浓度单位", "是否AFB1相关"]
    required_state = ["省份", "年份", "月份", "年月", "供应链环节", "状态ID"]
    for cols, df_name, df in [(required_conc, "浓度清洗表", conc), (required_state, "belief-MDP 状态特征表", state)]:
        miss = [c for c in cols if c not in df.columns]
        if miss:
            raise ValueError(f"{df_name} 缺少关键字段：{miss}")

    conc["省份_规范"] = conc["省份"].map(normalize_province)
    count_panel["省份_规范"] = count_panel["省份"].map(normalize_province)
    state["省份_规范"] = state["省份"].map(normalize_province)
    state["年份"] = to_numeric(state["年份"]).astype("Int64")
    conc["年份"] = to_numeric(conc["年份"]).astype("Int64")
    conc["月份"] = to_numeric(conc["月份"]).astype("Int64")

    bmdl_config = build_bmdl_config()
    bmdl_path = FEATURE_DIR / "peanut_bmdl_parameter_config.json"
    bmdl_path.write_text(json.dumps(bmdl_config, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.copy2(bmdl_path, OUT_DIR / "configs" / bmdl_path.name)
    bmdl_table = pd.DataFrame(bmdl_config["reported_points"])
    bmdl_table["unit"] = bmdl_config["unit"]
    bmdl_table["source_note"] = "用户提供截图；正式论文需补充可引用文献或原始来源"
    bmdl_table_path = FEATURE_DIR / "peanut_bmdl_parameter_table.csv"
    bmdl_table.to_csv(bmdl_table_path, index=False, encoding="utf-8-sig")
    shutil.copy2(bmdl_table_path, OUT_DIR / "tables" / bmdl_table_path.name)

    cons = consumption_raw.copy()
    cons["省份"] = cons["Province"].astype(str)
    cons["省份_规范"] = cons["Province"].map(normalize_province)
    cons["年份"] = to_numeric(cons["MonitorngYear"]).astype("Int64")
    cons["消费量_g_day"] = to_numeric(cons["Consumption_g_day"])
    cons["消费量_kg_day"] = cons["消费量_g_day"] / 1000.0
    cons["平均消费量_g_day"] = cons["消费量_g_day"]
    cons["平均消费量_kg_day"] = cons["消费量_kg_day"]
    cons["P95或高消费量_g_day"] = math.nan
    cons["P95或高消费量_kg_day"] = math.nan
    cons["人群类别"] = "总人群/未分层"
    cons["消费量单位"] = "g/day"
    cons["消费量匹配方式"] = "原始省份-年份记录"
    cons["消费量匹配置信度"] = "高"
    cons["是否建议人工复核"] = False
    cons["复核原因"] = "原始文件未提供 P95 或高消费量字段；当前仅使用平均消费量。"
    cons_cols = [
        "省份",
        "省份_规范",
        "年份",
        "人群类别",
        "消费量单位",
        "平均消费量_g_day",
        "平均消费量_kg_day",
        "P95或高消费量_g_day",
        "P95或高消费量_kg_day",
        "SampleCount",
        "Contaminated sample",
        "Mean_concentration_MP(ug/kg)",
        "BodyWeight (kg)",
        "消费量匹配方式",
        "消费量匹配置信度",
        "是否建议人工复核",
        "复核原因",
    ]
    consumption_table = cons[cons_cols].copy()
    consumption_table_path = FEATURE_DIR / "peanut_consumption_parameter_table.csv"
    consumption_table.to_csv(consumption_table_path, index=False, encoding="utf-8-sig")
    shutil.copy2(consumption_table_path, OUT_DIR / "tables" / consumption_table_path.name)

    pop = population_raw.copy()
    pop["省份_规范"] = pop["Province"].map(normalize_province)
    pop["年份"] = to_numeric(pop["MonitoringYear"]).astype("Int64")
    pop["人口原始值"] = to_numeric(pop["population"])
    pop["人口单位"] = "万人（根据中国省级人口量级推断）"
    pop["人口数_人"] = pop["人口原始值"] * 10000
    pop["人群类别"] = "总人口/未分层"
    pop["是否长表结构"] = True
    pop["人口匹配方式"] = "原始省份-年份记录"
    pop["人口匹配置信度"] = "高"
    pop["是否建议人工复核"] = False
    pop["复核原因"] = ""
    pop_cols = [
        "Province",
        "省份_规范",
        "年份",
        "人群类别",
        "人口原始值",
        "人口单位",
        "人口数_人",
        "是否长表结构",
        "人口匹配方式",
        "人口匹配置信度",
        "是否建议人工复核",
        "复核原因",
    ]
    population_table = pop[pop_cols].copy()
    population_table_path = FEATURE_DIR / "peanut_population_parameter_table.csv"
    population_table.to_csv(population_table_path, index=False, encoding="utf-8-sig")
    shutil.copy2(population_table_path, OUT_DIR / "tables" / population_table_path.name)

    national_cons_kg = float(cons["消费量_kg_day"].median())
    national_cons_g = national_cons_kg * 1000.0

    cons_by_key = {(r["省份_规范"], int(r["年份"])): r for _, r in cons.dropna(subset=["省份_规范", "年份"]).iterrows()}
    cons_by_prov = {k: g.sort_values("年份") for k, g in cons.dropna(subset=["省份_规范", "年份"]).groupby("省份_规范")}

    def match_consumption(prov, year):
        prov_n = normalize_province(prov)
        y = int(year) if pd.notna(year) else None
        if prov_n and y is not None and (prov_n, y) in cons_by_key:
            r = cons_by_key[(prov_n, y)]
            return r["消费量_g_day"], r["消费量_kg_day"], "同省同年", "高", False, ""
        if prov_n and prov_n in cons_by_prov and y is not None:
            g = cons_by_prov[prov_n].copy()
            g["年份差"] = (g["年份"].astype(int) - y).abs()
            r = g.sort_values(["年份差", "年份"]).iloc[0]
            return r["消费量_g_day"], r["消费量_kg_day"], f"同省最近年份({int(r['年份'])})", "中", True, "消费量数据年份未覆盖当前面板年份，使用同省最近年份。"
        return national_cons_g, national_cons_kg, "全国中位数默认值", "低", True, "省份无法匹配消费量，使用全国中位数默认值。"

    pop_by_key = {(r["省份_规范"], int(r["年份"])): r for _, r in pop.dropna(subset=["省份_规范", "年份"]).iterrows()}
    pop_by_prov = {k: g.sort_values("年份") for k, g in pop.dropna(subset=["省份_规范", "年份"]).groupby("省份_规范")}

    def match_population(prov, year):
        prov_n = normalize_province(prov)
        y = int(year) if pd.notna(year) else None
        if prov_n and y is not None and (prov_n, y) in pop_by_key:
            r = pop_by_key[(prov_n, y)]
            return r["人口数_人"], r["人口原始值"], "同省同年", "高", False, ""
        if prov_n and prov_n in pop_by_prov and y is not None:
            g = pop_by_prov[prov_n].copy()
            g["年份差"] = (g["年份"].astype(int) - y).abs()
            r = g.sort_values(["年份差", "年份"]).iloc[0]
            return r["人口数_人"], r["人口原始值"], f"同省最近年份({int(r['年份'])})", "中", True, "人口数据年份未覆盖当前面板年份，使用同省最近年份。"
        return math.nan, math.nan, "未匹配", "无", True, "省份或年份无法匹配人口数据。"

    afb1 = conc[conc["是否AFB1相关"].astype(str).str.lower().isin(["true", "1", "yes"])].copy()
    afb1["AFB1浓度_μg_kg_food"] = to_numeric(afb1["最终采用浓度值"])
    afb1 = afb1[afb1["AFB1浓度_μg_kg_food"].notna()].copy()

    cons_matches = afb1.apply(lambda r: match_consumption(r["省份"], r["年份"]), axis=1, result_type="expand")
    cons_matches.columns = ["消费量_g_day", "消费量_kg_day", "消费量匹配方式", "消费量匹配置信度", "是否建议人工复核_消费量", "消费量复核原因"]
    edi = pd.concat([afb1.reset_index(drop=True), cons_matches.reset_index(drop=True)], axis=1)
    edi["体重_kg_bw"] = BODY_WEIGHT_KG
    edi["EDI_μg_kg_bw_day"] = edi["AFB1浓度_μg_kg_food"] * edi["消费量_kg_day"] / BODY_WEIGHT_KG
    for key, val in BMDL_SCENARIOS.items():
        col_suffix = key.replace("_bmdl", "")
        edi[f"BMDL_{key}_μg_kg_bw"] = val
        edi[f"MOE_{col_suffix}_bmdl"] = val / edi["EDI_μg_kg_bw_day"].replace(0, math.nan)
    edi["MOE_cutoff"] = MOE_CUTOFF
    edi["是否低于MOE阈值"] = edi["MOE_default_bmdl"] < MOE_CUTOFF
    edi["MOE风险等级"] = edi["MOE_default_bmdl"].map(risk_level)
    edi["MOE风险惩罚项"] = edi["MOE_default_bmdl"].map(lambda x: max(0.0, (MOE_CUTOFF - x) / MOE_CUTOFF) if pd.notna(x) and math.isfinite(float(x)) else math.nan)

    risk_cols = [
        "序号",
        "省份",
        "年份",
        "月份",
        "年月",
        "供应链环节",
        "产品分类",
        "产品名称",
        "AFB1浓度_μg_kg_food",
        "消费量_g_day",
        "消费量_kg_day",
        "消费量匹配方式",
        "消费量匹配置信度",
        "是否建议人工复核_消费量",
        "消费量复核原因",
        "体重_kg_bw",
        "EDI_μg_kg_bw_day",
        "MOE_low_bmdl",
        "MOE_sensitive_bmdl",
        "MOE_default_bmdl",
        "MOE_high_bmdl",
        "MOE_upper_bmdl",
        "MOE_cutoff",
        "是否低于MOE阈值",
        "MOE风险等级",
        "MOE风险惩罚项",
    ]
    existing_risk_cols = [c for c in risk_cols if c in edi.columns]
    risk_table = edi[existing_risk_cols].copy()
    risk_table_path = FEATURE_DIR / "peanut_edi_moe_risk_table.csv"
    risk_table.to_csv(risk_table_path, index=False, encoding="utf-8-sig")
    shutil.copy2(risk_table_path, OUT_DIR / "data" / risk_table_path.name)

    group_keys = ["省份", "年份", "月份", "年月", "供应链环节"]
    summary = edi.groupby(group_keys, dropna=False).agg(
        EDI记录数=("EDI_μg_kg_bw_day", "count"),
        EDI均值=("EDI_μg_kg_bw_day", "mean"),
        EDI中位数=("EDI_μg_kg_bw_day", "median"),
        EDI_P95=("EDI_μg_kg_bw_day", lambda s: s.quantile(0.95)),
        MOE_default_均值=("MOE_default_bmdl", "mean"),
        MOE_default_中位数=("MOE_default_bmdl", "median"),
        MOE_default_最小值=("MOE_default_bmdl", "min"),
        低于MOE阈值记录数=("是否低于MOE阈值", "sum"),
        MOE风险惩罚项_均值=("MOE风险惩罚项", "mean"),
    ).reset_index()
    summary["低于MOE阈值比例"] = summary["低于MOE阈值记录数"] / summary["EDI记录数"]
    summary["MOE风险等级_主导"] = summary["MOE_default_中位数"].map(risk_level)
    risk_summary_path = FEATURE_DIR / "peanut_edi_moe_risk_summary.csv"
    summary.to_csv(risk_summary_path, index=False, encoding="utf-8-sig")
    shutil.copy2(risk_summary_path, OUT_DIR / "tables" / risk_summary_path.name)

    state_cons = state.apply(lambda r: match_consumption(r["省份"], r["年份"]), axis=1, result_type="expand")
    state_cons.columns = ["消费量_g_day", "消费量_kg_day", "消费量匹配方式", "消费量匹配置信度", "是否建议人工复核_消费量", "消费量复核原因"]
    state_pop = state.apply(lambda r: match_population(r["省份"], r["年份"]), axis=1, result_type="expand")
    state_pop.columns = ["人口数_人", "人口原始值_万人", "人口匹配方式", "人口匹配置信度", "是否建议人工复核_人口", "人口复核原因"]
    state_ext = pd.concat([state.reset_index(drop=True), state_cons.reset_index(drop=True), state_pop.reset_index(drop=True)], axis=1)
    state_ext["体重_kg_bw"] = BODY_WEIGHT_KG
    state_ext["BMDL_default_μg_kg_bw"] = BMDL_SCENARIOS["default_bmdl"]
    state_ext["BMDL_low_μg_kg_bw"] = BMDL_SCENARIOS["low_bmdl"]
    state_ext["BMDL_sensitive_μg_kg_bw"] = BMDL_SCENARIOS["sensitive_bmdl"]
    state_ext["BMDL_high_μg_kg_bw"] = BMDL_SCENARIOS["high_bmdl"]
    state_ext["BMDL_upper_μg_kg_bw"] = BMDL_SCENARIOS["upper_bmdl"]

    state_ext = state_ext.merge(summary, on=group_keys, how="left")
    state_ext["是否低于MOE_cutoff"] = state_ext["低于MOE阈值比例"].fillna(0) > 0
    state_ext["人口加权风险_proxy"] = state_ext["低于MOE阈值比例"].fillna(0) * state_ext["人口数_人"]
    state_ext["MOE风险惩罚_proxy"] = state_ext["MOE风险惩罚项_均值"].fillna(0)
    add_cols = [
        "消费量_kg_day",
        "人口数_人",
        "体重_kg_bw",
        "BMDL_default_μg_kg_bw",
        "EDI均值",
        "EDI_P95",
        "MOE_default_中位数",
        "MOE_default_最小值",
        "低于MOE阈值比例",
        "人口加权风险_proxy",
        "MOE风险惩罚_proxy",
    ]
    if "belief_mdp_state_vector_columns" in state_ext.columns:
        prior = state_ext["belief_mdp_state_vector_columns"].fillna("").astype(str)
        state_ext["belief_mdp_state_vector_columns"] = prior.map(lambda x: x + "," + ",".join(add_cols) if x else ",".join(add_cols))

    state_ext_path = FEATURE_DIR / "peanut_belief_mdp_state_features_with_moe_edi.csv"
    state_ext.to_csv(state_ext_path, index=False, encoding="utf-8-sig")
    shutil.copy2(state_ext_path, OUT_DIR / "data" / state_ext_path.name)

    panel_matches = state_ext[["省份", "年份", "人口匹配方式", "人口匹配置信度", "人口数_人"]].copy()
    total_units = len(panel_matches)
    pop_success = int(panel_matches["人口数_人"].notna().sum())
    pop_unmatched = total_units - pop_success
    unmatched_pop = (
        panel_matches[panel_matches["人口数_人"].isna()][["省份", "年份"]]
        .drop_duplicates()
        .sort_values(["省份", "年份"])
    )
    cons_success_exact = int((state_ext["消费量匹配方式"] == "同省同年").sum())
    cons_success_any = int(state_ext["消费量_kg_day"].notna().sum())
    cons_review = int(state_ext["是否建议人工复核_消费量"].sum())
    pop_review = int(state_ext["是否建议人工复核_人口"].sum())

    # Figures
    cons_fig = consumption_table.groupby("省份_规范")["平均消费量_g_day"].median().sort_values(ascending=False).head(25)
    svg_bar(OUT_DIR / "figures" / "consumption_parameter_distribution.svg", "消费量参数分布（省级中位数，g/day）", cons_fig.index.astype(str).tolist(), cons_fig.tolist(), "g/day")
    pop_match_counts = state_ext["人口匹配方式"].fillna("未匹配").value_counts()
    svg_bar(OUT_DIR / "figures" / "population_matching_status.svg", "人口匹配情况", pop_match_counts.index.astype(str).tolist(), pop_match_counts.tolist(), "状态单元数")
    svg_hist(OUT_DIR / "figures" / "edi_distribution.svg", "EDI 分布", risk_table["EDI_μg_kg_bw_day"], bins=20, x_label="EDI 分箱频数")
    svg_hist(OUT_DIR / "figures" / "moe_distribution_log10.svg", "MOE 分布（log10）", risk_table["MOE_default_bmdl"], bins=20, transform=lambda x: math.log10(x), x_label="log10(MOE) 分箱频数")
    risk_counts = risk_table["MOE风险等级"].fillna("无法计算").value_counts()
    svg_bar(OUT_DIR / "figures" / "moe_risk_level_distribution.svg", "MOE 风险等级分布", risk_counts.index.astype(str).tolist(), risk_counts.tolist(), "记录数")
    prov_risk = risk_table.groupby("省份").agg(
        风险比例=("是否低于MOE阈值", "mean"),
        记录数=("是否低于MOE阈值", "count"),
        MOE中位数=("MOE_default_bmdl", "median"),
    ).reset_index()
    prov_risk = prov_risk[prov_risk["记录数"] >= 1].sort_values(["风险比例", "MOE中位数"], ascending=[False, True]).head(25)
    svg_bar(OUT_DIR / "figures" / "province_moe_risk_ranking.svg", "省份维度 MOE 风险排序（低于阈值比例）", prov_risk["省份"].astype(str).tolist(), prov_risk["风险比例"].tolist(), "低于阈值比例")

    upstream_checks = {
        "required_files_all_present": True,
        "concentration_rows": int(len(conc)),
        "afb1_rows_with_numeric_concentration": int(len(afb1)),
        "count_panel_rows": int(len(count_panel)),
        "state_feature_rows": int(len(state)),
        "count_panel_state_feature_row_match": int(len(count_panel)) == int(len(state)),
        "negative_concentration_rows": int((conc["最终采用浓度值"].pipe(to_numeric) < 0).sum()),
        "risk_table_rows": int(len(risk_table)),
        "risk_summary_rows": int(len(summary)),
    }

    if cons_review:
        errors.append({
            "status": "degraded_but_continued",
            "stage": "消费量匹配",
            "issue": "消费量文件不覆盖 2023-2024 面板年份，部分或全部状态单元使用同省最近年份或全国中位数。",
            "effect": "EDI/MOE 可计算，但属于 prototype assumptions，正式论文需替换或论证外推规则。",
            "manual_review": True,
        })
    if pop_review:
        errors.append({
            "status": "degraded_but_continued",
            "stage": "人口匹配",
            "issue": "部分状态单元未能同省同年匹配人口，使用最近年份或标记缺失。",
            "effect": "人口加权风险 proxy 对未匹配单元为空或依赖回退年份。",
            "manual_review": True,
        })
    errors.append({
        "status": "degraded_but_continued",
        "stage": "BMDL 参数化",
        "issue": "P1/P5/P95/P99 与敏感/不敏感人群命名方向存在歧义。",
        "effect": "保留情景值并使用 lognormal 近似作为原型，不作为最终毒理学结论。",
        "manual_review": True,
    })

    dqn_ready = True
    dqn_blockers = []
    if pop_unmatched > 0:
        dqn_blockers.append("仍存在人口未匹配状态单元，人口加权 reward 需人工复核或补齐。")
    if cons_review > 0:
        dqn_blockers.append("消费量对 2023-2024 采用同省最近年份回退，正式 reward 前需确认可接受性。")
    dqn_blockers.append("仍未接入预算、产能、抽检成本、处置/召回损失、动作空间和约束参数。")
    dqn_ready = False

    report = f"""# PEANUT MOE/EDI 外部参数匹配与风险度量准备报告

## 1. 本轮任务目的

本轮在不运行 DQN 的前提下，基于修复后的 AFB1 浓度清洗表、计数面板和 belief-MDP 状态特征表，接入消费量、人口、体重和 BMDL prototype 参数，构建 EDI/MOE 风险度量数据基础，并判断是否具备进入最小 belief-MDP / DQN prototype 的条件。

## 2. 输入文件

- 浓度清洗表：`{inputs['concentration'].as_posix()}`
- 浓度分布摘要：`{inputs['distribution'].as_posix()}`
- 计数面板：`{inputs['count_panel'].as_posix()}`
- Beta-Binomial belief states：`{inputs['belief_states'].as_posix()}`
- belief-MDP 状态特征：`{inputs['state_features'].as_posix()}`
- 上轮 DQN 前置判断：`{inputs['readiness_after_repair'].as_posix()}`
- 消费量文件：`{inputs['consumption_raw'].as_posix()}`
- 人口文件：`{inputs['population_raw'].as_posix()}`

## 3. 消费量文件读取与字段识别

消费量文件读取成功，共 `{len(consumption_raw)}` 行。识别字段包括 `Province`、`MonitorngYear`、`Consumption_g_day`、`BodyWeight (kg)`、`SampleCount`、`Mean_concentration_MP(ug/kg)` 等。原始消费量单位为 `g/day`，已转换为 `kg/day = g/day / 1000`。

原始文件未提供 P95 或高消费量字段，因此本轮消费量参数表保留 P95/高消费量为空，并将该点标记为后续人工复核事项。

## 4. 人口文件读取与字段识别

人口文件读取成功，共 `{len(population_raw)}` 行。识别字段包括 `Province`、`MonitoringYear`、`population`。该表为长表结构。人口原始值按中国省级人口量级推断为“万人”，并同步生成 `人口数_人 = population * 10000`。

## 5. 匹配规则

消费量匹配规则：

1. 优先按省份规范化名称 + 同年匹配。
2. 若面板年份不在消费量表中，使用同省最近年份。
3. 若省份无法匹配，使用全国中位数默认值，并标记低置信度和人工复核。

人口匹配规则：

1. 优先按省份规范化名称 + 同年匹配。
2. 若年份不完全一致，使用同省最近年份。
3. 若无法匹配，保留缺失并记录清单。

## 6. 匹配质量

- belief-MDP 状态单元总数：`{total_units}`
- 消费量任意规则成功匹配单元数：`{cons_success_any}`
- 消费量同省同年匹配单元数：`{cons_success_exact}`
- 消费量建议人工复核单元数：`{cons_review}`
- 人口成功匹配单元数：`{pop_success}`
- 人口未匹配单元数：`{pop_unmatched}`
- 人口建议人工复核单元数：`{pop_review}`

人口未匹配省份/年份清单：

{unmatched_pop.to_markdown(index=False) if not unmatched_pop.empty else '无。'}

## 7. 体重参数

体重统一设定为 `{BODY_WEIGHT_KG}` kg bw。

## 8. BMDL 参数

BMDL 来源为用户提供截图中的 QIVIVE predicted BMDL10 based on HCC。本轮仅作为 MOE/EDI prototype 参数，不能作为最终毒理学结论。正式论文需补充可引用文献或原始来源。

情景参数：

- low BMDL：`0.050 μg/kg bw`
- sensitive BMDL：`0.066 μg/kg bw`
- default BMDL：`0.105 μg/kg bw`
- high BMDL：`0.158 μg/kg bw`
- upper BMDL：`0.189 μg/kg bw`
- MOE cutoff：`{MOE_CUTOFF}`

## 9. BMDL lognormal 或情景参数构建逻辑

以 default BMDL `0.105 μg/kg bw` 作为默认中心值。由于截图中的 P1/P5/P95/P99 与 sensitive/less sensitive 命名方向存在歧义，本轮不强行解释为普通统计分位数；配置文件保留所有情景点，并按低/高端点成对估计 lognormal 的近似 sigma，同时保留五个情景值供敏感性分析。该近似仅供原型风险度量准备。

## 10. EDI 计算逻辑

使用 AFB1 最终采用浓度，优先解释为 `μg/kg food`。消费量已转为 `kg/day`。计算公式：

`EDI = AFB1浓度(μg/kg food) × 消费量(kg/day) / 体重(kg bw)`

输出 EDI 单位为 `μg/kg bw/day`。

## 11. MOE 计算逻辑

`MOE = BMDL / EDI`

已按多个 BMDL 情景计算 `MOE_low_bmdl`、`MOE_sensitive_bmdl`、`MOE_default_bmdl`、`MOE_high_bmdl`、`MOE_upper_bmdl`，并以 cutoff `{MOE_CUTOFF}` 生成 `是否低于MOE阈值`、`MOE风险等级` 和 `MOE风险惩罚项`。

## 12. 当前结果是否可用于正式论文

当前结果适合作为 PEANUT 风险监管 workflow 的 prototype 数据基础，不建议直接作为正式论文结论。主要原因是消费量年份回退、BMDL 来源仍需正式可引用文献、P95/高消费量字段缺失，以及 reward 所需预算/成本/产能/召回损失等外部参数尚未接入。

## 13. Prototype assumptions

- 体重固定为 60 kg bw。
- 消费量使用平均消费量，缺少高消费量/P95 场景。
- 2023-2024 状态使用消费量同省最近年份回退。
- BMDL 情景值来自用户截图，lognormal 仅为近似。
- 人口单位推断为万人。

## 14. 当前是否可以进入 DQN prototype

当前仍不建议进入正式 DQN。本轮已经具备最小 belief-MDP 状态特征扩展和 EDI/MOE reward proxy 的雏形，但 DQN 仍缺动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

若只做最小 DQN prototype，建议状态可使用：belief posterior 均值/方差、抽检覆盖强度、AFB1 记录覆盖强度、浓度可用率、EDI/MOE 汇总特征、低于 MOE cutoff 比例、人口加权风险 proxy、MOE 风险惩罚 proxy。动作可先设为省份-环节抽检强度档位；reward 可使用风险惩罚下降、人口加权风险下降、抽检成本惩罚的线性组合；约束应至少包括预算和产能。

当前阻塞项：

{chr(10).join('- ' + x for x in dqn_blockers)}

## 15. 上游核验摘要

```json
{json.dumps(upstream_checks, ensure_ascii=False, indent=2)}
```

## 16. 下一步建议

先补齐或确认 DQN/MDP 必需外部参数：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重，并确认消费量最近年份回退和 BMDL 情景参数是否可作为论文前分析假设。
"""
    report_path = REPORT_DIR / "peanut_moe_edi_external_parameter_matching_report.md"
    report_path.write_text(report, encoding="utf-8")
    shutil.copy2(report_path, OUT_DIR / "reports" / report_path.name)

    error_log = "# PEANUT MOE/EDI 错误、降级与假设日志\n\n"
    error_log += "本轮未发现导致任务停止的核心输入读取错误。以下为自动修复、降级继续或需要后续人工复核的问题。\n\n"
    for i, e in enumerate(errors, start=1):
        error_log += f"## {i}. {e['stage']}\n\n"
        error_log += f"- 状态：{e['status']}\n"
        error_log += f"- 问题：{e['issue']}\n"
        error_log += f"- 影响：{e['effect']}\n"
        error_log += f"- 是否需要人工复核：{e['manual_review']}\n\n"
    error_path = REPORT_DIR / "peanut_moe_edi_error_log.md"
    error_path.write_text(error_log, encoding="utf-8")
    shutil.copy2(error_path, OUT_DIR / "logs" / error_path.name)

    readiness = f"""# DQN 前置状态判断：MOE/EDI 外部参数接入后

1. 消费量数据是否读取成功：成功，文件 `{inputs['consumption_raw'].name}`，共 `{len(consumption_raw)}` 行。
2. 人口数据是否读取成功：成功，文件 `{inputs['population_raw'].name}`，共 `{len(population_raw)}` 行。
3. 消费量匹配质量：任意规则成功 `{cons_success_any}/{total_units}`；同省同年 `{cons_success_exact}/{total_units}`；因年份回退或默认值建议复核 `{cons_review}` 个状态单元。
4. 人口匹配质量：成功 `{pop_success}/{total_units}`；未匹配 `{pop_unmatched}`。
5. EDI 是否可计算：可计算，输出 `{risk_table_path.as_posix()}`，记录数 `{len(risk_table)}`。
6. MOE 是否可计算：可计算，已按 5 个 BMDL 情景生成 MOE。
7. BMDL lognormal 或情景参数是否已配置：已配置，见 `{bmdl_path.as_posix()}`；lognormal 为 prototype 近似，不作最终毒理学结论。
8. belief-MDP 状态特征是否已加入 MOE/EDI：已加入，见 `{state_ext_path.as_posix()}`。
9. 当前是否可以进入最小 DQN prototype：暂不建议正式进入；若仅做 sandbox prototype，可基于新增风险 proxy 设计环境，但仍缺关键动作、成本、预算和约束参数。
10. 如果仍不能进入，缺什么：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重，以及正式 BMDL 文献来源/消费量高分位参数确认。
11. 如果未来进入 DQN prototype，建议：
    - 状态：belief posterior、覆盖强度、浓度可用率、EDI/MOE 汇总、低于 cutoff 比例、人口加权风险 proxy、MOE 惩罚 proxy。
    - 动作：省份-环节抽检强度档位、专项抽检投放、复检/召回触发档位。
    - reward：风险下降收益 - 抽检成本 - 处置成本 - 约束违约惩罚。
    - 约束：预算、检测能力、区域最低覆盖、重点风险区域优先级。
"""
    readiness_path = REPORT_DIR / "peanut_pre_dqn_readiness_after_moe_edi.md"
    readiness_path.write_text(readiness, encoding="utf-8")
    shutil.copy2(readiness_path, OUT_DIR / "reports" / readiness_path.name)

    readme = f"""# {TASK_NAME}

## 任务名称

MOE/EDI 外部参数匹配与风险度量准备

## 执行日期

{RUN_DATE}

## 输入文件

- `{inputs['concentration'].as_posix()}`
- `{inputs['distribution'].as_posix()}`
- `{inputs['count_panel'].as_posix()}`
- `{inputs['belief_states'].as_posix()}`
- `{inputs['state_features'].as_posix()}`
- `{inputs['consumption_raw'].as_posix()}`
- `{inputs['population_raw'].as_posix()}`

## 输出文件

- `data/peanut_edi_moe_risk_table.csv`
- `data/peanut_belief_mdp_state_features_with_moe_edi.csv`
- `tables/peanut_consumption_parameter_table.csv`
- `tables/peanut_population_parameter_table.csv`
- `tables/peanut_edi_moe_risk_summary.csv`
- `configs/peanut_bmdl_parameter_config.json`
- `tables/peanut_bmdl_parameter_table.csv`
- `reports/peanut_moe_edi_external_parameter_matching_report.md`
- `reports/peanut_pre_dqn_readiness_after_moe_edi.md`
- `logs/peanut_moe_edi_error_log.md`
- `figures/*.svg`

## 关键参数

- 体重：{BODY_WEIGHT_KG} kg bw
- BMDL default：0.105 μg/kg bw
- BMDL scenarios：0.050, 0.066, 0.105, 0.158, 0.189 μg/kg bw
- MOE cutoff：{MOE_CUTOFF}

## 匹配结果

- 消费量任意规则成功匹配：{cons_success_any}/{total_units}
- 消费量同省同年匹配：{cons_success_exact}/{total_units}
- 人口成功匹配：{pop_success}/{total_units}
- 人口未匹配：{pop_unmatched}/{total_units}

## 未解决问题

- 消费量未覆盖 2023-2024，主要使用同省最近年份回退。
- 消费量文件未提供 P95/高消费量字段。
- BMDL 参数来自用户截图，正式论文需补充可引用来源。
- DQN 仍缺动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

## 下一步建议

补齐 DQN/MDP 外部约束和成本参数，并确认消费量/BMDL prototype 假设是否可作为后续最小环境输入。
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    # Project state updates.
    long_rule = "每个实质性任务必须创建 `outputs/YYYYMMDD_中文任务名/` 独立输出目录，并将关键结果、报告、图表、日志和 README 同步整理到该目录。"
    updates = {
        ROOT / "project_state" / "current_focus.md": f"# Current Focus\n\n当前继续 PEANUT 项目，但不进入 DQN。本轮已完成 MOE/EDI 外部参数接入、消费量/人口匹配、BMDL prototype 参数化和 belief-MDP 状态特征扩展；下一步应补齐 DQN/MDP 动作、预算、产能、抽检成本、处置/召回损失和约束参数。\n\n长期输出规则：{long_rule}\n",
        ROOT / "project_state" / "next_step.md": "# Next Step\n\n不要运行 DQN。下一步先补齐或确认最小 belief-MDP / DQN prototype 所需外部参数：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重、约束条件，并确认消费量最近年份回退和 BMDL 情景参数是否可接受。\n",
        ROOT / "project_state" / "conversation_handoff.md": f"# Conversation Handoff\n\n{RUN_DATE} 已完成 PEANUT MOE/EDI 外部参数匹配与风险度量准备。关键输出在 `{OUT_DIR.relative_to(ROOT).as_posix()}/`，标准目录同步输出在 `data/04_feature/` 和 `reports/`。DQN 未运行。当前仍不建议正式进入 DQN，因为缺动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。\n\n长期输出规则：{long_rule}\n",
        ROOT / "project_state" / "run_protocol.md": f"# Run Protocol\n\n- 启动任何实质性科研任务前，先读取项目状态、AGENTS.md、相关 references 和上游输出。\n- 下游 MOE/EDI、belief-MDP、POMDP 或 DQN 前必须先核验上游输出。\n- 不得修改 `data/01_raw`。\n- {long_rule}\n",
    }
    for p, text in updates.items():
        p.write_text(text, encoding="utf-8")

    append_entries = {
        ROOT / "project_state" / "changelog.md": f"\n## {RUN_DATE}\n\n- 新增 Run Output Directory Policy 到 `AGENTS.md`。\n- 创建 `{OUT_DIR.relative_to(ROOT).as_posix()}/` 并同步整理本轮 MOE/EDI 关键输出、报告、图表、日志和 README。\n- 生成 BMDL 参数配置、消费量参数表、人口参数表、EDI/MOE 风险表、风险摘要和加入 MOE/EDI 的 belief-MDP 状态特征表。\n- 重新生成 DQN 前置判断报告；本轮未运行 DQN。\n",
        ROOT / "project_state" / "decision_log.md": f"\n## {RUN_DATE}\n\n### Adopt task-specific output directories for substantive research tasks\n\nRationale: 用户要求每轮实质性科研任务都有独立、可追踪、中文命名的输出目录，便于查找关键结果、报告、图表、日志和 README。\n\nImpact: 后续任务必须创建 `outputs/YYYYMMDD_中文任务名/`，标准目录继续保留，但关键产物需同步复制到任务目录。\n\n### Use MOE/EDI prototype parameters before DQN\n\nRationale: 当前 DQN 仍缺动作、预算、成本和约束参数，但已有消费量、人口、体重和 BMDL 情景值可以先构建风险度量基础。\n\nImpact: `peanut_belief_mdp_state_features_with_moe_edi.csv` 可作为后续最小 belief-MDP 环境设计输入；正式 DQN 仍需等待外部约束参数补齐。\n",
        ROOT / "project_state" / "lessons_learned.md": f"\n## {RUN_DATE}\n\n- 消费量数据与监管面板年份不一致时，可用同省最近年份作为 prototype 回退，但必须标记人工复核，不能作为正式论文结论直接使用。\n- 省级人口英文长表可通过省份中英文映射、同年优先和最近年份回退接入 belief-MDP 状态特征。\n- 截图给出的 BMDL P1/P5/P95/P99 若与敏感性命名方向存在歧义，应保留情景值并记录歧义，避免强行解释为普通统计分位数。\n- {long_rule}\n",
        ROOT / "project_state" / "project_memory.md": f"\n## {RUN_DATE} PEANUT MOE/EDI memory\n\n- {long_rule}\n- PEANUT 当前已有 MOE/EDI 风险度量基础：消费量、人口、60 kg 体重、BMDL 情景和风险 proxy 已接入 belief-MDP 状态特征。\n- 当前不要进入正式 DQN；仍需动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。\n",
    }
    for p, text in append_entries.items():
        with p.open("a", encoding="utf-8") as f:
            f.write(text)

    print(json.dumps({
        "out_dir": str(OUT_DIR),
        "risk_table_rows": len(risk_table),
        "risk_summary_rows": len(summary),
        "state_rows": len(state_ext),
        "consumption_any_match": cons_success_any,
        "consumption_exact_match": cons_success_exact,
        "population_success": pop_success,
        "population_unmatched": pop_unmatched,
        "dqn_ready": dqn_ready,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
