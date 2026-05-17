# 🌱 VitroVision

> Computer Vision สำหรับพืชเพาะเลี้ยงเนื้อเยื่อในขวด (In Vitro Tissue Culture)

## 📌 Overview

โปรเจกต์นี้ใช้ Machine Learning และ Image Processing วิเคราะห์ภาพพืชที่เพาะเลี้ยงเนื้อเยื่ออยู่ในขวด เพื่อช่วยในการประเมินคุณภาพและการเจริญเติบโตของพืช

## 🎯 Objectives

- [ ] รวบรวม dataset ภาพพืชเพาะเลี้ยงเนื้อเยื่อ
- [ ] พัฒนา image preprocessing pipeline
- [ ] Train classification model ด้วย Transfer Learning
- [ ] Evaluate และ deploy model

## 🛠️ Tech Stack

| ส่วน | เทคโนโลยี |
|-----|----------|
| Language | Python 3.11 |
| ML Framework | PyTorch + timm |
| CV | OpenCV, albumentations |
| Detection | YOLOv8 (ultralytics) |
| Notebook | JupyterLab |
| Dataset | Roboflow |

## 📁 Project Structure

```
VitroVision/
├── data/
│   ├── raw/          # ภาพต้นฉบับ (ไม่ push GitHub)
│   ├── processed/    # ภาพหลัง preprocessing
│   ├── augmented/    # ภาพ augmentation (ไม่ push GitHub)
│   └── labels/       # annotation files
├── notebooks/        # Jupyter notebooks
├── src/
│   ├── data/         # dataset loaders
│   ├── models/       # model definitions
│   └── utils/        # helper functions
├── models/           # saved models (ไม่ push GitHub)
├── results/          # กราฟและรายงาน
└── config/           # config files
```

## 🚀 Getting Started

```bash
# 1. Clone repo
git clone https://github.com/peeradon4778/VitroVision.git
cd VitroVision

# 2. Activate conda environment
conda activate ml

# 3. Install dependencies
pip install -r requirements.txt

# 4. เปิด JupyterLab
jupyter lab
```

## 📊 Progress Log

ดู [CHANGELOG.md](CHANGELOG.md) สำหรับประวัติการพัฒนา

---
*Developed by Peeradon | Plant Factory Research*
