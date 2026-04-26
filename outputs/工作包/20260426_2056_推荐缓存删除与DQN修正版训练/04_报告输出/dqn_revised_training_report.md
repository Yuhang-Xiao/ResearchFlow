# PEANUT DQN 修正版 experimental training report

- 训练 episodes：281
- 最终 moving average reward：474.810668
- 最终 mean loss：0.128869
- 最终 epsilon：0.050000
- DQN total reward：469.858674
- DQN mean action：3.660234
- DQN constraint violation rate：0.000000

Reward 修正版采用 risk reward、information gain、sampling cost、opportunity penalty、constraint penalty 分解，并使用 robust scale + tanh 做重标度。
