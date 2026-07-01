# 🔑 VitroVision v2 — Keyword Map สำหรับศึกษา

> สร้าง 2026-07-01 · ใช้เป็นแผนที่หัวข้อค้นคว้า (Consensus / Google Scholar / GitHub / HuggingFace)
> **ลำดับศึกษา:** เริ่ม **C (refraction) + D (glare)** ก่อน — 2 อันนี้ตัดสินว่าโปรเจกต์เป็นไปได้ไหม
> กฎ citation เดิม: cite ได้เมื่อ resolve ถึง paper จริง (Consensus/PubMed) + DOI/URL กดได้

---

## 🎯 Pipeline v2 (ภาพรวม)
วิดีโอรอบขวด → segment ต้นออกจากแก้ว/glare → 3D reconstruction → ดึง trait เชิงสรีระ (ปริมาตร / leaf area จริง / architecture) แบบ non-destructive
**คำถามชีววิทยา (CSBI anchor):** 3D-derived traits วัดการเจริญ/vigor ของต้น TC ได้ดีกว่า 2D projected area ไหม → เทียบ 3D vs 2D vs manual/destructive บน culture หลายชนิดที่มีในแล็บ

---

## ✅ SAM 3 — verify แล้ว (2026-07-01, facebook/sam3 บน Hugging Face)
- **มีจริง:** `facebook/sam3` (0.9B params) + `facebook/sam3.1` (มี.ค. 2026 เร็วขึ้น ~7x)
- **ทำอะไร:** Promptable Concept Segmentation (PCS) — พิมพ์ข้อความ `"leaf"`/`"shoot"`/`"plantlet"` → segment **ทุก instance** + **track ข้ามเฟรมวิดีโอ** (open-vocab)
- **impact:** อาจยุบ 2 ขั้น YOLO(detect)→SAM(segment) เหลือ SAM 3 ตัวเดียว (detect concept เองจาก text)
- ⚠️ **gated** (request access + login HF) · license = "other" (Meta ไม่ใช่ MIT/Apache — เช็คก่อนตีพิมพ์) · แนะนำ **CUDA/bfloat16, ไม่มี CPU/ONNX** → เครื่อง 8GB CPU **ช้ามาก** ต้อง Colab/Kaggle GPU
- บทบาทใน v2: **segmenter ฝั่ง 2D** (แยกต้นออกจากแก้ว/glare ต่อเฟรม) — **ไม่ใช่**ตัวสร้าง 3D
- refs: https://huggingface.co/facebook/sam3 · https://github.com/facebookresearch/sam3 · https://ai.meta.com/blog/segment-anything-model-3/

---

## A. การเก็บภาพ (Capture)
- `AR 3D capture` / `Apple Object Capture RealityKit` / `RealityScan Polycam photogrammetry app`
- `ARKit LiDAR 3D scanning` — ⚠️ S24 FE **ไม่มี LiDAR** → เดินสาย **RGB video → SfM** แทน
- `turntable multi-view image acquisition` / `video frame extraction structure from motion`
- `ChArUco / ArUco pose estimation scale calibration` — ให้ 3D มีหน่วยจริง (cm) ต่อยอด ArUco เดิมได้

## B. วิธีสร้าง 3D (Reconstruction)
- `COLMAP structure from motion` + `OpenMVS multi-view stereo` — มาตรฐาน, CPU ได้ (ช้า) ← ตัวเทสต์ de-risk
- `Gaussian Splatting 3DGS` / `nerfstudio NeRF` / `gsplat` — สวย แต่ต้อง GPU
- `NeuS implicit surface reconstruction` — ได้ mesh ผิว, ฐานของงาน through-glass
- `visual hull space carving silhouette` — reconstruct จาก silhouette (ทนเมื่อผิวเรียบไม่มี texture)

## C. 🔴 หัวใจ/ด่านตาย — วัตถุใน**ภาชนะโปร่งใส** (refraction)
- `refraction-aware 3D reconstruction transparent object`
- `reconstruction object inside transparent container` ← Tong 2023 ReNeuS (ตรงงานเป๊ะ)
- `refractive structure from motion` / `eikonal rendering refraction`
- `underwater refraction correction photogrammetry` — ปัญหาเดียวกัน (interface หักเหแสง)
- `index matching liquid transparent vessel imaging` — ลบ refraction เชิงกายภาพ
- `flat-walled vessel vs cylindrical jar optical distortion` — ขวดผนังแบน = ลด refraction (hardware ถูกสุด)

## D. Glare / แสงสะท้อน (Polarized + algo)
- `cross-polarization photography specular removal` — CPL ที่เลนส์ + polarizer ที่ไฟ (มาตรฐานถ่ายวัตถุมันเงา)
- `linear polarizer glare reduction` / `polarized illumination specular highlight`
- `specular highlight removal dichromatic reflection model` — ลบ algo หลังถ่าย
- `single image reflection removal deep learning` — ลบเงาสะท้อนบนแก้ว
- `diffuse dome / light tent illumination reflective object` — setup ไฟนุ่มลด hotspot

## E. Segmentation (แยกต้นออกจากแก้ว/พื้นหลัง ต่อเฟรม)
- `SAM 3 promptable concept segmentation` ✅ (ดูด้านบน) — text prompt → mask ทุกใบ + track
- `SAM 2 video object segmentation` / `MobileSAM efficient` — เบากว่าถ้า GPU จำกัด
- `YOLOv8-seg / YOLO11 instance segmentation` + `YOLO SAM auto-labeling` (Zhao 2025) — ทำ label ฟรีจาก mask

## F. ดึงข้อมูลชีววิทยาจาก 3D (Point cloud → สรีระ)
- `point cloud plant phenotyping trait extraction`
- `leaf / organ segmentation point cloud` · `plant skeletonization architecture topology`
- `convex hull volume / surface area from mesh` — ปริมาตร, leaf area จริง (2D ทำไม่ได้)

## G. เฉพาะทาง in vitro (domain)
- `non-destructive phenotyping plant tissue culture` (Bethge "Phenomenon", multi-sensor ผ่านขวดปิด)
- `micropropagation image analysis` · `shoot multiplication rate quantification`

## H. Validation / anchor ชีววิทยา (CSBI)
- `3D vs 2D phenotyping accuracy comparison ground truth`
- `image-derived traits correlation manual measurement R2 RMSE`

---

## 🧪 เครื่องมือลองมือได้เลย (de-risk test)
COLMAP / Meshroom (AliceVision, ฟรี GUI) / Polycam หรือ RealityScan (แอปมือถือ)
→ **เทสต์ 1 วัน:** ถ่าย video ขวด dense ที่มี 1 ขวด → รัน photogrammetry → ดูว่า point cloud พังเพราะ refraction ไหม → เลือก path (2.5D / refraction-mitigated / neural GPU)

## 📚 Papers ที่ verify แล้ว (จาก Consensus 2026-07-01)
- Yang 2024, Comput. Electron. Agric. — multi-view SfM/MVS plant phenotyping (R²=0.999)
- Li 2022, Front. Plant Sci. — **RGB video → SfM** maize traits (R²=0.99)
- Wang 2025, Front. Plant Sci. — SfM+MVS + 6-view ICP registration
- Tong 2023, CVPR — "Seeing Through the Glass" (refraction ทำ SfM/neural มาตรฐานพัง; แก้ด้วย NeuS+ray tracing)
- Bethge 2023, Plant Methods — non-destructive in vitro phenotyping (เลี่ยง full-3D ใช้ laser depth + projected area)
