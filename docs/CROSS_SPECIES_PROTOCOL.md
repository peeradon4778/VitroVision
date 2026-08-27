# โปรโตคอลเก็บข้อมูลข้ามชนิด (Cross-Species Collection Protocol) — VitroVision

> เป้าหมาย: เก็บภาพถ่ายควบคุมของ**ชนิดพืชอื่น 2–3 ชนิด** ให้เปรียบเทียบกับชุดพริกจินดาได้ เพื่อพิสูจน์ว่า
> **SAM3 PCS แบบ zero-shot ใช้ได้ข้ามชนิดโดยไม่ต้องฝึกใหม่** (จุดขายหลักของโครงงาน)
> ใช้คู่กับ [`src/benchmark_cross_species.py`](../src/benchmark_cross_species.py) (รันบน Colab GPU)

---

## 1. สิ่งที่ต้องมี

- **ชนิดอื่น 2–3 ชนิด** ที่มี morphology ต่างจากพริกจินดาชัดเจน เช่น กล้วยไม้ (ใบเดี่ยว/รูปใบหอก), กล้วย (ใบใหญ่/ลำต้นเทียม), ไม้เนื้ออ่อนอื่นในแล็บ (ใช้ **culture dense ที่มีในแล็บอยู่แล้ว** ตามแนวคิดโปรเจกต์)
- **กล้อง/ขาตั้งเดียวกัน** กับชุดพริกจินดา (สำคัญสุด — กัน confound จาก setup)
- ขวดแก้ว/สารอาหาร/สภาพห้องเดียวกัน

## 2. การถ่าย (ให้เหมือนชุดพริกจินดา 20260814_batch)

| พารามิเตอร์ | ให้ทำ |
|---|---|
| ระยะกล้อง→ขวด | คงที่เท่ากับชุดพริกจินดา |
| ความสูง/มุม | คงที่ (ถ่ายตรงขวด ไม่เอียง) |
| แสง | ไฟห้องเดียว, กันแสงสะท้อน (glare) บนขวด — เปลี่ยนมุม/กันเงา |
| การโฟกัส | ต้นอยู่ในโฟกัสทั้งขวด |
| จำนวน/ชนิด | **≥ 10 ขวด/ชนิด** (เป้า) · ถ้าได้น้อยกว่า ให้ **≥ 5 ขวด/ชนิด** แล้วรายงานเป็น **pilot** ต่อชนิด |
| ขวด | ชนิด/ขนาดเดียวกัน ตรวจฝ้า/ไอน้ำน้อย |

> ⚠️ ถ้าชุดเล็ก (5–10 ขวด/ชนิด) เยอะพอจะได้ **ค่าเฉลี่ย/สัดส่วน** แต่**ยังไม่พอสรุปสถิติ** — รายงานอย่างซื่อตรงว่าเป็น pilot

## 3. การจัดเก็บไฟล์ (เลือกแบบใดแบบหนึ่ง)

**แบบ A — โฟลเดอร์ย่อย = ชนิด** (ง่ายสุด):
```
data/raw/cross_species/
  พริกจินดา/    (ถ้าอยากเก็บชุดเดิมกำกับ) 001.jpg ...
  กล้วยไม้/      001.jpg ...
  กล้วย/         001.jpg ...
```

**แบบ B — รวมโฟลเดอร์ + species_map.csv**:
```
data/raw/cross_species/
  001.jpg, 002.jpg ...
species_map.csv:
  image,species
  001.jpg,กล้วยไม้
  002.jpg,กล้วยไม้
  ...
```

## 4. ค่าวัดมือ (GT) สำหรับ validation ต่อชนิด

ถ้าอยากได้ตัวเลข "ตรงกับมือ" ข้ามชนิด ให้วัดต่อภาพ (protocol เดียวกับ §4 ของ `VALIDATION_PLAN.md`):
- `height_cm` (สำคัญสุด) · `width_cm` · `area_cm2`
- `expert_verdict` ∈ {ยังไม่พร้อม, พร้อมอนุบาล, ตรวจเอง}

เก็บเป็น `ground_truth_cross_species.csv`:
```
image,species,height_cm,width_cm,area_cm2,expert_verdict
001.jpg,กล้วยไม้,5.2,,,พร้อมอนุบาล
```

## 5. การรัน (Colab GPU — SAM3 ต้อง GPU)

```bash
# แบบ A (โฟลเดอร์ย่อย = ชนิด)
python src/benchmark_cross_species.py \
  --data data/raw/cross_species \
  --gt data/processed/ground_truth_cross_species.csv \
  --out data/processed/cross_species --hf-token <TOKEN> --device cuda

# แบบ B (+ species-map)
python src/benchmark_cross_species.py \
  --data data/raw/cross_species \
  --species-map data/raw/cross_species/species_map.csv \
  --gt data/processed/ground_truth_cross_species.csv \
  --out data/processed/cross_species --hf-token <TOKEN> --device cuda
```

ผลลัพธ์:
- `cross_species_per_image.csv` — trait รายภาพ+ชนิด
- `cross_species_summary.csv` — mean±std ต่อชนิด (sanity: area/height/zero_mask_rate)
- `cross_species_validation.csv` — Pearson r (height/area vs มือ) + generic-acceptance ต่อชนิด (ถ้ามี GT)
- `cross_species_compare.png` — กราฟเปรียบเทียบข้ามชนิด

## 6. อ่านผลยังไง (การตัดสิน)

1. **Segmentation ผ่านข้ามชนิด?** → `zero_mask_rate` ต่ำทุกชนิด + `height_proxy`/`area` เป็นสัดส่วนสมเหตุผล (ไม่ล้น/ไม่ศูนย์) → แปลว่า SAM3 วัดขนาดต้นได้ข้ามชนิด
2. **เกณฑ์พร้อมอนุบาล transfer ได้ไหม?** → ดู `generic_acc` ต่อชนิด: ถ้าสูงทุกชนิด → ใช้ `READY_HEIGHT` generic ได้; ถ้าตกในบางชนิด → ต้อง **calibrate ต่อชนิด** (เป็นข้อค้นพบที่ดี: เกณฑ์ตัดสินใจไม่จำเป็นต้อง transfer แต่ segmentation transfer ได้)
3. **ข้อควรระวัง:** sample เล็ก → รายงาน pilot + อย่าโอเวอร์เคลม; ถ้าชนิดที่ทดสอบ morphology ต่างมาก (เช่น กล้วยไม้ใบเดียว vs กล้วยใบใหญ่) คาดว่า SAM3 ยังทำได้แต่ feature/height อาจต้องตีความต่างกัน

## 7. แหล่งอ้างอิง / ที่มาของแนวคิด

- การใช้ SAM3 ในโหมด detector-free ด้วยพรอมป์ "plant" ข้ามโครงสร้างพืชหลากหลายให้ผลแม่นสุด (Orvati Nia et al., 2026)
- ข้อจำกัด: งานใกล้เคียง (Regni et al., 2025) ใช้ภาพ 3D แต่จำกัดชนิด — โครงงานนี้มุ่งข้ามชนิด
