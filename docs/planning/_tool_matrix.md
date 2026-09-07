# 🧪 VitroVision — Tool Evaluation Matrix (ทดสอบหลายเครื่องมือ + customize + benchmark)

> สร้าง: 2026-08-24 · สถานะ: วางแผน (ยังไม่มีผลรัน) — living doc อัปเดตเมื่อมีผลจริง
> เป้าหมาย: ทดสอบ segmentation tools หลายตัวกับพืชเพาะเลี้ยงเนื้อเยื่อ (TC) → customize ให้เหมาะกับ TC → เทียบ benchmark (ความเร็ว + ความแม่นยำ) → เลือกวิธีที่ดีที่สุด หรือพัฒนา model ของตัวเอง

---

## 1. เป้าหมาย

1. หา segmentation tool ที่แม่น + เร็วที่สุดสำหรับภาพ TC ผ่านขวดแก้ว (glare/ไอน้ำ/วุ้น/ราก)
2. Customize (prompt engineering / fine-tune / tuning) ให้ tool นั้นทำงานกับ TC ได้ดีเป็นพิเศษ
3. ได้ benchmark ตัวเลขจริง (mIoU/Dice/F1 + runtime) เป็นหลักฐานในเอกสาร
4. ถ้า customize แล้วยังไม่พอ → พัฒนา model เอง (ของใหม่ = contribution ตัวจริง)

---

## 2. Tools ภายใต้การทดสอบ (Matrix)

### 2.1 Zero-shot / Foundation (ไม่ต้องเทรน)

| # | Tool | วิธีใช้กับงานเรา | ข้อดี | ข้อจำกัด | GPU? | สถานะ |
|---|---|---|---|---|---|---|
| T1 | **SAM3 PCS** (facebook/sam3) | text prompt 5 คำ (plant/leaf/shoot/stem/root) + bottle ROI | เปิดคำศัพท์ + แม่นข้ามโครงสร้าง (Orvati Nia 2026) | gated, ช้า, ต้อง GPU | ต้อง | ✅ มี script |
| T2 | **SAM2** (sam2.1) | automatic mask → เลือก mask ใหญ่สุด | เร็ว/เบากว่า SAM3 | ไม่มี text prompt โดยตรง | แนะนำ | ✅ มี script |
| T3 | **SAM1** (segment-anything) | automatic mask | baseline ตระกูลเดิม | เก่าที่สุด | แนะนำ | ⬜ เพิ่ม |
| T4 | **MobileSAM** | automatic mask | เบา/เร็ว (edge) | ความแม่นยำต่ำกว่า | CPU ได้ | ⬜ เพิ่ม |
| T5 | **FastSAM** | automatic mask | **เร็วมาก** (YOLOv8-based) | คุณภาพ mask หยาบ | CPU ได้ | ⬜ เพิ่ม |
| T6 | **Grounding DINO + SAM** | text prompt "plant" → box → SAM mask | เปิดคำศัพท์แบบ text prompt (เทียบ SAM3 ได้) | 2 ขั้นตอน ช้า | แนะนำ | ⬜ เพิ่ม |
| T7 | **Segment Any Plant (SAP)** | few-shot plant seg (bioRxiv 2026) | เฉพาะพืชโดยตรง, mIoU 0.89–0.93 (งานต้นทาง) | few-shot ต้อง anchor image | แนะนำ | ⬜ เพิ่ม |

### 2.2 Supervised / Fine-tune (ต้องเทรน — ใช้ชุดของเรา)

| # | Tool | วิธีใช้ | ข้อดี | ข้อจำกัด | สถานะ |
|---|---|---|---|---|---|
| T8 | **YOLO-seg** (ultralytics) | fine-tune บน 50 ขวด (train) → test 50 | เร็วมาก, instance seg | COCO pretrained ใช้ตรงไม่ได้ (ไม่มี class plant) | ✅ script + ⬜ เทรน |
| T9 | **U-Net** (เทรนเอง) | binary seg plant/root | ควบคุมได้เต็มที่, เบา, CPU เร็ว | ต้อง dataset + annotation เยอะ | ⬜ |
| T10 | **DeepLab/SegFormer** | เทรนเอง | modern arch | เทรนนาน | ⬜ |

### 2.3 Classical (baseline ไม่ใช้ ML)

| # | Tool | วิธีใช้ | ข้อดี | ข้อจำกัด | สถานะ |
|---|---|---|---|---|---|
| T11 | **HSV green threshold** | color seg + morphology | ไม่ต้อง train, CPU เร็วสุด | พลาดต้นไม่เขียว/ราก, จับ glare | ✅ มี script |

---

## 3. ตัวแปรทดสอบ (Dimensions)

1. **โหมด:** zero-shot (T1–T7, T11) · supervised (T8–T10)
2. **Prompt variants** (เฉพาะ text-prompt tool): plant / plant+leaf / 5 คำ / +"seedling" / +"root" — ทดสอบ prompt sensitivity (อ้าง Dubois et al. 2026)
3. **ภาพขนาด:** 1024 px (หลัก) / 2048 px (ความละเอียดสูง — ช้าลง)
4. **ROI:** ใช้ bottle ROI vs ทั้งภาพ (ดูผลของ coverage)

---

## 4. เมตริก (ต่อ tool)

| กลุ่ม | เมตริก | หมายเหตุ |
|---|---|---|
| ความแม่นยำ | mIoU · Dice · Precision · Recall · F1 | เทียบ GT masks (ระดับพิกเซล) |
| งานตัดสินใจ | accuracy/confusion matrix ของ verdict (3 กลุ่ม) | เมื่อมี GT verdict |
| ความเร็ว | runtime/ภาพ (GPU + CPU ถ้าทำได้) | 100 ขวด/15 นาที = 9s/ภาพ (SAM3) เป็นจุดอ้างอิง |
| ต้นทุน | ค่า API/GPU, หน่วยความจำ, การติดตั้ง | สำหรับ decision-support low-cost |

---

## 5. เกณฑ์ตัดสินใจ (Decision Criteria)

**เรียงลำดับ — ใช้ข้อแรกที่ผ่าน:**

1. **Zero-shot ชนะ:** ถ้า tool zero-shot ตัวใดได้ mIoU ≥ **0.65** (ตามสมมติฐาน H₁) + runtime ≤ SAM3 → ใช้ตัวนั้นเป็น main engine (น่าจะ SAM3/Grounding-DINO)
2. **Fine-tune ชนะ:** ถ้า zero-shot ไม่ถึง 0.65 → fine-tune YOLO-seg/U-Net บนชุดเรา แล้วเทียบใหม่
3. **พัฒนาเอง:** ถ้า fine-tune แล้วยัง < 0.65 หรือ verdict accuracy < 70% → พัฒนา model ใหม่ (distill จาก SAM3 / เทรน U-Net+attention) — ของใหม่สำหรับกรรมการ
4. **root kill criterion (grill v3):** spike root ผ่าน (≥50% เจอ + conf ใกล้เคียง) → root ใน verdict/matrix · ไม่ผ่าน → ตัด root ออกจากโจทย์ + pivot (hyperhydricity/ยอด-ใบ)

**หมายเหตุ:** ความเร็วต้องสมดุลกับความแม่นยำ — เกณฑ์ "ดีที่สุด" = mIoU สูงสุดที่ runtime พอรับได้ (เป้า: ≤ 5s/ภาพ GPU หรือ ≤ 30s CPU)

---

## 6. แผนการทดลอง (Protocol)

1. **ชุดข้อมูล:** 100 ขวดพริกจินดา (มี) · GT masks ≥ 30 ขวด (annotate — กำลังทำ) · train/test split 50/50 (สำหรับ T8–T10)
2. **ลำดับ:**
   - [ ] Spike root (T1 prompt root) — ก่อนทุกอย่าง (kill criterion)
   - [ ] รัน zero-shot เต็มชุด (T1–T7, T11) บน Colab → ตาราง mIoU/Dice/F1/runtime
   - [ ] Prompt sensitivity (T1, T6)
   - [ ] Fine-tune YOLO-seg (T8) → เทียบ zero-shot vs supervised
   - [ ] ตัดสินใจตามเกณฑ์ข้อ 5
3. **เครื่อง:** Colab T4 (GPU) · เครื่อง local (CPU — สำหรับ T4/T5/T8/T11 ที่ CPU ได้)

---

## 7. งานค้าง (Checklist)

- [ ] spike test root (`src/root_spike_test.py` — รอรัน Colab)
- [ ] annotate GT masks ≥ 30 ขวด (`docs/DATA_TEMPLATES.md` §3)
- [ ] ขยาย `benchmark_colab.py`: เพิ่ม T3/T4/T5/T6 (SAM1/MobileSAM/FastSAM/Grounding DINO)
- [ ] ขยาย `benchmark_colab.py`: เพิ่ม T7 (SAP) เมื่อเข้าถึงได้
- [ ] รัน zero-shot เต็มชุดบน Colab → กรอกผลในตาราง §2 + §5
- [ ] fine-tune YOLO-seg (T8) + U-Net (T9)
- [ ] สรุปผลลงเอกสาร (proposal/report) + ตัดสินใจ main engine

---

## 8. บันทึกผลจริง (เติมเมื่อรัน)

| วันที่ | Tool | mIoU | Dice | F1 | runtime/ภาพ | หมายเหตุ |
|---|---|---|---|---|---|---|
| (รอ) | SAM3 | — | — | — | ~9s (1024px, T4) | อ้างอิงเริ่มต้น |
| (รอ) | SAM2 | — | — | — | — | |
| (รอ) | FastSAM | — | — | — | — | |
| (รอ) | Grounding DINO | — | — | — | — | |
| (รอ) | YOLO-seg (fine-tune) | — | — | — | — | |
| (รอ) | Classical HSV | — | — | — | 0.44s (CPU) | เร็วแต่พลาดมาก |
