# DQN Code Reproducibility Notes

    ## 可复现条件

    - 使用 `D:\anaconda3\envs\myenv1\python.exe`
    - CUDA/PyTorch 环境须通过 smoke test
    - canonical feature tables 不变
    - random seed、reward weights、budget/capacity、ACTION_VALUES 与 config 固定

    ## formal 前需确认

    action space、budget、unit cost、capacity、minimum coverage、reward weights、transition assumptions、training hyperparameters、baseline protocol、evaluation metrics。

    ## 风险

    - reward 权重可能驱动策略偏好，存在 reward hacking 风险。
    - transition 近似尚未 formal 化。
    - Q-learning 当前领先 DQN，说明 DQN 训练稳定性/样本效率仍需进一步验证。
    - 图表和 DOCX 需要 render QA，不能只看文件存在。
