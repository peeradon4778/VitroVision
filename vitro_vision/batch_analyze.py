"""
วิเคราะห์ภาพที่ถ่ายไว้แล้วใน shelf_manager/data/ แบบ batch
รัน: conda activate ml && python -m vitro_vision.batch_analyze --day 14

ใช้ตอน: มีภาพจาก VitroShelf อยู่แล้ว อยากรัน inference ย้อนหลัง
"""
import argparse
import os
import glob
from pathlib import Path
from . import classifier, api_client

DATA_DIR = Path(__file__).parent.parent / "shelf_manager" / "data"


def run(day_point: int, dry_run: bool = False):
    pattern = str(DATA_DIR / "**" / f"*_day{day_point:03d}_*.jpg")
    files = glob.glob(pattern, recursive=True)
    print(f"พบ {len(files)} ภาพ สำหรับ Day {day_point}")

    import cv2
    for path in files:
        name = Path(path).stem
        parts = name.split("_")
        bottle_id = parts[0]

        img = cv2.imread(path)
        if img is None:
            print(f"  SKIP {path}")
            continue

        status, conf = classifier.predict(img)
        print(f"  {bottle_id}: {status} ({conf:.0%})")

        if not dry_run:
            api_client.post_observation(bottle_id, day_point, status,
                                        ai_status=status, ai_confidence=conf)

    print("เสร็จสิ้น" + (" (dry run)" if dry_run else ""))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--day",     type=int, required=True)
    p.add_argument("--dry-run", action="store_true", help="ไม่ส่งข้อมูลไป API")
    args = p.parse_args()
    run(args.day, args.dry_run)
