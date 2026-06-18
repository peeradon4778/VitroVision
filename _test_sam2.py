# -*- coding: utf-8 -*-
"""Test SAM2 integration -- run from root: python _test_sam2.py"""
import sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent))

import numpy as np
import cv2

# 1. Import
print("1. import phenotyper...", end=" ")
from shelf_manager.phenotyper import measure, sam2_ready, seg_model_ready
print("OK")

# 2. SAM2 ready status
print(f"2. sam2_ready()      = {sam2_ready()}")
print(f"   seg_model_ready() = {seg_model_ready()}")

# 3. Synthetic TC bottle image (green plant zone, brown media zone)
print("3. create synthetic image 400x300...", end=" ")
img = np.ones((400, 300, 3), dtype=np.uint8) * 200
img[280:380, 30:270] = [100, 120, 150]   # media zone (bottom)
img[60:250,  80:220] = [40,  160,  60]   # plant zone (green, center)
_, buf = cv2.imencode('.jpg', img)
image_bytes = buf.tobytes()
print("OK")

# 4. measure()
print("4. calling measure()...", end=" ")
result = measure(image_bytes)
print("OK")

# 5. Print result
print("\n=== measure() result ===")
for k, v in result.items():
    print(f"  {k:<22} = {v}")

# 6. Assertions
print("\n=== assertions ===")
assert result != {}, "measure() must not return {}"
assert 'green_coverage_pct' in result
assert result['method'] in ('sam2_cv', 'classic_cv', 'yolov8_seg'), \
    f"unexpected method: {result['method']}"

expected = 'sam2_cv' if sam2_ready() else 'classic_cv'
assert result['method'] == expected, \
    f"expected '{expected}' got '{result['method']}'"
print(f"  method = '{result['method']}'  [OK]")

assert result['green_coverage_pct'] > 0, "green_coverage must be > 0"
print(f"  green_coverage_pct = {result['green_coverage_pct']}%  [OK]")

print("\nAll tests passed [OK]")
