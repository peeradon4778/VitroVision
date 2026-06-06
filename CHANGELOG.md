# Changelog — VitroVision

บันทึกการเปลี่ยนแปลงทั้งหมดของโปรเจกต์

รูปแบบ: `[วันที่] - สิ่งที่ทำ`

---

## [2026-06-04] — Full System Test + Bug Fixes + Production Reset

### Bug Fixes (4 จุด)
- `trainer.py` — `class _DS(Dataset)` อยู่ระดับ module ก่อน lazy-load `Dataset` → ย้ายเข้าไปใน `run_training()`
- `trainer.py` — `get_preview()` ใช้ `A.Compose` โดยไม่เรียก `_ensure_heavy()` ก่อน → เพิ่ม `_ensure_heavy()` บรรทัดแรก
- `drive_uploader.py` — `local_path` ว่างถ้า Drive upload ล้มเหลว เพราะ `_save_local` อยู่ใน `upload_image()` → แยก local save ออกมาทำก่อนใน `queue_upload()` ทันที ก่อน queue Drive
- `trainer.py` — `local_path=''` ใน DB ทำให้ `Path(base_dir)/Path('')` = directory → OpenCV crash silently → training thread stuck (CPU=0) → เพิ่ม `if not path: continue` + `p.is_file()`

### Train Run (2026-06-04)
- Dataset: 181 ภาพสังเคราะห์ที่ valid (filtered empty paths)
- Config: 10+15 epochs, lr=1e-4
- **Weighted F1: 0.750** (เพิ่มจาก 0.207 → 3.6×)
- **Cohen's κ: 0.627** (ดี — จากติดลบ −0.111)
- contaminated recall: 7/9 ✅  dead recall: 8/9 ✅

### Production Reset
- ล้าง DB (431 images, batches, metadata ขวดทั้ง 100)
- ลบ `data/` ทั้งหมด (ภาพทดสอบ + test_preview/)
- เก็บ `models/final/classifier.pt` (16.4 MB) ไว้สำหรับ Active Learning ต่อ
- พร้อมถ่ายภาพจริงแล้ว ✅

---

## [2026-06-03] — Trainer Refinement + Active Learning + Pipeline Preview

### Changed / Added
- `trainer.py` — refactor ครั้งใหญ่
  - Lazy-load heavy libs (`_ensure_heavy`) ประหยัด ~9s startup time
  - Class weights คำนวณ อัตโนมัติ — แก้ imbalanced dataset
  - Train/Val/Test split อัตโนมัติ: 70/15/15 (≥30 ภาพ) หรือ 80/20
  - Phase 1 head-only → Phase 2 fine-tune ทั้งหมด (CosineAnnealingLR)
  - `_evaluate()` — confusion matrix, Cohen's κ, Weighted F1, per-class metrics
  - `get_preview(n=8)` — ส่งคู่ original/augmented กลับเป็น base64 JPEG
  - บันทึก `metrics.json` พร้อมข้อมูลครบ
- `train.html` — Training UI ครบสมบูรณ์
  - **Active Learning Loop** section — progress bar, threshold ปรับได้, badge model status
  - **Class Weights card** — visualize imbalance แบบ bar
  - **Evaluation Results card** — confusion matrix สี, per-class precision/recall/F1 bars
  - **Pipeline Preview** — grid original ↔ augmented, random ทุกกด Refresh
  - Restore จาก localStorage — ผลรันก่อนหน้าแสดงทันทีเมื่อเปิดหน้าใหม่
  - Chart.js Loss/Accuracy curve real-time (SSE streaming)
- `main.py` — เพิ่ม Active Learning routes ครบ
  - `_al_load/save/increment_and_check/auto_retrain` — auto-retrain หลัง label ถึง threshold
  - `GET /train/al_status` — คืน count, pct, last_retrain_at, model_ready
  - `POST /train/al_threshold` — ปรับ threshold ได้จาก UI
  - `GET /train/preview` — ส่ง augmentation preview จาก trainer
  - Background ML loading thread — ไม่บล็อก Flask startup
- `base.html` — เพิ่ม ML loading banner
  - poll `/api/ml_status` ทุก 2s ขณะ torch/timm กำลังโหลด → ซ่อนเมื่อพร้อม
  - เพิ่ม Glass Room link ใน nav
- `VitroVision.bat` — ใช้ `conda env ml` python โดยตรง (`miniconda3\envs\ml\python.exe`)
  - รอ server พร้อมก่อนเปิด browser (curl loop)

### Train Run (2026-06-02 23:49)
- Dataset: 180 ภาพสังเคราะห์ (`syn_xxx`) — 60 ต่อ class, balanced
- ผล: **F1=0.207, κ=−0.111** (แย่ — ภาพสังเคราะห์ไม่ represent จริง)
- บทเรียน: ต้องเก็บภาพจริงจากขวดเพาะเลี้ยงเนื้อเยื่อ ≥200 ต่อ class

---

## [2026-06-02] — Scanner AR + Growth Timeline

### Added
- `scan.html` — AR overlay scanner สำหรับ iPad/มือถือ
  - กล้อง live ส่องกราด detect ArUco หลายขวดพร้อมกัน
  - Clarity arc (%) แสดงความชัดของ marker แต่ละอัน real-time
  - Auto-save อัตโนมัติเมื่อ clarity ≥ 75% + day_point picker
  - บันทึก phenotype (green_coverage, LCI, shoot_count_cv, media_color) ทุกครั้งที่ save
  - Session log chips ด้านล่างแสดงขวดที่บันทึกไปแล้ว
- `aruco_map.py` — DICT_4X4_100 map ID 0–99 ครบ 100 ขวด + detect คืน corners
- `generate_aruco.py` — สร้าง PDF 5 หน้า (20 marker/หน้า) พร้อม bottle_id label + เส้นตัด
- `/api/scan_save` — endpoint บันทึก snapshot จาก scanner (image + ai + phenotype)
- `/api/scan_aruco` — detect ArUco จาก frame คืน bottle_id + corners + bottle info
- `/api/bottle_timeline/<bottle_id>` — time series ทุก record ต่อขวด
- Growth Timeline section ใน `bottle.html`:
  - Status timeline (scatter chart สีตาม status)
  - Green Coverage % over time
  - Leaf Color Index (G/R ratio) over time พร้อม stress interpretation
  - Shoot Count manual vs CV เปรียบเทียบ
- `VitroVision.bat` — launcher ไฟล์เดียว แทน .bat เก่า 3 ไฟล์

### Changed
- `main.py` — รวม Training routes + Active Learning + Scanner routes ครบในไฟล์เดียว

---

## [2026-05-31] — Training UI + Inference + Phenotyper

### Added
- `trainer.py` — EfficientNet-B0 Transfer Learning 2-phase
  - Phase 1: freeze backbone train classifier head
  - Phase 2: unfreeze ทั้งหมด fine-tune LR ต่ำลง 10x
  - Class weights แก้ imbalanced dataset อัตโนมัติ
  - Train/Val/Test split อัตโนมัติ (70/15/15 ถ้า ≥30 ภาพ)
  - Export confusion matrix, Cohen's κ, Weighted F1, metrics.json
- `train.html` (VitroShelf) — Training UI ใน VitroShelf เอง
  - Phase timeline + progress bar animated
  - Loss/Accuracy chart real-time (SSE streaming)
  - Active Learning Loop — auto-retrain ทุก N ภาพใหม่ที่ label
  - Evaluation panel: confusion matrix + per-class precision/recall/F1
- `inference.py` — โหลด classifier.pt + predict_bytes(), auto-reload เมื่อ model ใหม่
- `phenotyper.py` — วัด phenotype จากภาพโดยไม่ต้องมี model
  - Classic CV (HSV): green_coverage_pct, leaf_color_index, shoot_count_cv, media_color_cv
  - YOLOv8-seg: auto-upgrade เมื่อมี models/phenotype/seg.pt
- `/api/predict` — inference endpoint สำหรับ overlay capture
- `/api/phenotype` — phenotype endpoint

---

## [2026-05-27] — VitroShelf Full Features

### Added
- `database.py` — SQLite schema ครบ: bottles, images, batches
  - images: shoot_count, vigor_score, height_class, root_density, callus_present
  - images: green_coverage_pct, leaf_color_index, shoot_count_cv, media_color_cv
  - images: ai_status, ai_confidence
  - `_migrate_db()` pattern ป้องกัน schema error บน DB เดิม
- Batch/Round system — Training round vs Inference round, reset ขวด 100 ใบ
- Capture Overlay — full-screen capture UX บน mobile
  - Status picker, Vigor 1–5 พร้อม tooltip, Height 4 ปุ่ม, Root density, Callus toggle
  - หลัง save → auto-navigate ไปขวดถัดไป
- `drive_uploader.py` — background thread upload ไป Google Drive
- REST API สำหรับ VitroVision: `GET /api/bottle/<id>`, `POST /api/bottle/<id>/observation`
- Dashboard: mini shelf grid สีจริงต่อขวด, Global Day Point, IP address สำหรับมือถือ

---

## [2026-05-17] — Project Init

### Added
- สร้าง project structure เริ่มต้น
- ตั้งค่า conda environment `ml` (Python 3.11)
- ติดตั้ง ML libraries: PyTorch, scikit-learn, OpenCV, albumentations, timm, YOLOv8
- สร้าง README.md และ CHANGELOG.md
- Push ขึ้น GitHub repo ครั้งแรก
