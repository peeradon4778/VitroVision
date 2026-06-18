"""
Phase C — Pseudo-label pipeline
ส่งภาพ → Gemini Teacher → CSV → (review) → commit เข้า DB → train DINOv2

วิธีใช้:
  # ขั้น 1: label ทุกภาพที่ยังไม่มี label จริง
  python -m vitro_vision.pseudo_labeler

  # label แค่ N ภาพแรก (ทดสอบก่อน)
  python -m vitro_vision.pseudo_labeler --limit 10

  # ขั้น 2: เปิด results/pseudo_labels_YYYYMMDD.csv
  #         ใส่ Y ใน column "approved" ที่ label ถูกต้อง

  # ขั้น 3: commit labels ที่ approved เข้า DB
  python -m vitro_vision.pseudo_labeler --commit results/pseudo_labels_20260619_0400.csv
"""
import sys, os, csv, time, argparse, sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

DB_PATH  = ROOT / 'shelf_manager' / 'vitroshelf.db'
OUT_DIR  = ROOT / 'results'
DELAY_S  = 1.5   # วินาทีระหว่าง Gemini call (rate limit)


def _get_unlabeled(db_path: Path) -> list[tuple]:
    """ดึงภาพที่ status = 'unknown' และมีไฟล์จริง"""
    conn = sqlite3.connect(str(db_path))
    rows = conn.execute(
        "SELECT id, bottle_id, local_path, day_point "
        "FROM images WHERE status = 'unknown' AND local_path != ''"
    ).fetchall()
    conn.close()
    valid = []
    for row_id, bottle_id, local_path, day_point in rows:
        p = Path(local_path) if Path(local_path).is_absolute() \
            else ROOT / 'shelf_manager' / local_path
        if p.exists():
            valid.append((row_id, bottle_id, str(p), day_point))
    return valid


def run(limit=None, db_path=DB_PATH):
    from shelf_manager.vision_analyzer import analyze_plant_image

    OUT_DIR.mkdir(exist_ok=True)
    rows = _get_unlabeled(db_path)

    if not rows:
        print("ไม่มีภาพที่ต้อง label (status=unknown + มีไฟล์)")
        return None

    if limit:
        rows = rows[:limit]

    print(f"จะ label {len(rows)} ภาพด้วย Gemini...")
    print(f"เวลาโดยประมาณ: ~{len(rows) * DELAY_S / 60:.1f} นาที\n")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    csv_path  = OUT_DIR / f'pseudo_labels_{timestamp}.csv'
    fieldnames = [
        'row_id', 'bottle_id', 'local_path', 'day_point',
        'pseudo_label', 'vigor', 'dev_stage',
        'contamination_signs', 'notes', 'approved'
    ]

    results = []
    errors  = 0

    for i, (row_id, bottle_id, local_path, day_point) in enumerate(rows, 1):
        print(f"[{i:3}/{len(rows)}] {bottle_id} day={day_point}... ", end='', flush=True)
        try:
            image_bytes = Path(local_path).read_bytes()
            r = analyze_plant_image(image_bytes)
            label  = r['status']
            vigor  = r['vigor']
            marker = 'Y' if label in ('healthy', 'contaminated', 'dead') and vigor > 0 else '?'
            print(f"{label} vigor={vigor} [{marker}]")
            results.append({
                'row_id': row_id, 'bottle_id': bottle_id,
                'local_path': local_path, 'day_point': day_point,
                'pseudo_label': label, 'vigor': vigor,
                'dev_stage': r['dev_stage'],
                'contamination_signs': r['contamination_signs'],
                'notes': r['notes'],
                'approved': 'Y' if marker == 'Y' else '',
            })
        except Exception as e:
            print(f"ERROR: {e}")
            errors += 1
            results.append({
                'row_id': row_id, 'bottle_id': bottle_id,
                'local_path': local_path, 'day_point': day_point,
                'pseudo_label': 'error', 'vigor': 0,
                'dev_stage': '', 'contamination_signs': str(e)[:80],
                'notes': '', 'approved': '',
            })

        if i < len(rows):
            time.sleep(DELAY_S)

    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    dist = {}
    for r in results:
        dist[r['pseudo_label']] = dist.get(r['pseudo_label'], 0) + 1

    print(f"\n=== สรุป ===")
    print(f"ทั้งหมด : {len(results)} ภาพ  (error: {errors})")
    for lbl, n in sorted(dist.items()):
        print(f"  {lbl:<14}: {n}")
    print(f"\nCSV บันทึกที่: {csv_path.name}")
    print(f"\nขั้นตอนต่อไป:")
    print(f"  1. เปิด results/{csv_path.name} ตรวจสอบ label")
    print(f"     column 'approved': Y = ใช้, ว่าง = ข้าม")
    print(f"  2. รัน: python -m vitro_vision.pseudo_labeler --commit results/{csv_path.name}")
    return csv_path


def commit(csv_path: str, db_path=DB_PATH):
    """เขียน approved labels จาก CSV → DB.images.status → พร้อม train DINOv2"""
    path = Path(csv_path)
    if not path.exists():
        print(f"ไม่พบไฟล์: {path}")
        return

    with open(path, 'r', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    approved = [r for r in rows if r.get('approved', '').strip().upper() == 'Y'
                and r['pseudo_label'] in ('healthy', 'contaminated', 'dead')]

    if not approved:
        print("ไม่มี row ที่ approved=Y และ label ถูกต้อง")
        return

    conn = sqlite3.connect(str(db_path))
    updated = 0
    for r in approved:
        conn.execute(
            "UPDATE images SET status=?, ai_status=?, ai_confidence=0.85 WHERE id=?",
            (r['pseudo_label'], r['pseudo_label'], int(r['row_id']))
        )
        updated += 1
    conn.commit()
    conn.close()

    dist = {}
    for r in approved:
        dist[r['pseudo_label']] = dist.get(r['pseudo_label'], 0) + 1

    print(f"เขียน {updated} labels เข้า DB แล้ว")
    for lbl, n in sorted(dist.items()):
        print(f"  {lbl}: {n}")
    print(f"\nพร้อม train DINOv2 — เปิด VitroShelf → Train หรือรัน vitro_vision/trainer.py")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VitroVision Pseudo-label Pipeline')
    parser.add_argument('--limit',  type=int,   default=None,
                        help='label แค่ N ภาพแรก (ทดสอบ)')
    parser.add_argument('--commit', type=str,   default=None,
                        help='path ของ CSV ที่ review แล้ว → เขียนเข้า DB')
    parser.add_argument('--db',     type=str,   default=str(DB_PATH),
                        help='path ของ vitroshelf.db')
    args = parser.parse_args()

    if args.commit:
        commit(args.commit, Path(args.db))
    else:
        run(limit=args.limit, db_path=Path(args.db))
