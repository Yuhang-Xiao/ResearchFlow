"""Train the experimental PEANUT DQN with self-synthesized parameters."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import shutil
import sys
import traceback
from collections import deque
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn

try:
    from .peanut_dqn_env_auto import (
        EXPERIMENTAL_LABEL,
        PeanutDQNEnv,
        build_field_mapping,
        ensure_dirs,
        load_config,
        prepare_state_matrix,
        read_state_table,
    )
    from .peanut_dqn_evaluate_auto import evaluate_baselines
except ImportError:  # pragma: no cover - direct script fallback
    from peanut_dqn_env_auto import (
        EXPERIMENTAL_LABEL,
        PeanutDQNEnv,
        build_field_mapping,
        ensure_dirs,
        load_config,
        prepare_state_matrix,
        read_state_table,
    )
    from peanut_dqn_evaluate_auto import evaluate_baselines


class QNetwork(nn.Module):
    def __init__(self, state_dim: int, n_actions: int, hidden_layers: list[int]) -> None:
        super().__init__()
        layers: list[nn.Module] = []
        last = state_dim
        for width in hidden_layers:
            layers.append(nn.Linear(last, width))
            layers.append(nn.ReLU())
            last = width
        layers.append(nn.Linear(last, n_actions))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity: int) -> None:
        self.buffer: deque[tuple[np.ndarray, int, float, np.ndarray, bool]] = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done) -> None:
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.asarray(states, dtype=np.float32),
            np.asarray(actions, dtype=np.int64),
            np.asarray(rewards, dtype=np.float32),
            np.asarray(next_states, dtype=np.float32),
            np.asarray(dones, dtype=np.float32),
        )

    def __len__(self) -> int:
        return len(self.buffer)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def select_action(q_net: QNetwork, state: np.ndarray, mask: np.ndarray, epsilon: float, device: torch.device) -> int:
    valid = np.where(mask)[0]
    if random.random() < epsilon:
        return int(random.choice(valid.tolist()))
    with torch.no_grad():
        s = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        q = q_net(s).detach().cpu().numpy()[0]
    q[~mask] = -1e9
    return int(np.argmax(q))


def write_df(df: pd.DataFrame, csv_path: Path, xlsx_path: Path | None = None) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    if xlsx_path is not None:
        xlsx_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(xlsx_path, index=False)


def save_svg_line(df: pd.DataFrame, x: str, ys: list[str], path: Path, title: str) -> None:
    plt.figure(figsize=(9, 5))
    for y in ys:
        if y in df:
            plt.plot(df[x], df[y], label=y)
    plt.title(title)
    plt.xlabel(x)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, format="svg")
    plt.close()


def save_svg_bar(df: pd.DataFrame, x: str, y: str, path: Path, title: str, rotate: int = 20) -> None:
    plt.figure(figsize=(9, 5))
    plt.bar(df[x].astype(str), df[y])
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=rotate, ha="right")
    plt.tight_layout()
    plt.savefig(path, format="svg")
    plt.close()


def train(config: dict[str, Any]) -> dict[str, Any]:
    ensure_dirs(config)
    paths = {k: Path(v) for k, v in config["paths"].items()}
    error_log = paths["log_dir"] / "dqn_auto_training_error_log.md"
    console_log = paths["log_dir"] / "dqn_auto_training_console_log.txt"
    previous_error_log = error_log.read_text(encoding="utf-8", errors="replace") if error_log.exists() else ""
    repaired_note = ""
    if "tabulate" in previous_error_log:
        repaired_note = (
            "\n## 自动修复记录\n\n"
            "- 首次训练在结果报告阶段因 pandas.to_markdown 依赖 tabulate 缺失而失败；"
            "已改用内置 CSV 文本生成 baseline 报告，不影响训练、模型或数值结果。\n"
        )
    error_log.write_text(
        f"# DQN auto training error log\n\n任务性质：{EXPERIMENTAL_LABEL}\n"
        f"{repaired_note}\n",
        encoding="utf-8",
    )
    console_log.write_text("", encoding="utf-8")

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA/GPU unavailable; CPU downgrade is forbidden for this task.")
    device_name = torch.cuda.get_device_name(0)
    if "4060 Ti" not in device_name:
        raise RuntimeError(f"Unexpected GPU: {device_name}")
    device = torch.device("cuda")

    set_seed(int(config["training"]["random_seed"]))
    raw_df = read_state_table(config)
    mapping = build_field_mapping(raw_df)
    work_df, states, matrix_meta = prepare_state_matrix(raw_df, mapping, config)
    env = PeanutDQNEnv(work_df, states, mapping, config)

    q_net = QNetwork(env.state_dim, env.n_actions, config["network"]["hidden_layers"]).to(device)
    target_net = QNetwork(env.state_dim, env.n_actions, config["network"]["hidden_layers"]).to(device)
    target_net.load_state_dict(q_net.state_dict())
    optimizer = torch.optim.Adam(q_net.parameters(), lr=float(config["training"]["learning_rate"]))
    buffer = ReplayBuffer(int(config["training"]["replay_buffer_size"]))

    gamma = float(config["training"]["gamma"])
    epsilon = float(config["training"]["epsilon_start"])
    epsilon_min = float(config["training"]["epsilon_min"])
    epsilon_decay = float(config["training"]["epsilon_decay"])
    batch_size = int(config["training"]["batch_size"])
    target_update = int(config["training"]["target_update_frequency"])
    episodes = int(config["training"]["episodes"])
    global_step = 0
    metrics: list[dict[str, Any]] = []
    training_log_rows: list[dict[str, Any]] = []

    try:
        for episode in range(1, episodes + 1):
            state = env.reset()
            done = False
            total_reward = 0.0
            losses: list[float] = []
            actions: list[float] = []
            violations = 0
            while not done:
                mask = env.action_mask()
                action = select_action(q_net, state, mask, epsilon, device)
                result = env.step(action)
                buffer.push(state, action, result.reward, result.next_state, result.done)
                state = result.next_state
                done = result.done
                total_reward += result.reward
                actions.append(result.info["action_value"])
                violations += int(result.info["constraint_violation"] > 0)
                global_step += 1

                if len(buffer) >= batch_size:
                    b_states, b_actions, b_rewards, b_next, b_dones = buffer.sample(batch_size)
                    ts = torch.tensor(b_states, dtype=torch.float32, device=device)
                    ta = torch.tensor(b_actions, dtype=torch.int64, device=device).unsqueeze(1)
                    tr = torch.tensor(b_rewards, dtype=torch.float32, device=device).unsqueeze(1)
                    tn = torch.tensor(b_next, dtype=torch.float32, device=device)
                    td = torch.tensor(b_dones, dtype=torch.float32, device=device).unsqueeze(1)
                    q_values = q_net(ts).gather(1, ta)
                    with torch.no_grad():
                        next_q = target_net(tn).max(dim=1, keepdim=True).values
                        target = tr + gamma * next_q * (1.0 - td)
                    loss = nn.functional.smooth_l1_loss(q_values, target)
                    optimizer.zero_grad()
                    loss.backward()
                    nn.utils.clip_grad_norm_(q_net.parameters(), 5.0)
                    optimizer.step()
                    losses.append(float(loss.item()))

                if global_step % target_update == 0:
                    target_net.load_state_dict(q_net.state_dict())

            epsilon = max(epsilon_min, epsilon * epsilon_decay)
            row = {
                "episode": episode,
                "total_reward": total_reward,
                "mean_loss": float(np.mean(losses) if losses else 0.0),
                "epsilon": epsilon,
                "mean_action": float(np.mean(actions) if actions else 0.0),
                "constraint_violation_rate": float(violations / max(1, len(actions))),
                "buffer_size": len(buffer),
                "device": str(device),
                "gpu": device_name,
            }
            metrics.append(row)
            training_log_rows.append(row)
            if episode % 10 == 0 or episode == 1:
                with console_log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except KeyboardInterrupt:
        error_log.write_text(error_log.read_text(encoding="utf-8") + "\n- 训练被中断，已保存当前可用结果。\n", encoding="utf-8")
    except Exception:
        tb = traceback.format_exc()
        error_log.write_text(error_log.read_text(encoding="utf-8") + "\n## Unresolved training error\n\n```text\n" + tb + "\n```\n", encoding="utf-8")
        raise

    metrics_df = pd.DataFrame(metrics)
    write_df(metrics_df, paths["table_dir"] / "peanut_dqn_auto_training_metrics.csv")
    write_df(pd.DataFrame(training_log_rows), paths["model_dir"] / "peanut_dqn_auto_training_log.csv")

    with torch.no_grad():
        all_q = q_net(torch.tensor(states, dtype=torch.float32, device=device)).detach().cpu().numpy()
    action_values = np.array(config["action_space"]["increments"])
    chosen_idx = all_q.argmax(axis=1)
    policy = work_df[[mapping["province"], mapping["year_month"], mapping["stage"]]].copy()
    policy.columns = ["省份", "年月", "供应链环节"]
    if mapping.get("state_id"):
        policy["状态ID"] = work_df[mapping["state_id"]]
    policy["recommended_action_index"] = chosen_idx
    policy["recommended_extra_sampling_batches"] = action_values[chosen_idx]
    policy["experimental_label"] = EXPERIMENTAL_LABEL
    population_risk_values = pd.to_numeric(work_df[mapping.get("population_risk")], errors="coerce").fillna(0)
    population_scale = float(population_risk_values.quantile(0.95)) if len(population_risk_values) else 1.0
    if population_scale <= 0:
        population_scale = 1.0
    policy["risk_score_proxy"] = (
        0.45 * pd.to_numeric(work_df[mapping["posterior_mean"]], errors="coerce").fillna(0)
        + 0.25 * pd.to_numeric(work_df[mapping["afb1_posterior_mean"]], errors="coerce").fillna(0)
        + 0.20 * pd.to_numeric(work_df[mapping.get("moe_penalty")], errors="coerce").fillna(0)
        + 0.10 * (population_risk_values / population_scale).clip(upper=1.0)
    )
    write_df(policy, paths["data_dir"] / "peanut_dqn_auto_policy.csv", paths["data_dir"] / "peanut_dqn_auto_policy.xlsx")

    q_df = policy[["省份", "年月", "供应链环节"]].copy()
    for i, action_value in enumerate(action_values):
        q_df[f"Q_action_{action_value}"] = all_q[:, i]
    q_df["experimental_label"] = EXPERIMENTAL_LABEL
    write_df(q_df, paths["data_dir"] / "peanut_dqn_auto_state_q_values.csv", paths["data_dir"] / "peanut_dqn_auto_state_q_values.xlsx")

    def dqn_policy_fn(eval_env: PeanutDQNEnv, state, mask):
        idx = eval_env.index_order[eval_env.position]
        q = all_q[idx].copy()
        q[~mask] = -1e9
        return int(np.argmax(q))

    comparison = evaluate_baselines(work_df, states, mapping, config, dqn_policy_fn=dqn_policy_fn)
    write_df(comparison, paths["table_dir"] / "peanut_dqn_auto_policy_comparison.csv")

    top = policy.sort_values("risk_score_proxy", ascending=False).head(50)
    write_df(top, paths["table_dir"] / "peanut_dqn_auto_top_priority_states.csv")
    action_summary = (
        policy.groupby("recommended_extra_sampling_batches")
        .size()
        .reset_index(name="state_count")
        .sort_values("recommended_extra_sampling_batches")
    )
    write_df(action_summary, paths["table_dir"] / "peanut_dqn_auto_action_summary.csv")
    constraint_summary = pd.DataFrame(
        [
            {
                "monthly_budget": config["constraints"]["monthly_budget"],
                "global_capacity": config["constraints"]["global_capacity"],
                "observed_policy_states": len(policy),
                "max_recommended_action": int(policy["recommended_extra_sampling_batches"].max()),
                "dqn_eval_constraint_violation_rate": float(
                    comparison.loc[comparison["policy"] == "dqn_policy", "constraint_violation_rate"].iloc[0]
                ),
                "experimental_label": EXPERIMENTAL_LABEL,
            }
        ]
    )
    write_df(constraint_summary, paths["table_dir"] / "peanut_dqn_auto_constraint_summary.csv")

    replay_summary = pd.DataFrame(
        [
            {
                "replay_buffer_size_final": len(buffer),
                "episodes": len(metrics_df),
                "state_dim": env.state_dim,
                "n_actions": env.n_actions,
                "feature_columns": ",".join(matrix_meta["feature_columns"]),
            }
        ]
    )
    write_df(replay_summary, paths["model_dir"] / "peanut_dqn_auto_replay_summary.csv")
    ledger = pd.DataFrame(
        [
            {
                "experiment_id": config["experiment"]["id"],
                "label": EXPERIMENTAL_LABEL,
                "status": "completed",
                "state_rows": len(work_df),
                "episodes": len(metrics_df),
                "device": str(device),
                "gpu": device_name,
            }
        ]
    )
    write_df(ledger, paths["model_dir"] / "experiment_ledger.csv")

    torch.save(
        {
            "model_state_dict": q_net.state_dict(),
            "config": config,
            "field_mapping": mapping,
            "feature_columns": matrix_meta["feature_columns"],
            "feature_mean": matrix_meta["mean"],
            "feature_std": matrix_meta["std"],
            "experimental_label": EXPERIMENTAL_LABEL,
        },
        paths["model_dir"] / "peanut_dqn_auto_model.pt",
    )

    save_svg_line(
        metrics_df,
        "episode",
        ["total_reward", "mean_loss", "epsilon"],
        paths["figure_dir"] / "peanut_dqn_auto_training_curve.svg",
        "DQN experimental training curve",
    )
    save_svg_bar(
        comparison,
        "policy",
        "total_reward",
        paths["figure_dir"] / "peanut_dqn_auto_policy_comparison.svg",
        "Policy comparison by total reward",
    )
    save_svg_bar(
        action_summary,
        "recommended_extra_sampling_batches",
        "state_count",
        paths["figure_dir"] / "peanut_dqn_auto_action_distribution.svg",
        "DQN action distribution",
        rotate=0,
    )
    save_svg_bar(
        top.head(20),
        "状态ID" if "状态ID" in top.columns else "年月",
        "risk_score_proxy",
        paths["figure_dir"] / "peanut_dqn_auto_top_priority_risk.svg",
        "Top priority state risk proxy",
        rotate=75,
    )
    save_svg_bar(
        comparison,
        "policy",
        "constraint_violation_rate",
        paths["figure_dir"] / "peanut_dqn_auto_constraint_violation.svg",
        "Constraint violation rate",
    )

    final_reward = float(metrics_df["total_reward"].iloc[-1]) if not metrics_df.empty else 0.0
    final_loss = float(metrics_df["mean_loss"].iloc[-1]) if not metrics_df.empty else 0.0
    dqn_reward = float(comparison.loc[comparison["policy"] == "dqn_policy", "total_reward"].iloc[0])
    best_baseline = comparison[comparison["policy"] != "dqn_policy"].sort_values("total_reward", ascending=False).iloc[0]
    report = f"""# PEANUT DQN 自动训练报告

任务性质：{EXPERIMENTAL_LABEL}

## 训练结论

- 状态数：{len(work_df)}
- 状态维度：{env.state_dim}
- 动作空间：{config['action_space']['increments']}
- 训练 episodes：{len(metrics_df)}
- 设备：{device} / {device_name}
- 最终 episode reward：{final_reward:.6f}
- 最终 mean loss：{final_loss:.6f}

## baseline 对比

DQN policy total reward = {dqn_reward:.6f}；最佳非 DQN baseline 为 `{best_baseline['policy']}`，total reward = {float(best_baseline['total_reward']):.6f}。

## 解释边界

本结果可以用于 workflow 闭环验收、prototype 方法探索和参数敏感性设计，不能作为正式监管政策结论、论文最终核心结论或用户确认参数后的 formal DQN 结果。
"""
    (paths["report_dir"] / "peanut_dqn_auto_training_report.md").write_text(report, encoding="utf-8")

    baseline_report = "# DQN baseline 对比报告\n\n```csv\n" + comparison.to_csv(index=False) + "```\n"
    (paths["report_dir"] / "peanut_dqn_auto_baseline_comparison_report.md").write_text(baseline_report, encoding="utf-8")
    limitations = f"""# DQN experimental limitations

- 本轮为 {EXPERIMENTAL_LABEL}。
- transition 采用 historical replay 与 Beta-Binomial uncertainty proxy，不代表真实监管干预因果效应。
- budget、capacity、cost、minimum coverage、reward weights 和训练超参数由 Codex 自动合成，正式版本仍需用户确认。
- 不能写成 final policy conclusion 或 formal DQN result。
"""
    (paths["report_dir"] / "peanut_dqn_auto_limitations_report.md").write_text(limitations, encoding="utf-8")
    next_steps = """# 下一步

1. 用户逐项确认 DQN 参数表中的 action、budget、capacity、cost、reward 和 transition 假设。
2. 用确认后的参数生成 formal config，不覆盖本轮 experimental config。
3. 重新运行环境 smoke test、上游审计和 formal DQN 训练。
4. 将 formal 结果与本轮 experimental 结果做敏感性对照。
"""
    (paths["report_dir"] / "peanut_dqn_auto_next_steps.md").write_text(next_steps, encoding="utf-8")

    return {
        "policy": policy,
        "q_values": q_df,
        "comparison": comparison,
        "metrics": metrics_df,
        "mapping": mapping,
        "feature_meta": matrix_meta,
        "device": str(device),
        "gpu": device_name,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    try:
        result = train(config)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "experimental_label": EXPERIMENTAL_LABEL,
                    "policy_rows": len(result["policy"]),
                    "gpu": result["gpu"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
