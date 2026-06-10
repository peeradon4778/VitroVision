# VitroVision

> Computational Phenotyping สำหรับ *Capsicum annuum* เพาะเลี้ยงเนื้อเยื่อในขวด

ระบบ Computer Vision วิเคราะห์ภาพขวดเพาะเลี้ยงเนื้อเยื่อ ตรวจสถานะพืช (healthy / contaminated / dead) และวัดค่า phenotype เชิงปริมาณ เพื่อเปรียบเทียบประสิทธิภาพสูตร MS 5 สูตรในการทดลองชีววิทยา

**เป้าหมาย:** Young Scientist Competition 2027 (CSBI) → ISEF

---

## ผลลัพธ์ปัจจุบัน

| Metric | ค่า |
|--------|-----|
| Weighted F1 | **0.750** |
| Cohen's κ | **0.627** (substantial agreement) |
| Dataset | 181 ภาพ (สังเคราะห์) — รอภาพจริงจาก lab |
| Model | EfficientNet-B0 (16.4 MB) |

---

## Biological Experiment

**Plant:** *Capsicum annuum* L. | **Design:** 5 สูตร MS × 20 ขวด = 100 ขวด

| สูตร | Treatment |
|------|-----------|
| A | MS (control) |
| B | MS + 1 mg/L BAP |
| C | MS + 5 mg/L BAP |
| D | MS + 5 mg/L BAP + 0.05 mg/L NAA |
| E | MS + 1 mg/L IBA |

---

## Features

**Classification (vitro_vision/)**
- EfficientNet-B0 Transfer Learning — healthy / contaminated / dead
- ArUco DICT_4X4_100 — ระบุ bottle_id อัตโนมัติจาก marker ติดข้างขวด
- Active Learning Loop — MC Dropout uncertainty sampling (`GET /api/al_query`), retrain อัตโนมัติเมื่อถึง threshold
- Experiment tracking ด้วย [wandb](https://wandb.ai/peeradon4778-pcshsbr-ac-th/vitrovision)

**Phenotyping (shelf_manager/)**
- 7 ค่า phenotype: `green_coverage_pct`, `leaf_color_index`, `shoot_count_cv`, `media_color_cv`, `texture_entropy`, `brown_coverage_pct`, `vigor_score`
- vigor_score: composite index 0–10 สำหรับเปรียบเทียบระหว่างสูตร

**Analytics Dashboard (VitroShelf web)**
- Growth curve ตามเวลาแยกตามสูตร MS
- Vigor heatmap, Status stacked bar, Scatter green vs vigor
- Statistical comparison: Kruskal-Wallis + Bonferroni Mann-Whitney U

---

## Tech Stack

| ส่วน | เทคโนโลยี |
|-----|----------|
| Language | Python 3.11 (conda env: `ml`) |
| ML | PyTorch + timm (EfficientNet-B0) |
| CV | OpenCV, albumentations |
| Explainability | pytorch-grad-cam (GradCAM++) |
| Detection | YOLOv8 (ultralytics), ArUco |
| Web App | Flask (VitroShelf), SQLite, Chart.js |
| Storage | Google Drive (auto-upload) |
| Experiment Tracking | Weights & Biases (wandb) |
| Cloud Training | Kaggle Notebooks (GPU T4) |
| Stats | scipy (Kruskal-Wallis, Mann-Whitney U) |

---

## Project Structure

```
VitroVision/
├── vitro_vision/          # ML package หลัก
│   ├── classifier.py      # predict healthy/contaminated/dead
│   ├── transforms.py      # centralized augmentation pipeline (albumentations)
│   ├── detector.py        # ArUco bottle_id detection
│   ├── scanner.py         # live camera scanner
│   └── batch_analyze.py   # วิเคราะห์ภาพย้อนหลัง
├── shelf_manager/         # VitroShelf web app
│   ├── main.py            # Flask entry point (port 5001)
│   ├── trainer.py         # EfficientNet training + wandb
│   ├── inference.py       # predict_bytes + predict_mc_dropout (MC Dropout)
│   ├── phenotyper.py      # 7-feature phenotype extraction
│   ├── database.py        # SQLite schema + migrations
│   ├── drive_uploader.py  # Google Drive background upload
│   └── templates/         # Jinja2 HTML (train, scan, analytics)
├── notebooks/
│   ├── 01_explore.ipynb
│   ├── 02_preprocess.ipynb
│   ├── 03_growth_analysis.ipynb   # Kruskal-Wallis + Bonferroni
│   ├── 04_train_kaggle.ipynb      # Kaggle GPU training
│   ├── 05_kfold_eval.ipynb        # Stratified 5-fold CV, Bootstrap CI, McNemar's test
│   └── 06_gradcam.ipynb           # GradCAM++ visualization (pytorch-grad-cam)
├── models/final/          # classifier.pt (ไม่ push GitHub)
├── results/               # กราฟ PNG, phenotype_summary.csv
├── generate_aruco.py      # PDF ArUco markers สำหรับปริ้นท์
├── _inject_mock.py        # inject mock data 500 records
├── _migrate_db.py         # DB migration script
└── VitroVision.bat        # launcher เปิดระบบทั้งหมด
```

---

## Getting Started

```bash
# 1. Clone repo
git clone https://github.com/peeradon4778/VitroVision.git
cd VitroVision

# 2. Activate conda environment (miniconda3)
conda activate ml

# 3. Install dependencies
pip install -r requirements.txt

# 4. รัน VitroShelf web app
python shelf_manager/main.py
# เปิด http://localhost:5001

# หรือใช้ launcher
VitroVision.bat
```

**รัน live scanner:**
```bash
python -m vitro_vision.scanner --day 14
```

**สร้าง ArUco PDF สำหรับปริ้นท์:**
```bash
python generate_aruco.py
# output: aruco_markers.pdf (5 หน้า, 20 marker/หน้า, ขนาด 3×3 cm)
```

---

## Objectives

- [x] Image preprocessing pipeline + dataset loaders
- [x] EfficientNet-B0 Transfer Learning (F1=0.750, κ=0.627)
- [x] ArUco bottle tracking (ID 0–99)
- [x] VitroShelf web app — capture, training UI, active learning
- [x] Phenotyper — 7 quantitative features + vigor_score
- [x] Analytics dashboard — growth curves, vigor heatmap, statistics
- [x] wandb experiment tracking
- [x] Kaggle GPU training notebook
- [x] Stratified 5-fold CV + Bootstrap CI (05_kfold_eval.ipynb) — รอภาพจริง
- [x] GradCAM++ visualization notebook (06_gradcam.ipynb)
- [ ] ภาพจริงจาก lab (เป้า 500+ ภาพ ภายใน ต.ค. 2569)
- [ ] Kappa ≥ 0.70 จากภาพจริง
- [ ] Human baseline Kappa (ครูที่ปรึกษา label 28 ภาพ)
- [ ] YSC 2027 proposal

---

## References

Wang, X. et al. (2024). Optimized tissue culture protocol for *Capsicum annuum*

Depetris, M. et al. (2025). Image-based phenotyping under aseptic conditions

ดู [CHANGELOG.md](CHANGELOG.md) สำหรับประวัติการพัฒนาทั้งหมด

---

*Peeradon Duangthong — PCSHSBR | peeradon4778@gmail.com*
