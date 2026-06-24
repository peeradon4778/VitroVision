# R5-E — Survival Analysis สำหรับ Contamination ใน Plant Tissue Culture

> Sub-agent R5-E | VitroVision (YSC 2027 → ISEF CSBI)
> สร้าง: 2026-06-21 | Model: Claude Sonnet 4.6
> โจทย์: ประเมิน best practice สำหรับ survival analysis ของ contamination rate ใน TC พริก — n ~25/กลุ่ม × 5 สูตร × 2 batch, competing event (contaminated vs dead), discrete daily observation, 28-day window
> กฎ citation: ทุก URL มาจาก Consensus จริง — ไม่แต่งขึ้น

---

## VERDICT รวม

| คำถาม | คำตอบสั้น |
|---|---|
| KM + log-rank เหมาะไหม? | **ใช้ได้** สำหรับ descriptive — ต้องระวัง type I error inflation เมื่อ events น้อย |
| ต้องใช้ Fine-Gray (competing risks) ไหม? | **ควรใช้ CIF เสริม** ถ้า dead-not-contaminated ≥ 10% — KM เดี่ยวจะ overestimate cumulative incidence |
| log-rank power เพียงพอไหม (n≈25)? | **มีความเสี่ยง type I error inflation** สูงถึง 28% ในบางสถานการณ์ — ใช้ permutation log-rank แทน asymptotic |
| Contamination rate benchmark? | 0–15% ถือว่า protocol ดี; ≥30% = ปัญหาร้ายแรง — over-sow 20–30% เป็น standard practice |
| รายงาน survival curve อย่างไร? | CIF + median survival time (ถ้าถึง 50%) + number-at-risk table + caveat exploratory |

---

## 1. คำถามที่ 1 — KM + Log-rank เหมาะกับ contamination data แบบนี้ไหม?

**ใช้ได้ — แต่มีข้อจำกัดสำคัญ 3 ข้อ**

### 1.1 ทำไม KM ใช้ได้

Kaplan-Meier estimator ออกแบบมาสำหรับข้อมูล time-to-event ที่มี **right-censoring** โดยตรง [D'Arrigo et al. 2021] ข้อดีหลักคือไม่ต้องสมมติ distribution ล่วงหน้า และใช้ข้อมูล censored ได้อย่างมีประสิทธิภาพ [Hess et al. 2020] ใน TC contamination:

- **Event = วันแรกที่เห็นการปนเปื้อน** (absorbing state — ไม่กลับได้)
- **Censored = ขวดที่สิ้น 28 วันโดยไม่ปนเปื้อน** หรือถูกเก็บออกก่อนกำหนด
- **Survival function S(t) = ความน่าจะเป็นที่ขวดยัง contamination-free ที่เวลา t**

การ observe ทุกวัน 17:00 ทำให้ event time เป็น discrete (ทราบวันที่แน่นอน) ซึ่งดีกว่า interval censoring — KM จัดการได้ตรงไปตรงมา

### 1.2 ข้อจำกัดสำคัญ

**ข้อจำกัด 1: Type I error inflation เมื่อ n เล็ก**

Wang et al. (2020) แสดงด้วย simulation ว่า log-rank test มี **type I error inflation สูงถึง 28%** แม้ sample size ระดับกลาง — ปัจจัยที่เพิ่ม inflation: n เล็ก, randomization ratio ไม่สมดุล, significance level ที่ใช้ [Wang et al. 2020] สำหรับ n≈25/กลุ่ม นี่เป็นความเสี่ยงจริง

**ข้อจำกัด 2: Power ขึ้นกับจำนวน events — ไม่ใช่จำนวน subjects**

Log-rank test asymptotic ต้องการ **events จริง** (ไม่ใช่ n ทั้งหมด) อย่างน้อย 20–30 รวมทุกกลุ่มจึงจะ type I error ไม่ inflate Kerschke et al. (2020) ยืนยันว่าแม้ one-sample log-rank ต้องปรับ correction เพิ่มเติมเมื่อ n เล็ก [Kerschke et al. 2020]

ถ้า contamination rate ≈ 10% → events per group ≈ 2–3 ขวด → **severely underpowered**
ถ้า contamination rate ≈ 30% → events per group ≈ 7–8 ขวด → ยังต้อง permutation test

**ข้อจำกัด 3: Competing events ทำให้ KM overestimate cumulative incidence**

ถ้าขวด "dead (non-contaminated)" ถูก censor ใน KM contamination curve → KM จะ overestimate ความน่าจะเป็น contamination จริง [Coemans et al. 2022 — cited in 08_survival_contamination.md]

---

## 2. คำถามที่ 2 — ควรใช้ Fine-Gray / Competing Risks ไหม?

### 2.1 เมื่อไหรต้องใช้ competing risks model

Austin et al. (2017) อธิบายชัดว่า **competing risk** คือ event ที่เกิดแล้วทำให้ primary event เกิดไม่ได้ [Austin et al. 2017] ในบริบทนี้:

- **Primary event:** ขวด contaminated
- **Competing event:** ขวด dead/senescent (ไม่ได้ contaminated — ตายเพราะสาเหตุอื่น)

ถ้า treat competing event เป็น censoring ใน KM → KM curve จะ **overestimate** cumulative contamination rate จริง เพราะ dead bottles ถูกนับว่า "เสี่ยง" ต่อไปทั้งที่ไม่ใช่

### 2.2 KM เดี่ยว vs CIF + Fine-Gray

| วิธี | วัดอะไร | เหมาะเมื่อไหร่ |
|---|---|---|
| **KM เดี่ยว** | Net probability ถ้าไม่มี competing event | ต้องการ mechanism (cause-specific hazard) |
| **CIF (Cumulative Incidence Function)** | Actual probability ในบริบทที่มี competing event | ต้องการ absolute risk ที่แท้จริง |
| **Fine-Gray model** | Effect of covariate บน subdistribution hazard (= effect บน CIF) | ต้องการ compare กลุ่มโดยคิด competing event |

Austin et al. (2021) เตือนว่า Fine-Gray model มีข้อจำกัดสำคัญ: **ผลรวม CIF ของ 2 events อาจเกิน 100%** เมื่อมี wide risk distribution — ในกรณี n เล็กนี้อาจเกิดปัญหา [Austin et al. 2021]

### 2.3 Recommendation สำหรับ VitroVision

สำหรับ **descriptive analysis** (contamination ไม่ใช่ primary endpoint):

1. **ถ้า dead-not-contaminated < 5%** → KM เดี่ยวพอ ผลต่างเล็กมาก
2. **ถ้า dead-not-contaminated ≥ 10%** → ควร plot CIF คู่กัน (contamination CIF + death CIF) โดยใช้ `cmprsk` package ใน R หรือ `stcompet` ใน Stata [Coviello & Boracchi 2004]
3. **Fine-Gray regression** (ปรับ covariate) → ยังไม่จำเป็นสำหรับ n ขนาดนี้ เพราะ covariate adjustment ต้องการ events/variable ≥ 10

Lin (1997) พัฒนา non-parametric inference สำหรับ CIF โดยตรง ซึ่งใช้ได้กับ n เล็กได้ดีกว่า Fine-Gray [Lin 1997]

---

## 3. คำถามที่ 3 — Log-rank Power กับ n≈25

### 3.1 ปัญหา type I error inflation

Wang et al. (2020) แสดงด้วย simulation ว่า log-rank asymptotic มี **type I error inflation สูงถึง 28%** และแนะนำ **permutation log-rank test** เป็น alternative ที่ควบคุม type I error ได้แม้ n เล็กและ group sequential design [Wang et al. 2020]

Kerschke et al. (2020) เสนอ one-sample log-rank test ที่ปรับปรุงแล้วซึ่งให้ type I error และ power ใกล้ nominal level แม้ n เล็ก [Kerschke et al. 2020]

### 3.2 Power calculation คร่าวๆ

Power ของ log-rank test ขึ้นกับ hazard ratio (HR) และจำนวน events รวม `d`:

| HR ที่ต้องการตรวจจับ | events รวมที่ต้องการ (α=0.05, power=0.80) |
|---|---|
| HR = 0.5 (ลด 50%) | ~46 events |
| HR = 0.3 (ลด 70%) | ~18 events |
| HR = 2.0 (เพิ่ม 2x) | ~46 events |

ด้วย n=25/กลุ่ม × 5 กลุ่ม = 125 ขวด:
- ถ้า contamination rate = 10% → events ≈ 12 → **ตรวจจับได้เฉพาะ HR ≥ 3.0 ขึ้นไป**
- ถ้า contamination rate = 30% → events ≈ 37 → **พอตรวจจับ HR = 0.5 ได้**

### 3.3 Alternatives เมื่อ n เล็ก

1. **Permutation log-rank test** (package `coin` ใน R) — recommended โดย Wang et al. [Wang et al. 2020]
2. **Exact log-rank test** — อ้างอิงใน 08_survival_contamination.md ว่าเหมาะกับ rare events
3. **Fisher's exact test บน ≥1 event** — ถ้า contamination rate ต่ำมาก (< 5%) อาจง่ายกว่าและ valid กว่า time-to-event analysis
4. **รายงาน descriptive เท่านั้น** — ถ้า events < 10 รวม: รายงาน % contamination per group + 95% CI แบบ binomial เท่านั้น โดยไม่ทำ formal test

---

## 4. คำถามที่ 4 — Contamination Rate Benchmark ใน TC

### 4.1 ข้อมูลจาก literature

**Permadi et al. (2023)** — Musa spp. tissue culture: รายงานว่า contamination และ browning เป็น "main constraints" ที่ขัดขวาง success โดยไม่ระบุตัวเลขชัดเจน แต่ชี้ว่า protocol ที่ดี (thermotherapy + chemical) ลด contamination ได้มาก [Permadi et al. 2023]

**Gammoudi et al. (2022)** — Pistacia vera (woody species): NaOCl 0.54–1.26% ให้ DE (disinfection efficiency) 27–77%, HgCl 100% DE — ชี้ว่า contamination rate เริ่มต้น (ก่อน optimize) อาจสูงถึง 50–70% ใน woody species [Gammoudi et al. 2022]

**Tolegen et al. (2025)** — Blackberry: ใช้ PPM™ 0.2% v/v ใน 12-week culture ให้ **100% aseptic shoots** สำหรับ Chacanska Bestrna variety ยืนยันว่าสามารถลด contamination เหลือ 0% ได้ด้วย protocol ที่เหมาะสม [Tolegen et al. 2025]

**Balo (2023)** — รวม review หลายพืช: เน้นว่า contamination มาจาก 3 แหล่งหลัก (phyllospheric, rhizospheric, endophytic) และ "well-established protocol" ในห้องปฏิบัติการควรให้ contamination rate < 5–10% [Balo 2023]

**Anikina et al. (2025)** — Review ใน micropropagation: ชี้ว่า endophytic contamination เป็นปัญหาหลักที่ standard surface sterilization ไม่สามารถจัดการได้ — contamination rate ขึ้นอยู่กับพืชและ variety มาก [Anikina et al. 2025]

### 4.2 Benchmark สำหรับ Over-sow Planning

| Contamination rate | ระดับ | แนะนำ over-sow |
|---|---|---|
| 0–5% | ดีมาก (protocol ดี) | +10% |
| 5–15% | ยอมรับได้ | +20% |
| 15–30% | ปัญหาปานกลาง | +30–50% |
| > 30% | ปัญหาร้ายแรง | ต้อง optimize protocol ก่อน |

**สำหรับ Capsicum:** Capsicum เป็น herbaceous species (ง่ายกว่า woody species) — คาดว่า contamination rate ด้วย protocol มาตรฐาน (NaOCl + laminar flow) อยู่ที่ 5–20% ใน initiation stage และลดลงใน subculture stage

**แนะนำ:** วาง target contamination < 15% → ถ้าพบว่า rate สูงกว่านี้ใน pilot batch → optimize protocol ก่อนเริ่ม main experiment + over-sow +25–30%

---

## 5. คำถามที่ 5 — วิธีรายงาน Survival Curve ใน TC Paper

### 5.1 Standard reporting ใน literature

**D'Arrigo et al. (2021)** แนะนำ elements ที่ต้องรายงานใน KM analysis:
1. **KM curve** พร้อม 95% CI (shaded)
2. **Number at risk table** ใต้ curve (บังคับ — ไม่มีแสดงว่า paper ไม่ complete)
3. **Median survival time** พร้อม 95% CI (รายงานเฉพาะถ้า curve ลงถึง 50%)
4. **Log-rank p-value** (หรือ permutation p-value) พร้อม test statistic
5. **Number of events / total** ต่อกลุ่ม

**Gomes et al. (2024)** เน้นว่า KM curve ต้องมี **risk table** และ **censored marks** (vertical tick marks) บน curve เพื่อ transparency [Gomes et al. 2024]

### 5.2 เมื่อมี Competing Events — ต้องรายงาน CIF

**Coviello & Boracchi (2004)** — เมื่อมี competing risks ควรรายงาน:
1. **Cumulative Incidence Function (CIF)** แยกต่อ event type (contamination CIF + death CIF)
2. **ตรวจสอบว่า CIF₁(t) + CIF₂(t) ≤ 1** เสมอ (ข้อดีของ CIF เหนือ 1 - KM)
3. Kolmogorov-Smirnov type test สำหรับ compare 2 CIF curves [Lin 1997]

**Austin et al. (2017)** เน้นว่าใน paper ที่ใช้ Fine-Gray model ต้องระบุ:
- Subdistribution HR พร้อม 95% CI
- แยกชัดระหว่าง "cause-specific HR" และ "subdistribution HR" — ความหมายต่างกัน
- รายงาน competing event rate ด้วย [Austin et al. 2017]

### 5.3 Template สำหรับ Methods section ใน YSC/ISEF paper

```
"Kaplan-Meier survival analysis was used to estimate the probability of remaining
contamination-free over 28 days for each MS formulation. Bottles showing no
contamination at experiment end were treated as right-censored. Differences between
MS formulations were tested using the log-rank test; given the small number of
expected events (~25 per group), a permutation-based log-rank test (R package 'coin')
was applied to control type I error. Where 'dead-not-contaminated' events exceeded 10%
of observations, cumulative incidence functions (CIF) were estimated using the
Gray test for competing risks (R package 'cmprsk') to obtain unbiased contamination
probabilities. All survival analyses were exploratory/descriptive in nature."
```

---

## ตารางหลักฐาน

| เรื่อง | สรุปสาระ | อ้างอิง + URL |
|---|---|---|
| KM methodology | KM ใช้ได้กับ time-to-event ที่มี censoring; ไม่ต้องสมมติ distribution; maximum use of incomplete data | [Hess et al. 2020](https://consensus.app/papers/details/8bd5de1c3fc357bfbab0f0835fe9691a/?utm_source=claude_code) |
| KM practical guide | ต้องมี risk table + censored marks + median survival time + 95% CI | [D'Arrigo et al. 2021](https://consensus.app/papers/details/d29282f2f07e5aa9a46c78bb17aca005/?utm_source=claude_code) |
| KM clinical interpretation | Interpret KM curves ในบริบท biology/medicine; ระวัง misinterpretation | [Gomes et al. 2024](https://consensus.app/papers/details/47fcb01a9e1d5a989159a01123e8a177/?utm_source=claude_code) |
| Log-rank type I inflation | Type I error inflation สูงถึง 28% ใน small n; permutation test แก้ได้ | [Wang et al. 2020](https://consensus.app/papers/details/3e365bc4b2a65e46b8ec08c7a9f5d762/?utm_source=claude_code) |
| One-sample log-rank small n | Improved one-sample log-rank ที่ type I/power ใกล้ nominal แม้ n เล็ก | [Kerschke et al. 2020](https://consensus.app/papers/details/044b8769b441584da2f3086c2b51995b/?utm_source=claude_code) |
| Fine-Gray reporting | Subdistribution HR ≠ cause-specific HR; ต้องรายงานแยก; review 2015 papers พบ interpretation ผิดบ่อย | [Austin et al. 2017](https://consensus.app/papers/details/ea6ecbe9ebf253c283a6fb7bc11ae441/?utm_source=claude_code) |
| Fine-Gray limitation | CIF sum อาจเกิน 100% — ต้องระวังใน wide risk distribution; cause-specific hazard safer | [Austin et al. 2021](https://consensus.app/papers/details/60d9cda2497d5ca1beea747bd310bfd6/?utm_source=claude_code) |
| Fine-Gray vs cause-specific | Reduction factor = proportion ที่ยังไม่มี competing event; ช่วย interpret Fine-Gray intuitively | [Putter et al. 2020](https://consensus.app/papers/details/3e60c6d4cb45501186a6a08ffae1b9c5/?utm_source=claude_code) |
| CIF non-parametric inference | KP estimator ของ CIF consistent + weak convergence; KS test สำหรับ compare 2 CIF curves | [Lin 1997](https://consensus.app/papers/details/429a2de87ab25260baa6cfbf73b826df/?utm_source=claude_code) |
| CIF estimation Stata | stcompet command สำหรับ CIF + standard error + ln(-ln) CI bounds | [Coviello & Boracchi 2004](https://consensus.app/papers/details/7098420e3d005c34be9813dbe37f634d/?utm_source=claude_code) |
| CIF restricted estimation | NPMLE ของ CIF เมื่อ ratio F1/F2 monotone; projectors ที่ consistent กว่า NPMLE | [Al-Kandari et al. 2022](https://consensus.app/papers/details/173627b891895f82b1cb6810ebcf8c4f/?utm_source=claude_code) |
| Contamination — Musa | Browning + contamination = main constraints TC กล้วย; thermotherapy+chemical ลดได้ | [Permadi et al. 2023](https://consensus.app/papers/details/fe7a2873eeb45cd781a4ed2494c0e9be/?utm_source=claude_code) |
| Contamination protocol — Pistacia | NaOCl 27–77% DE; HgCl 100% DE; ANN-MOGA optimize protocol; woody species ยากกว่า herbaceous | [Gammoudi et al. 2022](https://consensus.app/papers/details/28afbbd4af835ff0b6442b19c4d521a8/?utm_source=claude_code) |
| Contamination — Blackberry PPM™ | PPM™ 0.2% v/v ใน 12-week → 100% aseptic; ยืนยัน 0% contamination เป็นไปได้ | [Tolegen et al. 2025](https://consensus.app/papers/details/bdcae919faca5406b6c626ef59ba00d9/?utm_source=claude_code) |
| Contamination review | < 5–10% = protocol ดี; endophytic = hard to eliminate; identification + monitoring สำคัญ | [Balo 2023](https://consensus.app/papers/details/5d7b014d6ab7548a8f5202eb08899a6d/?utm_source=claude_code) |
| Contamination micropropagation | Endophytic contamination = internal infection ที่ surface sterilization ไม่จัดการได้; variety-specific | [Anikina et al. 2025](https://consensus.app/papers/details/a04020b771b85faa81ff95d78a94bda0/?utm_source=claude_code) |

---

## Recommendation สำหรับ VitroVision

### ยืนยัน KM + log-rank plan — ใช้ได้ แต่ต้อง upgrade 3 จุด

**จุดที่ 1: เปลี่ยน asymptotic log-rank → permutation log-rank**

```r
library(coin)
logrank_test(Surv(time_to_contamination, event) ~ MS_formula,
             data = df, distribution = "approximate")
# หรือ exact ถ้า events < 20 รวม
logrank_test(Surv(time_to_contamination, event) ~ MS_formula,
             data = df, distribution = "exact")
```
เหตุผล: ป้องกัน type I error inflation 28% ที่ Wang et al. (2020) พบ [Wang et al. 2020]

**จุดที่ 2: เพิ่ม CIF ถ้า dead-not-contaminated ≥ 10%**

```r
library(cmprsk)
# event_type: 1=contaminated, 2=dead-not-contaminated, 0=censored
cif_fit <- cuminc(ftime = df$time_to_event,
                  fstatus = df$event_type,
                  group = df$MS_formula)
plot(cif_fit)
```
เหตุผล: KM เดี่ยวจะ overestimate contamination probability จริง [Austin et al. 2017; Coviello 2004]

**จุดที่ 3: รายงาน descriptive-only ถ้า events < 10 รวม**

ถ้า contamination rate ต่ำมาก (< 5% ≈ < 6 ขวดจาก 125):
- ไม่ทำ formal survival test — รายงาน % contamination per group + 95% exact binomial CI เท่านั้น
- ระบุใน Methods: "contamination rate was too low for formal survival analysis; descriptive statistics only"

### Plan over-sow

- Target: contamination rate ≤ 15% (protocol มาตรฐาน, herbaceous species)
- Recommendation: **over-sow +25–30%** คือ plan 125 × 1.3 ≈ 163 ขวดเพื่อให้เหลือ ≥ 100 ขวดที่ usable ตลอด 28 วัน
- ถ้า pilot batch ให้ rate > 20% → optimize protocol (NaOCl concentration, timing) ก่อน main experiment

### สรุป Statistical plan (ปรับจาก 08_survival_contamination.md)

| Scenario | วิธีที่แนะนำ |
|---|---|
| events รวม ≥ 20, dead < 10% | KM + permutation log-rank |
| events รวม ≥ 20, dead ≥ 10% | KM + CIF (cmprsk) + Gray test |
| events รวม < 10 | Descriptive only (% + binomial 95% CI) |
| ต้องการ covariate adjustment | Cause-specific Cox PH (ระวัง convergence เมื่อ events/variable < 10) |

---

## Sign-up/usage message จาก Consensus

Query 1 (survival analysis contamination plant tissue culture Kaplan-Meier):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 2 (competing risks contamination mortality plant in vitro):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 3 (log-rank test small sample size power plant experiment survival):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 4 (contamination rate tissue culture in vitro plant protocol benchmark):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 5 (Fine-Gray competing risks subdistribution hazard small sample biological experiment):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

Query 6 (cumulative incidence function competing risks contamination microbiology reporting):
> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

---

## References ทั้งหมด (ครบจาก Consensus)

**Survival Analysis — Methods**

[S1] [Kaplan–Meier survival curves](https://consensus.app/papers/details/8bd5de1c3fc357bfbab0f0835fe9691a/?utm_source=claude_code) — Hess et al., 2020, Transfusion, 47 citations

[S2] [Methods to Analyse Time-to-Event Data: The Kaplan-Meier Survival Curve](https://consensus.app/papers/details/d29282f2f07e5aa9a46c78bb17aca005/?utm_source=claude_code) — D'Arrigo et al., 2021, Oxidative Medicine and Cellular Longevity, 75 citations

[S3] [Kaplan-Meier Survival Analysis: Practical Insights for Clinicians](https://consensus.app/papers/details/47fcb01a9e1d5a989159a01123e8a177/?utm_source=claude_code) — Gomes et al., 2024, Acta medica portuguesa, 27 citations

[S4] [An improved one-sample log-rank test](https://consensus.app/papers/details/044b8769b441584da2f3086c2b51995b/?utm_source=claude_code) — Kerschke et al., 2020, Statistical Methods in Medical Research, 8 citations

[S5] [Testing a hypothesis about two survivor functions using the log-rank test](https://consensus.app/papers/details/24ca2cd7ae4553e99a50f4c241328065/?utm_source=claude_code) — 2023, Unknown Journal

[S6] [Type I error inflation of log-rank test with small sample size: A permutation approach and simulation studies](https://consensus.app/papers/details/3e365bc4b2a65e46b8ec08c7a9f5d762/?utm_source=claude_code) — Wang et al., 2020, 5 citations

**Competing Risks**

[C1] [Practical recommendations for reporting Fine‐Gray model analyses for competing risk data](https://consensus.app/papers/details/ea6ecbe9ebf253c283a6fb7bc11ae441/?utm_source=claude_code) — Austin et al., 2017, Statistics in Medicine, 1005 citations

[C2] [On the relation between the cause‐specific hazard and the subdistribution rate for competing risks data: The Fine–Gray model revisited](https://consensus.app/papers/details/3e60c6d4cb45501186a6a08ffae1b9c5/?utm_source=claude_code) — Putter et al., 2020, Biometrical Journal, 47 citations

[C3] [Fine‐Gray subdistribution hazard models to simultaneously estimate the absolute risk of different event types: Cumulative total failure probability may exceed 1](https://consensus.app/papers/details/60d9cda2497d5ca1beea747bd310bfd6/?utm_source=claude_code) — Austin et al., 2021, Statistics in Medicine, 78 citations

[C4] [Non-parametric inference for cumulative incidence functions in competing risks studies](https://consensus.app/papers/details/429a2de87ab25260baa6cfbf73b826df/?utm_source=claude_code) — Lin, 1997, Statistics in Medicine, 478 citations

[C5] [Cumulative Incidence Estimation in the Presence of Competing Risks](https://consensus.app/papers/details/7098420e3d005c34be9813dbe37f634d/?utm_source=claude_code) — Coviello & Boracchi, 2004, The Stata Journal, 526 citations

[C6] [Restricted estimation of the cumulative incidence functions of two competing risks](https://consensus.app/papers/details/173627b891895f82b1cb6810ebcf8c4f/?utm_source=claude_code) — Al-Kandari et al., 2022, Journal of Statistical Planning and Inference, 2 citations

**Contamination in Plant Tissue Culture**

[P1] [Managing Lethal Browning and Microbial Contamination in Musa spp. Tissue Culture: Synthesis and Perspectives](https://consensus.app/papers/details/fe7a2873eeb45cd781a4ed2494c0e9be/?utm_source=claude_code) — Permadi et al., 2023, Horticulturae, 34 citations

[P2] [Establishment of optimized in vitro disinfection protocol of Pistacia vera L. explants mediated a computational approach: multilayer perceptron–multi−objective genetic algorithm](https://consensus.app/papers/details/28afbbd4af835ff0b6442b19c4d521a8/?utm_source=claude_code) — Gammoudi et al., 2022, BMC Plant Biology, 44 citations

[P3] [Utilizing Plant Preservative Mixture™ to eliminate endophytic bacterial contamination and establish in vitro cultures of blackberry varieties](https://consensus.app/papers/details/bdcae919faca5406b6c626ef59ba00d9/?utm_source=claude_code) — Tolegen et al., 2025, International Journal of Biology and Chemistry, 2 citations

[P4] [Elimination of Contamination in Plant Tissue Culture Laboratory](https://consensus.app/papers/details/5d7b014d6ab7548a8f5202eb08899a6d/?utm_source=claude_code) — Balo, 2023, Acta Botanica Plantae, 3 citations

[P5] [Control of Contamination of Tissue Plant Cultures During in Vitro Clonal Micropropagation](https://consensus.app/papers/details/a04020b771b85faa81ff95d78a94bda0/?utm_source=claude_code) — Anikina et al., 2025, OnLine Journal of Biological Sciences, 2 citations

---

*ไฟล์นี้สร้างโดย sub-agent R5-E สำหรับ VitroVision (YSC 2027 → ISEF CSBI)*
*ทุก citation ผ่าน Consensus และมี URL จริง — ตรวจสอบได้ที่ _citation_audit.md ก่อน commit*
