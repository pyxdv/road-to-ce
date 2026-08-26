#!/usr/bin/env python3
"""สร้างหน้า Class Wall จากไฟล์ข้อมูลนักศึกษาทั้งหมดใน students/

รัน:  python3 scripts/build_wall.py
ผล:   site/index.html

สคริปต์นี้ถูกเรียกโดย GitHub Actions ทุกครั้งที่มี Pull Request ถูก merge เข้า main
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STUDENTS = ROOT / "students"
OUT_DIR = ROOT / "site"
SKIP = {"_TEMPLATE.json"}

FALLBACK_ACCENT = "#38bdf8"


def esc(value):
    return html.escape(str(value), quote=True)


def safe_url(url):
    """อนุญาตเฉพาะ https:// เพื่อป้องกันลิงก์อันตรายบนหน้าสาธารณะ"""
    url = str(url)
    return url if url.startswith("https://") else "#"


def load_cards():
    cards = []
    for path in sorted(STUDENTS.glob("*.json")):
        if path.name in SKIP:
            continue
        try:
            cards.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            print(f"ข้าม {path.name}: JSON ไม่ถูกต้อง ({exc.msg})", file=sys.stderr)
    cards.sort(key=lambda c: (str(c.get("cohort", "")), str(c.get("github", "")).lower()))
    return cards


def render_card(card):
    accent = card.get("accent") or FALLBACK_ACCENT
    interests = card.get("interests") or []
    tags = "".join(f"<li>{esc(i)}</li>" for i in interests[:5])
    return f"""      <article class="card" style="--accent: {esc(accent)}">
        <header>
          <span class="cohort">{esc(card.get('cohort', '—'))}</span>
          <span class="year">{esc(card.get('year', ''))}</span>
        </header>
        <h2>{esc(card.get('display_name', card.get('github', '')))}</h2>
        <p class="tagline">{esc(card.get('tagline', ''))}</p>
        <ul class="tags">{tags}</ul>
        <footer>
          <a class="site" href="{esc(safe_url(card.get('site', '')))}" target="_blank" rel="noopener noreferrer">เปิดเว็บไซต์ ↗</a>
          <a class="gh" href="https://github.com/{esc(card.get('github', ''))}" target="_blank" rel="noopener noreferrer">@{esc(card.get('github', ''))}</a>
        </footer>
      </article>"""


def render_page(cards):
    by_cohort = {}
    for c in cards:
        by_cohort[str(c.get("cohort", "—"))] = by_cohort.get(str(c.get("cohort", "—")), 0) + 1
    stats = " · ".join(f"{k} {v} คน" for k, v in sorted(by_cohort.items()))
    cards_html = "\n".join(render_card(c) for c in cards)

    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Class Wall · เส้นทางสู่วิศวกรรมคอมพิวเตอร์</title>
<meta name="description" content="หน้ารวมเว็บไซต์ของนักศึกษาวิศวกรรมคอมพิวเตอร์ มทร.อีสาน จาก Pull Request ที่นักศึกษาเปิดเอง">
<style>
  :root {{
    --bg: #0b1020;
    --bg-soft: #131a30;
    --line: #24304f;
    --text: #e8edf7;
    --muted: #93a1c0;
    --accent: {FALLBACK_ACCENT};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background:
      radial-gradient(1100px 500px at 15% -10%, #1d2a52 0%, transparent 60%),
      radial-gradient(900px 420px at 95% 0%, #10305c 0%, transparent 55%),
      var(--bg);
    color: var(--text);
    font-family: "Segoe UI", "Noto Sans Thai", system-ui, sans-serif;
    line-height: 1.65;
    min-height: 100vh;
  }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 20px 80px; }}
  header.hero {{ padding: 72px 0 40px; }}
  .kicker {{
    font: 600 13px/1 ui-monospace, "SF Mono", Menlo, monospace;
    letter-spacing: .18em; text-transform: uppercase; color: var(--accent);
  }}
  h1 {{ font-size: clamp(32px, 6vw, 56px); margin: 14px 0 10px; line-height: 1.15; }}
  .lede {{ color: var(--muted); max-width: 62ch; margin: 0 0 22px; font-size: 17px; }}
  .stats {{
    display: inline-flex; gap: 10px; align-items: center; flex-wrap: wrap;
    border: 1px solid var(--line); background: rgba(19,26,48,.7);
    border-radius: 999px; padding: 8px 18px; font-size: 14px; color: var(--muted);
  }}
  .stats strong {{ color: var(--text); }}
  .grid {{
    display: grid; gap: 18px; margin-top: 38px;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }}
  .card {{
    position: relative; display: flex; flex-direction: column;
    background: linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
    border: 1px solid var(--line); border-radius: 16px; padding: 20px;
    overflow: hidden; transition: transform .18s ease, border-color .18s ease;
  }}
  .card::before {{
    content: ""; position: absolute; inset: 0 0 auto 0; height: 3px; background: var(--accent);
  }}
  .card:hover {{ transform: translateY(-4px); border-color: var(--accent); }}
  .card header {{ display: flex; gap: 8px; align-items: center; font-size: 12px; }}
  .cohort {{
    font: 600 11px/1 ui-monospace, Menlo, monospace; letter-spacing: .1em;
    color: var(--accent); border: 1px solid currentColor;
    border-radius: 999px; padding: 4px 9px;
  }}
  .year {{ color: var(--muted); }}
  .card h2 {{ font-size: 21px; margin: 12px 0 6px; }}
  .tagline {{ color: var(--muted); margin: 0 0 14px; font-size: 15px; flex: 1; }}
  .tags {{ list-style: none; display: flex; flex-wrap: wrap; gap: 6px; padding: 0; margin: 0 0 16px; }}
  .tags li {{
    font: 500 12px/1 ui-monospace, Menlo, monospace;
    background: rgba(255,255,255,.06); border-radius: 6px; padding: 5px 8px; color: var(--muted);
  }}
  .card footer {{
    display: flex; justify-content: space-between; align-items: center; gap: 10px;
    border-top: 1px solid var(--line); padding-top: 14px; font-size: 14px;
  }}
  .card a {{ text-decoration: none; }}
  .site {{ color: var(--accent); font-weight: 600; }}
  .gh {{ color: var(--muted); font-family: ui-monospace, Menlo, monospace; font-size: 13px; }}
  .card a:hover {{ text-decoration: underline; }}
  .empty {{
    border: 1px dashed var(--line); border-radius: 16px; padding: 48px 24px;
    text-align: center; color: var(--muted);
  }}
  footer.page {{
    margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--line);
    color: var(--muted); font-size: 14px;
  }}
  footer.page a {{ color: var(--accent); }}
  @media (prefers-reduced-motion: reduce) {{ .card {{ transition: none; }} }}
</style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <p class="kicker">road-to-ce · class wall</p>
      <h1>Class Wall</h1>
      <p class="lede">
        หน้ารวมเว็บไซต์ของนักศึกษาวิศวกรรมคอมพิวเตอร์ มทร.อีสาน
        ทุกรายการมาจาก Pull Request ที่นักศึกษาเปิดเองและมีเพื่อนร่วมรุ่นเป็นผู้ review
        หน้านี้ถูกสร้างขึ้นใหม่โดยอัตโนมัติทุกครั้งที่มีการ merge
      </p>
      <p class="stats"><strong>{len(cards)}</strong> เว็บไซต์{(' · ' + stats) if stats else ''}</p>
    </header>
    <main class="grid">
{cards_html if cards else '      <div class="empty">ยังไม่มีข้อมูล เปิด Pull Request แรกได้เลย</div>'}
    </main>
    <footer class="page">
      หน้านี้สร้างจากไฟล์ใน <code>students/</code> ด้วย <code>scripts/build_wall.py</code>
      · ต้องการเพิ่มชื่อของตนเอง อ่าน <a href="https://github.com/pyxdv/road-to-ce/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a>
    </footer>
  </div>
</body>
</html>
"""


def main():
    cards = load_cards()
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(render_page(cards), encoding="utf-8")
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"สร้าง site/index.html จากข้อมูล {len(cards)} รายการเรียบร้อย")
    return 0


if __name__ == "__main__":
    sys.exit(main())
