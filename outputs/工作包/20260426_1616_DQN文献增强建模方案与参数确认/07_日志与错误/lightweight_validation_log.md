# 轻量验证日志

- 直接使用 D:\anaconda3\envs\myenv1\python.exe -c "import workflow1" 失败：该 conda 环境未安装当前仓库包。
- 自动修复：设置 PYTHONPATH=D:\桌面\codex\workflow1\src 后验证。
- import workflow1 with PYTHONPATH 返回码：0
- python -m workflow1 --stage launch with PYTHONPATH 返回码：0

说明：这不影响 DQN 环境本身；正式脚本运行时应显式设置工作目录/PYTHONPATH，或先执行可追踪的 editable install。
