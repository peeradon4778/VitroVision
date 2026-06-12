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
- **citation glucose:** Phillips & Collins 1985 (verified) · **"Thomas 2026" = ผี ตัดทิ้งแล้ว**

---

## ✏️ ส่วนที่ 2 — รอพีรดนย์เติม (ค่าแล็บ — Group A)

### A1 · §1.7 สภาพห้องเพาะเลี้ยง
- **ผมแนะนำ (มาตรฐานทั่วไป):** อุณหภูมิ 25±2°C · photoperiod 16/8 ชม. · แสง LED ~40–50 µmol/m²/s
- กรอกค่าจริงห้องที่ใช้:
  - อุณหภูมิ → ตอบ: ______
  - photoperiod (เปิดไฟกี่ชม./วัน) → ตอบ: ______
  - ชนิดหลอด (LED/fluorescent) + ความสว่าง (µmol หรือ lux) → ตอบ: ______

### A2 · §2.1 กล้อง/การถ่าย
- **ผมแนะนำ:** มือถือถ่าย manual mode ล็อก exposure+WB, ความละเอียด ≥1920px, ระยะคงที่ ~25–30 cm, มี lightbox + แผ่นขาวอ้างอิงในเฟรม
  - รุ่นกล้อง/มือถือ → ตอบ: ______
  - ระยะถ่าย (cm) → ตอบ: ______
  - ตั้ง manual หรือ auto exposure/WB → ตอบ: ______

### A3 · §3.2 ค่า HSV threshold (green/brown)
- **ผมแนะนำ:** ยังกรอกไม่ได้ตอนนี้ — ต้อง **ถ่ายภาพ calibration 5–10 รูปด้วย rig จริงก่อน** แล้วผม tune ค่าให้ตรงแสง (ค่าใน prototype อาจเพี้ยน)
  - → action: ถ่าย calibration set แล้วส่งให้ผม (ทำตอนตั้ง rig เสร็จ)

### A4 · §1.1 เวลาฟอก Clorox + §1.2 ชนิดขวด
- เวลาแช่ Clorox ต่อรอบ (กี่นาที) + มี Tween-20/EtOH dip ไหม → ตอบ: ______
- ชนิด/ขนาดขวดที่ใช้ → ตอบ: ______

---

## 🤔 ส่วนที่ 3 — รอพีรดนย์ตัดสินใจ (Group B)

### B1 · §2.2 เวลาถ่ายในแต่ละวัน
- **ผมแนะนำ:** ล็อกเวลาเดิมทุกวัน เช่น **9:00 น.** (กัน diurnal effect จากไฟตู้เปิด-ปิด)
- → ตอบ: ______

### B2 · §5.3 α + การ correct multiple comparison
- **ผมแนะนำ:** α = **0.05** · primary+secondary endpoint ใช้ **Bonferroni** (conservative, กรรมการเจาะยาก) · เก็บ FDR ไว้เฉพาะ exploratory (contamination)
- → ตอบ: ______

---

## 📝 ส่วนที่ 4 — Do-now checklist เมื่อคืน (ไม่เคยเซฟ — เก็บไว้ที่นี่)

- [ ] **Germination pre-test** — ทดสอบ % งอก/เวลางอกของ 'พริกจินดา' ก่อน เพื่อกะ over-sow buffer ให้แม่น → ตอบผล: ______
- [ ] **Imaging rig spec** — สรุปสเปกชุดถ่าย (กล่อง/ระยะ/แสง/พื้นหลัง) ให้ reproducible → ลิงก์กับ A2
- [ ] **Expert vigor rubric 1–5** — มี draft ใน methods §4.1 แล้ว (5 ระดับ anchor) → **พีรดนย์ + ครู review ว่าใช้ได้ไหม** → sign-off: ______
- [ ] **Hypotheses sign-off** — มี draft ใน methods §6 (validation/biological/reproducibility/contamination) → ยืนยันถ้อยคำ → sign-off: ______

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
