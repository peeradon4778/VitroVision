import sqlite3
import shutil
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = os.path.join(os.path.dirname(__file__), "vitroshelf.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

print("=" * 45)
print("  VitroShelf Reset — ล้างข้อมูลทดสอบ")
print("=" * 45)
print()
print("สิ่งที่จะถูกล้าง:")
print("  • ภาพและประวัติทั้งหมดใน DB")
print("  • metadata ขวด (species, treatment, ...)")
print("  • ภาพใน local data/")
print()
print("สิ่งที่ไม่ถูกกระทบ:")
print("  • โครงสร้าง 100 ขวด (S01, S02)")
print("  • ภาพใน Google Drive  ← ลบมือเองที่ Drive")
print()

confirm = input("ยืนยันการล้างข้อมูล? พิมพ์ YES เพื่อดำเนินการ: ")
if confirm.strip() != "YES":
    print("ยกเลิก")
    exit()

print()

# 1. ล้าง DB
conn = sqlite3.connect(DB_PATH)
conn.execute("DELETE FROM images")
conn.execute("DELETE FROM batches")
conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('images','batches')")
conn.execute("""
    UPDATE bottles SET
        species='', treatment='', date_planted='', notes='',
        batch_id=NULL, cultivar='', media_formula='',
        pgr_detail='', passage_number=NULL
""")
conn.commit()
conn.close()
print("✓ DB cleared  (images, batches, metadata ขวดทั้งหมด)")

# 2. ล้าง local images
if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)
    print("✓ Local data/ cleared")
else:
    print("✓ Local data/ ไม่มีอยู่แล้ว")

print()
print("เสร็จแล้ว — พร้อมใช้งานจริง")
print()
print("ขั้นตอนต่อไป:")
print("  1. ลบ folder S01 และ S02 ใน Google Drive มือ")
print("  2. รัน main.py ตามปกติ")
