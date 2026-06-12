# 📋 ใบกรอก/ตัดสินใจ — VitroVision Methodology

> **ใบนี้คืออะไร:** รวม checkbox ทั้งหมดที่รอพีรดนย์เติมข้อมูล/ตัดสินใจ มาไว้ที่เดียว (เดิมกระจายอยู่หัว `10_methods_draft.md` §📌 TODO + do-now checklist เมื่อคืนที่อยู่ในแชตเฉยๆ ไม่เคยเซฟ)
> **วิธีใช้:** อ่าน "ผมแนะนำ" → กรอกในช่อง `→ ตอบ:` ได้เลย หรือบอกผมในแชต ผมจะ fold เข้า Methods v2 ให้
> สร้าง 2026-06-12 · sync กับ Research Design v1 (locked 2026-06-11)

---

## ✅ ส่วนที่ 1 — ล็อกแล้ว (ไว้ดูให้บริบทตรงกัน ไม่ต้องกรอก)

ตัดสินไปแล้ว ใช้เป็นกรอบได้เลย:

- **พืช/วัสดุ:** *Capsicum annuum* cv.'พริกจินดา', เมล็ดคีบจากผล (เกษตรกร อ.สตึก บุรีรัมย์), 1 เมล็ด/ขวด ขวดปิดผนึก
- **ฟอกเชื้อ:** whole-fruit Clorox 15%→10% ฟอก 2 รอบ, ไม่ใช้ GA₃
- **อาหาร:** MS full · Glucose 20 g/L · Kelcogel 3 g/L · pH 5.6–5.8 · PGR ก่อน autoclave · 121°C 15–20 min · ~30 mL/ขวด
- **5 สูตร:** A=MS, B=BAP1, C=BAP5, D=BAP5+NAA0.05, E=IBA1
- **Replication:** ≥2 batch → pool n≈40/สูตร · over-sow ~24-25 ขวด/สูตร/batch
- **นับวัน:** จากวัน "งอก (emergence)" ไม่ใช่วันหยอด · window 28 วัน
- **Layout:** เรียงสูตร aligned กับ row (ไม่ randomize) → คุม confound ด้วย position-as-covariate
- **Tracking:** ArUco DICT_4X4_100 ~3cm ติดก่อน inoculate (`aruco_stickers.pdf` พร้อมพิมพ์)
- **Validation:** expert ≥2 คน blind → consensus median = reference · Spearman ρ + quadratic-weighted κ + ICC(2,1)
- **Stats:** ขวด=หน่วยทดลอง · Gompertz growth curve/ขวด · KW/ART-ANOVA หรือ LMM เทียบสูตร · survival (KM+log-rank) สำหรับ contamination
- **Primary endpoint:** green_coverage_pct · Secondary: vigor, brown%, LCI, shoot_count
- **citation glucose:** Phillips & Hubstenberger 1985 (verified, DOI 10.1007/BF00040200 — แก้จาก "Collins" ที่ Consensus metadata ผิด) · **"Thomas 2026" = ผี ตัดทิ้งแล้ว**

---

## ✏️ ส่วนที่ 2 — รอพีรดนย์เติม (ค่าแล็บ — Group A)

### A1 · §1.7 สภาพห้องเพาะเลี้ยง — ✅ **ตอบแล้ว (2026-06-12): ค่าจริงตรง default**
- อุณหภูมิ → **25±2°C**
- photoperiod → **16/8 ชม. (light/dark)**
- หลอด + ความสว่าง → **LED ~40–50 µmol/m²/s**
- *(fold เข้า 10 §1.7 แล้ว)*

### A2 · §2.1 กล้อง/การถ่าย — ✅ **ตอบครบแล้ว (2026-06-12)**
  - รุ่นกล้อง/มือถือ → ✅ **Samsung Galaxy S24 FE** (main 50 MP ISOCELL GN3, f/1.8 OIS)
  - ความละเอียด → ✅ **12 MP** (binned, ล็อกตลอด)
  - ระยะถ่าย → ✅ **15–20 cm** เทสต์แล้วโฟกัสคม → ล็อกค่าเดียว (~18 cm) คงที่ทุกภาพ
  - **lightbox** → ✅ **ไม่ใช้** — ชดเชยด้วย: คุมแสงควบคุมเดียวกัน + Pro mode ล็อก WB/exposure + white card ในเฟรม (§2.1.1); เขียน limitation ตรงๆ
  - manual/auto → ⏳ เหลือยืนยัน **Pro mode lock** จริงตอนตั้ง rig: ______ (ค่าที่เหลือเป็น operational ไม่ block design)

### A3 · §3.2 ค่า HSV threshold (green/brown)
- **ผมแนะนำ:** ยังกรอกไม่ได้ตอนนี้ — ต้อง **ถ่ายภาพ calibration 5–10 รูปด้วย rig จริงก่อน** แล้วผม tune ค่าให้ตรงแสง (ค่าใน prototype อาจเพี้ยน)
  - → action: ถ่าย calibration set แล้วส่งให้ผม (ทำตอนตั้ง rig เสร็จ)

### A4 · §1.1 เวลาฟอก Clorox + §1.2 ชนิดขวด
- เวลาแช่ Clorox ต่อรอบ (กี่นาที) + มี Tween-20/EtOH dip ไหม → ตอบ: ______
- ชนิด/ขนาดขวดที่ใช้ → ตอบ: ______

---

## 🤔 ส่วนที่ 3 — รอพีรดนย์ตัดสินใจ (Group B)

### B1 · §2.2 เวลาถ่ายในแต่ละวัน — 🔶 **ตัดสินบางส่วน (2026-06-12)**
- **ตัดสิน:** ล็อกเวลาคงที่ทุกวัน ช่วงเย็นหลังเลิกเรียน (พีรดนย์เลือก "เวลาอื่น" ไม่ใช่ 9:00)
- ⏳ **เหลือ:** เวลาเป๊ะ (แนะนำ ~17:00) → ตอบ: ______

### B2 · §5.3 α + การ correct multiple comparison — ✅ **ตอบแล้ว (2026-06-12): hierarchical gatekeeping**
- α = **0.05** · **primary endpoint เดียว = green_coverage_pct** → 3 planned contrasts ใช้ **Bonferroni** (α/3 ≈ 0.017/คู่)
- **secondary** (vigor/brown/LCI/shoot) → **FDR (BH)** เป็น supportive · **contamination** → descriptive
- รายงาน **effect size + 95% CI** ทุกที่ · *(fold เข้า 10 §5.3 แล้ว)*

---

## 📝 ส่วนที่ 4 — Do-now checklist เมื่อคืน (ไม่เคยเซฟ — เก็บไว้ที่นี่)

- [ ] **Germination pre-test** — ทดสอบ % งอก/เวลางอกของ 'พริกจินดา' ก่อน เพื่อกะ over-sow buffer ให้แม่น → ตอบผล: ______
- [ ] **Imaging rig spec** — สรุปสเปกชุดถ่าย (กล่อง/ระยะ/แสง/พื้นหลัง) ให้ reproducible → ลิงก์กับ A2
- [🔶] **Expert assessment rubric** — อัปเกรดเป็น **2 axis** (developmental phase objective + vigor 1–5 holistic) + hyperhydric flag, มี citation ค้ำ (Myakisheva 2024/Ding 2025/Bock 2010/de Raadt 2021 — §4.1 v2) → **เหลือครู TC review เส้นแบ่ง grade 3/4 + ลองให้คะแนนจริงดู inter-rater** → sign-off: ______
- [x] **Hypotheses sign-off** — ✅ **SIGNED OFF พีรดนย์ 2026-06-12** — H1a/H1b/H2/H3/H4 ใน methods §6 (H₀/H₁ + threshold ตรง §4–§5) ยืนยันถ้อยคำแล้ว

---

## ⏳ ส่วนที่ 5 — รอเงื่อนไข (ไม่ต้องทำตอนนี้ แต่ track ไว้)

**Group C — ต้องมีของก่อนถึงทำได้:**
- [ ] §3.3 เทรนด้วยภาพจริง + 5-fold CV + แก้ healthy recall — *รอภาพจริงจาก lab*
- [ ] §4 inter-rater (ครู ≥2 คน blind) — *รอ validation set*
- [ ] §4.6 เก็บ survival ตอนอนุบาล — *วางแผน timeline ให้ทันก่อน ต.ค. 2026*

**Group D — งาน code (เฟส implement):**
- [x] §3.5 traits classical (Convex Hull/ExG/VARI/GLCM) — **เสร็จ 2026-06-12** (wire เข้า DB ครบ verify แล้ว)
- [ ] §3.6 hyperhydric binary flag — column `hyperhydricity` มีใน DB แล้ว เหลือต่อเข้า capture UI
- [ ] §2.4 label developmental stage ต่อภาพ (radicle/hypocotyl/cotyledon/true-leaf)
- [ ] §3.5 leaf count YOLOv8-seg — *รอ labeled data*
- [ ] §3.5 reference scale marker ในเฟรม — *physical (ตอนตั้ง rig)*
