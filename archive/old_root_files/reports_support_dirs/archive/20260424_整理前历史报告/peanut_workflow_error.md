# PEANUT workflow error handling log

## 最终状态

本轮最终流程已成功完成。以下错误均为中间运行阶段发现并已修复的问题，不是未解决阻断错误。

## 已解决错误 1

- 错误类型：`ImportError`
- 错误位置：`scripts/run_peanut_risk_workflow.py` 中 `pandas.DataFrame.to_markdown()` 调用。
- 错误原因：当前 Python 环境缺少 `tabulate`。
- 修复方式：改为脚本内置 Markdown 表格渲染函数，不再依赖 `tabulate`。

## 已解决错误 2

- 错误类型：`ModuleNotFoundError`
- 错误位置：`scripts/run_peanut_risk_workflow.py` 中 `matplotlib` 导入。
- 错误原因：当前 Python 环境缺少 `matplotlib`。
- 修复方式：改为纯 Python 生成 SVG 基础图表，不再依赖 `matplotlib`。

## 未解决错误

无。
