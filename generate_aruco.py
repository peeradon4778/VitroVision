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
from matplotlib import font_manager

# stdout เป็น UTF-8 กัน UnicodeEncodeError บน Windows console
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# ใช้ฟอนต์ที่มีภาษาไทย (Tahoma/Leelawadee มีบน Windows ทุกเครื่อง)
for _fp in [r'C:\Windows\Fonts\tahoma.ttf', r'C:\Windows\Fonts\LeelawUI.ttf', r'C:\Windows\Fonts\angsa.ttf']:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)
        plt.rcParams['font.family'] = font_manager.FontProperties(fname=_fp).get_name()
        break
plt.rcParams['axes.unicode_minus'] = False

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


STICKER_OUT = Path(__file__).parent / 'aruco_stickers.pdf'

# sticker layout (หน่วย cm) — แต่ละดวง = marker 3cm + รหัสขวด, เว้นขอบขาว
S_MARGIN  = 1.0     # ขอบหน้ากระดาษ
S_CELL_W  = 4.2     # กว้างต่อดวง (marker 3.0 + quiet zone ~0.5×2 = ~5mm ตามมาตรฐาน ArUco)
S_CELL_H  = 4.8     # สูงต่อดวง (marker 3.0 + ที่ใส่รหัสขวด)
S_MARKER  = 3.0     # ขนาด marker จริง = 3 cm
PAGE_W_CM = 21.0    # A4
PAGE_H_CM = 29.7


def make_sticker_pdf():
    """PDF แบบ sticker-ready — แต่ละดวง marker+รหัสขวดในตัว มีเส้นไดคัท เว้นขอบขาว"""
    items  = sorted(MARKER_MAP.items())
    n_cols = int((PAGE_W_CM - 2 * S_MARGIN) // S_CELL_W)
    n_rows = int((PAGE_H_CM - 2 * S_MARGIN) // S_CELL_H)
    per_pg = n_cols * n_rows
    n_pgs  = (len(items) + per_pg - 1) // per_pg

    with PdfPages(str(STICKER_OUT)) as pdf:
        for pg in range(n_pgs):
            page_items = items[pg * per_pg:(pg + 1) * per_pg]
            fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')

            # axes พื้นหลังเต็มหน้า (พิกัด cm) สำหรับวาดเส้นตัด + รหัสขวด
            bg = fig.add_axes([0, 0, 1, 1])
            bg.set_xlim(0, PAGE_W_CM); bg.set_ylim(0, PAGE_H_CM); bg.axis('off')
            bg.text(PAGE_W_CM / 2, PAGE_H_CM - 0.45,
                    f'VitroShelf ArUco · DICT_4X4_100 · พิมพ์ 100% · marker 3cm · '
                    f'เว้นขอบขาว ห้ามตัดชิดลายดำ · หน้า {pg+1}/{n_pgs}',
                    ha='center', va='top', fontsize=7, color='#666')

            for idx, (mid, bottle_id) in enumerate(page_items):
                r, c   = divmod(idx, n_cols)
                x_left = S_MARGIN + c * S_CELL_W
                y_top  = S_MARGIN + r * S_CELL_H           # cm จากบน
                y_bot  = PAGE_H_CM - y_top - S_CELL_H       # cm จากล่าง

                # เส้นไดคัท kiss-cut (มุมโค้ง) เว้นในเซลล์เล็กน้อย
                bg.add_patch(mpatches.FancyBboxPatch(
                    (x_left + 0.1, y_bot + 0.1), S_CELL_W - 0.2, S_CELL_H - 0.2,
                    boxstyle='round,pad=0,rounding_size=0.25',
                    fill=False, ec='#999', lw=0.6, ls='--'))

                # marker — วางบนเซลล์ เว้นขอบขาวรอบด้าน
                mk_x   = x_left + (S_CELL_W - S_MARKER) / 2
                mk_top = y_top + 0.35
                ax = fig.add_axes([
                    mk_x / PAGE_W_CM,
                    (PAGE_H_CM - mk_top - S_MARKER) / PAGE_H_CM,
                    S_MARKER / PAGE_W_CM,
                    S_MARKER / PAGE_H_CM])
                ax.imshow(gen_img(mid), cmap='gray', vmin=0, vmax=255,
                          interpolation='nearest', aspect='equal')
                ax.axis('off')

                # รหัสขวด ใต้ marker — ตัวใหญ่อ่านง่าย
                txt_y = PAGE_H_CM - (mk_top + S_MARKER + 0.5)
                bg.text(x_left + S_CELL_W / 2, txt_y, bottle_id,
                        ha='center', va='center', fontsize=11,
                        fontweight='bold', color='#111')

            pdf.savefig(fig, dpi=300)
            plt.close(fig)

    print(f'✓ บันทึกแล้ว (สติ๊กเกอร์): {STICKER_OUT}')
    print(f'  {len(items)} ดวง | {n_pgs} หน้า | {per_pg} ดวง/หน้า ({n_cols}×{n_rows})')


if __name__ == '__main__':
    make_pdf()
    make_sticker_pdf()
