# Reference Document Reader

## When To Use

Use this skill before major data cleaning, label engineering, simulation, machine learning, optimization, visualization, or report-writing tasks when relevant files may exist under `references/`. Also use it when the user explicitly asks Codex to read a Word/PDF outline, methodology note, model plan, data-cleaning plan, standard, paper, or informal research note.

## Supported Inputs

- `.docx`: Extract paragraph and table text with `python-docx` when possible.
- `.pdf`: Extract text from text-based PDFs with `pypdf` when possible.
- `.md` and `.txt`: Read as plain text.
- `.csv`: Inspect as tabular reference material, preserving source column names.
- `.xlsx`: Inspect workbook sheets, headers, and reference tables without treating them as raw research data unless the user asks.

Scanned PDFs, encrypted PDFs, damaged files, or image-only documents may not be readable because OCR is not enabled by default. Report that limitation clearly.

## Outputs

- Chinese reference summary.
- Extracted methodological requirements.
- Checklist for future workflow execution.
- Potential conflicts, assumptions, or unclear instructions.
- Recommended use in the current workflow.
- Optional processed summary saved under `references/processed_summaries/`.

## Recommended Workflow

1. Identify reference files relevant to the current task from `references/`.
2. Read only the needed files and avoid treating reference materials as raw datasets.
3. Extract actionable guidance for:
   - data cleaning and matching;
   - label engineering and target construction;
   - simulation, Monte Carlo, MDP, reinforcement learning, or optimization;
   - machine learning model framing, feature use, split strategy, metrics, and tuning;
   - visualization design and reporting requirements.
4. Summarize findings in Chinese by default.
5. Preserve technical terms in English when appropriate, including algorithm names, model names, package names, parameter names, metrics, and official standard names.
6. Preserve original source field names and do not blindly translate columns, labels, or standard clauses.
7. Do not blindly apply a reference. Check it against the user instruction, actual dataset evidence, repository rules, and privacy constraints.
8. If references conflict with user instructions, user explicit instruction wins.
9. If references conflict with observed dataset evidence, actual dataset evidence wins and the conflict should be recorded.
10. Save durable extracted guidance to `references/processed_summaries/` when it will guide future workflow stages.

## Summary Format

Use a concise Chinese structure:

- `参考文件`: file path and document type.
- `核心内容`: short Chinese summary.
- `可执行要求`: concrete cleaning/modeling/visualization/reporting requirements.
- `适用范围`: where this guidance should influence the workflow.
- `冲突与限制`: unreadable sections, scanned PDFs, ambiguous guidance, or conflicts.
- `建议用法`: how future workflow steps should cite or apply the reference.

