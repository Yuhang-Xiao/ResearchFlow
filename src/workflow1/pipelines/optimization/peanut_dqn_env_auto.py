"""Experimental PEANUT DQN environment utilities.

This module supports the self-synthesized DQN experimental run only. It uses
historical replay plus a lightweight Beta-Binomial uncertainty proxy; it does
not claim causal policy effects.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


EXPERIMENTAL_LABEL = "自动合成参数 DQN 实验版 / self-synthesized DQN experimental run"


@dataclass
class StepResult:
    next_state: np.ndarray
    reward: float
    done: bool
    info: dict[str, Any]


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dirs(config: dict[str, Any]) -> None:
    for key in [
        "run_package",
        "data_dir",
        "table_dir",
        "figure_dir",
        "report_dir",
        "model_dir",
        "config_dir",
        "log_dir",
    ]:
        Path(config["paths"][key]).mkdir(parents=True, exist_ok=True)


def read_state_table(config: dict[str, Any]) -> pd.DataFrame:
    path = Path(config["paths"]["state_features"])
    if not path.exists():
        raise FileNotFoundError(f"state feature table not found: {path}")
    df = pd.read_csv(path, encoding="utf-8-sig")
    if df.empty:
        raise ValueError("state feature table is empty")
    return df


def _first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def build_field_mapping(df: pd.DataFrame) -> dict[str, str | None]:
    mapping = {
        "province": _first_existing(df, ["省份", "省份_规范", "province"]),
        "year_month": _first_existing(df, ["年月", "year_month"]),
        "year": _first_existing(df, ["年份", "year"]),
        "month": _first_existing(df, ["月份", "month"]),
        "stage": _first_existing(df, ["供应链环节", "stage"]),
        "state_id": _first_existing(df, ["状态ID", "state_id"]),
        "total_count": _first_existing(df, ["抽检总批次数", "total_count"]),
        "fail_count": _first_existing(df, ["不合格批次数", "fail_count"]),
        "afb1_count": _first_existing(df, ["AFB1相关记录数", "afb1_count"]),
        "afb1_fail_count": _first_existing(df, ["AFB1相关不合格批次数", "afb1_fail_count"]),
        "concentration_count": _first_existing(df, ["浓度可用记录数", "concentration_count"]),
        "posterior_mean": _first_existing(df, ["总体不合格_后验均值", "posterior_mean"]),
        "posterior_var": _first_existing(df, ["总体不合格_后验方差", "posterior_variance"]),
        "afb1_posterior_mean": _first_existing(df, ["AFB1全样本不合格_后验均值", "afb1_posterior_mean"]),
        "afb1_posterior_var": _first_existing(df, ["AFB1全样本不合格_后验方差", "afb1_posterior_variance"]),
        "edi_mean": _first_existing(df, ["EDI均值", "EDI_mean"]),
        "edi_p95": _first_existing(df, ["EDI_P95", "EDI_p95"]),
        "moe_min": _first_existing(df, ["MOE_default_最小值", "MOE_default_min"]),
        "moe_penalty": _first_existing(df, ["MOE风险惩罚_proxy", "MOE风险惩罚项_均值", "moe_penalty"]),
        "population_risk": _first_existing(df, ["人口加权风险_proxy", "population_weighted_risk"]),
        "population": _first_existing(df, ["人口数_人", "population"]),
    }
    required = ["province", "year_month", "stage", "total_count", "posterior_mean", "posterior_var"]
    missing = [k for k in required if mapping[k] is None]
    if missing:
        raise ValueError(f"required state fields cannot be mapped: {missing}")
    return mapping


def prepare_state_matrix(
    df: pd.DataFrame, mapping: dict[str, str | None], config: dict[str, Any]
) -> tuple[pd.DataFrame, np.ndarray, dict[str, Any]]:
    feature_cols: list[str] = []
    for logical_name in config["state_space"]["features"]:
        col = mapping.get(logical_name, logical_name)
        if col and col in df.columns and col not in feature_cols:
            feature_cols.append(col)

    work = df.copy()
    fill_records: list[dict[str, Any]] = []
    for col in feature_cols:
        values = pd.to_numeric(work[col], errors="coerce")
        missing_before = int(values.isna().sum())
        if missing_before:
            if "MOE" in col or "EDI" in col or "风险" in col:
                fill_value = float(values.median()) if values.notna().any() else 0.0
            else:
                fill_value = 0.0
            values = values.fillna(fill_value)
            fill_records.append({"field": col, "missing_before": missing_before, "fill_value": fill_value})
        work[col] = values.astype(float)

    x = work[feature_cols].to_numpy(dtype=np.float32)
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std[std == 0] = 1.0
    x = (x - mean) / std
    meta = {"feature_columns": feature_cols, "fill_records": fill_records, "mean": mean, "std": std}
    return work, x.astype(np.float32), meta


def synthesize_budget_and_capacity(df: pd.DataFrame, mapping: dict[str, str | None]) -> dict[str, Any]:
    total_col = mapping["total_count"]
    monthly = df.groupby(mapping["year_month"])[total_col].sum()
    p50 = float(monthly.quantile(0.50))
    p75 = float(monthly.quantile(0.75))
    p90 = float(monthly.quantile(0.90))
    budget = max(1, int(round(p75)))
    local = df.groupby([mapping["province"], mapping["stage"]])[total_col].quantile(0.90)
    stage_p75 = df.groupby(mapping["stage"])[total_col].quantile(0.75)
    global_p75 = float(df[total_col].quantile(0.75))
    return {
        "monthly_total_p50": p50,
        "monthly_total_p75": p75,
        "monthly_total_p90": p90,
        "experimental_monthly_budget": budget,
        "local_capacity_p90": {f"{k[0]}|{k[1]}": max(1, int(round(v))) for k, v in local.items()},
        "stage_capacity_p75": {str(k): max(1, int(round(v))) for k, v in stage_p75.items()},
        "global_capacity_p75": max(1, int(round(global_p75))),
    }


class PeanutDQNEnv:
    """Small discrete-action historical replay environment."""

    def __init__(
        self,
        df: pd.DataFrame,
        states: np.ndarray,
        mapping: dict[str, str | None],
        config: dict[str, Any],
        training: bool = True,
    ) -> None:
        self.df = df.reset_index(drop=True)
        self.states = states
        self.mapping = mapping
        self.config = config
        self.actions = np.array(config["action_space"]["increments"], dtype=np.int64)
        self.training = training
        self.rng = np.random.default_rng(config["training"]["random_seed"])
        self.index_order = self._build_index_order()
        self.position = 0
        self.month_budget_remaining = float(config["constraints"]["monthly_budget"])
        self.current_month = None
        self.last_info: dict[str, Any] = {}
        self.population_risk_scale = self._build_population_risk_scale()

    @property
    def n_actions(self) -> int:
        return int(len(self.actions))

    @property
    def state_dim(self) -> int:
        return int(self.states.shape[1])

    def _build_index_order(self) -> np.ndarray:
        sort_cols = [self.mapping["year_month"], self.mapping["province"], self.mapping["stage"]]
        tmp = self.df.reset_index().sort_values(sort_cols)
        return tmp["index"].to_numpy(dtype=np.int64)

    def reset(self) -> np.ndarray:
        self.position = 0
        self.month_budget_remaining = float(self.config["constraints"]["monthly_budget"])
        self.current_month = None
        first_idx = self.index_order[self.position]
        self.current_month = self.df.loc[first_idx, self.mapping["year_month"]]
        return self.states[first_idx]

    def action_mask(self, state_index: int | None = None) -> np.ndarray:
        idx = self.index_order[self.position] if state_index is None else state_index
        row = self.df.loc[idx]
        cap = self._capacity_for_row(row)
        mask = (self.actions <= cap) & (self.actions <= self.month_budget_remaining)
        if not mask.any():
            mask[0] = True
        return mask.astype(bool)

    def step(self, action_index: int) -> StepResult:
        idx = int(self.index_order[self.position])
        row = self.df.loc[idx]
        month = row[self.mapping["year_month"]]
        if month != self.current_month:
            self.current_month = month
            self.month_budget_remaining = float(self.config["constraints"]["monthly_budget"])

        mask = self.action_mask(idx)
        chosen = int(action_index)
        violation = 0.0
        if chosen < 0 or chosen >= self.n_actions or not mask[chosen]:
            chosen = 0
            violation = 1.0
        action_value = float(self.actions[chosen])
        self.month_budget_remaining -= action_value

        reward, info = self._reward(row, action_value, violation)
        self.position += 1
        done = self.position >= len(self.index_order)
        next_state = np.zeros(self.state_dim, dtype=np.float32) if done else self.states[self.index_order[self.position]]
        self.last_info = info
        return StepResult(next_state=next_state, reward=reward, done=done, info=info)

    def _capacity_for_row(self, row: pd.Series) -> int:
        cap_cfg = self.config["constraints"]["local_capacity"]
        key = f"{row[self.mapping['province']]}|{row[self.mapping['stage']]}"
        if key in cap_cfg:
            return int(cap_cfg[key])
        stage_cap = self.config["constraints"].get("stage_capacity", {}).get(str(row[self.mapping["stage"]]))
        if stage_cap is not None:
            return int(stage_cap)
        return int(self.config["constraints"].get("global_capacity", 5))

    def _num(self, row: pd.Series, logical: str, default: float = 0.0) -> float:
        col = self.mapping.get(logical, logical)
        if col is None or col not in row:
            return default
        val = pd.to_numeric(row[col], errors="coerce")
        return default if pd.isna(val) else float(val)

    def _build_population_risk_scale(self) -> float:
        col = self.mapping.get("population_risk")
        if col is None or col not in self.df:
            return 1.0
        values = pd.to_numeric(self.df[col], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if values.empty:
            return 1.0
        scale = float(values.quantile(0.95))
        return scale if scale > 0 else 1.0

    def _reward(self, row: pd.Series, action_value: float, violation: float) -> tuple[float, dict[str, Any]]:
        weights = self.config["reward"]
        risk = (
            0.45 * self._num(row, "posterior_mean")
            + 0.25 * self._num(row, "afb1_posterior_mean")
            + 0.20 * self._num(row, "moe_penalty")
            + 0.10 * min(1.0, self._num(row, "population_risk") / self.population_risk_scale)
        )
        uncertainty = self._num(row, "posterior_var") + self._num(row, "afb1_posterior_var")
        action_scale = action_value / max(1.0, float(max(self.actions)))
        risk_coverage_gain = risk * np.log1p(action_value)
        information_gain = uncertainty * np.log1p(action_value)
        sampling_cost = weights["unit_sampling_cost"] * action_value
        reward = (
            weights["risk_reward_weight"] * risk_coverage_gain
            + weights["info_gain_weight"] * information_gain
            - weights["cost_weight"] * sampling_cost
            - weights["constraint_penalty_weight"] * violation
        )
        info = {
            "risk_score": float(risk),
            "uncertainty_score": float(uncertainty),
            "action_value": action_value,
            "action_scale": float(action_scale),
            "risk_coverage_gain": float(risk_coverage_gain),
            "information_gain": float(information_gain),
            "sampling_cost": float(sampling_cost),
            "constraint_violation": float(violation),
            "reward": float(reward),
        }
        return float(reward), info


def simulate_policy(env: PeanutDQNEnv, policy_fn) -> dict[str, Any]:
    state = env.reset()
    done = False
    rewards: list[float] = []
    violations = 0
    actions: list[float] = []
    while not done:
        mask = env.action_mask()
        action_index = int(policy_fn(env, state, mask))
        result = env.step(action_index)
        rewards.append(result.reward)
        violations += int(result.info["constraint_violation"] > 0)
        actions.append(result.info["action_value"])
        state = result.next_state
        done = result.done
    return {
        "total_reward": float(np.sum(rewards)),
        "mean_reward": float(np.mean(rewards) if rewards else 0.0),
        "constraint_violation_count": int(violations),
        "constraint_violation_rate": float(violations / max(1, len(rewards))),
        "mean_action": float(np.mean(actions) if actions else 0.0),
        "steps": int(len(rewards)),
    }
