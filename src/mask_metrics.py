"""Mask metrics — คำนวณ Level A (mIoU/Dice/F1/precision/recall) ระหว่าง mask สองชุด

ใช้ประเมิน:
  - SAM3 (หรือ student) เทียบ ground-truth masks มือ -> ตัวเลข "segment แม่น/ไม่" (H1, เกณฑ์ mIoU>=0.65)
  - เครื่องผูกกับ `benchmark_baselines.compute_metrics` (สูตรเดียวกันทั้งโปรเจกต์)

รัน (CPU, ทันที ไม่ต้องรอ Colab):
    python src/mask_metrics.py --pred data/processed/sam3_masks --gt data/processed/ground_truth_masks \
        --out data/processed/levelA --size 512
- --pred/--gt: โฟลเดอร์มี <title>.png (binary, ขาว=ต้น)
- --size: resize ทั้งคู่เป็น size×size (0 = ไม่ resize) — ทำเพื่อให้เทียบที่ resolution เดียวกัน
ผลลัพธ์: levelA_per_image.csv + levelA_summary.csv (mean±std) + ตัวเลขพิมพ์
"""

import argparse
import glob
import os

import cv2
import numpy as np
import pandas as pd

sys_path = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, sys_path)
from benchmark_baselines import compute_metrics  # noqa: E402


def load_mask_dir(d):
    """โหลดทุก mask binary ชื่อ -> bool"""
    out = {}
    for ext in ("*.png",):
        for p in glob.glob(os.path.join(d, ext)):
            name = os.path.splitext(os.path.basename(p))[0]
            m = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
            if m is not None:
                out[name] = m
    return out


def resize_bool(m, size):
    if size and size > 0 and (m.shape[0] != size or m.shape[1] != size):
        m = cv2.resize(m.astype(np.uint8), (size, size),
                       interpolation=cv2.INTER_NEAREST)
    return m.astype(bool)


def main():
    ap = argparse.ArgumentParser(description="Level A mask metrics (mIoU/Dice)")
    ap.add_argument("--pred", required=True, help="โฟลเดอร์ predicted masks")
    ap.add_argument("--gt", required=True, help="โฟลเดอร์ ground-truth masks (มือ)")
    ap.add_argument("--out", default="data/processed/levelA")
    ap.add_argument("--size", type=int, default=512, help="resize ทั้งคู่เป็น size×size (0=ไม่)")
    args = ap.parse_args()

    pred = load_mask_dir(args.pred)
    gt = load_mask_dir(args.gt)
    names = sorted(set(pred) & set(gt))
    if not names:
        raise SystemExit(f"ไม่มีชื่อภาพที่ตรงกันระหว่าง --pred/--gt ({len(pred)}/{len(gt)})")
    print(f"[INFO] pred={len(pred)} · gt={len(gt)} · ตรงกัน {len(names)} ภาพ")

    os.makedirs(args.out, exist_ok=True)
    rows = []
    for name in names:
        p = resize_bool(pred[name], args.size)
        g = resize_bool(gt[name], args.size)
        m = compute_metrics(p, g)
        m["image"] = name
        rows.append(m)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(args.out, "levelA_per_image.csv"), index=False,
              encoding="utf-8-sig")

    cols = ["iou", "dice", "precision", "recall", "f1"]
    summ = df[cols].agg(["mean", "std"]).round(4)
    summ.loc["n"] = [len(df)] + [None] * (len(cols) - 1)
    summ.to_csv(os.path.join(args.out, "levelA_summary.csv"), encoding="utf-8-sig")

    print("\n=== Level A: segmentation metrics (mean±std, n=%d) ===" % len(df))
    print(summ.to_string())
    print(f"\n[OK] {os.path.join(args.out, 'levelA_summary.csv')} + levelA_per_image.csv")


if __name__ == "__main__":
    main()
