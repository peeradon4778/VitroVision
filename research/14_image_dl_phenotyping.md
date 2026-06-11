# 14 — Image-Based & Deep Learning Morphological Phenotyping สำหรับต้นกล้าพืช

**วันที่:** 2026-06-11
**บริบท:** VitroVision — Capsicum annuum in vitro tissue culture, ถ่ายภาพ RGB ผ่านขวด (2D single-view), ส่ง YSC 2027 สาขา CSBI
**วัตถุประสงค์:** สำรวจว่า DL morphological phenotyping ของต้นกล้าควรวัด/segment โครงสร้างอะไร และ map กับ pipeline ปัจจุบัน

---

## 1. สรุป — Morphological Traits ที่ Image Phenotyping วัด และ Map กับ 7 Features ปัจจุบัน

### 1.1 Trait หลักที่ image-based phenotyping วัดได้

งาน high-throughput plant phenotyping ได้กำหนด taxonomy ของ trait ที่ quantify ได้จากภาพไว้กว้างขวาง [3] ครอบคลุม:

| กลุ่ม Trait | ตัวอย่าง Trait | จาก 2D RGB ได้ไหม |
|---|---|---|
| **Shoot architecture** | plant height (projected), internode length | ได้ (ประมาณ) |
| **Leaf morphology** | projected leaf area (PLA), leaf length, leaf width, leaf shape index | ได้ |
| **Leaf count** | จำนวนใบทั้งหมด, leaf age stage | ได้ (ยากถ้า overlap) |
| **Color indices** | Green%, NDVI (synthetic), G/R ratio, MNDVI, hue/saturation | ได้ดีมาก |
| **Texture / complexity** | entropy, surface roughness, venation pattern | ได้ |
| **Compactness / canopy** | convex hull area, solidity, circularity, canopy coverage ratio | ได้ |
| **Vigor / biomass proxy** | projected shoot area, shoot fresh weight proxy | ได้ (indirect) |
| **Stem** | stem diameter (จาก 2D ไม่แม่นยำ), internode visibility | จำกัด |
| **Chlorophyll/health** | SPAD proxy จาก RGB color ratio | ได้ (ประมาณ) |
| **Browning / necrosis** | brown%, necrotic area fraction | ได้ |

งาน pepper phenotyping โดยตรง [P1] ใช้ instance segmentation (deep learning) สำหรับ pepper fruit varieties โดย mAP เพิ่มจาก 0.63 (classical) → 0.97 (DL-based) ซึ่งแสดงให้เห็น superiority ของ DL ชัดเจน งานบน pepper seedling ที่ controlled environment [P2] ดึง 18 color features + 9 texture features (GLCM) + 1 morphological feature แล้วใช้ SVM จำแนก environmental stress ได้ accuracy 86% ซึ่งใกล้เคียงกับ approach ปัจจุบันของ VitroVision มาก

### 1.2 Mapping กับ 7 Features ปัจจุบันของ VitroVision

| Feature ปัจจุบัน | Status | Trait ที่ควรเพิ่มเติม/ยกระดับ |
|---|---|---|
| **green%** | มีแล้ว (color ratio) | ยกระดับเป็น synthetic NDVI (G-R)/(G+R) หรือ ExG index |
| **leaf color** | มีแล้ว (HSV/RGB mean) | เพิ่ม GLCM texture features (contrast, energy, homogeneity) |
| **shoot count** | มีแล้ว (count) | ยกระดับเป็น instance segmentation เพื่อแยก shoot แต่ละต้น |
| **entropy** | มีแล้ว (texture) | complement ด้วย fractal dimension หรือ lacunarity |
| **brown%** | มีแล้ว (necrosis) | เพิ่ม spatial distribution ของ brown pixels (clustered vs scattered) |
| **vigor** | มีแล้ว (composite score) | แยกเป็น projected shoot area + compactness index อย่างชัดเจน |
| **EfficientNet class** | มีแล้ว (classification) | เพิ่ม **projected leaf area (PLA)**, **leaf count**, **shoot height proxy**, **convex hull ratio** |

### 1.3 Traits ที่ควรเพิ่มในโมเดล (Priority)

**Priority 1 — เพิ่มได้ทันที จาก 2D classical CV:**
- **Projected Leaf Area (PLA)** — พื้นที่สีเขียวทั้งหมด (pixel count × scale factor)
- **Convex Hull Ratio (solidity)** = PLA / convex hull area — วัดความ "กระจาย" ของ canopy
- **Bounding Box Aspect Ratio** — plant height proxy จาก bounding box ของ shoot

**Priority 2 — ต้องการ DL segmentation:**
- **Leaf count** (N_leaves) — ใช้ CNN-based leaf counter [8,9,10]
- **Individual leaf area** (per-leaf PLA) — ต้องการ instance segmentation
- **Shoot segmentation mask** — แยก shoot/callus/agar boundary

**Priority 3 — Research-grade, ต้องการ annotation:**
- **Internode count / length proxy** — shoot architecture complexity
- **Leaf shape index** (elongation, circularity per leaf)
- **Chlorophyll proxy** จาก RGB (ExG, VARI, GLI) correlate กับ SPAD [5,6]

---

## 2. Deep Learning Segmentation Approaches

### 2.1 Semantic vs Instance Segmentation ใน Plant Phenotyping

**Semantic segmentation** แยก pixel ออกเป็นคลาส (leaf, stem, background, callus) ทั้งภาพ
**Instance segmentation** แยกแต่ละใบออกจากกัน (leaf 1, leaf 2, ...) — สำคัญมากสำหรับ leaf count และ per-leaf area

งาน HUMRC-PS [4] รวม U-Net + Mask R-CNN + Pelican Search Optimization ได้ accuracy 98.76% สำหรับ plant phenotyping traits (leaf morphology, color variations, size) โดย U-Net จับ local+global features ส่วน Mask R-CNN segment plant regions

งาน Weinan Shi et al. (2019) [S1] ใช้ FCN (semantic) + Mask R-CNN (instance) บน tomato seedlings แบบ multi-view และพบว่า 3D > 2D เนื่องจาก 2D errors ไม่ persist ข้าม viewpoint — แต่ใน VitroVision บริบท in-vitro single-view เราใช้ 2D เป็น baseline ก่อนได้

**Architecture ที่เหมาะสมสำหรับ VitroVision:**

| Architecture | Use Case | ข้อดี |
|---|---|---|
| **U-Net** (ResUNet) | Semantic segmentation shoot/callus/agar | เหมาะกับ small dataset, medical-image origin |
| **Mask R-CNN** | Instance segmentation รายใบ | detect + segment พร้อมกัน |
| **YOLOv8-seg** | Real-time instance segmentation | เร็ว, API ที่ VitroVision ใช้อยู่แล้ว |
| **SAM (Segment Anything)** | Zero-shot segmentation | ไม่ต้อง train annotation มาก |

### 2.2 Leaf Counting with DL

งาน LC-Net [8] ใช้ SegNet + CNN สำหรับ rosette plants บน CVPPP dataset ได้ผลดีกว่า DeepLab V3+, U-Net, RefineNet โดยป้อน original image + segmented leaf parts พร้อมกัน

งาน Aich & Stavness (2017) [10] ใช้ deconvolutional network สำหรับ segmentation + CNN สำหรับ leaf counting บน CVPPP-2017 ได้ mean absolute count difference = 1.62 ± 2.30 ซึ่ง acceptable สำหรับ in vitro context ที่ขวดมักมีใบน้อย (< 10 ใบ)

งาน Xu et al. (2022) [M1] ใช้ Mask R-CNN + YOLOv5 pipeline บน maize field images ได้ precision 96.9% สำหรับ segmentation

### 2.3 Pepper-Specific DL

งาน Gómez-Zamanillo et al. (2024) [P1] — instance segmentation บน pepper (Blocky Bell, Jalapeño, Lamuyo) ด้วย deep learning under field conditions พิสูจน์ว่า DL-based ดีกว่า classical ชัดเจน (mAP: 0.52–0.97 vs 0.39–0.67) นี่เป็น paper ที่สำคัญที่สุดสำหรับ VitroVision เพราะเป็น Capsicum โดยตรง

งาน Huo et al. (2025) [P3] ใช้ YOLOX + CA attention สำหรับ pepper phenotypic measurement (plant height R² = 0.973, stem diameter R² = 0.842) โดย HSV threshold segmentation + morphological operations ซึ่งใกล้เคียงกับ pipeline ปัจจุบันของเราที่ใช้ HSV

---

## 3. In Vitro / Controlled Environment CV Pipelines

### 3.1 In Vitro Image Analysis สำหรับ Plantlet Quality

งาน Aynalem et al. (2006) [IV1] เป็น landmark paper ที่เปรียบ visual assessment กับ digital image analysis บน in vitro stored pear plantlets พบว่า **G/R ratio และ MNDVI** (Modified NDVI จาก RGB) สัมพันธ์กับ visual ratings อย่างมีนัยสำคัญ (r² ≥ 0.5) สำหรับทุก cultivar ส่วน intensity, hue, saturation ไม่ consistent — นี่ validate approach ของ VitroVision ที่ใช้ green% และ brown%

**MNDVI formula (RGB-only):** `MNDVI = (G - R) / (G + R)` ซึ่งเทียบเท่า ExG index ใน remote sensing

### 3.2 PlantCV Pipeline

งาน Gehan et al. (2017) — PlantCV v2 [CV1] เป็น open-source image analysis toolkit สำหรับ plant phenotyping ที่รวม:
- Image normalization
- Multi-plant analysis
- Leaf segmentation
- Landmark identification for morphometrics
- Machine learning modules

PlantCV เป็น reference implementation ที่ VitroVision ควรพิจารณา adopt หรืออย่างน้อย study สำหรับ standard trait definitions

### 3.3 Cell Culture Quality Control ด้วย Morphology

งาน Imai et al. (2018) [CC1] — แม้จะเป็น cell culture (MSC) ไม่ใช่พืช แต่ approach ที่ใช้ time-course morphological profiles + PCA visualization + MT method สำหรับ error detection ใน culture process สามารถ adapt สำหรับ VitroVision ได้:
- วัด morphological profiles ต่อเนื่องตามเวลา
- ใช้ PCA แสดง trajectory ของ phenotype
- ตรวจจับ deviation จาก standard culture ได้ใน 2 วัน

### 3.4 Pepper Seedling Stress Classification

งาน Islam et al. (2024) [P2] ใช้ controlled plant growth chamber สำหรับ pepper seedlings (อายุ 2 สัปดาห์) ถ่ายภาพ RGB ทุกวัน สกัด:
- 18 color features (RGB, HSV, Lab color spaces)
- 9 GLCM texture features
- 1 morphological feature
แล้วใช้ SVM + Sequential Feature Selection (SFS) จำแนก stress ได้ 86% — approach นี้ใกล้เคียง VitroVision มาก และเป็น evidence สนับสนุน methodology

---

## 4. ข้อจำกัดของ 2D Single-View RGB และทางแก้

### 4.1 สิ่งที่ 2D วัดได้ดี

- Color-based traits: green%, G/R ratio, brown%, MNDVI, ExG → **ดีมาก**
- Projected area (PLA): พื้นที่ 2D ของ canopy → **ดี แต่ underestimate จริง**
- Texture/entropy: GLCM features → **ดี**
- Approximate leaf count: ถ้าใบไม่ overlap มาก → **พอใช้**
- Plant presence/absence, shoot count → **ดีมาก**
- Classification (EfficientNet) → **ดีมาก**

### 4.2 ข้อจำกัดหลัก

งาน Das Choudhury et al. (2020) [2D1] อธิบายชัดว่า: *"2D single-view images ของพืชโดยเฉพาะที่ advanced vegetative stage มี self-occlusion จาก leaf overlap ทำให้ข้อมูลที่จับได้ไม่ครบ และ phenotypes ที่คำนวณได้มีความผิดพลาด"*

ข้อจำกัดเฉพาะของ in vitro + 2D:

| ข้อจำกัด | ผลกระทบต่อ VitroVision | ทางแก้ |
|---|---|---|
| **Leaf occlusion** | leaf count underestimate, PLA underestimate | ยอมรับเป็น "visible leaf" metric; หรือ rotate ขวด |
| **Glass refraction/glare** | บิดเบือน color และ texture ที่ขอบขวด | mask boundary region, normalize illumination |
| **3D structure ไม่มี** | ไม่สามารถวัด real height, stem diameter, leaf angle ได้ | frame เป็น 2D projected traits อย่างชัดเจน |
| **Single viewpoint** | ไม่เห็นด้านหลัง | พิจารณาถ่าย 2-4 views ต่อขวด (cost: annotation) |
| **Scale ambiguity** | หน่วย pixel ไม่แน่นอน | ใส่ reference scale marker ในภาพ |
| **Lighting inconsistency** | color shift ข้ามวัน | color calibration card หรือ white balance normalization |

### 4.3 ทางแก้ที่ feasible สำหรับ VitroVision

1. **Frame 2D traits อย่างถูกต้อง** — เรียกว่า "projected leaf area", "visible shoot count" ไม่ใช่ "true leaf area" เพื่อความ scientific rigor (สำคัญสำหรับ YSC)
2. **Synthetic NDVI จาก RGB** — ใช้ ExG = 2G - R - B หรือ VARI = (G-R)/(G+R-B) แทน NDVI จริง [5]
3. **Illumination normalization** — ก่อน extract features ทุกครั้ง (histogram equalization หรือ CLAHE)
4. **Reference marker** — สติ๊กเกอร์สีบน ขวดเดิมๆ เพื่อ scale และ color calibration
5. **Multi-view เบื้องต้น** — ถ่าย 2 มุม (front/side 90°) ด้วย setup เดิม เพิ่ม information ได้ทันที

---

## 5. ข้อแนะนำต่อ Roadmap DL ของ VitroVision

### Phase A — ระยะสั้น (ก่อน YSC submission, ต.ค. 2026)

เพิ่ม traits จาก classical CV ก่อน ไม่ต้อง retrain model ใหม่:

```
เพิ่มใน feature vector ปัจจุบัน:
+ projected_leaf_area_px      (green mask pixel count)
+ convex_hull_ratio           (= green_area / convex_hull_area)
+ ExG_index                   (= 2G - R - B, normalized)
+ GLCM_contrast               (texture ละเอียดกว่า entropy)
+ GLCM_homogeneity
+ bounding_box_AR             (aspect ratio ≈ height/width proxy)
```

### Phase B — DL Segmentation (parallel development)

1. **Annotate 200-500 ภาพ** ด้วย semantic mask: shoot / agar / glass_background / brown_tissue
2. **Train U-Net (ResUNet-34)** บน conda env `ml` ที่มีอยู่ — PyTorch CPU feasible สำหรับ small dataset
3. **Output:** per-pixel segment → คำนวณ projected_shoot_area, shoot/total_area_ratio แม่นยำขึ้น

### Phase C — Instance Segmentation (post-YSC หรือ ISEF)

1. **YOLOv8-seg** (ที่ VitroVision มี ultralytics อยู่แล้ว) สำหรับ individual leaf instance
2. **Output:** leaf count (N_visible), per-leaf area distribution, leaf size variance (uniformity index)
3. **Biological interpretation:** N_leaves correlate กับ developmental stage; leaf size variance → culture uniformity

### Phase D — Phenotypic Growth Curve

- ถ่ายภาพ time-series ต่อขวด (เช่น day 0, 7, 14, 21)
- Plot phenotype trajectory: PLA(t), green%(t), N_leaves(t)
- คำนวณ growth rate = dPLA/dt เป็น vigor index เชิง dynamic
- อ้างอิง Imai et al. (2018) [CC1] ที่ใช้ time-course morphology สำหรับ culture QC

### สรุป Traits ที่แนะนำให้เพิ่ม (เรียงตาม priority)

| Rank | Trait | วิธี | ความสำคัญ YSC |
|---|---|---|---|
| 1 | Projected Leaf Area (PLA) | classical CV (green mask) | สูงมาก — quantitative, publishable |
| 2 | Convex Hull Ratio / Solidity | classical CV | สูง — shoot architecture |
| 3 | ExG / VARI color index | classical CV | สูง — chlorophyll proxy |
| 4 | GLCM texture (contrast, homogeneity) | classical CV | กลาง — ยืนยัน texture rigor |
| 5 | Leaf count (N_visible) | DL (YOLOv8-seg หรือ LC-Net) | สูงมาก — biological relevance |
| 6 | Semantic segmentation mask | DL (U-Net) | กลาง — ถ้ามี annotation |
| 7 | Growth rate dPLA/dt | time-series | สูง — ถ้ามีข้อมูล longitudinal |

---

## 6. References

[1] [Stem-Leaf Segmentation and Morphological Traits Extraction in Rapeseed Seedlings Using a Three-Dimensional Point Cloud](https://consensus.app/papers/details/e4a53178f6745e7b84b052ced5aa3ba2/?utm_source=claude_code) (Binqian Sun et al., 2025, Agronomy, 11 citations)

[2] [Three-dimensional reconstruction and phenotype measurement of maize seedlings based on multi-view image sequences](https://consensus.app/papers/details/68d17927b3eb5088a14ebf699c81641e/?utm_source=claude_code) (Yuchao Li et al., 2022, Frontiers in Plant Science, 41 citations)

[3] [Unlocking plant secrets: A systematic review of 3D imaging in plant phenotyping techniques](https://consensus.app/papers/details/9d0fce8d9609559c954967ac1fa655f0/?utm_source=claude_code) (Muhammad Salman Akhtar et al., 2024, Computers and Electronics in Agriculture, 66 citations)

[4] [HUMRC-PS: Revolutionizing plant phenotyping through Regional Convolutional Neural Networks and Pelican Search Optimization](https://consensus.app/papers/details/718e3582021a571088a1db79bd2d073b/?utm_source=claude_code) (P. Kumar et al., 2024, Evolving Systems, 31 citations)

[5] [An Improved Normalized Difference Vegetation Index (NDVI) Estimation Using Grounded Dino and Segment Anything Model for Plant Health Classification](https://consensus.app/papers/details/8af0fea98fb75a8aabcfe1350c4ec70f/?utm_source=claude_code) (A. Balasundaram et al., 2024, IEEE Access, 14 citations)

[6] [High-Throughput Analysis of Leaf Chlorophyll Content in Aquaponically Grown Lettuce Using Hyperspectral Reflectance and RGB Images](https://consensus.app/papers/details/6932ca0f54305e2cb754f61dfacf6762/?utm_source=claude_code) (M. F. Taha et al., 2024, Plants, 24 citations)

[7] [PSegNet: Simultaneous Semantic and Instance Segmentation for Point Clouds of Plants](https://consensus.app/papers/details/5f2e6c3f8fdf55049a1633ce2136d1d2/?utm_source=claude_code) (Dawei Li et al., 2022, Plant Phenomics, 82 citations)

[8] [A CNN-based model to count the leaves of rosette plants (LC-Net)](https://consensus.app/papers/details/924f2086215f5990b95178eab5b78137/?utm_source=claude_code) (Mainak Deb et al., 2024, Scientific Reports, 35 citations)

[9] [Rosette plant segmentation with leaf count using orthogonal transform and deep convolutional neural network](https://consensus.app/papers/details/f14744507a535b0986d66f7466604625/?utm_source=claude_code) (J. Praveen Kumar et al., 2020, Machine Vision and Applications, 32 citations)

[10] [Leaf Counting with Deep Convolutional and Deconvolutional Networks](https://consensus.app/papers/details/d91f4b1b9bb55008a3ecc4b90540b653/?utm_source=claude_code) (Shubhra Aich et al., 2017, ICCV Workshops, 166 citations)

[IV1] [Non-destructive evaluation of in vitro-stored plants: A comparison of visual and image analysis](https://consensus.app/papers/details/33f703b3d5ba5ee985dffa052c1a81e7/?utm_source=claude_code) (H. Aynalem et al., 2006, In Vitro Cellular & Developmental Biology - Plant, 19 citations)

[CV1] [PlantCV v2: Image analysis software for high-throughput plant phenotyping](https://consensus.app/papers/details/819a07885af45f5dad08fd535f6b2fbd/?utm_source=claude_code) (Malia A. Gehan et al., 2017, PeerJ, 282 citations)

[CC1] [In-process evaluation of culture errors using morphology-based image analysis](https://consensus.app/papers/details/53062238ee20585f923655c2b5f6732a/?utm_source=claude_code) (Yuta Imai et al., 2018, Regenerative Therapy, 16 citations)

[P1] [Deep learning-based instance segmentation for improved pepper phenotyping](https://consensus.app/papers/details/aa9013c3c954592681f0af1185ba3631/?utm_source=claude_code) (Laura Gómez-Zamanillo et al., 2024, Smart Agricultural Technology, 5 citations)

[P2] [Image Processing and Support Vector Machine (SVM) for Classifying Environmental Stress Symptoms of Pepper Seedlings Grown in a Plant Factory](https://consensus.app/papers/details/d675771916735be48bebf33aacfab6c0/?utm_source=claude_code) (Sumaiya Islam et al., 2024, Agronomy, 24 citations)

[P3] [Research on Obtaining Pepper Phenotypic Parameters Based on Improved YOLOX Algorithm](https://consensus.app/papers/details/019a29c67455538d84186b2c999fbb89/?utm_source=claude_code) (Yukang Huo et al., 2025, AgriEngineering, 8 citations)

[S1] [Plant-part segmentation using deep learning and multi-view vision](https://consensus.app/papers/details/893ad5b39c635c66b86802fbf9e02644/?utm_source=claude_code) (Weinan Shi et al., 2019, Biosystems Engineering, 124 citations)

[2D1] [Leveraging Image Analysis to Compute 3D Plant Phenotypes Based on Voxel-Grid Plant Reconstruction](https://consensus.app/papers/details/207db1a50c38506f94ec4d3248936842/?utm_source=claude_code) (Sruti Das Choudhury et al., 2020, Frontiers in Plant Science, 55 citations)

[SV1] [Prediction of Useful Eggplant Seedling Transplants Using Multi-View Images](https://consensus.app/papers/details/f94f53f248e05dcd8704e300e0b4779b/?utm_source=claude_code) (Xiangyang Yuan et al., 2024, Agronomy, 7 citations)

[SV2] [Selective transplantation method of leafy vegetable seedlings based on ResNet 18 network](https://consensus.app/papers/details/be3ac58b0bb350bdaa77158afec8de9f/?utm_source=claude_code) (Xin Jin et al., 2022, Frontiers in Plant Science, 16 citations)

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
