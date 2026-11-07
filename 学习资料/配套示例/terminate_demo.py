"""Stop only the single child created by this script, then reap it."""
import subprocess
import sys


def main():
    child = subprocess.Popen(
        [sys.executable, "-u", "-c",
         "import time; print('ready',flush=True); time.sleep(10)"],
        stdout=subprocess.PIPE, text=True,
    )
    try:
        assert child.stdout.readline().strip() == "ready"
        child.terminate()
        try:
            result = child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill()
            result = child.wait(timeout=3)
        print("child ended; exit code =", result)
    finally:
        if child.poll() is None:
            child.kill()
            child.wait(timeout=3)
        child.stdout.close()


if __name__ == "__main__":
    main()
