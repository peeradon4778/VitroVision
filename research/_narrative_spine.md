# 🎬 Narrative Spine — VitroVision (เส้นเรื่องโครงงานสำหรับนำเสนอ)

> **ใบนี้คืออะไร:** ร้อย research ทั้งหมดเป็น "เรื่องเดียว" ที่เล่าต่อเนื่องตั้งแต่ปัญหา → วิธี → ผล → impact + แปลแนวคิดยากให้กรรมการ/คนทั่วไปเข้าใจ ใช้เป็นโครงพูดพรีเซนต์ + โครงเขียน proposal/abstract
> สร้าง 2026-06-12 · อิง research 01–14 (audit แล้ว) + Methods draft + citation ที่ verify แล้ว
> **กรอบสาขา:** YSC 2027 → ISEF, **CSBI (ชีววิทยาเชิงคำนวณ)** — เครื่องมือ CV/ML ต้องผูกคำถามชีววิทยาเสมอ ห้ามลอยเป็น pure ML

## 🏷️ ชื่อโครงงาน Final (ล็อก 2026-06-18)

- **ไทย:** VitroVision: นวัตกรรมการวิเคราะห์ฟีโนไทป์เชิงคำนวณจากภาพของ *Capsicum frutescens* Mill. ในการเพาะเลี้ยงเนื้อเยื่อด้วย Vision-Language Models
- **EN:** VitroVision: Image-Based Computational Phenotyping of *Capsicum frutescens* Mill. in Vitro via Vision-Language Models
- **สาขา:** CS → CSBI (YSC 2027 → ISEF)

---

## 🎯 ประโยคเดียวที่ต้องจำ (one-liner / elevator pitch)

> "VitroVision คือเครื่องมือ computer vision ที่วัดสุขภาพและการเจริญของต้นพริกเพาะเลี้ยงเนื้อเยื่อ **จากภาพถ่ายผ่านขวด โดยไม่ต้องเปิดฝา** — แทนการประเมินด้วยสายตาที่ subjective — แล้วพิสูจน์ว่าวัดได้ตรงกับผู้เชี่ยวชาญและทำนายการรอดชีวิตจริงได้ โดยใช้การเปรียบเทียบ 5 สูตรอาหารเป็นบทพิสูจน์"

---

## โครงเรื่อง 5 องก์ (แต่ละองก์ = research ไฟล์ไหน)

### องก์ 1 — ปัญหา (ทำไมต้องสนใจ)
**เล่าว่า:** พริกเป็นพืชเศรษฐกิจสำคัญของไทย (ตลาด/มูลค่า/โรค) → การขยายพันธุ์ปลอดโรคด้วยการเพาะเลี้ยงเนื้อเยื่อ (tissue culture) จึงสำคัญ → **แต่** การประเมินว่าต้นในขวด "แข็งแรง/ปนเปื้อน/ตาย" ปัจจุบันใช้ **สายตามนุษย์** = ช้า, subjective (คนละคนให้คะแนนไม่ตรงกัน), ทำซ้ำเชิงเวลาไม่ได้, ไม่ scale
- **ใช้:** `03_capsicum_economic_context.md` (เศรษฐกิจ) + `01_capsicum_tissue_culture.md` (TC background)
- **Hook สำหรับ intro:** Depetris 2025 — "few studies have demonstrated image analysis to phenotype plants under aseptic conditions" (DOI 10.3390/plants14101499)

### องก์ 2 — ช่องว่าง + Objective (เราทำอะไรใหม่)
**เล่าว่า:** ยังไม่มีเครื่องมือ computational phenotyping ที่ **validate แล้ว** สำหรับพริก in vitro → เราสร้าง VitroVision: วัด phenotype จากภาพ non-destructive + พิสูจน์ความน่าเชื่อถือ 2 ทาง (ตรงกับผู้เชี่ยวชาญ + ทำนายผลจริง)
- **Claim หลัก = METHOD-primary:** ผลงานคือ "เครื่องมือที่ validate แล้ว" ส่วน **5 สูตรอาหาร MS เป็น use case** ที่พิสูจน์ว่าเครื่องมือจับความต่างทางชีววิทยาได้จริง
- **ใช้:** `05_narrative_problem_objective_impact.md` (objective/hypotheses)
- ⚠️ **ระวังตอนเล่า (จาก audit C-05):** อย่าปนคำว่า κ ของ "classifier 3-class (healthy/contam/dead)" กับ κ ของ "vigor rubric 1–5" — เป็นคนละการวัด ต้องพูดแยกชัดว่ากำลังพูดถึงตัวไหน

### องก์ 3 — วิธี (ออกแบบยังไงให้เชื่อถือได้)
**เล่าว่า:** 5 สูตร MS (A=control, B/C=BAP, D=BAP+NAA, E=IBA) × ≥2 batch, เพาะจากเมล็ด 1 เมล็ด/ขวดปิดผนึก, ถ่ายภาพผ่านขวดเกือบทุกวัน 28 วัน, ติด ArUco อ่านรหัสขวดอัตโนมัติ, สกัด 12 phenotype features + จำแนกสถานะด้วย EfficientNet
- **ใช้:** `02` (สูตร PGR), `11` (glucose), `12` (germination), `13` (PGR→morphology), `14` (image phenotyping), `09` (ArUco)
- **จุดแข็งที่ต้องชู:**
  - **Kelcogel (วุ้นใส) แทน agar** → ถ่ายภาพผ่านขวดคมกว่า = ออกแบบมาเพื่อ CV โดยตรง
  - **Glucose แทน sucrose** → มีหลักฐานเฉพาะพริก (Phillips & **Hubstenberger** 1985, DOI 10.1007/BF00040200 — *แก้จาก "Collins" ที่เคยพิมพ์ผิด*)
  - **ArUco** → tracking ขวดอัตโนมัติ ไม่ต้องจดมือ

### องก์ 4 — การวิเคราะห์ + ผลที่คาด (พิสูจน์ยังไง)
**เล่าว่า:** 2 แกนคู่กัน
- **แกนชีววิทยา:** fit growth curve (Gompertz) ต่อขวด → ดึง growth rate → เทียบ 5 สูตร (ART-ANOVA/LMM) + เช็คว่าผลซ้ำได้ข้าม batch + วิเคราะห์การปนเปื้อนแบบ survival (Kaplan-Meier)
- **แกน validation (พระเอก):** เทียบค่าที่ CV วัด กับคะแนนครู ≥2 คน (Spearman ρ + ICC + weighted κ) + พิสูจน์ว่าค่า CV ทำนาย "การรอดตอนย้ายอนุบาล" ได้
- **ใช้:** `06` (validation), `07` (growth curve/stats), `08` (survival)
- ⚠️ **ระวัง (audit C-02):** post-hoc method ที่ถูกต้องคือ **ART-C** (ตาม file 10 source of truth) ไม่ใช่ Dunn — file 02/07 เขียนขัดกัน ต้องพูดให้ตรง file 10

### องก์ 5 — Impact (แล้วไง / ใครได้ประโยชน์)
**เล่าว่า:** ได้ (1) เครื่องมือ phenotyping ที่ validated + non-destructive สำหรับห้องแล็บ TC ใช้ต่อได้ (2) biological finding — สูตรไหนเร่งโต/เสี่ยง hyperhydricity + ตรวจ hyperhydricity อัตโนมัติจากภาพ (3) วิธีที่ scale ได้ ลดงานคนประเมินด้วยตา
- **ใช้:** `05` (impact section) + `04` (architecture/แผนระบบ)

---

## 🧩 แปลแนวคิดยาก → ภาษาคน (เตรียมตอบกรรมการ)

| แนวคิด | พูดสั้นๆ ให้เข้าใจ | ทำไมสำคัญ |
|---|---|---|
| **Gold Standard Paradox** | "เราเทียบ AI กับครู แต่ครูเองก็ลำเอียงได้ เลยวัดว่าครู 2 คนตรงกันแค่ไหนก่อน (เพดาน) แล้วดูว่า AI ทำได้ถึงเพดานนั้นไหม" | กัน judge ถาม "ถ้า AI ไม่ตรงครู 100% = ผิดไหม" → ตอบว่าไม่ เพราะครูก็ไม่ตรงกันเอง |
| **Pseudoreplication** | "ถ่ายขวดเดียว 25 รูปไม่ได้แปลว่ามี 25 ตัวอย่าง — มันคือขวดเดียว เลยนับ **ขวด** เป็นหน่วย ไม่ใช่ภาพ" | นับผิด = ผลดูมีนัยสำคัญทั้งที่ไม่จริง (Hurlbert 1984) |
| **Criterion validity (survival)** | "แทนที่จะเถียงว่าคะแนน vigor ที่เราตั้งถูกไหม เราดูผลจริง: ต้นที่ระบบให้คะแนนสูง รอดตอนย้ายปลูกมากกว่าจริงไหม" | แก้ปัญหา vigor_score ตั้งน้ำหนักมือ — ให้ผลจริงเป็นตัวตัดสิน (ไม่ circular) |
| **classical CV ≠ AI / EfficientNet = AI** | "การนับพื้นที่สีเขียว = คณิตศาสตร์ภาพธรรมดา ไม่ใช่ AI; ส่วนที่เป็น AI จริงคือโมเดล deep learning ที่จำแนกสถานะ" | honest framing — อย่าเคลมเกินจริง กรรมการ CSBI จับได้ |
| **ทำไมต้อง ≥2 batch** | "ทำรอบเดียวอาจฟลุ้ก เลยทำ ≥2 รอบ แล้วเช็คว่าผลออกมาเหมือนกันไหม (reproducibility)" | n พอ + พิสูจน์ว่าผลไม่ใช่เหตุบังเอิญของรอบเดียว |

---

## ⚠️ 3 จุดเสี่ยงในเรื่องเล่า (ต้องเคลียร์ก่อนพรีเซนต์ — จาก audit)

1. **ตัวเลข n/κ ต้องตรงกันทุกที่** (C-01) — ตอนนี้ file 05 บอก n=181, file 10 บอก n=28 → **ต้องเช็ค metrics.json จริง** แล้วพูดเลขเดียวตลอด ห้ามให้ slide ขัด report
2. **κ วัดกับอะไร** (C-05) — แยกให้ชัด: classifier 3-class = ตัวหนึ่ง, vigor ordinal validation = อีกตัว
3. **อย่าอ้าง paper ผี** — "Thomas 2026" ตัดทิ้ง (เหลือ note ใน file 08 ต้องลบ); citation ที่ load-bearing เช็คชื่อ co-author ให้ตรง (Phillips & Hubstenberger ไม่ใช่ Collins)

---

## 📌 ลำดับเล่าแนะนำ (3 นาที pitch)
ปัญหา (สายตา subjective) → ของใหม่ (เครื่องมือ validated) → วิธีสั้นๆ (5 สูตร + ถ่ายผ่านขวด) → **2 บทพิสูจน์** (ตรงกับครู + ทำนาย survival) → impact (แล็บใช้ต่อได้ + เจอผลชีววิทยา) → ปิดด้วย one-liner
