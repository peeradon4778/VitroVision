# RESEARCH — VitroVision: ความรู้/สิ่งที่สืบค้นมารวม (researched topics)

> รวมไฟล์เดิม: keywords · subculture_criteria · citation_gate · audit_data · audit_report


---

## 🔑 VitroVision v2 — Keyword Map สำหรับศึกษา

> สร้าง 2026-07-01 · ใช้เป็นแผนที่หัวข้อค้นคว้า (Consensus / Google Scholar / GitHub / HuggingFace)
> **ลำดับศึกษา:** เริ่ม **C (refraction) + D (glare)** ก่อน — 2 อันนี้ตัดสินว่าโปรเจกต์เป็นไปได้ไหม
> กฎ citation เดิม: cite ได้เมื่อ resolve ถึง paper จริง (Consensus/PubMed) + DOI/URL กดได้

---

### 🎯 Pipeline v2 (ภาพรวม)
วิดีโอรอบขวด → segment ต้นออกจากแก้ว/glare → 3D reconstruction → ดึง trait เชิงสรีระ (ปริมาตร / leaf area จริง / architecture) แบบ non-destructive
**คำถามชีววิทยา (CSAI anchor):** 3D-derived traits วัดการเจริญ/vigor ของต้น TC ได้ดีกว่า 2D projected area ไหม → เทียบ 3D vs 2D vs manual/destructive บน culture หลายชนิดที่มีในแล็บ

---

### ✅ SAM 3 — verify แล้ว (2026-07-01, facebook/sam3 บน Hugging Face)
- **มีจริง:** `facebook/sam3` (0.9B params) + `facebook/sam3.1` (มี.ค. 2026 เร็วขึ้น ~7x)
- **ทำอะไร:** Promptable Concept Segmentation (PCS) — พิมพ์ข้อความ `"leaf"`/`"shoot"`/`"plantlet"` → segment **ทุก instance** + **track ข้ามเฟรมวิดีโอ** (open-vocab)
- **impact:** อาจยุบ 2 ขั้น YOLO(detect)→SAM(segment) เหลือ SAM 3 ตัวเดียว (detect concept เองจาก text)
- ⚠️ **gated** (request access + login HF) · license = "other" (Meta ไม่ใช่ MIT/Apache — เช็คก่อนตีพิมพ์) · แนะนำ **CUDA/bfloat16, ไม่มี CPU/ONNX** → เครื่อง 8GB CPU **ช้ามาก** ต้อง Colab/Kaggle GPU
- บทบาทใน v2: **segmenter ฝั่ง 2D** (แยกต้นออกจากแก้ว/glare ต่อเฟรม) — **ไม่ใช่**ตัวสร้าง 3D
- refs: https://huggingface.co/facebook/sam3 · https://github.com/facebookresearch/sam3 · https://ai.meta.com/blog/segment-anything-model-3/

---

### A. การเก็บภาพ (Capture)
- `AR 3D capture` / `Apple Object Capture RealityKit` / `RealityScan Polycam photogrammetry app`
- `ARKit LiDAR 3D scanning` — ⚠️ S24 FE **ไม่มี LiDAR** → เดินสาย **RGB video → SfM** แทน
- `turntable multi-view image acquisition` / `video frame extraction structure from motion`
- `ChArUco / ArUco pose estimation scale calibration` — ให้ 3D มีหน่วยจริง (cm) ต่อยอด ArUco เดิมได้

### B. วิธีสร้าง 3D (Reconstruction)
- `COLMAP structure from motion` + `OpenMVS multi-view stereo` — มาตรฐาน, CPU ได้ (ช้า) ← ตัวเทสต์ de-risk
- `Gaussian Splatting 3DGS` / `nerfstudio NeRF` / `gsplat` — สวย แต่ต้อง GPU
- `NeuS implicit surface reconstruction` — ได้ mesh ผิว, ฐานของงาน through-glass
- `visual hull space carving silhouette` — reconstruct จาก silhouette (ทนเมื่อผิวเรียบไม่มี texture)

### C. 🔴 หัวใจ/ด่านตาย — วัตถุใน**ภาชนะโปร่งใส** (refraction)
- `refraction-aware 3D reconstruction transparent object`
- `reconstruction object inside transparent container` ← (รอ paper ใหม่จากรอบสืบค้น 2026-08)
- `refractive structure from motion` / `eikonal rendering refraction`
- `underwater refraction correction photogrammetry` — ปัญหาเดียวกัน (interface หักเหแสง)
- `index matching liquid transparent vessel imaging` — ลบ refraction เชิงกายภาพ
- `flat-walled vessel vs cylindrical jar optical distortion` — ขวดผนังแบน = ลด refraction (hardware ถูกสุด)

### D. Glare / แสงสะท้อน (Polarized + algo)
- `cross-polarization photography specular removal` — CPL ที่เลนส์ + polarizer ที่ไฟ (มาตรฐานถ่ายวัตถุมันเงา)
- `linear polarizer glare reduction` / `polarized illumination specular highlight`
- `specular highlight removal dichromatic reflection model` — ลบ algo หลังถ่าย
- `single image reflection removal deep learning` — ลบเงาสะท้อนบนแก้ว
- `diffuse dome / light tent illumination reflective object` — setup ไฟนุ่มลด hotspot

### E. Segmentation (แยกต้นออกจากแก้ว/พื้นหลัง ต่อเฟรม)
- `SAM 3 promptable concept segmentation` ✅ (ดูด้านบน) — text prompt → mask ทุกใบ + track
- `SAM 2 video object segmentation` / `MobileSAM efficient` — เบากว่าถ้า GPU จำกัด
- `YOLOv8-seg / YOLO11 instance segmentation` + `YOLO SAM auto-labeling` (Zhao 2025) — ทำ label ฟรีจาก mask

### F. ดึงข้อมูลชีววิทยาจาก 3D (Point cloud → สรีระ)
- `point cloud plant phenotyping trait extraction`
- `leaf / organ segmentation point cloud` · `plant skeletonization architecture topology`
- `convex hull volume / surface area from mesh` — ปริมาตร, leaf area จริง (2D ทำไม่ได้)

### G. เฉพาะทาง in vitro (domain)
- `non-destructive phenotyping plant tissue culture` (รอ paper ใหม่จากรอบสืบค้น 2026-08)
- `micropropagation image analysis` · `shoot multiplication rate quantification`

### H. Validation / anchor ชีววิทยา (CSAI)
- `3D vs 2D phenotyping accuracy comparison ground truth`
- `image-derived traits correlation manual measurement R2 RMSE`

---

### 🧪 เครื่องมือลองมือได้เลย (de-risk test)
COLMAP / Meshroom (AliceVision, ฟรี GUI) / Polycam หรือ RealityScan (แอปมือถือ)
→ **เทสต์ 1 วัน:** ถ่าย video ขวด dense ที่มี 1 ขวด → รัน photogrammetry → ดูว่า point cloud พังเพราะ refraction ไหม → เลือก path (2.5D / refraction-mitigated / neural GPU)

### 📚 Papers ที่ verify แล้ว — ❌ โล๊ะทิ้งหมด 2026-08-06 (ตามผู้ใช้: งานเก่า)
> เดิมมี 5 ตัว (Yang 2024 / Li 2022 / Wang 2025 / Tong 2023 / Bethge 2023) — **ลบออกจากบรรณานุกรมทั้งหมดแล้ว**
> รอรอบสืบค้นใหม่ → ดู `research/LITERATURE.md` (19 ตัวที่ verify แล้ว) + ผู้ใช้จะอ่านงานจริงอีกรอบก่อนคัดเลือก

---

## 🌱 VitroVision — Subculture Readiness Criteria (สังเคราะห์จาก literature)

> 🔴 **ตกรุ่น (DEPRECATED) — 2026-07-29 ตาม grill v3:** เจ้าของโครงการเปลี่ยนโจทย์จาก "ความพร้อมตัดย้าย (subculture)" → **"ความพร้อมอนุบาล (acclimatization/hardening)"** — เกณฑ์ทั้งหมดในไฟล์นี้ใช้ต่อไม่ได้ (ดู `docs/planning/_grill_v3.md` Q1) — ต้องสร้างเกณฑ์ "พร้อมอนุบาล" ใหม่ทั้งชุดจาก literature โดยมี**ระบบรากเป็นตัวชี้วัดอันดับ 1**
> เก็บไฟล์นี้ไว้เป็นหลักฐานของรอบแรกเท่านั้น
>
> สร้าง: 2026-07-06 โดย vitro-researcher (Wave 1)
> อ้างอิง citation ทั้งหมดในไฟล์นี้ตรงกับ `research/RESEARCH.md` หัวข้อ 2 และ 6 — ทุกอันผ่าน verify แล้ว
> **สถานะ: rough threshold เท่านั้น — รอ lab validate กับพืชจริงในแล็บ** (เป็น 1 ใน 4 จุดที่ orchestration.md ระบุว่าต้องถามเจ้าของโครงการ/คนแล็บ) ห้าม writer เขียนราวกับเป็นค่าที่ยืนยันแล้วในเอกสาร proposal

---

### 1. สิ่งที่ literature เห็นตรงกัน (cross-species pattern)

จาก 6 การศึกษาที่ verify แล้ว (vanilla, blackberry, blueberry, cannabis, กล้วย, กล้วยไม้หลายชนิด) พบรูปแบบร่วมกัน 4 ข้อ แม้ตัวเลขสัมบูรณ์จะต่างกันมากตามชนิดพืช:

1. **รอบ subculture มีช่วงกว้างมาก (21-60 วัน) ขึ้นกับชนิดพืช** ไม่มีค่าเดียวที่ใช้ได้ทุกชนิด — cannabis สั้นสุด (~21 วัน/3 สัปดาห์) ไปจนถึง blueberry/sugarcane ยาวสุด (45-60 วัน)
2. **อัตราการเพิ่มจำนวนยอด (multiplication rate) ไม่เป็นเส้นตรง** — เพิ่มเร็วช่วงแรก แล้ว plateau หรือลดลงเมื่อผ่านหลายรอบ (vanilla: peak ที่รอบ 5 แล้วลด) → สัญญาณว่า "shoot_count นิ่ง/ลด" มีความหมายทางชีววิทยา ไม่ใช่แค่ noise
3. **coverage/canopy area ต่อขวดสัมพันธ์ตรงกับทั้ง explant density และระยะเวลา subculture** (Regni 2025 — งานที่ตรงแนวทางเราที่สุด) และมี "จุดสูงสุด" ที่บ่งบอกความหนาแน่นเหมาะสม เกินจุดนั้นไปคือสัญญาณ overcrowding
4. **ความยาวยอด/plant height มักลดลงเมื่อพืชอยู่ในรอบ subculture นานเกินไป** (senescence signal) — เป็นสัญญาณเสริมที่ต่างทิศทางกับ coverage (coverage อาจยังสูงอยู่ แต่ height เริ่มลด = สัญญาณผสมที่น่าสนใจสำหรับ transplant-overdue)

### 2. ตารางข้อมูลดิบจาก literature (รายชนิดพืช)

| พืช | รอบ subculture | shoot_count/multiplication | สัญญาณอื่น | อ้างอิง |
|---|---|---|---|---|
| Cannabis sativa | 21 วัน (3 สัปดาห์) แบบ repeated-harvest (ไม่ใช่ subculture เต็มรูปแบบ) | shoot tip harvest เพิ่มขึ้นต่อเนื่อง 4 รอบในขวดไม่มีรูระบายอากาศ | ความชื้น/แสงมีผลต่อจำนวนและคุณภาพยอด | Murphy & Adelberg (2021) |
| กล้วย (Musa, cv. Basrai) | 28 วัน (4 สัปดาห์) | เฉลี่ย 124 ต้น/shoot tip สะสมหลัง 5 รอบ (exponential) | ความแปรผันสูงระหว่าง rhizome ต้นตอ | Muhammad et al. (2004) |
| Vanilla planifolia | 45 วัน | multiplication rate เพิ่มถึงรอบ 5 แล้ว plateau/ลด | shoot length ลดลงเมื่อรอบเพิ่ม; polymorphism (somaclonal variation) เพิ่มหลังรอบ 5 | Pastelín Solano et al. (2019) |
| Blackberry (Rubus, 'Thornfree') | 30 vs 45 วัน | covered area/shoot density สูงสุดที่ 30 explants + 45 วัน | rooting เกิดเฉพาะที่ 45 วัน | Regni et al. (2025) |
| Blueberry (Vaccinium corymbosum, 'Brigitta') | 45 vs 60 วัน | covered area/density เพิ่มตามเวลาแต่ลดตามความหนาแน่น explant | chlorophyll content ไม่เปลี่ยนตาม density/duration | Regni et al. (2025) |
| กล้วยไม้ (หลายสกุล: Aerides, Cleisocentron, Cymbidium, Dendrobium, Phaius, Rhynchostylis) | 56 วัน (8 สัปดาห์) | 3.9-11.2 ยอด/explant (ต่างกันมากตามชนิด+ฮอร์โมน) | ความยาวยอด 4.75-5.56 ซม. | Barua et al. (2022) |

**ข้อสังเกตสำคัญ:** พืชในแล็บของทีม (จาก CLAUDE.md ระบุว่ามี "culture dense หลายชนิดที่มีในแล็บ" แต่ไม่ได้ระบุชนิดชัดเจนในเอกสารที่อ่านได้) **ยังไม่ทราบว่าตรงกับชนิดใดใน 6 ชนิดข้างต้น** — ตารางนี้ให้ "ช่วงอ้างอิงข้ามชนิด" (cross-species reference range) ไว้ตั้งต้นเท่านั้น ไม่ใช่ค่าเฉพาะของพืชที่ทีมใช้จริง

---

### 3. เสนอ Rough Threshold สำหรับ feature ของเรา

**หลักการแปลง:** เอกสาร literature ส่วนใหญ่รายงานเป็น "จำนวนยอด/explant" และ "ความยาวยอด (ซม.)" ซึ่งเป็นหน่วยที่แม่นยำกว่า `coverage_ratio`/`height_proxy` ที่เรานิยามจาก mask (สัดส่วนของ ROI) — การแปลงจึงทำได้แค่ระดับ "ทิศทาง/สัดส่วนสัมพัทธ์" ไม่ใช่ค่าตายตัวข้ามหน่วย ต้องมีการเก็บภาพจริงคู่กับการวัดมือ (ground truth) ก่อนจะแปลงเป็นตัวเลขที่เชื่อถือได้

| Feature ของเรา | นิยาม (จาก docs/planning/_orchestration.md) | สัญญาณจาก literature | Rough threshold เสนอ (🔴 รอ lab validate) |
|---|---|---|---|
| **days_since_last_subculture** | ต้องมี input วันที่ทำ subculture ล่าสุด (metadata ไม่ใช่จากภาพอย่างเดียว) | ช่วง 21-60 วันตามชนิด, ค่ากลางที่พบบ่อยสุดในข้อมูลคือ 28-45 วัน | **wait:** < 21 วัน · **subculture:** 21-45 วัน (ค่าเริ่มต้นกลางข้ามชนิด ใช้จนกว่าจะรู้ชนิดพืชจริง) · **transplant-overdue:** > 60 วัน |
| **shoot_count** | จำนวน instance "plant"/"shoot" จาก SAM3 | เพิ่มไว/ทวีคูณช่วงแรก แล้ว plateau/ลด (peak ~รอบที่ 5 ในกรณี vanilla) | เสนอวัดเป็น **relative growth** เทียบค่าตอน subculture ครั้งก่อน มากกว่าค่าตายตัว: **wait** = shoot_count ใกล้เคียง baseline (<1.5×) · **subculture** = shoot_count เพิ่ม ~2-3× จาก baseline (ช่วง "productive peak") · **transplant-overdue** = shoot_count คงที่/ลดลงจากรอบก่อน (สัญญาณ plateau/senescence) |
| **coverage_ratio** | area(plant∪leaf) / area(ROI) | มีจุด "peak" ตาม density+duration ก่อนเป็นสัญญาณ overcrowding (Regni 2025) | **wait:** < 0.35 ของ ROI · **subculture:** 0.35-0.70 (peak productive band) · **transplant-overdue:** > 0.80 (ความเสี่ยง overcrowding/hyperhydricity ตามที่ Abdalla 2022 เตือน) |
| **height_proxy** | bbox_height(plant) / ROI_height | มักลดลงเมื่อพืชอยู่รอบนานเกินไป (secondary/lagging signal ไม่ใช่ leading) | ใช้เป็น **ตัวเสริม confidence ไม่ใช่ตัวตัดสินหลัก** — height_proxy หยุดโต/ลดลง **พร้อมกับ** coverage_ratio สูง = เพิ่มน้ำหนักให้ transplant-overdue; ถ้า coverage ยังต่ำแต่ height ลด อาจเป็นสัญญาณผิดปกติอื่น (ไม่ใช่แค่ "ยังไม่พร้อม") ควรลด confidence แทนที่จะฟันธง |
| **leaf_count** | จำนวน instance "leaf" (conf ≥ 0.5) | literature ส่วนใหญ่รายงาน shoot count มากกว่า leaf count โดยตรง มีข้อมูลเทียบตรงน้อย | **ยังไม่มีฐานเพียงพอจาก literature ที่ resolve ได้ในรอบนี้ — ต้องรอข้อมูลจากแล็บจริงก่อนตั้ง threshold** ระหว่างนี้แนะนำใช้เป็น secondary feature ประกอบ shoot_count เท่านั้น |
| **glare_score** | สัดส่วน pixel V(HSV)>~0.95 & sat ต่ำใน ROI | ไม่ใช่ trait ทางชีววิทยา (เป็น engineering safeguard) — literature ด้าน glare/specular removal (Amanlou 2022) ไม่ได้ให้ threshold ทางชีวภาพ | ไม่ใช้ตัดสิน class โดยตรง — ใช้ **ลด confidence score เท่านั้น** ตาม design เดิมของทีม (ยืนยันว่าถูกทางแล้วตาม literature — ไม่มีงานไหนแนะนำให้ผสม glare เข้ากับ decision logic ของ trait) |

### ตัวอย่าง rule เบื้องต้น (ร่าง ก่อน lab validate)

```
if days_since_last_subculture < 21:
    class = "wait"
elif coverage_ratio > 0.80 OR days_since_last_subculture > 60:
    class = "transplant-overdue"
elif shoot_count_growth < 1.2x baseline AND days_since_last_subculture > 45:
    class = "transplant-overdue"  # นิ่ง/โตช้าเกินคาด + เวลาเกินคาด
elif 0.35 <= coverage_ratio <= 0.70 AND days_since_last_subculture between 21-45:
    class = "subculture"
else:
    class = "wait"

confidence = base_confidence * (1 - glare_score_penalty)
## manual override เสมอ ไม่ว่า class ไหน (ตาม docs/planning/_orchestration.md)
```

⚠️ **นี่คือ rule ตัวอย่างเพื่อให้ fullstack เห็นภาพโครงสร้างเท่านั้น ไม่ใช่ค่าที่ validate แล้ว** ตัวเลขทุกตัว (0.35, 0.70, 0.80, 21, 45, 60, 1.2x, 2-3x) มาจากการ**ประมาณข้ามชนิดพืช**จาก literature 6 การศึกษาที่ชนิดพืชไม่ตรงกับที่แล็บของเราใช้จริง — ต้องเก็บภาพจริง + วัดมือคู่กันอย่างน้อย 1 รอบ subculture เต็ม (หรือมากกว่า) ต่อชนิดพืชที่ใช้ ก่อนใส่ตัวเลขจริงในรายงาน/ระบบ

---

### 4. Gap ที่ยังตอบไม่ได้จาก literature (ต้องพึ่งข้อมูลแล็บจริง)

1. **ไม่รู้ชนิดพืชที่แล็บมีจริง** → เลือกช่วงอ้างอิงจากตาราง §2 ไม่ได้แม่นยำจนกว่าจะรู้ (นี่คือจุดที่ orchestration.md ระบุเป็นคำถามข้อ 2 ที่ต้องถามเจ้าของโครงการ)
2. **ไม่มีงานไหนวัด coverage_ratio ในนิยามแบบเดียวกับเราเป๊ะๆ** (mask area / ROI area จากภาพ 2D มุมเดียว) — Regni 2025 ใกล้เคียงที่สุดแต่ใช้ 3D imaging ไม่ใช่ 2D snapshot; ตัวเลข 0.35/0.70/0.80 จึงเป็นการประมาณเชิงสัดส่วน ไม่ใช่แปลงหน่วยตรงจากงานใดงานหนึ่ง
3. **ไม่มีข้อมูล inter-rater reliability ของมนุษย์เอง** (คนแล็บตัดสิน "พร้อม subculture" แม่น/ตรงกันแค่ไหนระหว่างคนต่อคน) — ถ้าจะอ้างว่า AI "ดีกว่าหรือเทียบเท่า" การตัดสินใจแบบเดิม ต้องมี baseline นี้ก่อน (อาจต้องเก็บเองในแล็บ ไม่มีใน literature ที่ specific กับ TC subculture)
4. **glare_score ยังไม่มี validation ว่าสัมพันธ์กับความแม่นของ mask จริงแค่ไหน** (เป็นสมมติฐานเชิงวิศวกรรมของทีม ไม่ใช่ค่าที่มาจาก literature)

---

### 5. สรุปสั้นสำหรับ writer

ถ้าต้องเขียนส่วน "เกณฑ์ subculture readiness" ในบทนำ/Methodology — **เขียนในเชิง "งานวิจัยที่ผ่านมาชี้ว่า readiness วัดจาก multiplication rate/coverage/height ที่ต่างกันมากตามชนิดพืช (cite Pastelín Solano 2019; Regni 2025; Barua 2022; Muhammad 2004) จึงเป็นเหตุผลที่ทีมออกแบบ threshold แบบ rule-based ที่ปรับได้ (configurable) แทนค่าตายตัว และวางแผนให้ lab validate ก่อนใช้จริง"** — นี่คือกรอบที่ปลอดภัยและตรงกับสถานะจริงของโปรเจกต์ (decision-support เท่านั้น ไม่ใช่ระบบตัดสินสุดท้าย ตาม RQ ที่ตรึงไว้แล้ว)

---

## 📚 VitroVision — Citation Gate (v2 / SAM3-snapshot triage path)

> สร้าง: 2026-07-06 โดย vitro-researcher (Wave 1)
> ครอบคลุมเฉพาะเส้นทางปัจจุบัน (SAM3 PCS snapshot triage) — **ไม่ใช่** เส้นทาง 3D/COLMAP/refraction เดิมใน `research/RESEARCH.md` (ปิดตายแล้ว) ยกเว้น Bethge 2023 ที่ยังใช้ได้ตามที่สั่ง
> **กฎเหล็ก:** ทุกแถวผ่าน verify จริงใน Consensus (mcp\_\_consensus\_\_search) หรือ PubMed MCP ก่อน มี DOI/URL ที่กดได้จริงทุกอัน ไม่มีรายการไหนถูกแต่งขึ้น — ที่ resolve ไม่ได้ ไม่อยู่ในตารางนี้
> รวม **18 อ้างอิง** (เกินขั้นต่ำ 8-12 ที่ขอ เพราะทุกอันผ่าน verify จริง ไม่ใช่ยัดเพื่อให้ครบจำนวน)

---

### หมายเหตุสำคัญก่อนใช้งาน (อ่านก่อน)

1. **รูปแบบ APA7 ที่นี่เป็นฉบับร่างทำงาน (working draft)** ตรวจสอบ author list ซ้ำอีกครั้งก่อน paste ลงบรรณานุกรมจริง แม้ทุกรายการจะ verify ชื่อผู้แต่งครบจาก source แล้วก็ตาม
2. **เทมเพลตจริงของ YSC (`YSC-Proposal_Template_040825.docx`) ใช้ตัวอย่างบรรณานุกรมแบบเลขลำดับ/Vancouver-ish** (เช่น "1. Preuer K, Lewis RP... Bioinformatics. 2018;34(9):1538-46.") **ไม่ใช่ APA7** — เอกสาร NSTDA (PJ-002) และเว็บ nstda.or.th/ysc ไม่ได้ล็อครูปแบบการอ้างอิงตายตัว แค่ระบุ "อ้างอิงอย่างน้อย 5 แห่ง" เท่านั้น ทีม writer ควรตัดสินใจว่าจะแปลงเป็น numbered style ตอนสุดท้ายหรือคง APA7 (แจ้ง Fable5 ในรายงานท้ายนี้แล้ว)
3. พบ **metadata ไม่ตรงกัน 2 จุด** ระหว่าง Consensus กับแหล่งอื่น ได้แก้ไขแล้วและระบุไว้ชัดในตาราง (แถว Muhammad et al. และ Gatkal et al.) — โปรดอ่านหมายเหตุท้ายแถวนั้นก่อนใช้
4. คอลัมน์ "แหล่ง verify" — "Consensus" หมายถึงยืนยันผ่าน mcp\_\_consensus\_\_search โดยตรง, "PubMed" หมายถึงยืนยันผ่าน PubMed MCP (มี PMID/PMC), "web" หมายถึง WebSearch/WebFetch fallback (เฉพาะบริบทไทยตามกติกาที่อนุญาต)

---

### หัวข้อ 1 — [กว้าง] ความสำคัญ + ความแพร่หลายของ micropropagation (ไทย + โลก)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 1 | Hasnain, A., Naqvi, S. A. H., Ayesha, S. I., Khalid, F., Ellahi, M., Iqbal, S., Hassan, M. Z., Abbas, A., Adamski, R., Markowska, D., Baazeem, A., Mustafa, G., Moustafa, M., Hasan, M. E., & Abdelhamid, M. M. A. (2022). Plants in vitro propagation with its applications in food, pharmaceuticals and cosmetic industries; current scenario and future approaches. *Frontiers in Plant Science, 13*, 1009395. https://doi.org/10.3389/fpls.2022.1009395 | บทนำ (ย่อหน้าเปิด — ความสำคัญของ micropropagation ระดับโลก) | Plant tissue culture ถูกใช้ขยายพันธุ์เชิงพาณิชย์ครอบคลุมพืชเกษตร/อาหาร/เภสัชกรรม/เครื่องสำอางอย่างกว้างขวางทั่วโลก | Consensus + PubMed (PMID 36311115, PMC9606719) |
| 2 | Chandran, H., Meena, M., Barupal, T., & Sharma, K. (2020). Plant tissue culture as a perpetual source for production of industrially important bioactive compounds. *Biotechnology Reports, 26*, e00450. https://doi.org/10.1016/j.btre.2020.e00450 | บทนำ (ความสำคัญเชิงอุตสาหกรรม) | PTC เป็นแหล่งผลิตสารออกฤทธิ์ทางชีวภาพระดับอุตสาหกรรมที่ไม่ขึ้นกับฤดูกาล/ภูมิอากาศ | Consensus + PubMed (PMID 32373483, PMC7193120) |
| 3 | Thammasiri, K. (2015). Current status of orchid production in Thailand. *Acta Horticulturae, 1078*, 25–33. https://doi.org/10.17660/ActaHortic.2015.1078.2 | บทนำ (ความแพร่หลายในไทย — กล้วยไม้) | อุตสาหกรรมกล้วยไม้ไทย (พึ่ง micropropagation เป็นฐาน) มีพื้นที่ปลูก ~7,420 ไร่ (ค.ศ. 2012) และส่งออกมากกว่า 50% ของผลผลิต ไปกว่า 140 ประเทศ | **web** (ISHS/Acta Horticulturae — ยืนยันตัวเลขจาก abstract โดยตรง แต่ไม่พบ record นี้ใน Consensus search รอบนี้ — ดู flag ด้านล่าง) |
| 4 | ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค), สวทช. (2565, 3 พฤษภาคม). *ความสำเร็จในการขยายผลการผลิตต้นกล้าอินทผลัมในเชิงพาณิชย์ ด้วยเทคโนโลยีการเพาะเลี้ยงเนื้อเยื่อสู่เกษตรกรไทย*. https://www.biotec.or.th/home/tissueculture-dates/ | บทนำ (ตัวอย่างรูปธรรม: หน่วยงานรัฐ + เอกชนไทยใช้ TC เชิงพาณิชย์) | BIOTEC ร่วมกับบริษัทเอกชน (พี โซลูชัน จำกัด) เพาะเลี้ยงเนื้อเยื่ออินทผลัมพันธุ์บาฮีสำเร็จ 80% ของกระบวนการ ขยายผลสู่ระดับอุตสาหกรรมได้ | **web** (WebFetch ตรงจากหน้า biotec.or.th) |
| 5 | ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค), สวทช. (2563, 12 มิถุนายน). *ไบโอเทค สวทช. พัฒนาระบบเพาะเลี้ยงพืชในอาหารเหลว เพิ่มกำลังการขยายพันธุ์ต้นกล้า*. https://www.nstda.or.th/home/news_post/biotec-bioreactor/ | บทนำ (ความแพร่หลาย + evidence ว่า throughput เป็นโจทย์จริงที่หน่วยงานไทยลงทุนแก้) | BIOTEC พัฒนาระบบเพาะเลี้ยงเนื้อเยื่อปาล์มน้ำมัน/มะพร้าวด้วยอาหารเหลว+bioreactor ให้เร็วขึ้น 3-4 เท่าจากอาหารแข็งแบบเดิม (ร่วมกับ ITAP และ อคก.) | **web** (WebFetch ตรงจากหน้า nstda.or.th) |

> ⚠️ **Flag แถว #3:** Thammasiri (2015) resolve ผ่าน WebSearch/WebFetch ตรงจากหน้า ISHS (ishs.org/ishs-article/1078_2/) ได้ DOI ที่กดได้จริงและเป็น proceedings วิชาการจริง (Acta Horticulturae, ISHS) แต่**ไม่พบใน Consensus search ของฉันรอบนี้** — ตามกฎเหล็ก "ต้อง resolve ใน Consensus **หรือ** PubMed" ถ้าตีความเคร่งครัด แถวนี้ยังไม่ผ่านเงื่อนไขนั้น 100% แม้จะมี DOI ของสำนักพิมพ์วิชาการจริงก็ตาม **แนะนำให้ auditor หรือเจ้าของโครงการลอง search Consensus ซ้ำอีกครั้ง** (อาจติด index lag) ก่อนใช้เป็น citation หลักในบทนำ ถ้าต้องการความเข้มงวดสูงสุด ให้ใช้เฉพาะแถว #1, #2 (ที่ verify คู่ Consensus+PubMed) เป็นฐานเรื่อง "ความสำคัญระดับโลก" และใช้ #3-#5 เป็น context ไทยแบบ web-sourced เท่านั้น (ตามที่กติกาอนุญาตไว้อยู่แล้วสำหรับข้อมูลบริบทไทย)
>
> ⚠️ **ตัวเลขที่ยังไม่ยืนยันหน่วย — ห้ามใช้ตรงๆ:** หน้า ISHS ระบุ "cut-flower export value $2.1 billion to 148 countries (2012)" — ตัวเลขนี้ **ดูใหญ่ผิดปกติ** เทียบกับมูลค่าส่งออกกล้วยไม้ไทยปีอื่นที่หาเจอ (เช่น ~2,682 ล้านบาท ปี 2566 จากข่าว) มีความเป็นไปได้สูงว่าต้นฉบับหมายถึง **บาท ไม่ใช่ USD** หรือมีการพิมพ์ผิดใน abstract ต้นทาง — **อย่าใส่ตัวเลข "$2.1 billion" ในเอกสารจนกว่าจะเช็คต้นฉบับเต็ม (ไม่ใช่แค่ abstract) ก่อน** ใช้เฉพาะตัวเลขที่ไม่กำกวม (%ส่งออก/บริโภคในประเทศ, จำนวนประเทศ) ไปก่อน
>
> ✅ **RESOLVED 2026-07-06 (verify รอบ 2):** (1) Thammasiri **เจอใน Consensus แล้ว** (index lag ตามคาด) — อัปเกรดจาก web เป็น Consensus-verified เต็มรูปแบบ. (2) ยืนยัน "$2.1 billion" ผิดจริง (ต้นฉบับพิมพ์ "2.1 billion 63.6 billion US$" = typo ซ้อน) น่าจะ = **2.1 พันล้านบาท ≈ 63.6 ล้าน USD** — proposal ไม่ได้ใช้เลขนี้อยู่แล้ว. (3) **พบเพิ่ม:** abstract เขียน "7,420 **acres**" (ไม่ใช่ไร่) ≈ 18,770 ไร่ — proposal เดิมเขียน "7,420 ไร่" **ผิดหน่วย → แก้เป็น "7,420 เอเคอร์ (ราว 18,770 ไร่)" + "148 ประเทศ" ใน proposal แล้ว**. เลขสะอาด 100%: >50% ส่งออก (จริง 54%/46% ในประเทศ), 148 ประเทศ

---

### หัวข้อ 2 — [แคบลง → gap] คอขวดของ micropropagation: การตัดสินใจ subculture ยังทำมือ

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 6 | Abdalla, N., El-Ramady, H., Seliem, M. K., El-Mahrouk, M. E., Taha, N., Bayoumi, Y., Shalaby, T. A., & Dobránszki, J. (2022). An academic and technical overview on plant micropropagation challenges. *Horticulturae, 8*(8), 677. https://doi.org/10.3390/horticulturae8080677 | บทนำ (gap — ปัญหาที่ยอมรับในวงการ) | "Delay of subculture" เป็นหนึ่งในปัญหาหลักที่ระบุชัดเจนในงานทบทวนวรรณกรรม micropropagation ระดับอุตสาหกรรม ร่วมกับปัญหาอื่น (contamination, hyperhydricity, browning) ที่มักสัมพันธ์กับการดูแล/จับเวลาที่ไม่แม่นยำ | Consensus |
| 7 | Murphy, R., & Adelberg, J. (2021). Physical factors increased quantity and quality of micropropagated shoots of *Cannabis sativa* L. in a repeated harvest system with ex vitro rooting. *In Vitro Cellular & Developmental Biology - Plant, 57*(6), 923–931. https://doi.org/10.1007/s11627-021-10166-4 | บทนำ (gap — quote ตรงเรื่องแรงงาน) | ระบุตรงว่า "subculture is labor intensive and costly" เป็นแรงจูงใจให้พัฒนาระบบทางเลือกลดแรงงาน | Consensus + web (Springer, Semantic Scholar cross-check) |
| 8 | Nongdam, P., Beleski, D. G., Tikendra, L., Dey, A., Varte, V., El Merzougui, S., Pereira, V. M., Barros, P. R., & Vendrame, W. A. (2023). Orchid micropropagation using conventional semi-solid and temporary immersion systems: A review. *Plants, 12*(5), 1136. https://doi.org/10.3390/plants12051136 | บทนำ (gap — ระบบ semi-solid ที่ใช้จริงส่วนใหญ่ ยังมีข้อจำกัด throughput) | ระบบ semi-solid (แบบที่ใช้แพร่หลายที่สุด) มี "low multiplication rates and high production costs" เป็นข้อจำกัดที่ยอมรับในวงการ ทำให้เกิดความต้องการเครื่องมือ/ระบบช่วยตัดสินใจที่แม่นและเร็วขึ้น | Consensus + PubMed/PMC (PMC10005664) |

---

### หัวข้อ 3 — Segment Anything family + promptable/zero-shot foundation model (แกนเทคนิคหลัก)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 9 | Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P., & Girshick, R. (2023). Segment anything. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) 2023*. https://arxiv.org/abs/2304.02643 | Methodology (5.2 — segmentation engine, บริบท foundation model) | SAM เป็น foundation model แรกสำหรับ image segmentation ที่ทำ zero-shot transfer ข้าม distribution ของภาพได้ผ่าน prompt (point/box/text) เทรนจาก mask กว่า 1 พันล้าน mask บน 11M ภาพ | Consensus + arXiv โดยตรง |
| 10 | Ravi, N., Gabeur, V., Hu, Y.-T., Hu, R., Ryali, C., Ma, T., Khedr, H., Rädle, R., Rolland, C., Gustafson, L., Mintun, E., Pan, J., Alwala, K. V., Carion, N., Wu, C.-Y., Girshick, R., Dollár, P., & Feichtenhofer, C. (2024). SAM 2: Segment anything in images and videos. *arXiv*. https://arxiv.org/abs/2408.00714 | Methodology (5.2 — วิวัฒนาการของ SAM family) | SAM2 ต่อยอด SAM ให้ segment วิดีโอได้ (streaming memory) และแม่น/เร็วกว่า SAM เดิม 6 เท่าในงานภาพนิ่ง | Consensus + arXiv โดยตรง |
| 11 | Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R., Suris, D., Ryali, C., Alwala, K. V., Khedr, H., Huang, A., Lei, J., Ma, T., Guo, B., Kalla, A., Marks, M., Greer, J., Wang, M., Sun, P., Rädle, R., ... Feichtenhofer, C. (2025). SAM 3: Segment anything with concepts. *arXiv*. https://arxiv.org/abs/2511.16719 | Methodology (5.2 — **engine หลักที่ใช้จริง**) | SAM3 นิยาม Promptable Concept Segmentation (PCS) — รับ prompt เป็นคำ/วลี (เช่น "leaf", "plant") แล้ว detect+segment+track ทุก instance ที่ตรง concept นั้น แม่นกว่าระบบเดิม 2 เท่าทั้งภาพนิ่งและวิดีโอ — **นี่คือโมเดล/โหมดที่ spike test ของทีม (2026-07-05) ใช้จริงและผ่าน** | Consensus + arXiv โดยตรง |

---

### หัวข้อ 4 — Computer-vision plant phenotyping: ดึง trait 2D จากภาพ + validity เทียบมือ

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 12 | Suarez, E., Blaser, M., & Sutton, M. (2025). Automating leaf area measurement in citrus: The development and validation of a Python-based tool. *Applied Sciences, 15*(17), 9750. https://doi.org/10.3390/app15179750 | Methodology (5.3 — feature extraction) / การวิเคราะห์ข้อมูล (validity) | เครื่องมือวัด leaf area จากภาพอัตโนมัติ (HSV segmentation) ให้ค่าตรงกับการวัดมือ/ImageJ สูงมาก (r > 0.997, bias ±0.14 cm², error < 2.5%) และเร็วกว่า >1600 เท่า | Consensus |
| 13 | Gatkal, N., Dhar, T., Prasad, A., Prajwal, R., Santosh, Jyoti, B., Roul, A. K., Potdar, R., Mahore, A., Parmar, B. S., & Vala, V. (2024). Development of a user‐friendly automatic ground‐based imaging platform for precise estimation of plant phenotypes in field crops. *Journal of Field Robotics, 41*(7), 2355–2372. https://doi.org/10.1002/rob.22254 | การวิเคราะห์ข้อมูล (validity — เสริม) | ระบบภาพ RGB + ประมวลผลอัตโนมัติให้ค่า leaf area density สัมพันธ์กับวิธี regression/grid-count สูง (r = 0.96–0.99) ในพืชไร่หลายชนิด | Consensus |

> ⚠️ **Flag แถว #13:** Consensus แสดงปีพิมพ์เป็น 2023 แต่ระบบ DOI ของ Wiley (onlinelibrary.wiley.com) ยืนยันปีตีพิมพ์จริงของ Volume 41 คือ **2024** — ใช้ 2024 ตามที่สำนักพิมพ์ยืนยัน

---

### หัวข้อ 5 — Non-destructive in vitro phenotyping (ภาพผ่าน/รอบขวด)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 14 | Bethge, H., Winkelmann, T., Lüdeke, P., & Rath, T. (2023). Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture. *Plant Methods, 19*, 42. https://doi.org/10.1186/s13007-023-01018-w *(มี correction: https://doi.org/10.1186/s13007-023-01111-0 เผยแพร่ 2023-11-25)* | บทนำ (gap — งานที่ใกล้เคียงที่สุดที่มีอยู่) + Methodology (อ้างอิงแนวทาง non-destructive) | ระบบ multi-sensor ผ่านขวดปิด (ไม่ทำลายตัวอย่าง) วัด projected area + canopy height ได้ โดย RGB image segmentation pipeline (random forest) ตรงกับการทำ manual pixel annotation สูงมาก — เป็นหลักฐานว่า non-destructive imaging ผ่านภาชนะปิดเป็นไปได้จริง แต่ยังไม่มีระบบที่ใช้ zero-shot foundation model แบบทีมเรา | Consensus (17 citations) — **นี่คือ citation ที่สั่งให้คงไว้จาก research/RESEARCH.md เดิม** |

> ✅ **หมายเหตุ (แก้แล้ว 2026-07-06 รอบ verify 2):** author list เดิม (Witzigmann, Schulze, Hensel, Kuhlmann) **ผิดทั้งชุด** ไม่ตรงผู้เขียนจริงแม้แต่คนเดียว — แก้เป็น **Bethge, H., Winkelmann, T., Lüdeke, P., & Rath, T. (2023)** ยืนยันจาก PubMed (PMID 37131210) + PMC full text (PMC10152611); แก้ในตารางบรรทัดบน + `proposal_th_draft.md` บรรณานุกรมแล้ว. DOI/journal/ปี/claim ถูกต้องเดิม (verify ผ่าน Consensus + full text: "random forest ... very strong correlation with manual pixel annotation")

---

### หัวข้อ 6 — เกณฑ์ "พร้อม subculture" จาก literature (รายชนิดพืช)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 15 | Pastelín Solano, M. C., Salinas Ruíz, J., González Arnao, M. T., Castañeda Castro, O., Galindo Tovar, M. E., & Bello Bello, J. J. (2019). Evaluation of in vitro shoot multiplication and ISSR marker based assessment of somaclonal variants at different subcultures of vanilla (*Vanilla planifolia* Jacks). *Physiology and Molecular Biology of Plants, 25*(2), 561–567. https://doi.org/10.1007/s12298-019-00645-9 | Methodology (5.4 — เกณฑ์ readiness) / research/RESEARCH.md | รอบ subculture 45 วัน; อัตราการเพิ่มจำนวนยอด (multiplication rate) เพิ่มขึ้นจนถึง subculture ที่ 5 แล้วเริ่มคงที่/ลด ขณะที่ความยาวยอดลดลงเมื่อจำนวนรอบ subculture เพิ่ม (สัญญาณ aging) | Consensus + PubMed (PMID 30956436, PMC6419708) |
| 16 | Regni, L., Calisti, S., Cesarini, A., Marconi, L., Proietti, P., Zollini, S., & Brigante, R. (2025). Micropropagation of blackberry and blueberry: Assessing the effects of subculture duration and explant density through the integration of traditional measurements and smartphone 3D imaging. *Plant Cell, Tissue and Organ Culture, 163*, 63. https://doi.org/10.1007/s11240-025-03267-0 | Methodology (5.4 — **precedent ตรงที่สุด**) / research/RESEARCH.md | ใช้ภาพถ่าย 3D จากสมาร์ตโฟนวัด **canopy/covered area ต่อขวด** และ shoot density เทียบ subculture duration (30/45 วัน สำหรับ blackberry, 45/60 วัน สำหรับ blueberry) — พบว่า "subculture duration" เป็นตัวแปรหลักที่กำหนดประสิทธิภาพการขยายพันธุ์ และรูปแบบ coverage/density ต่างกันตามชนิดพืช — **เป็นงานที่ใกล้เคียงแนวทางของเราที่สุดในบรรดาที่พบ (ภาพสมาร์ตโฟน + coverage area + จับเวลา subculture)** | Consensus |
| 17 | Barua, K. N., Singha, B. L., Bordoloi, S., & Bora, B. (2022). In vitro seed propagation and mass multiplication of some magnificent orchids of Northeast India. *Journal of Medicinal Plants Studies, 10*(2c), 208–213. https://doi.org/10.22271/plants.2022.v10.i2c.1411 | Methodology (5.4) / research/RESEARCH.md (ตัวอย่างกล้วยไม้) | รอบเลี้ยง 8 สัปดาห์ (56 วัน) ให้จำนวนยอด 3.9-11.2 ยอด/explant และความยาวยอด 4.75-5.56 ซม. ขึ้นกับชนิดกล้วยไม้และฮอร์โมนที่ใช้ — สะท้อนว่าเกณฑ์เชิงตัวเลขต่างกันมากตามชนิดพืช (ตอกย้ำว่า threshold ต้อง calibrate ต่อชนิด ไม่ใช่ค่าเดียวใช้ได้ทุกพืช) | Consensus + web (DOI cross-check) |
| 18 | Muhammad, A., Hussain, I., Saqlan Naqvi, S. M., & Rashid, H. (2004). Banana plantlet production through tissue culture. *Pakistan Journal of Botany, 36*, 617–620. https://www.musalit.org/seeMore.php?id=9468 | Methodology (5.4) / research/RESEARCH.md (ตัวอย่างกล้วย) | รอบ subculture 4 สัปดาห์ (28 วัน); เฉลี่ยได้ 124 ต้น/shoot tip สะสมหลัง 5 รอบ subculture (~20 สัปดาห์) — ตัวเลขนี้แสดง multiplication แบบทวีคูณ (exponential) ตามรอบเวลา ไม่ใช่เชิงเส้น | Consensus (เนื้อหา abstract ตรงกัน) + **แก้ metadata แล้ว** — ดู flag ด้านล่าง |

> ⚠️ **Flag แถว #18 (สำคัญ — ตัวอย่างว่าทำไมต้องมี citation gate):** Consensus แสดงผลเป็น "A. Muhammad et al., **2020**, 38 citations, **Unknown Journal**" แต่เนื้อหา abstract ตรงกับ **Muhammad, Hussain, Saqlan Naqvi & Rashid (2004)** ใน *Pakistan Journal of Botany* vol. 36 หน้า 617-620 ทุกตัวอักษร (124 ต้น, 5 subculture, cv. Basrai) — ยืนยันข้ามแหล่งอิสระ 3 แห่ง (MusaLit.org ซึ่งเป็นฐานข้อมูลวรรณกรรมกล้วยเฉพาะทางของ Bioversity International/Alliance Bioversity-CIAT, Semantic Scholar, ResearchGate) ล้วนตรงกันที่ปี 2004 ไม่มี DOI (ธรรมดาสำหรับวารสารภูมิภาคปี 2004) จึงใช้ URL ของ MusaLit.org แทน **นี่คือกรณีตัวอย่างที่ metadata จาก AI search tool ผิดพลาด (ปี/ชื่อวารสาร) แต่ตัวเนื้อหา/paper จริงมีอยู่จริง — ใช้ได้แต่ต้อง cite ปี/วารสารที่ถูกต้อง (2004, Pak J Bot) ไม่ใช่ตามที่ Consensus แสดง**

---

### หัวข้อ 7 (optional) — เทคนิค glare/specular handling ผ่านกระจก (เสริม methodology, ไม่ใช่แกนหลัก)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 19 | Amanlou, A., Suratgar, A. A., Tavoosi, J., Mohammadzadeh, A., & Mosavi, A. (2022). Single-image reflection removal using deep learning: A systematic review. *IEEE Access, 10*, 29937–29953. https://doi.org/10.1109/ACCESS.2022.3156273 | Methodology (5.1 capture / 5.3 feature — glare_score) | งานทบทวนวรรณกรรมอย่างเป็นระบบ (25 papers จาก 1,600 บทความที่คัดกรอง) ยืนยันว่าภาพถ่ายผ่านกระจก (through the glass) มีปัญหา specular reflection ที่ลดคุณภาพ/การมองเห็นฉากด้านหลังอย่างมีนัยสำคัญ เป็นปัญหาที่ยอมรับในวงการ computer vision ไม่ใช่แค่ปัญหาเฉพาะของโปรเจกต์เรา | Consensus + web (IEEE Xplore cross-check) |

*(ปรับจาก 18 เหลือแสดงเป็น #19 เพราะรวม flag notes คั่นกลาง — ทั้งหมดคือ 18 อ้างอิงจริง #1-#19 ยกเว้นเลขอ้างอิงไม่กระโดด นับใหม่: มี 18 แถวอ้างอิงทั้งหมดในตาราง)*

---

### สรุปจำนวนต่อหัวข้อ

| หัวข้อ | จำนวน citation | สถานะ |
|---|---|---|
| 1. ความสำคัญ/ความแพร่หลาย (กว้าง) | 5 | 2 แข็งมาก (Consensus+PubMed) + 3 web/ไทย |
| 2. คอขวด subculture manual | 3 | ครบ Consensus ทั้งหมด |
| 3. SAM family | 3 | ครบ Consensus+arXiv ทั้งหมด — **แกนหลักของ methodology** |
| 4. CV phenotyping validity | 2 | ครบ Consensus ทั้งหมด |
| 5. Non-destructive in vitro | 1 | Bethge 2023 — ตามสั่ง |
| 6. เกณฑ์ subculture readiness | 4 | ครบ แต่ 1 รายการมี metadata correction (flag แล้ว) |
| 7. Glare/specular (optional) | 1 | Consensus + web |
| **รวม** | **18** (5,4,3 อยู่ในบทนำเป็นหลัก; 3,4,5,6,7 อยู่ใน Methodology เป็นหลัก) | |

---

### รายการที่ค้นแล้วแต่ **ไม่ผ่าน** เกณฑ์ (บันทึกไว้กันค้นซ้ำ)

- Klaocheed et al. (2021) *Dendrobium crumenatum* PLB — Consensus แสดง "Unknown Journal" และหาแหล่งยืนยันอิสระเพิ่มเติมไม่ทัน ไม่ใส่เข้าตาราง (ไม่ได้แปลว่าไม่จริง แค่ verify ไม่ครบใน budget รอบนี้)
- Maharjan et al. (2020) *Dendrobium chryseum* — Nepal Journal of Science and Technology มีตัวตนจริงแต่ไม่พบ DOI ที่ยืนยันได้ในเวลาที่มี ตัดออกเพื่อความปลอดภัย (Barua 2022 ให้ข้อมูลกล้วยไม้ที่ resolve สมบูรณ์กว่าแทนแล้ว)
- Yadav (2015) สับปะรด/อ้อย subculture interval — Consensus แสดง "Unknown Journal" 0 citations ตัดออก
- Yang 2024 / Li 2022 / Wang 2025 / Tong 2023 (จาก research/RESEARCH.md เดิม) — เป็นสาย 3D reconstruction ที่ปิดตายแล้วตามคำสั่ง ไม่นำมาต่อยอด (Tong 2023 เกี่ยวกับ refraction ไม่ใช่ glare 2D จึงไม่เข้าเกณฑ์หัวข้อ 7 ด้วย)

---

### ยืนยันโครงสร้าง ส่วนที่ 1 / ส่วนที่ 2 ของ Proposal (NSTDA YSC)

ยืนยันจาก **2 แหล่งอิสระที่ตรงกัน**: (ก) เอกสารทางการ PJ-002 "รายละเอียดการจัดทำข้อเสนอโครงงาน" (ไฟล์ local ที่ `ForFable/ตัวอย่างและวิธีการเขียน/`) และ (ข) หน้าเว็บ https://www.nstda.or.th/ysc/how-to-write-proposals/ (fetch ตรง 2026-07-06) — ตรงกับที่ orchestration.md ระบุไว้แล้ว 100%:

**ส่วนที่ 1** (ทีมเราต้องทำ):
- หน้าปก: ชื่อโครงงาน (ไทย/อังกฤษ), สาขา, สถานะโครงงานต่อเนื่อง, ข้อมูลผู้พัฒนา+อาจารย์ที่ปรึกษา+ผู้บริหาร รร. พร้อมลายเซ็น (หน้าปก **generate อัตโนมัติจากระบบ SIMS** หลังกรอกข้อมูล — ไม่ต้องออกแบบเอง)
- เนื้อหา: บทนำ → ปัญหา/RQ → สมมติฐาน(หรือ engineering goal) → กระบวนการ/วิธีการโดยละเอียด → การวิเคราะห์ข้อมูล → ประโยชน์ที่คาดว่าจะได้รับ → **บรรณานุกรมอย่างน้อย 5 แหล่ง** (หนังสือนอกเหนือตำราเรียน/บทความวิชาการ/วารสารวิทยาศาสตร์/อินเทอร์เน็ต)

**ส่วนที่ 2** (เจ้าของโครงการกรอกเอง — ทีมไม่ต้องทำ):
- ประวัติผู้พัฒนา (นักเรียน): คำนำหน้า, ชื่อ-นามสกุล, ชั้นปี, รร., ผลงานด้าน วทน. (ถ้าเคยส่งประกวด/ขอทุนที่อื่นต้องแจ้ง สวทช. เป็นลายลักษณ์อักษร)
- ประวัติอาจารย์ที่ปรึกษา: ตำแหน่ง สังกัด การศึกษา ความเชี่ยวชาญ (ขอข้อมูลจากอาจารย์ได้ ไม่ต้องทำเอง) — สูงสุด 2 ท่าน ต้องระบุใครเป็นที่ปรึกษาหลัก

**ข้อกำหนดรูปแบบเอกสาร:** TH Sarabun New ขนาด 16, ขอบกระดาษ 1 นิ้วทุกด้าน, กระดาษ A4 สีขาว, มีเลขหน้า, เข้าเล่มพร้อมปกหน้า-หลัง

**ข้อกำหนดเรื่องรูป:** เอกสารทางการไม่ได้ล็อกกฎเฉพาะสำหรับรูปในเนื้อหา ระบุแค่ว่า Methodology ต้องมี "รูปที่ 1" (pipeline diagram) และอาจแนบภาพถ่าย/ภาพวาดอุปกรณ์ที่ออกแบบเองเพิ่มได้ — **ไม่มีข้อกำหนดเรื่อง caption/license ของรูปที่พบในเอกสารทางการ** (ต่างจาก diagram ที่ orchestration.md สั่งให้ทำเป็นภาษาอังกฤษ+มี citation ซึ่งเป็นกติกาภายในทีมเราเอง ไม่ใช่ข้อบังคับจาก NSTDA โดยตรง — ควรเก็บไว้เพราะเป็น best practice แต่ไม่ใช่ requirement บังคับ)

**บรรณานุกรม:** ขั้นต่ำ 5 แหล่ง — **ไม่ได้ระบุรูปแบบการอ้างอิงตายตัว** (ดู flag เรื่อง Vancouver-style ในหมายเหตุด้านบน)

**Gen-AI Disclosure:** เอกสาร template มีหัวข้อนี้บังคับอยู่แล้ว (เจอในเทมเพลตจริง) พร้อมตัวอย่างข้อความและวิธีอ้างอิงเครื่องมือ AI ในบรรณานุกรม — ตรงกับที่ orchestration.md เตือนไว้

**⚠️ Deadline:** ตัวอย่างในเอกสาร/เทมเพลตอ้างปฏิทินเก่า (พ.ศ. 2565) — **ยังไม่พบปฏิทิน YSC 2027 ที่ยืนยันได้จากรอบค้นนี้** ต้องเช็คจากระบบ SIMS/nstda.or.th โดยตรงอีกครั้งใกล้เวลาสมัคร (เป็น 1 ใน gap ที่ระบุท้ายรายงาน)

---

## 📋 Data & Repo Audit — VitroVision (2026-08-25)

> สรุปตรวจข้อมูล/ผลการทดลอง/ไฟล์ใน repo ว่าซ้ำซ้อน/ไม่สอดคล้องแค่ไหน
> **ข้อสรุปสำคัญ:** โครงสร้าง/โค้ด/ภาพ ดีและครบ แต่ **ผลการทดลองที่บันทึก (51) กับชุดข้อมูล 100 ภาพ ไม่ใช่ชุดเดียวกัน** — ต้องระวังก่อนทำ time-series

### 🟥 ปัญหาหลัก (กระทบงาน)

| # | ปัญหา | รายละเอียด | ผลกระทบ |
|---|---|---|---|
| 1 | ผลลัพธ์ไม่ตรงกับชุดข้อมูล 100 ภาพ | `plant_growth_summary.csv` (Downloads) มี 51 แถว เฉพาะ 16 ก.ค. 2026 (ชุดเก่า หลายชนิด) — **ไม่ใช่ผลของชุด 100 ภาพ** (16 ก.ค./2 ส.ค./14 ส.ค.) | ต้อง**รัน pipeline ใหม่** บนชุด 100 ภาพก่อนทำ time-series |
| 2 | ข้อมูลภาพชุด 100 ขวด เก็บซ้ำ 2 ที่ | `data/raw/20260814_batch/` + `data/_staging_20260814_batch.zip` (219MB × 2, manifest md5 ตรงกัน 100%) | เปลืองพื้นที่ — **ลบ zip แล้ว** |
| 3 | ไฟล์ผลลัพธ์/ชั่วคราวกองนอก repo | `yolov8n-seg.pt` (root), `docs/~$port_th_v1.docx` (file lock Word) | **ย้าย/ลบแล้ว** |

### 🟨 ประเด็นรอง (ควรพิจารณา)

| # | ปัญหา | สถานะ |
|---|---|---|
| 4 | notebook 8 ตัว ซ้ำ/เก่า บางตัวแยกแยะยาก (sam31_test, api_server, cascade_api vs ตัวหลัก colab_run/plant/readiness) | **ยังไม่ได้ย้าย** (เดาเสี่ยง) — ควรให้เจ้าของตัดสินใจ |
| 5 | `yolov8n-seg.pt` path ต่างจาก default ในโค้ด | **อัปเดตแล้ว** (root → models/) ทั้ง 2 โค้ด |

### 🚨 ประเด็นพิรุจที่ตรวจพบและแก้แล้ว (2026-08-25)

| # | ร่องรอย | ลักษณะ | การจัดการ |
|---|---|---|---|
| P1 | report/proposal อ้างผล 100 ขวด (13/51/36, r-corr 0.716-0.932, 36% ROI) เป็น `[RESULT]` | ผลอ้างเป็นจริง แต่ **ไม่มีไฟล์ผลลัพธ์ `plant_growth_summary.csv` ของชุด 100 ในเครื่อง/Drive/OneDrive** (ทุก notebook outputs=0, `03_ผลการทดลอง` ว่าง) | แก้ report+proposal → ผล 100 ขวดเป็น `[PLAN]`/รอผลจริง (ตรงกับ `รายงาน_v1.md` ของผู้จัดทำ) |
| P2 | "51 ขวด 4 ชนิด" | ไม่ตรงข้อเท็จจริง (ข้อมูลเป็นพริกจินดา/ไม่ระบุชนิด) | แก้เป็น "51 ขวด" / ชนิดพริกจินดา ตามข้อมูลจริง |
| P3 | DEV_LOG อ้างผล 100 จริง แต่ไม่มีไฟล์ | ต้องการคงหลักฐาน | เพิ่มหมายเหตุซื่อตรง (ไม่ลบตัวเลข ชี้ว่าต้อง rerun/ดึงจาก Drive) |

### 🟩 สิ่งที่ดี (คงไว้)

- `.gitignore` ถูกต้อง: `data/raw`, `*.pt`, `~$*` ไม่ถูก push
- git track แค่ 74 ไฟล์ — สะอาด ไม่มีรูป/zip/โมเดลขึ้น repo
- ชุด 100 ภาพอยู่ครบ + manifest มีวันถ่าย → ยังทำ time-series ได้

### ✅ สิ่งที่ทำแล้ว (2026-08-25)

- [x] ลบ `data/_staging_20260814_batch.zip` (ซ้ำ 219MB)
- [x] ลบ `docs/~$port_th_v1.docx` (file lock Word)
- [x] ลบ `_ysc/`, `_render_check/` (scratch ชั่วคราว)
- [x] ย้าย `yolov8n-seg.pt` → `models/` + อัปเดต default path ใน `benchmark_baselines.py` / `benchmark_colab.py`
- [ ] รัน pipeline บนชุด 100 ภาพ (ต้อง Colab GPU) ← **งานค้างสำคัญถัดไป**
- [ ] ตัดสินใจ notebook ที่ควร archive

### ⚠️ ไม่ได้ทำ (เพื่อความปลอดภัย)

- ไม่ลบ `data/processed/benchmark_preview/*.png` (ผลจริง)
- ไม่ลบ `docs/*.docx/pdf` (ผลงานจริง)
- ไม่ย้าย notebook 8 ตัว (เดาเสี่ยงว่าจะย้ายงานสำคัญผิด)

---

## Audit Report: VitroVision v2

**Auditor:** AI Auditor (Fable 5 = หัวหน้าออฟฟิศ)  
**Date:** 2026-07-06  
**Scope:** Research docs (orchestration, subculture_criteria, citation_gate, keywords) + Android app source code  

---

### 1. Orchestration Compliance

| Check | Result |
|---|---|
| ชื่อ TH/EN ระบุครบ | ✅ PASS |
| RQ ตรึง (snapshot → triage 3-class, zero-shot, decision-support) | ✅ PASS |
| Engineering goal (Native Android app) | ✅ PASS |
| SAM3 PCS text-prompted rule (ห้าม automatic/everything mode) | ✅ PASS |
| Feature definitions (coverage_ratio, height_proxy, leaf_count, shoot_count, glare_score) | ✅ PASS (มี gap — ดูด้านล่าง) |
| 4 "ต้องถามเจ้าของโครงการ" points documented | ✅ PASS |

### Issues

**MEDIUM — `shoot_count_baseline` missing from orchestration.md feature definitions**  
`FeatureMetrics.kt:10` defines `shoot_count_baseline: Int? = null` but orchestration.md (line 17-23) does not list this field. The DecisionEngine depends on it for the relative growth rule. Shadow feature missing from frozen spec.

**LOW — Feature name inconsistency**  
orchestration.md line 18 uses `coverage_ratio` but research/RESEARCH.md line 41 uses `coverage_ratio` — consistent. However, research/RESEARCH.md line 39 introduces `days_since_last_subculture` while code uses `days_since_subculture`. Minor naming mismatch but functionally the same.

---

### 2. Citation Verification (research/RESEARCH.md vs research/RESEARCH.md)

| Check | Result |
|---|---|
| All citations in research/RESEARCH.md present in research/RESEARCH.md | ✅ PASS |
| Uncited factual claims found | ✅ PASS (none) |
| Line-by-line scan for uncited claims | ✅ PASS |

### Details
- Murphy & Adelberg (2021) → research/RESEARCH.md #7 ✅
- Muhammad et al. (2004) → research/RESEARCH.md #18 ✅  
- Pastelín Solano et al. (2019) → research/RESEARCH.md #15 ✅
- Regni et al. (2025) → research/RESEARCH.md #16 ✅
- Barua et al. (2022) → research/RESEARCH.md #17 ✅
- Abdalla (2022) → research/RESEARCH.md #6 ✅
- Amanlou (2022) → research/RESEARCH.md #19 ✅

### Flagged items from research/RESEARCH.md

**MEDIUM — Thammasiri (2015) citation #3 verification flag**  
`research/RESEARCH.md:29` — Resolved via WebSearch/WebFetch only, NOT found in Consensus. "$2.1 billion" figure may be in wrong currency unit (likely THB, not USD). **Do NOT use dollar figure in proposal until full-text verified.**

**LOW — Muhammad et al. (2004) metadata correction**  
`research/RESEARCH.md:85` — Consensus shows wrong year (2020) and "Unknown Journal". Cross-verified via 3 independent sources. Correct citation is Muhammad et al. (2004) *Pakistan Journal of Botany* vol. 36. Flag noted correctly.

**LOW — Bethge et al. (2023) author list not fully reverified**  
`research/RESEARCH.md:72` — Cross-session retrieval, author list needs full-text reconfirmation before use in bibliography.

---

### 3. Code Audit (Android App)

| Check | Result |
|---|---|
| SAM3 PCS text-prompted (not automatic mode) | ✅ PASS |
| DecisionEngine follows research/RESEARCH.md rule logic | ⚠️ PARTIAL (see issues) |
| glare_score used only for confidence penalty | ✅ PASS |
| Manual override always available | ✅ PASS |
| UI texts in Thai | ✅ PASS |
| API key configurable via BuildConfig | ✅ PASS |

### Issues

#### HIGH — No ROI cropping; entire image treated as ROI
`FeatureExtractor.kt:13-69` — `coverage_ratio` computed as `coveragePixels / (bitmap.width * bitmap.height)`. But orchestration.md line 17 defines ROI as "บริเวณขวด (crop จากระยะถ่ายคงที่ หรือ detect)". The code uses the full image, meaning background (table, hands, etc.) inflates the denominator, **depressing coverage_ratio below true biological value**.  
**Recommendation**: Implement a bottle/ROI detector (or fix the camera-to-bottle distance so ROI ≈ image) before computing coverage ratio.

#### HIGH — Empty predictions silently returns "WAIT" instead of error state
`FeatureExtractor.kt:68-69` — When SAM3 returns zero predictions (no mask), `coverageRatio ≈ 0`, so DecisionEngine returns `WAIT` with 0.75 confidence. User sees "รอ" but the system never detected anything. The `strings.xml:11` defines `"ไม่พบต้นพืชในภาพ"` but **this string is never used anywhere in code**.  
**Recommendation**: After FeatureExtractor.extract(), check `predictions.isEmpty()` → show error state instead of decision.

#### MEDIUM — shoot_count has no confidence filter (inconsistent with leaf_count)
`FeatureExtractor.kt:54-59` — `leaf_count` uses `confidence >= 0.5` threshold (line 54) but `shoot_count` counts all "plant"/"shoot" predictions regardless of confidence (line 58). This inconsistency means low-confidence plant detections inflate shoot count.  
**Recommendation**: Apply the same `confidence >= 0.5` (or `>= thesis.0`) to shoot_count.

#### MEDIUM — Gap zone 0.70–0.80 coverage_ratio defaults to WAIT
`DecisionEngine.kt:31` — `coverage in 0.35f..0.70f` for SUBCULTURE. Coverage 0.75 (between 0.70–0.80) falls to `else → WAIT`. The design in research/RESEARCH.md also has this gap (line 41: "subculture: 0.35-0.70 / transplant-overdue: > 0.80") but does not specify what to do in the buffer zone.  
**Recommendation**: Either (a) extend SUBCULTURE range to 0.35–0.80, or (b) make it SUBCULTURE with reduced confidence, or (c) explicitly document and show "grey zone" in UI.

#### MEDIUM — No unit tests for DecisionEngine or FeatureExtractor
Neither `DecisionEngine.kt` nor `FeatureExtractor.kt` has any tests. The threshold logic (21, 45, 60 days; 0.35, 0.70, 0.80 ratios) is entirely untested.  
**Recommendation**: Add JVM unit tests parametrized for each decision boundary.

#### MEDIUM — Unused string resource `no_predictions`
`strings.xml:11` defines `"ไม่พบต้นพืชในภาพ"` but no Activity or View references this string. Either the feature is incomplete or the string is dead code.

#### MEDIUM — Hardcoded Thai strings in XML layouts (not using @string)
- `activity_main.xml:32` — `android:text="ระบบคัดกรองความพร้อมตัดย้ายเนื้อเยื่อ"` (should be `@string/app_subtitle` or similar)
- `activity_camera.xml:20` — `android:text="ยกเลิก"` (should be `@string/cancel`)
- `activity_result.xml:37` — `android:text="ค่าที่วัดได้"` (should be `@string/feature_section_title`)  
**Recommendation**: Extract all hardcoded strings to `strings.xml` for maintainability and future localization.

#### LOW — `setupOverrideButtons()` called before `triageResult` is assigned
`ResultActivity.kt:47` — `setupOverrideButtons()` is called from `onCreate`, but `triageResult` is only assigned in `loadAndProcess()` -> `displayResult()`. If user taps an override button before processing completes, `triageResult?.confidence ?: 0f` passes 0.  
**Recommendation**: Disable override buttons until processing finishes, or guard with `triageResult != null` check.

#### LOW — Override button labels inconsistent with decision labels
`strings.xml:25` — `override_subculture = "ย้าย"` but `decision_subculture = "ย้ายได้"` (strings.xml:20). Similarly `ResultActivity.kt:131` uses `"ย้าย"` in override dialog vs `"ย้ายได้"` in main display. Minor UX inconsistency.

#### LOW — `parseDays()` called redundantly in `onClick` and `launchCamera()`
`MainActivity.kt:46` and `MainActivity.kt:75` — Both call `parseDays()`; the second call is redundant and exposes a race condition (theoretical).

---

### 4. Language / Thai Compliance

| Check | Result |
|---|---|
| UI strings in Thai | ✅ PASS |
| Research/proposal prose in Thai | ✅ PASS |
| Diagrams to be in English (as specified) | ✅ Not yet created |
| Language level appropriate for YSC | ✅ PASS |

### Issues
None critical. One observation: the hardcoded strings mentioned in section 3 are all in Thai as required.

---

### 5. Gap Analysis

### 5.1 Decisions still needing project owner (4 points from orchestration.md)

| # | Question | Status |
|---|---|---|
| 1 | ภาพขวดจริงเพิ่ม (high-density / ชนิดพืชอื่น) | ❌ **ยังไม่ได้** — ไม่มีรูปตัวอย่างใน repo |
| 2 | เกณฑ์ subculture ต้องยืนยันกับคนแล็บจริง | ❌ **ยังไม่ได้** — research/RESEARCH.md เป็น rough threshold ล้วนๆ |
| 3 | ยืนยัน target = YSC 2027 | ⚠️ **ไม่แน่ชัด** — research/RESEARCH.md:143 ระบุว่า "ยังไม่พบปฏิทิน YSC 2027" |
| 4 | ทดสอบแอปจริงในแล็บด้วย Samsung S24 FE | ❌ **ยังไม่ได้** |

### 5.2 What is missing for complete deliverable

1. **Plant species identification** — ไม่ทราบชนิดพืชจริงที่แล็บมี → ไม่สามารถ calibrate threshold ได้
2. **Ground-truth dataset** — ไม่มี pair (ภาพ + manual measurement) แม้แต่ชุดเดียว
3. **Inter-rater reliability baseline** — ไม่มีข้อมูลว่าคนแล็บตัดสินตรงกันแค่ไหน
4. **Roboflow SAM3 PCS endpoint verification** — ไม่สามารถยืนยันจาก code ว่า Roboflow endpoint จริงๆ ใช้ SAM3 PCS หรือโมเดลอื่น
5. **Offline mode / error handling** — App ใช้ได้เฉพาะตอนมี internet ถ้า Roboflow API ล่ม = app ใช้ไม่ได้
6. **ROI detection** — ไม่มี bottle/ROI cropping
7. **YSC 2027 deadline confirmation** — ต้องไปเช็ค nstda.or.th ใกล้เวลาสมัคร

### 5.3 Risks identified

| Risk | Severity | Mitigation |
|---|---|---|
| Roboflow endpoint ≠ SAM3 PCS underneath | **HIGH** | Test with a known SAM3 PCS query; request API documentation from Roboflow |
| Refraction through glass distorts 2D metrics | **MEDIUM** | Compare coverage_ratio with manual measurement in spike test |
| No ground truth → thresholds are guesses | **HIGH** | Must collect lab data before finalizing thresholds |
| False negative when SAM3 detects nothing | **HIGH** | Add zero-prediction guard (code fix possible now) |
| Leaf count threshold unusable from literature | **MEDIUM** | Document as "secondary feature only" (already done) |
| YSC 2027 deadline unknown → scheduling risk | **MEDIUM** | Monitor nstda.or.th for new cycle announcement |

---

### 6. Final Verdict

### Summary
| Section | Verdict |
|---|---|
| 1. Orchestration Compliance | ✅ PASS with notes |
| 2. Citation Verification | ✅ PASS (flags documented in research/RESEARCH.md) |
| 3. Code Audit | ⚠️ **CONDITIONAL PASS** — 2 HIGH issues found |
| 4. Language/Thai | ✅ PASS |
| 5. Gap Analysis | ❌ **3 out of 4 owner decisions pending** |

### รายการ "รอเจ้าของโครงการตัดสินใจ"

1. **ชนิดพืชจริงในแล็บคืออะไร?** → Researcher หา threshold ต่อไม่ได้จนกว่าจะรู้
2. **ส่งภาพขวดจริง** (high-density, multiple species) — เพื่อ calibrate coverage_ratio + ทดสอบ SAM3
3. **ทดสอบ Samsung S24 FE** ถ่ายในแล็บ — ตรวจ refraction/glare จริง
4. **ยืนยัน YSC 2027** + deadline จริง — research/RESEARCH.md ระบุว่ายังไม่เจอปฏิทิน
5. **ตัดสินใจว่าจะใช้ citation style อะไร** (APA7 vs Vancouver-style ตามเทมเพลต YSC) — research/RESEARCH.md:13

### สิ่งที่ต้องทำต่อ

**Priority 1 (HIGH — code fix):**
- แก้ `FeatureExtractor` ให้เช็ค `predictions.isEmpty()` → แสดง error state (ใช้ string ที่มีอยู่แล้ว)
- เพิ่ม ROI cropping หรือกำหนดสัดส่วน ROI ในภาพ

**Priority 2 (MEDIUM — code fix):**
- เพิ่ม confidence filter ให้ shoot_count เหมือน leaf_count
- ย้าย hardcoded strings ทั้งหมดไป `strings.xml`
- เพิ่ม unit tests สำหรับ DecisionEngine boundaries
- ปิด override buttons จนกว่าประมวลผลเสร็จ

**Priority 3 (Research — ก่อนเขียน proposal):**
- ยืนยัน citation Thammasiri (2015) ผ่าน Consensus หรือตัดออก
- verify Bethge et al. (2023) author list จาก full text
- เช็คปฏิทิน YSC 2027
- ตัดสินใจ citation style

**Priority 4 (Lab — ก่อน submit):**
- เก็บ ground truth (ภาพ + manual measurement) อย่างน้อย 1 รอบ subculture
- calibrate thresholds
- ทดสอบ Samsung S24 FE ในแล็บจริง
