# 这台 Windows 电脑的 VS Code 仿真入口

完整的组件、版本、文件位置和日常流程见 [当前开发环境说明](../../当前开发环境说明.md)。本页保留快速操作与最初安装记录，最新核对日期以环境说明为准。

环境安装在 WSL 的 Ubuntu-24.04 中。Windows 上的 VS Code 负责编辑，Icarus / Verilator 执行仿真，GTKWave 查看波形，Scala CLI 与 Java 21 生成 Chisel RTL。

## 每次怎么打开

在 VS Code 打开 **整个仓库文件夹** `D:\Projects\毕设`，这样才能读到根目录的 `.vscode/tasks.json`。也可以使用 WSL 扩展的“在 WSL 中重新打开文件夹”。Windows 窗口下任务也已配置为调用 Ubuntu-24.04。

## 最先做的两步

1. 按 **Ctrl+Shift+B**：执行默认任务“仿真：计数器（第 2 天）”。终端应出现 `PASS counter4: reset/hold/increment/wrap`。
2. 打开“终端 → 运行任务”，选择 **波形：打开计数器波形**：会先重新仿真，再打开 GTKWave，预先列出 clk、reset、enable、count。

## 其他任务

在“终端 → 运行任务”中选择：

- “仿真：选择器（第 1 天）”
- “仿真：安全停止门（第 2 天）”
- “Chisel：生成安全门 RTL（第 3 天）”
- “Python：进程与策略示例（第 4-5 天）”
- “检查：全部 RTL 示例”
- “检查：仿真环境版本”
- “语法：Verilog 综合示例”：对应 01 册 V6。
- “语法：Chisel 综合示例生成 RTL”：对应 02 册 C6。
- “语法：仿真已有 Chisel 综合示例”：检查仓库里已生成的版本。

右上角的通用“运行文件”按钮不是这里的仿真入口，使用任务菜单即可。改完源文件后先保存，再重新运行相应任务。

## 文件在哪里

计数器设计：`学习资料/配套示例/counter4.sv`。

计数器仿真文件：`学习资料/配套示例/counter4_tb.sv`。

波形输出：`学习资料/配套示例/.outputs/counter4.vcd`。

仿真产物已由 Git 忽略。Chisel 任务优先使用已有的 Java 21，并针对该子进程使用 Maven Central；不会更改你的全局 Maven 或 Java 配置。

## 本机安装与验证记录

安装日期：2026-11-07。Ubuntu-24.04 中已安装 Icarus Verilog 12.0、GTKWave 3.3.116、Verilator 5.020、C/C++ 编译工具和 Scala CLI 1.9.1；使用已有的 OpenJDK 21。Scala CLI 启动器位于 `/usr/local/bin/scala-cli`，JAR 位于 `/opt/scala-cli/`，不再依赖本仓库的临时目录。

VS Code 已安装微软 WSL 扩展与 Verilog HDL 扩展；WSL 内的 VS Code Server 也已准备，远程 Verilog 扩展已安装。

实际验证：

- VS Code 计数器任务对应的 Windows 调用命令运行成功。
- Icarus 四组 RTL 测试通过。
- Verilator 实际编译并运行计数器测试通过。
- Python 四个例子通过。
- Chisel 使用已有 Java 21 成功生成 RTL。
- GTKWave 已打开计数器波形，并预置四个信号和完整时间范围。

本周环境已具备。Chipyard 的完整系统工程与 FPGA 工具链留待后续研究平台明确后再配置。
