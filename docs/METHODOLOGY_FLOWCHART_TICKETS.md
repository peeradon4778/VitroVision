# 🔖 Ticket: สร้างภาพประกอบ Flowchart 3 ภาพ (ระเบียบวิธี/สถาปัตยกรรม)

> สร้าง 2026-09 · ใช้ควบคู่ `docs/proposal_ysc.md` (มาตรา 5) และ `docs/_make_flowcharts.py`
> เครื่องมือวาด: **Draw.io** (user) · แก้ไข script + commit/push (pi)
> **ลำดับ:** ทำทั้ง 3 ภาพ → อัปเดต link ใน `proposal_ysc.md` → **commit + push** → ค่อยทำงานอื่นต่อ

---

## ⏱ ขั้นตอนที่ต้องทำ (สั่งได้ทีเดียว)

### [ ] STEP 1 — ตรวจภาพเดิมใน repo (ฐานอ้างอิง)
- [ ] เปิด `docs/assets/flow_overview.png`, `flow_pipeline.png`, `flow_validation.png` (เดิมมีอยู่) เพื่อดูโครงสร้างที่เคยวาด
- [ ] เปิด `docs/_make_flowcharts.py` (script เดิมที่ generate flowchart) เผื่อดัดแปลง/นำโครงสร้างมาใช้
- [ ] ตัดสินใจ: วาดใหม่บน Draw.io หรือ adapt จากเดิม

### [ ] STEP 2 — วาดภาพที่ 1: ภาพรวมระบบ (System Overview)
- [ ] Nodes: ถ่ายภาพขวด → ตรวจจับ ROI ขวด → แบ่งส่วนต้น (U-Net) → คำนวณ feature (6 กลุ่ม) → ตัดสินใจ verdict
- [ ] แทรกกล่อง "ภาพไม่ชัด → ส่งมนุษย์ตรวจ" (อยู่ตรงขั้นประเมิน)
- [ ] ระบุสถาปัตยกรรม: U-Net + MobileNetV3-Small (~3.6M params, val_dice ≈ 0.98)

### [ ] STEP 3 — วาดภาพที่ 2: สถาปัตยกรรม U-Net (Architecture) ← ใหม่
- [ ] **Encoder:** MobileNetV3-Small (ImageNet weights) — stem → B1 → B2 → B3 → B4 (แยก downsample)
- [ ] **Decoder:** U-Net decoder — Up1→Up2→Up3→Up4
- [ ] **Skip connections:** วาดเป็นเส้นประจาก encoder แต่ละ level → decoder (concat)
- [ ] **Output:** 1×1 conv + sigmoid → binary mask 256×256
- [ ] ระบุ: กลั่นจาก SAM3 (teacher), params ~3.6M

### [ ] STEP 4 — วาดภาพที่ 3: ขั้นตอนการตรวจสอบความถูกต้อง (Validation)
- [ ] ระดับพิกเซล (mIoU/Dice/F1) vs วิธีพื้นฐาน (SAM2, YOLO-seg, classical)
- [ ] ระดับภาพ (confusion matrix, acc/prec/sens/spec/F1/MCC/kappa) vs ผู้เชี่ยวชาญ
- [ ] inter-rater (ICC / Cohen's kappa)
- [ ] cross-species

### [ ] STEP 5 — บันทึก + อัปเดต link ในเอกสาร
- [ ] บันทึกเป็น `docs/assets/*.png` (คงชื่อเดิม `flow_overview`, `flow_pipeline`, `flow_validation` หรือตั้งใหม่ชัดเจน)
- [ ] ตรวจว่า `proposal_ysc.md` อ้าง path รูปถูกต้อง (`docs/assets/...`)
- [ ] ตรวจขนาด/คุณภาพรูป (DPI พอ พื้นหลังขาว)

### [ ] STEP 6 — COMMIT + PUSH
- [ ] `git add` ภาพใหม่ + ไฟล์ docs ที่แก้
- [ ] `git commit -m "docs: เพิ่ม flowchart สถาปัตยกรรม U-Net + อัปเดตภาพระเบียบวิธี"`
- [ ] `git push` (ใช้ token) → **เสร็จแล้วค่อยไปทำงานอื่นทีเดียว**

---

## 📌 หมายเหตุ
- **รูปแบบ flow** ยึดโครงจาก `proposal_ysc.md` มาตรา 5 เท่านั้น อย่าใส่รายละเอียดโค้ด/epoch (ข้อเสนอ ≠ รายงาน)
- ใช้ 3 รูปให้ครบตามที่ข้อเสนออ้าง (โปรเจกต์ปัจจุบันมี flowchart 3 ตัว: overview / pipeline / validation → เพิ่ม architecture เป็นตัวแยก)
- ไม่ commit โมเดล/ไฟล์ใหญ่/data/secret ลง repo
