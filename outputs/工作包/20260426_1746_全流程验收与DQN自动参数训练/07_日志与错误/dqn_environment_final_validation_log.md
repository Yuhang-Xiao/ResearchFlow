# DQN environment final validation log

说明：第一次 Start-Process 数组传参导致 -c 代码被拆分，已按自动修复策略改用稳健参数字符串重新验证。


## & "D:/anaconda3/envs/myenv1/python.exe" -c "import sys; print(sys.executable)"
ExitCode: 0
STDOUT:
D:\anaconda3\envs\myenv1\python.exe

STDERR:


## & "D:/anaconda3/envs/myenv1/python.exe" -c "import workflow1; print(getattr(workflow1, '__version__', 'NO_VERSION'))"
ExitCode: 0
STDOUT:
0.1.0

STDERR:


## & "D:/anaconda3/envs/myenv1/python.exe" -m workflow1 --stage launch
ExitCode: 0
STDOUT:
{'config_path': '.codex\\config.toml', 'config_loaded': True, 'stage': 'launch', 'status': 'ok', 'details': {'message': 'One-line launch context prepared. No heavy data processing was started.', 'memory_files': ('project_state/project_memory.md', 'project_state/run_protocol.md', 'project_state/current_focus.md', 'project_state/next_step.md', 'project_state/decision_log.md', 'project_state/lessons_learned.md', 'project_state/conversation_handoff.md'), 'raw_files': ('data\\01_raw\\Concentration_and_Consumption pEANUT.xlsx', 'data\\01_raw\\FINAL_SiChuan_2023_ALL_DATA.xlsx', 'data\\01_raw\\PEANUT2023-20241.xlsx', 'data\\01_raw\\PEANUTwithProb0627.xlsx', 'data\\01_raw\\population_long_clean.xlsx', 'data\\01_raw\\raw_data_inventory.csv'), 'reference_files': ('references\\README.md', 'references\\data_cleaning\\README.md', 'references\\literature\\README.md', 'references\\modeling\\README.md', 'references\\notes\\README.md', 'references\\notes\\�����빩Ӧ������ǰ��-�о��ƻ�-Ф�.docx', 'references\\notes\\ʳƷ��ȫ���ռ�����Ż�_Codex���й������ܽ�.docx', 'references\\processed_summaries\\20260426_dqn_literature_enhanced_method_summary.md', 'references\\processed_summaries\\README.md', 'references\\processed_summaries\\dqn_model_spec_summary.md', 'references\\processed_summaries\\peanut_research_plan_summary.md', 'references\\reference_inventory.csv', 'references\\standards\\README.md', 'references\\visualization\\README.md'), 'next_step': '\ufeff# Next Step\n\n��һ��������һ�仰��� dry-run ��ȫ prototype �滮�����磺�����ǰ���ݵ��Զ��������̡���� PEANUT ʳƷ��ȫ���ռ��ȫ���̡����ݵ�ǰ�о�Ŀ���Զ�ѡ��ģ�Ͳ����� prototype��\n\n��Ҫ������ʵ prototype ʵ�飬��Ҫ�û���ȷ����������Ӧ prototype����Ҫ������ʽ DQN���Ա�����ȷ�� project_state/dqn_parameter_confirmation_table.csv �����в�������ȷ��Ȩѵ����', 'notes': ('This launcher only prepares context and recommendations.', 'Use intake/validation/cleaning-plan before actual cleaning.')}}

STDERR:
INFO:workflow1:Loaded config: True
INFO:workflow1:Routing stage: launch


## & "D:/anaconda3/envs/myenv1/python.exe" -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO CUDA')"
ExitCode: 0
STDOUT:
2.11.0+cu126
12.6
True
NVIDIA GeForce RTX 4060 Ti

STDERR:


## & "D:/anaconda3/envs/myenv1/python.exe" -c "import numpy, pandas, sklearn, matplotlib, openpyxl, xlsxwriter, yaml, gymnasium; print('core ok')"
ExitCode: 0
STDOUT:
core ok

STDERR:

