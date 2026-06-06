"""Export ArUco markers เป็น PNG รายขวด สำหรับนำไปจัดใน Canva
ใช้:  conda activate ml && python export_aruco_png.py
ผลลัพธ์: โฟลเดอร์ aruco_png/ มี 100 ไฟล์ เช่น S01-A-01_ID0.png
"""
import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / 'shelf_manager'))
from aruco_map import MARKER_MAP

DICT      = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
MARKER_PX = 354   # 3cm ที่ 300 DPI (30mm × 300/25.4 ≈ 354px)
BORDER    = 40    # ขอบขาวรอบ marker (quiet zone)
LABEL_H   = 56    # พื้นที่ข้อความด้านล่าง
FONT      = cv2.FONT_HERSHEY_SIMPLEX

OUT_DIR = Path.home() / 'OneDrive' / 'Desktop' / 'aruco_png'
OUT_DIR.mkdir(exist_ok=True)


def make_marker_img(marker_id: int, bottle_id: str, seq: int) -> np.ndarray:
    # สร้าง marker ขาวดำ
    marker = cv2.aruco.generateImageMarker(DICT, marker_id, MARKER_PX)

    # เพิ่ม quiet zone (border ขาว)
    total_w = MARKER_PX + BORDER * 2
    total_h = MARKER_PX + BORDER * 2 + LABEL_H
    canvas  = np.ones((total_h, total_w), dtype=np.uint8) * 255
    canvas[BORDER:BORDER + MARKER_PX, BORDER:BORDER + MARKER_PX] = marker

    # bottle_id บรรทัดบน (ตัวใหญ่)
    font_scale = 0.75
    thickness  = 2
    text_size  = cv2.getTextSize(bottle_id, FONT, font_scale, thickness)[0]
    tx = (total_w - text_size[0]) // 2
    ty = BORDER + MARKER_PX + 28
    cv2.putText(canvas, bottle_id, (tx, ty), FONT, font_scale, 0, thickness, cv2.LINE_AA)

    # marker ID + ลำดับ บรรทัดล่าง (ตัวเล็ก)
    id_text      = f'ID: {marker_id}  |  No.{seq}'
    font_scale2  = 0.45
    text_size2   = cv2.getTextSize(id_text, FONT, font_scale2, 1)[0]
    tx2 = (total_w - text_size2[0]) // 2
    ty2 = ty + 22
    cv2.putText(canvas, id_text, (tx2, ty2), FONT, font_scale2, 100, 1, cv2.LINE_AA)

    return canvas


def main():
    items = sorted(MARKER_MAP.items())
    for seq, (mid, bottle_id) in enumerate(items, start=1):
        img  = make_marker_img(mid, bottle_id, seq)
        name = f'{seq:03d}_{bottle_id}_ID{mid}.png'
        cv2.imwrite(str(OUT_DIR / name), img)

    print(f'Done: {len(items)} files -> {OUT_DIR}')
    print()
    print('Canva instructions:')
    print('  1. Upload all files from aruco_png/')
    print('  2. Layout on A4 — fits ~30-35 per sheet')
    print('  3. Print at 100% actual size (do NOT fit to page)')
    print('  4. Cut and stick on bottle neck (side, not cap)')
    print()
    print('Mapping:')
    print('  S01-A-01 = ID 0   |   S01-E-10 = ID 49')
    print('  S02-A-01 = ID 50  |   S02-E-10 = ID 99')


if __name__ == '__main__':
    main()
