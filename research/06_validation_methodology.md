# 06 — Validation Methodology สำหรับ VitroVision

> **สถานะ:** Draft v1 | วันที่สร้าง: 2026-06-11
> **วัตถุประสงค์:** รวบรวม evidence base สำหรับการเลือก validation metrics เมื่อ validate ระบบ CV เทียบกับ expert ordinal score (gold standard)
> **โปรเจกต์:** VitroVision — Computational Phenotyping ของ *Capsicum annuum* in vitro tissue culture (YSC 2027 / CSBI)

---

## 1. สรุปภาพรวม (Executive Summary)

การ validate ระบบ image analysis เทียบกับ expert visual rating นั้นมีความซับซ้อน 3 ชั้น:

1. **ความแตกต่างระหว่าง correlation กับ agreement** — Spearman ρ วัดว่า rank ขึ้น-ลงไปด้วยกันไหม แต่ไม่บอกว่าค่าตรงกันจริงหรือเปล่า [6] ขณะที่ ICC absolute agreement และ quadratic-weighted κ วัด agreement ที่แท้จริง
2. **Gold Standard Paradox** — expert score เองก็มี bias โดยธรรมชาติ ดังนั้นถ้า CV system "ตรงกับ expert" ไม่ได้แปลว่า CV ผิด — อาจแปลว่า CV objective กว่า [3]
3. **ลำดับขั้นของ validation** — ต้องวัด inter-rater agreement ระหว่าง expert ≥2 คนก่อน เพื่อกำหนด ceiling (ขีดสูงสุดที่สมเหตุสมผล) ก่อนเปรียบ CV กับ expert

**Decision สำหรับ VitroVision:** ใช้ **Spearman ρ (primary) + quadratic-weighted κ + ICC(2,1) absolute agreement** เป็น metric suite ซึ่งสอดคล้องกับ best practice ที่ de Raadt et al. 2021 แนะนำ [1]

---

## 2. แต่ละ Metric ใช้เมื่อไหร่และทำไม

### 2.1 Spearman ρ — Rank Correlation (Primary Metric)

**ใช้เมื่อ:** ข้อมูลเป็น ordinal scale, ไม่มีสมมติฐาน normal distribution, ต้องการวัดความสัมพันธ์แบบ monotonic

**ข้อดี:**
- Robust ต่อ outlier และ non-normal distribution [4]
- เหมาะกับ ordinal score ที่ interval ระหว่าง grade ไม่เท่ากัน (เช่น Grade 1→2 ≠ Grade 4→5 ในแง่ phenotypic change)
- Interpretation ตรงไปตรงมาสำหรับ judge/panel ของ YSC

**ข้อจำกัดสำคัญ:**
- ρ สูงไม่ได้หมายความว่า agreement ดี — rater A อาจ rate [1,2,3,4] ขณะ rater B rate [2,3,4,5] ซึ่งให้ ρ = 1.0 แต่ agreement = 0 [6]
- Svensson 2012 เตือนว่า "a measure of association must not be used as a measure of agreement, even though such misuse of correlation coefficients is common" [6]

**ดังนั้น:** ต้องรายงาน Spearman ρ คู่กับ metric ที่วัด agreement จริงเสมอ

**A priori threshold (VitroVision):**
- Acceptable: ρ ≥ 0.70
- Target/Excellent: ρ ≥ 0.85

---

### 2.2 Quadratic-Weighted κ (Cohen's Kappa, Quadratic Weights)

**ใช้เมื่อ:** ข้อมูล ordinal categorical ≥3 ระดับ, ต้องการ penalize disagreement ที่ห่างกันมากกว่าห่างกันน้อย

**หลักการ:** Quadratic weighting ให้ penalty = (i−j)²/(k−1)² โดยที่ i,j = ระดับของ rater แต่ละคน, k = จำนวน category รวม — disagreement ห่าง 2 step ถูก penalize 4× มากกว่า disagreement 1 step

**ข้อดี:**
- มี chance-correction ซึ่ง percent agreement ไม่มี [7]
- เหมาะกับกรณีที่ distribution ของ label ไม่สมดุล (prevalence bias)
- de Raadt 2021 แสดงว่า quadratic-weighted κ ให้ผลสรุปที่ใกล้เคียงกับ ICC และ Pearson correlation "a great number of times" [1]

**ข้อจำกัด:**
- Sensitive ต่อ prevalence (ถ้า label กระจุกที่ grade ใด grade หนึ่งมาก κ จะต่ำกว่าที่ควร)
- Li et al. 2023 เน้นว่าต้องระบุชัดว่าใช้ unweighted / linear-weighted / quadratic-weighted เพราะให้ค่าต่างกันมาก [5]

**A priori threshold (VitroVision):**
- Acceptable: κ ≥ 0.60 (Landis & Koch: substantial agreement)
- Target: κ ≥ 0.80 (almost perfect)

---

### 2.3 ICC(2,1) — Two-Way Mixed, Absolute Agreement, Single Measures

**ใช้เมื่อ:** ต้องการวัด absolute agreement (ไม่ใช่แค่ consistency) และ rater ถูก sample มาจาก population ของ expert ที่กว้างกว่า

**ความแตกต่าง ICC model ที่สำคัญ:**

| Model | เมื่อใช้ |
|---|---|
| ICC(1,1) One-way random | rater แต่ละคน rate คนละ subject (ไม่เกี่ยวกับ VitroVision) |
| ICC(2,1) Two-way mixed, absolute | **รูปแบบที่ VitroVision ใช้** — rater เดิมทุกคน rate ทุก sample, ต้องการ absolute agreement |
| ICC(3,1) Two-way mixed, consistency | ไม่ต้องการ absolute agreement, ยอมรับ systematic offset ระหว่าง rater |

Koo & Li 2016 กำหนด guideline ที่อ้างอิงกันอย่างกว้างขวาง (24,121 citations): [2]
- ICC < 0.50 = poor reliability
- 0.50–0.75 = moderate reliability
- **0.75–0.90 = good reliability**
- ICC > 0.90 = excellent reliability

**เหตุผลที่เลือก ICC(2,1) absolute แทน consistency:**
- "Absolute agreement" คือถาม "ถ้า expert A ให้ 3 แต่ CV ให้ 5 ถือว่าตรงไหม?" — คำตอบคือ "ไม่"
- "Consistency" จะบอกว่า "pattern ตรงกันไหม แต่ scale อาจ offset?" — เหมาะกับ test-retest ของ instrument เดียวกัน ไม่เหมาะกับ human vs. machine

**A priori threshold (VitroVision):**
- Acceptable: ICC(2,1) ≥ 0.75
- Target: ICC(2,1) ≥ 0.90

---

### 2.4 เมื่อไหรใช้อะไร — สรุปตาราง

| คำถามที่ต้องการตอบ | Metric ที่เหมาะสม |
|---|---|
| CV และ expert เรียง rank เหมือนกันไหม? | Spearman ρ |
| CV และ expert เห็นด้วย (agree) จริงๆ ไหม? | ICC(2,1) absolute agreement |
| ถ้า disagree ห่างมากควร penalize มากกว่า? | Quadratic-weighted κ |
| Expert ด้วยกันเองเห็นด้วยแค่ไหน? (ceiling) | Inter-rater ICC + κ ก่อน validate CV |

---

## 3. Paper Verification — Bock / de Raadt / Aeffner

### 3.1 Bock et al. 2010 — VERIFIED ✓

**Full citation:**
Bock, C.H., Poole, G.H., Parker, P.E., & Gottwald, T.R. (2010). Plant Disease Severity Estimated Visually, by Digital Photography and Image Analysis, and by Hyperspectral Imaging. *Critical Reviews in Plant Sciences*, 29(2), 59–107.

**URL:** https://consensus.app/papers/details/0eed3dce2a225af296ce79274426cc95/?utm_source=claude_code

**Citations:** 817 (Consensus, 2026)

**Key quotes และ relevance สำหรับ VitroVision:**
- Review นี้เป็น definitive reference ว่า "image analysis has been increasingly used over the last thirty years" เป็น objective substitute ของ visual rating
- Bock ระบุว่า "both interrater and intrarater reliability can be variable, particularly if training or rating aids are not used" — รองรับความจำเป็นของการวัด inter-rater ก่อน
- แนะนำ "accuracy" (closeness to true value) และ "precision" (consistency) เป็น framework ในการประเมิน — แตกต่างจาก agreement metrics แต่เสริมกัน
- เตือนว่า "there is a widespread tendency to overestimate disease severity at low severities (<10%)" — ใน VitroVision context หมายถึง expert อาจ over-score ที่ Grade 1 (contamination น้อย / growth น้อย)

**Relevance ระดับ:** สูงมาก — เป็น methodological backbone สำหรับ justify ว่าทำไม CV จึงเหนือกว่า visual rating ในแง่ objectivity

---

### 3.2 de Raadt et al. 2021 — VERIFIED ✓

**Full citation:**
de Raadt, A., Warrens, M.J., Bosker, R.J., & Kiers, H.A.L. (2021). A Comparison of Reliability Coefficients for Ordinal Rating Scales. *Journal of Classification*, 38, 519–543. https://doi.org/10.1007/s00357-021-09386-5

**URL:** https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code

**Citations:** 99 (Consensus, 2026) | ถูกอ้างถึงใน Maschke et al. 2023 (Academic Radiology) โดยตรง

**Key quotes:**
- "for the data in this study, **the same conclusion about inter-rater reliability was reached in virtually all cases** with the four correlation coefficients [Spearman, Pearson, Kendall, ICC(3,1)]"
- "differences between quadratic kappa and the Pearson and intraclass correlations increase if agreement becomes larger"
- "quadratically weighted kappa tend to measure agreement in a similar way [as correlation coefficients]: their values are very highly correlated"

**Implication สำหรับ VitroVision:**
- การใช้ metric suite (Spearman + κ + ICC) ไม่ใช่ redundant — แต่ให้ evidence จาก 3 มุมมอง (rank association / chance-corrected agreement / absolute agreement)
- ถ้าทั้ง 3 metrics ผ่าน threshold → convergent validity แข็งแกร่ง
- ถ้า Spearman สูงแต่ ICC ต่ำ → บ่งชี้ว่ามี systematic offset ระหว่าง CV กับ expert (ต้องปรับ calibration)

**Note:** Paper นี้อยู่ใน *Journal of Classification* (statistics/machine learning journal) ไม่ได้ index ใน PubMed — verified ผ่าน Consensus และ cross-reference ใน biomedical literature

---

### 3.3 Aeffner et al. 2017 — VERIFIED ✓

**Full citation (from PubMed, PMID: 28557614):**
Aeffner, F., Wilson, K., Martin, N.T., Black, J.C., Hendriks, C.L.L., Bolon, B., Rudmann, D.G., Gianani, R., Koegler, S.R., Krueger, J., & Young, G.D. (2017). The Gold Standard Paradox in Digital Image Analysis: Manual Versus Automated Scoring as Ground Truth. *Archives of Pathology & Laboratory Medicine*, 141(9), 1267–1275.

**DOI:** [10.5858/arpa.2016-0386-RA](https://doi.org/10.5858/arpa.2016-0386-RA)

**Citations:** 154 (Consensus, 2026) | PMID: 28557614

**Key quotes:**
- "The paradox of this validation strategy, however, is that tIA [tissue image analysis] is often used to assist pathologists to score complex biomarkers **because it is more objective and reproducible than manual evaluation alone** by overcoming known biases in a human's visual evaluation of tissue"
- "Awareness of the gold standard paradox is necessary when using traditional pathologist scores to analytically validate a tIA tool **because image analysis is used specifically to overcome known sources of bias** in visual assessment of tissue sections"

**Concept หลัก — Gold Standard Paradox:**
ถ้า CV system ถูกออกแบบมาเพื่อ *เอาชนะ* bias ของ human rater แล้วใช้ human rater เป็น gold standard นั้นหมายความว่ายิ่ง CV ดีเท่าไหร่ ความเห็นด้วยกับ gold standard อาจยิ่ง *ต่ำลง* ได้ในบางกรณี

**สำหรับ VitroVision:** Paradox นี้ต้อง address ใน Methods section โดย:
1. ระบุว่า inter-rater agreement ระหว่าง expert มีค่าเท่าไหร่ (เป็น empirical ceiling)
2. ถ้า CV เกินหรือใกล้เคียง inter-rater expert ก็ถือว่า perform ได้ในระดับ "human expert"
3. ถ้า CV สูงกว่า expert-expert agreement ในบาง metric — นั่นคือ evidence ของ objectivity ที่เพิ่มขึ้น

---

## 4. ข้อแนะนำสำหรับ Methods Section ของ VitroVision

### 4.1 ลำดับขั้นตอน Validation ที่แนะนำ

```
Step 1: Inter-rater study (Expert vs Expert, blind)
        ├── Expert A และ Expert B rate ชุด sample เดียวกัน (≥30 ขวด, blind)
        ├── คำนวณ: Spearman ρ, quadratic-weighted κ, ICC(2,1) absolute
        └── ผลนี้ = empirical ceiling สำหรับ CV validation

Step 2: CV vs Expert validation
        ├── CV predict score สำหรับ sample ชุดเดียวกับที่ expert rate
        ├── เปรียบ CV กับ Expert A (primary) และ Expert B (secondary)
        └── คำนวณ: ชุด metric เดียวกัน

Step 3: Interpret ด้วยบริบท Gold Standard Paradox
        ├── ถ้า CV ≥ expert-expert ceiling → ถือว่า perform ได้เทียบเท่าหรือเหนือกว่า human
        └── ถ้า CV < ceiling แต่ผ่าน a priori threshold → still valid
```

### 4.2 A Priori Thresholds (ระบุใน pre-registration หรือ Methods ก่อนเก็บข้อมูล)

| Metric | Acceptable | Target/Excellent | อ้างอิง |
|---|---|---|---|
| Spearman ρ | ≥ 0.70 | ≥ 0.85 | Bock 2010 [8]; Schober 2018 [4] |
| Quadratic-weighted κ | ≥ 0.60 | ≥ 0.80 | Li et al. 2023 [5] |
| ICC(2,1) absolute | ≥ 0.75 | ≥ 0.90 | Koo & Li 2016 [2] |

### 4.3 การ Address Gold Standard Paradox ใน Paper

เขียนใน Limitations/Discussion ว่า:
> "Expert visual score ที่ใช้เป็น gold standard มีข้อจำกัดที่ทราบในวรรณกรรม (Aeffner et al., 2017) — expert score เป็น subjective และ subject to known cognitive biases เช่น overestimation ที่ low severity (Bock et al., 2010). Inter-rater agreement ระหว่าง expert (ICC = [ค่า], κ = [ค่า]) เป็น empirical ceiling ที่บ่งชี้ว่าความตรงกันของ CV กับ expert score อยู่ในระดับ [ดีกว่า/เทียบเท่า/ต่ำกว่า] ขีดจำกัดที่ inherent ของ gold standard เอง"

### 4.4 Reporting Checklist สำหรับ Methods

- [ ] ระบุ rater จำนวนกี่คน (≥2), expertise level, blind conditions
- [ ] ระบุชัดว่าใช้ ICC model อะไร: "ICC(2,1), two-way mixed effects, absolute agreement, single measures"
- [ ] ระบุ software ที่คำนวณ (แนะนำ: `pingouin` library ใน Python หรือ `irr` ใน R)
- [ ] รายงาน 95% CI ของ ICC ไม่ใช่แค่ point estimate
- [ ] ระบุ κ weights: "quadratic-weighted κ" ไม่ใช่แค่ "κ"
- [ ] Pre-register threshold ก่อน data collection ถ้าต้องการ → credibility สูง

### 4.5 Sample Size Guidance

Koo & Li 2016 แนะนำให้ใช้ sample ≥30 subjects เพื่อให้ 95% CI ของ ICC แคบพอที่จะ interpret ได้ [2] สำหรับ VitroVision ที่มีเป้าหมาย 100 ขวด — แนะนำ random sample ≥40 ขวดสำหรับ validation set (stratified ตาม grade distribution)

---

## 5. References

[1] [A Comparison of Reliability Coefficients for Ordinal Rating Scales](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) (de Raadt et al., 2021, *Journal of Classification*, 99 citations) — DOI: 10.1007/s00357-021-09386-5

[2] [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) (Koo TK & Li MY, 2016, *Journal of Chiropractic Medicine*, 24,121 citations) — [DOI: 10.1016/j.jcm.2016.02.012](https://doi.org/10.1016/j.jcm.2016.02.012) | PMID: 27330520

[3] [The Gold Standard Paradox in Digital Image Analysis: Manual Versus Automated Scoring as Ground Truth](https://consensus.app/papers/details/2933b13a23705d7ea2c1f1fcd7927ea1/?utm_source=claude_code) (Aeffner F et al., 2017, *Archives of Pathology & Laboratory Medicine*, 154 citations) — [DOI: 10.5858/arpa.2016-0386-RA](https://doi.org/10.5858/arpa.2016-0386-RA) | PMID: 28557614

[4] [Correlation Coefficients: Appropriate Use and Interpretation](https://consensus.app/papers/details/2d40ef246f7f5233959a1ab6bdc4827a/?utm_source=claude_code) (Schober P et al., 2018, *Anesthesia & Analgesia*, 7,865 citations)

[5] [Kappa statistic considerations in evaluating inter-rater reliability between two raters: which, when and context matters](https://consensus.app/papers/details/4d70ccc3215b51f193265540584c2387/?utm_source=claude_code) (Li M et al., 2023, *BMC Cancer*, 145 citations)

[6] [Different ranking approaches defining association and agreement measures of paired ordinal data](https://consensus.app/papers/details/ff13ba4d3c3650a196ff18e8a26fd3c8/?utm_source=claude_code) (Svensson E, 2012, *Statistics in Medicine*, 63 citations)

[7] [Interrater reliability estimators tested against true interrater reliabilities](https://consensus.app/papers/details/c0e5ba15fc835263bb3a3beee686af28/?utm_source=claude_code) (Zhao X et al., 2022, *BMC Medical Research Methodology*, 56 citations)

[8] [Plant Disease Severity Estimated Visually, by Digital Photography and Image Analysis, and by Hyperspectral Imaging](https://consensus.app/papers/details/0eed3dce2a225af296ce79274426cc95/?utm_source=claude_code) (Bock CH et al., 2010, *Critical Reviews in Plant Sciences*, 817 citations)

[9] [From visual estimates to fully automated sensor-based measurements of plant disease severity: status and challenges for improving accuracy](https://consensus.app/papers/details/34c6a80dfdf75d1f9966228ed64f9b61/?utm_source=claude_code) (Bock CH et al., 2020, *Phytopathology Research*, 192 citations)

[10] [Updated guidelines on selecting an intraclass correlation coefficient for interrater reliability, with applications to incomplete observational designs](https://consensus.app/papers/details/9a91923f2d035b8eab74cbd0b386b475/?utm_source=claude_code) (ten Hove D et al., 2022, *Psychological Methods*, 71 citations)

---

*ไฟล์นี้สร้างโดย Claude Code research sub-agent (claude-sonnet-4-6) วันที่ 2026-06-11*
*Sources: Consensus (consensus.app) + PubMed (via MCP tools)*
*ข้อมูลจาก PubMed: According to PubMed — DOI links included per legal requirement*

---

> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
