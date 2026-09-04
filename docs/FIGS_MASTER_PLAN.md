# 🖼 Master Plan: ภาพประกอบข้อเสนอ VitroVision (ภาพเยอะแทน text)

> สร้าง 2026-09 · ใช้คู่ `proposal_ysc.md` + `METHODOLOGY_FLOWCHART_TICKETS.md`
> หลักการ: งาน Tech → **ทุกหัวข้อสำคัญมีภาพกำกับ 1 ภาพ** · text ลดลง 30–50% · แต่ละรูป = 1 message ใหญ่

---

## 📋 ตาราง "ภาพใดแทนหัวข้อใด" (อ่านได้เลย)

| # | ชื่อภาพ (ไฟล์) | หัวข้อในข้อเสนอ | แทนย่อหน้าอะไร | สิ่งที่ต้องเห็นในภาพ |
|---|---------------|----------------|---------------|---------------------|
| **F1** | `fig_system_overview.png` | มาตรา 5.1 ภาพรวม | 5 ขั้นตอนบรรยาย | ถ่ายภาพ→ROI→segment(U-Net)→feature 6 กลุ่ม→verdict |
| **F2** | `fig_unet_architecture.png` | มาตรา 5.3 สถาปัตยกรรม | คำอธิบาย encoder/decoder | MobileNetV3 encoder ↔ U-Net decoder + **skip connections (เส้นประ)** + output mask |
| **F3** | `fig_data_pipeline.png` | มาตรา 5.2–5.3 ข้อมูล & ฝึก | เก็บ/เทรน/ทดสอบ | greenhouse→split 85/15→SAM3 pseudo-label→U-Net→test 98 ขวด |
| **F4** | `fig_validation_levels.png` | มาตรา 5.5 ตรวจสอบ | 3 ระดับการตรวจ | pixel / image / inter-rater / cross-species |
| **F5** | `fig_verdict_threshold.png` | มาตรา 6 วิเคราะห์ | เกณฑ์ + ผล verdict | threshold 0.20 → acc/sens/spec + confusion |
| **F6** | `fig_results.png` | มาตรา 6 ผล | ค่า metric ต่างๆ | mIoU/Dice bar, correlation scatter, error bar |

---

## 🧩 รายละเอียดแต่ละภาพ (ให้วาด / วาง Draw.io)

### F1 — System Overview
```
[ถ่ายภาพขวด] → [ตรวจจับ ROI ขวด] → [Segment ต้น (U-Net)] → [คำนวณ feature 6 กลุ่ม] → [Verdict]
                             ↘ ภาพไม่ชัด (glare/ฝ้า) → [ส่งมนุษย์ตรวจ]
```
- สี: ฟ้า = กระบวนการ · ส้ม = output · เทา = error path

### F2 — U-Net Architecture (หัวใจ)
```
Image 256×256×3
  │
  ▼
ENCODER: MobileNetV3-Small (ImageNet weights)
 [B1][B2][B3][B4]  ──(skip connection, เส้นประ)──▶
  ▼
DECODER: U-Net
 [Up1][Up2][Up3][Up4]  ← concat skip
  ▼
Output: 1×1 conv + sigmoid → binary mask 256×256
```
- ระบุ: ~3.6M params · val_dice ≈ 0.98 · กลั่นจาก SAM3

### F3 — Data & Training Pipeline
```
[greenhouse 1,200 ภาพ] → split 85/15 → train/aug + val
                                     │
[SAM3 teacher] → pseudo-labels ──────┘
                                     ▼
                              [U-Net best (dice 0.98)]
                                     ▼
[ขวดจริง 98 ภาพ unseen] → test → mask+feature → verdict
```
- เน้น: ชุดเทรน ≠ ชุดเทสต์ (unseen)

### F4 — Validation Levels
```
[Model mask] ──┬─ A. Pixel: mIoU/Dice/F1/P/R ──▶ vs ground_truth_masks (≥30)
               ├─ B. ค่าวัด: r/MAE/RMSE ──────▶ vs ground_truth.csv
               ├─ C. Verdict: acc/sens/spec/MCC/kappa ──▶ vs expert
               └─ inter-rater: ICC/Cohen's kappa ──▶ (2 คน blind)
```

### F5 — Verdict Threshold
```
height_proxy สแกน 0.12–0.55 → เลือก Youden-balanced = 0.20
→ acc 0.653 · sens 0.717 · spec 0.579
→ multi-trait logistic AUC 0.639 (ไม่ดีกว่า single → หนุน 3D)
```

### F6 — Results
- Bar chart: mIoU/Dice เทียบวิธีพื้นฐาน (SAM2/YOLO-seg/classical)
- Scatter: height_proxy vs expert height (Pearson r)
- Error bar / box: verdict fee (พร้อม/ไม่พร้อม)

---

## 🎯 กฎการวาดภาพ (ให้เอกสารอ่านง่ายจริง)
1. **1 ภาพ = 1 message** อย่ายัดเยียดหลายเรื่องในรูปเดียว
2. **ภาพก่อน text** — เติมข้อความเฉพาะที่จำเป็น
3. **ใช้ icon/ลูกศร/สี** แทน sentence ยาว
4. **ใช้ตาราง** แทนย่อหน้าบรรยาย (metric, วัสดุ, สถานที่)
5. **label ภาษาอังกฤษ** ชัดเจน (กันฟอนต์ไทยเพี้ยน)
6. **ชื่อไฟล์คงที่** เพื่อให้ `proposal_ysc.md` อ้าง path ได้ตรง

---

## 📌 สิ่งที่ต้องทำ (อ้างอิง ticket)
- วาด 6 ภาพ (F1–F6) บน Draw.io
- อัปเดต link ใน `proposal_ysc.md` (ทุกที่อ้าง `docs/assets/...`)
- **commit + push** ทั้งภาพ + ข้อเสนอ
