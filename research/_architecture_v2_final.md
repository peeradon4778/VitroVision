# VitroVision — Architecture v2 Final (Synthesis R1–R5)

> **สร้าง:** 2026-06-21 · Synthesize จาก Grill (Q1–Q11) + R1–R5 (10+10 sub-files)
> **อ้างอิง:** `_architecture_redesign_session.md` (grill + R1–R5 progress)
> **เทียบกับ v1:** `architecture_overview.md` (session 6, 2026-06-19)
> **กฎ:** v2 นี้ = source of truth สำหรับ implement — ถ้า v1 ขัดแย้ง ใช้ v2

---

## ⚡ CHANGE SUMMARY (v1 → v2) — อ่านก่อนดู architecture เต็ม

| Layer | เปลี่ยนอะไร | เหตุผล (R ไหน) |
|---|---|---|
| **L0** | white card → **6-patch DIY** (R/G/B/W/gray/black); เพิ่ม cross-pol option (รอเทสต์) | R4-B: white อย่างเดียวแก้ color ได้แย่สุด |
| **L1** | +`dev_stage` +`hyperhydricity` ใน FormData; +C3 camera gates (Laplacian/glare/torch/grid); ตัด CLI scanner | Q5+GAP-4/5; R2; Q2 |
| **L2** | +`expert_scores` table; +`survival` field; ตัด `/glass` routes | GAP-1/2; Q4 |
| **L3 NEW** | แยก Color Correction เป็น layer เดิม: **glare mask → flat-field → CCM (PlantCV 3×3)** ก่อนทุกอย่าง | R4-C: CCM ต้องมาก่อน index เสมอ |
| **L4** | segmenter: SAM2-tiny → **MobileSAM + box-prompt (YOLOv8n)** + GroundingDINO offline; add instance seg 3-class (leaf/shoot/stem) | R2: SAM2-tiny หนักเกิน CPU |
| **L5** | feature set: +NGRDI🥇/CIVE/ExG-ExR/LBP; +specular_fraction; +shoots/explant; ตัด perimeter; scale cm² (ArUco) | R1/R3: NGRDI ชนะ ExG; R3: perimeter ICC=0.27 |
| **L6** | API async: local phenotype ก่อน → background Gemini → update DB; VLM = qualitative เท่านั้น (vigor description ไม่ใช่เลข) | Q7/Q8/Q9; R1: VLM ห้ามออกเลข |
| **L7 NEW** | เพิ่ม Analysis/Validation layer: `validation_stats.py` (ICC/QWK/ART-C/Gompertz/KM) | Q11/R5 |

**ข้อห้ามใหม่ที่ต้องจำ:**
- ❌ plain Polynomial CCM → ใช้ Linear/Affine หรือ RPCC เท่านั้น
- ❌ inpaint glare → MASK-OUT เก็บ specular_fraction
- ❌ SAM2 everything-mode → box-prompt (YOLOv8 box → SAM)
- ❌ VLM ออกตัวเลข vigor → qualitative description เท่านั้น
- ❌ Dunn's post-hoc → ART-C
- ❌ pool ข้อมูล old engine กับ new engine → re-validate ทั้งหมด (bridge study)

---

## 🏗️ ARCHITECTURE V2 — FULL

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L0 — PHYSICAL  (rig + protocol)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ขวดแยมแก้วใส 125 mL × 100 ขวด
  5 สูตร (A=MS, B=BAP1, C=BAP5, D=BAP5+NAA0.05, E=IBA1) × 20 ขวด
  ArUco DICT_4X4_100 ~3cm ติดข้าง → scale reference (cm²/mm)

  กล้อง: Samsung Galaxy S24 FE (50MP ISOCELL GN3, f/1.8 OIS, ถ่าย 12MP)
         Pro mode: WB ~4000K / ISO 50 / SS lock — ล็อกครั้งเดียวใน Samsung Camera
         ระยะ ~18cm คงที่ · 17:00น. ทุกวัน · เก็บ sow_date + emergence_date

  แสง: [v2 — รอผล day 0 test ก่อนเคาะ A5.1]
    Option A (pending): Cross-pol filter + LED panel high-CRI + diffuser
                        → ตัด specular reflection บนขวด/ใบ ← แนะนำถ้า glare รุนแรง
    Option B (fallback): Diffuse light-tent + ambient แสงตู้เพาะ
                         → ง่ายกว่า CP ไม่เสียแสง 1.5-2 stops

  Color target ในเฟรม [v2 — เปลี่ยนจาก white card เดี่ยว]:
    DIY 6-patch: White (ขาว) · Mid-gray 18% · Red · Green · Blue · Black
    วางทุกภาพ ใกล้ขวด เอียงเลี่ยงแสงสะท้อน
    ⚠️ characterize ค่าจริงที่พิมพ์ได้ก่อน (Cugmas 2025: DIY ΔE ~4.28)

  ห้องเพาะเลี้ยง: 25±2°C / 16h light / 8h dark / LED 40–50 µmol/m²/s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L1 — DATA CAPTURE  (scan.html web scanner)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  shelf_manager/templates/scan.html

  Camera gates (C3 — ก่อน auto-capture) [v2]:
    ✅ ArUco clarity ≥ 75%     (มีแล้ว)
    ⬜ Laplacian sharpness gate (patch-based, threshold ~100–200)   ← เพิ่ม
    ⬜ Glare detection gate     (HSV V สูง + S ต่ำ → % ไม่เกิน threshold)  ← เพิ่ม
    ⬜ torch auto-on            (เปิดไฟมือถือเพิ่มแสงอัตโนมัติ)   ← เพิ่ม
    ⬜ Grid overlay             (ช่วย center ขวด)                  ← เพิ่ม

  FormData ส่ง /api/scan_save [v2 — เพิ่ม 2 fields]:
    bottle_id · day_point · ai_status · ai_confidence · clarity · photo
    ✅ dev_stage    (GAP-4: radicle / hypocotyl / cotyledon / true_leaf)  ← done 2026-06-21
    ✅ hyperhydricity (GAP-5: bool checkbox)                              ← done 2026-06-21

  ArUco backbone (ไม่เปลี่ยน):
    shelf_manager/aruco_map.py   · vitro_vision/detector.py
    generate_aruco.py → aruco_stickers.pdf (พิมพ์แล้ว ✅)

  ❌ ตัดออก: vitro_vision/scanner.py (CLI scanner — Q2 ไม่เคยเปิดใช้)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L2 — STORAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SQLite: vitroshelf.db  (shelf_manager/database.py)

  ✅ มีแล้ว:
    batches       (batch_id, name, sow_date, emergence_date, notes)
    bottles       (bottle_id, treatment, emergence_date, ...)
    images        (image_id, bottle_id, day_point, dev_stage,
                   local_path, drive_file_id, 14 phenotype features)
    growth_observations

  ✅ GAP-1 (done 2026-06-21):
    expert_scores (image_id, rater_id, vigor_grade 1–5,
                   hyperhydric_flag, dev_stage_check, ts)
    ← รองรับ ≥2 rater + consensus median

  ⬜ ต้องเพิ่ม (GAP-2):
    bottles: +acclim_survival BOOL, +acclim_date DATE, +survival_check_date DATE

  Google Drive: backup-only (Q3 — degrade gracefully ไม่ block scan)
  ✅ ตัดออกแล้ว: /glass · /api/glass_stream routes (Q4) — done 2026-06-21

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L3 — COLOR CORRECTION  (NEW explicit layer — v2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  shelf_manager/phenotyper.py  (เพิ่ม pipeline stages)

  ลำดับบังคับ (ห้ามสลับ):
    [1] Glare mask        HSV adaptive threshold (V สูง + S ต่ำ) → binary mask
                          → MASK-OUT (ไม่ใช่ inpaint); เก็บ specular_fraction
    [2] Flat-field        หาร flat frame ที่ถ่ายครั้งเดียวสำหรับ rig
                          → แก้ non-uniform illumination กลางเฟรม–ขอบ
    [3] CCM (affine 3×3)  PlantCV: detect_color_card → get_color_matrix
                          → affine_color_correction(rgb_img, color_chip_size)
                          หรือ pcv.transform.auto_correct_color()
                          ← ต้องทำก่อน ExG / NGRDI / VARI ทุกครั้ง
    [4] → เข้า L4 segmentation

  ⚠️ WB_CARD_CORNER: เปิดหลังถ่าย calibration set จาก 6-patch rig จริง
  ⚠️ อย่า double-correct: flat-field แก้ non-uniform; CCM แก้ global color cast
     ถ้าใช้ทั้งคู่ ต้องแยก purpose ชัดเจน

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L4 — SEGMENTATION  (v2 — เปลี่ยน engine)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  shelf_manager/phenotyper.py  +  vitro_vision/detector.py

  v2 chain (เปลี่ยนจาก SAM2-tiny everything-mode):

    [Production]  YOLOv8n-seg  →  MobileSAM box-prompt
                  YOLOv8n detects bbox → MobileSAM segments per prompt
                  instance seg 3-class: leaf / shoot / stem
                  ← CPU-capable (R2: SAM2-tiny หนักเกิน 8GB RAM)

    [Pre-annotation offline]  GroundingDINO → zero-shot bounding boxes
                  → ใช้สร้าง training data สำหรับ YOLOv8n-seg fine-tune
                  ← รัน offline ครั้งเดียว ไม่ใช่ production

    [Fallback]    HSV green threshold (classic) ← ถ้า GPU/model ไม่ available

  ArUco → scale:
    measure marker_side_px ต่อภาพ → px/cm ratio → area_cm² / height_mm
    ← Q6: เพิ่ม scale reference แทนการรายงานหน่วย pixel

  ⚠️ Bridge study ต้องทำก่อน collect validation data:
     run HSV + run MobileSAM บน n≥30 ขวดชุดเดียวกัน → Bland-Altman per feature
     → freeze pipeline → re-compute κ/ICC บน engine ใหม่

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L5 — FEATURE EXTRACTION  (quantitative classical CV)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  shelf_manager/phenotyper.py → measure() → 16+ features

  ┌─ Color indices (after CCM — บังคับ) ─────────────────────────┐
  │  green_coverage_pct *   ← primary endpoint สำหรับสถิติ       │
  │  NGRDI = (G-R)/(G+R) 🥇 ← เพิ่ม v2, sensitive กว่า ExG      │
  │  ExG = 2G-R-B           ← คง                                  │
  │  ExR = 1.4R-G                                                  │
  │  CIVE (color index vegetation extraction) ← เพิ่ม v2          │
  │  VARI = (G-R)/(G+R-B)                                         │
  │  LCI (leaf color index)  ← คง                                  │
  │  brown_coverage_pct      ← คง                                  │
  ├─ Texture (mask erosion + interior-only บังคับ) ───────────────┤
  │  GLCM contrast/homogeneity/correlation (discretize 32-64 bins)│
  │  LBP (Local Binary Patterns) ← เพิ่ว v2                       │
  ├─ Architecture ────────────────────────────────────────────────┤
  │  shoot_count / explant 🆕  ← จาก instance seg (ปลดล็อกโดย L4)│
  │  plant_area_cm²            ← ArUco scale (v2)                  │
  │  convex_hull_ratio          ← คง                               │
  ├─ Glare / quality ─────────────────────────────────────────────┤
  │  specular_fraction 🆕  ← glare mask area / total (HH marker)  │
  └─ ตัดออก: perimeter (ICC=0.27 R3 — unreliable ห้ามใช้) ────────┘

  (* ทุก index ต้องคำนวณหลัง CCM เสมอ — ห้ามใช้ raw RGB)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L6 — AI CLASSIFICATION  (qualitative — async)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Output: 3-class healthy / contaminated / dead (EfficientNet → DINOv2)
  + vigor_description / dev_stage (Gemini VLM — qualitative)

  [Local DL classifier]
  shelf_manager/inference.py   → /api/predict
  timm: efficientnet_b0 (baseline) → upgrade DINOv2 เมื่อมี labeled data

  [Gemini VLM — async API, Q7/Q8/Q9]
  shelf_manager/vision_analyzer.py → analyze_plant_image()
  gemini-3.5-flash · async call background (ไม่ block scan flow)
  JSON output:
    status: "healthy" | "contaminated" | "dead"     ← qualitative (Q9)
    vigor_description: string (ไม่ใช่ตัวเลข 1–5)   ← ห้าม VLM ออกเลข
    dev_stage: "radicle" | "hypocotyl" | "cotyledon" | "true_leaf"
    contamination_signs: string
    hyperhydric_flag: bool (ถ้าเห็น glassy/waterlogged)
  Flow: capture → phenotype local L3-L5 → save DB → POST Gemini BG → update DB

  [Pseudo-labeling loop — training only]
  vitro_vision/pseudo_labeler.py
  → Gemini teacher → human review → commit → train DINOv2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L7 — ANALYSIS & VALIDATION  (NEW — Q11 ปลดล็อก)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  vitro_vision/validation_stats.py  (ต้องเขียนใหม่)

  Module 1 — Inter-rater Reliability:
    icc_21(ratings_matrix)       → ICC(2,1) absolute agreement + 95%CI
    qwk(r1, r2)                  → Quadratic-weighted κ
    cohen_kappa_binary(r1, r2)   → Cohen's κ สำหรับ hyperhydric flag
    krippendorff_alpha(ratings)  → สำหรับ rater ≥ 3

  Module 2 — CV vs Expert Validation:
    spearman_ci(green_pct, vigor) → ρ + 95% CI bootstrap
    bland_altman(green_pct, vigor_pct_normalized)  → bias + LoA

  Module 3 — Treatment Comparison:
    art_anova(df, formula)       → ART-ANOVA (artool R bridge หรือ scipy)
    art_c_posthoc(art_result)    → ART-C contrast test
    epsilon_squared(art_result)  → ε²p effect size (ไม่ใช่ η²)

  Module 4 — Growth Curve:
    fit_gompertz(days, green_pct) → K, k, tm, R²adj per bottle
    extract_traits(params)        → AGRmax, AUC, early_vigor, lag_period
    lmm_compare(params_df)        → LMM treatment comparison on K/k/tm
    [key ref: Depetris 2025 — in vitro Lolium green coverage RGB (ใกล้ VitroVision สุด)]

  Module 5 — Survival / Contamination:
    contamination_decision(events_n) → route ไป test ที่ถูก
    km_permutation(time, event, group) → KM + permutation log-rank
    cif_analysis(time, event_type)    → cumulative incidence ถ้า competing

  Threshold pass/fail (ดู R5_validation_stats.md):
    ICC(2,1) human IRR ≥ 0.75 (Good)
    QWK vigor-rubric ≥ 0.61 (Substantial)
    Spearman ρ CV vs expert ≥ 0.80
    ICC repeatability ≥ 0.75

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  INFRASTRUCTURE — Flask Web App  (port 5001)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  shelf_manager/main.py  (รัน: VitroVision.bat)
  [ไม่เปลี่ยนโครงสร้าง routes หลัก — ดู v1 สำหรับ route list]
  เพิ่ม Phase A (ก.ค.): manifest.json (PWA), rate-of-change column
  ตัด: /glass · /api/glass_stream (Q4)
```

---

## 📋 IMPLEMENTATION TASKS (จาก Synthesize)

### 🔴 Priority 1 — ก่อน/ระหว่าง batch 1 (ทำทันที)

| # | Task | ไฟล์ที่แก้ | ความซับซ้อน |
|---|---|---|---|
| **T1** | **Bridge study script** — run HSV + MobileSAM บน n≥30 ขวด → Bland-Altman per feature | `vitro_vision/validation_stats.py` (Module 2) | M |
| ✅ **T2** | **GAP-1 expert_scores table** — สร้าง table + routes `/api/expert_score` + UI ใน bottle.html | done 2026-06-21 | M |
| ✅ **T3** | **GAP-4 dev_stage + GAP-5 hyperhydricity** ใน scan.html FormData → DB | done 2026-06-21 | S |
| **T4** | **6-patch color target** — characterize DIY target ค่าจริง + เปิด WB_CARD_CORNER + test CCM | `phenotyper.py` (_white_balance_correct) | S |
| ✅ **T5** | **Glare mask pipeline** — HSV adaptive V high+S low → specular_fraction เป็น feature | done 2026-06-21 | S |
| **T6** | **ทักครู ≥2 คน** — เป็น rater (lead time นาน) | — | — |

### 🟡 Priority 2 — ก.ค. (ระหว่างต้นโต — ทำชิลๆ)

| # | Task | ไฟล์ที่แก้ | ความซับซ้อน |
|---|---|---|---|
| ✅ **T7** | **NGRDI + CIVE** — เพิ่มใน feature set + DB + analytics API | done 2026-06-21 | S |
| **T8** | **shoots/explant** จาก instance seg (ต้องมี YOLOv8n-seg ก่อน) | `phenotyper.py` | L |
| **T9** | **ArUco scale px→cm** — คำนวณ px/cm ratio ต่อภาพ → area_cm²/height_mm | `aruco_map.py` + `phenotyper.py` | M |
| **T10** | **C3 camera gates** — Laplacian sharpness, glare, torch, grid ใน scan.html | `scan.html` | M |
| **T11** | **Flat-field correction** — ถ่าย flat frame ของ rig → divide ใน pipeline | `phenotyper.py` | S |
| **T12** | **Gemini async flow** — Gemini call เป็น background job (ไม่ block scan) | `main.py` + `vision_analyzer.py` | M |
| **T13** | **validation_stats.py Module 1+2** — ICC/QWK/Spearman/Bland-Altman | `vitro_vision/validation_stats.py` | M |
| **T14** | **Web App Phase A** — manifest.json PWA + rate-of-change column dashboard | `main.py` + `templates/` | S |
| ✅ **T15** | **ตัด glass routes** (`/glass`, `/api/glass_stream`, `/api/glass_state`) | done 2026-06-21 | S |

### 🟢 Priority 3 — ส.ค.–ต.ค. (หลังมีข้อมูล)

| # | Task | ไฟล์ที่แก้ | ความซับซ้อน |
|---|---|---|---|
| **T16** | **validation_stats.py Module 3** — ART-ANOVA + ART-C + ε²p | `validation_stats.py` | L |
| **T17** | **validation_stats.py Module 4** — Gompertz NLS per bottle + LMM | `validation_stats.py` | L |
| **T18** | **validation_stats.py Module 5** — KM + permutation log-rank + CIF | `validation_stats.py` | M |
| **T19** | **GAP-2 survival** field ใน bottles — ใส่วันอนุบาล | `database.py` + `main.py` | S |
| **T20** | **MobileSAM + YOLOv8n-seg fine-tune** บนภาพ batch 1 (ต้องมี labeled data) | `vitro_vision/` | XL |
| **T21** | **DINOv2 upgrade** classifier หลัง pseudo-label + human review | `vitro_vision/trainer.py` | L |
| **T22** | **sync narrative + report_outline** §3 ให้ตรง v2 (SAM2→MobileSAM, VLM=qualitative) | `_narrative_spine.md` + `report_outline.md` | M |

---

## 🔗 DECISION LOG (Q11 ปลดล็อก — สรุปทุก decision)

| Q | Decision | status |
|---|---|---|
| Q1 | API = qualitative; classical CV = quantitative (stats) | ✅ รอยืนยัน day 0 |
| Q2 | ตัด CLI scanner | ✅ locked |
| Q3 | Drive backup-only | ✅ locked |
| Q4 | ตัด glass detection | ✅ locked |
| Q5 | Pro mode manual Samsung Camera | ✅ locked |
| Q6 | ArUco → scale cm (เพิ่ม) | ✅ locked |
| Q7 | Gemini API async (ไม่ block scan) | ✅ locked |
| Q8 | SAM = local seg / API = cloud classify | ✅ locked |
| Q9 | classical = quantitative / API = qualitative | ✅ locked |
| Q10 | WB: 2-layer + 6-patch (R4 ยืนยัน) | ✅ locked |
| Q11 | L7 stats: ART + Gompertz + KM/CIF | ✅ **ปลดล็อก R5** |
| A5.1 | cross-pol vs diffuse light-tent | ⏳ **รอเทสต์ day 0** |
| A3 | HSV threshold calibration | ⏳ รอภาพ rig จริง |

---

*สร้าง: 2026-06-21 | Synthesize R1–R5 ครบ | ต่อไป: implement T1–T6 (Priority 1)*
