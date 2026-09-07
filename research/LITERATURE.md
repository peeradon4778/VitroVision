# LITERATURE — VitroVision: References / บรรณานุกรมอ้างอิงรวม

> รวมไฟล์เดิม: citations_20260806 · citations_benefits_20260806 · citations_colab_20260806 · citations_dataset_size_20260806 · citations_new_20260817


---

## 📚 Citations รอบใหม่ — VitroVision v2 (verify 2026-08-06)

> สืบค้นโดยทีมวิจัยตามกฎ citation เหล็ก (Consensus + PubMed + verify DOI/URL) — **19 ตัว ✅ verify แล้ว**
> ผู้ใช้กำลังอ่านงานจริงอีกรอบเพื่อคัดเลือกก่อนเข้าบรรณานุกรม
> อ้างอิงเก่า (Yang 2024 / Li 2022 / Wang 2025 / Tong 2023 / Bethge 2023) ถูกโล๊ะจาก research/RESEARCH.md แล้ว

---

### หมวด 1 — Non-destructive phenotyping ของ plant tissue culture
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Bethge et al., "Phenomenon" low-cost multi-sensor phenotyping of in vitro culture | 2023 | Plant Methods | https://doi.org/10.1186/s13007-023-01018-w |

⚠️ ยังไม่มีงาน 2025–2026 เจาะจง phenotyping พืชในขวด TC ผ่าน glass container โดยตรง → ช่องว่าง = **novelty ของเรา**

### หมวด 2 — SfM / photogrammetry / multi-view plant phenotyping
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Photogrammetric apparatus + robotic arm (routine morphological analysis) | 2025 | Plant Methods | https://doi.org/10.1186/s13007-025-01445-x |
| 3D reconstruction binocular camera, self-occlusion handling | 2025 | Front. Plant Sci. | https://doi.org/10.3389/fpls.2025.1642388 |
| Zhuo & You — PlantMDE: 3D phenotyping จาก single image (monocular depth) | 2025 | Comput. Electron. Agric. | https://doi.org/10.1016/j.compag.2025.110925 |
| Hrzich et al. — low-cost SfM photogrammetry wheat (point cloud) | 2025 | arXiv | https://arxiv.org/abs/2504.16840 |

### หมวด 3 — 3D Gaussian Splatting (3DGS) / NeRF สำหรับ plant phenotyping
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| **PlantGaussian** — Shen, Jing, Deng, Jia, Wu | 2025 | Crop Journal 13:607–618 | https://doi.org/10.1016/j.cj.2025.01.011 |
| Li et al. — Survey: classical → NeRF → 3DGS in plant phenotyping | 2025 | Plant Phenomics 7:100137 | https://doi.org/10.1016/j.plaphe.2025.100137 |
| Seed 3D: panoramic video + SfM + 3DGS (maize/wheat/rice) | 2025 | Agriculture 15(22):2329 | https://doi.org/10.3390/agriculture15222329 |
| Li et al. — Object-Centric 3DGS strawberry (video + SAM-2) | 2025 | arXiv | https://arxiv.org/abs/2511.02207 |
| **Wheat3DGS** — Zhang et al. (ETH Zürich) | 2025 | CVPR Workshops | https://doi.org/10.1109/CVPRW67362.2025.00533 |
| Chen et al. — Sugarcane 3D phenotyping: instance seg + 3DGS | 2026 | Agriculture 16(3):375 | https://doi.org/10.3390/agriculture16030375 |

### หมวด 4 — Transparent object / refraction-aware 3D reconstruction (ต่อจาก Tong 2023)
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Surface reconstruction ของ**ขวดแก้ว**ด้วย neural implicit | 2026 | J. Intell. Manuf. 37(7):2903–2918 | https://doi.org/10.1007/s10845-025-02668-4 |
| Tian et al. — Geometry-aware Gaussian Splatting ของ transparent objects | 2026 | Eng. Appl. Artif. Intell. | https://doi.org/10.1016/j.engappai.2026.113787 |
| **TSGS** — normal + de-lighting priors สำหรับ transparent surface | 2025 | ACM MM pp 7220–7229 | https://doi.org/10.1145/3746027.3754548 |

### หมวด 5 — SAM2 / SAM3 / foundation segmentation models สำหรับพืช
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Abbey & Meroz — **Segment Any Plant (SAP)**: SAM2 few-shot สำหรับ plant time-series | 2026 | bioRxiv | https://doi.org/10.64898/2026.03.11.711099 |
| **EMSAM** — Enhanced Multi-Scale SAM สำหรับ leaf disease segmentation | 2025 | Front. Plant Sci. | https://doi.org/10.3389/fpls.2025.1564079 |
| Vashisht et al. — SAM-2 สำหรับ grape leaf segmentation | 2025 | LNNS (SmartCom 2025) pp 375–386 | https://doi.org/10.1007/978-981-96-7517-3_32 |

### หมวด 6 — 3D traits vs 2D projected area
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| van Marrewijk et al. — เทียบ 2D-to-3D segmentation vs 3D segmentation | 2025 | Biosystems Engineering | https://doi.org/10.1016/j.biosystemseng.2025.104147 |

### เสริม
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Review: 3D crop phenotyping ด้วย point cloud (CCP vs FCP) | 2026 | Front. Plant Sci. | https://doi.org/10.3389/fpls.2026.1731852 |

---

### จับคู่กับส่วนของข้อเสนอ
- **บทนำ (phenotyping gap):** Bethge 2023 · Survey Plant Phenomics 2025 · Review 2026
- **บทนำ (novelty):** 3DGS/วิดีโอ 2025–2026 → "มีคนทำ 3DGS กับพืชแล้ว แต่ยังไม่มีใครทำในขวดแก้ว TC"
- **ระเบียบวิธี (เก็บภาพ):** Seed video+SfM+3DGS · Photogrammetric apparatus · Strawberry video 3DGS
- **ระเบียบวิธี (segment):** SAP · SAM-2 grape · EMSAM
- **ระเบียบวิธี (refraction):** ขวดแก้ว neural implicit · geometry-aware 3DGS · TSGS
- **การวิเคราะห์ (3D vs 2D):** van Marrewijk · PlantMDE

### ⚠️ 3 จุดที่ต้องปิดก่อนเขียนอ้างอิงจริง
1. **TSGS ACM MM** (10.1145/3746027.3754548) — author ชื่อเต็มถูกตัด ต้องดึงใหม่ ห้ามเดา
2. **Plant Methods 2025** (10.1186/s13007-025-01445-x) + **Front. Plant Sci. 2025** (10.3389/fpls.2025.1642388) — author list บางส่วนถูกตัด ต้องดึงชื่อเต็ม
3. **arXiv 2 ตัว** (2504.16840, 2511.02207) — ใช้ URL arXiv อย่างเดียว ห้ามใช้ DOI 10.48550 (CrossRef 404)
4. อย่าอ้างว่า "มีงาน 3D traits vs 2D vs manual ใน TC" — ยังไม่มี → ใช้ van Marrewijk (ใกล้เคียง) + ชี้ novelty

---

## 📚 Citations: เหตุผล "AI/CV แปลงข้อมูลชีววิทยาเป็นดิจิทัลมีประโยชน์" (verify 2026-08-06)

> สืบค้นโดยทีมวิจัย — **9 ตัว ✅ verify ครบ** (PubMed/doi.org/หน้า publisher จริง)
> ใช้ในบทนำ: สนับสนุนว่าทำไม digital phenotyping ด้วยโมเดลถึงมีประโยชน์

---

### ตาราง (เรียงตามความสำคัญ)
| # | Paper | ปี | วารสาร | DOI/URL | ชี้ประโยชน์ด้าน |
|---|---|---|---|---|---|
| 1 | **Bethge et al. "Phenomenon"** — phenotyping ผ่านขวด TC ไม่เปิดฝา รักษาสภาพปลอดเชื้อ + **60–70% ของต้นทุน micropropagation = แรงงานคน** | 2023 | Plant Methods 19:42 | https://doi.org/10.1186/s13007-023-01018-w | ⭐ ตรงงานที่สุด: non-destructive ในขวด TC + ตัวเลขต้นทุน |
| 2 | **Murphy et al.** — บททบทวนหลัก: image-based HTP nondestructive + ลดแรงงาน; DL ดึงข้อมูลจากภาพ | 2024 | Annu. Rev. Plant Biol. 75:771 | https://doi.org/10.1146/annurev-arplant-070523-042828 | ลดแรงงาน + non-destructive |
| 3 | **Nguyen et al.** — manual/labor-intensive + destructive เพิ่ม human error ขัดขวางติดตามต่อเนื่อง; HTP ให้ real-time, accuracy & consistency สูงกว่า; ต่อยอด GWAS/breeding | 2025 | Plants 14(6):907 | https://doi.org/10.3390/plants14060907 | ครบห่วงโซ่: 1+2+3+5 |
| 4 | Meraj et al. — manual measurement "not reliable, not precise", tedious ในสเกลใหญ่ | 2024 | iScience 27:108709 | https://doi.org/10.1016/j.isci.2023.108709 | ข้อ 1 |
| 5 | **Peters et al.** — CNN ตรวจจับราก ดีเท่า human expert แต่ efficient + reproducible | 2023 | Sci. Rep. 13 | https://doi.org/10.1038/s41598-023-28400-x | ⭐ objectivity (ข้อ 3) |
| 6 | **Zhang et al.** — AI vs 5 ผู้เชี่ยวชาญ: observer bias จำกัด reproducibility; โมเดล 100% internal consistency; ลด bias/ค่าแรง | 2026 | Scientific Data 13(1) | https://doi.org/10.1038/s41597-026-06926-9 (arXiv:2507.11279) | ⭐ objectivity หลักฐานตรงสุด |
| 7 | Papoutsoglou et al. — ข้อมูล phenotyping แบบ FAIR นำกลับมาใช้ใหม่ได้ (meta-analysis, QTL) | 2023 | Scientific Data 10:457 | https://doi.org/10.1038/s41597-023-02364-z | ข้อมูลต่อยอด (ข้อ 5) |
| 8 | Shoaib et al. — การตรวจ visual "subjective, prone to evaluator bias"; optical sensing+ML เห็นการเปลี่ยนแปลงก่อนมีอาการ | 2025 | Front. Plant Sci. 16:1670593 | https://doi.org/10.3389/fpls.2025.1670593 | เห็น subtle change (ข้อ 4) |
| 9 | Wang & Ghatrehsamani — scoping review 79 studies: HSI+ML จำแนกโรคได้ **90.2% ในระยะ asymptomatic** | 2026 | Smart Agric. Technol. 14:102123 | https://doi.org/10.1016/j.atech.2026.102123 | ⭐ early detection เชิงปริมาณ (ข้อ 4) |

---

### แผนผังข้ออ้าง 5 ข้อ (ใช้เขียนบทนำ)
1. **ลดแรงงาน/เวลา/ผิดพลาด vs manual** → #2, #3, #4, #1 (ตัวเลข 60–70%)
2. **Non-destructive → ติดตามต่อเนื่อง** (เหมาะงานตัวอย่างจำกัด/TC) → #1 (ตัวหลัก), #2, #3
3. **Objectivity/reproducibility** → #5, #6, #8
4. **เห็น trait ที่ตาเปล่าจับไม่ได้** → #9 (90.2%), #8, #2
5. **ข้อมูลดิจิทัลต่อยอดได้** (stats/breeding/FAIR) → #7, #3

### 🎯 3 ตัวหลักแนะนำบทนำ
1. **Bethge 2023** — ตรงงานสุด (ขวด TC) + ตัวเลขต้นทุนแรงงาน เปิดบทนำ
2. **Murphy 2024 (Annu. Rev. Plant Biol.)** — บททบทวน flagship กลางบทนำ
3. **Nguyen 2025** — ครอบคลุมครบห่วงโซ่ ปิดบทนำ

### ⚠️ ข้อควรระวัง
- #6 ตีพิมพ์ 2026 (Scientific Data) — ถ้ายื่น proposal ก่อนเผยแพร่ทางการ อ้าง arXiv:2507.11279 แทน
- #8 อ้างเป็น "Shoaib et al., Front. Plant Sci. 16:1670593 (2025)" ตามหน้าวารสาร (metadata DOI ระบุ 2026)

---

## 📚 Citations: Google Colab ในงานวิจัย (verify 2026-08-06)

> สืบค้นโดยทีมวิจัย — **14 ตัว ✅ verify ครบ** (Crossref API + เปิดหน้า article จริง)
> สำหรับอ้างในข้อเสนอ: เหตุผลใช้ Colab GPU (SAM3) + reproducibility + related work ใน tissue culture CV
> อ่านแล้วคัดเลือก → บอกทีมว่าตัวไหนเข้า บรรณานุกรม

---

### หมวด A — ใช้ Colab รัน DL/CV ในงาน plant science จริง (อ้างได้ "Colab ใช้ได้จริงกับงานแบบเรา")
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| A1 | Rippner et al. — segment ภาพ X-ray ราก/ดิน (PyTorch FCN-ResNet101) **ทั้ง workflow บน Colab** + เผยแพร่ notebook | 2022 | Front. Plant Sci. 13:893140 | https://doi.org/10.3389/fpls.2022.893140 |
| A2 | **Jawed et al.** — ฝึก+deploy บน Colab ชัดเจน "Colab speeds up training… without specialized hardware… improves reproducibility and scalability" + notebook GitHub + Zenodo | 2026 | Scientific Reports 16:9704 | https://doi.org/10.1038/s41598-026-38209-z |
| A3 | **ZeroCostDL4Mic** (von Chamier et al.) — แพลตฟอร์ม DL segmentation (U-Net/StarDist/YOLOv2) รันบน **Colab ฟรี ไม่ต้องซื้อ GPU** | 2021 | Nature Communications 12:2276 | https://doi.org/10.1038/s41467-021-22518-0 |

### หมวด B — งานประเมิน Colab (free tier, resource, scalability)
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| B1 | Carneiro Pessoa et al. — **งานคลาสสิกสุด**: วิเคราะห์ hardware/performance/limitations ของ Colab free tier (เร็วเท่า dedicated workstation แต่ไม่ scalable) | 2018 | IEEE Access 6:61377 | https://doi.org/10.1109/ACCESS.2018.2874767 |
| B2 | Sharma et al. — benchmark CNN บน GPU vs TPU ของ Colab | 2021 | AIS (Springer) | https://doi.org/10.1007/978-981-33-4604-8_49 |

### หมวด C — Reproducibility / Open science ผ่าน Colab notebook
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| C1 | Samuel & Mietchen — ศึกษา notebooks จากสิ่งพิมพ์ biomedical (execute ได้จริง) | 2024 | GigaScience 13:giad113 | https://doi.org/10.1093/gigascience/giad113 |
| C2 | **ColabPCR** (Lozano et al.) — วารสารตีพิมพ์งานที่ **artifact หลักคือ Colab notebook** = หลักฐานว่า "notebook เป็นผลงานที่รับได้" | 2026 | Comput. Biol. Chem. 123:109035 | https://doi.org/10.1016/j.compbiolchem.2026.109035 |
| C3 | Caprarelli et al. — "Notebooks Now!" AGU ให้ computational notebook เป็น primary publication (FAIR) | 2023 | Earth Space Sci. 10(12) | https://doi.org/10.1029/2023EA003458 |

### หมวด D — เปรียบเทียบ Colab กับแพลตฟอร์มอื่น
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| D1 | Mandal et al. — **Colab T4 vs AWS g4dn.xlarge (T4)** สำหรับ semantic segmentation | 2024 | IEEE HiPCW | https://doi.org/10.1109/HIPCW63042.2024.00054 |
| D2 | Munanday et al. — CNN บน GPU/TPU/CPU ของ Colab | 2023 | JARASET 31(3) | https://doi.org/10.37934/araset.31.3.5067 |

### หมวด E — ⭐ งาน CV กับ tissue culture/flask โดยตรง (context — **ไม่ระบุ Colab ห้ามอ้างว่าใช้**)
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| E1 | **Rajapaksha et al.** — YOLOv8 **detect flask** (precision 0.990, mAP50 0.995) + segment leaf/stem/root/โรคใน **coconut tissue culture** — ตรงสุดกับขวด TC ของเรา | 2024 | IEEE ICAC pp 432–437 | https://doi.org/10.1109/ICAC64487.2024.10851150 |
| E2 | Egi et al. — YOLOv8-seg callus/leaf/necrosis ใน TC บน Tesla T4 cloud | 2025 | Plants 15(1):47 | https://doi.org/10.3390/plants15010047 |
| E3 | **Zhao et al.** — SAM→mask→auto-annotate→YOLOv8 (ตรง pipeline SAM+YOLO ของเรา) | 2025 | Agronomy 15(5):1081 | https://doi.org/10.3390/agronomy15051081 |
| E4 | Sikdar et al. — YOLOv12 detect culture vessel (79.6–89.5%) + phenotyping lingonberry micropropagation | 2025 | Smart Agric. Tech. 12:101388 | https://doi.org/10.1016/j.atech.2025.101388 |

---

### ใช้ตัวไหนกับส่วนไหนของข้อเสนอ
- **บทนำ — ทำไมต้อง Colab:** A3 (ZeroCostDL4Mic) + A1 (Rippner) + A2 (Jawed 2026 — สดสุด peer-reviewed ระบุ Colab+reproducibility ชัด)
- **ระเบียบวิธี — เหตุผลเลือก GPU SAM3:** B1 (Pessoa) + B2 + D1 (Colab T4 ≈ AWS สำหรับ segmentation)
- **ระเบียบวิธี — ข้อจำกัดที่รับรู้ (session timeout, ไม่ scalable):** B1 (limitations)
- **Reproducibility / open science:** C1 + C2 (ColabPCR — precedent ว่า notebook = ผลงานที่รับได้) + C3
- **Related work / ช่องว่างวิจัย:** E1–E4 → "CV กับขวด TC กำลังมาแรง (detect flask, SAM+YOLO) แต่ **ยังไม่มีใครทำ 3D phenotyping ผ่านขวดแก้ว**"

### ⚠️ ข้อควรระวัง
1. E1–E4 **ไม่ระบุ Colab** — อ้างเป็น related work เท่านั้น ห้ามผูกกับ Colab
2. A4 (Ag Data Commons dataset) ยังไม่ได้เปิดดูเอง — ใช้เป็นข้อมูลเสริม
3. วิธีเขียน 2 เส้นแยก: (A–D) = "Colab พิสูจน์แล้วในงาน plant CV + reproducible" · (E) = "มีงาน CV ใน TC แล้วแต่ยังไม่มี 3D ผ่านขวด" — กัน reviewer จับผิด

### 🎯 คำแนะนำชุดหลัก (3 ตัวขาดไม่ได้)
1. **Jawed 2026 (Sci Rep)** — เหตุผล Colab ดีที่สุด: สด 2026, ระบุ Colab+reproducibility+scalability + เผยแพร่ notebook/Zenodo
2. **Pessoa 2018 (IEEE Access)** — คลาสสิกที่ reviewer รู้จัก + พูดข้อจำกัดตรงๆ
3. **ZeroCostDL4Mic 2021 (Nat Commun)** — democratization ของ DL segmentation ทางชีววิทยา

---

## Dataset Size สำหรับ Segmentation — งานวิจัยหลักฐาน (2026-08-06)

> สืบค้นโดย vitro-researcher 2026-08-06 · ตรวจ title/ปี/DOI จริงทุกตัว
> บริบท: ผู้ใช้มีภาพ TC 51 ภาพ (ถ่าย 16 ก.ค. 69) — โจทย์: ถ้าไม่ใช้ zero-shot ต้องมี dataset กี่ภาพงานจึงมีน้ำหนัก

### คำตอบสั้น (จากหลักฐาน)

| วิธี | จำนวนภาพที่ควรมี | หลักฐาน |
|---|---|---|
| เทรน segmentation จากศูนย์ (scratch) | ~1,000 ภาพขึ้นไป | Prashanth WACV 2024 (1,000 ภาพ → mAP@0.5 0.648) |
| Fine-tune pretrained model | ~100–1,000 ภาพ/class | Callus YOLO (122 ภาพ → mAP50 0.855); Shahinfar (asymptote ~150–500/class, classification) |
| Fine-tune เฉพาะส่วนเล็ก (mask decoder/LoRA) | 5–20 ภาพก็ขยับได้ | Aubreville arXiv:2407.04651 (medical) |
| Zero-shot foundation model (SAM3) | ไม่ต้องเทรน | Sapkota 2025 (SAM3 vs YOLO11 fine-tuned) |

### หลักฐานสำคัญ (โดเมน TC/พืช)

1. **Egi & Öter 2026 (Plants 15(1):47)** — เทรน YOLO-seg บน **callus ถั่วเลนทิล 122 ภาพ, 3 classes, 1,185 masks** ถ่ายใน biosafety cabinet (สภาพคล้ายแล็บผู้ใช้มาก) → YOLOv8 mAP50 = **0.855** — หลักฐานตรงสุดว่า TC + ~100 ภาพ เทรนสำเร็จได้ https://doi.org/10.3390/plants15010047 · PMC12788146
2. **Prashanth 2024 (WACV)** — 1,000 ภาพ (900/100), 4,682 masks → mAP@0.5 = 0.648 https://openaccess.thecvf.com/content/WACV2024/html/Prashanth_Towards_Accurate_Disease_Segmentation_in_Plant_Images_A_Comprehensive_Dataset_WACV_2024_paper.html
3. **Alkhudaydi 2019 (Plant Phenomics)** — 90 ภาพ side-view wheat → IoU = **0.40** (ผลกลาง ๆ = ภาพ <100 เทรนตรง ๆ ไม่ดี) https://doi.org/10.34133/2019/7368761
4. **Najafian 2023 (Plant Phenomics)** — เทรนตรง ~38 ภาพ → Dice 0.51–0.64; สำเร็จที่ Dice 0.89 ต้องใช้ synthesis + 10,000 ภาพ https://doi.org/10.34133/plantphenomics.0025
5. **Laco 2024 (APL Bioeng, SAAVY)** — 3D tissue culture (spheroid) เทรน **24 ภาพ** + COCO-pretrained → ใช้ได้จริง (งานง่าย/ภาพระเบียบ หลักสิบภาพพอ) https://doi.org/10.1063/5.0189222

### Fine-tune foundation model vs zero-shot

6. **Sapkota 2025 (SAM3 vs YOLO11, arXiv:2512.11884)** — MinneApple 670 ภาพ: YOLO11m fine-tuned F1 72.2% vs SAM3 zero-shot 59.8% แต่ SAM3 **ไม่เสื่อมเมื่อ IoU เข้มงวด** (mask boundary แม่นกว่า) → เหมาะกับงานวัดพื้นที่ https://doi.org/10.48550/arXiv.2512.11884
7. **Li 2023 (ASA, Sensors 23(18):7884)** — SAM + adapter (freeze encoder), 1,100 ภาพ coffee → Dice +41.48% ดีกว่า zero-shot ทุก 12 tasks https://doi.org/10.3390/s23187884 · PMC10534855
8. **Williams 2024 (Leaf Only SAM)** — Mask R-CNN fine-tuned ดีกว่า SAM zero-shot (recall 78.7 vs 63.2) แต่ zero-shot ไม่ต้อง annotate https://doi.org/10.1016/j.atech.2024.100515 · arXiv:2305.09418
9. **Aubreville 2024 (arXiv:2407.04651)** — fine-tune เฉพาะ mask decoder ด้วย 5–20 ภาพ ใช้ได้จริง (medical) https://arxiv.org/abs/2407.04651

### ข้อแนะนำสำหรับ 51 ภาพของผู้ใช้

- **อย่าเทรนเองจากศูนย์ด้วย 51 ภาพ** — ต่ำกว่าเกณฑ์ (เสี่ยง overfit + น้ำหนักวิชาการต่ำ)
- **แผนที่ literature รองรับ:** SAM3 zero-shot เป็นแกน + few-shot fine-tune (mask decoder/LoRA) เทียบกัน 3 ทาง (zero-shot vs few-shot vs manual) → 51 ภาพกลายเป็นจุดแข็ง (scarce-data + foundation model)
- นำเสนอ 51 ภาพเป็น "แรงจูงใจใช้ foundation model" ไม่ใช่ "dataset พอเทรนเอง"
- ถ้าจะพูดว่า "กี่ภาพถึงพอ" ใช้กรอบ: scratch ~1,000 / fine-tune ~100–1,000 / few-shot 5–20 (พร้อม caveat: Shahinfar 150–500 มาจาก classification)

### ข้อจำกัด

- ไม่มี guideline "X ภาพต่อ class" ตายตัวสำหรับ segmentation พืช (Shahinfar เป็น classification)
- ยังไม่มี paper เทรน segmentation ผ่านขวดแก้ว TC (refraction) โดยตรง — Callus YOLO ถ่ายแบบเปิด cabinet → จุดนี้เป็นช่องว่างงานวิจัยของผู้ใช้เอง

---

## 📚 Citations ใหม่ รอบ 2026-08-17 — งาน ≤5 ปี (2021–2026), แนวทาง AI + การเกษตร

> กฎรอบนี้: **เฉพาะงานวิจัยอายุไม่เกิน 5 ปี + แนวทางปรับใช้ AI กับเทคโนโลยีการเกษตร**
> สถานะ: ✅ = verify แล้ว (เปิด paper จริง + DOI/URL กดได้) · ⚠️ = ยังต้อง verify เพิ่ม
> ตรวจโดย: ทีมวิจัย (web_explore/web_search/fetch_content + อ่าน full text)

---

### หมวด 1 — ⭐ หลักฐานตรงสุด: SAM3 ใช้กับ plant segmentation ได้จริง

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

### หมวด 2 — Zero-shot / foundation model กับ segmentation พืช (2025–2026)

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

### หมวด 3 — AI + Tissue culture / micropropagation (2024–2025)

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

### หมวด 4 — งานสนับสนุนอื่น (จากไฟล์ verify เดิม, ทุกตัว ≤5 ปี)

อ้างอิงไฟล์เดิม (ทั้งหมด verify 2026-08-06, อายุ ≤5 ปี):
- `research/LITERATURE.md` — 9 ตัว: Murphy 2024 (Annu. Rev. Plant Biol. 75:771), Nguyen 2025 (Plants 14:907), Peters 2023 (Sci. Rep.), Zhang 2026 (Sci. Data 13), Papoutsoglou 2023, Shoaib 2025, Wang & Ghatrehsamani 2026
- `research/LITERATURE.md` — 14 ตัว: Rippner 2022, Jawed 2026 (Sci. Rep. 16:9704), ZeroCostDL4Mic 2021, Carneiro Pessoa 2018* (*>5 ปี — ใช้เฉพาะถ้าจำเป็น), Samuel & Mietchen 2024, ColabPCR 2026, Caprarelli 2023
- `research/LITERATURE.md` — Egi & Öter 2026 (Plants 15:47, YOLO-seg callus 122 ภาพ), Sapkota 2025 (SAM3 vs YOLO11, arXiv:2512.11884), Li 2023, Williams 2024, Aubreville 2024

---

### ⚠️ งานที่เห็นแต่ยังไม่ verify (ห้ามอ้างก่อน verify)
- **AgriSAM3 (Sapkota et al. 2025)** — README ใช้ arXiv placeholder "XXXX.XXXXX" → ต้องหาหมายเลขจริงก่อนอ้าง
- **Intelligent control system for clonal micro-propagation (2025, IJIRSS)** — วารสารไม่น่าเชื่อถือ → งด
- **Text-conditioned Segmentation for Tomato via Procedural Synthetic Data (arXiv 2607.18576)** — ตัวเลข arXiv ผิดปกติ → งด

---

### แผนใช้ในรายงาน
| ส่วน | ใช้ตัวไหน |
|---|---|
| บทนำ: ปัญหาแรงงาน/ความแปรปรวน | Bethge 2023, Murphy 2024, Nguyen 2025, Zhang 2026 |
| บทนำ: ช่องว่างงานวิจัย | Bethge 2023, Regni 2025, Diningrat 2024 |
| ระเบียบวิธี: ทำไม SAM3 | **Orvati Nia 2026** ⭐, Carion 2025 |
| Related work: zero-shot/foundation | SAP 2026, Zero-shot vertical 2025, ZeroPlantSeg 2025 |
| ข้อจำกัด: prompt sensitivity | **Text guidance 2026** ⭐ |
| วิธี: Colab/reproducibility | Rippner 2022, Jawed 2026, ZeroCostDL4Mic 2021 |
