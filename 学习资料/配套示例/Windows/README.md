# Windows：PowerShell 运行说明

Python 与策略模型可以原生运行；RTL 与 Chisel 可选择原生工具，或进入已安装的 WSL Ubuntu，并改用 [Ubuntu-WSL 说明](../Ubuntu-WSL/README.md)。本页命令在 PowerShell 中执行。

## 1. 安装并定位目录

从 [Python 官网](https://www.python.org/downloads/windows/) 安装 Python 3，保留 Python Launcher（若安装器提供）。重新打开 PowerShell，检查：

```powershell
py -3 --version
```

没有 `py` 而已有 `python` 时，可将下文 `py -3` 换成 `python`。本项目不要求两套 Python 同时安装。

打开你电脑上的“配套示例”目录；下面是本资料作者的路径，需要按自己的位置修改：

```powershell
Set-Location -LiteralPath 'D:\Projects\毕设\学习资料\配套示例'
```

也可以在文件管理器中进入“配套示例”，在地址栏输入 `powershell` 并按回车。确认 `Get-ChildItem` 能列出 `.py` 和 `.sv` 文件。

## 2. 运行 Python

```powershell
py -3 run_examples.py python
```

或者依次执行：

```powershell
py -3 process_demo.py
py -3 pipe_demo.py
py -3 terminate_demo.py
py -3 policy_model.py
```

也提供 `Windows/run_examples.ps1`，可在执行策略允许时运行 `& '.\Windows\run_examples.ps1' python`。若被执行策略阻止，直接使用上面的 Python 命令，无需为学习修改全局执行策略。

## 3. 运行 RTL

若原生环境已有 [Icarus Verilog](https://steveicarus.github.io/iverilog/usage/installation.html)，确保 `Get-Command iverilog,vvp` 能找到工具，再执行：

```powershell
py -3 run_examples.py rtl
```

没有原生工具时，可使用 WSL Ubuntu 路径。WSL 属于 Windows 的 Linux 环境，进入后按 Ubuntu 的命令安装；不要在 PowerShell 直接输入 `sudo apt install ...`。

```powershell
wsl
```

进入 WSL 后打开 [Ubuntu-WSL 说明](../Ubuntu-WSL/README.md)，D 盘路径对应 `/mnt/d/`。没有 WSL 的读者可先按 [微软官方安装说明](https://learn.microsoft.com/windows/wsl/install) 安装，或先完成手算，不强制本周装完整系统环境。

## 4. 运行 Chisel

WinGet 可用时，按 Scala CLI 官方安装方式执行：

```powershell
winget install virtuslab.scalacli
```

安装后重新开终端，回到示例目录：

```powershell
scala-cli version
py -3 run_examples.py chisel
```

启动器会指定 `--jvm 21`，Scala CLI 按需管理 JDK。若原生 Windows 后端不支持或失败，可转到 WSL 完成 Chisel 生成；已有 `SafetyGate.generated.sv` 也可先做仿真。

如果已有 Java 21 且自动下载 JDK 卡住，可用 `py -3 run_examples.py chisel --java-home '你的 JDK 21 目录'` 指向已有 JDK；该目录应包含 `bin\java.exe`。

## 5. Windows 的进程终止行为

`terminate_demo.py` 在 Windows 使用 TerminateProcess。不要用 Linux 的 `-15` 作为唯一正确答案；本次环境此前观察到退出码 1。重点是已知子进程结束，并且父进程完成等待。

详细背景见 [Python subprocess](https://docs.python.org/3/library/subprocess.html)、[Scala CLI 安装](https://scala-cli.virtuslab.org/install/) 和 [Chisel 安装](https://www.chisel-lang.org/docs/installation)。
