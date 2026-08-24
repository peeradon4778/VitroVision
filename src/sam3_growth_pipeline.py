"""SAM 3 Plant Tissue Culture Growth Analysis Pipeline — Multi-Dimensional (headless batch).

รันบน Google Colab แบบสคริปต์ (GPU + token) สำหรับภาพจำนวนมาก:
    python sam3_growth_pipeline.py --data /content/data --out /content/results [--synthetic] [--config config.json]

--config: ไฟล์ JSON ตั้งค่า (PIXEL_TO_CM, threshold, prompts, species thresholds) โดยไม่ต้องแก้โค้ด
          ตัวอย่าง: pipeline_config.example.json (สร้างจาก config กลางของโปรเจกต์)

ข้อกำหนด:
- ต้องมี GPU (CUDA) — facebook/sam3 เป็น gated model ที่ไม่รองรับ CPU
- ต้องตั้ง HF_TOKEN (token ที่มี access ถึง facebook/sam3)

ผลลัพธ์:
- plant_growth_summary.csv/.xlsx — feature หลายมิติทุกภาพ (โครงสร้าง/อวัยวะ/ความซับซ้อน/สี/คุณภาพภาพ/verdict)
- _progress.csv — checkpoint รายภาพ (กัน Colab timeout)
- species_summary.csv — สถิติสรุปแยกชนิดพืช
- ใส่ --synthetic → สร้างภาพต้นจำลอง (รู้ค่าจริง) + รัน SAM3 เทียบ → benchmark_IoU_Dice_MAE.csv
- ถ้ามี <data>/ground_truth.csv (image, leaf_count, shoot_count, root_count, height_cm, width_cm, area_cm2)
  → validation_metrics.csv (Pearson/MAE/RMSE เทียบการวัดมือจริง)
"""

import argparse
import glob
import json
import math
import os
import time

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from PIL import Image

PROMPTS = ["plant", "leaf", "shoot", "stem", "root"]
SCORE_THRESHOLD = 0.5
MASK_THRESHOLD = 0.5
DETECT_BOTTLE = True  # SAM3 หา 'glass jar bottle' มากำหนด ROI → coverage สัมพัทธ์ขวด
PIXEL_TO_CM = None  # calibrate ก่อนใช้: 1 px = ? cm
LOWER_GREEN = (35, 40, 40)
UPPER_GREEN = (85, 255, 255)
LOWER_YELLOW = (15, 60, 60)
UPPER_YELLOW = (35, 255, 255)
LOWER_BROWN = (0, 40, 40)
UPPER_BROWN = (15, 200, 130)
GLARE_V = 0.95
GLARE_S = 0.15
CONDENSE_V = 0.92
CONDENSE_S = 0.30
BASE_CONFIDENCE = 0.80
COVERAGE_READY = 0.20  # พริกจินดา: ตั้งตามผู้เชี่ยวชาญ 2026-08-18 (เดิม 0.35 จาก literature) — อยู่ระหว่าง validate
COVERAGE_OVERDENSE = 0.80
USE_SPECIES_THRESHOLDS = False  # True = ใช้ threshold ต่อชนิดจาก SPECIES_THRESHOLDS
SPECIES_THRESHOLDS = {
    "กล้วย": {"ready": 0.35, "overdense": 0.80},
    "กล้วยไม้": {"ready": 0.30, "overdense": 0.75},
    "มันฝรั่ง": {"ready": 0.40, "overdense": 0.85},
}


def load_config(cfg_path=None):
    """โหลด config.json มาแทนค่าคงที่ (PIXEL_TO_CM, threshold, prompts, species thresholds)
    โดยไม่ต้องแก้โค้ด — ใช้คู่กับ docs/CALIBRATION_GUIDE.md"""
    global PROMPTS, SCORE_THRESHOLD, MASK_THRESHOLD, DETECT_BOTTLE, PIXEL_TO_CM
    global USE_SPECIES_THRESHOLDS, SPECIES_THRESHOLDS, COVERAGE_READY, COVERAGE_OVERDENSE
    if not cfg_path or not os.path.exists(cfg_path):
        print(f"[INFO] ไม่พบ --config ({cfg_path}) — ใช้ค่าเริ่มต้นในโค้ด")
        return
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    PROMPTS = cfg.get("prompts", PROMPTS)
    SCORE_THRESHOLD = float(cfg.get("score_threshold", SCORE_THRESHOLD))
    MASK_THRESHOLD = float(cfg.get("mask_threshold", MASK_THRESHOLD))
    DETECT_BOTTLE = bool(cfg.get("detect_bottle", DETECT_BOTTLE))
    PIXEL_TO_CM = float(cfg["pixel_to_cm"]) if cfg.get("pixel_to_cm") else PIXEL_TO_CM
    USE_SPECIES_THRESHOLDS = bool(cfg.get("use_species_thresholds", USE_SPECIES_THRESHOLDS))
    if cfg.get("species_thresholds"):
        SPECIES_THRESHOLDS = cfg["species_thresholds"]
    if cfg.get("coverage"):
        COVERAGE_READY = float(cfg["coverage"].get("ready", COVERAGE_READY))
        COVERAGE_OVERDENSE = float(cfg["coverage"].get("overdense", COVERAGE_OVERDENSE))
    print(f"[INFO] โหลด config: {cfg_path}")
    print(f"  prompts={PROMPTS} · pixel_to_cm={PIXEL_TO_CM} · "
          f"species_thresholds={'เปิด' if USE_SPECIES_THRESHOLDS else 'ปิด'}")


def extract_zips(data_dir):
    import zipfile
    for z in glob.glob(os.path.join(data_dir, "*.zip")):
        print(f"พบ zip: {os.path.basename(z)} — กำลังแตก...")
        with zipfile.ZipFile(z) as zf:
            n_img = 0
            for n in zf.namelist():
                if n.lower().endswith((".jpg", ".jpeg", ".png")):
                    try:
                        zf.extract(n, data_dir)
                        n_img += 1
                    except Exception as ex:
                        print(f"ข้าม {n}: {ex}")
            print(f"แตกแล้ว {n_img} ไฟล์ภาพ")


def load_images(data_dir):
    exts = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG")
    extract_zips(data_dir)
    paths = []
    for e in exts:
        paths += glob.glob(os.path.join(data_dir, e))
    images = {}
    for p in sorted(paths):
        try:
            images[os.path.basename(p)] = Image.open(p).convert("RGB")
        except Exception as ex:
            print(f"ข้ามไฟล์ {p}: {ex}")
    return images


def masks_to_numpy(result):
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


def union_bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1


def segment_prompt(model, processor, device, image, prompt):
    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    result = processor.post_process_instance_segmentation(
        outputs, threshold=SCORE_THRESHOLD, mask_threshold=MASK_THRESHOLD,
        target_sizes=inputs.get("original_sizes").tolist())[0]
    return masks_to_numpy(result)


def count_confident(scores, masks):
    if scores is not None and len(scores) > 0:
        return int((scores >= SCORE_THRESHOLD).sum())
    return len(masks)


def safe_div(a, b):
    return float(a / b) if b > 0 else 0.0


def generic_species(filename):
    return "ไม่ระบุชนิด"


def _merged_count(mask, dilate_k=7, min_area_frac=0.01):
    """นับอวัยวะ: รวมชิ้นส่วนที่ติดกัน (กัน over-segmentation) + ตัดชิ้นเล็กเกินไปทิ้ง"""
    if not mask.any():
        return 0, [], None
    dil = cv2.dilate(mask.astype(np.uint8), np.ones((dilate_k, dilate_k), np.uint8))
    num, labels = cv2.connectedComponents(dil)
    comps = [int((labels == i).sum()) for i in range(1, num)]
    if not comps:
        return 0, [], None
    min_area = max(200, min_area_frac * max(comps))
    areas = [a for a in comps if a >= min_area]
    merged = np.zeros_like(mask)
    for i in range(1, num):
        if comps[i - 1] >= min_area:
            merged |= (labels == i)
    return len(areas), areas, merged


def draw_overlay(img, masks, color=(0, 200, 0)):
    img_rgb = np.array(img).copy()
    for m in masks:
        contours, _ = cv2.findContours((m.astype(np.uint8)) * 255,
                                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img_rgb, contours, -1, color, 2)
    return img_rgb


COLORS = {"plant": (0, 200, 0), "leaf": (0, 120, 255), "shoot": (255, 120, 0),
          "stem": (120, 60, 200), "root": (200, 0, 200)}


def extract_features(img, masks_by_prompt, roi=None):
    rgb = np.array(img)
    H, W = rgb.shape[:2]

    if roi is None:
        roi = np.ones((H, W), dtype=bool)
    rbb = union_bbox(roi)
    if rbb is None:
        rbb = (0, 0, W, H)
    _, _, roi_w, roi_h = rbb
    roi_area = int(roi.sum())

    union = np.zeros((H, W), dtype=bool)
    for p in PROMPTS:
        m = masks_by_prompt.get(p, (np.zeros((0, H, W), dtype=bool), None))[0]
        if len(m) > 0:
            union |= m.any(axis=0)
    mask_in_roi = union & roi
    area = int(mask_in_roi.sum())
    coverage_ratio = safe_div(area, roi_area)

    ph_union = np.zeros((H, W), dtype=bool)
    for p in ("plant", "shoot"):
        m = masks_by_prompt.get(p, (np.zeros((0, H, W), dtype=bool), None))[0]
        if len(m) > 0:
            ph_union |= m.any(axis=0)
    if not ph_union.any():
        ph_union = mask_in_roi
    bb = union_bbox(ph_union & roi)
    if bb is not None:
        _, _, bw, bh = bb
        height_proxy = safe_div(bh, roi_h)
        width_proxy = safe_div(bw, roi_w)
        aspect_ratio = safe_div(bh, bw)
        compactness = safe_div(area, bh * bw)
    else:
        height_proxy = width_proxy = aspect_ratio = compactness = 0.0
        bw = bh = 0

    hull_ratio = 0.0
    perimeter_px = 0.0
    if area > 0:
        contours, _ = cv2.findContours((mask_in_roi.astype(np.uint8)) * 255,
                                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            hull_ratio = safe_div(area, cv2.contourArea(cv2.convexHull(cnt)))
            perimeter_px = float(cv2.arcLength(cnt, True))
    perimeter_ratio = safe_div(perimeter_px, 2 * (roi_w + roi_h))

    counts = {}
    for p in PROMPTS:
        m, s = masks_by_prompt.get(p, (np.zeros((0, H, W), dtype=bool), None))
        counts[p] = count_confident(s, m)

    leaf_masks = masks_by_prompt.get("leaf", (np.zeros((0, H, W), dtype=bool), None))[0]
    leaf_mask_union = leaf_masks.any(axis=0) if len(leaf_masks) > 0 else None
    leaf_count_raw = counts.get("leaf", 0)
    leaf_count_method = "prompt"
    if leaf_mask_union is None or not leaf_mask_union.any():
        leaf_mask_union = (ph_union & roi) if ph_union.any() else None
        if leaf_mask_union is not None:
            leaf_count_method = "fallback"
    if leaf_mask_union is not None and leaf_mask_union.any():
        leaf_count, leaf_areas, leaf_merged = _merged_count(leaf_mask_union & roi)
    else:
        leaf_count, leaf_areas = 0, []
    mean_leaf_area = float(np.mean(leaf_areas)) if leaf_areas else 0.0
    leaf_area_cv = safe_div(float(np.std(leaf_areas)), max(np.mean(leaf_areas), 1e-6)) if leaf_areas else 0.0
    max_leaf_area = float(max(leaf_areas)) if leaf_areas else 0.0

    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    green = cv2.inRange(hsv, np.array(LOWER_GREEN), np.array(UPPER_GREEN)) > 0
    yellow = cv2.inRange(hsv, np.array(LOWER_YELLOW), np.array(UPPER_YELLOW)) > 0
    brown = cv2.inRange(hsv, np.array(LOWER_BROWN), np.array(UPPER_BROWN)) > 0
    if area > 0:
        green_pct = 100.0 * int((green & mask_in_roi).sum()) / area
        yellow_pct = 100.0 * int((yellow & mask_in_roi).sum()) / area
        brown_pct = 100.0 * int((brown & mask_in_roi).sum()) / area
        dark_green_ratio = 100.0 * int(((hsv[..., 2] < 90) & green & mask_in_roi).sum()) / area
        g_ratio = rgb[..., 1].astype(np.float32) / (rgb.sum(axis=2).astype(np.float32) + 1e-6)
        greenness = float(g_ratio[mask_in_roi].mean())
        mean_hue = float(hsv[..., 0][mask_in_roi].mean())
        mean_sat = float(hsv[..., 1][mask_in_roi].mean())
        mean_val = float(hsv[..., 2][mask_in_roi].mean())
    else:
        green_pct = yellow_pct = brown_pct = dark_green_ratio = 0.0
        greenness = mean_hue = mean_sat = mean_val = 0.0
    healthy_color = green_pct - yellow_pct - brown_pct

    v = hsv[..., 2].astype(np.float32) / 255.0
    s = hsv[..., 1].astype(np.float32) / 255.0
    glare_score = 100.0 * int(((v > GLARE_V) & (s < GLARE_S) & roi).sum()) / max(roi_area, 1)
    condensation_score = 100.0 * int(((v > CONDENSE_V) & (s < CONDENSE_S) & roi).sum()) / max(roi_area, 1)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)[roi]
    brightness_mean = float(gray.mean()) if len(gray) else 0.0
    brightness_std = float(gray.std()) if len(gray) else 0.0

    score_list = [s for _, s in masks_by_prompt.values() if s is not None and len(s) > 0]
    if score_list:
        all_scores = np.concatenate(score_list)
        mean_score = float(all_scores.mean())
        min_score = float(all_scores.min())
        score_std = float(all_scores.std())
    else:
        mean_score = min_score = score_std = 0.0

    return {
        "total_area_px": area,
        "coverage_ratio": round(coverage_ratio, 6),
        "height_proxy": round(height_proxy, 6),
        "width_proxy": round(width_proxy, 6),
        "aspect_ratio": round(aspect_ratio, 6),
        "compactness": round(compactness, 6),
        "canopy_h_cm": round(bh * PIXEL_TO_CM, 2) if (bb is not None and PIXEL_TO_CM) else None,
        "canopy_w_cm": round(bw * PIXEL_TO_CM, 2) if (bb is not None and PIXEL_TO_CM) else None,
        "hull_ratio": round(hull_ratio, 6),
        "perimeter_px": round(perimeter_px, 2),
        "perimeter_ratio": round(perimeter_ratio, 6),
        "leaf_count": leaf_count,
        "leaf_count_raw": leaf_count_raw,
        "leaf_count_method": leaf_count_method,
        "shoot_count": counts.get("plant", 0) + counts.get("shoot", 0),
        "root_count": counts.get("root", 0),
        "stem_count": counts.get("stem", 0),
        "mean_leaf_area_px": round(mean_leaf_area, 2),
        "leaf_area_cv": round(leaf_area_cv, 4),
        "max_leaf_area_px": round(max_leaf_area, 2),
        "green_pct": round(green_pct, 2),
        "greenness": round(greenness, 4),
        "dark_green_ratio": round(dark_green_ratio, 2),
        "yellow_ratio": round(yellow_pct, 2),
        "brown_ratio": round(brown_pct, 2),
        "healthy_color": round(healthy_color, 2),
        "mean_hue": round(mean_hue, 2),
        "mean_sat": round(mean_sat, 2),
        "mean_val": round(mean_val, 2),
        "glare_score": round(glare_score, 2),
        "condensation_score": round(condensation_score, 2),
        "brightness_mean": round(brightness_mean, 2),
        "brightness_std": round(brightness_std, 2),
        "mean_score": round(mean_score, 4),
        "min_score": round(min_score, 4),
        "score_std": round(score_std, 4),
    }


def analyze_image(model, processor, device, img, filename, species=None):
    masks_by_prompt = {}
    roi = None
    if DETECT_BOTTLE:
        b_masks, _ = segment_prompt(model, processor, device, img, "glass jar bottle")
        if len(b_masks) > 0:
            bb = union_bbox(b_masks.any(axis=0))
            if bb is not None:
                x, y, bw, bh = bb
                roi = np.zeros((np.array(img).shape[0], np.array(img).shape[1]), dtype=bool)
                roi[y:y + bh, x:x + bw] = True
    for prompt in PROMPTS:
        masks_by_prompt[prompt] = segment_prompt(model, processor, device, img, prompt)

    feat = extract_features(img, masks_by_prompt, roi)
    if species is None:
        species = generic_species(filename)
    if USE_SPECIES_THRESHOLDS and species in SPECIES_THRESHOLDS:
        th = SPECIES_THRESHOLDS[species]
    else:
        th = {"ready": COVERAGE_READY, "overdense": COVERAGE_OVERDENSE}  # ค่ากลาง generic

    if DETECT_BOTTLE and roi is None:
        # หาขวดไม่เจอ → ROI ทั้งภาพ → ค่า coverage ไม่น่าเชื่อถือ → กัน verdict ผิด
        verdict = "ROI-ไม่ชัด-ตรวจเอง"
        pass  # หมายเหตุ ROI เพิ่มในส่วน notes ด้านล่าง (กัน notes ยังไม่ถูกนิยาม)
    elif feat["coverage_ratio"] >= th["overdense"]:
        verdict = "หนาแน่นเกิน-ตรวจ"
    elif feat["coverage_ratio"] >= th["ready"]:
        verdict = "พร้อมอนุบาล"
    else:
        verdict = "ยังไม่พร้อม"

    confidence = max(BASE_CONFIDENCE * (1.0 - feat["glare_score"] / 100.0), 0.0)
    readiness_index = (0.4 * min(feat["coverage_ratio"] / max(th["overdense"], 1e-6), 1.0)
                       + 0.3 * min(feat["height_proxy"], 1.0)
                       + 0.3 * min(feat["green_pct"] / 100.0, 1.0))

    notes = []
    if DETECT_BOTTLE and roi is None:
        notes.append("ไม่พบขวด (SAM3) → ROI ทั้งภาพ")
    if feat["leaf_count_method"] == "fallback":
        notes.append("leaf prompt ไม่เจอ → นับใบจาก plant+shoot")
    if feat["glare_score"] > 40:
        notes.append("glare สูง confidence ถูกลด")
    if feat["condensation_score"] > 40:
        notes.append("ภาพมัว/ฝ้า ตรวจผลระวัง")
    if feat["leaf_count"] == 0 and feat["coverage_ratio"] > 0.05:
        notes.append("มี coverage แต่ไม่พบใบ")
    if feat["yellow_ratio"] > 30:
        notes.append("ใบเหลืองมาก")

    warnings = []
    if feat["glare_score"] > 40:
        warnings.append("glare")
    if feat["condensation_score"] > 40:
        warnings.append("condensation")
    quality_warning = "|".join(warnings)

    feat.update({
        "image": filename,
        "species": species,
        "verdict": verdict,
        "readiness_index": round(readiness_index, 4),
        "confidence": round(confidence, 4),
        "quality_warning": quality_warning,
        "note": " | ".join(notes),
    })
    return feat, masks_by_prompt


def draw_synthetic_plant(n_leaves, H=400, W=400, seed=0):
    rng = np.random.default_rng(seed)
    canvas = np.full((H, W, 3), 250, dtype=np.uint8)
    gt_mask = np.zeros((H, W), dtype=bool)
    base_y = H - 60
    cv2.line(canvas, (W // 2, base_y), (W // 2, 120), (40, 110, 40), 6)
    gt_mask[110:base_y + 3, W // 2 - 3:W // 2 + 4] = True
    for i in range(n_leaves):
        cx = int(W // 2 + rng.integers(-90, 90))
        cy = int(130 + rng.integers(0, 190))
        rx = int(rng.integers(20, 45))
        ry = int(rng.integers(14, 30))
        angle = float(rng.integers(0, 180))
        col = (int(rng.integers(30, 60)), int(rng.integers(140, 190)), int(rng.integers(30, 60)))
        em = np.zeros((H, W), dtype=np.uint8)
        cv2.ellipse(em, (cx, cy), (rx, ry), angle, 0, 360, 255, -1)
        canvas[em > 0] = col
        gt_mask |= em > 0
    return Image.fromarray(canvas), gt_mask


def synthetic_benchmark(model, processor, device, data_dir, out_dir, n=5):
    global DETECT_BOTTLE
    _db = DETECT_BOTTLE
    DETECT_BOTTLE = False  # ภาพจำลองไม่มีขวด — benchmark ใช้ ROI ทั้งภาพ
    syn_dir = os.path.join(data_dir, "synthetic")
    os.makedirs(syn_dir, exist_ok=True)
    syn_rows = []
    leaf_vals = [3, 5, 7, 9, 12][:n]
    for i, nl in enumerate(leaf_vals):
        img, gt = draw_synthetic_plant(nl, seed=i * 7 + 1)
        name = f"synth_{i:03d}_leaf{nl}.png"
        img.save(os.path.join(syn_dir, name))
        ys, xs = np.where(gt)
        syn_rows.append({"image": name, "true_leaf_count": nl,
                         "true_area_px": int(gt.sum()),
                         "true_height_px": int(ys.max() - ys.min()) + 1})
    syn_gt = pd.DataFrame(syn_rows)

    rows = []
    masks_store = {}
    for _, r in syn_gt.iterrows():
        img = Image.open(os.path.join(syn_dir, r["image"])).convert("RGB")
        feat, mbp = analyze_image(model, processor, device, img, r["image"])
        rows.append(feat)
        masks_store[r["image"]] = mbp
    syn_df = pd.DataFrame(rows)
    bm = syn_df.merge(syn_gt, on="image", suffixes=("_sam3", "_true"))

    bm["leaf_err"] = (bm["leaf_count"] - bm["true_leaf_count"]).abs()
    count_mae = float(bm["leaf_err"].mean())
    count_rmse = float((bm["leaf_err"] ** 2).mean() ** 0.5)

    ious, dices = [], []
    for idx, r in bm.iterrows():
        union = np.zeros((400, 400), dtype=bool)
        for p in ("plant", "leaf"):
            m = masks_store[r["image"]].get(p, (np.zeros((0, 400, 400), dtype=bool), None))[0]
            if len(m) > 0:
                union |= m.any(axis=0)
        _, gt = draw_synthetic_plant(int(r["true_leaf_count"]), seed=idx * 7 + 1)
        inter = int((union & gt).sum())
        iou = inter / max(int((union | gt).sum()), 1)
        dice = 2 * inter / max(int(union.sum()) + int(gt.sum()), 1)
        ious.append(iou)
        dices.append(dice)

    bm["area_ratio"] = bm["total_area_px"] / bm["true_area_px"].clip(lower=1)
    report = bm[["image", "true_leaf_count", "leaf_count", "leaf_err",
                 "true_area_px", "total_area_px", "area_ratio"]].copy()
    report["iou"] = np.round(ious, 4)
    report["dice"] = np.round(dices, 4)
    report.loc["MEAN"] = report[["leaf_err", "area_ratio", "iou", "dice"]].mean().round(4)
    out_csv = os.path.join(out_dir, "benchmark_IoU_Dice_MAE.csv")
    report.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print("=== SYNTHETIC BENCHMARK (ภาพจำลอง known-truth — พิสูจน์ pipeline ไม่ใช่ข้อมูลแล็บจริง) ===")
    print(report.to_string())
    print(f"Leaf count MAE = {count_mae:.2f} / RMSE = {count_rmse:.2f} | mIoU = {np.mean(ious):.3f} | mDice = {np.mean(dices):.3f}")
    print(f"บันทึก: {out_csv}")
    DETECT_BOTTLE = _db


def _setup_thai_font():
    """ลงทะเบียนฟองต์ไทยให้ matplotlib (Noto Sans Thai บน Colab / Tahoma บน Windows)"""
    import matplotlib.font_manager as fm
    cands = []
    for f in fm.findSystemFonts():
        if "thai" in os.path.basename(f).lower():
            cands.append(f)
    for pref in ["NotoSansThai", "Tahoma", "LeelawadeeUI", "AngsanaNew", "THSarabun"]:
        for f in fm.findSystemFonts():
            if os.path.basename(f).startswith(pref):
                cands.append(f)
                break
    for f in cands:
        try:
            fm.fontManager.addfont(f)
            plt.rcParams["font.family"] = fm.FontProperties(fname=f).get_name()
            print(f"[INFO] ใช้ฟอนต์ไทย: {os.path.basename(f)}")
            return
        except Exception:
            continue


def build_report(df, images, all_masks, out_dir):
    """สร้าง overlay PNG (6 ภาพแรก) + กราฟ PNG + report.html ฝังรูปทั้งหมด"""
    import base64
    import shutil
    import time

    _setup_thai_font()
    os.makedirs(os.path.join(out_dir, "overlays"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "plots"), exist_ok=True)

    overlay_paths = []
    for k, name in enumerate(list(images)[:6]):
        n = 1 + len(PROMPTS)
        fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 4.2))
        axes[0].imshow(images[name])
        axes[0].set_title("ต้นฉบับ")
        axes[0].axis("off")
        for i, p in enumerate(PROMPTS):
            masks, _ = all_masks[name][p]
            ov = draw_overlay(images[name], masks, COLORS.get(p, (0, 200, 0)))
            axes[i + 1].imshow(ov)
            axes[i + 1].set_title(f"{p} — {len(masks)} mask")
            axes[i + 1].axis("off")
        plt.suptitle(name, fontsize=12)
        plt.tight_layout()
        png = os.path.join(out_dir, "overlays", f"overlay_{k + 1:02d}_{name}")
        fig.savefig(png, dpi=120, bbox_inches="tight")
        plt.close(fig)
        overlay_paths.append(png)

    plot_paths = []
    dims = pd.DataFrame(index=df["image"])
    dims["โครงสร้าง"] = (df["coverage_ratio"] + df["height_proxy"]) / 2
    dims["ความซับซ้อน"] = df["hull_ratio"]
    dims["สีสุขภาพ"] = df["green_pct"] / 100.0
    dims["อวัยวะ"] = np.clip((df["leaf_count"] + df["shoot_count"]) / 10.0, 0, 1)
    mean_dims = dims.mean()

    labels = list(mean_dims.index)
    values = list(mean_dims.values) + [list(mean_dims.values)[0]]
    angles = [i * 2 * math.pi / len(labels) for i in range(len(labels))] + [0]
    fig1 = plt.figure(figsize=(6, 6))
    ax1 = fig1.add_subplot(111, polar=True)
    ax1.plot(angles, values, "o-", linewidth=2, color="seagreen")
    ax1.fill(angles, values, alpha=0.25, color="seagreen")
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(labels)
    ax1.set_ylim(0, 1)
    ax1.set_title("ค่าเฉลี่ย 4 มิติของทุกภาพ (0-1)")
    plt.tight_layout()
    p1 = os.path.join(out_dir, "plots", "radar_4dim.png")
    fig1.savefig(p1, dpi=200, bbox_inches="tight")
    plt.close(fig1)
    plot_paths.append(p1)

    fig2, axes2 = plt.subplots(1, 2, figsize=(13, 5))
    axes2[0].bar(df["image"], df["green_pct"], color="seagreen")
    axes2[0].set_title("Plant Health Index (% Green ภายใน mask)")
    axes2[0].set_ylabel("%")
    axes2[0].set_ylim(0, 100)
    axes2[0].tick_params(axis="x", rotation=60, labelsize=7)
    axes2[1].scatter(df["leaf_count"], df["green_pct"], s=60, color="green")
    axes2[1].set_xlabel("Leaf Count (SAM3)")
    axes2[1].set_ylabel("Green Coverage (%)")
    axes2[1].set_title("Leaf Count vs Green")
    plt.tight_layout()
    p2 = os.path.join(out_dir, "plots", "green_bar_scatter.png")
    fig2.savefig(p2, dpi=200, bbox_inches="tight")
    plt.close(fig2)
    plot_paths.append(p2)

    sel = ["coverage_ratio", "height_proxy", "width_proxy", "compactness", "leaf_count",
           "shoot_count", "root_count", "green_pct", "yellow_ratio", "hull_ratio", "readiness_index"]
    cm = df[sel].corr()
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    im = ax3.imshow(cm, cmap="coolwarm", vmin=-1, vmax=1)
    ax3.set_xticks(range(len(cm)))
    ax3.set_xticklabels(cm.columns, rotation=45, ha="right")
    ax3.set_yticks(range(len(cm)))
    ax3.set_yticklabels(cm.columns)
    for i in range(len(cm)):
        for j in range(len(cm)):
            ax3.text(j, i, f"{cm.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
    plt.colorbar(im)
    ax3.set_title("Correlation ระหว่าง feature")
    plt.tight_layout()
    p3 = os.path.join(out_dir, "plots", "feature_heatmap.png")
    fig3.savefig(p3, dpi=200, bbox_inches="tight")
    plt.close(fig3)
    plot_paths.append(p3)

    fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5))
    vc = df["verdict"].value_counts()
    axes4[0].pie(vc.values, labels=vc.index, autopct="%1.0f%%", startangle=90,
                 colors=["#d9534f", "#5cb85c", "#f0ad4e"])
    axes4[0].set_title("สัดส่วน verdict")
    axes4[1].hist(df["readiness_index"], bins=15, color="steelblue", edgecolor="white")
    axes4[1].axvline(0.5, color="red", ls="--", lw=1.5)
    axes4[1].set_title("การกระจาย readiness_index (เส้นแดง = 0.5)")
    axes4[1].set_xlabel("readiness_index")
    plt.tight_layout()
    p4 = os.path.join(out_dir, "plots", "verdict_pie_hist.png")
    fig4.savefig(p4, dpi=200, bbox_inches="tight")
    plt.close(fig4)
    plot_paths.append(p4)

    def img_b64(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()

    main_cols = ["image", "verdict", "readiness_index", "coverage_ratio", "leaf_count",
                 "shoot_count", "green_pct", "yellow_ratio", "confidence", "note"]
    thead = "<tr><th>#</th>" + "".join(f"<th>{c}</th>" for c in main_cols) + "</tr>"
    trows = ""
    for k, (_, r) in enumerate(df.sort_values("readiness_index", ascending=False).iterrows(), 1):
        trows += "<tr><td>{}</td>{}</tr>".format(
            k, "".join("<td>{}</td>".format("" if pd.isna(r[c]) else r[c]) for c in main_cols))

    html = (
        '<html><head><meta charset="utf-8"><title>รายงานวิเคราะห์การเจริญพืช (SAM3)</title>'
        '<style>body{font-family:Tahoma,sans-serif;margin:30px}h1{color:#1a7a4f}'
        'table{border-collapse:collapse}td,th{border:1px solid #999;padding:3px 8px;font-size:12px}'
        'img{max-width:100%;border:1px solid #ccc;margin:6px 0}'
        'h2{border-bottom:2px solid #1a7a4f;padding-bottom:4px;margin-top:40px}</style></head><body>'
        f"<h1>รายงานวิเคราะห์การเจริญพืชเพาะเลี้ยงเนื้อเยื่อ (SAM3)</h1>"
        f"<p>จำนวนภาพ: {len(df)} | สร้างเมื่อ: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>"
        f"<p><b>verdict:</b> {df['verdict'].value_counts().to_dict()}</p>"
        "<table>" + thead + trows + "</table>"
        "<h2>ภาพ overlay ตัวอย่าง</h2>"
        + "".join(f'<p><b>{os.path.basename(p)}</b></p><img src="{img_b64(p)}">' for p in overlay_paths)
        + "<h2>กราฟวิเคราะห์</h2>"
        + "".join(f'<img src="{img_b64(p)}">' for p in plot_paths)
        + "</body></html>"
    )
    report_path = os.path.join(out_dir, "report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    zip_path = os.path.join(out_dir, "..", "vitro_report.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    shutil.make_archive(zip_path[:-4], "zip", out_dir)
    print(f"[INFO] สร้าง: {out_dir}/ (CSV/XLSX/report.html/overlays/plots) + {zip_path}")


def main():
    parser = argparse.ArgumentParser(description="SAM3 plant tissue culture growth analysis (multi-dim)")
    parser.add_argument("--data", default="/content/data", help="โฟลเดอร์ภาพต้นฉบับ")
    parser.add_argument("--out", default="/content/results", help="โฟลเดอร์ผลลัพธ์")
    parser.add_argument("--synthetic", action="store_true", help="รัน synthetic benchmark เพิ่ม (ไม่ต้องมี ground truth)")
    parser.add_argument("--config", default=None, help="ไฟล์ config.json (PIXEL_TO_CM/threshold/prompts)")
    args = parser.parse_args()

    load_config(args.config)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Execution Device: {device}")
    if device == "cpu":
        raise SystemExit("ต้องใช้ GPU — facebook/sam3 ไม่รองรับ CPU")

    from transformers import Sam3Processor, Sam3Model
    start = time.time()
    model = Sam3Model.from_pretrained("facebook/sam3").to(device)
    processor = Sam3Processor.from_pretrained("facebook/sam3")
    print(f"[INFO] โหลดโมเดลเสร็จใน {time.time() - start:.1f} วินาที")

    images = load_images(args.data)
    if not images:
        raise SystemExit(f"ไม่พบภาพใน {args.data}")
    print(f"[INFO] โหลดภาพ {len(images)} ภาพ")

    os.makedirs(args.out, exist_ok=True)
    species_map = {}
    sp_csv = os.path.join(args.data, "species_map.csv")
    if os.path.exists(sp_csv):
        _sp = pd.read_csv(sp_csv)
        species_map = dict(zip(_sp["image"].astype(str), _sp["species"].astype(str)))
        print(f"[INFO] โหลด species_map.csv — {len(species_map)} รายการ")
    rows = []
    all_masks = {}
    progress_path = os.path.join(args.out, "_progress.csv")
    total = len(images)
    for i, (name, img) in enumerate(images.items(), 1):
        feat, mbp = analyze_image(model, processor, device, img, name, species=species_map.get(name))
        all_masks[name] = mbp
        rows.append(feat)
        # checkpoint รายภาพ — กัน Colab timeout/ค้าง กลางทาง
        pd.DataFrame(rows).to_csv(progress_path, index=False, encoding="utf-8-sig")
        print(f"  [{i}/{total}] {name} — leaf={feat['leaf_count']} shoot={feat['shoot_count']} "
              f"cov={feat['coverage_ratio']:.2f} green={feat['green_pct']:.0f}% {feat['verdict']}")
    df = pd.DataFrame(rows)

    csv_path = os.path.join(args.out, "plant_growth_summary.csv")
    xlsx_path = os.path.join(args.out, "plant_growth_summary.xlsx")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)
    print(f"[INFO] บันทึก: {csv_path} / {xlsx_path}")

    # สรุปแยกชนิดพืช (งานหลายชนิด — ดูค่าเฉลี่ย/การกระจาย verdict ต่อชนิด)
    if "species" in df.columns and df["species"].nunique() > 1:
        sp_sum = df.groupby("species").agg(
            n=("image", "count"),
            coverage_mean=("coverage_ratio", "mean"),
            leaf_mean=("leaf_count", "mean"),
            shoot_mean=("shoot_count", "mean"),
            green_mean=("green_pct", "mean"),
            ready_pct=("verdict", lambda s: (s == "พร้อมอนุบาล").mean() * 100),
        ).reset_index()
        sp_path = os.path.join(args.out, "species_summary.csv")
        sp_sum.to_csv(sp_path, index=False, encoding="utf-8-sig")
        print("=== สรุปแยกชนิด ===")
        print(sp_sum.to_markdown(index=False))
        print(f"บันทึก: {sp_path}")


    build_report(df, images, all_masks, args.out)

    show_cols = ["image", "species", "leaf_count", "shoot_count", "root_count", "stem_count",
                 "coverage_ratio", "height_proxy", "green_pct", "yellow_ratio", "hull_ratio",
                 "readiness_index", "confidence", "quality_warning", "verdict", "note"]
    print(df[show_cols].to_markdown(index=False))

    pairs = [("leaf_count", "coverage_ratio"), ("leaf_count", "shoot_count"),
             ("coverage_ratio", "height_proxy"), ("green_pct", "healthy_color"),
             ("coverage_ratio", "total_area_px")]
    print("=== SANITY CHECK (Pearson r บนภาพจริง — ค่าบวกสมเหตุผล = ข้อมูลสอดคล้อง) ===")
    for a, b in pairs:
        r = df[a].astype(float).corr(df[b].astype(float))
        print(f"  {a} ~ {b}: r = {r:.3f}")

    gt_path = os.path.join(args.data, "ground_truth.csv")
    if os.path.exists(gt_path):
        gt = pd.read_csv(gt_path)
        m = df.merge(gt, on="image", suffixes=("_sam3", "_manual"))
        feature_map = {"leaf_count": "leaf_count", "shoot_count": "shoot_count",
                       "root_count": "root_count", "height_proxy": "height_cm",
                       "width_proxy": "width_cm", "total_area_px": "area_cm2"}
        results = []
        for f_sam, f_manual in feature_map.items():
            if f_manual not in m.columns:
                continue
            a = m[f_sam].astype(float)
            b = m[f_manual].astype(float)
            r = a.corr(b)
            if pd.isna(r):
                r = 0.0
            results.append({"feature_SAM3": f_sam, "manual_GT": f_manual,
                            "pearson_r": round(r, 4), "MAE": round(float((a - b).abs().mean()), 4),
                            "RMSE": round(float((((a - b) ** 2).mean()) ** 0.5), 4), "n": len(m)})
        val = pd.DataFrame(results)
        val_path = os.path.join(args.out, "validation_metrics.csv")
        val.to_csv(val_path, index=False, encoding="utf-8-sig")
        print("=== VALIDATION vs GROUND TRUTH ===")
        print(val.to_markdown(index=False))
        print(f"บันทึก: {val_path}")
    else:
        print("[INFO] ไม่พบ ground_truth.csv — ใช้ --synthetic เพื่อพิสูจน์ความตรงแทน")

    if args.synthetic:
        synthetic_benchmark(model, processor, device, args.data, args.out)


if __name__ == "__main__":
    main()
