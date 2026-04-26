# DQN myenv1 PyTorch CUDA 12.6 重装报告

## 执行范围

- 目标解释器：`D:\anaconda3\envs\myenv1\python.exe`
- 未使用默认 `python` 进行安装、验证或 smoke test。
- 未使用 base 环境。
- 未使用错误路径 `D:\anaconda3\envs\myevn1\python.exe`。
- 未删除整个 `myenv1` 环境。
- 未运行正式 DQN 训练。

## 卸载前状态

- `sys.executable`: `D:\anaconda3\envs\myenv1\python.exe`
- `pip -V`: `D:\anaconda3\envs\myenv1\Lib\site-packages\pip`
- 原 PyTorch：`torch 2.11.0+cu130`
- 原 CUDA build：`torch.version.cuda = 13.0`
- 原 CUDA 可用性：`False`
- 原 GPU device count：`0`

## 卸载结果

- 已卸载：`torch 2.11.0+cu130`
- 已卸载：`torchvision 0.26.0+cu130`
- `torchaudio` 卸载时原本未安装。
- 卸载后 `pip list | findstr /I "torch torchvision torchaudio triton nvidia cuda"` 未再列出 cu130 相关包。
- pip 报告 `~orch` 临时目录残留警告；本轮未手动删除目录，避免越过“只卸载/重装 Python 包”的边界。

## 安装结果

使用官方 PyTorch CUDA 12.6 wheel 源：

`https://download.pytorch.org/whl/cu126`

安装成功：

- `torch 2.11.0+cu126`
- `torchvision 0.26.0+cu126`
- `torchaudio 2.11.0+cu126`

安装后验证：

- `torch.__version__`: `2.11.0+cu126`
- `torch.version.cuda`: `12.6`
- `torch.cuda.is_available()`: `True`
- `torch.cuda.device_count()`: `1`
- GPU: `NVIDIA GeForce RTX 4060 Ti`
- OpenMP 冲突：未再观察到。

## 日志

- `07_日志与错误/env_before_pytorch_reinstall.txt`
- `07_日志与错误/pytorch_uninstall_log.txt`
- `07_日志与错误/pytorch_cu126_install_log.txt`
- `07_日志与错误/post_install_validation_log.txt`
- `07_日志与错误/torch_gpu_smoke_test_log.txt`
