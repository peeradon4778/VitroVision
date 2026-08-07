# DEV_LOG — บันทึกการพัฒนา (Development Log)

> หลักฐานกระบวนการทำงาน — เขียนทุกครั้งที่แก้โค้ด **ก่อน** commit
> รูปแบบ: `yyyy-mm-dd | หมวด | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ`

## 2026-08-07 — วันนี้

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| บ่าย | สร้าง pipeline SAM3 วัดการเจริญพืชในขวด (6 มิติ: โครงสร้าง/อวัยวะ/ความซับซ้อน/สี/คุณภาพภาพ/verdict) — 5 prompts (plant/leaf/shoot/stem/root), synthetic benchmark, sanity check, export CSV/XLSX | `notebooks/sam3/sam3_growth_pipeline.ipynb`, `src/sam3_growth_pipeline.py` | compile ผ่าน; feature math, IoU/Dice (1.0/0.0/0.533), generator deterministic — เทสต์ผ่าน |
| บ่าย | เปลี่ยนการประเมินเป็น**โหมดค่ากลาง (generic)** — ใช้ได้หลายชนิดพืช, ชนิดไม่เข้า verdict (`USE_SPECIES_THRESHOLDS=False`), ลบ species auto-match | ไฟล์เดิม | compile ผ่านทั้ง notebook + .py |
| บ่าย | รันครั้งแรกบน Colab — 51 ภาพ 16/07/2026 ได้ `plant_growth_summary.csv/.xlsx` (40 คอลัมน์) | ผลใน Downloads | correlation สมเหตุผล (shoot↔height r=0.853, green↔yellow r=-0.597) แต่พบ: verdict ลำเอียงจาก ROI ทั้งภาพ, leaf_count 0 บนภาพมีต้น, over-segmentation |
| เย็น | **รอบ 2:** เปิด `DETECT_BOTTLE=True` (ROI ขวด), นับใบแบบ merged กัน over-seg, fallback นับใบจาก plant+shoot (`leaf_count_method`), ฟอนต์ไทยในกราฟ | ไฟล์เดิม | เทสต์: ชิ้นติดกัน=1/แยก=2, fallback=2, build_report สร้างครบ — ผ่าน |
| เย็น | export เพิ่มภาพ/กราฟ: `overlays/` (6 ภาพ), `plots/` (radar/bar/scatter/heatmap/pie/hist), `report.html` ฝังรูป, `vitro_report.zip` | ไฟล์เดิม | build_report สร้างครบ ผ่าน |
| เย็น | ตั้งระบบ log ของโปรเจกต์: LOG_MAP + DEV_LOG + requirements.txt | `docs/LOG_MAP.md`, `docs/DEV_LOG.md`, `requirements.txt` | — |
| เย็น | commit ชุด SAM3 + log, tag milestone `v0.1` | commit `10112dd` (feat) + `15c266a` (docs) | git log ยืนยัน 2 commits, tag v0.1 ตั้งแล้ว |
| กลางคืน | เพิ่มคู่มือ calibrate cm + แม่แบบ data (ground_truth.csv, species_map.csv) — เตรียมของให้รอบหน้ารัน Colab | `docs/CALIBRATION_GUIDE.md`, `docs/DATA_TEMPLATES.md` | commit `dcf836e` ผ่าน |

## ข้อควรทำต่อ (backlog)

- [ ] รัน Colab รอบ 2 ด้วย notebook ใหม่ (ROI ขวด + นับใบใหม่) → นำผลเทียบกับรอบ 1
- [ ] ตรวจ overlay 6 ภาพที่ export: ยืนยัน mask ขวด/ใบถูกต้อง
- [ ] ติดตั้ง `PIXEL_TO_CM` (calibrate กับขวดจริง) เพื่อให้ได้ค่า cm
- [ ] เปิด `USE_SPECIES_THRESHOLDS=True` เมื่อมีข้อมูลจริงต่อชนิด
- [ ] วาง `ground_truth.csv` เมื่อวัดมือได้ → validation metrics
- [ ] tag milestone (v0.1) + ตั้ง Zenodo DOI เมื่องานนิ่ง

---

## แม่แบบ entry ใหม่ (คัดลอกไปใช้)

```md
| วันที่ | สิ่งที่ทำ: <เปลี่ยนอะไร ทำไม อย่างไร> | <ไฟล์> | <ผลเทสต์: เทสต์อะไร ได้ผลอะไร> |
```
