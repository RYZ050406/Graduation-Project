"""Re-run finite examples and inspect each PDF page's basic geometry."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys

import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "配套示例"
TEMP = ROOT.parent / "tmp" / "pdfs"
TEMP.mkdir(parents=True, exist_ok=True)


def check_python():
    results = {}
    for name in ("process_demo.py", "pipe_demo.py", "terminate_demo.py", "policy_model.py"):
        proc = subprocess.run([sys.executable, str(EXAMPLES / name)],
            capture_output=True, text=True, timeout=15, check=True)
        results[name] = proc.stdout.strip()
    return results


def check_pdfs():
    results = []
    for path in sorted(ROOT.glob("*.pdf")):
        reader = PdfReader(path)
        with pdfplumber.open(path) as pdf:
            for number, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                if len(text) < 40:
                    raise AssertionError(f"Nearly blank page: {path.name}/{number}")
                if "\ufffd" in text or "\u25a0" in text:
                    raise AssertionError(f"Replacement or square glyph: {path.name}/{number}")
                import re
                if any(re.match(r"^[，。！？；：、）】]", line)
                       for line in text.splitlines()):
                    raise AssertionError(f"Chinese punctuation at line start: {path.name}/{number}")
                chars = [c for c in page.chars if c.get("text", "").strip()]
                bad = [c for c in chars if c["x0"] < 43 or c["x1"] > page.width - 43
                       or c["top"] < 17 or c["bottom"] > page.height - 18]
                if bad:
                    raise AssertionError(f"Character outside margins: {path.name}/{number}: {bad[:3]}")
        results.append({"file": path.name, "pages": len(reader.pages),
                        "bytes": path.stat().st_size, "outlines": len(reader.outline)})
    expected_count = len(list(Path(__file__).resolve().parent.glob("[0-9][0-9]_*.md"))) + 1
    if len(results) != expected_count:
        raise AssertionError(f"Expected {expected_count} PDFs, got {len(results)}")
    return results


def main():
    report = {"python": check_python(), "pdfs": check_pdfs()}
    (TEMP / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
