# 📚 Citations: Google Colab ในงานวิจัย (verify 2026-08-06)

> สืบค้นโดยทีมวิจัย — **14 ตัว ✅ verify ครบ** (Crossref API + เปิดหน้า article จริง)
> สำหรับอ้างในข้อเสนอ: เหตุผลใช้ Colab GPU (SAM3) + reproducibility + related work ใน tissue culture CV
> อ่านแล้วคัดเลือก → บอกทีมว่าตัวไหนเข้า บรรณานุกรม

---

## หมวด A — ใช้ Colab รัน DL/CV ในงาน plant science จริง (อ้างได้ "Colab ใช้ได้จริงกับงานแบบเรา")
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| A1 | Rippner et al. — segment ภาพ X-ray ราก/ดิน (PyTorch FCN-ResNet101) **ทั้ง workflow บน Colab** + เผยแพร่ notebook | 2022 | Front. Plant Sci. 13:893140 | https://doi.org/10.3389/fpls.2022.893140 |
| A2 | **Jawed et al.** — ฝึก+deploy บน Colab ชัดเจน "Colab speeds up training… without specialized hardware… improves reproducibility and scalability" + notebook GitHub + Zenodo | 2026 | Scientific Reports 16:9704 | https://doi.org/10.1038/s41598-026-38209-z |
| A3 | **ZeroCostDL4Mic** (von Chamier et al.) — แพลตฟอร์ม DL segmentation (U-Net/StarDist/YOLOv2) รันบน **Colab ฟรี ไม่ต้องซื้อ GPU** | 2021 | Nature Communications 12:2276 | https://doi.org/10.1038/s41467-021-22518-0 |

## หมวด B — งานประเมิน Colab (free tier, resource, scalability)
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| B1 | Carneiro Pessoa et al. — **งานคลาสสิกสุด**: วิเคราะห์ hardware/performance/limitations ของ Colab free tier (เร็วเท่า dedicated workstation แต่ไม่ scalable) | 2018 | IEEE Access 6:61377 | https://doi.org/10.1109/ACCESS.2018.2874767 |
| B2 | Sharma et al. — benchmark CNN บน GPU vs TPU ของ Colab | 2021 | AIS (Springer) | https://doi.org/10.1007/978-981-33-4604-8_49 |

## หมวด C — Reproducibility / Open science ผ่าน Colab notebook
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| C1 | Samuel & Mietchen — ศึกษา notebooks จากสิ่งพิมพ์ biomedical (execute ได้จริง) | 2024 | GigaScience 13:giad113 | https://doi.org/10.1093/gigascience/giad113 |
| C2 | **ColabPCR** (Lozano et al.) — วารสารตีพิมพ์งานที่ **artifact หลักคือ Colab notebook** = หลักฐานว่า "notebook เป็นผลงานที่รับได้" | 2026 | Comput. Biol. Chem. 123:109035 | https://doi.org/10.1016/j.compbiolchem.2026.109035 |
| C3 | Caprarelli et al. — "Notebooks Now!" AGU ให้ computational notebook เป็น primary publication (FAIR) | 2023 | Earth Space Sci. 10(12) | https://doi.org/10.1029/2023EA003458 |

## หมวด D — เปรียบเทียบ Colab กับแพลตฟอร์มอื่น
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| D1 | Mandal et al. — **Colab T4 vs AWS g4dn.xlarge (T4)** สำหรับ semantic segmentation | 2024 | IEEE HiPCW | https://doi.org/10.1109/HIPCW63042.2024.00054 |
| D2 | Munanday et al. — CNN บน GPU/TPU/CPU ของ Colab | 2023 | JARASET 31(3) | https://doi.org/10.37934/araset.31.3.5067 |

## หมวด E — ⭐ งาน CV กับ tissue culture/flask โดยตรง (context — **ไม่ระบุ Colab ห้ามอ้างว่าใช้**)
| # | Paper | ปี | วารสาร | หลักฐาน |
|---|---|---|---|---|
| E1 | **Rajapaksha et al.** — YOLOv8 **detect flask** (precision 0.990, mAP50 0.995) + segment leaf/stem/root/โรคใน **coconut tissue culture** — ตรงสุดกับขวด TC ของเรา | 2024 | IEEE ICAC pp 432–437 | https://doi.org/10.1109/ICAC64487.2024.10851150 |
| E2 | Egi et al. — YOLOv8-seg callus/leaf/necrosis ใน TC บน Tesla T4 cloud | 2025 | Plants 15(1):47 | https://doi.org/10.3390/plants15010047 |
| E3 | **Zhao et al.** — SAM→mask→auto-annotate→YOLOv8 (ตรง pipeline SAM+YOLO ของเรา) | 2025 | Agronomy 15(5):1081 | https://doi.org/10.3390/agronomy15051081 |
| E4 | Sikdar et al. — YOLOv12 detect culture vessel (79.6–89.5%) + phenotyping lingonberry micropropagation | 2025 | Smart Agric. Tech. 12:101388 | https://doi.org/10.1016/j.atech.2025.101388 |

---

## ใช้ตัวไหนกับส่วนไหนของข้อเสนอ
- **บทนำ — ทำไมต้อง Colab:** A3 (ZeroCostDL4Mic) + A1 (Rippner) + A2 (Jawed 2026 — สดสุด peer-reviewed ระบุ Colab+reproducibility ชัด)
- **ระเบียบวิธี — เหตุผลเลือก GPU SAM3:** B1 (Pessoa) + B2 + D1 (Colab T4 ≈ AWS สำหรับ segmentation)
- **ระเบียบวิธี — ข้อจำกัดที่รับรู้ (session timeout, ไม่ scalable):** B1 (limitations)
- **Reproducibility / open science:** C1 + C2 (ColabPCR — precedent ว่า notebook = ผลงานที่รับได้) + C3
- **Related work / ช่องว่างวิจัย:** E1–E4 → "CV กับขวด TC กำลังมาแรง (detect flask, SAM+YOLO) แต่ **ยังไม่มีใครทำ 3D phenotyping ผ่านขวดแก้ว**"

## ⚠️ ข้อควรระวัง
1. E1–E4 **ไม่ระบุ Colab** — อ้างเป็น related work เท่านั้น ห้ามผูกกับ Colab
2. A4 (Ag Data Commons dataset) ยังไม่ได้เปิดดูเอง — ใช้เป็นข้อมูลเสริม
3. วิธีเขียน 2 เส้นแยก: (A–D) = "Colab พิสูจน์แล้วในงาน plant CV + reproducible" · (E) = "มีงาน CV ใน TC แล้วแต่ยังไม่มี 3D ผ่านขวด" — กัน reviewer จับผิด

## 🎯 คำแนะนำชุดหลัก (3 ตัวขาดไม่ได้)
1. **Jawed 2026 (Sci Rep)** — เหตุผล Colab ดีที่สุด: สด 2026, ระบุ Colab+reproducibility+scalability + เผยแพร่ notebook/Zenodo
2. **Pessoa 2018 (IEEE Access)** — คลาสสิกที่ reviewer รู้จัก + พูดข้อจำกัดตรงๆ
3. **ZeroCostDL4Mic 2021 (Nat Commun)** — democratization ของ DL segmentation ทางชีววิทยา
