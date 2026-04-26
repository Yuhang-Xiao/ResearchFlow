# DOCX 渲染 QA

- DOCX：`09_论文输出/09_word导出/results_draft.docx`
- 渲染器：documents skill artifact-tool renderer
- 渲染页数：1
- 页面 PNG：`09_论文输出/09_word导出/rendered_pages/page-1.png`
- 视觉检查：通过；未见文字重叠、表格挤压、裁切或缺字。
- 说明：渲染命令退出码为 0；控制台 reader thread 出现一次 GBK 解码警告，但页面 PNG 已正常生成，不影响页面 QA。
