# R4 — WB / แสง / สี (Physical + Algorithmic) — Synthesis

> **สร้าง:** 2026-06-21 · 5 Consensus sub-agents (R4-A…E) · ทุก cite มี URL จาก Consensus จริง
> **คำถามต้นทาง:** Q10 (grill) — white card อย่างเดียวไม่พอ เพราะ primary endpoint = green_coverage_pct (green channel) → ต้องวาง WB/สี/แสง ให้ valid ข้าม 28 วัน + ข้าม 5 สูตร
> **กฎ citation:** URL ด้านล่าง = Consensus page จริง — ก่อนเข้ารูปเล่ม resolve DOI + verify PubMed เฉพาะตัว load-bearing
> **ไฟล์ลูก (รายละเอียดเต็ม):** `R4A_physical_lighting.md` · `R4B_color_reference.md` · `R4C_color_calibration_algo.md` · `R4D_illumination_normalization.md` · `R4E_glare_removal_algo.md`

---

## 🎯 VERDICT รวม — "2 ด่าน × 3 ชั้น"

WB/สี ของ VitroVision ต้องคุมเป็น **pipeline 2 ด่าน** ไม่ใช่ขั้นเดียว:
- **ด่านกายภาพ (ก่อนกดชัตเตอร์):** cross-polarization + diffuse light + color target ในเฟรม → ตัด glare และให้ reference สีตั้งแต่ต้นทาง
- **ด่าน algorithm (หลังถ่าย):** mask glare → CCM color correction → flat-field → segmentation → vegetation index

**กฎทอง:** physical แก้ glare ชนะ software เสมอ (R4-A, R4-E ตรงกัน) → ลงทุน rig ก่อน แล้ว algorithm เป็น fallback/เสริม ไม่ใช่ตัวหลัก

---

## 🔧 R4-A — Physical Lighting & Glare (`R4A_physical_lighting.md`)
- **Cross-polarization** (polarizing film หน้าไฟ + หน้าเลนส์ ไขว้ 90°) = คำตอบหลักของ glare บนแก้ว/ใบเงา ทำเองด้วยมือถือได้ ~100–300 บาท/แผ่น
- ⚠️ **กระทบ protocol:** CP กินแสง ~1.5–2 stops → **ต้องเพิ่ม LED panel high-CRI + diffuser** ชดเชย (ISO50 + ambient เดิมจะได้ภาพมืด) → **นี่คือการเปลี่ยน rig จริง ต้องเคาะ** (ดู decision ค้างด้านล่าง)
- Diffuse/dome/light-tent = แนวที่สอง ทำง่ายกว่า CP
- **gap:** CP ไม่แก้ refraction distortion จากผิวขวดโค้ง (แก้ถูกๆ ไม่ได้) → เขียนเป็น limitation
- cite: Bae 2020 (smartphone cross-pol), Azinović 2022 CVPR, Bethge 2023 (ถ่ายพืช in vitro ผ่านขวดปิด — analog ใกล้สุด)

## 🎨 R4-B — Color Reference Target (`R4B_color_reference.md`)
- **แนะนำ DIY 6-patch:** White + Mid-gray(18%) + **R/G/B + Black** → เทียบเท่า ColorChecker 24-patch ไม่ต้องซื้อ X-Rite ($50+)
- white/neutral อย่างเดียว = correction แย่สุด → **ยืนยัน Q10/R3** ว่าต้องมี chromatic patch (เลือก green คร่อม hue ใบพริกจริง)
- วาง **ทุกภาพ** ใกล้ขวด เอียงเลี่ยงแสงสะท้อน อย่าโฟกัสคมจัด → per-image correction
- ⚠️ **DIY ต้อง characterize ค่าจริงที่พิมพ์** อย่าเชื่อค่าตั้งใจพิมพ์ (Cugmas 2025: ΔE 4.28)
- ⚠️ confound เฉพาะงาน: ฝ้า/หยดน้ำในขวด — color target แก้ไม่ได้ ต้อง defend เอง
- cite: Sunoj 2018 (RGB primaries ≈ 24-patch), Chopin 2018 (in-frame ลด SD ข้ามวัน), Cugmas 2025 (DIY reliability)

## 🧮 R4-C — Color Calibration Matrix (`R4C_color_calibration_algo.md`)
- **Default = Linear/Affine CCM (3×3)** (exposure-invariant + มีใน PlantCV) · **upgrade = Root-Polynomial (RPCC)** · ❌ **ห้าม plain Polynomial** (ขึ้นกับ exposure)
- **PlantCV workflow จริง:** ทางลัด `pcv.transform.auto_correct_color(rgb_img, color_chip_size="passport")` · manual = `detect_color_card` → `get_color_matrix` → `std_color_matrix` → `affine_color_correction(...)`
- **ลำดับ pipeline:** capture → linearize → **glare/shadow mask** → **CCM (ก่อนทุกอย่างที่ใช้ค่าสี)** → segmentation → index (ExG/NGRDI/VARI). CCM ต้องมาก่อน index เสมอ; full CCM subsume white-balance
- ตัวเลข: linear CCM ลด color error 67–77% (ΔE<2.3); polynomial >50%
- cite: Finlayson 2015 (RPCC), Berry 2018 (method ใน PlantCV), Kang 2025 (single-patch ไม่พอ)

## 💡 R4-D — Illumination Normalization (`R4D_illumination_normalization.md`)
- **Flat-field correction** (หาร flat frame ทำครั้งเดียว) = คุ้มสุด แก้แสงไม่สม่ำเสมอ "กลางเฟรม–ขอบ/เงาขวด" ที่ **color target แก้ไม่ได้**
- เสริมด้วย **Shades-of-Gray** · ❌ เลี่ยง White-Patch/Max-RGB (glare ขวดทำลายการประมาณขาว)
- **เสริม ไม่ซ้ำ color target** — แยก 3 แกน: (A) non-uniform ในเฟรม → flat-field เท่านั้นทำได้ · (B) global color cast → ซ้ำกับ target เลือกอันเดียว **อย่า double-correct** · (C) drift ข้ามวันแสงแปรปรวน → ต้องมีทั้งคู่
- ⚠️ **กับดัก Retinex:** ใช้ได้เฉพาะสาย measurement-preserving · **ห้ามใช้สาย perceptual/low-light-enhancement** บน measurement path (bias green_coverage ข้ามวัน)
- cite: Wang 2023 (ELM vs Retinex), Finlayson 2004 (Shades of Gray), Chopin 2018

## ✨ R4-E — Specular Highlight Removal (`R4E_glare_removal_algo.md`)
- **CPU-practical:** Detection ด้วย **HSV adaptive threshold** (V สูง + S ต่ำ) → ได้ glare mask · DL highlight removal หนัก/hallucinate texture → ไม่ใช้
- **MASK-OUT ชนะ inpaint** เชิง honest: (1) เราวัดตัวเลข — inpaint = เติม pixel ปลอมเข้ารายงาน · (2) **hyperhydricity = phenotype เป้าหมายที่ใบเงาวับ** — inpaint ทับ = ลบหลักฐาน → เก็บ `specular_fraction` เป็น feature เสริมบ่ง HH ได้ · inpaint ใช้แค่ visualization layer แยก
- ระวัง: แยก specular บนผิวใบ (HSV/DRM) ≠ reflection บนผิวขวดแก้ว (คนละ algorithm)
- cite: Bethge 2023 (auto-detect hyperhydricity, HH = optical feature, SVM 85%), Zhang 2025 (specular ทำ index เพี้ยน), Morgand 2014/15 (HSV real-time detection)

---

## 🔗 ลำดับ Pipeline สังเคราะห์ (เอาไป implement ได้เลย)
```
[ด่านกายภาพ]  cross-pol + diffuse LED + color target(6-patch) + ArUco ในเฟรม
      ↓ capture (S24 FE, Pro lock, ระยะ/มุมตรึง)
[ด่าน algo]   1. linearize (de-gamma)
              2. glare/specular MASK (HSV adaptive) → เก็บ specular_fraction
              3. flat-field correction (แก้ non-uniform ในเฟรม)
              4. CCM color correction จาก 6-patch (affine 3×3 หรือ RPCC) ← ทำ global color เพียงครั้งเดียว ห้ามซ้ำ Gray-World
              5. segmentation (HSV/SAM/YOLO) — ไม่นับ pixel ใน glare mask
              6. vegetation index (NGRDI/ExG/VARI) + green_coverage_pct
```
> ตัด double-correction: ใช้ **CCM จาก target** เป็นตัวคุม global color cast (แกน B) → **ไม่ต้อง** Gray-World/Shades-of-Gray ซ้ำ; flat-field ทำเฉพาะแกน A (non-uniform)

---

## ⚖️ Decision ที่ R4 งัดขึ้นมา (ต้องเคาะ — เพิ่มใน `_decisions_pending.md`)
1. 🔴 **ติด cross-polarizer + เพิ่ม LED ไหม?** — แก้ glare ดีสุด แต่ = เปลี่ยน rig + protocol แสง (ชน "ไม่ใช้ lightbox/ISO50") · ทางเลือก: (a) CP+LED เต็มสูบ (b) diffuse light-tent อย่างเดียว เบากว่า (c) พึ่ง algo mask-out อย่างเดียว — **ควรเทสต์วันถ่าย day 0 ก่อนเคาะ**
2. 🟡 **อัปเกรด white card → 6-patch DIY (R/G/B/W/gray/black)** — low-cost, evidence แข็ง, ทำได้เลย → น่าจะ "เอา" แทบไม่มี downside
3. 🟡 **เปลี่ยน `phenotyper._white_balance_correct()` (WB_CARD_CORNER) → PlantCV affine CCM** จาก 6-patch — แทนการ tune HSV มือ

## 🚨 จุดเชื่อมกับ research อื่น
- **R3-E (RGB patch)** → R4-B/C ยืนยัน + ทำให้เป็นรูปธรรม (6-patch + PlantCV affine)
- **R3-A (segmenter เปลี่ยน = systematic shift)** → CCM/flat-field ต้อง freeze ก่อน validate κ; เปลี่ยน WB pipeline ทีหลัง = ต้อง re-validate ใหม่เช่นกัน
- **R2-C (polarizer/glare physical)** → R4-A ขยายเป็น rig spec จริง
- **hyperhydricity** → R4-E `specular_fraction` เป็น feature bonus (เชื่อม endpoint ชีววิทยา)
