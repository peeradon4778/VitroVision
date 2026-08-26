"""Benchmark เต็มรูปแบบบน Google Colab (GPU):
เปรียบเทียบ segmentation ของ 4 วิธี (classical / YOLO-seg / SAM2 / SAM3 PCS)
กับ ground truth masks (mIoU, Dice, precision, recall, F1)

รัน:
    python benchmark_colab.py --data /content/data --gt /content/gt_masks \
        --out /content/bench --hf-token <TOKEN> \
        [--baselines classical,yolo,sam2,sam3] [--img-size 1024]

ข้อกำหนด (Colab):
- GPU (T4 ขึ้นไป) — SAM3 ไม่รองรับ CPU
- HF_TOKEN ที่มี access ถึง facebook/sam3
- ติดตั้ง: pip install sam2 hydra-core ultralytics transformers>=4.55
- GT masks: โฟลเดอร์ --gt ที่มี <ชื่อภาพ>.png (binary, ขาว = พืช)

ผลลัพธ์:
- benchmark_summary.csv — metric รายภาพ/รายวิธี
- benchmark_summary_stats.csv — mean±std ต่อวิธี
- benchmark_compare.png — bar chart เปรียบเทียบ mIoU/Dice/F1
"""

import argparse
import os
import sys
import time

import cv2
import numpy as np
import pandas as pd
import torch

sys.path.insert(0, os.path.dirname(__file__))
from benchmark_baselines import (classical_green_seg, compute_metrics, load_gt_mask,
                                 load_images, resize_to_gt, yolo_seg)

# ---- SAM2 (Colab: pip install sam2 + ดาวน์โหลด checkpoint) ----
try:
    from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator
    from sam2.build_sam import build_sam2
    from hydra import initialize_config_dir
    import sam2 as sam2_pkg
    SAM2_AVAILABLE = True
except ImportError:
    SAM2_AVAILABLE = False

SAM3_PROMPTS = ["plant", "leaf"]  # union — เทียบกับ GT "plant"


# ---------------------------------------------------------------- SAM3
def load_sam3(device):
    from transformers import Sam3Processor, Sam3Model
    model = Sam3Model.from_pretrained("facebook/sam3").to(device)
    processor = Sam3Processor.from_pretrained("facebook/sam3")
    return model, processor


def sam3_plant_mask(model, processor, device, img_rgb, prompts=SAM3_PROMPTS,
                    score_thr=0.5, mask_thr=0.5):
    """รวม mask ของพรอมป์ (plant+leaf) จาก SAM3 PCS → union bool mask"""
    from PIL import Image
    pil = Image.fromarray(img_rgb)
    union = np.zeros(img_rgb.shape[:2], dtype=bool)
    for p in prompts:
        inputs = processor(images=pil, text=p, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        result = processor.post_process_instance_segmentation(
            outputs, threshold=score_thr, mask_threshold=mask_thr,
            target_sizes=inputs.get("original_sizes").tolist())[0]
        masks = result["masks"]
        if hasattr(masks, "cpu"):
            masks = masks.cpu()
        masks = np.asarray(masks).astype(bool)
        if masks.ndim == 3 and masks.shape[0] > 0:
            union |= masks.any(axis=0)
    return union


# ---------------------------------------------------------------- SAM2
def load_sam2(device, checkpoint, config_name="sam2.1_hiera_l.yaml"):
    cfg_dir = os.path.join(os.path.dirname(sam2_pkg.__file__), "configs", "sam2.1")
    with initialize_config_dir(config_dir=cfg_dir):
        model = build_sam2(config_name, checkpoint, device=device)
    return model


def sam2_autoseg(model, img_rgb, pred_iou_thresh=0.6, stability_score_thresh=0.8):
    gen = SAM2AutomaticMaskGenerator(
        model, pred_iou_thresh=pred_iou_thresh,
        stability_score_thresh=stability_score_thresh,
        points_per_side=32, min_mask_region_area=500)
    masks = gen.generate(img_rgb)
    if not masks:
        return np.zeros(img_rgb.shape[:2], dtype=bool)
    best = max(masks, key=lambda m: m["area"])
    return best["segmentation"].astype(bool)


# ---------------------------------------------------------------- runner
def run_all(image_path, methods, ctx):
    """รันทุกวิธีกับภาพเดียว คืน dict {method: mask}"""
    img = cv2.imread(image_path)
    H, W = img.shape[:2]
    # resize ลดความละเอียด (Colab GPU + consistency)
    if ctx["img_size"] and max(H, W) > ctx["img_size"]:
        scale = ctx["img_size"] / max(H, W)
        img = cv2.resize(img, (int(W * scale), int(H * scale)),
                         interpolation=cv2.INTER_AREA)
    out = {}
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for m in methods:
        t0 = time.time()
        if m == "classical":
            out[m] = classical_green_seg(img)
        elif m == "yolo":
            out[m] = yolo_seg(ctx["yolo_model"], img)
        elif m == "sam2":
            out[m] = sam2_autoseg(ctx["sam2_model"], img_rgb)
        elif m == "sam3":
            out[m] = sam3_plant_mask(ctx["sam3_model"], ctx["sam3_processor"],
                                     ctx["device"], img_rgb)
        out[m + "_runtime"] = time.time() - t0
    out["_image_path"] = image_path
    return out


def main():
    ap = argparse.ArgumentParser(description="Benchmark เต็มบน Colab (4 วิธี เทียบ GT)")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพ")
    ap.add_argument("--gt", default=None, help="โฟลเดอร์ GT masks (<ชื่อภาพ>.png)")
    ap.add_argument("--out", default="/content/bench", help="โฟลเดอร์ผลลัพธ์")
    ap.add_argument("--baselines", default="classical,yolo,sam2,sam3")
    ap.add_argument("--hf-token", default=None, help="HF_TOKEN (SAM3 gated)")
    ap.add_argument("--sam2-checkpoint", default="sam2.1_hiera_large.pt",
                    help="path checkpoint SAM2 (ต้องดาวน์โหลดก่อน)")
    ap.add_argument("--yolo-weights", default="models/yolov8n-seg.pt",
                    help="weights YOLO-seg (COCO = reference เท่านั้น ต้อง fine-tune เพื่อใช้จริง)")
    ap.add_argument("--yolo-classes", default=None, help="class IDs (คั่น ,) — default ทุก class")
    ap.add_argument("--img-size", type=int, default=1024, help="resize ด้านยาว max (0 = ไม่ resize)")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] device: {device}")
    if "sam3" in args.baselines and device == "cpu":
        raise SystemExit("SAM3 ไม่รองรับ CPU — ต้องรันบน Colab GPU")

    if args.hf_token:
        from huggingface_hub import login
        login(token=args.hf_token, add_to_git_credential=False)

    methods = [m.strip() for m in args.baselines.split(",") if m.strip()]
    os.makedirs(args.out, exist_ok=True)

    ctx = {"device": device, "img_size": args.img_size, "yolo_model": None,
           "sam2_model": None, "sam3_model": None, "sam3_processor": None}

    # ---- โหลดโมเดล ----
    if "yolo" in methods:
        from ultralytics import YOLO
        print(f"[INFO] โหลด YOLO-seg: {args.yolo_weights} (COCO = reference)")
        ctx["yolo_model"] = YOLO(args.yolo_weights)
        ctx["yolo_classes"] = ([int(x) for x in args.yolo_classes.split(",")]
                               if args.yolo_classes else None)
    if "sam2" in methods:
        if not SAM2_AVAILABLE:
            raise SystemExit("sam2 ไม่พร้อม — รัน: pip install sam2 hydra-core")
        print(f"[INFO] โหลด SAM2: {args.sam2_checkpoint}")
        ctx["sam2_model"] = load_sam2(device, args.sam2_checkpoint)
    if "sam3" in methods:
        print("[INFO] โหลด SAM3 (facebook/sam3) — ใช้เวลาหลายนาที")
        ctx["sam3_model"], ctx["sam3_processor"] = load_sam3(device)

    images = load_images(args.data)
    print(f"[INFO] ภาพ {len(images)} · วิธี: {methods}")

    rows = []
    for i, img_path in enumerate(images, 1):
        res = run_all(img_path, methods, ctx)
        name = os.path.basename(res["_image_path"])
        gt = load_gt_mask(args.gt, res["_image_path"]) if args.gt else None
        for m in methods:
            row = {"image": name, "baseline": m,
                   "runtime_s": round(res[m + "_runtime"], 2),
                   "pred_area_px": int(res[m].sum())}
            if gt is not None:
                pred = resize_to_gt(res[m], gt.shape)
                row.update(compute_metrics(pred, gt))
            rows.append(row)
        if i % 10 == 0:
            print(f"  ... {i}/{len(images)}")

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(args.out, "benchmark_summary.csv"), index=False,
              encoding="utf-8-sig")
    print(f"[OK] บันทึก benchmark_summary.csv ({len(df)} แถว)")

    if args.gt and "iou" in df.columns:
        summary = df.groupby("baseline")[["iou", "dice", "precision", "recall", "f1"]] \
            .agg(["mean", "std"]).round(4)
        summary.columns = ["_".join(c) for c in summary.columns]
        summary.to_csv(os.path.join(args.out, "benchmark_summary_stats.csv"),
                       encoding="utf-8-sig")
        print("\n=== สรุป mean±std ต่อวิธี ===")
        print(summary.to_string())
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(1, 3, figsize=(14, 4))
            for ax, metric in zip(axes, ["iou", "dice", "f1"]):
                means = summary[f"{metric}_mean"]
                stds = summary[f"{metric}_std"]
                ax.bar(means.index, means, yerr=stds, capsize=4,
                       color=["#1B5E20", "#C62828", "#EF6C00", "#4057B2"])
                ax.set_title(f"{metric.upper()} (mean±std)")
                ax.set_ylim(0, 1)
                for xi, (m, s) in enumerate(zip(means, stds)):
                    ax.text(xi, m + s + 0.03, f"{m:.3f}", ha="center", fontsize=9)
            plt.tight_layout()
            plt.savefig(os.path.join(args.out, "benchmark_compare.png"), dpi=150)
            print(f"[OK] บันทึก benchmark_compare.png")
        except Exception as e:
            print(f"[WARN] สร้างกราฟไม่ได้: {e}")
    else:
        print("[INFO] ไม่มี GT masks — รายงาน runtime/พื้นที่ (ใส่ --gt เพื่อ mIoU/Dice)")


if __name__ == "__main__":
    main()
