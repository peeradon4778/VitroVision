"""prepare_annotation — คัด 30 ภาพแบบ stratified + สร้างโฟลเดอร์ทำงานสำหรับ annotate mask มือ

เหตุผล (validate-plan §2.2/§3): ระดับ A ต้อง ≥30 ภาพ ครอบคลุม 3 คลาส verdict + ความหลากหลายทางสัณฐาน
  (ภาพ dense/หลายต้น, ต้นจิ๋ว height≈0 ให้ความท้าทาย/การครอบคลุมมาก)

เลือกแบบ:
  - รวมทั้งหมดคลาส 'ตรวจเอง' (มีแค่ 2 → มีค่า, เป็นกรณี borderline)
  - ดึงประเภท 'dense/multi' (leaf>30) และ 'tiny' (height≈0) เข้าไปเพื่อ diversity
  - เติม 'ยังไม่พร้อม' / 'พร้อมอนุบาล' ให้ครบตามสัดส่วนที่ตั้ง (--n, ต่อคลาส config)
ผลลัพธ์:
  - <out>/annotate_list.csv  (image, expert_verdict, note, bucket, order)
  - <out>/images/            (สำเนา 30 ภาพที่คัด — ใช้อนุญาต seed/annotation บนโฟลเดอร์นี้)

รัน:
  python src/prepare_annotation.py --gt data/processed/ground_truth.csv \
      --data data/raw/20260814_batch --out data/work/annotate --n 30
"""

import argparse
import os
import shutil

import pandas as pd


def bucket_of(note):
    """จัดกลุ่มภาพตามลักษณะสนใจ"""
    n = str(note) if pd.notna(note) else ""
    if "หลายต้น" in n or "นับไม่ไหว" in n or "leaf>30" in n or "หนาแน่น" in n:
        return "dense/multi"
    if "height≈0" in n or "height" in n and "0" in n:
        return "tiny"
    return "typical"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", required=True, help="ground_truth.csv")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพต้นฉบับ")
    ap.add_argument("--out", default="data/work/annotate")
    ap.add_argument("--n", type=int, default=30, help="จำนวนภาพเป้าหมาย")
    ap.add_argument("--per-class", default=None,
                    help="เช่น 'ยังไม่พร้อม:10,พร้อมอนุบาล:10,ตรวจเอง:5' (default: คำนวณอัตโนมัติ)")
    args = ap.parse_args()

    gt = pd.read_csv(args.gt, encoding="utf-8-sig")
    gt["bucket"] = gt["note"].apply(bucket_of)
    classes = gt["expert_verdict"].astype(str).value_counts()
    print("คลาสใน GT:", classes.to_dict())

    # --- คำนวณโควตาต่อคลาส ---
    quotas = {}
    if args.per_class:
        for tok in args.per_class.split(","):
            k, v = tok.strip().split(":")
            quotas[k.strip()] = int(v)
    else:
        # default: ตรวจเอง = ทุกตัว (cap 5), ที่เหลือแบ่งครึ่งยังไม่พร้อม/พร้อมอนุบาล
        check = min(int(classes.get("ตรวจเอง", 0)), 5)
        remaining = args.n - check
        quotas = {"ตรวจเอง": check,
                  "ยังไม่พร้อม": remaining // 2,
                  "พร้อมอนุบาล": remaining - remaining // 2}

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.join(args.out, "images"), exist_ok=True)

    picked = []
    rng = __import__("numpy").random.default_rng(42)
    for cls, quota in quotas.items():
        pool = gt[gt["expert_verdict"].astype(str) == cls].copy()
        if len(pool) == 0:
            print(f"  [skip] '{cls}' ไม่มีใน GT")
            continue
        # สุ่ม stratified ตามสัดส่วน bucket ภายในคลาส (ให้ mix สมดุล ไม่ over-sample dense)
        # ยังคงบังคับรวม: ถ้าเป็น 'ตรวจเอง' เอาทุกตัว, ถ้ามี tiny ให้ได้อย่างน้อย 1
        if cls == "ตรวจเอง":
            sel = pool.copy()
        else:
            sel = []
            # proportional per bucket
            prop = pool["bucket"].value_counts(normalize=True)
            for b, frac in prop.items():
                bpool = pool[pool["bucket"] == b]
                take = max(int(round(frac * quota)), 1 if (b == "tiny" and len(bpool)) else 0)
                take = min(take, len(bpool))
                if b == "dense/multi":
                    take = min(take, max(1, quota // 4))  # จำกัด dense ไม่ให้เกิน ~25%
                sel.extend(bpool.sample(n=take, random_state=rng).to_dict("records"))
            # ถ้าเลือกขาด quota ให้เติมจากที่เหลือแบบสุ่ม
            if len(sel) < quota:
                rest = pool.loc[~pool["image"].isin([s["image"] for s in sel])]
                extra = rest.sample(n=min(quota - len(sel), len(rest)), random_state=rng)
                sel.extend(extra.to_dict("records"))
            sel = pd.DataFrame(sel)
            if len(sel) > quota:
                sel = sel.sample(n=quota, random_state=rng)
        take = min(int(quota) if cls != "ตรวจเอง" else len(sel), len(pool))
        sel = sel.head(take)
        picked.append(sel)
        print(f"  '{cls}': เลือก {len(sel)}/{len(pool)} (โควตา {quota}) · bucket {sel['bucket'].value_counts().to_dict()}")

    df = pd.concat(picked).reset_index(drop=True)
    df = df[["image", "expert_verdict", "note", "bucket"]].copy()
    df["order"] = range(1, len(df) + 1)
    if len(df) > args.n:
        df = df.head(args.n)
    df.to_csv(os.path.join(args.out, "annotate_list.csv"), index=False, encoding="utf-8-sig")

    # --- คัดลอกภาพ ---
    copied = 0
    for _, r in df.iterrows():
        src = os.path.join(args.data, r["image"])
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(args.out, "images", r["image"]))
            copied += 1
        else:
            print(f"  [warn] ไม่พบภาพ {r['image']}")
    print(f"\n[OK] คัดเลือก {len(df)} ภาพ → {os.path.join(args.out, 'images')} (คัดลอก {copied})")
    print(f"[OK] manifest: {os.path.join(args.out, 'annotate_list.csv')}")
    print("\n=== สรุป bucket ===")
    print(df["bucket"].value_counts().to_string())
    print("\n=== กระจายตามคลาส verdict ===")
    print(df["expert_verdict"].value_counts().to_string())
    print("\n[Colab] สร้าง seed (SAM3) สำหรับ 30 ภาพนี้:")
    print(f"  python src/train_unet_distill.py generate-pseudo --data {args.out}/images --out {args.out}/seed --hf-token <TOKEN> --limit {len(df)}")


if __name__ == "__main__":
    main()
