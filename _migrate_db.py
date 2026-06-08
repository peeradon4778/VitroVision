import sqlite3, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shelf_manager'))

conn = sqlite3.connect('vitroshelf.db')
existing = {row[1] for row in conn.execute('PRAGMA table_info(images)')}
print('existing cols (images):', sorted(existing))

to_add = [
    ('texture_entropy',    'REAL DEFAULT NULL'),
    ('brown_coverage_pct', 'REAL DEFAULT NULL'),
]
for col, defn in to_add:
    if col not in existing:
        conn.execute(f'ALTER TABLE images ADD COLUMN {col} {defn}')
        print(f'  + Added: {col}')
    else:
        print(f'  = Already exists: {col}')

# vigor_score type — ถ้ามีแล้วจะเป็น INTEGER ต้องไม่ทำอะไร (SQLite ไม่ rename type)
if 'vigor_score' not in existing:
    conn.execute('ALTER TABLE images ADD COLUMN vigor_score REAL DEFAULT 0')
    print('  + Added: vigor_score')
else:
    print('  = Already exists: vigor_score')

conn.commit()
conn.close()
print('Migration done.')
