# VitroVision Research Docs Auto-Sync Prompt

คุณคือ Claude ทำงานใน GitHub Actions CI ตี 4 ICT
โปรเจกต์: VitroVision — Computer Vision สำหรับ Capsicum annuum in vitro tissue culture

## สถาปัตยกรรมปัจจุบัน (source of truth)

ก่อนทำงาน อ่าน `shelf_manager/phenotyper.py` บรรทัด 1-35 และ `vitro_vision/classifier.py`
บรรทัด 1-45 เพื่อยืนยัน engine จริงที่ deploy อยู่ แล้วใช้ค่าที่อ่านได้จากโค้ดจริงเป็น
source of truth ทั้งหมด

## Fallback ถ้าอ่านไม่ได้

สถาปัตยกรรม ณ วันที่ตั้ง cron (2026-06-18):

```
ภาพขวด TC → SAM2 point-prompt (primary) → mask → 14 Classical CV features
Fallback chain: YOLOv8-seg > SAM2+CV > Classic HSV
Classifier: EfficientNet-B0 (legacy — Phase B จะ swap → DINOv2)
```

14 features: green_coverage_pct, leaf_color_index, shoot_count_cv, media_color_cv,
texture_entropy, brown_coverage_pct, vigor_score, convex_hull_ratio, exg_mean,
vari_mean, glcm_contrast, glcm_homogeneity, method (tag)

## ไฟล์ที่ต้องอัปเดต

อัปเดตเฉพาะส่วนที่ล้าสมัย ห้ามเขียนทับเนื้อหาที่ยังถูกต้อง

### 1. research/04_final_architecture_ux_plan.md
- แก้ทุกที่ที่บอก "7 features" → จำนวน features จริงจากโค้ด
- แก้ทุกที่ที่บอก segmentation เป็น HSV → SAM2 point-prompt
- เพิ่ม note "Phase A เสร็จแล้ว" ถ้ายังไม่มี

### 2. research/14_image_dl_phenotyping.md
- อัปเดต "Mapping กับ N features ปัจจุบัน" ให้ตรงกับ features จากโค้ด
- เพิ่มแถว SAM2 ใน mapping table ถ้ายังไม่มี

### 3. research/10_methods_draft.md
- ใน section Image Processing/Segmentation เพิ่มคำอธิบาย SAM2 point-prompt
  (fg: upper-center plant zone, bg: lower media + corner) พร้อม cite Ravi 2024
- แทนที่คำอธิบาย HSV-only ด้วย "SAM2 primary, HSV fallback"

### 4. research/_narrative_spine.md
- อัปเดต section "เครื่องมือทำอะไร" ให้สะท้อน SAM2 เป็น segmentation engine
- frame: "SAM2 foundation model → classical CV feature extraction"

### 5. research/_data_dictionary.md
- อัปเดต "Phenotyper traits" source column: "HSV threshold" → "SAM2+CV"
- เพิ่มแถว features ใหม่ที่ยังไม่มี (convex_hull_ratio, exg_mean, vari_mean,
  glcm_contrast, glcm_homogeneity)

### 6. research/_citation_audit.md
- เพิ่ม citations ต่อไปนี้ถ้ายังไม่มี (ผ่าน gate แล้ว — มี URL จริง):
  - Ravi et al. 2024, SAM 2, ArXiv
    URL: https://consensus.app/papers/details/31972e1fad1953e78d9d32908e51ff23/
  - Bao et al. 2025, Zero-Shot Instance Segmentation for Plant Phenotyping, Front Plant Sci
    URL: https://consensus.app/papers/details/86cfd544ceb55be0b83c171e98d0e997/
  - Zhang et al. 2024, Adapting SAM for Plant Recognition, Horticulturae
    URL: https://consensus.app/papers/details/8894e0b9a4ef584693f8437041494881/

## กฎสำคัญ

- ห้าม git add / commit / push — GitHub Actions จัดการเอง
- ห้ามแก้ไฟล์นอก research/ และ research/ เท่านั้น
- ถ้าไฟล์ใดมี note "อัปเดต 2026-06-18" หรือกล่าวถึง SAM2 ถูกต้องแล้ว ให้ข้ามไฟล์นั้น
- ห้าม hallucinate citation — ใช้เฉพาะ URL ที่ระบุข้างบน
- จบงานด้วยการสรุปสั้น: อัปเดตกี่ไฟล์ + state ที่อ่านได้จาก phenotyper.py
