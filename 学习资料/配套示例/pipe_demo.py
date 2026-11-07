"""One child sends a fixed string to its parent through a pipe."""
import subprocess
import sys


def main():
    result = subprocess.run(
        [sys.executable, "-c", "print('hello from child')"],
        capture_output=True, text=True, check=True, timeout=5,
    )
    print("parent received:", result.stdout.strip())
    assert result.stdout.strip() == "hello from child"


if __name__ == "__main__":
    main()
