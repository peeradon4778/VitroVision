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

## 2026-08-24 — ปรับ framing เอกสารตาม YSC Category Wizard (75→95 คะแนน) + อัปเดตผล 100 ขวด

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| กลางคืน | ทดสอบ proposal กับ YSC Wizard Tools (Category Wizard, ysc-wizard.vercel.app) — รอบ 1 (framing ชีววิทยา) ได้ **75/100** · รอบ 2 (framing แบบ CS: dataset contribution + baseline + ablation) ได้ **95/100** (โมเดล Typhoon 2.5 30B SCB 10X Cloud) — จุดอ่อนที่พบ: Scope 5/15 → 14/15, Metric 17/25 → 24/25 · สาขาที่แนะนำ: CS → CSAI (AI/ML) อันดับ 1 | ทดสอบออนไลน์ (ไม่ใช่ไฟล์) | 75 → 95/100 — framing เปลี่ยนทุกอย่าง |
| กลางคืน | ปรับ proposal: บทคัดย่อ/RQ/สมมติฐาน/วัตถุประสงค์ framing แบบ CS · methodology ตรง pipeline จริง (5 prompts, ROI detection, 6 กลุ่ม features, verdict ROI-ไม่ชัด) · เพิ่ม 7.6 Baseline Comparison + Sensitivity Analysis · เพิ่ม segmentation metrics (mIoU/Dice/F1) · เพิ่ม dataset contribution + citations ใหม่ (Orvati Nia 2026, Abbey & Meroz 2026, Dubois 2026) | `docs/proposal_th_draft.md` (381→403 บรรทัด) | โครงสร้างครบ 13 หัวข้อ |
| กลางคืน | ปรับ report v1: บทคัดย่อ framing CS + เพิ่มผล 100 ขวด [RESULT] (13/51/36 + correlation r = 0.716–0.932) · อัปเดต 1.4/3.6/5/6.2 ให้มี baseline/ablation plan · แก้ H₁ เป็น 5 prompts · เกณฑ์ ready 0.20 | `docs/report_th_v1.md` (243→272 บรรทัด) | — |
| กลางคืน | เขียน benchmark baselines (classical/SAM2/YOLO-seg) + Colab script เต็ม (classical/YOLO/SAM2/SAM3 PCS + GT metrics + กราฟเปรียบเทียบ) + template ground_truth_masks — ทดสอบ local: classical 100 ภาพ 0.44s/ภาพ · YOLO-seg (COCO) 0.33s/ภาพ (พื้นที่ทุก class = reference เท่านั้น เพราะ COCO ไม่มี class plant) | `src/benchmark_baselines.py`, `src/benchmark_colab.py`, `docs/DATA_TEMPLATES.md` | compile ผ่าน; รันครบ 100 ภาพ 2 วิธี — SAM2/SAM3 ต้องรันบน Colab GPU (SAM2 ยังไม่มี checkpoint ในเครื่อง) |
| กลางคืน | ปรับ proposal สู่โครงสร้าง **"ไอเดีย + pilot evidence + ต่อยอด"** (ตามบรีฟ: ขอทุนพัฒนาต่อ ไม่ใช่ทำเสร็จแล้ว) — ทิศทางต่อยอด = **time-series monitoring** (greenhouse/plant factory/phenotyping, zero-budget framing) — แก้แล้ว: บทคัดย่อ (เพิ่ม pilot 100 ขวด + ต่อยอด), 3.3 gap (เพิ่ม time-series/เปิด dataset), เพิ่ม 3.7 Pilot Results (13/51/36 + corr), 4. วัตถุประสงค์ (pilot→ต่อยอด) — **ยังเหลือ:** 7.7 time-series methodology, Gantt, งบ zero-budget, ประโยชน์ | `docs/proposal_th_draft.md` | — (ยังไม่เสร็จ — ต่อรอบหน้า) |
| กลางคืน | **Distill pipeline: SAM3 → U-Net เล็ก** — `src/train_unet_distill.py` 3 เฟส: (1) generate-pseudo: SAM3 → pseudo-GT masks (plant+leaf union) (2) train: U-Net ~2M params (BCE+Dice, augment flip/brightness, save best by val dice) (3) eval: mIoU/Dice/F1 + runtime — ตามแผน Tool Matrix ข้อ 5.3 (พัฒนาเอง) — ทดสอบ local 5 ภาพ 3 epochs ผ่าน (loss 1.45→1.32) — แก้บั๊ก: augment negative stride + decoder channel ลำดับ | `src/train_unet_distill.py` | compile ผ่าน; train/eval ทดสอบผ่าน (ข้อมูลจำลอง) — generate-pseudo ต้อง Colab GPU (SAM3) |
| กลางคืน | เขียน **Tool Evaluation Matrix** — แผนทดสอบ segmentation tools หลายตัวกับ TC (T1 SAM3 · T2 SAM2 · T3 SAM1 · T4 MobileSAM · T5 FastSAM · T6 Grounding DINO+SAM · T7 SAP · T8 YOLO-seg fine-tune · T9 U-Net · T10 DeepLab · T11 classical) + ตัวแปรทดสอบ + เมตริก (mIoU/Dice/F1/runtime) + **เกณฑ์ตัดสินใจ** (zero-shot ≥0.65 ชนะ → ไม่ใช่ fine-tune → ไม่ใช่พัฒนาเอง + root kill criterion) + protocol + checklist | `research/_tool_matrix.md` | — |
| กลางคืน | รีวิว feasibility: พบว่าเอกสาร (96/100) นำหน้างานจริง — verdict จริงใช้แค่ coverage_ratio (root_count คำนวณได้แต่ไม่ใช้ใน verdict) + ยังไม่เคย spike prompt "root" (kill criterion จาก grill v3 ยังไม่ทดสอบ) + ROI ไม่ชัด 36% + benchmark/GT ยังไม่มีตัวเลข → **เตรียม spike test root**: `src/root_spike_test.py` (ทดสอบ prompt plant/leaf/root, คำนวณ root_ratio + conf, ตรวจ kill criterion: เจอ root ≥50% + conf(root) ไม่ต่ำกว่า plant/leaf เกิน 0.15) — แก้บั๊ก load_images (images filter split) | `src/root_spike_test.py` | compile ผ่าน; load_images/filter/summarize ทดสอบผ่าน — ต้องรันบน Colab GPU |
| กลางคืน | **ทดสอบฉบับ "ความพร้อมอนุบาล" ใน Category Wizard (เต็มระบบ)** — ชื่อ/บทคัดย่อ/วัตถุประสงค์ใหม่ (ย่อ 94/1056/265) ได้ **96/100** (SCB 10X Cloud) — Unit 24/25 · Metric 24/25 · Scope 14/15 · Scope-Out 10/10 · Boundary 5/5 · Impact 19/20 · สาขา CS→CSAI (Tie-Breaking Rule 1: ยึดเป้าหมาย+องค์ความรู้) · ทางเลือก CSEB 72%, BIPT 65% — ยืนยันว่าเปลี่ยนโจทย์เป็นอนุบาลแล้วคะแนนไม่ตก | ทดสอบออนไลน์ | 96/100 — framing อนุบาลถูกต้อง |
| กลางคืน | **แก้ framing หลัก: subculture → ความพร้อมอนุบาล (acclimatization)** — ตามคำยืนยันเจ้าของโครงการ + grill v3 (29/07) · เปลี่ยนชื่อโครงงาน TH/EN, verdict เป็น ยังไม่พร้อม/พร้อมอนุบาล/ตรวจเอง (ROI ไม่ชัดหรือหนาแน่นเกิน), ระบบราก (root_ratio) = ตัวชี้วัดอันดับ 1, สมมติฐาน/RQ/บทคัดย่อ/metadata/confusion matrix/ประโยชน์ — ทำทั้ง proposal (28 จุด) + report (11 จุด) + scope lock + orchestration + ทำเครื่องหมาย subculture_criteria ตกรุ่น + สร้าง docx ใหม่ | `docs/proposal_th_draft.md`, `docs/report_th_v1.md`, `research/_scope_lock_new_round.md`, `research/_orchestration.md`, `research/subculture_criteria.md`, `docs/proposal_th_draft.docx` | grep ยืนยันไม่มี "ตัดย้าย/subculture" เหลือในเนื้อหา (เหลือเฉพาะชื่อ paper อ้างอิง + ตัวแปร metadata days_since_last_subculture) |
| กลางคืน | **ทดสอบยืนยันซ้ำ** — นำบทคัดย่อฉบับใหม่จากไฟล์จริง (ย่อ 1,232/1,500 ตัว) เข้า Category Wizard (Retry หลัง API ล่ม 1 รอบ) ได้ **96/100** (SCB 10X Cloud) — Unit 24/25 · Metric 24/25 · Scope 14/15 · Scope-Out 10/10 · Boundary 5/5 · Impact 19/20 · สาขา CS→CSAI อันดับ 1 · ทางเลือก BIPT 74% (ระบบย้ำไม่ควรจัด BIPT เพราะยึดคู่ (วัตถุ, ตัวชี้วัด) ไม่ใช่คำในชื่อ) | ทดสอบออนไลน์ (ผลบันทึกใน DEV_LOG) | 96/100 — ยืนยัน framing ใหม่ถูกต้อง |

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
