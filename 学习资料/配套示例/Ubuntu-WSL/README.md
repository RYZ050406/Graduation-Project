# Ubuntu / WSL Ubuntu：运行说明

命令在 Ubuntu 终端执行。Windows 用户先进入 WSL Ubuntu；macOS 用户只有需要 Linux 特定机制时才需要 Linux 虚拟机或远程 Linux 主机。

## 1. 安装 Python 和 Icarus

```bash
sudo apt update
sudo apt install python3 iverilog
python3 --version
iverilog -V
```

WSL 中可以按作者的 D 盘路径定位；自己的路径不同请替换：

```bash
cd '/mnt/d/Projects/毕设/学习资料/配套示例'
```

原生 Ubuntu 如果克隆在主目录：

```bash
cd "$HOME/Graduation-Project/学习资料/配套示例"
```

## 2. 运行 Python 与 RTL

```bash
bash Ubuntu-WSL/run_examples.sh python
bash Ubuntu-WSL/run_examples.sh rtl
```

也可单独执行 `python3 process_demo.py` 等文件。RTL 输出写入 `.outputs/`，包括计数器的 VCD 波形。

## 3. 安装并运行 Chisel

按 [Scala CLI 官方安装页](https://scala-cli.virtuslab.org/install/) 的 Linux 步骤安装。已有 Scala CLI 可跳过。官方快速安装命令是：

```bash
curl -sSLf https://scala-cli.virtuslab.org/get | sh
```

执行安装器提示的 PATH 配置并重新打开终端，然后回到示例目录：

```bash
scala-cli version
bash Ubuntu-WSL/run_examples.sh chisel
```

启动器使用 `--jvm 21` 管理教学 JDK。首次下载依赖需要网络；若需要指定 Maven Central，可针对单次运行：

```bash
COURSIER_REPOSITORIES=https://repo.maven.apache.org/maven2 \
  bash Ubuntu-WSL/run_examples.sh chisel
```

若已经有 Java 21，可用 `readlink -f "$(command -v java)"` 定位可执行文件，取 `bin/java` 前面的 JDK 目录。例如：

```bash
bash Ubuntu-WSL/run_examples.sh chisel \
  --java-home /usr/lib/jvm/java-21-openjdk-amd64
```

路径按实际安装修改。这会跳过自动选择与下载 JDK，但库及后端首次使用仍需联网。

## 4. 只读观察 Linux 进程

```bash
ps -o pid,ppid,stat,comm -p $$
cat /proc/self/cgroup
```

第一行查看当前 shell；第二行查看执行 cat 的任务所属 cgroup。不同内核和 WSL 配置输出不同。本周不要求改动 cgroup 或系统权限。

Python 的 terminate 在 POSIX 上发送 SIGTERM，示例可能输出 -15；这与 Windows 的退出码不同。系统调用与组管理细节按第 03 册继续学习。

## 5. 手工仿真单个模块

```bash
iverilog -g2012 -s counter4_tb -o counter4.vvp counter4.sv counter4_tb.sv
vvp counter4.vvp
```

不要把手写安全门与 Chisel 适配器一并编译，二者都声明了 `safety_gate` 模块。具体覆盖范围见上一级 [验证记录](../示例说明与验证记录.md)。
