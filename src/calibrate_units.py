"""Calibrate หน่วย cm — เปลี่ยน proxy (px) ที่ SAM3 วัดได้ให้เป็นเซนติเมตรจริง + คำนวณ MAE/RMSE

สองวิธี:
  1) เชิงประจักษ์ (ทำเลย) — fit mapping proxy->cm จากค่าวัดมือ (ground_truth height_cm/area_cm2)
     ให้ K เช่น canopy_h_cm = K * height_proxy แล้วรายงาน MAE/RMSE แบบ cross-validated (out-of-fold)
  2) เชิงเรขาคณิต (ต้องมีขนาดขวดจริง) — PIXEL_TO_CM = ขวดกว้างจริง(cm) / ขวดกว้าง(px) ตาม CALIBRATION_GUIDE
     ใส่ลง config.json ได้เมื่อมีค่าจริง

รัน (CPU):
    python src/calibrate_units.py --summary data/processed/plant_growth_summary.csv \
        --gt data/processed/ground_truth.csv --out data/processed/calibration

ผลลัพธ์:
  - calibration_summary.csv   (K, R2, CV_MAE, CV_RMSE ต่อ trait)
  - calibrated_canopy.csv     (แถวต่อภาพ: canopy_h_cm, canopy_w_cm, canopy_area_cm2)
  - calibration_fit.png       (scatter proxy vs มือ + เส้น fit)

หมายเหตุความซื่อตรง:
  - K ที่ได้คือ factor รวม (roi_h * PIXEL_TO_CM) ของชุดภาพนี้ — เปลี่ยนมุม/ระยะ/ชนิด ต้อง recalibrate
  - MAE/RMSE รายงานจาก cross-validation (out-of-fold) จึงไม่ optimistic ไม่ in-sample
  - เชิงเรขาคณิตที่แท้จริง (PIXEL_TO_CM raw px) ต้องใช้ขนาดขวดจริง + ตรวจจับขวด — ดู 2)
"""

import argparse
import os

import numpy as np
import pandas as pd


# ---------------------------------------------------------------- CV regression
# ฟังก์ชัน CV แบบ out-of-fold (ซื่อตรง ไม่ in-sample): รองรับผ่าน origin และ OLS with-intercept
def oof_cv(x, y, k_folds=5, seed=42, intercept=True):
    """Fit (k, b) = y ~ k*x (+ b ถ้า intercept) บน train folds → pred out-of-fold
    คืน k, b, MAE, RMSE, R2(OOF)"""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < k_folds:
        k_folds = max(2, n)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    folds = np.array_split(idx, k_folds)
    oof = np.full(n, np.nan)
    ks, bs = [], []
    for fold in folds:
        tr = np.setdiff1d(np.arange(n), fold)
        x_tr, y_tr = x[tr], y[tr]
        if intercept:
            A = np.column_stack([x_tr, np.ones(len(x_tr))])
            coef, *_ = np.linalg.lstsq(A, y_tr, rcond=None)
            k, b = float(coef[0]), float(coef[1])
        else:
            k = float((x_tr * y_tr).sum() / (x_tr * x_tr).sum()) if (x_tr * x_tr).sum() > 0 else 0.0
            b = 0.0
        ks.append(k); bs.append(b)
        oof[fold] = k * x[fold] + b
    # full-data fit (สำหรับใช้ convert จริง)
    if intercept:
        A = np.column_stack([x, np.ones(len(x))])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        k, b = float(coef[0]), float(coef[1])
    else:
        k = float((x * y).sum() / (x * x).sum()) if (x * x).sum() > 0 else 0.0
        b = 0.0
    mae = float(np.mean(np.abs(oof - y)))
    rmse = float(np.sqrt(np.mean((oof - y) ** 2)))
    ss_res = float(((y - oof) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return {"k": k, "b": b, "mae": mae, "rmse": rmse, "r2": r2, "n": n, "oof": oof}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True, help="plant_growth_summary.csv")
    ap.add_argument("--gt", required=True, help="ground_truth.csv")
    ap.add_argument("--out", default="data/processed/calibration")
    ap.add_argument("--folds", type=int, default=5)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    sm = pd.read_csv(args.summary, encoding="utf-8-sig")
    gt = pd.read_csv(args.gt, encoding="utf-8-sig")
    m = sm.merge(gt, on="image", how="inner")

    # ---- คำนวณ calibration ต่อ trait (เลือกแบบ CV RMSE ดีกว่า) ----
    def fit_trait(proxy, target, folds):
        if proxy is None or target is None or len(target) < 3:
            return None
        best = None
        for inter in (True, False):
            r = oof_cv(proxy, target, folds, intercept=inter)
            if best is None or r["rmse"] < best["rmse"]:
                best = r
                best["model"] = "intercept" if inter else "origin"
        return best

    rows = []
    pairs = [
        ("canopy_h_cm", m["height_proxy"], m["height_cm"]),
        ("canopy_w_cm", m["width_proxy"], m["width_cm"]),
        ("canopy_area_cm2", m["total_area_px"], m["area_cm2"]),
    ]
    fits = {}
    for trait, proxy, target in pairs:
        mask = target.notna() & proxy.notna()
        if mask.sum() < 3:
            continue
        r = fit_trait(proxy[mask], target[mask], args.folds)
        if r is None:
            continue
        fits[trait] = (r, proxy[mask], target[mask])
        rows.append({"trait": trait, "model": r["model"],
                     "k": round(r["k"], 5), "b": round(r["b"], 4),
                     "r2_oof": round(r["r2"], 4),
                     "cv_mae": round(r["mae"], 3), "cv_rmse": round(r["rmse"], 3),
                     "n": int(r["n"])})

    summary = pd.DataFrame(rows)
    summary.to_csv(os.path.join(args.out, "calibration_summary.csv"), index=False,
                   encoding="utf-8-sig")

    # ---- ใช้ mapping convert ทุกภาพเป็น cm ----
    cal = m[["image", "species", "height_proxy", "width_proxy", "total_area_px",
             "height_cm", "width_cm", "area_cm2"]].copy()
    for trait, col, proxy_col in [
        ("canopy_h_cm", "canopy_h_cm", "height_proxy"),
        ("canopy_w_cm", "canopy_w_cm", "width_proxy"),
        ("canopy_area_cm2", "canopy_area_cm2", "total_area_px")]:
        if trait in fits:
            r, _, _ = fits[trait]
            cal[col] = np.round(r["k"] * cal[proxy_col] + r["b"], 2)
        else:
            cal[col] = None
    cal.to_csv(os.path.join(args.out, "calibrated_canopy.csv"), index=False,
               encoding="utf-8-sig")

    print("=== Calibration (proxy -> cm) — cross-validated (เลือกแบบ CV ดีกว่า) ===")
    print(summary.to_string(index=False))
    print("\n[INFO] model=origin (k*x) หรือ intercept (k*x+b) — เลือกตาม CV RMSE")
    print("[INFO] MAE/RMSE มาจาก cross-validation (out-of-fold) — ไม่ optimistic")
    print(f"[INFO] บันทึก: {os.path.join(args.out, 'calibration_summary.csv')} + calibrated_canopy.csv")

    # ---- กราฟ fit (ใช้ mapping ที่ชนะ) ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, min(len(fits), 3), figsize=(5 * min(len(fits), 3), 4.5))
        if not isinstance(axes, np.ndarray):
            axes = [axes]
        for ax, (trait, (r, proxy, target)) in zip(axes, fits.items()):
            ax.scatter(proxy, target, s=22, alpha=0.7, color="#1B5E20")
            xs = np.linspace(proxy.min(), proxy.max(), 50)
            ax.plot(xs, r["k"] * xs + r["b"], "r-",
                    label=f"{r['model']}: k={r['k']:.2f} b={r['b']:.2f}")
            ax.set_xlabel(trait.split('_')[0] + "_proxy"); ax.set_ylabel(trait)
            ax.set_title(f"{trait} calibration (CV RMSE={r['rmse']:.2f})")
            ax.legend(); ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "calibration_fit.png"), dpi=150)
        print(f"[OK] กราฟ: {os.path.join(args.out, 'calibration_fit.png')}")
    except Exception as e:
        print(f"[WARN] กราฟไม่ได้: {e}")


if __name__ == "__main__":
    main()
