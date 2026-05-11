"""Generic LaTeX paper package exporter for workflow1."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


LATEX_SPECIALS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
}


def latex_escape(text: object) -> str:
    value = "" if text is None else str(text)
    return "".join(LATEX_SPECIALS.get(ch, ch) for ch in value)


def _latex_cell(text: object, max_len: int | None = None) -> str:
    value = "" if text is None else str(text)
    if max_len and len(value) > max_len:
        value = value[: max_len - 1] + "."
    value = latex_escape(value)
    return (
        value.replace("/", r"/\allowbreak ")
        .replace("-", r"-\allowbreak ")
        .replace(":", r":\allowbreak ")
        .replace(r"\_", r"\_\allowbreak ")
    )


def write_latex_table(path: str | Path, headers: list[str], rows: list[list[object]], caption: str, label: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    spec = "p{0.22\\linewidth}" * len(headers)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{latex_escape(caption)}}}",
        rf"\label{{{label}}}",
        rf"\begin{{tabular}}{{{spec}}}",
        r"\toprule",
        " & ".join(latex_escape(h) for h in headers) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(latex_escape(cell) for cell in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_compact_latex_table(
    path: str | Path,
    headers: list[str],
    rows: list[list[object]],
    caption: str,
    label: str,
    *,
    notes: str = "",
    column_spec: str | None = None,
) -> None:
    """Write a page-safe main-text table.

    Uses ``tabularx`` and ``adjustbox`` so long labels wrap instead of
    colliding with neighboring columns. This is intended for main-paper tables,
    not exhaustive appendices.
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    spec = column_spec or ("l" + "Y" * (len(headers) - 1))
    lines = [
        r"\begin{table}[!htbp]",
        r"\centering",
        r"\small",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        rf"\caption{{{latex_escape(caption)}}}",
        rf"\label{{{label}}}",
        r"\begin{threeparttable}",
        r"\begin{adjustbox}{max width=\textwidth}",
        rf"\begin{{tabularx}}{{\textwidth}}{{{spec}}}",
        r"\toprule",
        " & ".join(rf"\makecell[l]{{{_latex_cell(h, 42)}}}" for h in headers) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(_latex_cell(cell, 120) for cell in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabularx}", r"\end{adjustbox}"])
    if notes:
        lines.extend([r"\begin{tablenotes}[flushleft]", r"\footnotesize", rf"\item {latex_escape(notes)}", r"\end{tablenotes}"])
    lines.extend([r"\end{threeparttable}", r"\end{table}", r"\FloatBarrier"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_longtable_appendix(
    path: str | Path,
    headers: list[str],
    rows: list[list[object]],
    caption: str,
    label: str,
) -> None:
    """Write an appendix longtable with wrapped cells."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    width = max(0.12, 0.92 / max(1, len(headers)))
    spec = "".join([f"p{{{width:.2f}\\textwidth}}" for _ in headers])
    lines = [
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.1}",
        rf"\begin{{longtable}}{{{spec}}}",
        rf"\caption{{{latex_escape(caption)}}}\label{{{label}}}\\",
        r"\toprule",
        " & ".join(_latex_cell(h, 42) for h in headers) + r" \\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        " & ".join(_latex_cell(h, 42) for h in headers) + r" \\",
        r"\midrule",
        r"\endhead",
    ]
    for row in rows:
        lines.append(" & ".join(_latex_cell(cell, 120) for cell in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_references_bib(path: str | Path, entries: list[dict[str, object]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = []
    for entry in entries:
        key = re.sub(r"[^A-Za-z0-9_:-]", "", str(entry["key"]))
        chunks.append(
            "\n".join(
                [
                    f"@{entry.get('type', 'article')}{{{key},",
                    f"  title = {{{latex_escape(entry.get('title', ''))}}},",
                    f"  author = {{{latex_escape(entry.get('author', ''))}}},",
                    f"  year = {{{latex_escape(entry.get('year', ''))}}},",
                    f"  journal = {{{latex_escape(entry.get('journal', ''))}}},",
                    f"  doi = {{{latex_escape(entry.get('doi', ''))}}},",
                    f"  url = {{{latex_escape(entry.get('url', ''))}}}",
                    "}",
                ]
            )
        )
    path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")


def build_article_tex(
    *,
    title: str,
    authors: str,
    abstract: str,
    keywords: list[str],
    sections: dict[str, str],
    bibliography_file: str = "references.bib",
) -> str:
    body = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[a4paper,margin=1in]{geometry}",
        r"\usepackage{fontspec}",
        r"\usepackage{graphicx}",
        r"\usepackage{booktabs}",
        r"\usepackage{longtable}",
        r"\usepackage{array}",
        r"\usepackage{tabularx}",
        r"\usepackage{makecell}",
        r"\usepackage{threeparttable}",
        r"\usepackage{adjustbox}",
        r"\usepackage{siunitx}",
        r"\usepackage{caption}",
        r"\usepackage{subcaption}",
        r"\usepackage{placeins}",
        r"\usepackage[numbers,sort&compress]{natbib}",
        r"\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}",
        r"\usepackage{float}",
        r"\newcolumntype{Y}{>{\raggedright\arraybackslash}X}",
        r"\sisetup{detect-all=true}",
        r"\setmainfont{Times New Roman}",
        rf"\title{{{latex_escape(title)}}}",
        rf"\author{{{latex_escape(authors)}}}",
        r"\date{}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        abstract,
        r"\end{abstract}",
        r"\noindent\textbf{Keywords:} " + latex_escape("; ".join(keywords)),
        "",
    ]
    for heading, text in sections.items():
        body.append(rf"\section{{{latex_escape(heading)}}}")
        body.append(text.strip())
        body.append("")
    body.extend(
        [
            r"\bibliographystyle{plainnat}",
            rf"\bibliography{{{Path(bibliography_file).with_suffix('').as_posix()}}}",
            r"\end{document}",
        ]
    )
    return "\n".join(body) + "\n"


def compile_latex(tex_path: str | Path, timeout: int = 180) -> dict[str, object]:
    tex_path = Path(tex_path)
    latexmk = shutil.which("latexmk")
    if not latexmk:
        return {"status": "fail", "error": "latexmk not found on PATH", "pdf": ""}
    cmd = [latexmk, "-xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    proc = subprocess.run(cmd, cwd=tex_path.parent, text=True, capture_output=True, timeout=timeout)
    log = tex_path.parent / "latex_build_log.txt"
    log.write_text((proc.stdout or "") + "\n\nSTDERR:\n" + (proc.stderr or ""), encoding="utf-8", errors="replace")
    pdf = tex_path.with_suffix(".pdf")
    status = "pass" if proc.returncode == 0 and pdf.exists() and pdf.stat().st_size > 0 else "fail"
    final_log = tex_path.with_suffix(".log")
    final_log_text = final_log.read_text(encoding="utf-8", errors="replace") if final_log.exists() else proc.stdout or ""
    return {
        "status": status,
        "returncode": proc.returncode,
        "pdf": str(pdf) if pdf.exists() else "",
        "log": str(log),
        "undefined_references": "undefined references" in final_log_text.lower(),
        "missing_citations": "undefined citations" in final_log_text.lower(),
    }


def scan_tex_crossrefs(tex: str) -> dict[str, int]:
    citation_groups = re.findall(r"\\cite[tp]?\{([^}]+)\}", tex)
    citation_keys = [key.strip() for group in citation_groups for key in group.split(",") if key.strip()]
    return {
        "figure_labels": len(re.findall(r"\\label\{fig:", tex)),
        "table_labels": len(re.findall(r"\\label\{tab:", tex)),
        "figure_refs": len(re.findall(r"\\ref\{fig:", tex)),
        "table_refs": len(re.findall(r"\\ref\{tab:", tex)),
        "citations": len(citation_keys),
    }
