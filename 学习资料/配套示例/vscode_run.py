"""Actions used by the VS Code task menu. Run inside Ubuntu / WSL."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

import run_examples as examples


def installed_java21():
    candidates = []
    if os.environ.get("JAVA_HOME"):
        candidates.append(Path(os.environ["JAVA_HOME"]))
    executable = shutil.which("java")
    if executable:
        candidates.append(Path(executable).resolve().parent.parent)
    for home in candidates:
        result = subprocess.run([str(home / "bin" / "java"), "-version"],
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and re.search(r'version "21(?:\.|\")', result.stderr + result.stdout):
            return str(home)
    return None


def waveform():
    wave = examples.OUTPUT / "counter4.vcd"
    if not wave.exists():
        examples.rtl_examples("counter4")
    session = examples.OUTPUT / "counter4.gtkw"
    session.write_text(
        '[*] Counter4 study waveforms\n'
        '[dumpfile] "counter4.vcd"\n'
        '[timestart] 0\n[size] 1100 650\n[signals_width] 170\n'
        '@28\ncounter4_tb.clk\ncounter4_tb.reset\ncounter4_tb.enable\n'
        '@24\ncounter4_tb.count[3:0]\n', encoding="utf-8")
    zoom = examples.OUTPUT / "counter4_zoom.tcl"
    zoom.write_text('gtkwave::/Time/Zoom/Zoom_Full\n', encoding="ascii")
    log_path = examples.OUTPUT / "gtkwave.log"
    with log_path.open("a", encoding="utf-8") as log:
        process = subprocess.Popen([examples.tool("gtkwave"), wave.name, "--save", session.name,
                                    "--script", zoom.name], cwd=examples.OUTPUT,
            stdout=log, stderr=log, start_new_session=True,
            env={**os.environ, "GDK_BACKEND": "x11"})
    time.sleep(1)
    if process.poll() is not None:
        raise RuntimeError(f"GTKWave exited early; see {log_path}")
    (examples.OUTPUT / "gtkwave.pid").write_text(str(process.pid), encoding="ascii")
    print(f"GTKWave opened: PID={process.pid}; signals=clk, reset, enable, count", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("mux2", "counter4", "safety_gate", "rtl", "python",
                                            "chisel", "wave", "check", "syntax_basics",
                                            "syntax_chisel", "chisel_syntax"))
    action = parser.parse_args().action
    try:
        if action in ("mux2", "counter4", "safety_gate", "syntax_basics", "syntax_chisel"):
            examples.rtl_examples(action)
        elif action == "rtl":
            examples.rtl_examples()
        elif action == "python":
            examples.python_examples()
        elif action in ("chisel", "chisel_syntax"):
            os.environ.setdefault("COURSIER_REPOSITORIES", "https://repo.maven.apache.org/maven2")
            home = installed_java21()
            print(f"Java 21: {home or 'managed by Scala CLI'}", flush=True)
            examples.chisel_example(home, "syntax_basics" if action == "chisel_syntax" else None)
        elif action == "wave":
            waveform()
        else:
            for name, flag in (("python3", "--version"), ("iverilog", "-V"),
                               ("verilator", "--version"), ("gtkwave", "--version"),
                               ("scala-cli", "version")):
                result = subprocess.run([examples.tool(name), flag], capture_output=True,
                                        text=True, timeout=30, check=True)
                print(name + ": " + (result.stdout or result.stderr).splitlines()[0], flush=True)
            print("Java 21: " + str(installed_java21()), flush=True)
    except (RuntimeError, subprocess.SubprocessError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
