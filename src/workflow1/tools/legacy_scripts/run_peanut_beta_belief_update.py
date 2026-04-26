from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "data/04_feature/peanut_count_panel.csv"
OUT_DIR = ROOT / "data/04_feature"
REPORT_DIR = ROOT / "reports"
TABLE_DIR = ROOT / "reports/tables"
STATE_DIR = ROOT / "project_state"


CONFIG = {
    "prior_alpha": 1.0,
    "prior_beta": 1.0,
    "forgetting_factor": 0.95,
    "time_unit": "month",
    "tracks": {
        "overall_noncompliance": {
            "success_column": "不合格批次数",
            "trial_column": "抽检总批次数",
            "meaning": "省份-时间-供应链环节层面的总体不合格概率",
        },
        "afb1_noncompliance_all_samples": {
            "success_column": "AFB1相关不合格批次数",
            "trial_column": "抽检总批次数",
            "meaning": "以全部抽检批次为分母的 AFB1 相关不合格概率",
        },
        "afb1_noncompliance_conditional": {
            "success_column": "AFB1相关不合格批次数",
            "trial_column": "AFB1相关记录数",
            "meaning": "在 AFB1 相关记录中不合格的条件概率；当分母为0时不更新，仅传播遗忘先验",
        },
    },
}


def ensure_dirs() -> None:
    for p in [OUT_DIR, REPORT_DIR, TABLE_DIR, STATE_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def to_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def md_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "无记录。"
    small = df.head(max_rows).copy()
    small = small.astype(object).where(pd.notna(small), "")
    cols = [str(c) for c in small.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in small.iterrows():
        vals = [str(row[c]).replace("\n", " ").replace("|", "/")[:240] for c in small.columns]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def beta_variance(alpha: float, beta: float) -> float:
    total = alpha + beta
    if total <= 0:
        return np.nan
    return alpha * beta / (total * total * (total + 1.0))


def normal_approx_interval(mean: float, variance: float, z: float = 1.96) -> tuple[float, float]:
    if pd.isna(mean) or pd.isna(variance):
        return np.nan, np.nan
    sd = math.sqrt(max(float(variance), 0.0))
    return max(0.0, mean - z * sd), min(1.0, mean + z * sd)


def update_track(panel: pd.DataFrame, success_col: str, trial_col: str, prefix: str) -> pd.DataFrame:
    alpha0 = CONFIG["prior_alpha"]
    beta0 = CONFIG["prior_beta"]
    lam = CONFIG["forgetting_factor"]
    rows = []
    sort_cols = ["省份", "供应链环节", "年份", "月份", "年月"]
    ordered = panel.sort_values(sort_cols).copy()
    for (province, stage), g in ordered.groupby(["省份", "供应链环节"], dropna=False, sort=False):
        alpha_prior = alpha0
        beta_prior = beta0
        previous_mean = np.nan
        for _, r in g.iterrows():
            n_raw = r.get(trial_col, 0)
            y_raw = r.get(success_col, 0)
            n = 0 if pd.isna(n_raw) else int(max(0, n_raw))
            y = 0 if pd.isna(y_raw) else int(max(0, y_raw))
            y = min(y, n)

            prior_mean = alpha_prior / (alpha_prior + beta_prior)
            prior_var = beta_variance(alpha_prior, beta_prior)
            prior_lo, prior_hi = normal_approx_interval(prior_mean, prior_var)

            if n > 0:
                alpha_post = alpha_prior + y
                beta_post = beta_prior + n - y
                updated = True
            else:
                alpha_post = alpha_prior
                beta_post = beta_prior
                updated = False
            post_mean = alpha_post / (alpha_post + beta_post)
            post_var = beta_variance(alpha_post, beta_post)
            post_lo, post_hi = normal_approx_interval(post_mean, post_var)
            observed_rate = y / n if n > 0 else np.nan
            delta = post_mean - previous_mean if pd.notna(previous_mean) else np.nan

            strength = alpha_post + beta_post
            if post_mean >= 0.10:
                level = "高"
            elif post_mean >= 0.03:
                level = "中"
            elif post_mean >= 0.01:
                level = "低"
            else:
                level = "极低"
            uncertainty = "高" if post_var >= 0.0025 or strength < 20 else ("中" if post_var >= 0.0005 or strength < 80 else "低")

            rows.append(
                {
                    "省份": province,
                    "供应链环节": stage,
                    "年份": r["年份"],
                    "月份": r["月份"],
                    "年月": r["年月"],
                    f"{prefix}_观测成功数": y,
                    f"{prefix}_观测试验数": n,
                    f"{prefix}_观测率": observed_rate,
                    f"{prefix}_先验alpha": alpha_prior,
                    f"{prefix}_先验beta": beta_prior,
                    f"{prefix}_先验均值": prior_mean,
                    f"{prefix}_先验方差": prior_var,
                    f"{prefix}_先验95下限_正态近似": prior_lo,
                    f"{prefix}_先验95上限_正态近似": prior_hi,
                    f"{prefix}_后验alpha": alpha_post,
                    f"{prefix}_后验beta": beta_post,
                    f"{prefix}_后验均值": post_mean,
                    f"{prefix}_后验方差": post_var,
                    f"{prefix}_后验标准差": math.sqrt(max(post_var, 0.0)),
                    f"{prefix}_后验95下限_正态近似": post_lo,
                    f"{prefix}_后验95上限_正态近似": post_hi,
                    f"{prefix}_后验强度": strength,
                    f"{prefix}_风险等级_经验阈值": level,
                    f"{prefix}_不确定性等级": uncertainty,
                    f"{prefix}_较上期后验均值变化": delta,
                    f"{prefix}_本期是否更新": updated,
                }
            )

            alpha_prior = alpha0 + lam * (alpha_post - alpha0)
            beta_prior = beta0 + lam * (beta_post - beta0)
            previous_mean = post_mean
    return pd.DataFrame(rows)


def make_state_features(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    required = [
        "省份",
        "年份",
        "月份",
        "年月",
        "供应链环节",
        "抽检总批次数",
        "不合格批次数",
        "AFB1相关记录数",
        "AFB1相关不合格批次数",
        "浓度可用记录数",
    ]
    missing = [c for c in required if c not in panel.columns]
    if missing:
        raise RuntimeError("计数面板缺少核心字段：" + "、".join(missing))

    p = panel.copy()
    p["年份"] = pd.to_numeric(p["年份"], errors="coerce").astype("Int64")
    p["月份"] = pd.to_numeric(p["月份"], errors="coerce").astype("Int64")
    numeric_cols = [
        "抽检总批次数",
        "合格批次数",
        "不合格批次数",
        "AFB1相关记录数",
        "AFB1相关不合格批次数",
        "浓度可用记录数",
    ]
    for c in numeric_cols:
        if c in p.columns:
            p[c] = pd.to_numeric(p[c], errors="coerce").fillna(0).clip(lower=0)

    p["年月排序"] = p["年份"].astype(str) + "-" + p["月份"].astype(str).str.zfill(2)
    p = p.sort_values(["省份", "供应链环节", "年份", "月份", "年月"]).reset_index(drop=True)

    tracks = {}
    tracks["总体不合格"] = update_track(p, "不合格批次数", "抽检总批次数", "总体不合格")
    tracks["AFB1全样本不合格"] = update_track(p, "AFB1相关不合格批次数", "抽检总批次数", "AFB1全样本不合格")
    tracks["AFB1条件不合格"] = update_track(p, "AFB1相关不合格批次数", "AFB1相关记录数", "AFB1条件不合格")

    base_cols = ["省份", "供应链环节", "年份", "月份", "年月"]
    state = p.merge(tracks["总体不合格"], on=base_cols, how="left")
    state = state.merge(tracks["AFB1全样本不合格"], on=base_cols, how="left")
    state = state.merge(tracks["AFB1条件不合格"], on=base_cols, how="left")

    state["状态ID"] = (
        state["省份"].astype(str)
        + "|"
        + state["供应链环节"].astype(str)
        + "|"
        + state["年月"].astype(str)
    )
    state["时间步序号"] = state.groupby(["省份", "供应链环节"], dropna=False).cumcount() + 1
    state["样本覆盖强度"] = np.log1p(state["抽检总批次数"])
    state["AFB1记录覆盖强度"] = np.log1p(state["AFB1相关记录数"])
    state["浓度可用率"] = np.where(state["AFB1相关记录数"] > 0, state["浓度可用记录数"] / state["AFB1相关记录数"], np.nan)
    state["总体观测不合格率"] = np.where(state["抽检总批次数"] > 0, state["不合格批次数"] / state["抽检总批次数"], np.nan)
    state["AFB1全样本观测不合格率"] = np.where(state["抽检总批次数"] > 0, state["AFB1相关不合格批次数"] / state["抽检总批次数"], np.nan)
    state["AFB1条件观测不合格率"] = np.where(state["AFB1相关记录数"] > 0, state["AFB1相关不合格批次数"] / state["AFB1相关记录数"], np.nan)
    state["belief_mdp_state_vector_columns"] = (
        "总体不合格_后验alpha,总体不合格_后验beta,总体不合格_后验均值,总体不合格_后验方差,"
        "AFB1全样本不合格_后验alpha,AFB1全样本不合格_后验beta,AFB1全样本不合格_后验均值,AFB1全样本不合格_后验方差,"
        "AFB1条件不合格_后验alpha,AFB1条件不合格_后验beta,AFB1条件不合格_后验均值,AFB1条件不合格_后验方差,"
        "抽检总批次数,AFB1相关记录数,浓度可用记录数,样本覆盖强度,AFB1记录覆盖强度,浓度可用率"
    )

    meta = {
        "rows": int(len(state)),
        "groups": int(state.groupby(["省份", "供应链环节"], dropna=False).ngroups),
        "province_count": int(state["省份"].nunique(dropna=True)),
        "stage_count": int(state["供应链环节"].nunique(dropna=True)),
        "time_count": int(state["年月"].nunique(dropna=True)),
        "config": CONFIG,
    }
    return state, meta


def write_excel_if_possible(df: pd.DataFrame, path: Path, error_log: list[dict]) -> None:
    try:
        df.to_excel(path, index=False)
    except Exception as exc:
        error_log.append(
            {
                "status": "degraded_but_continued",
                "error_type": type(exc).__name__,
                "location": str(path),
                "message": str(exc),
                "repair": "XLSX 输出失败，保留 CSV 作为主输出。",
                "effect": "不影响核心数值结果；仅影响 Excel 格式可用性。",
                "manual_review": "否",
            }
        )


def update_project_state(meta: dict, outputs: list[str]) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    with (STATE_DIR / "changelog.md").open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {today}\n\n"
            "- 基于 `data/04_feature/peanut_count_panel.csv` 实现 Beta-Binomial 信念更新原型，生成 belief-MDP 状态特征表、最新状态表、汇总表、配置和技术报告。\n"
        )
    with (STATE_DIR / "decision_log.md").open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {today}\n\n"
            "### Use Beta(1,1) prior and 0.95 forgetting factor for the first PEANUT belief-update prototype\n\n"
            "Rationale: 当前用户要求实现 Beta-Binomial 信念更新原型，但尚未提供外部先验强度或遗忘因子。Beta(1,1) 是弱信息先验，0.95 遗忘因子可保留历史信息同时允许月度风险变化。\n\n"
            "Impact: 输出状态特征表可直接作为 belief-MDP 原型输入；后续如获得专家先验或校准参数，可重跑并替换 `prior_alpha`、`prior_beta` 和 `forgetting_factor`。\n"
        )
    with (STATE_DIR / "lessons_learned.md").open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {today} Beta-Binomial Belief Update Lessons\n\n"
            "- 在没有专家先验时，可用 Beta(1,1) 作为弱信息先验启动原型，但必须在报告中标记为可调整假设。\n"
            "- 对 AFB1 风险建议同时保留“全样本分母”和“AFB1相关记录条件分母”两条信念轨道，便于后续监管目标在检出概率与条件严重性之间切换。\n"
            "- belief-MDP 状态表应保留 alpha、beta、后验均值、后验方差、样本覆盖强度和浓度可用率，以同时表达风险水平与不确定性。\n"
        )
    next_step = (
        "# Next Step\n\n"
        "基于 `data/04_feature/peanut_belief_mdp_state_features.csv` 设计最小 belief-MDP 环境：定义动作档位、预算/产能约束、奖励函数中的抽检成本、处置/召回损失、信息价值权重，并补充 MOE/EDI 所需消费量、人口、体重和 BMDL 参数。\n"
    )
    write_text(STATE_DIR / "next_step.md", next_step)
    handoff = (
        "# Conversation Handoff\n\n"
        "## 当前状态\n\n"
        "已基于 `data/04_feature/peanut_count_panel.csv` 完成 Beta-Binomial 信念更新原型，并生成可用于后续 belief-MDP 的状态特征表。\n\n"
        "## 核心假设\n\n"
        f"- 弱信息先验：Beta({CONFIG['prior_alpha']}, {CONFIG['prior_beta']})。\n"
        f"- 月度遗忘因子：{CONFIG['forgetting_factor']}。\n"
        "- 同时构建总体不合格、AFB1 全样本不合格、AFB1 条件不合格三条信念轨道。\n\n"
        "## 核心输出\n\n"
        + "\n".join(f"- `{o}`" for o in outputs)
        + "\n\n## 下一步建议\n\n"
        "下一步应设计最小 belief-MDP 环境，补充动作、预算、产能、成本、召回损失、信息价值权重，以及 MOE/EDI 所需消费量、人口、体重和 BMDL 参数。\n\n"
        "## 新对话继续 Prompt\n\n"
        "请继续 PEANUT 项目。先读取 `data/04_feature/peanut_belief_mdp_state_features.csv`、`reports/peanut_beta_binomial_belief_update_report.md` 和 `project_state/next_step.md`，在不修改 `data/01_raw` 的前提下，设计最小 belief-MDP 环境的状态、动作、约束与奖励函数参数需求。\n"
    )
    write_text(STATE_DIR / "conversation_handoff.md", handoff)


def main() -> int:
    ensure_dirs()
    error_log: list[dict] = []
    if not PANEL_PATH.exists():
        raise FileNotFoundError("缺少计数面板：data/04_feature/peanut_count_panel.csv")

    try:
        panel = pd.read_csv(PANEL_PATH)
    except UnicodeDecodeError:
        panel = pd.read_csv(PANEL_PATH, encoding="utf-8-sig")
        error_log.append(
            {
                "status": "repaired",
                "error_type": "UnicodeDecodeError",
                "location": str(PANEL_PATH),
                "message": "默认编码读取失败",
                "repair": "改用 utf-8-sig 读取。",
                "effect": "不影响结果。",
                "manual_review": "否",
            }
        )

    state, meta = make_state_features(panel)
    belief_path = OUT_DIR / "peanut_beta_binomial_belief_states.csv"
    state_path = OUT_DIR / "peanut_belief_mdp_state_features.csv"
    latest_path = TABLE_DIR / "peanut_belief_state_latest.csv"
    summary_path = TABLE_DIR / "peanut_belief_state_summary_by_stage.csv"
    config_path = OUT_DIR / "peanut_beta_binomial_config.json"
    xlsx_path = OUT_DIR / "peanut_belief_mdp_state_features.xlsx"

    to_csv(state, belief_path)
    to_csv(state, state_path)
    write_excel_if_possible(state, xlsx_path, error_log)
    config_path.write_text(json.dumps(CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")

    latest_idx = state.sort_values(["省份", "供应链环节", "年份", "月份"]).groupby(["省份", "供应链环节"], dropna=False).tail(1).index
    latest = state.loc[latest_idx].sort_values(["AFB1全样本不合格_后验均值", "总体不合格_后验均值"], ascending=False)
    to_csv(latest, latest_path)

    summary = state.groupby("供应链环节", dropna=False).agg(
        状态行数=("状态ID", "count"),
        省份数=("省份", "nunique"),
        抽检总批次数=("抽检总批次数", "sum"),
        不合格批次数=("不合格批次数", "sum"),
        AFB1相关记录数=("AFB1相关记录数", "sum"),
        AFB1相关不合格批次数=("AFB1相关不合格批次数", "sum"),
        平均总体后验风险=("总体不合格_后验均值", "mean"),
        平均AFB1全样本后验风险=("AFB1全样本不合格_后验均值", "mean"),
        平均AFB1条件后验风险=("AFB1条件不合格_后验均值", "mean"),
        平均总体后验方差=("总体不合格_后验方差", "mean"),
        平均AFB1全样本后验方差=("AFB1全样本不合格_后验方差", "mean"),
    ).reset_index()
    to_csv(summary, summary_path)

    error_log_path = REPORT_DIR / "peanut_beta_binomial_error_log.md"
    if error_log:
        rows = [
            f"- 状态：{e['status']}；错误：{e['error_type']}；位置：`{e['location']}`；修复：{e['repair']}；影响：{e['effect']}；需人工复核：{e['manual_review']}"
            for e in error_log
        ]
        write_text(error_log_path, "# Beta-Binomial 信念更新错误日志\n\n## 已自动修复或降级处理\n\n" + "\n".join(rows) + "\n\n## 未解决错误\n\n无。\n")
    else:
        write_text(error_log_path, "# Beta-Binomial 信念更新错误日志\n\n## 已自动修复错误\n\n无。\n\n## 已降级处理错误\n\n无。\n\n## 未解决且需要用户处理的错误\n\n无。\n")

    report = f"""# PEANUT Beta-Binomial 信念更新原型报告

## 输入

- 计数面板：`data/04_feature/peanut_count_panel.csv`
- 面板行数：{len(panel)}
- 输出状态行数：{meta['rows']}
- 省份数：{meta['province_count']}
- 供应链环节数：{meta['stage_count']}
- 时间点数：{meta['time_count']}

## 方法

本轮实现 Beta-Binomial 共轭信念更新原型。对每个 `省份 × 供应链环节` 按年月排序，逐期读取观测计数，并维护 Beta 分布参数。

默认先验为 `Beta({CONFIG['prior_alpha']}, {CONFIG['prior_beta']})`。这是弱信息先验，用于在没有专家先验或历史校准参数时启动原型。

跨期传播采用遗忘因子 `{CONFIG['forgetting_factor']}`：

```text
alpha_next = alpha0 + lambda * (alpha_post - alpha0)
beta_next  = beta0  + lambda * (beta_post  - beta0)
```

该设定保留历史抽检信息，同时允许月度风险随季节、供应链条件或监管响应变化。

## 信念轨道

1. `总体不合格`：成功数为 `不合格批次数`，试验数为 `抽检总批次数`。
2. `AFB1全样本不合格`：成功数为 `AFB1相关不合格批次数`，试验数为 `抽检总批次数`。
3. `AFB1条件不合格`：成功数为 `AFB1相关不合格批次数`，试验数为 `AFB1相关记录数`；当 AFB1 相关记录数为 0 时，本期不更新，仅传播既有信念。

## belief-MDP 状态特征

状态表保留以下核心特征：

- 索引：`状态ID`、`省份`、`供应链环节`、`年份`、`月份`、`年月`、`时间步序号`
- 观测：`抽检总批次数`、`不合格批次数`、`AFB1相关记录数`、`AFB1相关不合格批次数`、`浓度可用记录数`
- 信念：三条轨道的先验/后验 `alpha`、`beta`、均值、方差、标准差、近似 95% 区间
- 派生：`样本覆盖强度`、`AFB1记录覆盖强度`、`浓度可用率`、观测率、风险等级、不确定性等级

## 供应链环节摘要

{md_table(summary, 20)}

## 最新状态 Top 20（按 AFB1 全样本后验风险）

{md_table(latest[['省份','供应链环节','年月','抽检总批次数','AFB1相关记录数','AFB1相关不合格批次数','总体不合格_后验均值','AFB1全样本不合格_后验均值','AFB1条件不合格_后验均值','AFB1全样本不合格_不确定性等级']].head(20), 20)}

## 输出文件

- `data/04_feature/peanut_beta_binomial_belief_states.csv`
- `data/04_feature/peanut_belief_mdp_state_features.csv`
- `data/04_feature/peanut_belief_mdp_state_features.xlsx`
- `data/04_feature/peanut_beta_binomial_config.json`
- `reports/tables/peanut_belief_state_latest.csv`
- `reports/tables/peanut_belief_state_summary_by_stage.csv`
- `reports/peanut_beta_binomial_belief_update_report.md`
- `reports/peanut_beta_binomial_error_log.md`

## 限制与下一步

- 当前先验和遗忘因子是原型假设，后续可用专家意见、历史数据或交叉验证校准。
- 该状态表尚未包含预算、产能、抽检成本、处置/召回损失、消费量、人口、体重和 BMDL，因此还不能直接训练 DQN。
- 下一步应定义 belief-MDP 的动作档位、硬约束和奖励函数，并补齐 MOE/EDI 外部参数。
"""
    report_path = REPORT_DIR / "peanut_beta_binomial_belief_update_report.md"
    write_text(report_path, report)

    outputs = [
        belief_path.relative_to(ROOT).as_posix(),
        state_path.relative_to(ROOT).as_posix(),
        xlsx_path.relative_to(ROOT).as_posix() if xlsx_path.exists() else "",
        config_path.relative_to(ROOT).as_posix(),
        latest_path.relative_to(ROOT).as_posix(),
        summary_path.relative_to(ROOT).as_posix(),
        report_path.relative_to(ROOT).as_posix(),
        error_log_path.relative_to(ROOT).as_posix(),
    ]
    outputs = [o for o in outputs if o]
    update_project_state(meta, outputs)

    run_summary = {"meta": meta, "outputs": outputs, "error_count": len(error_log)}
    write_text(REPORT_DIR / "peanut_beta_binomial_run_summary.json", json.dumps(run_summary, ensure_ascii=False, indent=2))
    print(json.dumps(run_summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        ensure_dirs()
        err = f"""# Beta-Binomial 信念更新错误日志

## 未解决且需要用户处理的错误

- 错误类型：`{type(exc).__name__}`
- 错误位置：`scripts/run_peanut_beta_belief_update.py`
- 错误信息：{exc}

## 已尝试的自动修复

脚本内置了编码降级读取、XLSX 输出失败时保留 CSV、目录自动创建、Markdown 表格内置渲染等轻量修复策略。当前错误属于核心输入或核心字段问题，无法可靠自动修复。
"""
        write_text(REPORT_DIR / "peanut_beta_binomial_error_log.md", err)
        print(err, file=sys.stderr)
        raise
