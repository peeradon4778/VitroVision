# _audit_issues.md — Audit ความสอดคล้อง Research Files
**เวอร์ชัน:** 1.0 | **วันที่ audit:** 2026-06-12
**ผู้ audit:** claude-sonnet-4-6 (sub-agent VitroVision)
**ไฟล์ที่ตรวจ:** 01–14 + _decisions_pending.md (รวม 15 ไฟล์)
**เกณฑ์เทียบ:** Research Design v1 (locked 2026-06-11) ตามที่สรุปไว้ใน `10_methods_draft.md` header และ `_decisions_pending.md` §1

---

## ประเภท 1 — Contradiction (ขัดแย้งกันข้ามไฟล์)
*เรียงตามความรุนแรง: อันที่ judge จะเจาะถามก่อน*

---

### [C-01] **CRITICAL** — κ ตัวเลข 2 ชุดขัดกันใน paper เดียวกัน
**ไฟล์ที่ขัด:**
- `05_narrative_problem_objective_impact.md:76` — `κ = 0.627 บนภาพ **สังเคราะห์** 181 ภาพ`
- `10_methods_draft.md:192` — `baseline ปัจจุบัน Cohen's κ=0.6274, weighted F1=0.7496 จาก n=28`

**ปัญหา:** ไฟล์ 05 บอก n=181 ภาพ, ไฟล์ 10 บอก n=28 — dataset ขนาดไม่ตรงกันเลย ทั้งที่อ้าง κ จากแหล่งเดียวกัน (ภาพสังเคราะห์/mock) Judge ISEF/YSC จะถามทันทีว่า "ตัวเลข 181 vs 28 คืออะไร"

**วิธีแก้:** ตรวจ `models/final/metrics.json` ว่า n ที่ใช้จริงคือเท่าไหร่ แล้วแก้ทั้ง 2 ไฟล์ให้ตรงกัน พร้อมระบุให้ชัดว่าเป็น "ภาพสังเคราะห์ n=XX" ทุกที่ที่กล่าวถึง κ=0.627

---

### [C-02] **HIGH** — Post-hoc method ขัดแย้งระหว่างไฟล์ 02 กับ 07 กับ 10
**ไฟล์ที่ขัด:**
- `02_media_formulations_review.md:100` — "KW omnibus → Dunn + **Holm/BH**"
- `07_growthcurve_repeated_measures.md:16` — "Post-hoc **Dunn + Bonferroni**"
- `10_methods_draft.md:341` — "**Kruskal-Wallis + Dunn** = secondary/preliminary เท่านั้น" (primary = ART-C)

**ปัญหา:** ไฟล์ 02 แนะนำ Holm/BH, ไฟล์ 07 แนะนำ Bonferroni, ไฟล์ 10 (source of truth) บอกว่า Dunn เป็น secondary เท่านั้น และ primary คือ ART-C เมื่อ non-normal — สามไฟล์ให้คำตอบต่างกันทั้งที่เขียนวันเดียวกัน

**วิธีแก้:** ยึดไฟล์ 10 เป็นเกณฑ์: primary = LMM (ถ้า normal) หรือ ART-ANOVA+ART-C (ถ้าไม่ normal); Dunn เป็น secondary/preliminary เท่านั้น; correction = Bonferroni (ตามที่ _decisions_pending.md §B2 แนะนำ) แก้ไฟล์ 02 และ 07 ให้สอดคล้อง

---

### [C-03] **HIGH** — "Substantial agreement" threshold κ ขัดกัน
**ไฟล์ที่ขัด:**
- `06_validation_methodology.md:60` — "Acceptable: κ ≥ 0.60 (Landis & Koch: substantial agreement)"
- `05_narrative_problem_objective_impact.md:74` — H1: "Cohen's κ ≥ 0.70" คือ threshold ของ "substantial agreement"

**ปัญหา:** ไฟล์ 06 ระบุ κ ≥ 0.60 = substantial (ตาม Landis & Koch), แต่ไฟล์ 05 บอก κ ≥ 0.70 คือ substantial — ตัวเลข threshold ต่างกัน judge ถามได้

**วิธีแก้:** ไฟล์ 10 (source of truth) ใช้ Acceptable κ ≥ 0.60 / Target κ ≥ 0.80 ซึ่งตรงกับ Landis & Koch ที่ 06 อ้าง ส่วนไฟล์ 05 ที่บอก κ ≥ 0.70 คือตัวเลข hypothesis (ตั้งใจสูงกว่า acceptable) ควรแก้ไฟล์ 05 ให้ระบุชัดว่า "H1 ตั้งเป้าที่ κ ≥ 0.70 (เหนือ acceptable ≥ 0.60 ของ Landis & Koch)" เพื่อไม่ให้สับสน

---

### [C-04] **HIGH** — n/สูตร ไม่ตรงกันระหว่างไฟล์เก่า (02) กับ decision ล็อก
**ไฟล์ที่ขัด:**
- `02_media_formulations_review.md:6,18,88,90` — ใช้ "5 สูตร × 20 ขวด" / "n=20/กลุ่ม (รวม 100)" ตลอด
- `10_methods_draft.md:105` + `_decisions_pending.md:17` — ล็อกที่ "≥2 batch → pool n ≈ 40 ขวด/สูตร · over-sow ~24–25 ขวด/สูตร/batch"

**ปัญหา:** ไฟล์ 02 วิเคราะห์ power บน n=20/สูตร แต่ decision ล็อกแล้วที่ n≈40/สูตร (pool 2 batch) — power analysis ใน 02 อ้างอิง assumption ผิด และตัวเลข 100 ขวดรวม (20×5) กลายเป็นตัวเลขต่อ batch ไม่ใช่ total

**วิธีแก้:** เพิ่มหมายเหตุใน `02` ว่า "n=20/สูตร = ต่อ batch; total pool n≈40 ตาม decision v1 locked 2026-06-11" — ไม่ต้องแก้ power analysis เพราะ 02 เขียนก่อน lock แต่ต้องไม่ให้เข้าใจผิดว่า total = 100

---

### [C-05] **MEDIUM** — Hypothesis framing ของ validation ขัดกันระหว่างไฟล์
**ไฟล์ที่ขัด:**
- `05_narrative_problem_objective_impact.md:73–75` — H1 ตั้งเป้า "Cohen's κ ≥ 0.70" เป็น classification accuracy (healthy/contaminated/dead) วัดกับ "ground truth ที่ label โดยผู้เชี่ยวชาญ"
- `10_methods_draft.md:268–271` + `06_validation_methodology.md:192–197` — Validation suite (Spearman ρ + κ + ICC) ใช้กับ **ordinal vigor rubric 1–5** ไม่ใช่ 3-class classification

**ปัญหา:** H1 ใน 05 วัด κ กับ 3-class classifier (healthy/contaminated/dead) แต่ validation protocol ใน 06 และ 10 ออกแบบสำหรับ ordinal vigor 1–5 — เป็น task ต่างกันโดยสิ้นเชิง; κ ใน H1 กับ κ ใน validation protocol วัดคนละสิ่ง

**วิธีแก้:** แก้ไฟล์ 05 ให้ระบุชัดว่า H1 = κ ของ **3-class status classifier** (EfficientNet), H2 = ρ/κ/ICC ของ **ordinal vigor phenotyper** (convergent validity) — แยก 2 hypothesis ให้ชัด

---

### [C-06] **MEDIUM** — Dataset ที่ใช้ train คลุมเครือข้ามไฟล์
**ไฟล์ที่ขัด:**
- `04_final_architecture_ux_plan.md:14` — "classifier κ=0.627" (ไม่ระบุ n หรือ dataset ชัด)
- `05_narrative_problem_objective_impact.md:76` — κ=0.627 จาก "181 ภาพสังเคราะห์"
- `10_methods_draft.md:192` — κ=0.6274 จาก "n=28 (CI กว้าง ~±0.20)"

**ปัญหา:** ไฟล์ 04 ไม่ระบุ n, ไฟล์ 05 บอก n=181, ไฟล์ 10 บอก n=28 — 3 ไฟล์ 3 n ต่างกัน

**วิธีแก้:** ดู [C-01] — แก้พร้อมกัน ระบุ n ที่ถูกต้องในทุกไฟล์ให้ตรงกัน

---

### [C-07] **MEDIUM** — Thomas 2026 ยังปรากฏใน 08 เป็น section heading
**ไฟล์ที่ขัด:**
- `08_survival_contamination.md:61–69` — มี section "## 3. Thomas 2026 — ผลการ Verify" ที่รายงานว่า "ไม่พบ paper ที่ตรงกัน" แต่ยังเก็บชื่อ Thomas 2026 ไว้เป็น section
- `10_methods_draft.md:306` — ระบุชัดว่า "Thomas 2026 ที่เคยอ้างใน design ถูกตัดทิ้ง"
- `_decisions_pending.md:24` — 'Thomas 2026" = ผี ตัดทิ้งแล้ว'

**ปัญหา:** แม้ 08 จะ verify ว่า paper นี้ไม่มี และเตือนไว้ท้ายไฟล์ แต่การมี section heading ชื่อ "Thomas 2026" ยังอยู่ทำให้ reader ใหม่อาจเข้าใจผิดว่า paper นี้มีอยู่จริง และยังมีชื่อ Thomas 2026 ปรากฏใน footnote บรรทัด 239 ซึ่งเป็น footer warning

**วิธีแก้:** ใน `08` rename section เป็น "## 3. Citation ที่ Verify ไม่ผ่าน — Thomas 2026 (ผี, ตัดทิ้ง)" และเพิ่ม `**[ตัดทิ้ง — AI hallucination]**` ในหัวข้อ; หรือ collapse เป็น callout box สั้นๆ แทน section เต็ม

---

## ประเภท 2 — ซ้ำซ้อน (เนื้อหาซ้ำกันโดยไม่จำเป็น)

---

### [D-01] **MEDIUM** — Power analysis มี 2 เวอร์ชันที่ดริฟต์กัน
**ไฟล์ที่ซ้ำ:**
- `02_media_formulations_review.md:88–92` — power analysis บน KW, n=20/สูตร
- `10_methods_draft.md:97–105` — power analysis บน KW≈one-way ANOVA, n≈40/สูตร (ตารางครบ)

**ปัญหา:** มี power analysis 2 ชุด assumption ต่างกัน (n ต่างกัน) และข้อสรุปต่างกัน — ไฟล์ 02 สรุปว่า "n=20 เพียงพอ" แต่ไฟล์ 10 พิสูจน์ว่าต้องการ n≈40 สำหรับ medium effect

**วิธีแก้:** ไฟล์ 02 ควรอ้างอิงไปยังไฟล์ 10 (`→ ดู 10_methods_draft.md §1.4 สำหรับ power analysis ฉบับสมบูรณ์`) แทนการ maintain analysis แยก

---

### [D-02] **MEDIUM** — คำอธิบาย hyperhydricity ซ้ำอยู่ 3 ไฟล์
**ไฟล์ที่ซ้ำ:**
- `01_capsicum_tissue_culture.md:43–44` — อธิบาย hyperhydricity + features ที่ CV จับได้
- `13_pgr_morphology.md:67–116` — อธิบาย hyperhydricity ละเอียด + visual features + Bethge precedent
- `10_methods_draft.md:214–219` — §3.6 อธิบาย hyperhydricity + visual proxy + Bethge

**ปัญหา:** เนื้อหา 3 ก้อนครอบคลุมประเด็นเดียวกัน (ลักษณะ hyperhydricity + CV ตรวจจับได้) ทั้ง Bethge 2023 ถูกอ้างถึงใน 13 และ 10 ซ้ำกัน

**วิธีแก้:** ไฟล์ 13 ควรเป็น source of truth สำหรับ hyperhydricity biology; ไฟล์ 10 §3.6 อ้าง "→ ดู `13_pgr_morphology.md` §4"; ไฟล์ 01 ย่อลงเหลือ one-liner reference

---

### [D-03] **MEDIUM** — Gold Standard Paradox อธิบายซ้ำใน 06 และ 10
**ไฟล์ที่ซ้ำ:**
- `06_validation_methodology.md:160–168` — อธิบาย Gold Standard Paradox + Aeffner 2017 + ขั้นตอน interpret
- `10_methods_draft.md:282–290` — §4.5 อธิบาย Gold Standard Paradox เหมือนกันทุกประเด็น + ข้อความ Discussion draft

**ปัญหา:** เนื้อหาซ้อน 100% ระหว่าง 06 §3.3 กับ 10 §4.5 รวมถึง quote เดียวกันจาก Aeffner

**วิธีแก้:** ไฟล์ 10 §4.5 อ้าง `→ ดู `06_validation_methodology.md` §3–§4 สำหรับ rationale เต็ม` แทนการ duplicate ย่อหน้า; เก็บเฉพาะ "ข้อความ Discussion ที่จะใส่จริง" ไว้ใน 10

---

### [D-04] **MEDIUM** — Precedent ArUco อธิบายซ้ำใน 09 และ 10
**ไฟล์ที่ซ้ำ:**
- `09_methods_misc.md:33–44` — ArUco precedents: Wienbruch 2025 + Costa 2024 + การประยุกต์กับ VitroVision
- `10_methods_draft.md:127–128` — §1.8 cite Wienbruch 2025 + Costa 2024 เหมือนกัน

**ปัญหา:** รายละเอียด precedent เหมือนกันทั้ง 2 ไฟล์ (เพียงแต่ 09 ละเอียดกว่า)

**วิธีแก้:** ไฟล์ 10 §1.8 เก็บแค่ citation สั้นๆ + "ดู `09_methods_misc.md` §2 สำหรับ paper details"; ไฟล์ 09 เป็น source

---

### [D-05] **LOW** — Contamination survival analysis methodology ซ้ำใน 08 และ 10
**ไฟล์ที่ซ้ำ:**
- `08_survival_contamination.md:19–57` — KM + log-rank theory + censoring types + few-event caveat + R code
- `10_methods_draft.md:357–364` — §5.5 สรุปเดิม (KM + log-rank + few-event + exact test + Coemans)

**ปัญหา:** §5.5 ใน 10 เป็น condensed version ของ 08 ซ้ำซ้อนพอสมควร

**วิธีแก้:** ไฟล์ 10 §5.5 เพิ่ม `→ methodology rationale: ดู `08_survival_contamination.md`$` และตัด R code ออกจาก 08 ถ้าไม่ได้ใช้เป็น implementation guide

---

### [D-06] **LOW** — Conceptual framework "ปัญหา 3 ชั้น" ซ้ำใน 03, 05
**ไฟล์ที่ซ้ำ:**
- `03_capsicum_economic_context.md:§4–5` — Gap analysis + "ช่องว่าง manual monitoring"
- `05_narrative_problem_objective_impact.md:§1.1–1.3` — ปัญหา 3 ชั้น (เกษตร / ชีววิทยา / เทคนิค)

**ปัญหา:** เนื้อหาส่วนมากใน 05 §1 synthesize มาจาก 03 ซ้ำซ้อนกัน แม้ 05 จะ reference กลับ 03 แต่ข้อมูลก็ถูกเขียนใหม่อีกครั้ง

**วิธีแก้:** เป็น intentional synthesis — รับได้ แต่ถ้าอัปเดต 03 ต้องอัปเดต 05 ด้วย ให้ track เป็น paired files

---

## ประเภท 3 — ไม่ตรง Decision ที่ล็อกแล้ว

---

### [L-01] **HIGH** — ไฟล์ 02 แนะนำ "เพิ่ม BAP กลาง 2–3 mg/L" แต่ design ล็อกแล้ว 5 สูตรตายตัว
**ไฟล์ที่ขัด:**
- `02_media_formulations_review.md:75,96` — "เพิ่ม **BAP ระดับกลาง 2–3 mg/L** (เช่นสูตร B2 = MS + 2.5 BAP)" เป็น priority สูงสุด
- `_decisions_pending.md:15` + `10_methods_draft.md:64–68` — 5 สูตร A=MS, B=BAP1, C=BAP5, D=BAP5+NAA0.05, E=IBA1 ล็อกแล้วใน v1

**ปัญหา:** ไฟล์ 02 ยัง "แนะนำ" เพิ่มสูตรซึ่งเกินไปจาก decision ที่ล็อกแล้ว — ถ้าอ่านไฟล์ 02 ก่อนจะสับสนว่า design ยังไม่เสร็จ

**วิธีแก้:** เพิ่ม note ต้นไฟล์ 02 ว่า "⚠️ ไฟล์นี้เขียนก่อน lock; ข้อแนะนำการเพิ่มสูตรถูกพิจารณาและตัดสินใจไม่เพิ่มใน Research Design v1 (locked 2026-06-11) — ดู `_decisions_pending.md`"

---

### [L-02] **HIGH** — ไฟล์ 02 แนะนำยก NAA เป็น 0.1–0.5 แต่ lock ที่ NAA=0.05
**ไฟล์ที่ขัด:**
- `02_media_formulations_review.md:79,98` — "พิจารณายก NAA เป็น 0.1–0.5 mg/L"
- `_decisions_pending.md:15` + `10_methods_draft.md:67` — สูตร D = BAP5+NAA**0.05** ล็อกแล้ว

**ปัญหา:** เหมือน L-01 — ไฟล์ 02 แนะนำเปลี่ยน NAA ซึ่งขัดกับ decision ล็อก

**วิธีแก้:** แก้พร้อมกับ L-01 ใน note เดียวกัน

---

### [L-03] **HIGH** — ไฟล์ 05 ยังอ้าง n=20/สูตร/100 ขวด ทั้งที่ lock ที่ n≈40
**ไฟล์ที่ขัด:**
- `05_narrative_problem_objective_impact.md:163` — `RC2: n จำกัด (20/สูตร, 100 ขวด)`
- `_decisions_pending.md:17` — "pool n≈40/สูตร · over-sow ~24-25 ขวด/สูตร/batch"

**ปัญหา:** ไฟล์ 05 §6.2 RC2 ยังใช้ n=20/สูตร ซึ่งเป็นค่าก่อน decision lock; total 100 ขวดเป็น per-batch ไม่ใช่ total

**วิธีแก้:** แก้ RC2 ใน 05 เป็น "n จำกัด (~24–25 ขวด/สูตร/batch, pool 2 batch → n≈40/สูตร)" และ update total เป็น ~250 ขวดรวม (ต่อ batch × 2)

---

### [L-04] **MEDIUM** — ไฟล์ 07 สรุปแบบย่อ "Step 1" ยังอ้างนับ ~20 ขวด/สูตร
**ไฟล์ที่ขัด:**
- `07_growthcurve_repeated_measures.md:5` — "5 สูตร MS × ~20 ขวด/สูตร (pool ≥2 batch → n≈40/สูตร)"
- **ข้อดี:** บรรทัดนี้บอก pool → n≈40 ถูกต้อง แต่ "~20 ขวด/สูตร" ในวงเล็บอาจสับสนว่าเป็น 20 รวมหรือ 20 ต่อ batch

**ปัญหา:** คลุมเครือเล็กน้อย แต่ไม่ขัดกันจริง

**วิธีแก้:** แก้เป็น "5 สูตร MS × ~24–25 ขวด/สูตร/batch (pool ≥2 batch → n≈40/สูตร)"

---

### [L-05] **MEDIUM** — ไฟล์ 09 กล่าวถึง ArUco ในบริบทที่ยังไม่ระบุ DICT ชัดเจน
**ไฟล์ที่ขัด:**
- `09_methods_misc.md:42` — "การติด ArUco marker (**DICT_4X4_100**) ข้างขวด..." — ถูกต้อง ✓
- `10_methods_draft.md:127` — "DICT_4X4_100" — ถูกต้อง ✓
- `_decisions_pending.md:19` — "ArUco DICT_4X4_100" — ถูกต้อง ✓

**หมายเหตุ:** ไม่พบ DICT_4X4_50 ในไฟล์ใดเลย — ตัวเลขที่กังวลในโจทย์ไม่ปรากฏในชุดนี้ ถือว่า clean ✅

---

### [L-06] **LOW** — ไฟล์ 05 แนะนำเพิ่มสูตร TDZ เป็น cytokinin-type contrast
**ไฟล์ที่ขัด:**
- `05_narrative_problem_objective_impact.md` (ผ่าน reference ถึง 02 §2.2 ข้อ 4) — แนะนำ TDZ/kinetin เป็น optional
- `_decisions_pending.md` — ไม่มีสูตร TDZ; 5 สูตร A–E ล็อกแล้ว

**ปัญหา:** ระดับต่ำมาก เพราะ 05 mark ว่า "(optional)" แต่ยังอาจสับสน

**วิธีแก้:** เพิ่ม "(ตัดแล้ว ไม่อยู่ใน v1 locked)" ในวงเล็บ

---

## สรุปจำนวน Issue

| ประเภท | จำนวน | Critical/High | Medium | Low |
|--------|--------|---------------|--------|-----|
| Contradiction | 7 | 4 (C-01, C-02, C-03, C-04) | 2 (C-05, C-06) | 1 (C-07) |
| ซ้ำซ้อน | 6 | 0 | 3 (D-01, D-02, D-03) | 3 (D-04, D-05, D-06) |
| ไม่ตรง decision | 6 | 2 (L-01, L-02) | 3 (L-03, L-04, L-05) | 1 (L-06) |
| **รวม** | **19** | **6** | **8** | **5** |

---

## 3 Issue ที่สำคัญสุด (Judge จะเจาะถามก่อน)

1. **[C-01] κ ตัวเลข n ขัดกันสามที่ (n=28 vs n=181 vs ไม่ระบุ)** — judge จะถาม "κ=0.627 มาจากชุดข้อมูลขนาดเท่าไหร่" ถ้าตอบไม่ตรงกัน credibility พัง → แก้ก่อนสุด

2. **[C-05] Validation H1 วัด κ ของ classifier กับ κ ของ vigor rubric คนละ task แต่ถูก lump รวมกัน** — judge CSBI จะถามว่า "ตัวเลข κ ที่อ้างอิงนั้นวัดกับอะไรกันแน่" ซึ่งเป็นปัญหา construct validity → แก้ก่อนนำส่ง proposal

3. **[C-02] Post-hoc method ขัดกัน 3 ไฟล์ (Dunn+Holm/BH vs Dunn+Bonferroni vs ART-C)** — judge จะถาม "ใช้วิธีไหนจริง" ต้องตอบได้ชัดเจนว่า 10 คือ source of truth และวิธีอื่นเก่ากว่า

---

*audit โดย claude-sonnet-4-6 — 2026-06-12 — รายงานนี้เป็นแผนที่ปัญหา*

---

## ✅ Resolution Log — แก้แล้ว 2026-06-12 (claude-opus-4-8)

ground truth ที่ใช้แก้: `models/final/metrics.json` → **κ=0.6274 บน test set n=28; total synthetic dataset 181 = train 126 / val 27 / test 28** (ทั้งสองเลขจริง คนละความหมาย)

| Issue | สถานะ | แก้ที่ |
|---|---|---|
| C-01 | ✅ | `05` H1 + RC1 — ระบุ κ บน test n=28 จาก total 181 (126/27/28) ทุกจุด |
| C-02 | ✅ | `02` §2.3/§2.4 + `07` §1 — supersede เป็น primary ART-C/LMM, Dunn+**Bonferroni** secondary (ยึด `10`) |
| C-03 | ✅ | `05` H1 — ระบุ Landis&Koch substantial = κ≥0.60 (acceptable), H1 target ≥0.70 |
| C-04 | ✅ | `02` banner — "20/สูตร = ต่อ batch", pool 2 batch → n≈40 total |
| C-05 | ✅ | `05` H1 — แยกชัด: κ ของ 3-class classifier ≠ validation ของ ordinal vigor (ρ/wκ/ICC) |
| C-06 | ✅ | `05` (รวมกับ C-01) |
| C-07 | ✅ | `08` §3 rename "[ตัดทิ้ง — AI hallucination]" + callout + footer warning |
| D-01 | ✅ | `02` §2.3 — power analysis ชี้ไป `10` §1.4 (ฉบับสมบูรณ์ n≈40) |
| D-02 | ✅ | `13` §4 = source; `10` §3.6 + `01` ชี้ไป 13 |
| D-03 | ✅ | `10` §4.5 ชี้ไป `06` §3–4 (เก็บเฉพาะ Discussion text) |
| D-04 | ✅ | `10` §1.8 ชี้ไป `09` §2 |
| D-05 | ✅ | `10` §5.5 ชี้ไป `08` |
| D-06 | ☑️ accepted | `03`↔`05` = intentional synthesis (track เป็น paired files, ไม่แก้) |
| L-01 | ✅ | `02` banner — BAP กลาง 2–3 ไม่เพิ่ม (design v1 locked) |
| L-02 | ✅ | `02` banner — NAA คง 0.05 ไม่ยก |
| L-03 | ✅ | `05` RC2 — ~24–25/batch → pool n≈40 |
| L-04 | ✅ | `07` line 5 — "~24–25 ขวด/สูตร/batch" |
| L-05 | ☑️ clean | ไม่พบ DICT_4X4_50 (ถูกต้องอยู่แล้ว) |
| L-06 | ✅ | `05` ⚠️ validate ข้อ 5 + RC4/RC6 — TDZ/design locked เป็น acknowledged limitation |

**สรุป:** 17 issue แก้โดยตรง · D-06 รับเป็น intentional · L-05 clean อยู่แล้ว = ครบ 19/19. ไฟล์ที่แตะ: `01, 02, 05, 07, 08, 10`. **ยังไม่ commit**
