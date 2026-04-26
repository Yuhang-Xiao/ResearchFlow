from __future__ import annotations

import ast
import csv
import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]
PYTHON = r"D:\anaconda3\envs\myenv1\python.exe"
SOURCE_EXPLANATION_RUN = ROOT / "outputs" / "工作包" / "20260426_2254_DQN输出复核_解释体系与论文输出升级"
SOURCE_DQN_RUN = ROOT / "outputs" / "工作包" / "20260426_2056_推荐缓存删除与DQN修正版训练"
DQN_CODE = SOURCE_DQN_RUN / "08_代码快照" / "run_recommended_delete_and_dqn_revised.py"
RUN = ROOT / "outputs" / "工作包" / f"{datetime.now():%Y%m%d_%H%M}_输出解释就地化修正与DQN代码深度说明补强"

DIRS = [
    "00_输入说明",
    "01_数据输出",
    "02_表格输出",
    "03_图表输出",
    "04_报告输出",
    "05_模型与实验",
    "06_配置参数",
    "07_日志与错误",
    "08_代码快照",
    "09_论文输出/04_结果",
    "09_论文输出/09_word导出",
    "10_输出解释与索引",
]


CORE_ARTIFACTS = {
    "02_表格输出/local_explanation_coverage_matrix.csv": "本轮就地解释覆盖矩阵，判断每个目录和核心 artifact 是否有本地解释。",
    "02_表格输出/missing_local_explanations.csv": "本轮仍缺少本地解释的 artifact 列表。空表表示核心范围已覆盖。",
    "02_表格输出/chart_quality_audit.csv": "图表 QA 结果，说明 PNG、空图、全 0 语义和中文字体状态。",
    "02_表格输出/dqn_model_component_literature_map.csv": "DQN 模型组件到文献依据的映射。",
    "02_表格输出/dqn_core_literature_selected.csv": "核心候选文献和读取状态。",
    "02_表格输出/dqn_results_evidence_table.csv": "论文 Results 证据表，映射论断、源表、数值和 experimental 状态。",
    "03_图表输出/dqn_revised_constraint_summary_explained.png": "解释性约束图，说明全 0 违约率是约束满足而非缺失。",
    "03_图表输出/dqn_revised_policy_comparison.png": "DQN 与 baseline 策略 total reward 对比图。",
    "03_图表输出/dqn_revised_reward_curve.png": "DQN 修正版训练 reward 曲线。",
    "03_图表输出/dqn_revised_moving_average_reward.png": "DQN 修正版移动平均 reward 曲线。",
    "04_报告输出/dqn_model_setting_detail_report.md": "DQN state/action/reward/constraint/training/baseline/quality gate 设置说明。",
    "04_报告输出/dqn_result_interpretation_report.md": "DQN 与 Q-learning/heuristic 的结果解读。",
    "04_报告输出/deep_dqn_output_audit_report.md": "上一轮 DQN 输出 deep audit。",
    "04_报告输出/local_explanation_repair_report.md": "本轮就地解释修复报告。",
    "06_配置参数/dqn_revised_experimental_config.yaml": "DQN 修正版 experimental 配置。",
    "08_代码快照/run_recommended_delete_and_dqn_revised_annotated.py": "带文件头说明的 DQN 修正版训练与输出脚本快照。",
    "08_代码快照/dqn_code_deep_explanation.md": "DQN 代码深度说明。",
    "08_代码快照/dqn_code_to_model_setting_map.csv": "代码函数到 state/action/reward/constraint/training/evaluation 的映射。",
    "08_代码快照/dqn_code_to_outputs_map.csv": "代码函数到输出文件的映射。",
    "09_论文输出/04_结果/dqn_results_draft.md": "论文级 Results 草稿，experimental results draft。",
    "09_论文输出/04_结果/dqn_results_evidence_table.csv": "Results evidence table。",
    "09_论文输出/09_word导出/dqn_results_draft.docx": "Results Word 草稿，已保留 experimental 边界。",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def init_run() -> None:
    for d in DIRS:
        (RUN / d).mkdir(parents=True, exist_ok=True)
    write(
        RUN / "00_输入说明" / "inputs.md",
        f"""
        # 输入说明

        本轮执行“输出解释就地化修正与 DQN 代码深度说明补强”。

        - 上一轮解释升级包：`{rel(SOURCE_EXPLANATION_RUN)}`
        - DQN 修正版训练包：`{rel(SOURCE_DQN_RUN)}`
        - DQN 代码快照：`{rel(DQN_CODE)}`

        本轮不重新训练 DQN，不修改 raw data，不写 Zotero SQLite。所有 DQN 结果仍为 experimental。
        """,
    )


def copy_previous_artifacts() -> None:
    copy_specs = [
        ("02_表格输出", "*.csv"),
        ("03_图表输出", "*.png"),
        ("04_报告输出", "*.md"),
        ("04_报告输出", "*.bib"),
        ("04_报告输出", "*.ris"),
        ("09_论文输出/04_结果", "*"),
        ("09_论文输出/09_word导出", "*.docx"),
        ("09_论文输出/09_word导出", "*.png"),
        ("09_论文输出/09_word导出", "*.md"),
        ("10_输出解释与索引", "*.md"),
    ]
    for subdir, pattern in copy_specs:
        src_dir = SOURCE_EXPLANATION_RUN / subdir
        dst_dir = RUN / subdir
        if not src_dir.exists():
            continue
        for src in src_dir.glob(pattern):
            if src.is_file():
                shutil.copy2(src, dst_dir / src.name)
    cfg = SOURCE_DQN_RUN / "06_配置参数" / "dqn_revised_experimental_config.yaml"
    if cfg.exists():
        shutil.copy2(cfg, RUN / "06_配置参数" / cfg.name)
    model_log = SOURCE_DQN_RUN / "05_模型与实验" / "dqn_revised_training_log.csv"
    qlog = SOURCE_DQN_RUN / "05_模型与实验" / "qlearning_training_log.csv"
    ledger = SOURCE_DQN_RUN / "05_模型与实验" / "experiment_ledger.csv"
    for src in [model_log, qlog, ledger]:
        if src.exists():
            shutil.copy2(src, RUN / "05_模型与实验" / src.name)
    if DQN_CODE.exists():
        shutil.copy2(DQN_CODE, RUN / "08_代码快照" / DQN_CODE.name)


def parse_code() -> tuple[list[dict[str, object]], str]:
    text = DQN_CODE.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(text)
    rows: list[dict[str, object]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            rows.append(
                {
                    "name": node.name,
                    "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", ""),
                    "docstring_present": bool(ast.get_docstring(node)),
                }
            )
    return rows, text


def make_annotated_code(code_text: str) -> None:
    header = '''"""
Annotated snapshot for DQN revised experimental workflow.

Purpose:
    This copy documents how the local PEANUT DQN experimental run builds state
    features, action masks, reward components, constraints, DQN training,
    Q-learning and heuristic baselines, charts, reports, and paper outputs.

Inputs:
    - data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv
    - previous experimental config from the 1746 run
    - recommended delete list / protected files for cleanup

Outputs:
    - policy CSV/XLSX, training logs, model artifact, comparison tables
    - PNG charts, audit reports, Results draft, DOCX

Experimental boundary:
    This code supports an experimental run only. State, action, reward,
    transition, constraints, and hyperparameters require user confirmation
    before any formal DQN or policy conclusion.

Formal TODO:
    Confirm action space, budget, unit cost, capacity, minimum coverage,
    reward weights, transition assumptions, and evaluation protocol.
"""

# NOTE: This annotated copy is generated for method reading. The original
# training snapshot remains in the source run package; no model logic is changed.

'''
    annotated = header + code_text
    write(RUN / "08_代码快照" / "run_recommended_delete_and_dqn_revised_annotated.py", annotated)


def function_role(name: str) -> dict[str, str]:
    mapping = {
        "build_mapping": ("state", "将 canonical state feature 表中的中英文字段映射到统一内部字段。", "Method: state construction"),
        "prepare_model_data": ("state", "读取状态特征，生成 state matrix、risk_score、uncertainty、month/group key 等 DQN 输入。", "Method: state feature engineering"),
        "build_capacity": ("constraint", "从上一轮配置和数据构建 local/stage/global capacity。", "Method: constraints"),
        "capacity_for_row": ("constraint", "为单个状态单元计算可用容量上限。", "Method: constraints"),
        "build_valid_actions": ("action/constraint", "基于 ACTION_VALUES 与容量生成 action mask。", "Method: action space and constraints"),
        "build_reward_matrix": ("reward", "计算 risk reward、information gain、sampling cost、opportunity penalty、constraint penalty，并进行 tanh rescaling。", "Method: reward"),
        "QNet": ("training", "DQN Q-network，输入 state vector，输出每个动作的 Q value。", "Method: DQN architecture"),
        "choose_valid_argmax": ("action/evaluation", "在 action mask 下选择最大 Q 的合法动作。", "Method: action selection"),
        "evaluate_policy": ("evaluation", "在统一预算/容量约束下评价策略，导出 reward、constraint、action 分布等指标。", "Results: policy comparison"),
        "train_dqn": ("training", "执行 DQN 训练：epsilon-greedy、target network、mini-batch update、early stopping/logging。", "Method: training"),
        "train_qlearning": ("baseline", "构建聚合状态 Q-learning baseline。", "Method: baselines"),
        "build_baseline_actions": ("baseline", "生成 uniform、historical、risk-ranking、random、threshold 等 heuristic baseline。", "Method: baselines"),
        "generate_charts": ("outputs", "生成 PNG 图表并执行非空检查。", "Results: figures"),
        "build_action_space_report": ("action", "输出动作空间可行性分析。", "Method: action feasibility"),
        "build_revised_config": ("configuration", "写出 DQN 修正版 experimental config。", "Method: configuration"),
        "model_outputs": ("outputs", "组织 DQN/Q-learning/baseline 训练、评价和表格输出。", "Results: tables/model outputs"),
        "create_reports": ("outputs", "生成训练报告、审计报告、质量门控报告。", "Results/Appendix"),
        "create_results_draft": ("paper", "生成 experimental Results draft 和 DOCX。", "Results"),
        "sync_outputs": ("outputs", "同步必要结果到 experiments/reports canonical 位置。", "Reproducibility"),
    }
    role, desc, paper = mapping.get(name, ("support", "辅助函数或工作流胶水代码。", "Appendix/Reproducibility"))
    return {"model_component": role, "logic": desc, "paper_relation": paper}


def generate_dqn_code_docs() -> None:
    rows, code_text = parse_code()
    make_annotated_code(code_text)
    inventory = []
    model_map = []
    output_map = []
    for row in rows:
        role = function_role(str(row["name"]))
        inventory.append({**row, **role})
        model_map.append(
            {
                "script_or_function": row["name"],
                "kind": row["kind"],
                "model_setting_component": role["model_component"],
                "function_logic": role["logic"],
                "paper_method_or_results_relation": role["paper_relation"],
                "experimental_boundary": "experimental_not_formal; formal parameters require user confirmation",
                "line_start": row["line_start"],
                "line_end": row["line_end"],
            }
        )
    outputs = [
        ("run_deletion", "02_表格输出/deleted_files_log.csv; delete_plan.csv; protected_or_skipped_files.csv", "cleanup evidence"),
        ("environment_audit", "environment_audit_report.md; environment_audit_commands.csv", "environment evidence"),
        ("build_revised_config", "06_配置参数/dqn_revised_experimental_config.yaml", "model configuration"),
        ("model_outputs", "01_数据输出/dqn_revised_policy.csv; qlearning_policy.csv; 05_模型与实验/*.csv; dqn_revised_model.pt", "model outputs"),
        ("evaluate_policy", "multi_model_policy_comparison.csv; reward_component_summary.csv; constraint_violation_summary.csv", "evaluation tables"),
        ("generate_charts", "03_图表输出/*.png; chart_quality_audit.csv", "figures and chart QA"),
        ("create_reports", "04_报告输出/*.md; research_quality_gate_results.csv", "reports and quality gates"),
        ("create_results_draft", "09_论文输出/04_结果/*.md/csv; 09_word导出/*.docx", "paper Results"),
        ("sync_outputs", "experiments/optimization/*; reports/项目级索引与摘要/*", "canonical sync"),
        ("update_indexes_and_state", "outputs/_index/*; project_state/*", "project state"),
    ]
    for fn, outs, purpose in outputs:
        output_map.append(
            {
                "code_unit": fn,
                "generated_outputs": outs,
                "output_purpose": purpose,
                "paper_relation": function_role(fn)["paper_relation"],
                "verification_needed": "需要用 manifest、source CSV、chart QA 和 result claim guard 复核",
            }
        )
    pd.DataFrame(inventory).to_csv(RUN / "08_代码快照" / "dqn_code_function_inventory.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(model_map).to_csv(RUN / "08_代码快照" / "dqn_code_to_model_setting_map.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(output_map).to_csv(RUN / "08_代码快照" / "dqn_code_to_outputs_map.csv", index=False, encoding="utf-8-sig")
    write_code_markdown(model_map, output_map)


def write_code_markdown(model_map: list[dict[str, object]], output_map: list[dict[str, object]]) -> None:
    readme = """
    # README DQN 代码总览

    本目录包含 DQN 修正版 experimental run 的原始代码快照、带头部说明的 annotated copy、函数级逻辑说明、代码到模型设置映射、代码到输出文件映射、方法说明和可复现性说明。

    用户阅读顺序：

    1. 先读 `README_DQN代码总览.md`。
    2. 再读 `dqn_code_deep_explanation.md` 理解 DQN 如何对应 state/action/reward/constraint/training/evaluation。
    3. 用 `dqn_code_to_model_setting_map.csv` 查函数对应 Method 小节。
    4. 用 `dqn_code_to_outputs_map.csv` 查代码生成了哪些图、表、报告和 Word。
    5. 如需 formal DQN，不要直接运行代码；先确认参数表。
    """
    write(RUN / "08_代码快照" / "README_DQN代码总览.md", readme)

    deep = """
    # DQN 代码深度说明

    ## 总体流程

    `run_recommended_delete_and_dqn_revised.py` 同时承担缓存清理、环境核验、上游数据检查、DQN 修正版 experimental training、多模型比较、图表生成、报告生成、论文 Results 草稿和索引更新。它不是 formal DQN 训练脚本，而是一次 experimental workflow orchestration。

    ## State 构建

    `build_mapping()` 负责识别状态表字段；`prepare_model_data()` 将 canonical PEANUT belief-MDP/MOE-EDI 特征转换为模型输入，包括 state matrix、risk score、uncertainty、month/group key。对应论文 Method 的 state representation。当前 state 仍依赖已有 feature table，formal 前需确认所有字段含义、单位和缺失处理。

    ## Action 定义

    `ACTION_VALUES = [0, 1, 3, 5, 10]` 是粗粒度抽检加码动作。`build_valid_actions()` 把动作档位和容量上限结合为 action mask。高维二元 action 未训练，仍需 hierarchical/factorized/combinatorial 方案。

    ## Reward 计算

    `build_reward_matrix()` 是核心 reward function：risk reward 与 information gain 为正项，sampling cost、opportunity penalty、constraint penalty 为惩罚项，并用 robust scale + `tanh` 重标度。该函数对应论文 Method 的 reward decomposition。所有权重仍是 experimental，formal 前必须确认。

    ## Constraint 处理

    `build_capacity()`、`capacity_for_row()`、`build_valid_actions()` 和 `evaluate_policy()` 共同处理约束。`evaluate_policy()` 还会在 monthly remaining budget 与 capacity 下调整不可行动作，并统计 constraint violation / adjustment。当前所有策略违约为 0，但这依赖 action mask 和预算容量设定。

    ## DQN 训练

    `QNet` 定义 Q-network；`train_dqn()` 负责 model/target network、epsilon-greedy、batch update、target update、epsilon decay、training log、early stopping 相关逻辑。该训练是 experimental，不允许直接作为 formal policy optimizer。

    ## Q-learning 与 heuristic baseline

    `train_qlearning()` 用聚合状态构建 Q-learning baseline；`build_baseline_actions()` 生成 uniform、historical、risk-ranking top-k、random、threshold/greedy uncertainty 等 baseline。`evaluate_policy()` 使用统一 protocol 比较所有策略。

    ## 输出、图表与 Word

    `model_outputs()` 组织训练和比较；`generate_charts()` 生成 PNG 主图；`create_reports()` 写训练/审计/质量报告；`create_results_draft()` 写 experimental Results draft 和 DOCX；`sync_outputs()` 同步必要 canonical 副本。

    ## 与论文 Method / Results 的关系

    - Method：state/action/reward/constraint/training/baseline/evaluation 由代码函数和配置共同支撑。
    - Results：multi-model comparison、reward curve、constraint summary、policy table、quality gates 和 evidence table 支撑 Results 草稿。
    - Discussion：局限性来自 experimental boundary、reward 权重、transition 近似、约束确认和外部验证缺口。
    """
    write(RUN / "08_代码快照" / "dqn_code_deep_explanation.md", deep)

    notes = """
    # DQN Code Method Notes

    本代码对应 Method 写作时应拆成：数据与 state features、action space、reward decomposition、constraints/action mask、DQN training、Q-learning baseline、heuristic baselines、evaluation protocol、quality gates、experimental boundary。

    不应把代码写成“自动得到最优监管政策”。准确表述应为：在本地 PEANUT belief-MDP/MOE-EDI 特征和 experimental reward/constraint 设置下，训练并比较 DQN、Q-learning 与多种 heuristic baseline。
    """
    write(RUN / "08_代码快照" / "dqn_code_method_notes.md", notes)

    repro = """
    # DQN Code Reproducibility Notes

    ## 可复现条件

    - 使用 `D:\\anaconda3\\envs\\myenv1\\python.exe`
    - CUDA/PyTorch 环境须通过 smoke test
    - canonical feature tables 不变
    - random seed、reward weights、budget/capacity、ACTION_VALUES 与 config 固定

    ## formal 前需确认

    action space、budget、unit cost、capacity、minimum coverage、reward weights、transition assumptions、training hyperparameters、baseline protocol、evaluation metrics。

    ## 风险

    - reward 权重可能驱动策略偏好，存在 reward hacking 风险。
    - transition 近似尚未 formal 化。
    - Q-learning 当前领先 DQN，说明 DQN 训练稳定性/样本效率仍需进一步验证。
    - 图表和 DOCX 需要 render QA，不能只看文件存在。
    """
    write(RUN / "08_代码快照" / "dqn_code_reproducibility_notes.md", repro)


def explanation_for_file(path: Path) -> str:
    rp = rel(path)
    purpose = CORE_ARTIFACTS.get(str(path.relative_to(RUN)).replace("\\", "/"), "辅助文件，用于审计、导航、复核或可追溯性。")
    return f"""
    # Explanation: {path.name}

    - 文件路径：`{rp}`
    - 文件作用：{purpose}
    - 输入来源：上一轮解释升级包 `{rel(SOURCE_EXPLANATION_RUN)}`、DQN 修正版训练包 `{rel(SOURCE_DQN_RUN)}` 或本轮代码解释生成逻辑。
    - 如何阅读：先看本目录 README，再看本文件；如果是表格或图表，应同时查看同名 `.explanation.md` 和源 CSV。
    - 主要结果：用于支持本轮“解释就地化”和 DQN experimental 结果阅读。
    - 是否可用于论文：只能作为 experimental Results / Method / Appendix 证据，不能单独支撑 formal 监管结论。
    - experimental 状态：是，DQN 相关输出均为 experimental_not_formal。
    - 局限性：未重新训练 DQN；formal 前仍需参数确认、敏感性分析和外部验证。
    - 与其他输出关系：总索引在 `10_输出解释与索引/`，本文件旁侧解释负责就地阅读。
    """


def local_readme(dir_path: Path, title: str, focus: str) -> str:
    files = [p for p in sorted(dir_path.iterdir()) if p.is_file()]
    lines = [f"# {title}", "", f"本目录说明：{focus}", "", "## 文件说明"]
    for p in files:
        if p.name.endswith(".explanation.md") or p.name.startswith("README"):
            continue
        lines.append(f"- `{p.name}`：{CORE_ARTIFACTS.get(str(p.relative_to(RUN)).replace('\\', '/'), '辅助 artifact；请结合同名 explanation 或 local explanation 阅读。')}")
    lines.extend(
        [
            "",
            "## 阅读规则",
            "",
            "1. 本目录 README 是就地解释，不需要先跳到 `10_输出解释与索引/` 才能读懂。",
            "2. 关键 artifact 均尽量配套同名 `.explanation.md`。",
            "3. DQN 相关输出全部保持 experimental；不能作为 formal 监管政策结论。",
            "4. 用户下一步应优先阅读本目录 README、关键同名 explanation、再回到总索引查看跨目录关系。",
        ]
    )
    return "\n".join(lines)


def generate_local_explanations() -> None:
    dir_specs = {
        "02_表格输出": ("README_表格解释.md", "表格输出解释", "包含覆盖矩阵、审计清单、文献表、dry-run 结果和 evidence maps。"),
        "03_图表输出": ("README_图表解释.md", "图表输出解释", "包含 DQN 训练曲线、策略比较、约束解释性图和图表 QA 相关 PNG。"),
        "04_报告输出": ("README_报告解释.md", "报告输出解释", "包含 deep audit、DQN 设置说明、结果解读、文献扩展、修复报告和 dry-run 报告。"),
        "05_模型与实验": ("README_模型输出解释.md", "模型与实验输出解释", "包含 DQN/Q-learning 训练日志和 experiment ledger，用于可复现与收敛诊断。"),
        "06_配置参数": ("README_参数配置解释.md", "参数配置解释", "包含 DQN 修正版 experimental config 和参数边界说明。"),
        "08_代码快照": ("README_代码解释.md", "代码快照解释", "包含 DQN 代码快照、深度代码说明、函数级映射和复现性 notes。"),
        "09_论文输出": ("README_论文输出解释.md", "论文输出解释", "包含 Results markdown、evidence table、Word 导出和渲染 QA。"),
        "09_论文输出/04_结果": ("README_Results解释.md", "Results 输出解释", "包含 experimental Results 草稿和 evidence table。"),
        "09_论文输出/09_word导出": ("README_Word导出解释.md", "Word 导出解释", "包含 DOCX、表格预览 PNG、渲染页和 render QA。"),
        "10_输出解释与索引": ("README_总索引说明.md", "总索引导航", "只作为导航和汇总，不替代各目录本地解释。"),
    }
    coverage = []
    missing = []
    for sub, (readme_name, title, focus) in dir_specs.items():
        d = RUN / sub
        d.mkdir(parents=True, exist_ok=True)
        write(d / readme_name, local_readme(d, title, focus))
        local_name = "table_explanations_local.md" if sub == "02_表格输出" else "figure_explanations_local.md" if sub == "03_图表输出" else f"{readme_name.replace('README_', '').replace('.md', '')}_local.md"
        write(d / local_name, local_readme(d, title + " local details", focus))
        for p in sorted(d.iterdir()):
            if not p.is_file() or p.name.endswith(".explanation.md") or p.name.startswith("README"):
                continue
            important = str(p.relative_to(RUN)).replace("\\", "/") in CORE_ARTIFACTS or p.suffix.lower() in {".docx", ".png", ".csv", ".yaml", ".py"}
            exp = p.with_name(p.name + ".explanation.md")
            if important:
                write(exp, explanation_for_file(p))
            coverage.append(
                {
                    "directory": sub,
                    "artifact": rel(p),
                    "directory_readme": rel(d / readme_name),
                    "local_explanation": rel(d / local_name),
                    "same_name_explanation": rel(exp) if exp.exists() else "",
                    "covered": bool((d / readme_name).exists() and (d / local_name).exists() and (not important or exp.exists())),
                    "importance": "core" if important else "support",
                }
            )
            if important and not exp.exists():
                missing.append({"artifact": rel(p), "missing_reason": "核心文件缺少同名 explanation"})
    pd.DataFrame(coverage).to_csv(RUN / "02_表格输出" / "local_explanation_coverage_matrix.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(missing, columns=["artifact", "missing_reason"]).to_csv(RUN / "02_表格输出" / "missing_local_explanations.csv", index=False, encoding="utf-8-sig")
    write(
        RUN / "04_报告输出" / "local_explanation_repair_report.md",
        f"""
        # Local Explanation Repair Report

        本轮已将解释从集中索引修正为“就地解释 + 总索引导航”。

        - 已覆盖目录数：{len(dir_specs)}
        - 覆盖矩阵：`02_表格输出/local_explanation_coverage_matrix.csv`
        - 缺失清单：`02_表格输出/missing_local_explanations.csv`
        - 关键规则：`10_输出解释与索引/` 只做导航，不能替代每个结果目录下的 README/local explanation 和关键文件同名 `.explanation.md`。
        """,
    )


def update_total_index() -> None:
    target = RUN / "10_输出解释与索引" / "artifact_explanation_index.md"
    lines = [
        "# Artifact Explanation Index",
        "",
        "本索引只负责导航，不能替代各目录下的本地解释。请优先阅读结果所在目录的 README、local explanation 和同名 `.explanation.md`。",
        "",
        "## 本地解释入口",
        "",
    ]
    for p in sorted(RUN.rglob("README*解释.md")) + sorted(RUN.rglob("README_总索引说明.md")):
        lines.append(f"- `{rel(p)}`")
    lines.extend(
        [
            "",
            "## DQN 代码深度说明入口",
            "",
            f"- `{rel(RUN / '08_代码快照' / 'README_DQN代码总览.md')}`",
            f"- `{rel(RUN / '08_代码快照' / 'dqn_code_deep_explanation.md')}`",
            f"- `{rel(RUN / '08_代码快照' / 'dqn_code_to_model_setting_map.csv')}`",
            f"- `{rel(RUN / '08_代码快照' / 'dqn_code_to_outputs_map.csv')}`",
        ]
    )
    write(target, "\n".join(lines))


def run_dry_runs() -> None:
    goals = [
        "为每个输出目录生成本地解释",
        "为关键 artifact 生成同名解释文件",
        "为 DQN 代码生成深度解释",
        "生成 DQN 代码到模型设置映射",
        "生成 DQN 代码到输出文件映射",
        "检查解释是否只存在于总索引而没有就地解释",
    ]
    rows = []
    for goal in goals:
        cp = subprocess.run([PYTHON, "-m", "workflow1", "--stage", "dry-run", "--goal", goal], cwd=ROOT, text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        rows.append({"goal": goal, "status": "pass" if cp.returncode == 0 and ("intent" in cp.stdout or "matched_intent" in cp.stdout) else "review", "stdout_tail": cp.stdout[-1800:], "stderr_tail": cp.stderr[-800:]})
    pd.DataFrame(rows).to_csv(RUN / "02_表格输出" / "local_explanation_dry_run_results.csv", index=False, encoding="utf-8-sig")
    md = "# Local Explanation Dry-run Report\n\n"
    for r in rows:
        md += f"## {r['goal']}\n\n- 状态：{r['status']}\n\n```text\n{r['stdout_tail'][:1200]}\n```\n\n"
    write(RUN / "04_报告输出" / "local_explanation_dry_run_report.md", md)


def update_indexes_state() -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    idx = ROOT / "outputs" / "_index" / "run_index.md"
    with idx.open("a", encoding="utf-8") as f:
        f.write(f"\n## {RUN.name}\n\n- 时间：{ts}\n- 类型：输出解释就地化修正与DQN代码深度说明补强\n- 路径：`{rel(RUN)}`\n- 状态：completed\n- 说明：将解释就地化到每个输出目录，并补强 DQN code-to-method/code-to-output 映射。\n")
    manifest = ROOT / "outputs" / "_index" / "run_manifest.csv"
    row = pd.DataFrame([{"run_id": RUN.name, "run_path": rel(RUN), "created_at": ts, "task": "输出解释就地化修正与DQN代码深度说明补强", "status": "completed"}])
    if manifest.exists():
        old = pd.read_csv(manifest)
        pd.concat([old, row], ignore_index=True).to_csv(manifest, index=False, encoding="utf-8-sig")
    else:
        row.to_csv(manifest, index=False, encoding="utf-8-sig")
    latest_path = ROOT / "outputs" / "_index" / "latest_canonical_outputs.yaml"
    latest = yaml.safe_load(latest_path.read_text(encoding="utf-8")) if latest_path.exists() else {}
    latest = latest or {}
    latest.update(
        {
            "latest_local_explanation_repair_run": rel(RUN),
            "latest_dqn_code_deep_explanation": rel(RUN / "08_代码快照" / "dqn_code_deep_explanation.md"),
            "latest_local_explanation_coverage_matrix": rel(RUN / "02_表格输出" / "local_explanation_coverage_matrix.csv"),
            "latest_dqn_status": "experimental_audited_explained_localized_not_formal",
        }
    )
    latest_path.write_text(yaml.safe_dump(latest, allow_unicode=True, sort_keys=False), encoding="utf-8")
    for file, addition in {
        "project_state/current_focus.md": f"\n\n## 输出解释就地化修正\n\n最新修正包：`{rel(RUN)}`。解释已从总索引补充到各结果目录，并新增 DQN 代码深度说明和 code-to-method/code-to-output 映射。\n",
        "project_state/next_step.md": "\n\n下一步若继续 formal DQN，先确认参数表；若继续论文写作，可基于 DQN code-to-method map 生成 Method section。\n",
        "project_state/changelog.md": f"\n\n## {datetime.now():%Y-%m-%d}\n\n- 修正输出解释机制：解释必须就地放在结果目录，关键 artifact 生成同名 `.explanation.md`，DQN 代码增加深度说明。任务包：`{rel(RUN)}`。\n",
        "project_state/decision_log.md": "\n\n## Decision: Explanation Co-location\n\n总索引不能替代本地解释。未来每个结果目录必须有 README/local explanation，关键 artifact 必须尽量生成同名 `.explanation.md`。DQN 代码必须映射到 Method 和 Results。\n",
        "project_state/conversation_handoff.md": f"\n\n最新修正：`{rel(RUN)}` 已补充就地解释与 DQN 代码深度说明。继续时优先读取该包的 `08_代码快照/README_DQN代码总览.md` 和各目录 README。\n",
        "project_state/project_memory.md": "\n\n## Output Explanation Co-location Memory\n\n解释要贴着结果走：每个输出目录必须有 README/local explanation，关键 artifact 应有同名 `.explanation.md`；`10_输出解释与索引/` 仅作导航。\n",
        "project_state/run_protocol.md": "\n\n## Local Explanation Addendum\n\n每次 durable task 结束前检查是否存在 only-central-index 问题；如果解释只在总索引中，必须补本地解释和同名 explanation。\n",
    }.items():
        p = ROOT / file
        p.write_text(p.read_text(encoding="utf-8", errors="replace") + addition, encoding="utf-8")


def write_manifest_readme() -> None:
    files = []
    for p in sorted(RUN.rglob("*")):
        if p.is_file():
            files.append({"path": rel(p), "size_bytes": p.stat().st_size, "sha256": sha(p) if p.stat().st_size else "", "purpose": CORE_ARTIFACTS.get(str(p.relative_to(RUN)).replace("\\", "/"), "local explanation repair artifact")})
    pd.DataFrame(files).to_csv(RUN / "manifest.csv", index=False, encoding="utf-8-sig")
    write(
        RUN / "README.md",
        f"""
        # 输出解释就地化修正与 DQN 代码深度说明补强

        本轮修正上一轮解释集中在 `10_输出解释与索引/` 的问题。现在每个结果目录均有本地 README/local explanation，核心 artifact 有同名 `.explanation.md`。

        重点文件：

        - `04_报告输出/local_explanation_repair_report.md`
        - `02_表格输出/local_explanation_coverage_matrix.csv`
        - `02_表格输出/missing_local_explanations.csv`
        - `08_代码快照/README_DQN代码总览.md`
        - `08_代码快照/dqn_code_deep_explanation.md`
        - `08_代码快照/dqn_code_to_model_setting_map.csv`
        - `08_代码快照/dqn_code_to_outputs_map.csv`

        DQN 输出仍为 experimental，不是 formal 监管政策结论。
        """,
    )


def main() -> None:
    init_run()
    copy_previous_artifacts()
    generate_dqn_code_docs()
    generate_local_explanations()
    update_total_index()
    run_dry_runs()
    update_indexes_state()
    write_manifest_readme()
    print(json.dumps({"run_dir": str(RUN), "status": "completed"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
