# R4-B — Color Reference Target ในเฟรม (VitroVision)

> สำหรับ: green_coverage_pct ของพริก TC ถ่ายผ่านขวดแก้ว, Samsung S24 FE, ~18cm, WB lock ~4000K, **ไม่มี lightbox**, มี white card ในเฟรมแล้ว, ถ่าย 17:00 × 28 วัน
> คำถาม R4-B: ควรวาง color reference อะไร / กี่ patch / ตรงไหน เพื่อให้สีเขียวแม่นและเทียบข้ามวันได้

---

## VERDICT (สั้น)

**ใช้ DIY color patch แบบ 6 ช่อง: White + Mid-gray + Red + Green + Blue (+ Black)** วางในเฟรมทุกภาพ แล้วทำ **per-image color correction** (3×3 matrix หรือ root-polynomial regression) จากค่าที่อ่านจาก patch ในภาพนั้น ๆ

- **white card อย่างเดียวไม่พอ** — ยืนยัน finding R3: neutral patch (white/gray) ล้วน ๆ ให้ผล correction "แย่" สำหรับงานที่อิงสีจริง [1]
- **ไม่ต้องใช้ ColorChecker 24 ช่องเต็ม** — R/G/B primaries ให้ผลเทียบเท่า 24 patch ในงาน plant phenotyping [1]
- **อย่าพิมพ์ DIY เองแบบมั่ว ๆ** — printed replica มี error สูง (CIEDE2000 เฉลี่ย 4.28, match สีที่ตั้งใจแค่ 4%) ถ้าทำ DIY ต้อง **วัดค่าจริงของ patch ที่พิมพ์ด้วย spectrophotometer/อ้างอิงที่เชื่อถือได้ แล้วใช้ค่าที่วัดจริงเป็น reference** ไม่ใช่ค่าที่ตั้งใจจะพิมพ์ [2]
- **target ในเฟรม = ทางออกของการ "ไม่มี lightbox"** — มันทำหน้าที่เป็น ground-truth ในทุกภาพ จึงชดเชยแสงที่แปรปรวนข้ามวันได้ ทั้งที่แสงไม่คุม[3][4]

---

## ตารางเทียบ reference target แต่ละแบบ

| Target | ความแม่น (สีจริง/เขียว) | ต้นทุน | เหมาะกับเราไหม | อ้างอิง |
|---|---|---|---|---|
| **White card อย่างเดียว** (มีอยู่แล้ว) | แก้ WB ได้ แต่ correction สีจริงแย่ (CPI 0.26–1.0 = แย่สุด) | ฟรี | ❌ ไม่พอสำหรับ green endpoint | Sunoj 2018 [1] |
| **18% Gray card** | ใกล้เคียง white card; แก้ exposure/WB ได้ แต่ไม่ครอบ chroma | ~$10–20 | ⚠️ ดีกว่า white นิด แต่ neutral-only ยังแย่ | Sunoj 2018 [1]; Minaker 2021 [5] |
| **DIY RGB patch (4–6 ช่อง)** | เทียบเท่า 24-patch (CPI 0.21–0.24) ถ้าค่า reference ถูกต้อง | ~$0–5 (พิมพ์/ตัดเอง) | ✅ **แนะนำ** — คุ้มสุด ครอบ chroma + เขียว | Sunoj 2018 [1] |
| **ColorChecker 24-patch (X-Rite/Macbeth)** | มาตรฐานทอง, ใช้ใน field trial ข้ามวัน 4 เดือน, ใช้ทำ ΔE benchmark | ~$50–90+ | ⚠️ ดีแต่ overkill + แพงสำหรับงบนี้ | Chopin 2018 [3]; Damschen 2025 [6]; Mojaravscki 2024 [7] |
| **Reference color "board/stripe" + AR** | ลด color variance ได้ถึง ~90% ข้ามแสง | ปานกลาง (ต้องเขียน app) | ⚠️ ดีมากแต่ implement หนัก | Zhang 2023 [4] |

---

## ตอบทีละข้อ

### 1) White card vs Gray vs ColorChecker vs DIY RGB — อะไรเหมาะกับ plant phenotyping งบน้อย
- Sunoj 2018 ทดสอบบนภาพพืช lab+field ด้วย ColorChecker จริง: **neutral patch ล้วน (white, gray) ให้ correction แย่ที่สุด** (CPI 0.26–1.0), ส่วน **R+G+B patches ให้ผลเทียบเท่า 24 patch** (CPI 0.21–0.24) และ "simple and practical" [1]
- แปลว่า white card ที่เรามีอยู่ + gray card **ไม่พอ** เพราะ endpoint เราอิง **สีเขียวจริง** ไม่ใช่แค่ความสว่าง → ต้องมี chromatic patch (โดยเฉพาะเขียว)
- ColorChecker เต็ม = มาตรฐานที่ดี (Chopin ใช้ในแปลง 4 เดือน [3]) แต่สำหรับงบน้อย **เกินจำเป็น** เพราะ RGB primaries ก็พอ

### 2) จำนวน patch ขั้นต่ำ
- **4–6 patch พอ** ไม่ต้อง 24: white + gray + R + G + B (+black เพื่อ anchor จุดดำ/ช่วย polynomial) [1]
- หลักการ fitting: **3×3 linear matrix** (exposure-invariant, Finlayson 2015) หรือ **root-polynomial regression** ซึ่งแม่นกว่า linear และยัง exposure-invariant (ดีกว่า neural net ด้วยซ้ำในงานข้าม dataset) [8]
- **สำคัญต่อ endpoint เรา:** เลือก green patch ให้ **คร่อมช่วง hue เขียวของใบพริกจริง** ไม่ใช่เขียว primary สด ๆ อย่างเดียว — green channel accuracy คือ primary endpoint จึงควร anchor ตรงโซนสีที่เราจะวัดจริง

### 3) ตำแหน่งวาง / ขนาด / glare (หลักฐาน **บางส่วนเป็นการอนุมาน** — ระบุชัด)
- **ตำแหน่ง/กำลังขยาย/แสงรอบข้าง ไม่ได้กระทบ white balance อย่างมีนัยสำคัญ** — Minaker 2021 ทดสอบแล้วไม่ต่าง [5] → วางตรงไหนก็ได้ ขอให้ **อยู่ในเฟรมทุกภาพ** และโดนแสงชุดเดียวกับต้นพริก
- **อย่าโฟกัสคมที่ card เกินไป** — Minaker พบว่า card ที่ "crisp focus" กลับทำ color accuracy แย่ลง (ΔE 15.78) [5] → target เบลอเล็กน้อยยอมรับได้/ดีกว่า (ลด noise/texture ต่อ patch)
- **ถ่ายเอียงเล็กน้อยเพื่อเลี่ยง specular/non-Lambertian reflectance** — Zhang 2023 แนะนำมุมถ่ายที่ลดแสงสะท้อนเงาวับ [4] → วาง patch ให้ **ไม่ตั้งฉากตรง ๆ กับแหล่งแสง/ไม่สะท้อนเข้ากล้อง**, เลี่ยงเงาขอบขวด
- **ขนาด:** ให้แต่ละ patch กินพื้นที่พอให้สุ่ม pixel เฉลี่ยได้นิ่ง (กะ ≥ หลายสิบ px ต่อด้าน) — ข้อนี้เป็น best-practice อนุมาน ไม่มี paper ระบุตัวเลขตรง ๆ
- วางในระนาบเดียวกับขวด ที่ระยะ ~18cm เดิม เพื่อให้แสงตกใกล้เคียงต้นพริก

### 4) target ในเฟรมลด error / เพิ่ม cross-day consistency ได้จริงแค่ไหน (ตัวเลข)
- **Chopin 2018** (มาตรฐานทอง ของข้อนี้): ใส่ ColorChecker ทุกภาพในแปลงทดลอง **4 เดือน**, fit quadratic least-squares → **ลด error ระหว่างค่าที่วัดกับ reference ในทุกภาพ** และที่สำคัญ **std ของ mean canopy color ข้ามหลายวันลดลงอย่างมีนัยสำคัญ** หลัง color correction [3] — ตรงกับ goal cross-day ของเราเป๊ะ
- **Zhang 2023:** reference board + correction algorithm **ลด color variance ได้ถึง ~90%** ข้ามสภาพแสงต่างกัน [4]
- **Li 2025 (soil, smartphone หลายรุ่น/หลายแสง):** color plate calibration **ลด variation ของค่าสีข้ามมือถือ/ข้ามแสงได้สม่ำเสมอ** เพิ่ม precision [9]
- **Damschen 2025:** ใช้ Macbeth ColorChecker หา ΔE → เสนอ threshold **ΔE ≤ 3 ให้ผล detection กระทบ < 1%** [6] → ใช้เป็นเกณฑ์ตรวจคุณภาพ correction ของเราได้ (target: ΔE หลังแก้ ≤ 3)
- **Mojaravscki 2024 (olive, มือถือ, แสงธรรมชาติ):** color correction ทุกวิธีช่วยเพิ่ม detection เทียบกับภาพดิบ [7]

### 5) DIY แทน X-Rite ได้ไหม / พิมพ์เองเชื่อถือแค่ไหน
- **ได้ แต่มีเงื่อนไขสำคัญ:** Cugmas 2025 พิมพ์ CCT replica เอง (spot color RAL เดียวกับต้นฉบับ) แล้ววัดด้วย spectrophotometer พบ **CIEDE2000 เฉลี่ย 4.28, สูงสุด 9.46**, และ replica **match สีที่ตั้งใจไว้แค่ 4%** (ต้นฉบับ match 54%) → error สีระดับนี้ทำให้การวัดคลาดเคลื่อนอย่างมีนัยสำคัญ [2]
- **บทเรียน:** อย่าใช้ "ค่าสีที่ตั้งใจจะพิมพ์" เป็น reference เด็ดขาด → ต้อง **วัดค่าจริงของ patch ที่พิมพ์ออกมา** (spectrophotometer เช่น Nix / หรือยืม ColorChecker จริงมา calibrate DIY ครั้งเดียว) แล้วใช้ค่าที่วัดได้นั้นเป็น reference value ในสมการ correction
- ทางเลือก DIY ที่ปฏิบัติได้: ใช้กระดาษสี/แผ่นพลาสติกสีที่ matte (กันสะท้อน), เคลือบ/laminate ด้าน, แล้ว **ทำ one-time characterization** ด้วยอุปกรณ์อ้างอิง 1 ครั้ง — Wright 2023 มี Python script ฟรีทำ color correction จาก ColourChecker chart (โค้ดดัดแปลงใช้ DIY chart ได้) แต่ method เดิมเขาใช้ **lightbox** ซึ่งเราไม่มี — เราใช้ in-frame target แทน lightbox [10]

---

## คำแนะนำ FINAL

1. **Target:** DIY color patch **6 ช่อง** = White, Mid-gray (~18%), Red, **Green (คร่อม hue ใบพริกจริง)**, Blue, Black
2. **จำนวน:** 6 patch (ขั้นต่ำใช้ได้ 4–5; 6 เผื่อ anchor ดำ + เขียวเฉพาะทาง) — **ไม่ต้อง 24** [1]
3. **ตำแหน่ง:** ในเฟรม **ทุกภาพ**, ระนาบเดียว/ระยะใกล้เคียงขวด (~18cm), โดนแสงชุดเดียวกับต้นพริก, **เอียงเล็กน้อยเลี่ยงแสงสะท้อน**, เลี่ยงเงาขอบขวด, **อย่าโฟกัสคมจัดที่ card** [5][4]
4. **วิธีแก้สี:** derive **per-image** correction (3×3 linear หรือ root-polynomial) จาก patch ในภาพนั้น ๆ — นี่คือเหตุผลที่ in-frame ชนะ calibration shot ครั้งเดียว [3][8]
5. **เกณฑ์คุณภาพ:** ตั้งเป้า **ΔE ≤ 3** หลัง correction (อิง Damschen) [6]; รายงาน std ของ green metric ก่อน/หลังแก้ เป็นหลักฐาน cross-day (อิง Chopin) [3]
6. **DIY ต้อง characterize ค่าจริง** ของ patch ที่พิมพ์ 1 ครั้ง อย่าเชื่อค่าที่ตั้งใจพิมพ์ [2]

### ⚠️ ข้อจำกัดเฉพาะงานเรา (ไม่มีใน paper — ต้อง defend เองที่ YSC)
- **ถ่ายผ่านแก้ว:** target อยู่นอกขวด → matrix แก้ camera+แสง แต่ **ไม่แก้ผลของแก้วต่อ light path ของต้นพริก** อย่างไรก็ดี tint/refraction ของแก้วชุดเดิม ~คงที่ทุกวัน = systematic offset ไม่ใช่ตัวแปรข้ามวัน ดังนั้น in-frame target **ยังให้ cross-day consistency ได้ตามเป้า**
- **หยดน้ำ/ฝ้า (condensation) ในขวด** คือ confound ข้ามวันตัวจริง — แปรตามอุณหภูมิ/เวลา ทำให้แสงกระเจิงและสีเขียวเพี้ยนได้ **color target แก้ไม่ได้** ต้องคุมด้วยวิธีอื่น (เวลา/อุณหภูมิถ่าย, เช็ดฝ้า, หรือ flag ภาพที่มีฝ้า)

---

## References (จาก Consensus จริง — มี URL)

[1] [Color calibration of digital images for agriculture and other applications](https://consensus.app/papers/details/379b4ba741f155fb973ab1cb976e1664/?utm_source=claude_code) (S. Sunoj et al., 2018, ISPRS J. Photogrammetry & Remote Sensing, 74 citations)
[2] [Effect of color calibration in a smartphone mHealth app for skin erythema monitoring](https://consensus.app/papers/details/ef5a48779c455917ad66c0f24d534eab/?utm_source=claude_code) (B. Cugmas et al., 2025)
[3] [Land-based crop phenotyping by image analysis: consistent canopy characterization from inconsistent field illumination](https://consensus.app/papers/details/2125c6b5d648596a96ea9c4152c7da31/?utm_source=claude_code) (J. Chopin et al., 2018, Plant Methods, 23 citations)
[4] [A novel systems solution for accurate colorimetric measurement through smartphone-based augmented reality](https://consensus.app/papers/details/0fa57cd0904656eeb5abdeff7c9bb528/?utm_source=claude_code) (G. Zhang et al., 2023, PLOS ONE, 9 citations)
[5] [Optimizing Color Performance of the Ngenuity 3-Dimensional Visualization System](https://consensus.app/papers/details/f7c23949c9e15d94904c5f1892d5f9a1/?utm_source=claude_code) (S.A. Minaker et al., 2021, Ophthalmology Science, 36 citations)
[6] [SAFE-COLOR: Color Fidelity Benchmarks and Thresholds for Safety-Critical Object Detection](https://consensus.app/papers/details/55471acb7a9c51a48a640bda666091ac/?utm_source=claude_code) (M. Damschen et al., 2025, IEEE IV)
[7] [Comparative Evaluation of Color Correction as Image Preprocessing for Olive Identification under Natural Light Using Cell Phones](https://consensus.app/papers/details/f020c8e52d24523bb168c8950d2c4887/?utm_source=claude_code) (D. Mojaravscki et al., 2024, AgriEngineering, 9 citations)
[8] [Color Correction Using Root-Polynomial Regression](https://consensus.app/papers/details/68ccd54f5af15d4bac1ca705350bfbca/?utm_source=claude_code) (G. Finlayson et al., 2015, IEEE Trans. Image Processing, 196 citations)
[9] [Using a Reference Color Plate to Correct Smartphone-Derived Soil Color Measurements with Different Smartphones Under Different Lighting Conditions](https://consensus.app/papers/details/9826b122e23c545f8589ae5164e15a1e/?utm_source=claude_code) (S. Li et al., 2025, Soil Systems)
[10] [Free and open-source software for object detection, size, and colour determination for use in plant phenotyping](https://consensus.app/papers/details/f274a1aa301e5e219957706e65ed12d3/?utm_source=claude_code) (H.C. Wright et al., 2023, Plant Methods, 7 citations)

---
*Create or connect a free Consensus account to return more than 3 results per search in Claude Code: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
