# R5-C — Aligned Rank Transform ANOVA (ART/ART-C) สำหรับ Plant Experiment

> Sub-agent R5-C | VitroVision (YSC 2027 → ISEF CSBI)
> โจทย์: ยืนยัน ART-ANOVA + ART-C เป็นวิธีที่ถูกต้องสำหรับ 5-treatment (สูตร MS, BAP1, BAP5, BAP5+NAA, IBA1) x 2 batch design ที่ข้อมูลไม่ normal (green_coverage_pct skewed, vigor ordinal 1-5)
> ทุก citation มาจาก Consensus จริง + URL

---

## VERDICT รวม

**ART-ANOVA + ART-C เป็นทางเลือกที่ถูกต้องและแนะนำสำหรับ VitroVision design นี้**

- ART รองรับ factorial design ที่ข้อมูลไม่ normal รวมถึง interaction effects
- ART-C แก้ปัญหา Type I error inflation ที่เกิดจากการใช้ contrast test ปกติบน ART data — validated บน 72,000 synthetic datasets
- มีงานวิจัยจาก Horticulturae ที่ใช้ ART + SAS/ARTool กับ horticultural experiment โดยตรง
- ถ้ามี batch effect (random effect) ควร model ไว้เป็น random factor ใน ART ANOVA (batch as factor) หรือพิจารณา GLMM สำหรับ proportion data (green_coverage_pct)
- Effect size: รายงาน **partial eta squared (η²p)** หรือ **epsilon squared (ε²)** จาก ART ANOVA; ε² มี bias น้อยกว่าเมื่อ n เล็ก

---

## ตารางหลักฐาน

| เรื่อง | สรุปสาระ | อ้างอิง + URL |
|---|---|---|
| ART สำหรับ factorial nonparametric | ART = preprocessing align data → averaged ranks → F-test ปกติ; รองรับ N factors, interaction effects; เป็นทางเลือกที่ accessible กว่าวิธีอื่น | [Wobbrock et al., 2011](https://consensus.app/papers/details/2d2654a99b2e558b83d0d0311ab26151/?utm_source=claude_code) (2,905 citations, CHI) |
| ART vs permutation methods ใน factorial | เปรียบ ART กับ 3 permutation methods + ANOVA-Type Test ใน 2-factor design: ทุกวิธีมี trade-off ขึ้นกับ distribution, variance, n; ART เป็นหนึ่งใน candidate ที่ใช้ได้จริง | [Harrar et al., 2018](https://consensus.app/papers/details/df1891c6f47a5974896797c2587f1a83/?utm_source=claude_code) (15 citations, J. Applied Statistics) |
| ART กับ count/split-plot (นอก continuous) | ART บน split-plot x count data: performance ไม่ได้เหนือกว่า simple ANOVA เสมอ; ต้องพิจารณา distribution ของข้อมูลจริง | [Yang, 2018](https://consensus.app/papers/details/daea605b4c3d52c48674d9f36b59852e/?utm_source=claude_code) |
| **ART-C post-hoc contrast test** | ART-C แก้ Type I error inflation จาก contrast ปกติบน ART data; validated 72,000 datasets; power สูงกว่า Mann-Whitney U, Wilcoxon, ART-only; **ห้ามใช้กับ Cauchy distribution** | [Elkin et al., 2021](https://consensus.app/papers/details/840aeef0be5c529f853e5f0d1d9af7c7/?utm_source=claude_code) (691 citations, UIST 2021) |
| ART ใน horticultural research | ART + ARTool + SAS ใน horticultural experiment; parametric ปกติไม่เหมาะถ้า non-normal มาก; ART ช่วย test interaction effects ที่ Kruskal-Wallis ทำไม่ได้ | [Durner, 2019](https://consensus.app/papers/details/3c3d048c803459d1a3de8fc2c218c955/?utm_source=claude_code) (14 citations, Horticulturae) |
| Kruskal-Wallis กับ one-way multi-treatment plant | KW เทียบ ANOVA บน yam yield data (5 plots): ทั้งสองให้ผลสอดคล้องกันเมื่อ normality violation แต่ variances homogeneous; **KW ไม่รองรับ interaction** | [Acha, 2018](https://consensus.app/papers/details/6bfbdeb5e2e95f608179512ae1ff8116/?utm_source=claude_code) (J. Applied Stat.) |
| GLMM สำหรับ plant science non-normal data | GLMM ใช้ได้กับ binomial/Poisson/gamma distributions; เหมาะสำหรับ proportion data (เช่น green_coverage_pct ที่เป็น bounded 0-1); รองรับ random effects (batch) | [Madden et al., 2024](https://consensus.app/papers/details/e303828eea7358b3bfe2d6b32daa4307/?utm_source=claude_code) (11 citations, Frontiers in Horticulture) |
| LMM vs repeated measures ANOVA | LMM จัดการ missing data และ nonlinear individual differences ได้ดีกว่า repeated measures ANOVA; เหมาะสำหรับ longitudinal/batch design | [Krueger et al., 2004](https://consensus.app/papers/details/65b713a8dcdc5c9cb37e501483d9aa05/?utm_source=claude_code) (564 citations, Biol. Res. Nursing) |
| Effect size: epsilon squared vs eta squared | ε² มี bias น้อยที่สุดใน one-way ANOVA; ω² มี RMSE น้อยที่สุด; η² มี bias สูงเมื่อ n เล็ก | [Okada, 2013](https://consensus.app/papers/details/6bc20e3f14fe5da8b3b0e26626f2d969/?utm_source=claude_code) (110 citations, Behaviormetrika) |
| Partial eta squared bias correction | partial η²p มี positive bias; ε²p และ ω²p เป็นทางเลือกที่ less biased; หรือใช้ adjusted partial η² | [Mordkoff, 2019](https://consensus.app/papers/details/d11dab2219d55788ad5c931fbfb92339/?utm_source=claude_code) (106 citations, AMPPS) |

---

## คำตอบ 5 ข้อ

### Q1: ART-ANOVA ถูกต้องสำหรับ 5-treatment design ที่ข้อมูลไม่ normal ไหม?

**ใช่ ถูกต้อง** [Wobbrock et al., 2011] พัฒนา ART สำหรับ nonparametric factorial data โดยเฉพาะ รองรับ N factors และ interaction effects ซึ่ง Kruskal-Wallis และ Friedman ทำไม่ได้ [Durner, 2019] ยืนยันการใช้ ART + ARTool ใน horticultural research จริงๆ

**เงื่อนไขที่ต้องระวัง:**
- ข้อมูลต้องไม่ใช่ Cauchy distribution (หางหนักมาก)
- สำหรับ count data / split-plot ART อาจไม่ได้เหนือกว่า ANOVA ปกติเสมอ [Yang, 2018]
- ถ้า green_coverage_pct ถูก treat เป็น proportion (bounded 0-1) ควรพิจารณา GLMM beta regression แทน

### Q2: ART-C vs Dunn's test ต่างกันอย่างไร?

| ประเด็น | Dunn's test | ART-C |
|---|---|---|
| เหมาะสำหรับ | One-way KW (1 factor) | Multifactor ART (factorial) |
| Type I error | ควบคุมได้ใน one-way | ควบคุมได้ใน factorial [Elkin, 2021] |
| Interaction context | ไม่รองรับ | รองรับ |
| Power | ปานกลาง | สูงกว่า Mann-Whitney U, Wilcoxon, ART |

**สรุป:** ถ้า design มีมากกว่า 1 factor (เช่น สูตร × batch) → ใช้ **ART-C** ไม่ใช่ Dunn's test เพราะ Dunn's ออกแบบมาสำหรับ one-way เท่านั้น

### Q3: Effect size ที่เหมาะกับ ART

**แนะนำ:** รายงาน **partial epsilon squared (ε²p)** หรือ **partial omega squared (ω²p)** แทน η² เพราะ:
- η² มี positive bias โดยเฉพาะเมื่อ n เล็ก [Levine et al., 2002; Mordkoff, 2019]
- ε² มี bias น้อยที่สุดใน Monte Carlo study 1,000,000 replications [Okada, 2013]
- ω² มี RMSE น้อยที่สุด [Okada, 2013]

สำหรับ ART specifically: ใช้ η²p/ε²p ที่คำนวณจาก F และ df ใน ART ANOVA output (ARTool คำนวณให้อัตโนมัติ)

**สำหรับ vigor score (ordinal):** สามารถรายงาน **rank-biserial correlation r** สำหรับ pairwise comparison ได้เพิ่มเติม

### Q4: ถ้ามี batch effect ควรใช้ LMM แทน ART ไหม?

**ขึ้นกับโจทย์:**

| สถานการณ์ | Recommendation |
|---|---|
| batch = fixed factor (ต้องการเปรียบบน batch) | ใส่ batch เป็น fixed factor ใน ART ANOVA (สูตร × batch) |
| batch = random factor (ต้องการ generalize ข้าม batch) | ใช้ LMM หรือ GLMM (batch เป็น random effect) |
| green_coverage_pct เป็น proportion 0-1 + batch random | **GLMM beta/logit** [Madden et al., 2024] — เหมาะที่สุด |
| vigor ordinal 1-5 + batch random | Ordinal mixed model หรือ ART + batch as factor |

สำหรับ VitroVision ที่มี 2 batch: batch น้อยเกินไปสำหรับ random effect ที่ estimate ได้ดี → **แนะนำใส่ batch เป็น fixed factor ใน ART ANOVA** (สูตร × batch design) จะเหมาะกว่า LMM

[Krueger et al., 2004] แสดงว่า LMM เหนือกว่า repeated measures ANOVA เมื่อมี missing data หรือ nonlinear individual pattern แต่ VitroVision ไม่ได้มีปัญหานี้

### Q5: ข้อควรระวัง/ข้อผิดพลาดที่พบบ่อยใน ART

1. **Post-hoc contrast ผิดวิธี:** การทำ pairwise comparison บน ART-ranked data โดยตรง (ไม่ใช่ ART-C) จะ inflate Type I error [Elkin et al., 2021] — ต้องใช้ ART-C เสมอ

2. **Interaction term ปัญหา:** ART ยืนยันได้ดีสำหรับ main effects แต่ interaction test ใน ART มี sensitivity ต่ำกว่าบาง permutation method [Harrar et al., 2018] — interpret ด้วยความระมัดระวัง

3. **Distribution outlier:** ART-C ไม่ work กับ Cauchy distribution [Elkin et al., 2021] — ตรวจ QQ plot ก่อน

4. **Data type mismatch:** สำหรับ proportion data (green_coverage_pct) ART treat ว่าเป็น continuous ทั่วไป แต่ GLMM beta regression จะ model bounded nature ได้ถูกต้องกว่า [Madden et al., 2024]

5. **η² overestimate:** การรายงาน η² แทน ε² หรือ ω² จะทำให้ effect size ดูใหญ่เกินจริงเมื่อ n เล็ก [Okada, 2013]

6. **Multiple testing:** ART-C มี family-wise error rate control ใน pairwise — ต้องระบุ adjustment method (เช่น Bonferroni, Holm) อย่างชัดเจน

---

## Recommendation สำหรับ VitroVision

### Primary Analysis

```
Variable: green_coverage_pct (continuous skewed)
Model: ART ANOVA (สูตร × batch, fixed effects)
Post-hoc: ART-C pairwise (5 สูตร, Holm correction)
Effect size: partial ε²p หรือ ω²p
Tool: ARTool (R package 'ARTool') หรือ ARTweb
```

```
Variable: vigor_score (ordinal 1-5)
Model: ART ANOVA เดียวกัน (rank-based เหมาะกับ ordinal)
Post-hoc: ART-C pairwise
Effect size: ε²p + rank-biserial r สำหรับ pairwise
```

### Secondary / Robustness Check

- ถ้า green_coverage_pct ถูก treat เป็น proportion อย่างเคร่งครัด → เพิ่ม GLMM beta regression เป็น sensitivity analysis
- รายงานทั้ง KW (for referees ที่คุ้นเคย) + ART result คู่กันได้ แต่ emphasize ART เพราะรองรับ interaction

### เหตุผลที่เลือก ART-C แทน Dunn's

Dunn's test ออกแบบสำหรับ one-way KW เท่านั้น สำหรับ factorial design (สูตร × batch) ART-C เป็นวิธีเดียวที่ validated สำหรับ multifactor contrast test ใน nonparametric framework [Elkin et al., 2021]

---

## References ทั้งหมด (จาก Consensus)

1. [The aligned rank transform for nonparametric factorial analyses using only anova procedures](https://consensus.app/papers/details/2d2654a99b2e558b83d0d0311ab26151/?utm_source=claude_code) — Wobbrock et al., 2011, CHI (2,905 citations)

2. [An Aligned Rank Transform Procedure for Multifactor Contrast Tests](https://consensus.app/papers/details/840aeef0be5c529f853e5f0d1d9af7c7/?utm_source=claude_code) — Elkin et al., 2021, UIST (691 citations)

3. [Effective Analysis of Interactive Effects with Non-Normal Data Using the Aligned Rank Transform, ARTool and SAS University Edition](https://consensus.app/papers/details/3c3d048c803459d1a3de8fc2c218c955/?utm_source=claude_code) — Durner, 2019, Horticulturae (14 citations)

4. [A comparison of recent nonparametric methods for testing effects in two-by-two factorial designs](https://consensus.app/papers/details/df1891c6f47a5974896797c2587f1a83/?utm_source=claude_code) — Harrar et al., 2018, J. Applied Statistics (15 citations)

5. [A Study on the Performance of the Aligned Rank Transform Procedure for Testing Interaction in Split-plot Designs](https://consensus.app/papers/details/daea605b4c3d52c48674d9f36b59852e/?utm_source=claude_code) — Yang, 2018

6. [Analysis of Yam Yield Data: A Comparison of One-Way ANOVA and Kruskal-Wallis Test](https://consensus.app/papers/details/6bfbdeb5e2e95f608179512ae1ff8116/?utm_source=claude_code) — Acha, 2018

7. [Alternate Forms of the One-Way ANOVA F and Kruskal-Wallis Test Statistics](https://consensus.app/papers/details/22552a3125ab57b49025ccc73a938941/?utm_source=claude_code) — Johnson, 2022, J. Statistics and Data Science Education (35 citations)

8. [The value of generalized linear mixed models for data analysis in the plant sciences](https://consensus.app/papers/details/e303828eea7358b3bfe2d6b32daa4307/?utm_source=claude_code) — Madden et al., 2024, Frontiers in Horticulture (11 citations)

9. [A Comparison of the General Linear Mixed Model and Repeated Measures ANOVA Using a Dataset with Multiple Missing Data Points](https://consensus.app/papers/details/65b713a8dcdc5c9cb37e501483d9aa05/?utm_source=claude_code) — Krueger et al., 2004, Biol. Res. Nursing (564 citations)

10. [Is Omega Squared Less Biased? A Comparison of Three Major Effect Size Indices in One-Way ANOVA](https://consensus.app/papers/details/6bc20e3f14fe5da8b3b0e26626f2d969/?utm_source=claude_code) — Okada, 2013, Behaviormetrika (110 citations)

11. [A Simple Method for Removing Bias From a Popular Measure of Standardized Effect Size: Adjusted Partial Eta Squared](https://consensus.app/papers/details/d11dab2219d55788ad5c931fbfb92339/?utm_source=claude_code) — Mordkoff, 2019, AMPPS (106 citations)

12. [Eta Squared, Partial Eta Squared, and Misreporting of Effect Size in Communication Research](https://consensus.app/papers/details/4a6f579adfc756108256c9c63fd5755c/?utm_source=claude_code) — Levine et al., 2002, Human Communication Research (1,051 citations)

---

## Sign-up/usage message จาก Consensus

Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
