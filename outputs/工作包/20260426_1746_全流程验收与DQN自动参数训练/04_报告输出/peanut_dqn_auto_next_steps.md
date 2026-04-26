# 下一步

1. 用户逐项确认 DQN 参数表中的 action、budget、capacity、cost、reward 和 transition 假设。
2. 用确认后的参数生成 formal config，不覆盖本轮 experimental config。
3. 重新运行环境 smoke test、上游审计和 formal DQN 训练。
4. 将 formal 结果与本轮 experimental 结果做敏感性对照。
