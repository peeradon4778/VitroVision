# Runbook: Distill SAM3 → U-Net student → Hugging Face (VitroVision)

> เป้าหมาย: สร้าง **โมเดล segmentation "ของเราเอง"** (U-Net เล็ก ~2M params) โดยกลั่นจาก **SAM3** (teacher)
> แล้วอัปโหลดขึ้น **Hugging Face** — เป็น artifact ที่ deploy ได้ (ต่อยอดแอป Android) และเป็น "หลักฐานโมเดลเรา"
> ใช้โค้ด: [`src/train_unet_distill.py`](../src/train_unet_distill.py) (4 เฟส) · รันบน **Colab GPU (T4+)**

---

## ⚠️ อ่านก่อน (ความซื่อตรง — สำคัญมากสำหรับกรรมการ)

- โมเดลนี้ฝึกจาก **pseudo-label ของ SAM3** (teacher) — **ยังไม่ใช่ human ground-truth masks**
- ดังนั้นตัวเลข mIoU/Dice ที่ได้ในเฟส eval คือ **เทียบ pseudo-GT ของ SAM3 ไม่ใช่เทียบมนุษย์**
- ถ้าอยากให้โมเดล "แม่นจริง" ต้อง annotate mask มือก่อน (ดู `VALIDATION_PLAN.md` Level A) แล้ว `--gt` ในเฟส eval
- ชุดข้อมูลปัจจุบัน **1 ชนิด × 100 ภาพ** → โมเดลนี้เป็น **prototype** ไม่ใช่ production
- ต้องทำแบบนี้เพราะ: SAM3 = ของ Meta (gated) โมเดลกลั่นนี้ **เป็นของเรา** และอัปโหลด HF ได้แบบชอบธรรม

---

## 📦 1. เตรียมบน Colab

```bash
# ติดตั้ง (ถ้ายังไม่มี)
pip install torch torchvision transformers>=4.50 accelerate huggingface_hub \
    opencv-python-headless pillow numpy pandas matplotlib seaborn tabulate openpyxl

# login HF (gated SAM3 + push โมเดล)
from huggingface_hub import login
login()   # paste HF token (ต้องมีสิทธิ์อ่าน facebook/sam3 + สิทธิ์เขียน repo ใหม่)

# อัปโหลด repo โปรเจกต์ (มี src/) หรือ clone
!git clone https://github.com/peeradon4778/VitroVision.git
%cd VitroVision
```

วางภาพลง `/content/data/20260814_batch/` (หรืออัปโหลดจาก repo `data/raw/20260814_batch`)

## 🎯 2. เฟส 1 — สร้าง pseudo-GT จาก SAM3 (teacher)

```bash
python src/train_unet_distill.py generate-pseudo \
  --data data/raw/20260814_batch \
  --out distill --hf-token <TOKEN> --limit 100
```
- สร้าง `distill/pseudo_masks/<image>.png` (ขาว=ต้น, ชุด plant+leaf union)
- ⏱️ 100 ภาพบน T4 → ~10-20 นาที

## 🎯 3. เฟส 2 — เทรน U-Net student

```bash
python src/train_unet_distill.py train \
  --data data/raw/20260814_batch \
  --pseudo distill/pseudo_masks --out distill \
  --epochs 40 --img-size 256 --batch 8 --lr 1e-3
```
- สร้าง `distill/unet_model.pt` (save ที่ val_dice สูงสุด)
- ⏱️ 40 epochs × 100 ภาพ บน T4 → ~10-20 นาที
- ถ้ามี cross-species (โฟลเดอร์ย่อยต่อชนิด) ให้ `--data data/raw/cross_species` + `--species-holdout <ชนิด>` เพื่อทดสอบ **zero-shot species** (train ไม่เห็นชนิดนั้น)

## 🎯 4. เฟส 3 — ประเมิน student

```bash
# เทียบ pseudo-GT (SAM3) — เป็นตัวเลข baseline ของความใกล้เคียง teacher
python src/train_unet_distill.py eval \
  --data data/raw/20260814_batch --pseudo distill/pseudo_masks \
  --model distill/unet_model.pt --out distill --img-size 256
```
- สร้าง `distill/unet_eval.csv` (iou/dice/precision/recall + runtime/ภาพ)

```bash
# ✅ (เมื่อ annotate mask มือแล้ว) เทียบ GT จริง — ตัวเลขที่น่าเชื่อถือ
python src/train_unet_distill.py eval \
  --data data/raw/20260814_batch --gt ground_truth_masks \
  --model distill/unet_model.pt --out distill --img-size 256
```

## 🚀 5. เฟส 4 — อัปโหลดขึ้น Hugging Face

```bash
python src/train_unet_distill.py hf-push \
  --model distill/unet_model.pt \
  --repo peeradon4778/vitrovision-unet-small \
  --token <TOKEN> --out distill --img-size 256 \
  --eval-csv distill/unet_eval.csv
```
- สร้าง/อัปเดต repo `https://huggingface.co/<repo>` ประกอบด้วย:
  `pytorch_model.bin` + `config.json` + `README.md` (model card bilingual พร้อมประเด็นซื่อตรง)
- หลังนี้ ใครก็โหลดได้: `UNetSmall().load_state_dict(torch.load('pytorch_model.bin'))`

---

## 🔁 ลำดับฝังใน Colab (copy-paste ทั้งบล็อก)

```python
# 2) pseudo
!python src/train_unet_distill.py generate-pseudo --data data/raw/20260814_batch --out distill --hf-token $HF_TOKEN --limit 100
# 3) train
!python src/train_unet_distill.py train --data data/raw/20260814_batch --pseudo distill/pseudo_masks --out distill --epochs 40 --img-size 256 --batch 8 --lr 1e-3
# 4) eval (pseudo)
!python src/train_unet_distill.py eval --data data/raw/20260814_batch --pseudo distill/pseudo_masks --model distill/unet_model.pt --out distill --img-size 256
# 5) push HF
!python src/train_unet_distill.py hf-push --model distill/unet_model.pt --repo peeradon4778/vitrovision-unet-small --token $HF_TOKEN --out distill --img-size 256 --eval-csv distill/unet_eval.csv
```

## 🧭 สิ่งที่ได้ / ขั้นต่อไป

- ✅ **โมเดลของเราเอง** (~2M params, CPU-run ได้) บน HF — ใช้ต่อกับ Android / จัดแสดง
- ⏳ **ที่ต้องปรับปรุงก่อนเชื่อถือเต็ม:** (1) annotate mask มือ → eval กับ GT จริง (2) cross-species (เพิ่มชนิด) (3) calibrate หน่วย (มีความสูง cm แล้ว)
- 🔗 ลิงก์งานใกล้เคียงที่ใช้วิธีเดียวกัน: Orvati Nia et al. (2026) · ครู: `facebook/sam3` (gated)

## ⚠️ ข้อควรระวัง

- SAM3 ต้อง GPU + token ที่เข้าถึง `facebook/sam3` (gated)
- อย่าอ้างว่าโมเดลนี้ "segment แม่นกว่ามนุษย์" — จริง ๆ ฝึกจาก pseudo-label ของ SAM3 เอง
- `data/processed/*` และ `models/*` อยู่ใน `.gitignore` — โมเดล/ผลลัพธ์ไม่ push เข้า repo (เก็บบน HF แทน)
