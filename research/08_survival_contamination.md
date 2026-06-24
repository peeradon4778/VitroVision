# 08 — Survival Analysis: Contamination & Criterion Validity (Acclimatization)

**โปรเจกต์:** VitroVision — Computational Phenotyping สำหรับ *Capsicum frutescens* in vitro TC  
**วันที่เขียน:** 2026-06-11  
**Research sub-agent:** Claude Sonnet 4.6 (ภายใต้ Orchestrator Fable 5)  
**Sources:** Consensus (Semantic Scholar/Scopus/PubMed), PubMed MCP

---

## 1. สรุปสั้น

การวิเคราะห์ด้านเวลาใน tissue culture มีสองแกนหลักที่เชื่อมกัน: (A) **time-to-contamination** — contamination เป็น absorbing state ใน TC ดังนั้น Kaplan-Meier (KM) + log-rank test จึงเหมาะสมทางทฤษฎี แต่มีข้อจำกัดสำคัญเมื่อ event มีน้อย; (B) **survival-to-acclimatization** — ใช้เป็น criterion validity เชิง objective ตรวจสอบว่า green% หรือ vigor score ที่วัดได้ใน vitro จริงๆ ทำนายผลลัพธ์ปลายทาง (ex vitro survival) ได้ไหม — นี่คือแกน non-circular ที่แข็งแกร่งที่สุดของ validation

---

## 2. Kaplan-Meier + Log-rank ใน Contamination ของ In Vitro Culture

### 2.1 พื้นฐาน Time-to-Event Analysis

Kaplan-Meier estimator และ log-rank test เป็น non-parametric methods สำหรับข้อมูลประเภท time-to-event [1][2][3] จุดเด่นหลักคือรองรับ **censoring** — กรณีที่ไม่ทราบเวลาจริงของ event (เช่น ขวดยังไม่ปนเปื้อนเมื่อสิ้นสุดการทดลอง) โดยไม่ต้องตัดข้อมูลทิ้งหรือสมมติ distribution ล่วงหน้า [3]

ใน context ของ TC contamination:
- **Event** = วันแรกที่ตรวจพบการปนเปื้อน (มองเห็นด้วยตา หรือระบบ vision วินิจฉัย)
- **Censored observation** = ขวดที่สิ้นสุด follow-up โดยยังไม่ปนเปื้อน (right-censored) หรือถูกเก็บออกก่อนกำหนดด้วยเหตุอื่น
- **Survival function S(t)** = ความน่าจะเป็นที่ขวดยังคง contamination-free จนถึงเวลา t
- **Log-rank test** = เปรียบเทียบ survival curves ระหว่าง 5 สูตร MS ว่าต่างกันนัยสำคัญหรือไม่

Time-to-event analysis ถูกนำมาใช้กับข้อมูล biological ในหลายบริบทที่คล้ายกัน เช่น seed germination (time-to-germination) ซึ่ง McNair et al. (2012) แสดงว่า survival analysis มีข้อดีเหนือกว่า germination index แบบดั้งเดิมอย่างชัดเจน [4] และ Romano et al. (2020) ยืนยันว่าวิธีนี้แก้ปัญหา ungerminated seeds (= right-censoring) ได้ตรงประเด็นกว่า non-linear regression ทั่วไป [5] Onofri et al. (2022) เสนอ unified framework สำหรับ time-to-event data ใน plant sciences พร้อม R package `drcte` ที่ implement KM, log-rank, Cox PH model ครบ [6]

การนำ KM มาใช้กับ **contamination** ใน in vitro culture นั้นสมเหตุสมผลโดยตรง เพราะ contamination ที่แสดงออกมาแล้วไม่กลับได้ (absorbing state) — ตรงกับ assumption พื้นฐานของ survival analysis ที่ event เกิดได้ครั้งเดียวต่อหน่วย

### 2.2 Censoring: ประเภทและวิธีจัดการ

| ประเภท Censoring | สถานการณ์ใน TC | วิธีจัดการ |
|---|---|---|
| **Right censoring** | ขวดยังไม่ปนเปื้อนเมื่อสิ้นสุด experiment | รองรับโดย KM โดยตรง |
| **Interval censoring** | ตรวจ 2 ครั้ง/สัปดาห์ ไม่ทราบวันแน่นอน | ใช้ midpoint หรือ interval-censored KM |
| **Competing events** | ขวดเสียหาย/ถูกเก็บก่อนปนเปื้อน | ระวัง: censoring ใน competing event อาจทำให้ cumulative incidence bias สูง [7] |

สำหรับ TC ที่ตรวจ 2 ครั้ง/สัปดาห์ ควรบันทึกว่า "ปนเปื้อนระหว่างวัน X และ Y" และใช้ midpoint เป็นค่า time-to-event เพื่อลด interval censoring bias

### 2.3 Few-Event Caveat: ข้อควรระวังสำคัญ

**นี่คือจุดอ่อนหลักของ design นี้** Power ของ log-rank test ขึ้นอยู่กับ **จำนวน events จริง** (ไม่ใช่จำนวนขวด) เป็นหลัก [8]:

- ถ้าอัตราปนเปื้อน = 10% จาก 100 ขวด → events ≈ 10 ตัว → underpowered มาก
- ถ้าอัตราปนเปื้อน = 30% → events ≈ 30 ตัว → power ดีขึ้นแต่ยังจำกัด
- Log-rank test asymptotic อาจไม่แม่นยำเมื่อ events < 20–30 รวม [8]

**แนวทางแก้ไข:**
1. รายงาน KM curve เป็น **descriptive/exploratory** เท่านั้น — ไม่ claim causal conclusion
2. ถ้า events น้อย ใช้ **exact permutation test** แทน asymptotic log-rank [8]
3. บันทึก number at risk ทุก time point ใน table ใต้ KM plot
4. ถ้าต้องการ covariate adjustment → Cox PH model แต่ต้องระวัง convergence เมื่อ events น้อย
5. ระบุ power limitation ชัดเจนใน Methods section: *"Due to the exploratory nature of this analysis and potentially limited contamination events, KM analysis is reported descriptively with log-rank p-values interpreted as hypothesis-generating rather than confirmatory."*

---

## 3. Paper อ้างอิง: Survival-to-Acclimatization (peer-reviewed, PubMed-indexed)

**[T-alt-1] Ahmed et al. (2026) — Dragon fruit micropropagation and acclimatization**  
วัด survival rate 97% ระหว่าง acclimatization ใน peat moss:perlite 1:1 เชื่อมกับ morphophysiological parameters (shoot length, root number, fresh weight) — ตัวอย่างชัดของ in vitro phenotype → ex vitro survival  
DOI: [10.1186/s12870-026-08246-x](https://doi.org/10.1186/s12870-026-08246-x) [10]

**[T-alt-2] Kongbangkerd et al. (2026) — Ginger TIS micropropagation**  
ระบุชัดว่า plantlet quality (shoot height, fresh weight, leaf length) จาก TIS system ส่งผลต่อ ex vitro survival rate (สูงสุด 88.9%) — แสดง link โดยตรงระหว่าง in vitro phenotype และ acclimatization outcome  
DOI: [10.1038/s41598-026-37182-x](https://doi.org/10.1038/s41598-026-37182-x) [11]

**[T-alt-3] Méndez-Hernández et al. (2023) — Coffee somatic embryogenesis bioreactor**  
วัด fresh weight, length, leaf number, root length ใน vitro และ link กับ acclimatization rate > 90% — ตัวอย่าง multi-parameter in vitro quality → ex vitro survival  
DOI: [10.3390/plants12173055](https://doi.org/10.3390/plants12173055) [12]

---

## 4. Survival-to-Acclimatization เป็น Criterion Validity

### 4.1 Logic ของ Criterion Validity แบบ Non-circular

ใน measurement validation มี 3 กลยุทธ์หลัก:
1. **Face/content validity** — ผู้เชี่ยวชาญตัดสินว่า measurement สมเหตุสมผล (circular)
2. **Convergent validity** — เทียบกับ gold standard อื่น (เช่น SPAD vs spectrophotometer) → ยังอาจ circular ถ้า gold standard มี error เหมือนกัน
3. **Criterion validity** — วัด measurement แล้วทำนาย **outcome ปลายทางที่เป็นอิสระ** — นี่คือแกนที่แข็งแกร่งที่สุด

สำหรับ VitroVision: ถ้า green% / vigor score ที่ระบบวัดใน vitro → สามารถทำนาย **อัตรารอดชีวิตระหว่าง acclimatization** (ex vitro, 4–6 สัปดาห์หลัง transplant) ได้อย่างมีนัยสำคัญ → นั่นคือ evidence of criterion validity ที่ไม่วนกลับมาใช้ตัวมันเองเป็น reference

### 4.2 Precedent ใน Plant Science

บทความจาก plant TC พบ link ระหว่าง in vitro phenotype กับ acclimatization survival ซ้ำแล้วซ้ำเล่า:
- Kongbangkerd et al. (2026): immersion frequency → plantlet quality → survival rate 88.9% [11]
- Ahmed et al. (2026): media composition → morphophysiological description → survival 97% [10]
- Méndez-Hernández et al. (2023): bioreactor parameters → vigor parameters → acclimatization > 90% [12]
- Wojtania et al. (2022): photoperiod/temperature → dormancy induction → ลด survival ระหว่าง acclimatization [13]

pattern ที่ซ้ำในวรรณกรรมคือ: **ต้นที่มี morphophysiological quality สูงใน vitro → รอดตาย acclimatization สูงกว่า** — VitroVision ใช้ pattern นี้เป็น testable hypothesis สำหรับ criterion validity

### 4.3 Framework สำหรับ Criterion Validity ใน VitroVision

```
[in vitro measurement]          [ex vitro outcome]
green% (ระบบวัด)    ──────→    อัตรารอด 4-wk acclimatization
vigor score (1–5)   ──────→    (binary: รอด/ไม่รอด per ขวด)
leaf count          
root presence
```

**Statistical test:** Logistic regression หรือ Spearman correlation ระหว่าง in vitro score (สัปดาห์ที่ 4–6 ก่อน transplant) กับ binary/proportion survival หลัง acclimatization

ถ้า AUC > 0.70 หรือ r > 0.5, p < 0.05 → criterion validity ผ่านเกณฑ์ที่ยอมรับได้ในงาน phenotyping [14]

---

## 5. ข้อแนะนำ Methods

### 5.1 Contamination Survival Analysis

```
Data collection:
- บันทึกวันที่เริ่มเพาะขวด (Day 0) ต่อขวด
- ตรวจ contamination 2x/week → บันทึก "first visible contamination" per bottle
- ถ้าไม่ปนเปื้อนจนสิ้น experiment → mark as right-censored (event=0)

Variables:
- time_to_contamination: วันนับจาก Day 0
- event: 1=contaminated, 0=censored
- MS_formula: factor 5 levels (สูตร MS ที่ 1–5)

Analysis (R):
library(survival)
library(survminer)

km_fit <- survfit(Surv(time_to_contamination, event) ~ MS_formula, data = df)
ggsurvplot(km_fit, risk.table = TRUE, pval = TRUE)
survdiff(Surv(time_to_contamination, event) ~ MS_formula, data = df)  # log-rank

# ถ้า events น้อย → exact test
library(coin)
logrank_test(Surv(time_to_contamination, event) ~ MS_formula, data = df,
             distribution = "exact")
```

**Reporting:** ระบุ number of events per group, median survival time (ถ้า curve ลงถึง 50%), 95% CI ของ KM curve, และ caveat ว่า analysis เป็น exploratory

### 5.2 Criterion Validity (Survival-to-Acclimatization)

```
Timeline:
- สัปดาห์ 4–6 ของ in vitro: บันทึก green%, vigor score, root presence
- transplant → track ex vitro survival สัปดาห์ 2, 4, 6

Analysis:
# Logistic regression: vigor score → survival (binary)
model <- glm(survived_4wk ~ vigor_score + green_pct + root_present,
             data = df, family = binomial)
# ROC/AUC
library(pROC)
roc_obj <- roc(df$survived_4wk, fitted(model))
auc(roc_obj)

# หรือ Spearman correlation สำหรับ continuous survival proportion
cor.test(df$green_pct, df$survival_proportion_4wk, method = "spearman")
```

**Interpretation standard:**
- AUC 0.70–0.80 = acceptable criterion validity
- AUC > 0.80 = good criterion validity
- ถ้า AUC < 0.70 → discuss limitation ใน Discussion section

### 5.3 Data collection sheet (แนะนำ)

| Bottle_ID | MS_formula | Start_date | Contamination_date | Censored | Vigor_wk4 | Green_pct_wk4 | Survived_acclim |
|---|---|---|---|---|---|---|---|
| B001 | MS1 | 2026-07-01 | 2026-07-15 | 0 | — | — | — |
| B002 | MS1 | 2026-07-01 | NA | 1 | 3 | 72% | 1 |

---

## 6. References

[1] D'Arrigo G et al. (2021). "Methods to Analyse Time-to-Event Data: The Kaplan-Meier Survival Curve." *Oxidative Medicine and Cellular Longevity*. 72 citations.  
URL: https://consensus.app/papers/details/d29282f2f07e5aa9a46c78bb17aca005/

[2] In J et al. (2018). "Survival analysis: Part I — analysis of time-to-event." *Korean Journal of Anesthesiology*. 45 citations.  
URL: https://consensus.app/papers/details/ec7f927cc63657049410188105e193d0/

[3] Schober P et al. (2018). "Survival Analysis and Interpretation of Time-to-Event Data: The Tortoise and the Hare." *Anesthesia and Analgesia*. 224 citations.  
URL: https://consensus.app/papers/details/9f1273e914755e21a94b1a0f3a30e5aa/

[4] McNair JN et al. (2012). "How to analyse seed germination data using statistical time-to-event analysis: non-parametric and semi-parametric methods." *Seed Science Research*. 191 citations.  
URL: https://consensus.app/papers/details/c3dfaac0e6c65a74956a5ff47c801f2d/

[5] Romano A et al. (2020). "Germination Data Analysis by Time-to-Event Approaches." *Plants*. 35 citations.  
URL: https://consensus.app/papers/details/19e6bf43990153529c1aa0f9cbb64b76/

[6] Onofri A et al. (2022). "A Unified Framework for the Analysis of Germination, Emergence, and Other Time-To-Event Data in Weed Science." *Weed Science*. 50 citations.  
URL: https://consensus.app/papers/details/e24096f4c3ad565ab82e919d7c5dea5b/

[7] Coemans M et al. (2022). "Bias by censoring for competing events in survival analysis." *BMJ*. 83 citations.  
URL: https://consensus.app/papers/details/0ec8a6260c4a5854ae1b08efa40363a8/

[8] Reutzel K (2021). "Survival Analysis: An Exact Method for Rare Events." 1 citation.  
URL: https://consensus.app/papers/details/ff2eb68e07f45c8fa89a1963b62d3aa4/

[9] Thomas JP et al. (2010). "Influence of beneficial microorganisms during in vivo acclimatization of in vitro-derived tea (*Camellia sinensis*) plants." *Plant Cell, Tissue and Organ Culture (PCTOC)*. 41 citations.  
URL: https://consensus.app/papers/details/a31cdca95fe75ecab2d460170620e71b/

[10] Ahmed EZ et al. (2026). "Integrated media and plant growth regulators comparative evaluation for enhanced in vitro propagation and acclimatization of *Selenicereus costaricensis*." *BMC Plant Biology*.  
DOI: [10.1186/s12870-026-08246-x](https://doi.org/10.1186/s12870-026-08246-x) — (According to PubMed, PMID: 41699499)

[11] Kongbangkerd A et al. (2026). "Optimizing immersion time and frequency in a twin-bottle temporary immersion system for mass production of *Zingiber officinale* Roscoe." *Scientific Reports*.  
DOI: [10.1038/s41598-026-37182-x](https://doi.org/10.1038/s41598-026-37182-x) — (According to PubMed, PMID: 41593351)

[12] Méndez-Hernández HA et al. (2023). "In Vitro Conversion of *Coffea* spp. Somatic Embryos in SETIS Bioreactor System." *Plants (Basel)*.  
DOI: [10.3390/plants12173055](https://doi.org/10.3390/plants12173055) — (According to PubMed, PMID: 37687302)

[13] Wojtania A et al. (2022). "Growth Cessation and Dormancy Induction in Micropropagated Plantlets of Rhubarb 'Raspberry' Influenced by Photoperiod and Temperature." *International Journal of Molecular Sciences*.  
DOI: [10.3390/ijms24010607](https://doi.org/10.3390/ijms24010607) — (According to PubMed, PMID: 36614049)

[14] Chapu I et al. (2022). "Exploration of Alternative Approaches to Phenotyping of Late Leaf Spot and Groundnut Rosette Virus Disease for Groundnut Breeding." *Frontiers in Plant Science*. 18 citations.  
URL: https://consensus.app/papers/details/0ccdfc0adbeb5d0bbc3ff412c6c42d14/

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*

---

*ไฟล์นี้สร้างโดย research sub-agent VitroVision สำหรับ YSC 2027*
