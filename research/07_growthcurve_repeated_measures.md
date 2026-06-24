# 07 — Growth-Curve Modeling & Repeated-Measures Statistics สำหรับ VitroVision

**วันที่:** 2026-06-11  
**ขอบเขต:** Statistical pipeline สำหรับ green_coverage_pct time-series จากขวดเพาะเลี้ยง Capsicum frutescens in vitro  
**Design:** 5 สูตร MS × ~24–25 ขวด/สูตร/batch (over-sow; pool ≥2 batch → n≈40/สูตร), ~20–25 timepoints/ขวด ตลอด 28 วัน  

---

## 1. สรุปสั้น

งานนี้มีโครงสร้างข้อมูลแบบ **hierarchical repeated measures**: ภาพซ้ำอยู่ใน "ขวด" (vessel) ขวดซ้ำอยู่ใน "batch" และ batch ซ้ำอยู่ใน "สูตรอาหาร" (MS formula) วิธีที่ถูกต้องคือ

1. **Fit growth curve ต่อขวด** → ดึง 2–3 parameter (growth rate *k*, inflection point *t₀*, อาจมี plateau *K*) มาเป็น summary statistics ต่อ vessel
2. **เทียบ parameter ระหว่าง 5 สูตร** โดย treat batch เป็น random factor
3. หาก parameter ไม่ normal/unbalanced → **ART ANOVA** หรือ **LMM** (เลือกตาม criteria ด้านล่าง)
4. Post-hoc **ตาม model ที่ใช้** — ถ้า ART-ANOVA ต้องใช้ **ART-C** (Elkin 2021) ไม่ใช่ contrast ปกติ; ถ้า LMM ใช้ estimated marginal means + Bonferroni; **Dunn + Bonferroni = เฉพาะกรณี KW omnibus (secondary/preliminary)** — ทั้งหมด correct ด้วย **Bonferroni** (ตาม `_decisions_pending.md` §B2 + `10_methods_draft.md` = source of truth)

หัวใจสำคัญ: **ภาพแต่ละภาพ ≠ หน่วยสถิติ** — ต้องใช้ขวด (vessel) เป็น experimental unit เท่านั้น ไม่เช่นนั้นเป็น pseudoreplication [1]

---

## 2. Growth-Curve Model ไหนเหมาะกับ 28-day Window ที่อาจไม่ถึง Plateau

### ปัญหาหลัก: incomplete sigmoid

ใน 28 วัน ขวดบางสูตรอาจยังอยู่ในช่วง exponential หรือ linear ไม่ถึง plateau จึงทำให้ parameter *K* (carrying capacity) ไม่ stable และมี correlation สูงกับ *k*

### ตัวเลือกโมเดล

| โมเดล | สมการ | จุดแข็ง | ข้อจำกัด |
|---|---|---|---|
| **Logistic (3-param)** | `y = K / (1 + exp(-k(t - t₀)))` | symmetric sigmoid, interpretable | ต้องการ plateau ที่ชัดเจน |
| **Gompertz (3-param)** | `y = K · exp(-exp(-k(t - t₀)))` | asymmetric, เร็วในช่วงต้น, เหมาะ bio growth | plateau ยังต้องการ |
| **Gompertz (reduced/2-param)** | ตัด K ออก หรือ fix K=100 | stable เมื่อ data ไม่ถึง plateau | ต้องสมมติ K ล่วงหน้า |
| **Natural spline / GAM** | data-driven curve | ไม่บังคับรูปแบบ, fit ดีเสมอ | parameter ไม่ interpretable ทางชีววิทยา |
| **Linear (ช่วง log-phase)** | `y = a + bt` | simple, robust | ไม่ได้จับ inflection |

### คำแนะนำสำหรับ VitroVision (28-day window)

**แนะนำ: Gompertz 3-parameter เป็น primary; พร้อม fallback เป็น 2-parameter Gompertz (fix K=100)**

เหตุผล:
- Gompertz เหมาะกับ biological growth ที่ asymmetric — growth สูงช่วงต้น ค่อยๆ ช้าลง [1]
- Vaghi et al. (2020) พิสูจน์ว่า Gompertz reduced (1–2 param) มี predictive power ดีกว่า logistic เมื่อ data ไม่สมบูรณ์ โดยใช้ **nonlinear mixed-effects (NLME)** framework [2]
- Parameter *k* (growth rate) และ *t₀* (inflection point) ยังคง identifiable ใน 28-day window แม้ไม่เห็น plateau
- หาก residual plots แสดง poor fit → ใช้ **natural cubic spline** แล้วดึง AUC หรือ slope ที่ timepoint กลาง แทน

### จุดที่ต้องระวัง

- **Convergence failure**: ขวดที่ growth ช้ามาก หรือ coverage ไม่ขยับ — ต้องกำหนด lower bound ให้ k > 0 และตั้ง starting values จาก data เสมอ
- **Correlation K–k**: ถ้า K ไม่ stable ให้ fix K = 100 (max coverage %) หรือใช้ Bayesian inference กับ prior informative บน K [2]
- **Per-vessel fit quality**: รายงาน R² หรือ RMSE ต่อขวด — ขวดที่ fit ไม่ดี (R² < 0.7) ควร flag ไว้ และวิเคราะห์ sensitivity กับ/ไม่มีขวดนั้น

---

## 3. Pseudoreplication — Argument + Citation

### นิยามและปัญหา

**Pseudoreplication** หมายถึงการใช้ inferential statistics กับข้อมูลที่ไม่ใช่ replicates อิสระจริงๆ ในบริบทของ VitroVision คือการนับ **ภาพแต่ละภาพเป็น n** แทนที่จะนับ **ขวด** เป็น n

Hurlbert (1984) นิยามไว้ชัดเจนว่า pseudoreplication เกิดขึ้นเมื่อ treatment ไม่ถูก replicated อย่างแท้จริง หรือ replicates ไม่ statistically independent — พบใน 27% ของงานวิจัย ecological ที่ตรวจสอบ 176 งาน [1]

### ทำไม Experimental Unit ต้องเป็น "ขวด" ไม่ใช่ "ภาพ"

```
Treatment (สูตร MS)
    └── Batch (random factor)
            └── Vessel/ขวด  ← EXPERIMENTAL UNIT
                    └── Photo @ t₁, t₂, ..., t₂₅  ← repeated measures ใน unit เดียวกัน
```

ภาพ 25 ภาพจากขวดเดียวกันไม่ใช่ 25 observations อิสระ เพราะ:
1. ทุกภาพมาจาก *plant population เดียวกัน* ในขวดเดียวกัน
2. Batch effect ซึมผ่านทุกภาพในขวดเท่ากัน
3. Measurement error ที่ขวดหนึ่ง (เช่น contamination ลำต้น) ติดตามภาพทุกภาพในขวดนั้น

หากใช้ภาพเป็น n:
- n จะ inflate จาก ~200 ขวด → ~5,000 ภาพ
- Standard error จะเล็กเกินจริง → p-value ต่ำเกินจริง → ผล significant ที่ไม่จริง
- เป็น Type I error inflation แบบ classic pseudoreplication [1]

### แนวปฏิบัติ

วิธีถูกต้องคือ **สรุปข้อมูลรายขวดก่อน** (ดึง growth parameter ต่อขวด) แล้วจึงนำไปวิเคราะห์สถิติ ข้อถกเถียงของ Oksanen (2001) [3] เกี่ยวกับ scale ของ inference ไม่ apply กับกรณีนี้ เพราะ VitroVision ต้องการ conclusion ระดับ "สูตร MS" ซึ่งต้องการ replication ระดับขวด

---

## 4. ART vs LMM — ตัดสินอย่างไรสำหรับ Unbalanced/Nonparametric Data

### Aligned Rank Transform (ART) ANOVA

Wobbrock et al. (2011) เสนอ ART เพื่อจัดการ **nonparametric factorial data** โดยใช้การ "align" data ก่อนทำ rank แล้วจึง run ANOVA ปกติ [4] จุดเด่นคือ:
- สามารถ test **interaction effects** (formula × batch) ซึ่ง Kruskal-Wallis ทำไม่ได้
- มี open-source tool: **ARTool** (R package `ARTool`)
- Elkin et al. (2021) ขยาย ART ด้วย **ART-C** สำหรับ post-hoc contrast tests ที่ไม่ inflate Type I error [5]

### Linear Mixed Model (LMM)

LMM (formula `lmer(param ~ formula + (1|batch))`) เหมาะเมื่อ:
- Distribution ของ parameter ใกล้เคียง normal (ตรวจด้วย Shapiro-Wilk หรือ QQ-plot)
- มี unbalanced design (ขวดต่อ batch ไม่เท่ากัน)

Frey et al. (2024) เตือนว่า **ห้าม drop block (batch) effect ออกจากโมเดลแม้จะ non-significant** เพราะจะทำให้ Type I error rate ผิดพลาดทั้งแบบ inflate และ deflate ขึ้นอยู่กับ term ที่ test [6]

### Decision Tree สำหรับ VitroVision

```
ดึง growth parameter ต่อขวด (k, t₀)
          │
          ▼
Shapiro-Wilk test + QQ-plot ต่อ parameter
          │
   ┌──────┴──────┐
normal (p>0.05)  non-normal (p≤0.05)
   │                    │
   ▼                    ▼
LMM: lmer(k ~        ART ANOVA:
formula + (1|batch)) art(k ~ formula + batch + formula:batch)
+ emmeans post-hoc   + ART-C post-hoc contrast
          │                    │
          └──────┬─────────────┘
                 ▼
    Interpret formula:batch interaction
    → p < 0.05 = treatment effect ขึ้นกับ batch
      (reproducibility ต่ำ, ต้องรายงาน limitation)
    → p ≥ 0.05 = effect สม่ำเสมอข้าม batch
      (reproducibility ดี, conclusion ถูกต้อง)
```

### เมื่อใดใช้ Kruskal-Wallis

Kruskal-Wallis (Kruskal & Wallis 1952) [7] เป็น one-way nonparametric test ที่เหมาะเมื่อ:
- มีแค่ **1 factor** (formula) โดยไม่สนใจ batch
- เป็น **preliminary test** ก่อน full ART/LMM
- Sample size เล็กมาก (n < 10/group) ที่ LMM/ART ไม่ stable

สำหรับ VitroVision ที่มี 2 factors (formula + batch) และต้องการ test interaction = reproducibility → **ART ANOVA หรือ LMM เหมาะกว่า** Kruskal-Wallis

---

## 5. ข้อแนะนำ Pipeline สถิติสำหรับ VitroVision (Step-by-Step)

### Step 0: ตรวจสอบ Data Quality
- ตรวจ green_coverage_pct ต่อขวด: ลบ outlier frames (blur, occlusion)
- Flag ขวดที่มี timepoints < 15 (ข้อมูลน้อยเกินไปสำหรับ curve fitting)
- บันทึก batch assignment ต่อขวด (สำคัญมาก!)

### Step 1: Fit Growth Curve ต่อขวด
```python
from scipy.optimize import curve_fit
import numpy as np

def gompertz(t, K, k, t0):
    return K * np.exp(-np.exp(-k * (t - t0)))

# สำหรับขวดที่อาจไม่ถึง plateau: fix K=100
def gompertz_fixed_K(t, k, t0, K=100):
    return K * np.exp(-np.exp(-k * (t - t0)))

# ดึง: k (growth rate), t0 (inflection point) ต่อขวด
# เก็บ R² และ RMSE ต่อขวดเพื่อ quality check
```

**Output**: DataFrame ที่มี columns: `vessel_id`, `formula`, `batch`, `k`, `t0`, `R2`, `RMSE`

### Step 2: Check Normality ของ Parameters
```r
# R
shapiro.test(df$k[df$formula == "MS0"])  # ทำทุกสูตร
qqnorm(df$k); qqline(df$k)
```

### Step 3A: ถ้า Normal → LMM
```r
library(lme4); library(emmeans)
model_k <- lmer(k ~ formula + (1|batch), data=df)
# ตรวจ formula:batch interaction
model_k_int <- lmer(k ~ formula + (1|batch) + formula:batch, data=df)  # ถ้าไม่ converge ให้ skip
emmeans(model_k, pairwise ~ formula, adjust="bonferroni")
```

### Step 3B: ถ้า Non-Normal → ART ANOVA
```r
library(ARTool)
m <- art(k ~ formula * batch, data=df)  # batch as fixed factor ใน ART
anova(m)
# Post-hoc ด้วย ART-C
art.con(m, "formula", adjust="bonferroni")
```

### Step 4: Interpret formula:batch Interaction
- **Interaction p < 0.05**: treatment effect ไม่คงที่ข้าม batch → รายงานเป็น limitation; อาจต้องเพิ่ม batch หรือ randomize ใหม่
- **Interaction p ≥ 0.05**: effect reproducible ข้าม batch → confidence สูงขึ้น

### Step 5: Dunn Post-hoc (กรณีใช้ Kruskal-Wallis เป็น secondary)
```r
library(dunn.test)
dunn.test(df$k, df$formula, method="bonferroni")
```

### Step 6: Visualization
- Box plot ต่อ formula × parameter (k และ t₀) พร้อม overlay individual vessels
- Growth curve overlay: median curve ต่อสูตร บน scatter ของ all vessels
- Heatmap: k และ t₀ ต่อ vessel จัดเรียงตาม formula + batch

### Step 7: Reporting (YSC/JSTP format)
- รายงาน n (จำนวนขวด) ไม่ใช่จำนวนภาพ
- ระบุ random effect structure
- รายงาน interaction term และ interpret เป็น reproducibility
- ถ้า ART → cite Wobbrock 2011 [4] และ Elkin 2021 [5]

---

## 6. References

[1] [Pseudoreplication and the Design of Ecological Field Experiments](https://consensus.app/papers/details/b070b32bf90a524bad71600279dca39e/?utm_source=claude_code) (Hurlbert S.H., 1984, Ecological Monographs, 8346 citations) — foundational paper defining pseudoreplication; ใช้ cite เหตุผลที่ vessel ต้องเป็น experimental unit

[2] [Population modeling of tumor growth curves and the reduced Gompertz model improve prediction of the age of experimental tumors](https://consensus.app/papers/details/eb7c21a2698d53ed93899926e8e4e291/?utm_source=claude_code) (Vaghi C. et al., 2020, PLoS Computational Biology, 146 citations) — ยืนยัน Gompertz > Logistic สำหรับ incomplete time-series; แสดง NLME framework + Bayesian estimation

[3] [Logic of experiments in ecology: is pseudoreplication a pseudoissue?](https://consensus.app/papers/details/d64ae57dd95059ac81a91cadd7a75445/?utm_source=claude_code) (Oksanen L., 2001, Oikos, 585 citations) — ข้อถกเถียง counterpoint แต่ไม่ apply กับ vessel-level inference ของ VitroVision

[4] [The aligned rank transform for nonparametric factorial analyses using only anova procedures](https://consensus.app/papers/details/2d2654a99b2e558b83d0d0311ab26151/?utm_source=claude_code) (Wobbrock J. et al., 2011, CHI Proceedings, 2882 citations) — primary citation สำหรับ ART ANOVA; ใช้ cite เมื่อรายงานวิธีสถิติ

[5] [An Aligned Rank Transform Procedure for Multifactor Contrast Tests](https://consensus.app/papers/details/840aeef0be5c529f853e5f0d1d9af7c7/?utm_source=claude_code) (Elkin L. et al., 2021, UIST Proceedings, 685 citations) — ART-C algorithm สำหรับ post-hoc contrast ที่ถูกต้อง

[6] [Analyze as randomized — Why dropping block effects in designed experiments is a bad idea?](https://consensus.app/papers/details/810639a65da352d495ad8d6eb86e71ac/?utm_source=claude_code) (Frey J. et al., 2024, Agronomy Journal, 9 citations) — ยืนยันว่าต้องเก็บ batch/block ใน model เสมอ ไม่ว่าจะ significant หรือไม่

[7] [Use of Ranks in One-Criterion Variance Analysis](https://consensus.app/papers/details/8cf64c2969c852c6a186607ef10e3b05/?utm_source=claude_code) (Kruskal W. & Wallis W., 1952, Journal of the American Statistical Association, 12610 citations) — original Kruskal-Wallis paper

[8] [The use of Gompertz models in growth analyses, and new Gompertz-model approach: An addition to the Unified-Richards family](https://consensus.app/papers/details/cd41380ae0955137a03a08e39e44218d/?utm_source=claude_code) (Tjørve K. & Tjørve E., 2017, PLoS ONE, 708 citations) — comprehensive review ของ Gompertz parametrisations; ใช้เลือก form ที่ appropriate

[9] [Reliability and Feasibility of Linear Mixed Models in Fully Crossed Experimental Designs](https://consensus.app/papers/details/c5143b307c0251f0a3d7fadb4c516941/?utm_source=claude_code) (Scandola M. et al., 2024, Advances in Methods and Practices in Psychological Science, 22 citations) — step-by-step guide สำหรับ LMM random effects structure; ใช้เมื่อ decide random slope vs intercept

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
