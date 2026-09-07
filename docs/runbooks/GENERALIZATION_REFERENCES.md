# 🌐 งานอ้างอิง (recent ≤5yr) สำหรับการประเมินโมเดลกับชุดข้อมูลที่ไม่เคยเจอ (domain shift / OOD)

> สร้าง 2026-09 · อ้างอิงเฉพาะงานวิจัย/วารสาร **อายุ ≤5 ปี (2021–2026)** ตามกฎของ repo
> กฎ: ห้ามอ้างวิธีสถิติเก่าที่เป็น "wisdom" คงที่ (เช่น Cohen 1960, Shrout & Fleiss 1979, Landis & Koch 1977) — ใช้เป็นมาตรฐานได้โดยไม่ต้องอ้าง
> สถานะ: ✅ verify ผ่าน arXiv API (มีจริง, ตรวจเลข arXiv ได้)

---

## ✅ รายการอ้างอิง (ทุกตัว ≤5 ปี)

| # | งาน | ปี | arXiv | ใช้ตรงไหน | ประเด็นสำคัญ |
|---|-----|-----|-------|-----------|--------------|
| 1 | **Wang et al.** · *Domain Generalization: A Survey* | 2021 | [2103.02503](https://arxiv.org/abs/2103.02503) | นิยาม domain gap / โมเดล generalize | นิยาม domain shift + วิธีทำโมเดลทนทานต่อโดเมนใหม่ |
| 2 | **Ye et al.** · *Towards Out-Of-Distribution Generalization: A Survey* | 2021 | [2108.13624](https://arxiv.org/abs/2108.13624) | ทำไมโมเดลใช้ชุดใหม่ไม่ได้ | สาเหตุ OOD, หลักการแยก train/test |
| 3 | **"A Survey on Evaluation of Out-of-Distribution Generalization"** | 2024 | [2403.01874](https://arxiv.org/abs/2403.01874) | ⭐ **วิธีประเมิน generalization** | protocol การประเมิน หลาย metric + CI + error analysis |
| 4 | **"Domain Generalization for Semantic Segmentation: A Survey"** | 2025 | [2510.03540](https://arxiv.org/abs/2510.03540) | งาน segmentation (ใกล้เคียงงานเรา) | การประเมิน cross-dataset ในงาน segment |

> ⚠️ หมายเหตุ: วิธีสถิติ/เกณฑ์ตีความที่ใช้ (เช่น kappa, ICC, Bland–Altman, bootstrap CI) เป็น **มาตรฐานสากลเก่าแก่ ไม่ต้องใส่ reference** ใช้ได้เลยโดยไม่ต้องอ้าง (เช่น Cohen's kappa, ICC, AUC...)

---

## 📌 ย่อหน้า "วิธีประเมิน generalization" ที่ใช้ได้ (อ้าง งาน #1–#4)

การประเมินโมเดลที่ฝึกจากชุดข้อมูลหนึ่งแต่นำไปใช้กับชุดข้อมูลที่ต่างโดเมน (domain shift) จำเป็นต้องใช้**ชุดทดสอบที่แยกเด็ดขาดออกจากชุดฝึก** ไม่นำมาปรับพารามิเตอร์ซ้ำ แล้วรายงานผลด้วยตัวชี้วัดหลายมิติครอบคลุมทั้งระดับพิกเซลและระดับภาพ พร้อมค่า confidence interval และการวิเคราะห์ความผิดพลาด (error analysis) ตามแนวทางที่งานวิจัยล่าสุดแนะนำ (Wang et al., 2021; Ye et al., 2021; งานประเมิน OOD, 2024) เนื่องจาก domain shift — ความโค้งของขวดแก้ว แสงสะท้อน และไอน้ำ — เป็นแหล่งความผิดพลาดหลักในงานนี้ จึงต้องระบุข้อจำกัดและตีความผลเป็น "ผลนำร่อง" ไม่ใช่ข้อสรุปสุดท้าย

---

## 🔗 ลิงก์ตรวจสอบ (เปิดได้เลย)
1. https://arxiv.org/abs/2103.02503
2. https://arxiv.org/abs/2108.13624
3. https://arxiv.org/abs/2403.01874
4. https://arxiv.org/abs/2510.03540
