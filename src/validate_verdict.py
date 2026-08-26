#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
validate_verdict.py — Level C: ตรวจความถูกต้องของการจัดกลุ่ม verdict (H2)
เทียบ verdict ของ SAM3 (จาก plant_growth_summary.csv) กับ expert_verdict จาก ground_truth.csv

คำนวณ: confusion matrix, accuracy, per-class precision/recall(sensitivity)/specificity/F1,
        macro-F1, MCC, Cohen's kappa (inter-rater agreement ระหว่าง SAM3 กับผู้เชี่ยวชาญ)

ใช้:
    python src/validate_verdict.py \
        --summary data/processed/plant_growth_summary.csv \
        --gt data/processed/ground_truth.csv \
        --out data/processed/verdict_confusion.csv

หมายเหตุ: ground_truth.csv ต้องมีคอลัมน์ `image` + `expert_verdict`
          (เติมเองจาก docs/assets/ground_truth_template.csv)
"""
import argparse
import os
import pandas as pd
import numpy as np

# คลาสเป้าหมาย (เรียงลำดับ) — ใช้เพื่อให้ confusion matrix คงที่
CLASSES = ["ยังไม่พร้อม", "พร้อมอนุบาล", "ตรวจเอง"]


def normalize_verdict(v):
    """จับคู่ value verdict ของ pipeline ให้อยู่ใน 3 คลาสมาตรฐาน."""
    if not isinstance(v, str):
        return None
    v = v.strip()
    if v == "พร้อมอนุบาล":
        return "พร้อมอนุบาล"
    if v == "ยังไม่พร้อม":
        return "ยังไม่พร้อม"
    # "ROI-ไม่ชัด-ตรวจเอง", "หนาแน่นเกิน-ตรวจ" → หมวด "ตรวจเอง" (ส่งคนตรวจ)
    if "ตรวจ" in v or v in ("ROI-ไม่ชัด-ตรวจเอง", "หนาแน่นเกิน-ตรวจ"):
        return "ตรวจเอง"
    return None


def confusion_report(expert, pred, classes=None):
    """expert = ค่าอ้างอิง (จริง) / pred = ค่าจากระบบ (SAM3)."""
    classes = classes or CLASSES
    from sklearn.metrics import confusion_matrix, cohen_kappa_score, matthews_corrcoef
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support

    # ตัดแถวที่ expert หรือ pred ไม่มีค่า (ยังไม่ได้กรอก)
    valid = (expert.notna()) & (pred.notna())
    y_true = expert[valid].map(normalize_verdict)
    y_pred = pred[valid].map(normalize_verdict)

    cm = confusion_matrix(y_true, y_pred, labels=classes)
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=classes, zero_division=0)
    try:
        kappa = cohen_kappa_score(y_true, y_pred)
    except Exception:
        kappa = np.nan
    try:
        mcc = matthews_corrcoef(y_true, y_pred)
    except Exception:
        mcc = np.nan

    df = pd.DataFrame({
        "class": classes,
        "n_ref": support,
        "precision": np.round(prec, 4),
        "sensitivity(recall)": np.round(rec, 4),
        "f1": np.round(f1, 4),
    })

    return {
        "n": int(len(y_true)),
        "n_skipped": int((~valid).sum()),
        "accuracy": round(float(acc), 4),
        "macro_f1": round(float(f1.mean()), 4),
        "mcc": round(float(mcc), 4) if not np.isnan(mcc) else None,
        "cohen_kappa": round(float(kappa), 4) if not np.isnan(kappa) else None,
        "confusion_matrix": cm,     # row=expert, col=SAM3
        "per_class": df,
    }


def main():
    ap = argparse.ArgumentParser(description="Verdict confusion matrix (Level C)")
    ap.add_argument("--summary", required=True, help="plant_growth_summary.csv (มีคอลัมน์ verdict)")
    ap.add_argument("--gt", required=True, help="ground_truth.csv (มีคอลัมน์ expert_verdict)")
    ap.add_argument("--out", default="data/processed/verdict_confusion.csv")
    args = ap.parse_args()

    s = pd.read_csv(args.summary, encoding="utf-8-sig")
    g = pd.read_csv(args.gt, encoding="utf-8-sig")
    if "image" not in s.columns or "verdict" not in s.columns:
        raise SystemExit("summary ต้องมีคอลัมน์ image + verdict")
    if "image" not in g.columns or "expert_verdict" not in g.columns:
        raise SystemExit("ground_truth ต้องมีคอลัมน์ image + expert_verdict")

    # รวม (merge) ตาม image
    m = s[["image", "verdict"]].merge(g[["image", "expert_verdict"]], on="image")

    res = confusion_report(m["expert_verdict"], m["verdict"])

    print("=" * 60)
    print("VERDICT VALIDATION  (expert = reference / SAM3 = predicted)")
    print("=" * 60)
    n_filled = int((m["expert_verdict"].notna()).sum())
    print(f"ภาพทั้งหมด: {len(m)}  |  กรอก expert_verdict: {n_filled}  |  ข้าม: {res['n_skipped']}")
    if n_filled == 0:
        print("\n⚠️ ยังไม่มี expert_verdict — เติมใน ground_truth.csv ก่อน (docs/assets/ground_truth_template.csv)")
        print("   ตัวอย่าง: 001.jpg,,,,,,,พร้อมอนุบาล")
        return 0
    print(f"\nAccuracy   : {res['accuracy']}")
    print(f"Macro-F1   : {res['macro_f1']}")
    print(f"MCC        : {res['mcc']}")
    print(f"Cohen kappa: {res['cohen_kappa']}")
    print("\n--- Per-class (SAM3 วัดเทียบผู้เชี่ยวชาญ) ---")
    print(res["per_class"].to_string(index=False))
    print("\n--- Confusion matrix (row=expert, col=SAM3) ---")
    print("{:<14}".format("expert\\SAM3") + "".join(f"{c:<12}" for c in CLASSES))
    cm = res["confusion_matrix"]
    for i, c in enumerate(CLASSES):
        print(f"{c:<14}" + "".join(f"{cm[i][j]:<12}" for j in range(len(CLASSES))))

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    # บันทึกผลแยกไฟล์ (matrix + per-class)
    out = args.out.replace(".csv", "_full.csv")
    res["per_class"].assign(n=res["n"])
    with open(out, "w", encoding="utf-8-sig") as f:
        f.write("metric,value\n")
        for k, v in [("n", res["n"]), ("accuracy", res["accuracy"]),
                     ("macro_f1", res["macro_f1"]), ("mcc", res["mcc"]),
                     ("cohen_kappa", res["cohen_kappa"])]:
            f.write(f"{k},{v}\n")
        f.write("\nconfusion_matrix_row_expert_col_sam3\n")
        f.write("expert," + ",".join(CLASSES) + "\n")
        for i, c in enumerate(CLASSES):
            f.write(c + "," + ",".join(str(x) for x in cm[i]) + "\n")
    print(f"\nบันทึก: {out}")


if __name__ == "__main__":
    main()
