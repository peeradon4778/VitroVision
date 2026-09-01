# -*- coding: utf-8 -*-
"""
VitroVision — เทรนโมเดล segmentation "ของเราเอง" (แทนที่ SAM3 ในจุด segmentation ของ pipeline)

โมเดล: U-Net + MobileNetV3-Small (encoder: timm-mobilenetv3_small_100, pretrain ImageNet) ~3.6M params
เป้าหมาย: segment ต้นเพาะเลี้ยงเนื้อเยื่อในขวดแก้ว (glare/ไอน้ำ/ความโค้งแก้ว) — รันบน CPU ได้

ขั้นตอน (stage):
  prepare   — สร้าง teacher masks แบบ classical-green จาก 100 ภาพขวด (CPU, ไม่พึ่ง SAM3)
  pretrain  — เทรนบน greenhouse_leafy_segmentation (HF, 3,348 คู่ image+mask) เพื่อให้เห็นใบ/ต้นไม้ทั่วไป
  finetune  — fine-tune กับ 100 ภาพขวดของเรา (80 train / 20 holdout) ด้วย teacher mask
  eval      — ประเมิน holdout (mIoU/Dice เทียบ teacher) + สร้างภาพ overlay ตัวอย่าง
  push      — อัปโหลด pytorch_model.bin + config.json + model card ขึ้น HF repo

ความซื่อตรง (honesty):
  - teacher = classical-green (ไม่ใช่ SAM3 ไม่ใช่ human GT) -> ตัวเลข eval เทียบ teacher เท่านั้น
  - เมื่อ annotate mask มือครบ 30 ภาพ จะ fine-tune/eval กับ GT จริงในภายหลัง
"""
import argparse
import glob
import json
import os
import sys
import time

import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

import segmentation_models_pytorch as smp

sys.stdout.reconfigure(encoding="utf-8")

IMG_SIZE = 256
ENCODER = "timm-mobilenetv3_small_100"   # MobileNetV3-Small (timm)
MODEL_REPO = "peeradon4778/vitrovision-unet-small"

# เกณฑ์สีเขียว (ตรงกับ space/app.py fallback)
_LOWER_GREEN = np.array([35, 40, 40], dtype=np.uint8)
_UPPER_GREEN = np.array([85, 255, 255], dtype=np.uint8)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
BATCH_DIR = os.path.join(ROOT, "data", "raw", "20260814_batch")
TEACHER_DIR = os.path.join(ROOT, "data", "processed", "green_teacher_masks")
WORK_DIR = os.path.join(ROOT, "data", "work")
GREENHOUSE_DIR = os.path.join(WORK_DIR, "greenhouse_ds")
MODEL_DIR = os.path.join(ROOT, "models")
SAMPLE_DIR = os.path.join(WORK_DIR, "model_eval_samples")


# ---------------------------------------------------------------- model
def build_model():
    m = smp.Unet(encoder_name=ENCODER, encoder_weights="imagenet", in_channels=3, classes=1)
    return m


# ---------------------------------------------------------------- teacher (classical green)
def green_mask(rgb_bgr):
    """rgb_bgr: HxWx3 (BGR uint8) -> mask 0/255 uint8"""
    hsv = cv2.cvtColor(rgb_bgr, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, _LOWER_GREEN, _UPPER_GREEN)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return m


# ---------------------------------------------------------------- metrics / loss
def dice_coef(pred_bin, target):
    inter = (pred_bin * target).sum()
    return (2.0 * inter + 1e-6) / (pred_bin.sum() + target.sum() + 1e-6)


def iou_coef(pred_bin, target):
    inter = (pred_bin * target).sum()
    return (inter + 1e-6) / (pred_bin.sum() + target.sum() - inter + 1e-6)


def bce_dice_loss(logits, target):
    bce = nn.functional.binary_cross_entropy_with_logits(logits, target)
    prob = torch.sigmoid(logits)
    d = dice_coef((prob > 0.5).float(), target)
    return bce + (1.0 - d)


# ---------------------------------------------------------------- dataset (จากโฟลเดอร์บนดิสก์)
class DiskMaskDataset(Dataset):
    """คู่ (ภาพ jpg, mask png) บนดิสก์ — โหลดทีละ batch ไม่กิน RAM"""

    def __init__(self, pairs, size=IMG_SIZE, augment=False):
        self.pairs = pairs          # list[(img_path, mask_path)]
        self.size = size
        self.augment = augment

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, i):
        ip, mp = self.pairs[i]
        img = cv2.imread(ip, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (self.size, self.size), interpolation=cv2.INTER_AREA)
        msk = cv2.imread(mp, cv2.IMREAD_GRAYSCALE)
        msk = cv2.resize(msk, (self.size, self.size), interpolation=cv2.INTER_NEAREST)
        if self.augment and np.random.rand() < 0.5:
            img = cv2.flip(img, 1)
            msk = cv2.flip(msk, 1)
        x = torch.from_numpy(img.astype(np.float32) / 255.0).permute(2, 0, 1)   # 3,S,S
        y = torch.from_numpy((msk > 127).astype(np.float32)).unsqueeze(0)      # 1,S,S
        return x, y


# ---------------------------------------------------------------- stage: prepare
def cmd_prepare(args):
    os.makedirs(TEACHER_DIR, exist_ok=True)
    imgs = sorted(glob.glob(os.path.join(BATCH_DIR, "*.jpg")))
    if not imgs:
        raise SystemExit(f"ไม่พบภาพใน {BATCH_DIR}")
    made = 0
    for p in imgs:
        stem = os.path.splitext(os.path.basename(p))[0]
        out = os.path.join(TEACHER_DIR, stem + ".png")
        if os.path.exists(out):
            made += 1
            continue
        img = cv2.imread(p, cv2.IMREAD_COLOR)
        m = green_mask(img)
        cv2.imwrite(out, m)
        made += 1
    print(f"[prepare] teacher masks ครบ {made}/{len(imgs)} -> {TEACHER_DIR}")


# ---------------------------------------------------------------- stage: pretrain (greenhouse)
def _export_greenhouse(n):
    """โหลด greenhouse_leafy_segmentation จาก HF แล้ว export เป็น jpg/png บนดิสก์ (ครั้งเดียว)"""
    os.makedirs(os.path.join(GREENHOUSE_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(GREENHOUSE_DIR, "masks"), exist_ok=True)
    existing = len(glob.glob(os.path.join(GREENHOUSE_DIR, "images", "*.jpg")))
    if existing >= n:
        print(f"[pretrain] greenhouse export แล้ว {existing} ภาพ (ข้าม)")
        return existing
    from datasets import load_dataset
    ds = load_dataset("Project-AgML/greenhouse_leafy_segmentation", split="train", streaming=True)
    count = 0
    for i, row in enumerate(ds):
        if count >= n:
            break
        img = np.array(row["image"])
        msk = np.array(row["mask"])
        if img.ndim != 3 or msk.ndim < 2:
            continue
        g = msk.mean(axis=2).astype(np.uint8) if msk.ndim == 3 else msk.astype(np.uint8)
        fn = f"{count:05d}"
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(GREENHOUSE_DIR, "images", fn + ".jpg"), img_bgr)
        cv2.imwrite(os.path.join(GREENHOUSE_DIR, "masks", fn + ".png"), (g > 127).astype(np.uint8) * 255)
        count += 1
        if count % 500 == 0:
            print(f"[pretrain] export {count}...", flush=True)
    print(f"[pretrain] greenhouse export ครบ {count} ภาพ -> {GREENHOUSE_DIR}")
    return count


def cmd_pretrain(args):
    n = _export_greenhouse(args.n)
    imgs = sorted(glob.glob(os.path.join(GREENHOUSE_DIR, "images", "*.jpg")))
    pairs = [(p, os.path.join(GREENHOUSE_DIR, "masks", os.path.splitext(os.path.basename(p))[0] + ".png"))
             for p in imgs]
    rng = np.random.RandomState(0)
    rng.shuffle(pairs)
    nval = max(1, int(0.1 * len(pairs)))
    val_pairs, train_pairs = pairs[:nval], pairs[nval:]
    print(f"[pretrain] train={len(train_pairs)} val={len(val_pairs)} (จาก {n} ภาพ)", flush=True)

    train_ds = DiskMaskDataset(train_pairs, augment=True)
    val_ds = DiskMaskDataset(val_pairs, augment=False)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
    val_dl = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=0)

    model = build_model()
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    os.makedirs(MODEL_DIR, exist_ok=True)
    best = -1.0
    for ep in range(args.epochs):
        model.train()
        t0 = time.time()
        tot_loss, nb = 0.0, 0
        for x, y in train_dl:
            opt.zero_grad()
            loss = bce_dice_loss(model(x), y)
            loss.backward()
            opt.step()
            tot_loss += loss.item() * x.size(0)
            nb += x.size(0)
        model.eval()
        vd, nv = 0.0, 0
        with torch.no_grad():
            for x, y in val_dl:
                prob = torch.sigmoid(model(x))
                vd += dice_coef((prob > 0.5).float(), y).item() * x.size(0)
                nv += x.size(0)
        vd /= max(nv, 1)
        dt = time.time() - t0
        print(f"[pretrain] ep {ep+1}/{args.epochs} loss={tot_loss/max(nb,1):.4f} val_dice={vd:.4f} ({dt:.0f}s)", flush=True)
        if vd > best:
            best = vd
            torch.save(model.state_dict(), os.path.join(MODEL_DIR, "vitrovision_unet_pretrain.pt"))
            print(f"[pretrain] save best val_dice={best:.4f}", flush=True)
    print(f"[pretrain] เสร็จ best val_dice={best:.4f}", flush=True)


# ---------------------------------------------------------------- stage: finetune (100 ภาพขวด)
def cmd_finetune(args):
    imgs = sorted(glob.glob(os.path.join(BATCH_DIR, "*.jpg")))
    pairs = []
    for p in imgs:
        stem = os.path.splitext(os.path.basename(p))[0]
        m = os.path.join(TEACHER_DIR, stem + ".png")
        if os.path.exists(m):
            pairs.append((p, m))
    print(f"[finetune] ภาพขวดที่มี teacher mask: {len(pairs)}")
    # deterministic split: ทุกตัวที่ 5 -> val
    train_pairs = [p for i, p in enumerate(pairs) if i % 5 != 0]
    val_pairs = [p for i, p in enumerate(pairs) if i % 5 == 0]
    print(f"[finetune] train={len(train_pairs)} val={len(val_pairs)}", flush=True)

    train_ds = DiskMaskDataset(train_pairs, augment=True)
    val_ds = DiskMaskDataset(val_pairs, augment=False)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
    val_dl = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=0)

    model = build_model()
    if args.init and os.path.exists(args.init):
        model.load_state_dict(torch.load(args.init, map_location="cpu"))
        print(f"[finetune] เริ่มจาก {args.init}", flush=True)
    else:
        print("[finetune] เริ่มจาก ImageNet weights (ไม่มี pretrain checkpoint)", flush=True)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    os.makedirs(MODEL_DIR, exist_ok=True)
    best = -1.0
    for ep in range(args.epochs):
        model.train()
        t0 = time.time()
        tot_loss, nb = 0.0, 0
        for x, y in train_dl:
            opt.zero_grad()
            loss = bce_dice_loss(model(x), y)
            loss.backward()
            opt.step()
            tot_loss += loss.item() * x.size(0)
            nb += x.size(0)
        model.eval()
        vd, nv = 0.0, 0
        with torch.no_grad():
            for x, y in val_dl:
                prob = torch.sigmoid(model(x))
                vd += dice_coef((prob > 0.5).float(), y).item() * x.size(0)
                nv += x.size(0)
        vd /= max(nv, 1)
        dt = time.time() - t0
        print(f"[finetune] ep {ep+1}/{args.epochs} loss={tot_loss/max(nb,1):.4f} val_dice={vd:.4f} ({dt:.0f}s)", flush=True)
        if vd > best:
            best = vd
            torch.save(model.state_dict(), os.path.join(MODEL_DIR, "vitrovision_unet_small.pt"))
            json.dump({"arch": "smp_unet", "encoder": ENCODER, "img_size": IMG_SIZE,
                       "classes": 1, "task": "tissue_culture_plant_segmentation",
                       "teacher": "classical_green", "pretrain": "greenhouse_leafy_segmentation"},
                      open(os.path.join(MODEL_DIR, "config.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
            print(f"[finetune] save best val_dice={best:.4f}", flush=True)
    print(f"[finetune] เสร็จ best val_dice={best:.4f}", flush=True)


# ---------------------------------------------------------------- stage: eval
def cmd_eval(args):
    cfg = json.load(open(os.path.join(MODEL_DIR, "config.json"), encoding="utf-8"))
    model = build_model()
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "vitrovision_unet_small.pt"), map_location="cpu"))
    model.eval()
    imgs = sorted(glob.glob(os.path.join(BATCH_DIR, "*.jpg")))
    pairs = []
    for p in imgs:
        stem = os.path.splitext(os.path.basename(p))[0]
        m = os.path.join(TEACHER_DIR, stem + ".png")
        if os.path.exists(m):
            pairs.append((p, m))
    val_pairs = [p for i, p in enumerate(pairs) if i % 5 == 0]  # holdout 20% (ไม่เคยเห็นตอน finetune)
    print(f"[eval] holdout (ไม่เคยเห็นตอน train) = {len(val_pairs)} ภาพ")

    os.makedirs(SAMPLE_DIR, exist_ok=True)
    dice_s, iou_s = [], []
    rows = []
    with torch.no_grad():
        for p, m in val_pairs:
            stem = os.path.splitext(os.path.basename(p))[0]
            img = cv2.imread(p, cv2.IMREAD_COLOR)
            gt = (cv2.imread(m, cv2.IMREAD_GRAYSCALE) > 127).astype(np.uint8)
            H, W = img.shape[:2]
            inp = cv2.resize(img, (IMG_SIZE, IMG_SIZE)).astype(np.float32) / 255.0
            x = torch.from_numpy(inp.transpose(2, 0, 1)).float().unsqueeze(0)
            prob = torch.sigmoid(model(x))[0, 0].numpy()
            pred_small = prob > 0.5
            pred = cv2.resize(pred_small.astype(np.uint8) * 255, (W, H), interpolation=cv2.INTER_NEAREST) > 0
            gts = cv2.resize(gt * 255, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_NEAREST) > 0
            d = float(dice_coef(torch.from_numpy(pred_small.astype(np.float32)),
                                torch.from_numpy(gts.astype(np.float32))))
            iu = float(iou_coef(torch.from_numpy(pred_small.astype(np.float32)),
                                torch.from_numpy(gts.astype(np.float32))))
            dice_s.append(d); iou_s.append(iu)
            rows.append({"img": stem, "dice": round(d, 4), "iou": round(iu, 4)})
            if len(dice_s) <= 8:  # ภาพตัวอย่าง
                ov = img.copy()
                ov[pred] = (ov[pred] * 0.5 + np.array([0, 200, 0]) * 0.5).astype(np.uint8)  # เขียว=pred
                red = cv2.resize((gt * 255).astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST) > 0
                ov[red & (~pred)] = (0, 0, 255)   # แดง = teacher ที่ model พลาด
                cv2.putText(ov, f"dice={d:.3f}", (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.imwrite(os.path.join(SAMPLE_DIR, f"{stem}_eval.png"), ov)
    dice_s = np.array(dice_s); iou_s = np.array(iou_s)
    print(f"[eval] mean dice={dice_s.mean():.4f}  mean IoU={iou_s.mean():.4f}  (n={len(dice_s)})")
    print(f"[eval] min={dice_s.min():.4f} max={dice_s.max():.4f}")
    json.dump(rows, open(os.path.join(WORK_DIR, "eval_holdout.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[eval] ภาพตัวอย่าง -> {SAMPLE_DIR} | ผลลัพธ์ -> {os.path.join(WORK_DIR, 'eval_holdout.json')}")


# ---------------------------------------------------------------- stage: push (HF)
def cmd_push(args):
    from huggingface_hub import HfApi, login
    tok = os.environ.get("HF_TOKEN") or None
    api = HfApi(token=tok)
    repo = args.repo or MODEL_REPO
    try:
        api.create_repo(repo_id=repo, repo_type="model", exist_ok=True)
    except Exception as e:
        print(f"[push] create_repo: {e}")
    files = {
        os.path.join(MODEL_DIR, "vitrovision_unet_small.pt"): "pytorch_model.bin",
        os.path.join(MODEL_DIR, "config.json"): "config.json",
    }
    for local, remote in files.items():
        if not os.path.exists(local):
            print(f"[push] ไม่พบ {local} — รัน finetune ก่อน")
            return
    # model card
    card = _model_card()
    card_path = os.path.join(MODEL_DIR, "hf_README.md")
    open(card_path, "w", encoding="utf-8").write(card)
    for local, remote in files.items():
        api.upload_file(path_or_fileobj=local, path_in_repo=remote, repo_id=repo, repo_type="model")
        print(f"[push] upload {remote} OK")
    api.upload_file(path_or_fileobj=card_path, path_in_repo="README.md", repo_id=repo, repo_type="model")
    print(f"[push] เสร็จ -> https://huggingface.co/{repo}")


def _model_card():
    return f"""---
tags: [segmentation, plant, tissue-culture, computer-vision, u-net, mobilenetv3]
license: mit
---

# VitroVision U-Net Small — segmentation ต้นเพาะเลี้ยงเนื้อเยื่อในขวดแก้ว

โมเดล **ของเราเอง** (U-Net + MobileNetV3-Small, ~3.6M params) สำหรับ segment ต้นเพาะเลี้ยงเนื้อเยื่อ
**ผ่านขวดแก้ว** (non-destructive) — ใช้**แทนที่ SAM3** ในจุด segmentation ของ VitroVision pipeline
(ประมวลผลบน CPU ได้ เร็ว เหมาะ mobile/edge)

## การเทรน
- encoder: `timm-mobilenetv3_small_100` (ImageNet pretrained)
- pretrain: `Project-AgML/greenhouse_leafy_segmentation` (3,348 คู่ image+mask จาก HF)
- fine-tune: 100 ภาพขวดเพาะเลี้ยงเนื้อเยื่อของเรา (80/20) โดย teacher = classical-green mask
- input: RGB 256x256, output: probability mask (plant=1)

## ความซื่อตรง (honesty)
- teacher ปัจจุบัน = **classical-green** (ไม่ใช่ SAM3, ไม่ใช่ human GT)
  -> mIoU/Dice ที่รายงานเทียบ **teacher** ไม่ใช่เทียบมนุษย์
- human ground-truth masks (30 ภาพ) กำลัง annotate -> จะ fine-tune/eval กับ GT จริงเมื่อพร้อม
- ชุดข้อมูลเฉพาะ: 1 ชนิด (พริก) x 100 ภาพ -> prototype สำหรับโชว์/ต่อยอด

## ใช้ยังไง
```python
import segmentation_models_pytorch as smp, torch, cv2, numpy as np
m = smp.Unet(encoder_name="timm-mobilenetv3_small_100", in_channels=3, classes=1)
m.load_state_dict(torch.load("pytorch_model.bin", map_location="cpu"))
m.eval()
img = cv2.imread("bottle.jpg"); img = cv2.resize(img, (256, 256)) / 255.0
x = torch.from_numpy(img.transpose(2, 0, 1)).float().unsqueeze(0)
mask = (torch.sigmoid(m(x)) > 0.5).numpy()[0, 0]
```

## ข้อมูลอ้างอิง
- U-Net: Ronneberger et al. 2015 (arXiv:1505.04597)
- MobileNetV3: Howard et al. 2019 (arXiv:1905.02244)
- greenhouse dataset: Project-AgML/greenhouse_leafy_segmentation (HuggingFace)
"""


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="VitroVision U-Net small (แทน SAM3) — train/eval/push")
    ap.add_argument("stage", choices=["prepare", "pretrain", "finetune", "eval", "push"])
    ap.add_argument("--n", type=int, default=1500, help="จำนวนภาพ greenhouse ที่ใช้ pretrain")
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--init", default=None, help="checkpoint เริ่มต้นของ finetune (pretrain)")
    ap.add_argument("--repo", default=None, help="HF repo (default: peeradon4778/vitrovision-unet-small)")
    args = ap.parse_args()
    print(f"[{args.stage}] เริ่ม", flush=True)
    t0 = time.time()
    {"prepare": cmd_prepare, "pretrain": cmd_pretrain, "finetune": cmd_finetune,
     "eval": cmd_eval, "push": cmd_push}[args.stage](args)
    print(f"[{args.stage}] เสร็จใน {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
