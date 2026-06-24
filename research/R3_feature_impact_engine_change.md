# R3 — Feature Impact หลังเปลี่ยนเครื่องยนต์ (ค่าที่วัดต้องเปลี่ยนตามไหม?)

> **สร้าง:** 2026-06-20 · 5 Consensus sub-agents (R3-A…E) · ทุก cite มี URL จาก Consensus จริง
> **คำถามต้นทาง:** comment #7 — เปลี่ยน engine แล้วค่าที่วัดต้องเปลี่ยนตามไหม
> **คำตอบสั้น: เปลี่ยน — และเป็นผลกระทบ methodology หนักสุดในชุด research นี้**

---

## 🚨 ผลที่สำคัญที่สุด (กระทบ κ + การ pool data)

**เปลี่ยน segmenter → ค่า feature เลื่อนแบบ SYSTEMATIC (มีทิศทาง ไม่ใช่ noise สุ่ม)** [R3-A]
- หลักฐาน smoking gun: 18 วิธี segment ภาพชุดเดียวกัน → FVC error ต่างกัน **~8 เท่า** (NRMSE 5.1%→42.3%) [R3-A7 Jiang 2025]
- HSV จะ "กิน" พิกเซลพืชในเงา/หลัง glare หาย → green% ต่ำกว่าจริง; SAM จะ recover ส่วนนั้น → ค่าพุ่งขึ้น = **method effect ล้วน ไม่ใช่ต้นเปลี่ยน** [R3-A3]

**กฎเหล็ก 3 ข้อ (บังคับ):**
1. ❌ **ห้าม pool ข้อมูล HSV เก่า + SAM ใหม่ ตรงๆ** — distribution คนละแบบ → ML จับ batch effect ปลอมเป็น signal [R3-A4]
2. ✅ **เปลี่ยน engine = re-process ทั้ง dataset ด้วย engine เดียว** + **re-validate κ ใหม่บน mask จริง** — κ ที่ validate บน HSV ใช้ยืนยัน SAM ไม่ได้
3. ✅ ถ้าจำเป็นต้องรวม → paired re-segmentation บน calibration set → Bland-Altman (bias+LoA) ต่อ feature → linear correction เฉพาะถ้า bias เล็ก+คงที่ [R3-A5 ลด bias 23%]

> **เชื่อมโยง guardrail:** κ=0.6274 = smoke-test อยู่แล้ว → ต้องรัน validation ใหม่บน engine ใหม่อยู่แล้ว = ไม่เสียอะไรเพิ่ม แค่ต้องทำให้ถูกตั้งแต่แรก

---

## 🌱 Instance seg ปลดล็อก trait ใหม่ (R3-B) — พระเอกเชิง biology
trait ที่ whole-plant mask เดียว **คำนวณไม่ได้โดยหลักการ** เพราะ mask รวมไม่รู้ว่ามีกี่ใบ/กี่ยอด:

| Organ-level feature (ใหม่) | → map TC endpoint | priority |
|---|---|---|
| **shoot instance count** | = **shoot multiplication number (shoots/explant)** = primary endpoint มาตรฐาน micropropagation! | 🥇 Tier 1 |
| **leaf count** (per-leaf instance) | developmental/vigor proxy | 🥇 Tier 1 |
| **individual leaf area distribution + max/mean** | vigor + uniformity ของ culture | 🥇 Tier 1 |
| shoot length รายยอด | proliferation vigor | 🥈 Tier 2 |
| per-organ color (leaf/shoot ระดับ instance) | chlorosis/hyperhydricity รายองค์ประกอบ (whole mask เฉลี่ยกลบ) | 🥈 Tier 2 |

- precedent: YOLOv11-AreaNet วัด per-leaf area ต้นกล้า broccoli R²=0.983 + เห็น growth rate รายใบ [R3-B1]
- ⚠️ **gap:** ยังไม่มี paper ทำ shoot-count-by-instance-seg ในขวด TC โดยตรง = **novelty ของเรา** (เชื่อม R2 fine-tune 3-class)

---

## 📏 ArUco scale → absolute units (R3-C) — ยืนยัน Q6
**เปลี่ยนจาก % → หน่วยจริง (cm²/mm) เฉพาะ trait ที่มีหน่วย:**

| feature ปัจจุบัน | → เปลี่ยนเป็น | gain | evidence |
|---|---|---|---|
| projected leaf area (% frame) | **cm²/mm²** | gain สูงสุด, error 0.5–1cm, accuracy 97% | C2,C3 |
| plant/seedling height (px) | **mm/cm** | RMSE ~1cm, MAPE<3%, เทียบข้ามวันได้ | C5,C7,C8 |
| stem length, leaf size | **mm** | RMSE 0.24–0.27cm | C1,C7 |

- **ไม่ต้องเปลี่ยน:** ratio ไร้หน่วย (solidity, aspect ratio, % chlorosis, convex_hull_ratio) — scale-invariant อยู่แล้ว
- **validity gain หลัก:** ตัด camera-distance error (error หลักของ pixel-based) → cross-day/cross-สูตร comparable → defend ต่อ destructive ground-truth ได้ [C4,C5,C6]
- ⚠️ **caveat methods:** ArUco ต้อง coplanar กับ canopy — ต้นสูงขึ้นในขวด = parallax/height bias เล็กน้อย ต้อง note [C4,C5]

---

## 🎯 Mask quality sensitivity (R3-D) — feature ไหนเชื่อได้แค่ไหน
หลักฐานจาก radiomics (วัด feature reproducibility ข้าม segmenter อย่างเป็นระบบ):

**ลำดับความน่าเชื่อถือ:** ExG-ExR (interior) ≈ GLCM (fixed params) > area/solidity > convex hull > **perimeter (เปราะสุด)**

| feature | robustness | หมายเหตุ |
|---|---|---|
| color/greenness mean (ExG, ExG-ExR) | ✅ robust | ค่าเฉลี่ยทั้ง region; ใช้ ExG-ExR (zero threshold) แทน ExG+Otsu [D8] |
| GLCM texture | ✅ robust สุดข้าม segmenter (ICC สูงสุด [D1]) | **แต่** ต้อง fix discretization (absolute bin size) ไม่งั้นเลื่อนตาม ROI [D5,D6] |
| area, solidity | 🟡 ปานกลาง | รายงานพร้อม uncertainty |
| convex hull | 🟠 fragile | |
| **perimeter, shape descriptors** | 🔴 fragile สุด (ICC=0.27) | ผูก boundary ตรงๆ [D1,D2] |

**Preprocessing บังคับให้ feature เสถียรข้าม segmenter:**
1. **Mask erosion 2–5px** ก่อนคำนวณ → ตัด edge pixel กำกวม [D7 plant CV proven]
2. **คำนวณ color/texture บน interior เท่านั้น** (eroded mask) กัน background bleed
3. **Fix GLCM params** (ROI, pixel-offset, absolute gray-level discretization) [D5,D6]
4. **Stability test:** perturb mask/หลาย segmenter → วัด ICC → เก็บเฉพาะ feature ICC>0.9 [D3,D4 radiomics standard]

---

## ⏱️ Temporal normalization (R3-E) — บังคับ ไม่งั้น growth curve เพี้ยน
**ปัญหาแกน:** "พืชเขียวขึ้นจริง หรือแค่แสงเปลี่ยน?" [E1]

**สิ่งที่ต้องมี (ก่อนเปลี่ยน engine):**
1. ⚠️ **วาง color reference target ในทุกภาพ ทุกวัน** — และ **white/gray card อย่างเดียวไม่พอ!** ต้องมี **RGB patches** เพราะ endpoint = green channel [E3] → **อัปเดต Q10: WB plan ต้องเพิ่ม RGB color patch ไม่ใช่แค่ white card**
2. **per-image color correction** (linear/affine/quadratic) เทียบ reference ก่อนวัด green% — **PlantCV มี module พร้อมใช้** [E2]
3. **คงสเกล** (ระยะ, mm/px, มุม, พื้นหลัง) ผ่าน ArUco
4. 🚨 **CRITICAL:** สลับ engine → **re-process ทุกวันย้อนหลังด้วย engine+normalization version เดียวกัน** — อย่าผสมเส้นเดียว (ย้ำ R3-A)

**Temporal traits ที่ควร report (robust กว่า single-day):**
- สกัดจาก **Gompertz fit** ไม่ใช่ค่ารายวันดิบ: **asymptote (max coverage), relative growth rate, time-to-inflection, AUC** [E4,E6]
- growth rate จาก **first-order derivative ของ fitted curve** ไม่ใช่ผลต่างรายวัน (noisy) [E5]
- report fit quality (R², AIC, residual SD) ทุก jar + คำนึง autocorrelation/unequal variance [E4]
- เหตุผล robust: derived trait จาก smoothed curve ดูดซับ noise รายวัน (รวม residual lighting/seg noise) [E4]

---

## 📌 ACTION items จาก R3 (รอเคาะ — กระทบ methods หนัก)
1. 🚨 **เขียน re-validation protocol:** เปลี่ยน engine → re-process ทั้ง dataset + re-run κ/ICC ใหม่ (อย่า pool เก่า-ใหม่)
2. 🚨 **อัปเดต WB plan (Q10):** เพิ่ม **RGB color patch** ในเฟรม ไม่ใช่แค่ white card + ใช้ PlantCV color-correction ทุกภาพ
3. เพิ่ม organ-level features (shoot count→multiplication number, leaf count, leaf area dist) — เชื่อม R2 fine-tune
4. เปลี่ยน area→cm², height/stem→mm ผ่าน ArUco scale (Q6) + note coplanar caveat
5. เพิ่ม mask erosion + interior-only + fix GLCM discretization + feature stability test (ICC>0.9)
6. report Gompertz-derived traits (asymptote/RGR/inflection/AUC) ไม่ใช่ค่ารายวันดิบ
7. paired re-segmentation calibration set (HSV vs SAM) → Bland-Altman ก่อนตัดสินใจ pool

---

## 📚 Verified papers (key)
- Jiang 2025 — 18 seg methods, FVC error 8× — https://consensus.app/papers/details/ee3219f2853451f6a22030f62a98a958/
- Pasini 2023 — shape ICC=0.27 / GLCM robust สุด — https://consensus.app/papers/details/4e9d009440c05dfdb3799288e1cb6d85/
- Chopin 2018 — color checker ทุกภาพ ลด SD ข้ามวัน — https://consensus.app/papers/details/2125c6b5d648596a96ea9c4152c7da31/
- Berry 2018 — PlantCV color standardization — https://consensus.app/papers/details/49a47eac2e8c5837922198ba9fced429/
- Sunoj 2018 — gray-card อย่างเดียวไม่พอ ต้อง RGB patch — https://consensus.app/papers/details/379b4ba741f155fb973ab1cb976e1664/
- Tjørve 2017 — Unified Gompertz derived traits — https://consensus.app/papers/details/cd41380ae0955137a03a08e39e44218d/
- Zhang 2025 YOLOv11-AreaNet per-leaf area R²=0.983 — https://consensus.app/papers/details/80558ed0820d558480078463fce56d81/
- Masykur 2023/2024 ArUco leaf area cm² — https://consensus.app/papers/details/600e89db2e28534e9fea66c7615f923c/
(รายการเต็มอยู่ใน transcript sub-agents)
