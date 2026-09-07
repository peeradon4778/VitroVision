# 🔖 Ticket: สร้างภาพประกอบ 6 ภาพ (ภาพเยอะแทน text)

> สร้าง 2026-09 · ใช้คู่ `docs/proposal_ysc.md` + `docs/FIGS_MASTER_PLAN.md`
> เครื่องมือวาด: **Draw.io** (user) · แก้ไข script + commit/push (pi)
> เป้าหมาย: งาน Tech → **ภาพเยอะ** ลด text · **ทำครบ 6 ภาพ → อัปเดต link → commit + push → ค่อยไปงานถัด**

---

## 🖼 STEP 1 — วาดภาพทั้ง 6 (ตาม FIGS_MASTER_PLAN.md)

### [ ] F1 `fig_system_overview.png` — ภาพรวมระบบ (มาตรา 5.1)
- ถ่ายภาพขวด → ROI → Segment (U-Net) → feature 6 กลุ่ม → verdict
- แทรก error path: ภาพไม่ชัด (glare/ฝ้า) → ส่งมนุษย์ตรวจ

### [ ] F2 `fig_unet_architecture.png` — สถาปัตยกรรม U-Net (มาตรา 5.3) ← ใหม่
- Encoder: MobileNetV3-Small (ImageNet weights) [B1–B4]
- Decoder: U-Net [Up1–Up4]
- **Skip connections (เส้นประ)** จาก encoder แต่ละ level → decoder
- Output: 1×1 conv + sigmoid → binary mask 256×256
- ระบุ: ~3.6M params · val_dice ≈ 0.98 · กลั่นจาก SAM3

### [ ] F3 `fig_data_pipeline.png` — ข้อมูล & การฝึก (มาตรา 5.2–5.3) ← ใหม่
- greenhouse 1,200 → split 85/15 → train/aug + val
- SAM3 teacher → pseudo-labels → ฝึก U-Net
- test ขวดจริง 98 ภาพ (unseen)

### [ ] F4 `fig_validation_levels.png` — ระดับการตรวจสอบ (มาตรา 5.5)
- pixel (mIoU/Dice/F1/P/R) · ค่าวัด (r/MAE/RMSE) · verdict (acc/sens/spec/MCC/kappa) · inter-rater (ICC/kappa)

### [ ] F5 `fig_verdict_threshold.png` — เกณฑ์ verdict (มาตรา 6) ← ใหม่
- สแกน 0.12–0.55 → Youden = 0.20 → acc 0.653/sens 0.717/spec 0.579
- multi-trait AUC 0.639 (ไม่ดีกว่า single → หนุน 3D)

### [ ] F6 `fig_results.png` — ผล (มาตรา 6)
- bar: mIoU/Dice เทียบวิธีพื้นฐาน · scatter: height vs expert · error/box

---

## 🖥 STEP 2 — บันทึก + อัปเดต link
- [ ] บันทึกเป็น `docs/assets/*.png` (ใช้ชื่อตาม FIGS_MASTER_PLAN)
- [ ] ตรวจ `proposal_ysc.md` อ้าง path ถูกต้องทุกภาพ (`docs/assets/...`)
- [ ] ตรวจขนาด/DPI/พื้นหลังขาว · label อังกฤษ

## 📤 STEP 3 — COMMIT + PUSH
- [ ] `git add` ภาพ 6 ไฟล์ + `proposal_ysc.md` + `.md` ที่แก้
- [ ] `git commit -m "docs: เพิ่ม flowchart 6 ภาพ + อัปเดตข้อเสนอ (ภาพเยอะแทน text)"`
- [ ] `git push` (ใช้ token) → **เสร็จแล้วค่อยไปงานถัดไปทีเดียว**

---

## 📌 หมายเหตุ
- ยึดโครง `proposal_ysc.md` มาตรา 5–6 เท่านั้น อย่าใส่รายละเอียดโค้ด/epoch (ข้อเสนอ ≠ รายงาน)
- 1 ภาพ = 1 message · ภาพก่อน text · ใช้ตารางแทนย่อหน้า
- ไม่ commit โมเดล/ไฟล์ใหญ่/data/secret
