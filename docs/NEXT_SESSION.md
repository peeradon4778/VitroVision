# 📌 NEXT SESSION — งานต่อจากจุดพัก (2026-09-01)

> สถานะ ณ จุดพัก + สิ่งที่ต้องทำต่อครั้งหน้า เปิดไฟล์นี้ก่อนทำงานต่อเสมอ

## 🧪 1. โมเดล (อีกจอรันอยู่ — ใกล้เสร็จ)

- **สถานะ:** เทรน U-Net (MobileNetV3-Small, smp) บน greenhouse dataset 1200 ภาพ → **epoch 3/5, val_dice 0.9728** (save best แล้ว)
- ไฟล์: `data/work/greenhouse_ds/best_model.pt` (14.5MB) · `ckpt.pt` (resume) · log: `data/work/pretrain.log`
- **ต่อครั้งหน้า:**
  - [ ] ให้อีกจอเทรนจนครบ (หรือรัน `src/train_greenhouse.py` resume ต่อ)
  - [ ] เทสต์บน 100 ภาพขวด → `test_100.csv` + `pred_100/` + ค่า acc/sens
  - [ ] เอา `final_model.pt` ไปอัป `space/app.py` (อีกจอแก้ space ไว้แล้ว — ตรวจให้ตรงสถาปัตยกรรม)
  - [ ] push โมเดลขึ้น HF `vitrovision-unet-small` (ต้อง WRITE token — ขั้นผู้ใช้)

## 🌐 2. HF Space (ยังไม่เสร็จ)

- [ ] Space **`vitrovision`** บน HF ยังเป็น **Trackio ผิด** → แก้ SDK เป็น **Gradio** + อัป 3 ไฟล์ (`space/app.py` ล่าสุด, `requirements.txt`, `README.md`)
- [ ] หลัง push โมเดล → Space โหลดโมเดลจริงอัตโนมัติ (fallback classical-green ระหว่างรอ)

## 📝 3. ข้อเสนอ YSC (deadline 10 ก.ย. — เหลือ ~9 วัน)

- **สถานะ:** clone ไฟล์รุ่นพี่ (`docs/VitroVision_Proposal_YSC.docx` → Desktop `VitroVision_ข้อเสนอ_YSC_clone.docx`) เนื้อหา VitroVision + flowchart 3 รูป + ชิดซ้าย + เลขหน้ากลาง — **รอคุณเปิด Word ตรวจ**
- ไฟล์ build: `docs/build_clone.py` (แก้+รันใหม่ได้), flowchart: `docs/_make_flowcharts.py`, header/footer: `docs/_copy_hf.py` + `docs/_fix_footer.py`
- **ต่อครั้งหน้า:**
  - [ ] คุณตรวจ docx (จัดวาง/เนื้อหา/รูป) → บอกจุดแก้ → ผมปรับ `build_clone.py` แล้ว rebuild
  - [ ] เติมส่วน 14 (ประวัติผู้พัฒนา + อาจารย์ที่ปรึกษา — ข้อมูลจริงของคุณ)
  - [ ] Form 6 (Research Continuation) + Form 3 (Risk) + CoC/PDPA (ผมร่างให้ได้)
  - [ ] หน้าปก SIMS + รหัสโครงการ (มีแล้ว: `29YCSE00054T`) → ประกอบ PDF ไฟล์เดียว 3 ส่วน
  - [ ] อัปโหลดก่อน 10 ก.ย.

## 🌱 4. Level A (annotate) — พักไว้ (ไม่บังคับ)

- seed masks พร้อมแล้วที่ `data/work/annotate/seed/pseudo_masks/` (30 ไฟล์)
- ทำเมื่อมีเวลา: เปิด `annotation_tool.py` → ป้าย 30 mask → `mask_metrics.py` → mIoU

## 🔧 5. สภาพ Git (สำคัญ)

- commit ทั้งหมดอยู่ **local เท่านั้น ยังไม่ push GitHub** (กฎ: ต้องสั่งก่อน push)
- ไฟล์ที่อีกจอแก้: `space/` + `src/train_greenhouse.py` + `src/train_vitrovision_model.py` (commit จุดพักแล้ว)
- รหัสโครงการ: `29YCSE00054T` · ลิงก์ติดตาม: nstda.or.th/sims

## ✅ Commit ล่าสุด (จุดพัก)

`dea52bb` clone v2 · `38800fc` clone v1 · `3fe338a` เขียนใหม่ตาม ref · `b1e9fac/5af7b9d` train_greenhouse · บั๊ก annotation/seed ก่อนหน้า
