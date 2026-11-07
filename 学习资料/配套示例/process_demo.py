"""A finite parent/child lifecycle example; works on Windows and Linux."""
import os
import subprocess
import sys


def main():
    print(f"parent pid={os.getpid()}", flush=True)
    child_code = (
        "import os,time; "
        "print('child pid=',os.getpid(),'ppid=',os.getppid(),flush=True); "
        "time.sleep(0.3); print('child done',flush=True)"
    )
    child = subprocess.Popen([sys.executable, "-u", "-c", child_code])
    print(f"created child pid={child.pid}", flush=True)
    result = child.wait(timeout=5)
    print(f"wait returned, exit code={result}", flush=True)
    assert result == 0


if __name__ == "__main__":
    main()
