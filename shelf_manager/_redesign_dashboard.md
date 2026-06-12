# Redesign Plan — Dashboard (index.html)

> **สถานะ:** แผน (ยังไม่ implement) · สร้าง 2026-06-12
> **ขอบเขต:** dashboard (`templates/index.html`) + **theme tokens ใน `base.html` (ทั้งแอปได้ตาม)** + backend hook เล็กน้อย
> **ทิศทาง:** **Workflow-first + Re-theme** → **Warm Paper (Claude/Fable minimal)** — เปลี่ยนจาก dark+green
> เดิมเป็นโทนกระดาษอุ่น accent clay/coral, serif หัวข้อ, whitespace เยอะ. ไม่เปลี่ยน route/feature/data
> **⚠️ scope เพิ่มจาก "polish":** เป็น re-theme → `base.html` (theme + nav + fonts) เปลี่ยนด้วย → ทุกหน้าได้
> โทนใหม่ทันที แต่ **dashboard คือหน้าแรกที่ polish layout เต็ม** หน้าอื่น (shelf/bottle/scan/...) ได้ธีมแต่ค่อย fine-tune ทีหลัง
> **อ้างอิงไฟล์ปัจจุบัน:** `templates/index.html` (227 บรรทัด), `templates/base.html`, `main.py:index()`, `database.py:get_stats()`

---

## เป้าหมาย
หน้านี้มีงานจริงข้อเดียว: **เปิดทุกเย็น 17:00 → รู้สถานะวันนี้ → กดไปถ่าย 100 ขวด**
redesign ต้องทำให้ flow นั้นชัดและเร็วที่สุด พร้อม polish ความสม่ำเสมอของ UI

## ปัญหาของเดิม (เจาะจง)
1. ไม่มี hierarchy — การ์ด gray-900 เต็มกว้างเรียงต่อกัน น้ำหนักเท่ากันหมด
2. เปลือง horizontal space บน desktop (controls เรียงตั้งทั้งที่จับคู่ได้)
3. token ไม่นิ่ง — border (gray-800/700/green-800/blue-800), rounded (xl/2xl), margin (mb-6/8) ปนกัน
4. ไม่มี primary CTA "เริ่มถ่าย"
5. stats ไม่ตรงงานจริง — "ภาพรอบนี้" ควรเป็น "ถ่ายวันนี้ Y/100 ขวด"

---

## Theme — Warm Paper (Claude/Fable minimal) · เลือก 2026-06-12

> ใส่ใน `base.html` → ทั้งแอป inherit. **หลักการ:** โทนกระดาษอุ่น, accent น้อยชิ้น (coral เฉพาะ
> primary action), serif หัวข้อ, whitespace เยอะ, เส้น hairline, เงาแทบไม่มี, มุมโค้งกลางๆ

### Design tokens
| token | hex | ใช้ที่ |
|---|---|---|
| `bg` (พื้นหน้า) | `#FAF9F5` | body background (paper) |
| `surface` (การ์ด) | `#FFFFFF` | card / panel |
| `ink` (ตัวอักษรหลัก) | `#2A2722` | heading + body |
| `muted` | `#908A7E` | label, hint, secondary |
| `line` (เส้น) | `#EAE7DF` | border hairline (1px) |
| `accent` (clay) | `#D97757` | ปุ่มหลัก, active state, progress |
| `accent-hover` | `#C45D3E` | hover ปุ่มหลัก |

**Status (ปรับให้เข้าโทนอุ่น อ่านชัดบนพื้นขาว):**
| สถานะ | hex | หมายเหตุ |
|---|---|---|
| healthy | `#6E8B5A` | sage เขียวอุ่น (ไม่ neon) |
| contaminated | `#C98A3C` | amber/clay |
| dead | `#B84A3E` | muted red |
| unknown | `#B8B3A8` | warm gray |
| empty cell | `#EFECE4` | จางสุด |

### Typography
- **Heading:** serif **Fraunces** (variable, อบอุ่นมีคาแรกเตอร์แบบ Tiempos) — น้ำหนัก 400–600
- **Body / UI:** sans **Inter** (humanist สะอาด)
- โหลดผ่าน Google Fonts ใน `<head>` ของ base.html:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  ```
- ขนาด: H1 serif ~28–32px, section heading serif ~18–20px, body 14–15px, line-height โปร่ง (1.5–1.6)

### Tailwind config (แทน block เดิมใน base.html)
```js
tailwind.config = {
  theme: { extend: {
    colors: {
      paper:'#FAF9F5', surface:'#FFFFFF', ink:'#2A2722', muted:'#908A7E',
      line:'#EAE7DF', clay:{DEFAULT:'#D97757', hover:'#C45D3E'},
      st:{ healthy:'#6E8B5A', contam:'#C98A3C', dead:'#B84A3E',
           unknown:'#B8B3A8', empty:'#EFECE4' },
    },
    fontFamily: { serif:['Fraunces','Georgia','serif'], sans:['Inter','system-ui','sans-serif'] },
    boxShadow: { soft:'0 1px 2px rgba(42,39,34,.04), 0 1px 3px rgba(42,39,34,.03)' },
  } },
}
```

### Style rules (ใช้ทั่วหน้า)
- พื้น `bg-paper text-ink font-sans` ที่ `<body>` · heading ใช้ `font-serif`
- card = `bg-surface border border-line rounded-2xl shadow-soft` (เงานุ่มมาก ไม่ใช่เงาเข้ม)
- ปุ่มหลัก = `bg-clay hover:bg-clay-hover text-white rounded-xl` · ปุ่มรอง = `border border-line text-ink hover:bg-paper`
- ระยะ: card padding `p-5`, gap ระหว่าง section `space-y-6`
- **accent discipline:** coral ใช้เฉพาะ primary action + active + progress — ห้ามใช้เป็นพื้นทั่วไป (นั่นคือกุญแจ minimal)

> **ข้อแลก (ยอมรับแล้ว):** Warm Paper สว่าง → จ้าตอนถ่ายกลางคืน. ถ้าใช้จริงแล้วแสบตา ค่อยเพิ่ม
> dark toggle ทีหลัง (tokens แยก theme ได้ ไม่ต้องรื้อ) — **ไม่ทำตอนนี้**

---

## งานที่จะทำ

### P0 — hierarchy + workflow

**P0.1 Header status strip** (แทน `<h1>Dashboard</h1>` เปล่า)
- แสดง: `🌱 {รอบ} · Day {global-day} · ถ่ายวันนี้ {Y}/{total}` + progress bar เล็ก
- ปุ่ม primary **"📷 เริ่มถ่าย"** → `/scan` (ตรงกับ ArUco workflow)
- "Day" ดึงจาก localStorage `vitro_global_day` (JS อัปเดต strip ด้วยตอน setGlobalDay)
- responsive: strip เป็น flex, ปุ่มตกบรรทัดใหม่บนจอแคบ

**P0.2 จัด operational zone 2 คอลัมน์** (desktop `md:grid-cols-2`, มือถือ stack)
- ซ้าย = Batch card (คงเนื้อหา/modal เดิม) · ขวา = Global Day stepper (คงเดิม)
- ลดความสูงหน้า + แยก "operational controls" ออกจาก "overview" ชัด

**P0.3 Stats cards ตรงงานจริง**
- เปลี่ยนใบที่ 2 "ภาพรอบนี้" → **"ถ่ายวันนี้ {Y}/{total}"** + progress bar
- เพิ่ม icon + accent บางๆ ทั้ง 4 ใบ (ขวด 🧪 / ถ่ายวันนี้ 📷 / Healthy ✓ / Cont+Dead ⚠)
- คง grid-cols-2 (มือถือ) / md:grid-cols-4

### P1 — consistency + polish
- **card token เดียว:** `bg-gray-900 border border-gray-800 rounded-2xl` + accent variant เฉพาะที่จำเป็น (เช่น batch active = border-green-700/purple-700)
- vertical rhythm มาตรฐาน: ใช้ `space-y-6` ครอบ section ทั้งหน้า แทน mb-6/8 ปน
- **shelf heatmap polish:** เพิ่ม `title=` (tooltip) ต่อ cell = `{bottle_id} · {status}`; ทำ H/C/D count เด่นขึ้น (chip เล็กแทน text จาง)
- **empty state** (ไม่มี batch): การ์ด onboarding เป็นมิตร + ปุ่มเริ่มรอบเด่น

---

## Backend hook ที่ต้องเพิ่ม (สำหรับ "ถ่ายวันนี้ Y/total")

`database.py` — ฟังก์ชันใหม่:
```python
def get_today_capture_count():
    """จำนวนขวด (distinct) ที่มีภาพถ่าย 'วันนี้' ใน batch ปัจจุบัน + total bottles"""
    active = get_active_batch()
    bid = active["id"] if active else None
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM bottles").fetchone()[0]
        today = conn.execute("""
            SELECT COUNT(DISTINCT bottle_id) FROM images
            WHERE date(date_taken) = date('now','localtime')
              AND (? IS NULL OR batch_id = ?)
        """, (bid, bid)).fetchone()[0]
    return {"today": today, "total": total}
```
`main.py:index()` — เรียกแล้วส่ง `today_capture` เข้า template (เพิ่ม 1 บรรทัด)

> หมายเหตุ: "Day point" (localStorage) กับ "ถ่ายวันนี้" (date จริง) เป็นคนละแกน — strip แสดงทั้งคู่ได้

---

## ของที่ "ไม่แตะ"
- route ทั้งหมด, DB schema, JS global-day logic (`vitro_global_day` localStorage)
- modal เริ่มรอบใหม่ (เนื้อหา/action เดิม — แค่ restyle ตาม token), mobile access banner
- **เปลี่ยน:** สีสถานะย้ายจาก neon (green/orange/red/slate) → warm (`st.*` ใน config); base.html nav ได้ธีมใหม่ด้วย

## เลย์เอาต์เป้าหมาย (desktop)
```
┌─ Header strip: 🌱 รอบ1 · Day 7 · ถ่าย 12/100 ▮▮▯▯ ── [📷 เริ่มถ่าย] ┐
├─ Mobile access banner (ย่อ) ──────────────────────────────────────┤
├─ Batch card ──────────────────┬─ Global Day stepper ──────────────┤  ← grid-cols-2
├─ Stats: [🧪 ขวด] [📷 ถ่ายวันนี้ ▮▮] [✓ Healthy] [⚠ Cont/Dead] ───┤
├─ Shelf S01 (heatmap+tooltip) ─┬─ Shelf S02 (heatmap+tooltip) ─────┤
└─ Legend ───────────────────────────────────────────────────────────┘
```

## ไฟล์ที่จะแก้ตอน implement
- `templates/base.html` — theme tokens (tailwind.config), Google Fonts, restyle nav เป็น Warm Paper
- `templates/index.html` — โครงใหม่ (P0+P1) + token ใหม่
- `database.py` — เพิ่ม `get_today_capture_count()`
- `main.py` — `index()` ส่ง `today_capture` เข้า template

## Acceptance / วิธีทดสอบ
1. `python -m py_compile main.py database.py` ผ่าน
2. รัน app → เปิด `/` → header strip โชว์ รอบ/Day/ถ่ายวันนี้ + ปุ่ม "เริ่มถ่าย" ลิงก์ `/scan`
3. ตั้ง Global Day → strip อัปเดตเลข Day ทันที (JS)
4. ใส่ภาพ mock วันนี้ 1 ขวด → reload → "ถ่ายวันนี้" ขึ้นเป็น 1/100
5. มือถือ (จอแคบ) → ทุก section stack, ปุ่มถ่ายกดถึงด้วยนิ้ว, stats grid-cols-2
6. desktop → operational + shelf เป็น 2 คอลัมน์

## ลำดับ implement (ตอนได้ไฟเขียว)
0. **(แนะนำ) static HTML mockup** — ทำหน้า dashboard เดี่ยวๆ ด้วย Warm Paper theme + mock data
   เปิดในเบราว์เซอร์ดู look ก่อน → ปรับจนพอใจ แล้วค่อย port เข้า template (de-risk ธีมก่อนแตะแอปจริง)
1. theme tokens + fonts ใน `base.html` (Warm Paper) — เช็คทุกหน้าไม่พัง
2. backend hook (`get_today_capture_count` + ส่งเข้า index) — ทดสอบ round-trip
3. P0.1 header strip + JS sync
4. P0.2 operational 2-col + P0.3 stats
5. P1 token/spacing/heatmap tooltip/empty-state
6. ทดสอบตาม acceptance → commit `feat: redesign dashboard (warm paper + workflow-first)`
