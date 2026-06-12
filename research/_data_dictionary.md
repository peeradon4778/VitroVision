# 🗂️ Data Dictionary + Endpoint Mapping — VitroVision

> **ใบนี้คืออะไร:** map ทุก field ข้อมูลที่ระบบเก็บ → ทุก hypothesis/endpoint ใน Methods (research/10 §4–6) เพื่อพิสูจน์ว่า "ข้อมูลที่เก็บครบพอตอบทุกคำถามวิจัยไหม" และชี้ **ช่องว่าง** ที่ยังไม่มีที่เก็บ/ยังไม่ capture
> สร้าง 2026-06-12 · อิง `shelf_manager/database.py` schema จริง + Methods draft v1

---

## 1. ตาราง `bottles` (1 แถว = 1 ขวด = หน่วยทดลอง)

| Field | ชนิด | ความหมาย | ใช้ใน endpoint |
|---|---|---|---|
| `bottle_id` | TEXT PK | รหัสขวด (เช่น S01-A-01) ผูกกับ ArUco | key เชื่อมทุกตาราง |
| `shelf`, `row`, `col` | TEXT/INT | ตำแหน่งบนชั้น | §5.6 position confound (covariate) |
| `batch_id` | INT | รอบที่ทำ | §1.5/§5.4 batch = random factor, reproducibility |
| `cultivar` | TEXT | 'พริกจินดา' | scope/limitation |
| `media_formula` | TEXT | A/B/C/D/E | **ตัวแปรต้นหลัก** — §5.3 เทียบ 5 สูตร |
| `pgr_detail` | TEXT | BAP/NAA/IBA mg/L | อธิบายสูตร |
| `passage_number` | INT | passage | ปกติ=1 (จากเมล็ด) |
| `species`, `treatment`, `date_planted`, `notes` | TEXT | metadata | date_planted ใช้ context |

---

## 2. ตาราง `images` (1 แถว = 1 ภาพถ่าย ณ วันหนึ่ง)

### ข้อมูลพื้นฐาน + สถานะ
| Field | ชนิด | ความหมาย | ใช้ใน endpoint |
|---|---|---|---|
| `bottle_id`, `batch_id` | — | เชื่อมขวด/รอบ | grouping |
| `day_point` | INT | วันที่เท่าไร (operator กรอก) | **แกน X ของ growth curve** §5.1 |
| `date_taken` | TEXT | timestamp จริง | audit/ordering |
| `status` | TEXT | healthy/contaminated/dead/unknown | §5.5 survival (time-to-contamination), §4.6 |
| `hyperhydricity` | INT(0/1) | flag ภาวะใบฉ่ำน้ำ | §3.6 hyperhydricity rate/สูตร |
| `has_roots` | INT(0/1) | มีรากไหม | morphology เสริม |
| `ai_status`, `ai_confidence` | TEXT/REAL | ผล EfficientNet | §3.3 DL classification |

### Phenotyper traits (12 ตัว — classical CV จาก `phenotyper.py`)
| Field | ความหมาย | endpoint |
|---|---|---|
| `green_coverage_pct` | % พื้นที่เขียว = projected leaf area | **PRIMARY** §3.4 → growth curve |
| `vigor_score` | คะแนนรวม 0–10 (rule-based) | Secondary; §4.6 re-derive แบบ data-driven |
| `brown_coverage_pct` | % น้ำตาล (necrosis) | Secondary |
| `leaf_color_index` | G/R ratio | Secondary (chlorophyll proxy) |
| `shoot_count_cv` | จำนวนยอดประมาณ | Secondary |
| `texture_entropy` | Shannon entropy | morphology |
| `media_color_cv` | สีอาหาร | proxy ปนเปื้อน |
| `convex_hull_ratio` | solidity (ทรงกระจุก/กระจาย) | **ใหม่ 2026-06-12** — shoot architecture |
| `exg_mean` | Excess Green (threshold-free) | **ใหม่** — chlorophyll proxy ทนแสง |
| `vari_mean` | VARI vegetation index | **ใหม่** — chlorophyll proxy |
| `glcm_contrast` | GLCM พื้นผิวหยาบ | **ใหม่** — texture ละเอียดกว่า entropy |
| `glcm_homogeneity` | GLCM พื้นผิวเรียบ | **ใหม่** — texture |
| `phenotype_method` | classic_cv / yolov8_seg | provenance |

### Manual growth fields (กรอกมือ — optional)
`shoot_count`, `shoot_height_class`, `root_density`, `callus_present`, `media_color`

---

## 3. Endpoint → Data mapping (มุมกลับ: คำถามวิจัยแต่ละข้อใช้ข้อมูลอะไร + ครบไหม)

| Endpoint / Hypothesis (Methods §) | ข้อมูลที่ต้องใช้ | สถานะ |
|---|---|---|
| **§5.1 Growth curve/ขวด (Gompertz)** | green% time-series ต่อ bottle_id + day_point | ✅ ครบ |
| **§5.3 เทียบ 5 สูตร** | per-bottle growth params + media_formula + batch_id | ✅ ครบ (params คำนวณตอน analysis) |
| **§5.4 Reproducibility (formula×batch)** | batch_id ในทั้ง bottles+images | ✅ ครบ |
| **§5.6 Position confound** | shelf/row/col | ✅ ครบ |
| **§3.4 Secondary endpoints** | vigor/brown/LCI/shoot + 5 traits ใหม่ | ✅ ครบ (wire DB แล้ว) |
| **§5.5 Contamination survival** | status + day_point (derive time-to-contam) | ⚠️ derive ได้ แต่ไม่มี field "วันเริ่มปนเปื้อน" ตรงๆ |
| **§3.6 Hyperhydricity rate** | hyperhydricity flag | ⚠️ column มี แต่ capture UI ยังไม่ wire |
| **§4.1–4.4 Convergent validity (CV vs expert)** | expert vigor 1–5 (≥2 raters) ต่อภาพ | ❌ **ไม่มีที่เก็บ** |
| **§4.6 Criterion validity (survival-to-acclimatization)** | binary survival หลังย้ายอนุบาล | ❌ **ไม่มีที่เก็บ** |
| **§2.4 Developmental stage** | label radicle/hypocotyl/cotyledon/true-leaf | ❌ **ไม่มี field** |
| **§1.3 Germination endpoint** | %germination + time-to-emergence | ❌ ไม่มี emergence date field (มีแต่ date_planted) |

---

## 4. 🔴 ช่องว่าง (GAPS) — เรียงตามความสำคัญ

> นี่คือผลลัพธ์หลักของ task นี้: ข้อมูลที่ "method ต้องใช้" แต่ "ระบบยังเก็บไม่ได้"

### GAP-1 · Expert vigor score (validation) — **สำคัญสุด**
Validation เป็น claim หลักของโปรเจกต์ (METHOD-primary) แต่ **ไม่มีที่เก็บคะแนนครู** ต้องเพิ่ม:
- ตารางใหม่ `expert_scores` (image_id, rater_id, vigor_grade 1–5, hyperhydric_flag, timestamp) — รองรับ ≥2 rater/ภาพ + consensus median
- ต้องมีก่อนเริ่ม validation study (Group C ใน decisions sheet)

### GAP-2 · Survival-to-acclimatization (criterion validity)
แกน non-circular ที่พิสูจน์ vigor_score แต่ยังไม่มี field. ต้องเพิ่มใน bottles:
- `acclim_survival` (INT 0/1/NULL), `acclim_date`, `acclim_check_date`
- ใช้ตอน harvest (ก.ย.–ต.ค.) — ไม่เร่งตอนนี้ แต่ schema ควรเผื่อ

### GAP-3 · Emergence date + germination tracking
นับวันจาก "งอก" คือ decision ที่ล็อก แต่ day_point กรอกมือ ไม่มี anchor. ควรเพิ่มใน bottles:
- `sow_date`, `emergence_date` → ให้ระบบคำนวณ day-from-emergence อัตโนมัติ + ได้ germination% / time-to-emergence ฟรี

### GAP-4 · Developmental stage label (§2.4)
ไม่มี field. เพิ่มใน images: `dev_stage` (TEXT: radicle/hypocotyl/cotyledon/true_leaf/abnormal)

### GAP-5 · Hyperhydric capture UI (§3.6)
column `hyperhydricity` + `add_image()` รองรับแล้ว แต่ **ต้องเช็คว่าฟอร์มถ่าย/scanner ส่งค่าเข้ามาจริงไหม** — ถ้ายัง ต้องเพิ่ม checkbox ในหน้า capture (งานเล็ก)

### GAP-6 · Contamination onset (เสริม)
derive จาก first status=contaminated ได้ แต่ถ้าอยากแม่น ควรมี `contam_onset_day` ที่ confirm. — priority ต่ำ (derive พอใช้)

---

## 5. สรุปสำหรับวางแผน

- **ข้อมูล growth + biological comparison (พระเอกฝั่งชีววิทยา): ครบแล้ว** ✅ — เก็บภาพแล้ว run analysis ได้เลย
- **ข้อมูล validation (พระเอกฝั่ง method): ยังขาด GAP-1, GAP-2** ❌ — ต้องเพิ่ม schema ก่อน validation study
- **GAP-3/4/5 = งาน schema + capture เล็ก** ทำใน Redesign (Phase 2) ทีเดียวได้
- **ลำดับแนะนำ:** GAP-1 (expert_scores) ทำก่อนสุดเพราะ validation คือ claim หลัก + ต้องมีก่อนครูให้คะแนน
