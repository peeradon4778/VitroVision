# R1 — Phenomics Feature Set Audit (14 features ทันสมัยไหม?)

> **สร้าง:** 2026-06-20 · 5 Consensus sub-agents (R1-A…E) · ทุก cite มี URL จาก Consensus จริง
> **คำถามต้นทาง:** comment #5 — 14 hand-crafted features ทันสมัย/เป็นที่ยอมรับแค่ไหน + ควรเปลี่ยนเป็น API-based phenomics ไหม
> **กฎ citation:** URL ด้านล่างเป็น Consensus page จริง — ก่อนเข้ารูปเล่มต้อง resolve DOI + verify PubMed (เฉพาะตัว load-bearing)

---

## 🎯 VERDICT รวม

**14 features = "still-acceptable แต่ dated บางส่วน" ไม่ถึงขั้นทิ้ง** — สนาม SOTA ย้ายไป learned features/embeddings แล้ว [A1,A2,A4][E4,E5] **แต่** ข้อได้เปรียบของ deep features ผูกกับ "labeled data จำนวนมาก" ซึ่งเรายังไม่มี → hand-crafted features ที่ interpretable คือทางเลือกที่ honest + defensible สำหรับ batch 1 (ตรงกับ 2-phase framing เดิม)

**ทิศทาง: HYBRID ไม่ใช่ replace** — เก็บ classical CV (quantitative, deterministic, เข้าสถิติได้) + เพิ่ม indices ใหม่ + ให้ VLM/learned ทำ qualitative เท่านั้น

---

## 📊 ตารางตัดสิน per-feature

### เก็บไว้ (defensible)
| Feature | เหตุผล | อ้างอิง |
|---|---|---|
| green_coverage_pct* | primary endpoint, = canopy/projected area เป็น trait มาตรฐานเกือบทุกงาน | A5, B (Smith 1989, Bethge 2023) |
| ExG (2G−R−B) | ยัง best-practice สำหรับ segmentation/coverage ไม่ถูก supersede | C1 (Meyer&Neto 2008, Jiang 2025) |
| VARI | valid, correlate vigor/yield สูง (maize r=0.99) | C2 (Coswosk 2024) |
| GLCM (entropy/contrast/homogeneity) | มี precedent **ในใบพริกโดยตรง** (Patil 2022) + ใช้ใน SOTA fusion; interpretable | D1,D2 (Patil 2022 chili, Ahmad 2021) |
| convex_hull_ratio, shoot_count | shape traits มาตรฐาน — แต่ควร upgrade เป็น instance-seg | A3, B (Davidson 2024) |

### เพิ่ม (มีหลักฐานแข็ง — เรียงความคุ้มค่า)
| เพิ่ม | ทำไม | priority |
|---|---|---|
| **NGRDI = (G−R)/(G+R)** | chlorophyll/N proxy ที่ขาด, correlate r>0.93 ทั้ง lettuce+basil, ต้นทุนต่ำ (channel เดิม) | 🥇 เพิ่มก่อนเลย (C5,C6) |
| **CIVE** | correlate chlorophyll r≈0.94–0.97 | 🥈 (C6) |
| **ExG−ExR** | auto zero-threshold (ไม่ต้องจูน Otsu), ทนพื้นหลังขวดรบกวน +55% | 🥈 (C1 Meyer&Neto) |
| **TGI** | chlorophyll-targeted ดีสุดจากกล้องถูก — **แต่ขึ้นกับ camera sensitivity** ต้อง calibrate/ใช้ gvTGI | 🥉 (C4,C7,C8) |
| **CIELAB greenness** | in-vitro-validated (Depetris 2025), perceptually-uniform แม่นกว่า ExG บางเงื่อนไข | 🥉 (B9) |
| **LBP texture** | complement GLCM, robust ต่อ noise กว่า, ชนะ GLCM หลายงาน → "ไม่พึ่ง descriptor เดียว" | 🥉 (D5 Turkoglu) |

### ลด priority (ไม่ลบ)
| Feature | ปัญหา |
|---|---|
| leaf_color_index = G/R | ratio แบบ SR-family **ไวต่อ glass glare/specular มากสุด**, ข้อมูลทับ NGRDI (normalized stabler) → คงไว้แต่ลด priority, ระบุ limitation (C10) |
| vigor_score (rule-based) | คงเป็นแกน deterministic — **ห้ามให้ VLM ออกตัวเลขแทน** (ดูล่าง) |

---

## 🧪 In-vitro-specific gaps (ที่ 14 features ขาด — B)
| Trait ขาด | วัด RGB ได้ไหม | อ้างอิง | หมายเหตุ |
|---|---|---|---|
| **Browning intensity + temporal onset** | ✅ ดี | Liu 2024, Kaewubon 2014 | มีแค่ brown_coverage% (coverage เดียว ไม่มี intensity/onset) |
| **Shoot multiplication RATE (per-subculture, temporal)** | ✅ ถ้า instance-seg+time | Smith 1989, Niazian 2018, Davidson 2024 | shoot_count = snapshot เดียว ไม่ใช่ rate |
| **Biomass-density proxy (weighted density→fresh weight)** | ✅ | Smith 1989, Bethge 2023 | แทนการชั่ง (destructive) |
| **Canopy height / media volume** | ⚠️ ต้อง depth/stereo | Bethge 2023 | เราเป็น 2D ล้วน |
| **Hyperhydricity index** | ⚠️ proxy เท่านั้น | Bethge 2023 HH | สัญญาณจริงอยู่ **SWIR/NIR** (RGB จับไม่ได้); RGB ทำได้แค่ glare/saturation/VIS-415nm proxy — **frame ระวัง อย่า over-claim** |
| **Contamination onset** | ❓ ไม่มี standard | — | **ไม่มี paper verified ให้อ้าง** = ทั้ง risk + novelty |

---

## 🤖 VLM / API สำหรับ phenomics — สรุปสำคัญ (E)
- **มีงาน VLM phenotyping จริง** (AgEval: Gemini/Claude/GPT/LLaVA บน 12 stress tasks; few-shot F1 46%→73%) [E7]
- ⚠️ **PlantXpert 2026: quantitative reasoning ของ VLM ยังอ่อน** (fine-tune ดีสุด ~78%) → **ห้ามให้ Gemini ออกตัวเลข vigor โดยตรง** จะไม่ reproducible defend ไม่ได้ [E9]
- ✅ VLM ควรจำกัดบทบาท = **qualitative description / triage / sanity-check** — ตัวเลขต้องมาจากสูตร deterministic
- เส้นทาง learned low-risk: frozen DINOv2 + linear probe/LoRA (ไม่ต้อง label เยอะ) = batch-2 upgrade ไม่ใช่ batch-1 [E8]

> **นัยต่อ Q1 (grill):** ผลนี้ปรับ "API แทนทั้งหมด" → **API ทำ qualitative (status/dev_stage/vigor-description), classical CV ทำ quantitative (เข้าสถิติ)** = ตรงกับ Q9 ที่ lock ไว้แล้ว ✅

---

## ✅ Validation framework (E — ยืนยัน L7 เดิมใช้ได้)
- ordinal vigor → **weighted Cohen's κ** (McHugh 2012: κ≥0.41 หลวมไป ตั้ง threshold สูงกว่า)
- continuous vigor_score → **ICC** + **Bland-Altman** (2 raters)
- **คำนวณ human inter-rater κ เป็น ceiling** — ถ้ามนุษย์เองได้ κ ต่ำ (Douphrate 2019: κ=0.43 ขณะ machine r>0.99) = argument ทองว่าระบบแก้ subjectivity ได้ → ตรง narrative "ดูตาเปล่าก็ได้?"
- ⚠️ κ=0.6274 ปัจจุบัน = smoke-test ภาพมั่ว ต้องทำ validation จริงก่อนใส่รายงาน

---

## ⚠️ Glass/specular caveat (C — สำคัญต่อเราเฉพาะ)
ratio indices (G/R, VARI) ไวต่อ glare บนผิวขวด → protocol บังคับ: (1) glare/specular detection + mask saturated pixels (2) lock WB ก่อนถ่ายทุกครั้ง (3) รายงาน correction pipeline ใน method — ทั้งหมดอยู่ใน `camera_optimization_plan.md` แล้ว ทำให้ครบ
- งานวิจัยขั้นสูง: polarization index (NSRVI/DSRVI ลบ glare R²≈0.89–0.92) = future work/limitation

---

## ⚠️ Verification flags
- **"Ranario 2025" + "Paci 2024"** (อ้างใน memory architecture papers) — **Consensus ไม่คืน paper ตรงชื่อ** → เสี่ยง hallucinated แบบ "Thomas 2026" → **ต้อง resolve PubMed ก่อนใช้** ห้ามเข้ารูปเล่มจนกว่าจะ verify
- PlantXpert 2026 = preprint ใหม่มาก 0 citations → supporting เท่านั้น
- UAV/satellite papers (A5,A7,A8) + soybean-seed (A6) context ต่างจาก in-vitro jar → ใช้สนับสนุน "feature สมัยใหม่มีอะไร" ได้ แต่อย่า over-claim directly transferable

---

## 📌 ACTION items จาก R1 (ยังไม่ทำ — รอเคาะ)
1. เพิ่ม NGRDI + CIVE + ExG−ExR ใน `phenotyper.py` (low cost, high value)
2. เพิ่ม browning intensity + temporal onset (ไม่ใช่แค่ coverage%)
3. เพิ่ม LBP เป็น texture complement
4. คง vigor_score deterministic — VLM = qualitative เท่านั้น (ยืนยัน Q9)
5. shoot multiplication rate (temporal) — รอ instance-seg (เชื่อม R2)
6. resolve "Ranario/Paci" ใน PubMed ก่อนใช้ในรูปเล่ม
