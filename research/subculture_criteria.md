# 🌱 VitroVision — Subculture Readiness Criteria (สังเคราะห์จาก literature)

> สร้าง: 2026-07-06 โดย vitro-researcher (Wave 1)
> อ้างอิง citation ทั้งหมดในไฟล์นี้ตรงกับ `research/citation_gate.md` หัวข้อ 2 และ 6 — ทุกอันผ่าน verify แล้ว
> **สถานะ: rough threshold เท่านั้น — รอ lab validate กับพืชจริงในแล็บ** (เป็น 1 ใน 4 จุดที่ orchestration.md ระบุว่าต้องถามเจ้าของโครงการ/คนแล็บ) ห้าม writer เขียนราวกับเป็นค่าที่ยืนยันแล้วในเอกสาร proposal

---

## 1. สิ่งที่ literature เห็นตรงกัน (cross-species pattern)

จาก 6 การศึกษาที่ verify แล้ว (vanilla, blackberry, blueberry, cannabis, กล้วย, กล้วยไม้หลายชนิด) พบรูปแบบร่วมกัน 4 ข้อ แม้ตัวเลขสัมบูรณ์จะต่างกันมากตามชนิดพืช:

1. **รอบ subculture มีช่วงกว้างมาก (21-60 วัน) ขึ้นกับชนิดพืช** ไม่มีค่าเดียวที่ใช้ได้ทุกชนิด — cannabis สั้นสุด (~21 วัน/3 สัปดาห์) ไปจนถึง blueberry/sugarcane ยาวสุด (45-60 วัน)
2. **อัตราการเพิ่มจำนวนยอด (multiplication rate) ไม่เป็นเส้นตรง** — เพิ่มเร็วช่วงแรก แล้ว plateau หรือลดลงเมื่อผ่านหลายรอบ (vanilla: peak ที่รอบ 5 แล้วลด) → สัญญาณว่า "shoot_count นิ่ง/ลด" มีความหมายทางชีววิทยา ไม่ใช่แค่ noise
3. **coverage/canopy area ต่อขวดสัมพันธ์ตรงกับทั้ง explant density และระยะเวลา subculture** (Regni 2025 — งานที่ตรงแนวทางเราที่สุด) และมี "จุดสูงสุด" ที่บ่งบอกความหนาแน่นเหมาะสม เกินจุดนั้นไปคือสัญญาณ overcrowding
4. **ความยาวยอด/plant height มักลดลงเมื่อพืชอยู่ในรอบ subculture นานเกินไป** (senescence signal) — เป็นสัญญาณเสริมที่ต่างทิศทางกับ coverage (coverage อาจยังสูงอยู่ แต่ height เริ่มลด = สัญญาณผสมที่น่าสนใจสำหรับ transplant-overdue)

## 2. ตารางข้อมูลดิบจาก literature (รายชนิดพืช)

| พืช | รอบ subculture | shoot_count/multiplication | สัญญาณอื่น | อ้างอิง |
|---|---|---|---|---|
| Cannabis sativa | 21 วัน (3 สัปดาห์) แบบ repeated-harvest (ไม่ใช่ subculture เต็มรูปแบบ) | shoot tip harvest เพิ่มขึ้นต่อเนื่อง 4 รอบในขวดไม่มีรูระบายอากาศ | ความชื้น/แสงมีผลต่อจำนวนและคุณภาพยอด | Murphy & Adelberg (2021) |
| กล้วย (Musa, cv. Basrai) | 28 วัน (4 สัปดาห์) | เฉลี่ย 124 ต้น/shoot tip สะสมหลัง 5 รอบ (exponential) | ความแปรผันสูงระหว่าง rhizome ต้นตอ | Muhammad et al. (2004) |
| Vanilla planifolia | 45 วัน | multiplication rate เพิ่มถึงรอบ 5 แล้ว plateau/ลด | shoot length ลดลงเมื่อรอบเพิ่ม; polymorphism (somaclonal variation) เพิ่มหลังรอบ 5 | Pastelín Solano et al. (2019) |
| Blackberry (Rubus, 'Thornfree') | 30 vs 45 วัน | covered area/shoot density สูงสุดที่ 30 explants + 45 วัน | rooting เกิดเฉพาะที่ 45 วัน | Regni et al. (2025) |
| Blueberry (Vaccinium corymbosum, 'Brigitta') | 45 vs 60 วัน | covered area/density เพิ่มตามเวลาแต่ลดตามความหนาแน่น explant | chlorophyll content ไม่เปลี่ยนตาม density/duration | Regni et al. (2025) |
| กล้วยไม้ (หลายสกุล: Aerides, Cleisocentron, Cymbidium, Dendrobium, Phaius, Rhynchostylis) | 56 วัน (8 สัปดาห์) | 3.9-11.2 ยอด/explant (ต่างกันมากตามชนิด+ฮอร์โมน) | ความยาวยอด 4.75-5.56 ซม. | Barua et al. (2022) |

**ข้อสังเกตสำคัญ:** พืชในแล็บของทีม (จาก CLAUDE.md ระบุว่ามี "culture dense หลายชนิดที่มีในแล็บ" แต่ไม่ได้ระบุชนิดชัดเจนในเอกสารที่อ่านได้) **ยังไม่ทราบว่าตรงกับชนิดใดใน 6 ชนิดข้างต้น** — ตารางนี้ให้ "ช่วงอ้างอิงข้ามชนิด" (cross-species reference range) ไว้ตั้งต้นเท่านั้น ไม่ใช่ค่าเฉพาะของพืชที่ทีมใช้จริง

---

## 3. เสนอ Rough Threshold สำหรับ feature ของเรา

**หลักการแปลง:** เอกสาร literature ส่วนใหญ่รายงานเป็น "จำนวนยอด/explant" และ "ความยาวยอด (ซม.)" ซึ่งเป็นหน่วยที่แม่นยำกว่า `coverage_ratio`/`height_proxy` ที่เรานิยามจาก mask (สัดส่วนของ ROI) — การแปลงจึงทำได้แค่ระดับ "ทิศทาง/สัดส่วนสัมพัทธ์" ไม่ใช่ค่าตายตัวข้ามหน่วย ต้องมีการเก็บภาพจริงคู่กับการวัดมือ (ground truth) ก่อนจะแปลงเป็นตัวเลขที่เชื่อถือได้

| Feature ของเรา | นิยาม (จาก _orchestration.md) | สัญญาณจาก literature | Rough threshold เสนอ (🔴 รอ lab validate) |
|---|---|---|---|
| **days_since_last_subculture** | ต้องมี input วันที่ทำ subculture ล่าสุด (metadata ไม่ใช่จากภาพอย่างเดียว) | ช่วง 21-60 วันตามชนิด, ค่ากลางที่พบบ่อยสุดในข้อมูลคือ 28-45 วัน | **wait:** < 21 วัน · **subculture:** 21-45 วัน (ค่าเริ่มต้นกลางข้ามชนิด ใช้จนกว่าจะรู้ชนิดพืชจริง) · **transplant-overdue:** > 60 วัน |
| **shoot_count** | จำนวน instance "plant"/"shoot" จาก SAM3 | เพิ่มไว/ทวีคูณช่วงแรก แล้ว plateau/ลด (peak ~รอบที่ 5 ในกรณี vanilla) | เสนอวัดเป็น **relative growth** เทียบค่าตอน subculture ครั้งก่อน มากกว่าค่าตายตัว: **wait** = shoot_count ใกล้เคียง baseline (<1.5×) · **subculture** = shoot_count เพิ่ม ~2-3× จาก baseline (ช่วง "productive peak") · **transplant-overdue** = shoot_count คงที่/ลดลงจากรอบก่อน (สัญญาณ plateau/senescence) |
| **coverage_ratio** | area(plant∪leaf) / area(ROI) | มีจุด "peak" ตาม density+duration ก่อนเป็นสัญญาณ overcrowding (Regni 2025) | **wait:** < 0.35 ของ ROI · **subculture:** 0.35-0.70 (peak productive band) · **transplant-overdue:** > 0.80 (ความเสี่ยง overcrowding/hyperhydricity ตามที่ Abdalla 2022 เตือน) |
| **height_proxy** | bbox_height(plant) / ROI_height | มักลดลงเมื่อพืชอยู่รอบนานเกินไป (secondary/lagging signal ไม่ใช่ leading) | ใช้เป็น **ตัวเสริม confidence ไม่ใช่ตัวตัดสินหลัก** — height_proxy หยุดโต/ลดลง **พร้อมกับ** coverage_ratio สูง = เพิ่มน้ำหนักให้ transplant-overdue; ถ้า coverage ยังต่ำแต่ height ลด อาจเป็นสัญญาณผิดปกติอื่น (ไม่ใช่แค่ "ยังไม่พร้อม") ควรลด confidence แทนที่จะฟันธง |
| **leaf_count** | จำนวน instance "leaf" (conf ≥ 0.5) | literature ส่วนใหญ่รายงาน shoot count มากกว่า leaf count โดยตรง มีข้อมูลเทียบตรงน้อย | **ยังไม่มีฐานเพียงพอจาก literature ที่ resolve ได้ในรอบนี้ — ต้องรอข้อมูลจากแล็บจริงก่อนตั้ง threshold** ระหว่างนี้แนะนำใช้เป็น secondary feature ประกอบ shoot_count เท่านั้น |
| **glare_score** | สัดส่วน pixel V(HSV)>~0.95 & sat ต่ำใน ROI | ไม่ใช่ trait ทางชีววิทยา (เป็น engineering safeguard) — literature ด้าน glare/specular removal (Amanlou 2022) ไม่ได้ให้ threshold ทางชีวภาพ | ไม่ใช้ตัดสิน class โดยตรง — ใช้ **ลด confidence score เท่านั้น** ตาม design เดิมของทีม (ยืนยันว่าถูกทางแล้วตาม literature — ไม่มีงานไหนแนะนำให้ผสม glare เข้ากับ decision logic ของ trait) |

### ตัวอย่าง rule เบื้องต้น (ร่าง ก่อน lab validate)

```
if days_since_last_subculture < 21:
    class = "wait"
elif coverage_ratio > 0.80 OR days_since_last_subculture > 60:
    class = "transplant-overdue"
elif shoot_count_growth < 1.2x baseline AND days_since_last_subculture > 45:
    class = "transplant-overdue"  # นิ่ง/โตช้าเกินคาด + เวลาเกินคาด
elif 0.35 <= coverage_ratio <= 0.70 AND days_since_last_subculture between 21-45:
    class = "subculture"
else:
    class = "wait"

confidence = base_confidence * (1 - glare_score_penalty)
# manual override เสมอ ไม่ว่า class ไหน (ตาม _orchestration.md)
```

⚠️ **นี่คือ rule ตัวอย่างเพื่อให้ fullstack เห็นภาพโครงสร้างเท่านั้น ไม่ใช่ค่าที่ validate แล้ว** ตัวเลขทุกตัว (0.35, 0.70, 0.80, 21, 45, 60, 1.2x, 2-3x) มาจากการ**ประมาณข้ามชนิดพืช**จาก literature 6 การศึกษาที่ชนิดพืชไม่ตรงกับที่แล็บของเราใช้จริง — ต้องเก็บภาพจริง + วัดมือคู่กันอย่างน้อย 1 รอบ subculture เต็ม (หรือมากกว่า) ต่อชนิดพืชที่ใช้ ก่อนใส่ตัวเลขจริงในรายงาน/ระบบ

---

## 4. Gap ที่ยังตอบไม่ได้จาก literature (ต้องพึ่งข้อมูลแล็บจริง)

1. **ไม่รู้ชนิดพืชที่แล็บมีจริง** → เลือกช่วงอ้างอิงจากตาราง §2 ไม่ได้แม่นยำจนกว่าจะรู้ (นี่คือจุดที่ orchestration.md ระบุเป็นคำถามข้อ 2 ที่ต้องถามเจ้าของโครงการ)
2. **ไม่มีงานไหนวัด coverage_ratio ในนิยามแบบเดียวกับเราเป๊ะๆ** (mask area / ROI area จากภาพ 2D มุมเดียว) — Regni 2025 ใกล้เคียงที่สุดแต่ใช้ 3D imaging ไม่ใช่ 2D snapshot; ตัวเลข 0.35/0.70/0.80 จึงเป็นการประมาณเชิงสัดส่วน ไม่ใช่แปลงหน่วยตรงจากงานใดงานหนึ่ง
3. **ไม่มีข้อมูล inter-rater reliability ของมนุษย์เอง** (คนแล็บตัดสิน "พร้อม subculture" แม่น/ตรงกันแค่ไหนระหว่างคนต่อคน) — ถ้าจะอ้างว่า AI "ดีกว่าหรือเทียบเท่า" การตัดสินใจแบบเดิม ต้องมี baseline นี้ก่อน (อาจต้องเก็บเองในแล็บ ไม่มีใน literature ที่ specific กับ TC subculture)
4. **glare_score ยังไม่มี validation ว่าสัมพันธ์กับความแม่นของ mask จริงแค่ไหน** (เป็นสมมติฐานเชิงวิศวกรรมของทีม ไม่ใช่ค่าที่มาจาก literature)

---

## 5. สรุปสั้นสำหรับ writer

ถ้าต้องเขียนส่วน "เกณฑ์ subculture readiness" ในบทนำ/Methodology — **เขียนในเชิง "งานวิจัยที่ผ่านมาชี้ว่า readiness วัดจาก multiplication rate/coverage/height ที่ต่างกันมากตามชนิดพืช (cite Pastelín Solano 2019; Regni 2025; Barua 2022; Muhammad 2004) จึงเป็นเหตุผลที่ทีมออกแบบ threshold แบบ rule-based ที่ปรับได้ (configurable) แทนค่าตายตัว และวางแผนให้ lab validate ก่อนใช้จริง"** — นี่คือกรอบที่ปลอดภัยและตรงกับสถานะจริงของโปรเจกต์ (decision-support เท่านั้น ไม่ใช่ระบบตัดสินสุดท้าย ตาม RQ ที่ตรึงไว้แล้ว)
