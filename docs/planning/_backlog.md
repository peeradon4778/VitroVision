# 📥 VitroVision — Backlog & สถานะปัจจุบัน (living doc)

> อัปเดต 2026-09-01 · เขียนใหม่ให้ตรงสถานะจริง
> สถานะ: ▶️ กำลังทำ · 🟡 รอ · ✅ เสร็จ · 💤 รอเคาะ
> ที่มาของสถานะ: `docs/DEV_LOG.md` + runbooks

---

## 🧭 สถานะภาพรวม (ณ 2026-09-01)

- **โมเดลหลัก:** U-Net + MobileNetV3-Small (กลั่นจาก SAM3) — เทรนเสร็จ · val_dice ≈ 0.98 · เกณฑ์ `height_proxy ≥ 0.20` → acc 0.653 / sens 0.717 / spec 0.579
- **Pilot (SAM3):** zero-shot ผ่านชุด 100 ขวดพริกจินดา · height r = 0.638 · เกณฑ์ `0.275` → acc 0.755 / sens 0.917
- **ชุดข้อมูล:** 100 ขวด (`data/raw/20260814_batch`) + `ground_truth.csv` (60 พร้อม / 38 ยังไม่พร้อม / 2 ตรวจเอง) + ชุด greenhouse สำหรับเทรน U-Net
- **Deploy:** HF Space (Gradio) — ยังต้องปรับให้เสร็จ + push โมเดล

### ✅ เสร็จแล้ว
- [x] ตั้งชื่อโครงงาน TH/EN + เคาะ RQ/เป้าหมาย
- [x] Spike test SAM3 text-prompted (พิสูจน์มองทะลุขวด/glare)
- [x] เทรน U-Net กลั่น (val_dice 0.98) + benchmark เทียบ baseline (classical/YOLO/SAM)
- [x] สร้างชุด 100 ขวด + ground_truth + calibration บางส่วน
- [x] สร้างเครื่องมือ validate (mask_metrics, interrater) + ร่างข้อเสนอ/รายงาน
- [x] จัดระเบียบ repo (docs/deliverables|runbooks|scripts, research ลดเหลือ 2 ไฟล์)

### ▶️ กำลังทำ / 🟡 รอ (งานค้างหลัก — ลำดับความสำคัญ)

**🔴 งานส่ง YSC (deadline 10 ก.ย. 2026):**
- [ ] Rebuild docx จาก md ใหม่ (ชื่อ/เนื้อหาใหม่) — `proposal_th_submit`, `report_th_v1`, `ysc_proposal_filled`
- [ ] เติมส่วน 14 (ประวัติผู้พัฒนา + อาจารย์ที่ปรึกษา)
- [ ] แบบฟอร์ม: Form 6 (Research Continuation) · Form 3 (Risk) · CoC/PDPA
- [ ] หน้าปก + รหัสจาก SIMS (`29YCSE00054T`) → ประกอบ PDF ไฟล์เดียว

**🟡 โมเดล/Deploy:**
- [ ] อัปเดต HF Space เป็น Gradio + อัปโมเดล `vitrovision-unet-small` (ต้อง WRITE token)
- [ ] เทรนต่อ/ทดสอบ 100 ขวดบนโมเดลจริง (test_100.csv)

**🟡 Validation:**
- [ ] Level A: annotate ground-truth masks ≥ 30 ภาพ → มัioU/Dice (`mask_metrics.py`)
- [ ] Inter-rater (ICC/Cohen's kappa) ด้วยผู้ประเมินหลายคน
- [ ] การสอบเทียบหน่วยจริง (px→cm) — ทำได้บางส่วน
- [ ] ทดสอบข้ามชนิดพืช (cross-species)

## 💤 รอเคาะ
- [ ] เกณฑ์ความพร้อมต่อชนิด (ต้องยืนยันกับคนแล็บจริง)
- [ ] การใช้ข้อมูล 3 มิติ (จำกัดจากภาพ 2D ผ่านขวด)

---

## 📎 อ้างอิง
- สถาปัตยกรรม/โมเดล: `docs/planning/_orchestration.md`
- ขอบเขต: `docs/planning/_scope_lock_new_round.md`
- การตัดสินใจสำคัญ: `docs/planning/_grill_v3.md`
- เครื่องมือทดสอบ/ผล: `docs/planning/_tool_matrix.md`
- ประวัติการทำจริง: `docs/DEV_LOG.md`
