## รหัสโครงการ: 29YCSE00054T

**ชื่อโครงงาน (ภาษาไทย):** VitroVision : การประยุกต์ใช้ปัญญาประดิษฐ์เชิงคอมพิวเตอร์วิทัศน์เพื่อวิเคราะห์และทำนายการเจริญเติบโตของพืชเพาะเลี้ยงเนื้อเยื่อ

**ชื่อโครงงาน (ภาษาอังกฤษ):** VitroVision : Application of AI-Based Computer Vision for Analyzing and Predicting the Growth of Tissue Cultured Plants

**สาขา:** CSAI (Computer Science and Artificial Intelligence — AI/ML)

## บทคัดย่อ/บทสรุป (Abstract/Synopsis)

2. บทคัดย่อ

การเพาะเลี้ยงเนื้อเยื่อพืช (plant tissue culture) เป็นเทคโนโลยีหลักของการขยายพันธุ์พืชเชิงพาณิชย์ แต่การตัดสินใจว่าเมื่อใดจึงควรย้ายต้นออกอนุบาล (acclimatization) ยังคงอาศัยการตรวจด้วยสายตาของนักวิทยาศาสตร์เป็นรายขวด ซึ่งเป็นคอขวดด้านแรงงานและเวลา และมีความแปรปรวนระหว่างผู้ประเมิน การเปิดขวดเพื่อวัดมีความเสี่ยงต่อการปนเปื้อน จึงจำเป็นต้องประเมินแบบไม่ทำลายผ่านขวดแก้วปิด ซึ่งมีอุปสรรคจากแสงสะท้อน (glare) ไอน้ำ และความโค้งของแก้ว

โครงงานนี้มุ่งพัฒนาและประเมินระบบวิเคราะห์การเจริญเติบโตของพืชเพาะเลี้ยงเนื้อเยื่อแบบไม่ทำลายผ่านขวดแก้วปิดด้วยคอมพิวเตอร์วิทัศน์ โดยเป็น**งานต่อเนื่องที่เริ่มดำเนินการแล้วและจะแล้วเสร็จภายในปีนี้** งานที่เริ่มไปแล้วประกอบด้วย (1) การทบทวนวรรณกรรมด้าน segmentation สำหรับงานเพาะเลี้ยงเนื้อเยื่อและ foundation model (2) **การสร้างชุดข้อมูลภาพถ่ายจริงผ่านขวดแก้ว 100 ขวด พร้อมบันทึกค่าอ้างอิงจากผู้ประเมิน** และ (3) **การทดลองนำร่องด้วยแบบจำลอง Segment Anything Model 3 (SAM3) แบบ zero-shot** ซึ่งผลเบื้องต้นชี้**ความเป็นไปได้**ของแนวทาง: ค่าลักษณะที่วัดจากภาพสอดคล้องกับการวัดด้วยมือ (สหสัมพันธ์ของความสูง r = 0.638 ดีกว่า classical 0.498 / YOLO-COCO 0.133) และเกณฑ์ความสูงของต้นสอดคล้องกับการประเมินของผู้เชี่ยวชาญในเบื้องต้น (accuracy 0.755, sensitivity 0.917) ทั้งนี้ผลดังกล่าวยังเป็นเพียงผลนำร่อง ยังต้องยืนยันด้วยการประเมินที่เข้มข้นขึ้นกับผู้ประเมินหลายคนและการเทียบกับวิธีพื้นฐาน

แผนดำเนินงานต่อเนื่องที่เหลือ ครอบคลุมการประเมินเปรียบเทียบกับวิธีพื้นฐาน (SAM2, YOLO-seg, การแบ่งส่วนเชิงคลาสสิก) การตรวจสอบระดับพิกเซลกับ ground truth ที่ผู้ประเมินกำกับ (mIoU/Dice/F1) การวิเคราะห์ความไวของพรอมป์และเกณฑ์ตัดสินใจ การกลั่นแบบจำลองขนาดใหญ่เป็น **U-Net ขนาดเล็ก** ที่ทำงานบนอุปกรณ์ทั่วไป และการทดสอบข้ามชนิดพืช เพื่อให้ได้ระบบต้นทุนต่ำที่ห้องปฏิบัติการเพาะเลี้ยงเนื้อเยื่อใช้งานได้จริง พร้อมชุดข้อมูลเปิดสำหรับการวิจัยต่อยอด

---

**คำสำคัญ (Keywords):** การเพาะเลี้ยงเนื้อเยื่อ, การวัดลักษณะปรากฏของพืชด้วยภาพ, การแบ่งส่วนภาพ, แบบจำลองพื้นฐาน, zero-shot, การทำนายการเจริญ

## บทนำ (Introduction)

### 1 ความสำคัญของการเพาะเลี้ยงเนื้อเยื่อพืชในระดับโลกและไทย

การเพาะเลี้ยงเนื้อเยื่อพืช (plant tissue culture หรือ micropropagation) เป็นเทคโนโลยีการขยายพันธุ์พืชที่ใช้ชิ้นส่วนขนาดเล็ก (explant) เพาะเลี้ยงในสภาพปลอดเชื้อบนอาหารสังเคราะห์ ปัจจุบันเทคโนโลยีนี้ถูกใช้อย่างกว้างขวางในเชิงพาณิชย์ครอบคลุมพืชเกษตร อาหาร เภสัชกรรม และเครื่องสำอางทั่วโลก (Hasnain et al., 2022) และเป็นแหล่งผลิตสารออกฤทธิ์ทางชีวภาพระดับอุตสาหกรรมที่ไม่ขึ้นกับฤดูกาลหรือสภาพภูมิอากาศ (Chandran et al., 2020)

สำหรับประเทศไทย การเพาะเลี้ยงเนื้อเยื่อมีบทบาทสำคัญอย่างยิ่งในอุตสาหกรรมกล้วยไม้ ซึ่งเป็นสินค้าส่งออกสำคัญที่ประเทศไทยมีพื้นที่ปลูกประมาณ 7,420 เอเคอร์ (ราว 18,770 ไร่, ข้อมูล พ.ศ. 2555) และส่งออกมากกว่า 50% ของผลผลิตไปยังกว่า 148 ประเทศ (Thammasiri, 2015) นอกจากนี้หน่วยงานวิจัยของไทย เช่น ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค) ได้พัฒนาและถ่ายทอดเทคโนโลยีการเพาะเลี้ยงเนื้อเยื่อในเชิงพาณิชย์สำหรับพืชหลายชนิด เช่น อินทผลัมพันธุ์บาฮี (ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ, 2565) และระบบเพาะเลี้ยงในอาหารเหลวด้วย bioreactor สำหรับปาล์มน้ำมันและมะพร้าวที่ช่วยเพิ่มความเร็วในการขยายพันธุ์ 3-4 เท่า (ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ, 2563)

### 2 ปัญหา: การตัดสินใจย้ายต้นออกอนุบาล (acclimatization) ยังเป็นคอขวด

แม้เทคโนโลยีเพาะเลี้ยงเนื้อเยื่อจะพัฒนาไปมาก แต่กระบวนการหนึ่งที่ยังคงพึ่งพาแรงงานคนอย่างมากคือการตัดสินใจว่าเมื่อใดจึงควรย้ายต้นกล้าออกจากขวดไปยังสภาพอนุบาล (acclimatization/hardening) ซึ่งเป็นขั้นตอนที่ต้องพิจารณารายขวด ทุก 3-8 สัปดาห์ของรอบการขยายพันธุ์ ขึ้นกับชนิดพืช (Pastelín Solano et al., 2019; Regni et al., 2025; Barua et al., 2022) การตัดสินใจที่ผิดพลาด — ย้ายเร็วเกินไป (ต้นยังไม่สมบูรณ์ มีระบบรากไม่ดี) หรือช้าเกินไป (แออัด เสี่ยง hyperhydricity) — อาจส่งผลกระทบร้ายแรง เช่น การตายของเนื้อเยื่อ (necrosis) และประสิทธิภาพการขยายพันธุ์ที่ลดลง (Abdalla et al., 2022)

ปัจจุบันการประเมินความพร้อมอนุบาลในห้องปฏิบัติการส่วนใหญ่อาศัยการตรวจสอบด้วยสายตาของนักวิทยาศาสตร์เป็นรายขวด ซึ่งเป็นกระบวนการที่ "ใช้แรงงานมากและมีค่าใช้จ่ายสูง" (Murphy & Adelberg, 2021) และในระบบ semi-solid ที่แพร่หลายที่สุด ก็ยังมีข้อจำกัดด้าน "อัตราการเพิ่มจำนวนต่ำและต้นทุนการผลิตสูง" (Nongdam et al., 2023) ยิ่งไปกว่านั้น ในห้องปฏิบัติการที่มีปริมาณขวดหลายร้อยถึงหลายพันขวด การตรวจสอบรายขวดอย่างละเอียดทำได้ไม่ทั่วถึง นักวิทยาศาสตร์มักใช้ประสบการณ์ส่วนบุคคลในการตัดสินใจ ซึ่งมีความแปรปรวนสูงระหว่างบุคคล

### 3 ช่องว่างขององค์ความรู้ (Research Gap)

งานวิจัยที่ผ่านมามีความพยายามในการนำ computer vision มาใช้กับพืชเพาะเลี้ยงเนื้อเยื่อแบบไม่ทำลายตัวอย่าง (non-destructive) ผ่านขวดปิด เช่น ระบบ "Phenomenon" ที่ใช้ multi-sensor และ random forest segmentation สำหรับวัด projected area และ canopy height (Bethge et al., 2023) แต่ระบบดังกล่าวเป็น hardware เฉพาะราคาสูงและยังไม่ใช้ foundation model ที่สามารถ zero-shot ข้ามชนิดพืชได้

ในด้านการประเมินความหนาแน่นของพืชในขวด Regni et al. (2025) เป็นงานที่ใกล้เคียงกับแนวทางของเรามากที่สุด โดยใช้ภาพถ่าย 3D จากสมาร์ตโฟนวัด canopy/covered area ต่อขวดและ shoot density ใน blackberry และ blueberry แต่ยังไม่มีงานใดที่ใช้ zero-shot foundation model ในการ segment ผ่านขวดแก้วโดยตรง หรือพัฒนาระบบ decision-support สำหรับจัดกลุ่มความพร้อมอนุบาลโดยอิงระบบราก

**ช่องว่างที่เหลืออยู่:** (1) ยังไม่มีระบบ low-cost ที่ติดตามการเจริญของต้นกล้าในขวด **ตามเวลา (time-series)** แบบ end-to-end ตั้งแต่ถ่ายภาพ → แบ่งส่วน → เก็บ feature → วิเคราะห์อัตราการเจริญ → แจ้งเตือนความพร้อมอนุบาล (2) ยังไม่มีงาน zero-shot foundation model ที่ถูกประเมินเทียบกับวิธีพื้นฐาน (baseline) ด้วยชุดข้อมูลภาพผ่านขวดแก้วโดยตรง และ (3) ยังไม่มีชุดข้อมูลเปิดของภาพเพาะเลี้ยงเนื้อเยื่อผ่านขวดแก้วสำหรับการวิจัยต่อ — **นี่คือช่องว่างที่โครงงานนี้มุ่งตอบ**

**นอกจากนี้ยังไม่มีระบบ low-cost (ใช้เพียงสมาร์ตโฟน) ที่สามารถทำงานข้ามชนิดพืช (cross-species) โดยไม่ต้องฝึกโมเดลใหม่ (re-train) สำหรับพืชแต่ละชนิด** — นี่คือช่องว่างที่ VitroVision มุ่งตอบ

### 4 คำถามวิจัย (Research Question)

ด้วยภาพถ่ายเพียงภาพเดียว (single snapshot) ผนวกกับ SAM3 PCS zero-shot segmentation (พรอมป์ 5 คำ รวม root + การตรวจจับขอบเขตขวด) และ rule-based triage algorithm ระบบสามารถจัดกลุ่มความพร้อมอนุบาลของขวดเพาะเลี้ยงเนื้อเยื่อ (ยังไม่พร้อม / พร้อมอนุบาล โดยมีเงื่อนไขส่งภาพที่ประมวลผลไม่ชัดให้มนุษย์ตรวจ) ได้ถูกต้องเพียงใดเมื่อเทียบกับวิธีพื้นฐาน (baseline) และค่าอ้างอิงจากผู้ประเมิน?

### 5 วัตถุประสงค์ของโครงงาน

เพื่อพัฒนาระบบประเมินความพร้อมอนุบาลของต้นกล้าเพาะเลี้ยงเนื้อเยื่อแบบไม่ทำลายผ่านขวดแก้ว ด้วย SAM3 zero-shot segmentation และขยายสู่การติดตามการเจริญตามเวลา (time-series monitoring) เปรียบเทียบกับวิธีพื้นฐาน (baseline) และตรวจสอบความถูกต้องกับค่าอ้างอิงจากผู้ประเมิน (ground truth) — รายละเอียดในหัวข้อ 4

### 6 สมมติฐาน

**H₁:** SAM3 PCS ที่ใช้ text prompts 5 คำ (plant, leaf, shoot, stem, root) สามารถ segment ต้นพืชเพาะเลี้ยงเนื้อเยื่อผ่านขวดแก้วที่มี glare, ฝ้า และ condensation ได้ โดยมี mIoU เฉลี่ย ≥ 0.65 เมื่อเทียบกับ ground truth ที่ annotate โดยมนุษย์ และสูงกว่า baseline (SAM2, YOLO-seg, การแบ่งส่วนเชิงคลาสสิก) อย่างมีนัยสำคัญ (อ้างอิงจากผล spike test 2026-07-05 และงาน Orvati Nia et al. 2026 ที่พบว่า SAM3 ให้ความแม่นยำสูงสุดข้ามโครงสร้างพืช)

**H₂:** ชุด feature 6 กลุ่ม (โครงสร้าง/อวัยวะ/ความซับซ้อน/สี/คุณภาพภาพ/verdict) ที่คำนวณจาก mask ของ SAM3 PCS — โดยเฉพาะสัดส่วนความสูงของต้น (height_proxy) ซึ่งเป็นตัวชี้วัดหลักของความพร้อมอนุบาลในรอบนี้ (หลังผลนำร่องพบว่าการตรวจจับรากผ่านขวดแก้วยังไม่ได้ผล จึงใช้ความสูงแทน ซึ่งตรงกับมุมของผู้เชี่ยวชาญ) — สามารถจัดกลุ่มความพร้อมอนุบาลด้วย rule-based algorithm ได้ถูกต้อง ≥ 70% เมื่อเทียบกับการประเมินโดยนักวิทยาศาสตร์ห้องปฏิบัติการ (ผลนำร่องเบื้องต้นชี้ทิศทางสอดคล้อง: accuracy 0.755, sensitivity 0.917 — ยังต้องยืนยันเพิ่มกับผู้ประเมินหลายคน)

### 7 ผลการทดลองนำร่อง (Pilot Results) [RESULT]

รัน `sam3_growth_pipeline.py` บนชุดภาพจริง 100 ขวดพริกจินดา (ชุด `data/raw/20260814_batch`, วันถ่าย 16 ก.ค./2 ส.ค./14 ส.ค. 2569) ผ่าน Colab T4 ได้ผลลัพธ์จริง (`data/processed/plant_growth_summary.csv`):

| กลุ่ม | จำนวนขวด | ร้อยละ |
|---|---|---|
| พร้อมอนุบาล | 75 | 75% |
| ยังไม่พร้อม | 25 | 25% |

**การตรวจสอบกับค่าอ้างอิงจากผู้ประเมิน (validation):** เกณฑ์ความพร้อมอิงความสูง (`height_proxy ≥ 0.275`) ตามนิยาม "ต้นสมบูรณ์/โตพอ/พร้อมย้าย" ของผู้ประเมิน → Accuracy 0.755, **Sensitivity 0.917**, F1 0.821, MCC 0.472 **[RESULT เบื้องต้น — ผลนำร่องชี้ความเป็นไปได้ ยังต้องยืนยันกับผู้ประเมินหลายคนและชุดประเมินที่เข้มข้นขึ้น]** ส่วนเกณฑ์เดิมที่อิง coverage_ratio ให้ accuracy = 0.43 / sensitivity = 0.15 (ไม่สอดคล้อง)

**ข้อจำกัดจากผลจริง:** (1) การตรวจจับระบบรากยังไม่ได้ผล — ตรวจพบรากเพียง 1/100 ภาพ จึงไม่ได้ใช้ root_ratio เป็นตัวชี้วัดอันดับ 1 ในรอบนี้ (หันไปใช้ความสูงแทนตามมุมผู้เชี่ยวชาญ) [OPEN — ต้องปรับปรุงพรอมป์/วิธี] (2) หน่วยทางกายภาพ — **calibrate เชิงประจักษ์แล้ว** (8/27): height `canopy_h_cm = 5.098*height_proxy + 1.432` (CV_MAE 1.15cm) · area cm² **calibrate ไม่ได้** เพราะค่าวัดมือ area_cm2 เองไม่น่าเชื่อถือ → รายงานซื่อตรง อย่าอ้าง area cm² [RESULT บางส่วน · geometric PIXEL_TO_CM รอขนาดขวดจริง] (3) ผลเป็น pilot (n = 98 ภาพที่ผู้ประเมินระบุชัด) ยังต้องตรวจกับผู้ประเมินหลายคน (inter-rater) ก่อนยืนยันเป็นข้อสรุป [PLAN] การประเมินเปรียบเทียบกับวิธีพื้นฐานระดับค่าวัด (trait เทียบมือ) ได้ผลแล้ว: SAM3 r=0.638 ดีกว่า classical 0.498 / YOLO-COCO 0.133 (ดู 7.6.0) [RESULT บางส่วน — ความสอดคล้องกับมือ] ส่วนระดับพิกเซล (mIoU/Dice) ยังต้อง annotate ground-truth masks [PLAN]

---

## 2. วัตถุประสงค์ (Objective/s)

วัตถุประสงค์ของโครงงานมีสามข้อหลัก โดยมุ่งให้ได้ผลลัพธ์ดังนี้

2.1 **พัฒนาและสร้างโมเดลที่ออกแบบมาโดยเฉพาะสำหรับการวิเคราะห์ต้นเพาะเลี้ยงเนื้อเยื่อในขวดแก้ว** โดยให้สามารถตรวจจับ จำแนก และวัดลักษณะเชิงปริมาณของต้นภายในขวดได้อย่างแม่นยำและอัตโนมัติ โดยไม่จำเป็นต้องเปิดขวดหรือทำลายตัวอย่างต้น ซึ่งเป็นข้อจำกัดสำคัญของงานเพาะเลี้ยงเนื้อเยื่อ

2.2 **ทดสอบและเปรียบเทียบประสิทธิภาพของโมเดลกับข้อมูลจริงที่ประเมินโดยผู้เชี่ยวชาญ** และเทียบกับโมเดลหรือวิธีวิเคราะห์ภาพอื่นที่มีความสามารถใกล้เคียงกัน ได้แก่ SAM2 ของ Meta ซึ่งเป็นโมเดลแบ่งส่วนรุ่นก่อนหน้า YOLO-seg เช่น YOLOv8-seg ของ Ultralytics และวิธีแบ่งส่วนเชิงคลาสสิก เช่น การแยกด้วยสีหรือวิธี Otsu เพื่อแสดงให้เห็นว่าโมเดลที่พัฒนาขึ้นมีระดับความแม่นยำและความสม่ำเสมออย่างไรเมื่อเทียบกับโมเดลหรือวิธีเหล่านี้ เมื่อนำไปใช้กับข้อมูลจริง

2.3 **แสดงให้เห็นว่าโมเดลช่วยลดภาระงานในกระบวนการเก็บข้อมูลและวิเคราะห์ข้อมูลได้จริง** โดยใช้ระยะเวลาที่ใช้ในการทำงานเป็นตัวชี้วัดเปรียบเทียบ เพื่อพิสูจน์ว่าโมเดลนี้เป็นเครื่องมือที่ช่วยลดระยะเวลาการทำงานของนักวิจัยหรือผู้ปฏิบัติงานในห้องปฏิบัติการได้อย่างเป็นรูปธรรม

---

## 3. สมมติฐาน (Hypothesis/es)

**สมมติฐานที่ 1 (เชิงเทคนิค — segmentation):** SAM3 PCS ที่ใช้ text prompts 5 คำ (plant, leaf, shoot, stem, root) สามารถ segment ต้นพืชเพาะเลี้ยงเนื้อเยื่อผ่านขวดแก้วซึ่งมีสิ่งรบกวนทางแสง (glare, condensation, reflection) ได้ โดยมีค่าเฉลี่ย Intersection over Union (mIoU) ระหว่าง mask ที่ได้จากการ segment อัตโนมัติกับ ground truth ที่ annotate โดยมนุษย์ ≥ 0.65 และสูงกว่า baseline ทั้ง 3 วิธี (SAM2, YOLO-seg, การแบ่งส่วนเชิงคลาสสิก)

**สมมติฐานที่ 2 (เชิงการประยุกต์ — การจัดกลุ่ม):** ชุด feature 6 กลุ่มที่คำนวณจาก SAM3 mask ผนวกกับ metadata (days_since_last_subculture) โดยเฉพาะสัดส่วนความสูงของต้น (height_proxy — ตัวชี้วัดหลักในรอบนี้ เนื่องจากสัดส่วนระบบรากยังตรวจจับผ่านขวดแก้วไม่ได้ผล) สามารถจำแนกขวดเพาะเลี้ยงเนื้อเยื่อออกเป็นกลุ่มความพร้อมอนุบาล (ยังไม่พร้อม / พร้อมอนุบาล) ได้ถูกต้อง ≥ 70% เมื่อเทียบกับการประเมินโดยนักวิทยาศาสตร์ที่มีประสบการณ์ในห้องปฏิบัติการ โดยมีค่า minimum sensitivity ≥ 0.6 สำหรับกลุ่มพร้อมอนุบาล (กลุ่มเป้าหมายหลัก)

---

## 4. วัสดุอุปกรณ์และสถานที่ดำเนินงาน (Materials and Workplace/s)

### 4.1 รายการวัสดุอุปกรณ์ (List of Materials)

4.1.1 สมาร์ตโฟน Samsung Galaxy S24 FE (กล้อง 50MP) และขาตั้งกล้อง — ถ่ายภาพขวดในระยะคงที่

4.1.2 ขวดเพาะเลี้ยงเนื้อเยื่อมาตรฐาน (ขวดแก้วใส) และพืชเพาะเลี้ยงเนื้อเยื่ออย่างน้อย 2–3 ชนิด

4.1.3 บัญชี Google Colab (โควตา GPU ฟรี) — รันโมเดล SAM3 และเทรนโมเดล

4.1.4 สิทธิ์เข้าถึงโมเดล `facebook/sam3` (Hugging Face, gated)

4.1.5 คอมพิวเตอร์สำหรับพัฒนา (เชื่อมต่ออินเทอร์เน็ต) + Python (OpenCV, PyTorch, segmentation-models-pytorch)

### 4.2 รายชื่อสถานที่ดำเนินงาน (List of Workplace/s)

4.2.1 ห้องปฏิบัติการเพาะเลี้ยงเนื้อเยื่อพืช โรงเรียนวิทยาศาสตร์จุฬาภรณราชวิทยาลัย บุรีรัมย์ (ถ่ายภาพชุดข้อมูลและเก็บค่าอ้างอิงจากผู้ประเมิน)

4.2.2 Google Colab / Hugging Face (ประมวลผลโมเดลและเผยแพร่ผลงานออนไลน์)

## 5. ระเบียบวิธีการทดลอง (Methodology)

### 5.1 การเก็บข้อมูล (Data Collection)

การเก็บข้อมูลภาพถ่ายขวดเพาะเลี้ยงเนื้อเยื่อดำเนินการตามขั้นตอนดังนี้

**5.1.1 การจัดฉากถ่ายภาพมาตรฐาน**

- วางขวดเพาะเลี้ยงเนื้อเยื่อบนพื้นหลังสีขาว/ดำด้าน (matte) เพื่อลดแสงสะท้อน
- ติดตั้งสมาร์ตโฟนบนขาตั้งกล้องในระยะคงที่ 20-30 เซนติเมตรจากขวด โดยให้กล้องอยู่ในแนวระดับเดียวกันกับกึ่งกลางขวด
- จัดแสงจากด้านข้าง (side-lighting) มุมประมาณ 45 องศา หลีกเลี่ยงแสงจากด้านหน้าโดยตรงเพื่อลด glare
- ถ่ายภาพที่ความละเอียด 12-50MP (ขึ้นกับกล้อง) ในรูปแบบ JPEG โดยไม่ใช้แฟลช
- ถ่ายภาพซ้ำ 2-3 ครั้งต่อขวด เพื่อให้มีภาพสำรองในกรณีที่เกิด glare หรือ motion blur

**5.1.2 ข้อมูล metadata ที่บันทึกคู่กับภาพ**

- วันที่ถ่ายภาพ (timestamp)
- วันที่ตัดย้ายครั้งล่าสุด (days_since_last_subculture) — บริบทอายุของต้นในรอบขยายพันธุ์
- ชนิดพืช (species/cultivar)
- จำนวนวันที่อยู่ในรอบขยายพันธุ์ปัจจุบัน
- การประเมินโดยนักวิทยาศาสตร์ (ground truth): ยังไม่พร้อม / พร้อมอนุบาล / ตรวจเอง

**5.1.3 จำนวนตัวอย่างเป้าหมาย**

- อย่างน้อย 100 ขวด กระจายครอบคลุม 3 คลาส (≥ 30 ตัวอย่างต่อคลาส)
- ครอบคลุมพืชอย่างน้อย 2-3 ชนิดหรือสายพันธุ์ ที่มีความแตกต่างทางสัณฐานวิทยา

### 5.2 ขั้นตอนการประมวลผลภาพ (Image Processing Pipeline)

**5.2.1 การรัน SAM3 PCS (facebook/sam3) บน Google Colab**

1. รวบรวมภาพถ่ายขวดจากชุดข้อมูล (ภาพจริงจากห้องปฏิบัติการ ผ่าน `data/raw/`)
2. ตรวจหาขอบเขตขวด (bottle ROI detection) เพื่อใช้เป็นกรอบอ้างอิงของพื้นที่ปกคลุม (coverage_ratio)
3. รัน segmentation ด้วย SAM3 PCS (facebook/sam3, gated — ต้องยืนยันสิทธิ์ผ่าน Hugging Face) บน GPU (Colab T4) แบบ headless batch ด้วยคำสั่ง:
   `python sam3_growth_pipeline.py --data <โฟลเดอร์ภาพ> --out <โฟลเดอร์ผลลัพธ์> [--config config.json]`
4. กำหนดค่า: พรอมป์ข้อความ 5 คำ `["plant", "leaf", "shoot", "stem", "root"]`, score threshold ≥ 0.5, mask threshold ≥ 0.5
5. รับผลลัพธ์เป็น binary mask ต่อพรอมป์ พร้อม confidence score และ bounding box

**5.2.2 การจัดระเบียบผลลัพธ์**

- แยก mask ตาม class ของพรอมป์ (plant/leaf/shoot/stem/root)
- นับใบแบบ merged (รวมชิ้นส่วนที่ติดกันเป็น 1 ใบ) เพื่อลด over-segmentation พร้อม fallback นับจาก plant+shoot เมื่อไม่พบ mask ใบ
- ตรวจพบขวดไม่เจอ (ROI ไม่ชัด) → กันไม่ให้ verdict ผิดโดยส่งไปให้มนุษย์ตรวจ (ดูหัวข้อ 7.4)
- คำนวณ PIXEL_TO_CM จาก config เมื่อมีค่าสอบเทียบ (ตาม CALIBRATION_GUIDE)

**5.2.3 หมายเหตุสำคัญเกี่ยวกับ SAM3 PCS**

Spike test เมื่อวันที่ 5 กรกฎาคม 2569 ทดสอบ SAM3 PCS กับภาพขวดเพาะเลี้ยงเนื้อเยื่อจริงด้วย text prompts "plant" และ "leaf" — ผลยืนยันว่าโมเดลสามารถ segment ตำแหน่งต้นพืชภายในขวดแก้วได้สำเร็จ แม้มี glare และ condensation และแยกแยะต้นพืชจากพื้นหลัง/ขอบขวดได้ ซึ่งพิสูจน์ feasibility ของแนวทาง zero-shot segmentation งานอิสระของ Orvati Nia et al. (2026) เปรียบเทียบ SAM v2.1/SAM3/YOLOv11/YOLOv12/BiRefNet บนภาพพืชมากกว่า 50,000 ภาพ พบว่า SAM3 ให้ความแม่นยำสูงสุดและสม่ำเสมอที่สุดข้ามโครงสร้างพืช โดยใช้โหมด detector-free + พรอมป์ข้อความ "plant" ตรงกับแนวทางของโครงงานนี้

### 5.3 การคำนวณ Feature (Feature Extraction)

เมื่อได้ mask ของพรอมป์ทั้ง 5 คำแล้ว ระบบคำนวณ feature 6 กลุ่ม ดังนี้

**ตารางที่ 1: นิยามของ feature ที่ใช้ในระบบ**

| กลุ่ม | Feature | สูตร/นิยาม | หน่วย |
|---|---|---|---|
| โครงสร้าง | `coverage_ratio` | area(plant∪leaf masks) / area(ROI) | สัดส่วน (0-1) |
| โครงสร้าง | `height_proxy` | bbox_height(plant mask) / ROI_height | สัดส่วน (0-1) |
| โครงสร้าง | `projected_area_px` | พื้นที่ฉายภาพรวมของ mask | พิกเซล |
| อวัยวะ | `leaf_count` | จำนวนใบ (นับแบบ merged กัน over-segmentation; fallback จาก plant+shoot) | จำนวนเต็ม |
| อวัยวะ | `shoot_count`, `stem_count`, `root_count` | จำนวน instance ต่อพรอมป์ (confidence ≥ 0.5) | จำนวนเต็ม |
| ความซับซ้อน | `hull_ratio` | พื้นที่ mask / พื้นที่ convex hull (ความซับซ้อนของรูปร่าง) | สัดส่วน (0-1) |
| สี | `green/yellow/brown_ratio` | สัดส่วนพิกเซลใน ROI แยกตามช่วง HSV | สัดส่วน (0-1) |
| คุณภาพภาพ | `glare_score`, `condensation_score` | สัดส่วนพิกเซล specular/ฝ้าภายใน ROI | สัดส่วน (0-1) |
| การตัดสินใจ | `verdict`, `confidence` | ผลจัดกลุ่ม 3 คลาส + คะแนนความมั่นใจ (ดู 7.4) | — |

**หมายเหตุ:**
- ROI คือพื้นที่ภายในขวด กำหนดโดยการตรวจจับขวดอัตโนมัติ (bottle detection) หรือ crop คงที่จากการจัดฉากถ่ายมาตรฐาน
- `height_proxy` เป็นสัดส่วนสัมพัทธ์ ไม่ใช่ความยาวจริงในหน่วยเซนติเมตร (2D proxy) — เปลี่ยนเป็นหน่วย cm ได้เมื่อตั้งค่า `PIXEL_TO_CM`

### 5.4 ขั้นตอนวิธีตัดสินใจ (Decision Algorithm)

ระบบใช้ rule-based algorithm (ไม่ใช่ machine learning model) สำหรับจัดกลุ่มขวดเป็น 3 คลาส เพื่อให้สามารถตรวจสอบ ปรับแก้ และอธิบายการตัดสินใจได้ (interpretable/explainable)

**ตารางที่ 2: เกณฑ์การจัดกลุ่มความพร้อมอนุบาล (ค่าเริ่มต้น generic — ปรับได้ผ่าน config และต้อง calibrate กับข้อมูลจริง)**

| กลุ่ม | เงื่อนไข |
|---|---|
| **ยังไม่พร้อม** | `height_proxy < 0.275` — ต้นยังไม่โตพอ/ยังไม่พร้อมย้าย |
| **พร้อมอนุบาล** | `height_proxy ≥ 0.275` — ต้นสมบูรณ์/โตพอ/พร้อมย้าย (อัปเดต 2026-08-26: แทน coverage ซึ่งเป็นตัวชี้วัดที่ผิด · validation acc 0.755, sens 0.917) |

**หมายเหตุ:** verdict หลักมี 2 กลุ่มข้างต้น ส่วนภาพที่ประมวลผลไม่ชัด (หาขวด ROI ไม่เจอ / มี glare หรือฝ้ารุนแรง) จะถูกทำเครื่องหมาย **“ตรวจเอง”** เพื่อส่งให้มนุษย์ตรวจแทนการเดาคลาส — เป็นกลไกป้องกันความผิดพลาด (quality guard) **ไม่ใช่**คลาสทางชีววิทยาที่สาม

**⚠️ คำเตือน:** สำหรับความพร้อมอนุบาล ความหนาแน่นสูง (coverage สูง) มิได้แปลว่าดีเสมอไป — ต้นแออัดเสี่ยง hyperhydricity (grill v3, 2026-07-29) — เกณฑ์ต้อง calibrate กับข้อมูลจริงและผู้เชี่ยวชาญในห้องปฏิบัติการก่อนนำไปใช้ ระบบรองรับการตั้งค่าเฉพาะชนิดพืชผ่าน `--config` (SPECIES_THRESHOLDS)

**5.4.1 การคำนวณ confidence score**

```
confidence = base_confidence × (1 - glare_penalty)
```

โดยที่:
- `base_confidence` = 0.85 (ค่าเริ่มต้น หากเข้าเงื่อนไขของคลาสโดยตรง)
- `glare_penalty` = min(glare_score × 2, 0.5) — ลด confidence เมื่อ glare สูง
- ถ้า `coverage_ratio` และ `days_since_last_subculture` ให้ผลตรงกันข้าม (เช่น coverage สูงแต่วันน้อย) ให้ลด base_confidence เหลือ 0.60 ก่อนคูณ glare_penalty

**5.4.2 การปรับแก้โดยผู้ใช้ (Manual Override)**

ทุกรายการที่ระบบประมวลผลจะแสดงผลลัพธ์พร้อม:
- คลาสที่ทำนาย + confidence score
- ภาพที่ overlay mask + bbox
- ปุ่ม "เปลี่ยนคลาส" ให้ผู้ใช้เลือกคลาสด้วยตนเอง
- ช่องบันทึกหมายเหตุ (optional)

### 5.5 การตรวจสอบความถูกต้อง (Validation)

1. **Ground truth annotation:** annotate mask (plant/leaf) บนภาพตัวอย่าง ≥ 30 ขวด โดยมนุษย์ → คำนวณ mIoU/Dice ของ segmentation เทียบกับ ground truth
2. **เปรียบเทียบกับค่าอ้างอิงจากผู้ประเมิน:** นำภาพพร้อม metadata มาทดสอบระบบ คำนวณ confusion matrix, precision, recall, F1-score สำหรับแต่ละคลาสของ verdict
3. **Iterative threshold tuning:** หากผล validation แรกต่ำกว่าเป้าหมาย (accuracy < 70%) ให้ปรับ threshold แล้วทดสอบซ้ำ บันทึกทุกการเปลี่ยนแปลง
4. **Cross-species test:** ทดสอบระบบกับพืชต่างชนิดกันเพื่อดูว่า threshold ชุดเดียวใช้ได้กับทุกชนิดหรือไม่
5. **Inter-rater reliability:** หากเป็นไปได้ ให้เปรียบเทียบการประเมินระหว่างนักวิทยาศาสตร์ 2 คนขึ้นไป เพื่อดู baseline ของมนุษย์เอง

### 5.6 การประเมินเปรียบเทียบกับวิธีพื้นฐาน (Baseline Comparison) และการวิเคราะห์ความไว (Sensitivity Analysis)

**5.6.0 ผลที่ได้เบื้องต้น — ระดับค่าวัด (trait/measurement) [RESULT]: `src/benchmark_traits.py`** — เปรียบเทียบ proxy ของ "ขนาดต้น" ที่แต่ละวิธีได้จาก segmentation กับค่าที่วัดมือ (`height_cm`, `area_cm2`) ด้วย Pearson r (scale-free — proxy เป็น px แต่เทียบกับ cm ได้โดยไม่ต้องสอบเทียบหน่วย):

| วิธี | ความสูง (r เทียบมือ, n=100) | พื้นที่ (r เทียบมือ, n=80) | อัตราล้มเหลว (mask=0) | เวลาเฉลี่ย/ภาพ |
|---|---|---|---|---|
| **SAM3 PCS** | **0.638** | **0.398** | 0.01 | — |
| classical (HSV เขียว) | 0.498 | 0.261 | **0.23** | 0.27 s |
| YOLO-seg (COCO pretrain) | 0.133 | 0.050 | 0.13 | 0.33 s |

> SAM3 ตรงกับค่าวัดมือมากกว่า baseline อย่างชัดเจนด้านความสูง (r=0.638 > classical 0.498 > YOLO-COCO 0.133) และล้มเหลวน้อยกว่า (1% vs 23%/13%) — สอดคล้องกับ Orvati Nia et al. (2026) ที่ SAM3 ดีที่สุดในโหมด detector-free ส่วน YOLO-COCO ไม่มีคลาส "plant" จึงจับทั้งฉากแทนต้น (ต้อง fine-tune เพื่อใช้จริง) ⚠️ ค่านี้คือ "ความสอดคล้องกับมือ" ไม่ใช่ mIoU/Dice ระดับพิกเซล — การทดสอบระดับพิกเซล (Level A) ยังต้องใช้ ground-truth masks [OPEN]

**5.6.1 Baseline segmentation** — รันวิธีพื้นฐาน 3 วิธีบนชุดข้อมูลเดียวกัน และเปรียบเทียบด้วยตัวชี้วัดมาตรฐาน: SAM2 (Ravi et al., 2024), YOLO-seg (เช่น YOLOv8-seg), และการแบ่งส่วนเชิงคลาสสิก (thresholding/color segmentation) รายงาน mIoU, Dice, precision, recall, F1 พร้อมเวลาประมวลผลต่อภาพ — อ้างอิงจากงาน Orvati Nia et al. (2026) ที่ใช้เกณฑ์การเปรียบเทียบลักษณะเดียวกัน [PLAN — ระดับค่าวัดทำแล้ว ดู 7.6.0 / ระดับพิกเซลรอ ground-truth masks]

**5.6.2 Prompt sensitivity** — ทดสอบชุดพรอมป์ทางเลือก (เช่น plant อย่างเดียว, plant+leaf, ครบ 5 คำ, คำพ้อง เช่น "seedling") แล้วรายงานความแปรปรวนของ mIoU และ verdict — อ้างอิงงาน Dubois et al. (2026) ที่พบว่า SAM3 แบบชี้นำด้วยข้อความไวต่อถ้อยคำพรอมป์

**5.6.3 Threshold sensitivity** — ทดสอบค่า ready/overdense ช่วง 0.10–0.90 (step 0.05) แล้วรายงานผลต่อ accuracy ของ verdict และเลือกชุด threshold ที่ให้ MCC สูงสุด

---

## 6. การวิเคราะห์ข้อมูล (Data Analysis)

### 6.1 การวิเคราะห์ความสัมพันธ์ระหว่าง Feature กับความพร้อมอนุบาล

- ใช้ scatter plot และ box plot แสดงการกระจายตัวของแต่ละ feature จำแนกตามกลุ่ม (ยังไม่พร้อม / พร้อมอนุบาล / ตรวจเอง)
- คำนวณ correlation matrix ระหว่าง features เพื่อตรวจสอบ multicollinearity (เช่น coverage_ratio กับ shoot_count, root_ratio กับความพร้อมอนุบาล)
- วิเคราะห์ว่าชุด feature ใดที่มีอำนาจจำแนกสูงสุดโดยใช้ feature importance จาก simple decision tree (ใช้เพื่อการวิเคราะห์เท่านั้น — algorithm จริงเป็น rule-based)
- เปรียบเทียบผลระหว่างพืชต่างชนิดว่า feature thresholds ต้องปรับต่างกันหรือไม่

### 6.2 การประเมินความแม่นยำของระบบ (Classification Metrics)

**การประเมิน segmentation (เปรียบเทียบ baseline):** คำนวณ mIoU, Dice coefficient, precision, recall และ F1 ที่ระดับพิกเซล โดยเทียบ mask ของ SAM3 กับ ground truth ที่ annotate โดยมนุษย์ และเทียบกับ baseline (SAM2, YOLO-seg, การแบ่งส่วนเชิงคลาสสิก) บนชุดภาพเดียวกัน พร้อมบันทึกเวลาประมวลผลต่อภาพเพื่อพิจารณา trade-off ระหว่างความแม่นยำกับต้นทุนการคำนวณ

**การประเมิน verdict (การจัดกลุ่มความพร้อมอนุบาล):**

**ตารางที่ 3: แม่แบบ confusion matrix สำหรับการประเมินผล**

| จริง \ ทำนาย | ยังไม่พร้อม | พร้อมอนุบาล | ตรวจเอง |
|---|---|---|---|
| **ยังไม่พร้อม** | TN_wait | FP_ready | FP_check |
| **พร้อมอนุบาล** | FN_wait (missed) | TP_ready | FP_check |
| **ตรวจเอง** | FN_wait | FN_ready | TP_check |

เมตริกหลักที่ใช้:
- **Accuracy:** สัดส่วนการทำนายถูกต้องทั้งหมด (เป้าหมาย ≥ 70%)
- **Precision (ต่อกลุ่ม):** ความแม่นยำเมื่อระบบบอกว่ากลุ่มนั้น
- **Recall/Sensitivity (ต่อกลุ่ม):** ความสามารถในการตรวจจับกลุ่มนั้น (เป้าหมาย ≥ 0.6 สำหรับกลุ่มพร้อมอนุบาล)
- **F1-score:** ค่าเฉลี่ย harmonic ระหว่าง precision และ recall

### 6.3 การปรับเทียบ Threshold (Threshold Tuning)

ใช้ validation set เพื่อทดสอบค่า threshold ที่แตกต่างกัน:
- coverage_ratio: ทดสอบตั้งแต่ 0.25-0.85 (step 0.05)
- days_since_last_subculture: ทดสอบตั้งแต่ 14-70 (step 7)
- เลือกชุด threshold ที่ให้ Matthews Correlation Coefficient (MCC) สูงสุด (เนื่องจากคลาสไม่สมดุล — expected class imbalance)

---

## 7. แผนการดำเนินงาน (Research Plan)

| กิจกรรม | ก.ย. | ต.ค. | พ.ย. | ธ.ค. |
|---|---|---|---|---|
| ส่งข้อเสนอ YSC 2027 (ภายใน 10 ก.ย.) | █ | | | |
| เก็บข้อมูลภาพถ่ายซ้ำรายรอบ + metadata (time-series) | █ | █ | | |
| สร้าง ground-truth masks (≥30 ภาพ) + วัดมือ | █ | █ | | |
| รัน baseline (SAM2 / YOLO-seg / classical) + mIoU/Dice | | █ | | |
| เทรน U-Net ขนาดเล็ก (กลั่นจาก SAM3) + ทดสอบบนชุด 100 ขวด | | █ | █ | |
| วิเคราะห์ growth curve + threshold sensitivity (MCC สูงสุด) | | | █ | |
| ตรวจข้ามชนิด (cross-species) + inter-rater | | | █ | |
| เขียนรายงานฉบับสมบูรณ์ + เปิดชุดข้อมูล (FAIR) | | | | █ |

**หมายเหตุ:** แผนยืดหยุ่นได้ตามความพร้อมของวัสดุพืชในห้องปฏิบัติการและผลการทดสอบระหว่างทาง — ครอบคลุมการดำเนินงานต่อเนื่องจนจบปี 2569 ตามกรอบเวลาการประกวด

## 8. ประโยชน์และผลที่คาดว่าจะได้รับ (Benefits and Expected Results)

8.1 **เพิ่มประสิทธิภาพห้องปฏิบัติการเพาะเลี้ยงเนื้อเยื่อ:** ลดเวลาที่นักวิทยาศาสตร์ต้องใช้ในการตรวจสอบขวดทีละขวด — ระบบช่วยคัดกรองขวดที่ "พร้อมอนุบาล" ก่อน แล้วให้นักวิทยาศาสตร์ตรวจสอบขวดที่ระบบระบุว่ายังไม่พร้อมหรือต้องตรวจเองเฉพาะในกรณีที่ confidence ต่ำ

8.2 **การติดตามแบบไม่ทำลายตัวอย่าง (Non-destructive monitoring):** ไม่ต้องเปิดขวดหรือสัมผัสพืชเพื่อประเมินสภาพ ซึ่งลดความเสี่ยงการปนเปื้อน (contamination) — สอดคล้องกับแนวทางของ Bethge et al. (2023)

8.3 **เครื่องมือช่วยตัดสินใจ (Decision-support tool) ที่ทำงานข้ามชนิดพืช:** เป็นครั้งแรกที่มีระบบ zero-shot ที่ปรับใช้กับพืชหลายชนิดโดยไม่ต้อง retrain โมเดล ซึ่งแตกต่างจากระบบ CV เฉพาะพืชที่ผ่านมา — ช่วยลดต้นทุนในการพัฒนาโมเดลต่อชนิดพืช

8.4 **การจัดลำดับความสำคัญของงานในห้องปฏิบัติการ:** นักวิทยาศาสตร์สามารถจัดลำดับขวดที่ต้องย้ายออกอนุบาลก่อน-หลังตามความเร่งด่วน (ขวดที่พร้อมอนุบาลและเสี่ยงแออัดควรมาก่อน) ลดความสูญเสียจาก overcrowding

8.5 **การบันทึกประวัติการเจริญเติบโต (Growth history tracking):** เมื่อใช้ระบบอย่างต่อเนื่องหลายรอบขยายพันธุ์ จะได้ข้อมูลอนุกรมเวลา (time-series) ของ coverage_ratio, root_ratio, shoot_count ต่อขวด ซึ่งอาจใช้วิเคราะห์แนวโน้มและคาดการณ์ล่วงหน้าได้

8.6 **ต้นทุนต่ำ ใช้ง่าย:** ใช้เพียงสมาร์ตโฟน Android ที่มีอยู่แล้วในห้องปฏิบัติการส่วนใหญ่ ไม่ต้องซื้อ hardware เพิ่ม (ต่างจากระบบเฉพาะทาง)

8.7 **ชุดข้อมูลเปิด (Open dataset):** ชุดข้อมูลภาพเพาะเลี้ยงเนื้อเยื่อผ่านขวดแก้วพร้อม metadata และการกำกับภาพ จะจัดทำตามหลัก FAIR (Findable, Accessible, Interoperable, Reusable) เพื่อเปิดให้นักวิจัยอื่นใช้ต่อ — เป็นทรัพยากรใหม่สำหรับงาน phenotyping ในสภาพเพาะเลี้ยงเนื้อเยื่อที่ยังขาดแคลน

### 8.8 เส้นทางต่อยอด (Future Work) (Future Work) [PLAN]

ผลนำร่องชุด 100 ขวดนี้พิสูจน์ความเป็นไปได้ของแนวทางแล้ว จึงเป็นฐานสู่การต่อยอดใน 4 ทิศทาง (เรียงตามความพร้อมข้อมูล):

**1) จาก "จัดกลุ่ม" → "ทำนายการเจริญ" (time-series prediction)** — ข้อมูลนำร่องเป็นชุดถ่าย 3 วัน (16 ก.ค. / 2 ส.ค. / 14 ส.ค.) จึงเป็นชุดเวลา (time-series) ของการเจริญต่อขวด ต่อยอดสร้าง **growth curve** (coverage/height/leaf ต่อเวลา) + ทำนาย**อัตราการเจริญ**และ**เวลาที่ต้นจะพร้อมอนุบาล** เปลี่ยนจากระบบที่ตอบ "พร้อมหรือไม่" เป็นระบบที่**ตอบ "จะพร้อมเมื่อไร"** — ยกระดับจาก classifier เป็น predictor (ต่อยอดสู่ greenhouse/plant factory)

**2) ข้ามชนิด (multi-species zero-shot)** — เพราะใช้ SAM3 แบบไม่ต้อง retrain (พรอมป์ "plant" ข้ามชนิด — Orvati Nia et al., 2026) จึงต่อยอดทดสอบกับพืช 2–3 ชนิด (เช่น กล้วยไม้, กล้วย) เพื่อพิสูจน์ generalization สู่การใช้งานจริงในแล็บที่มีหลายชนิด

**3) ชุดข้อมูลเปิด (FAIR) + baseline ครบ** — เปิด dataset (ภาพ + metadata + ground truth) ตามหลัก FAIR และรันการเปรียบเทียบกับวิธีพื้นฐาน (SAM2 / YOLO-seg / classical) ครบถ้วน (mIoU/Dice/F1) เพื่อให้ผลชัดและใช้ต่อได้ในวงกว้าง

**4) สู่แอปมือถือ (deployment)** — มี component Android ในโปรเจกต์ (`src/android/`) ต่อยอดเป็นแอป "ถ่ายภาพ → verdict ภายในไม่กี่วินาที" สำหรับแล็บจริง ลดแรงงานตรวจด้วยตา ~60–70% ของต้นทุน (Bethge et al., 2023)

> หมายเหตุ: ทิศทางทั้ง 4 เป็นแผนต่อยอด (งานระยะถัดไป) — ผลนำร่องตอนนี้คือการยืนยันความเป็นไปได้ในขั้นแรก [PLAN]

---

## 9. การเปิดเผยข้อมูลเกี่ยวกับ Generative AI และเทคโนโลยีปัญญาประดิษฐ์ที่ช่วยในกระบวนการจัดทำข้อเสนอ (Disclosure of Generative AI and AI-Assisted Technologies in the Writing Process)

โครงงานนี้ใช้เครื่องมือ Generative AI (Gen-AI) ในหลายขั้นตอนของกระบวนการพัฒนาและเขียนข้อเสนอโครงงาน โดยมีการเปิดเผยรายละเอียดดังนี้

### 9.1 เครื่องมือที่ใช้

| เครื่องมือ | ผู้พัฒนา | เวอร์ชัน/วันที่ | การใช้งาน |
|---|---|---|---|
| Claude Opus 4.8 | Anthropic | กรกฎาคม 2569 | การสังเคราะห์วรรณกรรม การเขียนข้อเสนอโครงงาน การออกแบบ pipeline |
| DeepSeek V4 | 深度求索 (DeepSeek) | กรกฎาคม 2569 | การช่วยเขียนและตรวจทานเนื้อหาทางเทคนิค |
| Roboflow AI | Roboflow Inc. | กรกฎาคม 2569 | การติดต่อและประมวลผล SAM3 PCS API |
| Consensus (AI Research Search) | Consensus Inc. | กรกฎาคม 2569 | การค้นหาและตรวจสอบวรรณกรรมทางวิทยาศาสตร์ |
| PubMed MCP | NCBI/NLM | กรกฎาคม 2569 | การเข้าถึงเนื้อหาเต็มของบทความวิจัย |

### 9.2 ขอบเขตการใช้งาน

1. **การสังเคราะห์วรรณกรรมและการตรวจสอบการอ้างอิง (Literature Synthesis & Citation Verification):** ใช้ Consensus AI และ PubMed MCP ในการค้นหา ตรวจสอบ และยืนยันความถูกต้องของบทความวิจัยที่อ้างอิงในข้อเสนอโครงงานนี้ ทุกการอ้างอิงที่ปรากฏในบรรณานุกรมผ่านการตรวจสอบยืนยันจากฐานข้อมูลจริง (Consensus หรือ PubMed) ว่าเป็นบทความที่มีอยู่จริง มี DOI/URL ที่เข้าถึงได้ และเนื้อหาที่อ้างอิงตรงกับต้นฉบับ — **ไม่มีรายการอ้างอิงใดที่มาจากการสร้างข้อมูลเทียมของ AI (AI hallucination)**

2. **การเขียนข้อเสนอโครงงาน (Proposal Writing Assistance):** ใช้ Claude Opus 4.8 เป็นผู้ช่วยในการเรียบเรียงเนื้อหาส่วนต่าง ๆ ของข้อเสนอ โดยเฉพาะการจัดโครงสร้างแบบพีระมิด (pyramid structure) ในบทนำ การออกแบบวิธีการดำเนินการ และการเรียบเรียงภาษาไทยทางวิชาการ — เนื้อหาทั้งหมดได้รับการตรวจทานและปรับแก้โดยผู้พัฒนาโครงงานก่อนนำไปใช้

3. **การสร้างโค้ด (Code Generation):** ใช้ Claude Opus 4.8 ในการช่วยเขียนโค้ดต้นแบบสำหรับ Android application, การเชื่อมต่อ Roboflow SAM3 PCS API, และการคำนวณ feature extraction — โค้ดทุกส่วนผ่านการตรวจสอบและทดสอบโดยผู้พัฒนา

4. **การสร้าง Diagram (Diagram Generation):** ใช้ไวยากรณ์ **Mermaid** (สำหรับแผนภาพสถาปัตยกรรม/การออกแบบใน `docs/diagrams.md`) และ **matplotlib (Python)** (สำหรับภาพสถาปัตยกรรมในข้อเสนอ) ในการสร้างแผนภาพ — **ผู้พัฒนาเป็นผู้เขียนและตรวจทานโครงสร้าง เนื้อหา และภาษาอังกฤษของแผนภาพเอง** โดยใช้ Claude ช่วยเฉพาะการเขียนโค้ด/โครงสร้าง (ครอบคลุมในข้อ 12.2.3 แล้ว) — **ไม่ได้ใช้เครื่องมือสร้างภาพด้วย Gen-AI (image-generation) สำหรับแผนภาพ**

### 9.3 ข้อจำกัดและการตรวจสอบโดยมนุษย์

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

## 10. บรรณานุกรม (Bibliography)

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

Orvati Nia, F., Peeples, J., Murray, S. C., McFarland, A., Vann, T., Salehi, S., Hardin, R., Baltensperger, D. D., Ibrahim, A. M. H., Thomasson, J. A., Fadamiro, H., Subramanian, N. K., Pillai, S. D., Roston, R., Ishimwe, J., Basak, D., Oladepo, N., & Vysyaraju, U. (2026). *A data-driven image extraction and analysis pipeline for plant phenotyping in controlled environments* (preprint). bioRxiv. https://doi.org/10.64898/2026.02.25.707797

Abbey, A., & Meroz, Y. (2026). *Segment any plant (SAP): Foundation-model segmentation for plant time-series phenotyping* (preprint). bioRxiv. https://doi.org/10.64898/2026.03.11.711099

Dubois, R., Bousset, L., Jumel, S., Leclerc, M., Parisey, N., & Joly, A. (2026). *Text guidance is powerful but prompt-sensitive for weakly-supervised leaf symptom segmentation* (preprint). bioRxiv. https://doi.org/10.64898/2026.07.10.737680

---

*ข้อเสนอโครงงานนี้ (ส่วนที่ 1) จัดทำเพื่อส่งประกวด YSC 2027 สาขา CSAI (AI/ML) — เนื้อหาเป็นของผู้พัฒนาโครงงาน โดยผลนำร่อง 100 ขวดระบุเป็น [RESULT] (รันจริงบน Colab 2026-08-26) ส่วนการประเมิน baseline / ground truth ยังเป็น [PLAN]*

---
