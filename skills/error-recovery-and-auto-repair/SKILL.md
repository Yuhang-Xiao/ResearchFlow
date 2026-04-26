---
name: error-recovery-and-auto-repair
description: Recover from lightweight workflow errors and decide when to stop. Use when Codex encounters missing lightweight dependencies, path or encoding failures, Chinese filename issues, table or chart output failures, Excel sheet mismatches, optional parser failures, ordinary dtype conversion errors, or any scientific workflow error that might be safely repaired without user input.
---

# Error Recovery and Auto Repair

## When To Trigger

Use this skill whenever a workflow step fails or degrades because of dependencies, file paths, encodings, output formats, chart/table rendering, sheet selection, optional parsers, directory creation, or lightweight code errors.

Also use it before asking the user for help: first decide whether the error is safely auto-repairable.

## Errors To Auto-Repair

Attempt autonomous repair for:

- Missing lightweight Python packages when a standard-library or existing-dependency substitute is available.
- Missing `tabulate`, `matplotlib`, `seaborn`, `openpyxl`, `python-docx`, `pypdf`, or similar lightweight optional packages.
- Charting failures; substitute SVG, CSV summaries, Markdown tables, or text summaries.
- Markdown table rendering failures; use an internal Markdown table helper.
- Word/PDF failures caused by Chinese paths, spaces, or special characters; use `pathlib`, relative paths, directory scanning, and filename matching.
- Excel sheet-name mismatches; inspect available sheets and choose the most plausible sheet based on headers, dimensions, and task goal.
- Missing output folders; create them.
- Output format failures; use CSV instead of XLSX, SVG instead of PNG, or Markdown instead of rich formatting.
- Non-critical figure failures; continue core tables and reports while recording the skipped figure.
- Encoding, path, missing-directory, lightweight code, and ordinary dtype conversion errors.
- Incomplete regex rules, minor field-name mismatches, inconsistent unit spellings, and stale derived reports when they can be repaired from available raw or cleaned data.

## Errors That Must Stop

Stop and ask the user only when:

- Raw data are missing, corrupted, or unreadable.
- A required research plan or reference document is missing and the task cannot proceed without it.
- Critical fields are completely unidentifiable and no reasonable substitute exists.
- API keys, login, paid access, external database permission, MCP/Zotero configuration, or other manual authorization is required.
- Critical external parameters must be supplied by the user, such as consumption, population, BMDL, budget, cost, capacity limits, recall losses, or policy constraints.
- A repair may overwrite, mutate, or damage `data/01_raw`.
- Different cleaning choices would materially change scientific conclusions and require user selection.
- The available repair would create clearly unreliable results.
- Memory or compute limits cannot be solved by chunking, streaming, sampling, or degraded outputs.
- An unresolved upstream concentration, AFB1 label, count panel, or belief-state defect would affect downstream modeling conclusions.

## Auto-Repair Priority Strategy

1. Classify the error as auto-repairable, degradable, or must-stop.
2. Preserve raw inputs and existing outputs unless the user requested replacement.
3. Try 1-3 minimal fixes, starting with the least invasive:
   - Switch path handling to `pathlib`, relative paths, directory scan, or filename matching.
   - Swap optional libraries for standard-library or already-installed alternatives.
   - Change only the failed output format while keeping core data products.
   - Use chunking, dtype coercion, encoding fallback, or safer parsing for ordinary data-read issues.
4. Continue the workflow only when the repaired output is scientifically acceptable.
5. If repair changes interpretability, precision, completeness, or downstream assumptions, mark the result for manual review.

## Degraded Execution Records

Every repair or downgrade must be recorded in the task report or `reports/*_error_log.md` with:

- Original error type and message.
- Location or stage.
- Repair or downgrade attempted.
- Final status: repaired, degraded but continued, or unresolved.
- Effect on outputs and scientific conclusions.
- Whether manual review is needed.

## Project State Updates

At the end of a durable task:

- Update `project_state/lessons_learned.md` with reusable repair lessons.
- Update `project_state/decision_log.md` if the repair affects later workflow design, accepted outputs, model assumptions, or interpretation.
- Update `project_state/conversation_handoff.md` if a future Codex conversation must know about the repair or downgrade.
- Keep `project_state/next_step.md` focused on the next scientific step, not routine repaired errors.
