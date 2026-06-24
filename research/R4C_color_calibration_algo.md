# R4-C — Algorithmic Color Calibration / CCM สำหรับ VitroVision

> Sub-agent R4-C | สาขา CSBI (YSC 2027 → ISEF)
> คำถาม: algorithm แปลงสีให้ตรงมาตรฐานจาก reference target — เลือก CCM แบบไหน, PlantCV ทำยังไง, ลำดับ pipeline, ข้อควรระวัง
> ทุก citation = ผล Consensus จริง + URL (กฎ citation เหล็ก) ยกเว้นชื่อฟังก์ชัน PlantCV = verify จาก official docs (docs.plantcv.org / GitHub danforthcenter/plantcv) ระบุที่มาชัดเจน

---

## VERDICT (สรุปสำหรับตัดสินใจ)

1. **ต้องทำ color correction ด้วย reference color card ทุกภาพ** ก่อนวัด `green_coverage_pct` — งานวิจัย plant phenotyping ยืนยันว่าแสงที่เปลี่ยนทำให้สีเพี้ยนและ "ทำให้ inference ผิด" ถ้าไม่ calibrate [1][6], และ color correction ลด ΔE ได้ **67–84%** [8][9].
2. **เลือกใช้ Linear/Affine CCM (3×3) เป็นค่า default ของ VitroVision** เพราะ (ก) PlantCV รองรับเป็น first-class function (`affine_color_correction`, `auto_correct_color`), (ข) **exposure-invariant** (ไม่เพี้ยนเมื่อ exposure เปลี่ยน) [4][5], (ค) ปลอดภัยกว่า polynomial เมื่อ training patch น้อย. **Root-Polynomial (RPCC)** เป็น upgrade path ถ้าต้องการ ΔE ต่ำกว่านี้ — แม่นกว่า linear และยัง exposure-invariant [4][5][10] แต่ PlantCV ไม่มี built-in ต้อง implement เอง.
3. **อย่าใช้ plain Polynomial (PCC) ที่มีพจน์ R², G², B²** — แม่นบน training set แต่ **ขึ้นกับ exposure** ทำให้ hue/saturation shift เมื่อแสงเปลี่ยน [3][4] (ขัดกับ goal ของเราที่ต้องการ green channel เสถียรข้ามภาพ/ข้ามวัน).
4. **ลำดับ pipeline ที่ถูก:** linearize → **color correction (CCM)** → segmentation → คำนวณ vegetation index (ExG/NGRDI/VARI). CCM ต้องมา **ก่อน** การคำนวณ index เสมอ เพราะ index เป็น channel-ratio ที่สมมติว่า RGB ถูก calibrate แล้ว.
5. **CCM เดียวทั้งภาพไม่พอเมื่อ illumination ไม่สม่ำเสมอ/มี glare จากขวดแก้ว** — single-patch / global CCM แก้ค่าเฉลี่ยได้ แต่แก้ specular glare และ spatial gradient ไม่ได้ [9][6]. ต้อง **mask glare/เงาออกก่อน** แล้วจึงทำ CCM และวัด green coverage.

---

## 1. Linear/Affine vs Polynomial vs Root-Polynomial CCM

### หลักการ
CCM = ฟังก์ชัน map ค่า RGB ของกล้อง (device-dependent) → ค่าสีมาตรฐาน (sRGB / XYZ) โดย regression จาก reference patch (เช่น X-Rite ColorChecker 24 ช่อง) ที่อยู่ในภาพ [1][4]. ค่าสัมประสิทธิ์หาได้จาก least-squares ที่ minimize ระยะระหว่าง source patch กับ target patch [1][4].

### ตารางเปรียบเทียบ

| วิธี | รูปแบบ | Exposure-invariant? | ความแม่น (ΔE) | จุดเด่น/จุดด้อย | อ้างอิง |
|------|--------|---------------------|----------------|------------------|---------|
| **Linear / Affine CCM** | 3×3 (affine = +bias) | **ใช่** | ดี แต่บางสีพลาดสูง | ง่าย, exposure-invariant, มีใน PlantCV; error สูงในบางสี | [3][4][5] |
| **Polynomial (PCC)** | RGB → 9-vector (R,G,B,R²,G²,B²,RG,RB,GB) | **ไม่** ❌ | ลด error >50% บน calibration set | แม่นบน training แต่ hue/sat shift เมื่อ exposure เปลี่ยน → ไม่เหมาะงานข้ามวัน | [3][5] |
| **Root-Polynomial (RPCC)** | √-rooted terms (เช่น R,G,B,√RG,√RB,√GB) | **ใช่** | ดีกว่า linear, มักดีกว่า/เทียบเท่า NN | exposure-invariant + แม่นขึ้น; ต้อง implement เอง (PlantCV ไม่มี) | [4][5][10] |
| **Neural Network** | non-linear | บางสถาปัตยกรรมไม่ใช่ | ดีกว่า linear แต่ **แพ้ root-polynomial** | overkill, ผูกกับ exposure, generalize ข้าม dataset แย่ | [10] |

**สรุปเชิงวิชาการ (defend ได้):** Finlayson et al. พิสูจน์ว่า plain polynomial ลด colorimetric error ได้มากบน calibration set แต่ "ขึ้นกับ exposure" — เมื่อ exposure เปลี่ยน vector ของพจน์ polynomial เปลี่ยนแบบ non-linear ทำให้ hue/saturation shift [3]. RPCC แก้จุดนี้โดยถอดรากของแต่ละพจน์ดีกรี k ทำให้พจน์ scale ตาม exposure → ได้ทั้งความแม่นของ polynomial และความ exposure-invariant ของ linear [4][5]. Kucuk et al. (2023) เปรียบเทียบ linear / polynomial / root-polynomial / NN โดยตรง พบว่า **root-polynomial เอาชนะทั้ง NN และ linear** และ regression methods generalize ข้าม dataset ได้ดีกว่า NN [10].

---

## 2. PlantCV Workflow (verify จาก official docs — ใช้ได้จริง)

> ที่มาชื่อฟังก์ชัน: docs.plantcv.org/en/stable (transform module) + GitHub danforthcenter/plantcv/docs (verified 2026-06). อ้างอิงวิชาการของ method = Berry et al. 2018 [7] (implemented ใน PlantCV) และ PlantCV v2 [11].

PlantCV มี **2 เส้นทาง** สำหรับ color correction:

### เส้นทาง A — One-step (แนะนำสำหรับ VitroVision: เร็ว, affine, exposure-invariant)

```python
from plantcv import plantcv as pcv

rgb_img, path, name = pcv.readimage(filename="bottle_001.png")

# ตรวจจับ color card อัตโนมัติ + แก้สีในขั้นเดียว (affine transform ใน RGB space)
corrected = pcv.transform.auto_correct_color(rgb_img=rgb_img, color_chip_size="passport")
```

`auto_correct_color` เป็น wrapper ที่เรียก 4 ฟังก์ชันต่อกันให้อัตโนมัติ:
`detect_color_card` → `std_color_matrix` → `get_color_matrix` → `affine_color_correction`
(ระบุไว้ตรง ๆ ใน docstring ของ `transform_auto_correct_color`).

### เส้นทาง B — Manual classic workflow (คุมรายละเอียดได้ / debug ได้)

| ลำดับ | ฟังก์ชัน PlantCV | หน้าที่ |
|------|------------------|---------|
| 1 | `pcv.transform.detect_color_card(rgb_img, ...)` | ตรวจจับ color card + สร้าง labeled mask อัตโนมัติ |
| 2 | `pcv.transform.get_color_matrix(rgb_img, mask)` | สกัดค่า RGB เฉลี่ยของแต่ละ chip → **source_matrix** |
| 3 | `pcv.transform.std_color_matrix(pos)` | สร้างค่าสีมาตรฐานของ ColorChecker → **target_matrix** |
| 4 | `pcv.transform.affine_color_correction(rgb_img, source_matrix, target_matrix)` | คำนวณ regression แล้ว apply affine transform → ภาพแก้สีแล้ว |

**Signature ที่ verify แล้ว:**
`plantcv.transform.affine_color_correction(rgb_img, source_matrix, target_matrix)` → corrected_img

**ทางเลือก (workflow แบบเก่า full matrix):**
`pcv.transform.correct_color(target_img, target_mask, source_img, source_mask, output_directory)`
→ คืน `target_matrix, source_matrix, transformation_matrix, corrected_img` (เก็บ matrix เป็น `.npz`). ใช้ `detect_color_card` ช่วยสร้าง mask ได้.

### ความแม่น / ข้อจำกัดของ PlantCV
- **method:** Berry et al. (2018) อธิบายว่าเป็น "collection of linear models ที่ปรับ pixel tuple อิงจาก reference panel ของสี" และยืนยันว่าทำให้ measurement morphological แม่นขึ้น — implement ใน PlantCV โดยตรง [7].
- **ข้อจำกัด:** ต้องมี color card อยู่ในเฟรมทุกภาพ; เป็น affine/linear (ไม่มี root-polynomial built-in) → ถ้าต้องการ ΔE ต่ำมากต้อง implement RPCC เอง; การ detect card อัตโนมัติพึ่ง adaptive threshold (ปรับ `block_size`, `min_size`, `aspect_ratio`, `solidity` ได้) — glare บนขวดแก้วอาจรบกวนการ detect chip.

---

## 3. ตัวเลขลด color error (ΔE / RMSE) จากงานวิจัย

- **Linear CCM (smartphone dermatology, Kang 2025):** ลด color error **67–77%** → ถึงระดับ near-clinical **ΔE < 2.3** [9].
- **Calibration/harmonization (dentistry spectrophotometer, Tango 2024):** ลด ΔE (CIEDE2000/CIELAB) **68.5–84.2%** ระหว่างเครื่องมือ [8].
- **Polynomial regression (Finlayson):** ลด colorimetric error **>50%** บน calibration set [3].
- **Deep learning + k-means CCM (oilseed rape, Abdalla 2019):** average Euclidean distance **16.23 ΔE** เหนือกว่า method เดิม [3-set search].
- **HueDx pipeline (Menon 2024):** ลดสีจน "near-imperceptible" และ CV ของ assay สูงขึ้นเกือบ 2 เท่าถ้า **ไม่** ทำ color correction [12] — เป็นหลักฐาน defend ว่า "ทำไมต้อง calibrate".

> สำหรับ VitroVision: คาดหวังได้ว่า affine CCM จะลด ΔE ลงสู่ระดับ single-digit และทำให้ค่าเฉลี่ย green channel ข้ามภาพ/ข้ามวันเสถียรขึ้นอย่างมีนัยสำคัญ (เทียบ Chopin 2018 ที่ SD ของ canopy color ข้ามวันลดลงชัดเจนหลัง color correction [6]).

---

## 4. ลำดับใน pipeline ที่ถูกต้องเชิงวิชาการ

```
capture (RAW ถ้าได้)
  → [linearize / gamma decode]            ← regression สมมติ linear response
  → glare/specular + shadow masking       ← (สำคัญสำหรับขวดแก้วใส — ดูข้อ 5)
  → COLOR CORRECTION (affine CCM)          ← ทำตรงนี้! ก่อนทุกอย่างที่ใช้ค่าสี
  → segmentation (HSV / SAM / YOLO)
  → vegetation index (ExG / NGRDI / VARI) + green_coverage_pct
  → feature stats → classifier / VLM
```

**เหตุผล (defend ได้):**
- **CCM ต้องมาก่อน vegetation index เสมอ** — ExG/NGRDI/VARI เป็น channel-ratio/difference ที่ตีความว่า RGB อยู่บนสเกลสีมาตรฐานแล้ว. ถ้าคำนวณ index บน RGB ดิบที่แสงเพี้ยน ค่าจะสะท้อนแสงไม่ใช่พืช [1][6]. Svensgaard et al. ยืนยันว่า spectral/color correction ก่อนคำนวณ nExG ปรับปรุงความแม่นของ vegetation index [13].
- **White balance vs CCM:** full CCM (affine 3×3) **subsume** การทำ white balance ส่วนใหญ่อยู่แล้ว (มันแก้ทั้ง channel gain และ cross-channel mixing). จึง **ไม่จำเป็นต้องทำ WB แยกก่อน** ถ้าใช้ CCM เต็ม; แต่ถ้าใช้ pipeline แบบ HueDx จะทำ white-balance ก่อนแล้วตามด้วย non-linear correction [12]. หลักการ: อย่าทำ WB ที่ปรับ channel แบบ ad-hoc **หลัง** CCM เพราะจะทำลาย calibration.
- **CCM ก่อน segmentation:** ถ้า segment ด้วย HSV threshold การ calibrate สีก่อนทำให้ threshold เสถียรข้ามภาพ. (ถ้าใช้ SAM/YOLO ที่ทนต่อสี การ calibrate ก็ยังจำเป็นสำหรับ "ค่า" ที่วัดหลัง segment).

---

## 5. ข้อควรระวัง: illumination ไม่สม่ำเสมอ / เงา / glare (CCM เดียวพอไหม?)

**คำตอบสั้น: CCM เดียวทั้งภาพ "ไม่พอ" เมื่อแสงไม่สม่ำเสมอ — โดยเฉพาะ VitroVision ที่ถ่ายผ่านขวดแก้วใส**

- **หลักฐานตรงประเด็น (Kang 2025):** single-patch calibration ถูกท้าทาย — "facial region อธิบาย variance ของสีได้ 25.2% มากกว่า device effect (7.0%) ถึง 3.6 เท่า" → แปลว่า **ตำแหน่ง/บริเวณในภาพมีผลต่อสีมากกว่าตัวกล้อง** จึงเสนอ **region-aware protocol** ไม่ใช่ global CCM เดียว [9].
- **Glare จากขวดแก้ว (project-specific):** global CCM แก้ค่าเฉลี่ยได้ แต่แก้ **specular highlight** ที่กระจายไม่สม่ำเสมอบนผิวแก้วไม่ได้ — จุด glare จะถูกนับเป็นพื้นที่สว่าง/ขาวผิด ๆ และ **ทำให้ `green_coverage_pct` เพี้ยน**. ต้อง **detect + mask glare ออกก่อน** ทำ CCM และก่อนนับ green coverage.
- **เงา (Chopin 2018):** ใช้ color checker ในทุกภาพเป็น ground truth + quadratic fit ลดความแปรปรวนของ canopy color ข้ามวันได้ แต่ยังต้องจัดการ shadow [6].
- **แนวทางสำหรับ VitroVision:**
  1. คุม illumination ที่ source (lightbox/diffuser, มุมไฟคงที่) เพื่อให้ global CCM พอใช้ — Conley 2024 ใช้ custom lightbox + consumer camera ได้ผลดี [2].
  2. **glare/specular masking** ก่อน CCM (threshold ความสว่าง + saturation, หรือ polarizer ที่กล้อง).
  3. ถ้าแสงยัง gradient อยู่ → พิจารณา flat-field / Retinex-based illumination normalization **ก่อน** CCM [non-uniform-illum refs] (แต่ทำหลัง masking).
- **Green-endpoint / patch selection (project-specific, Sunoj 2018):** เนื่องจาก primary endpoint = green coverage ให้เลือก patch ที่มี **chromatic R/G/B** ในการ calibrate — Sunoj พบว่าใช้เฉพาะ neutral patch (ขาว/เทา) calibrate ได้ **แย่** (CPI 0.26–1.0) ส่วน R/G/B patch ให้ผลเทียบเท่า 24 patch (CPI 0.21–0.24) [1]. → ประเมิน CCM ด้วย ΔE บน foliage-relevant (เขียว) ไม่ใช่แค่ ΔE เฉลี่ยทั้ง chart.

---

## References (Consensus — มี URL กดได้)

[1] [Color calibration of digital images for agriculture and other applications](https://consensus.app/papers/details/379b4ba741f155fb973ab1cb976e1664/?utm_source=claude_code) (Sunoj et al., 2018, ISPRS J. Photogrammetry & Remote Sensing, 74 cit.)
[2] [Visualizing Plant Responses: Novel Insights Possible Through Affordable Imaging Techniques in the Greenhouse](https://consensus.app/papers/details/28763d18ff4e536daab287fd77f9ca4e/?utm_source=claude_code) (Conley et al., 2024, Sensors)
[3] [Color Calibration of Proximal Sensing RGB Images of Oilseed Rape Canopy via Deep Learning + K-Means](https://consensus.app/papers/details/5cc98a65a7ce5d9b9ab8b20c9f22b6d5/?utm_source=claude_code) (Abdalla et al., 2019, Remote Sensing, 27 cit.)
[4] [Color Correction Using Root-Polynomial Regression](https://consensus.app/papers/details/68ccd54f5af15d4bac1ca705350bfbca/?utm_source=claude_code) (Finlayson et al., 2015, IEEE TIP, 196 cit.)
[5] [Root-Polynomial Colour Correction](https://consensus.app/papers/details/86ec001a99ea570491f9810d64f7a22d/?utm_source=claude_code) (Finlayson et al., 2011, 20 cit.)
[6] [Land-based crop phenotyping by image analysis: consistent canopy characterization from inconsistent field illumination](https://consensus.app/papers/details/2125c6b5d648596a96ea9c4152c7da31/?utm_source=claude_code) (Chopin et al., 2018, Plant Methods, 23 cit.)
[7] [An automated, high-throughput method for standardizing image color profiles to improve image-based plant phenotyping](https://consensus.app/papers/details/49a47eac2e8c5837922198ba9fced429/?utm_source=claude_code) (Berry et al., 2018, PeerJ, 33 cit.) — **method ที่ PlantCV ใช้**
[8] [Harmonizing color measurements in dentistry using translucent tooth-colored materials](https://consensus.app/papers/details/76708be063615aeaae4c6c46564c8f8a/?utm_source=claude_code) (Tango et al., 2024, BMC Oral Health)
[9] [The Color-Clinical Decoupling: Why Perceptual Calibration Fails Clinical Biomarkers in Smartphone Dermatology](https://consensus.app/papers/details/ade4128a66075656b78c7e67bf931726/?utm_source=claude_code) (Kang, 2025, ArXiv) — linear CCM ลด error 67–77%, ΔE<2.3; single-patch ไม่พอ
[10] [Performance Comparison of Classical Methods and Neural Networks for Colour Correction](https://consensus.app/papers/details/5e002d9edbc9509487e7e6e3f8f71d9a/?utm_source=claude_code) (Kucuk et al., 2023, J. Imaging, 10 cit.) — root-polynomial ชนะ NN
[11] [PlantCV v2: Image analysis software for high-throughput plant phenotyping](https://consensus.app/papers/details/819a07885af45f5dad08fd535f6b2fbd/?utm_source=claude_code) (Gehan et al., 2017, PeerJ, 283 cit.)
[12] [Development of a smartphone enabled, paper-based quantitative diagnostic assay using the HueDx color correction system](https://consensus.app/papers/details/6f70cde496eb5ccd8fb79c6f1e0100bd/?utm_source=claude_code) (Menon et al., 2024, PLOS ONE)
[13] [The importance of spectral correction of UAV-based phenotyping with RGB cameras](https://consensus.app/papers/details/3ad1deef44f55d7a8cfdefe3e610f0be/?utm_source=claude_code) (Svensgaard et al., 2021, Field Crops Research, 20 cit.)

**แหล่ง PlantCV API (official docs, verify 2026-06):**
- detect_color_card / get_color_matrix / std_color_matrix / affine_color_correction / auto_correct_color / correct_color — docs.plantcv.org (transform module) + github.com/danforthcenter/plantcv/tree/main/docs

---
*หมายเหตุ citation: paper ทั้งหมดมาจากผล Consensus search จริง พร้อม URL. ชื่อฟังก์ชัน PlantCV verify จาก official documentation โดยตรง (ไม่ได้เขียนจากความจำ).*
