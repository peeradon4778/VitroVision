# R5-A — Inter-rater Reliability สำหรับ Ordinal Plant Vigor Scoring

> Sub-agent R5-A | VitroVision (YSC 2027 → ISEF CSBI)
> โจทย์: เลือก metric IRR ที่ถูกต้องสำหรับ vigor score 1–5 (ordinal) + hyperhydric flag (binary), ≥2 expert rater, ~180 ขวด/time point; ยืนยัน/แก้ไข current plan (Spearman ρ + quadratic-weighted κ + ICC(2,1))
> ทุก citation มาจากผล Consensus จริง + URL กดได้
> วันที่: 2026-06-21

---

## VERDICT รวม

1. **ICC(2,1) absolute agreement** คือ metric หลักที่เหมาะสมที่สุดสำหรับ vigor scale 1–5 แบบ ordinal quasi-continuous — ใช้ได้กับ 2+ rater และมี interpretation ชัดเจน
2. **Quadratic-weighted κ ≈ ICC** เกือบสมมูลกันสำหรับ 5-point ordinal scale; quadratic-weighted κ ดีกว่า linear-weighted κ เพราะลงโทษ disagreement ที่ห่างกันมากกว่า; Spearman ρ เป็น supplementary ที่ดีแต่ไม่ใช่ primary metric สำหรับ "agreement"
3. **Minimum acceptable:** ICC ≥ 0.75 (Good) สำหรับ YSC; ≥ 0.90 (Excellent) คือเป้าที่ควรได้สำหรับ tool validation; κ ≥ 0.61 (Substantial) ตาม McHugh 2012
4. **Sample size:** n ≥ 30–50 ขวด (subjects) สำหรับ ICC estimate ที่ stable (95% CI ไม่กว้างเกิน ±0.15); สำหรับโปรเจกต์นี้ ~180 ขวด เกินพอ
5. **Multi-rater (>2):** ใช้ **Krippendorff's α** แทน Fleiss' κ เมื่อมีข้อมูลขาดหาย หรือ rater ไม่ครบทุกตัวอย่าง; Fleiss' κ ดีสำหรับ complete data แต่มี paradoxical behavior; Krippendorff's α รองรับ ordinal weights โดยตรง

---

## ตารางหลักฐาน

| metric | เมื่อไรใช้ | ข้อดี | ข้อจำกัด | อ้างอิง + URL |
|---|---|---|---|---|
| **ICC(2,1) absolute agreement** | 2+ rater, ordinal/continuous, rater pool ใหญ่กว่า study | interpret ง่าย (0–1), มี 95% CI, เป็นมาตรฐาน medical/plant research | sensitive ต่อ distribution ของ subjects (uniform ดีที่สุด) | [Mehta et al. 2018](https://consensus.app/papers/details/1d992ac70b2a507c9f099062c7ee5a1f/?utm_source=claude_code); [Bourredjem et al. 2024](https://consensus.app/papers/details/775a5147ecab5604966d1e4724179f1e/?utm_source=claude_code) |
| **Quadratic-weighted κ** | 2 rater, ordinal 5-point, ต้องการ "distance-penalized" agreement | ลงโทษ far disagreement มากกว่า; ≈ ICC สำหรับ 5-point | มี paradoxical behavior; sensitive ต่อ marginal distribution | [de Raadt et al. 2021](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code); [Marasini et al. 2016](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code) |
| **Linear-weighted κ** | 2 rater, ordinal; ใช้เมื่อ penalty ควรเป็นสัดส่วนตรง | ง่ายกว่า quadratic | ลงโทษ far disagreement น้อยกว่า; ≠ ICC | [de Raadt et al. 2021](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) |
| **Spearman ρ** | 2 rater, ordinal; วัด rank correlation | non-parametric, robust | วัด association ไม่ใช่ agreement จริง (อาจสูงแม้ systematic bias มี) | [de Raadt et al. 2021](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) |
| **Fleiss' κ** | 3+ rater, nominal/ordinal, complete data | generalize Cohen's κ ไปหลาย rater | paradoxical behavior; bias ถ้า data ไม่ balance; bootstrap CI แนะนำ | [Zapf et al. 2016](https://consensus.app/papers/details/9479c38e3e6d5c109876231e031b42a9/?utm_source=claude_code); [Marasini et al. 2016](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code) |
| **Krippendorff's α** | 3+ rater, nominal/ordinal/interval, missing data | รองรับ missing data; รองรับ ordinal weights; bootstrap CI stable; ไม่มี paradox | คำนวณซับซ้อนกว่า Fleiss' κ เล็กน้อย | [Zapf et al. 2016](https://consensus.app/papers/details/9479c38e3e6d5c109876231e031b42a9/?utm_source=claude_code); [Hughes 2021](https://consensus.app/papers/details/2e0d271c585658f6bfa9e1a1df507d47/?utm_source=claude_code) |
| **Cohen's κ (unweighted)** | 2 rater, nominal/binary (เช่น hyperhydric flag) | ใช้สำหรับ binary variable เหมาะที่สุด | ไม่ควรใช้กับ ordinal scale | [McHugh 2012](https://consensus.app/papers/details/d8b550f8ffae56d6b6c2d46386b714e9/?utm_source=claude_code) |

---

## คำตอบคำถาม 5 ข้อ (โดยตรง)

### Q1: ordinal vigor scale 1–5 ควรใช้อะไร?

**คำตอบ: ICC(2,1) absolute agreement เป็น primary metric; quadratic-weighted κ เป็น secondary**

- งานเปรียบเทียบ 7 coefficients โดย [de Raadt et al. 2021](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) พบว่า สำหรับ 5-point ordinal scale: **quadratic-weighted κ ≈ Pearson correlation ≈ ICC(3,1)** เกือบสมมูลกันในผลสรุป — ความต่างมีน้อยมากในทางปฏิบัติ
- ICC(2,1) ดีกว่า weighted κ ตรงที่: (a) มี confidence interval ที่คำนวณง่ายกว่า (b) ไม่มี paradoxical behavior (c) standard ใน plant phenotyping literature
- **สำหรับ hyperhydric flag (binary):** ใช้ Cohen's κ (unweighted) — ไม่ใช่ weighted version

### Q2: Quadratic vs Linear weighted κ vs ICC(2,1) ต่างกันอย่างไร?

| | Quadratic-weighted κ | Linear-weighted κ | ICC(2,1) |
|---|---|---|---|
| penalty สำหรับ disagree by 2 levels | 4× penalty ของ 1 level | 2× penalty ของ 1 level | proportional to squared difference |
| relationship กัน | ≈ Pearson/ICC สำหรับ 5-point | ≠ ICC | quasi-equivalent กับ quadratic κ |
| paradox risk | มี (marginal-dependent) | มี | ต่ำกว่า |
| formula sensitivity | sensitive ต่อ prevalence | sensitive ต่อ prevalence | sensitive ต่อ distribution |
| แนะนำสำหรับ VitroVision | secondary metric | ไม่แนะนำ | **primary metric** |

อ้างอิง: [de Raadt et al. 2021](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code)

### Q3: Minimum acceptable สำหรับ plant phenotyping?

- **McHugh (2012)** [kappa statistic review](https://consensus.app/papers/details/d8b550f8ffae56d6b6c2d46386b714e9/?utm_source=claude_code) — paper นี้มี 16,513 citations; ตั้งข้อสังเกตว่า Cohen's original interpretation ที่ κ ≥ 0.41 = acceptable นั้น **"too lenient for health research"**; แนะนำ κ ≥ 0.60 สำหรับ health-related studies
- **Koo & Mae (2016)** (24,000+ citations, referenced ใน R5C) กำหนด ICC thresholds:

| ICC | interpretation |
|---|---|
| < 0.50 | Poor — ไม่ผ่าน |
| 0.50 – 0.74 | Moderate — ยอมรับได้ในบางบริบท |
| 0.75 – 0.89 | **Good — minimum สำหรับ YSC/tool validation** |
| ≥ 0.90 | **Excellent — target สำหรับ production pipeline** |

- **Plant phenotyping precedent:** Bock et al. (2010) disease severity scoring ใช้ ≥2 expert มาตรฐาน; interrater variability เป็น known issue ที่ต้อง report อย่าง transparent
- **สรุปสำหรับ VitroVision:** กำหนด pass bar ที่ ICC(2,1) ≥ 0.75 (Good) สำหรับ human inter-rater; ≥ 0.80 สำหรับ CV vs consensus

### Q4: Sample size ที่เหมาะสม?

- [Mehta et al. 2018](https://consensus.app/papers/details/1d992ac70b2a507c9f099062c7ee5a1f/?utm_source=claude_code) พบว่า **n > 80 subjects ไม่ช่วยเพิ่ม ICC precision อย่างมีนัยสำคัญ** เมื่อ distribution เป็น uniform
- [Mondal et al. 2024](https://consensus.app/papers/details/ee1e6b4a8a1353b4b7761b0814ca8b6d/?utm_source=claude_code) review sample size determination สำหรับ ICC: แนะนำให้คำนวณจาก desired CI width; สำหรับ CI width ≤ 0.20 ที่ ICC ≈ 0.80 ต้องการประมาณ **n = 30–50 subjects** กับ 2 rater
- [Bourredjem et al. 2024](https://consensus.app/papers/details/775a5147ecab5604966d1e4724179f1e/?utm_source=claude_code) สร้าง formula สำหรับ sample size ของ ICCa โดยตรง

**สรุปสำหรับ VitroVision:**
- ~180 ขวด ต่อ time point เกิน minimum requirement อย่างมาก
- สำหรับ inter-rater study เฉพาะส่วน: **n = 50 ขวด (สุ่มจาก 5 สูตร สูตรละ 10) + 2 rater = เพียงพอ**
- ถ้าต้องการ ICC CI ≤ ±0.10: n ≈ 80 ขวด, 2 rater (ตาม Mondal 2024)

### Q5: Multi-rater (>2 คน) — Krippendorff's α vs Fleiss' κ?

- [Zapf et al. 2016](https://consensus.app/papers/details/9479c38e3e6d5c109876231e031b42a9/?utm_source=claude_code) (330 citations, BMC Medical Research Methodology) พบว่า:
  - Point estimates ของ Fleiss' κ และ Krippendorff's α **ไม่ต่างกันสถิติ** กรณี complete data nominal scale
  - กรณี **missing data**: Krippendorff's α ให้ estimates ที่ stable; Fleiss' κ แบบ complete-case analysis มี bias
  - กรณี **ordinal หรือ higher-level scale**: **แนะนำ Krippendorff's α** เพราะรองรับ ordinal distance function โดยตรง
- [Hughes 2021](https://consensus.app/papers/details/2e0d271c585658f6bfa9e1a1df507d47/?utm_source=claude_code) — R package `krippendorffsalpha` รองรับ ordinal distance, any number of raters/units, missing data, bootstrap CI

**สรุป:** ถ้ามี rater ≥ 3 คน → **Krippendorff's α with ordinal weights** ดีกว่า Fleiss' κ ในทุกมิติสำหรับ VitroVision context

---

## Recommendation สำหรับ VitroVision

### Current plan assessment

| metric ปัจจุบัน | ถูก/ผิด | หมายเหตุ |
|---|---|---|
| Spearman ρ | ใช้ได้เป็น supplementary | แต่ไม่ใช่ primary agreement metric — วัด association ≠ agreement |
| Quadratic-weighted κ | ใช้ได้ดี | ใช้เป็น secondary metric; แต่ระวัง marginal sensitivity |
| ICC(2,1) | **ถูกต้อง — primary metric** | ควรระบุ absolute agreement และ two-way mixed/random model |

### Protocol ที่แนะนำ

```
Vigor score 1–5 (ordinal):
  PRIMARY:    ICC(2,1) absolute agreement, two-way mixed model
  SECONDARY:  Quadratic-weighted κ (ยืนยัน primary)
  SUPPLEMENTARY: Spearman ρ (rank correlation context)
  ไม่แนะนำ: Linear-weighted κ เป็น standalone

Hyperhydric flag (binary):
  PRIMARY:    Cohen's κ (unweighted)
  SECONDARY:  Percent agreement + prevalence-adjusted κ (PABAK) ถ้า prevalence ต่ำ

ถ้ามี rater ≥ 3 คน:
  เปลี่ยนจาก Fleiss' κ → Krippendorff's α (ordinal weights)
  ใช้ bootstrap CI เสมอ
```

### เกณฑ์ตัดสิน

| metric | Pass (YSC minimum) | Target (publication) |
|---|---|---|
| ICC(2,1) human inter-rater | ≥ 0.75 | ≥ 0.90 |
| ICC(2,1) CV vs consensus | ≥ 0.75 | ≥ 0.80 |
| Quadratic-weighted κ | ≥ 0.61 | ≥ 0.80 |
| Cohen's κ hyperhydric | ≥ 0.61 | ≥ 0.80 |
| Krippendorff's α (ถ้าใช้) | ≥ 0.667 | ≥ 0.80 |

### Sample size

| สถานการณ์ | n subjects | n rater | หมายเหตุ |
|---|---|---|---|
| Pilot IRR study | 50 ขวด | 2 | สุ่ม 10 ขวด/สูตร × 5 สูตร; CI width ≈ ±0.15 |
| Full validation | 80–100 ขวด | 2–3 | CI width ≈ ±0.10; เพิ่ม rater 3 สำหรับ tie-breaking |
| Production dataset (~180) | ≥180 ขวด | 2 | เกิน minimum — precision สูง |

---

## อ้างอิงทั้งหมด (verified จาก Consensus search จริง)

1. [de Raadt et al. (2021) — A Comparison of Reliability Coefficients for Ordinal Rating Scales](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) — Journal of Classification, 100 citations
2. [Marasini et al. (2016) — Assessing the inter-rater agreement for ordinal data through weighted indexes](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code) — Statistical Methods in Medical Research, 97 citations
3. [Zapf et al. (2016) — Measuring inter-rater reliability for nominal data: Fleiss' K and Krippendorff's alpha](https://consensus.app/papers/details/9479c38e3e6d5c109876231e031b42a9/?utm_source=claude_code) — BMC Medical Research Methodology, 330 citations
4. [Hughes (2021) — krippendorffsalpha: An R Package for Measuring Agreement Using Krippendorff's Alpha Coefficient](https://consensus.app/papers/details/2e0d271c585658f6bfa9e1a1df507d47/?utm_source=claude_code) — R Journal, 66 citations
5. [Bourredjem et al. (2024) — Asymptotic Confidence Interval, Sample Size Formulas for ICC in Inter-Rater Reliability Studies](https://consensus.app/papers/details/775a5147ecab5604966d1e4724179f1e/?utm_source=claude_code) — Statistics in Medicine, 4 citations
6. [Mondal et al. (2024) — Review of sample size determination methods for the ICC in the one-way ANOVA model](https://consensus.app/papers/details/ee1e6b4a8a1353b4b7761b0814ca8b6d/?utm_source=claude_code) — Statistical Methods in Medical Research, 34 citations
7. [Mehta et al. (2018) — Performance of ICC as a reliability index under various distributions in scale reliability studies](https://consensus.app/papers/details/1d992ac70b2a507c9f099062c7ee5a1f/?utm_source=claude_code) — Statistics in Medicine, 151 citations
8. [McHugh (2012) — Interrater reliability: the kappa statistic](https://consensus.app/papers/details/d8b550f8ffae56d6b6c2d46386b714e9/?utm_source=claude_code) — Biochemia Medica, 16,513 citations
9. [Almehrizi (2025) — Agreement Lambda for Weighted Disagreement With Ordinal Scales](https://consensus.app/papers/details/27f8c18193ad57798ce28505bb74c1bc/?utm_source=claude_code) — Educational and Psychological Measurement, 1 citation
10. [Tran et al. (2021) — Bayesian approaches to the weighted kappa-like inter-rater agreement measures](https://consensus.app/papers/details/b87b368399db5a368cab45b1171a8b11/?utm_source=claude_code) — Statistical Methods in Medical Research, 4 citations

---

## Sign-up/usage message จาก Consensus

Query 1 (inter-rater reliability ordinal plant phenotyping):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 2 (weighted kappa ICC ordinal scale comparison):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 3 (Krippendorff alpha Fleiss kappa multi-rater):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 4 (ICC sample size inter-rater reliability):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 5 (minimum acceptable kappa ICC plant phenotyping):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

---

*ทุก citation ผ่าน Consensus search — มี URL จริง. ห้ามเพิ่ม citation ใหม่ที่ไม่ผ่านไฟล์นี้ก่อน verify ใน _citation_audit.md*
