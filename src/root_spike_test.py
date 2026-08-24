"""Spike test: SAM3 PCS กับ prompt "root" — ทดสอบ kill criterion ของระบบราก
(ระบบราก = ตัวชี้วัดอันดับ 1 ของความพร้อมอนุบาล — grill v3, 2026-07-29)

รันบน Colab (GPU):
    python root_spike_test.py --data <โฟลเดอร์ภาพ> --out <ผลลัพธ์> --hf-token <TOKEN> \
        [--limit 20] [--images 001.jpg,010.jpg] [--img-size 1024]

เกณฑ์ kill (จาก grill v3):
  ✅ ผ่าน ถ้า: เจอ root mask ใน >= 50% ของภาพทดสอบ และ confidence(root) ไม่ต่ำกว่า plant/leaf อย่างชัดเจน
  ❌ ไม่ผ่าน (ตัดราก) ถ้า: เจอ < 50% หรือ conf(root) << conf(plant/leaf)
     → pivot: ย้ายแกนไป hyperhydricity + ลักษณะยอด/ใบ (ตาม grill v3)

ผลลัพธ์:
  root_spike_summary.csv — ต่อภาพ: root/plant/leaf (count, area_px, conf_max) + root_ratio
  สรุป console: % เจอ root, mean root_ratio, เปรียบเทียบ conf
"""

import argparse
import glob
import os
import time

import numpy as np
import pandas as pd
import torch
from PIL import Image

ROOT_KILL_MIN_DETECT = 0.50   # ต้องเจอ root >= 50% ของภาพ
ROOT_KILL_CONF_GAP = 0.15     # conf(root) ต่ำกว่า plant/leaf เกิน 0.15 → ถือว่าต่ำกว่าชัดเจน


def load_images(data_dir, limit=None, images=None):
    exts = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
    files = []
    for e in exts:
        files += glob.glob(os.path.join(data_dir, e))
    files = sorted(set(files))
    if images:
        want = {i.strip().split(".")[0] for i in images.split(",")}
        files = [f for f in files if os.path.splitext(os.path.basename(f))[0] in want]
    if limit:
        files = files[:limit]
    return files


def load_sam3(device):
    from transformers import Sam3Processor, Sam3Model
    model = Sam3Model.from_pretrained("facebook/sam3").to(device)
    processor = Sam3Processor.from_pretrained("facebook/sam3")
    return model, processor


def seg_prompt(model, processor, device, pil_img, prompt, score_thr=0.5, mask_thr=0.5):
    """คืน (masks bool (N,H,W), scores np.array) ของ prompt เดียว"""
    inputs = processor(images=pil_img, text=prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    result = processor.post_process_instance_segmentation(
        outputs, threshold=score_thr, mask_threshold=mask_thr,
        target_sizes=inputs.get("original_sizes").tolist())[0]
    masks = result["masks"]
    if hasattr(masks, "cpu"):
        masks = masks.cpu()
    masks = np.asarray(masks).astype(bool)
    scores = result.get("scores")
    if scores is not None:
        if hasattr(scores, "cpu"):
            scores = scores.cpu()
        scores = np.asarray(scores)
    return masks, scores


def summarize(masks, scores):
    """คืน dict: count, area_px, conf_max (0 ถ้าไม่มี instance)"""
    if masks is None or len(masks) == 0:
        return {"count": 0, "area_px": 0, "conf_max": 0.0}
    area = int(masks.any(axis=0).sum())
    conf = float(scores.max()) if scores is not None and len(scores) > 0 else 0.0
    return {"count": int(len(masks)), "area_px": area, "conf_max": conf}


def main():
    ap = argparse.ArgumentParser(description="Spike test: SAM3 PCS prompt root (kill criterion)")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพ")
    ap.add_argument("--out", default="root_spike", help="โฟลเดอร์ผลลัพธ์")
    ap.add_argument("--hf-token", default=None, help="HF_TOKEN (facebook/sam3 gated)")
    ap.add_argument("--limit", type=int, default=None, help="ใช้ภาพแรก N ไฟล์ (default: ทั้งหมด)")
    ap.add_argument("--images", default=None, help="ระบุชื่อภาพ คั่นด้วย , (เช่น 001.jpg,010.jpg)")
    ap.add_argument("--img-size", type=int, default=1024, help="resize ด้านยาว max")
    ap.add_argument("--prompts", default="plant,leaf,root", help="prompt ที่ทดสอบ คั่น ,")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] device: {device}")
    if device == "cpu":
        raise SystemExit("SAM3 ไม่รองรับ CPU — ต้องรันบน Colab GPU")

    if args.hf_token:
        from huggingface_hub import login
        login(token=args.hf_token, add_to_git_credential=False)

    prompts = [p.strip() for p in args.prompts.split(",") if p.strip()]
    os.makedirs(args.out, exist_ok=True)

    print("[INFO] โหลด SAM3 (facebook/sam3) — ใช้เวลาหลายนาที")
    t0 = time.time()
    model, processor = load_sam3(device)
    print(f"[INFO] โหลดเสร็จใน {time.time()-t0:.1f}s")

    images = load_images(args.data, limit=args.limit,
                         images=args.images.split(",") if args.images else None)
    if not images:
        raise SystemExit(f"ไม่พบภาพใน {args.data}")
    print(f"[INFO] ทดสอบ {len(images)} ภาพ · prompts: {prompts}")

    rows = []
    for i, path in enumerate(images, 1):
        name = os.path.basename(path)
        img = Image.open(path).convert("RGB")
        if args.img_size and max(img.size) > args.img_size:
            img = img.resize((args.img_size, args.img_size))  # ภาพจริง 2992² → 1024² เร็วขึ้น
        row = {"image": name}
        res = {}
        for p in prompts:
            masks, scores = seg_prompt(model, processor, device, img, p)
            s = summarize(masks, scores)
            res[p] = s
            row[f"{p}_count"] = s["count"]
            row[f"{p}_area_px"] = s["area_px"]
            row[f"{p}_conf_max"] = s["conf_max"]
        # root_ratio ตามนิยาม grill v3: area(mask root)/area(mask plant)
        plant_area = res["plant"]["area_px"] if "plant" in res else 0
        root_area = res["root"]["area_px"] if "root" in res else 0
        row["root_ratio"] = round(root_area / plant_area, 4) if plant_area > 0 else 0.0
        row["root_detected"] = 1 if (res["root"]["count"] > 0) else 0
        rows.append(row)
        if i % 5 == 0:
            print(f"  ... {i}/{len(images)}")

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(args.out, "root_spike_summary.csv"), index=False, encoding="utf-8-sig")
    print(f"[OK] บันทึก root_spike_summary.csv ({len(df)} ภาพ)")

    # ---- สรุป + kill criterion ----
    n = len(df)
    if "root" in prompts:
        det_rate = df["root_detected"].mean()
        mean_ratio = df["root_ratio"].mean()
        mean_conf_root = df["root_conf_max"].mean()
        ref_prompts = [p for p in prompts if p != "root"]
        mean_conf_ref = df[[f"{p}_conf_max" for p in ref_prompts]].mean().mean() if ref_prompts else 0
        print("\n=== สรุป spike test root ===")
        print(f"ภาพทดสอบ: {n}")
        print(f"เจอ root mask: {det_rate:.0%} ({int(df['root_detected'].sum())}/{n})")
        print(f"root_ratio เฉลี่ย (root_area/plant_area): {mean_ratio:.4f}")
        print(f"conf(root) เฉลี่ย: {mean_conf_root:.3f} · conf({'+'.join(ref_prompts)}) เฉลี่ย: {mean_conf_ref:.3f}")
        passed = (det_rate >= ROOT_KILL_MIN_DETECT
                  and mean_conf_root >= mean_conf_ref - ROOT_KILL_CONF_GAP)
        print("\n--- เกณฑ์ kill (grill v3) ---")
        print(f"  1) เจอ root >= {ROOT_KILL_MIN_DETECT:.0%}? {'✅' if det_rate >= ROOT_KILL_MIN_DETECT else '❌'}")
        print(f"  2) conf(root) ไม่ต่ำกว่า plant/leaf เกิน {ROOT_KILL_CONF_GAP}? "
              f"{'✅' if mean_conf_root >= mean_conf_ref - ROOT_KILL_CONF_GAP else '❌'}")
        if passed:
            print("\n🎉 สรุป: ROOT ผ่าน kill criterion → เอา root_ratio เข้า verdict ได้ (ขั้นต่อไป)")
        else:
            print("\n🛑 สรุป: ROOT ไม่ผ่าน → ตัดรากทิ้ง ตาม grill v3 "
                  "(pivot ไป hyperhydricity + ลักษณะยอด/ใบ) — แก้เอกสารให้ซื่อสัตย์")


if __name__ == "__main__":
    main()
