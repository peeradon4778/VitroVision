# R2 — Segmentation Model Lineup (fallback chain ใหม่)

> **สร้าง:** 2026-06-20 · 5 Consensus sub-agents (R2-A…E) · ทุก cite มี URL จาก Consensus จริง
> **คำถามต้นทาง:** comment #6 — เปลี่ยน lineup ของ fallback chain ให้เข้าสถาปัตยกรรมใหม่ (SAM2=segment local / API=classify ตาม Q8)
> **chain เดิม:** SAM2 hiera_tiny (148MB) → YOLOv8-seg → HSV green threshold
> **ข้อจำกัด:** CPU-only, 8GB RAM, ~100 ขวด/วัน, ไม่มี labeled mask (batch 1 = data แรก)

---

## 🎯 VERDICT รวม — เปลี่ยน lineup (ใช่) แต่เปลี่ยนแบบมีโครงสร้าง

**SAM2-tiny หนักเกินจำเป็น** — เป็น video-transformer สำหรับงาน still-image ขวดเดี่ยวบน CPU [R2-B]. **MobileSAM เป็น SAM variant เดียวที่ paper ยืนยันว่ารัน CPU ได้ลื่น** (เล็กกว่า SAM เดิม >60×, เร็วกว่า FastSAM 5×) [R2-B1]

**กฎเหล็กเรื่อง prompt:** ❌ **ห้ามใช้ "everything/automatic mask" mode** = failure mode หลักในฉากกลมกลืน/glare [R2-A3,A5] → ✅ ใช้ **box prompt จาก YOLOv8 ป้อนให้ SAM** (box ชนะ point ชัดเจน, point กำกวมในเกษตร) [R2-A6,A3]

**🔑 Convergence (หลาย agent เจออิสระกัน = สัญญาณแข็ง):**
- **Bethge "Phenomenon" 2023** — phenotype พืช in-vitro ผ่าน**ขวดปิดจริง** ด้วย Random Forest superpixel segmentation (เจอโดย R1-B, R2-C) = proof ว่า segment ผ่านภาชนะใสทำได้ + classical ML พอเมื่อ label น้อย
- **Bao 2025 (GroundingDINO+SAM+VC-NMS)** — zero-shot plant phenotyping ไม่มี annotation, **ชนะ supervised YOLOv11** ด้าน generalization, ใช้ green-index refine box (เจอโดย R2-A, R2-E)
- **Leaf Only SAM** — zero-shot leaf segmentation no-train (เจอโดย R2-A, R2-E)

---

## 🏗️ Chain ใหม่ที่เสนอ (2 เฟส ตรงกับ 2-phase framing)

### เฟส Pre-annotation (offline, batch, CPU-ช้า-รับได้) — batch 1
```
GroundingDINO (text prompt "green seedling")
   → box → MobileSAM/SAM2 → mask
   → + HSV green-index gating (refine box, ตัด glare/พื้นหลังแก้ว) [R2-A,E ใช้ NCGI]
   → human review → weak labels (ไม่ใช่ final ground truth — ดิบแพ้ supervised ~15 จุด)
```
> GroundingDINO หนักบน CPU (หลายวินาที/ภาพ) แต่ pre-annotation 100 ขวดครั้งเดียว offline รับได้ [R2-E]
> ทางเบากว่า prototype: CLIPSeg (โมเดลเดียว) หรือ FastSAM [R2-E3]

### เฟส Production (รายวัน, เร็ว) — หลัง fine-tune
```
1. YOLOv8n-seg (primary, fine-tune จาก weak labels)  ← แม่น+เร็วสุดบน edge
2. MobileSAM (box-prompted refine เฉพาะขวด confidence ต่ำ)  ← on-demand ไม่ใช่ทุกเฟรม
3. HSV green threshold (fallback สุดท้าย)
```

### Physical layer (ทำก่อน — ถูก + ได้ผลสูงสุด)
- **Polarizer filter** หน้าเลนส์ → กด specular glare บนกระจกโค้ง (polarization = วิธีลด reflection FP ดีสุดกับวัตถุใส) [R2-C9,C10]
- diffuse light ไม่มี point source + คุม condensation (acclimatize อุณหภูมิก่อนถ่าย)

### Preprocessing (algorithmic glare)
- highlight removal ก่อน segment: dichromatic global-optimization (ไม่ต้อง train) [R2-C6] หรือ two-stage threshold+inpaint [R2-C5]

---

## 📊 Instance-seg tier — ปลดล็อก leaf + shoot counting (R2-D)
**คง YOLOv8n-seg — อย่ารีบเปลี่ยนเป็น YOLO11** (accuracy gap เล็กมาก, YOLOv8n เร็วกว่า 3.3 vs 4.8ms, switching cost ต่ำสลับทีหลังได้) [R2-D1]
- **แผน:** fine-tune YOLOv8n-seg เป็น 3 class: `leaf` / `shoot/growing-point` / `stem` → count instance
  - precedent ตรงมาก: **YOLOv8-SDC** แยก cotyledon/stem/growing-point ในต้นกล้า melon ได้ Mask mAP 99.1% **ชนะ YOLOv11/Mask R-CNN** [R2-D2-melon]
  - ใบเล็กหลุด → เติม BiFPN (พิสูจน์ช่วย small-leaf, best-Dice 86.4% CVPPP) [R2-D3-leafseg]
  - ใบซ้อนหนัก → fallback two-stream segmentation-guided counting (ไม่ต้อง label ทุกใบ) [R2-D1-leafcount]
- ⚠️ **gap:** ยังไม่มี paper ทำ per-organ instance-seg ของต้นในขวดเพาะเลี้ยงโดยตรง = novelty ของเรา

---

## 🤖 VLM segmentation — honest state (R2-E, ยืนยัน Q8)
- **Gemini/GPT-4o ออก box/point ได้ ไม่ออก pixel mask เอง** → architecture ถูกต้อง = Gemini (classify + region) → SAM (mask) [R2-E5]
- Set-of-Mark: SAM แบ่ง region ก่อน → GPT-4V อ้างถึง mark → ชนะ finetuned referring seg [R2-E2]
- VLM ที่ออก mask ในตัวต้องเป็น GLaMM (pixel-grounding LMM เฉพาะ) ไม่ใช่ Gemini API [R2-E6]
- **ยืนยัน Q8 lock: SAM = mask (local) / Gemini = classify+region (cloud)** ✅

---

## ⚠️ Honest framing สำหรับ YSC/CSBI
- zero-shot SAM **แพ้ fine-tuned ~15 จุด accuracy** → frame ว่าเลือกเพราะ "no label + CPU constraint" ไม่ใช่ "แม่นสุด" [R2-A1,A4]
- EdgeSAM/EfficientViT-SAM ตัวเลขเร็วสุด **benchmark บน mobile NPU/GPU+TensorRT ไม่ใช่ x86 CPU** → อย่าอ้างกับเครื่องเรา [R2-B3,B5]
- **ควร benchmark จริง 3 ตัวบนเครื่องเป้าหมาย** (SAM2-tiny vs MobileSAM vs YOLOv8n-seg-only) → รายงานเป็น empirical result = จุดขาย [R2-B]

---

## 📌 ACTION items จาก R2 (รอเคาะ)
1. **เปลี่ยน primary: SAM2-tiny → YOLOv8n-seg + MobileSAM (box-prompted on-demand)** — benchmark บนเครื่องจริงก่อนยืนยัน
2. **ห้าม everything-mode** — เปลี่ยนเป็น box-prompt flow (YOLOv8 box → SAM)
3. ติด **polarizer + diffuse light** (physical glare) — ทดสอบ batch 1
4. เพิ่ม **highlight-removal preprocessing** ก่อน segment
5. **GroundingDINO "green seedling" pre-annotation** offline → weak labels → fine-tune
6. fine-tune YOLOv8n-seg **3-class (leaf/shoot/stem)** → leaf+shoot counting (เชื่อม R1 shoot multiplication rate)
7. Random Forest superpixel เป็น baseline ทางเลือก (Bethge precedent) ถ้า SAM ผ่านกระจกไม่ไหว

---

## 📚 Verified papers (key)
- Bethge 2023 "Phenomenon" — through-vessel in-vitro phenotyping — https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/
- Bao 2025 — zero-shot plant phenotyping GroundingDINO+SAM+VC-NMS — https://consensus.app/papers/details/86cfd544ceb55be0b83c171e98d0e997/
- MobileSAM (Zhang 2023) — CPU-capable SAM — https://consensus.app/papers/details/105eb97215715c84b8326d7e5c60e57a/
- Leaf Only SAM (Williams 2023) — https://consensus.app/papers/details/4def311216355693ba414d1f21de6b44/
- YOLOv8-SDC melon seedling organ-seg (Li 2025) — https://consensus.app/papers/details/cdc62ff48eb053809bf27b95592c64d5/
- Grounded SAM (Ren 2024) — https://consensus.app/papers/details/de2b824320965dc798eacf1a05a13474/
- Kalra 2020 polarization transparent-object seg (CVPR, 150 cit) — https://consensus.app/papers/details/d4c1a1a63cc15973bd3fa58d09a0ccb0/
- Set-of-Mark GPT-4V (Yang 2023) — https://consensus.app/papers/details/5593e891018e5a64895e1ce61cfdc9ab/
(รายการเต็ม ~30 ฉบับอยู่ใน transcript sub-agents)
