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

## 2026-08-17 — ล็อกขอบเขตรอบใหม่ + citations ≤5 ปี + ร่างรายงาน v1

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| เย็น | ล็อกขอบเขตงานรอบใหม่ตามคู่มือ Research Writing Adviser (ระยะ 0) ก่อนเขียนเอกสาร — ปัญหา/RQ/วัตถุประสงค์/ข้อมูล/วิธี/ผลที่มี/ข้อจำกัด/รูปแบบยื่น + งานค้างรอบนี้ | `research/_scope_lock_new_round.md` | ครบ 11 หัวข้อ, [OPEN] 3 จุด (ชุดภาพใหม่, ground truth, calibration) |
| เย็น | รวบรวม citations รอบใหม่ **งาน ≤5 ปี (2021–2026) แนว AI+agriculture** — หลักฐานตรงสุด: Orvati Nia et al. 2026 (SAM3 ชนะสุดข้ามโครงสร้างพืช, ใช้ text prompt "plant" ตรงกับวิธีเรา), Carion et al. 2025 (SAM 3 paper), Segment Any Plant, prompt-sensitive paper (ใช้ในข้อจำกัด) | `research/citations_new_20260817.md` | 6 ตัว ✅ verify แล้ว (เปิด paper จริง + DOI กดได้), 2 ตัว ⚠️ รอ verify เพิ่ม |
| เย็น | ร่างรายงานฉบับ v1 (บทคัดย่อ + บทนำ + วิธี + ผลรอบ 1) ใช้สถานะ [FACT]/[PLAN]/[EXPECTED]/[RESULT]/[OPEN] กำกับทุกข้อความ — ห้ามอ้าง citation ที่ไม่ verify | `docs/report_th_v1.md` (243 บรรทัด) | โครงสร้างครบ 5 บท; [OPEN] 4 จุดที่ต้องเติมหลักฐาน |
| เย็น | บันทึก notebook รอบรันชุด 20260814 (พริกจินดา 100 ขวด) | `notebooks/sam3/colab_run_20260814_batch.ipynb` | รันบน Colab T4 ผ่าน |

## 2026-08-18 — pipeline: config JSON + ROI fallback + threshold พริกจินดา

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| กลางคืน | เพิ่ม `--config config.json` — ตั้ง PIXEL_TO_CM / threshold / prompts / species thresholds **โดยไม่ต้องแก้โค้ด** (คู่กับ CALIBRATION_GUIDE) | `src/sam3_growth_pipeline.py` | load_config โหลดครบทุกค่า; ไม่มีไฟล์ → ใช้ค่าเริ่มต้น — เทสต์ผ่าน |
| กลางคืน | ปรับ `COVERAGE_READY` 0.35→**0.20** (พริกจินดา ตั้งตามผู้เชี่ยวชาญ 2026-08-18 — อยู่ระหว่าง validate) | ไฟล์เดิม | — |
| กลางคืน | **กัน verdict ผิด:** หา ROI ขวดไม่เจอ → verdict `ROI-ไม่ชัด-ตรวจเอง` (ไม่เดาจาก ROI ทั้งภาพ) + เพิ่ม `quality_warning` (glare/condensation) และ counts ใช้ `.get()` กัน key หาย | ไฟล์เดิม | เทสต์: ภาพไม่มีขวด → verdict ส่งคนตรวจ; key หายไม่ crash — ผ่าน |
| กลางคืน | เตรียม notebook รอบ 2 ฉบับสะอาดสำหรับรันชุด 100 ขวด | `notebooks/sam3/colab_run_v2_clean.ipynb` | — |

## 2026-08-19 — วิเคราะห์ผลรันจริง 100 ขวด (พริกจินดา) + สรุปผล

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| เช้า–บ่าย | วิเคราะห์ผลรัน Colab ชุด 100 ขวดพริกจินดา (`data/raw/20260814_batch`) — จัดกลุ่ม verdict 3 กลุ่ม + ตรวจความสัมพันธ์ระหว่าง features + เตรียมผลสรุปสำหรับรายงาน/การนำเสนอ | `notebooks/sam3/colab_run_v2_clean.ipynb` (ผลอยู่ใน Downloads/Colab) | **ผลจริง:** 13 พร้อมอนุบาล / 51 ยังไม่พร้อม / 36 ROI-ไม่ชัด-ตรวจเอง; corr leaf↔coverage 0.760, coverage↔height 0.716, green↔healthy 0.922, leaf↔shoot 0.538, coverage↔area 0.932; **100 ขวด/~15 นาที** |
| บ่าย | สรุปสถาปัตยกรรม/design diagrams ของระบบ (Mermaid, ภาษาอังกฤษตามข้อกำหนด YSC) | `docs/diagrams.md` | — |

## ข้อควรทำต่อ (backlog)

- [x] ~~รัน Colab รอบ 2 ด้วย notebook ใหม่~~ → **ทำแล้ว 18/08** (`colab_run_v2_clean.ipynb`) — ผล 100 ขวดพริกจินดา: 13 พร้อมอนุบาล / 51 ยังไม่พร้อม / 36 ROI-ไม่ชัด-ตรวจเอง
- [x] ~~ติดตั้ง `PIXEL_TO_CM`~~ → **โค้ดรองรับแล้วผ่าน `--config`** — เหลือ calibrate ค่าจริงกับขวด
- [x] ~~เปิด `USE_SPECIES_THRESHOLDS=True`~~ → **รองรับผ่าน `--config` แล้ว** — เหลือป้อนค่าเมื่อมีข้อมูลต่อชนิด
- [ ] ตรวจ overlay ที่ export: ยืนยัน mask ขวด/ใบถูกต้อง (มี overlay จาก Colab รอบ 100 ขวด)
- [ ] ลด 36 ขวด "ROI-ไม่ชัด" (SAM3 หาขวดไม่เจอบ่อย) — ลองปรับ prompt/mask threshold หรือ train ขวด ROI
- [ ] calibrate ค่า `PIXEL_TO_CM` กับขวดจริง → นำผลไปต่อยอด feature หน่วย cm
- [ ] วาง `ground_truth.csv` เมื่อวัดมือได้ → validation metrics
- [ ] เขียนรายงานฉบับเต็มต่อจาก v1 (เติมบทวิธี/ผล/อภิปรายด้วยผล 100 ขวด + citations ที่ verify)
- [ ] ตรวจ citation ในเอกสาร/การนำเสนอ กับ `citation_gate.md`/`citations_new_20260817.md` (อ้างอิง Regni 2025, Bethge 2023 เป็นต้น)
- [ ] tag milestone (v0.2 หลังผล 100 ขวด) + ตั้ง Zenodo DOI เมื่องานนิ่ง

---

## แม่แบบ entry ใหม่ (คัดลอกไปใช้)

```md
| วันที่ | สิ่งที่ทำ: <เปลี่ยนอะไร ทำไม อย่างไร> | <ไฟล์> | <ผลเทสต์: เทสต์อะไร ได้ผลอะไร> |
```
