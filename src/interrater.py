"""Inter-rater reliability — ICC(2,1) ต่อเนื่อง + Cohen's kappa ต่อคลาส (งาน T5)

ใช้ตอบจุดอ่อน "การประเมินด้วยสายตาในงานเพาะเลี้ยงเนื้อเยื่อมีความแปรปรวนระหว่างผู้ประเมิน"
(Zhang et al., 2026) — คำนวณความสม่ำเสมอระหว่างผู้ประเมิน 2+ คน

รัน:
  # ต่อเนื่อง (height_cm/width_cm/area_cm2 จาก 2 raters)
  python src/interrater.py --csv gt.csv --cols raterA_height,raterB_height --type continuous
  # คลาส (expert_verdict จาก 2 raters)
  python src/interrater.py --csv gt.csv --cols raterA_verdict,raterB_verdict --type categorical

csv ต้องมีคอลัมน์ id (เช่น image) + 1 คอลัมน์ต่อผู้ประเมิน
ผลลัพธ์: พิมพ์ ICC(2,1) หรือ Cohen's kappa + % agreement + (ต่อเนื่อง) MAE/Pearson
"""

import argparse

import numpy as np
import pandas as pd
from scipy import stats


def icc_2_1(X):
    """ICC(2,1) two-way random, single measure — เมทริกซ์ subjects x raters"""
    X = np.asarray(X, float)
    n, k = X.shape
    if n < 2 or k < 2:
        return None
    grand = X.mean()
    row_mean = X.mean(axis=1)  # per subject
    col_mean = X.mean(axis=0)  # per rater
    ss_total = ((X - grand) ** 2).sum()
    ss_sub = k * ((row_mean - grand) ** 2).sum()
    ss_rat = n * ((col_mean - grand) ** 2).sum()
    ss_err = ss_total - ss_sub - ss_rat
    df_sub, df_rat, df_err = n - 1, k - 1, (n - 1) * (k - 1)
    ms_sub = ss_sub / df_sub
    ms_rat = ss_rat / df_rat
    ms_err = ss_err / df_err if df_err else 0.0
    icc = (ms_sub - ms_err) / (ms_sub + (k - 1) * ms_err + k * (ms_rat - ms_err) / n)
    return icc


def cohen_kappa(y1, y2):
    """Cohen's kappa (หลายคลาสได้) + observed agreement"""
    y1 = np.asarray(y1)
    y2 = np.asarray(y2)
    n = len(y1)
    if n == 0:
        return None, None
    obs = (y1 == y2).mean()
    # confusion
    cats = sorted(set(y1) | set(y2))
    mat = pd.crosstab(pd.Series(y1), pd.Series(y2), dropna=False).reindex(index=cats, columns=cats).fillna(0).values
    # expected agreement by chance
    row = mat.sum(1); col = mat.sum(0)
    pe = float((row @ col) / (n * n))
    kappa = (obs - pe) / (1 - pe) if (1 - pe) > 0 else None
    return kappa, obs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--id", default="image", help="คอลัมน์ id (เช่น image)")
    ap.add_argument("--cols", required=True, help="คอลัมน์ผู้ประเมิน (คั่น ,)")
    ap.add_argument("--type", required=True, choices=["continuous", "categorical"])
    args = ap.parse_args()

    df = pd.read_csv(args.csv, encoding="utf-8-sig")
    cols = [c.strip() for c in args.cols.split(",")]
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise SystemExit(f"ไม่พบคอลัมน์: {missing}")
    sub = df[cols].dropna()
    print(f"[INFO] ผู้ประเมิน {len(cols)} คน · {len(sub)} ตัวอย่างสมบูรณ์ (จาก {len(df)})")

    if args.type == "continuous":
        icc = icc_2_1(sub.values)
        print(f"\n=== ICC(2,1) continuous ({cols}) → {icc:.4f}" if icc is not None else "ICC ไม่ได้ (n หรือ k ไม่พอ)")
        # pairwise Pearson + MAE
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                a, b = sub[cols[i]].values, sub[cols[j]].values
                r = np.corrcoef(a, b)[0, 1]
                mae = np.mean(np.abs(a - b))
                print(f"  {cols[i]} vs {cols[j]}: Pearson r={r:.3f} · MAE={mae:.3f}")
    else:
        print(f"\n=== Cohen's kappa categorical ({cols}) ===")
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                kap, obs = cohen_kappa(sub[cols[i]].values, sub[cols[j]].values)
                if kap is None:
                    print(f"  {cols[i]} vs {cols[j]}: kappa ไม่ได้ (คลาสเดียว)")
                else:
                    # จัด classification ความแรง (Landis & Koch)
                    strength = ("poor" if kap < 0 else "slight" if kap < 0.2 else "fair" if kap < 0.4
                                else "moderate" if kap < 0.6 else "substantial" if kap < 0.8 else "near-perfect")
                    print(f"  {cols[i]} vs {cols[j]}: kappa={kap:.3f} ({strength}) · agreement={obs:.1%}")


if __name__ == "__main__":
    main()
