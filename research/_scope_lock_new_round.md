# 🔒 ระยะ 0: ล็อกขอบเขตงาน — VitroVision รอบใหม่ (2026-08-17)

> สร้างตามคู่มือ Research_Writing_Adviser_TH.md (ระยะที่ 0) ก่อนเขียนเอกสาร
> สถานะ: [OPEN] = ต้องตัดสินใจ/รอข้อมูล

## บันทึกขอบเขต

| รายการ | คำตอบ |
|---|---|
| **ปัญหา** | การตัดสินใจ "พร้อมตัดย้าย/ออกอนุบาล" ของพืชเพาะเลี้ยงเนื้อเยื่อยังพึ่งพาสายตาคนเป็นรายขวด — คอขวดแรงงาน/เวลา มีความแปรปรวนระหว่างผู้ประเมิน |
| **คำถามวิจัย** | ด้วยภาพถ่ายเพียงภาพเดียว + SAM3 PCS zero-shot segmentation + rule-based triage จัดกลุ่มขวด (wait / subculture / transplant-overdue) ได้ถูกต้องแค่ไหน? |
| **วัตถุประสงค์** | (1) สร้าง pipeline วัดการเจริญแบบ non-destructive ผ่านขวดแก้ว (2) ปรับปรุง feature/verdict ให้ robust กว่ารอบ 1 (3) ทดสอบกับชุดภาพใหม่หลายชนิด/หลายช่วงอายุ (4) เทียบ 3 คลาสกับ ground truth เมื่อมี |
| **ข้อมูล** | ชุดภาพใหม่ — [OPEN: รอ path จากผู้ใช้] · เดิม: 51 ขวด 4 ชนิด (16/07/2569) |
| **วิธีการ** | SAM3 PCS (facebook/sam3) 5 prompts → mask → feature (โครงสร้าง/อวัยวะ/สี/คุณภาพภาพ) → rule-based verdict + confidence → CSV/XLSX/กราฟ/report.html; รันบน Colab GPU |
| **ผลที่มีแล้ว** | [RESULT] spike test 05/07/2569 พิสูจน์ feasibility; รอบ 1 (51 ภาพ) ได้ correlation สมเหตุผล (shoot↔height r=0.853, green↔yellow r=−0.597) — ยังไม่ใช่ผล validation จริง |
| **สิ่งที่ยังไม่มี** | [OPEN] ชุดภาพใหม่ · ground truth annotation · PIXEL_TO_CM calibration · เปรียบเทียบกับ manual measurement |
| **ข้อจำกัด** | SAM3 = gated + GPU เท่านั้น (Colab T4) · threshold 0.35/0.80 เป็นค่า literature ข้ามชนิด ยังไม่ calibrate · ชนิดนอกตารางใช้ค่ากลาง |
| **รูปแบบยื่น** | รายงานภาษาไทย + สไลด์นำเสนอ + บรรณานุกรม APA7 (citation ต้อง verify + DOI กดได้) |

## สถานะภายใน (ตามคู่มือ)

- [FACT] = ตรวจแล้วจากข้อมูลจริง/paper จริง
- [PLAN] = วิธีการที่วางแผน ยังไม่ใช่ผล
- [EXPECTED] = ผลที่คาดว่าจะเกิด — ห้ามเขียนเป็นผลแล้ว
- [RESULT] = ผลทดลองจริง มีไฟล์/การคำนวณรองรับ
- [OPEN] = ยังต้องถาม/ตัดสินใจ

## งานค้างรอบนี้ (ตาม backlog เดิมที่ยังไม่ทำ)

- [ ] รัน pipeline กับชุดภาพใหม่ (รอ path ภาพ)
- [ ] ปรับปรุง pipeline: ตรวจ overlay mask, นับใบ, verdict bias จาก ROI ทั้งภาพ
- [ ] PIXEL_TO_CM calibration (ขวดจริง)
- [ ] ground_truth.csv + validation metrics เมื่อวัดมือได้
- [ ] เขียนรายงานฉบับเต็ม (ยังไม่มี — งานหลักรอบนี้)
- [ ] สไลด์ชุดใหม่
