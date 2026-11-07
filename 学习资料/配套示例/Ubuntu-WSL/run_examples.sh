#!/bin/bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'python3 was not found. Read Ubuntu-WSL/README.md first.' >&2
  exit 1
fi
if [ "$#" -eq 0 ]; then set -- python; fi
exec python3 "$script_dir/../run_examples.py" "$@"
