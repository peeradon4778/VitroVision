"""Cross-species benchmark: ทดสอบว่า SAM3 PCS แบบ zero-shot ใช้ได้ข้ามชนิดพืช (cross-species) หรือไม่

คำถามที่ตอบ:
  1) Segmentation generalization — SAM3 แบ่งส่วน/วัดขนาดต้น (area/height) ได้เสถียรข้ามชนิดไหม
     (ดู n, mean±std ของ trait, zero_mask_rate, sanity ของความสูง/พื้นที่)
  2) Readyness threshold transfer — เกณฑ์ generic (READY_HEIGHT) ใช้ได้ข้ามชนิดไหม หรือต้อง calibrate ต่อชนิด
     (ถ้ามี --gt expert_verdict → คำนวณ accuracy ต่อชนิด; เทียบ generic vs per-species threshold)

รันบน Colab (GPU — SAM3 ต้อง GPU):
    python src/benchmark_cross_species.py --data <data_base> --out <out> --hf-token <TOKEN>
        [--species-map <image,species.csv>] [--gt <gt.csv>] [--config config.json] [--limit N]

รูปแบบ --data (รองรับ 2 แบบ):
    A) `--data <base>` โดยแต่ละโฟลเดอร์ย่อย = ชนิดหนึ่ง (ชื่อโฟลเดอร์ = species)
    B) `--data <folder>` (ภาพรวมกัน) + `--species-map <csv image,species>` ระบุชนิดต่อภาพ
--gt: CSV `image,species,height_cm,width_cm,area_cm2,expert_verdict` (อย่างน้อย height หรือ verdict ก็พอ)

ผลลัพธ์: cross_species_per_image.csv, cross_species_summary.csv, cross_species_compare.png
หมายเหตุ: sample ต่อชนิดอาจเล็ก — รายงานเป็น pilot ต่อชนิด (n, mean±std) ไม่ใช่ข้อสรุปสถิติขั้นสุดท้าย
"""

import argparse
import glob
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))


# ---------------------------------------------------------------- io helpers
def collect_species_images(base, species_map=None, limit=None):
    """คืน list ของ (species, image_path) ตามรูปแบบ A หรือ B"""
    items = []
    if species_map is not None:
        # รูปแบบ B: ทุกภาพใน base → ระบุชนิดผ่าน csv
        df = pd.read_csv(species_map, encoding="utf-8-sig")
        imgs = sorted(glob.glob(os.path.join(base, "*.jpg")) +
                      glob.glob(os.path.join(base, "*.jpeg")) +
                      glob.glob(os.path.join(base, "*.png")))
        name2sp = dict(zip(df["image"].astype(str), df["species"].astype(str)))
        for p in imgs:
            sp = name2sp.get(os.path.basename(p))
            if sp is None:
                sp = "unknown"
            items.append((sp, p))
    else:
        # รูปแบบ A: โฟลเดอร์ย่อย = ชนิด
        for sp in sorted(os.listdir(base)):
            sdir = os.path.join(base, sp)
            if not os.path.isdir(sdir):
                continue
            imgs = sorted(glob.glob(os.path.join(sdir, "*.jpg")) +
                          glob.glob(os.path.join(sdir, "*.jpeg")) +
                          glob.glob(os.path.join(sdir, "*.png")))
            for p in imgs:
                items.append((sp, p))
    # limit ต่อชนิด (กันรันยาวบน Colab เมื่อชุดเล็ก)
    if limit:
        from collections import defaultdict
        cnt = defaultdict(int)
        limited = []
        for sp, p in items:
            if cnt[sp] < limit:
                limited.append((sp, p))
                cnt[sp] += 1
        items = limited
    return items


def pearson(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) != len(y) or len(x) < 3:
        return None
    mx, my = x.mean(), y.mean()
    num = float(((x - mx) * (y - my)).sum())
    denom = (float(((x - mx) ** 2).sum()) * float(((y - my) ** 2).sum())) ** 0.5
    return num / denom if denom > 0 else None


def accuracy(gt_cls, pred_cls):
    gt = np.asarray(gt_cls, float)
    pr = np.asarray(pred_cls, float)
    if len(gt) == 0:
        return None, 0
    return float((gt == pr).mean()), len(gt)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Cross-species benchmark (SAM3 zero-shot)")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพ (หรือ base ที่มีโฟลเดอร์ย่อย=ชนิด)")
    ap.add_argument("--out", required=True, help="โฟลเดอร์ผลลัพธ์")
    ap.add_argument("--species-map", default=None, help="CSV image,species (รูปแบบ B)")
    ap.add_argument("--gt", default=None, help="CSV image,species,height_cm,width_cm,area_cm2,expert_verdict")
    ap.add_argument("--config", default=None, help="config.json (ใช้ค่าคงที่ pipeline)")
    ap.add_argument("--hf-token", default=None, help="HF_TOKEN (SAM3 gated)")
    ap.add_argument("--limit", type=int, default=None, help="จำกัดภาพต่อชนิด (สำหรับชุดเล็ก)")
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    args = ap.parse_args()

    import torch
    import cv2
    from PIL import Image
    import sam3_growth_pipeline as P

    # ตั้งค่า pipeline ตาม config.json (ค่า READY_HEIGHT, thresholds, prompts, etc.)
    if args.config:
        P.load_config(args.config)
    else:
        # โหลด config.json ข้างโปรเจกต์ถ้ามี
        cfg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
        if os.path.exists(cfg):
            P.load_config(cfg)

    device = args.device if (args.device == "cuda" and torch.cuda.is_available()) else "cpu"
    if device == "cpu":
        print("[WARN] SAM3 ไม่รองรับ CPU — ผล segmentation จะไม่ได้จริง unless GPU")

    if args.hf_token:
        from huggingface_hub import login
        login(token=args.hf_token, add_to_git_credential=False)

    # โหลด SAM3
    print(f"[INFO] โหลด SAM3 (facebook/sam3) — หลายนาที (device={device})")
    from transformers import Sam3Processor, Sam3Model
    model = Sam3Model.from_pretrained("facebook/sam3").to(device)
    processor = Sam3Processor.from_pretrained("facebook/sam3")

    items = collect_species_images(args.data, args.species_map, args.limit)
    print(f"[INFO] ภาพรวม {len(items)} · จำแนกตามชนิด")

    rows = []
    t0 = time.time()
    for i, (species, img_path) in enumerate(items, 1):
        img = Image.open(img_path).convert("RGB")
        filename = os.path.basename(img_path)
        try:
            feat, _ = P.analyze_image(model, processor, device, img, filename, species=species)
        except Exception as e:
            print(f"  [ERR] {filename}: {e}")
            continue
        rows.append(feat)
        if i % 10 == 0:
            print(f"  ... {i}/{len(items)} ({time.time()-t0:.0f}s)")

    if not rows:
        print("[ERR] ไม่มีภาพผลลัพธ์"); return

    df = pd.DataFrame(rows)
    df["zero_mask"] = (df["total_area_px"] <= 0).astype(int)
    df.to_csv(os.path.join(args.out, "cross_species_per_image.csv"), index=False,
              encoding="utf-8-sig")

    # ---- สรุปต่อชนิด ----
    key_traits = ["total_area_px", "coverage_ratio", "height_proxy", "width_proxy",
                  "leaf_count", "shoot_count", "green_pct", "glare_score"]
    summary_rows = []
    for sp, g in df.groupby("species"):
        row = {"species": sp, "n": len(g)}
        for t in key_traits:
            row[f"{t}_mean"] = round(float(g[t].mean()), 3) if len(g) else None
            row[f"{t}_std"] = round(float(g[t].std()), 3) if len(g) > 1 else None
        row["zero_mask_rate"] = round(float(g["zero_mask"].mean()), 4)
        vc = g["verdict"].value_counts().to_dict()
        row["verdict_ready"] = vc.get("พร้อมอนุบาล", 0)
        row["verdict_not_ready"] = vc.get("ยังไม่พร้อม", 0)
        summary_rows.append(row)
    summary = pd.DataFrame(summary_rows).set_index("species")
    summary.to_csv(os.path.join(args.out, "cross_species_summary.csv"), encoding="utf-8-sig")

    print("\n=== สรุป cross-species (mean±std ต่อชนิด) ===")
    print(summary.to_string())

    # ---- Validation ต่อชนิด (ถ้ามี GT) ----
    if args.gt:
        gt = pd.read_csv(args.gt, encoding="utf-8-sig")
        gt["image"] = gt["image"].astype(str)
        df["image"] = df["image"].astype(str)
        m = df.merge(gt, on=["image", "species"] if "species" in gt.columns else "image",
                     how="inner", suffixes=("", "_gt"))
        print("\n=== Validation ต่อชนิด (เทียบค่าวัดมือ) ===")
        val_rows = []
        for sp, g in m.groupby("species"):
            r = {"species": sp, "n": len(g)}
            if "height_cm" in g.columns and g["height_cm"].notna().sum() >= 3:
                r["height_r_vs_manual"] = round(
                    pearson(g["height_proxy"], g["height_cm"]), 3)
            if "area_cm2" in g.columns and g["area_cm2"].notna().sum() >= 3:
                r["area_r_vs_manual"] = round(
                    pearson(g["total_area_px"], g["area_cm2"]), 3)
            if "expert_verdict" in g.columns:
                # generic READY_HEIGHT -> พร้อมอนุบาล (1) เทียบ expert_verdict == "พร้อมอนุบาล"
                pred = (g["height_proxy"] >= P.READY_HEIGHT).astype(int)
                exp = (g["expert_verdict"].astype(str) == "พร้อมอนุบาล").astype(int)
                acc, n = accuracy(exp, pred)
                r["generic_acc"] = round(acc, 3) if acc is not None else None
                r["n_acc"] = n
            val_rows.append(r)
        val_df = pd.DataFrame(val_rows).set_index("species")
        val_df.to_csv(os.path.join(args.out, "cross_species_validation.csv"),
                      encoding="utf-8-sig")
        print(val_df.to_string())

    # ---- กราฟเปรียบเทียบ ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        sp = summary.index.tolist()
        x = np.arange(len(sp))
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        axes[0].bar(x, summary["height_proxy_mean"], color="#1B5E20")
        axes[0].set_title("mean height_proxy")
        axes[0].set_xticks(x); axes[0].set_xticklabels(sp, rotation=30, ha="right")
        axes[1].bar(x, summary["total_area_px_mean"], color="#2E7D32")
        axes[1].set_title("mean total_area_px")
        axes[1].set_xticks(x); axes[1].set_xticklabels(sp, rotation=30, ha="right")
        axes[2].bar(x, summary["zero_mask_rate"], color="#C62828")
        axes[2].set_title("zero_mask_rate (lower better)")
        axes[2].set_xticks(x); axes[2].set_xticklabels(sp, rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "cross_species_compare.png"), dpi=150)
        print(f"\n[OK] บันทึกกราฟ: {os.path.join(args.out, 'cross_species_compare.png')}")
    except Exception as e:
        print(f"[WARN] กราฟไม่ได้: {e}")


if __name__ == "__main__":
    main()
