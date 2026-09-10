# -*- coding: utf-8 -*-
"""สร้างข้อสอบปลายภาคหน่วยที่ 3 ฉบับ 5 นาที — ครอบคลุมเฉพาะ Mission 0 และ Mission 1

หน้า 1 คือกระดาษคำถามสำหรับแจกนักศึกษา หน้า 2 คือเฉลยและเกณฑ์สำหรับผู้สอน
พิมพ์แจกเฉพาะหน้า 1 เท่านั้น

รัน:  python3 worksheet/tools/build_final_exam.py
ตรวจจำนวนหน้า:  python3 worksheet/tools/check_pages.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from docx import Document
from docx.shared import Twips
from docxlib import (SZ, SZ_SMALL, cell_text, clear_body, grid, para, rich,
                     set_header, shade)

RED = "C00000"
BLUE = "1F4E79"
ACCENT = "DEEAF6"
GREY = "F2F2F2"
SZ_TINY = 26           # 13pt

SRC = str(HERE / 'template.docx')
OUT = str(HERE.parent / 'final-exam-3.1.docx')

MARGIN = 1000
WIDTH = 9900

doc = Document(SRC)
clear_body(doc)
set_header(doc, {"1/2568": "1/2569"})

sec = doc.sections[0]
for side in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
    setattr(sec, side, Twips(MARGIN))


def split_box(headers, src_lines, view_lines):
    """กล่องสองคอลัมน์ ซ้ายคือซอร์ส markdown ขวาคือผลการแสดงผล

    view_lines เป็น (ข้อความ, ตัวหนา) เพื่อให้ฝั่งขวาดูเหมือนหน้าที่ render แล้วจริง
    """
    t = grid(doc, 2, 2, [4750, WIDTH - 4750])
    for i, h in enumerate(headers):
        cell_text(t.rows[0].cells[i], h, bold=True, align="center", size=SZ_TINY)
        shade(t.rows[0].cells[i], ACCENT)

    src = t.rows[1].cells[0]
    shade(src, GREY)
    for i, line in enumerate(src_lines):
        cell_text(src, line, size=SZ_TINY, first=(i == 0))

    view = t.rows[1].cells[1]
    for i, (line, bold) in enumerate(view_lines):
        cell_text(view, line, bold=bold, size=SZ_TINY, first=(i == 0))
    return t


# ==========================================================================
# หน้า 1 · กระดาษคำถาม
# ==========================================================================
para(doc, "ข้อสอบปลายภาค · หน่วยที่ 3 พื้นฐานอินเทอร์เน็ตและบริการออนไลน์",
     bold=True, color=RED, align="center", after=0)
para(doc, "เวลา 5 นาที · 10 คะแนน · ห้ามเปิดเอกสารและอุปกรณ์ทุกชนิด",
     size=SZ_TINY, align="center", after=4)

info = grid(doc, 1, 6, [1150, 2600, 1150, 1750, 1000, WIDTH - 7650])
for i, label in enumerate(("ชื่อ-สกุล", "รหัสนักศึกษา", "กลุ่มเรียน")):
    cell_text(info.rows[0].cells[i * 2], label, bold=True, size=SZ_TINY)
    cell_text(info.rows[0].cells[i * 2 + 1], "")

para(doc, "สถานการณ์", bold=True, color=BLUE, size=SZ_SMALL, before=8, after=1)
para(doc, "อาเนียมี GitHub username ว่า  anya-forger  และกำลังจะ commit ไฟล์ "
          "README.md ขึ้นหน้า profile ของตนเอง",
     size=SZ_TINY, after=3)
split_box(
    ["ซอร์ส  README.md", "ผลการแสดงผลบนหน้า profile"],
    ['# อาเนีย ฟอร์เจอร์ · 6740xxxxxx',
     'รักการเขียนโปรแกรมและเทคโนโลยี ตั้งใจเรียนและพัฒนาตัวเอง',
     '',
     '## กำลังเรียนรู้',
     '- Python',
     '- HTML',
     '',
     '## ติดต่อ',
     'โทร **08x-xxx-xxxx** · หอพักช่อชงโค ห้อง 401',
     'เรียนจันทร์ 13:00 ห้อง 26-401 · พฤหัส 09:00 ห้อง 26-305',
     '',
     '<script> const KEY = "sk-live-8f2b91..." </script>'],
    [('อาเนีย ฟอร์เจอร์ · 6740xxxxxx', True),
     ('รักการเขียนโปรแกรมและเทคโนโลยี ตั้งใจเรียนและพัฒนาตัวเอง', False),
     ('', False),
     ('กำลังเรียนรู้', True),
     ('•  Python', False),
     ('•  HTML', False),
     ('', False),
     ('ติดต่อ', True),
     ('โทร 08x-xxx-xxxx · หอพักช่อชงโค ห้อง 401', False),
     ('เรียนจันทร์ 13:00 ห้อง 26-401 · พฤหัส 09:00 ห้อง 26-305', False),
     ('', False),
     ('(บรรทัดสุดท้ายไม่ปรากฏบนหน้านี้)', False)])

rich(doc, [("ข้อ 1  (3 คะแนน)  ", True, BLUE),
           ("ขีดเส้นใต้ 3 จุดใน", False),
           ("ฝั่งซอร์ส README.md", True),
           (" ที่ต้องแก้ก่อน commit", False)],
     size=SZ_SMALL, before=9, after=0)

rich(doc, [("ข้อ 2  (2 คะแนน)  ", True, BLUE),
           ("เลือกมา 1 จุดที่คิดว่าเสี่ยงที่สุด แล้วเขียนเหตุผล 1 ประโยค", False)],
     size=SZ_SMALL, before=8, after=3)
para(doc, "_" * 92, size=SZ_SMALL, after=0)

rich(doc, [("ข้อ 3  (3 คะแนน)  ", True, BLUE),
           ("นอกจากหน้า profile ข้างบน อาเนียยังมี", False),
           ("เว็บไซต์ส่วนตัว", True),
           (" ที่ทำด้วย GitHub Pages", False),
           (" และต้องการให้เปิดได้ที่ URL ระดับบนสุด ", False),
           ("คือไม่มีชื่อ repository ต่อท้าย", True),
           ("  จงเติม", False)],
     size=SZ_SMALL, before=9, after=3)
q3 = grid(doc, 3, 2, [4600, WIDTH - 4600])
for i, (label, prefix) in enumerate([
        ("ก. ต้องตั้งชื่อ repository ว่า", ""),
        ("ข. URL เว็บไซต์ที่ได้คือ", "https://"),
        ("ค. URL หน้า profile ของอาเนียคือ", "https://")]):
    cell_text(q3.rows[i].cells[0], label, size=SZ_TINY)
    cell_text(q3.rows[i].cells[1], prefix, size=SZ_TINY)

rich(doc, [("ข้อ 4  (2 คะแนน)  ", True, BLUE),
           ("เขียนบรรทัดแนะนำตัว (tagline) ใหม่ให้อาเนีย 1 บรรทัด สมมติข้อมูลได้",
            False)],
     size=SZ_SMALL, before=9, after=3)
para(doc, "_" * 92, size=SZ_SMALL, after=0)

# ==========================================================================
# หน้า 2 · เฉลยและเกณฑ์ สำหรับผู้สอน
# ==========================================================================
head2 = para(doc, "เฉลยและเกณฑ์การให้คะแนน — สำหรับผู้สอน ห้ามพิมพ์แจกนักศึกษา",
             bold=True, color=RED, size=SZ_SMALL, after=3)
head2.paragraph_format.page_break_before = True

key = grid(doc, 5, 3, [900, 6400, WIDTH - 7300])
for i, h in enumerate(("ข้อ", "เฉลยและเกณฑ์", "LLO")):
    cell_text(key.rows[0].cells[i], h, bold=True, align="center", size=SZ_TINY)
    shade(key.rows[0].cells[i], ACCENT)

ROWS = [
    ("1",
     ["จุดละ 1 คะแนน ตอบถูก 3 จุดใดก็ได้จาก 5 จุดที่ฝังไว้",
      "เบอร์โทรศัพท์ · ที่อยู่หอพักพร้อมเลขห้อง · ตารางเรียนที่ระบุห้องและเวลา",
      "API key ในโค้ด · ชื่อเต็มคู่กับรหัสนักศึกษา",
      "จุดสอน : GitHub ตัด <script> ทิ้งตอน render จึงไม่โผล่ฝั่งขวา แต่ทุกคนกดดูซอร์สได้",
      "นักศึกษาที่คิดว่าไม่แสดงผลแล้วปลอดภัย คือกลุ่มที่ต้องอธิบายเพิ่มตอนเฉลย"],
     "LLO5"),
    ("2",
     ["2 = ระบุผลลัพธ์ของความเสี่ยง เช่น ตามตัวได้ บัญชีถูกใช้แทน หรือผิด PDPA",
      "1 = บอกเพียงว่าไม่ควรใส่ โดยไม่ระบุผลที่ตามมา"],
     "LLO5"),
    ("3",
     ["ก. anya-forger.github.io   ข. anya-forger.github.io   ค. github.com/anya-forger",
      "ข้อละ 1 คะแนน · ข้อ ก. ผิดถ้าสะกดไม่ตรง username ทุกตัวอักษร รวมขีดกลาง",
      "ตอบแบบ project page คือชื่อ repo อื่นแล้ว URL มีชื่อ repo ต่อท้าย ได้ 0 ในข้อ ก. และ ข.",
      "เพราะขัดเงื่อนไขในโจทย์ แต่ควรอธิบายความต่างของ user site กับ project page ตอนเฉลย",
      "ตอบ anya-forger เฉย ๆ คือสับสนกับ repo ของหน้า profile ในสถานการณ์ ให้ 0 และอธิบายเพิ่ม"],
     "LLO2"),
    ("4",
     ["2 = เจาะจงจนนึกภาพออก มีสิ่งของ ปัญหา หรือเป้าหมายที่จับต้องได้",
      "1 = เจาะจงขึ้นแต่ยังกว้าง · 0 = คำกว้าง เช่น สนใจ IoT และ AI",
      "ตัวอย่างที่ได้เต็ม : อยากทำเว็บที่เปิดจากมือถือแล้วโหลดไม่ถึงสองวินาที"],
     "LLO4"),
]
for i, (no, lines, llo) in enumerate(ROWS, 1):
    cell_text(key.rows[i].cells[0], no, align="center", size=SZ_TINY)
    for j, line in enumerate(lines):
        cell_text(key.rows[i].cells[1], line, size=SZ_TINY, first=(j == 0))
    cell_text(key.rows[i].cells[2], llo, align="center", size=SZ_TINY)

para(doc, "การจัดสรรเวลาและน้ำหนัก", bold=True, color=BLUE, size=SZ_SMALL,
     before=9, after=2)
T2 = grid(doc, 1, 1, [WIDTH])
cell = T2.rows[0].cells[0]
for j, line in enumerate([
        "เวลา  อ่านสถานการณ์ 45 วิ · ข้อ 1 45 วิ · ข้อ 2 55 วิ · ข้อ 3 40 วิ · "
        "ข้อ 4 60 วิ  รวม 4 นาที 5 วินาที",
        "สัดส่วน  LLO5 = 5 คะแนน · LLO2 = 3 คะแนน · LLO4 = 2 คะแนน · จุดตัดผ่าน 6 จาก 10",
        "ข้อสอบ 5 นาทีมีค่าความเที่ยงต่ำโดยธรรมชาติ ไม่ควรให้น้ำหนักเกิน 10% ของเกรด",
        "หลักฐานหลักของหน่วยนี้คือ URL เว็บไซต์จริงและใบงานหน้า 1 ที่ลงชื่อแล้ว",
        "ไม่ออกข้อสอบ LLO1 และ LLO3 เพราะ Mission 2 และ Mission 3 ยังไม่ได้สอน",
]):
    cell_text(cell, line, size=SZ_TINY, first=(j == 0))

doc.save(OUT)
print("เขียนไฟล์แล้ว:", OUT)
