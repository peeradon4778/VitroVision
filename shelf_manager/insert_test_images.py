"""Insert test images เข้า DB — clear เก่าก่อน"""
import sqlite3, re
from pathlib import Path
from datetime import datetime

DB  = Path(__file__).parent / 'vitroshelf.db'
DIR = Path(__file__).parent / 'data' / 'test_preview'

conn = sqlite3.connect(str(DB))
deleted = conn.execute(
    "DELETE FROM images WHERE local_path LIKE '%test_preview%'"
).rowcount
print(f'Cleared {deleted} old test records')

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
count = 0
for img_path in sorted(DIR.glob('syn_*.jpg')):
    m = re.search(r'_(healthy|contaminated|dead)\.jpg$', img_path.name)
    if not m:
        continue
    conn.execute(
        "INSERT INTO images (bottle_id, day_point, date_taken, status, local_path) VALUES (?,?,?,?,?)",
        ('S01-A-01', 0, now, m.group(1), str(img_path))
    )
    count += 1

conn.commit()
conn.close()
print(f'Inserted {count} images')
