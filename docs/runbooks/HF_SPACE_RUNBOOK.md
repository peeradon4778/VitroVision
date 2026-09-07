# 🚀 VitroVision — Runbook: โมเดล + HF Space (ให้ได้เดโม่โชว์)

> สรุป **สิ่งที่ต้องรัน** ครบ ทั้ง Colab + HF เพื่อให้มี **โมเดลใช้งานได้** + **เว็บเดโม่สแกนกล้องบน HuggingFace**
> งานเบื้องหลัง (ไฟล์/โค้ด/ข้อเสนอ) ผมทำแล้ว → เหลือแค่ step ที่ต้องใช้บัญชี HF/GPU + token ของคุณ

---

## ✅ สิ่งที่ผมทำเบื้องหลังแล้ว (ไม่ต้องทำซ้ำ)

- สร้าง + แก้โค้ด/ไฟล์ทั้งหมด: `space/app.py` (webcam scan, UI อังกฤษ, fallback) · `requirements.txt` · `README.md`
- แก้บั๊ก `train_unet_distill.py` (dict/ชื่อไฟล์) · `annotation_tool.py` (save/utf8/stroke)
- สร้าง `colab_distill_unet.ipynb` (4 เฟส) · `colab_seed_annotate_30.ipynb`
- Rebuild ข้อเสนอ DOCX (3 ตัว) + อัปเดตชื่อ "การเจริญเติบโต"
- ไฟล์ทั้งหมดอยู่ใน `OneDrive\Desktop\VitroVision_colab\`

---

## 🟦 STEP A — รัน Colab เทรนโมเดล (ต้อง GPU + WRITE token)

**เตรียมบน Google Drive** ให้ได้ `MyDrive/VitroVision_colab/`:
- `batch_images/` — ภาพชุด 100 ขวด (`001.jpg`...`100.jpg`)
- `sam3_growth_pipeline.py`, `train_unet_distill.py`

**Colab:**
1. Runtime → **GPU (T4)**
2. Cell token → วาง **WRITE** token (`hf_...`)
3. รันทุก cell ตามลำดับ → 4 เฟส:

```
1) generate-pseudo  (SAM3 → pseudo masks)
2) train            (U-Net ~2M)
3) eval             (mIoU/Dice)
4) hf-push          → https://huggingface.co/peeradon4778/vitrovision-unet-small
```

**เช็ค:** ทุกเฟส `returncode: 0` · โหลดไฟล์ `unet_model.pt` + `unet_eval.csv`

---

## 🟦 STEP B — ตั้ง HF Space (SDK = Gradio)

> ⚠️ **สำคัญ:** ถ้า Space ขึ้นเป็น **Trackio** = ตั้ง SDK ผิด ให้แก้เป็น **Gradio** แล้วอัปไฟล์ใหม่

1. HF → `+` → **New Space**: ชื่อ `vitrovision-space` · **SDK = Gradio** · License MIT · **CPU basic** (ฟรี)
2. **Files** → Upload → ลาก **3 ไฟล์** จาก `OneDrive\Desktop\VitroVision_colab\space\`:
   - `app.py` · `requirements.txt` · `README.md`
3. Build ~1 นาที → **เปิด Space** → กด 📷 ใช้กล้องสแกนได้เลย (โหมด demo = classical-green)

**หลัง push โมเดล (STEP A เสร็จ):** Space โหลด `vitrovision-unet-small` ให้อัตโนมัติ → ใช้ **โมเดลจริง** (ไม่มี fallback)

---

## 🟩 STEP C — (optional) Level A / annotate — **พักไว้ก่อน**

`colab_seed_annotate_30.ipynb` → seed SAM3 30 ภาพ → `annotation_tool.py` ป้ายมือ → `mask_metrics.py`
_(ไม่บังคับก่อนส่งข้อเสนอ — ระบุเป็นแผน [PLAN] ได้อย่างซื่อตรง)_

---

## 🟪 STEP D — ข้อเสนอ (deadline 10 ก.ย.)

- ✅ ผม rebuild DOCX แล้ว (`proposal_th_draft.docx` / `report_th_v1.docx` / `ysc_proposal_filled.docx`)
- ⬜ คุณเติม **ส่วน 14** (ประวัติผู้พัฒนา + อาจารย์ที่ปรึกษา) — ข้อมูลจริงของคุณ
- ⬜ **Form 6** (Research Continuation) + **Form 3** (Risk) + CoC/PDPA
- ⬜ **หน้าปก SIMS + รหัสโครงการ** (สร้างจากระบบเท่านั้น) → ประกอบ PDF

---

## 🔐 หมายเหตุความปลอดภัย
- อย่าแชร์ **write_token** (ถ้าปรากฏใน log ให้ถือว่าเสี่ยง → **สร้าง token ใหม่** แล้ววางใหม่)
- โมเดลกลั่นจาก **facebook/sam3 (gated)** → model card ระบุที่มาไว้แล้ว

> กลับมาดูcommit/ผลลัพธ์ได้เลย — ทุกไฟล์ใน `OneDrive\Desktop\VitroVision_colab\` + repo (branch master)
