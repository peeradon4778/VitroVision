# R5-C: Inter-Rater Agreement — ≥2 Raters & Gold Standard Paradox
**VitroVision / YSC 2027 Research Sub-agent Report**
Date: 2026-06-21 | Agent: R5-C

---

## VERDICT (สรุปก่อนอ่าน)

| คำถาม | คำตอบสั้น |
|---|---|
| ICC ตัวไหน? | **ICC(2,1) absolute agreement** — สำหรับ report inter-rater; ICC(2,k) เสริมถ้า design ใช้ consensus ของ k rater ตลอด |
| วิธีรวม rater เป็น reference | **Median** ของ 2–3 rater (ดีกว่า mean บน ordinal 1–5, immune to outlier) |
| Gold Standard Paradox | รายงาน **"human ceiling"** (ICC ระหว่าง expert) ควบคู่ ICC(CV vs consensus) — ไม่ต้อง Latent Class Analysis สำหรับ YSC |
| กี่ rater พอ? | **2 พอได้** สำหรับ YSC; ≥3 แนะนำในงานวิจัยตีพิมพ์ |
| Precedent plant phenotyping | มี — disease severity scoring ใช้ ≥2 expert มาตลอด (Bock et al. 2010); in vitro plant scoring มี Aynalem et al. 2006 |

---

## 1. ICC(2,1) vs ICC(2,k) — เมื่อไหร่ใช้อะไร

### ตาราง: เลือก ICC model

| ICC Form | Model | Type | ใช้เมื่อ | เกณฑ์ผ่าน |
|---|---|---|---|---|
| **ICC(2,1)** | Two-way random | Absolute agreement | วัด inter-rater ของ **rater แต่ละคน** (ถ้า rater สุ่มมาจาก pool rater ที่ใหญ่กว่า) | ≥0.75 = good, ≥0.90 = excellent |
| **ICC(2,1) mixed** | Two-way mixed | Absolute agreement | วัด inter-rater เมื่อ **rater ชุดนี้คือ rater ที่สนใจ** (fixed raters) — เหมาะสุดสำหรับ VitroVision | ≥0.75 = good |
| **ICC(2,k)** | Two-way | Absolute agreement | วัด reliability ของ **ค่า average/median** ของ k rater — ใช้เมื่อ production pipeline จะ average รวมกันจริงๆ | สูงกว่า ICC(2,1) เสมอ; ≥0.90 |
| ICC(1,1) | One-way | — | ใช้เมื่อไม่สนใจ systematic bias ระหว่าง rater | ไม่แนะนำสำหรับ phenotyping |

**แหล่งอ้างอิง:** Koo & Mae (2016) [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — guideline มาตรฐาน 24,000+ citations; Andrade (2026) [A primer on ICC](https://consensus.app/papers/details/9f77e141e416577d93700393c7459cdb/?utm_source=claude_code) — ยืนยัน: "For most inter-rater reliability, the two-way mixed model for single measures, absolute agreement"

### สรุปสำหรับ VitroVision

```
report ทั้ง 2 ค่า:
  ICC(2,1) absolute agreement  → inter-rater ของ rater แต่ละคน ("เพดาน")
  ICC(2,k) absolute agreement  → reliability ของ consensus k รอบ → ใช้เป็น target ของ CV
```

---

## 2. วิธีรวม ≥2 Rater เป็น Reference Standard

### เปรียบเทียบวิธี

| วิธี | เหมาะกับ | ข้อดี | ข้อเสีย |
|---|---|---|---|
| **Median** | Ordinal 1–5 | Robust vs outlier; ไม่ถูก rater ที่ bias ดึง | อาจได้ .5 ถ้า 2 rater ให้ต่างกัน 1 ระดับ |
| Mean | Continuous / interval | คำนวณง่าย | ใน ordinal 1–5 อาจได้ 2.33 — ไม่ใช่ category จริง |
| Majority vote | Nominal/categorical | ชัดเจน | ต้องมีคี่ rater; ไม่ดีถ้า tie |
| Clinically adjudicated | สูตรซับซ้อน | Valid ที่สุด | ต้องใช้ panel discuss; ใช้เวลามาก |

**แหล่งอ้างอิง:** 
- Patel et al. (2022) [Clinically Adjudicated Reference Standards](https://consensus.app/papers/details/20bbe817a6b15c759e804dd750762ca6/?utm_source=claude_code) — อธิบาย consensus panel approach; ใช้ใน infectious disease diagnostics
- Marasini et al. (2016) [Assessing inter-rater agreement for ordinal data through weighted indexes](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code) — ยืนยัน ordinal data ต้องใช้ weighted statistics

### คำแนะนำ VitroVision (vigor 1–5):

- **ถ้า 2 rater**: ถ้า agree → ใช้ค่านั้น; ถ้า differ by 1 → median = .5 → round ลง (conservative) หรือให้ rater 3 ตัดสิน
- **ถ้า 3 rater**: median ชัดเจนเสมอ — แนะนำเพิ่ม rater 3 สำหรับ final validation set

---

## 3. Gold Standard Paradox / Imperfect Reference Standard

### คืออะไร

ถ้า expert เองก็ไม่ agree 100% → reference standard ที่ใช้ก็ "imperfect" → ถ้า CV ไม่ตรงกับ reference อาจเป็นเพราะ noise ใน reference ไม่ใช่ CV ผิด

### วิธีจัดการ (spectrum จากง่ายไปยาก)

| ระดับ | วิธี | เหมาะกับ | ต้องทำสำหรับ YSC? |
|---|---|---|---|
| **1 (พอสำหรับ YSC)** | รายงาน ICC ระหว่าง expert (human ceiling) ควบคู่ ICC(CV vs consensus) | งาน competition / report ที่โปร่งใส | **ใช่ — ทำแค่นี้พอ** |
| 2 | Correction formula (Sensitivity/Specificity adjustment) | diagnostic test accuracy, known imperfect reference | ไม่จำเป็น |
| 3 | **Latent Class Analysis (LCA)** | สถานการณ์ที่ไม่มี gold standard เลย; ≥3 raters/tests | ซับซ้อนเกินสำหรับ YSC |
| 4 | Bayesian hierarchical LCA | งานวิจัยตีพิมพ์ขั้นสูง | ไม่จำเป็น |

**แหล่งอ้างอิง:**
- Umemneku et al. (2019) [Diagnostic test evaluation in absence of gold standard](https://consensus.app/papers/details/85fbe8d0e23f54469735ff8d4cd9dd07/?utm_source=claude_code) — systematic review 51 วิธี; ยืนยันว่า correction methods มี complexity สูงและ clinical application จำกัด
- Uebersax & Grove (1990) [Latent class analysis of diagnostic agreement](https://consensus.app/papers/details/e149a11bb52158a188e2f0c427cde64a/?utm_source=claude_code) — foundation paper ของ LCA approach
- Albert & Dodd (2008) [Estimating diagnostic accuracy with multiple raters and partial gold standard](https://consensus.app/papers/details/a3f230d3a5a75fbf99dcbecd467bab14/?utm_source=claude_code) — เตือนว่า LCA bias สูงถ้า dependence structure ผิด

### วิธีรายงาน Gold Standard Paradox สำหรับ VitroVision / YSC

```
ตัวอย่างข้อความในรายงาน:
"Inter-rater agreement ระหว่าง expert (human ceiling): ICC(2,1) = X.XX [95% CI: X.XX–X.XX]
CV vs consensus: ICC(2,1) = X.XX [95% CI: X.XX–X.XX]
CV สามารถทำได้ X% ของ human ceiling ซึ่งบ่งชี้ว่าความแตกต่างที่เหลือสะท้อน
inherent variability ของ visual assessment ไม่ใช่ error ของ CV"
```

---

## 4. กี่ Rater พอ?

### หลักฐาน

- **2 rater** — เป็น minimum ที่ยอมรับได้ในวรรณกรรม; ใช้ ICC two-way ได้
- **3 rater** — แนะนำสำหรับ ordinal scale เพื่อให้ median ชัดเจน; ช่วยแก้ tie
- ไม่มีหลักฐานว่าต้อง ≥4 สำหรับ phenotyping scale 5-point

**แหล่งอ้างอิง:**
- Saito et al. (2006) [Effective number of subjects and raters for inter-rater reliability](https://consensus.app/papers/details/f6982131d55b51d7aefe45cbac5e6955/?utm_source=claude_code) — วิเคราะห์ว่า optimal design ขึ้นกับ between-rater variance; 2 rater ใช้ได้แต่ precision ต่ำกว่า
- Vanbelle et al. (2024) [Comprehensive guide for multi-observer ordinal data](https://consensus.app/papers/details/bda06793b9915d6ea4783677845b42a6/?utm_source=claude_code) — ให้ R package สำหรับคำนวณ minimum sample size

### คำแนะนำ VitroVision:

- **Phase 1 (pilot):** 2 expert รater พอสำหรับ establish ICC
- **Phase 2 (validation):** เพิ่ม rater ที่ 3 สำหรับ subset เพื่อ confirm median stability

---

## 5. Precedent ใน Plant Phenotyping / Tissue Culture

### Paper ที่ใช้ ≥2 Expert Validate Image Scoring

| Paper | Domain | รายละเอียด | URL |
|---|---|---|---|
| Bock et al. (2010) | Plant disease severity | Classic review — ยืนยัน inter-rater และ intrarater variability เป็น core challenge; image analysis ช่วยลด subjectivity; ≥2 rater มาตรฐาน | [Link](https://consensus.app/papers/details/0eed3dce2a225af296ce79274426cc95/?utm_source=claude_code) |
| Aynalem et al. (2006) | In vitro plant (pear TC) | เปรียบ visual rating vs digital image analysis บน in vitro stored plantlets; ใช้ visual rating + correlation กับ image metrics (MNDVI, G/R) | [Link](https://consensus.app/papers/details/33f703b3d5ba5ee985dffa052c1a81e7/?utm_source=claude_code) |
| Ghosal et al. (2018) | Soybean disease (DL) | อธิบาย inter- และ intrarater cognitive variability เป็น motivation ของ CV/ML; expert subjectivity = แรงผลักดันหลัก | [Link](https://consensus.app/papers/details/8842eb126cb35b4abc4b67f33c8fa781/?utm_source=claude_code) |
| Singh et al. (2020) | Plant stress phenotyping | Machine-augmented phenotyping — standardization ของ visual assessments เป็น prerequisite ก่อนใช้ ML | [Link](https://consensus.app/papers/details/8df18446a70553b3bdb60943116d7b87/?utm_source=claude_code) |

---

## 6. คำแนะนำปฏิบัติสำหรับ VitroVision

### Protocol ที่แนะนำ

```
Step 1: Expert rating session (blind)
  - Expert A และ B ให้คะแนน vigor 1–5 แยกกัน บนขวดชุดเดียวกัน (n ≥ 50 ขวด)
  - ไม่บอกว่าอีกคนให้คะแนนเท่าไหร่

Step 2: คำนวณ Human Ceiling
  - ICC(2,1) absolute agreement ระหว่าง Expert A vs B
  - Weighted Kappa (linear weights) สำหรับ ordinal — เป็น supplementary
  - รายงาน 95% CI เสมอ

Step 3: สร้าง Reference Standard
  - Consensus = median(A, B) [ถ้า tie → แก้โดยเพิ่ม Expert C หรือ round down]

Step 4: วัด CV vs Reference
  - ICC(2,1) ของ CV score vs consensus median
  - ICC(2,k) ของ CV score vs consensus median (k=2 rater)
  - รายงาน: "CV ทำได้ XX% ของ human ceiling"

Step 5: Gold Standard Paradox — ระบุในรายงาน
  - ถ้า ICC(CV) < ICC(human): "CV ยังมีช่องว่างจาก human ceiling แต่ human ceiling เอง = X.XX ไม่ใช่ 1.0"
  - ถ้า ICC(CV) ≥ ICC(human): "CV มี consistency ≥ human rater individual"
```

### เกณฑ์ตัดสิน (Koo & Mae 2016)

| ICC value | interpretation |
|---|---|
| < 0.50 | Poor |
| 0.50 – 0.74 | Moderate |
| 0.75 – 0.89 | Good |
| ≥ 0.90 | Excellent |

---

## 7. ข้อควรระวัง

1. **อย่า report ICC โดยไม่บอก model/type** — ผู้อ่านจะตีความผิด (Koo & Mae 2016)
2. **Weighted Kappa แทน ICC** ก็ได้สำหรับ ordinal — แต่ ICC ใช้ได้กับ "quasi-continuous" ordinal (vigor 1–5) และ interpret ง่ายกว่า
3. **Systematic bias** ระหว่าง rater (เช่น Expert A ให้คะแนนสูงกว่าเสมอ) → ควรรายงาน mean difference ด้วย ไม่ใช่แค่ ICC consistency
4. **LCA ไม่จำเป็นสำหรับ YSC** — complexity สูง, ต้องการ ≥3 tests, และ bias risk สูงถ้า model ผิด (Albert & Dodd 2008) → รายงาน ceiling แบบ transparent พอ
5. **Sample size** — ควรมี ≥30–50 ขวดสำหรับ ICC estimate ที่ stable (95% CI ไม่กว้างเกิน)

---

## อ้างอิงทั้งหมด (verified จาก Consensus)

1. Koo & Mae (2016) — [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — J Chiropr Med, 24,359 citations
2. Andrade (2026) — [A primer on the intraclass correlation coefficient as a measure of reliability in medical research](https://consensus.app/papers/details/9f77e141e416577d93700393c7459cdb/?utm_source=claude_code) — Indian J Psychiatry
3. Benchoufi et al. (2020) — [Interobserver agreement issues in radiology](https://consensus.app/papers/details/f8c96df426f856c98931cd9a04f821c0/?utm_source=claude_code) — Diagn Interv Imaging, 288 citations
4. Umemneku et al. (2019) — [Diagnostic test evaluation in the absence of gold standard](https://consensus.app/papers/details/85fbe8d0e23f54469735ff8d4cd9dd07/?utm_source=claude_code) — PLoS ONE, 161 citations
5. Zhao et al. (2022) — [Interrater reliability estimators tested against true interrater reliabilities](https://consensus.app/papers/details/c0e5ba15fc835263bb3a3beee686af28/?utm_source=claude_code) — BMC Med Res Methodol, 56 citations
6. Patel et al. (2022) — [Clinically Adjudicated Reference Standards for Evaluation of Infectious Diseases Diagnostics](https://consensus.app/papers/details/20bbe817a6b15c759e804dd750762ca6/?utm_source=claude_code) — Clin Infect Dis, 23 citations
7. Marasini et al. (2016) — [Assessing inter-rater agreement for ordinal data through weighted indexes](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code) — Stat Methods Med Res, 97 citations
8. Uebersax & Grove (1990) — [Latent class analysis of diagnostic agreement](https://consensus.app/papers/details/e149a11bb52158a188e2f0c427cde64a/?utm_source=claude_code) — Stat Med, 144 citations
9. Albert & Dodd (2008) — [Estimating Diagnostic Accuracy with Multiple Raters and Partial Gold Standard](https://consensus.app/papers/details/a3f230d3a5a75fbf99dcbecd467bab14/?utm_source=claude_code) — J Am Stat Assoc, 47 citations
10. Saito et al. (2006) — [Effective number of subjects and raters for inter-rater reliability](https://consensus.app/papers/details/f6982131d55b51d7aefe45cbac5e6955/?utm_source=claude_code) — Stat Med, 78 citations
11. Vanbelle et al. (2024) — [Comprehensive guide for multi-observer ordinal data](https://consensus.app/papers/details/bda06793b9915d6ea4783677845b42a6/?utm_source=claude_code) — BMC Med Res Methodol, 17 citations
12. Liljequist et al. (2019) — [Intraclass correlation — discussion and demonstration of basic features](https://consensus.app/papers/details/4e405215b70a567caffa4271ad95cc90/?utm_source=claude_code) — PLoS ONE, 796 citations
13. Bock et al. (2010) — [Plant Disease Severity Estimated Visually, by Digital Photography and Image Analysis](https://consensus.app/papers/details/0eed3dce2a225af296ce79274426cc95/?utm_source=claude_code) — Crit Rev Plant Sci, 823 citations
14. Aynalem et al. (2006) — [Non-destructive evaluation of in vitro-stored plants: visual and image analysis](https://consensus.app/papers/details/33f703b3d5ba5ee985dffa052c1a81e7/?utm_source=claude_code) — In Vitro Cell Dev Biol Plant, 19 citations
15. Ghosal et al. (2018) — [An explainable deep machine vision framework for plant stress phenotyping](https://consensus.app/papers/details/8842eb126cb35b4abc4b67f33c8fa781/?utm_source=claude_code) — PNAS, 468 citations
16. Singh et al. (2020) — [Challenges and Opportunities in Machine-Augmented Plant Stress Phenotyping](https://consensus.app/papers/details/8df18446a70553b3bdb60943116d7b87/?utm_source=claude_code) — Trends Plant Sci, 187 citations

---

*ทุก citation ผ่าน Consensus search — มี URL จริง. ห้ามเพิ่ม citation ใหม่ที่ไม่ผ่านไฟล์นี้ก่อน verify ใน _citation_audit.md*
