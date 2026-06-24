# VitroVision — System Architecture Overview

> **สร้าง:** 2026-06-19 (session 6) · **อัปเดต:** ตามโค้ดเปลี่ยน
> **วัตถุประสงค์:** ภาพรวมทั้งระบบ 7 layer สำหรับอ้างอิง, polish, และ present ต่อกรรมการ YSC
> **Polish items:** 12 รายการ — ดู `_backlog.md` หัวข้อ "Architecture Polish"

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L0 — PHYSICAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ขวดแยมแก้วใส 125 mL × 100 ขวด
  5 สูตร (A=MS, B=BAP1, C=BAP5, D=BAP5+NAA0.05, E=IBA1) × 20 ขวด
  ArUco marker (DICT_4X4_100, ~3cm) ติดข้างขวดทุกใบ — ID 0–99
  Samsung Galaxy S24 FE — Pro mode, 12MP, ~18cm, WB/ISO lock, 17:00น. ทุกวัน
  ห้องเพาะเลี้ยง: 25±2°C / 16h light / LED 40–50 µmol
  ไม่มี lightbox → ชดเชยด้วย Pro mode lock + white card + ถ่ายเวลาเดิม

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L1 — DATA CAPTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [ทางหลัก] Web scanner (hands-free)
  shelf_manager/templates/scan.html
    ├── getUserMedia() → live camera preview
    ├── POST /api/scan_aruco → detect ArUco + measure clarity
    ├── clarity ≥ 75% → auto-capture
    └── POST /api/scan_save → บันทึกภาพ + metadata → DB
         FormData: bottle_id, day_point, ai_status,
                   ai_confidence, clarity, bottle_count, photo
         ⚠️ GAP-4/5: ยังขาด dev_stage + hyperhydricity

  [ทางสำรอง] CLI scanner
  vitro_vision/scanner.py
    ├── SPACE = capture, Q = quit
    └── POST → VitroShelf API (api_client.py)

  ArUco backbone (ใช้ทั้ง 2 ทาง):
    shelf_manager/aruco_map.py   marker_id (0–99) → bottle_id (S01-A-01…)
    vitro_vision/detector.py     detect_markers() + draw_markers()
    generate_aruco.py            → aruco_stickers.pdf (100 markers, พิมพ์แล้ว ✅)
    vitro_vision/config.py       ARUCO_DICT = "DICT_4X4_100"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L2 — STORAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  SQLite: vitroshelf.db  (shelf_manager/database.py)
    ├── batches       batch_id, name, sow_date, notes
    ├── bottles       bottle_id, treatment, emergence_date, species
    ├── images        image_id, bottle_id, day_point, status,
    │                 dev_stage, local_path, drive_file_id,
    │                 green_coverage_pct, ... (14 phenotype features)
    └── growth_observations
    ⚠️ GAP-1: expert_scores table ยังไม่มี (ต้องมีก่อน ส.ค.)
    ⚠️ GAP-2: survival field ใน bottles ยังไม่มี

  Google Drive: shelf_manager/drive_uploader.py
    └── sync ภาพขึ้น cloud อัตโนมัติหลัง capture

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L3 — PHENOTYPE EXTRACTION (Classical CV)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  shelf_manager/phenotyper.py → measure(image_bytes) → 14 features

  Segmentation (fallback chain):
    1. SAM2 hiera_tiny (148MB)   _sam2_plant_mask()   ← primary
    2. YOLOv8-seg (seg.pt)       _yolov8_seg()        ← fallback 1
    3. HSV green threshold       _classic_cv()         ← fallback 2

  14 Quantitative Features (คำนวณบน plant mask):
    ┌─ Color      ─┐ green_coverage_pct*  brown_coverage_pct
    │              │ leaf_color_index (G/R)  media_color_cv
    ├─ Vegetation ─┤ exg_mean (ExG = 2G-R-B)  vari_mean (VARI)
    ├─ Architecture┤ shoot_count_cv  convex_hull_ratio
    ├─ Texture    ─┤ texture_entropy  glcm_contrast  glcm_homogeneity
    └─ Composite  ─┘ vigor_score (rule-based)  phenotype_method
    (* = primary endpoint สำหรับสถิติ)

  WB correction: _white_balance_correct()
    WB_CARD_CORNER = None  ← ปิดอยู่ รอถ่าย white card จาก rig จริงก่อน

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L4 — DEEP LEARNING CLASSIFIER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Output classes: healthy / contaminated / dead

  [Web trainer — Active Learning]          [Standalone trainer]
  shelf_manager/trainer.py                 vitro_vision/trainer.py
  timm: efficientnet_b0                    timm: vit_small_patch14_dinov2
  เทรนผ่าน /train routes + SSE stream     รัน offline / batch
  Active Learning loop (_al_*)            vitro_vision/train_app.py

  Inference:
    shelf_manager/inference.py   → /api/predict (EfficientNet, web)
    vitro_vision/classifier.py   → predict(image_bgr) (DINOv2, CLI)

  Model files:
    models/final/classifier.pt       ← EfficientNet ใช้งาน
    models/checkpoints/              ← training checkpoints
    models/sam2/sam2.1_hiera_tiny.pt ← SAM2 (L3)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L5 — VLM TEACHER (Gemini, semi-supervised)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [Real-time analysis]                 [Batch pseudo-labeling]
  shelf_manager/vision_analyzer.py     vitro_vision/pseudo_labeler.py
  analyze_plant_image(bytes) → JSON    run() → ภาพ unlabeled → Gemini → CSV
  → /api/analyze_vision route          commit() → CSV → DB (update status/vigor)

  Model: gemini-3.5-flash ✅ (Auth key AQ. format, .env พร้อม)
  JSON output: status / vigor (1–5) / dev_stage / contamination_signs / notes

  Flow: ภาพ batch 1 → pseudo_labeler.run() → human review → commit → เทรน DINOv2
  Deploy: local model เท่านั้น (VLM ทำงานเฉพาะช่วง training)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L6 — FLASK WEB APP  (port 5001)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  shelf_manager/main.py  (รัน: VitroVision.bat หรือ python shelf_manager/main.py)

  Batch / Shelf:    /                     dashboard
                    /batch/new            สร้าง batch ใหม่
                    /shelf/<shelf_id>     ดูชั้นวาง
                    /bottle/<bottle_id>   รายละเอียดขวด

  Capture:          /scan                 live scanner (L1)
                    /api/scan_aruco       detect ArUco frame
                    /api/scan_save        บันทึกภาพ → DB

  Emergence:        /api/bottle/<id>/emergence   บันทึกวันงอก
                    /api/germination_stats        สถิติงอก
                    /api/suggest_day_point        คำนวณ day point

  Analysis:         /api/phenotype        รัน L3 phenotyper
                    /api/predict          รัน L4 classifier
                    /api/analyze_vision   รัน L5 Gemini

  Training:         /train                หน้า train
                    /train/start          เริ่ม train (SSE)
                    /train/stop           หยุด train
                    /train/stream         SSE log stream
                    /train/al_status      Active Learning status

  Growth / Analytics:/analytics           growth curve dashboard
                    /api/growth_data      time-series ต่อสูตร
                    /api/phenotype/series/<id>  series ต่อขวด
                    /api/bottle_timeline/<id>   timeline

  Glass detection:  /glass               real-time glass event
                    /api/glass_stream    SSE stream

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L7 — ANALYSIS & VALIDATION  (รอ data batch 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  vitro_vision/growth_validator.py   validate Gompertz curve/ขวด
  vitro_vision/batch_analyze.py      batch process ภาพย้อนหลัง
  /analytics → /api/growth_data      growth curve 5 สูตร (frontend)

  สถิติ (ยังไม่ implement — รอ data):
    Gompertz 3-param fit   scipy.optimize.curve_fit  (growth_validator)
    ART-ANOVA + ART-C      R ARTool                  (5 สูตร)
    Spearman ρ / κ / ICC   pingouin / sklearn         (validation)
    KM + log-rank          R survival                 (contamination)
  ⚠️ validation_stats.py ยังไม่มี — เขียนตอนมี data batch 1
```

---

## GAPs (สิ่งที่ขาด — จัดเรียงตาม deadline)

| # | GAP | Layer | Deadline | กระทบอะไร |
|---|---|---|---|---|
| GAP-4/5 | dev_stage + hyperhydricity ใน scan.html auto-capture | L1 | ก่อนต้นมีระยะ | ข้อมูล phenotype ไม่ครบ |
| GAP-1 | ตาราง `expert_scores` (image_id, rater_id, vigor_grade, hyperhydric_flag) | L2/L6 | ก่อน ส.ค. | ครูให้คะแนนไม่ได้ |
| GAP-2 | `acclim_survival` field ใน bottles | L2 | ตอนอนุบาล | Criterion validity |
| — | `validation_stats.py` (κ/ICC/ART-C calculators) | L7 | ก่อนวิเคราะห์ | รันสถิติไม่ได้ |

---

## Architecture Polish — 12 items pending (2026-06-19)

> พีรดนย์เขียน 12 comments หลังเห็น 7-layer map ครั้งแรก — implement ทีละ item ใน session ถัดๆ ไป

| # | Layer | รายการ | สถานะ |
|---|---|---|---|
| 1 | L0 | Physical setup guideline — rig spec / white card position | 🔲 |
| 2 | L1 | scan.html: เพิ่ม dev_stage + hyperhydricity (GAP-4/5) | 🔲 |
| 3 | L1 | C3 camera gates — Laplacian, glare, orientation, grid | 🔲 |
| 4 | L2 | ยืนยัน drive_uploader.py ทำงานจริงกับ batch 1 | 🔲 |
| 5 | L3 | WB calibration — เปิด WB_CARD_CORNER หลัง rig จริง | 🔲 |
| 6 | L3 | HSV threshold calibrate กับ rig จริง (batch 1 day 0) | 🔲 |
| 7 | L4 | train.html label fix: "EfficientNet-B0" → "DINOv2-Small" | 🔲 |
| 8 | L5 | ทดสอบ pseudo_labeler.run() จริงกับภาพ batch 1 | 🔲 |
| 9 | L6 | GAP-1: expert_scores table + routes | 🔲 |
| 10 | L6 | GAP-2: survival field ใน bottles | 🔲 |
| 11 | L7 | เขียน validation_stats.py (κ/ICC/ART-C) | 🔲 |
| 12 | L7 | sync _narrative_spine.md §3 + report_outline.md §3.8 | 🔲 |

---

*สร้างโดย Claude Sonnet 4.6 · 2026-06-19 · อัปเดตทุกครั้งที่ architecture เปลี่ยน*
