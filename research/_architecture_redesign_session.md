# 🏗️ Architecture Redesign — Session State (2026-06-20)

> **ใบนี้คืออะไร:** เซฟ state ของ session redesign สถาปัตยกรรม — grill decisions + research R1–R5 progress
> **ทำไมมี:** session ยาว กัน token หมดแล้ว grill decisions (อยู่แค่ในแชต) หาย
> **resume ยังไง:** อ่านไฟล์นี้ + R1/R2/R3 files → ทำ R4, R5 ต่อ → แล้ว synthesize เป็น final architecture

---

## 🔒 GRILL DECISIONS (locked 2026-06-20) — 10 ข้อ

| # | Decision | ผล |
|---|---|---|
| Q1 | API-based phenotyping direction | ✅ **เป็น direction หลัก** แต่ R1 ปรับ: API ทำ **qualitative** (status/dev_stage/vigor-desc) / classical CV ทำ **quantitative** (เข้าสถิติ) — **รอ test ภาพ TC จริงยืนยัน model quality (action วันถ่าย day 0)** |
| Q2 | CLI scanner (`vitro_vision/scanner.py`) | ✅ **ตัดออก** (ไม่เคยเปิดใช้) |
| Q3 | Google Drive (`drive_uploader.py`) | ✅ **เก็บ backup-only** — degrade gracefully ไม่ block scan · **ต้อง test upload ก่อน batch 1** (ยังไม่ test ตั้งแต่ sync ล่าสุด) |
| Q4 | Glass detection (`/glass`,`/api/glass_stream`) | ✅ **ตัดออก** (ไม่ผูก hypothesis ไหน) |
| Q5 | Pro mode กล้อง | ✅ **manual ตั้งครั้งเดียวใน Samsung Camera** (WB~4000K/ISO50/SS1-100) → browser รับ stream ต่อ; web handle เฉพาะที่ browser ทำได้ (torch/sharpness/glare/grid) |
| Q6 | ArUco | ✅ **เพิ่ม scale reference → วัดเป็น cm จริง** (R3-C ยืนยัน area→cm², height→mm) |
| Q7 | L4 Classifier | ✅ **API-based, async call** (capture+phenotype local ก่อน → ส่ง API background → อัปเดต DB ทีหลัง; เน็ตช้าไม่ block) |
| Q8 | Segmentation role | ✅ **SAM = segment (local) / API = classify+vigor (cloud)** — R2-E ยืนยัน Gemini ออก box/point ไม่ออก mask |
| Q9 | 14 features split | ✅ **classical CV = quantitative stats / API = vigor + dev_stage** (R1 ยืนยัน: VLM quantitative reasoning อ่อน ห้ามออกเลข) |
| Q10 | WB correction | ✅ 2-layer (Pro mode + white card) ก่อน · ⚠️ **R3-E แก้: white card อย่างเดียวไม่พอ ต้องเพิ่ม RGB color patch** เพราะ endpoint=green channel → **R4 จะเจาะเรื่องนี้** |

**Parked:**
- Q11 — L7 stats framework → รอ research (R5) ก่อนเคาะ

---

## 📊 RESEARCH PROGRESS (5 R หัวข้อ × 5 sub-agents)

| R | หัวข้อ | สถานะ | ไฟล์ |
|---|---|---|---|
| R1 | Phenomics feature set | ✅ เสร็จ | `R1_phenomics_feature_audit.md` |
| R2 | Segmentation model lineup | ✅ เสร็จ | `R2_segmentation_lineup.md` |
| R3 | Feature impact หลังเปลี่ยน engine | ✅ เสร็จ | `R3_feature_impact_engine_change.md` |
| R4 | WB correction (Physical + Algorithmic) | ✅ เสร็จ (2026-06-21) | `R4_wb_lighting.md` (+R4A–E ไฟล์ลูก) |
| R5 | Validation stats framework (Q11) | ✅ เสร็จ (2026-06-21) | `R5_validation_stats.md` (+10 ไฟล์ลูก) |

---

## 🎯 RESEARCH KEY TAKEAWAYS (R1–R3)

**R1 (features):** hybrid ไม่ใช่ replace · เพิ่ม NGRDI🥇/CIVE/ExG-ExR/LBP · in-vitro gap: browning intensity+temporal, shoot multiplication rate · **VLM ห้ามออกเลข vigor** (PlantXpert 2026) · ⚠️ "Ranario 2025"+"Paci 2024" ใน memory **verify PubMed ก่อนใช้** เสี่ยง hallucinate

**R2 (segmentation):** **SAM2-tiny หนักเกิน → MobileSAM (CPU-capable)** · ❌ ห้าม everything-mode → ✅ **box-prompt (YOLOv8 box→SAM)** · chain ใหม่ 2 เฟส: GroundingDINO pre-annotation offline → YOLOv8n-seg production · **physical: polarizer+diffuse light** · fine-tune YOLOv8n-seg **3-class (leaf/shoot/stem)** ปลดล็อก counting · convergence: Bethge"Phenomenon"(ผ่านขวดปิดจริง) + Bao2025(zero-shot ชนะ supervised)

**R3 (feature impact):** 🚨 **เปลี่ยน segmenter = ค่าเลื่อน systematic (8× variance)** → ห้าม pool เก่า-ใหม่ + re-validate κ ใหม่ · instance seg ปลดล็อก **shoot count = shoots/explant (TC endpoint!)** · perimeter เปราะสุด(ICC=0.27) GLCM robust → mask erosion+interior-only+fix discretization+ICC>0.9 filter · ⚠️ **WB ต้องเพิ่ม RGB patch + PlantCV color-correction ทุกภาพ** · report Gompertz-derived traits ไม่ใช่ค่ารายวันดิบ

**R4 (WB/แสง/สี):** 2 ด่าน — physical (cross-pol+diffuse LED+6-patch target+ArUco) ก่อน / algo (mask glare→flat-field→CCM→seg→index) หลัง · physical ชนะ software เสมอ · **6-patch DIY (RGBWgK) ≈ ColorChecker 24** ไม่ต้องซื้อ X-Rite · **Linear/Affine CCM (3×3) ใน PlantCV** default / RPCC upgrade / ❌ห้าม plain polynomial · CCM มาก่อน index เสมอ · flat-field เสริม target (แก้ non-uniform ในเฟรมที่ target ทำไม่ได้) อย่า double-correct global color · **glare = MASK-OUT ไม่ inpaint** (honest + เก็บ specular_fraction เป็น HH feature) · ⚠️ cross-pol กิน 1.5–2 stops = เปลี่ยน rig/protocol ต้องเคาะ + เทสต์ day 0

---

## ▶️ NEXT (resume)
1. ~~**R4**~~ ✅ เสร็จ 2026-06-21 → `R4_wb_lighting.md`
2. ~~**R5**~~ ✅ เสร็จ 2026-06-21 → `R5_validation_stats.md` — Q11 ปลดล็อกแล้ว
3. ~~**Synthesize**~~ ✅ เสร็จ 2026-06-21 → `_architecture_v2_final.md` (22 implementation tasks, 3 priorities)
4. **Action วันถ่าย day 0:** test Drive upload · ตั้ง Pro mode · ถ่าย 5 ภาพ TC → `/api/analyze_vision` ดู Gemini output (ปลดล็อก Q1) · **+เทสต์ glare: ลอง cross-pol/diffuse ดูว่าต้องลงทุน rig แค่ไหน (ปลด R4 decision #1)**
