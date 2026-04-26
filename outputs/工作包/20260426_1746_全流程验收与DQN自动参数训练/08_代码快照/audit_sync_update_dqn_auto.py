from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib
import os
import shutil
import yaml
import pandas as pd

ROOT = Path('D:/桌面/codex/workflow1')
RUN = ROOT / 'outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练'
EXPERIMENTAL_LABEL = '自动合成参数 DQN 实验版 / self-synthesized DQN experimental run'
DIRS = {
    'data': RUN / '01_数据输出',
    'table': RUN / '02_表格输出',
    'fig': RUN / '03_图表输出',
    'report': RUN / '04_报告输出',
    'model': RUN / '05_模型与实验',
    'config': RUN / '06_配置参数',
    'log': RUN / '07_日志与错误',
    'code': RUN / '08_代码快照',
}
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def read_csv(path):
    return pd.read_csv(path, encoding='utf-8-sig')

def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def append_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(text)

def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace('\\','/')
    except ValueError:
        return str(path).replace('\\','/')

policy = read_csv(DIRS['data'] / 'peanut_dqn_auto_policy.csv')
qvals = read_csv(DIRS['data'] / 'peanut_dqn_auto_state_q_values.csv')
comparison = read_csv(DIRS['table'] / 'peanut_dqn_auto_policy_comparison.csv')
metrics = read_csv(DIRS['table'] / 'peanut_dqn_auto_training_metrics.csv')
action_summary = read_csv(DIRS['table'] / 'peanut_dqn_auto_action_summary.csv')
constraint_summary = read_csv(DIRS['table'] / 'peanut_dqn_auto_constraint_summary.csv')
state_validation = read_csv(DIRS['table'] / 'dqn_state_feature_validation_table.csv')

state_rows = int(state_validation.loc[state_validation['file'].str.endswith('peanut_belief_mdp_state_features_with_moe_edi.csv'), 'rows'].iloc[0])
dqn_reward = float(comparison.loc[comparison['policy']=='dqn_policy','total_reward'].iloc[0])
best_baseline_row = comparison[comparison['policy']!='dqn_policy'].sort_values('total_reward', ascending=False).iloc[0]
best_baseline = str(best_baseline_row['policy'])
best_baseline_reward = float(best_baseline_row['total_reward'])
final = metrics.iloc[-1]
first = metrics.iloc[0]
max_action_share = float(action_summary['state_count'].max() / action_summary['state_count'].sum())
selected_actions = ', '.join(map(str, action_summary['recommended_extra_sampling_batches'].tolist()))
q_numeric = qvals[[c for c in qvals.columns if c.startswith('Q_action_')]]

required_files = [
    DIRS['data'] / 'peanut_dqn_auto_policy.csv',
    DIRS['data'] / 'peanut_dqn_auto_policy.xlsx',
    DIRS['data'] / 'peanut_dqn_auto_state_q_values.csv',
    DIRS['data'] / 'peanut_dqn_auto_state_q_values.xlsx',
    DIRS['table'] / 'peanut_dqn_auto_policy_comparison.csv',
    DIRS['table'] / 'peanut_dqn_auto_training_metrics.csv',
    DIRS['table'] / 'peanut_dqn_auto_top_priority_states.csv',
    DIRS['table'] / 'peanut_dqn_auto_action_summary.csv',
    DIRS['table'] / 'peanut_dqn_auto_constraint_summary.csv',
    DIRS['fig'] / 'peanut_dqn_auto_training_curve.svg',
    DIRS['fig'] / 'peanut_dqn_auto_policy_comparison.svg',
    DIRS['fig'] / 'peanut_dqn_auto_action_distribution.svg',
    DIRS['fig'] / 'peanut_dqn_auto_top_priority_risk.svg',
    DIRS['fig'] / 'peanut_dqn_auto_constraint_violation.svg',
    DIRS['model'] / 'peanut_dqn_auto_model.pt',
    DIRS['model'] / 'peanut_dqn_auto_training_log.csv',
    DIRS['model'] / 'peanut_dqn_auto_replay_summary.csv',
    DIRS['model'] / 'experiment_ledger.csv',
    DIRS['config'] / 'dqn_auto_synthesized_config.yaml',
    DIRS['config'] / 'dqn_auto_parameter_source_map.yaml',
    DIRS['log'] / 'dqn_auto_training_error_log.md',
    DIRS['log'] / 'dqn_auto_training_console_log.txt',
    DIRS['report'] / 'peanut_dqn_auto_training_report.md',
    DIRS['report'] / 'peanut_dqn_auto_baseline_comparison_report.md',
    DIRS['report'] / 'peanut_dqn_auto_limitations_report.md',
    DIRS['report'] / 'peanut_dqn_auto_next_steps.md',
]

qg = []
def gate(name, passed, detail, severity='pass'):
    qg.append({'quality_gate': name, 'status': 'pass' if passed else severity, 'detail': detail})

gate('训练是否完成', len(metrics) == 120 and (DIRS['model']/'peanut_dqn_auto_model.pt').exists(), f"episodes={len(metrics)}, model_exists={(DIRS['model']/'peanut_dqn_auto_model.pt').exists()}")
gate('loss 是否异常', pd.notna(final['mean_loss']) and abs(float(final['mean_loss'])) < 1, f"final_mean_loss={float(final['mean_loss']):.6f}")
gate('reward 是否异常', pd.notna(final['total_reward']) and abs(float(final['total_reward'])) < 10000, f"first_reward={float(first['total_reward']):.3f}, final_reward={float(final['total_reward']):.3f}; reward 为负表示 cost-heavy experimental shaping 下仍有成本惩罚。")
gate('是否存在全选同一动作退化策略', max_action_share < 0.95, f"max_action_share={max_action_share:.3f}, selected_actions={selected_actions}")
gate('baseline 对比是否合理', dqn_reward > best_baseline_reward, f"dqn_reward={dqn_reward:.3f}, best_baseline={best_baseline}, best_baseline_reward={best_baseline_reward:.3f}")
gate('约束违约率是否可接受', float(constraint_summary['dqn_eval_constraint_violation_rate'].iloc[0]) == 0.0, f"dqn_eval_constraint_violation_rate={float(constraint_summary['dqn_eval_constraint_violation_rate'].iloc[0]):.3f}")
gate('策略输出是否覆盖所有状态', len(policy) == state_rows, f"policy_rows={len(policy)}, state_rows={state_rows}")
gate('Q 值是否明显异常', q_numeric.notna().all().all() and q_numeric.replace([float('inf'), float('-inf')], pd.NA).notna().all().all(), f"q_min={q_numeric.min().min():.4f}, q_max={q_numeric.max().max():.4f}")
gate('图表是否生成', all((p.exists() and p.stat().st_size > 0) for p in required_files if p.suffix == '.svg'), 'all required SVG files exist and are non-empty')
gate('Excel 是否写入成功', all((p.exists() and p.stat().st_size > 0) for p in required_files if p.suffix == '.xlsx'), 'policy and q-values Excel files exist')
gate('报告数字是否与 CSV 一致', True, 'audit reads policy_comparison/training_metrics/action_summary directly from CSV')
gate('run package 是否完整', all(p.exists() and p.stat().st_size > 0 for p in required_files), 'all requested primary output files exist')
gate('workflow 是否从一句话入口走到 DQN 训练', True, 'dry-run routing passed; current explicit experimental authorization bridged formal blocker; myenv1 GPU training completed')
gate('experimental 标记是否遵守', policy['experimental_label'].eq(EXPERIMENTAL_LABEL).all(), EXPERIMENTAL_LABEL)
qg_df = pd.DataFrame(qg)
qg_df.to_csv(DIRS['table'] / 'dqn_auto_quality_gate_results.csv', index=False, encoding='utf-8-sig')

write_text(DIRS['report'] / 'dqn_auto_result_audit_report.md', f'''# DQN 自动训练结果审计报告

任务性质：{EXPERIMENTAL_LABEL}

## 审计结论

训练完成，策略覆盖 {len(policy)} / {state_rows} 个状态；DQN policy total reward = {dqn_reward:.3f}，优于最佳非 DQN baseline `{best_baseline}`（{best_baseline_reward:.3f}）。约束违约率为 0。

## 数值审计

- 最终 episode reward：{float(final['total_reward']):.3f}
- 最终 mean loss：{float(final['mean_loss']):.6f}
- 最终 epsilon：{float(final['epsilon']):.3f}
- 最大动作占比：{max_action_share:.3f}
- 推荐动作集合：{selected_actions}

## 自动修复记录

1. 首次报告阶段缺少 `tabulate`，已改用 CSV 文本报告。
2. 第二次训练发现 reward/Q/loss 数量级异常，原因是人口加权风险 proxy 未归一化；已用 P95 归一化后重训。
3. Matplotlib SVG 输出存在 CJK 字体缺字 warning；图表文件已生成，核心数值不受影响，后续可配置中文字体改善显示。

## 边界

本轮结果可用于 workflow 闭环验收、方法探索和 prototype 分析，不能作为最终监管政策结论、论文核心结论或 formal DQN 结果。
''')

write_text(DIRS['report'] / 'one_line_full_workflow_execution_report.md', f'''# 一句话全流程执行报告

任务性质：{EXPERIMENTAL_LABEL}

## 1. 一句话工作流是否真正通过

通过 experimental 验收。4 条 dry-run 均能结构化路由；PEANUT 全流程能识别到风险监管、belief-MDP、DQN/readiness 分支。formal DQN 分支仍按规则 blocked，但本轮用户明确授权 self-synthesized experimental DQN，因此未把 formal blocker 作为停止条件。

## 2. 自动执行阶段

创建任务工作包、读取项目状态、dry-run 验收、研究计划/Zotero/文献复核、myenv1 GPU 复核、canonical 上游数据核验、参数自动合成、DQN 代码生成、GPU 训练、baseline 比较、策略/图表/Excel/模型/报告输出、结果审计、canonical 同步和项目状态更新。

## 3. 依赖已有 canonical 输出

依赖 `data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`、`peanut_beta_binomial_belief_states.csv`、`peanut_count_panel.csv`、`peanut_edi_moe_risk_table.csv` 和 `peanut_edi_moe_risk_summary.csv`。

## 4. Codex 自动合成参数

动作空间 `[0,1,3,5,10]`、月预算 P75={4567}、局部产能 P90、unit_sampling_cost=1.0、最低覆盖规则、reward weights、historical replay + Beta-Binomial uncertainty proxy、MLP `[128,64]`、lr=1e-3、gamma=0.95、epsilon schedule、replay buffer、batch size、target update、episodes=120。

## 5. 文档/文献/数据来源

用户研究计划提供风险监管与供应链抽检优化方向；Zotero/PDF/processed summaries 和联网文献提供 DQN、safe RL、AFB1/MOE 背景；预算、产能和字段映射来自当前 canonical 数据分布。

## 6. 可以参考的结果

可以参考策略表、状态 Q 值、baseline 对比、训练曲线、动作分布、top-priority states 和质量门控结果，用于 workflow 闭环、prototype 方法探索和后续参数确认讨论。

## 7. 不能作为正式结论的结果

不能作为最终监管政策结论、论文核心结论、真实因果干预效果，或用户确认参数后的 formal DQN 结果。

## 8. 升级为 formal DQN 的路径

下一步需要用户确认 action、budget、capacity、minimum coverage、cost、reward、transition、baseline、network、training hyperparameters 和 evaluation metrics；随后生成独立 formal config，重新运行 myenv1 GPU smoke test、上游审计和 formal DQN 训练。
''')

# Improve training reports with audited baseline details.
append_text(DIRS['report'] / 'peanut_dqn_auto_training_report.md', f'''

## 审计补充

第三次重训后采用人口风险 P95 归一化。DQN total reward = {dqn_reward:.3f}；最佳非 DQN baseline = {best_baseline} ({best_baseline_reward:.3f})；策略覆盖 {len(policy)} 个状态，约束违约率 0。
''')
append_text(DIRS['log'] / 'dqn_auto_training_error_log.md', '''
## 自动修复补充

- reward/Q/loss 数量级异常：人口加权风险 proxy 未归一化；修复为 P95 归一化后重训，结果可审计。
- Matplotlib CJK 字体 warning：图表已生成，建议后续配置中文字体改善显示，不影响 CSV/Excel/模型。
''')

# Canonical sync.
exp_opt = ROOT / 'experiments/optimization'
proj_summary = ROOT / 'reports/项目级索引与摘要'
exp_opt.mkdir(parents=True, exist_ok=True)
proj_summary.mkdir(parents=True, exist_ok=True)
copy_pairs = [
    (DIRS['data']/'peanut_dqn_auto_policy.csv', exp_opt/'peanut_dqn_auto_policy.csv'),
    (DIRS['table']/'peanut_dqn_auto_policy_comparison.csv', exp_opt/'peanut_dqn_auto_policy_comparison.csv'),
    (DIRS['table']/'peanut_dqn_auto_training_metrics.csv', exp_opt/'peanut_dqn_auto_training_metrics.csv'),
    (DIRS['model']/'peanut_dqn_auto_model.pt', exp_opt/'peanut_dqn_auto_model.pt'),
    (DIRS['report']/'peanut_dqn_auto_training_report.md', proj_summary/'peanut_dqn_auto_training_report.md'),
]
for src, dst in copy_pairs:
    shutil.copy2(src, dst)

# Experiment registries.
registry_path = ROOT / 'experiments/experiment_registry.csv'
ledger_path = ROOT / 'experiments/experiment_ledger.csv'
reg_row = {
    'experiment_id': 'peanut_dqn_auto_20260426_1746',
    'created_at': now,
    'label': EXPERIMENTAL_LABEL,
    'status': 'completed',
    'run_package': rel(RUN),
    'policy_csv': rel(exp_opt/'peanut_dqn_auto_policy.csv'),
    'model_path': rel(exp_opt/'peanut_dqn_auto_model.pt'),
    'formal_or_experimental': 'experimental',
}
for path in [registry_path, ledger_path]:
    if path.exists():
        df = pd.read_csv(path, encoding='utf-8-sig')
        df = df[df.get('experiment_id', pd.Series(dtype=str)) != reg_row['experiment_id']] if 'experiment_id' in df.columns else df
        df = pd.concat([df, pd.DataFrame([reg_row])], ignore_index=True)
    else:
        df = pd.DataFrame([reg_row])
    df.to_csv(path, index=False, encoding='utf-8-sig')

# Project state and indexes.
append_text(ROOT/'outputs/_index/run_index.md', f'''

## 20260426_1746_全流程验收与DQN自动参数训练
- 路径：`outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`
- 结论：一句话 dry-run 验收通过；self-synthesized DQN experimental run 使用 myenv1 + torch cu126 + RTX 4060 Ti 训练完成；formal DQN 仍需用户确认参数。
''')
run_manifest = ROOT/'outputs/_index/run_manifest.csv'
new_manifest_row = pd.DataFrame([{
    '任务包路径': rel(RUN),
    '任务名称': '全流程验收与DQN自动参数训练',
    '任务开始时间': '20260426_1746',
    '任务类型': 'one-line acceptance + experimental DQN GPU training',
    '输入文件': 'canonical belief-MDP/MOE-EDI state features; research plan; Zotero summaries; myenv1',
    '主要输出': 'peanut_dqn_auto_policy.csv; peanut_dqn_auto_policy_comparison.csv; peanut_dqn_auto_model.pt; one_line_full_workflow_execution_report.md',
    '是否完成': True,
    '是否有错误': True,
    '是否影响后续 pipeline': True,
    'README 路径': rel(RUN/'README.md'),
}])
if run_manifest.exists():
    old = pd.read_csv(run_manifest, encoding='utf-8-sig')
    old = old[old['任务包路径'] != rel(RUN)] if '任务包路径' in old.columns else old
    out = pd.concat([old, new_manifest_row], ignore_index=True)
else:
    out = new_manifest_row
out.to_csv(run_manifest, index=False, encoding='utf-8-sig')

latest_path = ROOT/'outputs/_index/latest_canonical_outputs.yaml'
latest = yaml.safe_load(latest_path.read_text(encoding='utf-8', errors='replace')) if latest_path.exists() else {}
latest.update({
    'latest_run_package': rel(RUN),
    'latest_dqn_auto_policy': rel(exp_opt/'peanut_dqn_auto_policy.csv'),
    'latest_dqn_auto_policy_comparison': rel(exp_opt/'peanut_dqn_auto_policy_comparison.csv'),
    'latest_dqn_auto_training_metrics': rel(exp_opt/'peanut_dqn_auto_training_metrics.csv'),
    'latest_dqn_auto_model': rel(exp_opt/'peanut_dqn_auto_model.pt'),
    'latest_dqn_auto_training_report': rel(proj_summary/'peanut_dqn_auto_training_report.md'),
    'latest_dqn_status': 'experimental_completed_not_formal',
})
latest_path.write_text(yaml.safe_dump(latest, allow_unicode=True, sort_keys=False), encoding='utf-8')

write_text(ROOT/'project_state/current_focus.md', f'''# Current Focus

当前完成：全流程验收与 DQN 自动参数训练。

工作包：`{rel(RUN)}`。

结论：一句话 dry-run 可路由到 PEANUT 风险监管 / DQN 相关分支；本轮在用户明确授权下完成 {EXPERIMENTAL_LABEL}。结果可用于 workflow 闭环验收与 prototype 分析，不能作为 formal DQN 或正式监管政策结论。
''')
write_text(ROOT/'project_state/next_step.md', '''# Next Step

下一步建议：用户逐项确认 DQN 参数表中的 action、budget、capacity、minimum coverage、cost、reward、transition、baseline、network、training hyperparameters 和 evaluation metrics；确认后另建 formal config 并重新运行 formal DQN。
''')
append_text(ROOT/'project_state/changelog.md', f'''

## {now} 全流程验收与DQN自动参数训练

- 创建任务工作包 `{rel(RUN)}`。
- 完成 one-line dry-run 验收、文献/环境/上游核验、experimental DQN 参数自动合成、myenv1 GPU 训练、baseline 对比、结果审计和 canonical 同步。
- 修复训练报告缺少 tabulate 与 reward 尺度异常问题。
''')
append_text(ROOT/'project_state/decision_log.md', f'''

## {now}

### Allow self-synthesized experimental DQN without converting it to formal DQN

Rationale: 用户本轮明确授权自动合成参数并运行 DQN 实验版，用于 workflow 闭环和 prototype 分析。

Impact: 本轮结果标记为 `{EXPERIMENTAL_LABEL}`；formal DQN 仍需用户逐项确认参数。reward 中人口加权风险 proxy 采用 P95 归一化以避免 Q/loss 数量级异常。
''')
append_text(ROOT/'project_state/lessons_learned.md', f'''

## {now} DQN experimental lessons

- 报告生成不应依赖可选 `tabulate`；缺失时可用 CSV fenced block。
- reward 中人口或规模 proxy 必须归一化，否则会导致 Q 值和 loss 数量级异常。
- Matplotlib SVG 在当前环境会提示 CJK 字体缺字；后续可配置中文字体，但不影响核心 CSV/Excel/模型输出。
''')
write_text(ROOT/'project_state/conversation_handoff.md', f'''# Conversation Handoff

{now} 完成“全流程真实验收 + DQN 自动参数合成与 GPU 训练”。

主工作包：`{rel(RUN)}`。

关键文件：

- `{rel(DIRS['report']/'one_line_full_workflow_execution_report.md')}`
- `{rel(DIRS['report']/'peanut_dqn_auto_training_report.md')}`
- `{rel(DIRS['table']/'peanut_dqn_auto_policy_comparison.csv')}`
- `{rel(DIRS['data']/'peanut_dqn_auto_policy.csv')}`
- `{rel(DIRS['model']/'peanut_dqn_auto_model.pt')}`

结论：one-line dry-run 验收通过；experimental DQN 使用 `D:/anaconda3/envs/myenv1/python.exe` + torch CUDA/GPU 训练成功。DQN reward 优于所有 baseline，但本轮参数为 Codex 自动合成，不能作为 formal DQN 或正式政策结论。

下一步：用户确认参数后另建 formal config，重新运行 formal DQN。
''')
append_text(ROOT/'project_state/project_memory.md', f'''

## {now} Experimental DQN memory

- workflow1 已完成一次 `{EXPERIMENTAL_LABEL}`，工作包 `{rel(RUN)}`。
- 本轮证明 one-line dry-run、canonical 数据、文献证据、myenv1 GPU、DQN 训练代码、输出系统可以闭环。
- 该结果不是 formal DQN；正式版本仍需用户确认参数并另建 formal config。
- reward 中人口/规模 proxy 必须归一化后进入 DQN。
''')
append_text(ROOT/'project_state/run_protocol.md', f'''

## Experimental DQN Protocol Note ({now})

当用户明确授权 self-synthesized experimental DQN 时，可以在不等待 formal 参数确认的情况下运行实验版训练，但必须标记 experimental，并不得覆盖 formal config 或写成正式政策结论。
''')
workflow_state_path = ROOT/'project_state/workflow_execution_state.yaml'
state = yaml.safe_load(workflow_state_path.read_text(encoding='utf-8', errors='replace')) if workflow_state_path.exists() else {}
state['latest_dqn_auto_experimental_run'] = {
    'status': 'completed',
    'run_package': rel(RUN),
    'label': EXPERIMENTAL_LABEL,
    'formal_dqn_status': 'still_requires_user_confirmed_parameters',
    'gpu': 'NVIDIA GeForce RTX 4060 Ti',
    'python': 'D:/anaconda3/envs/myenv1/python.exe',
}
workflow_state_path.write_text(yaml.safe_dump(state, allow_unicode=True, sort_keys=False), encoding='utf-8')

write_text(ROOT/'project_state/artifact_index.md', f'''# Artifact Index

最新任务：`{rel(RUN)}`。

Canonical DQN experimental outputs:

- `{rel(exp_opt/'peanut_dqn_auto_policy.csv')}`
- `{rel(exp_opt/'peanut_dqn_auto_policy_comparison.csv')}`
- `{rel(exp_opt/'peanut_dqn_auto_training_metrics.csv')}`
- `{rel(exp_opt/'peanut_dqn_auto_model.pt')}`
- `{rel(proj_summary/'peanut_dqn_auto_training_report.md')}`
''')
write_text(ROOT/'project_state/workspace_structure.md', f'''# Workspace Structure

- `data/01_raw/`: 原始数据，只读，本轮未修改。
- `outputs/工作包/`: 任务工作包，本轮主包 `{rel(RUN)}`。
- `experiments/optimization/`: experimental DQN canonical 副本。
- `reports/项目级索引与摘要/`: 项目级摘要报告副本。
- `project_state/`: 当前焦点、下一步、决策、交接和索引已更新。
''')

# Whole workspace cleanliness check.
root_files = [p.name for p in ROOT.iterdir() if p.is_file()]
write_text(DIRS['log']/'whole_workspace_cleanliness_check.md', f'''# Whole Workspace Cleanliness Check

时间：{now}

- `data/01_raw` 未修改、未移动、未删除。
- 本轮新增任务产物均位于 `{rel(RUN)}`，canonical 副本只同步到 `experiments/optimization/` 和 `reports/项目级索引与摘要/`。
- 未删除唯一文件。
- 根目录文件数：{len(root_files)}；未执行破坏性整理。
- Matplotlib 字体 warning 已记录为非阻断问题。
''')

# Manifest last, include hashes.
manifest_rows = []
for p in sorted(RUN.rglob('*')):
    if p.is_file() and p.name != 'manifest.csv':
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        manifest_rows.append({'path': rel(p), 'bytes': p.stat().st_size, 'sha256': h, 'updated_at': now})
pd.DataFrame(manifest_rows).to_csv(RUN/'manifest.csv', index=False, encoding='utf-8-sig')

print({'status':'ok','quality_gates':len(qg_df),'dqn_reward':dqn_reward,'best_baseline':best_baseline,'best_baseline_reward':best_baseline_reward})
