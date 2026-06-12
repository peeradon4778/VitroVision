"""Plant phenotyping จากภาพขวด tissue culture
- Classic CV: ทำงานได้ทันที ไม่ต้องมี model
- YOLOv8-seg: ทำงานอัตโนมัติเมื่อมี models/phenotype/seg.pt
"""
import cv2
import numpy as np
from pathlib import Path

SEG_MODEL_PATH = Path(__file__).parent.parent / 'models' / 'phenotype' / 'seg.pt'

_seg_model = None
_seg_mtime = 0.0


def _load_seg():
    global _seg_model, _seg_mtime
    if not SEG_MODEL_PATH.exists():
        _seg_model = None
        return
    t = SEG_MODEL_PATH.stat().st_mtime
    if t == _seg_mtime:
        return
    try:
        from ultralytics import YOLO
        _seg_model = YOLO(str(SEG_MODEL_PATH))
        _seg_mtime = t
        print(f'[phenotyper] โหลด YOLOv8-seg model ใหม่')
    except Exception as e:
        print(f'[phenotyper] โหลด seg ไม่ได้: {e}')
        _seg_model = None


def _glcm_features(gray: np.ndarray, levels: int = 16) -> tuple[float, float]:
    """GLCM contrast/homogeneity (horizontal offset, symmetric)
    numpy ล้วน — ไม่ต้องพึ่ง scikit-image
    contrast สูง → พื้นผิวหยาบ/ตัดกันมาก; homogeneity สูง → เรียบสม่ำเสมอ
    """
    q = np.clip(gray.astype(np.int32) * levels // 256, 0, levels - 1)
    left, right = q[:, :-1].ravel(), q[:, 1:].ravel()
    glcm = np.zeros((levels, levels), dtype=np.float64)
    np.add.at(glcm, (left, right), 1.0)
    glcm += glcm.T                      # symmetric (ซ้าย↔ขวา)
    s = glcm.sum()
    if s == 0:
        return 0.0, 0.0
    p = glcm / s
    i = np.arange(levels).reshape(-1, 1)
    j = np.arange(levels).reshape(1, -1)
    contrast    = float(np.sum(p * (i - j) ** 2))
    homogeneity = float(np.sum(p / (1.0 + np.abs(i - j))))
    return round(contrast, 4), round(homogeneity, 4)


def _classic_cv(bgr: np.ndarray) -> dict:
    """วิเคราะห์ด้วย HSV color segmentation — ไม่ต้องมี model"""
    h, w = bgr.shape[:2]

    # crop เฉพาะส่วนกลางขวด (หลีกเลี่ยง label + ฝา + ขอบ)
    roi = bgr[int(h * 0.08):int(h * 0.92), int(w * 0.05):int(w * 0.95)]
    roi_h, roi_w = roi.shape[:2]
    roi_area = roi_h * roi_w

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Green mask: Hue 35–90° (เขียว–เหลืองเขียว), ตัด background ขาว/มืด
    mask = cv2.inRange(hsv,
                       np.array([35, 35, 35]),
                       np.array([90, 255, 235]))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
    mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # ── Green coverage % ──────────────────────────────────────
    green_px      = int(mask.sum() // 255)
    green_coverage = round(green_px / roi_area * 100, 2)

    # ── Leaf Color Index (LCI) ────────────────────────────────
    # LCI = mean(G) / mean(R) ของ pixel ที่เป็นสีเขียว
    # healthy deep green → G สูง R ต่ำ → LCI > 1.5
    # yellowing/stress → G ≈ R → LCI ≈ 1.0
    if green_px > 50:
        b_ch = roi[:, :, 0].astype(float)[mask > 0]
        g_ch = roi[:, :, 1].astype(float)[mask > 0]
        r_ch = roi[:, :, 2].astype(float)[mask > 0]
        mean_r = r_ch.mean() + 1e-6
        mean_g = g_ch.mean()
        lci = round(float(mean_g / mean_r), 4)
    else:
        lci = 0.0

    # ── Media color ───────────────────────────────────────────
    # ดูส่วนล่าง 20% ของขวด (ที่เป็น media เลี้ยงเชื้อ)
    bottom    = bgr[int(h * 0.72):int(h * 0.90), int(w * 0.1):int(w * 0.9)]
    bottom_h  = cv2.cvtColor(bottom, cv2.COLOR_BGR2HSV)
    mean_sat  = float(bottom_h[:, :, 1].mean())
    mean_hue  = float(bottom_h[:, :, 0].mean())

    if mean_sat < 25:
        media_color = 'clear'
    elif 15 <= mean_hue <= 35:
        media_color = 'yellow'
    elif mean_hue > 35:
        media_color = 'brown'
    else:
        media_color = 'normal'

    # ── Shoot count (approximate) ─────────────────────────────
    min_blob = max(int(roi_area * 0.003), 30)
    _, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    shoots = sum(1 for i in range(1, len(stats))
                 if stats[i, cv2.CC_STAT_AREA] >= min_blob)

    # ── Texture entropy ────────────────────────────────────────
    # Shannon entropy ของ grayscale ROI
    # สูง → พื้นผิวซับซ้อน (contamination/callus)
    # ต่ำ → เรียบ (media ใส / ไม่มีการเจริญ)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
    hist_norm = hist / (hist.sum() + 1e-6)
    nonzero = hist_norm[hist_norm > 0]
    texture_entropy = round(float(-np.sum(nonzero * np.log2(nonzero))), 4)

    # ── Brown coverage % ──────────────────────────────────────
    # ตรวจ contamination สีน้ำตาล/ส้มในขวด
    brown_mask = cv2.inRange(hsv,
                             np.array([5,  40, 40]),
                             np.array([25, 255, 200]))
    brown_mask = cv2.morphologyEx(brown_mask, cv2.MORPH_OPEN, kernel)
    brown_px = int(brown_mask.sum() // 255)
    brown_coverage = round(brown_px / roi_area * 100, 2)

    # ── Vigor score (0–10) ────────────────────────────────────
    # คะแนนสุขภาพรวม — ใช้เปรียบเทียบระหว่างสูตร
    # green_coverage: 0–40% → 0–5 คะแนน
    # lci: 1.0–2.5 → 0–3 คะแนน
    # brown penalty: ลดตาม brown_coverage
    green_score = min(green_coverage / 8.0, 5.0)
    lci_score   = min(max((lci - 1.0) / 0.5, 0.0), 3.0)
    brown_penalty = min(brown_coverage / 5.0, 3.0)
    vigor_score = round(max(green_score + lci_score - brown_penalty, 0.0), 2)

    # ── Morphological & color-index traits (research 14) ──────
    # หมายเหตุ: green_coverage_pct = projected leaf area (normalized) อยู่แล้ว

    # Convex Hull Ratio (solidity) = plant_area / hull_area
    # ต่ำ → ทรงกระจาย/หลายยอดแยก, สูง(→1) → กระจุกแน่น (จับ shoot architecture)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours and green_px > 50:
        hull_area = cv2.contourArea(cv2.convexHull(np.vstack(contours)))
        convex_hull_ratio = round(min(green_px / hull_area, 1.0), 4) if hull_area > 0 else 0.0
    else:
        convex_hull_ratio = 0.0

    # ExG / VARI — vegetation color indices (threshold-free, ทนต่อแสง)
    # ใช้ normalized chromatic coords → bounded + robust กว่า HSV threshold
    bf = roi[:, :, 0].astype(np.float32)
    gf = roi[:, :, 1].astype(np.float32)
    rf = roi[:, :, 2].astype(np.float32)
    tot = bf + gf + rf + 1e-6
    rn, gn, bn = rf / tot, gf / tot, bf / tot
    exg_mean  = round(float((2.0 * gn - rn - bn).mean()), 4)
    vari      = (gn - rn) / (gn + rn - bn + 1e-6)
    vari_mean = round(float(np.clip(vari, -1.0, 1.0).mean()), 4)

    # GLCM texture (contrast/homogeneity) — ละเอียดกว่า Shannon entropy เดิม
    glcm_contrast, glcm_homogeneity = _glcm_features(gray)

    return {
        'green_coverage_pct': green_coverage,
        'leaf_color_index':   lci,
        'shoot_count_cv':     shoots,
        'media_color_cv':     media_color,
        'texture_entropy':    texture_entropy,
        'brown_coverage_pct': brown_coverage,
        'vigor_score':        vigor_score,
        'convex_hull_ratio':  convex_hull_ratio,
        'exg_mean':           exg_mean,
        'vari_mean':          vari_mean,
        'glcm_contrast':      glcm_contrast,
        'glcm_homogeneity':   glcm_homogeneity,
        'method':             'classic_cv',
    }


def _yolov8_seg(bgr: np.ndarray) -> dict | None:
    """segmentation ด้วย YOLOv8-seg — คืน None ถ้าไม่สำเร็จ"""
    if _seg_model is None:
        return None
    try:
        results = _seg_model(bgr, verbose=False)[0]
        h, w    = bgr.shape[:2]

        # รวม mask ทุก instance
        plant_mask = np.zeros((h, w), dtype=np.uint8)
        if results.masks is not None:
            for mask_data in results.masks.data.cpu().numpy():
                m = cv2.resize((mask_data * 255).astype(np.uint8), (w, h))
                plant_mask = np.maximum(plant_mask, m)

        # Green coverage
        total_px      = h * w
        plant_px      = int((plant_mask > 127).sum())
        green_coverage = round(plant_px / total_px * 100, 2)

        # LCI จาก segmented pixels
        b_ch = bgr[:, :, 0].astype(float)[plant_mask > 127]
        g_ch = bgr[:, :, 1].astype(float)[plant_mask > 127]
        r_ch = bgr[:, :, 2].astype(float)[plant_mask > 127]
        if len(r_ch) > 50:
            lci = round(float(g_ch.mean() / (r_ch.mean() + 1e-6)), 4)
        else:
            lci = 0.0

        # Shoot count จาก YOLO instances
        shoot_count = len(results.boxes) if results.boxes is not None else 0

        # Media color (ยังใช้ classic CV ในส่วนนี้)
        classic = _classic_cv(bgr)

        return {
            'green_coverage_pct': green_coverage,
            'leaf_color_index':   lci,
            'shoot_count_cv':     shoot_count,
            'media_color_cv':     classic['media_color_cv'],
            'texture_entropy':    classic['texture_entropy'],
            'brown_coverage_pct': classic['brown_coverage_pct'],
            'vigor_score':        classic['vigor_score'],
            'convex_hull_ratio':  classic['convex_hull_ratio'],
            'exg_mean':           classic['exg_mean'],
            'vari_mean':          classic['vari_mean'],
            'glcm_contrast':      classic['glcm_contrast'],
            'glcm_homogeneity':   classic['glcm_homogeneity'],
            'method':             'yolov8_seg',
        }
    except Exception as e:
        print(f'[phenotyper] seg inference ไม่สำเร็จ: {e}')
        return None


def measure(image_bytes: bytes) -> dict:
    """วัด phenotyping parameters — คืน dict หรือ {} ถ้าภาพอ่านไม่ได้

    Returns:
        green_coverage_pct  float  % พื้นที่สีเขียว = projected leaf area (normalized)
        leaf_color_index    float  G/R ratio (healthy ≈ 1.5–2.5, stress ≈ 0.8–1.2)
        shoot_count_cv      int    จำนวนยอดโดยประมาณ
        media_color_cv      str    clear / normal / yellow / brown
        texture_entropy     float  Shannon entropy ของ grayscale (สูง = ซับซ้อน/contamination)
        brown_coverage_pct  float  % พื้นที่สีน้ำตาล (contamination indicator)
        vigor_score         float  คะแนนสุขภาพรวม 0–10 (เปรียบเทียบระหว่างสูตรได้)
        convex_hull_ratio   float  solidity = plant/hull area (ต่ำ=กระจาย, สูง=กระจุก)
        exg_mean            float  Excess Green index เฉลี่ย (threshold-free greenness)
        vari_mean           float  VARI เฉลี่ย (vegetation index ทนแสง, -1..1)
        glcm_contrast       float  GLCM contrast (พื้นผิวหยาบ/ตัดกัน)
        glcm_homogeneity    float  GLCM homogeneity (พื้นผิวเรียบสม่ำเสมอ)
        method              str    classic_cv หรือ yolov8_seg
    """
    arr = np.frombuffer(image_bytes, np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        return {}

    _load_seg()
    result = _yolov8_seg(bgr) if _seg_model is not None else None
    return result if result is not None else _classic_cv(bgr)


def seg_model_ready() -> bool:
    _load_seg()
    return _seg_model is not None
