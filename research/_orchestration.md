# 🎯 VitroVision — Orchestration Tracker (Fable 5 = หัวหน้าออฟฟิศ)

> เริ่มรอบ: 2026-07-06 · target: **YSC 2027** สาขา CSBI
> อ่านคู่กับ `_backlog.md` (สถานะจริง) — ไฟล์นี้ = แผนแจกงาน + สถานะ deliverable

---

## 🔒 ตรึงแล้ว (อย่าถกซ้ำ)
- ชื่อ TH: **VitroVision — ระบบคัดกรองความพร้อมของการตัดย้ายเนื้อเยื่อด้วย Zero-Shot จากโมเดล SAM3 สำหรับพืชเพาะเลี้ยงเนื้อเยื่อ**
- ชื่อ EN: **VitroVision: A SAM3-Powered Zero-Shot Vision System for Subculture Readiness in Plant Tissue Culture**
- RQ: snapshot เดียว → triage 3 คลาส (wait / subculture / transplant-overdue) แบบ zero-shot ข้ามชนิดพืช (decision-support เท่านั้น)
- Engineering goal: Native Android app ถ่าย 1 รูป → mask + trait metrics + triage 3-class + confidence + manual override
- Segmentation engine: **SAM3 PCS text-prompted** (prompt เริ่ม `["plant","leaf"]`) — พิสูจน์ผ่าน spike test 2026-07-05 · **ห้ามใช้ SAM automatic/everything mode เด็ดขาด**
- สถาปัตยกรรม: cloud-primary (app → Roboflow SAM3 PCS API → mask/ผล → on-device feature extract + decision)

## 📐 นิยาม feature (ให้ fullstack + writer ตรงกัน)
- ROI = บริเวณขวด (crop จากระยะถ่ายคงที่ หรือ detect)
- `coverage_ratio` = area(plant∪leaf masks) / area(ROI)
- `height_proxy` = bbox_height(plant mask) / ROI_height
- `leaf_count` = จำนวน instance "leaf" (conf ≥ 0.5)
- `shoot_count` = จำนวน "plant"/"shoot" detections
- `glare_score` = สัดส่วน pixel ใน ROI ที่ V(HSV)>~0.95 & saturation ต่ำ (specular)
- Decision (rule-based, threshold รอ lab validate): wait / subculture / transplant-overdue + confidence (ลดเมื่อ glare สูง) + manual override เสมอ

## 📄 เอกสารเป้าหมาย
- YSC Proposal **ส่วน 1 เท่านั้น** (ภาษาไทยก่อน) = บทคัดย่อ → บทนำ(พีระมิด กว้าง→แคบ→gap→RQ) → วัตถุประสงค์ → สมมติฐาน → วัสดุอุปกรณ์ → **Methodology (เด่นพิเศษ + รูป pipeline/architecture)** → การวิเคราะห์ข้อมูล → แผนงาน(Gantt 2-3 เดือน) → ความเสี่ยง → ประโยชน์ → **Gen-AI disclosure (สำคัญ ใช้เต็มระบบ)** → บรรณานุกรม APA7
- ส่วน 2 (ประวัติผู้พัฒนา/อาจารย์) = เจ้าของโครงการกรอกเอง — **ไม่ต้องทำ**
- Diagram/infographic = **ภาษาอังกฤษเท่านั้น** + ต้องมี citation
- เทมเพลต: `ForFable/เทมเพลต YSC/YSC-Proposal_Template_040825.docx`
- ตัวอย่าง CS + guide: `ForFable/ตัวอย่างและวิธีการเขียน/*.pdf`

## 👥 คลื่นงาน
**Wave 1 (parallel — launch พร้อมกัน):**
- [ ] Researcher — citation pool ใหม่ (verify Consensus/PubMed) + เกณฑ์ subculture จาก lit + ยืนยัน ส่วน1/2 จาก NSTDA + งานวิจัย optimize
- [ ] Designer — architecture + pipeline diagram (EN, ระดับตีพิมพ์) + design system + wireframe แอป
- [ ] Fullstack — Android skeleton + Roboflow SAM3 PCS integration + feature extract + rule decision + result screen + regenerate spike overlay

**Wave 2 (หลัง Researcher ส่ง citation pool):**
- [ ] Writer — ร่าง Proposal ส่วน 1 (ไทย) ใช้ citation ที่ verify แล้วเท่านั้น + engineering spec doc

**Wave 3 (หลัง Writer+Fullstack+Designer):**
- [ ] Auditor — ตรวจ citation, โค้ด (SAM3 text-prompted compliance), ภาษาเอกสาร, UX/UI + สรุปสถานะ + สิ่งที่เจ้าของต้องตัดสินใจ

## ⛔ กติกา
ไม่ commit/push โดยไม่สั่ง · ทุก claim วิชาการ verify ก่อนเข้าเอกสาร · prose ไทย, diagram EN · ติดปัญหา → ทำ Ticket

## 🎫 Tickets (ปัญหาที่ต้องให้เจ้าของโครงการช่วย)
*(ยังไม่มี)*

## ❓ 4 จุดต้องถามเจ้าของโครงการ (ห้ามเดา)
1. ภาพขวดจริงเพิ่ม (high-density / ชนิดพืชอื่น)
2. เกณฑ์ "พร้อม subculture" ต้องยืนยันกับคนแล็บจริง (researcher หา rough จาก lit ไปก่อน)
3. ยืนยัน target = YSC 2027
4. ทดสอบแอปจริงในแล็บด้วย Samsung S24 FE (mobile data)
