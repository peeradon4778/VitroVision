# 📥 VitroVision — Backlog & งานค้าง (living doc)

> **ใบนี้คืออะไร:** ที่เก็บงานค้าง/ไอเดีย/สิ่งที่ตั้งใจทำต่อ — ถาวร ไม่หายเมื่อจบเซสชัน
> **วิธีใช้:** จดอะไรก็โยนลง `📌 INBOX` ด้านล่างได้เลย (ไม่ต้องจัดระเบียบ) เดี๋ยว `/vitro` จะ triage ให้
> **`/vitro` อ่านไฟล์นี้ทุกครั้ง** แล้วบอก direction ว่าควรเคาะ/ทำอะไรต่อ
> สถานะ: 🔴 เร่ง · 🟡 ระหว่างต้นโต · 🟢 ภายหลัง · 💤 รอเคาะ(decision) · ✅ เสร็จ
> อัปเดตล่าสุด: 2026-06-21 (T2/T3/T5/T7/T15 ✅ implement แล้ว · R5D synthesize ✅ — Depetris 2025 + lag period เพิ่มใน R5_validation_stats)

---

## 🧭 DIRECTION ตอนนี้ (next move ที่แนะนำ)

> **deadline:** เอกสาร ~กลาง ก.ย. · ตัวโครงงาน ถึง ต.ค. · **batch 1 day 0 = 22 มิ.ย. 2026 · ตอนนี้ day 2 (24 มิ.ย.) · เก็บภาพ day 1 แล้ว 1 รอบ**

1. **ถัดไปทันที:** implement **T1 Bridge study** + ทักครู **T6** (≥2 rater, lead time นาน)
2. **ระหว่างต้นโต (ก.ค.):** T9 ArUco px→cm · T10 C3 camera gates · T13 validation_stats.py · T14 PWA manifest.json
3. **ก่อนส่ง เค้าโครง:** T22 sync `_narrative_spine.md` + `report_outline.md` §3.8 + T16–T18 ART/Gompertz/KM modules

✅ **เสร็จ 2026-06-21 (session นี้):**
- T2 GAP-1: `expert_scores` table + `add_expert_score()` + `get_expert_scores_by_image()` + routes POST/GET
- T3 GAP-4/5: `dev_stage` + `hyperhydricity` ใน scan.html FormData + ปุ่ม stage/HH ใน topbar
- T5 Glare mask: `_glare_mask()` + `specular_fraction` feature ใน phenotyper.py + DB migration
- T7 NGRDI/CIVE: `ngrdi_mean` + `cive_mean` ใน phenotyper.py + DB migration + update_image_phenotype
- T15 Cut glass: ลบ `/glass`, `/api/glass_stream`, `/api/glass_state`, `_glass_*` vars+fn ออกจาก main.py

---

## 📌 INBOX (จดเร็ว ยังไม่ triage — โยนอะไรลงตรงนี้ได้เลย)

*(ว่าง)*

---

## 🏛️ ARCHITECTURE REDESIGN (กำลังทำ — session 2026-06-20)

> **state เต็มอยู่ที่ `research/_architecture_redesign_session.md`** (grill decisions + research)
> grill ปิดแล้ว 10 decisions (Q1–Q10 lock, Q11 parked) · research 5 หัวข้อ ทำทีละ R ด้วย 5 sub-agents

- [x] **Grill session** — 10 decisions locked (CLI cut, Glass cut, Drive backup-only, Pro mode manual, ArUco scale-cm, API async classifier, SAM=seg/API=classify, classical=quant/API=qual)
- [x] **R1** Phenomics features → `R1_phenomics_feature_audit.md`
- [x] **R2** Segmentation lineup → `R2_segmentation_lineup.md`
- [x] **R3** Feature impact → `R3_feature_impact_engine_change.md`
- [x] **R4** WB/แสง (Physical+Algorithmic) — ✅ เสร็จ 2026-06-21 (5 sub-agents) → `R4_wb_lighting.md` + R4A–E
- [x] **R5** Validation stats (ปลด Q11) — ✅ เสร็จ 2026-06-21 (10 sub-files, 2 sessions) → `R5_validation_stats.md`
- [x] **Synthesize** R1–R5 → final architecture v2 + task breakdown ✅ เสร็จ 2026-06-21 → `_architecture_v2_final.md`
- [ ] ⚠️ **verify "Ranario 2025"+"Paci 2024" ใน PubMed** ก่อนใช้ (เสี่ยง hallucinate แบบ Thomas 2026)

---

## 🏗️ Architecture Polish (12 comments — 2026-06-19)

> ภาพรวม 7-layer ถูก map ครั้งแรก session 6 — พีรดนย์เขียน 12 comments ไว้สำหรับ polish แต่ละส่วน
> รอ session ถัดไปมาค่อยๆ implement ทีละ comment

- [ ] **Polish L0:** Physical setup — rig spec / white card position / ArUco placement guideline
- [x] **Polish L1:** scan.html — เพิ่ม dev_stage + hyperhydricity ใน auto-capture FormData (GAP-4/5) ✅ 2026-06-21
- [ ] **Polish L1:** C3 camera gates — Laplacian sharpness, glare, orientation, grid overlay
- [ ] **Polish L2:** Google Drive sync — verify drive_uploader.py ทำงานจริงกับ batch 1
- [ ] **Polish L3:** WB calibration — เปิด WB_CARD_CORNER หลังถ่าย white card จาก rig จริง
- [ ] **Polish L3:** HSV threshold — calibrate กับ rig จริงหลัง batch 1 day 0
- [ ] **Polish L4:** train.html label fix — "EfficientNet-B0" → "DINOv2-Small"
- [ ] **Polish L5:** pseudo_labeler.py — ทดสอบ run() จริงกับภาพ batch 1
- [x] **Polish L6:** GAP-1 expert_scores table + routes ✅ 2026-06-21
- [ ] **Polish L6:** GAP-2 survival field ใน bottles
- [ ] **Polish L7:** เขียน validation_stats.py (κ/ICC/ART-C calculators)
- [ ] **Polish L7:** sync _narrative_spine.md §3 + report_outline.md §3.8

---

## 🔴 ก่อน batch 1 (เร่ง — กระทบ 3 วันนี้)

- [x] **GAP-3 · sow_date + emergence_date** — DB + API + UI ✅ commit f502368
- [x] **white-card auto-tune** — `_white_balance_correct()` พร้อมแล้ว ปิดอยู่ (`WB_CARD_CORNER=None`) ✅ commit f502368
- [ ] **เทสต์ scanner + ArUco ที่ระยะ rig จริง (~18cm)** → อ่าน ID ออกไหม, clarity ≥75% ติดไหม, white card อยู่ในเฟรมพอ auto-tune
- [x] ตั้ง rig + Pro mode preset + ติด ArUco (`aruco_stickers.pdf`) — ✅ **ติด ArUco ครบทุกขวดแล้ว 2026-06-21**
- [ ] **เปิด WB_CARD_CORNER** หลังถ่าย calibration set แล้วส่งให้ดู (แก้ 1 บรรทัดใน `phenotyper.py`)

## 🟡 ระหว่างต้นโต (ก.ค. — ทำชิลๆ คู่ขนานกับถ่ายภาพ)

- [ ] **VLM integration (Gemini)** — `vision_analyzer.py` + `pseudo_labeler.py` (Gemini teacher) พร้อมแล้ว รอเพียง **`GOOGLE_API_KEY`** ใส่ใน `.env` แล้วรันได้เลย *(แก้ 2026-06-19: เดิมจดผิดว่า Groq/gsk_ — โค้ดจริงใช้ `google.genai` = Gemini)*

- [ ] **C3 · Camera optimization ใน `scan.html`** — research 5 agents ครบแล้ว พร้อม implement: torch auto-on, Laplacian sharpness gate (patch-based, threshold ~100–200), glare detection, color calibration matrix, grid overlay, orientation check, EXIF metadata — ดูแผนใน `research/camera_optimization_plan.md`

- [ ] **Web App Phase A** (low-hanging fruit) — เพิ่ม `manifest.json` → PWA installable; ลด free-text → dropdown/tap; เพิ่ม rate-of-change column ใน dashboard — evidence จาก 5 agents ใน `research/webapp_arch_proposal.md`

- [ ] **Web App Phase B** (ก.ค.) — Module nav (Capture/Analysis/Data/Reports); linked view timeline↔ภาพขวด; Flag button ใน scan.html ไม่ตัด flow

- [x] **GAP-1 · ตาราง `expert_scores`** (image_id, rater_id, vigor_grade 1–5, hyperhydric_flag, ts) รองรับ ≥2 rater + consensus median ✅ 2026-06-21
- [x] **GAP-4 · field `dev_stage`** ใน images — capture UI 1-tap ใน scan.html (ปุ่ม "ระยะ") ✅ 2026-06-21
- [x] **GAP-5 · เช็ค hyperhydric** — scan.html ส่ง `hyperhydricity` เข้า DB แล้ว (ปุ่ม HH) ✅ 2026-06-21
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
- [ ] ลบ paper ผี "Thomas 2026" — ✅ ลบแล้ว (2026-06-19) ไม่มีเหลือแล้ว

---

## ✅ เสร็จแล้ว (2026-06-19 session 6)
- **Gemini Auth key** ✅ — `.env` พร้อม, `vision_analyzer.py` อัปเดตเป็น `gemini-3.5-flash`
- **7-layer architecture map** ✅ — L0 Physical → L7 Analysis/Validation ครบทุก module, จด GAPs, pending polish 12 items
- **VLM research** ✅ — ทางเลือก Gemini/GPT-4o/Qwen/LLaVA พร้อม research backing (Ranario 2025, Paci 2024, Roumeliotis 2025)
- **เครื่อง spec** ✅ — 8GB RAM, AMD iGPU, CPU-only → local VLM ไม่เหมาะ → API เท่านั้น

## ✅ เสร็จแล้ว (2026-06-19 session 5)
- **ล็อก methodology §3** ใน `10_methods_draft.md` ให้ตรงสถาปัตย์จริง: SAM2 segmentation + 14 features (เดิมเขียน 7/HSV) + EfficientNet baseline + DINOv2 + **VLM (Gemini) teacher** (เดิมไม่พูดถึงเลยทั้งที่ชื่อโครงงานมี VLM) + กรอบ honest "เค้าโครง=วิธี ไม่ใช่ผล, ห้ามใส่ κ=0.6274"
- แก้ factual: config.py ARUCO_DICT 4X4_50→4X4_100 (dead code) · memory trainer=DINOv2 (จริง: 2 trainer, ตัวเว็บยัง EfficientNet) · VLM=Gemini ไม่ใช่ Groq
- **follow-up (ค้าง):** sync `_narrative_spine.md` org3 + `report_outline.md` §3.8 ให้ตรง §3 ใหม่ (ยังอ้าง EfficientNet/12-feat ไม่มี SAM2/VLM)

## ✅ เสร็จแล้ว (2026-06-17 session)
- ปิด decision Q1–Q6 (batch1=20มิ.ย., batch2=deployment, rubric, Q4 auto-tune, Q5 capture-time, Q6 flag)
- สร้าง `report_outline.md`, `appendix_rubric_onepager.md`, `expert_scoring_sheet.csv`
- แก้ memory κ=0.6274 = smoke-test (ไม่ใช่ผลจริง) + เก็บ memory ปรัชญา 2 เฟส
- rewrite `/vitro` ให้ครอบทั้งงาน + อ่านไฟล์ก่อนตอบ
