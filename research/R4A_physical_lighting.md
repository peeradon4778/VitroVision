# R4-A — Physical Lighting & Glare Geometry สำหรับถ่ายภาพพืชในขวดแก้ว

> Sub-agent R4-A | VitroVision (YSC 2027 → ISEF CSBI)
> โจทย์: จัดแสงเชิงกายภาพเพื่อถ่ายภาพต้นพริก (Capsicum) เพาะเลี้ยงเนื้อเยื่อ **ผ่านขวดแยมแก้วใส 125 mL** ให้คม ไม่มี glare บน low-cost rig (Samsung S24 FE, ~18 cm, ไม่มี lightbox)
> ทุก citation มาจากผล Consensus จริง + URL กดได้ (กฎ citation เหล็ก)

---

## VERDICT รวม

1. **Cross-polarization (CP) คือคำตอบหลักของ glare** — มีหลักฐานทั้งใน plant imaging, biomedical และ "ทำเองด้วยมือถือ + polarizing sheet" ราคาถูก หลักการคือใส่ polarizer ที่ **แหล่งแสง** และ analyzer ที่ **เลนส์** ไขว้กัน 90° → specular reflection (ที่รักษา polarization) ถูกบล็อก ส่วนแสงที่กระเจิงจากเนื้อใบ (depolarized) ผ่านเข้ากล้องได้ [2][3][7][8][9]. งานที่ใกล้โจทย์ที่สุด: Azinović 2022 (CVPR) เปลี่ยน **flashlight มือถือให้เป็น polarized source + ติด polarizer บนกล้อง** [9] และ Bae 2020 (JAAD) ทำ cross-pol ด้วย smartphone ราคาถูก [8].

2. **แต่ CP มีต้นทุนที่ต้องจ่าย 2 อย่าง — ต้องระบุชัดในโครงงาน:**
   - **(a) Light budget:** polarizer ไขว้กัน 2 ชั้น = เสียแสง ~1.5–2 stops. ปัจจุบัน Pro mode ล็อก ISO50 + ไม่มี lightbox + แสง 17:00 → **CP จะทำให้ภาพมืดเกินไป (underexposure)**. ดังนั้น CP **บังคับ** ต้องมีแหล่งแสงสว่างที่ติด polarizer ได้ (เช่น LED panel / ใช้ flash มือถือ) ไม่สามารถ cross-polarize แสง ambient/หน้าต่างได้.
   - **(b) เป็นการเปลี่ยน protocol ไม่ใช่แค่ซื้อ accessory:** ต้องมีแหล่งแสงควบคุม (ตอนนี้ protocol ไม่มี). ถ้าจะทำ CP ต้องยอมรับว่าต้องเพิ่มไฟ + อาจต้องปลดล็อก/ปรับ exposure.

3. **Diffuse illumination (dome/softbox) = แนวที่สองที่ทำง่ายกว่า** ลด glare บนผิวโค้งได้โดยไม่เสียแสงเท่า CP. หลักฐานจาก machine vision การตรวจชิ้นงานผิวมันเงา: dome light ให้แสงสม่ำเสมอ ลด reflection [4][5] และการรวม dark/bright field เพิ่ม contrast จาก ~40% → >90% [6]. งาน plant phenotyping ก็ย้ำว่า "evenly distributed diffuse illumination" สำคัญ [10].

4. **CP แก้ glare ได้ แต่ไม่แก้ refraction distortion จากผิวขวดโค้ง** — เป็นคนละปัญหา. การหักเหแสงทำให้ภาพบิด แก้ด้วยวิธีถูกๆ ไม่ได้ (Tong 2023 CVPR แก้ด้วย neural rendering หนักเกินสำหรับนักเรียน [13]). **mitigation ราคาถูก:** ถ่ายผ่านส่วนที่แบนที่สุดของขวด / พิจารณาขวดผนังตรง (cylindrical แทน jar คอแคบ) / ตรึง ROI ให้อยู่กลางขวดเสมอ.

5. **มี precedent ตรงโจทย์มาก: "Phenomenon" (Bethge 2023, Plant Methods)** — ระบบ low-cost phenotyping ที่ถ่าย/วัดพืช in vitro **ผ่านขวดปิดผนึก (closed vessels) แบบ non-destructive** รักษา aseptic ได้ และ validate RGB segmentation ด้วย random forest ได้ correlation สูงมากกับ manual annotation [11]. นี่คือ analog ที่ใกล้ที่สุดและควรอ้างเป็น backbone.

**บรรทัดล่างสุด:** rig ที่แนะนำ = **Cross-pol (สไตล์ Azinović/Bae ทำเองด้วย polarizing film) + แหล่งแสง LED สว่างติด polarizer (จ่ายค่า light budget) + diffuser ให้แสงนุ่ม + white/color card ในเฟรม** โดย **named gap = geometric distortion จากผิวโค้ง** ยังแก้ถูกๆ ไม่ได้.

---

## ตารางหลักฐาน per-เทคนิค

| เทคนิค | ได้ผลแค่ไหน / สาระสำคัญ | บริบท | อ้างอิง + URL |
|---|---|---|---|
| **Cross-polarization (หลักการในพืช)** | Polarimetry แยกแสงสะท้อนผิวใบ (glare) ออกจากแสงกระเจิงในเนื้อใบได้ ลด error ของ vegetation index ลง 1 order of magnitude | maize field, hyperspectral (พิสูจน์ principle, ไม่ใช่ rig นักเรียน) | Krafft 2023, Plant Phenomics — https://consensus.app/papers/details/31e7bd33520c506a9c64a9b1ed78a7e7/ [1] |
| **Polarization บนใบพืช (single image)** | โมเดล polarization แยก diffuse vs specular บนผิวใบได้แม่นจากภาพ polarization ภาพเดียว | leaf normal estimation | Xue 2023, ISPRS J. — https://consensus.app/papers/details/8832f3fa5a0d5c33bb25bdabb4d52830/ [2] |
| **Cross-polarized illumination กับตัวอย่างพืช** | CP ให้ภาพ background-free, high-contrast ของโครงสร้างพืช (ราก/ท่อลำเลียง) ในระบบ lensless ราคาถูก | plant samples, lensless | Zhou 2020, Optics Express — https://consensus.app/papers/details/4be0a0fc54cd57e59aaa3b8fe4818978/ [3] |
| **CP ลด specular (biomedical, near-cross)** | ใช้ near-cross-polarization states ลด specular highlight โดย **ไม่ต้องลดความเข้มแสง** + คงคอนทราสต์ | tissue imaging (Mueller matrix) | Pardo 2025, Optics Express — https://consensus.app/papers/details/900909db70fe5aad83f412390e4f340b/ [7] |
| **CP filter DIY (ทำเอง ราคาถูก)** ⭐ | สอนทำ cross-pol filter จาก **polarizing sheet ตัดติด ring flash** หมุน 90° → ภาพ "devoid of any glare" บนผิวมันเงา (เล็บ) | DSLR + ring flash, สอน step-by-step | Goktay 2023, Skin Appendage Disord. — https://consensus.app/papers/details/df8997249e195f319a91b90d128327c4/ [8] |
| **Smartphone cross-pol** ⭐ | ทำ cross-pol ด้วย **มือถือ** ราคาถูก ลด glare ผิว ไม่ต้องใช้อุปกรณ์แพง | smartphone (ตรงกับ S24 FE) | Bae 2020, JAAD — https://consensus.app/papers/details/3688ad0e5c5151678b38e2100b956841/ [9] |
| **Polarized smartphone (flash→polarized source)** ⭐ | **เปลี่ยน flashlight มือถือเป็น polarized source + ติด polarization foil บนกล้อง** ถ่าย cross-pol & parallel-pol = blueprint setup ตรงโจทย์ | smartphone + polarization foil | Azinović 2022, CVPR — https://consensus.app/papers/details/e42ac88d614c5bb994af219ff4ff227b/ [10] |
| **CP เชิงปริมาณ (gain)** | crossed-polarization ปรับปรุง diffuse:specular ratio ได้ ~40 dB | LFI / optical imaging | Mowla 2018, Applied Optics — https://consensus.app/papers/details/bd8272394dc557f3ac1643e10b2a27e4/ [12] |
| **Dome light บนผิว specular** | dome light ให้ uniform illumination ตรวจ defect บนผิวมันเงา (อะลูมิเนียม) ได้ + YOLOv8 recall 84.7% | machine vision inspection | Nascimento 2025, Int. J. Adv. Manuf. Technol. — https://consensus.app/papers/details/894fb66659465d2081279b76deec2fbe/ [4] |
| **Diffuse + dark/bright field** | structured diffuse illumination เพิ่ม detection contrast บนผิว shiny (รวม **glass**) จาก ~40% → >90% | specular surface (metal/plastic/glass) | Forte 2016, Opt. Lasers Eng. — https://consensus.app/papers/details/9b92da6e8a3e5b1e92fe1b59c51213f0/ [5] |
| **Diffuse uniformity design** | freeform diffuse-reflection ให้ uniformity >56% เหนือ integrating sphere สำหรับ precision inspection | LED diffuse optics | Rao 2026, Photonics — https://consensus.app/papers/details/8e88025c6f4e5455b72a067911bdca0d/ [6] |
| **Diffuse จำเป็นใน plant phenotyping** | ย้ำความสำคัญของ "evenly distributed diffuse illumination"; LED ในตัวอาจบิด spectral response | hyperspectral QA pipeline | Detring 2024, Plant Methods — https://consensus.app/papers/details/2723b178ad73576da11eff524ac1d3a1/ [11] |
| **Low-cost rig in vitro ผ่านขวดปิด** ⭐⭐ | ระบบ "Phenomenon" ถ่าย/วัดพืช in vitro **ผ่าน closed vessel** รักษา aseptic, RGB+depth, segmentation correlation สูงมากกับ manual | plant in vitro culture (closest analog) | Bethge 2023, Plant Methods — https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/ [13] |
| **Low-cost RPi rig + PlantCV** | RPi + กล้องถูกๆ + PlantCV สกัด shape/area/height/**color** ได้ reproducible | DIY phenotyping | Tovar 2018, Appl. Plant Sci. — https://consensus.app/papers/details/e12d24fcec0150409333669162b8ff7a/ [14] |
| **Refraction ผ่านภาชนะใส (gap)** | reflection/refraction หลายชั้นที่ผิว glass ทำภาพบิด แก้ด้วย neural rendering (หนัก ไม่ใช่ของนักเรียน) | transparent container, CVPR | Tong 2023, CVPR — https://consensus.app/papers/details/26429b1289a758a9accc4b66a69e38d9/ [15] |
| **Color calibration (ColorChecker)** | calibration matrix 3×3 จาก color patches ทำภาพ homogeneous เทียบ phenology ข้ามวันได้ (RGB patches ก็พอ) | agriculture RGB | Sunoj 2018, ISPRS J. — https://consensus.app/papers/details/379b4ba741f155fb973ab1cb976e1664/ [16] |
| **Linearization + grey standard** | กล้อง consumer ภาพดิบใช้วัดเชิงปริมาณไม่ได้ ต้อง linearize + normalize ด้วย grey standard; รองรับวัตถุ shiny | consumer camera toolbox (ImageJ) | Troscianko 2015, Methods Ecol. Evol. — https://consensus.app/papers/details/2bfb97122d0b54398d9198bc2d63524b/ [17] |

⭐ = actionable/buildable โดยตรง | ⭐⭐ = analog ใกล้โจทย์ที่สุด

---

## RIG SPEC แนะนำ (actionable, ซื้อได้จริงด้วยงบนักเรียน)

### หลักการ: 3 ชั้นป้องกัน glare (ทำพร้อมกันได้)
```
[LED panel สว่าง] → [polarizing film ที่ไฟ] → [diffuser] → ขวดพริก ← [polarizing film บนเลนส์ S24 FE หมุน 90°]
                         (กำจัด glare)        (นุ่ม ลด hotspot)               (analyzer ตัด specular)
```

### ของที่ต้องซื้อ/ทำ (เรียงตาม priority)

| # | ของ | สเปก / ที่ทำ | ราคาประมาณ | อ้างอิงหลักการ |
|---|---|---|---|---|
| 1 | **Linear polarizing film (sheet)** | ฟิล์มโพลาไรซ์แผ่น (ขายเป็นแผ่น A4) ตัด 2 ชิ้น: ชิ้นนึงติดหน้าไฟ, ชิ้นนึงติดหน้าเลนส์มือถือ (คลิป/เทป) แล้วหมุนชิ้นเลนส์จนภาพมืดสุด = ไขว้ 90° | ~100–300 บาท/แผ่น | Goktay 2023 [8], Bae 2020 [9], Azinović 2022 [10] |
| 2 | **LED panel/แผงไฟ video สว่าง (ปรับความสว่างได้)** | ต้องสว่างพอชดเชย light budget ที่เสียไป ~2 stops จาก CP; เลือก high-CRI (≥90) WB คงที่ ~4000–5000K | ~300–800 บาท | จำเป็นเพราะ CP กิน 1.5–2 stops (ดู VERDICT 2a) |
| 3 | **Diffuser** | กระดาษไข / แผ่น diffusion / กล่องโฟม/กระดาษทำ light tent เล็กครอบขวด เจาะช่องเลนส์ | ~0–150 บาท (DIY) | dome/diffuse ลด specular [4][5][6][11] |
| 4 | **White/grey + color card ในเฟรม** | X-Rite ColorChecker (ถ้ามีงบ) หรือ grey card ราคาถูก + แผ่นขาว วางในเฟรมทุกภาพ → ใช้ normalize/ calibrate ข้ามวัน | ~150–1500 บาท | Sunoj 2018 [16], Troscianko 2015 [17] |
| 5 | **ขาตั้ง/jig ตรึงตำแหน่ง** | ขาตั้งมือถือ + จิ๊กวางขวด ตรึงระยะ 18 cm และมุมเดิมทุกวัน (reproducibility) | ~150–500 บาท | reproducible rig [13][14] |
| 6 | **(ทางเลือก) ขวดผนังตรง** | ถ้าทำได้ ใช้ขวด/vial ผนังตรง (cylindrical) แทน jar คอแคบ → ลด refraction distortion + ถ่ายผ่านส่วนแบน | — | mitigation gap refraction [15] |

### Workflow ถ่ายภาพ (protocol ที่ปรับ)
1. **ปิดไฟห้อง/แสง ambient ให้มากที่สุด** ใช้เฉพาะ LED panel ที่ติด polarizer (CP ใช้กับแสง ambient ไม่ได้)
2. ครอบ diffuser, วางขวดใน jig, ใส่ color card ในเฟรม
3. หมุน polarizer ที่เลนส์จนเห็น glare หายไป (ภาพมืดสุดของ specular) = cross state
4. ถ่าย Pro mode — **อาจต้องปลดล็อก ISO/shutter เล็กน้อย** เพื่อชดเชย light budget (อย่าฝืนล็อก ISO50 จนภาพดำ); ล็อก WB ตาม LED panel
5. (ทางเลือกขั้นสูง สไตล์ Azinović [10]) ถ่าย 2 เฟรม: cross-pol (ตัด glare) + parallel-pol → ลบกันได้ specular map ถ้าต้องวิเคราะห์ผิวใบ hyperhydric

---

## ข้อควรระวัง / Gaps

- **Light budget เป็นข้อจำกัดที่แท้จริงที่สุด:** CP 2 ชั้น กิน ~1.5–2 stops. ถ้ายังยืนยันล็อก ISO50 + ไม่เพิ่มไฟ → ภาพจะดำ/noise. ต้องเลือกอย่างใดอย่างหนึ่ง: เพิ่ม LED สว่าง **หรือ** ผ่อนล็อก exposure. นี่คือเส้นแบ่งระหว่าง rig ที่ใช้ได้จริง กับ rig ที่ได้ภาพดำ.
- **CP ≠ แก้ refraction:** กำจัด glare ได้ แต่ภาพยังบิดจากผิวโค้ง (named gap). วิธีถูกๆ ที่ทำได้คือเชิงกายภาพ (ถ่ายส่วนแบน / ขวดผนังตรง / ตรึง ROI) ไม่ใช่ algorithm. อย่าเคลม CP แก้ distortion ในรายงาน.
- **อย่าให้ paper "principle" รั่วเข้า rig spec:** Krafft 2023 [1] / Xue 2023 [2] / Pardo 2025 [7] เป็นระบบ hyperspectral/Mueller-matrix ราคาแพง — อ้างได้เฉพาะ **"polarization ใช้ได้ผลในการถ่ายพืช/เนื้อเยื่อ"** ห้ามอ้างว่าเป็น rig ที่นักเรียนสร้าง. ตัว buildable จริง = Goktay [8] + Bae [9] + Azinović [10] + Bethge [13].
- **Gap หลักฐานเชิง geometry เฉพาะ "ผิวขวดโค้ง vs dome/ring/axial":** หลักฐาน dome ส่วนใหญ่มาจาก machine vision ตรวจชิ้นงานโลหะ/พลาสติก [4][5][6] ไม่ใช่ขวดแก้วโค้งใส่พืชโดยตรง — ใช้ได้แบบ transfer-principle. คำตอบ defensible = diffuse + CP รวมกัน.
- **Color card บังคับสำหรับ green_coverage_pct:** primary endpoint อิง green channel ข้าม 28 วัน — ถ้าไม่ normalize ด้วย white/color card ในเฟรม ค่าจะ drift ตามแสง [16][17]. ข้อนี้ห้ามข้าม.
- **WB/exposure ของ LED:** Detring 2024 [11] เตือนว่า LED illumination บิด spectral response ที่บางช่วงคลื่นได้ → เลือก high-CRI และ calibrate ด้วย color card เสมอ.

---

### Reference list
[1] [Mitigating Illumination-, Leaf-, and View-Angle Dependencies in Hyperspectral Imaging Using Polarimetry](https://consensus.app/papers/details/31e7bd33520c506a9c64a9b1ed78a7e7/) (Krafft et al., 2023, Plant Phenomics)
[2] [Polarimetric monocular leaf normal estimation model for plant phenotyping](https://consensus.app/papers/details/8832f3fa5a0d5c33bb25bdabb4d52830/) (Xue et al., 2023, ISPRS J. Photogramm. Remote Sens.)
[3] [Lensless imaging of plant samples using the cross-polarized light](https://consensus.app/papers/details/4be0a0fc54cd57e59aaa3b8fe4818978/) (Zhou et al., 2020, Optics Express)
[4] [Automated optical system for quality inspection on reflective parts](https://consensus.app/papers/details/894fb66659465d2081279b76deec2fbe/) (Nascimento et al., 2025, Int. J. Adv. Manuf. Technol.)
[5] [Exploring combined dark and bright field illumination to improve the detection of defects on specular surfaces](https://consensus.app/papers/details/9b92da6e8a3e5b1e92fe1b59c51213f0/) (Forte et al., 2016, Opt. Lasers Eng.)
[6] [Design of a Combined-Freeform-Surface Diffuse-Reflection System for High-Uniformity, Compact LED Inspection Illumination](https://consensus.app/papers/details/8e88025c6f4e5455b72a067911bdca0d/) (Rao et al., 2026, Photonics)
[7] [Method for reducing specular reflections in Mueller matrix imaging](https://consensus.app/papers/details/900909db70fe5aad83f412390e4f340b/) (Pardo et al., 2025, Optics Express)
[8] [Cross-Polarized Photography of the Nail Unit: A Practical Way to Eliminate Specular Reflections on the Nail Plate](https://consensus.app/papers/details/df8997249e195f319a91b90d128327c4/) (Goktay et al., 2023, Skin Appendage Disorders)
[9] [Simple Cross-Polarized Photography Using a Smartphone](https://consensus.app/papers/details/3688ad0e5c5151678b38e2100b956841/) (Bae et al., 2020, J. Am. Acad. Dermatol.)
[10] [High-Res Facial Appearance Capture from Polarized Smartphone Images](https://consensus.app/papers/details/e42ac88d614c5bb994af219ff4ff227b/) (Azinović et al., 2022, CVPR)
[11] [Quality assurance of hyperspectral imaging systems for neural network supported plant phenotyping](https://consensus.app/papers/details/2723b178ad73576da11eff524ac1d3a1/) (Detring et al., 2024, Plant Methods)
[12] [Polarization-sensitive laser feedback interferometry for specular reflection removal](https://consensus.app/papers/details/bd8272394dc557f3ac1643e10b2a27e4/) (Mowla et al., 2018, Applied Optics)
[13] [Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture](https://consensus.app/papers/details/cc3472b7e6cf5326ae1be0abce40d674/) (Bethge et al., 2023, Plant Methods)
[14] [Raspberry Pi–powered imaging for plant phenotyping](https://consensus.app/papers/details/e12d24fcec0150409333669162b8ff7a/) (Tovar et al., 2018, Appl. Plant Sci.)
[15] [Seeing Through the Glass: Neural 3D Reconstruction of Object Inside a Transparent Container](https://consensus.app/papers/details/26429b1289a758a9accc4b66a69e38d9/) (Tong et al., 2023, CVPR)
[16] [Color calibration of digital images for agriculture and other applications](https://consensus.app/papers/details/379b4ba741f155fb973ab1cb976e1664/) (Sunoj et al., 2018, ISPRS J. Photogramm. Remote Sens.)
[17] [Image calibration and analysis toolbox – a free software suite for objectively measuring reflectance, colour and pattern](https://consensus.app/papers/details/2bfb97122d0b54398d9198bc2d63524b/) (Troscianko et al., 2015, Methods Ecol. Evol.)

> Create or connect a free Consensus account to return more than 3 results per search in Claude Code: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
