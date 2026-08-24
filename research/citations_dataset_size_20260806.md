# Dataset Size สำหรับ Segmentation — งานวิจัยหลักฐาน (2026-08-06)

> สืบค้นโดย vitro-researcher 2026-08-06 · ตรวจ title/ปี/DOI จริงทุกตัว
> บริบท: ผู้ใช้มีภาพ TC 51 ภาพ (ถ่าย 16 ก.ค. 69) — โจทย์: ถ้าไม่ใช้ zero-shot ต้องมี dataset กี่ภาพงานจึงมีน้ำหนัก

## คำตอบสั้น (จากหลักฐาน)

| วิธี | จำนวนภาพที่ควรมี | หลักฐาน |
|---|---|---|
| เทรน segmentation จากศูนย์ (scratch) | ~1,000 ภาพขึ้นไป | Prashanth WACV 2024 (1,000 ภาพ → mAP@0.5 0.648) |
| Fine-tune pretrained model | ~100–1,000 ภาพ/class | Callus YOLO (122 ภาพ → mAP50 0.855); Shahinfar (asymptote ~150–500/class, classification) |
| Fine-tune เฉพาะส่วนเล็ก (mask decoder/LoRA) | 5–20 ภาพก็ขยับได้ | Aubreville arXiv:2407.04651 (medical) |
| Zero-shot foundation model (SAM3) | ไม่ต้องเทรน | Sapkota 2025 (SAM3 vs YOLO11 fine-tuned) |

## หลักฐานสำคัญ (โดเมน TC/พืช)

1. **Egi & Öter 2026 (Plants 15(1):47)** — เทรน YOLO-seg บน **callus ถั่วเลนทิล 122 ภาพ, 3 classes, 1,185 masks** ถ่ายใน biosafety cabinet (สภาพคล้ายแล็บผู้ใช้มาก) → YOLOv8 mAP50 = **0.855** — หลักฐานตรงสุดว่า TC + ~100 ภาพ เทรนสำเร็จได้ https://doi.org/10.3390/plants15010047 · PMC12788146
2. **Prashanth 2024 (WACV)** — 1,000 ภาพ (900/100), 4,682 masks → mAP@0.5 = 0.648 https://openaccess.thecvf.com/content/WACV2024/html/Prashanth_Towards_Accurate_Disease_Segmentation_in_Plant_Images_A_Comprehensive_Dataset_WACV_2024_paper.html
3. **Alkhudaydi 2019 (Plant Phenomics)** — 90 ภาพ side-view wheat → IoU = **0.40** (ผลกลาง ๆ = ภาพ <100 เทรนตรง ๆ ไม่ดี) https://doi.org/10.34133/2019/7368761
4. **Najafian 2023 (Plant Phenomics)** — เทรนตรง ~38 ภาพ → Dice 0.51–0.64; สำเร็จที่ Dice 0.89 ต้องใช้ synthesis + 10,000 ภาพ https://doi.org/10.34133/plantphenomics.0025
5. **Laco 2024 (APL Bioeng, SAAVY)** — 3D tissue culture (spheroid) เทรน **24 ภาพ** + COCO-pretrained → ใช้ได้จริง (งานง่าย/ภาพระเบียบ หลักสิบภาพพอ) https://doi.org/10.1063/5.0189222

## Fine-tune foundation model vs zero-shot

6. **Sapkota 2025 (SAM3 vs YOLO11, arXiv:2512.11884)** — MinneApple 670 ภาพ: YOLO11m fine-tuned F1 72.2% vs SAM3 zero-shot 59.8% แต่ SAM3 **ไม่เสื่อมเมื่อ IoU เข้มงวด** (mask boundary แม่นกว่า) → เหมาะกับงานวัดพื้นที่ https://doi.org/10.48550/arXiv.2512.11884
7. **Li 2023 (ASA, Sensors 23(18):7884)** — SAM + adapter (freeze encoder), 1,100 ภาพ coffee → Dice +41.48% ดีกว่า zero-shot ทุก 12 tasks https://doi.org/10.3390/s23187884 · PMC10534855
8. **Williams 2024 (Leaf Only SAM)** — Mask R-CNN fine-tuned ดีกว่า SAM zero-shot (recall 78.7 vs 63.2) แต่ zero-shot ไม่ต้อง annotate https://doi.org/10.1016/j.atech.2024.100515 · arXiv:2305.09418
9. **Aubreville 2024 (arXiv:2407.04651)** — fine-tune เฉพาะ mask decoder ด้วย 5–20 ภาพ ใช้ได้จริง (medical) https://arxiv.org/abs/2407.04651

## ข้อแนะนำสำหรับ 51 ภาพของผู้ใช้

- **อย่าเทรนเองจากศูนย์ด้วย 51 ภาพ** — ต่ำกว่าเกณฑ์ (เสี่ยง overfit + น้ำหนักวิชาการต่ำ)
- **แผนที่ literature รองรับ:** SAM3 zero-shot เป็นแกน + few-shot fine-tune (mask decoder/LoRA) เทียบกัน 3 ทาง (zero-shot vs few-shot vs manual) → 51 ภาพกลายเป็นจุดแข็ง (scarce-data + foundation model)
- นำเสนอ 51 ภาพเป็น "แรงจูงใจใช้ foundation model" ไม่ใช่ "dataset พอเทรนเอง"
- ถ้าจะพูดว่า "กี่ภาพถึงพอ" ใช้กรอบ: scratch ~1,000 / fine-tune ~100–1,000 / few-shot 5–20 (พร้อม caveat: Shahinfar 150–500 มาจาก classification)

## ข้อจำกัด

- ไม่มี guideline "X ภาพต่อ class" ตายตัวสำหรับ segmentation พืช (Shahinfar เป็น classification)
- ยังไม่มี paper เทรน segmentation ผ่านขวดแก้ว TC (refraction) โดยตรง — Callus YOLO ถ่ายแบบเปิด cabinet → จุดนี้เป็นช่องว่างงานวิจัยของผู้ใช้เอง
