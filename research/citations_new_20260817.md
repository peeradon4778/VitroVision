# 📚 Citations ใหม่ รอบ 2026-08-17 — งาน ≤5 ปี (2021–2026), แนวทาง AI + การเกษตร

> กฎรอบนี้: **เฉพาะงานวิจัยอายุไม่เกิน 5 ปี + แนวทางปรับใช้ AI กับเทคโนโลยีการเกษตร**
> สถานะ: ✅ = verify แล้ว (เปิด paper จริง + DOI/URL กดได้) · ⚠️ = ยังต้อง verify เพิ่ม
> ตรวจโดย: ทีมวิจัย (web_explore/web_search/fetch_content + อ่าน full text)

---

## หมวด 1 — ⭐ หลักฐานตรงสุด: SAM3 ใช้กับ plant segmentation ได้จริง

### 1. Orvati Nia et al. 2026 (bioRxiv preprint) ✅ — ใช้ในบทนำ/ระเบียบวิธี
- **Title:** A Data-Driven Image Extraction and Analysis Pipeline for Plant Phenotyping in Controlled Environments
- **ผู้แต่ง:** Fahimeh Orvati Nia, Joshua Peeples, Seth C. Murray, et al. (Texas A&M University)
- **แหล่ง:** bioRxiv (preprint, โพสต์ 21 ก.ค. 2026) · DOI: https://doi.org/10.64898/2026.02.25.707797
- **ประเด็นสำคัญ (อ่าน full text แล้ว):**
  - เปรียบเทียบ BEN v2, BiRefNet, SAM v2.1, **SAM v3**, YOLOv11, YOLOv12 บน PGP v2 (ข้าวโพด/ฝ้าย/ข้าว/ข้าวฟ่าง ~53,404 ภาพ)
  - **"Among the evaluated segmentation approaches, SAM v3 provided the highest and most consistent accuracy across diverse crop structures"** — SAM3 ชนะสุดในความแม่นยำข้ามโครงสร้างพืช
  - **ใช้ SAM v3 แบบ detector-free + text prompt "plant" (ตรงกับวิธีของเรา!)** — ยืนยันแนวทาง text-prompt ของ VitroVision
  - ข้อเสีย: ใช้เวลาคำนวณมากกว่า classical/CNN
  - 863-dimensional feature vector ต่อต้น (vegetation indices + texture + morphology)
  - Pipeline open-source: github.com/Advanced-Vision-and-Learning-Lab/Plant_Analysis_Tool_Pipeline

### 2. Carion et al. 2025 — SAM 3 paper ทางการ ✅ (อ้างโมเดล)
- **Title:** SAM 3: Segment Anything with Concepts
- **แหล่ง:** arXiv:2511.16719 (2025) · https://arxiv.org/abs/2511.16719
- **ประเด็น:** 848M params, Promptable Concept Segmentation (PCS), presence token แยก concept ใกล้เคียง, SA-Co benchmark 270K concepts, ได้ 75–80% ของมนุษย์; SAM 3.1 ออก มี.ค. 2026 (เร็วขึ้น ~7x)
- ⚠️ License = SAM License (ไม่ใช่ MIT/Apache — ต้องเช็คก่อนตีพิมพ์)

---

## หมวด 2 — Zero-shot / foundation model กับ segmentation พืช (2025–2026)

### 3. Segment Any Plant (SAP) ✅
- bioRxiv 2026 · DOI: https://doi.org/10.64898/2026.03.11.711099
- SAM2 few-shot training-free, time-series plant segmentation: Arabidopsis, root, sunflower
- **mean IoU 0.89–0.93 จาก single-frame prompting** — foundation model segment พืชได้แม่น
- ใช้ใน: related work (งานก่อน SAM3 ในตระกูลเดียวกัน)

### 4. Text guidance is powerful but prompt-sensitive for weakly-supervised leaf symptom segmentation ✅ (ใช้ในข้อจำกัด!)
- bioRxiv 2026 · DOI: https://doi.org/10.64898/2026.07.10.737680
- SAM3 เป็น weak supervision สำหรับ segment อาการโรคใบ — **พบว่า prompt-sensitive: ผลขึ้นกับคำ prompt มาก**
- ใช้ใน: ข้อจำกัด/อภิปราย — สนับสนุนการออกแบบ prompt ให้รอบคอบ (ของเรามี 5 prompts)

### 5. Zero-shot instance segmentation for plant phenotyping in vertical farming ✅
- Front. Plant Sci. 2025 · DOI: https://doi.org/10.3389/fpls.2025.1536226
- Grounding DINO + SAM, VC-NMS — zero-shot segmentation ใน vertical farm
- ใช้ใน: related work (zero-shot แนวทางเดียวกับเรา ต่าง environment)

### 6. ZeroPlantSeg (Junhao Xing et al.) ⚠️ (verify arXiv ยัง)
- arXiv:2509.09116 · https://arxiv.org/abs/2509.09116
- Zero-shot hierarchical plant segmentation + text-to-image attention
- ยังไม่ได้อ่าน full — เปิด link ก่อนเข้า report

---

## หมวด 3 — AI + Tissue culture / micropropagation (2024–2025)

### 7. Diningrat et al. 2024 — AI ประเมิน growth ของ potato microtuber จากภาพ ✅
- J. Phys. Conf. Ser. 2908 012001 (ICASMA 2024) · DOI: https://doi.org/10.1088/1742-6596/2908/1/012001
- Digital imagery + AI ประเมินการเจริญ microtuber มันฝรั่งใน tissue culture
- ใช้ใน: related work ไทย/ระดับนานาชาติ งาน AI+TC

### 8. Regni et al. 2025 — smartphone 3D imaging + subculture duration (blackberry/blueberry) ✅ (มีในไฟล์เก่าแล้ว)
- Plant Cell Tiss Organ Cult · DOI: https://doi.org/10.1007/s11240-025-03267-0
- ใกล้เคียงเราที่สุด: วัด canopy/covered area ต่อขวด + shoot density เทียบ subculture duration

### 9. Bethge et al. 2023 — "Phenomenon" ✅ (มีในไฟล์เก่าแล้ว)
- Plant Methods 19:42 · https://doi.org/10.1186/s13007-023-01018-w
- multi-sensor phenotyping ในขวด TC แบบ non-destructive; 60–70% ต้นทุน micropropagation = แรงงานคน

---

## หมวด 4 — งานสนับสนุนอื่น (จากไฟล์ verify เดิม, ทุกตัว ≤5 ปี)

อ้างอิงไฟล์เดิม (ทั้งหมด verify 2026-08-06, อายุ ≤5 ปี):
- `citations_benefits_20260806.md` — 9 ตัว: Murphy 2024 (Annu. Rev. Plant Biol. 75:771), Nguyen 2025 (Plants 14:907), Peters 2023 (Sci. Rep.), Zhang 2026 (Sci. Data 13), Papoutsoglou 2023, Shoaib 2025, Wang & Ghatrehsamani 2026
- `citations_colab_20260806.md` — 14 ตัว: Rippner 2022, Jawed 2026 (Sci. Rep. 16:9704), ZeroCostDL4Mic 2021, Carneiro Pessoa 2018* (*>5 ปี — ใช้เฉพาะถ้าจำเป็น), Samuel & Mietchen 2024, ColabPCR 2026, Caprarelli 2023
- `citations_dataset_size_20260806.md` — Egi & Öter 2026 (Plants 15:47, YOLO-seg callus 122 ภาพ), Sapkota 2025 (SAM3 vs YOLO11, arXiv:2512.11884), Li 2023, Williams 2024, Aubreville 2024

---

## ⚠️ งานที่เห็นแต่ยังไม่ verify (ห้ามอ้างก่อน verify)
- **AgriSAM3 (Sapkota et al. 2025)** — README ใช้ arXiv placeholder "XXXX.XXXXX" → ต้องหาหมายเลขจริงก่อนอ้าง
- **Intelligent control system for clonal micro-propagation (2025, IJIRSS)** — วารสารไม่น่าเชื่อถือ → งด
- **Text-conditioned Segmentation for Tomato via Procedural Synthetic Data (arXiv 2607.18576)** — ตัวเลข arXiv ผิดปกติ → งด

---

## แผนใช้ในรายงาน
| ส่วน | ใช้ตัวไหน |
|---|---|
| บทนำ: ปัญหาแรงงาน/ความแปรปรวน | Bethge 2023, Murphy 2024, Nguyen 2025, Zhang 2026 |
| บทนำ: ช่องว่างงานวิจัย | Bethge 2023, Regni 2025, Diningrat 2024 |
| ระเบียบวิธี: ทำไม SAM3 | **Orvati Nia 2026** ⭐, Carion 2025 |
| Related work: zero-shot/foundation | SAP 2026, Zero-shot vertical 2025, ZeroPlantSeg 2025 |
| ข้อจำกัด: prompt sensitivity | **Text guidance 2026** ⭐ |
| วิธี: Colab/reproducibility | Rippner 2022, Jawed 2026, ZeroCostDL4Mic 2021 |
