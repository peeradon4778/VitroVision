# ระเบียบวิธีการทดลอง (Methodology) + ข้อมูลจริง — VitroVision

> เอกสารนี้รวม**ระเบียบวิธี**และ**ข้อมูลตัวเลขจริง**จากโปรเจกต์ เพื่อให้นำไปใส่ในข้อเสนอโครงงาน (ส่วน §5) ได้ทันที
> ที่มาของข้อมูลทุกตัว: `docs/DEV_LOG.md` · `data/processed/*.csv` · `docs/runbooks/CALIBRATION_GUIDE.md` · `config.json`
> ตัวเลขที่ทำแล้ว = **จริง** (จากผลรัน) · ตัวเลขที่จะทำ = **[PLAN]** (ยังไม่มีผล ต้องเขียนเป็นแผน)

---

## 5.1 ภาพรวมการทำงานของระบบ

ระบบแบ่งงานเป็น 5 ขั้นตอนหลัก:

1. **ถ่ายภาพขวด** (ผ่านแก้วปิด) — เก็บชุดข้อมูลจริง
2. **ตรวจจับขอบเขตขวด** (bottle ROI) — ใช้เป็นกรอบอ้างอิงพื้นที่
3. **แบ่งส่วนภาพ (segmentation)** — SAM3 เป็นต้นแบบ → กลั่นเป็น U-Net ขนาดเล็ก
4. **คำนวณ feature เชิงปริมาณ** จาก mask
5. **ตัดสินใจด้วยกฎ (rule-based)** — จำแนก "พร้อมอนุบาล / ยังไม่พร้อม / ตรวจเอง"

ภาพที่ประมวลผลไม่ชัด (glare/ฝ้า/ไม่พบขวด) จะถูกทำเครื่องหมาย **"ตรวจเอง"** เพื่อส่งให้มนุษย์ตรวจแทนการตัดสินใจอัตโนมัติ (ลดความเสี่ยงความผิดพลาด)

---

## 5.2 การเก็บข้อมูล (Data Collection)

- **อุปกรณ์:** สมาร์ตโฟน (ไม่มี LiDAR) ถ่ายภาพขวดบนพื้นหลังสีด้าน (matte) ระยะห่างคงที่
- **การจัดแสง:** แสงด้านข้างมุมประมาณ 45° หลีกเลี่ยงแสงตรงเพื่อลด glare
- **การถ่ายซ้ำ:** ถ่าย 2–3 ครั้ง/ขวด เพื่อกันภาพเบลอ/สะท้อน
- **metadata ที่บันทึก:** วันที่ถ่าย · จำนวนวันหลังตัดย้ายล่าสุด (`days_since_last_subculture`) · ชนิดพืช · การประเมินโดยนักวิทยาศาสตร์ (ground truth: ยังไม่พร้อม / พร้อมอนุบาล / ตรวจเอง)
- **ชุดข้อมูล (เสร็จแล้ว):**
  - **ชุดฝึก/ตรวจ:** ภาพ greenhouse สาธารณะ **1,200 ภาพ** (มี mask กำกับ) → แบ่ง train **1,080** / val **120** (90/10)
  - **ชุดทดสอบจริง (ของเรา):** ภาพขวดพริกจินดา **100 ขวด** (24 ส.ค. 2569, `20260814_batch`) → มี expert verdict **98 ภาพ**
  - **ชุดอ้างอิง (ground truth):** `data/processed/ground_truth.csv` (ความสูง/กว้าง/พื้นที่/verdict + หมายเหตุ)
- **เป้าหมายตัวอย่าง (แผน):** ≥100 ขวด ครอบคลุม 3 คลาส และ ≥2–3 ชนิด (เพื่อพิสูจน์ข้ามชนิด) **[PLAN]**

---

## 5.3 ขั้นตอนการประมวลผลภาพ (Image Processing Pipeline)

1. รวบรวมภาพถ่ายขวดจากชุดข้อมูล
2. ตรวจจับขอบเขตขวด (bottle ROI detection) เป็นกรอบอ้างอิงพื้นที่ปกคลุม
3. **แบ่งส่วนภาพด้วย SAM3** (`facebook/sam3`, Promptable Concept Segmentation) แบบ headless batch บน GPU ด้วยพรอมป์ข้อความ 5 คำ: `plant`, `leaf`, `shoot`, `stem`, `root` · เกณฑ์ `score_threshold=0.5`, `mask_threshold=0.5`
   - SAM3 ใช้เป็น**ต้นแบบ (teacher) เพื่อสร้าง pseudo-labels** ในการฝึก
   - **กลั่นเป็น U-Net ขนาดเล็ก** (MobileNetV3-Small encoder, ~3.6M params) ให้ทำงานบน CPU ได้จริง
4. รับผลลัพธ์เป็น binary mask ต่อพรอมป์ พร้อม confidence score และ bounding box
5. นับใบแบบ merged (รวมชิ้นส่วนติดกันเป็น 1 ใบ กัน over-segmentation) พร้อม fallback นับจาก `plant`+`shoot`

**การฝึก U-Net (เสร็จแล้ว):**

- สถาปัตยกรรม: `smp.Unet(encoder_name="timm-mobilenetv3_small_100", in_channels=3, classes=1)`
- ขนาดภาพ: 256×256 · batch 4 · lr 1e-3 · 15 epochs (resume จาก checkpoint)
- ฟังก์ชัน loss: BCE + Dice · แก้บั๊ก dice (รับ uint8 0/255 แล้ว cast bool) ก่อน
- ผล:`val_dice 0.977–0.981` (สูงสุด **0.9817**), loss 0.0366–0.0442
- ข้อมูลโมเดล: `final_model.pt` (14.5MB) + `best_model.pt` · ขึ้น HF `peeradon4778/vitrovision-unet-small` แล้ว

---

## 5.4 การคำนวณ feature และเกณฑ์ตัดสินใจ

**Feature เชิงปริมาณ 6 กลุ่ม** (คำนวณจาก mask):

| กลุ่ม | Feature |
| --- | --- |
| โครงสร้าง | coverage_ratio, height_proxy, hull_ratio |
| อวัยวะ | leaf_count, shoot_count, root_count |
| ความซับซ้อน | compactness |
| สี | green_pct, yellow_ratio, brown_ratio |
| คุณภาพภาพ | glare_score, condensation_score |
| การตัดสินใจ | verdict, confidence |

**เกณฑ์ตัดสินใจ (rule-based, อธิบายได้):**

- **แบบ SAM3 (นำร่อง):** `height_proxy ≥ 0.275` → "พร้อมอนุบาล"
- **แบบ U-Net (ใช้งานจริง):** ปรับเกณฑ์โดยสแกน 0.12–0.55 → เลือกค่า Youden-balanced **`height_proxy ≥ 0.20`** → "พร้อมอนุบาล"
- ภาพไม่ชัด → "ตรวจเอง"
- ค่า reference: `config.json` (`height_ready=0.20`, `coverage.ready=0.20`, `overdense=0.80`, `use_species_thresholds=false`)

---

## 5.5 การตรวจสอบความถูกต้อง (Validation)

1. **ระดับพิกเซล (segmentation):** create ground-truth masks ≥30 ภาพ → เทียบ mask ระบบ vs วิธีพื้นฐานด้วย mIoU/Dice/F1/precision/recall **[PLAN — รอ annotate]**
2. **ระดับการจัดกลุ่ม (classification):** เทียบ verdict ระบบ vs ผู้เชี่ยวชาญด้วย confusion matrix + accuracy/precision/sensitivity/specificity/F1/MCC/Cohen's kappa
3. **ความสอดคล้องระหว่างผู้ประเมิน:** ICC / Cohen's kappa (เทียบความแปรปรวนระบบ vs มนุษย์)
4. **การทดสอบข้ามชนิด:** ทดสอบกับพืชต่างชนิดโดยไม่ต้องฝึกใหม่ **[PLAN — ตากล้อง]**

---

## 6. ข้อมูลผลจริง (ตัวเลขที่นำไปใส่ข้อเสนอได้)

> จัดกลุ่มตามหัวข้อในข้อเสนอ — ตัวเลขจริงทั้งหมดมาจากผลรันแล้ว ยกเว้นที่ระบุ **[PLAN]**

### 6.1 ผลการแบ่งส่วนภาพ (Segmentation)

| รายการ | ค่าจริง |
| --- | --- |
| โมเดล U-Net (กลั่นจาก SAM3) | MobileNetV3-Small encoder, ~3.6M params |
| val_dice (ชุด val 120 ภาพ) | **0.9817** (ช่วง 0.977–0.981) |
| ชุดฝึก/ตรวจ | 1,080 / 120 (จาก 1,200 ภาพ greenhouse) |
| การกลั่น | SAM3 teacher → pseudo-labels → U-Net student |

### 6.2 การปรับเทียบ (Calibration) หน่วย px→cm

จาก `trait_benchmark_height_error_cm.csv` (100 ภาพ, calibrated):

| วิธี | MAE (cm) | RMSE (cm) | R²(out-of-fold) |
| --- | --- | --- | --- |
| SAM3 | **1.145** | **1.413** | **0.386** |
| Classical | 1.277 | 1.580 | 0.233 |
| YOLO-COCO | 1.501 | 1.810 | -0.006 |

### 6.3 ความสอดคล้องกับค่าที่วัดด้วยมือ (Trait benchmark, 100 ภาพ)

จาก `trait_benchmark_summary.csv`:

| วิธี | Height Pearson r (cm) | Height R² | Area Pearson r (cm²) | zero_mask % | runtime (s) |
| --- | --- | --- | --- | --- | --- |
| SAM3 | **0.638** | **0.407** | **0.398** | 1% | — |
| Classical | 0.498 | 0.248 | 0.261 | 23% | 0.23 |
| YOLO-COCO | 0.133 | 0.018 | 0.050 | 13% | 0.263 |

> ความหมาย: SAM3 วัดความสูงได้สอดคล้องกับการวัดด้วยมือดีที่สุด — ใช้เป็นข้อสรุปว่าวิธี "ทำนาย" จากภาพมีศักยภาพ

### 6.4 ผลการจัดกลุ่มความพร้อม (Classification — ระดับภาพ)

**SAM3 (เกณฑ์ 0.275):** accuracy **0.755**, sensitivity **0.917** — ผลนำร่อง [อ้างจาก DEV_LOG]
**U-Net (เกณฑ์ 0.20, Youden):** จาก 98 ภาพ → accuracy **0.653**, sensitivity **0.717**, specificity **0.579**

> ⚠️ **ข้อซื่อตรง:** U-Net แบ่งส่วนภาพดี (dice 0.98) แต่ feature 2D (height/width/coverage) แยก verdict ได้**ปานกลาง** (acc สูงสุด ~0.68 threshold 0.14; 0.20 = Youden-balanced) · multi-trait logistic in-sample AUC 0.639 ไม่ดีกว่า single proxy → **หนุนสมมติฐานว่าต้องใช้ภาพ 3D** (2D projected area มีข้อจำกัด)

### 6.5 การเทียบ baseline (Segmentation)

จาก `benchmark_classical_yolo/` — 100 ภาพ:

| Baseline | runtime (s/ภาพ) |
| --- | --- |
| Classical (สี/การแบ่งภาพแบบเดิม) | ~0.45 |
| YOLO-COCO (seg) | ~0.30 |

> อาจรายงานเป็น trade-off ต้นทุนเวลา ไม่ใช้เป็นผลความแม่นยำ (สรุป mIoU/Dice ต้องการ ground truth ระดับพิกเซล ซึ่งเป็น [PLAN])

---

## 7. การวิเคราะห์ข้อมูล (Data Analysis — เพิ่มคำอธิบาย)

- **Segmentation level:** mIoU / Dice (F1 พิกเซล) / precision / recall / pixel accuracy — มาตรฐาน Cityscapes/COCO
- **Classification level:** confusion matrix + accuracy / precision / sensitivity / specificity / F1 / MCC / Cohen's kappa — ใช้ MCC เป็นตัวเลือก threshold (ทน imbalance)
- **Threshold tuning:** สแกน 0.10–0.90 → เลือก MCC สูงสุด / Youden-balanced
- **Prompt sensitivity:** ทดสอบชุดพรอมป์ทางเลือก → รายงานความแปรปรวนของ mIoU-verdict (อ้าง Dubois et al., 2026)
- **Feature analysis:** scatter / box plot / correlation matrix — หา multicollinearity + อำนาจจำแนกแต่ละ feature

---

## 📌 ตารางสรุปข้อมูลที่ต้องใช้ (สำหรับกรอกข้อเสนอ)

| หัวข้อ | ข้อมูลจริง | ค่า |
| --- | --- | --- |
| ชนิดพืช (pilot) | พริกจินดา | 100 ขวด |
| ชุดฝึก (greenhouse) | 1,200 ภาพ | train 1,080 / val 120 |
| โมเดล | U-Net + MobileNetV3-Small | ~3.6M params |
| val_dice (U-Net) | สูงสุด | 0.9817 |
| เกณฑ์ SAM3 (ready) | height_proxy ≥ | 0.275 |
| เกณฑ์ U-Net (ready, Youden) | height_proxy ≥ | 0.20 |
| acc / sens / spec (U-Net, n=98) | — | 0.653 / 0.717 / 0.579 |
| acc / sens (SAM3 pilot) | — | 0.755 / 0.917 |
| Height r (SAM3 vs มือ) | Pearson | 0.638 |
| Height MAE/RMSE (SAM3) | cm | 1.145 / 1.413 |
| Level A mIoU/Dice | เทียบมนุษย์ | **[PLAN — annotate 30 ภาพ]** |
| Cross-species | ชนิดอื่น | **[PLAN — ถ่ายภาพ]** |
