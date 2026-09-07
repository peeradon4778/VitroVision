# 🎯 VitroVision — สถาปัตยกรรม & ทิศทางปัจจุบัน (Orchestration Tracker)

> อัปเดต 2026-09-01 · เขียนใหม่ให้ตรงสถานะจริง (ลบส่วนที่ pivot ไปแล้วออก)
> จุดหมาย: **YSC 2027** · รหัสโครงการ `29YCSE00054T` · สาขา **CSAI — Computer Science / AI-ML** · deadline ข้อเสนอ 10 ก.ย. 2026

---

## 🧭 ทิศทาง (Locked)

- **ชื่อ TH:** VitroVision : การประยุกต์ใช้ปัญญาประดิษฐ์เชิงคอมพิวเตอร์วิทัศน์เพื่อวิเคราะห์และทำนายการเจริญเติบโตของพืชเพาะเลี้ยงเนื้อเยื่อ
- **ชื่อ EN:** VitroVision : Application of AI-Based Computer Vision for Analyzing and Predicting the Growth of Tissue Cultured Plants
- **เป้าหมาย:** ประเมินฟีโนไทป์เชิงสรีระของพืชเพาะเลี้ยงเนื้อเยื่อแบบ **non-destructive ผ่านขวดแก้ว** โดยไม่จำกัดชนิดพืช → ช่วยตัดสินความพร้อมย้ายออกอนุบาล (acclimatization readiness)
- **Research Question:** ด้วยการประมวลผลภาพขวดเพียงภาพเดียว สามารถแบ่งส่วนต้นออกจากแก้ว/glare แล้วจัดกลุ่มความพร้อม (ยังไม่พร้อม / พร้อมอนุบาล / ตรวจเอง) ได้ถูกต้องเพียงพอหรือไม่ — แบบ decision-support ข้ามชนิดพืช โดยไม่ต้องฝึกชุดข้อมูลเฉพาะชนิด
- **หลักการ:** decision-support เท่านั้น ไม่ใช่ระบบตัดสินทางชีววิทยาขั้นสุดท้าย · มี "ตรวจเอง" เป็นทางออก (manual override เสมอ)

---

## 🏗️ สถาปัตยกรรมปัจจุบัน

```
ภาพขวด (สมาร์ตโฟน)
  → ตรวจจับขอบเขตขวด (bottle ROI)
  → แบ่งส่วนต้นออกจากแก้ว/glare/ไอน้ำ
       └─ แบบจำลองหลัก: U-Net + MobileNetV3-Small (~3.6M params) กลั่นจาก SAM3
          (SAM3 zero-shot = ต้นแบบ/teacher สร้าง pseudo-labels)
  → คำนวณค่าลักษณะ (feature) เชิงปริมาณ
  → ตัดสินใจด้วยกฎ (rule-based) → ยังไม่พร้อม / พร้อมอนุบาล / ตรวจเอง
```

### แบบจำลอง (Segmentation)
- **Main engine:** **U-Net + MobileNetV3-Small** (`src/train_greenhouse.py`, smp) — เทรนบนชุด greenhouse แล้ว · val_dice ≈ **0.98** · `src/train_unet_distill.py`
- **Teacher / ต้นแบบ:** **SAM3 PCS** (`facebook/sam3`) text-prompted (5 คำ: `plant`,`leaf`,`shoot`,`stem`,`root`) — ใช้ทำ pseudo-labels + เปรียบเทียบ baseline
- **ห้ามใช้** SAM automatic/everything mode (พิสูจน์แล้วว่าล้มเหลวกับกระจก/glare)
- **เหตุผลกลั่น:** SAM3 ต้อง GPU/ใหญ่ → กลั่นเป็น U-Net เล็กให้ทำงานบนอุปกรณ์ทั่วไป

### เกณฑ์ตัดสินใจ (rule-based, interpretable)
- SAM3 (ต้นแบบ): `height_proxy ≥ 0.275` → พร้อมอนุบาล
- U-Net (ใช้งานจริง): ปรับด้วย **Youden scan 0.12–0.55** → `height_proxy ≥ 0.20` → พร้อมอนุบาล
- ภาพประมวลผลไม่ชัด (glare/ฝ้า/ไม่พบขวด) → **ตรวจเอง** (ให้มนุษย์ตรวจ)

### การ deploy
- **HF Space Gradio** (`space/app.py`) — เว็บแอปสแกนขวดผ่านกล้อง/อัปโหลดภาพ
- โหลดโมเดล `<name>.pt` local → HF repo `peeradon4778/vitrovision-unet-small` (fallback classical-green ระหว่างรอ)

---

## 📐 นิยาม feature (หลัก)

| feature | นิยาม / สูตร |
|---|---|
| `coverage_ratio` | area(plant∪leaf masks) / area(ROI) |
| `height_proxy` | bbox_height(plant mask) / ROI_height |
| `leaf_count` | จำนวน instance "leaf" (conf ≥ 0.5) |
| `shoot_count` | จำนวน "plant"/"shoot" detections |
| `green_pct` | สัดส่วน pixel เขียว |
| `glare_score` / `condensation_score` | คุณภาพภาพ (ลด confidence เท่านั้น) |
| `verdict` / `confidence` | ผลตัดสิน + ความมั่นใจ |

> *ความหมายกลับทิศ: `coverage_ratio` สูง = แน่นขวด (ดีสำหรับ subculture แต่อาจแย่สำหรับอนุบาล) — ใช้แสดงข้อมูลได้ แต่ไม่ใช้ตัดสินใจโดยตรง*

---

## งานค้าง (อัปเดต — ดูรายละเอียดใน `docs/planning/_backlog.md`)
- [ ] อัปเดต HF Space เป็น Gradio + push โมเดลขึ้น `vitrovision-unet-small`
- [ ] ปิด Level A: annotate ground-truth masks ≥ 30 ภาพ → mIoU/Dice
- [ ] สอบเทียบหน่วยจริง px→cm (ทำได้บางส่วน)
- [ ] ทดสอบข้ามชนิดพืช
- [ ] ประกอบเอกสารส่ง YSC (ดู `docs/runbooks/YSC_SUBMISSION_TICKETS.md`)

## ⛔ กติกา
- ทุก claim วิชาการ verify ก่อนเข้าเอกสาร · prose ไทย, diagram EN · ไม่ commit/push โดยไม่สั่ง
