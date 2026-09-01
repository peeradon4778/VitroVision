# -*- coding: utf-8 -*-
"""train_greenhouse — เทรน U-Net (MobileNetV3-Small) บน greenhouse_leafy_segmentation
แบบ checkpoint/resume ต่อเนื่อง + เทสต์บน 100 ภาพขวด (ชุดทดสอบ VitroVision) ในตัว

รัน (env ml, CPU ก็ได้ — เรียกซ้ำได้เรื่อย ๆ มันจะ resume ต่อจนครบ):
    python src/train_greenhouse.py --data data/work/greenhouse_ds \
        --test data/raw/20260814_batch --out data/work/greenhouse_ds \
        --img-size 256 --batch 4 --epochs 15

- resume อัตโนมัติ: ถ้ามี <out>/ckpt.pt → โหลดแล้วเทรนต่อจาก epoch ถัดไป (ไม่เริ่มใหม่)
- save checkpoint ทุก epoch (กันงานหายถ้าเครื่องหลับ/ปิด)
- ครบ epochs → save final_model.pt + best_model.pt + ประเมินบน 100 ภาพขวด → test_100.csv
"""
import argparse
import glob
import os

import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

import segmentation_models_pytorch as smp

READY_HEIGHT = 0.20  # เกณฑ์พร้อมอนุบาล (tuned บนชุดประเมิน 98 ภาพ — Youden-balanced 0.717 sens / 0.579 spec)


def _stem(p):
    return os.path.splitext(os.path.basename(p))[0]


class SegDS(Dataset):
    def __init__(self, pairs, img_size=256, aug=False):
        self.pairs = pairs
        self.img_size = img_size
        self.aug = aug

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, i):
        ip, mp = self.pairs[i]
        img = cv2.imread(ip)
        img = cv2.resize(img, (self.img_size, self.img_size), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        mask = cv2.imread(mp, cv2.IMREAD_GRAYSCALE)
        mask = cv2.resize(mask, (self.img_size, self.img_size), interpolation=cv2.INTER_NEAREST)
        mask = (mask > 127).astype(np.float32)
        if self.aug and np.random.rand() > 0.5:
            img = cv2.flip(img, 1)
            mask = cv2.flip(mask, 1)
        return (torch.from_numpy(img.transpose(2, 0, 1)).float(),
                torch.from_numpy(mask).unsqueeze(0).float())


def dice_loss(pred, target, eps=1e-6):
    inter = (pred * target).sum()
    return 1 - (2 * inter + eps) / (pred.sum() + target.sum() + eps)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="greenhouse_ds (มี images/ + masks/)")
    ap.add_argument("--test", default=None, help="โฟลเดอร์ 100 ภาพขวด (ชุดทดสอบ)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--img-size", type=int, default=256)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--epochs", type=int, default=15, help="เป้า epoch รวม (resume ต่อยอด)")
    ap.add_argument("--lr", type=float, default=1e-3)
    args = ap.parse_args()

    # ---- จับคู่ภาพ-mask ----
    masks_dir = os.path.join(args.data, "masks")
    pairs = []
    for ip in sorted(glob.glob(os.path.join(args.data, "images", "*.*"))):
        stem = _stem(ip)
        mp = None
        for ext in (".png", ".jpg", ".jpeg"):
            c = os.path.join(masks_dir, stem + ext)
            if os.path.exists(c):
                mp = c
                break
        if mp:
            pairs.append((ip, mp))
    print(f"[info] pairs: {len(pairs)}")
    if len(pairs) < 10:
        raise SystemExit("ภาพ/mask น้อยเกินไป — เช็ค --data")

    rng = np.random.default_rng(42)
    idx = rng.permutation(len(pairs))
    nv = max(int(len(pairs) * 0.1), 1)
    val_idx, tr_idx = idx[:nv], idx[nv:]
    train_ds = SegDS([pairs[i] for i in tr_idx], args.img_size, aug=True)
    val_ds = SegDS([pairs[i] for i in val_idx], args.img_size, aug=False)
    print(f"[info] train {len(train_ds)} / val {len(val_ds)}")
    train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=2)

    # ---- โมเดล + resume ----
    os.makedirs(args.out, exist_ok=True)
    model = smp.Unet(encoder_name="timm-mobilenetv3_small_100", encoder_weights="imagenet",
                     in_channels=3, classes=1)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    bce = nn.BCEWithLogitsLoss()

    start_epoch, best = 0, 0.0
    ckpt_path = os.path.join(args.out, "ckpt.pt")
    if os.path.exists(ckpt_path):
        c = torch.load(ckpt_path, map_location="cpu")
        model.load_state_dict(c["model"])
        opt.load_state_dict(c["opt"])
        start_epoch = c["epoch"]
        best = c.get("best", 0.0)
        print(f"[resume] ต่อจาก epoch {start_epoch} (best val_dice {best:.4f})")

    # ---- เทรนต่อเนื่อง ----
    for epoch in range(start_epoch + 1, args.epochs + 1):
        model.train()
        tl = 0.0
        t0 = time_per_epoch = None
        import time
        t0 = time.time()
        for img, mask in train_loader:
            pred = model(img)
            loss = bce(pred, mask) + dice_loss(torch.sigmoid(pred), mask)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tl += loss.item() * len(img)
        model.eval()
        vd = 0.0
        with torch.no_grad():
            for img, mask in val_loader:
                p = torch.sigmoid(model(img)) > 0.5
                inter = (p & mask.bool()).sum().item()
                vd += (2 * inter / (p.sum().item() + mask.sum().item() + 1e-6)) * len(img)
        vd /= len(val_ds)
        dt = time.time() - t0
        print(f"[epoch {epoch}/{args.epochs}] loss {tl / len(train_ds):.4f} · "
              f"val_dice {vd:.4f} · {dt:.0f}s")
        if vd > best:
            best = vd
            torch.save(model.state_dict(), os.path.join(args.out, "best_model.pt"))
        torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
                    "epoch": epoch, "best": best}, ckpt_path)

    # ---- save final ----
    best_path = os.path.join(args.out, "best_model.pt")
    if os.path.exists(best_path):
        model.load_state_dict(torch.load(best_path, map_location="cpu"))
    torch.save(model.state_dict(), os.path.join(args.out, "final_model.pt"))
    print(f"[ok] final_model.pt saved (best val_dice {best:.4f})")

    # ---- เทสต์บน 100 ภาพขวด ----
    if args.test:
        model.eval()
        outdir = os.path.join(args.out, "pred_100")
        os.makedirs(outdir, exist_ok=True)
        rows = []
        with torch.no_grad():
            for ip in sorted(glob.glob(os.path.join(args.test, "*.jpg"))):
                img = cv2.imread(ip)
                H, W = img.shape[:2]
                x = cv2.resize(img, (args.img_size, args.img_size))
                x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
                t = torch.from_numpy(x.transpose(2, 0, 1)).float().unsqueeze(0)
                p = torch.sigmoid(model(t))[0, 0].numpy()
                m = cv2.resize((p > 0.5).astype(np.uint8) * 255, (W, H),
                               interpolation=cv2.INTER_NEAREST)
                cv2.imwrite(os.path.join(outdir, _stem(ip) + ".png"), m)
                ys, xs = np.where(m > 0)
                hh = (xs.max() - xs.min() + 1) / H if len(xs) else 0.0
                ww = (ys.max() - ys.min() + 1) / W if len(ys) else 0.0
                rows.append({"image": os.path.basename(ip),
                             "coverage_ratio": round(int((m > 0).sum()) / (H * W), 4),
                             "height_proxy": round(hh, 4),
                             "width_proxy": round(ww, 4)})
        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(args.out, "test_100.csv"), index=False, encoding="utf-8-sig")
        print(f"[ok] test_100.csv + pred_100/ ({len(df)} ภาพ)")
        print(df.describe().round(4).to_string())

        gt_csv = "data/processed/ground_truth.csv"
        if os.path.exists(gt_csv):
            gt = pd.read_csv(gt_csv, encoding="utf-8-sig")
            df["expert"] = df["image"].map(dict(zip(gt["image"], gt["expert_verdict"])))
            df["pred_verdict"] = df["height_proxy"].apply(
                lambda h: "พร้อมอนุบาล" if h >= READY_HEIGHT else "ยังไม่พร้อม")
            sub = df[df["expert"].isin(["พร้อมอนุบาล", "ยังไม่พร้อม"])].dropna()
            if len(sub):
                acc = (sub["pred_verdict"] == sub["expert"]).mean()
                sens = ((sub["pred_verdict"] == "พร้อมอนุบาล")
                        & (sub["expert"] == "พร้อมอนุบาล")).sum() \
                    / max((sub["expert"] == "พร้อมอนุบาล").sum(), 1)
                print(f"[verdict on 100] n={len(sub)} · acc {acc:.3f} · "
                      f"sensitivity(พร้อม) {sens:.3f}")
    print("[DONE] train_greenhouse เสร็จ")


if __name__ == "__main__":
    main()
