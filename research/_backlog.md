# 📥 VitroVision v2 — Backlog & งานค้าง (living doc)

> จดอะไรก็โยนลง 📌 INBOX ได้เลย — `/vitro` จะ triage ให้
> สถานะ: 🔴 เร่ง · 🟡 กำลังทำ/ศึกษา · 🟢 ภายหลัง · 💤 รอเคาะ · ✅ เสร็จ
> อัปเดตล่าสุด: 2026-07-29 (บันทึกงาน 2026-07-08 ที่ยังไม่เคยจด + จับ drift โค้ด↔เอกสาร)

---

## 🧭 DIRECTION ปัจจุบัน (อัปเดต 2026-07-29 — อ่านตรงนี้ก่อนทุกอย่าง)

**สิ่งที่สร้าง:** **web app** สำหรับ **เจ้าหน้าที่แล็บ** ใช้ประเมิน/บอก **"ความพร้อมของพืชที่จะส่งให้เกษตรกร"**
**เลิกแล้ว:** Android app · การประเมิน "ความพร้อม sub-culture"
**vision ปลายทาง (ไม่ใช่ scope ที่สร้างรอบนี้):** แพลตฟอร์มแบบ Fastwork ที่เชื่อม **แล็บเพาะเลี้ยง ↔ เกษตรกร/ผู้ซื้อ** (เลือกพืชไปปลูก + สั่งให้แล็บเพาะให้) โดย VitroVision เป็น **ชั้นความน่าเชื่อถือ** ที่บอกว่าต้นพร้อมส่งจริง — **ห้ามเริ่มสร้าง auth 2 บทบาท/listing/order/chat/review รอบนี้**
**เป้าหมายเฉพาะหน้า:** exhibition งานสัปดาห์วิทยาศาสตร์ (พักเรื่องกำหนดการตามคำสั่ง)
**การออกแบบ + คำถามที่ยัง grill ค้างอยู่:** → `research/_grill_v3.md`

<details><summary>🔒 (ตกรุ่น) DIRECTION เดิม RQ 2026-07-05 — subculture triage</summary>

### (เก่า) DIRECTION RQ เคาะ 2026-07-05

**ชื่อโครงงาน:**
- EN: VitroVision — Zero-Shot Snapshot Triage for Plant Tissue-Culture Subculture Decisions
- TH: VitroVision — ระบบคัดกรองความพร้อม Sub-culture ของขวดเพาะเลี้ยงเนื้อเยื่อพืชด้วยภาพถ่ายเดียวแบบ Zero-Shot

**Research Question:** Can a low-cost snapshot imaging system prioritize plant tissue-culture vessels into wait / subculture / transplant-overdue classes using zero-shot or weakly-supervised visual phenotyping, across multiple plant types — without training a custom dataset per species? กรอบเป็น decision-support/triage เท่านั้น ไม่ใช่ระบบตัดสินชีววิทยาสุดท้าย

**เส้นทางเดิมที่เลิกแล้ว (อย่าลากกลับ):** full 3D reconstruction / COLMAP / refraction-mitigation / multisensor rig / SAM 3 gated / species-ID เป็นแกน — เหตุผลคือ user ประเมินแล้วว่าซับซ้อนเกินเวลา 2 เดือนที่เหลือ และไม่ตรง engineering goal ที่ต้องส่งงานได้จริง รายละเอียดเต็มอยู่ใน memory `project-vitrovision-v2`

**Pipeline ปัจจุบัน:** Capture (Android, มุม/แสงคงที่) → Preprocess (crop, glare est., polarized pair ถ้ามี) → Segment (**SAM3 PCS text-prompted `["plant","leaf"]`** — พิสูจน์ผ่าน spike test 2026-07-05 · ห้าม automatic/everything mode) → Extract features (coverage ratio, height proxy, shoot count, glare score) → Decision (rule-based ก่อน → lightweight classifier ทีหลัง) → Output 3-class + confidence + manual override
> หมายเหตุ: `_orchestration.md` (2026-07-06) ตรึง engine เป็น SAM3 PCS แล้ว (ต่างจากบรรทัดเก่าที่เขียน SAM2 backbone) — ยึด _orchestration.md เป็นหลัก

</details>

---

## ✅✅ FIRST PASS เสร็จครบ (2026-07-06 — one-shot Fable 5 orchestrator)
รัน `/vitro <บรีฟ>` แตกงาน 3 waves เสร็จ deliverable ครบ (ยังไม่ commit อยู่ใน working tree):
- `research/_orchestration.md` · `research/citation_gate.md` (18 refs verified + 3 flag) · `research/subculture_criteria.md` (rough threshold)
- `docs/proposal_th_draft.md` (YSC ส่วน 1 ครบ 13 ส่วน) · `docs/diagrams.md` (6 diagram EN)
- `src/android/` (app skeleton 15 ไฟล์ Kotlin) · `research/audit_report.md` (self-audit เจอ 2 HIGH code bug)
- **target ตรึงแล้ว = YSC 2027 สาขา CSBI**

### ✅ แก้ตาม audit เสร็จ (2026-07-06 รอบต่อ — verify จากไฟล์จริงแล้ว)
- [x] fullstack: HIGH #1 ROI (`RoiConfig` ปรับได้ + document เป็น extension point, ไม่สร้าง detector) · HIGH #2 empty-prediction guard (`ResultActivity.displayNoPredictionsError` แสดง error ไม่ตกเป็น WAIT ปลอม) · shoot_count confidence filter (≥0.5) · gap zone 0.70-0.80 รวมเข้า SUBCULTURE (document เหตุผล) · unit tests 15 เคส (`DecisionEngineTest.kt` + junit ใน build.gradle) · override button guard — ⚠️ *agent stall ตอนจบแต่โค้ดเสร็จครบ (verify แล้ว); test ยังไม่ได้รันจริง ต้อง Gradle/SDK*
  - เหลือ LOW: override label "ย้าย" vs "ย้ายได้" ยังไม่ harmonize (ไม่กระทบการทำงาน)
- [x] researcher: Thammasiri เจอใน Consensus แล้ว (index lag) · **แก้ author list Bethge ผิดทั้งชุด → Bethge, Winkelmann, Lüdeke, Rath** (verify PubMed PMID 37131210) · แก้ "7,420 ไร่"→"7,420 เอเคอร์ (~18,770 ไร่)" + "148 ประเทศ" ใน proposal · YSC 2027 ยังไม่ประกาศทางการ (เช็คซ้ำปลาย ก.ค./ต้น ส.ค. 2569) · แนะคง APA7

### ⏳ 4 จุดค้าง — รอเจ้าของโครงการ (ทีม unblock เองไม่ได้)
1. ชนิดพืชจริงในแล็บคืออะไร (ตั้ง threshold แม่นไม่ได้ถ้าไม่รู้)
2. ส่งภาพขวดจริงเพิ่ม (high-density / หลายชนิด) เพื่อ calibrate + เทสต์ SAM3
3. ทดสอบแอปด้วย Samsung S24 FE ในแล็บจริง
4. ยืนยัน target = YSC 2027 + deadline จริง (ปฏิทินยังไม่เจอ)

---

## 🎪 2026-07-29: **เป้าหมายใหม่ = จัด exhibition ในงานสัปดาห์วิทยาศาสตร์** (ไม่ส่ง YSC แล้ว)
เจ้าของโครงการแจ้งเอง — **ห้ามสมมติว่าเป็น YSC/CSBI แล้ววางแผนต่อ**

**นี่ไม่ใช่แค่เปลี่ยน deadline แต่เปลี่ยน deliverable ทั้งก้อน:**
- ของที่ต้องส่งมอบ = **ระบบที่เดโมได้จริงต่อหน้าคน** + สื่อหน้าบูธ (โปสเตอร์/บอร์ด/จอ) — **ไม่ใช่เอกสาร proposal**
- เกณฑ์ตัดสินความสำเร็จเปลี่ยนจาก "ระเบียบวิธีวิจัยรัดกุม" → **"กดแล้วขึ้นผลภายในไม่กี่วินาที ต่อหน้าคนแปลกหน้า ซ้ำได้ทั้งวัน"**
- ⏱️ วันวิทยาศาสตร์แห่งชาติ = 18 ส.ค. ของทุกปี → ถ้างานจัดช่วงนั้น **เหลือ ~3 สัปดาห์จาก 29 ก.ค. 2569** (วัน/สถานที่/รูปแบบจริงยังต้องให้เจ้าของโครงการยืนยัน)

**🔴 ผลกระทบเชิงเทคนิคที่ใหญ่ที่สุด — สแตก Colab+ngrok ไม่เหมาะกับการเดโมสด:**
Colab ตัด session เมื่อ idle/ครบเวลา · ngrok free เปลี่ยน URL ทุกครั้งที่รีสตาร์ต · wifi งานอีเวนต์ไม่นิ่ง → ถ้าหลุดกลางงานคือจบ ต้องเลือกสถาปัตยกรรมที่ทนงานจริง + มี fallback เสมอ

ผลกระทบต่อของเดิม:
- `docs/proposal_th_draft.md` เขียนตามฟอร์แมต YSC (13 ส่วน + APA7 + Gen-AI disclosure) — **ไม่ใช่ deliverable แล้ว** แต่ใช้เป็นคลังเนื้อหาสำหรับโปสเตอร์/สคริปต์เล่าหน้าบูธได้ดีมาก (บทนำ ประโยชน์ วิธีการ)
- ข้อจำกัด "ต้องมีคำถามชีววิทยาแบบ CSBI" **ไม่ผูกอีกต่อไป** → กรอบเป็นนวัตกรรม/ของใช้ได้จริงล้วนได้เลย (ตรงกับที่เจ้าของโครงการอยากทำมาตั้งแต่ 07-02)
- deadline 10 ก.ย. 2569 **ไม่ใช่ deadline ของเราแล้ว** — ตารางด้านล่างเก็บไว้เป็นข้อมูลอ้างอิงเฉยๆ
- งาน audit/citation gate ที่ทำไว้ยังมีค่า แต่ **ลดความสำคัญลง** — งานหน้าบูธไม่มีใครตรวจ APA7

<details><summary>📎 (อ้างอิง) ปฏิทิน YSC 2027 ทางการ — ยืนยันแล้ว 2026-07-29 แต่ไม่ใช่เป้าแล้ว</summary>

### YSC 2027 — ปฏิทินทางการ
**แหล่ง:** โพสต์ YSC Thailand Fanpage (เพจทางการ NSTDA, 30K followers) วันที่ **22 ก.ค. 2026 เวลา 13:22 น.**
หัวข้อ "9 สาขาหลัก 64 สาขาย่อยใน YSC 2027" → `facebook.com/YSCThailandFanpage`
(เว็บ `nstda.or.th/ysc` ยัง**ไม่มี**หน้า YSC 2027 ณ วันนี้ — เพจ FB เร็วกว่า)

**VitroVision = ครั้งที่ 29 (YSC 2027)** · สาขา **CSBI = ชีววิทยาเชิงคำนวณและชีวสารสนเทศศาสตร์ (Computational Biology and Bioinformatics)** อยู่ใต้สาขาหลัก **วิทยาการคอมพิวเตอร์ (Computer Science)** — *อ่านจาก infographic ควรเปิดภาพเต็มยืนยันชื่อ/รหัสซ้ำอีกครั้ง*

| วันที่ | รายการ |
|---|---|
| **5 – 25 ส.ค. 2569** ก่อน 17:00 | ลงทะเบียนผู้เข้าแข่งขันในระบบ SIMS (`nstda.or.th/sims`) — ครั้งแรก / อัปเดตข้อมูลถ้ามีชื่ออยู่แล้ว |
| 15 – 30 ส.ค. 2569 | อบรมออนไลน์ Soft Skill (ครบหลักสูตรได้เกียรติบัตร) |
| **🔴 26 ส.ค. – 10 ก.ย. 2569** ก่อน 17:00 | **รับสมัครข้อเสนอโครงการผ่าน SIMS ← deadline จริงของ proposal** |
| 15 ก.ย. – 9 ต.ค. 2569 | กรรมการพิจารณาข้อเสนอโครงการ |
| 12 ต.ค. 2569 | ประกาศผลข้อเสนอที่ผ่านการพิจารณา (เว็บ YSC) |
| ต.ค. – ธ.ค. 2569 | ระยะพัฒนาโครงงาน + ศูนย์ประสานงานจัดกิจกรรมแนะนำ |
| 28 ธ.ค. 2569 ก่อน 17:00 | ส่งรายงานฉบับสมบูรณ์ รอบภูมิภาค |
| 2 – 14 ม.ค. 2570 | แข่งรอบภูมิภาค (นำเสนอผลงาน) + พิธีมอบทุนระดับภูมิภาค |
| 15 ม.ค. 2570 | ประกาศผลผู้ผ่านเข้ารอบชิงชนะเลิศ |
| 7 – 9 ก.พ. 2570 | ประกวดรอบชิงชนะเลิศ |
| 25 – 26 ก.พ. 2570 | ค่ายคัดเลือกเยาวชนไปแข่งระดับนานาชาติ (เส้นทางสู่ ISEF) |

**⏱️ นับจาก 29 ก.ค. 2569:** เหลือ **7 วัน** ถึงเปิดลงทะเบียน · เหลือ **43 วัน** ถึงปิดรับข้อเสนอโครงการ
**หมายเหตุจากโพสต์:** ปีนี้โครงงานที่ทำวิจัย**ในสัตว์**ต้องยื่นหลักฐานการอบรม/ใบอนุญาตใช้สัตว์ทดลองของอาจารย์ที่ปรึกษา — *VitroVision ใช้พืช ไม่กระทบ*

</details>

---

## 🔀 2026-07-08 — งานที่ทำแล้วแต่ไม่เคยจด (พบตอน orientation 2026-07-29)
มี 4 ไฟล์ใหม่ใน `notebooks/` (untracked) ที่ **เปลี่ยนสถาปัตยกรรมจากที่เอกสารเขียนไว้**:
- `test_sam3.py` (13:46) — ลอง SAM3 ผ่าน `transformers.pipeline("mask-generation")` local
- `sam31_test.ipynb` (14:14) — SAM3 บน Colab T4 ผ่าน `Sam3Model`/`Sam3Processor` + upload รูป, ทดสอบ 5 prompt (`leaf/shoot/plantlet/stem/plant tissue culture`) · หมายเหตุในไฟล์: **`facebook/sam3.1` ไม่มี transformers integration → ใช้ `facebook/sam3`**
- `sam3_api_server.ipynb` (14:54) — **FastAPI + SAM3 self-hosted บน Colab + ngrok** เปิด `POST /segment` ให้ Android เรียก (แทน Roboflow)
- `vitrovison_cascade_api.ipynb` (15:41) — **cascade ใหม่:** tap บนรูป → `detect_bottles("glass jar bottle")` → match tap กับขวด → crop ROI อัตโนมัติ → segment `["leaf","plant","stem"]` ใน ROI → คืน coverage/height/width/greenness/hue + mask + overlay ผ่าน `POST /cascade`

### ⚠️ Drift ที่ต้องเคาะ (โค้ดใหม่ ≠ เอกสาร ≠ แอป) — 3 จุด
1. **Inference path:** เอกสาร (`proposal_th_draft.md` วัสดุ/วิธี/Gantt/Gen-AI disclosure, `diagrams.md`, `_orchestration.md:14`) = **Roboflow cloud** · โค้ดใหม่ = **self-hosted Colab+ngrok** · `RoboflowRepository.kt:34` ยังชี้ `https://detect.roboflow.com/` → แอปเรียก API ที่ backend ใหม่ไม่ได้ให้บริการ (`/segment`, `/cascade`)
2. **ROI:** `proposal_th_draft.md:167` เขียนชัดว่า "crop คงที่ — **ไม่ใช้ automatic detection ในเวอร์ชันแรก**" (ตรงกับที่ปิด audit HIGH #1 แบบ "ไม่สร้าง detector") · แต่ cascade notebook **สร้าง bottle detector จริง** + เพิ่ม interaction ใหม่ (tap เลือกขวดจากหลายขวด) ที่ wireframe/diagram ยังไม่มี
3. **หน่วยวัด:** cascade คืน `height_cm`/`width_cm` จาก `PIXEL_TO_CM = 0.1  # placeholder` → เป็นตัวเลขที่ยัง**ไม่ calibrate** ห้ามให้ขึ้น UI หรือเข้าเอกสารในฐานะ "เซนติเมตร" (ผูกกับข้อค้าง "เขียน feature-extraction spec" ด้านล่าง)

### ยังยืนยันไม่ได้ (ในรีโปไม่มีหลักฐาน)
- notebook ทั้ง 3 ไฟล์ **ไม่มี cell output เก็บไว้** → บอกไม่ได้ว่ารันผ่านจริงหรือยัง (ผลอาจอยู่ฝั่ง Colab/Drive)
- `test_sam3.py` กับ notebook ใช้ **API สองแบบที่เข้ากันไม่ได้** สำหรับโมเดลเดียวกัน (`pipeline(text_prompts=...)` vs `Sam3Processor` + `post_process_instance_segmentation`) → อย่างมากถูกได้แค่แบบเดียว ต้องเคาะก่อนเขียนลง Methods
- `test_sam3.py:48` เรียก `ImageDraw.Draw` แต่ import แค่ `Image` (บรรทัด 4) → path fallback พังแน่นอน = หลักฐานว่ากิ่งนั้นไม่เคยรัน

### 🔴 ยังไม่ commit อะไรเลย
repo มีแค่ 3 commit (ล่าสุด = `65069b9 docs: add v2 backlog`) · deliverable ทั้งหมดตั้งแต่ 07-06 ถึง 07-08 **อยู่ใน working tree ไม่มี git history** (ตรวจแล้ว: ไม่มี secret ฝังในไฟล์ — `notebook_login()` เป็น interactive, API key อยู่ใน `BuildConfig`) → commit ได้ปลอดภัย รอคำสั่งเจ้าของโครงการ

---

## 📌 INBOX (จดเร็ว ยังไม่ triage)
*(ว่าง)*

---

## 🔴 เร่ง / ตัดสิน feasibility
- [ ] verify citation จาก 9 hand-off PDF ผ่าน Consensus/PubMed จริง (ยังไม่ผ่าน citation gate)
- [ ] นิยามเกณฑ์ "พร้อม subculture" ร่วมกับคนในแล็บ (coverage/height/shoot count threshold ต่อชนิดพืชที่มีจริง)
- [ ] ทดสอบ segmentation บนภาพขวดจริงอย่างน้อย 1 ใบ (ยังไม่มีใครทดสอบเลย — engine เป็นแค่ config ที่สลับได้ผ่าน Roboflow ไม่ใช่จุดตัดสินใจใหญ่แล้ว)
- [ ] เขียน feature-extraction spec ที่แม่นยำ (สูตรจริงของ coverage ratio/height proxy/shoot count จาก mask ที่ Roboflow ส่งกลับ)

## ✅ Infra พร้อมใช้ (2026-07-05)
- [x] Roboflow account + MCP server เชื่อมต่อแล้ว (`claude mcp list` = Connected), มี API key พร้อมใช้
- [x] `inference-sdk` ติดตั้งใน conda env `ml` แล้ว
- [x] เข้าถึง SAM2+SAM3 ผ่าน endpoint เดียวกันได้ — เลือกโมเดลคือ config swap ไม่ใช่ตัดสินสถาปัตยกรรมใหม่ทุกครั้ง (อย่าลากกลับมาถกอีก)

## ✅✅ SPIKE TEST ผ่านแล้ว (2026-07-05) — go/no-go หลักของโปรเจกต์
ทดสอบจริงกับภาพขวดจริง 1 ใบ (`20260518_184506.jpg`, ขวด low-density) ผ่าน Roboflow workflow_specs_run:
- **SAM2 unprompted ("segment everything" mode): ล้มเหลว** — fragment เป็น mask เล็กๆ 1-10px กว่า 90 ชิ้น (จับ glare/ไอน้ำ/สะท้อนแสง ไม่ใช่พืช) ตรงกับที่ literature เตือนไว้ว่า automatic mode ใช้ไม่ได้ในโดเมนนี้
- **SAM3 text-prompted (PCS, prompt=["plant","leaf"]): ผ่านชัดเจน** — ได้ 1 "plant" detection (conf 0.71, ครอบก้าน/ลำต้นทั้งกลุ่มแม่นยำ) + 17 "leaf" detections แยกใบทีละใบ (conf 0.57-0.91) แม่นยำมาก **แม้ผ่านกระจกขวด+glare+ไอน้ำ**
- ภาพ overlay อยู่ที่ scratchpad `imgA_sam3_overlay.png` (ดูใน session 2026-07-05)
- **สรุป:** domain-shift risk ที่กังวลกันมาตลอด (กระจก/glare/ไอน้ำ) ไม่ใช่ตัวบล็อกจริง **ถ้าใช้ text-prompted concept segmentation (SAM3 PCS) แทน unprompted/automatic mode** — นี่คือ finding สำคัญที่สุดของ spike, ต้องใส่ไว้ใน pipeline spec: **ห้ามใช้ SAM automatic/everything mode เด็ดขาด ใช้ text prompt หรือ box prompt เสมอ**
- ยังไม่ทดสอบภาพขวด high-density (ภาพกว้าง) — ทดสอบเพิ่มได้ภายหลังถ้าต้องการความมั่นใจเพิ่ม แต่ gate หลักผ่านแล้ว

## 🟡 กำลังศึกษา
- [ ] แหล่ง polarizer คู่ + clip-on mount ราคาถูกสำหรับ Android
- [ ] ทางเลือก decision layer เบา (rule-based → Logistic/XGBoost/MLP)

## 🟢 ภายหลัง
- [ ] เก็บ label จริงจากคนแล็บ (ready/borderline/not ready) เพื่อทำ few-shot refinement
- [ ] ต่อยอด metadata (media/PGR/genotype/อายุรอบเลี้ยง) เข้าโมเดล optimization ภายหลัง (ไม่ใช่แกนหลักของรอบนี้)

## 💤 รอเคาะ (decision ค้าง)
- [ ] target แข่งยังไม่เคาะ: YSC 2027 / JSTP / TTFR 2026

## ✅ เสร็จ
- [x] เคาะ Research Question + engineering goal + pipeline ใหม่ (2026-07-05, ผ่าน Consensus 9 รอบ)
- [x] ตั้งชื่อโครงงานไทย/อังกฤษ (2026-07-05)
- [x] เคาะ model/runtime decision: SAM2 cloud (dev backbone) + MobileSAM/EdgeSAM on-device fallback, box-prompted เสมอ (2026-07-05, ผ่าน Consensus 4 รอบเพิ่ม)

---

## 🔒 v1 (archived — อ้างอิงได้)
- Local: `Projects/Other/_VitroVision_v1_ARCHIVE_2026-07-01/`
- GitHub: tag `v1-final` + branch `archive/v1`

## 🔒 v2-early (archived ทางความคิด — อ้างอิงได้แต่ไม่ใช้แล้ว)
- เส้นทาง 3D/COLMAP/refraction/SAM3/species-ID ที่คุยกันช่วง 2026-07-01–02 ถูกแทนที่ด้วย RQ ด้านบนแล้ว
