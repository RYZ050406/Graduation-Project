# macOS：从零运行配套代码

适用于 Apple Silicon 与 Intel Mac；工具安装支持以官方页面和你的 macOS 版本为准。代码共用上一级源文件，命令在“终端 Terminal”执行。若终端提示前面带 `$` 或 `%`，不要把提示符一起复制。

## 1. 安装工具

打开终端，执行 `xcode-select --install`，若系统提示已安装即可继续。随后按 [Homebrew 官网](https://brew.sh/) 的说明安装 Homebrew，并执行安装完成时提示的 Next steps。已有 Homebrew 可跳过。

```bash
brew --version
brew install python icarus-verilog scala-cli
python3 --version
iverilog -V
scala-cli version
```

Homebrew 的 Icarus 包名为 **icarus-verilog**，安装后命令名是 `iverilog` 和 `vvp`。Chisel 教学启动器指定 Java 21，Scala CLI 会按需下载，不要求另行安装整套 JDK。

如果安装后提示 `brew: command not found`，先重新打开终端。若仍找不到，根据电脑架构执行对应的当前终端配置：

```bash
# Apple Silicon，Homebrew 默认在 /opt/homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"
```

```bash
# Intel，Homebrew 默认在 /usr/local
eval "$(/usr/local/bin/brew shellenv)"
```

两段选与你的安装路径相符的一段。`uname -m` 可查看当前终端架构，通常 arm64 表示 Apple Silicon，x86_64 表示 Intel 环境；Rosetta 终端可能显示 x86_64。首次安装请以安装器给出的 Next steps 为准。

## 2. 打开资料目录

先从 GitHub 获取仓库：当前仓库为私有，需要已获访问权限并完成 GitHub 身份验证；也可以在登录后的网页选择 Code → Download ZIP，解压后继续。已有文件可跳过下载。

```bash
git clone https://github.com/RYZ050406/Graduation-Project.git
cd 'Graduation-Project/学习资料/配套示例'
```

若放在“下载”文件夹且目录名就是 Graduation-Project，可用：

```bash
cd "$HOME/Downloads/Graduation-Project/学习资料/配套示例"
```

ZIP 解压后名称可能为 `Graduation-Project-main`，此时相应改名。也可输入 `cd `（末尾有空格），把 Finder 中的“配套示例”文件夹拖进终端，再按回车。`pwd` 查看当前目录，`ls` 列出文件。

## 3. 运行 Python 进程练习

```bash
bash macOS/run_examples.sh python
```

也可以逐个运行，便于对照第 03 册：

```bash
python3 process_demo.py
python3 pipe_demo.py
python3 terminate_demo.py
python3 policy_model.py
```

前三个观察创建与等待、管道、终止与回收；最后一个是逻辑策略模型。终止示例的退出码可能为 `-15`，表示在 POSIX 平台收到 SIGTERM；不要要求与 Windows 数字相同。

## 4. 运行 RTL 仿真

```bash
bash macOS/run_examples.sh rtl
```

应看到选择器、计数器、手写停止门和已有 Chisel 生成模块的 PASS。手工运行单个例子时可用：

```bash
iverilog -g2012 -s counter4_tb -o counter4.vvp counter4.sv counter4_tb.sv
vvp counter4.vvp
```

启动器运行产生的波形在 `.outputs/counter4.vcd`，手工命令运行则在当前目录。波形查看器是选用工具，读文本与逐拍表即可完成必学任务，不要求安装 GTKWave。

## 5. 运行 Chisel

```bash
bash macOS/run_examples.sh chisel
```

等价的直接命令：

```bash
scala-cli run chisel_project.scala SafetyGate.scala \
  --main-class EmitSafetyGate --server=false --jvm 21
```

首次运行会下载固定依赖与后端，输出包含 `module SafetyGate` 等 RTL。部分版本一次打印多个文件片段；不要把整屏输出随意当作单个可编译文件。已有生成主模块可先用于 `rtl` 练习。

若 Maven 下载失败，先保留完整报错，确认网络能访问仓库；若确实需要指定中央仓库，可只对这次运行设置：

```bash
COURSIER_REPOSITORIES=https://repo.maven.apache.org/maven2 \
  bash macOS/run_examples.sh chisel
```

若遇到架构或 `firtool` 报错，先检查 `uname -m`、`command -v brew` 和工具版本，按 [Chisel 安装页](https://www.chisel-lang.org/docs/installation) 核对支持；不要一边运行 Intel 终端、一边混用 arm64 工具。

若卡在下载 JDK 索引，而且电脑已经安装 Java 21，可用 `/usr/libexec/java_home -v 21` 查询路径，再把实际路径填入：

```bash
bash macOS/run_examples.sh chisel --java-home '/你的/Java21/Home'
```

这会使用已有 JDK，跳过自动选择和下载 JDK；Chisel 库及生成后端首次使用仍需下载。

## 6. macOS 与 Linux 的区别

macOS 可学习进程、父子关系、等待、信号与 IPC，并运行本套 Python 例子。`/proc/self/cgroup`、Linux namespace、cgroup 和 seccomp 是第 03 册的 Linux 专项内容，不能在 Mac 原生终端原样执行。

macOS 可使用下面的只读命令观察当前 shell：

```bash
ps -o pid,ppid,state,comm -p $$
```

如果后续研究必须使用 Linux cgroup 等机制，再进入 Linux 虚拟机或导师提供的 Linux 机器。本周基础练习无需因此先装 Linux。

## 测试说明与官方参考

步骤按官方安装方式编写；本次未在实体 macOS 上运行。Windows / Ubuntu 的实际验证见上一级记录。

- [Homebrew 安装与路径](https://docs.brew.sh/Installation)
- [Homebrew Icarus Verilog](https://formulae.brew.sh/formula/icarus-verilog)
- [Scala CLI 安装](https://scala-cli.virtuslab.org/install/)
- [Chisel 安装](https://www.chisel-lang.org/docs/installation)
- [Python subprocess 的平台差异](https://docs.python.org/3/library/subprocess.html)
