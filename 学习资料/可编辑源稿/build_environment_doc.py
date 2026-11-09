"""Build the standalone description of this machine without changing the course PDFs."""
from pathlib import Path

from pypdf import PdfReader

from build_pdfs import StudyDoc, parse, MARGIN, PAGE_H, PAGE_W, TEAL, GRAY


class EnvironmentDoc(StudyDoc):
    def decorate(self, c, doc):
        c.saveState()
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.2)
        c.line(MARGIN, PAGE_H - 39, PAGE_W - MARGIN, PAGE_H - 39)
        c.setFont("CNBold", 8.5)
        c.setFillColor(GRAY)
        c.drawString(MARGIN, PAGE_H - 29, "毕设开发环境 / Windows + WSL2 + VS Code")
        c.setFont("CN", 8.3)
        c.drawString(MARGIN, 27, "本机核对日期：2026-11-09")
        c.drawRightString(PAGE_W - MARGIN, 27, f"第 {doc.page} 页")
        c.restoreState()


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / "当前开发环境说明.md"
    target = root / "当前开发环境说明.pdf"
    markdown = source.read_text(encoding="utf-8")
    doc = EnvironmentDoc(target, "当前开发环境说明")
    doc.build(parse(markdown))
    planned = markdown.count("<!-- PAGE -->") + 1
    pages = len(PdfReader(target).pages)
    print(f"Environment document: {pages} pages; planned {planned}; {target}")
    if pages != planned:
        raise RuntimeError("Page count differs from the planned layout")


if __name__ == "__main__":
    main()
