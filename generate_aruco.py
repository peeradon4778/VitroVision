"""สร้าง PDF ArUco markers พร้อม label สำหรับพิมพ์ติดขวด 100 ใบ
ใช้:  conda activate ml && python generate_aruco.py
ผลลัพธ์: aruco_labels.pdf (5 หน้า, 20 ขวดต่อหน้า)
พิมพ์ที่ 100% actual size — marker ≈ 3cm
"""
import sys
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

sys.path.insert(0, str(Path(__file__).parent / 'shelf_manager'))
from aruco_map import MARKER_MAP

DICT      = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
COLS      = 4
ROWS      = 5
PER_PAGE  = COLS * ROWS   # 20
MARKER_PX = 300           # resolution ภาพก่อน scale

OUT = Path(__file__).parent / 'aruco_labels.pdf'


def gen_img(marker_id: int) -> np.ndarray:
    return cv2.aruco.generateImageMarker(DICT, marker_id, MARKER_PX)


def make_pdf():
    items = sorted(MARKER_MAP.items())   # [(0,'S01-A-01'), ...]
    n_pages = (len(items) + PER_PAGE - 1) // PER_PAGE

    with PdfPages(str(OUT)) as pdf:
        for page_idx in range(n_pages):
            page_items = items[page_idx * PER_PAGE : (page_idx + 1) * PER_PAGE]

            # A4 = 8.27 × 11.69 นิ้ว
            fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')

            # header
            fig.text(0.5, 0.975,
                     f'VitroShelf — ArUco DICT_4X4_100  ·  Page {page_idx+1}/{n_pages}',
                     ha='center', va='top', fontsize=8, color='#555')
            fig.text(0.5, 0.960,
                     'พิมพ์ที่ 100% (Actual Size)  ·  ตัดตามเส้นประ  ·  ขนาด marker ≈ 30mm',
                     ha='center', va='top', fontsize=7, color='#888')

            # grid
            gs = fig.add_gridspec(ROWS, COLS,
                                  left=0.04, right=0.96,
                                  top=0.94, bottom=0.02,
                                  wspace=0.35, hspace=0.65)

            for idx, (mid, bottle_id) in enumerate(page_items):
                r, c = divmod(idx, COLS)
                ax = fig.add_subplot(gs[r, c])

                img = gen_img(mid)
                ax.imshow(img, cmap='gray', vmin=0, vmax=255,
                          interpolation='nearest', aspect='equal')

                # กรอบตัด (เส้นประ)
                for spine in ax.spines.values():
                    spine.set_linestyle('--')
                    spine.set_edgecolor('#bbb')
                    spine.set_linewidth(0.6)
                ax.set_xticks([]); ax.set_yticks([])

                # bottle_id บน — ตัวใหญ่
                ax.set_title(bottle_id, fontsize=9, fontweight='bold',
                             color='#111', pad=4)
                # marker ID ล่าง — ตัวเล็ก
                ax.text(0.5, -0.14, f'ArUco ID: {mid}',
                        transform=ax.transAxes, ha='center',
                        fontsize=6.5, color='#777')

            pdf.savefig(fig, dpi=300)
            plt.close(fig)

    print(f'✓ บันทึกแล้ว: {OUT}')
    print(f'  {len(items)} markers  |  {n_pages} หน้า  |  {PER_PAGE} ต่อหน้า')
    print()
    print('วิธีติด:')
    print('  S01 → marker ID  0–49   (S01-A-01 = 0, S01-E-10 = 49)')
    print('  S02 → marker ID 50–99   (S02-A-01 = 50, S02-E-10 = 99)')


if __name__ == '__main__':
    make_pdf()
