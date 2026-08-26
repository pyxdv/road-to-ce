#!/usr/bin/env python3
"""ตรวจจำนวนหน้าจริงของไฟล์ .docx ด้วยการแปลงเป็น PDF

ต้องมี libreoffice-writer และ poppler-utils
ฟอนต์ TH Sarabun New ไม่มีในเครื่องนี้ จึงใช้ Sarabun แทนผ่าน fontconfig
ซึ่งสัดส่วนใกล้เคียงแต่ไม่เท่ากันเป๊ะ ตัวเลขที่ได้จึงเป็นค่าประมาณอย่างระมัดระวัง
Sarabun กว้างกว่า TH Sarabun New เล็กน้อย ผลที่ได้จึงไม่ต่ำกว่าความจริง
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMITS = {'worksheet-3.1-print.docx': 2}   # ไฟล์ที่มีเพดานจำนวนหน้า


def pages_of(docx):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(docx, tmp)
        subprocess.run(['soffice', '--headless', f'-env:UserInstallation=file://{tmp}/lo',
                        '--convert-to', 'pdf', '--outdir', tmp,
                        str(pathlib.Path(tmp) / docx.name)],
                       capture_output=True, timeout=300)
        pdf = pathlib.Path(tmp) / (docx.stem + '.pdf')
        if not pdf.exists():
            return None
        out = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True).stdout
        m = re.search(r'^Pages:\s+(\d+)', out, re.M)
        return int(m.group(1)) if m else None


def main():
    targets = sorted(ROOT.glob('*.docx'))
    failed = False
    for f in targets:
        n = pages_of(f)
        limit = LIMITS.get(f.name)
        if n is None:
            print(f'  {f.name}: แปลงไม่สำเร็จ')
            failed = True
        elif limit and n > limit:
            print(f'  {f.name}: {n} หน้า  เกินเพดาน {limit} หน้า')
            failed = True
        elif limit:
            print(f'  {f.name}: {n} หน้า  (เพดาน {limit}) ผ่าน')
        else:
            print(f'  {f.name}: {n} หน้า')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
