# R5 — Validation Stats Framework (L7) — Synthesis

> **สร้าง:** 2026-06-21 · 10 sub-agent files (R5A–E ×2 session) · ทุก cite มี URL จาก Consensus จริง
> **คำถามต้นทาง:** Q11 (grill, parked) — L7 stats framework: validate CV/ML phenotyping vs expert, method comparison, growth curve analysis, survival/contamination — หลัง architecture เปลี่ยน (SAM2 + DINOv2 + VLM)
> **กฎ citation:** URL ด้านล่าง = Consensus page จริง — ก่อนเข้ารูปเล่มให้ resolve DOI + verify PubMed เฉพาะตัว load-bearing
> **ไฟล์ลูก:** `R5A_interrater_reliability.md` · `R5A_continuous_validation.md` · `R5B_method_comparison.md` · `R5B_ordinal_validation.md` · `R5C_art_anova.md` · `R5C_inter_rater.md` · `R5D_growth_curve.md` · `R5D_sample_size.md` · `R5E_survival_contamination.md` · `R5E_revalidation_framework.md`

---

## 🎯 VERDICT รวม — Q11 ปลดล็อก

**L7 Stats Framework สำหรับ VitroVision ประกอบด้วย 4 modules ที่ validate กัน:**

1. **Inter-rater reliability:** ICC(2,1) absolute agreement = primary metric สำหรับ vigor 1–5; QWK = secondary; Spearman ρ = supplementary เท่านั้น (ไม่ใช่ agreement metric) — ยืนยัน current plan ถูกต้อง แต่ต้องระบุ ICC form ชัดเจน
2. **CV vs Expert method comparison:** Spearman ρ = primary (green% continuous vs vigor ordinal); Bland-Altman = secondary หลัง normalize vigor → %; ICC(2,1) สำหรับ repeatability — ห้ามใช้ Pearson r กับ ordinal raw
3. **Treatment comparison (5 สูตร):** ART-ANOVA + ART-C = ทางเลือกที่ถูกต้องสำหรับ non-normal factorial; ยืนยัน Dunn's ไม่เหมาะ (one-way only); effect size = ε²p ไม่ใช่ η²; ทางเลือก GLMM beta regression สำหรับ green% ที่เป็น proportion
4. **Longitudinal growth:** Gompertz 3-param = primary สำหรับ TC 28 วัน; NLS ต่อขวด → extract K/k/tm → LMM เทียบ treatment; derived traits AGRmax/tm/AUC คือตัวเลขที่รายงาน ไม่ใช่ daily values
5. **Survival / contamination:** KM + **permutation log-rank** (ไม่ใช่ asymptotic) สำหรับ n≈25; CIF เสริมถ้า dead-not-contaminated ≥10%; ถ้า events <10 → ไม่ทำ formal test รายงาน % + binomial CI เท่านั้น
6. **Re-validation หลัง architecture เปลี่ยน:** Bridge study (Bland-Altman old vs new feature values, n ≥ 30 ขวด) ก่อน collect validation data จริง — κ=0.6274 เดิมใช้ไม่ได้บน engine ใหม่ ต้อง re-compute ทั้งหมด
7. **⚠️ แยก κ ให้ชัด:** vigor-rubric κ (ordinal QWK) ≠ classifier-3class κ (unweighted Cohen's) — ห้าม report รวมหรือสลับ label

---

## 📊 R5-A — Inter-rater Reliability (IRR)

> ไฟล์ลูก: `R5A_interrater_reliability.md` · `R5C_inter_rater.md`

### metric สำหรับ vigor score 1–5

| metric | role | เหตุผล |
|---|---|---|
| **ICC(2,1) absolute agreement** | PRIMARY | interpret ง่าย, มี 95%CI, ไม่มี paradox, มาตรฐาน plant phenotyping |
| Quadratic-weighted κ (QWK) | secondary | ≈ ICC สำหรับ 5-point ordinal; ลงโทษ far disagreement; ใช้ยืนยัน primary |
| Spearman ρ | supplementary | วัด association ไม่ใช่ agreement — รายงานแยก context |
| **Cohen's κ (unweighted)** | PRIMARY สำหรับ binary | hyperhydric flag เป็น binary → ใช้ Cohen's κ เท่านั้น |
| Krippendorff's α (ordinal weights) | เมื่อ rater ≥ 3 | รองรับ missing data + ordinal distance; ดีกว่า Fleiss' κ ทุกมิติ |

### เกณฑ์ตัดสิน

| metric | Pass (YSC minimum) | Target |
|---|---|---|
| ICC(2,1) human inter-rater | **≥ 0.75** (Good) | ≥ 0.90 (Excellent) |
| ICC(2,1) CV vs consensus | **≥ 0.75** | ≥ 0.80 |
| QWK vigor-rubric | **≥ 0.61** (Substantial) | ≥ 0.80 |
| Cohen's κ hyperhydric | **≥ 0.61** | ≥ 0.80 |
| Krippendorff's α | **≥ 0.667** | ≥ 0.80 |

### Sample size
- n = **50 ขวด** (stratified: 10/สูตร × 5) + 2 rater = เพียงพอสำหรับ CI ±0.15
- n = **80 ขวด** + 2 rater สำหรับ CI ≤ ±0.10
- dataset ~180 ขวดของ VitroVision เกิน minimum อย่างมาก

**อ้างอิง:** [de Raadt et al. 2021](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) · [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) (24K citations) · [McHugh 2012](https://consensus.app/papers/details/d8b550f8ffae56d6b6c2d46386b714e9/?utm_source=claude_code) (16K citations) · [Zapf et al. 2016](https://consensus.app/papers/details/9479c38e3e6d5c109876231e031b42a9/?utm_source=claude_code)

---

## 📐 R5-B — Method Comparison: CV vs Expert

> ไฟล์ลูก: `R5B_method_comparison.md` · `R5A_continuous_validation.md` · `R5B_ordinal_validation.md`

### วิธีเทียบ green_coverage_pct (continuous) vs vigor score (ordinal 1–5)

```
ขั้น 1 — PRIMARY:   Spearman ρ
  ρ = spearmanr(green_pct, vigor_score)
  95% CI bootstrap (n = 1000)
  เป้า: ρ ≥ 0.80

ขั้น 2 — SECONDARY: Bland-Altman (normalized)
  vigor_pct = (vigor_score - 1) / 4 × 100   # normalize 1-5 → 0-100%
  diff = green_pct - vigor_pct
  mean = (green_pct + vigor_pct) / 2
  รายงาน: bias ± 1.96 SD; เป้า LOA ≤ ±15%

ขั้น 3 — REPEATABILITY: ICC(2,1) absolute agreement
  ถ่ายขวดเดิมซ้ำ Day 1 vs Day 2 (n ≥ 20 ขวด)
  เสริม: CV% per bottle < 10%
```

### ข้อผิดพลาดที่ต้องระวัง

| ห้ามทำ | เหตุผล |
|---|---|
| Pearson r กับ vigor (ordinal) | ละเมิด assumption |
| Bland-Altman โดยไม่ normalize | scale ต่างกัน ไม่มีความหมาย |
| ICC form ผิด (ICC(1,1) แทน (2,1)) | overestimate reliability |
| ไม่รายงาน n ต่อ vigor class | อาจ skewed ถ้า vigor 1 (dead) น้อย |

**Benchmark จาก lit:** ρ ≥ 0.80–0.99 (Jollet 2023 bean, Bao 2018 sorghum), ICC ≥ 0.75 (Koo & Mae 2016)

**Framing สำหรับ CSBI:** [Bock et al. 2024](https://consensus.app/papers/details/4f988282959f5d7b8dbb38c8c673cf2e/?utm_source=claude_code) — 4 ทศวรรษ plant disease พบ % scale แม่นกว่า ordinal scale → green_coverage_pct ไม่ใช่แค่ surrogate ของ vigor 1–5 แต่เป็น **objective measurement ที่ขจัด anchoring bias**

---

## 📊 R5-C — ART-ANOVA + ART-C (Treatment Comparison)

> ไฟล์ลูก: `R5C_art_anova.md`

### เมื่อไรใช้อะไร

| design | วิธีที่เลือก | เหตุผล |
|---|---|---|
| 5 สูตร × 2 batch, green% skewed | **ART-ANOVA** | รองรับ factorial + interaction; KW ทำไม่ได้ [Wobbrock 2011] |
| post-hoc contrast ข้ามสูตร | **ART-C** | ไม่ใช่ Dunn's — Dunn's ออกแบบสำหรับ one-way เท่านั้น [Elkin 2021] |
| green% เป็น proportion (0–1) | GLMM beta regression | ทางเลือกถ้า ART assumption ไม่ผ่าน [Madden 2024] |
| batch effect | ใส่ batch เป็น **fixed factor** | 2 batch น้อยเกิน → random effect unstable; LMM เมื่อ batch ≥ 5 |

### Effect size
- รายงาน **ε²p** (epsilon squared partial) — bias น้อยกว่า η²p เมื่อ n เล็ก [Okada 2013, 1M MC replications]
- หลีกเลี่ยง η²p เป็น primary effect size เพราะ positive bias

### ข้อห้าม
- ❌ อย่าทำ pairwise contrast บน ART-transformed data โดยตรง → ต้องใช้ ART-C เสมอ
- ❌ ห้ามใช้ ART-C กับ Cauchy distribution (heavy-tail)

**อ้างอิง:** [Wobbrock et al. 2011](https://consensus.app/papers/details/2d2654a99b2e558b83d0d0311ab26151/?utm_source=claude_code) (2,905 citations) · [Elkin et al. 2021](https://consensus.app/papers/details/840aeef0be5c529f853e5f0d1d9af7c7/?utm_source=claude_code) (691 citations, validated 72K datasets) · [Durner 2019](https://consensus.app/papers/details/3c3d048c803459d1a3de8fc2c218c955/?utm_source=claude_code) (horticultural, ใช้ ART จริง)

---

## 📈 R5-D — Gompertz Growth Curve (Longitudinal)

> ไฟล์ลูก: `R5D_growth_curve.md` · `R5D_sample_size.md`

### โมเดลและวิธี fit

| โมเดล | เมื่อใช้ | params |
|---|---|---|
| **Gompertz 3-param** ← primary | TC 28 วัน, asymmetric sigmoid | K (asymptote), k (rate), tm (inflection) |
| Gompertz 2-param | incomplete curve (≥14 วัน แต่ไม่ถึง plateau) — fix K=100 | k, tm เท่านั้น |
| Richards 4-param | sensitivity check เท่านั้น | เสี่ยง overfit บน 28-day window |
| Logistic | ถ้า plateau ชัดเจนและ symmetric | — |

### Pipeline fit

```
ขั้น 1 — QC per vessel: flag contaminated / incomplete

ขั้น 2 — NLS ต่อขวด (individual):
  fit Gompertz 3-param ด้วย scipy.optimize.curve_fit ใน Python
  เก็บ K, k, tm, R²adj ต่อขวด

  Incomplete curve protocol (3-tier):
    ≥ 20 วัน + reach plateau  → fit K, k, tm freely
    14–20 วัน                 → fix K=100; fit k, tm เท่านั้น; รายงานว่า K constrained
    < 14 วัน                  → รายงาน early_growth_rate (linear) เท่านั้น
    < 7 วัน                   → exclude + นับใน survival analysis

ขั้น 3 — Handle missing data:
  contaminated กลางช่วง → NLME borrow population mean [Kimura et al. 2025]
  ห้ามผสม complete กับ incomplete curves ใน ANOVA โดยไม่ flag

ขั้น 4 — เทียบ 5 treatment groups:
  LMM: lmer(trait ~ formula + (1|batch)) บน extracted parameters แต่ละตัว [primary]
  ART-ANOVA: fallback ถ้า parameter distribution skewed
  หรือ NLME with group fixed effects โดยตรง [Peek et al. 2002]
  ⚠️ ห้ามทดสอบโดยตรงบน raw green_pct รายวัน → pseudoreplication

ขั้น 5 — Cluster analysis บน [K, k, tm] เพื่อ visualize formula groupings [Maia et al. 2009]
```

### Derived traits (รายงานใน paper)

| Trait | สูตร / นิยาม | เหตุผล |
|---|---|---|
| **K** (asymptote) | max green_coverage ที่ขวดจะถึง | ceiling productivity ต่อสูตร |
| **k** (rate) | steepness ของ sigmoid | ความเร็วเจริญ |
| **tm** (inflection) | วันที่ growth rate สูงสุด | "เวลาเข้า rapid phase" |
| **AGRmax** | K · k / e | max absolute growth rate |
| **Lag period** 🆕 | เวลาก่อน exponential phase เริ่ม | สำคัญมากใน callus/TC [Shukor 2015] |
| **AUC** | integral ของ green_pct 28 วัน | overall biomass proxy |
| **Early vigor** | green_pct ที่ day 7–10 | germination speed [Borra-Serrano 2020] |

⚠️ รายงาน traits เหล่านี้ ไม่ใช่ค่า daily raw

**ใกล้โจทย์มากที่สุด (In Vitro):**
- [Depetris et al. 2025 🥇](https://consensus.app/papers/details/94906cb0d2645de8a69c5329f5b54d3d/?utm_source=claude_code) — วัด **green coverage จาก RGB image ของ Lolium in vitro** ซ้ำ non-destructively ตลอด experiment — ตรงกับ VitroVision ที่สุดในทุก paper ที่ค้นพบ (2 citations)
- [Shukor 2015](https://consensus.app/papers/details/dc495694c0de5a29ac605d622d07cb06/?utm_source=claude_code) — Gompertz NLS บน callus TC โดยตรง (6 citations)
- [Borra-Serrano et al. 2020](https://consensus.app/papers/details/adeba199b184589e87563034788009ff/?utm_source=claude_code) — Gompertz บน RGB canopy coverage time series (57 citations)
- [Peek et al. 2002](https://consensus.app/papers/details/e9e825b92a755d5bb9594aa4b231bc64/?utm_source=claude_code) — two-stage NLS+LMM (158 citations)
- [Kimura et al. 2025](https://consensus.app/papers/details/fc22afc45a315bbd8763dadda24fdb40/?utm_source=claude_code) — fragmented longitudinal data, Bayesian nonlinear — ลด MSE late-stage 84.3%
- [Tjørve et al. 2017](https://consensus.app/papers/details/cd41380ae0955137a03a08e39e44218d/?utm_source=claude_code) — Gompertz reparameterisation + Unified-Richards family (710 citations)

---

## ⏱️ R5-E — Survival Analysis (Contamination)

> ไฟล์ลูก: `R5E_survival_contamination.md` · `R5E_revalidation_framework.md`

### Decision tree ตาม events

```
นับ events (contaminated + dead-not-contaminated) ทุกกลุ่มรวม:

  events < 10 ขวด รวม:
    → ไม่ทำ formal survival test
    → รายงาน contamination % + binomial 95% CI ต่อสูตร
    → ตาราง: n, n_contaminated, % (95% CI), median day ถ้ามี

  events 10–30 ขวด:
    → KM curve + permutation log-rank (package: coin ใน R)  ← ไม่ใช่ asymptotic
    → ตรวจ competing events (dead-not-contaminated ≥ 10%?)
       ถ้าใช่ → เพิ่ม CIF (cumulative incidence function, package: cmprsk)

  events > 30 ขวด:
    → KM + asymptotic log-rank ใช้ได้
    → Fine-Gray regression ถ้าต้องการ covariate adjustment
```

### Benchmark contamination rate

| ระดับ | ความหมาย | action |
|---|---|---|
| < 5% | ดีมาก | ไม่ต้องปรับ protocol |
| 5–15% | ยอมรับได้ | over-sow +25–30% |
| 15–30% | ปัญหาปานกลาง | ตรวจสอบ protocol |
| > 30% | ปัญหาร้ายแรง | optimize ก่อน batch 2 |

### Reporting checklist
- [ ] KM curve + 95% CI (Hall-Wellner bands)
- [ ] Number-at-risk table ใต้ KM curve
- [ ] Permutation log-rank p-value + caveat "exploratory"
- [ ] CIF plot ถ้ามี competing events
- [ ] Contamination % ต่อสูตร + binomial CI (ตารางเสริม)

**อ้างอิง:** [Wang et al. 2020](https://consensus.app/papers/details/a050c3f9bbb2512c952d89bfc2571a5b/?utm_source=claude_code) (type I error 28%) · [Austin et al. 2017](https://consensus.app/papers/details/9d7b0fd843c55411b0d4c0e2ad44898a/?utm_source=claude_code) (competing risks) · [D'Arrigo et al. 2021](https://consensus.app/papers/details/9fdc7a6b0f135395c4b5bfc756e5b4d2/?utm_source=claude_code) (KM overview)

---

## 🔁 Re-validation Framework (หลัง Architecture เปลี่ยน)

> ไฟล์ลูก: `R5E_revalidation_framework.md`

**กฎเหล็ก:** κ=0.6274 เดิม = smoke-test บนภาพมั่ว engine เก่า → ห้ามใช้บน engine ใหม่ (SAM2+CCM)

### Bridge Study (ต้องทำก่อน formal validation)
1. วิ่ง engine เก่า (HSV threshold) + engine ใหม่ (SAM+CCM) บน **sample ชุดเดียวกัน** (n ≥ 30 ขวด, หลายวัน)
2. Bland-Altman plot ต่อแต่ละ feature: mean bias + LoA
3. ถ้า mean bias ≠ 0 อย่างมีนัยสำคัญ → systematic shift ต้องรายงาน (ไม่ใช่ซ่อน)
4. Freeze pipeline ทุก module → collect validation data
5. Re-compute ICC + κ บน frozen engine ใหม่

### Freeze order
```
L0 Physical (rig) → L1 Scanner → L2 Drive → L3 WB/CCM → L4 Segmenter → 
L5 Feature extractor → STOP → collect validation data → L6 Classifier
```

---

## 🔗 L7 Pipeline สังเคราะห์ (เอาไป implement ได้เลย)

```
[ก่อน batch 1 วัน 0]
  Bridge study (HSV vs SAM+CCM) ≥ 30 ขวด → Bland-Altman per feature → freeze pipeline

[batch 1 เก็บข้อมูล 28 วัน]
  → green_coverage_pct, vigor 1–5 (ครู blind), hyperhydric flag, contamination date
  → ทุกวัน 17:00 ตาม imaging protocol

[หลัง batch 1 เสร็จ — validation set n ≥ 50 ขวด]
  Step 1: Inter-rater (ICC(2,1), QWK, κ hyperhydric)
  Step 2: CV vs Expert (Spearman ρ, Bland-Altman normalized)
  Step 3: Repeatability (ICC(2,1), CV%)

[analysis]
  Growth:       NLS per bottle → Gompertz K/k/tm → LMM compare 5 สูตร
  Treatment:    ART-ANOVA (สูตร × batch) + ART-C post-hoc + ε²p
  Survival:     count events → decision tree → KM+permutation / % + CI
  Primary test: Bonferroni 3 planned contrasts (green% at day 14, 21, 28)
  Secondary:    FDR (BH) สำหรับ vigor/brown/LCI/shoot
```

---

## ✅ Q11 ปลดล็อก — Decision

**L7 Stats Framework ของ VitroVision = 4 modules:**

| Module | วิธี | status |
|---|---|---|
| IRR & CV vs Expert | ICC(2,1) + QWK + Spearman ρ + Bland-Altman | ✅ confirmed |
| Treatment comparison | ART-ANOVA + ART-C + ε²p | ✅ confirmed |
| Growth curve | Gompertz 3-param + NLS→LMM | ✅ confirmed |
| Survival/contamination | Decision tree → KM+permutation หรือ % + CI | ✅ confirmed |

**Implement ต่อ:** `validation_stats.py` ใน `vitro_vision/` — calculators สำหรับ ICC/QWK/ART/Gompertz/KM

---

*ทุก citation ผ่าน Consensus search — ต้องผ่าน `_citation_audit.md` ก่อนเข้ารูปเล่ม*
*สร้าง: 2026-06-21 | R5 sub-agents: 10 files × 2 sessions*
