from __future__ import annotations

import json
import math
import random
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[4]
RUN_DIR = ROOT / "outputs" / "工作包" / "20260425_1132_DQN初步运行"
DATA_DIR = RUN_DIR / "01_数据输出"
TABLE_DIR = RUN_DIR / "02_表格输出"
REPORT_DIR = RUN_DIR / "04_报告输出"
MODEL_DIR = RUN_DIR / "05_模型与实验"
CONFIG_DIR = RUN_DIR / "06_配置参数"
LOG_DIR = RUN_DIR / "07_日志与错误"

SEED = 20260425
random.seed(SEED)
np.random.seed(SEED)


INPUTS = {
    "cleaned_dataset": ROOT / "data" / "03_primary" / "peanut_cleaned_analysis_ready.csv",
    "concentration_table": ROOT / "data" / "04_feature" / "peanut_concentration_clean_table.csv",
    "count_panel": ROOT / "data" / "04_feature" / "peanut_count_panel.csv",
    "beta_binomial_states": ROOT / "data" / "04_feature" / "peanut_beta_binomial_belief_states.csv",
    "belief_mdp_features_with_moe_edi": ROOT / "data" / "04_feature" / "peanut_belief_mdp_state_features_with_moe_edi.csv",
    "edi_moe_risk_table": ROOT / "data" / "04_feature" / "peanut_edi_moe_risk_table.csv",
}


FEATURE_COLUMNS = [
    "抽检总批次数",
    "AFB1相关记录数",
    "浓度可用记录数",
    "总体不合格_后验均值",
    "总体不合格_后验方差",
    "AFB1全样本不合格_后验均值",
    "AFB1条件不合格_后验均值",
    "样本覆盖强度",
    "AFB1记录覆盖强度",
    "浓度可用率",
    "EDI均值",
    "EDI_P95",
    "MOE_default_均值",
    "低于MOE阈值比例",
    "人口加权风险_proxy",
    "MOE风险惩罚_proxy",
]

ACTIONS = {
    0: {"name": "维持/不加码", "inspection_units": 0, "cost": 0.0, "risk_reduction": 0.00, "info_gain": 0.00},
    1: {"name": "常规加密抽检", "inspection_units": 1, "cost": 0.25, "risk_reduction": 0.08, "info_gain": 0.08},
    2: {"name": "重点专项抽检", "inspection_units": 2, "cost": 0.70, "risk_reduction": 0.16, "info_gain": 0.16},
}

ASSUMPTIONS = {
    "prototype_scope": "sandbox_only_not_formal_policy",
    "algorithm": "Fitted Q iteration with sklearn MLPRegressor as a lightweight DQN-style function approximator; torch is not installed.",
    "action_space": ACTIONS,
    "reward": "10 * action_risk_reduction_on_risk_proxy + 1.5 * uncertainty_reduction - temporary_low_action_cost - 2 * constraint_proxy",
    "discount_gamma": 0.85,
    "fqi_iterations": 12,
    "formal_blockers": [
        "正式动作空间未确认：省份-环节抽检批次数、复检、召回/处置触发档位尚未参数化。",
        "缺少正式预算、单次抽检成本、检测产能上限和区域最低覆盖约束。",
        "缺少处置/召回损失、信息价值权重、约束违约惩罚权重。",
        "BMDL 与消费量高分位等毒理/暴露参数仍有 prototype 或待复核字段。",
        "当前历史数据没有真实干预动作与动作后状态转移，无法做因果意义上的 off-policy DQN 评估。",
    ],
}


def ensure_dirs() -> None:
    for p in (DATA_DIR, TABLE_DIR, REPORT_DIR, MODEL_DIR, CONFIG_DIR, LOG_DIR):
        p.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def key_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in ["省份", "年份", "月份", "年月", "供应链环节"] if c in df.columns]


def upstream_audit() -> tuple[dict, pd.DataFrame]:
    rows = []
    loaded = {}
    for name, path in INPUTS.items():
        if not path.exists():
            rows.append({"检查项": name, "状态": "FAIL", "说明": f"缺少文件: {path}"})
            continue
        df = read_csv(path)
        loaded[name] = df
        rows.append({"检查项": name, "状态": "PASS", "说明": f"读取成功；行数={len(df)}；列数={len(df.columns)}"})

    if set(INPUTS) - set(loaded):
        return loaded, pd.DataFrame(rows)

    count_panel = loaded["count_panel"]
    belief = loaded["beta_binomial_states"]
    mdp = loaded["belief_mdp_features_with_moe_edi"]
    conc = loaded["concentration_table"]
    edi = loaded["edi_moe_risk_table"]

    for left_name, left_df, right_name, right_df in [
        ("count_panel", count_panel, "beta_binomial_states", belief),
        ("beta_binomial_states", belief, "belief_mdp_features_with_moe_edi", mdp),
    ]:
        keys = key_columns(left_df)
        if not keys:
            rows.append({"检查项": f"{left_name}_keys", "状态": "WARN", "说明": "未找到标准省份-年月-环节键"})
            continue
        left_keys = set(map(tuple, left_df[keys].astype(str).values))
        right_keys = set(map(tuple, right_df[keys].astype(str).values))
        missing = left_keys - right_keys
        extra = right_keys - left_keys
        status = "PASS" if not missing and not extra else "WARN"
        rows.append({
            "检查项": f"{left_name}_vs_{right_name}_keyset",
            "状态": status,
            "说明": f"左侧键={len(left_keys)}；右侧键={len(right_keys)}；右侧缺失={len(missing)}；右侧额外={len(extra)}",
        })

    afb1_count = int(pd.to_numeric(conc.get("是否AFB1相关", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    conc_available = int(pd.to_numeric(conc.get("最终采用浓度值", pd.Series(dtype=float)), errors="coerce").notna().sum())
    limit_available = int(pd.to_numeric(conc.get("法规限量_数值", pd.Series(dtype=float)), errors="coerce").notna().sum())
    manual_review = int(pd.to_numeric(conc.get("是否建议人工复核", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    rows.append({
        "检查项": "concentration_must_pass_summary",
        "状态": "PASS" if afb1_count > 0 and conc_available > 0 and limit_available > 0 else "FAIL",
        "说明": f"AFB1相关={afb1_count}；浓度可解析={conc_available}；限量可解析={limit_available}；人工复核={manual_review}",
    })

    moe_numeric = pd.to_numeric(edi.get("MOE_default_bmdl", pd.Series(dtype=float)), errors="coerce")
    rows.append({
        "检查项": "moe_edi_numeric",
        "状态": "PASS" if moe_numeric.notna().sum() > 0 else "FAIL",
        "说明": f"MOE default 可用记录={int(moe_numeric.notna().sum())}；EDI/MOE表行数={len(edi)}",
    })

    return loaded, pd.DataFrame(rows)


def prepare_states(mdp: pd.DataFrame) -> pd.DataFrame:
    df = mdp.copy()
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors="coerce")

    risk = pd.to_numeric(df["人口加权风险_proxy"], errors="coerce").fillna(0)
    moe_penalty = pd.to_numeric(df["MOE风险惩罚_proxy"], errors="coerce").fillna(0)
    low_moe_ratio = pd.to_numeric(df["低于MOE阈值比例"], errors="coerce").fillna(0)
    uncertainty = pd.to_numeric(df["总体不合格_后验方差"], errors="coerce").fillna(0)
    coverage_gap = 1.0 - pd.to_numeric(df["样本覆盖强度"], errors="coerce").fillna(0).clip(0, 1)

    df["dqn_risk_proxy"] = (
        risk.rank(pct=True).fillna(0)
        + moe_penalty.rank(pct=True).fillna(0)
        + low_moe_ratio.fillna(0).clip(0, 1)
        + uncertainty.rank(pct=True).fillna(0) * 0.5
    ) / 3.5
    df["dqn_uncertainty_proxy"] = uncertainty.rank(pct=True).fillna(0)
    df["dqn_coverage_gap_proxy"] = coverage_gap
    df["state_row_id"] = np.arange(len(df))
    return df


def build_transitions(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["省份", "供应链环节"]
    ordered = df.sort_values(keys + ["年月排序", "年份", "月份"]).reset_index(drop=True)
    ordered["next_state_row_id"] = ordered.groupby(keys)["state_row_id"].shift(-1)
    ordered["next_state_row_id"] = ordered["next_state_row_id"].fillna(ordered["state_row_id"]).astype(int)
    return ordered


def reward_for_action(row: pd.Series, action: int) -> float:
    spec = ACTIONS[action]
    risk = float(row["dqn_risk_proxy"])
    uncertainty = float(row["dqn_uncertainty_proxy"])
    coverage_gap = float(row["dqn_coverage_gap_proxy"])
    risk_gain = spec["risk_reduction"] * risk
    info_gain = spec["info_gain"] * uncertainty
    constraint_proxy = max(0.0, spec["inspection_units"] - (1.0 + 2.0 * risk + coverage_gap))
    return 10.0 * risk_gain + 1.5 * info_gain - spec["cost"] - 2.0 * constraint_proxy


def train_fitted_q(states: pd.DataFrame) -> tuple[object, pd.DataFrame]:
    feature_cols = FEATURE_COLUMNS + ["dqn_risk_proxy", "dqn_uncertainty_proxy", "dqn_coverage_gap_proxy"]
    base = states.set_index("state_row_id")
    transitions = []
    for _, row in states.iterrows():
        for action in ACTIONS:
            transitions.append({
                "state_row_id": int(row["state_row_id"]),
                "next_state_row_id": int(row["next_state_row_id"]),
                "action": action,
                "reward": reward_for_action(row, action),
            })
    trans = pd.DataFrame(transitions)

    def make_x(frame: pd.DataFrame) -> np.ndarray:
        features = base.loc[frame["state_row_id"].values, feature_cols].fillna(0).to_numpy(dtype=float)
        actions = np.zeros((len(frame), len(ACTIONS)))
        actions[np.arange(len(frame)), frame["action"].values.astype(int)] = 1.0
        return np.hstack([features, actions])

    model = make_pipeline(
        StandardScaler(),
        MLPRegressor(
            hidden_layer_sizes=(48, 24),
            activation="relu",
            solver="adam",
            alpha=0.001,
            learning_rate_init=0.003,
            max_iter=500,
            random_state=SEED,
            early_stopping=True,
        ),
    )

    gamma = ASSUMPTIONS["discount_gamma"]
    y = trans["reward"].to_numpy(dtype=float)
    x = make_x(trans)
    for _ in range(ASSUMPTIONS["fqi_iterations"]):
        model.fit(x, y)
        next_values = []
        for action in ACTIONS:
            next_frame = pd.DataFrame({"state_row_id": trans["next_state_row_id"], "action": action})
            next_values.append(model.predict(make_x(next_frame)))
        max_next = np.vstack(next_values).max(axis=0)
        y = trans["reward"].to_numpy(dtype=float) + gamma * max_next

    model.fit(x, y)
    q_cols = {}
    for action, spec in ACTIONS.items():
        frame = pd.DataFrame({"state_row_id": states["state_row_id"], "action": action})
        q_cols[f"Q_action_{action}"] = model.predict(make_x(frame))
    q = pd.DataFrame(q_cols)
    q["recommended_action"] = q[[f"Q_action_{a}" for a in ACTIONS]].idxmax(axis=1).str.extract(r"(\d+)").astype(int)
    q["recommended_action_name"] = q["recommended_action"].map(lambda a: ACTIONS[int(a)]["name"])
    q["recommended_inspection_units"] = q["recommended_action"].map(lambda a: ACTIONS[int(a)]["inspection_units"])
    return model, pd.concat([states.reset_index(drop=True), q], axis=1)


def write_outputs(loaded: dict, audit: pd.DataFrame, policy: pd.DataFrame) -> dict:
    audit_path = TABLE_DIR / "peanut_dqn_upstream_audit_findings.csv"
    audit.to_csv(audit_path, index=False, encoding="utf-8-sig")

    policy_cols = [
        "省份", "年份", "月份", "年月", "供应链环节",
        "抽检总批次数", "AFB1相关记录数", "浓度可用记录数",
        "总体不合格_后验均值", "AFB1条件不合格_后验均值",
        "EDI均值", "EDI_P95", "MOE_default_均值", "低于MOE阈值比例",
        "人口加权风险_proxy", "MOE风险惩罚_proxy",
        "dqn_risk_proxy", "dqn_uncertainty_proxy", "dqn_coverage_gap_proxy",
        "Q_action_0", "Q_action_1", "Q_action_2",
        "recommended_action", "recommended_action_name", "recommended_inspection_units",
    ]
    policy_path = DATA_DIR / "peanut_dqn_prototype_policy.csv"
    policy[policy_cols].to_csv(policy_path, index=False, encoding="utf-8-sig")
    top_path = TABLE_DIR / "peanut_dqn_top_priority_states.csv"
    policy.sort_values(["recommended_action", "dqn_risk_proxy"], ascending=[False, False])[policy_cols].head(50).to_csv(
        top_path, index=False, encoding="utf-8-sig"
    )

    action_summary = (
        policy.groupby(["recommended_action", "recommended_action_name"], dropna=False)
        .agg(状态单元数=("state_row_id", "count"), 平均风险proxy=("dqn_risk_proxy", "mean"), 平均不确定性proxy=("dqn_uncertainty_proxy", "mean"))
        .reset_index()
    )
    action_summary_path = TABLE_DIR / "peanut_dqn_action_summary.csv"
    action_summary.to_csv(action_summary_path, index=False, encoding="utf-8-sig")

    CONFIG_DIR.joinpath("peanut_dqn_prototype_assumptions.json").write_text(
        json.dumps(ASSUMPTIONS, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    pass_count = int((audit["状态"] == "PASS").sum())
    warn_count = int((audit["状态"] == "WARN").sum())
    fail_count = int((audit["状态"] == "FAIL").sum())
    formal_ready = False
    prototype_ran = fail_count == 0
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "seed": SEED,
        "input_rows": {k: len(v) for k, v in loaded.items()},
        "audit_pass": pass_count,
        "audit_warn": warn_count,
        "audit_fail": fail_count,
        "prototype_ran": prototype_ran,
        "formal_dqn_ready": formal_ready,
        "policy_rows": len(policy),
        "action_counts": policy["recommended_action_name"].value_counts().to_dict(),
        "outputs": {
            "audit": str(audit_path),
            "policy": str(policy_path),
            "top_priority": str(top_path),
            "action_summary": str(action_summary_path),
        },
    }
    (LOG_DIR / "peanut_dqn_prototype_run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    report = [
        "# DQN 初步运行报告",
        "",
        "## 结论",
        "",
        "- 已完成上游核验和 DQN-style 沙盒初跑。",
        "- 本轮结果只能作为管线烟测和参数缺口定位，不能作为正式监管策略。",
        "- 正式 DQN 仍被阻断：动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束惩罚参数尚未确认。",
        "",
        "## 上游核验",
        "",
        f"- PASS: {pass_count}",
        f"- WARN: {warn_count}",
        f"- FAIL: {fail_count}",
        "",
        "## 沙盒模型设置",
        "",
        f"- 算法: {ASSUMPTIONS['algorithm']}",
        f"- 动作档位: {', '.join([str(k) + '=' + v['name'] for k, v in ACTIONS.items()])}",
        f"- gamma: {ASSUMPTIONS['discount_gamma']}",
        f"- FQI iterations: {ASSUMPTIONS['fqi_iterations']}",
        "",
        "## 动作分布",
        "",
        action_summary.to_markdown(index=False),
        "",
        "## 正式 DQN 缺口",
        "",
    ]
    report.extend([f"- {x}" for x in ASSUMPTIONS["formal_blockers"]])
    report.extend([
        "",
        "## 输出文件",
        "",
        f"- 上游核验表: `{audit_path}`",
        f"- prototype policy: `{policy_path}`",
        f"- 高优先级状态: `{top_path}`",
        f"- 动作汇总: `{action_summary_path}`",
    ])
    (REPORT_DIR / "peanut_dqn_prototype_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    ensure_dirs()
    loaded, audit = upstream_audit()
    if (audit["状态"] == "FAIL").any():
        audit.to_csv(TABLE_DIR / "peanut_dqn_upstream_audit_findings.csv", index=False, encoding="utf-8-sig")
        raise SystemExit("上游核验存在 FAIL，已阻断 DQN prototype。")
    states = prepare_states(loaded["belief_mdp_features_with_moe_edi"])
    states = build_transitions(states)
    _, policy = train_fitted_q(states)
    summary = write_outputs(loaded, audit, policy)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
