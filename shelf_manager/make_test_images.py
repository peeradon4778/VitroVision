"""สร้างภาพ synthetic 180 ใบ (60 ต่อ class) สำหรับ scale test"""
import cv2, numpy as np
from pathlib import Path

OUT = Path(__file__).parent / 'data' / 'test_preview'
OUT.mkdir(parents=True, exist_ok=True)

# ลบของเก่า
for f in OUT.glob('syn_*.jpg'):
    f.unlink()

rng = np.random.default_rng(0)

def make_bottle(plant_hue_range, media_bgr, bg_bgr, n_blobs, noise, brightness=1.0):
    img = np.ones((480, 360, 3), dtype=np.uint8)
    bg = tuple(int(c * brightness) for c in bg_bgr)
    img[:] = (235, 235, 235)
    cv2.rectangle(img, (50, 30), (310, 450), bg, -1)
    cv2.rectangle(img, (50, 30), (310, 450), (150, 150, 150), 2)
    # อาหารเลี้ยงเชื้อ
    media = tuple(int(c * brightness) for c in media_bgr)
    media_h = int(rng.integers(60, 110))
    cv2.rectangle(img, (52, 450-media_h), (308, 448), media, -1)
    # พืช
    for _ in range(n_blobs):
        cx  = int(rng.integers(80, 280))
        cy  = int(rng.integers(70, 360))
        rx  = int(rng.integers(10, 60))
        ry  = int(rng.integers(14, 75))
        ang = int(rng.integers(0, 180))
        hue = int(rng.integers(*plant_hue_range))
        sat = int(rng.integers(60, 230))
        val = int(rng.integers(55, 210))
        hsv = np.uint8([[[hue, sat, val]]])
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0].tolist()
        bgr = [int(c * brightness) for c in bgr]
        cv2.ellipse(img, (cx, cy), (rx, ry), ang, 0, 360, bgr, -1)
    # overall brightness jitter
    img = np.clip(img.astype(np.float32) * brightness, 0, 255).astype(np.uint8)
    # noise
    n_arr = rng.integers(-noise, noise, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + n_arr, 0, 255).astype(np.uint8)
    return img

CLASSES = {
    'healthy':      {'hue': (35, 78), 'media': (195, 218, 195), 'bg': (225, 240, 225)},
    'contaminated': {'hue': (12, 38), 'media': (115, 148, 165), 'bg': (180, 192, 195)},
    'dead':         {'hue': (8,  22), 'media': (65,  82,  88),  'bg': (165, 168, 165)},
}

count = 0
for label, cfg in CLASSES.items():
    for i in range(60):
        n_blobs    = int(rng.integers(5, 16))
        noise      = int(rng.integers(15, 45))
        brightness = float(rng.uniform(0.75, 1.15))
        img  = make_bottle(cfg['hue'], cfg['media'], cfg['bg'], n_blobs, noise, brightness)
        path = OUT / f'syn_{count+1:03d}_{label}.jpg'
        cv2.imwrite(str(path), img)
        count += 1

print(f'Created {count} images -> {OUT}')
counts = {}
for f in OUT.glob('syn_*.jpg'):
    lbl = f.stem.rsplit('_', 1)[-1]
    counts[lbl] = counts.get(lbl, 0) + 1
for lbl, n in sorted(counts.items()):
    print(f'  {lbl}: {n}')
