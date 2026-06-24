# 📘 VitroVision — โครงรูปเล่มโครงงาน (Report Outline)

> **ใบนี้คืออะไร:** แผนที่เดียวของรูปเล่มทั้งเล่ม — ทุกหัวข้อบอก **[มาจาก: ไฟล์ไหน]** + **[สถานะ]** เปิดดูไฟล์นี้แล้วรู้ว่าจะหยิบอะไรมาเขียนเมื่อไหร่
> สร้าง 2026-06-17 · อิง `_narrative_spine.md` + research 01–14 + `10_methods_draft.md`
> **กรอบ:** YSC 2027 → ISEF · สาขา **CSBI (ชีววิทยาเชิงคำนวณ)** — CV/ML ต้องผูกคำถามชีววิทยาเสมอ

**สถานะ:** ✍️ = เขียนได้เลย (ไม่ต้องรอ data) · ⏳ = รอ data จาก lab · 🔶 = ต้องเก็บกวาด/เช็คก่อน final

**ชื่อโครงงาน Final (ล็อก 2026-06-18)**
- **ไทย:** VitroVision: นวัตกรรมการวิเคราะห์ฟีโนไทป์เชิงคำนวณจากภาพของ *Capsicum frutescens* Mill. ในการเพาะเลี้ยงเนื้อเยื่อด้วย Vision-Language Models
- **EN:** VitroVision: Image-Based Computational Phenotyping of *Capsicum frutescens* Mill. in Vitro via Vision-Language Models

**One-liner (ท่องให้ขึ้นใจ):** *"CV ที่วัดสุขภาพ+การเจริญของพริก TC จากภาพผ่านขวด โดยไม่เปิดฝา — แทนสายตา subjective — แล้วพิสูจน์ว่าตรงกับผู้เชี่ยวชาญ + ทำนายการรอดจริงได้ โดยใช้ 5 สูตรอาหารเป็นบทพิสูจน์"*

---

## บทคัดย่อ (Abstract)
- [มาจาก: `_narrative_spine.md` L11] · [⏳ เติมตัวเลขผลท้ายสุด] — **เขียนหลังสุด (ต.ค.)**

---

## บทที่ 1 — บทนำ
| หัวข้อ | มาจาก | สถานะ |
|---|---|---|
| 1.1 ที่มาและความสำคัญ | `03_capsicum_economic_context` (เศรษฐกิจพริก) + `01_capsicum_tissue_culture` (ทำไม TC สำคัญ) | ✍️ |
| 1.2 ปัญหา: การประเมินด้วยสายตา = ช้า/subjective/ทำซ้ำเชิงเวลาไม่ได้ | `_narrative_spine` องก์ 1 · hook: Depetris 2025 | ✍️ |
| 1.3 วัตถุประสงค์ | `05_narrative_problem_objective_impact` | ✍️ |
| 1.4 สมมติฐาน (H1a/H1b/H2/H3/H4) | `10_methods_draft` §6 (signed off 2026-06-12) | ✍️ |
| 1.5 ขอบเขตการศึกษา | `10_methods` §1 (locked: cv.พริกจินดา, 5 สูตร, ≥2 batch, 28 วัน) | ✍️ |
| 1.6 นิยามศัพท์ (vigor, hyperhydricity, phenotype, growth curve) | spine §"แปลแนวคิดยาก" | ✍️ |
| 1.7 ประโยชน์ที่คาดว่าจะได้รับ | `05` (impact) | ✍️ |

> ⚠️ **C-05:** แยกให้ชัดทุกที่ — κ ของ "classifier 3-class (healthy/contam/dead)" ≠ κ ของ "vigor rubric 1–5" คนละการวัด

---

## บทที่ 2 — เอกสารและงานวิจัยที่เกี่ยวข้อง
| หัวข้อ | มาจาก | สถานะ |
|---|---|---|
| 2.1 การเพาะเลี้ยงเนื้อเยื่อพริก | `01_capsicum_tissue_culture` | ✍️ |
| 2.2 สูตรอาหาร MS + PGR (BAP/NAA/IBA) | `02_media_formulations_review` + `13_pgr_morphology` | ✍️ |
| 2.3 แหล่งคาร์บอน: glucose ในพริก | `11_carbon_source_glucose` (Phillips & **Hubstenberger** 1985) | ✍️ 🔶 เช็คชื่อ co-author ไม่ใช่ "Collins" |
| 2.4 การงอก/ontogeny ของพริก | `12_capsicum_germination_ontogeny` | ✍️ |
| 2.5 Image-based phenotyping / DL ในพืช | `14_image_dl_phenotyping` | ✍️ |
| 2.6 Hyperhydricity (vitrification) | `10` §3.6 | ✍️ |

---

## บทที่ 3 — วิธีดำเนินการ
> **แหล่ง truth หลัก = `10_methods_draft.md`** (มี draft ยาวแล้ว — งานคือเรียบเรียงเข้ารูปเล่ม)

| หัวข้อ | มาจาก | สถานะ |
|---|---|---|
| 3.1 พืช/วัสดุ + การฟอกเชื้อ (Clorox 15→10% ×2) | `10` §1 (locked) | ✍️ |
| 3.2 สูตรอาหาร 5 สูตร + เตรียมอาหาร (Kelcogel, glucose, pH) | `10` §1 + `02` | ✍️ |
| 3.3 สภาพห้องเพาะเลี้ยง (25±2°C, 16/8, LED 40–50) | `10` §1.7 (ตอบแล้ว) | ✍️ |
| 3.4 ระบบถ่ายภาพ (S24 FE, ~18cm, Pro mode, white card, 17:00) | `10` §2.1 + `_decisions_pending` A2 | ✍️ |
| 3.5 Tracking ขวด — ArUco DICT_4X4_100 | `09_methods_misc` | ✍️ |
| 3.6 Developmental stage labeling (capture-time) | `10` §2.4 (locked Q5 วันนี้) | ✍️ |
| 3.7 Preprocessing: white-card auto-tune → HSV (เขียว/น้ำตาล) | locked Q4 วันนี้ | ✍️ (code) 🔶 ต้องเขียนโปรแกรม |
| 3.8 สกัด phenotype features + classifier (EfficientNet) | `14` + `10` §3 | ✍️ |
| 3.9 Reference standard: expert 2-axis rubric + flag | `10` §4.1 + `appendix_rubric_onepager` | ✍️ |
| 3.10 การ validate (Spearman ρ + weighted κ + ICC) | `06_validation_methodology` | ✍️ |
| 3.11 Growth curve (Gompertz/ขวด) + เทียบสูตร | `07_growthcurve_repeated_measures` | ✍️ |
| 3.12 การวิเคราะห์การปนเปื้อน (KM + log-rank) | `08_survival_contamination` | ✍️ |
| 3.13 สถิติ + multiple comparison | `10` §5.3 (α=0.05, Bonferroni primary, FDR secondary) | ✍️ 🔶 post-hoc = **ART-C** ไม่ใช่ Dunn (C-02) |

---

## บทที่ 4 — ผลการทดลอง  ⏳ **ต้องรอ data จาก lab ทั้งบท**
| หัวข้อ | มาจาก (กรอบ) | ป้อนด้วย |
|---|---|---|
| 4.1 % งอก + survival ของ batch | `12` framework | data batch 1–2 |
| 4.2 Growth curve เทียบ 5 สูตร (primary: green_coverage_pct) | `07` | ภาพ 28 วัน |
| 4.3 Secondary endpoints (vigor, brown%, LCI, shoot_count) | `10` §3.5 | features จาก CV |
| 4.4 Validation: CV vs ครู (inter-rater κ/ICC + reference) | `06` | Task #3 (main scoring) |
| 4.5 Criterion validity: CV ทำนาย survival ตอนอนุบาล | `10` §4.6 | survival data |
| 4.6 Hyperhydricity rate ต่อสูตร | `10` §3.6 | expert flag |
| 4.7 การปนเปื้อน (KM curve) | `08` | running record |

---

## บทที่ 5 — สรุป อภิปราย และข้อเสนอแนะ  ⏳ (รอผลบท 4)
| หัวข้อ | มาจาก | สถานะ |
|---|---|---|
| 5.1 สรุปผล (เครื่องมือ validated + biological finding) | `05` + บท 4 | ⏳ |
| 5.2 อภิปราย (เทียบ literature, Gold Standard Paradox) | spine §แปลแนวคิด | ⏳ |
| 5.3 ข้อจำกัด (ไม่ใช้ lightbox, n, single cultivar ฯลฯ) | `10` limitations | ✍️ ร่างได้เลย |
| 5.4 Impact + การนำไปใช้ต่อ + future work (YOLO leaf count ฯลฯ) | `05` + `04_final_architecture_ux_plan` | ✍️ |

---

## บรรณานุกรม + ภาคผนวก
- **บรรณานุกรม:** ทุก citation ต้องผ่าน `_citation_audit.md` (gate) — verify ใน Consensus/PubMed + DOI กดได้
- **ภาคผนวก:** rubric เต็ม + calibration set (`appendix_rubric_onepager`), ArUco sheet, data dictionary (`_data_dictionary`), scoring sheets

---

## 🚨 3 ระเบิดเวลา — เก็บกวาดก่อน final (จาก audit)
1. 🔶 **n ไม่ตรงกัน** — `05` เขียน n=181, `10` เขียน n=28 → ยึดเลขเดียวจาก `metrics.json` จริง พูดเลขเดียวตลอด (slide ต้องตรง report)
2. 🔶 **κ วัดกับอะไร** — แยก classifier 3-class vs vigor ordinal ทุกที่ที่พูดถึง
3. 🔶 **paper ผี "Thomas 2026"** — ยังเหลือ note ใน `08_survival_contamination` → ลบ

---

## 🗓️ ลำดับเขียนที่แนะนำ (ขนานกับงาน lab)
- **ก.ค. (ระหว่างต้นโต):** เรียบเรียง **บท 1, 2, 3** จาก research docs → ได้ ~70% ของเล่มโดยไม่ต้องรอ data
- **ส.ค.–ก.ย. (data เข้า):** เติม **บท 4** ตามผลที่ทยอยมา + เริ่ม 5.3 (ข้อจำกัด)
- **ต.ค.:** **บท 5 + บทคัดย่อ** + เก็บ 3 ระเบิดเวลา + จัดรูปเล่ม/บรรณานุกรม
