# 🧪 VitroVision — เครื่องมือ (Tools) & ผลจริง

> อัปเดต 2026-09-01 · เขียนใหม่ให้ตรงสถานะจริง (มีผลรันแล้ว)
> ทิศทางที่ลงตัว: **SAM3 = ต้นแบบ/teacher สร้าง pseudo-labels → กลั่นเป็น U-Net เล็ก** สำหรับใช้งานจริง
> ผลตัวเลขจริงอยู่ใน `docs/DEV_LOG.md` + `docs/deliverables/proposal_ysc.md`

---

## 1. เส้นทางที่ตัดสินใจ (Decision Path — ทำแล้ว)

1. Spike SAM3 text-prompted มองทะลุขวด/glare ได้ → ใช้ SAM3 เป็นต้นแบบ
2. Benchmark เทียบ SAM3 vs baseline (classical / YOLO-COCO) → SAM3 ดีที่สุด (height r=0.638)
3. แต่ SAM3 ใหญ่/ต้อง GPU → **กลั่นเป็น U-Net + MobileNetV3-Small (~3.6M params)** เทรนบนชุด greenhouse
4. ผลแบ่งส่วนดี (val_dice 0.98) แต่**การจัดกลุ่มความพร้อมด้วย feature 2D ยังจำกัด** (acc 0.653) → **สรุปว่าภาพ 2D ผ่านขวดมีข้อจำกัด → ต้องเสริมข้อมูล 3 มิติ**

## 2. เครื่องมือ & สถานะ

| | Tool | บทบาท/สถานะ |
|---|---|---|
| T1 | **SAM3 PCS** (`facebook/sam3`) | ✅ ต้นแบบ/teacher — ใช้ text prompt 5 คำ + สร้าง pseudo-labels · benchmark สูงสุด (r=0.638) |
| T2 | SAM2 / YOLO-seg / classical | ✅ baseline เปรียบเทียบ (ผลต่ำกว่า SAM3) |
| T9 | **U-Net + MobileNetV3** (smp) | ✅ **Main engine** — val_dice ≈ 0.98 · deploy บน HF Space |
| T11 | Classical HSV green threshold | ✅ baseline (เร็วแต่พลาดมาก) |

## 3. ผลจริง (Verified)

### ระดับการวัด (ฟีโนไทป์) — เทียบมอ
| โมเดล | สหสัมพันธ์ height | อัตราล้มเหลว | height MAE (cm) | R²_oof |
|---|---|---|---|---|
| **SAM3** | **r = 0.638** | **1%** | 1.15 | 0.386 |
| Classical | 0.498 | 23% | 1.28 | 0.233 |
| YOLO-COCO | 0.133 | 13% | 1.50 | −0.006 |

### ระดับแบ่งส่วนภาพ
| โมเดล | Dice |
|---|---|
| U-Net (MobileNetV3, กลั่น) | ≈ 0.98 (val) |

### ระดับจัดกลุ่มความพร้อม (classification)
| โมเดล | เกณฑ์ | accuracy | sensitivity | specificity |
|---|---|---|---|---|
| SAM3 (pilot) | height_proxy ≥ 0.275 | 0.755 | 0.917 | — |
| U-Net | height_proxy ≥ 0.20 (Youden) | 0.653 | 0.717 | 0.579 |

### ระดับพิกเซล (mIoU/Dice เทียบ ground truth) — **ยังไม่เสร็จ**
- [ ] Level A: annotate ground-truth masks ≥ 30 ภาพ → mIoU/Dice/F1 (`src/mask_metrics.py`)

## 4. ตัวแปร / เมตริก
- พรอมปต์: 5 คำ (`plant`,`leaf`,`shoot`,`stem`,`root`) — ทดสอบ prompt sensitivity
- ROI: bottle ROI (ไม่ใช่ทั้งภาพ)
- เมตริก: mIoU·Dice·F1·precision·recall (พิกเซล) · acc/confusion matrix (งานตัดสินใจ) · runtime

## 5. ข้อสรุปเชิงเกณฑ์
- **ไม่ใช่ zero-shot ชนะแล้วจบ** — สรุปจริงคือ "SAM3 pilot ดี → แต่ deploy ต้องเล็ก → กลั่น U-Net" และผลจัดกลุ่มยังจำกัด
- **ช่องว่างที่เหลือ:** ภาพ 2D ผ่านขวดไม่พอสำหรับการตัดสินใจแม่นยำ → งานต่อยอด = ข้อมูล 3 มิติ / การสอบเทียบหน่วย / validation ข้ามชนิด
