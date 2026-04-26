"""Baseline and policy evaluation for the experimental PEANUT DQN run."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

try:
    from .peanut_dqn_env_auto import PeanutDQNEnv, simulate_policy
except ImportError:  # pragma: no cover - direct script fallback
    from peanut_dqn_env_auto import PeanutDQNEnv, simulate_policy


def evaluate_baselines(
    df: pd.DataFrame,
    states: np.ndarray,
    mapping: dict[str, str | None],
    config: dict[str, Any],
    dqn_policy_fn=None,
) -> pd.DataFrame:
    """Evaluate required baseline policies on the same environment."""

    rng = np.random.default_rng(config["training"]["random_seed"])
    risk_col = mapping.get("posterior_mean")
    afb1_col = mapping.get("afb1_posterior_mean")
    moe_col = mapping.get("moe_penalty")
    population_col = mapping.get("population_risk")

    def risk_values(frame: pd.DataFrame) -> np.ndarray:
        risk = np.zeros(len(frame), dtype=float)
        if risk_col in frame:
            risk += 0.55 * pd.to_numeric(frame[risk_col], errors="coerce").fillna(0).to_numpy()
        if afb1_col in frame:
            risk += 0.25 * pd.to_numeric(frame[afb1_col], errors="coerce").fillna(0).to_numpy()
        if moe_col in frame:
            risk += 0.20 * pd.to_numeric(frame[moe_col], errors="coerce").fillna(0).to_numpy()
        if population_col in frame:
            pop = pd.to_numeric(frame[population_col], errors="coerce").fillna(0)
            scale = float(pop.quantile(0.95)) if len(pop) else 1.0
            scale = scale if scale > 0 else 1.0
            risk += 0.10 * (pop / scale).clip(upper=1.0).to_numpy()
        return risk

    risks = risk_values(df)
    risk_threshold = float(np.quantile(risks, 0.75))
    total_col = mapping["total_count"]
    action_values = np.array(config["action_space"]["increments"])

    def uniform_policy(env: PeanutDQNEnv, state, mask):
        valid = np.where(mask)[0]
        target = np.argmin(np.abs(action_values[valid] - np.median(action_values)))
        return int(valid[target])

    def random_policy(env: PeanutDQNEnv, state, mask):
        valid = np.where(mask)[0]
        return int(rng.choice(valid))

    def historical_policy(env: PeanutDQNEnv, state, mask):
        idx = env.index_order[env.position]
        observed = float(pd.to_numeric(env.df.loc[idx, total_col], errors="coerce"))
        valid = np.where(mask)[0]
        chosen = valid[np.argmin(np.abs(action_values[valid] - min(observed, action_values.max())))]
        return int(chosen)

    def risk_ranking_policy(env: PeanutDQNEnv, state, mask):
        idx = env.index_order[env.position]
        risk = risks[idx]
        valid = np.where(mask)[0]
        if risk >= risk_threshold:
            return int(valid[-1])
        target = np.argmin(np.abs(action_values[valid] - 1))
        return int(valid[target])

    policies = {
        "uniform_allocation": uniform_policy,
        "historical_allocation": historical_policy,
        "risk_ranking_top_k": risk_ranking_policy,
        "random_policy": random_policy,
    }
    if dqn_policy_fn is not None:
        policies["dqn_policy"] = dqn_policy_fn

    rows: list[dict[str, Any]] = []
    for name, fn in policies.items():
        env = PeanutDQNEnv(df, states, mapping, config, training=False)
        metrics = simulate_policy(env, fn)
        metrics["policy"] = name
        rows.append(metrics)
    out = pd.DataFrame(rows)
    if "dqn_policy" in out["policy"].values:
        base = out.loc[out["policy"] == "risk_ranking_top_k", "total_reward"].iloc[0]
        out["reward_vs_risk_ranking"] = out["total_reward"] - base
    else:
        out["reward_vs_risk_ranking"] = np.nan
    return out
