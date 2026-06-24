# R4-D — Illumination Normalization / Shading Correction / Color Constancy

> สถานะ: research note (R4-D) สำหรับ VitroVision (YSC 2027 → ISEF, สาขา CSBI)
> ขอบเขต: ทำให้ "แสง/สี" คงที่ข้ามภาพและข้ามวัน เชิง **normalization algorithm** (ไม่ใช่จาก reference target โดยตรง — ส่วนนั้นคือ R4-C)
> ทุก citation มาจาก Consensus จริง + มี URL กดได้ (กฎเหล็กกัน paper ผี)

---

## VERDICT (สรุปก่อนยาว)

**ใช้ทั้งคู่ — color target (R4-C) และ normalization algorithm ไม่ซ้ำซ้อนกัน แต่ทำงานคนละแกน** หลักฐานชี้ขาดคือ Wang et al. 2023 (Plant Methods): วิธี reference-panel (Empirical Line Method) ทำงานดี **เฉพาะตอนแสงนิ่ง** แต่ **ด้อยลงเมื่อแสงแปรปรวน** ขณะที่ Retinex (color constancy แบบ per-image) ชนะภายใต้แสงแปรปรวนในการ estimate chlorophyll content [1]. นั่นพิสูจน์ว่า target กับ normalization **เสริมกัน** ไม่ใช่แทนกัน

แกนของปัญหา 3 แกน แต่ละแกนใช้เครื่องมือต่างกัน:

| แกนปัญหา | เครื่องมือที่แก้ | color target แก้ได้ไหม |
|---|---|---|
| **(A) แสงไม่สม่ำเสมอภายในเฟรม** (vignetting, เงา/แสงสะท้อนขวด กลางเฟรม vs ขอบ) | **Flat-field correction** | ❌ แก้ไม่ได้ (target แก้ global color ไม่แก้ gradient กลาง-ขอบ) → **complement แท้** |
| **(B) สี cast รวมทั้งภาพ / white balance เพี้ยน** | Color constancy (Gray-World / Shades-of-Gray) **หรือ** color target | ✅ แก้ได้ → **ตรงนี้ซ้ำซ้อนกับ R4-C** |
| **(C) แสงดริฟต์วันต่อวัน** (ความสว่าง/สีรวมเปลี่ยน) | Retinex / color constancy per-image **+** target | ✅ บางส่วน แต่ degrade เมื่อแสงแปรปรวน [1] → **เสริมกัน** |

**สำหรับ VitroVision โดยเฉพาะ (rig คงที่ + ล็อก WB/ISO + ไม่มี lightbox):**
1. **Flat-field correction = คุ้มสุด ทำง่ายสุด ทำก่อน** — เพราะ rig + WB ล็อก ทำให้ถ่าย flat frame ครั้งเดียว (rig เปล่า/พื้นหลังสม่ำเสมอ) แล้วหารได้เลย เป็นการแก้แกน (A) ที่ color target ทำไม่ได้
2. **Color constancy/target สำหรับแก้ดริฟต์ข้ามวัน** — ถ้ามี color target อยู่แล้ว (R4-C) ใช้เป็นหลัก; เสริม Shades-of-Gray เป็น fallback กรณีไม่มี target ในเฟรม
3. **segment ใน Lab/HSV** เพื่อลด sensitivity ต่อความสว่าง แต่ **ไม่พอเดี่ยวๆ** — ต้องมี (1)+(2) ด้วย

⚠️ **กับดักใหญ่:** อย่าใช้ Retinex แบบ "low-light enhancement / perceptual" (เพิ่ม contrast/ความสวย) บน measurement path — มันจะ **bias green_coverage_pct ข้ามวัน** ดูหัวข้อ "ข้อควรระวัง"

---

## 1. Flat-field / Vignetting correction (แกน A)

แสงไม่สม่ำเสมอกลางเฟรม-ขอบเฟรม (vignetting, เงา, แสงสะท้อน) เป็นปัญหาที่ **reference target แก้ไม่ได้** เพราะ target คืนค่าสีจุดเดียว/global ไม่ใช่ gradient เชิงพื้นที่

- เป็น "preprocessing สำคัญที่สุดในการวิเคราะห์ภาพเชิงปริมาณ" — flat-field correction แก้แสงไม่สม่ำเสมอจาก vignetting และรับประกันความแม่นยำของข้อมูลเชิงพื้นที่ [4]
- vignetting มีคุณสมบัติ low-rank + เปลี่ยนแบบ smooth (ค่อยๆ มืดลงจากกลางไปขอบ) จึงประมาณ/หารออกได้ [4]
- ในระบบ throughput สูง แสงไม่สม่ำเสมอ "สร้างความยากให้การประมวลผลและวิเคราะห์ข้อมูลภายหลัง" — แก้แบบทีละชั้น (stray light → inhomogeneity ความถี่สูง/ต่ำ) [5]
- มีงานปี 2026 (Nat. Commun.) ใช้ ML ประเมิน/ปรับ flat-field correction อัตโนมัติ (EVEN) — สะท้อนว่า field นี้ยัง active และสำคัญ [6]

**วิธีง่ายสำหรับ VitroVision:** ถ่าย flat frame (rig เปล่าหรือพื้นหลัง diffuse สม่ำเสมอ) ภายใต้แสง/WB เดียวกัน → corrected = raw / flat (normalize). ทำครั้งเดียวต่อ rig setup เพราะ rig + WB ล็อกแล้ว มูลค่าสูงเพราะ batch 1 ของโครงงานเน้นพิสูจน์เครื่องมือ

---

## 2. Color constancy algorithms (แกน B — Gray-World / White-Patch / Shades-of-Gray)

| Algorithm | สมมติฐาน | เหมาะ/ไม่เหมาะกับ VitroVision | อ้างอิง |
|---|---|---|---|
| **Gray-World** | ค่าเฉลี่ยฉากเป็นเทา | ใช้ได้ ทนต่อ glare กว่า White-Patch (ใช้ค่าเฉลี่ย ไม่ใช่ค่าสุดขั้ว) | [7] |
| **White-Patch / Max-RGB** | จุดสว่างสุด = ขาว | ⚠️ **เสี่ยงสุดกับขวดแก้ว** — แสงสะท้อน (specular glare) 1 พิกเซลทำลายการประมาณขาว | [7] |
| **Shades-of-Gray** (Lp / Minkowski norm) | generalize 2 อันบน, L6 ดีสุดในชุด calibrated | **แนะนำ** — กลางระหว่าง mean กับ max ทนกว่า White-Patch | [7] |
| **General Gray-World / learning-based** | เพิ่ม spatial/learning | ใช้ได้ แต่ overkill สำหรับ rig คุมแล้ว | [7][9] |

หลักฐานว่า color constancy ช่วย "ทำให้สีเป็นมาตรฐานเดียวกัน" ข้ามภาพ/อุปกรณ์: ในงาน dermoscopy (multisource images) การใช้ Gray-World / max-RGB / Shades-of-Gray **ก่อน** train/test เพิ่ม sensitivity จาก 71.0% → 79.7% และ specificity 55.2% → 76% [8]. หลักการเดียวกันใช้ได้กับ plant imaging ที่ต้องเทียบข้ามวัน

**คำแนะนำ:** ถ้าไม่มี target → **Shades-of-Gray (Lp-norm)** หรือ Gray-World; **หลีกเลี่ยง White-Patch/Max-RGB** เพราะขวดแก้วมี glare. ถ้ามี target แล้ว (R4-C) → color constancy เป็น **fallback** เมื่อ target หลุดเฟรม/บัง

---

## 3. Retinex / Illumination normalization (แกน C — แยก reflectance ออกจาก illumination)

Retinex โมเดลภาพ = reflectance × illumination แล้วประมาณ/หาร illumination ออก เหลือ reflectance (คุณสมบัติแท้ของวัตถุ ไม่ขึ้นกับแสง)

**หลักฐานชี้ขาด (discriminator paper):** Wang et al. 2023, *Plant Methods* — เทียบ 3 ทาง บนภาพ UAV เพื่อ estimate chlorophyll:
- **ELM (reference panel = แบบเดียวกับ color target)**: ดีตอนแสงนิ่ง แต่ **degrade ตอนแสงแปรปรวน (วันมีเมฆบางส่วน)**
- **Multi-scale Retinex (color constancy online)**: **ชนะ** ภายใต้แสงแปรปรวน (R² = 0.61 ตอนแสงแปรปรวน) [1]
- สรุปของ paper: illumination correction สำคัญต่อ performance ของ VI และ VI-based estimation โดยเฉพาะเมื่อแสงผันผวน [1]

→ นี่คือหลักฐานตรงว่า **target ≠ normalization** และ normalization ช่วยเพิ่ม **repeatability** จริงในงานพืช

⚠️ **แต่ระวัง Retinex 2 สาย:**
- **สาย measurement-preserving** (Wang 2023 [1], gcc ของ Sonnentag [3]) — validate กับ ground-truth สี/คลอโรฟิลล์ → **ใช้ได้กับ endpoint เชิงปริมาณ**
- **สาย perceptual / low-light enhancement** (Yang 2021 [10], Ying Sun 2022 [11], Xin Wang 2023 chemical-plant [12]) — optimize PSNR/SSIM/entropy/ความสวย → **ห้ามใช้บน measurement path** จะ bias green_coverage_pct

---

## 4. HSV / Lab color space — ช่วยลด sensitivity ต่อความสว่างได้แค่ไหน

แยก chromaticity (สี) ออกจาก intensity (ความสว่าง): ใน HSV ความสว่างไปอยู่ที่ V, ใน Lab ไปอยู่ที่ L — segment ด้วย H/S หรือ a/b จึงทนต่อการเปลี่ยนความสว่างได้บางส่วน

- การ segment ใน **CieLab** ให้ accuracy 97.4% และ robust กว่า index-based + Otsu ภายใต้ over/under-exposure [3-R3 = Riehle 2020] [13]
- HSV segment ภาพได้ดีกว่า color model อื่นในการแยก foreground [14]
- HSV ปรับ bound แบบ adaptive ทนต่อแสงเปลี่ยนได้ (IoU 0.81) [15]

**แต่ข้อจำกัดสำคัญ:** ยังไว้ใจ HSV/Lab เดี่ยวๆ ไม่ได้ —
- "ทั้งสองวิธีไวต่อการเปลี่ยน luminance; color misclassification เพิ่มขึ้นชัดเมื่อ >1500 lux" → เสนอให้เสริม HSV histogram normalization / adaptive exposure [16]
- color index แบบ empirical (รวม HSV ranges ตายตัว) "ไม่ทนต่อ imaging conditions ที่เปลี่ยน — ไม่มีตัวไหนใน 9 indices robust พอ" [2]; วิธี contrast-optimization ทนกว่า (F1 95%) [2]

→ **สรุป:** Lab/HSV **ลด** sensitivity ได้ (ควรใช้, ตรงกับที่ pipeline ใช้ HSV อยู่) แต่ **ไม่ขจัด** — ต้องมี flat-field (แกน A) + target/color-constancy (แกน B/C) ประกอบ ไม่งั้น threshold HSV จะดริฟต์ข้ามวัน

---

## 5. หลักฐาน cross-day reproducibility + ความสัมพันธ์กับ color target

| ข้อค้นพบ | หลักฐาน |
|---|---|
| Retinex เพิ่ม repeatability/ชนะ ref-panel เมื่อแสงแปรปรวน (chlorophyll est.) | Wang 2023, Plant Methods [1] |
| **gcc (green chromatic coordinate) กด effect ของแสงได้ดีกว่า ExG**; + per90 (moving window 3 วัน) ลด variability ข้ามวันเพิ่ม | Sonnentag 2012 [3] |
| gcc บนวันแดดเกือบคงที่ 11:00–15:00 แต่ **เพี้ยนเมื่อแสงน้อย (เมฆ/ฝน)** → ต้องคุมเงื่อนไขถ่าย | Nakano 2023 [17] |
| **color checker** ลด SD ของ canopy color ข้ามวันอย่างมีนัยสำคัญ (least-squares quadratic fit) | Chopin 2018, Plant Methods [18] |
| ColorChecker + 3×3 matrix ทำให้ภาพ homogeneous เพื่อเทียบ phenology; ใช้ R/G/B patches พอ | Sunoj 2018 [19] |
| color correction ด้วย ColourChecker ให้ผลคงที่ข้าม 4 สภาพแสง + ข้ามกล้อง | Wright 2023, Plant Methods [20] |

**ความสัมพันธ์กับ color target (R4-C) — เสริมหรือซ้ำ?**
- **เสริม (ไม่ซ้ำ):** flat-field (แกน A) + Retinex per-image ตอนแสงแปรปรวน (แกน C) — target ทำสองอย่างนี้ไม่ได้ [1][4]
- **ซ้ำ (เลือกอย่างใดอย่างหนึ่งพอ):** การแก้ global color cast (แกน B) — ถ้ามี target ดีๆ ในเฟรม + 3×3 matrix [19] แล้ว ก็ไม่จำเป็นต้องรัน Gray-World เพิ่ม (จะกลายเป็น double-correction ทำให้ค่าเพี้ยน)

**ลำดับที่แนะนำสำหรับ VitroVision pipeline:**
```
1. Flat-field correction (หาร flat frame)        ← แก้แกน A, target ทำไม่ได้, ทำครั้งเดียว
2. Color correction ด้วย color target (R4-C)     ← แก้แกน B+C หลัก (ถ้า target อยู่ในเฟรม)
   [ถ้าไม่มี target → Shades-of-Gray แทน]
3. แปลงเป็น Lab/HSV แล้ว segment                  ← ลด sensitivity เพิ่ม
4. คำนวณ green_coverage_pct จาก mask
```

---

## ข้อควรระวัง (สำคัญต่อความ valid ของโครงงาน)

1. **อย่าใช้ Retinex สาย perceptual/low-light-enhancement บน measurement path** — Yang 2021 [10], Ying Sun 2022 [11], Xin Wang 2023 [12] optimize ความสวย/contrast/PSNR ไม่ใช่ความถูกต้องเชิงปริมาณ จะ **bias green_coverage_pct ข้ามวัน** ใช้ได้เฉพาะสาย measurement-preserving ที่ validate กับ ground truth [1][3]

2. **White-Patch / Max-RGB อันตรายกับขวดแก้ว** — specular glare 1 จุดทำลายการประมาณขาว → ใช้ Shades-of-Gray/Gray-World หรือ mask highlights ก่อน [7]

3. **อย่า double-correct** — ถ้าใช้ color target แก้ global color แล้ว อย่ารัน Gray-World ทับ (แกน B ซ้ำกัน) จะทำให้ค่าผิดทิศ

4. **แยกให้ชัดว่า normalization ช่วยอะไร:**
   - **green_coverage_pct** = สัดส่วนพื้นที่จาก **segmentation** → normalization ช่วยโดย **ทำให้ threshold ใน HSV/Lab เสถียรข้ามวัน** (ไม่ใช่ค่า index โดยตรง)
   - **gcc / color ratio** = ค่าความเข้มสี → normalization ช่วยที่ตัวค่า
   - อย่าสับสนสองอันนี้เวลาเขียนรายงาน

5. **gcc/color index เพี้ยนตอนแสงน้อย** [17] — ตอกย้ำว่าการถ่าย 17:00 ทุกวันต้องคุมไม่ให้แสงต่ำเกินบางวัน (เมฆ/ฝน) — flat-field/target ไม่ช่วยถ้าแสงน้อยจน SNR แย่

6. **ไม่มี color index ตายตัวตัวไหน robust ข้ามสภาพแสง** [2] — การล็อก HSV range ตายตัวข้าม 28 วัน × 5 สูตรเสี่ยง ต้องมี normalization upstream หรือ adaptive threshold

---

## References (จาก Consensus จริง — URL กดได้)

[1] [The impact of variable illumination on vegetation indices and evaluation of illumination correction methods on chlorophyll content estimation using UAV imagery](https://consensus.app/papers/details/02390d76a82f587ab5a8670d7b969a6e/?utm_source=claude_code) (Wang et al., 2023, Plant Methods, 40 cit.) — **discriminator paper: ELM vs Retinex**
[2] [Robust plant segmentation of color images based on image contrast optimization](https://consensus.app/papers/details/18ee69959392572d9c3544e62043f992/?utm_source=claude_code) (Lu et al., 2022, Comput. Electron. Agric., 40 cit.)
[3] [Digital repeat photography for phenological research in forest ecosystems](https://consensus.app/papers/details/0fb80bffc8be540098e429e74e76fa5f/?utm_source=claude_code) (Sonnentag et al., 2012, Agric. For. Meteorol., 581 cit.) — **gcc กด illumination + per90**
[4] [A Novel Low Rank Smooth Flat-Field Correction Algorithm for Hyperspectral Microscopy Imaging](https://consensus.app/papers/details/32d14363e8865e47822a471f45cd9bbc/?utm_source=claude_code) (Wang et al., 2022, IEEE TMI, 16 cit.)
[5] [Flat-field correction for high-throughput fluorescence microscopy](https://consensus.app/papers/details/06626391a08055a9a47aa65558dd9cd0/?utm_source=claude_code) (Chang et al., 2022, Optical Engineering)
[6] [Automatic optimization of flat-field corrections by evaluation and enhancement (EVEN) in multimodal optical microscopy](https://consensus.app/papers/details/d9cccb57dd7f5cf7bf6a48c0c5f9674f/?utm_source=claude_code) (Corbetta et al., 2026, Nature Communications)
[7] [Shades of Gray and Colour Constancy](https://consensus.app/papers/details/33220b338ef45b8fa5c21f11709ef74a/?utm_source=claude_code) (Finlayson et al., 2004, 716 cit.) — **Gray-World/Max-RGB/Shades-of-Gray, L6 norm**
[8] [Improving Dermoscopy Image Classification Using Color Constancy](https://consensus.app/papers/details/2675bfe5970551bab55d23ec4aa4387c/?utm_source=claude_code) (Barata et al., 2015, IEEE JBHI, 230 cit.)
[9] [A comparison of computational color constancy algorithms. I: Methodology and experiments with synthesized data](https://consensus.app/papers/details/0cc7db95300b5ad7984482ce7ddce9b1/?utm_source=claude_code) (Barnard et al., 2002, IEEE TIP, 474 cit.)
[10] [Sparse Gradient Regularized Deep Retinex Network for Robust Low-Light Image Enhancement](https://consensus.app/papers/details/783f7a1450af5e00aea12d68235a9856/?utm_source=claude_code) (Yang et al., 2021, IEEE TIP, 683 cit.) — ⚠️ perceptual, ไม่ใช่ measurement
[11] [Low-Illumination Image Enhancement Algorithm Based on Improved Multi-Scale Retinex and ABC Algorithm Optimization](https://consensus.app/papers/details/99043906ddf45d3b9fd8ab84bd76c03f/?utm_source=claude_code) (Sun et al., 2022, Front. Bioeng. Biotechnol., 95 cit.) — ⚠️ perceptual
[12] [Improved Retinex algorithm for low illumination image enhancement in the chemical plant area](https://consensus.app/papers/details/b68d449bb48357a584da6e2bece7623b/?utm_source=claude_code) (Wang et al., 2023, Scientific Reports) — ⚠️ perceptual
[13] [Robust index-based semantic plant/background segmentation for RGB-images](https://consensus.app/papers/details/40680d46605351a28c89fa85f8c6d014/?utm_source=claude_code) (Riehle et al., 2020, Comput. Electron. Agric., 94 cit.) — **CieLab 97.4%**
[14] [Interactive Color Image Segmentation using HSV Color Space](https://consensus.app/papers/details/b39e359bf2eb51928fb41c4ff151f30a/?utm_source=claude_code) (Hema et al., 2019, 60 cit.)
[15] [Adaptive HSV segmentation for real-time object detection under varying lighting conditions](https://consensus.app/papers/details/a8bbba9aba6d5b27a74bd4d6a08360ef/?utm_source=claude_code) (Oleynikov et al., 2026)
[16] [Performance Evaluation of Contour Detection and Hough Transform for Shape Identification Using HSV Color Space](https://consensus.app/papers/details/5cb47343befb587b99d834ba4a36f9ff/?utm_source=claude_code) (Herdiyanto et al., 2025) — ไวต่อ luminance >1500 lux
[17] [Applicability of digital camera images to estimate vegetation parameters in semi-arid grasslands of Mongolia](https://consensus.app/papers/details/0648b0de03f752bba8cfbc274500908d/?utm_source=claude_code) (Nakano et al., 2023, J. Agric. Meteorol.) — gcc เพี้ยนตอนแสงน้อย
[18] [Land-based crop phenotyping by image analysis: consistent canopy characterization from inconsistent field illumination](https://consensus.app/papers/details/2125c6b5d648596a96ea9c4152c7da31/?utm_source=claude_code) (Chopin et al., 2018, Plant Methods, 23 cit.) — **color checker ลด SD canopy color ข้ามวัน**
[19] [Color calibration of digital images for agriculture and other applications](https://consensus.app/papers/details/379b4ba741f155fb973ab1cb976e1664/?utm_source=claude_code) (Sunoj et al., 2018, ISPRS J., 74 cit.) — ColorChecker 3×3 matrix
[20] [Free and open-source software for object detection, size, and colour determination for use in plant phenotyping](https://consensus.app/papers/details/f274a1aa301e5e219957706e65ed12d3/?utm_source=claude_code) (Wright et al., 2023, Plant Methods, 7 cit.) — ColourChecker ข้าม 4 สภาพแสง/กล้อง

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
