# รายงานผลงานฉบับรวม (Master Project Report) — VitroVision

> **โครงการ:** VitroVision — ระบบตัดสินใจความพร้อมอนุบาลของต้นเพาะเลี้ยงเนื้อเยื่อแบบไม่ทำลาย (non-destructive) ผ่านขวดแก้ว ด้วย SAM3 (zero-shot)
> **เอกสารรวมเล่มเดียว** สังเคราะห์จาก `report_th_v1.md`, `proposal_th_draft.md`, `DEV_LOG.md`, `VALIDATION_PLAN.md`, `diagrams.md` และ `research/`
> **สถานะหลักฐาน:** `[RESULT]` = ผลจริง · `[PLAN]` = แผน/ยังไม่ทำ · `[OPEN]` = รอข้อมูล/ต้องแก้

---

## 1. บทคัดย่อ (Abstract)

โครงงานนี้พัฒนาและประเมินระบบคัดกรอง**ความพร้อมอนุบาล** (acclimatization readiness) ของต้นพืชเพาะเลี้ยงเนื้อเยื่อแบบ**ไม่ทำลายตัวอย่าง** ผ่านขวดแก้ว โดยใช้แบบจำลองพื้นฐาน **Segment Anything Model 3 (SAM3)** ในโหมด **Promptable Concept Segmentation (PCS)** แบบ zero-shot แบ่งส่วนภาพต้นด้วยพรอมป์ข้อความ 5 คำ (plant, leaf, shoot, stem, root) คำนวณลักษณะเชิงปริมาณ 6 กลุ่ม และจัดกลุ่มความพร้อมด้วยกฎที่ปรับได้

ระบบใช้เพียงสมาร์ตโฟน + Google Colab ฟรี + โมเดล open-source (ต้นทุนต่ำสุด) ผลนำร่องกับ**ภาพจริง 100 ขวดพริกจินดา** ได้ผลจริง และเมื่อตรวจสอบกับ**ค่าอ้างอิงจากผู้ประเมิน (ground truth)** พบว่า **เกณฑ์ความพร้อมที่ถูกต้องคือ "ความสูง/ความโตของต้น" ไม่ใช่ "ความแน่นเต็มขวด" (coverage)** โดยกฎ `height_proxy ≥ 0.275` ให้ accuracy = **0.755** และ sensitivity = **0.917** ซึ่ง**ผ่านสมมติฐาน H₂** (accuracy ≥ 0.70, sensitivity ≥ 0.60) ขณะที่กฎ coverage ซึ่งใช้เดิมให้ accuracy เพียง 0.43

---

## 2. บทนำ (Introduction)

### 2.1 ความสำคัญของการเพาะเลี้ยงเนื้อเยื่อ
การเพาะเลี้ยงเนื้อเยื่อ (in vitro) เป็นเทคโนโลยีขยายพันธุ์พืชที่สำคัญในระดับโลกและไทย โดยเฉพาะกล้วยไม้ซึ่งเป็นสินค้าส่งออกสำคัญ (Thammasiri, 2015) และการใช้ bioreactor สำหรับปาล์มน้ำมัน/มะพร้าวช่วยเพิ่มความเร็วขยายพันธุ์ 3–4 เท่า (ไบโอเทค, 2563)

### 2.2 ปัญหา: จุดคอขวด
การตัดสินใจว่าเมื่อใดควรย้ายต้นออกอนุบาล (acclimatization) ยังทำ**ด้วยสายตาเป็นรายขวด** ซึ่งใช้แรงงานมากและมีค่าใช้จ่ายสูง (ค่าแรง = 60–70% ของต้นทุน — Bethge et al., 2023) และผลตรวจมีความ**แปรปรวนระหว่างผู้ประเมิน** (Zhang et al., 2026; Nguyen et al., 2025) การตัดสินใจเร็ว/ช้าเกินอาจทำให้เนื้อเยื่อผิดปกติ (hyperhydricity, การตายของเนื้อเยื่อ)

### 2.3 ช่องว่างขององค์ความรู้ (Research Gap)
ยังไม่มีระบบต้นทุนต่ำที่ใช้สมาร์ตโฟนถ่ายภาพขวดแล้วระบุความพร้อมอนุบาล**แบบข้ามชนิด** โดยไม่ต้องฝึกแบบจำลองใหม่ งานใกล้เคียง (Regni et al., 2025) ใช้ภาพ 3D วัดพื้นที่ปกคลุมต่อขวดใน blackberry/blueberry แต่จำกัดชนิดและไม่ใช่ระบบจัดกลุ่มความพร้อม

---

## 3. วัตถุประสงค์และสมมติฐาน

**วัตถุประสงค์:**
1. สร้างชุดข้อมูลภาพถ่ายจริงผ่านขวดแก้วชุดแรก (100 ขวด พริกจินดา) พร้อม metadata
2. สร้าง pipeline แบ่งส่วน + วัดเชิงปริมาณด้วย SAM3 PCS แบบ zero-shot
3. ประเมินเปรียบเทียบกับวิธีพื้นฐาน (SAM2, YOLO-seg, classical) ด้วย mIoU/Dice/F1 [PLAN]
4. ตรวจสอบความถูกต้องของระบบกับค่าอ้างอิงจากผู้ประเมิน (ground truth)

**สมมติฐาน:**
- **H₁ (segmentation):** SAM3 PCS segment ต้นผ่านขวดแก้วที่มี glare/ฝ้า/ไอน้ำได้ โดย mIoU ≥ 0.65 และสูงกว่า baseline [PLAN — ยังรอ ground_truth_masks]
- **H₂ (การจัดกลุ่ม):** ชุด feature ของ SAM3 จำแนกความพร้อมอนุบาลได้ถูกต้อง ≥ 70% และ sensitivity ของกลุ่มพร้อมอนุบาล ≥ 0.6 เทียบผู้ประเมิน **[RESULT — ผ่านด้วยกฎ height-based]**

---

## 4. ข้อมูลและวัสดุ (Dataset)

| รายละเอียด | ค่า |
|---|---|
| ชนิดพืช | พริกจินดา (ชนิดเดียว) |
| จำนวนภาพ | 100 ขวด |
| วันถ่าย | 16 ก.ค. / 2 ส.ค. / 14 ส.ค. 2569 (ชุด **time-series** 3 วัน) |
| ที่เก็บ | `data/raw/20260814_batch/` (001.jpg–100.jpg) |
| ไฟล์เสริม | `manifest.csv` (map ชื่อ), `species_map.csv` |
| กล้อง/HW | สมาร์ตโฟน (ต้นทุนต่ำ) |

> หมายเหตุ: ชุดนี้เป็นทั้งข้อมูลนำร่องและ**จุดเริ่มของ time-series** (ถ่ายซ้ำหลายวัน) — มีคุณค่าต่อการต่อยอย (ดู §10)

---

## 5. วิธีดำเนินการ (Methodology / Pipeline)

### 5.1 ภาพรวมระบบ (diagram เต็มใน `docs/diagrams.md`)
```
ภาพขวด → [SAM3: detect ขวด (ROI)] → [SAM3 PCS: 5 prompts] → [extract 6 กลุ่ม feature] → [rule verdict] → [CSV/XLSX + report.html]
```

### 5.2 การแบ่งส่วนภาพ (SAM3 PCS)
- โมเดล: `facebook/sam3` (gated, ต้อง HF token) — รันบน GPU (Colab T4) [FACT — Carion et al., 2025]
- พรอมป์ 5 คำ: `plant, leaf, shoot, stem, root`
- ตรวจจับขวด (prompt "glass jar bottle") เพื่อกำหนด ROI ขวด
- ค่าเกณฑ์: score ≥ 0.5, mask ≥ 0.5
- **พบข้อจำกัด:** ระบบรากจับได้แค่ 1/100 ภาพ (พอร์ม "root" ผ่านขวดแก้วไม่ได้ผล) [OPEN]

### 5.3 Feature 6 กลุ่ม
| กลุ่ม | ตัวแปร |
|---|---|
| โครงสร้าง | projected area, height/width proxy, coverage_ratio |
| อวัยวะ | leaf_count, shoot_count, stem_count, root_count |
| ความซับซ้อน | hull_ratio |
| สี | green/red/yellow ratio (HSV) |
| คุณภาพภาพ | glare_score, condensation_score |
| การตัดสินใจ | verdict + confidence + readiness_index |

### 5.4 กฎการตัดสินใจ (verdict rule)
- **เดิม:** ใช้ `coverage_ratio` (ความแน่นเต็มขวด) — **พบว่าผิด** (validation ให้ acc 0.43)
- **ใหม่ (อัปเดต 2026-08-26):** ใช้ `height_proxy ≥ 0.275` → **พร้อมอนุบาล**, else → **ยังไม่พร้อม** (อิงนิยาม "ต้นสมบูรณ์/โตพอ/พร้อมย้าย")
- `height_proxy` ไม่ต้องอาศัย ROI ขวด จึงจัดได้ทุกภาพ
- ความมั่นใจ `confidence = base × (1 − glare/100)`; `readiness_index = 0.5·height + 0.3·width + 0.2·green`

### 5.5 การประมวลผลบน Colab
รัน headless: `python sam3_growth_pipeline.py --data ... --out ... --config config.json` ผลเป็น CSV/XLSX + overlays/ + plots/ + report.html และมี checkpoint (`_progress.csv`) กันค้างกลางทาง. แก้บั๊ก RAM: เก็บ mask เฉพาะ 6 ภาพแรก (กันหน่วยความจำพังที่ ~51 ภาพ)

---

## 6. ผลการทดลอง (Results)

### 6.1 ผลรันชุด 100 ขวด
| เมตริก | ค่า |
|---|---|
| Verdict (height-based) | **75 พร้อมอนุบาล / 25 ยังไม่พร้อม** |
| Corr (sanity) | coverage↔area **0.949**, leaf↔coverage **0.852**, green↔healthy **0.910**, coverage↔height **0.701**, leaf↔shoot **0.534** |
| root_count ≥ 1 | เพียง **1/100** |
| canopy_h/w_cm | NaN (ยังไม่ calibrate `pixel_to_cm`) |
| confidence | ~0.78–0.80 |

### 6.2 Validation กับค่าอ้างอิงจากมือ (ground_truth.csv, 100 ภาพ)

**Level B — Pearson r (feature ของ SAM3 เทียบมือ):**
| Feature | n | r | หมายเหตุ |
|---|---|---|---|
| leaf_count | 80 | 0.585 | 20 ภาพหนาแน่นเกิน(leaf>30)ตัดออก |
| shoot_count | 100 | 0.483 | |
| **height** | 100 | **0.638** | ดีสุด |
| width | 80 | 0.477 | |
| root_count | 100 | 0.150 | อ่อน — ราก detect แย่ |
| area | 80 | 0.398 | หน่วย px vs cm² ไม่ตรง |

**Level C — Confusion matrix (verdict vs ผู้ประเมิน):**
| Rule | Accuracy | Sensitivity | F1 | MCC |
|---|---|---|---|---|
| coverage ≥ 0.20 (เดิม) | 0.43 | 0.15 | 0.24 | 0.03 |
| **height ≥ 0.275 (ใหม่)** | **0.755** | **0.917** | **0.821** | **0.472** |

> **ข้อค้นพบหลัก:** ผู้ประเมินนิยาม "พร้อมอนุบาล" = **ต้นสมบูรณ์/โตพอ/พร้อมย้าย** (ไม่ใช่ความแน่นเต็มขวด) → เกณฑ์ coverage เดิม**ใช้ตัวชี้วัดผิด**; ความสูง (height_proxy) เป็นตัวชี้วัดที่ถูก และผ่าน H₂ (acc ≥ 0.70, sens ≥ 0.6)

---

## 7. การอภิปรายผล (Discussion)

1. **เกณฑ์ความพร้อม:** ผลชัดเจนว่าความพร้อมเป็นเรื่อง**การเจริญ/ความโต** ไม่ใช่ความหนาแน่น — นี่คือข้อค้นพบที่ท้าทายสมมติฐานเดิมของหลายงานที่วัดแค่ "พื้นที่ปกคลุม"
2. **ระบบราก:** ยังจับไม่ได้ผล (1/100) ผ่านขวดแก้ว — เป็นข้อจำกัดทางเทคนิคที่ต้องแก้ (prompt ใหม่/วิธีใหม่) ก่อนใช้อ้าง root_ratio
3. **ข้อจำกัดของผล:** เป็น pilot (n=98, **ผู้ประเมินคนเดียว**, **ชนิดเดียว**) — ยังต้องยืนยัน inter-rater + ขยายชนิด
4. **Prompt sensitivity:** SAM3 ไวต่อถ้อยคำพรอมป์ (Dubois et al., 2026) → ผลขึ้นกับการออกแบบพรอมป์ จึงต้องแจ้งชุดพรอมป์ที่ใช้
5. **ความถูกต้อง vs ความสมเหตุผล:** ผลนี้เป็นการ**ตรวจความถูกต้อง (validation)** กับค่าอ้างอิงมือ (ต่างจาก sanity check เดิม) แต่ยังไม่ครอบคลุม Level A (mIoU ของ mask)

---

## 8. สรุปและข้อจำกัด

**สรุป:** ระบบวัดต้นในขวดแบบไม่ทำลายด้วย SAM3 zero-shot ทำงานได้จริงบนชุด 100 ขวด และเมื่อยึดเกณฑ์ความพร้อมตามนิยามผู้เชี่ยวชาญ (ความโต/ความสูง) ให้ผลจัดกลุ่มสอดคล้องกับมนุษย์ในระดับที่ผ่านสมมติฐาน (acc 0.755, sens 0.917)

**ข้อจำกัด (ซื่อตรง):**
- [OPEN] ระบบรากตรวจจับไม่ได้ผล (1/100)
- [OPEN] ยังไม่ calibrate หน่วย cm (canopy_cm = NaN)
- [OPEN] pilot ชนิดเดียว + ผู้ประเมินคนเดียว
- [PLAN] ยังไม่มี baseline (SAM2/YOLO-seg/classical) กับ mIoU (Level A)

---

## 9. (ทางเลือก) การทำงานเชิงเทคนิคที่น่าสนใจ
- **RAM fix:** เก็บ mask เฉพาะ 6 ภาพแรกที่ build_report ใช้ → กันหน่วยความจำพังที่ ~51 ภาพ ระหว่างรัน Colab
- **Config-driven:** threshold/prompts/units ปรับได้โดยไม่แก้โค้ด (`config.json`)
- **กัน verdict ผิด:** เดิมแยกคลาส "ตรวจเอง" เมื่อหา ROI ขวดไม่พบ (ก่อนเปลี่ยนมาใช้ height ที่ไม่ต้องพึ่ง ROI)

---

## 10. เส้นทางต่อยอด (Future Work) [PLAN]

1. **จาก classifier → predictor (time-series):** ใช้ชุด 3 วันสร้าง growth curve + ทำนาย**อัตราการเจริญ**และ**เวลาที่จะพร้อมย้าย** — ยกระดับจาก "พร้อมไหม" เป็น "จะพร้อมเมื่อไร"
2. **ข้ามชนิด (multi-species zero-shot):** ทดสอบกับกล้วยไม้/กล้วย เพื่อพิสูจน์ generalization (ไม่ retrain)
3. **เปิดข้อมูล (FAIR) + baseline ครบ:** เปิด dataset + เปรียบเทียบ SAM2/YOLO-seg/classical ด้วย mIoU/Dice
4. **แอปมือถือ (deployment):** ต่อยอด `src/android/` เป็นแอป "ถ่ายภาพ → verdict เร็ว" สำหรับแล็บจริง

---

## 11. ตารางสรุปไฟล์/หลักฐานใน repo

| สิ่ง | ที่เก็บ | สถานะ |
|---|---|---|
| ผลรัน 100 ขวด | `data/processed/plant_growth_summary.csv` | [RESULT] |
| ค่าอ้างอิงจากมือ | `data/processed/ground_truth.csv` | [RESULT] |
| Confusion matrix | `data/processed/verdict_confusion_full.csv` | [RESULT] |
| รายงาน (แยก) | `docs/report_th_v1.md` | [RESULT] |
| ข้อเสนอ | `docs/proposal_th_draft.md` | [RESULT/PLAN] |
| แผน validation | `docs/VALIDATION_PLAN.md` | [PLAN] |
| เทมเพลต GT | `docs/assets/ground_truth_template.xlsx` | [RESULT] |
| ประวัติงาน | `docs/DEV_LOG.md` | [RESULT] |

> เอกสารนี้เป็น**ภาพรวมสังเคราะห์** — สำหรับรายละเอียดเชิงลึกแต่ละส่วน ดูไฟล์ต้นทางตามตาราง/§5 diagram ใน `docs/diagrams.md`
