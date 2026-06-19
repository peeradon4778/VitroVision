# 📥 VitroVision — Backlog & งานค้าง (living doc)

> **ใบนี้คืออะไร:** ที่เก็บงานค้าง/ไอเดีย/สิ่งที่ตั้งใจทำต่อ — ถาวร ไม่หายเมื่อจบเซสชัน
> **วิธีใช้:** จดอะไรก็โยนลง `📌 INBOX` ด้านล่างได้เลย (ไม่ต้องจัดระเบียบ) เดี๋ยว `/vitro` จะ triage ให้
> **`/vitro` อ่านไฟล์นี้ทุกครั้ง** แล้วบอก direction ว่าควรเคาะ/ทำอะไรต่อ
> สถานะ: 🔴 เร่ง · 🟡 ระหว่างต้นโต · 🟢 ภายหลัง · 💤 รอเคาะ(decision) · ✅ เสร็จ
> อัปเดตล่าสุด: 2026-06-19 (session 3 — triage VLM INBOX, ก่อน batch 1)

---

## 🧭 DIRECTION ตอนนี้ (next move ที่แนะนำ)

> **deadline:** เอกสาร ~กลาง ก.ย. · ตัวโครงงาน ถึง ต.ค. · **batch 1 หยอด 20 มิ.ย. (อีก 3 วัน)**

1. **เร่งสุด (ก่อน 20 มิ.ย.):** GAP-3 (sow/emergence date) + white-card auto-tune + เทสต์ scanner/ArUco ที่ระยะ rig จริง
2. **ปลดล็อก claim หลัก:** GAP-1 (`expert_scores` table) — ต้องมีก่อนครูให้คะแนน (ส.ค.)
3. **เขียนคู่ขนาน (ก.ค.):** บท 1–3 ของรูปเล่ม (ไม่ต้องรอ data)

---

## 📌 INBOX (จดเร็ว ยังไม่ triage — โยนอะไรลงตรงนี้ได้เลย)

*(ว่าง)*

---

## 🔴 ก่อน batch 1 (เร่ง — กระทบ 3 วันนี้)

- [x] **GAP-3 · sow_date + emergence_date** — DB + API + UI ✅ commit f502368
- [x] **white-card auto-tune** — `_white_balance_correct()` พร้อมแล้ว ปิดอยู่ (`WB_CARD_CORNER=None`) ✅ commit f502368
- [ ] **เทสต์ scanner + ArUco ที่ระยะ rig จริง (~18cm)** → อ่าน ID ออกไหม, clarity ≥75% ติดไหม, white card อยู่ในเฟรมพอ auto-tune
- [ ] ตั้ง rig + Pro mode preset + ติด ArUco (`aruco_stickers.pdf`)
- [ ] **เปิด WB_CARD_CORNER** หลังถ่าย calibration set แล้วส่งให้ดู (แก้ 1 บรรทัดใน `phenotyper.py`)

## 🟡 ระหว่างต้นโต (ก.ค. — ทำชิลๆ คู่ขนานกับถ่ายภาพ)

- [ ] **VLM integration (Groq)** — `vision_analyzer.py` + `/api/analyze_vision` พร้อมแล้ว รอเพียง Groq API key (`gsk_...`) จาก console.groq.com ใส่ใน `.env` เป็น `GROQ_API_KEY=` แล้ว wire เข้าระบบได้เลย

- [ ] **GAP-1 · ตาราง `expert_scores`** (image_id, rater_id, vigor_grade 1–5, hyperhydric_flag, ts) รองรับ ≥2 rater + consensus median — *ปลดล็อก validation = พระเอกเอกสาร*
- [ ] **GAP-4 · field `dev_stage`** ใน images (radicle/hypocotyl/cotyledon/true_leaf) + capture UI 1-tap (Task #4) (decision Q5)
- [ ] **GAP-5 · เช็ค hyperhydric** — scanner ส่งค่า `hyperhydricity` เข้า DB จริงไหม ถ้ายัง เพิ่ม checkbox (decision Q6)
- [ ] **เขียนรูปเล่ม บท 1–3** จาก research docs (ดู `report_outline.md`) — *60% ของเล่ม ทำได้เลย*
- [ ] **Task #1 · ทักครู ≥2 คน** เป็น rater (lead time นาน ทักเนิ่นๆ)
- [ ] สคริปต์คำนวณ inter-rater (κ + ICC) เขียนรอ (Task #3)

## 🟢 ภายหลัง (ส.ค.–ต.ค.)

- [ ] **GAP-2 · field survival** (`acclim_survival/date/check_date`) ใน bottles (criterion validity ตัวที่ 4) — ใช้ตอนย้ายอนุบาล
- [ ] pilot ครู + เคาะเส้น grade 3/4 + lock rubric (Task #2)
- [ ] main blind scoring + validation stats (Task #3)
- [ ] train model ด้วยภาพจริง batch 1
- [ ] survival batch 1 subset ~30–40 ต้น (วัดรอดวันที่ 21)
- [ ] เทียบ 5 สูตร + reproducibility + เขียนบท 4
- [ ] บท 5 + บทคัดย่อ
- [ ] 🟠 GAP-6 contamination onset (เสริม priority ต่ำ)

## 💤 รอเคาะ (decision ค้าง — ดู `_decisions_pending.md`)

- [ ] A3 · HSV threshold (เขียว/น้ำตาล) — รอภาพ calibration จาก rig จริง
- [ ] A2 · ยืนยัน Pro mode lock ตอนตั้ง rig
- [ ] รูปเล่มกลาง ก.ย. = final หรือ draft อัปเดตได้? (ชี้ว่าต้องเร่งครูแค่ไหน) ← **ยังไม่ตอบ**

## 🚨 ก่อน final ห้ามลืม (audit landmines)

- [ ] n ให้ตรงทุกที่ (05=181 vs 10=28) → ยึด `models/metrics.json`
- [ ] แยก κ vigor-rubric ≠ κ classifier-3class ทุกที่
- [ ] ลบ paper ผี "Thomas 2026" (เหลือ note ใน `08_survival_contamination.md`)

---

## ✅ เสร็จแล้ว (2026-06-17 session)
- ปิด decision Q1–Q6 (batch1=20มิ.ย., batch2=deployment, rubric, Q4 auto-tune, Q5 capture-time, Q6 flag)
- สร้าง `report_outline.md`, `appendix_rubric_onepager.md`, `expert_scoring_sheet.csv`
- แก้ memory κ=0.6274 = smoke-test (ไม่ใช่ผลจริง) + เก็บ memory ปรัชญา 2 เฟส
- rewrite `/vitro` ให้ครอบทั้งงาน + อ่านไฟล์ก่อนตอบ
