# แผนตรวจสอบความถูกต้อง (Validation Plan) — VitroVision รอบชุด 100 ขวด

> เป้าหมาย: เปลี่ยนการประเมินจาก `[PLAN]` → `[RESULT]` โดย**ตรวจกับค่าอ้างอิงจากมนุษย์ (ground truth)** ตามที่ proposal/report สัญญาไว้
> อ้างอิง pipeline: `src/sam3_growth_pipeline.py` (อ่าน `ground_truth.csv` → `validation_metrics.csv`) · `src/benchmark_colab.py` (อ่าน `ground_truth_masks/` → mIoU/Dice)

---

## 1. ภาพรวม — เราจะตรวจอะไร

การตรวจมี 3 ระดับ ไล่จาก "ล่าง" (segmentation) ขึ้น "บน" (การตัดสินใจ):

| ระดับ | ตรวจอะไร | เทียบกับ | ค่าที่ได้ | ไฟล์/เครื่องมือ |
|---|---|---|---|---|
| **A. การแบ่งส่วน** | mask ต้นพืช ที่ SAM3 ผลิต | mask ที่ annotate มือ | mIoU, Dice, F1, precision, recall | `ground_truth_masks/` + `benchmark_colab.py` |
| **B. ค่าวัดเชิงปริมาณ** | leaf/shoot/root counts + height/width/area | ค่าที่วัดมือ | Pearson r, MAE, RMSE | `ground_truth.csv` + `sam3_growth_pipeline.py` |
| **C. การจัดกลุ่ม verdict** | คลาส ยังไม่พร้อม/พร้อมอนุบาล/ตรวจเอง | verdict ที่ผู้เชี่ยวชาญให้ | Confusion matrix, accuracy, sensitivity, specificity, MCC | วิเคราะห์ต่อจาก B (ดู §6) |

> ⚠️ **ข้อจำกัดที่ต้องแก้ก่อน** — ระดับ B ด้าน `root_count` ยัง**วัดไม่น่าเชื่อถือ** (จากรันจริง root_count ≥ 1 มีแค่ **1/100** ภาพ) ดังนั้นการ validate ด้านรากต้อง**รอปรับปรุงการตรวจจับรากก่อน** (ดู §7) ส่วน leaf/shoot/height/width/area validate ได้เลย

---

## 2. ข้อมูล & ไฟล์ที่ต้องมี

**ภาพชุดเป้าหมาย:** `data/raw/20260814_batch/` (100 ภาพ `001.jpg`–`100.jpg`, พริกจินดา)

### 2.1 ค่าวัดมือ → `ground_truth.csv`
- วางที่: **`data/processed/ground_truth.csv`** (เวลารัน Colab ให้คัดเข้า `/content/data/`)
- เทมเพลตพร้อมใช้: **`docs/assets/ground_truth_template.csv`** (100 แถว ชื่อภาพตรงแล้ว)
- คอลัมน์: `image,leaf_count,shoot_count,root_count,height_cm,width_cm,area_cm2,expert_verdict`

### 2.2 mask มือ → `ground_truth_masks/`
- โฟลเดอร์ `ground_truth_masks/` วางข้างๆ โฟลเดอร์ภาพ มี `<ชื่อภาพ>.png` (ขาว = ต้นพืช, ดำ = พื้นหลัง)
- จำนวนแนะนำ **≥ 30 ภาพ** ครอบคลุม 3 คลาส (ยังไม่พร้อม ≥ 10, พร้อมอนุบาล ≥ 5, ตรวจเอง ≥ 5)
- **≥ 2 คน** annotate เพื่อวัด inter-rater agreement (Cohen's kappa / IoU inter-annotator)

---

## 3. จำนวนตัวอย่าง & การสุ่ม (sampling plan)

- **ระดับ A, B:** ใช้ทั้งชุด 100 ภาพ (หรือสุ่ม 30–50 ตามเวลา) — draw แบบ stratified ให้ครบ 3 คลาส verdict
- **ระดับ C:** ใช้**ทุกภาพ** (100) เพราะต้องการ confusion matrix ครบ 3 คลาส
- **อำนาจการทดสอบ:** ถ้าต้องการ report sensitivity ของ "พร้อมอนุบาล" ด้วยความมั่นใจ 95% ที่ความแม่น 80% → ต้องมีกลุ่มพร้อมอนุบาล ≥ 20 ตัวอย่าง (ตอนนี้มี 14 → อาจต้องภาพเพิ่มหรือรายงานเป็น "ผลเบื้องต้น")

---

## 4. โปรโตคอลการวัดมือ (Protocol)

### 4.1 การวัดเชิงปริมาณ (B) — ต่อภาพ
1. **leaf_count** (จำนวนใบ): นับกลีบ/ใบที่มองเห็นผ่านขวดทั้งหมด (รวมที่ซ้อน/จาง)
2. **shoot_count** (จำนวนหน่อ): นับยอดหน่อที่แยกชัดเจน
3. **root_count** (จำนวนราก): นับรากที่มองเห็น (⚠️ ทราบดีว่ามองยากผ่านขวด — ถ้ามองไม่ชัดให้ใส่ 0 และจดหมายเหตุ)
4. **height_cm / width_cm:** วัดด้วยไม้บรรทัด/เวอร์เนีย (จากโคนถึงยอด สูงสุด / ความกว้าง)
5. **area_cm2:** ประมาณพื้นที่ฉายภาพ โดยวัดบนกระดาษกราฟ หรือใช้ `กว้าง × สูง × k` (k = 0.6–0.8 ตามรูปทรง)

### 4.2 การให้ verdict (C) — ต่อภาพ
- `expert_verdict` ∈ {`ยังไม่พร้อม`, `พร้อมอนุบาล`, `ตรวจเอง`}
- ให้ตัดสินตามเกณฑ์ห้องปฏิบัติการจริง (ผู้เชี่ยวชาญ) **โดยไม่เห็น** verdict ของ SAM3 (blind) กัน bias

---

## 5. การฝึกผู้ประเมิน & การลดความเอนเอียง

- **ฝึก (training):** ผู้ประเมินทุกคนดูตัวอย่าง 10 ภาพ ที่อธิบายเกณฑ์ชัดเจนก่อนวัดจริง
- **blinding:** ผู้ประเมินไม่เห็นผล SAM3 / ไม่รู้ว่าภาพไหนเป็นคลาสใด
- **วัด 2 คนต่อภาพ** (แบบ crossover กัน) → คำนวณ **inter-rater agreement**
  - ต่อเนื่อง (leaf/shoot/height...) → **ICC** (intraclass correlation)
  - ต่อคลาส (verdict) → **Cohen's kappa**
- **เหตุผล:** ผลการประเมินด้วยสายตาในงานเพาะเลี้ยงเนื้อเยื่อมีความแปรปรวนระหว่างผู้ประเมิน (Zhang et al., 2026) — ต้องควบคุม

---

## 6. ตัวชี้วัด & เกณฑ์ตัดสิน

| ระดับ | ตัวชี้วัด | สูตร | เกณฑ์เป้าหมาย |
|---|---|---|---|
| A | **IoU / Dice / F1** ต่อภาพ (mask) | พื้นที่ทับซ้อน / ยูเนียน | mIoU ≥ 0.65 (zero-shot ล้ำหน้าวิธีพื้นฐาน) |
| B | **Pearson r** | ว่า SAM3 ตรงกับมือ | r ≥ 0.7 (เชิงเด่น), ≥ 0.4 (พอใช้) |
| B | **MAE, RMSE** | | RMSE เล็ก (เทียบ ช่วงค่าจริง) |
| C | **accuracy, sensitivity** | TN/TP/FN/FP ต่อคลาส | accuracy ≥ 0.70 (สมมติฐาน H₂) |
| C | **sensitivity (พร้อมอนุบาล)** | TP/(TP+FN) | **≥ 0.60** (กลุ่มเป้าหมายหลัก) |
| C | **MCC** | imbalanced ดีกว่า accuracy | MCC ≥ 0.3 |

> สมมติฐานที่ต้องยืนยัน (จาก proposal): **H₂** = ชุด feature 6 กลุ่ม + metadata จำแนกความพร้อมอนุบาลได้ถูกต้อง ≥ 70% และ sensitivity ≥ 0.6 สำหรับกลุ่มพร้อมอนุบาล

---

## 7. ลำดับขั้นตอนปฏิบัติ (runbook)

1. **เตรียม** — annotate มือ: เติม `ground_truth.csv` (100 แถว) + สร้าง `ground_truth_masks/` (≥ 30 ภาพ) → จัดเก็บใน `data/processed/` (เอกสารหลักฐานใน repo)
2. **รัน validation (B)** — pipeline ตรวจพา `ground_truth.csv` อัตโนมัติ → ได้ `validation_metrics.csv` (Pearson/MAE/RMSE)
3. **รัน benchmark (A)** — `python src/benchmark_colab.py --data <ภาพ> --gt ground_truth_masks --out <ผล>` → ได้ mIoU/Dice/F1
4. **วิเคราะห์ confusion matrix (C)** — เทียบ `expert_verdict` กับคอลัมน์ `verdict` ของ SAM3 → accuracy/sensitivity/MCC
5. **รายงาน** — เติมผลลง `report_th_v1.md` + `proposal_th_draft.md` (เปลี่ยน `[PLAN]`→`[RESULT]`) + DEV_LOG + commit

### 7.1 หมายเหตุรอง
- **root_count:** จากผลรันจริง (1/100) การ validate ด้านราก**ยังไม่มีความหมาย**จนกว่าจะปรับปรุงการตรวจจับราก → แยกเป็นงานถัดไป ไม่บังคับในรอบนี้
- **หน่วย cm:** ต้องสอบเทียบ `PIXEL_TO_CM` ก่อน (ดู `CALIBRATION_GUIDE.md`) ไม่งั้น `height_cm/width_cm` ที่เทียบกับ SAM3 (ซึ่งเป็น `height_proxy/width_proxy` ไม่ใช่ cm) ต้องแปลความหมายอย่างระวัง

---

## 8. สิ่งที่ทำให้งานนี้เป็น "ผลงานจริง" (ต่อยอด)

เมื่อได้ validation ครบ 3 ระดับ → จะตอบได้ว่า:
- SAM3 ผ่านขวดแก้วแม่นแค่ไหน (เทียบมือ ม.มนุษย์) — เป็น**การตรวจสอบความถูกต้องจริง** ไม่ใช่แค่ sanity check
- การตัดสินใจจัดกลุ่มความพร้อมอนุบาลถูกต้อง ≥ 70% หรือไม่ (ยืนยัน/หักล้าง H₂)
- inter-rater agreement สูงแค่ไหน (กันจุดอ่อน observer bias)

> ขั้นสุดท้ายถ้าครบ: เปิดdataset + benchmark ครบ baseline (SAM2/YOLO-seg) + sensitivity analysis → ครบ contribution ตาม framing 96/100 ของ YSC
