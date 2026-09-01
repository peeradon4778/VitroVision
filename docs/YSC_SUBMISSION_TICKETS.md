# 🎫 Tickets: เตรียมส่ง YSC 2027 (VitroVision) — งานค้างที่ต้องปิดก่อน/หลังส่ง

> อัปเดต 2026-08-27 · สร้างจากรอบตรวจสถานะ (ชื่อใหม่ + ปรับเนื้อหา commit `03b8604` แล้ว)
> เป้าหมาย: ไล่งานให้ครบเพื่อส่งข้อเสนอ YSC 2027 (สาขา CSAI) ตาม `docs/SIMS_SUBMISSION_GUIDE.md` โดยไม่ทิ้งจุดที่กรรมการอาจจับ
> วิธีอ่าน: `[!!]` = บล็อก/ต้องทำก่อนส่ง · `[ ]` = ยังไม่ทำ · `[x]` = เสร็จแล้ว · `[OPEN]` = รอข้อมูล/ต้องแก้

---

## 🚦 สถานะรวม (ณ 2026-08-27)

- ✅ เปลี่ยนชื่อโครงงาน (TH/EN) ใหม่ — commit `03b8604`
- ✅ Calibration หน่วย px→cm + MAE/RMSE (height) — commit `f1961ae`, `c2b6268`
- ✅ Benchmark trait-level (SAM3 r=0.638) — commit `fbc8a13`, `49cc32d`
- ✅ Annotation tool + 30 ภาพ stratified — commit `121ab48`
- ✅ Validation tools (mIoU/Dice, inter-rater) — commit `02c927d`
- ⚠️ ยังต้องทำให้เสร็จก่อนส่ง ดู ticket ด้านล่าง

---

## 🎟️ A. เอกสาร/ชื่อ (ต้องตรงกันทุกจุดก่อนส่ง)

- [x] เปลี่ยนชื่อโครงงาน TH/EN ทุกจุดใน `docs/*.md` + `research/_orchestration.md` → `03b8604`
- [!!] **Rebuild docx จาก md ใหม่** — `docs/proposal_th_submit.docx`, `docs/report_th_v1.docx`, `docs/ysc_proposal_filled.docx` สร้างไว้ 24–26 ส.ค. (ก่อนเปลี่ยนชื่อ) → **ยังมีชื่อเก่า + เนื้อหาเก่า** ต้องรัน `make_*_docx.py` / `build_ysc_proposal.py` ใหม่
  - ไฟล์ที่ต้องอัปเดต: `proposal_th_draft.docx`, `report_th_v1.docx`, `ysc_proposal_filled.docx`
- [ ] ตรวจว่า `PROJECT_OVERVIEW.md` / `README.md` (หัวข้อ) ไม่มีชื่อ/ถ้อยคำที่ขัดกับชื่อใหม่ (README ยังเป็นแนวคิด v2 เก่า — อาจไม่ใช่ deliverable)
- [ ] ตรวจ citation กับ `research/citation_gate.md` / `citations_new_20260817.md` (ดึงอ้างอิง ≤5 ปีที่ verify แล้ว)

## 🎟️ B. Framing: ชื่อใหม่ ↔ ผลที่ validate (สำคัญต่อกรรมการ)

- [!!] **ปิดช่องว่าง "วิเคราะห์และทำนายการเจริญเติบโต" (ชื่อใหม่) vs "คัดกรองความพร้อมอนุบาล" (ผล pilot จริง)**
  - ผล pilot ที่ validate = จัดกลุ่มความพร้อม (height height_proxy ≥ 0.275 → acc 0.755 / sens 0.917)
  - ชื่อใหม่ไปทาง "ทำนายการเจริญ" → ต้องเชื่อมทั้งเนื้อเรื่อง (บทคัดย่อ/RQ/วัตถุประสงค์) ไม่ให้ดู "สัญญาเกินจริง"
  - ฐานที่ช่วยได้: calibration px→cm + time-series (ถ่าย 3 วัน) → พอจะพูด "ทำนาย" ได้ แต่ต้องมีผล/แผนชัดเจน
- [ ] ยืนยันว่า "ทำนาย" หมายถึงอะไรในขอบเขตนี้ (growth curve / forecast วันพร้อม) — ไม่ควรเกินงานจริง
- [ ] เช็คว่า `docs/report_th_v1.md` / `PROJECT_FULL_REPORT.md` (ที่ agent อีกตัวแก้ วัตถุประสงค์/สมมติฐานใหม่) สอดคล้องกับชื่อใหม่หรือยัง

## 🎟️ C. แบบฟอร์ม YSC (ดู `docs/YSC_FORMS_CHECKLIST.md`)

- [!!] **Form 6 — Research Continuation** (สำคัญสุด: ต่อยอด v1 + เคยส่งเวทีอื่น) — เจาะลึก v1 vs v2
- [!!] **Form 3 — Risk Assessment** (งานแล็บ + สารเคมี media/ฮอร์โมน)
- [ ] Code of Conduct / PDPA (ทุกคนในทีม)
- [ ] 1A — Student Checklist · 1B — Approval Form (นักเรียน+ผู้ปกครอง+SRC) · Adult Sponsor Checklist
- [ ] (รอบชิง) 2A — Student Support Disclosure / Gen-AI disclosure · 2C — Regulated Research Institution (ถ้าทำใน ม.)

## 🎟️ D. SIMS (ต้องทำในระบบเท่านั้น)

- [!!] **หน้าปก + รหัสโครงการจาก SIMS** — สร้างจากระบบเท่านั้น (ห้ามทำเอง) → `docs/SIMS_SUBMISSION_GUIDE.md`
- [ ] เลือกสาขา **CSAI** ให้ถูกตั้งแต่วันลงทะเบียน (เปลี่ยนทีหลังไม่ได้)
- [ ] กรอกข้อมูลจริง: สมาชิกทีม, อาจารย์ที่ปรึกษา
- [ ] **ส่วน 14 ประวัติย่อ** ในข้อเสนอ — ตอนนี้ว่าง (`___`) — ต้องกรอกจริงก่อนส่ง
  - หมายเหตุ: ตอนนี้ทำคนเดียว (อนาคตจะ 2 คน) — เตรียมรูปแบบทีมเมื่อมีสมาชิก

## 🎟️ E. หลักฐาน/ความซื่อตรง

- [ ] `MODEL_READINESS_TICKETS.md` — ยังระบุว่า "ยังไม่ใช่โมเดลเรา" (ต้องทำ G2/G3) — ตรวจว่าการ framing ใน proposal ไม่ขัดกับจุดนี้
- [ ] เก็บ `ground_truth_masks` (≥30 ภาพ) เพื่อปิด Level A (mIoU/Dice) — ต้องใช้ annotation tool ที่ agent อีกตัวทำ
- [ ] ตัดสินใจว่าจะบรรจุ "baseline mIoU/Dice ยังเป็น [PLAN]" ไว้ในข้อเสนอ (ซื่อตรง) หรือเก็บผลก่อนส่ง

---

> 📌 แหล่งอ้างอิง: `docs/DEV_LOG.md` · `docs/YSC_FORMS_CHECKLIST.md` · `docs/SIMS_SUBMISSION_GUIDE.md` · `docs/MODEL_READINESS_TICKETS.md`
> งานใน 4 หัวข้อ (calibration/baseline/annotation/validation) ที่ agent อีกตัวผลักไปแล้ว ให้ยึดผลจาก commit เป็นหลักเมื่อนำไปเขียนเอกสาร
