# 🏷️ Workflow: annotate ground-truth mask มือ → Level A mIoU (VitroVision)

> หน้าเดียวจบ — เปิดทำตามทีละขั้นตอน ถ้าทำครบจะได้ **Level A mIoU/Dice เทียบมนุษย์** (เกตสำคัญของ "โมเดลเรา")
> เป้าหมาย: annotate binary mask (ขาว=ต้น) บน **30 ภาพ** คัดแล้ว ครอบคลุม 3 คลาส verdict + สัณฐานหลากหลาย

---

## ✅ ขั้น 0 — (ทำแล้ว) คัด 30 ภาพ stratified
```bash
python src/prepare_annotation.py --gt data/processed/ground_truth.csv \
  --data data/raw/20260814_batch --out data/work/annotate --n 30
```
ผลลัพธ์ (ใน `data/work/annotate/`):
- `annotate_list.csv` — 30 ภาพ (image, expert_verdict, note, bucket, order)
- `images/` — สำเนา 30 ภาพที่คัด (ใช้สำหรับ seed + annotate)
- ผมรันไว้ให้แล้ว → อยู่ใน `data/work/annotate/` แล้ว

## 📤 ขั้น 1 — สร้าง seed จาก SAM3 (ทางเลือก แต่**แนะนำ** — ช่วยประหยัดแรงมาก)
บน **Colab GPU** (ต้อง token ที่เข้าถึง `facebook/sam3`):
```bash
# อัปโหลด data/work/annotate/images ไป Colab (หรือใช้ repo)
python src/train_unet_distill.py generate-pseudo \
  --data data/work/annotate/images --out data/work/annotate/seed \
  --hf-token <TOKEN> --limit 30
# ดาวน์โหลด data/work/annotate/seed/pseudo_masks/ กลับมาใส่เครื่อง
```
→ ได้ `data/work/annotate/seed/pseudo_masks/<ภาพ>.png` (mask คร่าว ๆ จาก SAM3)
> ไม่อยากใช้ seed ก็ข้ามไปขั้น 2 ได้ (annotate จาก 0 ช้ากว่าแต่ก็ได้)

## 🖱️ ขั้น 2 — annotate mask มือ
```bash
# ใช้เครื่องมือผม (Flask + เบราว์เซอร์)
python src/annotation_tool.py --data data/work/annotate/images \
  --seed data/work/annotate/seed/pseudo_masks \
  --out data/processed/ground_truth_masks --port 5000
# เปิด Chrome → http://localhost:5000
```
วิธีป้าย:
- **ขาว/เขียว = ต้น** (ใบ/ลำต้น/หน่อที่เห็นผ่านขวด) · ไม่รวมขวด/พื้นหลัง/glare
- ปุ่ม **เพิ่ม/ลบ** · **ขนาดพู่กัน** · **Undo** · `s`=บันทึก&ถัดไป · `←→`=สลับภาพ
- ภาพหนาแน่น (หลายต้น) → วาดทั้งก้อนที่เห็นว่าเป็นเนื้อเยื่อ
- ทำครบ 30 ภาพ → progress เต็ม

> ⚠️ **Blind:** เครื่องมือไม่โชว์ verdict ของ SAM3 — คุณตัดสินจากภาพล้วน ๆ กัน bias

## 📊 ขั้น 3 — ได้ Level A mIoU/Dice ทันที (ผมทำให้แล้ว)
```bash
python src/mask_metrics.py --pred <sam3_masks> --gt data/processed/ground_truth_masks --size 512
# --pred = <data/work/annotate/seed/pseudo_masks> (SAM3) หรือ <unet_model masks> (student)
```
→ ผล `levelA_summary.csv` (mIoU/Dice/F1/precision/recall) · **ถ้า mIoU ≥ 0.65 ผ่าน H₁**

## 👥 ขั้น 4 — inter-rater (optional แต่แนะนำ — ตอบ observer bias)
```bash
python src/interrater.py --csv ground_truth.csv --cols rA_verdict,rB_verdict --type categorical
python src/interrater.py --csv ground_truth.csv --cols rA_height,rB_height --type continuous
```

---

## 📦 หลักฐานที่ต้องเก็บ (ใส่ repo — ตามกฎ "evidence ใน repo")
- `data/processed/ground_truth_masks/*.png` (30 mask) → พิจารณา commit (หรือรายงานตัวเลข mIoU ลง report)
- `annotate_list.csv` (manifest 30 ภาพ) → เก็บเป็นหลักฐาน
- ตัวเลข mIoU/Dice → เขียน `docs/report_th_v1.md` §4.4 / `DEV_LOG`

## ⚠️ หมายเหตุความซื่อตรง
- ถ้า annotate **มี seed** → mask เป็นแบบ "แก้จาก SAM3" ถือเป็น human GT ได้ แต่ควร **inter-rater/คนละรอบ** กัน bias
- เปรียบเทียบ mIoU ให้ resize ทั้งคู่เป็น resolution เดียวกัน (คำสั่ง `--size`)
