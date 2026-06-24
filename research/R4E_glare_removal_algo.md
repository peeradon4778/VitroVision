# R4-E: การลบ Specular Highlight / Glare ด้วย Software (Algorithmic)

> Sub-agent R4-E | VitroVision (YSC 2027 → ISEF, CSBI)
> ขอบเขต: วิธี **algorithm/software** ตรวจจับและจัดการ glare บนภาพต้นพริก (Capsicum frutescens) เพาะเลี้ยงเนื้อเยื่อ **ถ่ายผ่านขวดแก้วใสโค้ง** — เป็น fallback/เสริมจาก R4-A (polarizer/diffuse เชิงกายภาพ)

---

## VERDICT (สรุปเชิงตัดสินใจ)

1. **glare กระทบ green segmentation / vegetation index จริงและวัดได้** — มีหลักฐานตรงว่า specular reflection จากผิวใบทำให้ค่า SR และ NDVI เพี้ยนมากที่สุด และลดความแม่นของการ inversion ค่าคลอโรฟิลล์ (SPAD) [1][2][3]. นี่คือเหตุผลทางวิทยาศาสตร์ว่า **ต้องจัดการ glare ก่อน downstream**.

2. **บน CPU ให้ใช้ pipeline คลาสสิก 2 ขั้น:** (ก) **Detection** ด้วย thresholding ใน HSV (saturation ต่ำ + value สูง) แบบ adaptive [4][8] → ได้ glare mask; (ข) **จัดการ mask นั้นด้วยการ MASK-OUT (ไม่นับ pixel) เป็นค่า default** ไม่ใช่ inpaint. Deep learning (Unet-Transformer / GAN) [5][6][7] ให้ผลสวยกว่าเชิงภาพแต่ **ไม่ practical บน CPU ของโครงงานนี้** (หนัก, ต้อง paired dataset, เสี่ยง hallucinate texture).

3. **mask-out ซื่อสัตย์เชิงสถิติกว่า inpaint สำหรับงานนี้** — เพราะ (i) เราวัด phenotype เชิงปริมาณ (พื้นที่เขียว, ดัชนีพืช) การเดาค่า pixel คืนด้วย inpaint = **สร้างข้อมูลปลอม** เข้าไปในตัวเลขที่จะรายงาน; (ii) **hyperhydricity (vitrified) คือ phenotype ที่ใบฉ่ำน้ำเงาวับ** — ความเงานั้น *เป็นสัญญาณ ไม่ใช่ noise*. ถ้า inpaint ทับ เท่ากับ "ลบหลักฐาน hyperhydric" ทิ้ง. mask-out + รายงาน "%พื้นที่ที่วัดได้ vs %ถูก mask" จึงโปร่งใสและไม่ปลอม phenotype [9].

4. **แนวทางผสมที่แนะนำจริง:** mask-out เป็นหลัก → ใช้ **glare-fraction (สัดส่วนพื้นที่ใบที่เป็น highlight)** เป็น *feature เสริมบ่งชี้ hyperhydricity* (ใบ vitrified จะมี specular มากผิดปกติ) → ถ้าจำเป็นต้องเติมภาพให้ "ดูครบ" เพื่อ visualization เท่านั้น ค่อย inpaint **แยก layer** และ **ห้ามนำ pixel ที่ inpaint ไปคำนวณดัชนี**.

---

## ตาราง: วิธี Detection ของ Glare/Specular

| วิธี | หลักการ | CPU-practical? | อ้างอิง + URL |
|---|---|---|---|
| **HSV thresholding (adaptive)** | specular = saturation ต่ำ + value/brightness สูง; ปรับ contrast ก่อน แล้ว auto-threshold + post-process ลด false positive | ✅ **ดีมาก** real-time, เบา, OpenCV ทำได้ตรง | [Morgand & Lavest 2014](https://consensus.app/papers/details/22b7ef7480cc5fcba60ee297b981ff51/?utm_source=claude_code) [4] |
| **Brightness classification + adaptive threshold** | จำแนกความสว่างภาพก่อน แล้วใช้ threshold ที่เปลี่ยนตามความสว่างจับ "absolute highlight" | ✅ ดี (ออกแบบมาเพื่อภาพ medical/endoscope ที่เงาเยอะ คล้ายผิวเปียก) | [Nie et al. 2023, Sensors](https://consensus.app/papers/details/d5c28e5a49905ece82ca2578405770cd/?utm_source=claude_code) [8] |
| **Dichromatic Reflection Model (DRM) clustering** | แยก diffuse/specular ตามทฤษฎี dichromatic; clustering (GMM/x-means) แยก saturated vs unsaturated highlight | ⚠️ ปานกลาง — งานเด่นๆ ใช้ **light field camera** (หลายมุมมอง) ไม่ใช่กล้องเดี่ยว; เวอร์ชัน single-image ทำได้แต่ซับซ้อน | [Feng et al. 2024](https://consensus.app/papers/details/45d5664fa21350c5b618920e6dbce462/?utm_source=claude_code) [10] · [Feng et al. 2022](https://consensus.app/papers/details/34b4631229b45012a82ed555c2853f99/?utm_source=claude_code) |
| **Deep highlight detection mask (encoder-decoder)** | เครือข่ายเรียน mask ของ highlight เป็น guidance ให้ removal | ❌ บน CPU ช้า, ต้อง train | [Wu et al. 2022](https://consensus.app/papers/details/0d16fd3ecc6258f2aa3efa71be367d0c/?utm_source=claude_code) [5] |

## ตาราง: วิธี Removal / จัดการ Glare

| วิธี | หลักการ | CPU-practical? | honest? | อ้างอิง + URL |
|---|---|---|---|---|
| **MASK-OUT (ไม่นับ pixel)** ⭐ | จับ glare → ตั้งเป็น invalid → คำนวณดัชนีเฉพาะ valid pixel + รายงานสัดส่วน masked | ✅ เบาที่สุด | ✅ **สูงสุด** — ไม่สร้างค่าปลอม, ไม่ทับ phenotype | (แนวปฏิบัติ; สอดคล้อง feature-masking [9]) |
| **Classical inpainting (exemplar/Telea/NS)** | เดาค่า pixel จากพื้นที่ข้างเคียง | ✅ OpenCV `cv2.inpaint` เบา | ⚠️ ปลอมค่า — ใช้ได้แค่ visualization, ห้ามนำไปคิดดัชนี | [Nie et al. 2023 (exemplar inpaint)](https://consensus.app/papers/details/d5c28e5a49905ece82ca2578405770cd/?utm_source=claude_code) [8] |
| **DRM diffuse-specular separation** | แยกองค์ประกอบ specular ออก เหลือ diffuse | ⚠️ single-image ทำได้แต่หนัก/เปราะ | ⚠️ ดีกว่า inpaint เชิงทฤษฎี แต่ saturated region ยังต้องเดา | [Yamamoto et al. 2021](https://consensus.app/papers/details/20b01e68cd9c526b8ef9e647b60b74e4/?utm_source=claude_code) [11] · [Kajiyama et al. 2023 WACV](https://consensus.app/papers/details/f20ef9c20184506d9a47792a32b78c32/?utm_source=claude_code) |
| **Deep highlight removal (Unet-Transformer / GAN)** | เครือข่าย map highlight→diffuse, hallucinate texture ใต้ glare | ❌ CPU ช้า, ต้อง paired dataset (PSD) | ❌ hallucinate texture = ปลอม phenotype โดยตรง | [Wu et al. 2022](https://consensus.app/papers/details/0d16fd3ecc6258f2aa3efa71be367d0c/?utm_source=claude_code) [5] · [Wu et al. 2021 PSD dataset](https://consensus.app/papers/details/f3a46ea147805738a668645a68be5924/?utm_source=claude_code) [6] · [Xu et al. 2022 attentive GAN](https://consensus.app/papers/details/2e95a0b18c955e159c0c65aa4af712fb/?utm_source=claude_code) [7] |
| **Single-image reflection removal (ภาพผ่านกระจก)** | แยก layer สะท้อนหน้ากระจก ออกจาก layer ฉากหลัง (ตรงเคส "ถ่ายผ่านขวดแก้ว") | ⚠️ deep ส่วนใหญ่; มี classical (dark channel prior) | ⚠️ คนละปัญหากับ specular บนใบ — แก้ "เงาสะท้อนบนผิวขวด" ไม่ใช่ "เงาบนใบ" | [Zhang et al. 2023 dark channel](https://consensus.app/papers/details/cc1ed24d7d5755fbabe7af84989b61ad/?utm_source=claude_code) [12] · [Amanlou et al. 2022 review](https://consensus.app/papers/details/fadd829c1a705f8099f7f359e41251b4/?utm_source=claude_code) [13] |

---

## คำแนะนำหลัก: MASK-OUT > INPAINT (และทำไม)

**ใช้ MASK-OUT เป็น default. Inpaint เฉพาะ visualization layer แยกต่างหากเท่านั้น.**

เหตุผลเชิง honest phenotype + hyperhydricity:

1. **เราวัดตัวเลข ไม่ใช่ทำภาพสวย.** downstream ของ VitroVision คือ %green area / vegetation index / health score. มีหลักฐานชัดว่า specular reflection ทำให้ SR/NDVI เพี้ยนและ chlorophyll inversion ผิด [1][2][3]. การ **inpaint = เติมค่า pixel ที่เครื่องเดาเอง** เข้าไปในตัวเลขที่จะเขียนในรายงาน → เป็น fabricated data เชิงสถิติ. การ **mask-out = บอกตรงๆ ว่า pixel นี้วัดไม่ได้** → denominator ลดลงแต่ทุกค่าที่เหลือเป็นค่าจริง.

2. **hyperhydricity เป็น phenotype เป้าหมาย ไม่ใช่ noise.** ใบ vitrified จะ translucent/glassy/ฉ่ำน้ำ → ผิวเปียกมันสะท้อนแสงมากผิดปกติ [9][14][15]. ถ้า "ลบ glare แบบ inpaint" เท่ากับ **กลบสัญญาณของโรคที่เราต้องตรวจจับ**. การ mask-out เก็บตำแหน่ง/ขนาด glare ไว้ใช้เป็น feature ได้ (เช่น `specular_fraction` ของพื้นที่ใบ) — ตรงกับงานที่ใช้ optical/spectral feature จำแนก HH ได้ (SVM acc ~85% เหนือ vegetation index 63%) [9].

3. **honest reporting ที่ป้องกันตอน defend (CSBI):** รายงานคู่กัน — "พื้นที่ใบที่วัด valid ได้ X% / ถูก mask เพราะ glare Y%". ถ้ากรรมการถามว่า "glare ทำผลเพี้ยนไหม" ตอบได้ด้วยตัวเลข ไม่ใช่ภาพที่ retouch แล้ว.

**Pipeline แนะนำ (CPU, OpenCV/PlantCV):**
```
1. แปลง BGR → HSV
2. glare_mask = (V > τ_v) AND (S < τ_s)   # adaptive τ ตาม brightness ของภาพ [4][8]
3. morphological close/dilate ขยาย mask เล็กน้อยกัน edge เงา
4. valid_green = green_segment AND (NOT glare_mask)
5. รายงาน: green_area = count(valid_green); glare_fraction = area(glare_mask ∩ leaf) / area(leaf)
6. (optional, visualization เท่านั้น) inpaint แยก layer ด้วย cv2.inpaint — ห้ามป้อนกลับเข้าขั้นคำนวณดัชนี
```

---

## ข้อควรระวัง

- **อย่าสับสน 2 ปัญหา:** (ก) specular highlight *บนผิวใบ* (dichromatic, แก้ด้วย HSV/DRM) vs (ข) reflection *บนผิวขวดแก้ว/หน้ากระจก* (single-image reflection removal [12][13]). VitroVision เจอทั้งคู่ — เงาบนใบ hyperhydric คือ (ก); แสงไฟสะท้อนบนผิวขวดโค้งคือ (ข). คนละ algorithm. ส่วนใหญ่ปัญหา hyperhydric = (ก).
- **threshold ไม่ universal:** τ_v, τ_s ต้อง calibrate ต่อ setup แสง/ขวด; ใช้ adaptive-by-brightness [8] ดีกว่า fix ค่าเดียว.
- **glare ขนาดใหญ่/อิ่มตัวเต็ม (V=255):** ข้อมูลใต้นั้น "หายจริง" — ไม่ว่า inpaint หรือ DL ก็เป็นการเดา; ยิ่งย้ำว่าควร mask-out + รายงาน ไม่ใช่แสร้งว่ากู้คืนได้.
- **DL highlight removal เสี่ยง domain gap:** dataset (PSD [6]) เป็นวัตถุทั่วไป ไม่ใช่ใบพืชผ่านขวดแก้ว — นำมาใช้ตรงๆ จะ generalize แย่ + hallucinate. ไม่คุ้มบน CPU.
- **เชิงกายภาพชนะเสมอเมื่อทำได้:** polarizer/diffuse (R4-A) ลด glare ที่ "ต้นทาง" ดีกว่าแก้ทีหลังด้วย software เสมอ — งาน vegetation index ที่ดีที่สุดใช้ **polarization (DoLP)** ลด specular [1][2]. Software R4-E = fallback เมื่อ optics ทำไม่ครบ.

---

## อ้างอิง (Consensus, มี URL)

[1] [Study on the influence of specular reflection on vegetation index and its elimination method](https://consensus.app/papers/details/386403b6b3dc59dfb3b79fc0d8e253a6/?utm_source=claude_code) (Zhang et al., 2025, Comput. Electron. Agric.)
[2] [A New Polarization-Based Vegetation Index to Improve the Accuracy of Vegetation Health Detection by Eliminating Specular Reflection](https://consensus.app/papers/details/6d13d6dbb771563898e49a86695a58a3/?utm_source=claude_code) (Li et al., 2022, IEEE TGRS)
[3] [A method to improve plant health monitoring accuracy by removing specular reflection](https://consensus.app/papers/details/67fa54f590665f40adf651917970ad1a/?utm_source=claude_code) (Li et al., 2022, ICMSP)
[4] [Generic and real-time detection of specular reflections in images](https://consensus.app/papers/details/22b7ef7480cc5fcba60ee297b981ff51/?utm_source=claude_code) (Morgand et al., 2015/VISAPP 2014)
[5] [Joint specular highlight detection and removal in single images via Unet-Transformer](https://consensus.app/papers/details/0d16fd3ecc6258f2aa3efa71be367d0c/?utm_source=claude_code) (Wu et al., 2022, Computational Visual Media)
[6] [Single-Image Specular Highlight Removal via Real-World Dataset Construction](https://consensus.app/papers/details/f3a46ea147805738a668645a68be5924/?utm_source=claude_code) (Wu et al., 2021, IEEE TMM)
[7] [Highlight Removal from A Single Grayscale Image Using Attentive GAN](https://consensus.app/papers/details/2e95a0b18c955e159c0c65aa4af712fb/?utm_source=claude_code) (Xu et al., 2022, Applied AI)
[8] [Specular Reflections Detection and Removal for Endoscopic Images Based on Brightness Classification](https://consensus.app/papers/details/d5c28e5a49905ece82ca2578405770cd/?utm_source=claude_code) (Nie et al., 2023, Sensors)
[9] [Towards automated detection of hyperhydricity in plant in vitro culture](https://consensus.app/papers/details/5a5eb58a215a52a9bdc3e5314635467b/?utm_source=claude_code) (Bethge et al., 2023, PCTOC)
[10] [Specular highlight removal of light field image combining dichromatic reflection with exemplar patch filling](https://consensus.app/papers/details/45d5664fa21350c5b618920e6dbce462/?utm_source=claude_code) (Feng et al., 2024, Optics and Lasers in Engineering)
[11] [General Improvement Method of Specular Component Separation Using High-Emphasis Filter and Similarity Function](https://consensus.app/papers/details/20b01e68cd9c526b8ef9e647b60b74e4/?utm_source=claude_code) (Yamamoto et al., 2021, ITE)
[12] [Single Image Reflection Removal Based on Dark Channel Sparsity Prior](https://consensus.app/papers/details/cc1ed24d7d5755fbabe7af84989b61ad/?utm_source=claude_code) (Zhang et al., 2023, IEEE TCSVT)
[13] [Single-Image Reflection Removal Using Deep Learning: A Systematic Review](https://consensus.app/papers/details/fadd829c1a705f8099f7f359e41251b4/?utm_source=claude_code) (Amanlou et al., 2022, IEEE Access)
[14] [Hyperhydricity in Plant Tissue Culture](https://consensus.app/papers/details/7ba487e729365e3bb751a4a7cb57b0e1/?utm_source=claude_code) (Polivanova et al., 2022, Plants)
[15] [Hiperidricidade: uma desordem metabólica](https://consensus.app/papers/details/9fe8c4e162ee5ad3a64080439447c3c0/?utm_source=claude_code) (Vasconcelos et al., 2012, Ciencia Rural)

---
*หมายเหตุ Consensus:* Create or connect a free Consensus account to return more than 3 results per search in Claude Code: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
