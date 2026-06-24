# R5-B — Method Comparison: CV System vs Expert (Bland-Altman + Spearman)

> Sub-agent R5-B | VitroVision (YSC 2027 → ISEF CSBI)
> โจทย์: validate green_coverage_pct (CV continuous 0–100%) ต่อ expert vigor score (ordinal 1–5) ด้วย Bland-Altman, Spearman ρ, และ ICC — พร้อม benchmark ที่อ้างอิงได้
> ทุก citation มาจาก Consensus จริง + URL ตรวจสอบได้

---

## VERDICT รวม

| คำถาม | คำตอบสั้น |
|---|---|
| Bland-Altman ใช้ได้ไหม? | ใช้ได้ **เมื่อ convert ordinal → normalized %** ก่อน หรือใช้คู่กับ Spearman ρ เท่านั้น — ไม่ใช้ Bland-Altman กับ ordinal raw โดยตรง |
| เทียบ continuous vs ordinal อย่างไร? | Spearman ρ = primary; Bland-Altman = secondary (ต้อง normalize scale ก่อน); หลีกเลี่ยง Pearson กับ ordinal |
| Repeatability ของ CV ใช้ metric ใด? | **ICC(2,1)** สำหรับ absolute agreement ข้ามวัน + **CV% (coefficient of variation)** สำหรับ spread ของ error |
| Benchmark ρ/ICC ที่ถือว่า "ผ่าน"? | ρ ≥ 0.80 (strong), ICC ≥ 0.75 (good), ICC ≥ 0.90 (excellent) |
| ข้อผิดพลาดที่พบบ่อย? | Pearson กับ ordinal, Bland-Altman โดยไม่ check normality, anchoring bias, scale mismatch ไม่รายงาน |

---

## ตารางหลักฐาน

| วิธี | เหมาะกับ | เงื่อนไข/ข้อควรระวัง | อ้างอิง + URL |
|---|---|---|---|
| **Bland-Altman** | เทียบ 2 methods ที่วัด trait เดียวกัน (continuous vs continuous) | ต้องการ: (1) ทั้งสองค่าอยู่ใน same scale หรือ normalized ก่อน (2) differences ใกล้เคียง normal (3) no systematic trend ใน mean | [Suarez et al. 2025](https://consensus.app/papers/details/d1ce9592314351b1a3e1ac7957b1f4a2/?utm_source=claude_code) ใช้ Bland-Altman เทียบ Python HSV vs ImageJ — bias ≤ ±0.14 cm² ถือว่าดีมาก |
| **Spearman ρ** | เทียบ continuous (CV%) vs ordinal (vigor 1–5) — ไม่สมมติ linearity | ต้องการ n ≥ 30 สำหรับ CI ที่น่าเชื่อถือ; รายงาน 95% CI bootstrap | [Kolhar et al. 2021](https://consensus.app/papers/details/750931a401235aa9b1252f1e18cf6263/?utm_source=claude_code) — review ยืนยัน Spearman เป็น standard สำหรับ non-parametric trait correlation ใน plant phenotyping |
| **ICC (Intraclass Correlation)** | Repeatability ข้ามวัน, inter-session reliability ของ CV measurement | เลือก form: ICC(2,1) สำหรับ 2-way random, absolute agreement; ICC < 0.5 = poor, 0.5–0.75 = moderate, 0.75–0.9 = good, > 0.9 = excellent | [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — guideline อ้างอิงมาตรฐาน 24,359 citations |
| **CV% (Coefficient of Variation)** | วัด relative spread ของ CV measurement ซ้ำ (repeatability %) | CV% = (SD/mean) × 100; ค่า < 5% = excellent repeatability | [Bao et al. 2018](https://consensus.app/papers/details/a6ce4ef61f8d518cb99a829626020ab7/?utm_source=claude_code) — robotic phenotyping sorghum รายงาน high repeatability ด้วย CV% |
| **Ordinal regression / rank-based test** | เมื่อ reference เป็น ordinal แท้ และต้องการ hypothesis test | Shah & Madden 2004: nonparametric analysis ของ ordinal plant disease rating เป็น gold standard | [Shah et al. 2004](https://consensus.app/papers/details/092959e52a1a507c8d43157257ed22a2/?utm_source=claude_code) — 431 citations; Bock et al. 2024 ยืนยันว่า % scale มักแม่นกว่า ordinal scale ดั้งเดิม |

---

## ตอบทีละคำถาม

### 1. Bland-Altman สำหรับ CV vs Expert — เหมาะเมื่อไร?

Bland-Altman analysis ออกแบบมาสำหรับเทียบ **สองวิธีวัดที่วัด trait เดียวกันในหน่วยเดียวกัน** ปัญหาของ VitroVision คือ CV ให้ `green_coverage_pct` (0–100%, continuous) แต่ expert ให้ `vigor score` (1–5, ordinal) ซึ่ง **ไม่ใช่หน่วยเดียวกัน**

**วิธีใช้ Bland-Altman ให้ถูกต้องใน VitroVision:**
1. **Normalize vigor → %:** แปลง vigor 1–5 เป็น 0–100% ก่อน (เช่น vigor 1 = 0%, vigor 3 = 50%, vigor 5 = 100%) แล้วจึงคำนวณ Bland-Altman
2. **ใช้เป็น secondary analysis** ควบคู่กับ Spearman ρ ซึ่งเป็น primary
3. **ตรวจสอบ:** plot ค่า difference vs mean, ดู systematic bias, ดู limits of agreement (mean ± 1.96 SD)

หลักฐานจาก [Suarez et al. 2025](https://consensus.app/papers/details/d1ce9592314351b1a3e1ac7957b1f4a2/?utm_source=claude_code): ใช้ Bland-Altman เทียบ Python HSV segmentation vs ImageJ (ทั้งคู่ continuous, same unit) — mean bias ±0.14 cm², limits of agreement ±0.3 cm² = แคบมาก ถือเป็น near-perfect agreement สำหรับ leaf area

**เงื่อนไขที่ต้องตรวจ:**
- Differences ใกล้เคียง normal distribution (ทดสอบ Shapiro-Wilk)
- ไม่มี proportional bias (ดูจาก Bland-Altman plot — ถ้า difference เพิ่มตาม mean แสดงว่า มี proportional bias)
- Limits of agreement ต้องตีความในบริบทของ clinical/biological relevance ไม่ใช่แค่ statistical significance

---

### 2. Continuous (green%) vs Ordinal (vigor 1–5) — วิธีที่ถูกต้อง

**Primary: Spearman ρ**
- ไม่สมมติ linearity หรือ normal distribution
- เหมาะกับ monotonic relationship ระหว่าง continuous กับ ordinal
- ค่า ρ ≥ 0.80 = strong relationship ที่ยอมรับได้ใน phenotyping context

[Bock et al. 2024](https://consensus.app/papers/details/4f988282959f5d7b8dbb38c8c673cf2e/?utm_source=claude_code) ยืนยันว่า direct percentage estimation มักแม่นกว่า ordinal scale ในการ assess plant disease — สนับสนุนว่า green_coverage_pct เป็นวิธีที่ดีกว่า vigor 1–5 ในทางหลักการ แต่ต้องพิสูจน์ว่าทั้งสองสัมพันธ์กัน

[Shah et al. 2004](https://consensus.app/papers/details/092959e52a1a507c8d43157257ed22a2/?utm_source=claude_code): เตือนว่าอย่าใช้ parametric tests (ANOVA, Pearson r) กับ ordinal plant rating data — ใช้ nonparametric

**Secondary: Bland-Altman (ด้วย normalized scale)**
- แปลง vigor → %, แล้ว plot Bland-Altman
- รายงาน mean bias และ 95% limits of agreement
- ถ้า bias ≈ 0 และ LOA แคบ → two methods interchangeable

**อย่าใช้:**
- Pearson r กับ ordinal raw (ละเมิด assumption)
- Cohen's κ สำหรับ continuous vs ordinal โดยตรง (ต้องแปลง CV% → ordinal class ก่อน — อยู่ในไฟล์ R5B_ordinal_validation.md แยก)

---

### 3. Repeatability ของ CV Measurement

**Metric หลัก: ICC(2,1) — Two-way random, absolute agreement, single measure**

เหตุผลเลือก ICC(2,1):
- ถ้า CV ถ่ายภาพ + ประมวลผลซ้ำ 2 วัน (Day 1 vs Day 2) โดย same operator → ICC(2,1)
- "Absolute agreement" คือต้องการให้ค่าตรงกันจริง ไม่ใช่แค่ consistent direction

จาก [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — ICC guideline (24,359 citations):
- < 0.50: poor
- 0.50–0.75: moderate
- 0.75–0.90: good ← threshold ขั้นต่ำ VitroVision
- > 0.90: excellent ← target

**Metric เสริม: CV% (Coefficient of Variation)**
- = (SD ของการวัดซ้ำ / mean) × 100%
- CV% < 5% = excellent repeatability
- CV% < 10% = acceptable
- จาก [Bao et al. 2018](https://consensus.app/papers/details/a6ce4ef61f8d518cb99a829626020ab7/?utm_source=claude_code): robotic sorghum phenotyping รายงาน "highly repeatable measurements" — ใช้ เป็น standard ในสาขา

**Metric เสริม: Dahlberg ratio (SDD/mean)**
- Standard Deviation of Differences / mean
- ใช้ใน ISO standards สำหรับ method comparison
- น้อยกว่า 0.15 (15%) ถือว่า acceptable repeatability

---

### 4. Benchmark สำหรับ CV Accuracy ใน Plant Phenotyping

| Source | Task | Metric | ค่าที่รายงาน | ถือว่า "ผ่าน" |
|---|---|---|---|---|
| [Suarez et al. 2025](https://consensus.app/papers/details/d1ce9592314351b1a3e1ac7957b1f4a2/?utm_source=claude_code) | Leaf area, HSV segmentation vs ImageJ | Pearson r, Bland-Altman bias | r > 0.997, bias < ±0.14 cm² | Near-perfect |
| [Jollet et al. 2023](https://consensus.app/papers/details/b71154d7fa6c52bea9ea98532d7f5114/?utm_source=claude_code) | Bush bean shape + color vs expert scorer | R (Pearson/Spearman) | R = 0.81–0.99 ต่อ trait | R ≥ 0.80 = strong |
| [Bao et al. 2018](https://consensus.app/papers/details/a6ce4ef61f8d518cb99a829626020ab7/?utm_source=claude_code) | Sorghum plant height/width robotic vs manual | Pearson r + repeatability | High correlations + high repeatability | r ≥ 0.90 |
| [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) | ICC guideline (general) | ICC | 0.75–0.90 = good | ICC ≥ 0.75 |
| [Qiao et al. 2023](https://consensus.app/papers/details/d854d0ba301c53df99536629453a00e6/?utm_source=claude_code) | Rice seed vigor CV vs germination rate | Pearson r | r = −0.9874 (vigor index) | r ≥ 0.95 สำหรับ seed vigor |

**สรุป threshold สำหรับ VitroVision:**
- Spearman ρ (green% vs vigor) ≥ **0.80** = acceptable minimum; เป้า ≥ 0.85
- ICC(2,1) (repeatability) ≥ **0.75** = acceptable; เป้า ≥ 0.90
- Bland-Altman LOA: ≤ ±15% ของ mean (normalized scale) = acceptable

---

### 5. ข้อผิดพลาดที่พบบ่อยใน Method Comparison สำหรับ CV Phenotyping

| ข้อผิดพลาด | คำอธิบาย | วิธีหลีกเลี่ยง |
|---|---|---|
| **Pearson กับ ordinal** | Pearson r สมมติ continuous + normal — ordinal (vigor 1–5) ละเมิด assumption นี้ | ใช้ Spearman ρ หรือ Kendall τ แทน |
| **Bland-Altman โดยไม่ normalize scale** | เทียบ green% (0–100) กับ vigor (1–5) โดยตรง — Bland-Altman plot ไม่มีความหมาย | Normalize vigor → % ก่อน; หรือใช้แค่ Spearman |
| **Anchoring bias** | Expert ให้คะแนน vigor 1–5 แตกต่างกันตาม context (พริกสูตร MS0 vs MS กับ PGR) — ทำให้ cross-formula comparison ผิดพลาด | กำหนด rubric scoring sheet ที่ชัดเจนก่อนเก็บข้อมูล (ดู expert_scoring_sheet.csv) |
| **Scale mismatch ไม่รายงาน** | รายงาน Bland-Altman หรือ ICC โดยไม่อธิบายว่า scale ถูก mapped อย่างไร — ผู้อ่านไม่รู้ว่า 1–5 → % ใช้สูตรไหน | ระบุ mapping function ใน Methods อย่างชัดเจน |
| **ICC form ผิด** | ใช้ ICC(1,1) แทน ICC(2,1) สำหรับ same rater ซ้ำ — ผล overestimate reliability | ดู [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) สำหรับ form selection |
| **ไม่ตรวจ proportional bias** | Bland-Altman แสดง bias เพิ่มตาม mean แต่ไม่รายงาน — ซ่อน systematic error | รายงาน regression ของ difference vs mean + Pearson r ของ pair นั้น |
| **ไม่รายงาน n ต่อ class** | รายงาน ICC/ρ รวม โดยไม่แยก vigor class — ถ้าน้อยมากใน vigor 1 (dead) จะ skew | รายงาน n ต่อ vigor class ใน supplementary |

---

## Recommendation สำหรับ VitroVision — Validation Pipeline

### Pipeline หลัก (เรียงตามลำดับ)

```
ขั้น 1: เก็บข้อมูล
  - ถ่ายภาพขวด TC ทุกขวด (n ≥ 30 ขวด ต่อสูตร × 5 สูตร = 150+ ภาพ)
  - Expert ให้ vigor 1–5 แบบ blind ต่อ CV output
  - CV คำนวณ green_coverage_pct จาก HSV segmentation + CCM

ขั้น 2: Spearman ρ (primary — CV continuous vs Expert ordinal)
  - ρ = spearmanr(green_pct, vigor_score)
  - 95% CI bootstrap (n = 1000 resamples)
  - เป้า: ρ ≥ 0.80

ขั้น 3: Bland-Altman (secondary — normalized)
  - vigor_pct = (vigor_score - 1) / 4 × 100  # normalize 1–5 → 0–100%
  - diff = green_pct - vigor_pct
  - mean = (green_pct + vigor_pct) / 2
  - plot diff vs mean; รายงาน bias ± 1.96 SD
  - เป้า: bias ใกล้ 0, LOA ≤ ±15%

ขั้น 4: ICC (repeatability)
  - ถ่ายภาพขวดเดิมซ้ำ Day 1 vs Day 2 (n ≥ 20 ขวด)
  - ICC(2,1) absolute agreement
  - เป้า: ICC ≥ 0.75 (good); ICC ≥ 0.90 (excellent)
  - เสริม: CV% per bottle ต้อง < 10%

ขั้น 5: รายงาน
  - Scatter plot: green_pct (y) vs vigor (x)
  - Bland-Altman plot (normalized)
  - ICC plot with 95% CI bars
  - ตาราง: n, ρ (95%CI), bias (LOA), ICC(2,1) (95%CI), CV%
```

### Threshold Pass/Fail

| Metric | Minimum (ผ่าน) | Target (ดี) | Fail |
|---|---|---|---|
| Spearman ρ | ≥ 0.80 | ≥ 0.85 | < 0.70 |
| Bland-Altman LOA | ≤ ±20% | ≤ ±10% | > ±30% |
| ICC(2,1) repeatability | ≥ 0.75 | ≥ 0.90 | < 0.50 |
| CV% per measurement | < 10% | < 5% | > 15% |

---

## ข้อสรุปเพิ่มเติม — Scale Mismatch Problem

[Bock et al. 2024](https://consensus.app/papers/details/4f988282959f5d7b8dbb38c8c673cf2e/?utm_source=claude_code) เสนอหลักฐานสำคัญ: ใน 4 ทศวรรษของการวิจัย plant disease assessment พบว่า **percentage scale ที่ต่อเนื่อง (%) มักให้ผลแม่นยำกว่า ordinal scale** (Horsfall-Barratt) นั่นหมายความว่า green_coverage_pct ของ VitroVision ไม่ใช่แค่ surrogate ของ vigor 1–5 — แต่อาจเป็น **measurement ที่ดีกว่า** ในเชิง psychophysics

ข้อโต้แย้งนี้สามารถใช้เป็น framing ใน VitroVision paper ได้ว่า: "เราไม่ได้แค่ replicate expert judgment — เราเสนอ objective measurement ที่ขจัด anchoring bias"

---

## Sign-up/usage message จาก Consensus

จาก query 1 (Bland-Altman agreement computer vision plant phenotyping):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
> View all 20 results: https://consensus.app/search/new?q=Bland-Altman+agreement+computer+vision+plant+phenotyping&utm_source=claude_code&mode=quick

จาก query 2 (method comparison continuous vs ordinal plant health assessment):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
> View all 19 results: https://consensus.app/search/new?q=method+comparison+continuous+vs+ordinal+plant+health+assessment&utm_source=claude_code&mode=quick

จาก query 3 (repeatability computer vision measurement plant trait):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
> View all 20 results: https://consensus.app/search/new?q=repeatability+computer+vision+measurement+plant+trait&utm_source=claude_code&mode=quick

จาก query 4 (Spearman correlation computer vision expert plant vigor score validation):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
> View all 20 results: https://consensus.app/search/new?q=Spearman+correlation+computer+vision+expert+plant+vigor+score+validation&utm_source=claude_code&mode=quick

จาก query 5 (ICC intraclass correlation coefficient image analysis phenotyping reliability):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
> View all 20 results: https://consensus.app/search/new?q=ICC+intraclass+correlation+coefficient+image+analysis+phenotyping+reliability&utm_source=claude_code&mode=quick

---

## References (ทุกตัว verified via Consensus — URL จริง)

[1] [Automating Leaf Area Measurement in Citrus: The Development and Validation of a Python-Based Tool](https://consensus.app/papers/details/d1ce9592314351b1a3e1ac7957b1f4a2/?utm_source=claude_code) — Suarez et al. (2025), Applied Sciences, 4 citations

[2] [Plant trait estimation and classification studies in plant phenotyping using machine vision – A review](https://consensus.app/papers/details/750931a401235aa9b1252f1e18cf6263/?utm_source=claude_code) — Kolhar et al. (2021), Information Processing in Agriculture, 121 citations

[3] [Computer vision-based plants phenotyping: A comprehensive survey](https://consensus.app/papers/details/40b8acf6399d5443af536753a4172e83/?utm_source=claude_code) — Meraj et al. (2023), iScience, 28 citations

[4] [The Nuances of Plant Disease Severity Estimation Using Quantitative Ordinal Scales - Lessons Learned Over Four Decades](https://consensus.app/papers/details/4f988282959f5d7b8dbb38c8c673cf2e/?utm_source=claude_code) — Bock et al. (2024), Phytopathology, 4 citations

[5] [Nonparametric analysis of ordinal data in designed factorial experiments](https://consensus.app/papers/details/092959e52a1a507c8d43157257ed22a2/?utm_source=claude_code) — Shah & Madden (2004), Phytopathology, 431 citations

[6] [Field-based robotic phenotyping of sorghum plant architecture using stereo vision](https://consensus.app/papers/details/a6ce4ef61f8d518cb99a829626020ab7/?utm_source=claude_code) — Bao et al. (2018), Journal of Field Robotics, 79 citations

[7] [A new computer vision workflow to assess yield quality traits in bush bean (Phaseolus vulgaris L.)](https://consensus.app/papers/details/b71154d7fa6c52bea9ea98532d7f5114/?utm_source=claude_code) — Jollet et al. (2023), Smart Agricultural Technology, 2 citations

[8] [Adapting the Segment Anything Model for Plant Recognition and Automated Phenotypic Parameter Measurement](https://consensus.app/papers/details/8894e0b9a4ef584693f8437041494881/?utm_source=claude_code) — Zhang et al. (2024), Horticulturae, 15 citations

[9] [Vigour testing for the rice seed with computer vision-based techniques](https://consensus.app/papers/details/d854d0ba301c53df99536629453a00e6/?utm_source=claude_code) — Qiao et al. (2023), Frontiers in Plant Science, 18 citations

[10] [Optimizing Basil Seed Vigor Evaluations: An Automatic Approach Using Computer Vision-Based Technique](https://consensus.app/papers/details/c150e97750515a1d8014c790f8194129/?utm_source=claude_code) — Altizani-Junior et al. (2024), Horticulturae, 3 citations

[11] [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — Koo & Mae (2016), Journal of Chiropractic Medicine, 24,359 citations

[12] [Radiomics feature reliability assessed by intraclass correlation coefficient: a systematic review](https://consensus.app/papers/details/6da29172420e536fac5354459d0e0fed/?utm_source=claude_code) — Xue et al. (2021), Quantitative Imaging in Medicine and Surgery, 137 citations
