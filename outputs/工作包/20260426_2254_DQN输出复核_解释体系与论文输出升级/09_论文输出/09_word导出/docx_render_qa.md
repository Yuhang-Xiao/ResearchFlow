# DOCX Render QA

- DOCX: `09_论文输出/09_word导出/dqn_results_draft.docx`
- Renderer: artifact-tool via documents skill
- Render output: `09_论文输出/09_word导出/rendered_pages/`
- Pages checked: page-1.png, page-2.png
- QA status: pass
- Notes: Initial native DOCX tables rendered poorly in artifact-tool, so the final Word uses embedded PNG table previews plus source CSV evidence tables. This preserves readability and traceability while avoiding malformed Word table rendering. The source CSV tables remain available for copying and verification.
