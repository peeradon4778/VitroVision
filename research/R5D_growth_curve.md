# R5-D — Gompertz Growth Curve Fitting สำหรับ In Vitro Plant Data

> Sub-agent R5-D | VitroVision (YSC 2027 → ISEF CSBI)
> วันที่: 2026-06-21
> โจทย์: fit Gompertz/logistic growth curve ต่อขวด (individual replicate) จาก green_coverage_pct 28 วัน × ~180 ขวด × 5 สูตร MS แล้วเปรียบเทียบ parameters ข้าม 5 treatment groups
> กฎ citation: ทุก citation มาจาก Consensus จริง + URL ที่ verify แล้ว

---

## VERDICT รวม

| คำถาม | คำตอบสั้น |
|---|---|
| โมเดลใดเหมาะสุดสำหรับ TC 28 วัน? | **Gompertz 3-param เป็น primary** (asymmetric sigmoid เหมาะ bio growth ช่วงต้น); Richards เป็น umbrella model ที่ flexible กว่า |
| วิธี fit ต่อ individual replicate | **NLS ต่อขวด** → ดึง parameters ออกเป็น summary stats; หรือ **NLME** เมื่อต้องการ shared population mean พร้อม random effects ต่อขวด |
| เทียบ parameters ระหว่าง 5 กลุ่ม | **LMM/ANOVA บน extracted parameters** (k, tm, K) หรือ **NLME with group fixed effects** |
| incomplete curves / contamination | Bayesian nonlinear model หรือ NLME ช่วย interpolate; ขวดที่ terminated early อาจ fit เฉพาะ subset parameters |
| Gompertz-derived traits ที่ established | max absolute growth rate (AGRmax), inflection time (tm), asymptote (K), early vigor, area under growth curve (AUC) |

---

## ตารางหลักฐาน

| เรื่อง | สรุปสาระ | อ้างอิง + URL |
|---|---|---|
| Gompertz ใน plant/callus TC | Modified Gompertz via NLS เป็น best model สำหรับ callus growth curve (sigmoidal) ของ Glycine wightii; Durbin-Watson test ยืนยัน autocorrelation ต่ำ ใช้ได้; ให้ lag period, max specific growth rate, asymptote | [Shukor 2015](https://consensus.app/papers/details/dc495694c0de5a29ac605d622d07cb06/?utm_source=claude_code) |
| Gompertz re-parameterisation และ biological meaning | ทบทวน Gompertz ทุก parameterisation (Ti-form vs W0-form); แนะนำ U-Gompertz ใหม่ที่ growth-rate constant = relative growth rate → comparable ข้าม models; เป็น special case ของ Unified-Richards family | [Tjørve et al. 2017, PLoS ONE, 710 citations](https://consensus.app/papers/details/cd41380ae0955137a03a08e39e44218d/?utm_source=claude_code) |
| NLME สำหรับ longitudinal plant data ข้ามกลุ่ม | Nonlinear Mixed-Effect Models (NLME) เปรียบ Gompertz/Logistic/Richards/von Bertalanffy บน pepper fruit growth ข้าม 8 cultivar; Richards ดีสุดสำหรับ length (Radj²=0.9960), Logistic ดีสุดสำหรับ width; NLME ให้ random effects ต่อ genotype + group fixed effects ใน framework เดียว | [Teixeira et al. 2023, Agronomy, 3 citations](https://consensus.app/papers/details/d21cdb2b2c095c54b6d96035e8228b80/?utm_source=claude_code) |
| Nonlinear mixed model ต่อ individual + treatment comparison | แนะนำ combine NLS per-plant กับ mixed model เพื่อจับ repeated measures; แต่ละ plant มี coefficients ของตัวเอง; coefficients กระจาย multivariate normal โดย mean ถูก determine โดย treatment; ให้ unbiased SE สำหรับ multiple treatment comparison | [Peek et al. 2002, Oecologia, 158 citations](https://consensus.app/papers/details/e9e825b92a755d5bb9594aa4b231bc64/?utm_source=claude_code) |
| เปรียบ nonlinear models หลาย treatment; cluster analysis | เปรียบ logistic/Gompertz/Richards บน banana cultivar × 5 dose regulator; logistic ดีสุด; cluster analysis บน extracted coefficients แยก treatment groups ออกได้ 3 กลุ่มตาม biological behavior | [Maia et al. 2009, Ciencia Rural, 22 citations](https://consensus.app/papers/details/1eda6916d35a5f08ac15aab963c79a68/?utm_source=claude_code) |
| Smoothing + trait extraction สำหรับ longitudinal plant phenotyping | SET (Smoothing and Extraction of Traits) เป็นทางเลือกต่อ traditional longitudinal analysis; แนะนำ LMM with splines + autocorrelation correction; traits ที่ extract ออกมา (เช่น growth rate intervals, AUC) ใช้เป็น biologically relevant parameters | [Brien et al. 2020, Plant Methods, 23 citations](https://consensus.app/papers/details/fd6e3c4486e058b38677a83d4c0b8103/?utm_source=claude_code) |
| Gompertz-derived traits สำหรับ canopy cover time series | Gompertz fit บน multi-temporal canopy cover (CC) ของ soybean ด้วย UAV RGB; extract AGRmax (max absolute growth rate), early vigor, asymptote, senescence parameters; 90.4% fits ได้ Radj²>0.70; parameters เหล่านี้ predict seed yield และ maturity ได้ | [Borra-Serrano et al. 2020, Remote Sensing, 57 citations](https://consensus.app/papers/details/adeba199b184589e87563034788009ff/?utm_source=claude_code) |
| Gompertz vs Logistic บน high-dimensional plant phenomics | Gompertz กับ Logistic ให้ RMSE ใกล้เคียงกัน (3.84 vs 3.84) สำหรับ maize plant volume; ทั้งคู่ด้อยกว่า XGBoost เมื่อ data ซับซ้อน; แต่สำหรับ interpretable TC parameters (biological meaning) — Gompertz/Logistic ยังคงเลือกได้ | [Gachoki et al. 2022, Am. J. Applied Math. & Stats, 9 citations](https://consensus.app/papers/details/491ced6d4d10561aa35c4561eee1e002/?utm_source=claude_code) |
| Fragmented / missing longitudinal data | Bayesian nonlinear model ช่วย interpolate ใน "fragmented longitudinal data" (citrus seedlings ที่ missing observations); ลด MSE ของ late-stage growth parameter ได้ 84.3%; เหมาะเมื่อขวดบางใบถูก terminate ก่อนกำหนด | [Kimura et al. 2025, bioRxiv, 0 citations](https://consensus.app/papers/details/fc22afc45a315bbd8763dadda24fdb40/?utm_source=claude_code) |
| Function-Valued Trait (FVT) approach | FVT = fit curve ทั้งเส้น → เปรียบ "shape of trajectory" แทนค่า point เดียว; เหมาะกับ plant ontogeny ที่ endpoint เดียวไม่เพียงพอ; รองรับ stress response + developmental divergence | [Baker et al. 2021, Am. J. Botany, 3 citations](https://consensus.app/papers/details/1d6a64d3d2ac5bbb9448e029e797ee17/?utm_source=claude_code) |
| Digital quantification of greenness in vitro (ใกล้เคียง VitroVision มากสุด) | วัด green coverage จาก RGB image ของ Lolium in vitro โดยใช้ CIELAB color space; วัดซ้ำ non-destructively ตลอด experiment; ยืนยัน image analysis approach สำหรับ in vitro plant growth quantification | [Depetris et al. 2025, Plants, 2 citations](https://consensus.app/papers/details/94906cb0d2645de8a69c5329f5b54d3d/?utm_source=claude_code) |
| Incomplete data / damaged experiment growth curve | ใช้ nonlinear calibration reconstruct growth curve จาก partial data ของ bulb crop; validate ด้วย auxiliary variable + lowess regression; ยืนยัน NLS approach ยังใช้ได้บน incomplete data | [Dasgupta 2015](https://consensus.app/papers/details/4b368fcf678654258b88d6866da73008/?utm_source=claude_code) |

---

## Q&A ตามโจทย์ที่ถาม

### Q1: Gompertz vs Logistic vs Richards — อะไรเหมาะกับ TC 28 วัน?

**Gompertz เป็น primary choice** สำหรับ in vitro plant growth ด้วยเหตุผลดังนี้:

- **Asymmetric sigmoid**: growth เร็วช่วงต้น → ช้าเมื่อเข้าใกล้ asymptote ตรงกับ biology ของ TC ที่มักเร่งตัวแล้วชะลอ [Tjørve et al. 2017]
- **ใช้กับ callus TC โดยตรง**: Shukor 2015 ยืนยัน modified Gompertz via NLS ดีที่สุดสำหรับ callus culture [Shukor 2015]
- **Canopy cover time series**: Borra-Serrano 2020 ใช้ Gompertz กับ RGB-derived canopy coverage ซึ่งตรงกับ green_coverage_pct ของ VitroVision มากที่สุด [Borra-Serrano et al. 2020]

**Richards** เป็น umbrella ที่ flexible ที่สุด (Gompertz และ Logistic เป็น special cases) แต่มี 4 parameters → ต้องการข้อมูลมากกว่า อาจ overfit เมื่อ incomplete curve

**Logistic** เหมาะเมื่อ plateau ชัดเจนและ symmetric; pepper fruit growth ให้ Logistic ดีสุดสำหรับ width [Teixeira et al. 2023] แต่ TC มักไม่ symmetric

**คำแนะนำ VitroVision:** Gompertz 3-param เป็น primary → fallback เป็น 2-param Gompertz (fix K=100 เมื่อ incomplete curve) → Richards เป็น sensitivity check

---

### Q2: NLS ต่อ Individual Replicate vs NLME — เมื่อไรเหมาะกัน?

**Two-stage approach (แนะนำสำหรับ VitroVision):**

**Stage 1 — NLS ต่อขวด:**
```python
# scipy.optimize.curve_fit ต่อขวด
from scipy.optimize import curve_fit
import numpy as np

def gompertz(t, K, k, tm):
    return K * np.exp(-np.exp(-k * (t - tm)))

# fit ต่อ vessel_id แต่ละขวด → ได้ (K_i, k_i, tm_i)
```
เหมาะเมื่อ: ต้องการ parameter ต่อขวด; n ต่อขวดพอ (≥10 timepoints); นำ parameter ไปทำ downstream analysis

**Stage 1 ทางเลือก — NLME (แนะนำถ้าต้องการ population inference):**
```r
# R: nlme หรือ nlmer
library(nlme)
nlme(green_pct ~ gompertz(day, K, k, tm),
     data = vessel_data,
     fixed = K + k + tm ~ formula,
     random = K + k + tm ~ 1 | batch/vessel_id)
```
เหมาะเมื่อ: บาง vessel มี missing data มาก → borrow strength จาก population; ต้องการ group-level parameters พร้อม CI โดยตรง [Peek et al. 2002]

**Stage 2 — เทียบ parameters ระหว่าง 5 สูตร:**
- นำ (K_i, k_i, tm_i) จาก NLS → LMM: `lmer(k ~ formula + (1|batch))` แต่ละ parameter
- หรือ NLME with group fixed effects (ทำใน stage 1 เลย)

---

### Q3: Stat Test เทียบ Gompertz Parameters ระหว่าง 5 Treatment Groups

| วิธี | เมื่อไรใช้ | เหตุผล |
|---|---|---|
| **LMM** (`lmer`) บน extracted parameter | n ≥ 30/กลุ่ม, parameter ≈ normal | batch เป็น random effect ถูกต้อง |
| **ART-ANOVA** | parameter skewed/non-normal | aligned rank transform; post-hoc ต้องใช้ ART-C |
| **NLME with group fixed effects** | ต้องการ simultaneous test หลาย parameter | Teixeira 2023 approach [Teixeira et al. 2023] |
| **Cluster analysis บน parameters** | สำรวจ / exploratory | Maia 2009 ใช้ cluster ระบุกลุ่มที่ biologically similar [Maia et al. 2009] |

**Post-hoc:** Bonferroni correction สำหรับ 5 กลุ่ม (ดู `_decisions_pending.md` §B2)

**อย่าใช้:** ทดสอบโดยตรงบน raw green_pct รายวัน — pseudoreplication; ต้อง reduce ต่อขวดก่อนเสมอ

---

### Q4: Incomplete Growth Curves — จัดการอย่างไร?

**แบ่งตาม severity:**

| สถานการณ์ | วิธีแนะนำ |
|---|---|
| Missing timepoints กลางช่วง (contamination ชั่วคราว) | NLME interpolates โดย borrow strength [Kimura et al. 2025] |
| Terminated ก่อน plateau (<20 วัน) | Fix K=100 หรือ K=max observed; fit เฉพาะ k และ tm; รายงานว่า K ถูก constrain |
| ไม่ถึง inflection point | ใช้ linear fit เฉพาะ log-phase แทน; หรือรายงาน "early growth rate" เท่านั้น |
| Contaminated ตั้งแต่ต้น (<7 วัน) | **Exclude** จาก growth curve analysis; รายงาน survival rate แยก |

**หลัก:** ไม่ควรผสม complete กับ incomplete curves ใน ANOVA โดยไม่ flag; ให้ report น้อยกว่า 3 parameters สำหรับ incomplete curves อย่างชัดเจน

---

### Q5: Gompertz-Derived Traits ที่ Established ใน TC / Plant Phenotyping

| Trait | สูตร / นิยาม | อ้างอิง |
|---|---|---|
| **Asymptote (K)** | ค่า green_coverage สูงสุดที่ขวดจะถึง | [Tjørve et al. 2017] |
| **Max Absolute Growth Rate (AGRmax)** | `K · k / e` (สูงสุดที่ inflection point) | [Borra-Serrano et al. 2020] |
| **Inflection time (tm)** | วันที่ growth rate เร็วสุด = "เวลาเข้า rapid phase" | [Teixeira et al. 2023] |
| **Lag period** | เวลาก่อน exponential phase เริ่ม; สำคัญมากใน callus/TC | [Shukor 2015] |
| **Early vigor** | ค่า green_coverage ช่วง day 7–10 สะท้อน germination speed | [Borra-Serrano et al. 2020] |
| **Area Under Growth Curve (AUC)** | integral ของ green_pct ตลอด 28 วัน = overall biomass proxy | [Baker et al. 2021] |
| **Senescence / decline rate** | สำหรับขวดที่ plateau แล้วลด — ต้องใช้ Richards หรือ double-sigmoid | [Brien et al. 2020] |

**สำหรับ VitroVision รายงาน:** K, k, tm, AGRmax, lag period, และ AUC — ไม่รายงาน raw green_pct รายวันเป็นตัวแทน treatment effect

---

## Recommendation สำหรับ VitroVision

### Pipeline ที่แนะนำ

```
[raw green_coverage_pct × 28 days × 180 vessels]
        ↓
1. QC per vessel: flag contaminated / incomplete
        ↓
2. Fit Gompertz 3-param per vessel (NLS, scipy.optimize.curve_fit)
   - Complete vessels (≥20 days, reach plateau): fit K, k, tm freely
   - Incomplete vessels (14–20 days): fix K=100, fit k, tm only
   - Very short (<14 days): report early_growth_rate only (linear)
        ↓
3. Extract per-vessel traits: K_i, k_i, tm_i, AGRmax_i, AUC_i, lag_i
        ↓
4. Compare across 5 MS formulas:
   - LMM: lmer(trait ~ formula + (1|batch))   [primary]
   - ART-ANOVA: if trait non-normal             [fallback]
   - Post-hoc: Bonferroni
        ↓
5. Cluster analysis on [K, k, tm] to visualize formula groupings
        ↓
6. Report: parameter ± SE per formula, not raw daily values
```

### Model Selection Rationale

- **Gompertz เหนือ Logistic** สำหรับ TC เพราะ growth asymmetric — accelerate เร็ว ชะลอช้า [Shukor 2015, Tjørve et al. 2017]
- **NLME เป็น upgrade** เมื่อ missing data มากหรือต้องการ population-level CI [Peek et al. 2002, Kimura et al. 2025]
- **Richards เป็น sensitivity check** เท่านั้น — ไม่ใช่ primary (4 params, overfit risk บน 28-day window)
- **AUC และ AGRmax** เป็น Gompertz-derived traits ที่ established ใน field phenotyping [Borra-Serrano et al. 2020]

### Alignment กับ existing VitroVision decisions

- ไฟล์ `07_growthcurve_repeated_measures.md` แนะนำ Gompertz 3-param เป็น primary ✓ สอดคล้องกับ evidence ที่ค้นพบ
- Vessel = experimental unit (ไม่ใช่ภาพรายวัน) ✓ ตรงกับ [Peek et al. 2002] anti-pseudoreplication principle
- Batch เป็น random effect ✓ รองรับโดย NLME framework [Teixeira et al. 2023]

---

## References ทั้งหมด (เรียงตาม query)

### Query 1: Gompertz growth curve fitting plant tissue culture
1. [The use of Gompertz models in growth analyses, and new Gompertz-model approach: An addition to the Unified-Richards family](https://consensus.app/papers/details/cd41380ae0955137a03a08e39e44218d/?utm_source=claude_code) (Tjørve et al., 2017, PLoS ONE, 710 citations)
2. [Test for the Presence of Autocorrelation in Modified Gompertz Model used for Modelling the Growth of Callus Cultures from Glycine wightii](https://consensus.app/papers/details/dc495694c0de5a29ac605d622d07cb06/?utm_source=claude_code) (Shukor M.S., 2015, Asian Journal of Plant Biology, 6 citations)

### Query 2: nonlinear growth curve comparison treatment groups plant
3. [Nonlinear Mixed-Effect Models to Describe Growth Curves of Pepper Fruits in Eight Cultivars Including Group Effects](https://consensus.app/papers/details/d21cdb2b2c095c54b6d96035e8228b80/?utm_source=claude_code) (Teixeira et al., 2023, Agronomy, 3 citations)
4. [Physiological response curve analysis using nonlinear mixed models](https://consensus.app/papers/details/e9e825b92a755d5bb9594aa4b231bc64/?utm_source=claude_code) (Peek et al., 2002, Oecologia, 158 citations)
5. [Método de comparação de modelos de regressão não-lineares em bananeiras](https://consensus.app/papers/details/1eda6916d35a5f08ac15aab963c79a68/?utm_source=claude_code) (Maia et al., 2009, Ciencia Rural, 22 citations)

### Query 3: longitudinal growth analysis in vitro plant parameters
6. [Smoothing and extraction of traits in the growth analysis of noninvasive phenotypic data](https://consensus.app/papers/details/fd6e3c4486e058b38677a83d4c0b8103/?utm_source=claude_code) (Brien et al., 2020, Plant Methods, 23 citations)
7. [Working with longitudinal data: quantifying developmental processes using function-valued trait modeling](https://consensus.app/papers/details/1d6a64d3d2ac5bbb9448e029e797ee17/?utm_source=claude_code) (Baker et al., 2021, American Journal of Botany, 3 citations)
8. [Digitally Quantifying Growth and Verdancy of Lolium Plants In Vitro](https://consensus.app/papers/details/94906cb0d2645de8a69c5329f5b54d3d/?utm_source=claude_code) (Depetris et al., 2025, Plants, 2 citations)

### Query 4: incomplete growth curve missing data nonlinear regression plant experiment
9. [Estimating fruit tree growth curves in breeding field using fragmented longitudinal data](https://consensus.app/papers/details/fc22afc45a315bbd8763dadda24fdb40/?utm_source=claude_code) (Kimura et al., 2025, bioRxiv, 0 citations)
10. [Growth Curve Reconstruction in Damaged Experiment via Nonlinear Calibration](https://consensus.app/papers/details/4b368fcf678654258b88d6866da73008/?utm_source=claude_code) (Dasgupta, 2015, 2 citations)

### Query 5: Gompertz derived traits maximum growth rate area under curve plant phenotyping
11. [Closing the Phenotyping Gap: High Resolution UAV Time Series for Soybean Growth Analysis Provides Objective Data from Field Trials](https://consensus.app/papers/details/adeba199b184589e87563034788009ff/?utm_source=claude_code) (Borra-Serrano et al., 2020, Remote Sensing, 57 citations)
12. [Modelling Plant Growth Based on Gompertz, Logistic Curve, Extreme Gradient Boosting and Light Gradient Boosting Models Using High Dimensional Image Derived Maize Phenomic Data](https://consensus.app/papers/details/491ced6d4d10561aa35c4561eee1e002/?utm_source=claude_code) (Gachoki et al., 2022, Am. J. Applied Mathematics and Statistics, 9 citations)

---

## Sign-up/usage message จาก Consensus

> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

> View all results:
> - https://consensus.app/search/new?q=Gompertz+growth+curve+fitting+plant+tissue+culture&utm_source=claude_code&mode=quick
> - https://consensus.app/search/new?q=nonlinear+growth+curve+comparison+treatment+groups+plant&utm_source=claude_code&mode=quick
> - https://consensus.app/search/new?q=longitudinal+growth+analysis+in+vitro+plant+parameters&utm_source=claude_code&mode=quick
> - https://consensus.app/search/new?q=incomplete+growth+curve+missing+data+nonlinear+regression+plant+experiment&utm_source=claude_code&mode=quick
> - https://consensus.app/search/new?q=Gompertz+derived+traits+maximum+growth+rate+area+under+curve+plant+phenotyping&utm_source=claude_code&mode=quick
