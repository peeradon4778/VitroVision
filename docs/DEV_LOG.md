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
| เช้า–บ่าย | วิเคราะห์ผลรัน Colab ชุด 100 ขวดพริกจินดา (`data/raw/20260814_batch`) — จัดกลุ่ม verdict 3 กลุ่ม + ตรวจความสัมพันธ์ระหว่าง features + เตรียมผลสรุปสำหรับรายงาน/การนำเสนอ | `notebooks/sam3/colab_run_v2_clean.ipynb` (ผลอยู่ใน Downloads/Colab) | **ผลจริง:** 13 พร้อมอนุบาล / 51 ยังไม่พร้อม / 36 ROI-ไม่ชัด-ตรวจเอง; corr leaf↔coverage 0.760, coverage↔height 0.716, green↔healthy 0.922, leaf↔shoot 0.538, coverage↔area 0.932; **100 ขวด/~15 นาที** · ⚠️ (อัปเดต 2026-08-25) ยังไม่พบไฟล์ผลลัพธ์ `plant_growth_summary.csv` ของชุด 100 ในเครื่อง — ต้อง rerun/ดึงจาก Drive ก่อนนำไปอ้างอิงเป็นหลักฐาน |
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

## 2026-08-25 — ตรวจภาษา report v1 (รอบที่ 1–3)

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| กลางวัน | ตรวจภาษา 3 รอบ (คู่มือ ระยะที่ 4) — แก้จุดไวยากรณ์/ความชัดเจน/ความสม่ำเสมอ โดยไม่แตะเนื้อหาทางเทคนิคหรือ [FACT]/[PLAN]: (1) "ด้วย…ด้วย" ซ้ำใน 3.1 → "โดยใช้พรอมป์" (2) "กลไกกันความผิดพลาด" → "กลไกป้องกันความผิดพลาด" (3) "กัน verdict ผิดพลาด" → "ช่วยป้องกันการให้ผลผิดพลาด" (4) "โดยแรงงานคิดเป็น" → "โดยค่าแรงงานคิดเป็น" (แม่นตามบริบทต้นทุน) (5) "ขวดแก้วที่มีแสงสะท้อน…" → "ขวดแก้วภายใต้แสงสะท้อน…" (glare ไม่ใช่สมบัติของขวด) | `docs/report_th_v1.md` | grep ยืนยันไม่เหลือ variant เก่า; อัปเดตสถานะ + checkbox ภาษา = เสร็จ (เหลือ ตรวจ render ใน Word) |

## 2026-08-25 — core generalize: augment บริบทขวด + cross-species split

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| กลางคืน | เพิ่ม **augmentation เชิงบริบทขวดแก้ว** ใน SegDataset._augment — หมุนเล็กน้อย (มุมถ่าย) + brightness/contrast (glare/ฝ้า/แสง) + จุด specular glare (ไม่แตะ mask) + Gaussian blur (ไอน้ำ) + พลิก — ทุกค่าใช้กับ img/mask พร้อมกัน mask ไม่เพี้ยน | `src/train_unet_distill.py` | รัน 200 iters: shape ตรง, mask คง binary {0,1}, img อยู่ช่วง [0,1] — ผ่าน |
| กลางคืน | เพิ่ม **cross-species split** — `_detect_species` (หาโฟลเดอร์ย่อยต่อชนิด) + `_split_by_species` (แยก train/val ตามชนิด + holdout อัตโนมัติหรือระบุ) + CLI flag `--species-holdout` — วัด zero-shot generalization ข้ามชนิด (train ไม่เห็นชนิด val) | ไฟล์เดิม | test 4 กรณี: single-species→[], multi-species→2, auto-holdout→ชนิดมากสุดเป็น val, ระบุ holdout—ผ่าน |

## 2026-08-25 — audit + จัดระเบียบ repo (ลบซ้ำ/ย้ายโมเดล)

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| กลางคืน | audit ข้อมูล/ผลใน repo — พบผลลัพธ์ (51 แถว) ≠ ชุดข้อมูล 100 ภาพ, ข้อมูลภาพขวดชุด 100 เก็บซ้ำ 2 ที่ (zip+โฟลเดอร์ 219MB, manifest md5 ตรงกัน), ไฟล์ชั่วคราว/โมเดลกองนอก repo · ลบ zip ซ้ำ + file lock Word + scratch (`_ysc/`, `_render_check/`) + ย้าย `yolov8n-seg.pt` root→`models/` + อัปเดต default path ใน 2 โค้ด · สร้าง `research/audit_data.md` | `research/audit_data.md`, `src/benchmark_baselines.py`, `src/benchmark_colab.py`, `models/yolov8n-seg.pt` | ลบ/ย้ายสำเร็จ; compile 2 โค้ดผ่าน; git track ยังสะอาด (74) — **ค้าง: รัน pipeline บนชุด 100 ภาพก่อนทำ time-series** |

## 2026-08-25 — แก้เอกสารกันพิรุจ: ผล 100 ขวดเป็น [PLAN] + ข้อมูลสอดคล้อง

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| กลางคืน | ตรวจร่องรอยพิรุจ (ความไม่สอดคล้องเอกสาร/ข้อมูล) — พบ report/proposal อ้างผล 100 ขวด (13/51/36, r-corr, 36%) เป็น `[RESULT]` แต่ **ไม่มีไฟล์ผลลัพธ์ `plant_growth_summary.csv` ของชุด 100 ในเครื่อง/Drive/OneDrive** (ทุก notebook outputs=0, `03_ผลการทดลอง` ว่าง) · แก้: report+proposal ผล 100 ขวด → `[PLAN]`/รอผลจริง; แก้ "4 ชนิด"→ชนิดเดียว; แก้ข้อเสนอแนะ 36%; DEV_LOG/scope_lock เพิ่มหมายเหตุซื่อตรง (ไม่ลบตัวเลข แต่ชี้ว่ายังไม่มีหลักฐาน — ต้อง rerun/ดึงจาก Drive) | `docs/report_th_v1.md`, `docs/proposal_th_draft.md`, `docs/DEV_LOG.md`, `research/_scope_lock_new_round.md` | grep ยืนยัน report+proposal ไม่มีผล 100 อ้างเป็นจริง ✓; DEV_LOG มีหมายเหตุซื่อตรง |

## ข้อควรทำต่อ (backlog)

- [x] ~~รัน Colab รอบ 2 ด้วย notebook ใหม่~~ → **ทำแล้ว 18/08** (`colab_run_v2_clean.ipynb`) — ผล 100 ขวดพริกจินดา: 13 พร้อมอนุบาล / 51 ยังไม่พร้อม / 36 ROI-ไม่ชัด-ตรวจเอง · ⚠️ ไฟล์ผลลัพธ์ยังไม่มีในเครื่อง ต้อง rerun/ดึงจาก Drive
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

## 2026-08-26 — เตรียมส่งข้อเสนอ YSC 2027 (สาขา CSAI) + ประกอบเนื้อหาลง template ทางการ

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| เช้า | ทำความเข้าใจการเขียนข้อเสนอจาก YSC FAQ (100 ข้อ) + คู่มือ YSC2027 + คลังแบบฟอร์ม/โลโก้ — เก็บ key rules (ผ่าน SIMS, หน้าปกจาก SIMS, PDF=ปก+8 หัวข้อ+ประวัติย่อ, ต่อเนื่องต้อง Form 6, Gen-AI ห้ามเขียนข้อเสนอแทนนักเรียน, Form 2C ถ้าทำในแล็บ ม.) | `research/` (อ้างอิง), `docs/` | เก็บข้อมูลครบ 100 Q&A + กติกา deadline/สาขา |
| เช้า | สร้าง **เช็กลิสต์แบบฟอร์ม** ที่ต้องส่ง (รอบข้อเสนอ/ชิง) — ต้องส่งทุกโครงงาน vs ส่งเมื่อเกี่ยวข้อง | `docs/YSC_FORMS_CHECKLIST.md` | ครบ 11 ข้อรอบข้อเสนอ + จุดเสี่ยง (2C/3/6, Gen-AI, template 200726) |
| เช้า | แก้ **สาขา CSBI → CSAI (AI/ML)** ตาม Category Wizard 96/100 + เพิ่ม **ส่วน 14 ประวัติย่อ** (เทมเพลตให้กรอก) | `docs/proposal_th_draft.md` | ยืนยันไม่มี "CSBI" เหลือ; ส่วน 14 ครบ |
| เช้า | สร้าง **คู่มือส่งข้อเสนอใน SIMS** (สมัคร/สร้างปก/ประกอบ PDF/อัปโหลด + ข้อควรระวัง) | `docs/SIMS_SUBMISSION_GUIDE.md` | ครบขั้นตอนตาม FAQ |
| สาย | ดาวน์โหลด **template ทางการ** `YSC-Proposal_Template_200726.docx` (283KB) + ส่องโครงสร้าง (290 ย่อหน้า/4 ตาราง, ฟอนต์เดิม TH Sarabun New 15pt, ระยะขอบ 1.905/2.54cm) | `docs/_ysc_template/` | โหลดผ่าน, อ่านโครงสร้างครบ |
| สาย | เขียน **`docs/build_ysc_proposal.py`** — เติมเนื้อหาลง template โดยตรง (คงโครงสร้าง, ลบ placeholder สีเทา/มนุษย์-สัตว์/สารเคมี, ฟอนต์ **TH Sarabun PSK 16pt**, แทรกรูป, เติมตาราง Gantt/Definitions, ดึงบรรณานุกรมจาก draft) | `docs/build_ysc_proposal.py` | รันผ่าน; ลบขยะ 94 ย่อหน้า; 12 หน้า; render PDF (Word COM) ตรวจถูก |
| สาย | สร้าง **รูป architecture** (matplotlib, English labels) + **โลโก้เครื่องมือ** (Claude/Colab/HuggingFace PNG) + เพิ่ม section เครื่องมือ/Gen-AI พร้อมโลโก้ | `docs/assets/vitro_architecture.png`, `docs/assets/logos/*.png` | รูป render สวย; โลโก้ 3/4 (roboflow 403 → ชื่อเปล่า) |
| กลางคืน | เตรียม **Colab run สะอาด** ชุด 100 ขวด + config.json (แก้ช่องโหว่หลักฐานผลลัพธ์ `plant_growth_summary.csv`) | `notebooks/sam3/colab_run_v2_evidence.ipynb`, `config.json` | ipynb valid; `load_config` อ่าน config ถูกครบ |
| กลางคืน | **Benchmark baseline** บนชุด 100 ภาพ (classical + YOLO-seg, CPU): runtime 0.43s/0.30s, area 1.36%/49.4% เฟรม, classical พัง 23/100 | `data/processed/benchmark_classical_yolo/benchmark_summary.csv` | รัน 100 ภาพ ~2 นาทีผ่าน; YOLO (COCO) ไม่ valid เพราะไม่มี class plant |

> ⚠️ ยังไม่เสร็จ (ค้าง): รวม Gen-AI disclosure 2 จุด, หน้าปก/รหัสโครงการ SIMS, กรอกประวัติผู้พัฒนา, ยืนยันผลนำร่อง 100 ขวด — หมายเหตุ commit เป็นจุดพักก่อน

## 2026-08-26 — ยืนยันผลนำร่อง 100 ขวดจริง (หลักฐานจาก Colab) + อัปเดตเอกสาร

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| บ่าย | รัน `sam3_growth_pipeline.py` ชุดจริง 100 ขวดพริกจินดา (20260814_batch) บน Colab T4 และแก้บั๊กหน่วยความจำ (เก็บ mask แค่ 6 ภาพแรก กัน RAM พัง ~51) — ได้ผลลัพธ์จริงครบ 100 ภาพ | `data/processed/plant_growth_summary.csv` | **verdict: 14 พร้อมอนุบาล / 51 ยังไม่พร้อม / 35 ROI-ไม่ชัด-ตรวจเอง [RESULT]** · corr: coverage↔area 0.949, ใบ↔coverage 0.852, เขียว↔healthy 0.910, coverage↔height 0.701, ใบ↔shoot 0.534 |
| บ่าย | ตรวจความถูกต้อง/ซื่อตรงของผล — verdict แยกจาก coverage ชัด (พร้อมอนุบาลทุกภาพ cov≥0.20, ROI-ไม่ชัดทุกภาพ cov<0.075) · **พบข้อจำกัดสำคัญ: root_count≥1 มีแค่ 1/100** (prompt "root" จับรากผ่านขวดแก้วไม่ได้) · canopy_h/w_cm เป็น NaN ทั้งหมด (pixel_to_cm ยังไม่ calibrate) | `data/processed/plant_growth_summary.csv` | **[RESULT + OPEN]** root_ratio ยังวัดได้จริงไม่ได้ — ตรงกับประเด็นที่ต้องปรับปรุงพรอมป์/วิธี, ต้อง calibrate หน่วย |
| บ่าย | อัปเดต `report_th_v1.md` + `proposal_th_draft.md`: เปลี่ยนผลชุด 100 จาก `[PLAN]` → `[RESULT]` (14/51/35 + corr จริง) + เพิ่มหมายเหตุซื่อตรงข้อจำกัดระบบราก/calibration | `docs/report_th_v1.md`, `docs/proposal_th_draft.md` | grep ยืนยันไม่เหลือผล 100 เป็น `[PLAN]` (คงไว้เฉพาะ baseline/ground truth) |

## 2026-08-26 — วางแผน ground truth + validation (ชุด 100 ขวด)

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| บ่าย | สร้างแผนตรวจสอบความถูกต้อง 3 ระดับ (A. segmentation mIoU/Dice, B. ค่าวัด Pearson/MAE/RMSE, C. verdict confusion matrix/accuracy/sensitivity≥0.6) + protocol วัดมือ + sampling + inter-rater (ICC/Cohen's kappa) + เกณฑ์ตัดสิน | `docs/VALIDATION_PLAN.md` | ครบ 8 หัวข้อ;☁ หมายเหตุ: root_count ยังวัดไม่ได้ (1/100) → ฝาก validate ใต้ root ไว้หลังปรับปรุงการตรวจจับราก |
| บ่าย | สร้างเทมเพลต `ground_truth.csv` 100 แถว ชื่อภาพตรงกับ batch (001–100.jpg) + คอลัมน์ expert_verdict | `docs/assets/ground_truth_template.csv` | 100 แถว, ตรงชื่อภาพ 100% — พร้อมกรอกค่ามือ |
| บ่าย | ปรับ label verdict เก่าใน DATA_TEMPLATES (wait/subculture → ยังไม่พร้อม/พร้อมอนุบาล/ตรวจเอง) | `docs/DATA_TEMPLATES.md` | grep ยืนยันไม่เหลือ label เก่า |

## 2026-08-26 — สคริปต์ verdict confusion matrix (Level C) + เชื่อมแผน validation

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| บ่าย | เขียน `src/validate_verdict.py` คำนวณ verdict confusion matrix (accuracy / per-class precision·sensitivity·F1 / macro-F1 / MCC / Cohen's kappa) เทียบ expert_verdict กับ verdict ของ SAM3 | `src/validate_verdict.py` | compile ผ่าน; smoke-test 100 แถว: Accuracy 0.92 / MCC 0.869 / kappa 0.867 — ทำงานครบ ใช้ได้เมื่อมี ground_truth จริง |
| บ่าย | เชื่อมคำสั่งรันเข้าแผน validation (ขั้นตอนที่ 4) | `docs/VALIDATION_PLAN.md` | ครอบคลุมทั้ง 3 ระดับ (A/B/C) |

## 2026-08-26 — validation vs มือ → เปลี่ยนเกณฑ์ความพร้อมใหม่ (coverage → วามสูง) + ผ่าน H₂

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| บ่าย | กรอกค่าอ้างอิงจากมือ (ground_truth) 100 ภาพ แล้วแปลง/คำนวณ area_cm2 + ระบุ verdict | `docs/assets/ground_truth_template.xlsx` → `data/processed/ground_truth.csv` | 100 แถว; expert_verdict: 60 พร้อมอนุบาล / 38 ยังไม่พร้อม / 2 ตรวจเอง; 20 ภาพหนาแน่นเกิน (leaf>30 / หลายต้น) กัน correlation |
| บ่าย | Validation ระดับ B (covid กับมือ) + C (confusion matrix) | `data/processed/verdict_confusion_*.csv` | B: leaf r=0.585, shoot 0.483, height 0.638, width 0.477, root 0.150, area 0.398 · **C: กฎ coverage เดิม acc=0.43, sens=0.15 (ไม่ตรงกับมือ)** |
| บ่าย | **ข้อค้นพบ:** เกณฑ์ความพร้อมของผู้เชี่ยวชาญ = "ต้นสมบูรณ์/โตพอ/พร้อมย้าย" ไม่ใช่ความแน่น → **coverage ใช้ผิดตัวชี้วัด**; ความสูง (height_proxy) จำแนกถูกกว่า | `docs/VALIDATION_PLAN.md` | sweep + 5-fold CV: height≥0.275 → acc 0.755 / sens 0.917 / MCC 0.472 (**ผ่านเป้า H₂** acc≥0.7, sens≥0.6) |
| บ่าย | เปลี่ยน rule ในโค้ด: coverage → `height_proxy ≥ READY_HEIGHT(0.275)` (configurable) + ลดคลาส "ตรวจเอง"/"หนาแน่นเกิน" | `src/sam3_growth_pipeline.py` | compile ผ่าน; verdict ใหม่: 75 พร้อมอนุบาล / 25 ยังไม่พร้อม |
| บ่าย | อัปเดต report/proposal: เกณฑ์/verdict/validation (H₂ ผ่าน / root ยังใช้ไม่ได้) + ยอดย่อ | `docs/report_th_v1.md`, `docs/proposal_th_draft.md` | grep ยืนยันไม่มีเลขเก่า 14/51/35 ค้าง |

## 2026-08-27 — Trait-level baseline benchmark: SAM3 vs classical vs YOLO-COCO (เทียบค่าวัดมือ)

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| เย็น | เขียน `src/benchmark_traits.py` — เปรียบเทียบ proxy ของ "ขนาดต้น" ที่แต่ละวิธีได้จาก segmentation กับค่าที่วัดมือ (`height_cm`, `area_cm2`) ด้วย Pearson r (scale-free: proxy เป็น px เทียบกับ cm ได้โดยไม่ต้องสอบเทียบหน่วย) + คำนวณอัตราล้มเหลว (mask=0) + เวลาเฉลี่ย/ภาพ | `src/benchmark_traits.py` | compile ผ่าน; รันชุดจริง 100 ภาพ (CPU ~90s) |
| เย็น | รัน bench กับชุดภาพจริง 100 ขวดพริกจินดา เทียบ SAM3 (จาก summary) vs classical (HSV เขียว) vs YOLO-seg (COCO pretrain = naive reference)
 | `data/processed/trait_benchmark/trait_benchmark_summary.csv`, `trait_benchmark_merged.csv`, `height_correlation.png`, `trait_compare_bar.png` | **ความสูง (r เทียบมือ): SAM3 0.638 > classical 0.498 > YOLO-COCO 0.133 (n=100)** · พื้นที่ (r, n=80): SAM3 0.398 > classical 0.261 > YOLO-COCO 0.050 · อัตราล้มเหลว mask=0: SAM3 0.01, classical 0.23, YOLO 0.13 |
| เย็น | อัปเดต report/proposal: เพิ่มผล baseline ระดับค่าวัด ([RESULT]) ใน 4.4 / 7.6.0 + เปลี่ยนจุด [PLAN] ระดับพิกเซลเป็น [OPEN-RESULT บางส่วน] (mIoU/Dice ยังต้อง annotate ground-truth masks) | `docs/report_th_v1.md`, `docs/proposal_th_draft.md` | grep ยืนยันไม่เหลือ baseline เป็น [PLAN] ล้วน — แยกชัด ระดับค่าวัด=[RESULT] / ระดับพิกเซล=[PLAN] |

> **ข้อสรุป (Trait-level):** SAM3 ตรงกับค่าวัดมือมากกว่า baseline อย่างชัดเจนด้านความสูง (r=0.638) และล้มเหลวน้อยกว่า (1% vs 23%/13%) — สนับสนุน Orvati Nia et al. (2026) ที่ SAM3 ดีสุดในโหมด detector-free · YOLO-COCO ไม่มี class "plant" จับทั้งฉากแทนต้น (ต้อง fine-tune) · **หมายเหตุความซื่อตรง:** ค่านี้คือความสอดคล้องกับมือ ไม่ใช่ mIoU/Dice ระดับพิกเซล (Level A) ซึ่งยังต้อง ground-truth masks [OPEN] · รูปถ่ายเป็นมุมเดียว ยังไม่ครอบคลุม 3D/refraction

## 2026-08-27 — เตรียม cross-species test (pipeline + โปรโตคอล) แบบพร้อมรันทันทีเมื่อมีข้อมูล

| เวลา | สิ่งที่ทำ | ไฟล์ | ผลการทดสอบ |
|---|---|---|---|
| เย็น | เขียน `src/benchmark_cross_species.py` — ประเมิน SAM3 แบบ zero-shot ข้ามชนิด: collect ภาพต่อชนิด (โฟลเดอร์ย่อย=ชนิด หรือ species_map.csv) → รัน `analyze_image` (รีไซเคิล pipeline) → สรุป mean±std ต่อชนิด + zero_mask_rate + verdict dist · ถ้ามี GT → Pearson r (height/area vs มือ) + generic_ac น์ต่อชนิด + กราฟ | `src/benchmark_cross_species.py` | py_compile ผ่าน; collect รูปแบบ A (โฟลเดอร์ย่อย) + B (species_map) ตรงทั้งคู่; helper pearson/accuracy ทำงานถูก |
| เย็น | สร้างโปรโตคอลเก็บข้อมูลข้ามชนิด — เงื่อนไขการถ่ายให้เหมือนชุดพริกจินดา, จำนวนขวด/ชนิด (≥10 เป็นปี, ≥5= pilot), รูปแบบจัดเก็บ A/B, ค่าวัดมือ GT, คำสั่งรัน Colab, วิธีตีความผล | `docs/CROSS_SPECIES_PROTOCOL.md` | ครบหัวข้อ 7; ชี้ 2 สิ่งที่ต้องตอบในผล: segmentation transfer ได้ไหม (zero_mask_rate ต่ำ) vs readyness threshold transfer ได้ไหม (generic_acc ต่อชนิด) |
| เย็น | ตรวจข้อมูลที่มี — **พบว่ายังไม่มีภาพชนิดอื่นใน repo/เครื่อง** (v1 archive = aruco+ผลเก่า, slide_photos = ภาพกลุ่ม, clones = เอกสาร) → cross-species ต้องรอถ่ายชนิดใหม่ในแล็บ (2-3 ชนิด ก่อน ตัวอย่างเล็ก= pilot) | data scan | ยืนยันไม่มีชุด cross-species; ต้องใช้ `docs/CROSS_SPECIES_PROTOCOL.md` เก็บข้อมูลก่อนรัน |

> **สถานะ:** cross-species = [PLAN → พร้อมรัน] · นักได้สร้าง pipeline + โปรโตคอลแล้ว แต่**ยังไม่มีข้อมูลชนิดอื่น** (รอถ่ายในแล็บ 2–3 ชนิด ก่อน · ชุดเล็ก = pilot ต่อชนิด) · คำถามเชิงวิทยาศาสตร์ที่ตอบ: (1) segmentation ข้ามชนิดไหม (2) เกณฑ์ readyness transfer ได้ไหม

## แม่แบบ entry ใหม่ (คัดลอกไปใช้)

```md
| วันที่ | สิ่งที่ทำ: <เปลี่ยนอะไร ทำไม อย่างไร> | <ไฟล์> | <ผลเทสต์: เทสต์อะไร ได้ผลอะไร> |
```
