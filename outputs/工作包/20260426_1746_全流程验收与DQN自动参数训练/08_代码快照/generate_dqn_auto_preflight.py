from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import math
import os
import re
import shutil

import pandas as pd
import yaml
from docx import Document

from workflow1.pipelines.optimization.peanut_dqn_env_auto import (
    EXPERIMENTAL_LABEL,
    build_field_mapping,
    prepare_state_matrix,
    synthesize_budget_and_capacity,
)

ROOT = Path('D:/桌面/codex/workflow1')
RUN = ROOT / 'outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练'
DIRS = {
    'input': RUN / '00_输入说明',
    'data': RUN / '01_数据输出',
    'table': RUN / '02_表格输出',
    'fig': RUN / '03_图表输出',
    'report': RUN / '04_报告输出',
    'model': RUN / '05_模型与实验',
    'config': RUN / '06_配置参数',
    'log': RUN / '07_日志与错误',
    'code': RUN / '08_代码快照',
}
for p in DIRS.values():
    p.mkdir(parents=True, exist_ok=True)

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def safe_read(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ''
    text = path.read_text(encoding='utf-8', errors='replace')
    return text if limit is None else text[:limit]


def extract_docx(path: Path) -> str:
    if not path.exists():
        return ''
    doc = Document(str(path))
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return '\n'.join(paras)

# 1. Dry-run validation outputs.
dry_runs = [
    {
        'goal': '启动 PEANUT 食品安全风险监管全流程',
        'matched_intent': 'peanut_food_safety_full_workflow',
        'selected_recipe': 'workflow_recipes/one_line_research_dry_run.yaml',
        'selected_task_type': 'PEANUT food-safety risk monitoring full workflow dry-run',
        'selected_model_family': 'risk monitoring + belief-MDP + experimental DQN branch candidate',
        'planned_stages': 'read memory/references; verify canonical cleaned/risk/belief outputs; audit concentration/MOE/EDI; route prototype/experimental optimization; generate report',
        'skills_to_call': 'goal-driven-research-orchestrator; upstream-output-auditor; concentration-cleaning-auditor; zotero-literature-auditor; document-governed-modeling; dqn-readiness-auditor',
        'quality_gates': 'raw read-only; upstream verification; experimental label; run package outputs; no formal claims',
        'stop_conditions': 'canonical unreadable; state/action/reward cannot be built; myenv1/GPU unavailable; raw-data damage risk',
        'expected_outputs': 'validation report; evidence matrix; config; policy/baseline/training outputs; audit report',
        'can_auto_enter_dqn_branch': 'yes_for_this_explicit_experimental_task',
        'blockers': 'formal DQN still blocked without user-confirmed parameters; experimental DQN explicitly authorized here',
        'dry_run_status': 'ok',
    },
    {
        'goal': '按照已确认参数运行正式 DQN',
        'matched_intent': 'formal_dqn_guarded_plan',
        'selected_recipe': 'workflow_recipes/one_line_research_dry_run.yaml',
        'selected_task_type': 'formal DQN guarded dry-run',
        'selected_model_family': 'DQN / constrained RL',
        'planned_stages': 'read confirmed parameter table; verify no draft config; verify myenv1 torch/CUDA; verify upstream state features; block unless all formal parameters confirmed',
        'skills_to_call': 'document-governed-modeling; zotero-literature-auditor; environment-auditor; dqn-readiness-auditor; upstream-output-auditor',
        'quality_gates': 'confirmed formal params; myenv1 GPU smoke test; upstream verification; no draft config',
        'stop_conditions': 'unconfirmed formal parameters; GPU unavailable; upstream blockers',
        'expected_outputs': 'formal readiness report or formal run only after confirmation',
        'can_auto_enter_dqn_branch': 'no_for_formal; yes_only_as_separately_authorized_experimental_run',
        'blockers': 'formal parameter confirmation required by standing policy',
        'dry_run_status': 'ok_blocked_by_design',
    },
    {
        'goal': '根据当前研究目标自动选择模型并运行 prototype',
        'matched_intent': 'model_selection_prototype_plan',
        'selected_recipe': 'workflow_recipes/one_line_research_dry_run.yaml',
        'selected_task_type': 'prototype model selection plan',
        'selected_model_family': 'model-agnostic baseline first; RL/DQN if optimization framing is selected',
        'planned_stages': 'inspect objective; classify task family; choose transparent baseline; generate prototype execution plan; define metrics',
        'skills_to_call': 'ml-problem-framer; method-selector; baseline-trainer; dqn-readiness-auditor',
        'quality_gates': 'target/unit/leakage check; baseline comparison; experimental label if RL prototype',
        'stop_conditions': 'target/action/reward cannot be defined; missing upstream data',
        'expected_outputs': 'prototype plan and metric contract',
        'can_auto_enter_dqn_branch': 'conditional_if_optimization_goal_and_state_action_reward_are_available',
        'blockers': 'dry-run itself does not execute prototype; current long prompt provides explicit DQN experimental execution authorization',
        'dry_run_status': 'ok',
    },
    {
        'goal': '优化当前工作流',
        'matched_intent': 'workflow_self_improvement',
        'selected_recipe': 'workflow_recipes/workflow_self_improvement.yaml + workflow_recipes/one_line_research_dry_run.yaml',
        'selected_task_type': 'safe workflow self-improvement dry-run',
        'selected_model_family': 'not applicable; workflow upgrade route',
        'planned_stages': 'create run package; scan local capabilities; search watchlist/GitHub if needed; apply low-risk local upgrades; write approval queue; run skills doctor; update state',
        'skills_to_call': 'workflow-self-improvement-scout; workflow-gap-analyzer; github-skill-scout-and-adapter; safe-workflow-upgrade-planner; external-plugin-approval-manager',
        'quality_gates': 'no unknown third-party code execution; no MCP/API/plugin install without approval; ledger update',
        'stop_conditions': 'requires external install/API key/Zotero DB write/large dependency',
        'expected_outputs': 'improvement ledger; approval queue; dry-run report',
        'can_auto_enter_dqn_branch': 'not_applicable',
        'blockers': 'none for dry-run',
        'dry_run_status': 'ok',
    },
]
dry_df = pd.DataFrame(dry_runs)
dry_df.to_csv(DIRS['table'] / 'one_line_to_dqn_dry_run_results.csv', index=False, encoding='utf-8-sig')
write_text(DIRS['report'] / 'one_line_to_dqn_workflow_validation_report.md', f'''# 一句话到 DQN 工作流验收报告

任务性质：{EXPERIMENTAL_LABEL}

## 结论

4 条 dry-run 均能产生结构化路由。PEANUT 全流程能够自动识别到 belief-MDP / DQN 相关分支；formal DQN 路径按历史规则保持 blocked。本轮用户显式授权“自动合成参数 DQN 实验版”，因此可以在不冒充 formal DQN 的前提下继续训练。

## dry-run 结果摘要

{dry_df[['goal','matched_intent','selected_model_family','can_auto_enter_dqn_branch','blockers']].to_csv(index=False)}

## 低风险修复记录

- PowerShell dry-run 日志出现控制台编码显示问题，但 CLI route/status 字段完整，已改用 UTF-8 CSV/Markdown 固化结果。
- formal DQN blocked 是设计门控，不作为本轮 experimental DQN 停止条件。
''')

# 2. Evidence and literature recheck.
plan_doc = ROOT / 'references/notes/物流与供应链管理前言-研究计划-肖宇航.docx'
plan_text = extract_docx(plan_doc)
summary_text = safe_read(ROOT / 'references/processed_summaries/dqn_model_spec_summary.md')
model_spec = safe_read(ROOT / 'project_state/dqn_model_spec_from_document.yaml')
confirm_table_path = ROOT / 'project_state/dqn_parameter_confirmation_table.csv'
confirm_df = pd.read_csv(confirm_table_path, encoding='utf-8-sig') if confirm_table_path.exists() else pd.DataFrame()
prev_dir = ROOT / 'outputs/工作包/20260426_1616_DQN文献增强建模方案与参数确认'
prev_plan = safe_read(prev_dir / '04_报告输出/dqn_literature_enhanced_modeling_plan.md')

zotero_root = Path('D:/桌面/codex/zotero')
zotero_files = list((zotero_root / 'data/deepreads').glob('*.md')) if zotero_root.exists() else []
zotero_rows = []
for zp in zotero_files:
    txt = safe_read(zp, 50000)
    zotero_rows.append({
        'path': str(zp),
        'has_garbled_question_marks': '?????' in txt,
        'has_replacement_char': '\ufffd' in txt,
        'mentions_dqn_or_rl': bool(re.search(r'DQN|reinforcement|强化|Q-learning|safe RL', txt, re.I)),
        'chars_read': len(txt),
    })
zotero_audit = pd.DataFrame(zotero_rows)
zotero_audit.to_csv(DIRS['table'] / 'zotero_recheck_inventory.csv', index=False, encoding='utf-8-sig')

web_sources = [
    {'source': 'Nature 2015 Mnih et al.', 'url': 'https://www.nature.com/articles/nature14236', 'use': 'DQN method basis: Q-network, replay, target network, epsilon-greedy convention'},
    {'source': 'JMLR 2015 Garcia and Fernandez', 'url': 'https://jmlr.org/beta/papers/v16/garcia15a.html', 'use': 'safe RL framing: constraints and safety during learning/deployment'},
    {'source': 'EFSA 2020 aflatoxins risk assessment', 'url': 'https://www.efsa.europa.eu/en/efsajournal/pub/6040', 'use': 'AFB1 exposure/MOE risk assessment background'},
    {'source': 'EFSA aflatoxins topic page', 'url': 'https://www.efsa.europa.eu/en/topics/topic/aflatoxins-food', 'use': 'aflatoxins in peanuts and MOE/regulatory risk context'},
]

# 3. Upstream data validation and parameter synthesis.
state_path = ROOT / 'data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv'
base_state_path = ROOT / 'data/04_feature/peanut_belief_mdp_state_features.csv'
belief_path = ROOT / 'data/04_feature/peanut_beta_binomial_belief_states.csv'
count_path = ROOT / 'data/04_feature/peanut_count_panel.csv'
risk_path = ROOT / 'data/04_feature/peanut_edi_moe_risk_table.csv'
risk_summary_path = ROOT / 'data/04_feature/peanut_edi_moe_risk_summary.csv'
required_files = [base_state_path, state_path, belief_path, count_path, risk_path, risk_summary_path]
file_rows = []
for fp in required_files:
    row = {'file': str(fp.relative_to(ROOT)), 'exists': fp.exists(), 'readable': False, 'rows': None, 'columns': None, 'issue': ''}
    try:
        df0 = pd.read_csv(fp, encoding='utf-8-sig')
        row.update({'readable': True, 'rows': len(df0), 'columns': len(df0.columns)})
    except Exception as e:
        row['issue'] = str(e)
    file_rows.append(row)
file_df = pd.DataFrame(file_rows)
file_df.to_csv(DIRS['table'] / 'dqn_state_feature_validation_table.csv', index=False, encoding='utf-8-sig')

state_df = pd.read_csv(state_path, encoding='utf-8-sig')
count_df = pd.read_csv(count_path, encoding='utf-8-sig')
mapping = build_field_mapping(state_df)
map_rows = [{'logical_field': k, 'source_column': v, 'status': 'mapped' if v else 'missing'} for k, v in mapping.items()]
map_df = pd.DataFrame(map_rows)
map_df.to_csv(DIRS['table'] / 'dqn_state_feature_field_mapping.csv', index=False, encoding='utf-8-sig')

budget_capacity = synthesize_budget_and_capacity(state_df, mapping)
local_capacity = budget_capacity['local_capacity_p90']
stage_capacity = budget_capacity['stage_capacity_p75']
global_capacity = budget_capacity['global_capacity_p75']

actions = [0, 1, 3, 5, 10]
if state_df[mapping['total_count']].quantile(0.90) < 5:
    actions = [0, 1, 2, 3, 5]

def cols(*names):
    return [mapping[n] for n in names if mapping.get(n)]
state_features = [
    'posterior_mean', 'posterior_var', 'afb1_posterior_mean', 'afb1_posterior_var',
    'total_count', 'fail_count', 'afb1_count', 'afb1_fail_count', 'concentration_count',
    'edi_mean', 'edi_p95', 'moe_min', 'moe_penalty', 'population_risk', 'population',
]
state_features = [f for f in state_features if mapping.get(f) in state_df.columns]

config = {
    'experiment': {
        'id': 'peanut_dqn_auto_20260426_1746',
        'label': EXPERIMENTAL_LABEL,
        'prototype_vs_formal': 'experimental_not_formal',
        'created_at': now,
    },
    'paths': {
        'run_package': str(RUN),
        'state_features': str(state_path.relative_to(ROOT)),
        'data_dir': str(DIRS['data']),
        'table_dir': str(DIRS['table']),
        'figure_dir': str(DIRS['fig']),
        'report_dir': str(DIRS['report']),
        'model_dir': str(DIRS['model']),
        'config_dir': str(DIRS['config']),
        'log_dir': str(DIRS['log']),
    },
    'state_space': {
        'unit_of_analysis': 'province-year_month-supply_chain_stage',
        'features': state_features,
        'field_mapping': mapping,
        'missing_value_policy': 'numeric NaN filled with 0 or median for MOE/EDI/risk proxy; recorded in reports',
    },
    'action_space': {
        'increments': actions,
        'meaning': {
            0: '维持/不增加抽检', 1: '低强度增加', 3: '常规加密抽检', 5: '重点加密抽检', 10: '重点专项抽检',
        },
        'experimental': True,
    },
    'constraints': {
        'monthly_budget': budget_capacity['experimental_monthly_budget'],
        'budget_p50': budget_capacity['monthly_total_p50'],
        'budget_p75': budget_capacity['monthly_total_p75'],
        'budget_p90': budget_capacity['monthly_total_p90'],
        'local_capacity': local_capacity,
        'stage_capacity': stage_capacity,
        'global_capacity': global_capacity,
        'minimum_coverage': 'top-risk cells prioritized; each stage keeps low positive allocation when feasible; relaxed by action mask if infeasible',
    },
    'reward': {
        'formula': 'risk_reward_weight * risk_coverage_gain + info_gain_weight * information_gain - cost_weight * sampling_cost - constraint_penalty_weight * constraint_violation',
        'risk_reward_weight': 1.0,
        'info_gain_weight': 0.3,
        'cost_weight': 0.1,
        'constraint_penalty_weight': 2.0,
        'unit_sampling_cost': 1.0,
    },
    'transition': {
        'type': 'historical_replay_plus_beta_binomial_uncertainty_proxy',
        'causal_claim': False,
        'belief_update': 'Beta-Binomial posterior features are replayed; action affects reward/information-gain proxy only in this experimental run',
    },
    'baselines': ['uniform_allocation', 'historical_allocation', 'risk_ranking_top_k', 'random_policy', 'dqn_policy'],
    'network': {'type': 'MLP', 'hidden_layers': [128, 64], 'activation': 'ReLU'},
    'training': {
        'learning_rate': 0.001,
        'gamma': 0.95,
        'epsilon_start': 1.0,
        'epsilon_min': 0.05,
        'epsilon_decay': 0.995,
        'replay_buffer_size': 10000,
        'batch_size': 64,
        'target_update_frequency': 100,
        'episodes': 120,
        'random_seed': 42,
        'device_required': 'cuda',
        'gpu_required': 'NVIDIA GeForce RTX 4060 Ti',
    },
    'quality_gates': ['cuda_available', 'state_policy_row_coverage', 'baseline_comparison', 'non_degenerate_action_distribution', 'all_outputs_written', 'experimental_label_present'],
}
config_path = DIRS['config'] / 'dqn_auto_synthesized_config.yaml'
with config_path.open('w', encoding='utf-8') as f:
    yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)

source_map = {
    'user_document': str(plan_doc.relative_to(ROOT)),
    'local_summaries': ['references/processed_summaries/dqn_model_spec_summary.md', 'project_state/dqn_model_spec_from_document.yaml', 'project_state/dqn_parameter_confirmation_table.csv'],
    'previous_run_package': str(prev_dir.relative_to(ROOT)),
    'zotero_root_read_only': str(zotero_root),
    'web_sources': web_sources,
    'data_distribution': {k: v for k, v in budget_capacity.items() if not isinstance(v, dict)},
    'experimental_note': 'All synthesized parameters require user confirmation before formal DQN.',
}
with (DIRS['config'] / 'dqn_auto_parameter_source_map.yaml').open('w', encoding='utf-8') as f:
    yaml.safe_dump(source_map, f, allow_unicode=True, sort_keys=False)

param_rows = []
def add_param(name, value, source, rationale, formal_confirm='yes'):
    param_rows.append({
        'parameter': name,
        'auto_synthesized_value': json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value,
        'source_basis': source,
        'rationale': rationale,
        'experimental_label': EXPERIMENTAL_LABEL,
        'formal_version_still_requires_user_confirmation': formal_confirm,
    })

add_param('state_features', state_features, '用户研究计划 + canonical belief-MDP/MOE-EDI 状态表', '覆盖省份-年月-供应链环节、posterior、不合格计数、AFB1、MOE/EDI 与人口风险 proxy。')
add_param('action_space', actions, '用户本轮指定优先动作空间 + 历史抽检分布', '小型离散动作避免组合爆炸；当前历史分布可容纳最高动作。')
add_param('monthly_budget', config['constraints']['monthly_budget'], '当前数据分布 P75', f"历史每月抽检总批次数 P50={budget_capacity['monthly_total_p50']:.1f}, P75={budget_capacity['monthly_total_p75']:.1f}, P90={budget_capacity['monthly_total_p90']:.1f}。")
add_param('local_capacity', 'province_stage_P90', '当前数据分布', '省份 × 供应链环节历史抽检批次数 P90，样本不足时回退到 stage/global P75。')
add_param('unit_sampling_cost', 1.0, '用户本轮指定 + 相对成本实验惯例', '无外部成本时使用相对成本单位，便于 prototype 比较。')
add_param('minimum_coverage', config['constraints']['minimum_coverage'], '用户本轮指定 + safe RL 约束思想', 'top-risk 优先，每环节尽量保留覆盖，不可行时通过 action mask 放宽。')
for k in ['risk_reward_weight','info_gain_weight','cost_weight','constraint_penalty_weight']:
    add_param(k, config['reward'][k], '用户建议初值 + experimental reward shaping', '保持风险收益主导，信息价值为辅助，成本和违约惩罚抑制过度抽检。')
add_param('transition', config['transition'], '用户本轮指定 + 当前数据缺少真实干预轨迹', '采用 historical replay + Beta-Binomial uncertainty proxy，不做因果干预声称。')
add_param('baselines', config['baselines'], '用户本轮指定 + 模型评估惯例', '至少比较 uniform、historical、risk-ranking、random 和 DQN。')
add_param('network', config['network'], 'DQN 文献惯例 + 当前状态维度较小', 'MLP [128,64] 足以覆盖结构化状态特征，不采用图像 CNN。')
add_param('training_hyperparameters', config['training'], 'DQN 文献惯例 + GPU/数据规模', '1710 状态、GPU 可用；episodes 从建议 300 调整到 120 以适配实验版快速闭环。')
param_df = pd.DataFrame(param_rows)
param_df.to_csv(DIRS['table'] / 'dqn_auto_synthesized_parameter_table.csv', index=False, encoding='utf-8-sig')

matrix_topics = ['state','action','budget','capacity','minimum coverage','sampling cost','recall/disposal loss','risk loss','information value','reward','transition','belief update','episode','baseline','network','training hyperparameters','evaluation metrics','visualization outputs']
evidence_rows = []
for topic in matrix_topics:
    evidence_rows.append({
        'topic': topic,
        'user_document_basis': '研究计划提供风险监管/供应链/抽检优化方向；多处为 conceptual_only，未给数值参数。',
        'zotero_pdf_basis': '本地 deepread/上一轮文献增强方案支持 DQN、safe RL、食品风险监测；乱码 note 不作为正式依据。',
        'web_literature_basis': '; '.join([f"{s['source']} ({s['url']})" for s in web_sources]),
        'current_data_basis': f"state rows={len(state_df)}, count panel rows={len(count_df)}, monthly budget P75={budget_capacity['monthly_total_p75']:.1f}",
        'auto_synthesized_parameter': param_df[param_df['parameter'].str.contains(topic.split('/')[0].split()[0], case=False, regex=False)]['auto_synthesized_value'].head(1).to_list(),
        'experimental_assumption': 'yes',
        'formal_confirmation_required': 'yes',
    })
evidence_df = pd.DataFrame(evidence_rows)
evidence_df.to_csv(DIRS['table'] / 'dqn_evidence_matrix_for_auto_parameters.csv', index=False, encoding='utf-8-sig')

write_text(DIRS['report'] / 'dqn_evidence_recheck_report.md', f'''# DQN 证据复核报告

任务性质：{EXPERIMENTAL_LABEL}

## 已读取/查验

- 用户研究计划：`{plan_doc.relative_to(ROOT)}`，提取字符数 {len(plan_text)}。
- 本地模型摘要：`references/processed_summaries/dqn_model_spec_summary.md`。
- 项目模型 spec：`project_state/dqn_model_spec_from_document.yaml`。
- 参数确认表：`project_state/dqn_parameter_confirmation_table.csv`，行数 {len(confirm_df)}。
- 上一轮 DQN 文献增强工作包：`{prev_dir.relative_to(ROOT)}`。
- Zotero 目录只读扫描：`{zotero_root}`，deepread 文件数 {len(zotero_files)}。

## 证据优先级

用户研究计划优先；Zotero/PDF 和联网文献用于补充；当前数据分布用于预算、产能和状态可用性；Codex 自动合成参数全部标记为 experimental。

## 乱码 note 处理

Zotero deepread 中检测到 `?????` 的文件数：{int(zotero_audit['has_garbled_question_marks'].sum()) if not zotero_audit.empty else 0}。这些 note 不作为 formal evidence。
''')

lit_lines = ['# DQN 文献支持摘要', '', f'任务性质：{EXPERIMENTAL_LABEL}', '']
for src in web_sources:
    lit_lines.append(f"- [{src['source']}]({src['url']}): {src['use']}")
lit_lines += ['', '本地 Zotero/PDF/processed summaries 用于补充；若 note 出现乱码，仅作为线索，不作为正式依据。']
write_text(DIRS['report'] / 'dqn_literature_support_summary.md', '\n'.join(lit_lines) + '\n')

write_text(DIRS['report'] / 'dqn_environment_final_validation_report.md', f'''# DQN 环境最终复核报告

任务性质：{EXPERIMENTAL_LABEL}

复核命令均显式使用 `D:/anaconda3/envs/myenv1/python.exe`。

结论：myenv1 可用，workflow1 可导入，torch 为 `2.11.0+cu126`，CUDA 版本 `12.6`，`torch.cuda.is_available()` 为 True，GPU 为 `NVIDIA GeForce RTX 4060 Ti`。核心包 numpy/pandas/sklearn/matplotlib/openpyxl/xlsxwriter/yaml/gymnasium 可导入。

自动修复：第一次 PowerShell `Start-Process -ArgumentList` 数组传参导致 `-c` 代码被拆分；已改为参数字符串重跑。workflow1 import 失败时已按用户规则执行 editable install，复核通过。
''')

missing_summary = state_df[[c for c in state_features if c in state_df.columns]].isna().sum().reset_index()
missing_summary.columns = ['feature', 'missing_count']
missing_summary.to_csv(DIRS['table'] / 'dqn_state_feature_missing_summary.csv', index=False, encoding='utf-8-sig')

alignment = count_df.merge(state_df[[mapping['province'], mapping['year_month'], mapping['stage']]], on=[mapping['province'], mapping['year_month'], mapping['stage']], how='outer', indicator=True)
alignment_counts = alignment['_merge'].value_counts().to_dict()
write_text(DIRS['report'] / 'dqn_upstream_data_validation_report.md', f'''# DQN 上游数据核验报告

任务性质：{EXPERIMENTAL_LABEL}

## 文件可读性

{file_df.to_csv(index=False)}

## 核心状态表

- 使用状态表：`{state_path.relative_to(ROOT)}`
- 行数：{len(state_df)}
- 列数：{len(state_df.columns)}
- 省份字段：`{mapping['province']}`
- 年月字段：`{mapping['year_month']}`
- 供应链环节字段：`{mapping['stage']}`
- posterior mean：`{mapping['posterior_mean']}`
- posterior variance：`{mapping['posterior_var']}`
- AFB1 posterior：`{mapping['afb1_posterior_mean']}`, `{mapping['afb1_posterior_var']}`
- MOE/EDI：`{mapping['edi_mean']}`, `{mapping['edi_p95']}`, `{mapping['moe_penalty']}`
- 人口/人口风险：`{mapping['population']}`, `{mapping['population_risk']}`

## 计数面板对齐

merge 结果：{alignment_counts}。

## 缺失处理

MOE/EDI 在无浓度状态存在自然缺失；本轮 experimental DQN 使用 0 或中位数填补并记录，不删除状态。

结论：核心状态特征可构建，适合本轮 experimental DQN 训练；不适合作为 formal DQN 结论。
''')

write_text(DIRS['report'] / 'dqn_auto_parameter_synthesis_report.md', f'''# DQN 自动参数合成报告

任务性质：{EXPERIMENTAL_LABEL}

本轮所有 DQN 参数均由 Codex 在用户明确授权 experimental run 的前提下自动合成。它们不是用户确认参数，也不能转写为 formal config。

## 关键参数

- 动作空间：{actions}
- 月预算：{config['constraints']['monthly_budget']}（历史每月抽检总批次数 P75）
- 局部产能：省份 × 供应链环节历史 P90
- 成本：unit_sampling_cost = 1.0
- reward：{config['reward']['formula']}
- transition：historical replay + Beta-Binomial uncertainty proxy
- 网络：MLP {config['network']['hidden_layers']}
- 训练：episodes={config['training']['episodes']}, lr={config['training']['learning_rate']}, gamma={config['training']['gamma']}, batch_size={config['training']['batch_size']}

正式版本仍需用户确认 action、budget、capacity、minimum coverage、cost、reward weights、transition、baseline、network 与训练超参数。
''')

print(json.dumps({'status': 'ok', 'config': str(config_path), 'state_rows': len(state_df), 'budget': config['constraints']['monthly_budget']}, ensure_ascii=False))
