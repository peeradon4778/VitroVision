"""Distillation: SAM3 (teacher) → U-Net เล็ก (student) สำหรับ plant segmentation ในขวด TC

3 เฟส:
  1) generate-pseudo : รัน SAM3 PCS บนภาพ → save pseudo-GT masks (plant union) → <out>/pseudo_masks/
  2) train            : เทรน U-Net (student) จาก pseudo masks (train/val split + augment + BCE+Dice)
  3) eval             : ประเมิน student (mIoU/Dice/F1 + runtime) บน val

รันบน Colab (GPU) — เฟส 1 ต้อง SAM3:
  python train_unet_distill.py generate-pseudo --data <ภาพ> --out <out> --hf-token <TOKEN> [--limit 100]
  python train_unet_distill.py train --data <ภาพ> --pseudo <out>/pseudo_masks --out <out> [--epochs 40] [--img-size 256]
  python train_unet_distill.py eval --data <ภาพ> --pseudo <out>/pseudo_masks --model <out>/unet_model.pt --out <out>

หลังมี GT จริง (annotate 30 ขวด) → validate student กับ GT จริง (--gt) เพื่อรายงานตัวเลขจริง
"""

import argparse
import glob
import os
import sys
import time

# ทำให้ import โมดูลพี่น้องใน src/ ทำงานได้ทั้งรันจาก root หรือ src/ ตรง ๆ
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset


# ═══════════════════════ U-Net เล็ก (student) ═══════════════════════

class DoubleConv(nn.Module):
    def __init__(self, cin, cout):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(cin, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True),
            nn.Conv2d(cout, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True))

    def forward(self, x):
        return self.block(x)


class UNetSmall(nn.Module):
    """U-Net ขนาดเล็ก: channels [16,32,64,128,256] ~2M params — รัน CPU ได้หลังเทรน"""

    def __init__(self, in_ch=3, out_ch=1, base=16):
        super().__init__()
        c = [base * (2 ** i) for i in range(5)]  # [16,32,64,128,256]
        self.enc = nn.ModuleList([DoubleConv(in_ch, c[0])] +
                                 [DoubleConv(c[i], c[i + 1]) for i in range(4)])
        self.pool = nn.MaxPool2d(2)
        self.up = nn.ModuleList([
            nn.ConvTranspose2d(c[i + 1], c[i], 2, stride=2) for i in range(4)])
        self.dec = nn.ModuleList([DoubleConv(c[i] * 2, c[i]) for i in range(4)])
        self.head = nn.Conv2d(c[0], out_ch, 1)

    def forward(self, x):
        skips = []
        for i, block in enumerate(self.enc):
            x = block(x)
            if i < 4:
                skips.append(x)
                x = self.pool(x)
        for i in range(4):
            x = self.up[3 - i](x)
            x = torch.cat([x, skips[3 - i]], dim=1)
            x = self.dec[3 - i](x)
        return torch.sigmoid(self.head(x))


# ═══════════════════════ Dataset ═══════════════════════

class SegDataset(Dataset):
    def __init__(self, image_paths, mask_dir, img_size=256, augment=False):
        self.items = []
        self.img_size = img_size
        self.augment = augment
        for ip in image_paths:
            name = os.path.splitext(os.path.basename(ip))[0]
            mp = os.path.join(mask_dir, name + ".png")
            if os.path.exists(mp):
                self.items.append((ip, mp))

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        ip, mp = self.items[i]
        img = cv2.imread(ip)
        img = cv2.resize(img, (self.img_size, self.img_size), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        mask = cv2.imread(mp, cv2.IMREAD_GRAYSCALE)
        mask = cv2.resize(mask, (self.img_size, self.img_size), interpolation=cv2.INTER_NEAREST)
        mask = (mask > 127).astype(np.float32)
        if self.augment:
            img, mask = self._augment(img, mask)
        return (torch.from_numpy(img.transpose(2, 0, 1)).float(),
                torch.from_numpy(mask).unsqueeze(0).float())

    def _augment(self, img, mask):
        """Augmentation เชิงบริบทขวดแก้ว — เลียนแบบ domain shift ที่เจอใน lab จริง
        (glare/ฝ้า/ไอน้ำ/แสง/มุม) เพื่อให้ model generalize ข้ามชนิดและข้ามสภาพ.
        กลับกันทั้ง 3 ค่า: ใช้ค่าเดิมกับ img, mask เสมอ เพื่อไม่ให้ mask เพี้ยน."""
        # 1) พลิก (spatial)
        if np.random.rand() > 0.5:
            img, mask = cv2.flip(img, 1), cv2.flip(mask, 1)
        if np.random.rand() > 0.5:
            img, mask = cv2.flip(img, 0), cv2.flip(mask, 0)
        # 2) หมุนเล็กน้อย (จำลองมุมถ่าย) — ใช้ rotate 0..10 องศา รอบมุมหลังที่เติม
        if np.random.rand() > 0.5:
            ang = float(np.random.uniform(-10, 10))
            h, w = img.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
            img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            mask = cv2.warpAffine(mask, M, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
        # 3) ความสว่าง/คอนทราสต์ (glare/ฝ้า/แสง) — ใช้ scipy.ndenumerate ไม่งั้น ใช้ numpy ตรง ๆ
        if np.random.rand() > 0.4:
            img = img * float(np.random.uniform(0.85, 1.15))
        img = np.clip(img, 0.0, 1.0)
        if np.random.rand() > 0.5:
            mean = float(img.mean())
            img = (img - mean) * float(np.random.uniform(0.9, 1.1)) + mean
            img = np.clip(img, 0.0, 1.0)
        # 4) จุดขาว (specular glare) จำลองแสงสะท้อนบนขวด — ใส่เฉพาะ img ไม่แตะ mask
        if np.random.rand() > 0.6:
            h, w = img.shape[:2]
            cx, cy = np.random.randint(0, w), np.random.randint(0, h)
            r = int(np.random.uniform(0.02, 0.06) * max(h, w))
            yy, xx = np.ogrid[:h, :w]
            disk = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
            img[disk] = 1.0
        # 5) ไอน้ำ/เบลอเล็กน้อย — ผสมภาพเบลอ
        if np.random.rand() > 0.6:
            k = (np.random.choice([3, 5]), np.random.choice([3, 5]))
            img = cv2.GaussianBlur(img, (int(k[0]) if int(k[0]) % 2 == 1 else 3,
                                         int(k[1]) if int(k[1]) % 2 == 1 else 3), 0)
            img = np.clip(img, 0.0, 1.0)
        return img, mask


def dice_loss(pred, target, eps=1e-6):
    inter = (pred * target).sum()
    return 1 - (2 * inter + eps) / (pred.sum() + target.sum() + eps)


# ═══════════════════════ เฟส 1: สร้าง pseudo-GT จาก SAM3 ═══════════════════════

def cmd_generate_pseudo(args):
    if args.hf_token:
        from huggingface_hub import login
        login(token=args.hf_token, add_to_git_credential=False)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] device: {device}")
    if device == "cpu":
        raise SystemExit("SAM3 ไม่รองรับ CPU — ต้อง Colab GPU")

    from sam3_growth_pipeline import PROMPTS, load_images, segment_prompt  # reuse (อยู่ใน src/ เดียวกัน)
    from PIL import Image

    os.makedirs(args.out, exist_ok=True)
    mask_dir = os.path.join(args.out, "pseudo_masks")
    os.makedirs(mask_dir, exist_ok=True)

    from transformers import Sam3Processor, Sam3Model
    print("[INFO] โหลด SAM3 (teacher) ...")
    model = Sam3Model.from_pretrained("facebook/sam3").to(device)
    processor = Sam3Processor.from_pretrained("facebook/sam3")

    imgs = load_images(args.data)  # dict {name: PIL.Image}
    items = list(imgs.items())
    if args.limit:
        items = items[:args.limit]
    print(f"[INFO] สร้าง pseudo masks {len(items)} ภาพ (prompt plant+leaf union)")

    plant_prompts = [p for p in PROMPTS if p in ("plant", "leaf")]
    for i, (name, pil) in enumerate(items, 1):
        pil = pil.convert("RGB")
        union = np.zeros((pil.size[1], pil.size[0]), dtype=bool)
        for p in plant_prompts:
            masks, _ = segment_prompt(model, processor, device, pil, p)
            if masks is not None and len(masks) > 0:
                union |= masks.any(axis=0)
        cv2.imwrite(os.path.join(mask_dir, name + ".png"),
                    (union * 255).astype(np.uint8))
        if i % 20 == 0:
            print(f"  ... {i}/{len(items)}")
    print(f"[OK] pseudo masks → {mask_dir}")


# ═══════════════════════ cross-species split helper ═══════════════════════

def _detect_species(data_dir):
    """หาโฟลเดอร์ย่อยต่อชนิด (data/<species>/*.jpg). ถ้ามี >=2 โฟลเดอร์ย่อยที่มีภาพ => หลายชนิด.
    คืน list ชื่อโฟลเดอร์ย่อย (species). ถ้าไม่พบ (ภาพล้วน ๆ ใน data_dir เดียว) คืน []
    """
    subs = []
    if os.path.isdir(data_dir):
        for name in sorted(os.listdir(data_dir)):
            p = os.path.join(data_dir, name)
            if os.path.isdir(p):
                imgs = glob.glob(os.path.join(p, "*.jpg")) + \
                       glob.glob(os.path.join(p, "*.JPG")) + \
                       glob.glob(os.path.join(p, "*.png"))
                if imgs:
                    subs.append(name)
    return subs


def _split_by_species(image_paths, holdout_species, data_dir):
    """แยก train/val ตามชนิด (โฟลเดอร์ย่อย).
    - ถ้า holdout_species ระบุ: ทุกภาพในชนิดนั้น -> val (test species ไม่เคยเห็น), ที่เหลือ -> train
    - ถ้าไม่ระบุ: เลือกชนิดที่มีภาพมากสุดเป็น holdout อัตโนมัติ, ที่เหลือ -> train
    คืน (train_paths, val_paths)
    """
    species = _detect_species(data_dir)
    if not species:
        raise SystemExit("cross-species ต้องการ --data ที่มีโฟลเดอร์ย่อยต่อชนิด")
    # map ภาพ -> species
    def sp_of(p):
        rel = os.path.relpath(p, data_dir)
        first = rel.split(os.sep)[0]
        return first if first in species else None
    by_species = {s: [] for s in species}
    for p in image_paths:
        s = sp_of(p)
        if s is not None:
            by_species[s].append(p)
    # เลือก holdout
    if holdout_species:
        if holdout_species not in by_species:
            raise SystemExit(f"holdout species '{holdout_species}' ไม่พบใน {data_dir}")
        hold = holdout_species
    else:
        hold = max(by_species, key=lambda s: len(by_species[s]))
    train_paths = [p for s, ps in by_species.items() if s != hold for p in ps]
    val_paths = by_species[hold]
    return train_paths, val_paths


# ═══════════════════════ เฟส 2: เทรน U-Net ═══════════════════════

def cmd_train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] device: {device}")

    image_paths = sorted(glob.glob(os.path.join(args.data, "*.jpg")) +
                         glob.glob(os.path.join(args.data, "*.JPG")) +
                         glob.glob(os.path.join(args.data, "*.png")))
    image_paths = sorted(set(image_paths))
    n = len(image_paths)
    if n == 0:
        raise SystemExit(f"ไม่พบภาพใน {args.data}")

    # ── cross-species split ──
    # ถ้า --data มีโฟลเดอร์ย่อยต่อชนิด (data/<species>/*.jpg) ให้แยก train/val โดย
    # ชนิดที่ train **ไม่เคยเห็น** (= zero-shot species) ออกไปเป็น val/test กลุ่มใหม่
    species = _detect_species(args.data)
    if len(species) >= 2:
        train_paths, val_paths = _split_by_species(image_paths, args.species_holdout, args.data)
        print(f"[INFO] cross-species: species={species} | holdout={args.species_holdout}"
              f" | train {len(train_paths)} · val {len(val_paths)}")
    else:
        split = int(n * 0.85)
        train_paths, val_paths = image_paths[:split], image_paths[split:]
        print(f"[INFO] single-species: train {len(train_paths)} · val {len(val_paths)}")

    train_ds = SegDataset(train_paths, args.pseudo, args.img_size, augment=True)
    val_ds = SegDataset(val_paths, args.pseudo, args.img_size, augment=False)
    if len(train_ds) == 0 or len(val_ds) == 0:
        raise SystemExit("pseudo masks ไม่ตรงกับภาพ (เช็ค --pseudo)")
    train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=2)

    model = UNetSmall().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    bce = nn.BCELoss()

    os.makedirs(args.out, exist_ok=True)
    best_dice = 0.0
    for epoch in range(1, args.epochs + 1):
        model.train()
        tl = 0.0
        for img, mask in train_loader:
            img, mask = img.to(device), mask.to(device)
            pred = model(img)
            loss = bce(pred, mask) + dice_loss(pred, mask)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tl += loss.item() * len(img)
        # val dice
        model.eval()
        vd, vi = 0.0, 0.0
        with torch.no_grad():
            for img, mask in val_loader:
                img, mask = img.to(device), mask.to(device)
                pred = model(img) > 0.5
                inter = (pred & mask.bool()).sum().item()
                union = (pred | mask.bool()).sum().item()
                dice = 2 * inter / (pred.sum().item() + mask.sum().item() + 1e-6)
                vd += dice * len(img)
                vi += (inter / (union + 1e-6)) * len(img)
        vd /= len(val_ds)
        vi /= len(val_ds)
        print(f"  epoch {epoch}/{args.epochs} · loss {tl / len(train_ds):.4f} · val_dice {vd:.4f} · val_iou {vi:.4f}")
        if vd > best_dice:
            best_dice = vd
            torch.save(model.state_dict(), os.path.join(args.out, "unet_model.pt"))
            print(f"    ✔ บันทึก best model (val_dice {vd:.4f})")


# ═══════════════════════ เฟส 3: ประเมิน student ═══════════════════════

def cmd_eval(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UNetSmall()
    model.load_state_dict(torch.load(args.model, map_location=device))
    model.to(device).eval()

    image_paths = sorted(set(glob.glob(os.path.join(args.data, "*.jpg")) +
                             glob.glob(os.path.join(args.data, "*.JPG")) +
                             glob.glob(os.path.join(args.data, "*.png"))))
    ds = SegDataset(image_paths, args.pseudo or args.gt, args.img_size, augment=False)
    if len(ds) == 0:
        raise SystemExit("ไม่มี mask ให้ประเมิน (--pseudo หรือ --gt)")
    loader = DataLoader(ds, batch_size=1, shuffle=False)

    rows = []
    t_total = 0.0
    with torch.no_grad():
        for img, mask in loader:
            img = img.to(device)
            t0 = time.time()
            pred = model(img) > 0.5
            t_total += time.time() - t0
            p, m = pred[0, 0].cpu().numpy().astype(bool), mask[0, 0].numpy().astype(bool)
            inter = (p & m).sum()
            union = (p | m).sum()
            rows.append({
                "image": ds.items[len(rows)][0],
                "iou": inter / (union + 1e-6),
                "dice": 2 * inter / (p.sum() + m.sum() + 1e-6),
                "precision": inter / (p.sum() + 1e-6),
                "recall": inter / (m.sum() + 1e-6),
            })
    df = pd.DataFrame(rows)
    df["runtime_s"] = t_total / max(len(rows), 1)
    os.makedirs(args.out, exist_ok=True)
    df.to_csv(os.path.join(args.out, "unet_eval.csv"), index=False, encoding="utf-8-sig")
    print(f"[OK] unet_eval.csv ({len(df)} ภาพ) — avg runtime {df['runtime_s'].iloc[0]:.3f}s/ภาพ ({'GPU' if device.type=='cuda' else 'CPU'})")
    print(df[["iou", "dice", "precision", "recall"]].mean().round(4).to_string())


# ═══════════════════════ เฟส 4: upload ขึ้น Hugging Face ═══════════════════════

def count_params(model):
    return sum(p.numel() for p in model.parameters())


def build_model_card(args, n_params, eval_mean=None):
    """สร้าง README.md (model card) สำหรับ HF — bilingual (TH/EN)"""
    n_m = n_params / 1e6
    eval_line = ""
    if eval_mean is not None:
        eval_line = (
            f"\n## Results (vs pseudo-GT from SAM3)\n"
            f"- mIoU / Dice / Precision / Recall: {eval_mean}\n"
        )
    return f"""---
language:
  - th
  - en
license: mit
tags:
  - computer-vision
  - image-segmentation
  - plant-phenotyping
  - tissue-culture
  - distillation
  - pytorch
pipeline_tag: image-segmentation
---

# VitroVision UNet Small (plant segmentation in vitro bottle)

โมเดล segmentation ขนาดเล็ก (~{n_m:.1f}M params) ที่ถูก **กลั่น (distill) จาก SAM3** (teacher, zero-shot PCS)
เพื่อแบ่งส่วนต้นพืชเพาะเลี้ยงเนื้อเยื่อในขวดแก้วแบบ non-destructive สำหรับงาน **VitroVision**

> ⚠️ **โมเดลสังเคราะห์จาก pseudo-label ของ SAM3** (ยังไม่มี human ground-truth masks เต็มชุด)
> ตัวเลข mIoU/Dice ที่ให้คือเทียบ pseudo-GT ของ teacher (SAM3) — **ไม่ใช่เทียบมนุษย์**
> อ้างอิงครู: `facebook/sam3` (gated). งานอ้างอิงที่ใช้วิธีเดียวกัน: Orvati Nia et al. (2026).

## Model

- **Architecture:** U-Net เล็ก (encoder/decoder, channels 16→32→64→128→256)
- **Input:** RGB, resize {args.img_size}x{args.img_size}, normalize 0-1
- **Output:** sigmoid probability mask (plant=1)
- **Params:** {n_params:,} ({n_m:.1f}M)
- **Train:** BCE + Dice loss, Adam lr=1e-3, augment เชิงบริบทขวด (flip/rotate/brightness/glare/blur)

## Usage

```python
from PIL import Image
import numpy as np, torch, cv2
from src.train_unet_distill import UNetSmall

model = UNetSmall()
model.load_state_dict(torch.load("pytorch_model.bin", map_location="cpu"))
model.eval()
img = np.array(Image.open("bottle.jpg").convert("RGB"))
img = cv2.resize(img, (256, 256)) / 255.0
x = torch.from_numpy(img.transpose(2, 0, 1)).float().unsqueeze(0)
mask = (model(x) > 0.5).numpy()[0, 0]
```

## Limits (ซื่อตรง)

- ฝึกด้วย pseudo-label ของ SAM3 ไม่ใช่ GT มนุษย์
- ชุดข้อมูล 1 ชนิด (พริกจินดา) × 100 ภาพ → ยังเป็น prototype
- ต้องการ cross-species / calibration เพิ่มก่อนใช้จริง
{eval_line}---
"""


def cmd_hf_push(args):
    """Upload unet_model.pt + config + model card ขึ้น Hugging Face Hub"""
    import json
    from huggingface_hub import HfApi

    device = torch.device("cpu")
    model = UNetSmall()
    model.load_state_dict(torch.load(args.model, map_location=device))
    model.eval()
    n_params = count_params(model)

    # จัดเร่งไฟล์ที่จะอัปโหลดในโฟลเดอร์ชั่วคราว
    stage = os.path.join(args.out, "hf_upload")
    os.makedirs(stage, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(stage, "pytorch_model.bin"))

    config = {
        "arch": "unet_small",
        "in_ch": 3, "out_ch": 1, "base": 16,
        "img_size": args.img_size,
        "input_norm": "resize 256x256, /255",
        "output_act": "sigmoid",
        "num_params": n_params,
        "teacher": "facebook/sam3",
        "distill": True,
        "task": "plant segmentation in vitro bottle",
        "framework": "pytorch",
    }
    with open(os.path.join(stage, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # อ่านผล eval (ถ้ามี) มาใส่ใน model card
    eval_mean = None
    e = getattr(args, "eval_csv", None)
    if e and os.path.exists(e):
        df = pd.read_csv(e, encoding="utf-8-sig")
        eval_mean = df[["iou", "dice", "precision", "recall"]].mean().round(4).tolist()

    with open(os.path.join(stage, "README.md"), "w", encoding="utf-8") as f:
        f.write(build_model_card(args, n_params, eval_mean))

    api = HfApi(token=args.token if args.token else None)
    api.create_repo(repo_id=args.repo, repo_type="model", exist_ok=True,
                    private=args.private)
    api.upload_folder(repo_id=args.repo, folder_path=stage,
                      repo_type="model", commit_message="VitroVision UNet Small (distill from SAM3)")
    print(f"[OK] uploaded → https://huggingface.co/{args.repo} (params {n_params:,})")


# ═══════════════════════ main ═══════════════════════

def main():
    ap = argparse.ArgumentParser(description="Distill SAM3 → U-Net (plant seg ในขวด TC)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("generate-pseudo", help="เฟส 1: SAM3 → pseudo masks")
    p1.add_argument("--data", required=True)
    p1.add_argument("--out", default="distill")
    p1.add_argument("--hf-token", default=None)
    p1.add_argument("--limit", type=int, default=None)
    p1.set_defaults(func=cmd_generate_pseudo)

    p2 = sub.add_parser("train", help="เฟส 2: เทรน U-Net")
    p2.add_argument("--data", required=True)
    p2.add_argument("--pseudo", required=True, help="โฟลเดอร์ pseudo_masks")
    p2.add_argument("--out", default="distill")
    p2.add_argument("--img-size", type=int, default=256)
    p2.add_argument("--epochs", type=int, default=40)
    p2.add_argument("--batch", type=int, default=8)
    p2.add_argument("--lr", type=float, default=1e-3)
    p2.add_argument("--species-holdout", default=None,
                    help="ชื่อชนิด (โฟลเดอร์ย่อย) ที่แยกเป็น val/test — train ไม่เห็นชนิดนี้")
    p2.set_defaults(func=cmd_train)

    p3 = sub.add_parser("eval", help="เฟส 3: ประเมิน student")
    p3.add_argument("--data", required=True)
    p3.add_argument("--pseudo", default=None, help="pseudo masks (val)")
    p3.add_argument("--gt", default=None, help="GT masks จริง (เมื่อ annotate แล้ว)")
    p3.add_argument("--model", required=True, help="unet_model.pt")
    p3.add_argument("--out", default="distill")
    p3.add_argument("--img-size", type=int, default=256)
    p3.set_defaults(func=cmd_eval)

    p4 = sub.add_parser("hf-push", help="เฟส 4: อัปโหลดโมเดลขึ้น Hugging Face")
    p4.add_argument("--model", required=True, help="unet_model.pt")
    p4.add_argument("--repo", required=True, help="HF repo id เช่น peeradon4778/vitrovision-unet-small")
    p4.add_argument("--token", default=None, help="HF token (write)")
    p4.add_argument("--out", default="distill")
    p4.add_argument("--img-size", type=int, default=256)
    p4.add_argument("--eval-csv", default=None, help="unet_eval.csv (ใส่ผลลง model card)")
    p4.add_argument("--private", action="store_true")
    p4.set_defaults(func=cmd_hf_push)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
