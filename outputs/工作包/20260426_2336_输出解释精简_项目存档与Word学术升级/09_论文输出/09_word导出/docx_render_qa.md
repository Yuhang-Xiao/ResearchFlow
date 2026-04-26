# DOCX Render QA

- DOCX: `09_论文输出/09_word导出/dqn_results_academic_with_figures.docx`
- Renderer: artifact-tool
- Rendered pages: `09_论文输出/09_word导出/rendered_pages/`
- Pages rendered: 5
- QA status: pass
- Notes: 原生 Word 表格在 artifact-tool 中会竖排，因此最终 Word 使用 PNG 化论文表格预览，并保留 `academic_results_evidence_table.csv` 作为可复制证据表。核心图表已嵌入 Word，页面渲染可读，无明显竖排表格或中文乱码。
