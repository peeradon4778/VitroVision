# 10 — Methods (v2)

> **สถานะ:** **v2** | สร้าง 2026-06-11 · อัปเดต 2026-06-12 (fold decisions + 19 audit fixes)
> **โปรเจกต์:** VitroVision — Computational phenotyping ของ *Capsicum annuum* in vitro tissue culture (YSC 2027 / CSBI)
> **อ้างอิงฐาน:** Research Design v1 (locked 2026-06-11) + research files `06`–`09` (citation verified ผ่าน Consensus/PubMed)
> **Decisions ที่ fold เข้า v2:**
> - Reference standard = **consensus (median) ของครู ≥2 คน** (รายงาน inter-rater แยก)
> - **Criterion validity (survival-to-acclimatization) = วิธีหลักพิสูจน์ vigor_score** (data-driven)
> - **Expert assessment = 2 axis** (developmental phase objective + vigor 1–5 holistic) + hyperhydric flag — §4.1
> - **Stats = hierarchical gatekeeping** (primary green% α=0.05/Bonferroni 3 contrasts · secondary FDR · contamination descriptive) — §5.3
> - **Env = ค่าจริง** 25±2°C / 16/8 h / LED 40–50 µmol — §1.7
> - **เวลาถ่าย = ล็อกคงที่ช่วงเย็น** (รอยืนยันเวลาเป๊ะ) — §2.2
> - ⏳ **เหลือรอ peeradon:** รุ่นกล้อง (§2.1) · เวลาถ่ายเป๊ะ (§2.2) · เวลาแช่ Clorox+ชนิดขวด (§1.1–1.2) · ค่า HSV calibrate กับ rig จริง (§3.2)

---

## 📌 TODO — จุดที่ต้องกลับมาแก้/กรอกเอง (รวมทุก ⚠️ ในไฟล์)

**A. ค่าแล็บที่ผมไม่รู้ (peeradon กรอก):**
- [x] §1.1 — whole-fruit Clorox 15%→10% ฟอก 2 รอบ → คีบเมล็ดจากผล (เกษตรกร อ.สตึก บุรีรัมย์), ไม่ใช้ GA₃, นับ day จาก emergence — **เหลือ:** เวลาแช่/รอบ + Tween/EtOH ไหม
- [x] §1.2 อาหาร — ตอบแล้ว (MS full / Glucose 20 / Kelcogel 3 g/L / pH 5.6–5.8 / PGR ก่อน autoclave / 121°C 15–20 min / ~30 mL/ขวด) — **เหลือ:** ชนิด/ขนาดขวด
- [x] §1.3 สถานะ — A/C/D ทำอาหารแล้วยังไม่หยอด, B/E พรุ่งนี้ → หยอด 1 เมล็ด/ขวดพร้อมกันทุกสูตร
- [x] §1.7 อุณหภูมิ/photoperiod/light = **ค่าจริงตรง default** 25±2°C / 16/8 h / LED 40–50 µmol (2026-06-12)
- [ ] §2.1 **รุ่นกล้อง/มือถือ** (เหลือตัวนี้ตัวเดียวใน §2.1 — ค่าอื่นใส่แล้ว)
- [ ] §3.2 ค่า HSV threshold (green/brown) ที่ calibrate กับ rig จริง — *รอถ่าย calibration set*
- [x] §1.2 citation glucose แทน sucrose — **ได้แล้ว** Phillips & Hubstenberger 1985 (Capsicum-specific, glucose superior) + Arafa 2023 (chlorophyll) → `11_carbon_source_glucose.md`

**B. การตัดสินใจ (peeradon ตัด):**
- [~] §2.2 ล็อกเวลาถ่าย = **ล็อกคงที่ช่วงเย็น** (ตัดสินแล้ว) — เหลือยืนยันเวลาเป๊ะ (แนะนำ ~17:00)
- [x] §5.3 α + correction = **hierarchical gatekeeping** (primary green% α=0.05/Bonferroni 3 contrasts · secondary FDR · contamination descriptive) (2026-06-12)

**C. งานที่ต้องทำก่อนรายงานเลขจริง:**
- [ ] §3.3 เทรนด้วยภาพจริง (ตอนนี้ mock) + รัน 5-fold CV + แก้ healthy recall (class weight) ก่อนรายงาน κ/F1
- [ ] §4 หา inter-rater (ครู ≥2 คน blind) ก่อน validate
- [ ] เก็บ survival ตอนอนุบาล (§4.6) — ต้องวางแผน timeline ให้ทันก่อน ต.ค. 2026

**D. งาน code/data ที่ตามมาจาก research 12–14 (เฟส implement):**
- [ ] §3.5 เพิ่ม traits classical: PLA, Convex Hull Ratio, ExG/VARI, GLCM (ทำได้เลยใน phenotyper.py)
- [ ] §3.5 leaf count ด้วย YOLOv8-seg (ต้องมี labeled data)
- [ ] §3.6/§2.3 เพิ่ม **hyperhydric binary flag** ใน data capture + DB schema
- [ ] §2.4 label developmental stage ต่อภาพ (radicle/hypocotyl/cotyledon/true-leaf)
- [ ] §3.5 ใส่ reference scale marker ในเฟรมถ่ายภาพ (แก้ข้อจำกัด 2D)

---

## 1. Plant material และ experimental design

### 1.1 Plant material และ explant source

ใช้ *Capsicum annuum* L. cv. **'พริกจินดา'** พันธุ์เดียวตลอดการทดลอง เพื่อตัด genotype effect ออก — ผลเป็น cultivar-specific (genotype-dependent regeneration response เป็นที่ทราบในพริก — Kothari et al. 2009) ระบุเป็น scope/limitation ชัดเจน

**Starting material = เมล็ดที่คีบจากผลพริก** → seed-derived seedlings (NOT clonal) ผลคือแต่ละต้นมี **genetic variation** ระหว่าง individual → within-treatment variance สูงกว่าระบบ clonal = เหตุผลเชิงสถิติที่ design ต้องใช้ ≥2 batch + n สูง (§1.4)

**แหล่งวัสดุ:** ผลพริก cv.'พริกจินดา' จาก**เกษตรกรผู้ปลูกใน อ.สตึก จ.บุรีรัมย์** (provenance ระบุได้ + อยู่ในพื้นที่ field survey ของโครงการ)

**Sterilization & seed excision (วิธีจริง 2026-06-11):** **whole-fruit surface sterilization** — ฟอกผิว**ผลพริกทั้งลูก**ด้วย Clorox (sodium hypochlorite) แบบ **2 สเตป: 15% → 10% (v/v), ฟอกล้าง 2 รอบ** → ผ่าผลในสภาพปลอดเชื้อ → คีบเมล็ดจากภายในวางบนอาหาร. เหตุผล: เนื้อผลเป็น barrier ทำให้ภายในปลอดเชื้อตามธรรมชาติ + เมล็ดไม่โดน bleach โดยตรง → ไม่ลด germination/viability (ต่างจากการจุ่มเมล็ดใน NaOCl โดยตรง). [Clorox household ~5–6% NaOCl → 15% v/v ≈ 0.9% NaOCl, 10% v/v ≈ 0.6% NaOCl]

**ไม่ใช้ GA₃ pre-treatment** — cv.'พริกจินดา' งอกง่ายอยู่แล้ว (ไม่ต้องเร่ง); การจัดการเมล็ดงอกไม่พร้อมกันใช้วิธี **align growth curve จากวันงอก (emergence)** แทน (§2.2) → design สะอาด ไม่มีฮอร์โมนภายนอกเพิ่ม

⚠️ **เหลือเล็กน้อย:** เวลาแช่ต่อรอบ (กี่นาที), มี Tween-20 / EtOH dip ก่อนไหม

### 1.2 Culture media — 5 สูตร

basal = **MS medium** (Murashige & Skoog 1962) ปรับเฉพาะ plant growth regulator (PGR):

| สูตร | PGR (mg/L) | บทบาท |
|---|---|---|
| A | — (MS เปล่า) | control / baseline |
| B | BAP 1 | cytokinin ต่ำ |
| C | BAP 5 | cytokinin สูง (เร่งยอด) |
| D | BAP 5 + NAA 0.05 | cytokinin สูง + auxin ต่ำ |
| E | IBA 1 | auxin (เร่งราก) |

> **design caveat (research file 02):** สูตร E (IBA เดี่ยว) อยู่คนละ stage กับ A–D — ตีความผลต้องระวัง ไม่ควรเทียบตรงใน omnibus test เดียวโดยไม่อธิบาย; BAP มีแค่ 2 จุด (1, 5) → ถ้าจะ claim dose-response ควรมีจุดกลาง แต่ถ้า scope = "เทียบ 5 สูตรที่มีอยู่" ก็ defend ได้

**องค์ประกอบอาหาร (ค่าจริงจากแล็บ, ยืนยัน 2026-06-11):**
- Basal: **MS full strength** (Murashige & Skoog 1962)
- Carbon source: **Glucose 20 g/L** (⚑ deviation จากตำรา — ตำรามาตรฐานใช้ sucrose 30 g/L; ต้องระบุ + justify ใน Methods, ดูหมายเหตุล่าง)
- Gelling agent: **Kelcogel (gellan gum) 3 g/L** — ⚑ deviation จาก agar แต่ **เป็นข้อดีต่องานนี้** (วุ้นใส → imaging ผ่านขวดคมกว่า agar ขุ่น)
- pH: **5.6–5.8** ก่อน autoclave
- PGR: ใส่**ก่อน autoclave** (autoclavable, ไม่ filter-sterilize)
- Autoclave: **121°C, 15–20 นาที**
- ปริมาตร: **~30 mL/ขวด** (อาหาร 1 L ทำได้ ~40 ขวด)

⚠️ **ยังต้องกรอก:** ชนิด/ขนาดขวด

> **⚑ หมายเหตุ deviation (defend ได้แล้ว — ดู `11_carbon_source_glucose.md`):**
> (1) **Glucose แทน sucrose** — **มี Capsicum-specific evidence โดยตรง: Phillips & Hubstenberger (1985) ระบุ "Glucose was superior to sucrose as the carbon source" ใน *Capsicum annuum* บน MS medium**. กลไก: glucose เป็น monosaccharide ดูดซึมเข้า glycolysis ตรง ไม่ต้อง invertase hydrolysis (Wan 2017; Ruan 2012) — สำคัญใน explant ที่ตัดขาดจาก phloem. โบนัส: glucose ส่งเสริมการสะสม chlorophyll (Arafa 2023) = ดีต่อ green_coverage phenotype. + ทุกสูตร A–E ใช้ glucose เหมือนกัน → คงที่ข้าม treatment ไม่ใช่ confound. การเลือก carbon source ตาม genotype/explant = established practice (Yaseen 2013 review).
> (2) **Gellan gum (Kelcogel 3 g/L)** — จุดแข็ง: medium ใส → through-bottle imaging คุณภาพสูงกว่า agar ขุ่น = สนับสนุน CV approach โดยตรง

### 1.3 Experimental unit และ sowing

- **1 เมล็ด/ขวด ขวดปิดผนึก** → (ก) imaging ผ่านขวดไม่ต้องเปิด (non-destructive, sterile-safe), (ข) contamination data สะอาด (1 เหตุการณ์/ขวด), (ค) **ขวด = experimental unit ชัดเจน**
- **Growth-curve alignment:** นับ day จากวัน **"งอก (emergence)"** ของแต่ละขวด ไม่ใช่วันหว่าน (germination timing ต่างกัน → เทียบ curve ตรง phase)
- **germination = secondary endpoint** (บันทึก % + time-to-germination ต่อสูตร)

**สถานะจริง (2026-06-11):** อาหารสูตร A/C/D **ทำเป็นขวดแล้ว แต่ยังไม่ได้หยอดเมล็ด** (พักขวดอาหารไว้เฉยๆ); สูตร B/E ทำพรุ่งนี้ (ครบ set 1). ✅ **ข้อดี:** เพราะยังไม่หยอดอะไรเลย → ทุกสูตรเริ่ม sow พร้อมกันจาก state เดียวกัน, ใช้ 1 เมล็ด/ขวด + ติด ArUco ก่อนหยอด + นับ day จากวันงอก ได้ครบทุกสูตรตั้งแต่ต้น = ไม่มี inconsistency ระหว่าง A/C/D กับ B/E

### 1.4 Replication และ power analysis

Power analysis a priori (k=5, α=0.05, KW≈one-way ANOVA):

| n/สูตร | Power (large f=0.40) | Power (medium f=0.25) |
|---|---|---|
| 20 (1 batch) | 0.90 | **0.47** ← ไม่พอ |
| ~40 (pool 2 batch) | >0.99 | **0.81** ← พอ |

n ที่ต้องการเพื่อ power 0.80: ใหญ่ ≥16, **กลาง ≥40**, เล็ก ≥240

**ตัดสิน: ≥2 batch → pool n ≈ 40 ขวด/สูตร** (powers medium effect 0.81 + reproducibility) · over-sow buffer ~24–25 ขวด/สูตร/batch กัน non-germination → เหลือ ~20 ใช้ได้ · validation set: ρ=0.70 ต้องการแค่ ~15 paired, ครูให้คะแนน ~40–50 ภาพ = เกินพอ

### 1.5 Batch design และ blocking

**Pooling ≠ stacking** — batch = **blocking/random factor** ไม่ใช่แค่กองรวมเพิ่ม n:
- batch ต่างกัน = เวลาเตรียม media / สภาพห้อง / seed lot ต่างเล็กน้อย
- model: `formula (fixed) + batch (random) + formula×batch` (§5)
- **`formula×batch` interaction = reproducibility check** — ไม่มีนัยสำคัญ = effect ซ้ำได้ข้าม batch (ผลน่าเชื่อถือ); มี = รายงาน limitation
- ห้าม drop batch แม้ non-significant (Frey et al. 2024 — Type I error เพี้ยน)

### 1.6 Positional layout และ confound control

- เรียงสูตร **aligned กับ row** (ไม่ randomize) — ผู้ทดลองยืนยันทุกตำแหน่งได้แสงเท่ากัน
- `bottle_id` เข้ารหัส **ชั้น/row/col** → วิเคราะห์โดยใส่ **position เป็น covariate / test row effect**
- position ไม่มีนัยสำคัญ = **พิสูจน์ด้วยข้อมูลว่าไม่มี positional confound** → ตอบ judge ได้โดยไม่ต้องสุ่ม (จุดอ่อน "ไม่ randomize" → จุดแข็ง "วัดและพิสูจน์แล้ว")

### 1.7 Environmental conditions

ห้องเพาะเลี้ยงควบคุม: **อุณหภูมิ 25±2°C · photoperiod 16/8 h (light/dark) · แสง LED ~40–50 µmol/m²/s** — ห้อง/operator เดียวตลอดการทดลอง สภาพคงที่ (ตัดเป็นตัวแปรร่วม)

### 1.8 Specimen tracking (ArUco)

ติด **ArUco marker (DICT_4X4_100, ~3 cm)** ข้างขวด **ก่อน inoculate ทุกครั้ง** → detect `bottle_id` อัตโนมัติจากภาพ (precedent: Wienbruch et al. 2025; accuracy เพียงพอ translation error ~1.36 mm — Costa et al. 2024) ไฟล์พร้อมพิมพ์: `aruco_stickers.pdf` (100 markers S01-A-01…S02-E-10). → ดู `09_methods_misc.md` §2 สำหรับ precedent ArUco ฉบับละเอียด

**Boundaries (proposal):** 5 สูตร MS เท่านั้น · contamination ธรรมชาติ = observational · ห้อง/operator เดียว · CV validated เฉพาะ camera/lighting setup นี้ · 2D RGB single-view · window 28 วัน · cultivar เดียว ('พริกจินดา')

## 2. Imaging protocol

### 2.1 Imaging rig (มาตรฐานคงที่)

ถ่ายภาพ **ผ่านขวด (non-destructive, ไม่เปิดฝา)** ในชุดถ่ายที่คุมตัวแปรคงที่ทุกครั้ง: ระยะกล้อง–ขวด, มุม, แสง, background — **1 มุม/ขวด** ใช้ **lightbox** (แสงสม่ำเสมอ) + **แผ่นอ้างอิงสีขาว (white reference card)** ในเฟรมทุกภาพ เพื่อ white-balance/normalize สีตอน post-process (สำคัญมากเพราะ feature หลักเป็นสี — green%/LCI)

⚠️ **ต้องกรอกค่าจริง:** รุ่นกล้อง/มือถือ, ความละเอียด (เช่น 1920×1080+), ระยะถ่าย (cm), แหล่งแสง lightbox (สี/ความสว่าง), exposure/ISO/white-balance ตั้ง manual หรือ auto (แนะนำ manual ล็อกค่า)

### 2.2 Temporal sampling

window **28 วัน** (start → พร้อมอนุบาล) ถ่าย **~20–25 timepoints/ขวด** (เกือบทุกวัน, ขาด 1–2 วันได้) — **fit growth curve กับเลข day จริง ไม่ใช่สมมติเว้นเท่ากัน** **Growth-curve align จากวัน "งอก (emergence)"** ของแต่ละขวด ไม่ใช่วันหว่าน

**ล็อกเวลาถ่ายเดิมทุกวัน** (ตัด diurnal effect จากรอบเปิด/ปิดไฟตู้เพาะ) — เวลาคงที่ในช่วงเย็นหลังเลิกเรียน *(แนะนำ ~17:00 น. — รอพีรดนย์ยืนยันเวลาเป๊ะตามตารางจริง)*

### 2.3 Status logging

บันทึกทุกครั้งที่ถ่าย: **status label** (healthy/contaminated/dead ตาม rubric) + **hyperhydric flag** (§3.6) + **วันเริ่มปนเปื้อน** (feed survival analysis §5) + วันงอก ทุก record ผูกกับ `bottle_id` จาก ArUco อัตโนมัติ

### 2.4 Developmental stage labeling (จาก `12_capsicum_germination_ontogeny.md`)

label ระยะพัฒนาการต่อภาพ เพื่อ align growth curve ตาม stage + รู้ว่ากำลังดู phenotype ระยะไหน (พริก in vitro, DAP = days after sowing):

| Stage | DAP โดยประมาณ | ลักษณะสังเกต |
|---|---|---|
| Radicle emergence (= วันงอก) | ~7–12 | รากแรกโผล่ → **เริ่มนับ day curve ที่นี่** |
| Hypocotyl elongation | ~5–10 | ลำต้นใต้ใบเลี้ยงยืด |
| **Cotyledon expanded** | **~10–14** | ใบเลี้ยงกางเต็ม = **anchor ชัดสุด** (Stoffella 1988) |
| True leaf คู่แรก | ~18–28 | ใบจริงคู่แรก |

> **window 28 วันครอบ S0–S6 ครบ** ถ้างอกใน DAP 7 · ระวัง: hypocotyl ยืดผิดปกติได้ถ้าแสงผ่านขวดน้อย → label เป็น abnormal แยก (กัน bias)

## 3. Phenotype extraction

### 3.1 Hybrid pipeline overview

ระบบ VitroVision เป็น **hybrid** — classical CV (โปร่งใส อธิบายได้) + deep learning เหมาะกับสภาพแสงควบคุมของตู้เพาะ

### 3.2 Classical CV — quantitative image analysis (7 features)

สกัด 7 features ต่อภาพ (โค้ดจริง `shelf_manager/phenotyper.py`):

| Feature | วิธีคำนวณ |
|---|---|
| `green_coverage_pct` | HSV thresholding แยก pixel เขียว / pixel พืชทั้งหมด ×100 |
| `leaf_color_index` (LCI) | อัตราส่วน G/R เฉลี่ยในพื้นที่พืช |
| `shoot_count` | connected components / morphology นับยอด |
| `media_color` | สีเฉลี่ยของอาหาร (proxy การเปลี่ยนแปลง/ปนเปื้อน) |
| `texture_entropy` | Shannon entropy ของ texture |
| `brown_coverage_pct` | HSV threshold สีน้ำตาล (necrosis/browning) |
| `vigor_score` | weighted score ตั้งมือ 0–10 (ดูหมายเหตุล่าง) |

⚠️ **ต้องกรอก/calibrate:** ค่า HSV threshold (green/brown range) ต้อง calibrate กับ lighting rig จริง (§2.1) — ค่าใน prototype อาจไม่ตรงกับ setup ใหม่; ระบุค่าที่ใช้จริงใน appendix

> **honest framing (CSBI):** 7 features นี้ = classical CV/คณิต **ไม่ใช่ AI** (HSV threshold, morphology, entropy, weighted score) — อย่าเรียกว่า "AI". ข้อจำกัด color index คือไวต่อแสง [Lu 2022] แต่ตู้เพาะคุมแสง → ข้อจำกัดเบาลง = เหตุผลที่ CV ใช้ได้ดีในบริบทนี้

### 3.3 Deep learning components

- **EfficientNet-B0** (transfer learning) จำแนกสถานะ **healthy / contaminated / dead**
- **YOLOv8-seg** (optional, ถ้าเทรน) — segmentation แยกพืช/อาหาร + นับยอดแม่นขึ้น (hook `models/phenotype/seg.pt`)
- = **AI จริง** ของโปรเจกต์ (justify EfficientNet choice: Atila 2021)

⚠️ **ต้องอัปเดตด้วยผลจริง:** baseline ปัจจุบัน Cohen's κ=0.6274, weighted F1=0.7496 จาก n=28 (CI กว้าง ~±0.20) — ต้องรัน **5-fold CV** + เทรนด้วยภาพจริง (ตอนนี้ใช้ภาพสังเคราะห์/mock) ก่อนรายงานเลขใน proposal; healthy recall ยังอ่อน (60%) รอแก้ด้วย class weight

### 3.4 Endpoints

**Primary = `green_coverage_pct`** (Depetris 2025, Signorelli 2025); **Secondary (Bonferroni)**: vigor_score, brown_coverage_pct, leaf_color_index, shoot_count

> **vigor_score:** น้ำหนักตั้งมือ **ไม่ใช้เป็นข้อสรุปสุดท้าย** — ถูก re-derive แบบ data-driven จาก survival ใน §4.6 (เก็บสูตรเดิมเป็น interpretable baseline คู่กัน)

### 3.5 Morphological trait roadmap (จาก research 12–14)

**Traits ที่ควรเพิ่ม** (เรียงตามทำง่าย→ยาก, ดู `14_image_dl_phenotyping.md`):

| Trait | วิธี | สถานะ |
|---|---|---|
| Projected Leaf Area (PLA) | classical CV | เพิ่มได้ทันที |
| Convex Hull Ratio (solidity) | classical CV | จับ shoot architecture (กระจุก vs เดี่ยว) |
| ExG / VARI color index | classical CV | chlorophyll proxy จาก RGB |
| GLCM texture | classical CV | ต่อยอดจาก entropy เดิม |
| Leaf count (N_visible) | **DL (YOLOv8-seg)** | มี hook แล้ว, biological relevance สูง |

> **ข้อจำกัด 2D single-view (ต้อง frame ให้ชัด):** occlusion → PLA/leaf-count underestimate, ไม่มี height/stem-diameter, glass glare บิด color → เรียก trait ว่า **"projected/visible"** เสมอ + ใส่ **reference scale marker** ในเฟรม. Pepper-specific DL precedent: Gómez-Zamanillo 2024 (instance seg mAP 0.39→0.97), Islam 2024 (color+GLCM 86%); reference pipeline = PlantCV (Gehan 2017)

### 3.6 Hyperhydricity = phenotype ที่ CV ควรจับ (finding thread)

จาก research 12+13: **BAP สูง (สูตร C) + ขวดปิดผนึก (ethylene สะสม) → hyperhydricity/vitrification** — external proxy ที่ CV เห็นได้: **ใบใส/ฉ่ำน้ำ (glassy/translucent), สีซีด/เหลือง, ลำต้น/ใบบวม, ขอบใบย่น**. มี precedent ตรง: Bethge et al. 2023 จับ hyperhydricity ด้วย ML ได้ ~85% accuracy. → **source of truth สำหรับชีววิทยา hyperhydricity = `13_pgr_morphology.md` §4** (visual features + กลไก PGR เต็ม)

> **เป็นจุดขายเชิง finding:** เชื่อม biology (cytokinin สูง + sealed vessel → hyperhydric) เข้ากับ CV (ตรวจอัตโนมัติจากภาพ) — ไม่ใช่แค่วัด growth. **candidate class เพิ่มเติม** สำหรับ classifier (นอกจาก healthy/contaminated/dead) เมื่อมี labeled data พอ; ระยะแรกบันทึกเป็น phenotype flag แยกก่อน

---

## 4. Validation of the VitroVision phenotyping system

### 4.0 หลักการ

งานเคลม **METHOD-primary** — VitroVision (เครื่องมือ) คือผลงานหลัก, 5 สูตรเป็น use case ความน่าเชื่อถือขึ้นกับการพิสูจน์ว่า (ก) ค่าที่เครื่องวัดสอดคล้องกับผู้เชี่ยวชาญ และ (ข) ทำนายผลลัพธ์ปลายทางที่มีความหมายทางชีววิทยาได้ จึง validate 2 แกนคู่กัน:
- **Convergent validity:** CV สอดคล้องกับ expert แค่ไหน
- **Criterion validity:** ค่า CV ทำนาย survival ตอนอนุบาลได้ไหม (แกน non-circular ไม่ต้องพึ่ง subjective score หรือเครื่องมือราคาแพง ที่เราไม่มี: SPAD/spectrophotometer)

### 4.1 Reference standard: expert assessment (2 axis + flag)

เนื่องจาก **ยังไม่มี validated ordinal vigor scale สำหรับ *Capsicum* in vitro โดยเฉพาะ** (วงการ TC ส่วนใหญ่ใช้ morphometric นับตรงๆ ไม่ใช่ ordinal scale — Rafiq 2021, Pattnaik 2000) เราจึงสร้าง reference เองตามหลัก rating-scale methodology (anchored ordinal scale ลด rater error — **Bock et al. 2010**; พิสูจน์ inter-rater ก่อนใช้ — **de Raadt et al. 2021**) โดยมี precedent ว่าการสร้าง visual scale สำหรับ in vitro regenerant เป็นวิธีที่ยอมรับ (**Myakisheva et al. 2024** — phase-based scale ของ hops regenerant; **Ding et al. 2025** — 5-level vigor classification)

ครูบันทึก **2 แกนแยกกัน + 1 flag** ต่อขวดต่อ timepoint:

**Axis A — Developmental phase (objective, นับโครงสร้างได้)** — ตาม phase-based assessment ของ Myakisheva 2024 แต่ใช้บริบทพริก:
| Phase | เกณฑ์ |
|---|---|
| Intensive growth | งอก + กำลังสร้างใบ/ยอดเร็ว (early sigmoid) |
| Slow growth | การเจริญชะลอ เข้าใกล้ plateau |
| Senescent / dying-off | เหลือง/น้ำตาล/ตาย |

> Axis A ผูกกับ Gompertz growth-curve parameter โดยตรง (§5.1) — ของ Myakisheva ใช้ internode-sigmoid, ของเราใช้ green%-Gompertz เป็น proxy (วัดผ่านขวด non-destructive แทนการนับ internode ด้วยมือ)

**Axis B — Vigor quality (holistic ordinal 1–5)** — ครูตัดสิน "ภาพรวมความสมบูรณ์" จากหลาย cue พร้อมกัน (สี+ทรงพุ่ม+จำนวนยอด+ความสมบูรณ์) **ไม่ใช่สูตรคำนวณจาก feature เดียว** (กัน circularity กับ CV):
| Grade | นิยาม holistic | cue ประกอบ (ไม่ใช่สูตร) |
|---|---|---|
| 1 | ตาย/ไม่งอก น้ำตาลเด่น ไม่มีส่วนเขียวมีชีวิต | — |
| 2 | อ่อนแอ งอกแต่ชะงัก เหลือง/ซีด เขียวน้อย | ไม่มียอดชัด/ยอดเดียวอ่อน |
| 3 | ปานกลาง เขียวบางส่วน เริ่มตั้งตัว | มี ≥1 ยอด ใบเริ่มกาง |
| 4 | ดี แข็งแรงชัด เขียวเข้ม ทรงสมบูรณ์ | ยอดชัดเจน ใบกางดี |
| 5 | ดีมาก สมบูรณ์เด่น พุ่มเขียวเข้มแน่น | หลายยอด/พุ่มแน่น แข็งแรงเต็มที่ |

> **เหตุผลที่ Axis B ต้อง holistic ไม่ anchor ด้วย green%:** ถ้า anchor ด้วย "% พื้นที่เขียว" จะวนกับ `green_coverage_pct` ที่ CV วัด → validation ดูปลอม. Axis B เป็น gestalt ที่ต่างจาก feature เดี่ยว → ใช้พิสูจน์ **convergent validity** (CV vs rubric §4.4) ส่วนความ **non-circular** หลักพึ่ง **criterion validity = survival-to-acclimatization** (§4.6)

**Flag — hyperhydric (binary แยก):** อาการ vitrification (ใบใส/ฉ่ำ/บวม/ซีด, §3.6) **ไม่ใช่แค่ vigor ต่ำ** — abnormal phenotype คนละแกน บันทึกแยก (อย่ายุบเป็น grade 1) เพื่อวิเคราะห์ hyperhydricity rate ต่อสูตร + เลี่ยงสับสนกับต้นโตช้าธรรมดา

rubric เต็ม + calibration set (ภาพตัวอย่างต่อ grade/phase) อยู่ใน appendix; ครูทุกคนได้ชุดเดียวกันก่อนเริ่ม (training aid)

### 4.2 Validation set และ blinding

- **Sample:** สุ่ม **≥40 ขวด** (stratified ตาม grade distribution คาด, ข้ามทั้ง 5 สูตร) — เกิน ≥30 ที่ Koo & Li 2016 แนะนำเพื่อให้ 95% CI ของ ICC แคบพอ interpret; เกินพอสำหรับ Spearman (ρ=0.70 ต้องการ ~15 paired)
- **1 ภาพ/ขวด** (independent unit — เลี่ยง pseudoreplication ในขั้น validation)
- **Blinding:** ครูให้คะแนนจากภาพ โดยไม่เห็นสูตร / bottle_id / ผล CV / คะแนน rater อื่น; ลำดับภาพสุ่มใหม่ต่อ rater
- **Raters:** ครู TC ≥2 คน อิสระต่อกัน

### 4.3 Reference score = consensus (median) + inter-rater study

**Reference standard ที่ใช้เทียบ CV = median ของคะแนนครู ≥2 คน ต่อขวด** (ทางเลือก B) — เกลี่ย noise ส่วนตัวของครูแต่ละคน → reference นิ่งและใกล้ "vigor จริง" มากกว่าการยึดครูคนเดียว ตอบ judge ได้ว่าไม่พึ่งความเห็นคนเดียว

**Inter-rater study (รายงานแยก, สร้าง empirical ceiling):**
- ครูทุกคน rate validation set ชุดเดียวกัน blind
- คำนวณ inter-rater agreement (ครู A vs ครู B): **Spearman ρ, quadratic-weighted κ, ICC(2,1) absolute**
- ค่านี้ = **ceiling** = ระดับที่ "มนุษย์ด้วยกันเองเห็นตรงกัน" → เป็นเกณฑ์ว่า CV ที่ดีควรทำได้ถึงไหน

### 4.4 Convergent validity — CV vs consensus reference

เทียบ CV กับ consensus reference (median ครู) ด้วย **metric suite 3 ตัว** ที่วัดคนละมุม — ไม่ redundant เพราะ de Raadt et al. 2021 แสดงว่าทั้งสามให้ข้อสรุปตรงกัน "in virtually all cases" *ยกเว้น*เมื่อ agreement สูงมาก ซึ่งจุดนั้นความต่างคือ diagnostic:

| Metric | คำถามที่ตอบ | Acceptable | Target | อ้างอิง |
|---|---|---|---|---|
| **Spearman ρ** (primary) | CV กับ expert เรียง rank เหมือนกันไหม | ≥0.70 | ≥0.85 | Bock 2010; Schober 2018 |
| **Quadratic-weighted κ** | เห็นด้วยจริงไหม + penalize disagreement ไกล (weight=(i−j)²) | ≥0.60 | ≥0.80 | Li et al. 2023 |
| **ICC(2,1) absolute** | ค่าตรงกันแบบ absolute ไหม (two-way mixed, single measures) | ≥0.75 | ≥0.90 | Koo & Li 2016 |

**กฎการรายงาน (บังคับ):**
- รายงาน Spearman ρ **คู่กับ agreement metric เสมอ** — ρ สูง ≠ agreement ดี (rater A=[1,2,3,4] vs B=[2,3,4,5] ให้ ρ=1.0 แต่ค่าจริงไม่ตรงเลย — Svensson 2012)
- ระบุเต็ม "**ICC(2,1), two-way mixed effects, absolute agreement, single measures**" และ "**quadratic-weighted κ**" (Li et al. 2023)
- รายงาน **95% CI** ทุกค่า
- **Pre-register a priori threshold** ก่อนเก็บข้อมูล

**Diagnostic:** ถ้า Spearman สูงแต่ ICC ต่ำ = **systematic offset** ระหว่าง CV กับ expert → แก้ด้วย calibration/rescaling ไม่ใช่ทิ้งโมเดล

### 4.5 การ interpret ผ่าน Gold Standard Paradox

*(→ rationale เต็ม + citation = `06_validation_methodology.md` §3–§4; ส่วนนี้เก็บเฉพาะข้อความ Discussion ที่จะใส่จริง)*

Expert visual score เป็น gold standard ที่มี bias โดยธรรมชาติ — Aeffner et al. 2017 ชี้ว่า image analysis ถูกสร้างมา *เพื่อเอาชนะ* bias ของการประเมินด้วยสายตา ดังนั้น "ไม่ตรงกับ expert 100%" ไม่จำเป็นต้องแปลว่า CV ผิด interpret ด้วยกรอบ:
1. ใช้ inter-rater ceiling (§4.3) เป็นตัวเทียบ
2. **CV ≥ ceiling** → perform เทียบเท่า/เหนือกว่ามนุษย์ → valid
3. **CV < ceiling แต่ผ่าน a priori threshold** → ยัง valid ในระดับที่ประกาศล่วงหน้า
4. CV เกิน expert–expert agreement ในบาง metric → evidence ของ objectivity ที่เพิ่มขึ้น (สอดคล้อง Bock 2010 ที่ว่ามนุษย์มัก overestimate ที่ severity ต่ำ เช่น Grade 1)

**ข้อความ Limitations/Discussion:**
> "Expert visual score ที่ใช้เป็น gold standard มีข้อจำกัดที่ทราบในวรรณกรรม (Aeffner et al., 2017) เช่น overestimation ที่ severity ต่ำ (Bock et al., 2010). Inter-rater agreement ระหว่างผู้เชี่ยวชาญ (ICC = [ค่า], weighted κ = [ค่า]) เป็น empirical ceiling ที่บ่งชี้ว่าความสอดคล้องของ VitroVision กับ expert อยู่ในระดับ [ดีกว่า/เทียบเท่า/ต่ำกว่า] ขีดจำกัดที่ inherent ของ gold standard เอง"

### 4.6 Criterion validity — survival-to-acclimatization (แกนหลักพิสูจน์ vigor_score)

แกนนี้คือ**คำตอบของปัญหา vigor_score ตั้งมือ**ที่ค้างมาตลอด: แทนที่จะ defend น้ำหนักที่เดาเอง ใช้ **outcome ปลายทาง (รอด/ไม่รอดตอนอนุบาล)** เป็นตัวตัดสินว่า feature ไหน/น้ำหนักแบบไหนมีความหมายทางชีววิทยาจริง — outcome นี้ objective, biologically meaningful, และไม่ต้องใช้เครื่องมือพิเศษ

**Protocol:**
- จบ window 28 วัน → นำต้นไปอนุบาล (ex vitro acclimatization) ตาม protocol มาตรฐาน
- บันทึก **binary survival** (รอด/ตาย) ที่จุดเวลากำหนด (เช่น 2–4 สัปดาห์หลังย้าย)

**สถิติ (vigor_score กลายเป็น data-driven):**
- **Logistic regression:** `survival ~ green_coverage + brown_coverage + leaf_color_index + shoot_count + texture_entropy` → ให้ข้อมูล survival กำหนดน้ำหนักของ feature ที่ทำนาย "รอด" ได้จริง → vigor_score ฉบับ data-driven = predicted probability ของ survival (แทนน้ำหนักตั้งมือ)
- รายงาน **AUC-ROC + odds ratio** เป็นหลักฐานว่า phenotype ที่ระบบวัดมีความหมายทางชีววิทยา
- เปรียบเทียบ green%/vigor ระหว่างกลุ่มรอด vs ตาย (Mann-Whitney U) เป็น supporting
- รองรับว่า in vitro quality → ex vitro survival มีจริง: **Ahmed et al. 2026** (BMC Plant Biol), **Kongbangkerd et al. 2026** (Sci Rep), **Méndez-Hernández et al. 2023** (Plants)

> เก็บ vigor_score สูตรเดิม (rule-based) ไว้เป็น interpretable baseline คู่กัน แต่**ข้อสรุปอ้างอิงเวอร์ชัน data-driven** ที่ survival เป็นตัวพิสูจน์
> "Thomas 2026" ที่เคยอ้างใน design ถูกตัดทิ้ง — verify แล้วไม่มี paper นี้จริง

### 4.7 Software และ reporting checklist

- **คำนวณ:** ICC ด้วย `pingouin` (Python) / `irr` (R); weighted κ ด้วย `sklearn.metrics.cohen_kappa_score(weights='quadratic')`; Spearman ด้วย `scipy.stats.spearmanr`; logistic regression + ROC ด้วย `scikit-learn`
- **Reporting checklist (Methods):**
  - [ ] จำนวน rater (≥2), expertise, blind conditions, reference = median consensus
  - [ ] ICC model เต็ม: "ICC(2,1), two-way mixed, absolute agreement, single measures"
  - [ ] κ weights: "quadratic-weighted"
  - [ ] 95% CI ของทุก metric
  - [ ] a priori threshold (pre-registered)
  - [ ] rubric เต็ม + calibration set ใน appendix

---

## 5. Statistical analysis

### 5.1 Growth-curve modeling (per vessel)

fit **Gompertz 3-parameter ต่อขวด** จาก green% time-series:
`y = K·exp(−exp(−k(t−t₀)))` → ดึง **growth rate *k*** และ **inflection *t₀*** (carrying capacity *K* อาจ unreliable ถ้าไม่ถึง plateau ใน 28 วัน)
- ถ้า K ไม่ stable → **fix K=100** (2-param fallback, Vaghi et al. 2020)
- รายงาน R²/RMSE ต่อขวด → **flag ขวด R²<0.7** แล้วทำ sensitivity analysis (มี/ไม่มีขวดนั้น)
- เลือก parametrisation ตาม Tjørve & Tjørve 2017
- implement: `scipy.optimize.curve_fit`

### 5.2 Unit of analysis (สำคัญสุด)

**ขวด = experimental unit ไม่ใช่ภาพ** — สรุป growth parameter รายขวดก่อนเสมอ ห้ามนับภาพ 20–25 ภาพ/ขวดเป็น n (= pseudoreplication, inflate n → false significant, Hurlbert 1984)

### 5.3 เปรียบเทียบ 5 สูตร

ตรวจ normality ของ parameter (Shapiro-Wilk + QQ-plot) แล้วแยกทาง:
- **normal → LMM:** `lmer(k ~ formula + (1|batch))` + emmeans (Bonferroni)
- **non-normal → ART ANOVA:** `art(k ~ formula × batch)` + post-hoc **ART-C** (Elkin 2021 — *ไม่ใช่* Dunn/contrast ปกติ)
- **Kruskal-Wallis + Dunn** = secondary/preliminary เท่านั้น (one-factor, test interaction ไม่ได้)

**Multiple-comparison strategy = hierarchical (gatekeeping)** — α = 0.05:
- **Primary endpoint เดียว = `green_coverage_pct`** → ทดสอบ 3 planned contrasts (ด้านล่าง) ด้วย **Bonferroni** = α/3 ≈ 0.017/คู่ (เบา เพราะแค่ 3 คู่ ไม่ใช่ all-pairwise 10 คู่)
- **Secondary endpoints** (vigor, brown%, LCI, shoot_count) → รายงานด้วย **FDR (Benjamini-Hochberg)** ในฐานะ supportive evidence
- **Contamination/survival** → descriptive (KM + log-rank exploratory, §5.5)
- **ทุกที่รายงาน effect size + 95% CI ไม่ใช่แค่ p** (variance TC สูง → CI เล่าความจริงดีกว่า p; เหมาะกรรมการ CSBI)
- **Figure หลัก:** growth curve 5 สูตร (mean ± CI band) + forest plot ของ 3 planned contrasts (effect size + CI)

**Planned contrasts (pre-registered — เพราะ A–E ไม่ใช่ gradient เดียว แต่เป็น 2-hormone exploration):**
แทนที่จะเคลม dose-response ข้าม A–E ด้วย omnibus เดียว (= caveat ไฟล์ 02) → กำหนดคู่เปรียบล่วงหน้าตามตรรกะชีววิทยา:
- **A vs B vs C** — ผลของ "ระดับ cytokinin" (0 → 1 → 5 BAP)
- **C vs D** — ผลของ "เติม NAA 0.05 เข้าไปใน BAP สูง"
- **A vs E** — ผลของ "auxin (IBA) เดี่ยว เทียบ control"

เหตุผลเชิง design: ทำครบ 5 สูตร**ในทุก batch** (complete block) เพื่อรักษา blocking — ห้ามแยก E ไปทำ batch หลัง (จะ confound IBA กับ batch effect แยกไม่ออก)

### 5.4 Reproducibility check

**`formula × batch` interaction** — อยากได้ **ไม่มีนัยสำคัญ** = effect ของสูตรซ้ำได้ข้าม batch (ผลน่าเชื่อถือ); มีนัยสำคัญ = รายงานเป็น limitation. **ห้าม drop batch แม้ non-significant** (Frey et al. 2024 — Type I error เพี้ยน)

### 5.5 Contamination — survival analysis (exploratory)

**Kaplan-Meier + log-rank** เปรียบ time-to-contamination ข้าม 5 สูตร — **exploratory** เพราะ power ขึ้นกับจำนวน events จริง (ปนเปื้อนน้อย = underpowered)
- events น้อย → ใช้ **exact permutation test** แทน asymptotic log-rank
- ระวัง **competing-event censoring** (ขวดที่ถูกเอาออกด้วยเหตุอื่น) — bias cumulative incidence (Coemans et al. 2022)
- analogous precedent: seed germination (McNair 2012, Onofri 2022); KM กับ TC contamination = งานแรกในบริบทนี้
- implement: R `survival`
- → methodology rationale เต็ม (censoring types, few-event caveat, exact test) = `08_survival_contamination.md`

### 5.6 Position confound check

ใส่ **position (ชั้น/row/col จาก bottle_id) เป็น covariate** หรือ test row effect → ถ้าไม่มีนัยสำคัญ = พิสูจน์ด้วยข้อมูลว่าไม่มี positional confound (§1.6)

## 6. Hypotheses

- **Validation (primary):** H₀ ρ=0 (CV vs consensus expert) → H₁ ρ>0, เป้า ρ≥0.70; + criterion: green%/vigor (data-driven) ทำนาย survival ตอนอนุบาล (AUC สูงกว่า chance)
- **Biological:** H₀ 5 สูตร growth-params เท่ากัน → H₁ ต่าง ≥1 สูตร. **ทิศทางขึ้นกับ trait:** คาด cytokinin สูง (C,D) ให้ **จำนวนยอด** > control (A) แต่ **vigor quality อาจไม่สูงกว่า** เพราะ BAP 5 เสี่ยง hyperhydric/stunted (§3.6) → จุดขาย CV = แยก "ยอดเยอะ" ออกจาก "ต้นสมบูรณ์" ได้
- **Reproducibility:** H₀ ไม่มี formula×batch interaction (อยาก fail to reject)
- **Contamination:** exploratory

## 7. Software

Python (`scipy.optimize.curve_fit`, `pingouin`, `scikit-learn`, `scipy.stats`), R (`lme4`, `emmeans`, `ARTool`, `dunn.test`, `survival`)

---

## References (verified — ดูไฟล์ 06–09 สำหรับ URL เต็ม)

Validation (06): Bock et al. 2010; de Raadt et al. 2021; Aeffner et al. 2017; Koo & Li 2016; Schober et al. 2018; Li et al. 2023; Svensson 2012 · Criterion: Ahmed et al. 2026; Kongbangkerd et al. 2026; Méndez-Hernández et al. 2023 · Stats (07): Hurlbert 1984; Vaghi et al. 2020; Tjørve & Tjørve 2017; Wobbrock et al. 2011; Elkin et al. 2021; Frey et al. 2024; Kruskal & Wallis 1952 · Survival (08): McNair et al. 2012; Onofri et al. 2022; Coemans et al. 2022 · Misc (09): Gal & Ghahramani 2015; Wienbruch et al. 2025; Ostertagová et al. 2014

*สร้างโดย Fable 5 (orchestrator) จาก Research Design v1 + research 06–09 · 2026-06-11*
