# -*- coding: utf-8 -*-
"""วาด flowchart ใหม่แบบแนวตั้ง (รูปจริงสวย ไม่ล้น) — docs/assets/flow_*.png"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "Tahoma"

OUT = "docs/assets"
os.makedirs(OUT, exist_ok=True)


def vflow(items, fname, note=None, box_h=1.35, gap=0.75):
    n = len(items)
    total = n * box_h + (n - 1) * gap + 1.6
    fig, ax = plt.subplots(figsize=(7.0, total / 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, total)
    ax.axis("off")
    y_top = total - 0.9
    y = y_top
    for i, (text, fc, ec) in enumerate(items):
        box = FancyBboxPatch((0.6, y - box_h / 2), 8.8, box_h,
                             boxstyle="round,pad=0.25", fc=fc, ec=ec, lw=1.6)
        ax.add_patch(box)
        ax.text(5, y, text, ha="center", va="center", fontsize=12.5,
                fontweight="bold" if i == n - 1 else "normal")
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((5, y - box_h / 2), (5, y - box_h / 2 - gap),
                                         arrowstyle="-|>", mutation_scale=20, lw=1.8, color="#1B5E20"))
        y -= (box_h + gap)
    if note:
        ax.text(5, y - 0.1, note, ha="center", va="top", fontsize=10.5,
                style="italic", color="#B71C1C", wrap=True)
    fig.tight_layout(pad=0.4)
    fig.savefig(f"{OUT}/{fname}", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ok", fname)


G = "#E8F5E9"; GE = "#2E7D32"
B = "#E3F2FD"; BE = "#1565C0"
O = "#FFF3E0"; OE = "#E65100"

vflow([
    ("ถ่ายภาพขวดเพาะเลี้ยงเนื้อเยื่อ\n(สมาร์ตโฟน + ขาตั้ง ระยะและแสงคงที่)", O, OE),
    ("ตรวจจับขอบเขตขวด (Bottle ROI)", G, GE),
    ("แบ่งส่วนภาพด้วย SAM3\nแบบ zero-shot 5 พรอมป์", G, GE),
    ("คำนวณ Feature เชิงปริมาณ 6 กลุ่ม", G, GE),
    ("ตัดสินใจด้วยกฎ (Rule-based)\nพร้อมอนุบาล / ยังไม่พร้อม", O, OE),
    ("ภาพไม่ชัด (glare/ฝ้า/ไม่พบขวด) → ส่งผู้เชี่ยวชาญตรวจ", O, OE),
], "flow_overview.png",
note="ภาพที่ประมวลผลไม่ชัดจะถูกทำเครื่องหมาย \"ตรวจเอง\" และส่งให้มนุษย์ตรวจแทนการตัดสินใจอัตโนมัติ")

vflow([
    ("รวบรวมภาพถ่ายขวดจากชุดข้อมูล", G, GE),
    ("ตรวจจับขอบเขตขวด (Bottle ROI)", G, GE),
    ("รัน SAM3 PCS บน GPU (headless batch)\nพรอมป์: plant, leaf, shoot, stem, root", G, GE),
    ("ได้ binary mask ต่อพรอมป์ + confidence + bbox", G, GE),
    ("นับใบแบบ merged (กัน over-segmentation)\nfallback นับจาก plant+shoot", G, GE),
    ("คำนวณ feature 6 กลุ่ม + verdict + confidence", O, OE),
], "flow_pipeline.png")

vflow([
    ("ชุดภาพจริง 100 ขวด + ค่าอ้างอิงจากผู้ประเมิน", B, BE),
    ("ระบบ (SAM3 / U-Net) และวิธีพื้นฐาน\n(SAM2, YOLO-seg, classical)", B, BE),
    ("เทียบระดับพิกเซลกับ ground truth\nmIoU, Dice, F1, precision, recall", B, BE),
    ("เทียบระดับการจัดกลุ่มกับผู้ประเมิน\naccuracy, sensitivity, specificity, F1, MCC, kappa", B, BE),
    ("เทียบ inter-rater (ICC, kappa) และทดสอบข้ามชนิด", B, BE),
    ("สรุปผล เทียบกับสมมติฐาน H1 และ H2", B, BE),
], "flow_validation.png")

print("[OK] flowcharts done")
