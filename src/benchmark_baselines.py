"""Benchmark: เปรียบเทียบ segmentation ของวิธี baseline กับ ground truth masks.

รันบนเครื่อง/Colab แบบ headless batch:
    python benchmark_baselines.py --data <โฟลเดอร์ภาพ> --gt <โฟลเดอร์ GT masks> --out <ผลลัพธ์> \
        [--baselines classical,sam2,yolo] [--yolo-weights models/yolov8n-seg.pt] \
        [--sam2-checkpoint sam2.1_hiera_large.pt] [--device cpu|gpu]

วิธี baseline ที่รองรับ:
  - classical : การแบ่งส่วนเชิงคลาสสิก (HSV สีเขียว + morphology) — รันได้ทันที CPU
  - sam2      : SAM2 automatic masks (facebook/sam2.1) — ต้องติดตั้ง sam2 + checkpoint
  - yolo      : YOLO-seg (ultralytics) — ใช้ weights ที่เทรนเอง/ปรับแล้ว (COCO pretrained ไม่มี class "plant")

ground truth masks: โฟลเดอร์ --gt ที่มีไฟล์ <ชื่อภาพ>.png (binary: ขาว = พืช)
ผลลัพธ์: benchmark_summary.csv (IoU/Dice/Precision/Recall/F1 ต่อภาพ) + สรุป mean±std ต่อ baseline

อ้างอิง: proposal 7.6.1 — เกณฑ์เปรียบเทียบตาม Orvati Nia et al. (2026)
"""

import argparse
import glob
import os
import time

import cv2
import numpy as np
import pandas as pd

# ---- SAM2 (optional — Colab ต้องติดตั้ง: pip install sam2 + download checkpoint) ----
try:
    from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator
    from sam2.build_sam import build_sam2

    SAM2_AVAILABLE = True
except ImportError:
    SAM2_AVAILABLE = False

# ---- YOLO-seg (optional) ----
try:
    from ultralytics import YOLO

    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False


# ---------------------------------------------------------------- utilities
def load_images(data_dir):
    """โหลด path ภาพทั้งหมด (.jpg/.jpeg/.png) เรียงตามชื่อ — กันซ้ำบน Windows (case-insensitive glob)"""
    exts = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
    files = []
    for e in exts:
        files += glob.glob(os.path.join(data_dir, e))
    return sorted(set(files))


def load_gt_mask(gt_dir, image_path):
    """โหลด binary GT mask: <ชื่อภาพ>.png ใน gt_dir (ขาว = พืช)"""
    name = os.path.splitext(os.path.basename(image_path))[0]
    gt_path = os.path.join(gt_dir, name + ".png")
    if not os.path.exists(gt_path):
        return None
    gt = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)
    return (gt > 127)


def compute_metrics(pred, gt):
    """IoU, Dice, precision, recall, F1 ที่ระดับพิกเซล (pred/gt เป็น bool mask)"""
    inter = float(np.logical_and(pred, gt).sum())
    union = float(np.logical_or(pred, gt).sum())
    iou = inter / union if union > 0 else float("nan")
    dice = 2 * inter / (pred.sum() + gt.sum()) if (pred.sum() + gt.sum()) > 0 else float("nan")
    tp = inter
    fp = float(np.logical_and(pred, ~gt).sum())
    fn = float(np.logical_and(~pred, gt).sum())
    prec = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
    rec = tp / (tp + fn) if (tp + fn) > 0 else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else float("nan")
    return {"iou": iou, "dice": dice, "precision": prec, "recall": rec, "f1": f1}


def resize_to_gt(pred, gt_shape):
    """ปรับ pred mask ให้ขนาดเดียวกับ GT (กรณีขนาดต่างกัน)"""
    if pred.shape != gt_shape:
        pred = cv2.resize(pred.astype(np.uint8), (gt_shape[1], gt_shape[0]),
                          interpolation=cv2.INTER_NEAREST).astype(bool)
    return pred


# ---------------------------------------------------------------- baselines
def classical_green_seg(img, low_h=35, high_h=85, min_s=0.30, min_v=0.25,
                        min_area_frac=0.002):
    """การแบ่งส่วนเชิงคลาสสิก: HSV สีเขียว + morphology cleanup.
    ใช้เป็น baseline ที่ไม่ต้อง train/ไม่ต้องใช้ ML"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (low_h, int(min_s * 255), int(min_v * 255)),
                       (high_h, 255, 255))
    # morphology: เปิด-ปิด กำจัดจุดเล็ก/เชื่อมชิ้นใกล้
    k = max(3, img.shape[0] // 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # กันชิ้นเล็กเกินไป (สัญญาณรบกวน)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    min_area = min_area_frac * img.shape[0] * img.shape[1]
    keep = np.zeros_like(mask)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            keep[lab == i] = 255
    return keep.astype(bool)


def sam2_autoseg(model, image_np, pred_iou_thresh=0.6, stability_score_thresh=0.8):
    """SAM2 automatic mask generator — เลือก mask ที่มีพื้นที่ใหญ่สุด (สมมติ plant ใหญ่สุดในเฟรม)
    หมายเหตุ: เป็น automatic (no text prompt) — รายงานผลพร้อมข้อจำกัดนี้"""
    gen = SAM2AutomaticMaskGenerator(
        model,
        pred_iou_thresh=pred_iou_thresh,
        stability_score_thresh=stability_score_thresh,
        points_per_side=32,
        min_mask_region_area=500,
    )
    masks = gen.generate(image_np)
    if not masks:
        return np.zeros(image_np.shape[:2], dtype=bool)
    # เลือก mask ที่ใหญ่สุด
    best = max(masks, key=lambda m: m["area"])
    return best["segmentation"].astype(bool)


def yolo_seg(model, image_np, class_ids=None, conf=0.25, imgsz=640):
    """YOLO-seg — รวม masks ของ class ที่ระบุ (--yolo-classes)
    ถ้า class_ids=None ใช้ทุก class (รายงานเป็น reference)
    masks ที่ได้มีขนาด imgsz — resize กลับเป็นขนาดภาพต้นฉบับ"""
    results = model.predict(image_np, conf=conf, verbose=False, imgsz=imgsz)
    H, W = image_np.shape[:2]
    union = np.zeros((H, W), dtype=bool)
    if not results or results[0].masks is None:
        return union
    masks = results[0].masks.data.cpu().numpy()  # (N, imgsz, imgsz) float 0-1
    classes = results[0].boxes.cls.cpu().numpy().astype(int)
    for m, c in zip(masks, classes):
        if class_ids is None or int(c) in class_ids:
            m_bool = (m > 0.5)
            if m_bool.shape != (H, W):
                m_bool = cv2.resize(m_bool.astype(np.uint8), (W, H),
                                    interpolation=cv2.INTER_NEAREST).astype(bool)
            union |= m_bool
    return union


# ---------------------------------------------------------------- runners
def run_baseline(name, img, model_ctx):
    """รัน baseline หนึ่งวิธี กับภาพเดียว คืน binary mask"""
    if name == "classical":
        return classical_green_seg(img)
    if name == "sam2":
        return sam2_autoseg(model_ctx["sam2_model"], cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if name == "yolo":
        return yolo_seg(model_ctx["yolo_model"], img, class_ids=model_ctx["yolo_classes"])
    raise ValueError(f"ไม่รู้จัก baseline: {name}")


def main():
    ap = argparse.ArgumentParser(description="Benchmark baselines เทียบ ground truth masks")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพ")
    ap.add_argument("--gt", default=None, help="โฟลเดอร์ GT masks (<ชื่อภาพ>.png, ขาว=พืช)")
    ap.add_argument("--out", default="benchmark_results", help="โฟลเดอร์ผลลัพธ์")
    ap.add_argument("--baselines", default="classical,sam2,yolo",
                    help="baseline ที่รัน คั่นด้วย , (classical, sam2, yolo)")
    ap.add_argument("--yolo-weights", default="models/yolov8n-seg.pt", help="weights YOLO-seg")
    ap.add_argument("--yolo-classes", default=None,
                    help="class IDs ให้รวม (คั่น ,) — default: ทุก class (reference)")
    ap.add_argument("--sam2-checkpoint", default="sam2.1_hiera_large.pt",
                    help="path checkpoint SAM2 (Colab: ดาวน์โหลดจาก facebook)")
    ap.add_argument("--sam2-config", default="configs/sam2.1/sam2.1_hiera_l.yaml",
                    help="config SAM2 (เทียบกับ checkpoint)")
    ap.add_argument("--device", default="cpu", choices=["cpu", "gpu"], help="device")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    baselines = [b.strip() for b in args.baselines.split(",") if b.strip()]

    device = "cuda" if (args.device == "gpu" and __import__("torch").cuda.is_available()) else "cpu"

    # ---- โหลดโมเดลตามที่เลือก ----
    model_ctx = {}
    if "sam2" in baselines:
        if not SAM2_AVAILABLE:
            print("[WARN] sam2 ไม่พร้อมใช้งาน — ข้าม (Colab: pip install sam2 + checkpoint)")
            baselines.remove("sam2")
        else:
            import torch
            from hydra import initialize_config_dir  # sam2 ใช้ hydra config
            print(f"[INFO] โหลด SAM2 checkpoint: {args.sam2_checkpoint} (device={device})")
            cfg_dir = os.path.join(os.path.dirname(__import__("sam2").__file__), "configs", "sam2.1")
            with initialize_config_dir(config_dir=cfg_dir):
                model = build_sam2(args.sam2_config, args.sam2_checkpoint, device=device)
            model_ctx["sam2_model"] = model
    if "yolo" in baselines:
        if not YOLO_AVAILABLE:
            print("[WARN] ultralytics ไม่พร้อม — ข้าม")
            baselines.remove("yolo")
        else:
            print(f"[INFO] โหลด YOLO-seg: {args.yolo_weights}")
            model_ctx["yolo_model"] = YOLO(args.yolo_weights)
            model_ctx["yolo_classes"] = ([int(x) for x in args.yolo_classes.split(",")]
                                         if args.yolo_classes else None)

    images = load_images(args.data)
    print(f"[INFO] ภาพ {len(images)} ไฟล์ · baselines: {baselines}")

    rows = []
    for i, img_path in enumerate(images, 1):
        img = cv2.imread(img_path)
        if img is None:
            continue
        gt = load_gt_mask(args.gt, img_path) if args.gt else None
        for b in baselines:
            t0 = time.time()
            pred = run_baseline(b, img, model_ctx)
            elapsed = time.time() - t0
            row = {"image": os.path.basename(img_path), "baseline": b,
                   "runtime_s": round(elapsed, 2), "pred_area_px": int(pred.sum())}
            if gt is not None:
                pred = resize_to_gt(pred, gt.shape)
                row.update(compute_metrics(pred, gt))
            rows.append(row)
        if i % 20 == 0:
            print(f"  ... {i}/{len(images)} ภาพ")

    df = pd.DataFrame(rows)
    out_csv = os.path.join(args.out, "benchmark_summary.csv")
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"\n[OK] บันทึก {out_csv}")

    # ---- สรุป mean ± std ต่อ baseline ----
    if args.gt and "iou" in df.columns:
        summary = df.groupby("baseline")[["iou", "dice", "precision", "recall", "f1"]].agg(
            ["mean", "std"]).round(4)
        summary.columns = ["_".join(c) for c in summary.columns]
        summary.to_csv(os.path.join(args.out, "benchmark_summary_stats.csv"),
                       encoding="utf-8-sig")
        print("\n=== สรุป mIoU/Dice/F1 ต่อ baseline (mean±std) ===")
        print(summary.to_string())
    else:
        print("\n[INFO] ไม่มี GT masks — รายงานเฉพาะ runtime/พื้นที่ (ใส่ --gt เพื่อคำนวณ mIoU/Dice)")


if __name__ == "__main__":
    main()
