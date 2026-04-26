# DQN auto training error log

任务性质：自动合成参数 DQN 实验版 / self-synthesized DQN experimental run


## 自动修复补充

- reward/Q/loss 数量级异常：人口加权风险 proxy 未归一化；修复为 P95 归一化后重训，结果可审计。
- Matplotlib CJK 字体 warning：图表已生成，建议后续配置中文字体改善显示，不影响 CSV/Excel/模型。
