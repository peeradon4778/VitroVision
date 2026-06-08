"""inject mock phenotype data เข้า DB เพื่อทดสอบ analytics page"""
import sqlite3, os, random, math
random.seed(42)

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shelf_manager'))
conn = sqlite3.connect('vitroshelf.db')

FORMULA_PARAMS = {
    'A': dict(green_base=12, green_g=0.50, lci_base=1.30, lci_g=0.020, brown=2.0, shoot=2, label='MS'),
    'B': dict(green_base=18, green_g=0.90, lci_base=1.60, lci_g=0.030, brown=1.5, shoot=4, label='MS+1BAP'),
    'C': dict(green_base=22, green_g=1.10, lci_base=1.80, lci_g=0.040, brown=1.0, shoot=6, label='MS+5BAP'),
    'D': dict(green_base=20, green_g=1.00, lci_base=1.70, lci_g=0.030, brown=1.2, shoot=5, label='MS+5BAP+NAA'),
    'E': dict(green_base=14, green_g=0.60, lci_base=1.40, lci_g=0.020, brown=3.0, shoot=3, label='MS+1IBA'),
}
BOTTLE_RANGE = {'A':(1,20),'B':(21,40),'C':(41,60),'D':(61,80),'E':(81,100)}
DAYS = [0, 7, 14, 21, 28]

# ล้างข้อมูลเก่าที่เป็น mock
conn.execute("DELETE FROM images WHERE phenotype_method='mock_data'")

# ดึง bottle_ids ที่มีอยู่
existing = {r[0] for r in conn.execute("SELECT bottle_id FROM bottles").fetchall()}

inserted = 0
for formula, p in FORMULA_PARAMS.items():
    lo, hi = BOTTLE_RANGE[formula]
    for n in range(lo, hi + 1):
        # หา bottle_id จริงใน DB
        matching = [b for b in existing if b.endswith(f'-{n:02d}') or b.endswith(str(n).zfill(3))]
        if not matching:
            # ลอง pattern อื่น
            matching = [b for b in existing]
            # เอาขวดตามลำดับ
            sorted_bottles = sorted(existing)
            idx = n - 1
            if idx < len(sorted_bottles):
                matching = [sorted_bottles[idx]]
            else:
                continue
        bottle_id = matching[0]

        for day in DAYS:
            noise = lambda s: random.gauss(0, s)
            green  = max(0, p['green_base'] + p['green_g'] * day + noise(2))
            lci    = max(0.5, p['lci_base'] + p['lci_g'] * day + noise(0.1))
            brown  = max(0, p['brown'] + noise(0.5))
            entropy = round(random.uniform(5.5, 7.5), 4)
            vigor  = round(min(10, max(0, green/8 + max(0,(lci-1)/0.5) - brown/5)), 2)
            shoot  = max(0, int(p['shoot'] + day * 0.1 + noise(1)))
            status = 'contaminated' if brown > 5.0 else 'healthy'
            date   = f'2026-06-{7 + day:02d}'

            # อัปเดต media_formula ในขวดด้วย
            conn.execute(
                "UPDATE bottles SET media_formula=?, pgr_detail=? WHERE bottle_id=?",
                (formula, p['label'], bottle_id)
            )
            conn.execute("""
                INSERT INTO images
                  (bottle_id, day_point, date_taken, status,
                   green_coverage_pct, leaf_color_index, shoot_count_cv,
                   texture_entropy, brown_coverage_pct, vigor_score,
                   media_color_cv, phenotype_method)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                bottle_id, day, date, status,
                round(green, 2), round(lci, 4), shoot,
                entropy, round(brown, 2), vigor,
                'normal' if day < 14 else ('yellow' if formula == 'E' else 'clear'),
                'mock_data'
            ))
            inserted += 1

conn.commit()
conn.close()
print(f'Inserted {inserted} mock records')
