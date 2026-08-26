#!/usr/bin/env python3
"""ตรวจไฟล์ข้อมูลนักศึกษาใน students/ ก่อนนำขึ้น Class Wall

รันเองในเครื่อง:   python3 scripts/validate_students.py
ตรวจเฉพาะบางไฟล์:  python3 scripts/validate_students.py students/somchai.json

ออกด้วย exit code 1 ถ้ามีไฟล์ไม่ผ่าน เพื่อให้ GitHub Actions ขึ้นสถานะแดง
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STUDENTS = ROOT / "students"

REQUIRED = ("github", "display_name", "cohort", "year", "tagline", "site")
OPTIONAL = ("interests", "accent")
COHORTS = ("ECP1N", "ECP2R")

USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

# รูปแบบข้อมูลส่วนบุคคลที่ห้ามเผยแพร่บน repository สาธารณะ
PRIVACY_PATTERNS = (
    (re.compile(r"\b\d{13}\b"), "เลข 13 หลัก (อาจเป็นเลขบัตรประชาชน)"),
    (re.compile(r"\b0\d{1,2}[- ]?\d{3}[- ]?\d{4}\b"), "เบอร์โทรศัพท์"),
    (re.compile(r"\b\+66[- ]?\d[- ]?\d{3}[- ]?\d{4}\b"), "เบอร์โทรศัพท์ (+66)"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "ที่อยู่อีเมล"),
    (re.compile(r"\b\d{3}-\d-\d{5}-\d\b"), "เลขบัญชีธนาคาร"),
)


class Problem(Exception):
    pass


def check_privacy(raw, errors):
    for pattern, label in PRIVACY_PATTERNS:
        found = pattern.search(raw)
        if found:
            errors.append(
                f"possible personal data — พบ{label} ในไฟล์: {found.group(0)!r}\n"
                f"       repository นี้เป็นสาธารณะและมีสำเนาคงอยู่ กรุณาลบข้อมูลนี้ออกแล้ว commit ใหม่"
            )


def check_site(url, errors):
    if not isinstance(url, str) or not url.startswith("https://"):
        errors.append('ช่อง "site" ต้องเป็น URL ที่ขึ้นต้นด้วย https:// เท่านั้น')
        return
    if re.search(r"\s", url):
        errors.append('ช่อง "site" มีช่องว่างปนอยู่')
    if len(url) > 200:
        errors.append('ช่อง "site" ยาวเกิน 200 ตัวอักษร')


def check_card(path):
    """คืน list ของข้อความปัญหา ถ้าว่างแปลว่าผ่าน"""
    errors = []
    raw = path.read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(
            f"invalid JSON ที่บรรทัด {exc.lineno} คอลัมน์ {exc.colno}: {exc.msg}\n"
            f"       ตรวจเครื่องหมายจุลภาคที่ขาดหรือเกิน และเครื่องหมายคำพูดรอบบรรทัดนั้น"
        )
        check_privacy(raw, errors)
        return errors

    if not isinstance(data, dict):
        errors.append("ไฟล์ต้องเป็น JSON object เปิดด้วย { และปิดด้วย }")
        check_privacy(raw, errors)
        return errors

    for field in REQUIRED:
        if field not in data or data[field] in ("", None, []):
            errors.append(f'ขาดช่องที่จำเป็น: "{field}"')

    unknown = set(data) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        errors.append(
            f"มีช่องที่ไม่รู้จัก: {sorted(unknown)} — ใช้ได้เฉพาะ {list(REQUIRED + OPTIONAL)}"
        )
    if errors:
        check_privacy(raw, errors)
        return errors

    username = data["github"]
    if not USERNAME_RE.match(str(username)):
        errors.append(f'"github": {username!r} ไม่ใช่รูปแบบชื่อผู้ใช้ GitHub ที่ถูกต้อง')
    elif path.stem != username:
        errors.append(
            f'filename must match "github" field — ไฟล์ชื่อ {path.name} '
            f'แต่ในไฟล์ระบุ "github": "{username}"\n'
            f"       เปลี่ยนชื่อไฟล์เป็น {username}.json (ตัวพิมพ์เล็ก-ใหญ่ต้องตรงกัน)"
        )

    if data["cohort"] not in COHORTS:
        errors.append(f'"cohort" ต้องเป็นค่าใดค่าหนึ่งใน {list(COHORTS)}')

    year = data["year"]
    if not isinstance(year, int) or not 2560 <= year <= 2600:
        errors.append('"year" ต้องเป็นปีการศึกษาแบบตัวเลข พ.ศ. เช่น 2569 (ไม่ต้องใส่เครื่องหมายคำพูด)')

    name = data["display_name"]
    if not isinstance(name, str) or not 1 <= len(name) <= 60:
        errors.append('"display_name" ต้องเป็นข้อความยาว 1–60 ตัวอักษร')

    tagline = data["tagline"]
    if not isinstance(tagline, str) or not 1 <= len(tagline) <= 120:
        errors.append('"tagline" ต้องเป็นข้อความยาว 1–120 ตัวอักษร')

    check_site(data["site"], errors)

    interests = data.get("interests", [])
    if not isinstance(interests, list) or len(interests) > 5:
        errors.append('"interests" ต้องเป็นลิสต์ ไม่เกิน 5 รายการ')
    elif any(not isinstance(i, str) or len(i) > 24 for i in interests):
        errors.append('แต่ละรายการใน "interests" ต้องเป็นข้อความไม่เกิน 24 ตัวอักษร')

    accent = data.get("accent")
    if accent is not None and not HEX_RE.match(str(accent)):
        errors.append('"accent" ต้องเป็นรหัสสี hex 6 หลัก เช่น "#38bdf8"')

    check_privacy(raw, errors)
    return errors


def load_cards():
    """อ่านไฟล์ข้อมูลที่ผ่านการตรวจแล้วทั้งหมด ใช้ร่วมกับ build_wall.py"""
    cards = []
    for path in sorted(STUDENTS.glob("*.json")):
        if path.name == "_TEMPLATE.json":
            continue
        cards.append(json.loads(path.read_text(encoding="utf-8")))
    return cards


def main(argv):
    if argv:
        targets = [pathlib.Path(a) for a in argv]
    else:
        targets = sorted(STUDENTS.glob("*.json"))

    targets = [p for p in targets if p.name != "_TEMPLATE.json"]
    if not targets:
        print("ไม่พบไฟล์ข้อมูลให้ตรวจ")
        return 0

    failed = 0
    for path in targets:
        problems = check_card(path)
        if problems:
            failed += 1
            print(f"\n❌ {path}")
            for p in problems:
                print(f"   • {p}")
        else:
            print(f"✅ {path}")

    print()
    if failed:
        print(f"ไม่ผ่าน {failed} ไฟล์ จากทั้งหมด {len(targets)} ไฟล์")
        print("แก้ไฟล์บน branch เดิมแล้ว commit ใหม่ Pull Request จะอัปเดตและตรวจซ้ำให้เอง")
        return 1

    print(f"ผ่านทั้งหมด {len(targets)} ไฟล์ 🎉")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
