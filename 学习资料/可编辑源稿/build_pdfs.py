"""Render the five Chinese study booklets with embedded fonts and bookmarks."""
from pathlib import Path
import argparse
import html
import json
import re

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Flowable, KeepTogether,
)
from pypdf import PdfReader, PdfWriter
import reportlab.lib.textsplit as textsplit
import reportlab.platypus.paragraph as paragraph_module


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent
TEMP = ROOT.parent / "tmp" / "pdfs"
TEMP.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("CN", str(FONT_DIR / "simsun.ttc"), subfontIndex=0))
pdfmetrics.registerFont(TTFont("CNBold", str(FONT_DIR / "simhei.ttf")))
pdfmetrics.registerFont(TTFont("Mono", str(FONT_DIR / "consola.ttf")))
pdfmetrics.registerFontFamily("CN", normal="CN", bold="CNBold", italic="CN", boldItalic="CNBold")

NAVY = colors.HexColor("#15334B")
TEAL = colors.HexColor("#137D85")
INK = colors.HexColor("#26394A")
GRAY = colors.HexColor("#657789")
LIGHT = colors.HexColor("#F1F6F8")
GOLD = colors.HexColor("#E1A949")
PAGE_W, PAGE_H = A4
MARGIN = 48
BODY_W = PAGE_W - 2 * MARGIN

# Reserve a little room for Chinese punctuation hanging at the line end.
for module in (textsplit, paragraph_module):
    module.ALL_CANNOT_START += "，。！？；：、）】》”’"

STYLES = {
    "title": ParagraphStyle("title", fontName="CNBold", fontSize=21,
        leading=29, textColor=NAVY, spaceAfter=15, wordWrap="CJK",
        keepWithNext=True),
    "h2": ParagraphStyle("h2", fontName="CNBold", fontSize=12.4,
        leading=19, textColor=TEAL, spaceBefore=10, spaceAfter=7,
        wordWrap="CJK", keepWithNext=True),
    "body": ParagraphStyle("body", fontName="CN", fontSize=10.8,
        leading=17.8, textColor=INK, spaceAfter=8, wordWrap="CJK", rightIndent=11),
    "bullet": ParagraphStyle("bullet", fontName="CN", fontSize=10.7,
        leading=17.4, textColor=INK, spaceAfter=6, leftIndent=11,
        firstLineIndent=-9, wordWrap="CJK"),
    "quote": ParagraphStyle("quote", fontName="CN", fontSize=10.2,
        leading=17, textColor=NAVY, backColor=LIGHT, borderColor=TEAL,
        borderWidth=0.7, borderPadding=9, spaceBefore=6, spaceAfter=12,
        wordWrap="CJK"),
    "cell": ParagraphStyle("cell", fontName="CN", fontSize=9.5,
        leading=15, textColor=INK, wordWrap="CJK"),
    "headcell": ParagraphStyle("headcell", fontName="CNBold", fontSize=9.5,
        leading=15, textColor=colors.white, wordWrap="CJK"),
    "ref": ParagraphStyle("ref", fontName="CN", fontSize=9.2,
        leading=15, textColor=GRAY, spaceAfter=7, wordWrap="CJK"),
}


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r'<font color="#17666F">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"https?://[^\s<]+", lambda m:
        '<link href="' + m.group(0) + '" color="#137D85">' + m.group(0) + '</link>', text)
    return text


class CodeBlock(Flowable):
    def __init__(self, code, label):
        Flowable.__init__(self)
        self.lines = code.rstrip("\n").splitlines() or [""]
        self.label = label or "text"
        self.font_size = 8.6
        self.line_height = 12.5
        self.height = 32 + self.line_height * len(self.lines)
        self.width = BODY_W
        self.spaceBefore = 4
        self.spaceAfter = 11

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        longest = max((sum(pdfmetrics.stringWidth(ch, "CN" if ord(ch) > 127 else "Mono",
            self.font_size) for ch in line) for line in self.lines), default=0)
        if longest > availWidth - 25:
            self.font_size *= (availWidth - 25) / longest
            if self.font_size < 6.8:
                raise ValueError(f"Code line too long: {longest}: {self.lines}")
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(LIGHT)
        c.roundRect(0, 0, self.width, self.height, 5, stroke=0, fill=1)
        c.setFillColor(TEAL)
        c.setFont("Mono", 7.2)
        c.drawString(11, self.height - 13, self.label.upper())
        y = self.height - 29
        for line in self.lines:
            x = 11
            for ch in line:
                font = "CN" if ord(ch) > 127 else "Mono"
                c.setFont(font, self.font_size)
                c.setFillColor(INK)
                c.drawString(x, y, ch)
                x += pdfmetrics.stringWidth(ch, font, self.font_size)
            y -= self.line_height


class ConceptFigure(Flowable):
    """Small native vector figures for the first encounters with system concepts."""
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.width = BODY_W
        self.height = 184 if kind == "tools" else 155
        self.spaceBefore = 5
        self.spaceAfter = 12

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def arrow(self, x1, y1, x2, y2, label=""):
        import math
        c = self.canv
        c.setStrokeColor(TEAL)
        c.setFillColor(TEAL)
        c.setLineWidth(1.1)
        c.line(x1, y1, x2, y2)
        angle = math.atan2(y2 - y1, x2 - x1)
        p = c.beginPath()
        p.moveTo(x2, y2)
        p.lineTo(x2 - 6 * math.cos(angle - .45), y2 - 6 * math.sin(angle - .45))
        p.lineTo(x2 - 6 * math.cos(angle + .45), y2 - 6 * math.sin(angle + .45))
        p.close()
        c.drawPath(p, stroke=0, fill=1)
        if label:
            c.setFont("CN", 8.4)
            c.setFillColor(GRAY)
            c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 6, label)

    def box(self, x, y, w, text, dark=False, h=31):
        c = self.canv
        c.setFillColor(NAVY if dark else colors.HexColor("#E6F0F3"))
        c.roundRect(x, y, w, h, 4, stroke=0, fill=1)
        c.setFillColor(colors.white if dark else INK)
        c.setFont("CNBold", 10)
        c.drawCentredString(x + w / 2, y + h / 2 - 3.3, text)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(LIGHT)
        c.roundRect(0, 0, self.width, self.height, 5, stroke=0, fill=1)
        if self.kind == "tools":
            self.box(124, 140, 250, "Chisel / Scala：构造电路", True)
            self.arrow(249, 140, 249, 119)
            self.box(124, 88, 250, "Verilog / SystemVerilog RTL")
            self.arrow(185, 88, 124, 60)
            self.arrow(313, 88, 374, 60)
            self.box(17, 21, 216, "仿真器 + 测试：检查行为")
            self.box(266, 21, 216, "综合与实现：配置 FPGA")
        else:
            self.box(10, 98, 58, "创建")
            self.box(111, 98, 63, "就绪")
            self.box(239, 98, 63, "运行", True)
            self.box(367, 98, 120, "退出、待回收")
            self.box(239, 15, 63, "阻塞")
            self.arrow(68, 113, 111, 113)
            self.arrow(174, 113, 239, 113, "调度")
            self.arrow(302, 113, 367, 113, "退出")
            self.arrow(270, 98, 270, 46)
            c.setFillColor(GRAY)
            c.setFont("CN", 8.4)
            c.drawString(278, 70, "等待事件")
            c.setStrokeColor(TEAL)
            c.line(239, 30, 142, 30)
            self.arrow(142, 30, 142, 98)
            c.setFillColor(GRAY)
            c.drawString(157, 40, "事件完成")
            c.setStrokeColor(TEAL)
            c.line(270, 129, 270, 143)
            c.line(270, 143, 142, 143)
            self.arrow(142, 143, 142, 129)
            c.setFont("CN", 8.4)
            c.setFillColor(GRAY)
            c.drawCentredString(206, 146, "被抢占，返回就绪")
        c.restoreState()


def table_rows(lines):
    rows = []
    for line in lines:
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r"[:\- ]+", x or "-") for x in cells):
            continue
        rows.append(cells)
    ncol = len(rows[0])
    if any(len(row) != ncol for row in rows):
        raise ValueError(f"Bad table: {rows}")
    weights = {
        2: [0.29, 0.71], 3: [0.20, 0.39, 0.41],
        4: [0.25, 0.25, 0.25, 0.25],
    }.get(ncol, [1 / ncol] * ncol)
    if ncol == 3 and rows[0][0] in ("天数", "分册"):
        weights = [0.17, 0.51, 0.32]
    if ncol == 3 and rows[0][0] in ("部分", "现象", "术语", "字段"):
        weights = [0.22, 0.39, 0.39]
    if ncol == 3 and rows[0][0] == "名称":
        weights = [0.29, 0.32, 0.39]
    data = [[Paragraph(inline(cell), STYLES["headcell" if r == 0 else "cell"])
             for cell in row] for r, row in enumerate(rows)]
    table = Table(data, colWidths=[BODY_W * x for x in weights],
                  repeatRows=1, hAlign="LEFT", spaceBefore=5, spaceAfter=12)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, TEAL),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#D9E4EA")),
    ]))
    return table


class StudyDoc(BaseDocTemplate):
    def __init__(self, path, unit):
        BaseDocTemplate.__init__(self, str(path), pagesize=A4,
            leftMargin=MARGIN, rightMargin=MARGIN, topMargin=61,
            bottomMargin=47, title=unit, author="学习资料 | 2026-11-07",
            subject="RTL、Chisel、操作系统进程与 Agent 安全目标入门")
        self.unit = unit
        self.headings = []
        frame = Frame(MARGIN, 47, BODY_W, PAGE_H - 108,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="main", frames=frame, onPage=self.decorate))

    def decorate(self, c, doc):
        c.saveState()
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.2)
        c.line(MARGIN, PAGE_H - 39, PAGE_W - MARGIN, PAGE_H - 39)
        c.setFont("CNBold", 8.5)
        c.setFillColor(GRAY)
        c.drawString(MARGIN, PAGE_H - 29, "五天基础学习资料 / " + self.unit)
        c.setFont("CN", 8.3)
        c.drawString(MARGIN, 27, "必学先行 · 示例驱动 · 先预测再验证")
        c.drawRightString(PAGE_W - MARGIN, 27, f"第 {doc.page} 页")
        c.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, "bookmark_title"):
            title = flowable.bookmark_title
            key = "heading_" + str(len(self.headings))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=0, closed=False)
            self.headings.append({"title": title, "page": self.page})


def parse(markdown):
    story = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == "<!-- PAGE -->":
            story.append(PageBreak())
            i += 1
            continue
        if line.startswith("```"):
            label = line[3:]
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            code = "\n".join(block)
            if code.startswith("Scala / Chisel 源代码"):
                story.append(ConceptFigure("tools"))
            elif code.startswith("创建 --> 就绪"):
                story.append(ConceptFigure("process"))
            else:
                story.append(CodeBlock(code, label))
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            story.append(table_rows(block))
            continue
        if line.startswith("# "):
            p = Paragraph(inline(line[2:]), STYLES["title"])
            p.bookmark_title = line[2:]
            story.append(p)
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), STYLES["h2"]))
            i += 1
            continue
        if line.startswith("> "):
            story.append(Paragraph(inline(line[2:]), STYLES["quote"]))
            i += 1
            continue
        if line.startswith("- ") or re.match(r"^\d+\. ", line):
            content = "• " + line[2:] if line.startswith("- ") else line
            story.append(Paragraph(inline(content), STYLES["bullet"]))
            i += 1
            continue
        block = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(
                ("#", "```", "|", "> ", "- ", "<!--")):
            block.append(lines[i].strip())
            i += 1
        text = " ".join(block)
        style = "ref" if re.match(r"^\[[A-Z]\d+\]", text) else "body"
        story.append(Paragraph(inline(text), STYLES[style]))
    return story


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--combined-output", default="五天基础学习资料_合订本_含语法补充.pdf",
                        help="Combined PDF filename; use another name if a viewer locks the previous file")
    args = parser.parse_args()
    if Path(args.combined_output).name != args.combined_output or not args.combined_output.endswith(".pdf"):
        parser.error("--combined-output must be a PDF filename, not a path")
    manifest = []
    for source in sorted(SOURCE.glob("[0-9][0-9]_*.md")):
        markdown = source.read_text(encoding="utf-8")
        unit = markdown.splitlines()[0].lstrip("# ")
        output = ROOT / (source.stem + ".pdf")
        doc = StudyDoc(output, unit)
        doc.build(parse(markdown))
        count = len(PdfReader(output).pages)
        expected = markdown.count("<!-- PAGE -->") + 1
        manifest.append({"file": output.name, "pages": count,
                         "expected_pages": expected, "headings": doc.headings})
        print(f"{output.name}: {count} pages (planned {expected})")
    merged = PdfWriter()
    for item in manifest:
        merged.append(str(ROOT / item["file"]), outline_item=item["file"][:-4],
                      import_outline=True)
    merged.add_metadata({"/Title": "五天基础学习资料 | 合订本",
                         "/Author": "学习资料", "/Subject": "零基础 · RTL / Chisel / 进程 / 技术目标"})
    merged_path = ROOT / args.combined_output
    with merged_path.open("wb") as stream:
        merged.write(stream)
    manifest.append({"file": merged_path.name, "pages": len(PdfReader(merged_path).pages)})
    (TEMP / "pdf_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
    print(f"{merged_path.name}: {manifest[-1]['pages']} pages")


if __name__ == "__main__":
    main()
