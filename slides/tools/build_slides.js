const pptxgen = require('pptxgenjs');

const BG      = '0B1020';
const PANEL   = '141B33';
const LINE    = '24304F';
const TEXT    = 'E8EDF7';
const MUTED   = '93A1C0';
const ACCENT  = '38BDF8';

// ต้องติดตั้งสองฟอนต์นี้ในเครื่องที่ใช้สอนก่อน ดาวน์โหลดฟรีที่ fonts.google.com
// ถ้าเครื่องไหนไม่มี PowerPoint จะเลือกฟอนต์อื่นแทนให้เอง สไลด์ยังใช้ได้แต่หน้าตาจะเปลี่ยน
// อยากกลับไปใช้ฟอนต์ที่มีติดเครื่องอยู่แล้ว เปลี่ยนเป็น 'Tahoma' กับ 'Courier New' ได้ทันที
const TH   = 'IBM Plex Sans Thai';     // เส้นหนากว่า TH Sarabun New อ่านชัดเมื่อฉายขึ้นจอ
const MONO = 'IBM Plex Mono';          // ตระกูลเดียวกัน ใช้กับหัวข้อย่อยและตัวอย่างโค้ด

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';           // 13.3 x 7.5 นิ้ว
pres.author = 'road-to-ce';
pres.title  = 'ใบงานที่ 3.1 สไลด์เปิดคาบ';

function slide() {
  const s = pres.addSlide();
  s.background = { color: BG };
  return s;
}

// บรรทัด prompt เล็ก ๆ มุมบนซ้าย ใช้เป็นลายเซ็นเดียวกันทุกสไลด์
function kicker(s, text) {
  s.addText('> ' + text, {
    x: 0.75, y: 0.5, w: 8, h: 0.35, margin: 0,
    fontFace: MONO, fontSize: 14, color: ACCENT, charSpacing: 1,
  });
}

function footer(s, text) {
  s.addText(text, {
    x: 0.75, y: 6.75, w: 11.8, h: 0.35, margin: 0,
    fontFace: TH, fontSize: 11, color: MUTED,
  });
}

/* ---------------------------------------------------------------- 1. Hook */
{
  const s = slide();
  kicker(s, 'unit 3 / worksheet 3.1');

  s.addText('90 นาทีจากนี้', {
    x: 0.75, y: 1.75, w: 11.8, h: 1.0, margin: 0,
    fontFace: TH, fontSize: 40, color: MUTED,
  });
  s.addText('เว็บของคุณจะเปิดได้จากทุกที่ในโลก', {
    x: 0.75, y: 2.7, w: 11.8, h: 1.3, margin: 0,
    fontFace: TH, fontSize: 54, bold: true, color: TEXT,
  });
  s.addText('และมันจะยังอยู่ต่อไป แม้คุณปิดคอมพิวเตอร์กลับบ้านแล้ว', {
    x: 0.75, y: 4.15, w: 11.8, h: 0.6, margin: 0,
    fontFace: TH, fontSize: 22, color: ACCENT,
  });

  footer(s, 'ใบงานที่ 3.1  ·  หน่วยที่ 3 พื้นฐานอินเทอร์เน็ตและบริการออนไลน์  ·  ECP1N / ECP2R  ·  ภาคเรียนที่ 1/2569');
  s.addNotes('≈20 วินาที\n\nยังไม่ต้องเปิดคอม ให้ฟังก่อน\nบอกว่าเมื่อจบคาบนี้ทุกคนจะมี URL ของตัวเอง ที่ส่งให้ที่บ้านเปิดดูได้');
}

/* ----------------------------------------------------------- 2. Live demo */
{
  const s = slide();
  kicker(s, 'live demo');

  s.addText('หยิบมือถือขึ้นมา แล้วพิมพ์ตามนี้', {
    x: 0.75, y: 1.3, w: 11.8, h: 0.8, margin: 0,
    fontFace: TH, fontSize: 36, bold: true, color: TEXT,
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: 0.75, y: 2.5, w: 11.8, h: 1.7, rectRadius: 0.12,
    fill: { color: PANEL }, line: { color: ACCENT, width: 1.5 },
  });
  s.addText('https://your-name.github.io', {
    x: 0.75, y: 2.5, w: 11.8, h: 1.7, margin: 0,
    fontFace: MONO, fontSize: 40, bold: true, color: ACCENT,
    align: 'center', valign: 'middle',
  });

  s.addText('นี่คือเว็บของอาจารย์ ไฟล์ไม่ได้อยู่บนเครื่องไหนในห้องนี้เลย', {
    x: 0.75, y: 4.6, w: 11.8, h: 0.5, margin: 0,
    fontFace: TH, fontSize: 22, color: TEXT,
  });
  s.addText('ใครที่ต่อ Wi-Fi อยู่ ลองปิด Wi-Fi แล้วใช้เน็ตมือถือเปิดดู ก็ยังขึ้นเหมือนเดิม', {
    x: 0.75, y: 5.15, w: 11.8, h: 0.5, margin: 0,
    fontFace: TH, fontSize: 18, color: MUTED,
  });

  footer(s, 'แก้ URL บนสไลด์นี้เป็นเว็บของผู้สอนก่อนใช้สอน');
  s.addNotes('≈30 วินาที\n\nสลับไปเปิดเว็บจริงบนจอ แล้วให้นักศึกษาเปิดตามบนมือถือ\nรอให้ห้องได้เสียงฮือฮาสักครู่ อย่ารีบข้าม\n\nอย่าลืมแก้ URL บนสไลด์ให้เป็นของตัวเองก่อนสอน');
}

/* -------------------------------------------------- 3. เกิดอะไรขึ้นเบื้องหลัง */
{
  const s = slide();
  kicker(s, 'what just happened');

  s.addText('กด Enter แล้วเกิดอะไรขึ้นบ้าง', {
    x: 0.75, y: 1.15, w: 11.8, h: 0.8, margin: 0,
    fontFace: TH, fontSize: 36, bold: true, color: TEXT,
  });

  const steps = [
    ['DNS',     'ชื่อโดเมน\nกลายเป็นเลข IP'],
    ['Connect', 'ต่อถึง server\nและเข้ารหัสด้วย TLS'],
    ['HTTP',    'ขอไฟล์\nแล้วได้ 200 OK'],
    ['Render',  'browser วาดออกมา\nเป็นหน้าเว็บ'],
  ];
  const cardW = 2.75, gap = 0.28, startX = 0.75;
  steps.forEach(([label, desc], i) => {
    const x = startX + i * (cardW + gap);
    s.addShape(pres.ShapeType.roundRect, {
      x, y: 2.35, w: cardW, h: 2.35, rectRadius: 0.1,
      fill: { color: PANEL }, line: { color: LINE, width: 1 },
    });
    s.addText(String(i + 1), {
      x: x + 0.3, y: 2.6, w: 0.6, h: 0.45, margin: 0,
      fontFace: MONO, fontSize: 20, bold: true, color: ACCENT,
    });
    s.addText(label, {
      x: x + 0.3, y: 3.1, w: cardW - 0.6, h: 0.45, margin: 0,
      fontFace: MONO, fontSize: 19, bold: true, color: TEXT,
    });
    s.addText(desc, {
      x: x + 0.3, y: 3.6, w: cardW - 0.6, h: 0.95, margin: 0,
      fontFace: TH, fontSize: 15, color: MUTED, lineSpacingMultiple: 1.2,
    });
  });

  s.addText('วันนี้ทำทั้งสองฝั่ง สร้างเว็บของตัวเอง แล้วย้อนดูว่ามันเดินทางมาถึงคนอ่านอย่างไร', {
    x: 0.75, y: 5.1, w: 11.8, h: 0.9, margin: 0,
    fontFace: TH, fontSize: 19, color: ACCENT,
  });

  footer(s, 'รายละเอียดทั้งหมดอยู่ในใบความรู้ที่ 3.1 หัวข้อ 1 ถึง 4');
  s.addNotes('≈30 วินาที\n\nไล่สี่ขั้นเร็ว ๆ ไม่ต้องลงลึก เพราะอ่านมาแล้วจากใบความรู้\nย้ำว่าเดี๋ยว Mission 3 จะได้วัดค่าจริงของขั้นเหล่านี้จากเว็บตัวเอง');
}

/* -------------------------------------------------------- 4. ภารกิจวันนี้ */
{
  const s = slide();
  kicker(s, 'today');

  s.addText('90 นาที 5 ภารกิจ', {
    x: 0.75, y: 1.15, w: 11.8, h: 0.8, margin: 0,
    fontFace: TH, fontSize: 36, bold: true, color: TEXT,
  });

  const missions = [
    ['0', 'Privacy Check',     'ตรวจข้อมูลก่อนเผยแพร่',   '5 นาที',  false],
    ['1', 'Go Live',           'เอาเว็บขึ้นออนไลน์',       '30 นาที', false],
    ['2', 'Make It Yours',     'ทำให้เป็นของเรา',          '30 นาที', true ],
    ['3', 'Trace the Request', 'ตามรอยข้อมูล',            '10 นาที', false],
    ['4', 'GitHub Profile',    'หน้าโปรไฟล์ของเรา',        '10 นาที', false],
  ];
  const rowH = 0.78, top = 2.15;
  missions.forEach(([num, en, th, time, main], i) => {
    const y = top + i * (rowH + 0.10);
    s.addShape(pres.ShapeType.roundRect, {
      x: 0.75, y, w: 11.8, h: rowH, rectRadius: 0.08,
      fill: { color: main ? '1B2C4A' : PANEL },
      line: { color: main ? ACCENT : LINE, width: main ? 1.5 : 1 },
    });
    s.addText(num, {
      x: 1.05, y, w: 0.6, h: rowH, margin: 0,
      fontFace: MONO, fontSize: 20, bold: true,
      color: main ? ACCENT : MUTED, valign: 'middle',
    });
    s.addText(en, {
      x: 1.75, y, w: 3.1, h: rowH, margin: 0,
      fontFace: MONO, fontSize: 17, bold: true, color: TEXT, valign: 'middle',
    });
    s.addText(th, {
      x: 5.0, y, w: 5.0, h: rowH, margin: 0,
      fontFace: TH, fontSize: 17, color: MUTED, valign: 'middle',
    });
    s.addText(time, {
      x: 10.3, y, w: 2.0, h: rowH, margin: 0,
      fontFace: TH, fontSize: 17, bold: main, align: 'right',
      color: main ? ACCENT : MUTED, valign: 'middle',
    });
  });

  footer(s, 'Mission 2 คือภารกิจหลักของคาบนี้ ได้เวลามากที่สุด');
  s.addNotes('≈25 วินาที\n\nไล่ชื่อภารกิจเร็ว ๆ ไม่ต้องอธิบายรายละเอียด\nชี้ให้เห็นว่า Mission 2 ได้เวลามากที่สุด เพราะเป็นส่วนที่ทำให้เว็บเป็นของเราจริง ๆ');
}

/* -------------------------------------------------------- 5. กฎข้อเดียว */
{
  const s = slide();
  kicker(s, 'rule #1');

  s.addText('ทุกอย่างที่ขึ้นวันนี้ เป็นสาธารณะ', {
    x: 0.75, y: 1.5, w: 11.8, h: 0.9, margin: 0,
    fontFace: TH, fontSize: 44, bold: true, color: TEXT,
  });
  s.addText('ลบทีหลังได้ แต่สำเนาที่คนอื่นเก็บไว้แล้ว เราลบไม่ได้', {
    x: 0.75, y: 2.5, w: 11.8, h: 0.6, margin: 0,
    fontFace: TH, fontSize: 22, color: ACCENT,
  });

  s.addText('ห้ามใส่ลงเว็บเด็ดขาด', {
    x: 0.75, y: 3.5, w: 11.8, h: 0.45, margin: 0,
    fontFace: TH, fontSize: 18, color: MUTED,
  });

  const banned = ['เลขบัตรประชาชน', 'เบอร์โทรศัพท์', 'ที่อยู่บ้าน', 'รูปบัตรนักศึกษา'];
  const chipW = 2.75, gap = 0.28;
  banned.forEach((t, i) => {
    const x = 0.75 + i * (chipW + gap);
    s.addShape(pres.ShapeType.roundRect, {
      x, y: 4.05, w: chipW, h: 0.85, rectRadius: 0.42,
      fill: { color: PANEL }, line: { color: 'F87171', width: 1.5 },
    });
    s.addText(t, {
      x, y: 4.05, w: chipW, h: 0.85, margin: 0,
      fontFace: TH, fontSize: 17, color: TEXT, align: 'center', valign: 'middle',
    });
  });

  s.addText('ใช้ชื่อเล่นได้ ไม่ต้องใส่ชื่อ-นามสกุลเต็มคู่กับรหัสนักศึกษา', {
    x: 0.75, y: 5.35, w: 11.8, h: 0.6, margin: 0,
    fontFace: TH, fontSize: 20, color: TEXT,
  });

  footer(s, 'เปิดใบงานหน้า Mission 0 แล้วเริ่มได้เลย');
  s.addNotes('≈15 วินาที\n\nพูดให้ช้าและหนักแน่นกว่าสไลด์อื่น\nจบด้วยการให้เปิดใบงานหน้า Mission 0 แล้วลงมือ');
}

/* ------------------------------------- 6. สไตล์ profile (ใช้ตอน Mission 4) */
{
  const s = slide();
  kicker(s, 'bonus · ใช้ตอน mission 4');

  s.addText('อยากให้หน้า profile ดูเท่กว่านี้ เลือกสไตล์ได้', {
    x: 0.75, y: 1.15, w: 11.8, h: 0.8, margin: 0,
    fontFace: TH, fontSize: 36, bold: true, color: TEXT,
  });

  // แต่ละใบ: ชื่อสไตล์ · ใครเหมาะ · ภาพจำลองหน้าตาของสไตล์นั้น
  // ในภาพจำลอง m = บรรทัดที่ใช้ฟอนต์ monospace, b = ตัวหนา
  const styles = [
    {
      name: 'minimalist', pick: false,
      who: 'เรียบ ไม่มีของตกแต่ง\nทุกบรรทัดต้องให้ข้อมูล',
      prev: [
        ['สมชาย', { b: true }],
        ['วิศวกรรมคอมพิวเตอร์ ปี 1', {}],
        ['', {}],
        ['กำลังทำ', { b: true }],
        ['เว็บส่วนตัวหน้าแรก', {}],
        ['', {}],
        ['กำลังเรียน', { b: true }],
        ['HTML · CSS · Git', { m: true }],
      ],
    },
    {
      name: 'learn-in-public ★', pick: true,
      who: 'เล่าว่ากำลังเรียนรู้อะไรอยู่\nเหมาะกับปี 1 ที่สุด',
      prev: [
        ['🔭 กำลังทำ …', {}],
        ['🌱 กำลังเรียน …', {}],
        ['🧠 บันทึกการเรียนรู้', { b: true }],
        ['   ส.ค. เพิ่งเข้าใจว่า', {}],
        ['   DNS ทำงานก่อน', {}],
        ['   browser ต่อหา server', {}],
        ['💬 ถามผมได้เรื่อง …', {}],
      ],
    },
    {
      name: 'visual', pick: false,
      who: 'มี badge โลโก้เครื่องมือ\nและการ์ดสถิติ',
      prev: [
        ['[ C ][ HTML5 ][ Git ]', { m: true }],
        ['[ Linux ][ VS Code ]', { m: true }],
        ['', {}],
        ['GitHub stats', { m: true, b: true }],
        ['commits  [##....]', { m: true }],
        ['ปี 1 ยังว่างเป็นปกติ', {}],
      ],
    },
    {
      name: 'terminal', pick: false,
      who: 'กลิ่นอาย command line\nสายฝังตัว เครือข่าย backend',
      prev: [
        ['$ whoami', { m: true, b: true }],
        ['somchai — ce freshman', { m: true }],
        ['$ ls interests/', { m: true, b: true }],
        ['embedded/ networking/', { m: true }],
        ['$ _', { m: true, b: true }],
      ],
    },
  ];

  const cardW = 2.74, gap = 0.28, top = 2.15, cardH = 3.05;
  styles.forEach((st, i) => {
    const x = 0.75 + i * (cardW + gap);

    s.addShape(pres.ShapeType.roundRect, {
      x, y: top, w: cardW, h: cardH, rectRadius: 0.1,
      fill: { color: st.pick ? '1B2C4A' : PANEL },
      line: { color: st.pick ? ACCENT : LINE, width: st.pick ? 1.5 : 1 },
    });
    s.addText(st.name, {
      x: x + 0.25, y: top + 0.18, w: cardW - 0.5, h: 0.32, margin: 0,
      fontFace: MONO, fontSize: 13, bold: true, color: st.pick ? ACCENT : TEXT,
    });
    s.addText(st.who, {
      x: x + 0.25, y: top + 0.58, w: cardW - 0.5, h: 0.62, margin: 0,
      fontFace: TH, fontSize: 11, color: MUTED, lineSpacingMultiple: 1.3,
    });

    s.addShape(pres.ShapeType.roundRect, {
      x: x + 0.22, y: top + 1.3, w: cardW - 0.44, h: 1.55, rectRadius: 0.07,
      fill: { color: '0E1526' }, line: { color: LINE, width: 1 },
    });
    s.addText(st.prev.map(([text, o], k) => ({
      text: text || ' ',
      options: {
        fontFace: o.m ? MONO : TH, fontSize: 9, bold: !!o.b,
        color: o.b ? TEXT : MUTED, breakLine: k < st.prev.length - 1,
      },
    })), {
      x: x + 0.35, y: top + 1.38, w: cardW - 0.7, h: 1.4, margin: 0,
      lineSpacingMultiple: 1.25,
    });
  });

  s.addText('starter/profile-readme/styles/  ·  gallery.md  ·  example-filled.md', {
    x: 0.75, y: 5.45, w: 11.8, h: 0.4, margin: 0,
    fontFace: MONO, fontSize: 13, color: ACCENT,
  });

  footer(s, 'ในคาบทำแบบพื้นฐานให้เสร็จก่อน · สไตล์อื่นเลือกทำต่อเองนอกเวลา · badge คือรูปจากบริการภายนอก ใส่เฉพาะเครื่องมือที่ใช้เป็นจริง');
  s.addNotes('≈40 วินาที · ไม่ใช่แผ่นเปิดคาบ ให้ข้ามไปใช้ตอนเข้า Mission 4 นาทีที่ ~75\n\nในคาบให้ทุกคนทำแบบพื้นฐานให้เสร็จก่อน อย่าเพิ่งเปิดให้เลือกสไตล์\nเพราะเวลาจะหมดไปกับการเลือกจนไม่ได้เขียนเนื้อหา\n\nถ้าเหลือเวลาท้ายคาบ เปิดไฟล์ gallery.md ให้ดูสัก 1 นาที\nแล้วบอกว่ากลับไปทำต่อเองที่บ้านได้ ไม่มีคะแนน แต่มีผลกับสี่ปีข้างหน้า\n\nถ้ามีคนถามเรื่อง badge ให้ย้ำว่ามันคือรูปที่ดึงมาจากเว็บอื่น\nใครก็ตั้งข้อความว่าอะไรก็ได้ ใส่เฉพาะเครื่องมือที่ใช้เป็นจริง');
}

pres.writeFile({ fileName: 'slides-3.1-opening.pptx' })
  .then(f => console.log('สร้างแล้ว:', f));
