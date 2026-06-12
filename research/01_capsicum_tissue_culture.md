# 01 — Capsicum Tissue Culture: งานวิจัยอ้างอิงสำหรับ VitroVision

> แหล่งหลัก: Consensus AI (peer-reviewed papers). คัดเฉพาะที่ apply กับ VitroVision (CV phenotyping ของ *Capsicum annuum* in vitro) ได้จริง
> วันที่รวบรวม: 2026-06-11 | ใช้กับ: YSC 2027 (CSBI) → ISEF | โครงงาน VitroVision

---

## TL;DR (อ่าน 1 นาที)

1. **พริก (Capsicum) เป็นพืช recalcitrant อย่างชัดเจน** — งานวิจัย 50 ปีตอกย้ำว่า in vitro response ต่ำ, ไม่ reproducible ข้าม genotype, และมักได้ shoot ที่ผิดรูป (SAM deformation) [7]. นี่คือ "ความยาก" ที่ทำให้การ monitor ด้วย CV มีคุณค่า — เพราะต้องคัดแยก response ที่ดี/เสียจำนวนมาก
2. **Explant ที่นิยมและได้ผลดีสุด** = cotyledonary node และ cotyledon-with-petiole (มากกว่า cotyledon leaf เปล่าๆ); nodal segment จาก in vitro seedling ก็ใช้ได้ดีกับ multiple shoot [1][3][6][8]. ตัวเลขอ้างอิง: cotyledonary node ตอบสนอง ~80% ใน 11–12 วัน [1]
3. **ความแปรปรวนสูงมากระหว่าง genotype/species** — C. annuum ได้ ~1.44 shoot/explant แต่ C. chinense ได้เกือบ 0 ในเงื่อนไขเดียวกัน [2]. นี่ support การออกแบบงานเราที่วัด 100 ขวด × 5 สูตร MS (ต้องการ throughput สูงเพื่อเห็น variance)
4. **ปัญหาหลักที่ CV จับได้:** browning/phenolic (วัดด้วย `brown_coverage_pct`), hyperhydricity (จับด้วย texture/color), shoot ต่ำ (`shoot_count_cv`), media contamination/เปลี่ยนสี (`media_color_cv`) — ทั้งหมดมี literature รองรับว่าเป็นตัวชี้วัดความสำเร็จมาตรฐาน [9][10][12]
5. **Gap ที่งานเราเติม:** มีระบบ CV/sensor สำหรับ in vitro แล้ว (เช่น "Phenomenon" multi-sensor [14]) แต่ **ยังไม่มีใครทำ image-based phenotyping เฉพาะ Capsicum TC** ที่เชื่อม 7 phenotype กับ recalcitrance scoring — นี่คือ novelty ของ VitroVision
6. **RGB color → chlorophyll/vigor เป็นวิธี non-destructive ที่ validated แล้ว** (R² 0.67–0.90) [11][13][15] → รองรับ `green_coverage_pct`, `leaf_color_index`, `vigor_score` ของเราโดยตรง

---

## 1. Protocol มาตรฐานการเพาะเลี้ยงเนื้อเยื่อพริก

### Explant types — แบบไหนนิยม / ได้ผลดี
- **Cotyledonary node ดีกว่า cotyledonary leaf**: Nadim et al. (2024) พบ cotyledonary node ตอบสนอง 80% ใน 11–12 วัน และ root initiation สูงสุด 83.77% บน MS + 1 mg/L IBA; media shoot induction ที่ดีสุด = MS + 8 mg/L BAP + 0.02 mg/L NAA + 0.5 mg/L IAA [1].
- **Cotyledon with partial petiole** เป็น explant ที่เหมาะสุดในพริกผลเล็ก (small-fruited pepper), bud induction 44.4% บน MS + 9.12 µM Zeatin + 0.57 µM IAA, rooting 86.7% [6].
- **Multiple explant comparison** (Dabauza et al., 2001 — 62 citations, งาน classic): เทียบ cotyledon, leaf, cotyledonary node, shoot-tip, embryonic cotyledon/hypocotyl → embryonic cotyledon ให้ผลดีสุด (3.45 elongated shoot/explant ใน 'Agridulce') แต่ขึ้นกับ variety × explant type อย่างมาก [8].
- **Nodal segment จาก in vitro seedling** ใช้ได้ดีกับ multiple shoot ในพริก recalcitrant 10 cultivar: ได้ 8.9–15.3 shoot/explant เมื่อเติม BAP + IAA + **spermidine** [3].

### Media / PGR ที่ recurring ในงานพริก
- **Base:** MS (full หรือ half-strength), sucrose 3%
- **Cytokinin หลัก:** BAP 5–8 mg/L (บางงานใช้ Zeatin)
- **Auxin เสริม:** IAA 0.5 mg/L, NAA 0.02–0.5 mg/L
- **Rooting:** IBA 0.5–2 mg/L (+ NAA)
- **Additives ที่ช่วย recalcitrance:** CuSO₄ + AgNO₃ (copper+silver synergy เพิ่ม regeneration) [2]; spermidine (polyamine) [3]; phloroglucinol [12-analog]

> **Apply → VitroVision (Method/Intro):** อ้าง [1][6][8] เป็น baseline protocol ของพริกในส่วน Method เพื่ออธิบายว่าเราเลือก explant/สูตร MS ใด; ตัวเลข shoot/explant และ % response ใช้เป็น ground-truth comparison กับ `shoot_count_cv` ที่ CV วัดได้

---

## 2. ปัญหาที่พบบ่อยใน Capsicum TC (recalcitrance & disorders)

- **Recalcitrance เป็นปัญหาเชิงระบบ:** Pijeira-Fernández et al. (2024) review 50 ปี — response เป็น genotype-dependent สูง, มักได้โครงสร้างที่มี **SAM deformation** (shoot apical meristem ผิดรูป), protocol ที่มีอยู่ "inefficient และ little reproducible" ข้าม genotype [7]. → เหตุผลเชิงชีววิทยาที่ต้อง monitor จำนวนมาก
- **Shoot induction ต่ำ & แปรปรวน:** C. annuum 1.44 shoot/cotyledon, 0.28 shoot/hypocotyl; C. chinense ~0.08/0.00 (เกือบไม่ตอบสนอง) [2].
- **Rooting ยาก & acclimatization survival ผันผวน:** survival 40–86.7% ขึ้นกับ cultivar [3]; งานหลายชิ้นระบุว่า rooting/acclimatization เป็น bottleneck สุดท้ายที่ "ต้องปรับปรุง" [2].
- **Browning / phenolic oxidation:** เป็นปัญหารุนแรงในพืชหลายชนิด; วิธีคุม = presoak antioxidant (PVP, ascorbic acid 15–250 mg/L), เติม activated charcoal, เลี้ยงในที่มืด, subculture บ่อย [10]. → ตรงกับ `brown_coverage_pct`
- **Hyperhydricity:** physiological disorder ที่พบบ่อยสุดใน in vitro → จับได้ด้วย `texture_entropy` + `leaf_color_index` (ใบ glassy/translucent). **รายละเอียด biology + visual features + กลไก PGR เต็ม = source of truth ที่ `13_pgr_morphology.md` §4** [4][9]
- **Contamination (microbial/endophytic):** surface sterilization ไม่พอกัน endophyte; แก้ด้วย antibiotics (kanamycin 500 ppm) หรือ PPM™ 0.2%; การปนเปื้อนทำสูญเสียวัสดุและทำ media เปลี่ยนสี/ขุ่น [5][16]. → ตรงกับ `media_color_cv`

> **Apply → VitroVision (Intro/Discussion):** ใช้ [7] เป็น "เหตุผลหลัก" ว่าทำไม Capsicum TC ต้องการ automated monitoring; ใช้ [4][9][10] อธิบาย biological meaning ของ phenotype แต่ละตัวใน Discussion (เชื่อม CV metric ↔ physiological disorder)

---

## 3. ตัวชี้วัด (phenotype/response) — เทียบกับ 7 phenotype ของ VitroVision

| Response ในงานวิจัยพริก/TC | Paper | Phenotype ของเราที่ proxy ได้ |
|---|---|---|
| Shoot number / multiple shoot per explant | [1][2][3][8] | `shoot_count_cv` |
| Shoot length / elongation | [8][12] | (เสริมได้จาก green_coverage + height) |
| % regeneration response, response time (วัน) | [1][3] | `vigor_score` (composite) |
| Rooting % | [1][3][6] | (นอก scope CV ภาพบน — แต่ใช้เป็น downstream label) |
| Greener tissue = regeneration ดีกว่า | [2] | `green_coverage_pct`, `leaf_color_index` |
| Browning / phenolic | [10] | `brown_coverage_pct` |
| Hyperhydricity (glassy texture) | [4][9] | `texture_entropy` |
| Contamination / media discoloration | [5][16] | `media_color_cv` |
| Survival / acclimatization rate | [3] | downstream outcome label |

**ข้อสังเกตสำคัญ:** Martínez-López (2021) ระบุชัดว่า explant ที่ regenerate ดี = "greener tissue" [2] → **เป็น literature support โดยตรง** ว่า `green_coverage_pct` / `leaf_color_index` ของเราเป็น proxy ที่มีฐานทางชีววิทยา ไม่ใช่ feature ที่คิดขึ้นมาลอยๆ

> **Apply → VitroVision (Method/Results):** ตารางนี้คือ "phenotype validation map" — ใส่ใน Method เพื่อ justify ว่าแต่ละ CV feature ผูกกับ established response variable ตัวไหน; ตอน Results เทียบ correlation ของ feature เรา กับ manual count/score

---

## 4. Computer Vision / Image-based phenotyping ใน Tissue Culture (Gap Analysis)

- **มีระบบ multi-sensor สำหรับ in vitro แล้ว — "Phenomenon"** (Bethge et al., 2023): low-cost xyz-scanner วัด projected area, canopy height, media height/volume ผ่านขวดปิด (รักษา aseptic); RGB segmentation ด้วย random forest correlate กับ manual annotation สูงมาก [14]. → **คู่แข่ง/prior art ที่ใกล้สุด** แต่เป็น hardware-heavy, generic plant, ไม่เจาะ Capsicum/recalcitrance
- **Deep learning ใน plant phenotyping เป็น mainstream แล้ว** [11][13] — CNN สำหรับ classification/detection/segmentation ของ stress, development, quality. แต่ review เหล่านี้ **ไม่ครอบคลุม in vitro TC โดยเฉพาะ** → ช่องว่าง
- **ML สำหรับ optimize TC protocol มีแล้ว** (แต่ใช้ tabular data ไม่ใช่ภาพ): Cannabis (GRNN + GA, predict shoot growth) [17]; Aronia (XGBoost/RF, R²>0.95 ทำนาย shoot/root) [18]; wallflower (MLP-NSGAII) [19]. → งานเหล่านี้ใช้ input เป็นความเข้มข้น PGR/แสง **ไม่ใช่ภาพถ่ายขวด** — VitroVision เติมมิติ image-based เข้าไป
- **RGB color → chlorophyll/health เป็นวิธี non-destructive ที่ validated:** sorghum (RGB R²=0.67–0.88, fusion 0.90) [13]; quinoa/amaranth (RGB ดีกว่า SPAD) [15]; tomato (stacking ensemble R²=0.836) [11]. → **รากฐานวิธีการของ `green_coverage_pct`/`leaf_color_index`/`vigor_score`**

### Gap ที่ VitroVision เติม (เขียนใน Intro/Discussion ได้ตรงๆ)
1. **ไม่มี image-based CV phenotyping เฉพาะ Capsicum in vitro** — prior art เป็น generic plant ([14]) หรือ ex vitro leaf ([11][13][15])
2. **ไม่มีใครเชื่อม CV feature กับ recalcitrance scoring** ของ Capsicum โดยเฉพาะ — ทั้งที่ recalcitrance คือปัญหาที่นิยามไว้ชัด [7]
3. **ระบบที่มี ([14]) เน้น growth metric (area/height)** ไม่จับ disorder (browning/hyperhydricity/contamination) ที่เป็นจุดตายของ Capsicum TC — 7 phenotype ของเราครอบคลุมทั้ง growth + disorder
4. **เป็น low-cost, image-only** (ถ่ายผ่านขวด) ไม่ต้อง scanner หรือ hyperspectral → reproducible ในห้องเรียน/ห้องวิจัยเล็ก

> **Apply → VitroVision (Intro novelty paragraph + Related Work):** ใช้ [14] เป็น closest prior art ที่ต้อง cite และ differentiate; [11][13][15] เป็น methodological foundation; [17][18][19] เป็นหลักฐานว่า "ML+TC เป็น direction ที่ชุมชนยอมรับแล้ว" แต่ยังเป็น tabular — เราต่อยอดเป็น image

---

## ตารางคัดกรอง: "Paper ไหน เอามาใช้กับงานเรายังไง"

| # | Paper (สั้น) | ใช้ตรงไหนใน VitroVision | Section |
|---|---|---|---|
| 1 | Nadim 2024 — cotyledon protocol, 80% response | baseline protocol พริก, ground-truth shoot/root % | Method/Intro |
| 2 | Martínez-López 2021 — recalcitrance, "greener=better" | justify green metric; species variance; Cu+Ag | Intro/Method/Discussion |
| 3 | Haque 2018 — 10 cultivar, nodal, spermidine | shoot/explant range, survival 40–87%, genotype variance | Method/Discussion |
| 4 | Sen 2013 — hyperhydricity phenolic/MDA | biological basis ของ texture_entropy + browning | Discussion |
| 5 | Kumari 2025 — endophyte/antibiotic | contamination → media_color_cv rationale | Discussion |
| 6 | Li 2024 — cotyledon+petiole, transcriptome | explant ที่ดีสุด small-fruited; bud/rooting % | Method |
| 7 | Pijeira-Fernández 2024 — recalcitrance review | **เหตุผลหลักของทั้งโครงงาน** (Intro hook) | Intro |
| 8 | Dabauza 2001 — explant comparison (classic) | เลือก explant; variety×explant interaction | Method |
| 9 | Polivanova 2022 — hyperhydricity review | นิยาม/สาเหตุ hyperhydricity, multifactor | Discussion |
| 10 | Amente 2021 — browning control review | brown_coverage_pct rationale + control methods | Discussion |
| 11 | Zhang 2025 — tomato RGB chlorophyll (stacking) | method foundation: RGB color feature → SPAD | Method |
| 13 | Zhang 2022 — sorghum RGB/hyperspectral fusion | RGB R² benchmark สำหรับ green/vigor metric | Method/Results |
| 14 | Bethge 2023 — "Phenomenon" in vitro multi-sensor | **closest prior art** (differentiate gap) | Related Work |
| 15 | Riccardi 2014 — quinoa RGB > SPAD | RGB non-destructive validated; ถูกกว่า SPAD | Method |
| 16 | Anikina 2025 — contamination control review | contamination loss, sterilization sensitivity | Discussion |
| 17 | Pepe 2021 — Cannabis ML (GRNN+GA) | prior art ML+TC (tabular) → เราต่อเป็น image | Related Work |
| 18 | Yaman 2025 — Aronia XGBoost R²>0.95 | ML ทำนาย shoot/root จาก condition; เราใช้ภาพ | Related Work |
| 19 | Fakhrzad 2022 — wallflower MLP-NSGAII | ANN model shoot/length/callus | Related Work |

*(Murphy 2024 — Deep Learning in Plant Phenotyping review — ใช้เป็น general DL framing; รวมในกลุ่ม [11]/[13] domain)*

---

## References

[1] [Development of In Vitro Regeneration Protocol for Sweet Pepper (Capsicum annuum L.) using Cotyledon as Explant](https://consensus.app/papers/details/3e2de8ef6ed052939014617cc97d1519/?utm_source=claude_code) (M. Nadim et al., 2024, J Bangladesh Agril Univ, 2 citations)

[2] [Screening of Suitable Plant Regeneration Protocols for Several Capsicum spp. through Direct Organogenesis](https://consensus.app/papers/details/d61b54c194a75d598fb47ee91e8d1dcf/?utm_source=claude_code) (Marina Martínez-López et al., 2021, Horticulturae, 11 citations)

[3] [An improved micropropagation protocol for the recalcitrant plant Capsicum – a study with ten cultivars of Capsicum spp.](https://consensus.app/papers/details/616ff501291a560c979c1d2ed72dacc1/?utm_source=claude_code) (Sk. Moquammel Haque et al., 2018, J Horticultural Science and Biotechnology, 13 citations)

[4] [Antioxidant enzyme activities, malondialdehyde, and total phenolic content of PEG-induced hyperhydric leaves in sugar beet tissue culture](https://consensus.app/papers/details/f0581af5bf345fd8969013f3b4dfafcd/?utm_source=claude_code) (A. Sen et al., 2013, In Vitro Cell Dev Biol-Plant, 67 citations)

[5] [Molecular identification and elimination of endophytic contamination using antibiotics from in vitro culture of Vitex peduncularis](https://consensus.app/papers/details/197c41d4c2a059ce8768f6d15d477abe/?utm_source=claude_code) (Runam Kumari et al., 2025, PCTOC, 2 citations)

[6] [Efficient In Vitro Regeneration System and Comparative Transcriptome Analysis ... Cotyledon with Partial Petiole in Small-Fruited Pepper (Capsicum annuum)](https://consensus.app/papers/details/4aa88f2330885ad2846eabd9e505909f/?utm_source=claude_code) (Xiaoqi Li et al., 2024, Int J Mol Sci, 4 citations)

[7] [Capsicum recalcitrance: physiological and molecular challenges of pepper tissue culture](https://consensus.app/papers/details/9148546138eb532ea79c0f839bfd670e/?utm_source=claude_code) (Gema Pijeira-Fernández et al., 2024, In Vitro Cell Dev Biol-Plant, 2 citations)

[8] [High Efficiency Organogenesis in Sweet Pepper (Capsicum annuum L.) Tissues from Different Seedling Explants](https://consensus.app/papers/details/1c95e7a9ab8b510dbfced77081413d78/?utm_source=claude_code) (M. Dabauza et al., 2001, Plant Growth Regulation, 62 citations)

[9] [Hyperhydricity in Plant Tissue Culture](https://consensus.app/papers/details/7ba487e729365e3bb751a4a7cb57b0e1/?utm_source=claude_code) (O. Polivanova et al., 2022, Plants, 102 citations)

[10] [Control of browning in plant tissue culture: A review](https://consensus.app/papers/details/4d0c72ef3ef7560bbd22f3b7f09aabfb/?utm_source=claude_code) (Gerema Amente et al., 2021, J Scientific Agriculture, 51 citations)

[11] [Study on the Detection of Chlorophyll Content in Tomato Leaves Based on RGB Images](https://consensus.app/papers/details/c6d02f21f7c053fc8298ada6dd1f6e6b/?utm_source=claude_code) (Xuehui Zhang et al., 2025, Horticulturae, 4 citations)

[12] [Deep Learning in Image-Based Plant Phenotyping](https://consensus.app/papers/details/a1ed382a0ebb5b1dadd0e8f2667a741c/?utm_source=claude_code) (Katherine M. Murphy et al., 2024, Annual Review of Plant Biology, 79 citations)

[13] [High throughput analysis of leaf chlorophyll content in sorghum using RGB, hyperspectral, and fluorescence imaging and sensor fusion](https://consensus.app/papers/details/e79f08a604b853fd8f0db8b2ee0c5ed0/?utm_source=claude_code) (Huichun Zhang et al., 2022, Plant Methods, 101 citations)

[14] [Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture](https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/?utm_source=claude_code) (Hans Bethge et al., 2023, Plant Methods, 15 citations)

[15] [Non-destructive evaluation of chlorophyll content in quinoa and amaranth leaves by simple and multiple regression analysis of RGB image components](https://consensus.app/papers/details/51cd213d8f0c56b3b9e2359ab0bb1e31/?utm_source=claude_code) (M. Riccardi et al., 2014, Photosynthesis Research, 111 citations)

[16] [Control of Contamination of Tissue Plant Cultures During in Vitro Clonal Micropropagation](https://consensus.app/papers/details/a04020b771b85faa81ff95d78a94bda0/?utm_source=claude_code) (Irina Anikina et al., 2025, OnLine J Biological Sciences, 2 citations)

[17] [Comparative Analysis of Machine Learning and Evolutionary Optimization Algorithms for Precision Micropropagation of Cannabis sativa](https://consensus.app/papers/details/9642653b6b6d5919802fdd62a47c62dc/?utm_source=claude_code) (Marco Pepe et al., 2021, Frontiers in Plant Science, 54 citations)

[18] [Integrating In Vitro Propagation and Machine Learning Modeling for Efficient Shoot and Root Development in Aronia melanocarpa](https://consensus.app/papers/details/1657e0a127b656c49ff287df03df8c5f/?utm_source=claude_code) (Mehmet Yaman et al., 2025, Horticulturae, 3 citations)

[19] [Mathematical modeling and optimizing the in vitro shoot proliferation of wallflower using MLP-NSGAII](https://consensus.app/papers/details/b5423cdd894f5c7cb9fcc94bef6cd2ec/?utm_source=claude_code) (Fazilat Fakhrzad et al., 2022, PLoS ONE, 18 citations)

> เพิ่มเติม: Micropropagation of Two Varieties of Bell pepper (Akther et al., 2020) — cotyledonary leaf, red variety 5.67 shoot/explant บน MS+BAP8+NAA0.02+IAA1: https://consensus.app/papers/details/92c4e6e4e78a55a8a444793368fd87a6/?utm_source=claude_code
> เพิ่มเติม: CNN for Image-Based High-Throughput Plant Phenotyping: A Review (Jiang et al., 2020, Plant Phenomics, 315 citations): https://consensus.app/papers/details/5a5b144e7d7d5c7891076fcdc15f6d52/?utm_source=claude_code

---

## Consensus message (verbatim)

> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
