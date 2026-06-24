# R5-A: Continuous Method Comparison — CV vs Expert
**VitroVision | YSC 2027 → ISEF (CSBI)**
**วันที่:** 2026-06-21 | **Agent:** R5-A | **Status:** FINAL

---

## VERDICT

สำหรับ primary endpoint `green_coverage_pct` (continuous 0–100%) และ secondary endpoints (NGRDI, ExG, brown%, LCI) — **วิธีมาตรฐานที่ยอมรับในสาขาคือ Bland-Altman plot + LoA เป็นหัวใจหลัก ร่วมกับ ICC(2,1) absolute agreement และ Spearman ρ เป็นตัวเสริม** ไม่ใช่ correlation อย่างเดียว

**เหตุผลสำคัญ:**
- Correlation (Pearson r / Spearman ρ) วัด *ความสัมพันธ์* ไม่ใช่ *ความตรงกัน* — สองวิธีที่ให้ค่าต่างกันสองเท่าก็ได้ r = 1.0 ได้ [[Giavarina 2015](https://consensus.app/papers/details/7939012957ff5ed797557cfed025a7dd/?utm_source=claude_code), [Bunce 2009](https://consensus.app/papers/details/bbc62319179b59fa9319d1b5804ad283/?utm_source=claude_code)]
- Bland-Altman วัด *bias* และ *LoA* ซึ่งบอกว่า "วิธีใหม่ต่างจากวิธีเก่าแค่ไหนในทางปฏิบัติ"
- ICC วัด *สัดส่วนความแปรปรวนที่เกิดจากตัวอย่างจริง* เทียบกับ error ทั้งหมด
- Bland-Altman + ICC ถูกใช้จริงในงาน crop image analysis validate กับ expert [[Osorio et al. 2020](https://consensus.app/papers/details/9d368982d16f5364bbf88551ab886db2/?utm_source=claude_code)]
- งาน in vitro tissue culture phenotyping ล่าสุดใช้ correlation กับ manual annotation ตรงๆ [[Bethge et al. 2023](https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/?utm_source=claude_code)]

---

## ตารางเปรียบเทียบวิธี Method Comparison

| วิธี | บทบาท | เมื่อใช้ | Threshold ผ่าน | อ้างอิง |
|------|--------|----------|----------------|---------|
| **Bland-Altman plot + LoA** | หัวใจหลัก — วัด bias + interval of agreement | ทุกครั้งที่ compare method A vs B บน continuous variable | LoA ต้องอยู่ใน *acceptable limits* ที่กำหนดล่วงหน้า (เช่น ±10% สำหรับ green_coverage_pct); mean bias → 0 ยิ่งดี | [Giavarina 2015](https://consensus.app/papers/details/7939012957ff5ed797557cfed025a7dd/?utm_source=claude_code), [Goedhart et al. 2021](https://consensus.app/papers/details/c3138f8fe4d75de59696c734a38fea6b/?utm_source=claude_code) |
| **ICC(2,1) Absolute Agreement** | วัด inter-rater reliability รวม systematic bias | มี ≥2 expert + CV วัดชุดเดียวกัน; rater เป็น "random sample" จาก population | ICC < 0.5 = poor; 0.5–0.75 = moderate; **0.75–0.90 = good; >0.90 = excellent** | [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code), [Andrade 2026](https://consensus.app/papers/details/9f77e141e416577d93700393c7459cdb/?utm_source=claude_code) |
| **ICC(3,1) Consistency** | วัด pattern agreement โดยไม่รวม systematic bias | เมื่อสนใจแค่ rank/trend ไม่ใช่ absolute value | เดียวกับ ICC(2,1) แต่ interpret ต่างกัน — ถ้า Consistency > Absolute Agreement บอกว่ามี systematic bias | [Liljequist et al. 2019](https://consensus.app/papers/details/4e405215b70a567caffa4271ad95cc90/?utm_source=claude_code) |
| **Spearman ρ** | ตัวเสริม — วัด monotonic rank-order agreement | ข้อมูลไม่ปกติ / ordinal-like / ต้องการ rank correlation; ไม่แทน Bland-Altman | ρ ≥ 0.7 = ยอมรับได้; ≥ 0.9 = ดีมาก (ค่าไม่ standardize เหมือน ICC) | [Bunce 2009](https://consensus.app/papers/details/bbc62319179b59fa9319d1b5804ad283/?utm_source=claude_code) |
| **Pearson r** | **ใช้เป็น primary ไม่ได้** — วัดแค่ linear relationship | เสริมเฉพาะในบริบท regression/prediction; ไม่ใช้แทน Bland-Altman | — | [Giavarina 2015](https://consensus.app/papers/details/7939012957ff5ed797557cfed025a7dd/?utm_source=claude_code), [Silveira et al. 2024](https://consensus.app/papers/details/03ab450e1f6256168ee8dec2ea5b6b0a/?utm_source=claude_code) |

---

## ICC Model Selection: ICC(2,1) vs ICC(3,1) สำหรับ VitroVision

```
คำถาม: expert ในการทดสอบนี้ = "ตัวอย่างจาก population of experts" หรือ "fixed rater ที่เจาะจง"?
```

- **ถ้า expert ในชุด validation = ตัวแทนจากกลุ่มผู้เชี่ยวชาญทั่วไป** → ใช้ **ICC(2,1) two-way random, absolute agreement** ✓
- ถ้า expert เหล่านี้จะถูกใช้เป็น rater เฉพาะตลอดโครงงาน (fixed) → ICC(3,1) two-way mixed, consistency
- **VitroVision แนะนำ ICC(2,1) absolute agreement** เพราะ:
  1. ต้องการพิสูจน์ว่า CV ให้ค่า absolute ตรงกับผู้เชี่ยวชาญ ไม่ใช่แค่ rank
  2. Expert ที่ใช้ validate ≠ expert กลุ่มเดิมที่จะใช้ production
  3. Andrade (2026) แนะนำ two-way mixed absolute agreement สำหรับ interrater ส่วนใหญ่

> ⚠️ ต้องรายงาน: model (two-way random/mixed), type (single/mean measures), definition (absolute agreement/consistency), CI 95% — ดู [Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code)

---

## คำแนะนำ: สิ่งที่ต้องรายงานใน Validation Section

### ขั้นต่ำที่ต้องมี (minimum reportable set)

| ตัวแปร/สถิติ | ค่าที่รายงาน | เกณฑ์ผ่าน (สำหรับ green_coverage_pct) |
|-------------|-------------|--------------------------------------|
| **Mean Bias** (Bland-Altman) | ค่า mean difference (CV − Expert) ± SD | |mean bias| ≤ 5 percentage points แนะนำ |
| **95% LoA** (Bland-Altman) | [lower LoA, upper LoA] | LoA ทั้งสองอยู่ใน ±10–15 pp (กำหนดล่วงหน้าตาม clinical relevance) |
| **ICC(2,1)** | ICC estimate + 95% CI | ICC ≥ 0.75 (good); target ≥ 0.90 (excellent) |
| **Spearman ρ** | ρ + p-value | ρ ≥ 0.80 |
| **n ขวด** | จำนวน unit ที่ใช้ + จำนวน expert | n ≥ 30 ขวด แนะนำ (ดู R5-D) |
| **Bland-Altman plot** | ภาพ — x = mean(CV, Expert), y = diff | ไม่มีรูปแบบ systematic (funnel/trend) |

### ตัวเสริมที่เพิ่ม credibility (optional แต่แนะนำ)

| สถิติ | เหตุผล |
|-------|--------|
| Inter-expert agreement (ICC ระหว่าง expert 1 vs expert 2) | แสดงว่า "gold standard" เองก็มี noise — ช่วย contextualize LoA ของ CV |
| Percentage differences plot (Bland-Altman แบบ %) | กรณี range ของ green_coverage กว้าง (0–100%) อาจมี heteroscedasticity |
| Scatter plot (CV vs Expert) + regression line | visual แสดง overall relationship ก่อน Bland-Altman |
| RMSE (root mean squared error) | metric เพิ่มเติมที่สาย CV นิยมรายงาน |

---

## หลักฐานจาก Plant/Crop Domain

### Osorio et al. 2020 — ตัวอย่างที่ตรงที่สุด
> **[A Deep Learning Approach for Weed Detection in Lettuce Crops Using Multispectral Images](https://consensus.app/papers/details/9d368982d16f5364bbf88551ab886db2/?utm_source=claude_code)**
> Kavir Osorio et al., 2020, AgriEngineering, 197 citations

- งานนี้ validate **coverage percentage ของวัชพืช** (continuous) จาก image analysis → เทียบกับ expert estimations หลายคน
- ใช้ครบ: **Bland-Altman plot + ICC + Dunn's test** เป็น statistical validation framework
- ผลลัพธ์: แสดงว่า DL methods ลด subjectivity ของ human estimation ได้
- **นี่คือ blueprint ที่ VitroVision ควร follow** — domain, metric, และ design ใกล้เคียงมาก

### Bethge et al. 2023 — In Vitro TC Phenotyping
> **[Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture](https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/?utm_source=claude_code)**
> Hans Bethge et al., 2023, Plant Methods, 16 citations

- พัฒนาระบบ phenotyping สำหรับ in vitro plant culture โดยเฉพาะ — ถ่ายผ่านขวดปิดผนึก
- validate RGB image segmentation pipeline (random forest) กับ **manual pixel annotation**
- รายงาน "very strong correlation" กับ manual annotation → แสดงว่า field ยอมรับวิธี correlation validate กับ manual annotation แต่ในยุคปัจจุบัน Bland-Altman จะ rigorous กว่า
- **Relevant มากสำหรับ VitroVision** — prove of concept ว่า TC vessel imaging + validation ทำได้จริง

### Chopin et al. 2018 — Color/Coverage Field Phenotyping
> **[Land-based crop phenotyping by image analysis: consistent canopy characterization from inconsistent field illumination](https://consensus.app/papers/details/2125c6b5d648596a96ea9c4152c7da31/?utm_source=claude_code)**
> Joshua Chopin et al., 2018, Plant Methods, 23 citations

- validate canopy colour metrics กับ ground truth colour checker
- ใช้ least squares error + SD เป็น validation metric
- แสดงปัญหา illumination variation — relevant กับ VitroVision (light consistency ใน setup)

---

## ข้อควรระวัง

1. **Bland-Altman ไม่ตัดสินว่า LoA "ผ่าน" หรือ "ไม่ผ่าน"** — ต้องกำหนด acceptable limits ล่วงหน้า (a priori) ก่อนเก็บข้อมูล มิฉะนั้นถูก reviewer ตั้งคำถามได้ [[Giavarina 2015](https://consensus.app/papers/details/7939012957ff5ed797557cfed025a7dd/?utm_source=claude_code)]

2. **Heteroscedasticity** — ถ้า green_coverage range กว้าง (0–100%) variance ของ difference อาจเพิ่มตาม magnitude → ต้องใช้ proportional Bland-Altman (% difference plot) หรือ log-transform [[Goedhart et al. 2021](https://consensus.app/papers/details/c3138f8fe4d75de59696c734a38fea6b/?utm_source=claude_code)]

3. **ICC form ต้องระบุชัด** — ICC(2,1) กับ ICC(3,1) ให้ค่าต่างกันถ้ามี systematic bias; ถ้ารายงานแค่ "ICC" โดยไม่ระบุ model ถือว่า incomplete [[Koo & Mae 2016](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code), [ten Hove et al. 2022](https://consensus.app/papers/details/9a91923f2d035b8eab74cbd0b386b475/?utm_source=claude_code)]

4. **SAM segmenter เปลี่ยน → ค่าเลื่อน systematic** — LoA ใหม่จะสะท้อน bias จาก segmentation algorithm ใหม่; ต้อง validate ใหม่ทั้งหมด ไม่ใช่แค่ re-run threshold เดิม

5. **Expert เองมี inter-rater variability** — ควรคำนวณ ICC ระหว่าง expert ด้วย เพื่อ contextualize ว่า "gold standard" มี noise เท่าไร ก่อนวัดว่า CV ตรงกับ expert แค่ไหน

6. **Spearman ρ ≠ substitute สำหรับ Bland-Altman** — ρ สูง (เช่น 0.95) ไม่หมายความว่า agreement ดี เพราะวัดแค่ rank order [[Bunce 2009](https://consensus.app/papers/details/bbc62319179b59fa9319d1b5804ad283/?utm_source=claude_code), [Choi et al. 2017](https://consensus.app/papers/details/aa3a310cc13353a2963c1ce766afed84/?utm_source=claude_code)]

---

## สรุป Decision Tree สำหรับ VitroVision

```
Validation Design:
├── Primary endpoint: green_coverage_pct (continuous)
├── n ขวด → ดู R5-D (แนะนำ ≥30)
├── Expert ≥ 2 คน ประเมินอิสระ
│
├── Step 1: วัด inter-expert ICC(2,1) → ถ้า <0.75 = "gold standard" เองไม่ reliable
├── Step 2: Bland-Altman (CV vs mean-of-experts) → mean bias + LoA
│            ✓ กำหนด acceptable LoA ล่วงหน้า (เช่น ±10 pp)
├── Step 3: ICC(2,1) absolute agreement (CV + experts รวม)
│            ✓ target ≥ 0.75 (good), ideal ≥ 0.90
├── Step 4: Spearman ρ เสริม
└── Step 5: ทำซ้ำสำหรับ secondary endpoints (NGRDI, ExG, brown%)
```

---

## References (verified จาก Consensus)

1. [Understanding Bland Altman analysis](https://consensus.app/papers/details/7939012957ff5ed797557cfed025a7dd/?utm_source=claude_code) — Giavarina D., 2015, Biochemia Medica, 3394 citations
2. [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://consensus.app/papers/details/9e40afb2fe3c5d48b30188f4667b5efd/?utm_source=claude_code) — Koo TK & Mae AY, 2016, Journal of Chiropractic Medicine, 24359 citations
3. [A Deep Learning Approach for Weed Detection in Lettuce Crops Using Multispectral Images](https://consensus.app/papers/details/9d368982d16f5364bbf88551ab886db2/?utm_source=claude_code) — Osorio K. et al., 2020, AgriEngineering, 197 citations
4. [BA-plotteR - A web tool for generating Bland-Altman plots](https://consensus.app/papers/details/c3138f8fe4d75de59696c734a38fea6b/?utm_source=claude_code) — Goedhart J. et al., 2021, Research in Veterinary Science, 37 citations
5. [Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture](https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/?utm_source=claude_code) — Bethge H. et al., 2023, Plant Methods, 16 citations
6. [Correlation, agreement, and Bland-Altman analysis](https://consensus.app/papers/details/bbc62319179b59fa9319d1b5804ad283/?utm_source=claude_code) — Bunce C., 2009, American Journal of Ophthalmology, 238 citations
7. [Updated guidelines on selecting an intraclass correlation coefficient for interrater reliability](https://consensus.app/papers/details/9a91923f2d035b8eab74cbd0b386b475/?utm_source=claude_code) — ten Hove D. et al., 2022, Psychological Methods, 72 citations
8. [Intraclass correlation – A discussion and demonstration of basic features](https://consensus.app/papers/details/4e405215b70a567caffa4271ad95cc90/?utm_source=claude_code) — Liljequist D. et al., 2019, PLoS ONE, 796 citations
9. [A primer on the intraclass correlation coefficient as a measure of reliability](https://consensus.app/papers/details/9f77e141e416577d93700393c7459cdb/?utm_source=claude_code) — Andrade C., 2026, Indian Journal of Psychiatry, 1 citation
10. [Land-based crop phenotyping by image analysis](https://consensus.app/papers/details/2125c6b5d648596a96ea9c4152c7da31/?utm_source=claude_code) — Chopin J. et al., 2018, Plant Methods, 23 citations

---

*ทุก URL ยืนยันจาก Consensus search — ห้าม fabricate ดู `_citation_audit.md` สำหรับ gate*

---

Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
