# -*- coding: utf-8 -*-
"""
VitroVision — Gradio Space: scan a plant in a tissue-culture bottle via webcam (or upload an image).
Segments the plant from the glass with a distilled U-Net (from SAM3), then computes
non-destructive traits and an acclimatization-readiness estimate.

Honesty notes:
  - The model is trained from SAM3 pseudo-labels (full human ground-truth not ready yet) -> prototype.
  - Displayed values (coverage / height_proxy / verdict) use the WHOLE frame as ROI (no bottle ROI)
    -> demo-scale numbers, not calibrated to the 100-bottle validation set.
  - If the model is not found (Colab training not run yet), a temporary classical-green segmentation
    is used and clearly labelled.

UI is intentionally English to avoid Thai font rendering issues (cv2.putText + some web fonts).

Run locally:
    python space/app.py            # http://127.0.0.1:7860 (after `pip install gradio torch opencv-python pillow huggingface_hub`)
"""
import os
import numpy as np
import cv2
import torch
import torch.nn as nn

# ---------------------------------------------------------------- model config (architecture copied from train_unet_distill.py)
MODEL_REPO = os.environ.get("VV_MODEL_REPO", "peeradon4778/vitrovision-unet-small")
IMG_SIZE = int(os.environ.get("VV_IMG_SIZE", "256"))
READY_HEIGHT = float(os.environ.get("VV_READY_HEIGHT", "0.275"))
BASE_CONFIDENCE = float(os.environ.get("VV_BASE_CONFIDENCE", "0.80"))
_LOWER_GREEN = np.array([35, 40, 40], dtype=np.int32)
_UPPER_GREEN = np.array([85, 255, 255], dtype=np.int32)


class DoubleConv(nn.Module):
    def __init__(self, cin, cout):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(cin, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True),
            nn.Conv2d(cout, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True))

    def forward(self, x):
        return self.block(x)


class UNetSmall(nn.Module):
    """Small U-Net: channels [16,32,64,128,256] ~2M params"""
    def __init__(self, in_ch=3, out_ch=1, base=16):
        super().__init__()
        c = [base * (2 ** i) for i in range(5)]
        self.enc = nn.ModuleList([DoubleConv(in_ch, c[0])] +
                                 [DoubleConv(c[i], c[i + 1]) for i in range(4)])
        self.pool = nn.MaxPool2d(2)
        self.up = nn.ModuleList([nn.ConvTranspose2d(c[i + 1], c[i], 2, stride=2) for i in range(4)])
        self.dec = nn.ModuleList([DoubleConv(c[i] * 2, c[i]) for i in range(4)])
        self.head = nn.Conv2d(c[0], out_ch, 1)

    def forward(self, x):
        skips = []
        for i, block in enumerate(self.enc):
            x = block(x)
            if i < 4:
                skips.append(x)
                x = self.pool(x)
        for i in range(4):
            x = self.up[3 - i](x)
            x = torch.cat([x, skips[3 - i]], dim=1)
            x = self.dec[3 - i](x)
        return torch.sigmoid(self.head(x))


# ---------------------------------------------------------------- model loading
def _try_load_state(path):
    sd = torch.load(path, map_location="cpu")
    m = UNetSmall()
    m.load_state_dict(sd)
    m.eval()
    return m


def load_model():
    """Try to load the real model: local .pt -> HF repo. On failure return (None, reason)."""
    for p in ("./vitrovision_unet.pt", "./unet_model.pt", "./pytorch_model.bin"):
        if os.path.exists(p):
            try:
                return _try_load_state(p), f"Model: local file {p}"
            except Exception as e:  # noqa: BLE001
                print(f"[warn] failed to load {p}: {e}")
    # download from HF model repo
    try:
        from huggingface_hub import hf_hub_download
        bpath = hf_hub_download(repo_id=MODEL_REPO, filename="pytorch_model.bin")
        return _try_load_state(bpath), f"Model: HF '{MODEL_REPO}' (distilled from SAM3)"
    except Exception as e:  # noqa: BLE001
        print(f"[warn] no model from HF ({MODEL_REPO}): {e}")
        return None, "Model not found - using temporary classical-green segmentation (train + push the model to go live)"

MODEL, MODEL_NOTE = load_model()


# ---------------------------------------------------------------- features from mask (ROI = whole frame)
def _union_bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    return x0, y0, x1 - x0 + 1, y1 - y0 + 1  # x,y,w,h


def segment_and_analyze(rgb, model=None):
    """rgb: HxWx3 uint8 (RGB). Returns (overlay_rgb uint8, metrics dict, model_note)."""
    H, W = rgb.shape[:2]
    model_note = MODEL_NOTE

    if model is not None:
        inp = cv2.resize(rgb, (IMG_SIZE, IMG_SIZE)).astype(np.float32) / 255.0
        x = torch.from_numpy(inp.transpose(2, 0, 1)).float().unsqueeze(0)  # 1,3,S,S
        with torch.no_grad():
            prob = model(x)[0, 0].numpy()  # S,S
        mask_small = prob > 0.5
        mask = cv2.resize(mask_small.astype(np.uint8) * 255, (W, H),
                          interpolation=cv2.INTER_NEAREST) > 0
        seg_method = "U-Net (distilled from SAM3)"
    else:
        # fallback: direct green (classical) - so the Space works while the model is pending
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        green = cv2.inRange(hsv, _LOWER_GREEN.astype(np.uint8), _UPPER_GREEN.astype(np.uint8)) > 0
        green = cv2.morphologyEx(green.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = green > 0
        seg_method = "classical-green (temporary - model pending)"

    area_px = int(mask.sum())
    coverage = area_px / (H * W)
    bb = _union_bbox(mask)
    if bb:
        _, _, bw, bh = bb
        height_proxy = bh / H
        width_proxy = bw / W
        compactness = area_px / (bh * bw + 1e-6)
    else:
        height_proxy = width_proxy = compactness = 0.0
        bh = bw = 0

    # color / health inside the mask
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    green_in = cv2.inRange(hsv, _LOWER_GREEN.astype(np.uint8), _UPPER_GREEN.astype(np.uint8)) > 0
    green_pct = 100.0 * int((green_in & mask).sum()) / max(area_px, 1)
    yellow_in = cv2.inRange(hsv, np.array([20, 60, 60], np.uint8), np.array([35, 255, 255], np.uint8)) > 0
    brown_in = cv2.inRange(hsv, np.array([8, 40, 40], np.uint8), np.array([20, 180, 120], np.uint8)) > 0
    yellow_pct = 100.0 * int((yellow_in & mask).sum()) / max(area_px, 1)
    brown_pct = 100.0 * int((brown_in & mask).sum()) / max(area_px, 1)

    # number of plant clumps (connected components large enough)
    num, lab, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8) * 255, connectivity=8)
    region_count = sum(1 for i in range(1, num) if stats[i, cv2.CC_STAT_AREA] > 0.005 * area_px)

    # glare / condensation (for confidence)
    glare_score = 100.0 * int(((hsv[..., 2] > 217) & (hsv[..., 1] < 38)).sum()) / (H * W)
    condensation_score = 100.0 * int(((hsv[..., 2] > 217) & (hsv[..., 1] < 20)).sum()) / (H * W)
    confidence = max(BASE_CONFIDENCE * (1.0 - glare_score / 100.0), 0.0)

    verdict = "Ready" if height_proxy >= READY_HEIGHT else "Not ready"
    readiness_index = 0.5 * min(height_proxy, 1.0) + 0.3 * min(width_proxy, 1.0) + 0.2 * min(green_pct / 100.0, 1.0)

    metrics = {
        "coverage_ratio": round(coverage, 4),
        "height_proxy": round(height_proxy, 4),
        "width_proxy": round(width_proxy, 4),
        "compactness": round(compactness, 4),
        "area_px": area_px,
        "region_count": region_count,
        "green_pct": round(green_pct, 1),
        "yellow_pct": round(yellow_pct, 1),
        "brown_pct": round(brown_pct, 1),
        "glare_score": round(glare_score, 1),
        "condensation_score": round(condensation_score, 1),
        "confidence": round(confidence, 3),
        "verdict": verdict,
        "readiness_index": round(readiness_index, 4),
        "seg_method": seg_method,
        "bbox_h_px": int(bh), "bbox_w_px": int(bw),
    }

    # overlay: green tint + bbox
    overlay = rgb.copy().astype(np.float32)
    overlay[mask] = 0.5 * overlay[mask] + 0.5 * np.array([60, 200, 60], np.float32)
    overlay = overlay.astype(np.uint8)
    if bb:
        x, y, w, h = bb
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), 2)
    label = f"{verdict}" + (" | U-Net" if model is not None else " | classical")
    cv2.putText(overlay, label, (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)
    cv2.putText(overlay, label, (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
    return overlay, metrics, model_note


def _verdict_long(v):
    return {"Ready": "Ready for acclimatization",
            "Not ready": "Not ready for acclimatization"}.get(v, v)


def _metrics_md(metrics, model_note):
    m = metrics
    lines = [
        f"**Segment:** {m['seg_method']}",
        f"**Result:** {_verdict_long(m['verdict'])} · readiness {m['readiness_index']} · confidence {m['confidence']}",
        f"- Plant area: {m['area_px']:,} px ({m['coverage_ratio']*100:.1f}% of frame)",
        f"- Height (height_proxy): **{m['height_proxy']}** · Width: {m['width_proxy']} · Compactness: {m['compactness']}",
        f"- Regions: {m['region_count']} · bbox {m['bbox_w_px']}x{m['bbox_h_px']} px",
        f"- Color: green {m['green_pct']}% · yellow {m['yellow_pct']}% · brown {m['brown_pct']}%",
        f"- Glare {m['glare_score']} · Condensation {m['condensation_score']}",
        "---",
        f"_note:_ {model_note}",
        "_Values (coverage / height / verdict) use the full frame (no bottle ROI) - demo scale._",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- Gradio UI
def build_ui():
    import gradio as gr

    def scan(image):
        if image is None:
            return None, _metrics_md({"seg_method": "-", "verdict": "-", "readiness_index": 0, "confidence": 0,
                                      "area_px": 0, "coverage_ratio": 0, "height_proxy": 0, "width_proxy": 0,
                                      "compactness": 0, "region_count": 0, "bbox_w_px": 0, "bbox_h_px": 0,
                                      "green_pct": 0, "yellow_pct": 0, "brown_pct": 0, "glare_score": 0,
                                      "condensation_score": 0}, MODEL_NOTE)
        rgb = image[..., :3].astype(np.uint8) if image.ndim == 3 else np.dstack([image] * 3)
        overlay, metrics, note = segment_and_analyze(rgb, model=MODEL)
        return overlay, _metrics_md(metrics, note)

    demo = gr.Interface(
        fn=scan,
        inputs=gr.Image(sources=["webcam", "upload"], type="numpy", label="Scan a plant in a bottle"),
        outputs=[
            gr.Image(type="numpy", label="Segmentation (green = plant)"),
            gr.Markdown(label="Measured values"),
        ],
        title="VitroVision - Non-destructive tissue culture plant scan",
        description="Use the camera (or upload a photo) to segment the plant and estimate acclimatization readiness.",
        theme="soft",
    )
    return demo


# expose demo at module level so HF Gradio Spaces auto-detect it
try:
    demo = build_ui()
except Exception as e:  # noqa: BLE001
    print("[warn] gradio UI not built:", e)
    demo = None

if __name__ == "__main__":
    print("[INFO]", MODEL_NOTE)
    if demo is not None:
        demo.launch()
    else:
        print("gradio not ready - run 'python space/app.py' after 'pip install gradio'")
