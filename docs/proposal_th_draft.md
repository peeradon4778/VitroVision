# ร่างข้อเสนอโครงงาน YSC 2027 — ส่วนที่ 1

---

## 1. ชื่อโครงงาน

**ภาษาไทย:** VitroVision — ระบบคัดกรองความพร้อมของการตัดย้ายเนื้อเยื่อด้วย Zero-Shot จากโมเดล SAM3 สำหรับพืชเพาะเลี้ยงเนื้อเยื่อ

**ภาษาอังกฤษ:** VitroVision: A SAM3-Powered Zero-Shot Vision System for Subculture Readiness in Plant Tissue Culture

**สาขา:** CSBI (Computer Science and Biology)

---

## 2. บทคัดย่อ

การเพาะเลี้ยงเนื้อเยื่อพืช (plant tissue culture) เป็นเทคโนโลยีหลักของการขยายพันธุ์พืชเชิงพาณิชย์ทั่วโลก รวมถึงประเทศไทยซึ่งเป็นฐานการผลิตกล้วยไม้ อินทผลัม ปาล์มน้ำมัน และพืชเศรษฐกิจอีกหลายชนิด ปัญหาสำคัญของกระบวนการนี้คือการตัดสินใจว่าเมื่อใดจึงควรตัดย้าย (subculture) ซึ่งปัจจุบันอาศัยการตรวจสอบด้วยสายตาของนักวิทยาศาสตร์เป็นรายขวด ทำให้เป็นคอขวดด้านแรงงานและเวลา โดยเฉพาะในห้องปฏิบัติการที่มีปริมาณขวดมาก

โครงงานนี้นำเสนอ VitroVision — ระบบคัดกรองความพร้อมของการตัดย้ายเนื้อเยื่อแบบ non-destructive ที่ใช้ SAM3 (Segment Anything Model 3) ในโหมด Promptable Concept Segmentation (PCS) เพื่อ segment ต้นพืชและใบจากภาพถ่ายเพียงภาพเดียวผ่านขวดแก้ว โดยผู้ใช้ถ่ายภาพขวดเพาะเลี้ยงด้วยสมาร์ตโฟนระบบปฏิบัติการ Android ส่งภาพไปยัง Roboflow SAM3 PCS API พร้อม text prompts คำว่า "plant" และ "leaf" จากนั้นระบบจะประมวลผล mask ที่ได้เพื่อคำนวณ feature ต่าง ๆ ได้แก่ coverage_ratio, height_proxy, leaf_count, shoot_count และ glare_score ก่อนนำเข้า rule-based decision algorithm เพื่อจัดกลุ่มขวดออกเป็น 3 คลาส ได้แก่ wait (ยังไม่พร้อม), subculture (พร้อมตัดย้าย), และ transplant-overdue (เกินเวลาที่เหมาะสม) พร้อม confidence score และตัวเลือกให้ผู้ใช้ปรับแก้ผลด้วยตนเอง (manual override)

ผลการทดสอบเบื้องต้น (spike test, 5 กรกฎาคม 2569) ยืนยันว่า SAM3 PCS สามารถ segment ต้นพืชที่เพาะเลี้ยงในขวดแก้วผ่านสิ่งรบกวน เช่น ฝ้า ไอน้ำ และแสงสะท้อน (glare) ได้จริง แม้ยังไม่ผ่านการปรับเทียบ (fine-tune) สำหรับงานนี้โดยเฉพาะ — เป็นหลักฐานเบื้องต้นว่าแนวทาง zero-shot segmentation มีความเป็นไปได้

ระบบนี้มีข้อจำกัดที่ชัดเจน: (1) เป็นเครื่องมือช่วยตัดสินใจ (decision-support) ไม่ใช่ระบบวินิจฉัยขั้นสุดท้าย (2) ค่า threshold ของการจัดกลุ่มเป็นค่า rough จากการสังเคราะห์วรรณกรรมข้ามชนิดพืช ต้องผ่านการเทียบค่า (calibration) กับข้อมูลในห้องปฏิบัติการจริงก่อนนำไปใช้ และ (3) ความแม่นยำของ segmentation ขึ้นอยู่กับคุณภาพของภาพ คุณภาพเครือข่ายอินเทอร์เน็ต และชนิดของพืช อย่างไรก็ตาม VitroVision นำเสนอแนวทางใหม่ในการใช้ foundation model ล่าสุดอย่าง SAM3 กับปัญหาทางชีววิทยาพืชที่ยังไม่มีระบบ low-cost อื่นรองรับ ซึ่งอาจช่วยเพิ่มประสิทธิภาพห้องปฏิบัติการเพาะเลี้ยงเนื้อเยื่อในประเทศไทยและประเทศกำลัง開発อื่น ๆ

---

## 3. บทนำ

### 3.1 ความสำคัญของการเพาะเลี้ยงเนื้อเยื่อพืชในระดับโลกและไทย

การเพาะเลี้ยงเนื้อเยื่อพืช (plant tissue culture หรือ micropropagation) เป็นเทคโนโลยีการขยายพันธุ์พืชที่ใช้ชิ้นส่วนขนาดเล็ก (explant) เพาะเลี้ยงในสภาพปลอดเชื้อบนอาหารสังเคราะห์ ปัจจุบันเทคโนโลยีนี้ถูกใช้อย่างกว้างขวางในเชิงพาณิชย์ครอบคลุมพืชเกษตร อาหาร เภสัชกรรม และเครื่องสำอางทั่วโลก (Hasnain et al., 2022) และเป็นแหล่งผลิตสารออกฤทธิ์ทางชีวภาพระดับอุตสาหกรรมที่ไม่ขึ้นกับฤดูกาลหรือสภาพภูมิอากาศ (Chandran et al., 2020)

สำหรับประเทศไทย การเพาะเลี้ยงเนื้อเยื่อมีบทบาทสำคัญอย่างยิ่งในอุตสาหกรรมกล้วยไม้ ซึ่งเป็นสินค้าส่งออกสำคัญที่ประเทศไทยมีพื้นที่ปลูกประมาณ 7,420 เอเคอร์ (ราว 18,770 ไร่, ข้อมูล พ.ศ. 2555) และส่งออกมากกว่า 50% ของผลผลิตไปยังกว่า 148 ประเทศ (Thammasiri, 2015) นอกจากนี้หน่วยงานวิจัยของไทย เช่น ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค) ได้พัฒนาและถ่ายทอดเทคโนโลยีการเพาะเลี้ยงเนื้อเยื่อในเชิงพาณิชย์สำหรับพืชหลายชนิด เช่น อินทผลัมพันธุ์บาฮี (ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ, 2565) และระบบเพาะเลี้ยงในอาหารเหลวด้วย bioreactor สำหรับปาล์มน้ำมันและมะพร้าวที่ช่วยเพิ่มความเร็วในการขยายพันธุ์ 3-4 เท่า (ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ, 2563)

### 3.2 ปัญหา: การตัดสินใจตัดย้าย (subculture) ยังเป็นคอขวด

แม้เทคโนโลยีเพาะเลี้ยงเนื้อเยื่อจะพัฒนาไปมาก แต่กระบวนการหนึ่งที่ยังคงพึ่งพาแรงงานคนอย่างมากคือการตัดสินใจว่าเมื่อใดจึงควรตัดย้าย (subculture) หรือย้ายพืชไปยังอาหารสด ซึ่งเป็นขั้นตอนที่ต้องทำซ้ำทุก 3-8 สัปดาห์ ขึ้นกับชนิดพืช (Pastelín Solano et al., 2019; Regni et al., 2025; Barua et al., 2022) การตัดสินใจที่ผิดพลาด — ทั้งที่ช้าหรือเร็วเกินไป — อาจส่งผลกระทบร้ายแรง เช่น hyperhydricity, การตายของเนื้อเยื่อ (necrosis) และประสิทธิภาพการขยายพันธุ์ที่ลดลง (Abdalla et al., 2022)

ปัจจุบันการประเมินความพร้อมในการตัดย้ายในห้องปฏิบัติการส่วนใหญ่อาศัยการตรวจสอบด้วยสายตาของนักวิทยาศาสตร์เป็นรายขวด ซึ่งเป็นกระบวนการที่ "ใช้แรงงานมากและมีค่าใช้จ่ายสูง" (Murphy & Adelberg, 2021) และในระบบ semi-solid ที่แพร่หลายที่สุด ก็ยังมีข้อจำกัดด้าน "อัตราการเพิ่มจำนวนต่ำและต้นทุนการผลิตสูง" (Nongdam et al., 2023) ยิ่งไปกว่านั้น ในห้องปฏิบัติการที่มีปริมาณขวดหลายร้อยถึงหลายพันขวด การตรวจสอบรายขวดอย่างละเอียดทำได้ไม่ทั่วถึง นักวิทยาศาสตร์มักใช้ประสบการณ์ส่วนบุคคลในการตัดสินใจ ซึ่งมีความแปรปรวนสูงระหว่างบุคคล

### 3.3 ช่องว่างขององค์ความรู้ (Research Gap)

งานวิจัยที่ผ่านมามีความพยายามในการนำ computer vision มาใช้กับพืชเพาะเลี้ยงเนื้อเยื่อแบบไม่ทำลายตัวอย่าง (non-destructive) ผ่านขวดปิด เช่น ระบบ "Phenomenon" ที่ใช้ multi-sensor และ random forest segmentation สำหรับวัด projected area และ canopy height (Bethge et al., 2023) แต่ระบบดังกล่าวเป็น hardware เฉพาะราคาสูงและยังไม่ใช้ foundation model ที่สามารถ zero-shot ข้ามชนิดพืชได้

ในด้านการประเมินความหนาแน่นของพืชในขวด Regni et al. (2025) เป็นงานที่ใกล้เคียงกับแนวทางของเรามากที่สุด โดยใช้ภาพถ่าย 3D จากสมาร์ตโฟนวัด canopy/covered area ต่อขวดและ shoot density เทียบกับระยะเวลา subculture ใน blackberry และ blueberry แต่ยังไม่มีงานใดที่ใช้ zero-shot foundation model ในการ segment ผ่านขวดแก้วโดยตรง หรือพัฒนาระบบ decision-support สำหรับการจัดลำดับความเร่งด่วนในการตัดย้ายแบบ 3 คลาส

**นอกจากนี้ยังไม่มีระบบ low-cost (ใช้เพียงสมาร์ตโฟน) ที่สามารถทำงานข้ามชนิดพืช (cross-species) โดยไม่ต้องฝึกโมเดลใหม่ (re-train) สำหรับพืชแต่ละชนิด** — นี่คือช่องว่างที่ VitroVision มุ่งตอบ

### 3.4 คำถามวิจัย (Research Question)

ด้วยภาพถ่ายเพียงภาพเดียว (single snapshot) ผนวกกับ SAM3 PCS zero-shot segmentation และ rule-based triage algorithm สามารถจัดกลุ่มขวดเพาะเลี้ยงเนื้อเยื่อใน 3 คลาส (wait / subculture / transplant-overdue) ได้อย่างถูกต้องเพียงใด?

### 3.5 วัตถุประสงค์ของโครงงาน

ดูในหัวข้อ 4

### 3.6 สมมติฐาน

**H₁:** SAM3 PCS ที่ใช้ text prompts "plant" และ "leaf" สามารถ segment ต้นพืชเพาะเลี้ยงเนื้อเยื่อผ่านขวดแก้วที่มี glare, ฝ้า และ condensation ได้ โดยมี mIoU เฉลี่ย ≥ 0.65 เมื่อเทียบกับ ground truth ที่ annotate โดยมนุษย์ (อ้างอิงจากผล spike test 2026-07-05 ที่แสดง feasibility)

**H₂:** ชุด feature 5 มิติ (coverage_ratio, height_proxy, leaf_count, shoot_count, glare_score) ที่คำนวณจาก mask ของ SAM3 PCS สามารถทำนายคลาส subculture readiness ด้วย rule-based algorithm ได้ถูกต้อง ≥ 70% เมื่อเทียบกับการประเมินโดยนักวิทยาศาสตร์ห้องปฏิบัติการ (รอการทดสอบกับข้อมูลจริง)

---

## 4. วัตถุประสงค์

1. เพื่อพัฒนาแอปพลิเคชัน Android ที่เชื่อมต่อกับ Roboflow SAM3 PCS API สำหรับการถ่ายภาพขวดเพาะเลี้ยงเนื้อเยื่อและ segment ต้นพืชและใบแบบ zero-shot ผ่าน text prompts "plant" และ "leaf"

2. เพื่อออกแบบชุด feature (coverage_ratio, height_proxy, leaf_count, shoot_count, glare_score) ที่คำนวณจาก SAM3 mask สำหรับบ่งชี้สถานะความพร้อมในการตัดย้ายของพืชเพาะเลี้ยงเนื้อเยื่อแบบ non-destructive

3. เพื่อสร้างและทดสอบ rule-based decision algorithm สำหรับจัดกลุ่มขวดเป็น 3 คลาส (wait / subculture / transplant-overdue) พร้อม confidence score และ manual override

4. เพื่อประเมินความถูกต้องของระบบเทียบกับการประเมินโดยนักวิทยาศาสตร์ห้องปฏิบัติการ และปรับเทียบ threshold สำหรับพืชแต่ละชนิด

---

## 5. สมมติฐาน

**สมมติฐานที่ 1 (เชิงเทคนิค — segmentation):** SAM3 PCS ที่ใช้ text prompts "plant" และ "leaf" สามารถ segment ต้นพืชเพาะเลี้ยงเนื้อเยื่อผ่านขวดแก้วซึ่งมีสิ่งรบกวนทางแสง (glare, condensation, reflection) ได้ โดยมีค่าเฉลี่ย Intersection over Union (mIoU) ระหว่าง mask ที่ได้จากการ segment อัตโนมัติกับ ground truth ที่ annotate โดยมนุษย์ ≥ 0.65

**สมมติฐานที่ 2 (เชิงชีววิทยา — การทำนาย):** ชุด feature ที่คำนวณจาก SAM3 mask (coverage_ratio, height_proxy, leaf_count, shoot_count) ผนวกกับ metadata (days_since_last_subculture) สามารถจำแนกขวดเพาะเลี้ยงเนื้อเยื่อออกเป็น 3 คลาสตามความพร้อมในการตัดย้ายได้ถูกต้อง ≥ 70% เมื่อเทียบกับการประเมินโดยนักวิทยาศาสตร์ที่มีประสบการณ์ในห้องปฏิบัติการ โดยมีค่า minimum sensitivity ≥ 0.6 สำหรับคลาส subculture (คลาสเป้าหมายหลัก)

---

## 6. วัสดุอุปกรณ์

| อุปกรณ์/ซอฟต์แวร์ | รายละเอียด | การใช้งาน |
|---|---|---|
| Samsung Galaxy S24 FE | สมาร์ตโฟนระบบ Android, กล้อง 50MP | ถ่ายภาพขวดเพาะเลี้ยงเนื้อเยื่อในระยะคงที่ |
| ขวดเพาะเลี้ยงเนื้อเยื่อ (มาตรฐาน) | ขวดแก้วใส ขนาดประมาณ 4-8 oz | ภาชนะบรรจุพืชเพาะเลี้ยงเนื้อเยื่อ |
| พืชเพาะเลี้ยงเนื้อเยื่อหลายชนิด | อย่างน้อย 2-3 ชนิด (เช่น กล้วยไม้, กล้วย, พืชที่แล็บมี) | ตัวอย่างสำหรับทดสอบระบบ |
| Roboflow Account (Plan ที่รองรับ SAM3 PCS API) | บัญชี Roboflow พร้อม API key | ส่งภาพไปยัง SAM3 PCS API |
| SAM3 PCS API (ผ่าน Roboflow) | โมเดล Carion et al. (2025) — Promptable Concept Segmentation | Segment ต้นพืชและใบจากภาพ |
| Android Studio + Kotlin/Java | IDE สำหรับพัฒนาแอปพลิเคชัน Android | พัฒนาแอปพลิเคชัน VitroVision |
| กล้องถ่ายรูป/ขาตั้งกล้อง | สำหรับจัดระยะถ่ายคงที่ | ถ่ายภาพในชุดข้อมูล validation |
| คอมพิวเตอร์สำหรับพัฒนา | เครื่องพัฒนาที่เชื่อมต่ออินเทอร์เน็ต | ทดสอบและ debug ระบบ |

---

## 7. วิธีการดำเนินการ (Methodology)

### 7.1 การเก็บข้อมูล (Data Collection)

การเก็บข้อมูลภาพถ่ายขวดเพาะเลี้ยงเนื้อเยื่อดำเนินการตามขั้นตอนดังนี้

**7.1.1 การจัดฉากถ่ายภาพมาตรฐาน**

- วางขวดเพาะเลี้ยงเนื้อเยื่อบนพื้นหลังสีขาว/ดำด้าน (matte) เพื่อลดแสงสะท้อน
- ติดตั้งสมาร์ตโฟนบนขาตั้งกล้องในระยะคงที่ 20-30 เซนติเมตรจากขวด โดยให้กล้องอยู่ในแนวระดับเดียวกันกับกึ่งกลางขวด
- จัดแสงจากด้านข้าง (side-lighting) มุมประมาณ 45 องศา หลีกเลี่ยงแสงจากด้านหน้าโดยตรงเพื่อลด glare
- ถ่ายภาพที่ความละเอียด 12-50MP (ขึ้นกับกล้อง) ในรูปแบบ JPEG โดยไม่ใช้แฟลช
- ถ่ายภาพซ้ำ 2-3 ครั้งต่อขวด เพื่อให้มีภาพสำรองในกรณีที่เกิด glare หรือ motion blur

**7.1.2 ข้อมูล metadata ที่บันทึกคู่กับภาพ**

- วันที่ถ่ายภาพ (timestamp)
- วันที่ตัดย้ายครั้งล่าสุด (days_since_last_subculture)
- ชนิดพืช (species/cultivar)
- จำนวนวันที่อยู่ในรอบ subculture ปัจจุบัน
- การประเมินโดยนักวิทยาศาสตร์ (ground truth): wait / subculture / transplant-overdue

**7.1.3 จำนวนตัวอย่างเป้าหมาย**

- อย่างน้อย 100 ขวด กระจายครอบคลุม 3 คลาส (≥ 30 ตัวอย่างต่อคลาส)
- ครอบคลุมพืชอย่างน้อย 2-3 ชนิดหรือสายพันธุ์ ที่มีความแตกต่างทางสัณฐานวิทยา

### 7.2 ขั้นตอนการประมวลผลภาพ (Image Processing Pipeline)

**7.2.1 การส่งภาพไปยัง SAM3 PCS API**

1. แอปพลิเคชันรับภาพจากกล้องสมาร์ตโฟน (หรือเลือกจากแกลเลอรี)
2. ปรับขนาดภาพให้มีด้านยาวสูงสุดไม่เกิน 2048 pixels (ลด payload และเวลา)
3. แปลงภาพเป็น base64 string
4. ส่ง POST request ไปยัง Roboflow SAM3 PCS endpoint พร้อม:
   - ภาพ (base64 encoded)
   - text prompts: `["plant", "leaf"]`
   - confidence threshold: 0.3 (ค่าเริ่มต้น)
5. รับ response ที่ประกอบด้วย:
   - predictions: array ของ instance detection
   - แต่ละ instance ประกอบด้วย: class name, confidence score, bbox (x, y, width, height), polygon points (mask), image dimensions

**7.2.2 การจัดระเบียบผลลัพธ์**

- แยก predictions เป็น 2 กลุ่มตาม class: "plant" และ "leaf"
- คัดกรอง instance ที่ confidence ต่ำกว่า 0.5 (ยกเว้นกรณีที่ไม่มี instance ใดผ่าน threshold ให้ใช้ค่า 0.3 เป็น lower bound)
- กรณีที่ได้ mask เป็น polygon points (ไม่ใช่ binary mask) ให้แปลงเป็น binary mask บน canvas ขนาดภาพเดิม

**7.2.3 หมายเหตุสำคัญเกี่ยวกับ SAM3 PCS**

Spike test เมื่อวันที่ 5 กรกฎาคม 2569 ได้ทดสอบ SAM3 PCS กับภาพขวดเพาะเลี้ยงเนื้อเยื่อจริง (ผ่าน Roboflow API) ด้วย text prompts "plant" และ "leaf" — ผลการทดสอบยืนยันว่าโมเดลสามารถ segment ตำแหน่งของต้นพืชที่อยู่ภายในขวดแก้วได้สำเร็จ แม้มี glare และ condensation ในภาพ โดยเฉพาะอย่างยิ่ง SAM3 PCS สามารถแยกแยะระหว่างต้นพืชกับพื้นหลังและขอบขวดได้ ซึ่งเป็นการพิสูจน์ feasibility ของแนวทาง zero-shot segmentation สำหรับงานนี้ก่อนเริ่มพัฒนาเต็มรูปแบบ

### 7.3 การคำนวณ Feature (Feature Extraction)

เมื่อได้ mask ของ "plant" และ "leaf" แล้ว ระบบจะคำนวณ feature ดังต่อไปนี้

**ตารางที่ 1: นิยามของ feature ที่ใช้ในระบบ**

| Feature | ตัวแปร | สูตร/นิยาม | หน่วย |
|---|---|---|---|
| coverage_ratio | `cr` | area(plant_mask ∪ leaf_mask) / area(ROI) | สัดส่วน (0-1) |
| height_proxy | `hp` | bbox_height(plant_mask) / ROI_height | สัดส่วน (0-1) |
| leaf_count | `lc` | จำนวน instance ที่มี class = "leaf" และ confidence ≥ 0.5 | จำนวนเต็ม |
| shoot_count | `sc` | จำนวน instance ที่มี class = "plant" (รวม "shoot") และ confidence ≥ 0.5 | จำนวนเต็ม |
| glare_score | `gs` | สัดส่วน pixel ใน ROI ที่มีค่า V (จาก HSV) > 0.95 และ S < 0.2 | สัดส่วน (0-1) |

**หมายเหตุ:**
- ROI (Region of Interest) คือพื้นที่ภายในขวดซึ่งกำหนดโดย crop คงที่จากการจัดฉากถ่ายมาตรฐาน (fixed-distance setup) — ไม่ใช้ automatic detection ในเวอร์ชันแรก
- `height_proxy` เป็นสัดส่วนสัมพัทธ์ ไม่ใช่ความยาวจริงในหน่วยเซนติเมตร (2D proxy ไม่ได้วัด 3D height จริง)
- ในการคำนวณ `coverage_ratio` ให้รวม mask ทั้ง plant และ leaf เพื่อไม่ให้นับซ้ำซ้อน

### 7.4 ขั้นตอนวิธีตัดสินใจ (Decision Algorithm)

ระบบใช้ rule-based algorithm (ไม่ใช่ machine learning model) สำหรับจัดกลุ่มขวดเป็น 3 คลาส เพื่อให้สามารถตรวจสอบ ปรับแก้ และอธิบายการตัดสินใจได้ (interpretable/explainable)

**ตารางที่ 2: เกณฑ์การจัดกลุ่มเบื้องต้น (Rough Thresholds — รอการเทียบค่ากับข้อมูลในห้องปฏิบัติการจริง)**

| คลาส | เงื่อนไข |
|---|---|
| **wait** | `days_since_last_subculture < 21` หรือ (`0 ≤ coverage_ratio < 0.35` และ `days_since_last_subculture ≤ 45`) |
| **subculture** | `0.35 ≤ coverage_ratio ≤ 0.70` และ `21 ≤ days_since_last_subculture ≤ 45` (และไม่เข้าเงื่อนไข transplant-overdue) |
| **transplant-overdue** | `coverage_ratio > 0.80` หรือ `days_since_last_subculture > 60` หรือ (`coverage_ratio > 0.70` และ `shoot_count` ลดลง/คงที่จากรอบก่อน) |

**⚠️ คำเตือน:** ตัวเลข 0.35, 0.70, 0.80, 21, 45, 60 ในตารางข้างต้นเป็นค่า rough ที่สังเคราะห์จากวรรณกรรมข้ามชนิดพืช (Pastelín Solano et al., 2019; Regni et al., 2025; Barua et al., 2022; Muhammad et al., 2004) — ยังไม่ผ่านการเทียบค่าจริงในห้องปฏิบัติการที่ทีมใช้งาน ในระบบจริง threshold เหล่านี้สามารถปรับค่าได้ (configurable) และต้องได้รับการ calibrate ก่อนนำไปใช้ในห้องปฏิบัติการใด

**7.4.1 การคำนวณ confidence score**

```
confidence = base_confidence × (1 - glare_penalty)
```

โดยที่:
- `base_confidence` = 0.85 (ค่าเริ่มต้น หากเข้าเงื่อนไขของคลาสโดยตรง)
- `glare_penalty` = min(glare_score × 2, 0.5) — ลด confidence เมื่อ glare สูง
- ถ้า `coverage_ratio` และ `days_since_last_subculture` ให้ผลตรงกันข้าม (เช่น coverage สูงแต่วันน้อย) ให้ลด base_confidence เหลือ 0.60 ก่อนคูณ glare_penalty

**7.4.2 การปรับแก้โดยผู้ใช้ (Manual Override)**

ทุกรายการที่ระบบประมวลผลจะแสดงผลลัพธ์พร้อม:
- คลาสที่ทำนาย + confidence score
- ภาพที่ overlay mask + bbox
- ปุ่ม "เปลี่ยนคลาส" ให้ผู้ใช้เลือกคลาสด้วยตนเอง
- ช่องบันทึกหมายเหตุ (optional)

### 7.5 การตรวจสอบความถูกต้อง (Validation)

1. **เปรียบเทียบกับ ground truth:** นำภาพขวดที่ถ่ายพร้อม metadata + การประเมินโดยนักวิทยาศาสตร์มาทดสอบระบบ คำนวณ confusion matrix, precision, recall, F1-score สำหรับแต่ละคลาส
2. **Iterative threshold tuning:** หากผล validation แรกต่ำกว่าเป้าหมาย (accuracy < 70%) ให้ปรับ threshold ในตารางที่ 2 แล้วทดสอบซ้ำ บันทึกทุกการเปลี่ยนแปลง
3. **Cross-species test:** ทดสอบระบบกับพืชต่างชนิดกันเพื่อดูว่า threshold ชุดเดียวใช้ได้กับทุกชนิดหรือไม่ หากผลต่างกันมาก ต้องแนะนำให้ calibrate threshold ต่อชนิดพืช
4. **Inter-rater reliability:** หากเป็นไปได้ ให้เปรียบเทียบการประเมินระหว่างนักวิทยาศาสตร์ 2 คนขึ้นไป เพื่อดู baseline ของมนุษย์เองก่อนเปรียบเทียบกับระบบ

---

## 8. การวิเคราะห์ข้อมูล

### 8.1 การวิเคราะห์ความสัมพันธ์ระหว่าง Feature กับ Subculture Readiness

- ใช้ scatter plot และ box plot แสดงการกระจายตัวของแต่ละ feature จำแนกตาม 3 คลาส (wait / subculture / transplant-overdue)
- คำนวณ correlation matrix ระหว่าง features เพื่อตรวจสอบ multicollinearity (เช่น coverage_ratio กับ shoot_count)
- วิเคราะห์ว่าชุด feature ใดที่มีอำนาจจำแนกสูงสุดโดยใช้ feature importance จาก simple decision tree (ใช้เพื่อการวิเคราะห์เท่านั้น — algorithm จริงเป็น rule-based)
- เปรียบเทียบผลระหว่างพืชต่างชนิดว่า feature thresholds ต้องปรับต่างกันหรือไม่

### 8.2 การประเมินความแม่นยำของระบบ (Classification Metrics)

**ตารางที่ 3: แม่แบบ confusion matrix สำหรับการประเมินผล**

| จริง \ ทำนาย | wait | subculture | transplant-overdue |
|---|---|---|---|
| **wait** | TN_wait | FP_subculture | FP_transplant |
| **subculture** | FN_wait (missed) | TP_subculture | FP_transplant |
| **transplant-overdue** | FN_wait | FN_subculture | TP_transplant |

เมตริกหลักที่ใช้:
- **Accuracy:** สัดส่วนการทำนายถูกต้องทั้งหมด (เป้าหมาย ≥ 70%)
- **Precision (ต่อคลาส):** ความแม่นยำเมื่อระบบบอกว่าคลาสนั้น
- **Recall/Sensitivity (ต่อคลาส):** ความสามารถในการตรวจจับคลาสนั้น (เป้าหมาย ≥ 0.6 สำหรับคลาส subculture)
- **F1-score:** ค่าเฉลี่ย harmonic ระหว่าง precision และ recall

### 8.3 การปรับเทียบ Threshold (Threshold Tuning)

ใช้ validation set เพื่อทดสอบค่า threshold ที่แตกต่างกัน:
- coverage_ratio: ทดสอบตั้งแต่ 0.25-0.85 (step 0.05)
- days_since_last_subculture: ทดสอบตั้งแต่ 14-70 (step 7)
- เลือกชุด threshold ที่ให้ Matthews Correlation Coefficient (MCC) สูงสุด (เนื่องจากคลาสไม่สมดุล — expected class imbalance)

---

## 9. แผนการดำเนินงาน (Gantt Chart — 3 เดือน)

| กิจกรรม | เดือนที่ 1 | เดือนที่ 2 | เดือนที่ 3 |
|---|---|---|---|
| **สัปดาห์ที่:** | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 9.1 เก็บข้อมูลภาพถ่ายขวด + metadata | █ | █ | | | | | | | | | | |
| 9.2 สร้าง ground truth (annotation + expert evaluation) | | █ | █ | | | | | | | | | |
| 9.3 พัฒนา Android app skeleton + camera integration | | | █ | █ | █ | | | | | | | |
| 9.4 เชื่อมต่อ Roboflow SAM3 PCS API + ทดสอบ | | | | █ | █ | | | | | | | |
| 9.5 สร้าง feature extraction module | | | | | █ | █ | | | | | | |
| 9.6 สร้างและปรับ rule-based decision algorithm | | | | | | █ | █ | | | | | |
| 9.7 ทดสอบระบบ + confusion matrix | | | | | | | █ | █ | █ | | | |
| 9.8 ปรับเทียบ threshold + validate ข้ามชนิดพืช | | | | | | | | | █ | █ | | |
| 9.9 เขียนรายงาน + เตรียม diagram | | | | | | | | | | █ | █ | |
| 9.10 ทบทวน + ส่ง proposal | | | | | | | | | | | █ | █ |

**หมายเหตุ:** แผนงานนี้ยืดหยุ่นและอาจปรับเปลี่ยนตามความพร้อมของวัสดุพืชในห้องปฏิบัติการและผลการทดสอบระหว่างทาง

---

## 10. ความเสี่ยงและแนวทางแก้ไข

| ความเสี่ยง | ระดับ | ผลกระทบ | แนวทางแก้ไข |
|---|---|---|---|
| SAM3 PCS ให้ segmentation คุณภาพต่ำสำหรับพืชบางชนิดหรือระยะการเจริญที่ผิดปกติ | ปานกลาง | feature ผิดพลาด → classification ผิด | (1) ใช้วิธีการส่งหลาย prompt (เพิ่ม "shoot", "root" หากจำเป็น) (2) ใช้ confidence threshold adjustment (3) สลับเป็น bounding box prompt (SAM3 PCS รองรับ) ถ้า polygon ไม่แม่น |
| Glare หรือ condensation รุนแรงจนมองไม่เห็นต้นพืชในภาพ | สูง | glare_score สูง → confidence ต่ำ → ระบบไม่มั่นใจ | (1) glare_score = 0.5 → ให้ flag "ภาพมี glare สูง" และให้ผู้ใช้ถ่ายใหม่โดยปรับแสง (2) ใช้ cross-polarization filter ถ้าจำเป็น |
| ระบบพึ่งพาการเชื่อมต่ออินเทอร์เน็ต (cloud API) | ปานกลาง | ไม่สามารถใช้งานในพื้นที่ที่ไม่มีสัญญาณ | (1) แจ้งเตือนสถานะ connection (2) บันทึกภาพใน local queue เพื่อส่งเมื่อมีสัญญาณ (3) ระยะยาว: พิจารณา on-device model (เช่น SAM3 เบาขนาด quantized) ถ้า Roboflow API latency สูงเกินไป |
| Threshold จาก literature ไม่เหมาะสมกับพืชจริงในห้องปฏิบัติการ | สูง | classification ผิดพลาดมาก (> 50%) | (1) threshold เป็น configurable (2) calibration กับ ground truth ก่อนใช้จริง (3) สร้างโหมด "เรียนรู้ threshold อัตโนมัติ" จากชุดข้อมูลที่ผู้ใช้ป้อน |
| จำนวนตัวอย่างไม่เพียงพอสำหรับ validation โดยเฉพาะคลาส transplant-overdue | ปานกลาง | validation ไม่น่าเชื่อถือ | (1) ใช้ stratified sampling (2) กรณี sample น้อย ใช้ leave-one-out หรือ bootstrapped confidence interval แทน split-test |

---

## 11. ประโยชน์ที่คาดว่าจะได้รับ

1. **เพิ่มประสิทธิภาพห้องปฏิบัติการเพาะเลี้ยงเนื้อเยื่อ:** ลดเวลาที่นักวิทยาศาสตร์ต้องใช้ในการตรวจสอบขวดทีละขวด — ระบบช่วยคัดกรองขวดที่ "พร้อมตัดย้าย" ก่อน แล้วให้นักวิทยาศาสตร์ตรวจสอบขวดที่ระบบระบุว่ายังไม่พร้อมหรือเกินเวลาเฉพาะในกรณีที่ confidence ต่ำ

2. **การติดตามแบบไม่ทำลายตัวอย่าง (Non-destructive monitoring):** ไม่ต้องเปิดขวดหรือสัมผัสพืชเพื่อประเมินสภาพ ซึ่งลดความเสี่ยงการปนเปื้อน (contamination) — สอดคล้องกับแนวทางของ Bethge et al. (2023)

3. **เครื่องมือช่วยตัดสินใจ (Decision-support tool) ที่ทำงานข้ามชนิดพืช:** เป็นครั้งแรกที่มีระบบ zero-shot ที่ปรับใช้กับพืชหลายชนิดโดยไม่ต้อง retrain โมเดล ซึ่งแตกต่างจากระบบ CV เฉพาะพืชที่ผ่านมา — ช่วยลดต้นทุนในการพัฒนาโมเดลต่อชนิดพืช

4. **การจัดลำดับความสำคัญของงานในห้องปฏิบัติการ:** นักวิทยาศาสตร์สามารถจัดลำดับขวดที่ต้องตัดย้ายก่อน-หลังตามความเร่งด่วน (คลาส transplant-overdue ควรมาก่อน subculture ปกติ) ลดความสูญเสียจาก overcrowding

5. **การบันทึกประวัติการเจริญเติบโต (Growth history tracking):** เมื่อใช้ระบบอย่างต่อเนื่องหลายรอบ subculture จะได้ข้อมูลอนุกรมเวลา (time-series) ของ coverage_ratio, shoot_count ต่อขวด ซึ่งอาจใช้วิเคราะห์แนวโน้มและคาดการณ์ล่วงหน้าได้

6. **ต้นทุนต่ำ ใช้ง่าย:** ใช้เพียงสมาร์ตโฟน Android ที่มีอยู่แล้วในห้องปฏิบัติการส่วนใหญ่ ไม่ต้องซื้อ hardware เพิ่ม (ต่างจากระบบเฉพาะทาง)

---

## 12. การเปิดเผยข้อมูลการใช้ Generative AI (Gen-AI Disclosure)

โครงงานนี้ใช้เครื่องมือ Generative AI (Gen-AI) ในหลายขั้นตอนของกระบวนการพัฒนาและเขียนข้อเสนอโครงงาน โดยมีการเปิดเผยรายละเอียดดังนี้

### 12.1 เครื่องมือที่ใช้

| เครื่องมือ | ผู้พัฒนา | เวอร์ชัน/วันที่ | การใช้งาน |
|---|---|---|---|
| Claude Opus 4.8 | Anthropic | กรกฎาคม 2569 | การสังเคราะห์วรรณกรรม การเขียนข้อเสนอโครงงาน การออกแบบ pipeline |
| DeepSeek V4 | 深度求索 (DeepSeek) | กรกฎาคม 2569 | การช่วยเขียนและตรวจทานเนื้อหาทางเทคนิค |
| Roboflow AI | Roboflow Inc. | กรกฎาคม 2569 | การติดต่อและประมวลผล SAM3 PCS API |
| Consensus (AI Research Search) | Consensus Inc. | กรกฎาคม 2569 | การค้นหาและตรวจสอบวรรณกรรมทางวิทยาศาสตร์ |
| PubMed MCP | NCBI/NLM | กรกฎาคม 2569 | การเข้าถึงเนื้อหาเต็มของบทความวิจัย |

### 12.2 ขอบเขตการใช้งาน

1. **การสังเคราะห์วรรณกรรมและการตรวจสอบการอ้างอิง (Literature Synthesis & Citation Verification):** ใช้ Consensus AI และ PubMed MCP ในการค้นหา ตรวจสอบ และยืนยันความถูกต้องของบทความวิจัยที่อ้างอิงในข้อเสนอโครงงานนี้ ทุกการอ้างอิงที่ปรากฏในบรรณานุกรมผ่านการตรวจสอบยืนยันจากฐานข้อมูลจริง (Consensus หรือ PubMed) ว่าเป็นบทความที่มีอยู่จริง มี DOI/URL ที่เข้าถึงได้ และเนื้อหาที่อ้างอิงตรงกับต้นฉบับ — **ไม่มีรายการอ้างอิงใดที่มาจากการสร้างข้อมูลเทียมของ AI (AI hallucination)**

2. **การเขียนข้อเสนอโครงงาน (Proposal Writing Assistance):** ใช้ Claude Opus 4.8 เป็นผู้ช่วยในการเรียบเรียงเนื้อหาส่วนต่าง ๆ ของข้อเสนอ โดยเฉพาะการจัดโครงสร้างแบบพีระมิด (pyramid structure) ในบทนำ การออกแบบวิธีการดำเนินการ และการเรียบเรียงภาษาไทยทางวิชาการ — เนื้อหาทั้งหมดได้รับการตรวจทานและปรับแก้โดยผู้พัฒนาโครงงานก่อนนำไปใช้

3. **การสร้างโค้ด (Code Generation):** ใช้ Claude Opus 4.8 ในการช่วยเขียนโค้ดต้นแบบสำหรับ Android application, การเชื่อมต่อ Roboflow SAM3 PCS API, และการคำนวณ feature extraction — โค้ดทุกส่วนผ่านการตรวจสอบและทดสอบโดยผู้พัฒนา

4. **การสร้าง Diagram (Diagram Generation):** [ระบุเครื่องมือที่ใช้หากใช้ Gen-AI สร้าง diagram เช่น "ใช้ Claude ในการช่วยออกแบบ architecture diagram"] — diagram ที่ใช้ในข้อเสนอโครงงานเป็นภาษาอังกฤษและมีที่มาของเนื้อหาที่อ้างอิง

### 12.3 ข้อจำกัดและการตรวจสอบโดยมนุษย์

ผู้พัฒนาโครงงานตระหนักดีว่า Generative AI มีข้อจำกัด โดยเฉพาะในเรื่อง:
- อาจสร้างข้อมูลอ้างอิงที่ไม่มีอยู่จริง (hallucination)
- ความไม่แม่นยำของเนื้อหาเชิงเทคนิคเฉพาะทาง
- อคติที่แฝงในข้อมูลเทรนของโมเดล

ด้วยเหตุนี้ _ทุกเนื้อหา_ ที่ได้จาก Gen-AI จึงผ่านการตรวจสอบทุกรายการดังนี้:
- ✓ การอ้างอิงวรรณกรรมทุกจุด — ตรวจสอบเทียบกับบทความจริงใน Consensus/PubMed
- ✓ โค้ดทุกส่วน — ทดสอบการทำงานจริง
- ✓ เนื้อหาทางชีววิทยา — ตรวจทานกับแหล่งอ้างอิงหลัก (primary literature)
- ✓ ภาษาและความถูกต้องของข้อความ — ตรวจทานโดยผู้พัฒนา

ผู้พัฒนาโครงงานขอรับผิดชอบต่อเนื้อหาทั้งหมดในข้อเสนอโครงงานนี้ แม้ส่วนที่เขียนโดยใช้เครื่องมือ Gen-AI ก็ตาม

---

## 13. บรรณานุกรม

**หมายเหตุ:** การอ้างอิงทั้งหมดในเอกสารนี้ผ่านการตรวจสอบการมีอยู่จริงและความถูกต้องของเนื้อหาผ่านฐานข้อมูล Consensus และ PubMed แล้ว (ยกเว้นรายการที่เป็นภาษาไทยซึ่งตรวจสอบจากแหล่งต้นทางโดยตรง) — ไม่มีรายการอ้างอิงใดที่ถูกสร้างขึ้นโดย AI โดยไม่มีการยืนยัน

Abdalla, N., El-Ramady, H., Seliem, M. K., El-Mahrouk, M. E., Taha, N., Bayoumi, Y., Shalaby, T. A., & Dobránszki, J. (2022). An academic and technical overview on plant micropropagation challenges. *Horticulturae, 8*(8), 677. https://doi.org/10.3390/horticulturae8080677

Amanlou, A., Suratgar, A. A., Tavoosi, J., Mohammadzadeh, A., & Mosavi, A. (2022). Single-image reflection removal using deep learning: A systematic review. *IEEE Access, 10*, 29937–29953. https://doi.org/10.1109/ACCESS.2022.3156273

Barua, K. N., Singha, B. L., Bordoloi, S., & Bora, B. (2022). In vitro seed propagation and mass multiplication of some magnificent orchids of Northeast India. *Journal of Medicinal Plants Studies, 10*(2c), 208–213. https://doi.org/10.22271/plants.2022.v10.i2c.1411

Bethge, H., Winkelmann, T., Lüdeke, P., & Rath, T. (2023). Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture. *Plant Methods, 19*, 42. https://doi.org/10.1186/s13007-023-01018-w

Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R., Suris, D., Ryali, C., Alwala, K. V., Khedr, H., Huang, A., Lei, J., Ma, T., Guo, B., Kalla, A., Marks, M., Greer, J., Wang, M., Sun, P., Rädle, R., … Feichtenhofer, C. (2025). SAM 3: Segment anything with concepts. *arXiv*. https://arxiv.org/abs/2511.16719

Chandran, H., Meena, M., Barupal, T., & Sharma, K. (2020). Plant tissue culture as a perpetual source for production of industrially important bioactive compounds. *Biotechnology Reports, 26*, e00450. https://doi.org/10.1016/j.btre.2020.e00450

Gatkal, N., Dhar, T., Prasad, A., Prajwal, R., Santosh, Jyoti, B., Roul, A. K., Potdar, R., Mahore, A., Parmar, B. S., & Vala, V. (2024). Development of a user-friendly automatic ground-based imaging platform for precise estimation of plant phenotypes in field crops. *Journal of Field Robotics, 41*(7), 2355–2372. https://doi.org/10.1002/rob.22254

Hasnain, A., Naqvi, S. A. H., Ayesha, S. I., Khalid, F., Ellahi, M., Iqbal, S., Hassan, M. Z., Abbas, A., Adamski, R., Markowska, D., Baazeem, A., Mustafa, G., Moustafa, M., Hasan, M. E., & Abdelhamid, M. M. A. (2022). Plants in vitro propagation with its applications in food, pharmaceuticals and cosmetic industries; current scenario and future approaches. *Frontiers in Plant Science, 13*, 1009395. https://doi.org/10.3389/fpls.2022.1009395

Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P., & Girshick, R. (2023). Segment anything. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) 2023*. https://arxiv.org/abs/2304.02643

Muhammad, A., Hussain, I., Saqlan Naqvi, S. M., & Rashid, H. (2004). Banana plantlet production through tissue culture. *Pakistan Journal of Botany, 36*, 617–620. https://www.musalit.org/seeMore.php?id=9468

Murphy, R., & Adelberg, J. (2021). Physical factors increased quantity and quality of micropropagated shoots of *Cannabis sativa* L. in a repeated harvest system with ex vitro rooting. *In Vitro Cellular & Developmental Biology - Plant, 57*(6), 923–931. https://doi.org/10.1007/s11627-021-10166-4

Nongdam, P., Beleski, D. G., Tikendra, L., Dey, A., Varte, V., El Merzougui, S., Pereira, V. M., Barros, P. R., & Vendrame, W. A. (2023). Orchid micropropagation using conventional semi-solid and temporary immersion systems: A review. *Plants, 12*(5), 1136. https://doi.org/10.3390/plants12051136

Pastelín Solano, M. C., Salinas Ruíz, J., González Arnao, M. T., Castañeda Castro, O., Galindo Tovar, M. E., & Bello Bello, J. J. (2019). Evaluation of in vitro shoot multiplication and ISSR marker based assessment of somaclonal variants at different subcultures of vanilla (*Vanilla planifolia* Jacks). *Physiology and Molecular Biology of Plants, 25*(2), 561–567. https://doi.org/10.1007/s12298-019-00645-9

Ravi, N., Gabeur, V., Hu, Y.-T., Hu, R., Ryali, C., Ma, T., Khedr, H., Rädle, R., Rolland, C., Gustafson, L., Mintun, E., Pan, J., Alwala, K. V., Carion, N., Wu, C.-Y., Girshick, R., Dollár, P., & Feichtenhofer, C. (2024). SAM 2: Segment anything in images and videos. *arXiv*. https://arxiv.org/abs/2408.00714

Regni, L., Calisti, S., Cesarini, A., Marconi, L., Proietti, P., Zollini, S., & Brigante, R. (2025). Micropropagation of blackberry and blueberry: Assessing the effects of subculture duration and explant density through the integration of traditional measurements and smartphone 3D imaging. *Plant Cell, Tissue and Organ Culture, 163*, 63. https://doi.org/10.1007/s11240-025-03267-0

Suarez, E., Blaser, M., & Sutton, M. (2025). Automating leaf area measurement in citrus: The development and validation of a Python-based tool. *Applied Sciences, 15*(17), 9750. https://doi.org/10.3390/app15179750

Thammasiri, K. (2015). Current status of orchid production in Thailand. *Acta Horticulturae, 1078*, 25–33. https://doi.org/10.17660/ActaHortic.2015.1078.2

ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค), สวทช. (2563, 12 มิถุนายน). *ไบโอเทค สวทช. พัฒนาระบบเพาะเลี้ยงพืชในอาหารเหลว เพิ่มกำลังการขยายพันธุ์ต้นกล้า*. https://www.nstda.or.th/home/news_post/biotec-bioreactor/

ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค), สวทช. (2565, 3 พฤษภาคม). *ความสำเร็จในการขยายผลการผลิตต้นกล้าอินทผลัมในเชิงพาณิชย์ ด้วยเทคโนโลยีการเพาะเลี้ยงเนื้อเยื่อสู่เกษตรกรไทย*. https://www.biotec.or.th/home/tissueculture-dates/

---

*เอกสารนี้เป็นร่าง (draft) สำหรับ proposal ส่วนที่ 1 ของโครงงาน VitroVision เพื่อส่งประกวด YSC 2027 สาขา CSBI — ยังไม่ผ่านการตรวจสอบโดย auditor และยังไม่ใช่ฉบับสมบูรณ์*
