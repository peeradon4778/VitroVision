# แผนที่ Log ทั้งหมดของโปรเจกต์ (LOG_MAP)

> **กฎเหล็ก:** อะไรก็ตามที่ไม่อยู่ใน repo นี้ = ไม่ใช่หลักฐานสำหรับกรรมการ
> เปิดไฟล์นี้ตัวเดียวแล้วรู้ว่าทุกอย่างเก็บที่ไหน

## หลักฐานใน repo (สำคัญที่สุด — ใช้ตอบกรรมการ)

| อะไร | ที่เก็บ | วิธีเปิดดู |
|---|---|---|
| ประวัติการแก้ไขโค้ดทุกครั้ง (git log) | `VitroVision\.git\` (ซ่อนอยู่) | `git log --oneline` / IDE Source Control / GitHub.com → Commits |
| บันทึกการพัฒนารายวัน (DEV_LOG) | `docs\DEV_LOG.md` | เปิดไฟล์นี้ |
| เวอร์ชัน library ทั้งหมด | `requirements.txt` | เปิดไฟล์ |
| โค้ด pipeline ฉบับสคริปต์ | `src\sam3_growth_pipeline.py` | เปิดไฟล์ |
| Notebook ฉบับ Colab | `notebooks\sam3\sam3_growth_pipeline.ipynb` | เปิดไฟล์ / อัปโหลด Colab |
| เอกสารวิจัย | `research\` , `docs\` | เปิดไฟล์ |
| ผลรันจริง (CSV/XLSX/กราฟ/report.html) | `results\` (หรือ Downloads หลังดาวน์โหลดจาก Colab) | เปิดไฟล์ |

## สำเนานอกเครื่อง (สำรอง ปลอดภัย)

| อะไร | ที่เก็บ | หมายเหตุ |
|---|---|---|
| repo ทั้งหมด (สำเนา 2) | github.com/peeradon4778/VitroVision | ต้อง push ถึงจะอัปเดต |
| บทสนทนากับ AI agent | นอก repo (เครื่องเรา — config ของ tool เช่น Antigravity/opencode) | **ไม่ใช่หลักฐาน** ถ้าอยากเก็บ ให้ export ออกมาใส่ `docs\` |

## วิธีเช็คว่า "บันทึกครบไหม" (ก่อนนำเสนอ 1 นาที)

```powershell
git -C "C:\Users\User\Documents\Workspace\Projects\Other\VitroVision" log --oneline -20
# + เปิด docs\DEV_LOG.md ดู entry ล่าสุดตรงกับวันนี้
```

## ขั้นตอนของ dev ทุกครั้งที่แก้โค้ด (ต้องครบ 3 อย่าง)

1. แก้โค้ด → ทดสอบให้ผ่าน
2. เขียน entry ใหม่ใน `docs\DEV_LOG.md` (วันที่, สิ่งที่ทำ, ไฟล์, ผลเทสต์)
3. Commit: `git add <ไฟล์>; git commit -m "feat|fix|docs|refactor|chore: <ข้อความ>"`
