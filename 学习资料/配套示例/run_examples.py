"""Shared launcher. Platform folders document installation and shell syntax."""
import argparse
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / ".outputs"


def tool(name):
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"Missing {name}. See the README in the folder for your OS.")
    return path


def run(args, cwd=ROOT, timeout=60):
    print("RUN:", subprocess.list2cmdline([str(x) for x in args]), flush=True)
    subprocess.run([str(x) for x in args], cwd=cwd, check=True, timeout=timeout)


def python_examples():
    for filename in ("process_demo.py", "pipe_demo.py", "terminate_demo.py", "policy_model.py"):
        run([sys.executable, ROOT / filename], timeout=20)
    print("PASS: all Python examples", flush=True)


def rtl_examples(selected=None):
    compiler, simulator = tool("iverilog"), tool("vvp")
    OUTPUT.mkdir(exist_ok=True)
    cases = (
        ("mux2", "mux2_tb", ("mux2.sv", "mux2_tb.sv")),
        ("counter4", "counter4_tb", ("counter4.sv", "counter4_tb.sv")),
        ("safety_gate", "safety_gate_tb", ("safety_gate.sv", "safety_gate_tb.sv")),
        ("chisel_gate", "safety_gate_tb", ("SafetyGate.generated.sv", "chisel_gate_adapter.sv", "safety_gate_tb.sv")),
        ("syntax_basics", "syntax_basics_tb", ("syntax_basics.sv", "syntax_basics_tb.sv")),
        ("syntax_chisel", "syntax_basics_tb", ("SyntaxBasics.generated.sv", "syntax_chisel_adapter.sv", "syntax_basics_tb.sv")),
    )
    for index, (name, top, files) in enumerate(cases, 1):
        if selected and selected != name:
            continue
        output = OUTPUT / f"case{index}.vvp"
        run([compiler, "-g2012", "-s", top, "-o", output,
             *(ROOT / filename for filename in files)], cwd=OUTPUT)
        run([simulator, output], cwd=OUTPUT)
    print(f"PASS: {selected or 'all RTL examples (including the supplied Chisel-generated module)'}", flush=True)


def chisel_example(java_home=None, selected=None):
    if java_home:
        java_home = Path(java_home).expanduser().resolve()
        executable = "java.exe" if sys.platform == "win32" else "java"
        if not (java_home / "bin" / executable).is_file():
            raise RuntimeError(f"No Java executable under {java_home / 'bin'}")
        java_args = ["--java-home", str(java_home)]
    else:
        java_args = ["--jvm", "21"]
    source, entry = (("SyntaxBasics.scala", "EmitSyntaxBasics") if selected == "syntax_basics"
                     else ("SafetyGate.scala", "EmitSafetyGate"))
    run([tool("scala-cli"), "run", "chisel_project.scala", source,
         "--main-class", entry, "--server=false", *java_args], timeout=900)
    print("PASS: Chisel generation completed; inspect the printed RTL", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=("python", "rtl", "chisel"),
                        nargs="?", default="python")
    parser.add_argument("--java-home", help="Optional existing Java 21 JDK for the chisel group")
    parser.add_argument("--example", choices=("mux2", "counter4", "safety_gate", "chisel_gate",
                                             "syntax_basics", "syntax_chisel"),
                        help="Select an RTL example, or syntax_basics for the chisel group")
    args = parser.parse_args()
    print(f"Platform: {platform.system()} {platform.machine()}; Python: {sys.version.split()[0]}",
          flush=True)
    try:
        if args.java_home and args.group != "chisel":
            raise RuntimeError("--java-home is only used with the chisel group")
        if args.example and not (args.group == "rtl" or
                                 (args.group == "chisel" and args.example == "syntax_basics")):
            raise RuntimeError("--example requires rtl, or chisel --example syntax_basics")
        if args.group == "chisel":
            chisel_example(args.java_home, args.example)
        elif args.group == "rtl":
            rtl_examples(args.example)
        else:
            python_examples()
    except (RuntimeError, subprocess.SubprocessError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
