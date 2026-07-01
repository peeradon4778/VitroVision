# 📥 VitroVision v2 — Backlog & งานค้าง (living doc)

> จดอะไรก็โยนลง 📌 INBOX ได้เลย — `/vitro` จะ triage ให้
> สถานะ: 🔴 เร่ง · 🟡 กำลังทำ/ศึกษา · 🟢 ภายหลัง · 💤 รอเคาะ · ✅ เสร็จ
> อัปเดตล่าสุด: 2026-07-01 (clean start)

---

## 🧭 DIRECTION ตอนนี้ (next move)
1. **ถัดไปทันที:** เทสต์ COLMAP/Meshroom บนวิดีโอขวด dense 1 ขวด → เช็คด่าน **refraction** (ตัดสินว่า 3D เป็นไปได้ไหม)
2. ศึกษา keyword หมวด **C (refraction) + D (glare)** ก่อน — ดู `research/keywords.md`
3. เลือกพืชหลัก 1 ชนิดจาก culture dense ในแล็บ + ตั้งคำถามชีววิทยา (3D vs 2D vs manual)

## 📌 INBOX (จดเร็ว ยังไม่ triage)
*(ว่าง)*

---

## 🔴 เร่ง / ตัดสิน feasibility
- [ ] เทสต์ COLMAP/Meshroom บนวิดีโอขวด dense → point cloud พังเพราะ refraction ไหม → เลือก path (2.5D / refraction-mitigated / neural GPU)
- [ ] เลือกขวด/พืชหลัก + ถ่ายวิดีโอ 360° ชุดแรก

## 🟡 กำลังศึกษา
- [ ] keyword หมวด C — refraction ผ่านภาชนะโปร่งใส (Tong 2023 ReNeuS ฯลฯ)
- [ ] keyword หมวด D — glare/cross-polarization (CPL)
- [ ] request access **SAM 3** บน HuggingFace (gated) + ลอง segment เฟรม (Colab GPU)
- [ ] ลอง YOLO-seg เป็น fallback ถ้า SAM 3 หนักไป

## 🟢 ภายหลัง
- [ ] point cloud → trait extraction (ปริมาตร / leaf area จริง / architecture)
- [ ] validation: 3D-traits vs 2D projected area vs manual/destructive
- [ ] ตั้ง citation gate file ใหม่ใน `research/`

## 💤 รอเคาะ (decision ค้าง)
- [ ] path 3D: 2.5D vs refraction-mitigated vs neural(GPU) — รอผลเทสต์ COLMAP
- [ ] ขวดผนังแบน vs โค้ง (ลด refraction เชิงกายภาพก่อนถ่าย?)

---

## 🔒 v1 (archived — อ้างอิงได้)
- Local: `Projects/Other/_VitroVision_v1_ARCHIVE_2026-07-01/`
- GitHub: tag `v1-final` + branch `archive/v1`
