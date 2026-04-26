# 输入说明

        本轮处理用户反馈：上一轮解释文件过多、Word 不够像学术论文且图表未充分写入、需要项目存档与缓存/冗余输出清理。

        保护范围：
        - `data/01_raw/`
        - latest DQN training run `outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练`
        - project_state、outputs/_index、canonical experiments
        - 旧 baseline run `outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`

        删除范围仅限：缓存、pycache、我方生成的失败/中间 run 包、过度生成的 `.explanation.md` 侧车和重复 local md。
