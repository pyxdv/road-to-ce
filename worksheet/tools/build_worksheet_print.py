# -*- coding: utf-8 -*-
"""สร้างใบงานที่ 3.1 ฉบับพิมพ์แจก — เฉพาะส่วนที่นักศึกษาต้องเขียนด้วยลายมือ

เป้าหมายคือพิมพ์ลงกระดาษ A4 ได้พอดี 2 หน้า ทุกข้อความจึงถูกตัดให้สั้นพอที่จะอยู่ใน
บรรทัดเดียวต่อแถวตาราง คำอธิบายแบบยาวอยู่ในใบงานฉบับเต็มและใบความรู้แล้ว

รัน:  python3 worksheet/tools/build_worksheet_print.py
ตรวจจำนวนหน้า:  python3 worksheet/tools/check_pages.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from docx import Document
from docx.shared import Twips
from docxlib import (SZ, SZ_SMALL, blank_lines, cell_text, clear_body, grid,
                     para, rich, set_header, shade)

RED = "C00000"
BLUE = "1F4E79"
ACCENT = "DEEAF6"
SZ_TINY = 26           # 13pt สำหรับเนื้อในตาราง

SRC = str(HERE / 'template.docx')
OUT = str(HERE.parent / 'worksheet-3.1-print.docx')

MARGIN = 1000          # ~0.7 นิ้ว
WIDTH = 9900           # ความกว้างตาราง (twips)

doc = Document(SRC)
clear_body(doc)
set_header(doc, {"1/2568": "1/2569"})

sec = doc.sections[0]
for side in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
    setattr(sec, side, Twips(MARGIN))


def T(rows, headers, widths, size=SZ_TINY):
    t = grid(doc, len(rows) + 1, len(headers), widths)
    for i, h in enumerate(headers):
        cell_text(t.rows[0].cells[i], h, bold=True, align="center", size=SZ_TINY)
        shade(t.rows[0].cells[i], ACCENT)
    for i, row in enumerate(rows, 1):
        for j, val in enumerate(row):
            cell_text(t.rows[i].cells[j], val, size=size)
    return t


# ==========================================================================
# หน้า 1
# ==========================================================================
para(doc, "ใบงานที่ 3.1  ส่วนที่ต้องเขียนด้วยลายมือ", bold=True, color=RED,
     align="center", after=3)

info = grid(doc, 3, 4, [1500, 3450, 1600, WIDTH - 6550])
for r, (a, b) in enumerate([("ชื่อ-สกุล", "รหัสนักศึกษา"),
                            ("กลุ่มเรียน", "GitHub username")]):
    cell_text(info.rows[r].cells[0], a, bold=True, size=SZ_TINY)
    cell_text(info.rows[r].cells[1], "")
    cell_text(info.rows[r].cells[2], b, bold=True, size=SZ_TINY)
    cell_text(info.rows[r].cells[3], "")
cell_text(info.rows[2].cells[0], "URL เว็บไซต์", bold=True, size=SZ_TINY)
cell_text(info.rows[2].cells[1], "https://", size=SZ_TINY)
cell_text(info.rows[2].cells[2], "URL หน้า profile", bold=True, size=SZ_TINY)
cell_text(info.rows[2].cells[3], "https://github.com/", size=SZ_TINY)

# ---- Mission 0 ----
para(doc, "Mission 0 · Privacy Check — ตรวจข้อมูลก่อนเผยแพร่",
     bold=True, color=BLUE, size=SZ_SMALL, before=7, after=1)
para(doc, "ลบต้นฉบับทีหลังได้ แต่สำเนาที่คนอื่นเก็บไว้ลบไม่ได้ ต้องผ่านก่อนเริ่ม Mission 1",
     size=SZ_TINY, after=2)
T([("", "ไม่มีเลขบัตรประชาชน หรือเลขบัญชีธนาคาร"),
   ("", "ไม่มีเบอร์โทรศัพท์ ที่อยู่บ้าน หรือภาพบัตรประจำตัว"),
   ("", "ไม่มีข้อมูลที่บอกได้ว่าเราอยู่ที่ไหนในแต่ละช่วงเวลา"),
   ("", "ใช้ชื่อที่ยินดีให้เผยแพร่ ไม่ใช่ชื่อเต็มคู่รหัสนักศึกษา"),
   ("", "ข้อความและรูปเป็นของตนเอง หรือระบุแหล่งที่มาแล้ว"),
   ("", "ยินดีให้คนที่ไม่รู้จักอ่านทุกบรรทัดที่เผยแพร่")],
  ["ยืนยัน", "รายการตรวจสอบ"], [800, WIDTH - 800])
rich(doc, [("ลงชื่อ ", True), ("__________________________   ", False),
           ("วันที่ ", True), ("____________________", False)],
     before=4, after=0, size=SZ_SMALL)

# ---- Mission 2 ----
para(doc, "Mission 2 · Make It Yours — ร่างเนื้อหาเว็บไซต์ของตนเอง",
     bold=True, color=BLUE, size=SZ_SMALL, before=6, after=2)
draft = T([("1. ชื่อที่ใช้แสดง", ""),
           ("2. หนึ่งประโยคแนะนำตัว", ""),
           ("3. ข้อความแนะนำตัว", ""),
           ("4. กำลังเรียนรู้", ""),
           ("5. ธีมสีที่เลือก", "")],
          ["ส่วนของหน้าเว็บ", "ข้อความที่จะใช้"], [2900, WIDTH - 2900])
HINTS = ["ใช้ชื่อเล่นได้ ไม่ต้องเป็นชื่อเต็ม",
         "เจาะจงจนคนอ่านนึกภาพออก",
         "2-3 บรรทัด มาจากไหน สนใจอะไร",
         "3 รายการ เฉพาะที่เรียนอยู่จริง",
         "6 ธีม ดูชื่อทั้งหมดในไฟล์ index.html"]
for i, (hint, extra) in enumerate(zip(HINTS, [1, 1, 2, 2, 1]), 1):
    cell_text(draft.rows[i].cells[0], hint, size=SZ_TINY, first=False)
    for _ in range(extra):
        cell_text(draft.rows[i].cells[1], "", first=False)

rich(doc, [("อีกสี่ปีข้างหน้า อยากให้คนที่เปิดดู profile ของเราเห็นอะไร  ", True),
           ("_______________________________", False)], before=4, after=0, size=SZ_SMALL)

# ==========================================================================
# หน้า 2
# ==========================================================================
# ใช้ page-break-before บนหัวข้อแรกของหน้า แทนการเพิ่มย่อหน้าที่มีตัวแบ่งหน้า
# เพราะย่อหน้านั้นจะกินหนึ่งบรรทัดท้ายหน้า 1 และถูกดันข้ามหน้าไปเอง
head2 = para(doc, "เช็กลิสต์การออกแบบ — ตรวจงานตนเองก่อนส่ง",
             bold=True, color=BLUE, size=SZ_SMALL, after=2)
head2.paragraph_format.page_break_before = True
T([("", "ย่อหน้าต่างให้แคบเท่าจอมือถือแล้ว ยังอ่านได้ ไม่ล้นจอ"),
   ("", "ถอยห่างสองเมตร ยังบอกได้ว่าส่วนใดสำคัญที่สุด"),
   ("", "เปลี่ยนธีมสี และแก้ค่าใน CSS อย่างน้อยหนึ่งค่า อธิบายได้ว่าแก้อะไร"),
   ("", "ไม่มีข้อความตัวอย่างหลงเหลือบนหน้าเว็บ"),
   ("", "ประโยคแนะนำตัวเจาะจงพอที่เพื่อนจะจำได้")],
  ["ผ่าน", "รายการตรวจสอบการออกแบบ"], [800, WIDTH - 800])
rich(doc, [("ค่าใน CSS ที่แก้ ", True), ("________________  ", False),
           ("ผลที่เกิดขึ้น ", True), ("____________________________", False)],
     before=2, after=0, size=SZ_SMALL)
rich(doc, [("ชื่อเพื่อนที่ช่วยอ่าน ", True), ("_____________  ", False),
           ("สิ่งที่เพื่อนจำได้ ", True), ("__________________________", False)],
     before=2, after=0, size=SZ_SMALL)

# ---- Mission 3 ----
para(doc, "Mission 3 · Trace the Request — บันทึกค่าที่วัดได้จากเว็บของตนเอง",
     bold=True, color=BLUE, size=SZ_SMALL, before=4, after=1)
T([("IP address ของเว็บตนเอง", "nslookup <โดเมน>", ""),
   ("RTT เฉลี่ย (ms)", "ping <โดเมน>", ""),
   ("status code หน้าแรก", "F12 > Network > Status", ""),
   ("เวอร์ชัน HTTP", "Protocol / แผงท้ายเว็บ", ""),
   ("ค่า TTFB", "แผงท้ายหน้าเว็บ", "")],
  ["สิ่งที่ต้องหา", "หาจากที่ใด", "ค่าที่วัดได้"], [3000, 3000, WIDTH - 6000])
rich(doc, [("เปิด DevTools ", True),
           ("กด F12 (Mac: Cmd+Option+I) > Network > Ctrl+F5 · "
            "ไม่เห็นคอลัมน์ Protocol ให้คลิกขวาที่หัวตาราง", False)],
     before=0, after=0, size=SZ_TINY)

# ---- คำถาม ----
para(doc, "คำถามท้ายภารกิจ", bold=True, color=BLUE, size=SZ_SMALL, before=4, after=1)
for i, q in enumerate([
    "จากค่า RTT ที่วัดได้ server อยู่ห่างออกไปกี่กิโลเมตร แสดงวิธีคิดด้วย",
    "เมื่อมีคนพิมพ์ URL ของเราจนหน้าเว็บขึ้น มีสี่ขั้นตอนหลักอะไรบ้าง ตามลำดับ",
], 1):
    rich(doc, [(f"{i}. ", True), (q, False)], after=1, size=SZ_SMALL)
    blank_lines(doc, 3, indent=280, size=SZ_TINY)

doc.save(OUT)
print("บันทึกแล้ว:", OUT)
