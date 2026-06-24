# R5B — Ordinal/Categorical Validation: κ ที่ถูกต้องสำหรับ VitroVision

**สถานะ:** เสร็จสมบูรณ์ (2026-06-21)
**โดย:** Research Sub-agent R5-B
**บริบท:** VitroVision (Capsicum TC) — validate 2 งานแยกกัน: (1) vigor rubric 1–5 (ordinal), (2) 3-class classifier healthy/contaminated/dead (nominal-ordered)

---

## VERDICT (สรุปหลัก)

| งาน | metric หลัก | เหตุผล | threshold ขั้นต่ำ |
|---|---|---|---|
| **Vigor 1–5 (ordinal)** | **Quadratic-weighted κ (QWK)** | ลงโทษ error ที่ไกลกว่า (เช่น 1 vs 5) หนักกว่า error ที่ใกล้ (1 vs 2) — ตรงกับธรรมชาติ ordinal | ≥ 0.61 (substantial) |
| **3-class nominal** | **Unweighted κ (Cohen's κ)** | ทุก class-error มีน้ำหนักเท่ากัน (healthy≠contaminated = contaminated≠dead) — ไม่มี ordering ที่ชัดเจน | ≥ 0.61 (substantial) |
| เสริมทั้งคู่ | **Krippendorff's α** | ถ้ามี ≥2 rater หรือมี missing data | ≥ 0.667 (Krippendorff เอง) |
| เสริม 3-class | **Gwet's AC1** | ถ้าคาดว่า class distribution skewed (เช่น healthy >> dead) | รายงานคู่กับ κ |

> ⚠️ **C-05 Warning ยังคงบังคับใช้:** κ ของ vigor (ordinal) และ κ ของ 3-class (nominal) คือ **metric คนละตัวกัน** — ต้องรายงานแยก label ชัดเจนในทุกตาราง/กราฟ

---

## ตารางเปรียบเทียบวิธี

| วิธี | เหมาะเมื่อไหร่ | ข้อควรระวัง | threshold (Landis & Koch 1977) | อ้างอิง |
|---|---|---|---|---|
| **Unweighted κ (Cohen's)** | Nominal categories, error ทุกประเภทมีน้ำหนักเท่ากัน | ไวต่อ prevalence — ถ้า class skewed κ จะต่ำแม้ agree สูง | 0.41–0.60 = moderate; 0.61–0.80 = substantial; >0.80 = almost perfect | McHugh (2012) [1] |
| **Linear-weighted κ** | Ordinal 5-class ที่ error แต่ละ step มีความสำคัญเท่ากัน | น้อยกว่า QWK ในการลงโทษ extreme error | เหมือน unweighted | Yılmaz (2025) [2] |
| **Quadratic-weighted κ (QWK)** | **Ordinal scale (vigor 1–5)** — error ไกลกว่า = แย่กว่ามาก | ค่าสูงกว่า linear-weighted เสมอ; มีความสัมพันธ์กับ ICC และ Pearson r | 0.61–0.80 = substantial | van Oest (2026) [3], de Raadt et al. (2021) [4], Andrés et al. (2019) [5] |
| **Krippendorff's α** | ≥2 rater, มี missing data, ต้องการ scale-agnostic metric | คำนวณซับซ้อนกว่า; ต้องระบุ metric function (ordinal/nominal) | α ≥ 0.667 (Krippendorff เอง); ≥ 0.800 ideal | Zapf et al. (2016) [6], Marzi et al. (2024) [7] |
| **Gwet's AC1** | เสริม κ เมื่อ class prevalence สูง/ต่ำมาก (ceiling/floor effect) | ไม่ใช่ substitute ของ κ โดยตรง — property ต่างกันพื้นฐาน | ≥ 0.61 (ใช้ Landis & Koch เป็น guideline เท่านั้น) | Vach et al. (2023) [8], Tan et al. (2023) [9], Zec et al. (2017) [10] |

---

## คำแนะนำเฉพาะ VitroVision

### งาน 1: Vigor Rubric 1–5 (Ordinal)

**metric หลัก → Quadratic-Weighted κ (QWK)**

เหตุผล:
- Scale 1–5 มี ordering ชัดเจน: vigor 1 (dead/no growth) → 5 (vigorous, ideal)
- Error ที่ expert ให้ 2 แต่ CV ให้ 5 มีความหมายต่างกับ error ที่ expert ให้ 2 แต่ CV ให้ 3
- QWK ลงโทษ error ไกลหนักกว่า — สอดคล้องกับ biological reality
- QWK มีความสัมพันธ์กับ ICC(3,1) และ Pearson r ซึ่งหมายความว่าถ้า QWK สูง composite score CV ก็ตรงกับ expert จริง [3][4][5]

**วิธีรายงาน:**
```
QWKvigour = 0.XX (95% CI [a, b]), n = XX ภาพ, 2 rater
ตีความ: substantial agreement (Landis & Koch 1977)
```

**threshold ขั้นต่ำ YSC/ISEF:** QWK ≥ 0.61 (substantial); ควรเป้า ≥ 0.70

**เสริม:** รายงาน Mean Absolute Error (MAE) ระหว่าง CV score กับ expert score ด้วย — เป็น intuitive metric ที่ judge เข้าใจง่าย

---

### งาน 2: 3-class Classifier (healthy / contaminated / dead)

**metric หลัก → Unweighted Cohen's κ**

เหตุผล:
- 3 class มี partial ordering (dead < contaminated < healthy ในแง่ TC outcome) แต่ **ไม่มี numeric distance** ที่ชัดเจน — contaminated ≠ midpoint ระหว่าง healthy กับ dead
- ใช้ unweighted κ เป็น standard nominal inter-rater metric

**⚠️ ความเสี่ยง Ceiling Effect / Prevalence Paradox:**
ถ้าในชุดข้อมูล healthy >> contaminated + dead (ซึ่งน่าจะเป็น ถ้าเก็บจากขวด TC ปกติ):
- κ จะต่ำกว่าที่ควรจะเป็น ทั้งที่ % agreement สูง [11]
- **แก้ไข:** รายงาน Gwet's AC1 คู่กับ κ เสมอ [8][9][10]

**วิธีรายงาน:**
```
Cohen's κ = 0.XX (95% CI [a, b]), Gwet's AC1 = 0.XX
Observed agreement = XX%
Per-class: sensitivity healthy/contaminated/dead = XX/XX/XX%
Confusion matrix แนบ
```

**threshold ขั้นต่ำ:** κ ≥ 0.61 หรือ AC1 ≥ 0.70 (ถ้า κ ต่ำเพราะ prevalence)

---

## Ceiling Effect — กลไก + วิธีรายงาน

### กลไก
เมื่อ expert ทั้ง 2 คนเห็นตรงกันสูงมาก (เช่น agree 95%) แต่ categories skewed (เช่น 90% ของภาพเป็น healthy):
- Expected agreement by chance (Pe) ก็สูงตาม → κ = (Po - Pe)/(1 - Pe) จะต่ำกว่าที่ควร
- Feinstein & Cicchetti (1990) เรียกว่า "kappa paradox" — high agreement but low kappa [11]
- เกิดได้ใน contamination detection ที่ healthy ครองส่วนใหญ่

### วิธีแก้และรายงาน

1. **รายงาน Po (observed agreement %) เสมอ** — อย่ารายงานแค่ κ โดดๆ
2. **รายงาน Gwet's AC1 คู่กัน** — AC1 stable กว่า κ เมื่อ prevalence สูง [8][9][10]
3. **Specific agreement รายคลาส** — รายงาน positive agreement / negative agreement แยก
4. **อย่าบอกว่า agreement แย่ เพียงเพราะ κ ต่ำ** — ถ้า Po สูงและ AC1 สูง ระบบดี; κ ต่ำเพราะ paradox ไม่ใช่เพราะ error

**ตัวอย่างการรายงานที่ถูกต้อง:**
```
"Cohen's κ = 0.52 อาจสะท้อน prevalence paradox (healthy = 78% ของ dataset)
Gwet's AC1 = 0.81 (substantial), observed agreement = 89%
ตีความ: ระบบมี agreement ดี — κ ต่ำเป็นผลของ class imbalance ไม่ใช่ error จริง"
```

---

## Landis & Koch (1977) — ยังใช้ได้ไหม?

**ตอบ: ใช้เป็น guideline ได้ แต่ต้องใช้ด้วยความระมัดระวัง**

- Landis & Koch (1977) เป็น threshold ที่ใช้กันอย่างแพร่หลายที่สุด — ยังคงถูก cite อย่างกว้างขวางในปี 2020s
- McHugh (2012) ตั้งข้อสังเกตว่า threshold ของ Landis & Koch อาจ "too lenient" สำหรับงาน health/clinical — threshold 0.41 ถือว่า moderate อาจไม่เพียงพอ [1]
- **สำหรับ VitroVision (YSC/ISEF context):** ใช้ Landis & Koch เป็น reference แต่ target เองที่ ≥ 0.70 (substantial–almost perfect boundary)
- **ใน plant phenotyping:** TomatoMAP study (2025) [12] ใช้ Cohen's Kappa statistics กับ inter-rater agreement ระหว่าง 5 domain experts — ยืนยันว่ายังเป็น standard ในสาขา

| κ | Landis & Koch label | คำแนะนำสำหรับ VitroVision |
|---|---|---|
| < 0.00 | Poor | ❌ ไม่ยอมรับ |
| 0.00–0.20 | Slight | ❌ ไม่ยอมรับ |
| 0.21–0.40 | Fair | ❌ ไม่ยอมรับ |
| 0.41–0.60 | Moderate | ⚠️ รายงาน limitation ชัดเจน |
| 0.61–0.80 | Substantial | ✅ acceptable minimum |
| 0.81–1.00 | Almost perfect | ✅ target ideal |

---

## Plant Phenotyping — Evidence จาก Literature

| paper | งานที่ทำ | validation metric | ผล |
|---|---|---|---|
| Zhang et al. (2025) TomatoMAP [12] | Image-based phenotyping 50 BBCH stages, 5 expert rater | Cohen's Kappa + inter-rater heatmap | AI comparable to expert agreement |
| Zhang et al. (2017) Soybean IDC [13] | ML iron deficiency chlorosis scoring vs expert | expert-rating equivalent scores | genome-wide association confirmed validity |
| Souza et al. (2023) Soybean seed vigor [14] | Seed vigor classification (image-based) vs specialist | accuracy 80.17% vs manual | automatable ≥ expert |
| Qiao et al. (2023) Rice seed vigor [15] | Multispectral vigor testing vs germination rate | Pearson r = −0.9874 (vigor index correlation) | strong agreement CV vs conventional |
| Liu et al. (2026) Bacterial TC detection [16] | Contamination detection in Alocasia TC | mAP50 = 0.949 | industrial-grade precision |

**ข้อสังเกต:** ใน plant phenotyping literature ส่วนใหญ่ใช้ accuracy/mAP เป็น primary metric แต่ paper ที่ validate ต่อ expert human rating ใช้ Cohen's κ (TomatoMAP) หรือ Pearson r (vigor studies) — สอดคล้องกับที่แนะนำ: QWK สำหรับ continuous ordinal score, κ สำหรับ categorical class

---

## แผนปฏิบัติ VitroVision

### ขั้นตอนหลังเก็บข้อมูล
```python
# Vigor 1–5 (ordinal)
from sklearn.metrics import cohen_kappa_score
qwk = cohen_kappa_score(expert_scores, cv_scores, weights='quadratic')

# 3-class nominal
kappa_nominal = cohen_kappa_score(expert_class, cv_class, weights=None)

# Krippendorff alpha (ถ้า rater ≥ 2)
import krippendorff
alpha = krippendorff.alpha(reliability_data, level_of_measurement='ordinal')

# Gwet's AC1 (เสริม 3-class)
# ใช้ irrCAC library (R) หรือ pingouin (Python)
import pingouin as pg
# gwet_ac1 = pg.intraclass_corr(...)  # ดู pingouin docs
```

### สิ่งที่ต้องรายงานใน paper/poster
1. **Vigor:** QWK, MAE, scatter plot (CV score vs expert score)
2. **3-class:** Unweighted κ, Gwet's AC1, confusion matrix, per-class sensitivity/specificity
3. **ทั้งคู่:** n (จำนวนภาพ), จำนวน rater, 95% CI bootstrap, observed agreement %

---

## References (Verified via Consensus)

[1] [Interrater reliability: the kappa statistic](https://consensus.app/papers/details/d8b550f8ffae56d6b6c2d46386b714e9/?utm_source=claude_code) — McHugh (2012), Biochemia Medica, 16,513 citations

[2] [Effect of Weighting Schemes on Weighted Kappa Coefficients in Multi-Rater Agreement Studies with Ordinal Categories](https://consensus.app/papers/details/87d81d655e1254ffb94ce1b8288cac18/?utm_source=claude_code) — Yılmaz (2025), Politeknik Dergisi

[3] [Quadratically Weighted Agreement Coefficients: Interpretations and Connections](https://consensus.app/papers/details/9d258e7108b85c26a4f797029e585468/?utm_source=claude_code) — van Oest et al. (2026), Psychometrika

[4] [A Comparison of Reliability Coefficients for Ordinal Rating Scales](https://consensus.app/papers/details/6c4d13618215505ca61bb61a12ead2e3/?utm_source=claude_code) — de Raadt et al. (2021), Journal of Classification, 100 citations

[5] [Hubert's multi-rater kappa revisited](https://consensus.app/papers/details/a4ced243156f5759af11b4acea4f0406/?utm_source=claude_code) — Andrés et al. (2019), British Journal of Mathematical and Statistical Psychology, 19 citations

[6] [Measuring inter-rater reliability for nominal data – which coefficients and confidence intervals are appropriate?](https://consensus.app/papers/details/9479c38e3e6d5c109876231e031b42a9/?utm_source=claude_code) — Zapf et al. (2016), BMC Medical Research Methodology, 330 citations

[7] [K-Alpha Calculator–Krippendorff's Alpha Calculator](https://consensus.app/papers/details/ec45eba2d1f45cd8b8cfbf38d86bce80/?utm_source=claude_code) — Marzi et al. (2024), MethodsX, 231 citations

[8] [Gwet's AC1 is not a substitute for Cohen's kappa – A comparison of basic properties](https://consensus.app/papers/details/7bd54225bfa6593d9057bf3483af080b/?utm_source=claude_code) — Vach et al. (2023), MethodsX, 66 citations

[9] [Quantifying Interrater Agreement and Reliability Between Thoracic Pathologists: Paradoxical Behavior of Cohen's Kappa](https://consensus.app/papers/details/a1a2f007ac275150a35a84f0fd8fe546/?utm_source=claude_code) — Tan et al. (2023), JTO Clinical and Research Reports, 21 citations

[10] [High Agreement and High Prevalence: The Paradox of Cohen's Kappa](https://consensus.app/papers/details/1e00133b54d05318a97a4681577d1b3a/?utm_source=claude_code) — Zec et al. (2017), The Open Nursing Journal, 139 citations

[11] [High agreement but low kappa: I. The problems of two paradoxes](https://consensus.app/papers/details/504906d3c1ca5759b89e1ad889d234f6/?utm_source=claude_code) — Feinstein & Cicchetti (1990), Journal of Clinical Epidemiology, 2,934 citations

[12] [Tomato Multi-Angle Multi-Pose Dataset for Fine-Grained Phenotyping](https://consensus.app/papers/details/cdbc94a49ca05984b6ae84b556986a88/?utm_source=claude_code) — Zhang et al. (2025), Scientific Data, 1 citation

[13] [Computer vision and machine learning for robust phenotyping in genome-wide studies](https://consensus.app/papers/details/a48ca2a1a7085b14a1930f9784b2b07a/?utm_source=claude_code) — Zhang et al. (2017), Scientific Reports, 90 citations

[14] [Soybean seed vigor classification through an effective image learning-based approach](https://consensus.app/papers/details/a74a3730e16b589daf8e82793ee9db37/?utm_source=claude_code) — Souza et al. (2023), Multimedia Tools and Applications, 5 citations

[15] [Vigour testing for the rice seed with computer vision-based techniques](https://consensus.app/papers/details/d854d0ba301c53df99536629453a00e6/?utm_source=claude_code) — Qiao et al. (2023), Frontiers in Plant Science, 18 citations

[16] [Intensity-Texture Enhanced Swin Fusion for Bacterial Contamination Detection in Alocasia Explants](https://consensus.app/papers/details/6f83d778729559738f4cb6148e729781/?utm_source=claude_code) — Liu et al. (2026), Sensors, 0 citations

[17] [A comprehensive guide to study the agreement and reliability of multi-observer ordinal data](https://consensus.app/papers/details/bda06793b9915d6ea4783677845b42a6/?utm_source=claude_code) — Vanbelle et al. (2024), BMC Medical Research Methodology, 17 citations

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
