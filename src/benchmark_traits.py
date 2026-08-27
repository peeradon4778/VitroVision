"""Trait-level benchmark: เปรียบเทียบ proxy ของ "ขนาดต้น" ที่แต่ละวิธีได้จาก segmentation mask
ว่าตรงกับค่าที่วัดมือ (height_cm / area_cm2) แค่ไหน — วิธีที่ proxy ตรงกับมือมากสุด = ดีที่สุด

วิธีเทียบ:
  - sam3     : prompt-based PCS (plant/leaf/shoot/stem/root) จาก plant_growth_summary.csv
  - classical: HSV สีเขียว + morphology (pure classical, ไม่ใช้ ML)
  - yolo     : YOLO-seg COCO pretrain (ไม่มี class "plant") = naive reference เท่านั้น ต้อง fine-tune เพื่อใช้จริง

ความซื่อตรงที่ต้องรายงาน:
  - Pearson r เป็น scale-free -> เทียบ proxy (px) กับค่าวัดมือ (cm) ได้โดยไม่ต้อง calibrate หน่วย
  - classical/yolo ใช้ mask เดียว (ไม่ใช่ union ของหลาย prompt เหมือน SAM3) — ต่างนิยามโดยธรรมชาติ
  - ถ้า baseline segment ไม่เจอ (area=0 เพื่อ proxy=0) ถือเป็นความล้มเหลวจริง ไม่ตัดทิ้ง (กัน bias)
  - ยิ่งได้ r สูง + zero-rate ต่ำ = วัดขนาดต้นตามมือได้ดีกว่า

รัน (CPU ก็ได้):
    python src/benchmark_traits.py --data data/raw/20260814_batch \
        --sam3 data/processed/plant_growth_summary.csv \
        --gt data/processed/ground_truth.csv \
        --out data/processed/trait_benchmark --yolo-weights models/yolov8n-seg.pt
"""

import argparse
import glob
import os
import sys
import time

import cv2
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from benchmark_baselines import classical_green_seg  # noqa: E402
from calibrate_units import oof_cv  # noqa: E402  (ต่อยอด: คำนวณ MAE/RMSE หน่วย cm)


# ---------------------------------------------------------------- io helpers
def load_images(data_dir):
    exts = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
    files = []
    for e in exts:
        files += glob.glob(os.path.join(data_dir, e))
    return sorted(set(files))


def bbox_of(mask):
    """คืน (x, y, w, h) ของ bounding box โดยรอบ mask จริง ผ่าน nonzero scan"""
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    return (x0, y0, x1 - x0 + 1, y1 - y0 + 1)


def mask_to_traits(mask):
    """จาก binary mask -> area_px + normalized height/width proxy (เทียบความสูง/กว้างเต็มภาพ)"""
    area = int(mask.sum())
    H, W = mask.shape[:2]
    bb = bbox_of(mask)
    if bb is None:
        return {"area_px": 0, "h_proxy": 0.0, "w_proxy": 0.0}
    _, _, bw, bh = bb
    return {
        "area_px": area,
        "h_proxy": float(bh) / H,  # สัดส่วนความสูง (normalize ความสูงภาพ) — scale-free เทียบ cm
        "w_proxy": float(bw) / W,
    }


# ---------------------------------------------------------------- baselines
def yolo_traits(model, img, imgsz=640, conf=0.25):
    """YOLO-seg: union mask ของทุก class (COCO = reference) -> traits"""
    results = model.predict(img, conf=conf, verbose=False, imgsz=imgsz)
    H, W = img.shape[:2]
    union = np.zeros((H, W), dtype=bool)
    if results and results[0].masks is not None:
        masks = results[0].masks.data.cpu().numpy()
        for m in masks:
            m_bool = m > 0.5
            if m_bool.shape != (H, W):
                m_bool = cv2.resize(m_bool.astype(np.uint8), (W, H),
                                    interpolation=cv2.INTER_NEAREST).astype(bool)
            union |= m_bool
    return union


# ---------------------------------------------------------------- stats
def pearson(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) != len(y) or len(x) < 3:
        return {"r": None, "r2": None, "n": int(len(x))}
    mx, my = x.mean(), y.mean()
    num = float(((x - mx) * (y - my)).sum())
    dx = float(((x - mx) ** 2).sum())
    dy = float(((y - my) ** 2).sum())
    denom = (dx * dy) ** 0.5
    r = num / denom if denom > 0 else None
    return {"r": r, "r2": (r * r) if r is not None else None, "n": int(len(x))}


def main():
    ap = argparse.ArgumentParser(description="Trait-level benchmark เทียบค่าวัดมือ (scale-free)")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพ")
    ap.add_argument("--sam3", required=True, help="plant_growth_summary.csv (ผล SAM3)")
    ap.add_argument("--gt", required=True, help="ground_truth.csv (ค่าวัดมือ)")
    ap.add_argument("--out", default="data/processed/trait_benchmark", help="โฟลเดอร์ผลลัพธ์")
    ap.add_argument("--yolo-weights", default="models/yolov8n-seg.pt")
    ap.add_argument("--method", default="classical,yolo", help="baselines ที่รัน (classical,yolo)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    import pandas as _pd  # noqa

    # ---- โหลดผล SAM3 + ค่าวัดมือ ----
    sam3 = pd.read_csv(args.sam3, encoding="utf-8-sig")
    gt = pd.read_csv(args.gt, encoding="utf-8-sig")
    sam3 = sam3[["image", "total_area_px", "height_proxy", "width_proxy"]].copy()
    gt = gt[["image", "height_cm", "width_cm", "area_cm2", "expert_verdict"]].copy()

    # ---- โหลด YOLO ถ้าเลือก ----
    yolo_model = None
    if "yolo" in args.method:
        from ultralytics import YOLO
        yolo_model = YOLO(args.yolo_weights)

    images = load_images(args.data)
    print(f"[INFO] ภาพ {len(images)} · วิธี baseline: {args.method}")

    rows = []
    t_start = time.time()
    for i, img_path in enumerate(images, 1):
        name = os.path.basename(img_path)
        img = cv2.imread(img_path)
        if img is None:
            continue
        item = {"image": name}
        if "classical" in args.method:
            t0 = time.time()
            mask = classical_green_seg(img)
            t = time.time() - t0
            tr = mask_to_traits(mask)
            item["classical_area_px"] = tr["area_px"]
            item["classical_h_proxy"] = round(tr["h_proxy"], 6)
            item["classical_w_proxy"] = round(tr["w_proxy"], 6)
            item["classical_runtime"] = round(t, 3)
        if "yolo" in args.method:
            t0 = time.time()
            mask = yolo_traits(yolo_model, img)
            t = time.time() - t0
            tr = mask_to_traits(mask)
            item["yolo_area_px"] = tr["area_px"]
            item["yolo_h_proxy"] = round(tr["h_proxy"], 6)
            item["yolo_w_proxy"] = round(tr["w_proxy"], 6)
            item["yolo_runtime"] = round(t, 3)
        rows.append(item)
        if i % 20 == 0:
            print(f"  ... {i}/{len(images)}  ({time.time()-t_start:.0f}s)")

    traits = pd.DataFrame(rows)
    # ---- ผสาน SAM3 + GT ----
    merged = traits.merge(sam3, on="image", how="left").merge(gt, on="image", how="left")
    merged.to_csv(os.path.join(args.out, "trait_benchmark_merged.csv"), index=False,
                  encoding="utf-8-sig")

    # ---- คำนวณ correlation ต่อวิธี ----
    # proxy ความสูง -> ช่อง h_proxy ของแต่ละวิธี เปรียบเทียบกับ height_cm (scale-free)
    method_h = {
        "sam3": ("height_proxy", "height_cm"),
        "classical": ("classical_h_proxy", "height_cm"),
        "yolo": ("yolo_h_proxy", "height_cm"),
    }
    method_area = {
        "sam3": ("total_area_px", "area_cm2"),
        "classical": ("classical_area_px", "area_cm2"),
        "yolo": ("yolo_area_px", "area_cm2"),
    }

    summary = []
    for name, (proxy, target) in method_h.items():
        if proxy not in merged.columns:
            continue
        sub = merged[merged[proxy].notna() & merged[target].notna()]
        stat = pearson(sub[proxy], sub[target])
        zero_rate = float((merged[proxy].fillna(0) <= 0).mean()) if proxy in merged else None
        runtime = merged.get(name + "_runtime")
        summary.append({
            "method": name, "metric": "height (proxy vs height_cm)",
            "n": stat["n"], "pearson_r": stat["r"], "r2": stat["r2"],
            "zero_mask_rate": round(zero_rate, 4) if zero_rate is not None else None,
            "mean_runtime_s": round(float(runtime.mean()), 3) if runtime is not None else None,
        })
    for name, (proxy, target) in method_area.items():
        if proxy not in merged.columns:
            continue
        sub = merged[merged[proxy].notna() & merged[target].notna()]
        stat = pearson(sub[proxy], sub[target])
        zero_rate = float((merged[proxy].fillna(0) <= 0).mean()) if proxy in merged else None
        runtime = merged.get(name + "_runtime")
        summary.append({
            "method": name, "metric": "area (proxy px vs area_cm2)",
            "n": stat["n"], "pearson_r": stat["r"], "r2": stat["r2"],
            "zero_mask_rate": round(zero_rate, 4) if zero_rate is not None else None,
            "mean_runtime_s": round(float(runtime.mean()), 3) if runtime is not None else None,
        })

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(os.path.join(args.out, "trait_benchmark_summary.csv"), index=False,
                      encoding="utf-8-sig")

    print("\n=== สรุป trait-level benchmark (Pearson r เทียบค่าวัดมือ) ===")
    print(summary_df.to_string(index=False))
    print("\n[INFO] r เป็น scale-free (px vs cm เทียบได้โดยไม่ calibrate)")
    print("[INFO] zero_mask_rate = สัดส่วนภาพที่วิธีนั้น segment ไม่เจอ (proxy=0)")

    # ---- ต่อยอด: Calibrated height MAE/RMSE (cm) ต่อวิธี — calibrate proxy->cm แล้ววัดความคลาดเคลื่อน ----
    calib_rows = []
    for name, (proxy, target) in method_h.items():
        if proxy not in merged.columns:
            continue
        sub = merged[merged[proxy].notna() & merged[target].notna()]
        if len(sub) < 3:
            continue
        # calibrate proxy->cm (มี intercept — สะท้อนว่า proxy วัดจากขวดไม่ใช่โคน)
        r = oof_cv(sub[proxy], sub[target], k_folds=5, intercept=True)
        calib_rows.append({
            "method": name, "metric": "height MAE/RMSE (cm, calibrated)",
            "n": r["n"], "k": round(r["k"], 3), "b": round(r["b"], 3),
            "cv_mae_cm": round(r["mae"], 3), "cv_rmse_cm": round(r["rmse"], 3),
            "r2_oof": round(r["r2"], 3),
        })
    calib_df = pd.DataFrame(calib_rows)
    if len(calib_df):
        calib_df.to_csv(os.path.join(args.out, "trait_benchmark_height_error_cm.csv"),
                        index=False, encoding="utf-8-sig")
        print("\n=== ต่อยอด: Calibrated height error (cm) — ยิ่ง MAE/RMSE ต่ำ = วัดขนาดต้นใกล้มือสุด ===")
        print(calib_df.to_string(index=False))
        print("[INFO] k,b = proxy->cm (มี intercept) · MAE/RMSE จาก cross-validation")


    # ---- กราฟ scatter height: proxy vs manual height_cm ต่อวิธี (label ภาษาอังกฤษกันกล่อง) ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
        colors = {"sam3": "#1B5E20", "classical": "#C62828", "yolo": "#EF6C00"}
        for ax, (name, (proxy, target)) in zip(axes, method_h.items()):
            if proxy not in merged.columns:
                continue
            sub = merged[merged[proxy].notna() & merged[target].notna()]
            ax.scatter(sub[target], sub[proxy], s=18, alpha=0.7, color=colors[name])
            stat = pearson(sub[proxy], sub[target])
            ax.set_title(f"{name}   (r={stat['r']:.3f}, n={stat['n']})")
            ax.set_xlabel("manual height (cm)"); ax.set_ylabel("proxy height")
            ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "height_correlation.png"), dpi=150)

        # ---- bar chart เปรียบเทียบ r ข้ามวิธี (height + area) ----
        fig2, ax2 = plt.subplots(figsize=(8, 4.5))
        order = ["sam3", "classical", "yolo"]
        x = np.arange(len(order))
        w = 0.38
        heights_r = []
        areas_r = []
        for m in order:
            hrow = summary_df[(summary_df.method == m) & summary_df.metric.str.startswith("height")]
            arow = summary_df[(summary_df.method == m) & summary_df.metric.str.startswith("area")]
            heights_r.append(hrow.pearson_r.iloc[0] if len(hrow) else float("nan"))
            areas_r.append(arow.pearson_r.iloc[0] if len(arow) else float("nan"))
        ax2.bar(x - w / 2, heights_r, w, color=colors["sam3"], label="height proxy vs manual height")
        ax2.bar(x + w / 2, areas_r, w, color=colors["yolo"], label="area proxy vs manual area")
        ax2.set_xticks(x); ax2.set_xticklabels(order)
        ax2.set_ylabel("Pearson r"); ax2.set_ylim(0, 0.75)
        ax2.set_title("Trait-level agreement with manual measurement")
        for xi, (h, a) in enumerate(zip(heights_r, areas_r)):
            if not np.isnan(h):
                ax2.text(xi - w / 2, h + 0.02, f"{h:.2f}", ha="center", fontsize=9)
            if not np.isnan(a):
                ax2.text(xi + w / 2, a + 0.02, f"{a:.2f}", ha="center", fontsize=9)
        ax2.legend(); ax2.grid(alpha=0.3, axis="y")
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "trait_compare_bar.png"), dpi=150)

        # ---- bar chart calibrated height MAE/RMSE (cm) ต่อวิธี — ยิ่งต่ำยิ่งดี ----
        if len(calib_df):
            fig3, ax3 = plt.subplots(figsize=(8, 4.5))
            x3 = np.arange(len(calib_df))
            maes = calib_df["cv_mae_cm"].astype(float)
            rmses = calib_df["cv_rmse_cm"].astype(float)
            ax3.bar(x3 - w / 2, maes, w, color=colors["sam3"], label="calibrated MAE (cm)")
            ax3.bar(x3 + w / 2, rmses, w, color=colors["yolo"], label="calibrated RMSE (cm)")
            ax3.set_xticks(x3); ax3.set_xticklabels(calib_df["method"])
            ax3.set_ylabel("height error (cm)"); ax3.set_title("Calibrated height error per method (lower better)")
            for xi, (ma, rm) in enumerate(zip(maes, rmses)):
                ax3.text(xi - w / 2, ma + 0.02, f"{ma:.2f}", ha="center", fontsize=8)
                ax3.text(xi + w / 2, rm + 0.02, f"{rm:.2f}", ha="center", fontsize=8)
            ax3.legend(); ax3.grid(alpha=0.3, axis="y")
            plt.tight_layout()
            plt.savefig(os.path.join(args.out, "height_error_cm_bar.png"), dpi=150)
        print(f"[OK] กราฟ: height_correlation.png + trait_compare_bar.png + height_error_cm_bar.png")
    except Exception as e:
        print(f"[WARN] กราฟไม่ได้: {e}")


if __name__ == "__main__":
    main()
