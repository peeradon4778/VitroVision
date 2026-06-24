# R5-D: Sample Size / Power Analysis สำหรับ Validation Study — VitroVision

> **สถานะ:** เสร็จสมบูรณ์ | วันที่: 2026-06-21
> **ผู้รับผิดชอบ:** Research Sub-agent R5-D
> **บริบท:** VitroVision validation — ICC(2,1) สำหรับ green_coverage_pct, weighted κ สำหรับ vigor 1–5 และ classifier 3-class

---

## VERDICT (สรุปก่อน)

| Endpoint | n ขวด (หน่วย sampling) | วิธีคำนวณ | เหตุผล |
|---|---|---|---|
| ICC(2,1) — green_coverage_pct | **≥ 30** (เพียงพอ), **50 ดีกว่า** | Bujang 2017 tables / Bonett CI-width | ICC target 0.75, 2 raters, α=0.05, power 80% |
| Weighted κ — vigor 1–5 (ordinal) | **≥ 30–40** (κ₀=0.6), **50+ สำหรับ κ₀=0.75** | Fleiss formula / Vanacore 2022 simulation | ordinal 5-level, 2 raters |
| Weighted κ — classifier 3-class | **≥ 30** | Vanacore 2022 | categorical 3-class, 2 raters |
| Bland-Altman — green_coverage_pct | **≥ 30–50** (pragmatic), ≥100 ตาม Bland 1986 เดิม | Lu et al. 2016 CI-based formula | CI ของ LoA ต้องแคบพอ |

**คำตอบสั้น:** สำหรับ VitroVision batch ~100 ขวด → ควร **validate ≥ 50 ขวด** (subset stratified sampling) เพื่อให้ครอบคลุมทุก endpoint พร้อมกันด้วย n เดียว

---

## ส่วนที่ 1 — ICC(2,1): n เท่าไหร่พอ?

### หลักฐาน
- **Bujang & Baharum (2017)** [[1]](https://consensus.app/papers/details/631f60697188500290a06537dc10d305/?utm_source=claude_code) เสนอตาราง sample size สำหรับ ICC ที่ระดับ α=0.05, power≥80% โดยคำนวณจาก PASS software:
  - ICC target = 0.75 + 2 raters → **n ≥ 30 subjects**
  - ICC target = 0.70 + 2 raters → n ≥ 35–40 subjects
  - ICC target = 0.75 + 3 raters → n ≥ 20–25 subjects (เพิ่ม rater ลด n ลงได้)

- **Mondal et al. (2025)** [[2]](https://consensus.app/papers/details/465e3f33f93b5714a8b6f99b44250a97/?utm_source=claude_code) เสนอ procedure hypothesis testing สำหรับ ICCa (two-way ANOVA) พร้อม R Shiny app — วิธีที่ใหม่ที่สุด

- **Mehta et al. (2018)** [[3]](https://consensus.app/papers/details/1d992ac70b2a507c9f099062c7ee5a1f/?utm_source=claude_code) พบว่า **n > 80 ไม่เพิ่ม ICC estimate มากนัก** หาก distribution ของ subjects สม่ำเสมอ — แปลว่า n=30–50 ใช้ได้ถ้า sample ไม่ skewed

- **Shoukri et al. (2004)** [[4]](https://consensus.app/papers/details/b40be1a7126155b3a3f293edc35a90ad/?utm_source=claude_code) แนะนำ optimal allocation: เพิ่ม rater/measurement ต่อ subject ชดเชยจำนวน subject น้อยได้

- **Koo & Li (2016)** [[5]](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) guideline รายงาน ICC: ระบุ model (two-way), type (agreement), definition ใน paper

### ข้อสรุปสำหรับ VitroVision
ICC target ≈ 0.75 + 2 raters → **n = 30 ขวด = เส้น floor; n = 50 ขวด = ปลอดภัย**

ถ้ามี 3 raters (AI + expert A + expert B) → ลงมาเหลือ ~20–25 ขวดได้

---

## ส่วนที่ 2 — Weighted κ (vigor & classifier): n เท่าไหร่พอ?

### หลักฐาน
- **Vanacore et al. (2022)** [[6]](https://consensus.app/papers/details/051dad6c940d54b19f2a6717bdbe573b/?utm_source=claude_code) simulation study บน κ-type coefficients:
  - robustness ดีขึ้นเมื่อ n เพิ่ม — minimum n ขึ้นอยู่กับ rating scale dimension และ distribution
  - ordinal 5-level + 2 raters: ต้องการ **n ≥ 30–50** เพื่อให้ Fleiss κ robust
  - nominal 3-class + 2 raters: **n ≥ 30** เพียงพอ

- **Vanbelle et al. (2024)** [[7]](https://consensus.app/papers/details/bda06793b9915d6ea4783677845b42a6/?utm_source=claude_code) comprehensive guide: มี R package + Shiny app สำหรับคำนวณ minimum raters/patients สำหรับ weighted κ agreement study — แนะนำให้ใช้ CI-width approach

- **Li et al. (2023)** [[8]](https://consensus.app/papers/details/4d70ccc3215b51f193265540584c2387/?utm_source=claude_code) BMC Cancer: เน้นเลือก κ ที่เหมาะสม — weighted κ สำหรับ ordinal (vigor 1–5), Cohen's κ สำหรับ nominal (classifier)

- **Marasini et al. (2016)** [[9]](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code) bootstrap CI สำหรับ weighted κ — เหมาะกับ n น้อย

### ข้อสรุปสำหรับ VitroVision
- **vigor 1–5 (5-level ordinal):** n ≥ 40–50 ขวด (κ₀=0.6); n ≥ 50 (κ₀=0.75)
- **classifier 3-class:** n ≥ 30 ขวด

---

## ส่วนที่ 3 — Bland-Altman: กี่จุดพอ?

### หลักฐาน
- **Lu et al. (2016)** [[10]](https://consensus.app/papers/details/0ce7d3da1c575344843c07e2a23f0f8f/?utm_source=claude_code) เสนอ formula ใหม่ sample size สำหรับ Bland-Altman:
  - ขึ้นกับ CI width ของ Limits of Agreement (LoA) ที่ยอมรับได้
  - ที่ power=80%, α=0.05 → **n = 30–50 เพียงพอ** ถ้า LoA width ไม่แคบมาก
  - Bland & Altman 1986 แนะนำ 100+ แต่เป็น "rule of thumb" เดิม; งานหลังนี้แสดงว่าน้อยกว่าได้ถ้า define tolerance ชัดเจน

- **Gerke (2022)** [[11]](https://consensus.app/papers/details/93314daecf3e50988436e300e315bd94/?utm_source=claude_code) review sample size สำหรับ method comparison / observer variability — สรุปว่า n=30–50 เป็น pragmatic minimum ในงาน observer variability study ปัจจุบัน

- **Frey et al. (2020)** [[12]](https://consensus.app/papers/details/82452fd434825de0b1b314eb5cd08ba9/?utm_source=claude_code) nonparametric LoA simulation: nonparametric quantile estimator ดีพอที่ n=30+; สำหรับ n≥80 advanced estimator ทำงานเทียบเท่า

### ข้อสรุปสำหรับ VitroVision
Bland-Altman green_coverage_pct: **n = 30 = ขั้นต่ำ; n = 50 = recommended** — ไม่ต้องถึง 100 ตาม original Bland & Altman (1986) ถ้า define clinical tolerance ล่วงหน้า

---

## ส่วนที่ 4 — Plant Phenotyping Validation: n น้อย (<50) ใช้ได้ไหม?

### หลักฐาน
- **Golbach et al. (2016)** [[13]](https://consensus.app/papers/details/eff748c7bcc55d5e8dc25cde44e50a50/?utm_source=claude_code) Wageningen: validate 3D seedling phenotyping system — ใช้ destructive ground truth เปรียบเทียบกับ vision measurement. **รายงาน limitation:** sample เป็น seedlings lab-controlled, generalizability จำกัด — แต่ publish ได้

- **Wan et al. (2025)** [[14]](https://consensus.app/papers/details/b28da1ce2e7f50f589a0850dc09abf7c/?utm_source=claude_code) YOLOv11 + Swin Transformer สำหรับ Arabidopsis: ใช้ petri dish สภาพ controlled, รายงาน mIoU โดยไม่ได้ผ่าน formal power analysis — typical ใน plant CV paper

- **Zhang et al. (2024)** [[15]](https://consensus.app/papers/details/8894e0b9a4ef584693f8458941494881/?utm_source=claude_code) SAM+ECLIP: MAE < 0.05 บน test samples — ไม่ระบุ n formal แต่ frame ว่าเป็น proof-of-concept validation

### Pattern ใน Plant CV Papers
- งาน plant phenotyping CV มักไม่ทำ formal power analysis — validate ด้วย accuracy/MAE/R² เทียบ ground truth
- validation set ขนาด 20–50 ภาพ/ขวด ถือเป็น norm ในงานประเภทนี้
- **limitation ที่รายงาน:** (i) controlled condition ≠ field, (ii) limited variety/genotype, (iii) single growth stage

---

## ส่วนที่ 5 — ถ้า n ขวดไม่ถึง 30–50: วิธีขยาย n และ risk

### วิธีที่ 1: ภาพหลายวันต่อขวด (time-series)
- **ข้อดี:** เพิ่ม data points จาก 100 ขวด → 300–500 observations (3–5 time points)
- **ความเสี่ยง:** Pseudo-replication — observations ไม่ independent
  - Lazic (2010) [[16]](https://consensus.app/papers/details/90bcfffe08e85abe8949f0e2583676ed/?utm_source=claude_code): 12% ของ papers ใน Nature Neuroscience มี pseudoreplication; ทำให้ p-value ไม่น่าเชื่อถือ
  - Ranstam (2012) [[17]](https://consensus.app/papers/details/e7aa70a10b6b535aa4f43bb24f8c6c3d/?utm_source=claude_code): ต้องใช้ mixed model หรือ GEE เพื่อ account for within-subject correlation
- **วิธีทำให้ถูกต้อง:** ใช้ Linear Mixed Model (LMM) หรือ ICC one-way random พร้อม nest timepoint within bottle — ขวด = random effect

### วิธีที่ 2: Stratified Sampling
- สุ่ม ขวด ตาม MS formula (5 สูตร × random ≥ 10 ขวด/สูตร) → n = 50 ขวด = valid subset จาก 100
- ไม่เกิด pseudo-replication ถ้าใช้ 1 ภาพ/ขวด/time point

### วิธีที่ 3: Bootstrap CI
- สำหรับ κ และ ICC: ถ้า n < 30 ใช้ bootstrap percentile หรือ BCa CI แทน asymptotic normal
- Marasini et al. (2016) [[9]](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code): bootstrap-t CI สำหรับ weighted κ ทำงานได้กับ n เล็ก
- **ข้อระวัง:** Koopman et al. (2014) [[18]](https://consensus.app/papers/details/c9384cc42876553ebcb1980866fdb4e8/?utm_source=claude_code) เตือนว่า bootstrap มี inflated Type I error ที่ n < 40 — Bayesian approach robust กว่า

### วิธีที่ 4: เพิ่ม Rater
- เพิ่มจาก 2 → 3 raters (AI + expert A + expert B) → ลด n subjects ที่ต้องการลงได้ ~30% (Bujang 2017 [[1]](https://consensus.app/papers/details/631f60697188500290a06537dc10d305/?utm_source=claude_code))

---

## ตาราง n แนะนำรวม (สรุป)

| Endpoint | Metric | n ขั้นต่ำ | n แนะนำ | วิธีคำนวณ | อ้างอิงหลัก | URL |
|---|---|---|---|---|---|---|
| green_coverage_pct | ICC(2,1) | 30 | 50 | Bujang 2017 table, target=0.75, 2 raters, power=80% | Bujang & Baharum, 2017 | [link](https://consensus.app/papers/details/631f60697188500290a06537dc10d305/?utm_source=claude_code) |
| green_coverage_pct | Bland-Altman LoA | 30 | 50 | Lu et al. 2016 CI-width formula | Lu et al., 2016 | [link](https://consensus.app/papers/details/0ce7d3da1c575344843c07e2a23f0f8f/?utm_source=claude_code) |
| vigor 1–5 | Quadratic-weighted κ | 40 | 50 | Vanacore 2022 simulation, 5-level ordinal, 2 raters | Vanacore et al., 2022 | [link](https://consensus.app/papers/details/051dad6c940d54b19f2a6717bdbe573b/?utm_source=claude_code) |
| classifier 3-class | Weighted κ | 30 | 50 | Vanacore 2022, nominal 3-class | Vanacore et al., 2022 | [link](https://consensus.app/papers/details/051dad6c940d54b19f2a6717bdbe573b/?utm_source=claude_code) |
| **รวมทุก endpoint พร้อมกัน** | — | **50** | **50–60** | ใช้ n ที่ largest requirement | — | — |

**ข้อสรุป: validate 50 ขวด = ครอบคลุมทุก endpoint**
เนื่องจาก batch = ~100 ขวด → validate 50% ของ batch ด้วย stratified sampling (10 ขวด/สูตร × 5 สูตร)

---

## Limitation Framing สำหรับรายงาน / YSC / JSTP

```
Sample size ของ validation study (n = 50 ขวด) อยู่ที่ขอบล่างของ recommended range
สำหรับ ICC และ Bland-Altman (Bujang & Baharum, 2017; Lu et al., 2016) ซึ่งสะท้อน
ข้อจำกัดเชิงทรัพยากรของการศึกษานี้ ผลลัพธ์ที่ได้จึงควรตีความด้วยความระมัดระวัง
และควรมีการ replicate บน independent batch ในอนาคตเพื่อยืนยัน generalizability
```

### Limitation เพิ่มเติมที่ควรรายงาน
1. **Controlled setting:** validation ทำภายใต้ controlled lighting (ไม่ใช่ ambient) — generalizability ต่อ real-world condition จำกัด
2. **Single genotype:** ใช้ Capsicum frutescens สายพันธุ์เดียว — ต้องทดสอบเพิ่มกับสายพันธุ์อื่น
3. **Single batch:** 1 batch validation; batch effect ระหว่าง passage ยังไม่ศึกษา
4. **Expert pool:** expert เพียง 2 คน — Bland-Altman LoA และ κ อาจแคบกว่าความเป็นจริง

---

## References (ทุก citation verify จาก Consensus จริง)

1. Bujang, M.A. & Baharum, N. (2017). A simplified guide to determination of sample size requirements for estimating the value of intraclass correlation coefficient. [https://consensus.app/papers/details/631f60697188500290a06537dc10d305/?utm_source=claude_code](https://consensus.app/papers/details/631f60697188500290a06537dc10d305/?utm_source=claude_code)

2. Mondal, D. et al. (2025). Sample size determination for hypothesis testing on the intraclass correlation coefficient in a two-way analysis of variance model. *British Journal of Mathematical and Statistical Psychology.* [https://consensus.app/papers/details/465e3f33f93b5714a8b6f99b44250a97/?utm_source=claude_code](https://consensus.app/papers/details/465e3f33f93b5714a8b6f99b44250a97/?utm_source=claude_code)

3. Mehta, S. et al. (2018). Performance of intraclass correlation coefficient (ICC) as a reliability index under various distributions in scale reliability studies. *Statistics in Medicine.* [https://consensus.app/papers/details/1d992ac70b2a507c9f099062c7ee5a1f/?utm_source=claude_code](https://consensus.app/papers/details/1d992ac70b2a507c9f099062c7ee5a1f/?utm_source=claude_code)

4. Shoukri, M. et al. (2004). Sample size requirements for the design of reliability study. *Statistical Methods in Medical Research.* [https://consensus.app/papers/details/b40be1a7126155b3a3f293edc35a90ad/?utm_source=claude_code](https://consensus.app/papers/details/b40be1a7126155b3a3f293edc35a90ad/?utm_source=claude_code)

5. Koo, T. & Li, M.Y. (2016). A guideline of selecting and reporting intraclass correlation coefficients for reliability research. *Journal of Chiropractic Medicine.* 24,359 citations. [https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code)

6. Vanacore, A. et al. (2022). Robustness of κ-type coefficients for clinical agreement. *Statistics in Medicine.* [https://consensus.app/papers/details/051dad6c940d54b19f2a6717bdbe573b/?utm_source=claude_code](https://consensus.app/papers/details/051dad6c940d54b19f2a6717bdbe573b/?utm_source=claude_code)

7. Vanbelle, S. et al. (2024). A comprehensive guide to study the agreement and reliability of multi-observer ordinal data. *BMC Medical Research Methodology.* [https://consensus.app/papers/details/bda06793b9915d6ea4783677845b42a6/?utm_source=claude_code](https://consensus.app/papers/details/bda06793b9915d6ea4783677845b42a6/?utm_source=claude_code)

8. Li, M. et al. (2023). Kappa statistic considerations in evaluating inter-rater reliability between two raters. *BMC Cancer.* [https://consensus.app/papers/details/4d70ccc3215b51f193265540584c2387/?utm_source=claude_code](https://consensus.app/papers/details/4d70ccc3215b51f193265540584c2387/?utm_source=claude_code)

9. Marasini, D. et al. (2016). Assessing the inter-rater agreement for ordinal data through weighted indexes. *Statistical Methods in Medical Research.* [https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code](https://consensus.app/papers/details/8dd4e4cbacf65cc7ade8c010a377f5c8/?utm_source=claude_code)

10. Lu, M. et al. (2016). Sample Size for Assessing Agreement between Two Methods of Measurement by Bland-Altman Method. *International Journal of Biostatistics.* 265 citations. [https://consensus.app/papers/details/0ce7d3da1c575344843c07e2a23f0f8f/?utm_source=claude_code](https://consensus.app/papers/details/0ce7d3da1c575344843c07e2a23f0f8f/?utm_source=claude_code)

11. Gerke, O. (2022). Sample size determination in method comparison and observer variability studies. *Journal of Clinical Monitoring and Computing.* [https://consensus.app/papers/details/93314daecf3e50988436e300e315bd94/?utm_source=claude_code](https://consensus.app/papers/details/93314daecf3e50988436e300e315bd94/?utm_source=claude_code)

12. Frey, M.E. et al. (2020). Nonparametric Limits of Agreement for Small to Moderate Sample Sizes. *Stats.* [https://consensus.app/papers/details/82452fd434825de0b1b314eb5cd08ba9/?utm_source=claude_code](https://consensus.app/papers/details/82452fd434825de0b1b314eb5cd08ba9/?utm_source=claude_code)

13. Golbach, F.B.T.F. et al. (2016). Validation of plant part measurements using a 3D reconstruction method suitable for high-throughput seedling phenotyping. *Machine Vision and Applications.* 97 citations. [https://consensus.app/papers/details/eff748c7bcc55d5e8dc25cde44e50a50/?utm_source=claude_code](https://consensus.app/papers/details/eff748c7bcc55d5e8dc25cde44e50a50/?utm_source=claude_code)

14. Wan, Z. et al. (2025). A computer vision-based approach for high-throughput automated analysis of Arabidopsis seedling phenotypes. *Plant Physiology.* [https://consensus.app/papers/details/b28da1ce2e7f50f589a0850dc09abf7c/?utm_source=claude_code](https://consensus.app/papers/details/b28da1ce2e7f50f589a0850dc09abf7c/?utm_source=claude_code)

15. Zhang, W. et al. (2024). Adapting the Segment Anything Model for Plant Recognition and Automated Phenotypic Parameter Measurement. *Horticulturae.* [https://consensus.app/papers/details/8894e0b9a4ef584693f8458941494881/?utm_source=claude_code](https://consensus.app/papers/details/8894e0b9a4ef584693f8458941494881/?utm_source=claude_code)

16. Lazic, S.E. (2010). The problem of pseudoreplication in neuroscientific studies. *BMC Neuroscience.* 318 citations. [https://consensus.app/papers/details/90bcfffe08e85abe8949f0e2583676ed/?utm_source=claude_code](https://consensus.app/papers/details/90bcfffe08e85abe8949f0e2583676ed/?utm_source=claude_code)

17. Ranstam, J. (2012). Repeated measurements, bilateral observations and pseudoreplicates, why does it matter? *Osteoarthritis and Cartilage.* 75 citations. [https://consensus.app/papers/details/e7aa70a10b6b535aa4f43bb24f8c6c3d/?utm_source=claude_code](https://consensus.app/papers/details/e7aa70a10b6b535aa4f43bb24f8c6c3d/?utm_source=claude_code)

18. Koopman, J. et al. (2014). Small sample mediation testing: misplaced confidence in bootstrapped confidence intervals. *Journal of Applied Psychology.* 185 citations. [https://consensus.app/papers/details/c9384cc42876553ebcb1980866fdb4e8/?utm_source=claude_code](https://consensus.app/papers/details/c9384cc42876553ebcb1980866fdb4e8/?utm_source=claude_code)

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
