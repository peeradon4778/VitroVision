# 📚 Citations รอบใหม่ — VitroVision v2 (verify 2026-08-06)

> สืบค้นโดยทีมวิจัยตามกฎ citation เหล็ก (Consensus + PubMed + verify DOI/URL) — **19 ตัว ✅ verify แล้ว**
> ผู้ใช้กำลังอ่านงานจริงอีกรอบเพื่อคัดเลือกก่อนเข้าบรรณานุกรม
> อ้างอิงเก่า (Yang 2024 / Li 2022 / Wang 2025 / Tong 2023 / Bethge 2023) ถูกโล๊ะจาก keywords.md แล้ว

---

## หมวด 1 — Non-destructive phenotyping ของ plant tissue culture
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Bethge et al., "Phenomenon" low-cost multi-sensor phenotyping of in vitro culture | 2023 | Plant Methods | https://doi.org/10.1186/s13007-023-01018-w |

⚠️ ยังไม่มีงาน 2025–2026 เจาะจง phenotyping พืชในขวด TC ผ่าน glass container โดยตรง → ช่องว่าง = **novelty ของเรา**

## หมวด 2 — SfM / photogrammetry / multi-view plant phenotyping
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Photogrammetric apparatus + robotic arm (routine morphological analysis) | 2025 | Plant Methods | https://doi.org/10.1186/s13007-025-01445-x |
| 3D reconstruction binocular camera, self-occlusion handling | 2025 | Front. Plant Sci. | https://doi.org/10.3389/fpls.2025.1642388 |
| Zhuo & You — PlantMDE: 3D phenotyping จาก single image (monocular depth) | 2025 | Comput. Electron. Agric. | https://doi.org/10.1016/j.compag.2025.110925 |
| Hrzich et al. — low-cost SfM photogrammetry wheat (point cloud) | 2025 | arXiv | https://arxiv.org/abs/2504.16840 |

## หมวด 3 — 3D Gaussian Splatting (3DGS) / NeRF สำหรับ plant phenotyping
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| **PlantGaussian** — Shen, Jing, Deng, Jia, Wu | 2025 | Crop Journal 13:607–618 | https://doi.org/10.1016/j.cj.2025.01.011 |
| Li et al. — Survey: classical → NeRF → 3DGS in plant phenotyping | 2025 | Plant Phenomics 7:100137 | https://doi.org/10.1016/j.plaphe.2025.100137 |
| Seed 3D: panoramic video + SfM + 3DGS (maize/wheat/rice) | 2025 | Agriculture 15(22):2329 | https://doi.org/10.3390/agriculture15222329 |
| Li et al. — Object-Centric 3DGS strawberry (video + SAM-2) | 2025 | arXiv | https://arxiv.org/abs/2511.02207 |
| **Wheat3DGS** — Zhang et al. (ETH Zürich) | 2025 | CVPR Workshops | https://doi.org/10.1109/CVPRW67362.2025.00533 |
| Chen et al. — Sugarcane 3D phenotyping: instance seg + 3DGS | 2026 | Agriculture 16(3):375 | https://doi.org/10.3390/agriculture16030375 |

## หมวด 4 — Transparent object / refraction-aware 3D reconstruction (ต่อจาก Tong 2023)
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Surface reconstruction ของ**ขวดแก้ว**ด้วย neural implicit | 2026 | J. Intell. Manuf. 37(7):2903–2918 | https://doi.org/10.1007/s10845-025-02668-4 |
| Tian et al. — Geometry-aware Gaussian Splatting ของ transparent objects | 2026 | Eng. Appl. Artif. Intell. | https://doi.org/10.1016/j.engappai.2026.113787 |
| **TSGS** — normal + de-lighting priors สำหรับ transparent surface | 2025 | ACM MM pp 7220–7229 | https://doi.org/10.1145/3746027.3754548 |

## หมวด 5 — SAM2 / SAM3 / foundation segmentation models สำหรับพืช
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Abbey & Meroz — **Segment Any Plant (SAP)**: SAM2 few-shot สำหรับ plant time-series | 2026 | bioRxiv | https://doi.org/10.64898/2026.03.11.711099 |
| **EMSAM** — Enhanced Multi-Scale SAM สำหรับ leaf disease segmentation | 2025 | Front. Plant Sci. | https://doi.org/10.3389/fpls.2025.1564079 |
| Vashisht et al. — SAM-2 สำหรับ grape leaf segmentation | 2025 | LNNS (SmartCom 2025) pp 375–386 | https://doi.org/10.1007/978-981-96-7517-3_32 |

## หมวด 6 — 3D traits vs 2D projected area
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| van Marrewijk et al. — เทียบ 2D-to-3D segmentation vs 3D segmentation | 2025 | Biosystems Engineering | https://doi.org/10.1016/j.biosystemseng.2025.104147 |

## เสริม
| Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|
| Review: 3D crop phenotyping ด้วย point cloud (CCP vs FCP) | 2026 | Front. Plant Sci. | https://doi.org/10.3389/fpls.2026.1731852 |

---

## จับคู่กับส่วนของข้อเสนอ
- **บทนำ (phenotyping gap):** Bethge 2023 · Survey Plant Phenomics 2025 · Review 2026
- **บทนำ (novelty):** 3DGS/วิดีโอ 2025–2026 → "มีคนทำ 3DGS กับพืชแล้ว แต่ยังไม่มีใครทำในขวดแก้ว TC"
- **ระเบียบวิธี (เก็บภาพ):** Seed video+SfM+3DGS · Photogrammetric apparatus · Strawberry video 3DGS
- **ระเบียบวิธี (segment):** SAP · SAM-2 grape · EMSAM
- **ระเบียบวิธี (refraction):** ขวดแก้ว neural implicit · geometry-aware 3DGS · TSGS
- **การวิเคราะห์ (3D vs 2D):** van Marrewijk · PlantMDE

## ⚠️ 3 จุดที่ต้องปิดก่อนเขียนอ้างอิงจริง
1. **TSGS ACM MM** (10.1145/3746027.3754548) — author ชื่อเต็มถูกตัด ต้องดึงใหม่ ห้ามเดา
2. **Plant Methods 2025** (10.1186/s13007-025-01445-x) + **Front. Plant Sci. 2025** (10.3389/fpls.2025.1642388) — author list บางส่วนถูกตัด ต้องดึงชื่อเต็ม
3. **arXiv 2 ตัว** (2504.16840, 2511.02207) — ใช้ URL arXiv อย่างเดียว ห้ามใช้ DOI 10.48550 (CrossRef 404)
4. อย่าอ้างว่า "มีงาน 3D traits vs 2D vs manual ใน TC" — ยังไม่มี → ใช้ van Marrewijk (ใกล้เคียง) + ชี้ novelty
