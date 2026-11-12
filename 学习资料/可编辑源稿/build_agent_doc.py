"""Build the standalone beginner's Agent booklet with the shared study styles."""
from pathlib import Path

from pypdf import PdfReader

from build_pdfs import StudyDoc, parse, MARGIN, PAGE_H, PAGE_W, TEAL, GRAY


class AgentDoc(StudyDoc):
    def __init__(self, target):
        super().__init__(target, "Agent 的组成与工作原理")
        self.author = "毕设学习资料 | 2026-11-12"
        self.subject = "零基础理解 Agent、模型、工具、进程与安全控制"

    def decorate(self, c, doc):
        c.saveState()
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.2)
        c.line(MARGIN, PAGE_H - 39, PAGE_W - MARGIN, PAGE_H - 39)
        c.setFont("CNBold", 8.5)
        c.setFillColor(GRAY)
        c.drawString(MARGIN, PAGE_H - 29, "毕设补充学习资料 / Agent 的组成与工作原理")
        c.setFont("CN", 8.3)
        c.drawString(MARGIN, 27, "从组成到执行，再联系进程与硬件保护 | 2026-11-12")
        c.drawRightString(PAGE_W - MARGIN, 27, f"第 {doc.page} 页")
        c.restoreState()


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / "Agent的组成与工作原理.md"
    target = source.with_suffix(".pdf")
    markdown = source.read_text(encoding="utf-8")
    AgentDoc(target).build(parse(markdown))
    planned = markdown.count("<!-- PAGE -->") + 1
    reader = PdfReader(target)
    print(f"Agent booklet: {len(reader.pages)} pages; planned {planned}; {target}")
    if len(reader.pages) != planned:
        for index, page in enumerate(reader.pages, 1):
            print(index, (page.extract_text() or "").splitlines()[:3])
        raise RuntimeError("Page count differs from the planned layout")


if __name__ == "__main__":
    main()
