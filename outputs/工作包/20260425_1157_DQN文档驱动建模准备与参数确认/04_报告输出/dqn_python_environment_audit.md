# DQN Python / torch 环境查验报告

## 结论

- 默认 Python torch 可用：否
- 用户指定的 `D:/anaconda3/envs/myevn1/python.exe` torch 可用：否
- 实际发现的 `D:/anaconda3/envs/myenv1/python.exe` torch 可用：是，但需要 KMP_DUPLICATE_LIB_OK=TRUE 才能绕过 OpenMP 冲突
- 正式 DQN 推荐解释器：`D:/anaconda3/envs/myenv1/python.exe（需用户确认是否为 myevn1 的拼写差异，并修复/接受 OpenMP workaround）`

## 命令结果

### default_python_sys

- 状态：PASS
- 命令：`python -c import sys; print(sys.executable); print(sys.version)`
```text
D:\anaconda3\python.exe
3.13.9 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 19:09:58) [MSC v.1929 64 bit (AMD64)]

```

### default_python_torch

- 状态：FAIL
- 命令：`python -c import torch; print(torch.__version__); print(torch.cuda.is_available())`
```text

Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import torch; print(torch.__version__); print(torch.cuda.is_available())
    ^^^^^^^^^^^^
ModuleNotFoundError: No module named 'torch'
```

### myevn1_path_exists

- 状态：FAIL
- 命令：`Test-Path D:\anaconda3\envs\myevn1\python.exe`
```text
False

```

### myevn1_python_sys

- 状态：FAIL
- 命令：`D:\anaconda3\envs\myevn1\python.exe -c import sys; print(sys.executable); print(sys.version)`
```text

FileNotFoundError: [WinError 2] 系统找不到指定的文件。
```

### myevn1_python_torch

- 状态：FAIL
- 命令：`D:\anaconda3\envs\myevn1\python.exe -c import torch; print(torch.__version__); print(torch.cuda.is_available())`
```text

FileNotFoundError: [WinError 2] 系统找不到指定的文件。
```

### myevn1_python_basic

- 状态：FAIL
- 命令：`D:\anaconda3\envs\myevn1\python.exe -c import numpy, pandas, sklearn; print('basic ok')`
```text

FileNotFoundError: [WinError 2] 系统找不到指定的文件。
```

### discovered_myenv1_path_exists

- 状态：PASS
- 命令：`Test-Path D:\anaconda3\envs\myenv1\python.exe`
```text
True

```

### discovered_myenv1_python_sys

- 状态：PASS
- 命令：`D:\anaconda3\envs\myenv1\python.exe -c import sys; print(sys.executable); print(sys.version)`
```text
D:\anaconda3\envs\myenv1\python.exe
3.13.12 | packaged by Anaconda, Inc. | (main, Feb 24 2026, 16:05:56) [MSC v.1942 64 bit (AMD64)]

```

### discovered_myenv1_python_torch_raw

- 状态：FAIL
- 命令：`D:\anaconda3\envs\myenv1\python.exe -c import torch; print(torch.__version__); print(torch.cuda.is_available())`
```text

OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.
```

### discovered_myenv1_python_torch_with_kmp_workaround

- 状态：PASS
- 命令：`D:\anaconda3\envs\myenv1\python.exe -c import torch; print(torch.__version__); print(torch.cuda.is_available())`
```text
2.11.0+cu130
False
D:\anaconda3\envs\myenv1\Lib\site-packages\torch\cuda\__init__.py:180: UserWarning: cudaGetDeviceCount() returned cudaErrorNotSupported, likely using older driver or on CPU machine (Triggered internally at C:\actions-runner\_work\pytorch\pytorch\pytorch\c10\cuda\CUDAFunctions.cpp:88.)
  return torch._C._cuda_getDeviceCount() > 0
```

### discovered_myenv1_python_basic

- 状态：FAIL
- 命令：`D:\anaconda3\envs\myenv1\python.exe -c import numpy, pandas, sklearn; print('basic ok')`
```text

Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import numpy, pandas, sklearn; print('basic ok')
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'sklearn'
```

## 配置建议

- 如果用户确认 `myenv1` 即目标环境，后续正式 DQN 可优先使用该解释器，但应先处理 OpenMP runtime 冲突。
- `myenv1` 当前缺少 `sklearn`；正式 DQN 仅用 PyTorch 时不一定阻断，但若评估/预处理依赖 sklearn，需要补装或改写。
- 本轮只写入 `project_state/environment_notes.md`，不新增 `.env`，避免未确认配置影响其他流程。
