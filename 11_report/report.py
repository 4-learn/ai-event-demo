import json
import os
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).parent
NAVY = colors.HexColor("#101722")
TEAL = colors.HexColor("#008777")
GRAY = colors.HexColor("#526174")
LIGHT = colors.HexColor("#F0F5F6")


def _register_font():
    candidates = [os.getenv("REPORT_FONT", ""), "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"]
    for filename in candidates:
        if filename and Path(filename).is_file():
            pdfmetrics.registerFont(TTFont("ReportCJK", filename))
            return
    raise RuntimeError("找不到中文字型，請安裝 fonts-wqy-zenhei 或設定 REPORT_FONT")


def save_report(report, output_path=None):
    _register_font()
    output_path = Path(output_path) if output_path else ROOT / "output" / "weekly_report.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stats = report["statistics"]
    evidence = {rule["id"]: rule for rule in report["evidence"]}
    page = canvas.Canvas(str(output_path), pagesize=A4)
    page.setTitle("通道占用七天回顧 - 教學模擬")
    width, height = A4

    def text(value, x, top, font_size=11, color=NAVY):
        page.setFillColor(color)
        page.setFont("ReportCJK", font_size)
        page.drawString(x, top, str(value))

    def paragraph(value, x, top, available_width, max_height, size=10.5, color=NAVY):
        style = ParagraphStyle("body", fontName="ReportCJK", fontSize=size, leading=size * 1.5, textColor=color, wordWrap="CJK")
        item = Paragraph(escape(value), style)
        _, item_height = item.wrap(available_width, max_height)
        if item_height > max_height:
            raise ValueError("報告文字超出一頁版面，請縮短內容後再輸出")
        item.drawOn(page, x, top - item_height)

    page.setFillColor(NAVY)
    page.rect(0, height - 112, width, 112, fill=1, stroke=0)
    text("通道占用｜七天回顧", 36, height - 43, 24, colors.white)
    text(f"{stats['period_start']} - {stats['period_end']}  |  台北時區", 36, height - 70, 10, colors.white)
    text("教學模擬資料 · 非真實工廠紀錄", 36, height - 93, 10, colors.HexColor("#75E2CF"))

    kpis = [(stats["event_count"], "占用事件"), (f"{stats['total_seconds'] / 60:.1f} 分鐘", "總占用時間"), (len(stats["zones"]), "觀測區域")]
    for index, (value, label) in enumerate(kpis):
        x = 36 + index * 178
        page.setFillColor(LIGHT)
        page.roundRect(x, 635, 167, 70, 8, fill=1, stroke=0)
        text(value, x + 12, 669, 22, TEAL)
        text(label, x + 12, 648, 10, GRAY)

    text("區域比較", 36, 609, 14)
    columns = [36, 203, 308, 442]
    for x, label in zip(columns, ["區域", "事件次數", "總占用（分鐘）", "最長單次（秒）"]):
        text(label, x, 581, 10, GRAY)
    zones = sorted(stats["zones"].items(), key=lambda item: item[1]["event_count"], reverse=True)
    if len(zones) > 2:
        raise ValueError("本版一頁模板只示範兩個區域")
    for index, (zone, values) in enumerate(zones):
        y = 552 - index * 28
        page.setStrokeColor(colors.HexColor("#DAE1E5"))
        page.line(36, y - 10, width - 36, y - 10)
        cells = [zone, values["event_count"], f"{values['total_seconds'] / 60:.1f}", f"{values['longest_seconds']:.0f}"]
        for x, value in zip(columns, cells):
            text(value, x, y, 11)

    text("回顧觀察", 36, 488, 14)
    paragraph(report["summary"], 36, 470, width - 72, 58)
    text("建議行動 · 供主管確認", 36, 393, 14)

    if len(report["recommendations"]) != 2:
        raise ValueError("本版報告需要兩項建議")
    cited = {}
    for index, item in enumerate(report["recommendations"]):
        rule = evidence[item["rule_id"]]
        if item["quote"] not in rule["text"] or not item["quote"].strip():
            raise ValueError("報告引用原文不符")
        top = 370 - index * 85
        text(f"{index + 1:02d}  {item['zone']}  |  {rule['section']}", 36, top, 10, TEAL)
        paragraph(item["action"], 36, top - 12, width - 72, 58)
        cited[rule["id"]] = rule

    text("規範來源 · 教學模擬辦法", 36, 190, 12)
    for index, rule in enumerate(cited.values()):
        y = 171 - index * 36
        text(rule["section"], 36, y, 9, GRAY)
        text(rule["source"], 36, y - 13, 8, TEAL)
        page.linkURL(rule["source"], (36, y - 16, width - 36, y - 4), relative=0, thickness=0)

    generated_at = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M")
    text(f"資料：{stats['dataset']}  |  產出：{generated_at}", 36, 72, 8, GRAY)
    paragraph("數字由 Python 計算，文字由 LLM 整理並經引用檢查。事件紀錄不能證明根本原因或責任；建議仍需現場確認。本報告不是正式法規或工安稽核結論。", 36, 57, width - 72, 32, 8, GRAY)
    page.showPage()
    page.save()
    output_path.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path.resolve()
