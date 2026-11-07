# 按操作系统选择代码入口

| 你的系统 | 独立安装与运行说明 | 运行入口 |
| --- | --- | --- |
| macOS，Apple Silicon / Intel | [macOS](macOS/README.md) | `bash macOS/run_examples.sh python` |
| Windows PowerShell | [Windows](Windows/README.md) | `py -3 run_examples.py python` |
| Ubuntu / Windows 内的 WSL Ubuntu | [Ubuntu-WSL](Ubuntu-WSL/README.md) | `bash Ubuntu-WSL/run_examples.sh python` |

先进入本目录，再执行表中的命令。`python` 表示运行四个 Python 例子；换成 `rtl` 会运行 RTL 仿真，换成 `chisel` 会构造并打印 RTL。先按自己系统的说明安装对应工具。

本目录中的 `.py`、`.sv` 和 `.scala` 是共用教学源代码。三个系统的目录分别放安装说明与启动脚本，便于按系统学习。启动脚本不会自动安装软件或更改系统设置。

- Python 例子只依赖标准库。
- RTL 例子需要 `iverilog` 和 `vvp`；输出写入 `.outputs/`，包括计数器波形。
- Chisel 需要 Scala CLI、网络及其管理的 Java 21；依赖固定在 `chisel_project.scala`。生成与仿真是不同步骤。
- 已有 Java 21 时可给 chisel 组加 `--java-home` 指定 JDK 路径，跳过自动下载 JDK；具体命令见各系统说明。
- `rtl` 组第四项测试使用仓库已有的 `SafetyGate.generated.sv`；它不会自动使用刚刚打印出来的 Chisel 结果。

具体文件解释与实际测试范围见 [示例说明与验证记录](示例说明与验证记录.md)。本次补充了 macOS 操作步骤，当前环境没有实体 Mac，不能把文档核对写成 macOS 实测通过。
