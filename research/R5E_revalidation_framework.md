# R5E — Re-Validation Framework หลัง Method Change (Segmenter: HSV → SAM/YOLOv8-seg)

> สร้าง: 2026-06-21 | Sub-agent: R5-E | คำถาม: Q11 (parked) — L7 stats framework หลัง architecture เปลี่ยน

---

## VERDICT

เมื่อเปลี่ยน segmenter จาก HSV-thresholding → SAM/YOLOv8-seg ซึ่งเป็น **measurement method change** ที่กระทบ feature values อย่าง systematic (variance เลื่อน ~8×) — κ=0.6274 เดิม **ใช้ไม่ได้** บน engine ใหม่ ต้อง re-validate ใหม่ทั้งหมดตาม bridge/calibration study framework

กรอบมาตรฐานที่ใช้ใน clinical และ plant phenotyping มี 4 ชั้น:
1. **Bridge study** (old vs. new method บน sample ชุดเดิม)
2. **Freeze protocol** (freeze ทุก module ก่อน collect validation data)
3. **Systematic bias check** (Bland-Altman / mean difference)
4. **Re-compute κ + ICC + MDC** บน engine ที่ freeze แล้ว

---

## 1. Bridge / Calibration Study — วิธีมาตรฐาน

**หลักการ:** วิ่ง old method และ new method บน **sample ชุดเดียวกัน** (n ≥ 30 ขวด, หลายวันที่) แล้ว plot ค่า feature ที่ได้ vs กัน — ไม่ใช่แค่ correlation

มาตรฐานอ้างอิงคือ **Bland-Altman analysis** [Bland & Altman 1986] ซึ่งเป็น gold standard เฉพาะ method comparison:
- Plot: แกน X = mean(old, new) แกน Y = (new − old)
- ดู **mean difference** (systematic bias) + **limits of agreement** (LoA = mean ± 1.96 SD)
- ถ้า mean difference ≠ 0 อย่างมีนัยสำคัญ = method ใหม่มี systematic shift ต้องรายงาน

> "Correlation does not provide a useful answer to the agreement between 2 methods of measurement" — Bland & Altman (1986) [1]

สำหรับ VitroVision: ทำ Bland-Altman plot ต่อ 1 feature (เช่น normalized_green_area, shoot_pixel_count, leaf_count_proxy) — ทั้งหมดที่เข้า classifier

---

## 2. ลำดับ Freeze ที่ถูก (Pipeline Lock Order)

**กฎเหล็ก:** ต้อง freeze ทีละชั้น จาก input ไป output — ห้ามเปลี่ยน downstream component หลัง collect validation data ไปแล้ว เพราะจะทำให้ต้อง re-validate ทุกชั้นใต้จุดที่เปลี่ยน

```
ลำดับ FREEZE (บังคับทำก่อน collect validation data):

L0: กล้อง + แสง         ← freeze hardware/setting ก่อน
     │
L1: Color calibration    ← freeze color card + WB correction algorithm
     │                      (R4B/R4C ที่ทำไปแล้ว)
     │
L2: Segmenter            ← freeze SAM/YOLOv8-seg weights + config
     │                      ❗ นี่คือจุดที่เปลี่ยนไป = เหตุที่ต้อง re-validate
     │
L3: Feature calculator   ← freeze extraction code (src/utils/)
     │
L4: Classifier           ← freeze model weights (ห้าม retrain ระหว่าง validation)
     │
L5: Ground truth protocol ← freeze rubric scoring sheet (expert_scoring_sheet.csv)

→ COLLECT validation data เมื่อ L0–L5 freeze แล้วทั้งหมด
→ ถ้าต้องแก้ L2 (เช่น retrain YOLOv8-seg) → re-validate ตั้งแต่ L2 ลงไปทั้งหมด
```

**หลักฐานจาก HTP phenotyping:** งานของ Bauer et al. (2022) [2] ที่ develop deep learning pipeline สำหรับ minirhizotron ทำ validation โดย freeze segmentation model (RootPainter) ก่อน จากนั้น compare กับ manual annotation — correlation = 0.9 ทำได้เพราะ pipeline ไม่เปลี่ยนระหว่าง validation; Okyere et al. (2023) [3] ก็ใช้แนวทางเดียวกันใน HTP segmentation comparison (MLP vs HSV-index) — freeze ทุก algorithm ก่อน evaluate SPAD prediction accuracy

---

## 3. Systematic Bias Detection — ก่อนคำนวณ κ/ICC ใหม่

### 3.1 ขั้นตอนตรวจ systematic drift

1. **รัน bridge study** (ข้อ 1) — ได้ vector of differences `d_i = new_i − old_i` ต่อ feature แต่ละตัว
2. **One-sample t-test** หรือ Wilcoxon signed-rank ทดสอบ H₀: mean(d) = 0
   - ถ้า reject H₀ = มี systematic bias → ต้องรายงานและอธิบายใน Methods
3. **Bland-Altman plot with regression line** — ถ้า slope ≠ 0 = proportional bias (new method drift ขึ้น/ลงตาม magnitude)
4. **ICC กับ systematic error:** Weir (2005) [4] แนะนำให้ใช้ ICC(2,1) (two-way mixed model) เพราะแยก systematic error ออกจาก random error ได้ — ถ้า systematic error ใหญ่ ICC(2,1) จะต่ำกว่า ICC(3,1) อย่างเห็นได้ชัด

> "Inferential tests of mean differences... are useful to determine if systematic error is present. If so, the measurement schedule should be modified to remove systematic error" — Weir (2005) [4]

### 3.2 สำหรับ VitroVision

- ทำ Bland-Altman ต่อ feature สำคัญ (เช่น `normalized_green_area`, `hue_mean`, `sat_mean`)
- ถ้าพบ systematic shift ใน feature ใด → ระบุใน Methods ว่า "engine change introduced mean offset of X ± Y units" → classifier ที่ train บน old feature space ต้องเทรนใหม่บน new feature space
- ICC(2,1) ก่อน vs หลัง freeze = ตัวชี้วัดว่า engine ใหม่ stable ขนาดไหน

---

## 4. MDC vs MID — ใน Context ของ VitroVision

| สถิติ | ความหมาย | สูตร | ใช้ตอบคำถามอะไร |
|-------|----------|------|-----------------|
| **SEM** (Standard Error of Measurement) | error รอบ single measurement | SEM = SD × √(1 − ICC) | pipeline ใหม่ noisy แค่ไหน |
| **MDC₉₅** (Minimum Detectable Change) | การเปลี่ยนแปลงที่เล็กที่สุด ที่เหนือ noise 95% | MDC = SEM × 1.96 × √2 | "เปลี่ยน engine แล้ว feature ต่างกันเกิน noise จริงไหม" |
| **MID** (Minimally Important Difference) | การเปลี่ยนแปลงที่ clinically/biologically meaningful | anchor-based หรือ 0.5 SD | "ความต่างของ feature ยังแยก phenotype ต่างๆ ได้ไหม" |

**Turner et al. (2009)** [5] ชี้ชัดว่า MDC ≠ MID — MDC บอกแค่ว่า "noise เท่าไหร่" แต่ไม่บอกว่า "สำคัญไหม" ต้องใช้ทั้งคู่

**Riemann & Lininger (2018)** [6] แนะนำ workflow:
```
1. คำนวณ ICC(2,1) จาก test-retest บน frozen pipeline
2. คำนวณ SEM จาก ICC
3. คำนวณ MDC₉₅ = SEM × 2.77
4. กำหนด MID จาก domain knowledge (เช่น ต่าง phenotype class ≥ X หน่วย)
5. ถ้า MDC > MID = pipeline ไม่ sensitive พอ = ต้อง improve ก่อน re-validate κ
```

**สำหรับ VitroVision:** MID คือ "feature ต้องต่างกันมากพอที่ classifier จะแยก phenotype class ได้" — กำหนดจาก feature distribution analysis ระหว่าง class ก่อน (ดู R1/R3 ที่ทำไปแล้ว)

---

## 5. Plant Phenotyping Pipeline Re-Validation — ตัวอย่างจริง

### 5.1 Bauer et al. 2022 — Deep Learning Minirhizotron [2]
- เปลี่ยนจาก manual annotation → DL segmentation (RootPainter + RhizoVision Explorer)
- **วิธี re-validate:** bridge study = run both pipelines บน 36,500+ images เดียวกัน
- **Metric:** Pearson correlation + Bland-Altman-style comparison
- **ผล:** r = 0.9, processing time ลด 98%
- **บทเรียน:** freeze segmentation model weights ก่อน collect validation subset

### 5.2 Okyere et al. 2023 — HTP Segmentation Algorithm Comparison [3]
- เปรียบ MLP vs SVM vs ExG/ExGR (HSV-based) บน cowpea + wheat
- **วิธี re-validate:** freeze algorithm → evaluate pixel classification accuracy + SPAD regression R²
- **ผล:** MLP > 98% pixel accuracy vs ExG ~94%
- **บทเรียน:** เมื่อเปลี่ยน segmenter ค่า downstream feature (SPAD prediction) เปลี่ยนตาม — ต้อง re-validate ทุก downstream metric ไม่ใช่แค่ segmentation IoU

### 5.3 Du et al. 2026 — 3D Plant Reconstruction Pipeline [7]
- เปลี่ยน reconstruction method → validate phenotypic parameter accuracy
- **วิธี:** validate 3 phenotypic parameters (plant height, leaf width, chord length) vs ground truth manual measurement
- **Metric:** MAE, RMSE, R² — ไม่ใช้ κ เพราะ continuous measurement
- **บทเรียน:** validation metric ต้องเหมาะกับ scale ของ output (κ = categorical, ICC/R² = continuous)

---

## 6. Step-by-Step Re-Validation Protocol สำหรับ VitroVision

```
PHASE 0 — PREPARATION (ก่อนเริ่ม)
  □ Freeze L0–L5 ทั้งหมด (hardware, color cal, SAM/YOLO weights, feature code, rubric)
  □ สร้าง validation set: n ≥ 30 ขวด, ครอบ 5 สูตร MS และหลายวันที่
  □ collect ground truth labels ใหม่ด้วย frozen rubric (expert_scoring_sheet.csv)

PHASE 1 — BRIDGE STUDY (old engine vs new engine)
  □ รัน HSV pipeline (old) และ SAM/YOLO pipeline (new) บน validation set เดียวกัน
  □ สร้าง Bland-Altman plot ต่อ feature สำคัญทุกตัว
  □ test H₀: mean(diff) = 0 ต่อ feature
  □ บันทึก: systematic bias, proportional bias, LoA

PHASE 2 — SYSTEMATIC BIAS REPORT
  □ ถ้าพบ systematic shift ≠ 0 → ระบุใน Methods section ของรายงาน
  □ อธิบายทิศทางและขนาดของ bias (เช่น "new engine overestimates green area by +12%")
  □ ตัดสินใจ: calibrate correction offset ไหม หรือรายงาน as-is พร้อมขอบเขต?

PHASE 3 — RE-COMPUTE RELIABILITY METRICS
  □ ICC(2,1) ระหว่าง annotator pair (human expert) บน new engine features
  □ SEM = SD × √(1 − ICC)
  □ MDC₉₅ = SEM × 2.77
  □ กำหนด MID จาก feature separation analysis ระหว่าง phenotype class
  □ ตรวจ: MDC < MID ไหม? ถ้าไม่ → pipeline ต้องปรับ

PHASE 4 — RE-COMPUTE κ
  □ รัน full annotation protocol บน validation set (≥ 2 independent raters)
  □ คำนวณ Cohen's κ (unweighted สำหรับ nominal phenotype class)
  □ คำนวณ Gwet's AC1 ควบคู่ (ป้องกัน kappa paradox เมื่อ class imbalanced)
  □ report: κ, AC1, 95% CI, % agreement raw

PHASE 5 — DOCUMENT
  □ อัพเดต _citation_audit.md ด้วย bridge study result
  □ อัพเดต architecture_overview.md ว่า validated บน engine version ไหน
  □ บันทึก engine version hash ใน models/ directory
```

---

## 7. ข้อควรระวัง

1. **อย่า re-validate ด้วย data ที่ใช้ train segmenter** — data leakage ทำให้ κ inflate
2. **Class imbalance ทำให้ κ ต่ำแบบ paradox** — ใช้ Gwet's AC1 ควบคู่ [Cibulka et al. 2021] [8]
3. **ICC form สำคัญมาก** — ICC(2,1) สำหรับ method comparison (generalize to new raters/time), ICC(3,1) ถ้า fixed raters เท่านั้น [Koo & Mae 2016] [9]
4. **อย่า interpret κ โดยไม่มี CI** — sample n=30 ทำให้ CI กว้างมาก (±0.2–0.3)
5. **Regression to the mean:** ถ้า bridge study พบ proportional bias (slope ≠ 0) — ค่า feature ที่ extreme (ขวดที่ดีมาก/แย่มาก) จะถูก overestimate/underestimate โดย new engine ไม่สม่ำเสมอ — ต้องรายงานแยก

---

## Citations

[1] [Statistical methods for assessing agreement between two methods of clinical measurement](https://consensus.app/papers/details/6563c591338851ab9fc0a0d2ff81528a/?utm_source=claude_code) — Bland & Altman, 1986, Lancet, 50,446 citations

[2] [Development and Validation of a Deep Learning Based Automated Minirhizotron Image Analysis Pipeline](https://consensus.app/papers/details/40adfa3eb17a5757ac1f8c43b6462d68/?utm_source=claude_code) — Bauer et al., 2022, Plant Phenomics, 40 citations

[3] [Machine Learning Methods for Automatic Segmentation of Images of Field- and Glasshouse-Based Plants for High-Throughput Phenotyping](https://consensus.app/papers/details/70d93f4bc85e50d6806aede5c472ec38/?utm_source=claude_code) — Okyere et al., 2023, Plants, 15 citations

[4] [Quantifying test-retest reliability using the intraclass correlation coefficient and the SEM](https://consensus.app/papers/details/72e1091b8a0f547a8a113daf1b4cc428/?utm_source=claude_code) — Weir, 2005, Journal of Strength and Conditioning Research, 5,107 citations

[5] [The minimal detectable change cannot reliably replace the minimal important difference](https://consensus.app/papers/details/7ee1068b4ea05614a68ead8fbb8e06e6/?utm_source=claude_code) — Turner et al., 2009, Journal of Clinical Epidemiology, 330 citations

[6] [Statistical Primer for Athletic Trainers: The Essentials of Understanding Measures of Reliability and Minimal Important Change](https://consensus.app/papers/details/9ac18b017d975831982180b43bc8046d/?utm_source=claude_code) — Riemann & Lininger, 2018, Journal of Athletic Training, 39 citations

[7] [Plant-to-camera enabled 3D morphological reconstruction: A high-fidelity approach for plant phenotyping](https://consensus.app/papers/details/314eec9539bd5093a83071a5bacf4ecd/?utm_source=claude_code) — Du et al., 2026, ISPRS Journal of Photogrammetry and Remote Sensing, 3 citations

[8] [The Conundrum of Kappa and why some Musculoskeletal Tests Appear Unreliable despite High Agreement](https://consensus.app/papers/details/441b6816ce0d543694552e9f2ddb70c7/?utm_source=claude_code) — Cibulka et al., 2021, Physical Therapy, 22 citations

[9] [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — Koo & Mae, 2016, Journal of Chiropractic Medicine, 24,359 citations

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
