from __future__ import annotations

import csv
import json
import math
import os
import re
import subprocess
import sys
import textwrap
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[4]
RUN_DIR = ROOT / "outputs" / "工作包" / "20260425_1157_DQN文档驱动建模准备与参数确认"
ZOTERO_DIR = Path("D:/桌面/codex/zotero")
DOCX_PATH = ROOT / "references" / "notes" / "物流与供应链管理前言-研究计划-肖宇航.docx"
DEFAULT_PY = Path(sys.executable)
MYEVN_PY = Path("D:/anaconda3/envs/myevn1/python.exe")
DISCOVERED_MYENV_PY = Path("D:/anaconda3/envs/myenv1/python.exe")

DIRS = {
    "inputs": RUN_DIR / "00_输入说明",
    "tables": RUN_DIR / "02_表格输出",
    "reports": RUN_DIR / "04_报告输出",
    "configs": RUN_DIR / "06_配置参数",
    "logs": RUN_DIR / "07_日志与错误",
    "code": RUN_DIR / "08_代码快照",
}

KEYWORDS = [
    "DQN", "deep reinforcement learning", "constrained reinforcement learning",
    "safe reinforcement learning", "POMDP", "MDP", "belief-MDP", "food safety monitoring",
    "inspection strategy", "sampling strategy", "Bayesian update", "Beta-Binomial",
    "MOE", "EDI", "aflatoxin", "AFB1", "peanut", "黄曲霉", "黄曲霉毒素",
    "抽检", "动态监管", "信念", "约束", "预算", "产能", "奖励", "损失", "召回",
]

MODEL_TERMS = {
    "state": ["状态", "state", "belief", "信念", "后验", "Beta", "MOE", "EDI", "风险特征"],
    "observation": ["观测", "observation", "抽检结果", "检测", "信号"],
    "action": ["动作", "action", "抽检", "复检", "召回", "处置", "批次"],
    "reward": ["reward", "奖励", "惩罚", "损失", "目标函数", "风险降低", "信息价值"],
    "constraint": ["约束", "constraint", "预算", "产能", "成本", "覆盖"],
    "transition": ["转移", "transition", "传播", "更新", "遗忘因子"],
    "episode_training": ["DQN", "网络", "训练", "episode", "replay", "epsilon", "学习率", "超参数"],
}

EXTERNAL_LITERATURE = [
    {
        "title": "Human-level control through deep reinforcement learning",
        "authors": "Mnih et al.",
        "year": "2015",
        "source": "Nature",
        "doi": "10.1038/nature14236",
        "url": "https://www.nature.com/articles/nature14236",
        "topic": "DQN original method",
        "role": "说明 DQN 以 neural network 近似 Q(s,a)，但不替代用户文档中的状态、动作和奖励设定。",
        "priority": "core_method_background",
    },
    {
        "title": "A Survey of Constraint Formulations in Safe Reinforcement Learning",
        "authors": "Wachi; Shen; Sui",
        "year": "2024",
        "source": "IJCAI",
        "doi": "10.24963/ijcai.2024/913",
        "url": "https://www.ijcai.org/proceedings/2024/913",
        "topic": "safe/constrained RL",
        "role": "支持把预算、产能、覆盖和风险红线写为约束或约束惩罚；不覆盖用户文档设定。",
        "priority": "constraint_background",
    },
    {
        "title": "State of the Art - A Survey of Partially Observable Markov Decision Processes",
        "authors": "Monahan",
        "year": "1982",
        "source": "Management Science",
        "doi": "10.1287/mnsc.28.1.1",
        "url": "https://pubsonline.informs.org/doi/10.1287/mnsc.28.1.1",
        "topic": "POMDP",
        "role": "支持在不可直接观测污染状态时使用 belief state；具体 belief 构造以项目文档为准。",
        "priority": "pomdp_background",
    },
    {
        "title": "Modeling cost-effective monitoring schemes for food safety contaminants: Case study for dioxins in the dairy supply chain",
        "authors": "van Asselt et al. / Food Research International article page",
        "year": "2021",
        "source": "Food Research International",
        "doi": "10.1016/j.foodres.2021.110110",
        "url": "https://www.sciencedirect.com/science/article/pii/S0963996921000077",
        "topic": "risk-based food safety monitoring optimization",
        "role": "支持预算受限食品安全监测优化的建模思想；正式动作和成本仍需用户确认。",
        "priority": "food_monitoring_background",
    },
    {
        "title": "Application of the Margin of Exposure (MOE) approach to substances in food that are genotoxic and carcinogenic: Example: Aflatoxin B1",
        "authors": "Benford et al.",
        "year": "2010",
        "source": "Food and Chemical Toxicology",
        "doi": "",
        "url": "https://www.sciencedirect.com/science/article/pii/S0278691509004980",
        "topic": "AFB1 MOE",
        "role": "支持 AFB1 作为 MOE 风险度量场景；BMDL 和暴露参数不得由 Codex 擅自定为正式值。",
        "priority": "moe_afb1_background",
    },
    {
        "title": "Margin of Exposure",
        "authors": "EFSA",
        "year": "current topic page",
        "source": "European Food Safety Authority",
        "doi": "",
        "url": "https://www.efsa.europa.eu/en/topics/topic/margin-exposure",
        "topic": "MOE interpretation",
        "role": "支持 MOE 的监管解释；项目正式阈值和惩罚映射仍需用户确认。",
        "priority": "official_moe_background",
    },
]


def ensure_dirs() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_docx_full(path: Path) -> tuple[list[str], list[list[list[str]]]]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    tables: list[list[list[str]]] = []
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)

    for child in root.find("w:body", ns):
        if child.tag == f"{{{ns['w']}}}p":
            text = "".join(t.text or "" for t in child.findall(".//w:t", ns)).strip()
            if text:
                paragraphs.append(text)
        elif child.tag == f"{{{ns['w']}}}tbl":
            table_rows = []
            for tr in child.findall(".//w:tr", ns):
                cells = []
                for tc in tr.findall("./w:tc", ns):
                    cell_text = " ".join(
                        "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()
                        for p in tc.findall(".//w:p", ns)
                    ).strip()
                    cells.append(cell_text)
                if any(cells):
                    table_rows.append(cells)
            if table_rows:
                tables.append(table_rows)
                paragraphs.append("[表格] " + " | ".join(table_rows[0]))
                for row in table_rows[1:]:
                    joined = " | ".join(row)
                    if joined:
                        paragraphs.append("[表格行] " + joined)
    return paragraphs, tables


def context_snippets(paragraphs: list[str]) -> dict[str, list[str]]:
    snippets = {}
    for key, terms in MODEL_TERMS.items():
        found = []
        for p in paragraphs:
            lower = p.lower()
            if any(t.lower() in lower for t in terms):
                found.append(p)
        snippets[key] = found[:80]
    return snippets


def classify_doc_spec(snippets: dict[str, list[str]]) -> dict:
    def joined(k: str) -> str:
        return "\n".join(snippets.get(k, []))

    spec = {
        "source_document": str(DOCX_PATH),
        "extracted_at": datetime.now().isoformat(timespec="seconds"),
        "governance": {
            "formal_dqn_must_follow_document": True,
            "sandbox_prototype_20260425_1132_allowed_as_formal_basis": False,
            "missing_formal_parameters_require_user_confirmation": True,
        },
        "problem_framing": {
            "document_summary": "研究计划将花生/AFB1 风险监管表述为受限 POMDP / belief-MDP / 深度强化学习问题；抽检既是风险干预动作，也是更新信念的信息获取机制。",
            "evidence": first_nonempty(joined("state"), joined("action"), joined("constraint")),
        },
        "state": {
            "document_status": "partially_specified",
            "elements": [
                "省份-时间-供应链环节状态单元",
                "Beta-Binomial posterior alpha/beta, posterior mean/variance",
                "样本覆盖强度、AFB1覆盖强度、浓度可用率",
                "MOE/EDI、人口权重、风险 proxy 等风险特征",
            ],
            "evidence": joined("state")[:3500],
            "needs_user_confirmation": True,
        },
        "observation": {
            "document_status": "partially_specified",
            "elements": ["抽检批次数", "不合格/AFB1不合格结果", "浓度检测值", "MOE/EDI 派生风险信号"],
            "evidence": joined("observation")[:2500],
            "needs_user_confirmation": True,
        },
        "action": {
            "document_status": "conceptual_only",
            "elements": ["跨省份/供应链环节的整数抽检批次数", "专项抽检", "复检/召回/处置触发档位"],
            "evidence": joined("action")[:3500],
            "needs_user_confirmation": True,
            "formal_values_defined": False,
        },
        "reward": {
            "document_status": "conceptual_only",
            "elements": ["MOE驱动的暴露风险降低", "抽检成本", "处置/召回损失", "信息价值", "约束违约惩罚"],
            "evidence": joined("reward")[:3500],
            "needs_user_confirmation": True,
            "formal_weights_defined": False,
        },
        "constraints": {
            "document_status": "conceptual_only",
            "elements": ["预算", "检测产能", "区域/环节最低覆盖", "重点风险区域优先级"],
            "evidence": joined("constraint")[:3500],
            "needs_user_confirmation": True,
            "formal_values_defined": False,
        },
        "transition_and_belief_update": {
            "document_status": "partially_specified",
            "elements": ["Beta-Binomial 共轭更新", "跨期遗忘因子", "belief-MDP 状态传播"],
            "evidence": joined("transition")[:3500],
            "needs_user_confirmation": True,
        },
        "training": {
            "document_status": "not_formally_specified",
            "elements": ["DQN 网络结构、learning rate、gamma、epsilon、replay buffer、batch size、episode 数均需确认"],
            "evidence": joined("episode_training")[:2500],
            "needs_user_confirmation": True,
        },
    }
    return spec


def first_nonempty(*values: str) -> str:
    for value in values:
        if value.strip():
            return value[:1200]
    return ""


def yaml_quote(s: str) -> str:
    if s is None:
        return "''"
    return json.dumps(str(s), ensure_ascii=False)


def to_yaml(obj, indent: int = 0) -> str:
    sp = "  " * indent
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.append(to_yaml(v, indent + 1))
            else:
                lines.append(f"{sp}{k}: {yaml_quote(v)}")
        return "\n".join(lines)
    if isinstance(obj, list):
        lines = []
        for v in obj:
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}-")
                lines.append(to_yaml(v, indent + 1))
            else:
                lines.append(f"{sp}- {yaml_quote(v)}")
        return "\n".join(lines)
    return f"{sp}{yaml_quote(obj)}"


def run_cmd(label: str, exe: Path | str, code: str | None = None, extra_env: dict | None = None) -> dict:
    if code is None:
        cmd = [str(exe)]
    else:
        cmd = [str(exe), "-c", code]
    try:
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        proc = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True, timeout=60, env=env)
        return {
            "检查项": label,
            "命令": " ".join(cmd),
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "状态": "PASS" if proc.returncode == 0 else "FAIL",
        }
    except Exception as exc:
        return {
            "检查项": label,
            "命令": " ".join(cmd),
            "returncode": "",
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
            "状态": "FAIL",
        }


def environment_audit() -> list[dict]:
    default_exe = "python"
    checks = [
        run_cmd("default_python_sys", default_exe, "import sys; print(sys.executable); print(sys.version)"),
        run_cmd("default_python_torch", default_exe, "import torch; print(torch.__version__); print(torch.cuda.is_available())"),
        {
            "检查项": "myevn1_path_exists",
            "命令": f"Test-Path {MYEVN_PY}",
            "returncode": 0 if MYEVN_PY.exists() else 1,
            "stdout": str(MYEVN_PY.exists()),
            "stderr": "",
            "状态": "PASS" if MYEVN_PY.exists() else "FAIL",
        },
        run_cmd("myevn1_python_sys", MYEVN_PY, "import sys; print(sys.executable); print(sys.version)"),
        run_cmd("myevn1_python_torch", MYEVN_PY, "import torch; print(torch.__version__); print(torch.cuda.is_available())"),
        run_cmd("myevn1_python_basic", MYEVN_PY, "import numpy, pandas, sklearn; print('basic ok')"),
        {
            "检查项": "discovered_myenv1_path_exists",
            "命令": f"Test-Path {DISCOVERED_MYENV_PY}",
            "returncode": 0 if DISCOVERED_MYENV_PY.exists() else 1,
            "stdout": str(DISCOVERED_MYENV_PY.exists()),
            "stderr": "",
            "状态": "PASS" if DISCOVERED_MYENV_PY.exists() else "FAIL",
        },
        run_cmd("discovered_myenv1_python_sys", DISCOVERED_MYENV_PY, "import sys; print(sys.executable); print(sys.version)"),
        run_cmd("discovered_myenv1_python_torch_raw", DISCOVERED_MYENV_PY, "import torch; print(torch.__version__); print(torch.cuda.is_available())"),
        run_cmd("discovered_myenv1_python_torch_with_kmp_workaround", DISCOVERED_MYENV_PY, "import torch; print(torch.__version__); print(torch.cuda.is_available())", {"KMP_DUPLICATE_LIB_OK": "TRUE"}),
        run_cmd("discovered_myenv1_python_basic", DISCOVERED_MYENV_PY, "import numpy, pandas, sklearn; print('basic ok')", {"KMP_DUPLICATE_LIB_OK": "TRUE"}),
    ]
    return checks


def scan_zotero() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    issue_rows: list[dict] = []
    if not ZOTERO_DIR.exists():
        return ([{"路径": str(ZOTERO_DIR), "标题": "", "文件类型": "", "匹配关键词": "", "是否有PDF": "否", "是否读取全文": "否", "note是否乱码": "未知", "是否可作正式依据": "否", "说明": "Zotero目录不可访问"}], [])

    files = [p for p in ZOTERO_DIR.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".csv", ".pdf", ".txt"}]
    pdf_by_stem = {normalize_title(p.stem): p for p in files if p.suffix.lower() == ".pdf"}
    text_files = [p for p in files if p.suffix.lower() in {".md", ".csv", ".txt"}]

    seen_titles = set()
    for path in text_files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            issue_rows.append({"文件": str(path), "问题类型": "read_error", "说明": f"{type(exc).__name__}: {exc}", "处理": "跳过该文件"})
            continue
        matches = [kw for kw in KEYWORDS if kw.lower() in text.lower() or kw.lower() in path.name.lower()]
        if not matches:
            continue
        title = infer_title(path, text)
        norm = normalize_title(title)
        if (str(path), title) in seen_titles:
            continue
        seen_titles.add((str(path), title))
        qmarks = text.count("?????")
        replacement = text.count("\ufffd")
        mojibake = count_mojibake(text)
        is_note = "deepreads" in path.parts or path.suffix.lower() == ".md"
        note_bad = is_note and (qmarks >= 2 or replacement >= 5 or mojibake > 30)
        if note_bad:
            issue_rows.append({
                "文件": str(path),
                "问题类型": "note_encoding_or_mojibake",
                "说明": f"?????次数={qmarks}; replacement={replacement}; mojibake_score={mojibake}",
                "处理": "不直接作为正式依据；优先追溯PDF或外部正式页面",
            })
        pdf = find_pdf_for_title(norm, pdf_by_stem)
        fulltext_read = "否"
        pdf_pages = ""
        pdf_error = ""
        if pdf:
            fulltext_read, pdf_pages, pdf_error = try_read_pdf(pdf)
            if pdf_error:
                issue_rows.append({"文件": str(pdf), "问题类型": "pdf_read_error", "说明": pdf_error, "处理": "记录为PDF不可完整读取"})
        role = literature_role(title, matches)
        formal_basis = "可作为方法背景" if not note_bad else "否，note疑似乱码，需PDF/正式页面复核"
        rows.append({
            "标题": title,
            "路径": str(path),
            "文件类型": path.suffix.lower(),
            "匹配关键词": "; ".join(matches[:12]),
            "是否有PDF": "是" if pdf else "否",
            "PDF路径": str(pdf) if pdf else "",
            "是否读取全文": fulltext_read,
            "PDF页数": pdf_pages,
            "note是否乱码": "是" if note_bad else "否",
            "乱码迹象": f"?????={qmarks}; �={replacement}; mojibake={mojibake}",
            "对DQN设定作用": role,
            "是否可作正式方法依据": formal_basis,
            "备注": pdf_error,
        })
    rows.sort(key=lambda r: (r["note是否乱码"], r["标题"]))
    return rows, issue_rows


def normalize_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def infer_title(path: Path, text: str) -> str:
    for line in text.splitlines()[:30]:
        clean = line.strip("# \ufeff\t")
        if clean and len(clean) > 8 and not clean.lower().startswith(("title,", "generated", "path,")):
            return clean[:180]
    return path.stem


def find_pdf_for_title(norm_title: str, pdf_by_stem: dict[str, Path]) -> Path | None:
    best = None
    best_score = 0
    title_words = set(norm_title.split())
    for stem, path in pdf_by_stem.items():
        words = set(stem.split())
        score = len(title_words & words)
        if score > best_score and score >= 4:
            best = path
            best_score = score
    return best


def count_mojibake(text: str) -> int:
    markers = ["绋", "鏂", "鍚", "浠", "鐩", "椋", "鎶", "娴", "湪", "€", "鈥", "銆"]
    return sum(text.count(m) for m in markers)


def try_read_pdf(path: Path) -> tuple[str, str, str]:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        pages = len(reader.pages)
        extracted_chars = 0
        empty_pages = 0
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_chars += len(page_text)
            else:
                empty_pages += 1
        if extracted_chars:
            status = f"是，已遍历全文{pages}页，可抽取文本字符数={extracted_chars}，空文本页={empty_pages}"
        else:
            status = f"否，已遍历全文{pages}页但PDF无可抽取文本"
        return status, str(pages), ""
    except Exception as exc:
        return "否", "", f"{type(exc).__name__}: {exc}"


def literature_role(title: str, matches: list[str]) -> str:
    lower = (title + " " + " ".join(matches)).lower()
    if "human-level control" in lower or "dqn" in lower or "deep reinforcement" in lower:
        return "DQN/Q-learning 方法背景；不能替代项目文档的 state/action/reward。"
    if "constraint" in lower or "safe reinforcement" in lower:
        return "约束强化学习背景；用于提醒正式 DQN 需预算/产能/安全约束。"
    if "pomdp" in lower or "belief" in lower:
        return "POMDP/belief-MDP 理论背景；用于支持信念状态建模。"
    if "bayesian" in lower or "beta" in lower:
        return "贝叶斯更新背景；用于支持 Beta-Binomial 信念更新。"
    if "aflatoxin" in lower or "moe" in lower or "edi" in lower:
        return "AFB1/MOE/EDI 风险度量背景。"
    if "monitoring" in lower or "inspection" in lower or "sampling" in lower:
        return "风险导向监测/抽检优化背景。"
    return "相关背景，需人工判断是否纳入正式方法依据。"


def current_data_inventory() -> list[dict]:
    outputs = {
        "cleaned_dataset": ROOT / "data/03_primary/peanut_cleaned_analysis_ready.csv",
        "count_panel": ROOT / "data/04_feature/peanut_count_panel.csv",
        "concentration_table": ROOT / "data/04_feature/peanut_concentration_clean_table.csv",
        "beta_binomial_states": ROOT / "data/04_feature/peanut_beta_binomial_belief_states.csv",
        "belief_mdp_features": ROOT / "data/04_feature/peanut_belief_mdp_state_features.csv",
        "belief_mdp_features_with_moe_edi": ROOT / "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv",
        "edi_moe_risk_table": ROOT / "data/04_feature/peanut_edi_moe_risk_table.csv",
    }
    rows = []
    for name, path in outputs.items():
        if path.exists():
            try:
                import pandas as pd
                df = pd.read_csv(path, nrows=2, low_memory=False)
                total_rows = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore")) - 1
                rows.append({"产物": name, "路径": str(path), "存在": "是", "行数估计": total_rows, "列名": "; ".join(df.columns[:50])})
            except Exception as exc:
                rows.append({"产物": name, "路径": str(path), "存在": "是", "行数估计": "", "列名": "", "错误": f"{type(exc).__name__}: {exc}"})
        else:
            rows.append({"产物": name, "路径": str(path), "存在": "否", "行数估计": "", "列名": ""})
    return rows


def parameter_confirmation_rows(spec: dict) -> list[dict]:
    required = [
        ("state 定义", "状态", "partially_specified", "文档列出 belief posterior、风险特征、覆盖强度等方向；具体列集合需确认", "当前数据可提供候选列", "是", "使用文档提到的 belief + MOE/EDI + 覆盖/不确定性特征作为候选，不作为正式定稿", "研究计划 + canonical belief-MDP features", "是", "否，待确认", "需用户确认最终字段"),
        ("observation 定义", "观测", "partially_specified", "抽检结果、检测浓度、风险信号用于更新 belief", "当前 count panel 和浓度表可估计", "是", "抽检批次/不合格/AFB1不合格/浓度作为候选", "研究计划 + count panel", "是", "否，待确认", ""),
        ("动作空间", "动作", "conceptual_only", "文档仅说明跨省份/环节整数抽检、专项抽检、复检/处置触发", "当前数据不能估计正式动作", "是", "建议由用户确认动作档位和每档批次数", "用户制度参数", "是", "否", "必须确认"),
        ("action mask", "约束", "not_specified", "文档要求预算/产能等硬约束，但未给 mask 规则", "不可估计", "是", "按预算、产能、最低覆盖生成 mask，待确认", "safe RL/CMDP 文献 + 用户参数", "是", "否", ""),
        ("每期预算", "预算", "not_specified", "未发现正式数值", "不可估计", "是", "建议值待用户提供", "用户外部监管参数", "否", "否", "必须确认"),
        ("产能上限", "产能", "not_specified", "未发现正式数值", "不可估计", "是", "建议值待用户提供", "实验室/监管能力参数", "否", "否", "必须确认"),
        ("单批次抽检成本", "成本", "conceptual_only", "文档提到单位成本/两环节成本，但未给正式数值", "不可估计", "是", "建议按环节分别给成本", "用户外部成本参数", "是", "否", "必须确认"),
        ("区域/环节最低覆盖约束", "约束", "conceptual_only", "文档提到最低覆盖和重点风险区域优先", "可从历史覆盖构造候选", "是", "建议用户给最低覆盖阈值", "监管公平性/覆盖要求", "是", "否", ""),
        ("inspection allocation rule", "动作", "conceptual_only", "文档要求跨省份/环节资源配置", "可生成候选排序但不能正式定规则", "是", "候选：按风险、人口权重、不确定性联合排序", "文档目标", "是", "否", ""),
        ("recall / disposal loss", "损失", "conceptual_only", "文档提到处置/召回损失", "当前数据不可估计", "是", "由用户提供或指定情景值", "监管/企业损失参数", "是", "否", "必须确认"),
        ("risk loss", "损失", "partially_specified", "文档要求 MOE/EDI 驱动暴露风险", "MOE/EDI proxy 已有", "是", "用 MOE风险惩罚作为候选，权重待确认", "MOE/EDI 输出", "是", "否", ""),
        ("information value weight", "权重", "conceptual_only", "文档提到信息价值/不确定性下降", "可用 posterior variance 构造候选", "是", "建议用不确定性下降 proxy，权重待确认", "belief update 文档", "是", "否", "必须确认"),
        ("reward function", "奖励", "conceptual_only", "风险降低 - 成本 - 处置损失 + 信息价值 - 约束违约惩罚", "只能构造 prototype", "是", "仅列候选公式，不定正式权重", "研究计划", "是", "否", "必须确认"),
        ("transition logic", "转移", "partially_specified", "Beta-Binomial 更新和遗忘因子方向已出现", "部分可由历史面板实现", "是", "沿用文档的 belief update；动作影响转移需确认", "研究计划 + belief states", "是", "否", ""),
        ("belief update", "信念更新", "partially_specified", "Beta-Binomial 共轭更新、遗忘因子", "已有 prototype 输出", "是", "prior/forgetting factor 需确认是否正式", "Beta-Binomial 输出", "是", "否，待确认", ""),
        ("time step", "时间", "partially_specified", "省份-月份-环节优先，月份不可用时按年", "当前数据有年月", "是", "建议月度", "研究计划 + 数据列", "是", "否，待确认", ""),
        ("episode definition", "训练", "not_specified", "未发现正式 episode 定义", "可按年度/全时序候选", "是", "建议按省份-环节时序或全局月度 episode，待确认", "DQN 实现需要", "是", "否", ""),
        ("baseline policies", "评估", "not_specified", "未发现正式 baseline", "可构造历史/随机/风险排序 baseline", "是", "候选：历史分配、随机、风险贪心、均匀覆盖", "评估需要", "是", "否", ""),
        ("DQN 网络结构", "训练超参数", "not_specified", "文档未给层数/宽度", "不可由数据正式决定", "是", "建议值待确认", "DQN 实现经验 + Mnih背景", "是", "否", "必须确认"),
        ("learning rate", "训练超参数", "not_specified", "未指定", "不可估计", "是", "建议值待确认", "训练配置", "是", "否", "必须确认"),
        ("gamma", "训练超参数", "not_specified", "未指定正式折扣因子", "不可估计", "是", "建议值待确认", "训练配置", "是", "否", "必须确认"),
        ("epsilon 策略", "训练超参数", "not_specified", "未指定", "不可估计", "是", "建议值待确认", "DQN 探索策略", "是", "否", "必须确认"),
        ("replay buffer 大小", "训练超参数", "not_specified", "未指定", "不可估计", "是", "建议值待确认", "DQN 实现参数", "是", "否", "必须确认"),
        ("batch size", "训练超参数", "not_specified", "未指定", "不可估计", "是", "建议值待确认", "训练配置", "是", "否", "必须确认"),
        ("episode 数", "训练超参数", "not_specified", "未指定", "不可估计", "是", "建议值待确认", "训练配置", "是", "否", "必须确认"),
        ("训练/验证划分", "评估", "not_specified", "未指定", "可按时间切分候选", "是", "建议时间外推验证，待确认", "防止泄漏", "是", "否", ""),
        ("evaluation metrics", "评估", "not_specified", "未指定", "可构造候选", "是", "候选：风险损失、预算违约、覆盖率、MOE改善、不确定性下降", "文档目标", "是", "否", ""),
        ("visualization outputs", "输出", "not_specified", "未指定正式图表", "可构造候选", "是", "建议策略地图、预算-风险曲线、约束违约图", "报告需要", "是", "否", ""),
        ("formal stopping conditions", "运行治理", "not_specified", "未指定", "不可估计", "是", "建议用户确认：参数未确认/上游核验失败/torch不可用时停止", "项目治理规则", "是", "否", ""),
    ]
    rows = []
    for item in required:
        rows.append({
            "参数名称": item[0],
            "参数类别": item[1],
            "文档是否已指定": item[2],
            "文档原文或摘要依据": item[3],
            "当前数据是否可估计": item[4],
            "是否需要我手动确认": item[5],
            "Codex建议值": item[6],
            "建议依据": item[7],
            "是否允许作为prototype assumption": item[8],
            "是否允许作为formal DQN参数": item[9],
            "备注": item[10],
        })
    return rows


def report_research_plan(paragraphs: list[str], tables: list[list[list[str]]], snippets: dict[str, list[str]], spec: dict) -> str:
    lines = [
        "# DQN 研究计划完整读取与模型规范抽取报告",
        "",
        f"- 文档路径：`{DOCX_PATH}`",
        f"- 完整读取方式：直接解析 DOCX `word/document.xml`，按正文段落和表格顺序抽取，不只读取标题或摘要。",
        f"- 非空正文/表格行计数：{len(paragraphs)}",
        f"- 表格数量：{len(tables)}",
        "",
        "## 总体判断",
        "",
        "研究计划已经明确把花生/AFB1 风险监管问题放在受限 POMDP、belief-MDP 和深度强化学习框架下：真实污染风险不可直接观测，抽检结果作为观测信号，Beta-Binomial 用于信念更新，MOE/EDI 用于暴露风险度量，DQN 用于在信念-风险特征空间学习动态抽检配置策略。",
        "",
        "但是，文档对正式 DQN 的若干关键数值参数没有给出可直接训练的最终值。因此本轮只生成模型规范草案和参数确认表，不允许进入正式训练。",
        "",
        "## 按建模模块抽取",
    ]
    labels = {
        "state": "State / belief-MDP 状态",
        "observation": "Observation / 观测",
        "action": "Action / 动作",
        "reward": "Reward / 损失函数",
        "constraint": "Constraints / 预算与产能约束",
        "transition": "Transition / belief update",
        "episode_training": "DQN 训练参数",
    }
    for key, label in labels.items():
        lines.extend(["", f"### {label}", ""])
        vals = snippets.get(key, [])
        if vals:
            for p in vals[:12]:
                lines.append(f"- {p[:800]}")
        else:
            lines.append("- 未在文档中找到足够明确的对应段落。")
    lines.extend([
        "",
        "## 不得由 Codex 自行定稿的关键项",
        "",
        "- 动作空间与每档抽检批次数",
        "- 每期预算、单位抽检成本、检测产能上限",
        "- 区域/环节最低覆盖约束",
        "- 处置/召回损失、风险损失权重、信息价值权重、约束违约惩罚",
        "- DQN 网络结构、learning rate、gamma、epsilon、replay buffer、batch size、episode 数",
        "",
        "## 输出",
        "",
        "- `06_配置参数/dqn_model_spec_from_research_plan.yaml`",
        "- canonical: `project_state/dqn_model_spec_from_document.yaml`",
        "- canonical: `references/processed_summaries/dqn_model_spec_summary.md`",
    ])
    return "\n".join(lines) + "\n"


def report_zotero(rows: list[dict], issues: list[dict]) -> str:
    total = len(rows)
    bad = sum(1 for r in rows if r["note是否乱码"] == "是")
    pdfs = sum(1 for r in rows if r["是否有PDF"] == "是")
    lines = [
        "# DQN Zotero 文献与 Note 编码查验报告",
        "",
        f"- Zotero 工作流目录：`{ZOTERO_DIR}`",
        f"- 相关文献/note 记录数：{total}",
        f"- 有可定位 PDF 的记录数：{pdfs}",
        f"- 疑似 `?????` 或 mojibake 乱码 note：{bad}",
        "",
        "## 判断",
        "",
        "本轮对 Zotero 目录中的 Markdown/CSV/TXT/PDF 做关键词扫描，并对 note 中的 `?????`、Unicode replacement character 与常见 UTF-8 误解码片段进行计数。疑似乱码 note 不作为正式模型依据，需追溯 PDF 或正式出版页面。",
        "",
        "## 可作为方法背景的重点材料",
        "",
    ]
    for row in rows[:30]:
        lines.append(f"- **{row['标题']}**：PDF={row['是否有PDF']}；全文读取={row['是否读取全文']}；note乱码={row['note是否乱码']}；作用={row['对DQN设定作用']}；正式依据判断={row['是否可作正式方法依据']}")
    if issues:
        lines.extend(["", "## 编码/PDF 问题", ""])
        for issue in issues[:40]:
            lines.append(f"- `{issue['文件']}`：{issue['问题类型']}；{issue['说明']}；处理={issue['处理']}")
    lines.extend([
        "",
        "## 结论",
        "",
        "Zotero 文献可以作为 DQN/POMDP/safe RL/MOE 的方法背景，但正式模型设定必须以用户研究计划和参数确认表为准。若 note 乱码或仅摘要级阅读，不得作为正式参数依据。",
    ])
    return "\n".join(lines) + "\n"


def report_external_lit() -> str:
    lines = [
        "# DQN 联网补充文献方法支持报告",
        "",
        "联网文献仅用于补充方法背景，不覆盖用户研究计划。若外部文献与用户文档冲突，以用户文档为准。",
        "",
        "## 候选文献",
        "",
    ]
    for item in EXTERNAL_LITERATURE:
        lines.append(f"- **{item['title']}** ({item['year']}, {item['source']}): {item['role']} URL: {item['url']}")
    lines.extend([
        "",
        "## 对本项目的边界",
        "",
        "- DQN 原始文献只说明 Q-learning + 深度网络函数逼近的算法基础，不定义本项目动作、预算和 reward。",
        "- safe/constrained RL 文献支持把预算、产能、安全阈值作为约束，但具体阈值必须由用户确认。",
        "- 食品安全监测优化文献支持预算受限监测设计，但不提供本项目可直接套用的抽检成本和召回损失。",
        "- MOE/AFB1 文献支持风险度量方向，但正式 BMDL、消费量高分位和风险惩罚映射仍需确认。",
    ])
    return "\n".join(lines) + "\n"


def report_environment(checks: list[dict]) -> str:
    my_torch = next((c for c in checks if c["检查项"] == "myevn1_python_torch"), {})
    discovered_torch = next((c for c in checks if c["检查项"] == "discovered_myenv1_python_torch_with_kmp_workaround"), {})
    default_torch = next((c for c in checks if c["检查项"] == "default_python_torch"), {})
    my_ok = my_torch.get("状态") == "PASS"
    discovered_ok = discovered_torch.get("状态") == "PASS"
    default_ok = default_torch.get("状态") == "PASS"
    lines = [
        "# DQN Python / torch 环境查验报告",
        "",
        "## 结论",
        "",
        f"- 默认 Python torch 可用：{'是' if default_ok else '否'}",
        f"- 用户指定的 `D:/anaconda3/envs/myevn1/python.exe` torch 可用：{'是' if my_ok else '否'}",
        f"- 实际发现的 `D:/anaconda3/envs/myenv1/python.exe` torch 可用：{'是，但需要 KMP_DUPLICATE_LIB_OK=TRUE 才能绕过 OpenMP 冲突' if discovered_ok else '否'}",
        f"- 正式 DQN 推荐解释器：`{'D:/anaconda3/envs/myevn1/python.exe' if my_ok else ('D:/anaconda3/envs/myenv1/python.exe（需用户确认是否为 myevn1 的拼写差异，并修复/接受 OpenMP workaround）' if discovered_ok else '待修复；当前未确认 torch 可用')}`",
        "",
        "## 命令结果",
        "",
    ]
    for c in checks:
        lines.extend([
            f"### {c['检查项']}",
            "",
            f"- 状态：{c['状态']}",
            f"- 命令：`{c['命令']}`",
            "```text",
            c.get("stdout", ""),
            c.get("stderr", ""),
            "```",
            "",
        ])
    lines.extend([
        "## 配置建议",
        "",
        "- 如果用户确认 `myenv1` 即目标环境，后续正式 DQN 可优先使用该解释器，但应先处理 OpenMP runtime 冲突。",
        "- `myenv1` 当前缺少 `sklearn`；正式 DQN 仅用 PyTorch 时不一定阻断，但若评估/预处理依赖 sklearn，需要补装或改写。",
        "- 本轮只写入 `project_state/environment_notes.md`，不新增 `.env`，避免未确认配置影响其他流程。",
    ])
    return "\n".join(lines) + "\n"


def report_missing(rows: list[dict], data_rows: list[dict]) -> str:
    needs = [r for r in rows if r["是否需要我手动确认"] == "是"]
    lines = [
        "# DQN 正式建模缺失项与参数确认报告",
        "",
        "## 结论",
        "",
        "当前不允许运行正式 DQN。原因不是上游数据完全不可用，而是正式决策参数尚未由用户确认；尤其是动作空间、预算、成本、产能、损失与 reward 权重。",
        "",
        f"- 需要用户确认的参数项：{len(needs)}",
        "- 已生成参数确认表：`02_表格输出/dqn_parameter_confirmation_table.csv`",
        "",
        "## 当前 canonical 数据可用性",
        "",
    ]
    for r in data_rows:
        lines.append(f"- {r['产物']}：存在={r['存在']}；行数估计={r.get('行数估计','')}；路径=`{r['路径']}`")
    lines.extend(["", "## 必须确认的关键参数", ""])
    for r in needs:
        lines.append(f"- {r['参数名称']}：{r['文档是否已指定']}；建议={r['Codex建议值']}；formal={r['是否允许作为formal DQN参数']}")
    lines.extend([
        "",
        "## 本轮禁止事项执行情况",
        "",
        "- 未运行正式 DQN。",
        "- 未使用 sklearn 替代正式 DQN。",
        "- 未修改 `data/01_raw`。",
        "- 未把 `20260425_1132_DQN初步运行` 的 sandbox 设定作为正式依据。",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    ensure_dirs()
    errors: list[dict] = []

    paragraphs, tables = read_docx_full(DOCX_PATH)
    snippets = context_snippets(paragraphs)
    spec = classify_doc_spec(snippets)
    yaml_text = to_yaml(spec) + "\n"
    write_text(DIRS["configs"] / "dqn_model_spec_from_research_plan.yaml", yaml_text)
    write_text(DIRS["configs"] / "dqn_model_spec_from_document.yaml", yaml_text)
    write_text(ROOT / "project_state" / "dqn_model_spec_from_document.yaml", yaml_text)

    research_report = report_research_plan(paragraphs, tables, snippets, spec)
    write_text(DIRS["reports"] / "dqn_research_plan_extraction_report.md", research_report)
    summary = "\n".join([
        "# DQN 模型规范摘要",
        "",
        "本摘要由研究计划完整 DOCX 抽取得到。正式 DQN 必须以该文档和用户后续确认的参数表为准。",
        "",
        "## 已明确方向",
        "",
        "- 问题框架：受限 POMDP / belief-MDP / 深度强化学习。",
        "- 隐状态：真实污染或风险水平不可直接观测。",
        "- 观测：抽检结果、浓度、合格/不合格、AFB1相关风险信号。",
        "- 信念更新：Beta-Binomial 和跨期遗忘/传播。",
        "- 风险度量：MOE/EDI 与人口/消费量/BMDL 参数。",
        "- 决策：预算和产能约束下的跨区域/环节抽检资源配置。",
        "",
        "## 尚未正式指定",
        "",
        "- 动作档位、预算、成本、产能、召回/处置损失、信息价值权重、reward 权重。",
        "- DQN 网络结构、学习率、gamma、epsilon、replay buffer、batch size、episode 数、训练/验证划分。",
    ]) + "\n"
    write_text(ROOT / "references" / "processed_summaries" / "dqn_model_spec_summary.md", summary)

    zotero_rows, issue_rows = scan_zotero()
    write_csv(DIRS["tables"] / "dqn_zotero_literature_inventory.csv", zotero_rows)
    write_csv(DIRS["logs"] / "dqn_zotero_note_encoding_issue_log.md.csv", issue_rows, ["文件", "问题类型", "说明", "处理"])
    issue_md = "# DQN Zotero note 编码问题日志\n\n"
    if issue_rows:
        issue_md += "\n".join(f"- `{r['文件']}`：{r['问题类型']}；{r['说明']}；处理={r['处理']}" for r in issue_rows) + "\n"
    else:
        issue_md += "- 未发现达到阈值的大量 `?????` 或 replacement-character 乱码 note。\n"
    write_text(DIRS["logs"] / "dqn_zotero_note_encoding_issue_log.md", issue_md)
    write_text(DIRS["reports"] / "dqn_zotero_literature_audit.md", report_zotero(zotero_rows, issue_rows))

    write_csv(DIRS["tables"] / "dqn_external_literature_candidates.csv", EXTERNAL_LITERATURE)
    write_text(DIRS["reports"] / "dqn_literature_method_support_report.md", report_external_lit())

    env_rows = environment_audit()
    write_csv(DIRS["tables"] / "dqn_environment_check.csv", env_rows)
    write_text(DIRS["reports"] / "dqn_python_environment_audit.md", report_environment(env_rows))
    my_ok = any(r["检查项"] == "myevn1_python_torch" and r["状态"] == "PASS" for r in env_rows)
    discovered_ok = any(r["检查项"] == "discovered_myenv1_python_torch_with_kmp_workaround" and r["状态"] == "PASS" for r in env_rows)
    env_notes = "\n".join([
        "# Environment Notes",
        "",
        f"- Last checked: {datetime.now().isoformat(timespec='seconds')}",
        f"- Default Python: see `{DIRS['tables'] / 'dqn_environment_check.csv'}`",
        f"- User-specified `D:/anaconda3/envs/myevn1/python.exe` exists and torch available: {'yes' if my_ok else 'no'}",
        f"- Discovered `D:/anaconda3/envs/myenv1/python.exe` torch available with KMP workaround: {'yes' if discovered_ok else 'no'}",
        f"- Formal DQN interpreter: {'D:/anaconda3/envs/myevn1/python.exe' if my_ok else ('D:/anaconda3/envs/myenv1/python.exe after user confirms path typo and OpenMP handling' if discovered_ok else 'not confirmed; do not run formal DQN')}",
        "- Do not downgrade formal DQN to sklearn only because default Python lacks torch.",
    ]) + "\n"
    write_text(ROOT / "project_state" / "environment_notes.md", env_notes)

    data_rows = current_data_inventory()
    write_csv(DIRS["tables"] / "dqn_current_canonical_data_inventory.csv", data_rows)
    param_rows = parameter_confirmation_rows(spec)
    write_csv(DIRS["tables"] / "dqn_parameter_confirmation_table.csv", param_rows)
    write_csv(ROOT / "project_state" / "dqn_parameter_confirmation_table.csv", param_rows)
    write_text(DIRS["reports"] / "dqn_missing_requirements_report.md", report_missing(param_rows, data_rows))

    inputs_md = "\n".join([
        "# 输入说明",
        "",
        f"- 研究计划 DOCX：`{DOCX_PATH}`",
        f"- Zotero 文库：`{ZOTERO_DIR}`",
        "- canonical 数据：见 `outputs/_index/latest_canonical_outputs.yaml`",
        "- 上次 DQN 初跑工作包仅作为 sandbox prototype 背景，不作为正式设定依据。",
        "- 本轮未修改 `data/01_raw`，未运行正式 DQN。",
    ]) + "\n"
    write_text(DIRS["inputs"] / "inputs.md", inputs_md)

    error_log = "# DQN pre-run audit error log\n\n"
    if errors:
        error_log += "\n".join(f"- {e}" for e in errors) + "\n"
    else:
        error_log += "- 未发生阻断性错误；所有降级或限制已在对应报告记录。\n"
    write_text(DIRS["logs"] / "dqn_pre_run_audit_error_log.md", error_log)

    readme = "\n".join([
        "# DQN 文档驱动建模准备与参数确认",
        "",
        "本任务包用于正式 DQN 之前的文档、文献、环境和参数 readiness 查验。未运行正式 DQN。",
        "",
        "## 关键结论",
        "",
        "- 已完整读取研究计划 DOCX，并抽取 DQN/POMDP/belief-MDP 相关规范。",
        "- `project_state/dqn_model_spec_from_document.yaml` 原本不存在，本轮已从文档抽取并同步 canonical。",
        "- 已查验 Zotero 文库、note 编码和本地 PDF 可用性。",
        f"- 用户指定的 `D:/anaconda3/envs/myevn1/python.exe` torch 可用：{'是' if my_ok else '否，路径不存在或不可运行'}。",
        f"- 实际发现的 `D:/anaconda3/envs/myenv1/python.exe` torch 可用：{'是，但需 OpenMP workaround' if discovered_ok else '否'}。",
        "- 当前不允许运行正式 DQN；需先确认参数表。",
        "",
        "## 主要文件",
        "",
        "- `04_报告输出/dqn_research_plan_extraction_report.md`",
        "- `04_报告输出/dqn_zotero_literature_audit.md`",
        "- `04_报告输出/dqn_literature_method_support_report.md`",
        "- `04_报告输出/dqn_python_environment_audit.md`",
        "- `04_报告输出/dqn_missing_requirements_report.md`",
        "- `02_表格输出/dqn_parameter_confirmation_table.csv`",
        "- `06_配置参数/dqn_model_spec_from_research_plan.yaml`",
    ]) + "\n"
    write_text(RUN_DIR / "README.md", readme)

    manifest_rows = []
    for path in RUN_DIR.rglob("*"):
        if path.is_file():
            manifest_rows.append({
                "path": str(path.relative_to(RUN_DIR)).replace("\\", "/"),
                "category": path.parts[-2] if len(path.parts) > 1 else "root",
                "bytes": path.stat().st_size,
            })
    write_csv(RUN_DIR / "manifest.csv", manifest_rows, ["path", "category", "bytes"])

    print(json.dumps({
        "run_dir": str(RUN_DIR),
        "doc_paragraph_rows": len(paragraphs),
        "zotero_records": len(zotero_rows),
        "zotero_issues": len(issue_rows),
        "myevn1_torch": my_ok,
        "discovered_myenv1_torch_with_kmp": discovered_ok,
        "formal_dqn_allowed": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
