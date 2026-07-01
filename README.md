# VitroVision

> Computer-vision phenotyping ของพืชเพาะเลี้ยงเนื้อเยื่อในขวดแก้ว (in vitro)
> **v2 — clean start (2026-07-01)** · เริ่มโครงสร้างใหม่ทั้งหมด ไม่ต่อยอดโค้ด v1

## แนวคิด v2 (pipeline)
วิดีโอรอบขวด → segment ต้นออกจากแก้ว/glare (SAM 3 / YOLO-seg) → 3D reconstruction → ดึง trait เชิงสรีระ (ปริมาตร / leaf area จริง / architecture) แบบ non-destructive

- **คำถามชีววิทยา (CSBI):** 3D-derived traits วัดการเจริญ/vigor ได้ดีกว่า 2D projected area ไหม (เทียบ 3D vs 2D vs manual)
- **ด่านตายที่ต้องเทสต์ก่อน:** การหักเหแสงผ่านขวดแก้วโค้ง (refraction) ทำให้ SfM มาตรฐานพัง
- รายละเอียด keyword ศึกษา: [`research/keywords.md`](research/keywords.md)

## v1 (archived — ปิดผนึกไว้)
งานเดิม (Capsicum tissue culture + VitroShelf web app) หยุดเพราะเมล็ดงอกไม่พอสำหรับ design เทียบ 5 สูตร (n ไม่พอ)
- **Local:** `Projects/Other/_VitroVision_v1_ARCHIVE_2026-07-01/`
- **GitHub:** tag `v1-final` + branch `archive/v1` (+ `archive/feat-dataset`)

## โครงสร้าง (จะขยายในอนาคตอันใกล้)
```
research/    เอกสารวิจัย + keyword map
data/        raw, processed (ไม่ push)
notebooks/   Jupyter
src/         โค้ด v2
models/      โมเดล (ไม่ push)
docs/        เอกสาร
```
