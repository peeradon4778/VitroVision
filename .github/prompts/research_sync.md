# VitroVision Research Docs Auto-Sync Prompt

คุณคือ Claude ทำงานใน GitHub Actions CI ตี 4 ICT
โปรเจกต์: VitroVision — Computer Vision สำหรับ Capsicum annuum in vitro tissue culture

## Step 1 — อ่าน source of truth จากโค้ดจริงก่อน

อ่านไฟล์เหล่านี้เพื่อรู้ state ปัจจุบันของระบบ:
- `shelf_manager/phenotyper.py` บรรทัด 1-35 → segmentation engine + feature list
- `vitro_vision/classifier.py` บรรทัด 1-45 → classification model
- `vitro_vision/trainer.py` บรรทัด 148-155 → model architecture ที่ใช้ train
- `vitro_vision/pseudo_labeler.py` บรรทัด 1-20 → VLM teacher pipeline

ใช้ค่าที่อ่านได้เป็น source of truth — ไม่ใช่ fallback ด้านล่าง

## Fallback (ถ้าอ่านโค้ดไม่ได้)

สถาปัตยกรรม ณ 2026-06-19:
```
ภาพขวด TC → SAM2 point-prompt (primary) → mask → 14 Classical CV features
Classifier: DINOv2-Small vit_small_patch14_dinov2 (img_size=224, 21.6M params)
VLM Teacher: Gemini Flash → pseudo_labeler.py → CSV → commit DB → train DINOv2
Fallback chain: YOLOv8-seg > SAM2+CV > Classic HSV
```

14 features: green_coverage_pct, leaf_color_index, shoot_count_cv, media_color_cv,
texture_entropy, brown_coverage_pct, vigor_score, convex_hull_ratio, exg_mean,
vari_mean, glcm_contrast, glcm_homogeneity, method (tag)

---

## Step 2 — อัปเดตไฟล์ที่ link กับ architecture

อัปเดตเฉพาะส่วนที่ล้าสมัย ห้ามเขียนทับเนื้อหาที่ถูกต้องอยู่แล้ว

### กลุ่ม A: Architecture & Methods (6 ไฟล์)

**research/04_final_architecture_ux_plan.md**
- แก้ "7 features" → 14 features ทุกที่
- แก้ segmentation HSV → SAM2 point-prompt
- แก้ classifier EfficientNet → DINOv2-Small
- เพิ่ม section "Phase A/B/C เสร็จแล้ว (2026-06-19)" ถ้ายังไม่มี

**research/14_image_dl_phenotyping.md**
- อัปเดต mapping table "7 features ปัจจุบัน" → 14 features
- เพิ่มแถว SAM2 segmentation layer ถ้ายังไม่มี
- อัปเดต "upgrade path" — SAM2 และ DINOv2 เสร็จแล้ว

**research/10_methods_draft.md**
- §4 Image Processing: เพิ่ม SAM2 point-prompt (fg: upper-center, bg: lower media + corner)
- cite Ravi 2024 (SAM2) สำหรับ segmentation
- แทนที่ HSV-only → "SAM2 primary, HSV fallback"
- แก้ classifier section: EfficientNet → DINOv2-Small

**research/_narrative_spine.md**
- อัปเดต "เครื่องมือทำอะไร" → SAM2 foundation model segmentation → DINOv2 classification
- เพิ่ม VLM Teacher (Gemini pseudo-label) เป็น layer ใหม่ถ้ายังไม่มี

**research/_data_dictionary.md**
- Phenotyper traits: source → "SAM2 point-prompt + Classical CV"
- เพิ่ม 7 features ใหม่ที่ยังไม่มี: convex_hull_ratio, exg_mean, vari_mean,
  glcm_contrast, glcm_homogeneity
- แก้ ai_status/ai_confidence: "EfficientNet" → "DINOv2-Small"

**research/_citation_audit.md**
- เพิ่ม citations ถ้ายังไม่มี (verified URLs):
  - Ravi et al. 2024, SAM 2, ArXiv
    https://consensus.app/papers/details/31972e1fad1953e78d9d32908e51ff23/
  - Bao et al. 2025, Zero-Shot Instance Segmentation for Plant Phenotyping, Front Plant Sci
    https://consensus.app/papers/details/86cfd544ceb55be0b83c171e98d0e997/
  - Zhang et al. 2024, Adapting SAM for Plant Recognition, Horticulturae
    https://consensus.app/papers/details/8894e0b9a4ef584693f8437041494881/

### กลุ่ม B: Narrative & Planning (4 ไฟล์)

**research/05_narrative_problem_objective_impact.md**
- แก้ประโยคที่อ้างถึง classical CV / HSV เป็น primary method
- frame: "SAM2 + DINOv2 + Gemini Teacher" เป็น novel contribution ถ้ายังไม่มี

**research/report_outline.md**
- อัปเดต section ML/CV ให้ระบุ SAM2, DINOv2, pseudo-label pipeline
- แก้ "EfficientNet" → "DINOv2" ทุกที่

**research/_decisions_pending.md**
- ย้าย decisions ที่ตัดสินแล้ว (SAM2=segmentation, DINOv2=classifier) ออกจาก pending
- เพิ่ม note "ตัดสินแล้ว 2026-06-19"

**research/_backlog.md**
- ย้าย "swap to DINOv2" และ "SAM2 segmentation" ออกจาก backlog → done
- อัปเดต remaining backlog items

### กลุ่ม C: README (1 ไฟล์)

**README.md**
- แก้ทุกที่ที่บอก EfficientNet-B0 → DINOv2-Small (vit_small_patch14_dinov2)
- แก้ "7-feature phenotype extraction" → "14-feature phenotype extraction"
- แก้ Tech Stack table: PyTorch + timm (DINOv2-Small)
- แก้ Objectives checklist: EfficientNet → DINOv2
- เพิ่ม SAM2 segmentation และ Gemini pseudo-label ใน Features section

---

## Step 3 — ไฟล์ที่ห้ามแตะ (ชีววิทยาล้วน ไม่ขึ้นกับ engine)

research/01, 02, 03, 06, 07, 08, 09, 11, 12, 13, appendix_rubric_onepager.md
→ เปลี่ยน engine ไม่กระทบเลย ข้ามทั้งหมด

---

## กฎสำคัญ

- ห้าม git add / commit / push — GitHub Actions จัดการเอง
- อ่านไฟล์ก่อนแก้เสมอ — ถ้าไฟล์นั้นกล่าวถึง SAM2/DINOv2 ถูกต้องแล้ว ให้ข้าม
- ห้าม hallucinate citation — ใช้เฉพาะ URL ที่ระบุข้างบนเท่านั้น
- ห้ามแก้เนื้อหาชีววิทยา (TC protocol, สูตร MS, citation พืช) — แก้เฉพาะส่วน CV/ML
- จบงานด้วยสรุป: อัปเดตกี่ไฟล์ / ข้ามกี่ไฟล์ (เหตุผล) / engine ที่อ่านได้จากโค้ดจริง
