# Audit Report: VitroVision v2

**Auditor:** AI Auditor (Fable 5 = หัวหน้าออฟฟิศ)  
**Date:** 2026-07-06  
**Scope:** Research docs (orchestration, subculture_criteria, citation_gate, keywords) + Android app source code  

---

## 1. Orchestration Compliance

| Check | Result |
|---|---|
| ชื่อ TH/EN ระบุครบ | ✅ PASS |
| RQ ตรึง (snapshot → triage 3-class, zero-shot, decision-support) | ✅ PASS |
| Engineering goal (Native Android app) | ✅ PASS |
| SAM3 PCS text-prompted rule (ห้าม automatic/everything mode) | ✅ PASS |
| Feature definitions (coverage_ratio, height_proxy, leaf_count, shoot_count, glare_score) | ✅ PASS (มี gap — ดูด้านล่าง) |
| 4 "ต้องถามเจ้าของโครงการ" points documented | ✅ PASS |

### Issues

**MEDIUM — `shoot_count_baseline` missing from orchestration.md feature definitions**  
`FeatureMetrics.kt:10` defines `shoot_count_baseline: Int? = null` but orchestration.md (line 17-23) does not list this field. The DecisionEngine depends on it for the relative growth rule. Shadow feature missing from frozen spec.

**LOW — Feature name inconsistency**  
orchestration.md line 18 uses `coverage_ratio` but subculture_criteria.md line 41 uses `coverage_ratio` — consistent. However, subculture_criteria.md line 39 introduces `days_since_last_subculture` while code uses `days_since_subculture`. Minor naming mismatch but functionally the same.

---

## 2. Citation Verification (citation_gate.md vs subculture_criteria.md)

| Check | Result |
|---|---|
| All citations in subculture_criteria.md present in citation_gate.md | ✅ PASS |
| Uncited factual claims found | ✅ PASS (none) |
| Line-by-line scan for uncited claims | ✅ PASS |

### Details
- Murphy & Adelberg (2021) → citation_gate.md #7 ✅
- Muhammad et al. (2004) → citation_gate.md #18 ✅  
- Pastelín Solano et al. (2019) → citation_gate.md #15 ✅
- Regni et al. (2025) → citation_gate.md #16 ✅
- Barua et al. (2022) → citation_gate.md #17 ✅
- Abdalla (2022) → citation_gate.md #6 ✅
- Amanlou (2022) → citation_gate.md #19 ✅

### Flagged items from citation_gate.md

**MEDIUM — Thammasiri (2015) citation #3 verification flag**  
`citation_gate.md:29` — Resolved via WebSearch/WebFetch only, NOT found in Consensus. "$2.1 billion" figure may be in wrong currency unit (likely THB, not USD). **Do NOT use dollar figure in proposal until full-text verified.**

**LOW — Muhammad et al. (2004) metadata correction**  
`citation_gate.md:85` — Consensus shows wrong year (2020) and "Unknown Journal". Cross-verified via 3 independent sources. Correct citation is Muhammad et al. (2004) *Pakistan Journal of Botany* vol. 36. Flag noted correctly.

**LOW — Bethge et al. (2023) author list not fully reverified**  
`citation_gate.md:72` — Cross-session retrieval, author list needs full-text reconfirmation before use in bibliography.

---

## 3. Code Audit (Android App)

| Check | Result |
|---|---|
| SAM3 PCS text-prompted (not automatic mode) | ✅ PASS |
| DecisionEngine follows subculture_criteria.md rule logic | ⚠️ PARTIAL (see issues) |
| glare_score used only for confidence penalty | ✅ PASS |
| Manual override always available | ✅ PASS |
| UI texts in Thai | ✅ PASS |
| API key configurable via BuildConfig | ✅ PASS |

### Issues

#### HIGH — No ROI cropping; entire image treated as ROI
`FeatureExtractor.kt:13-69` — `coverage_ratio` computed as `coveragePixels / (bitmap.width * bitmap.height)`. But orchestration.md line 17 defines ROI as "บริเวณขวด (crop จากระยะถ่ายคงที่ หรือ detect)". The code uses the full image, meaning background (table, hands, etc.) inflates the denominator, **depressing coverage_ratio below true biological value**.  
**Recommendation**: Implement a bottle/ROI detector (or fix the camera-to-bottle distance so ROI ≈ image) before computing coverage ratio.

#### HIGH — Empty predictions silently returns "WAIT" instead of error state
`FeatureExtractor.kt:68-69` — When SAM3 returns zero predictions (no mask), `coverageRatio ≈ 0`, so DecisionEngine returns `WAIT` with 0.75 confidence. User sees "รอ" but the system never detected anything. The `strings.xml:11` defines `"ไม่พบต้นพืชในภาพ"` but **this string is never used anywhere in code**.  
**Recommendation**: After FeatureExtractor.extract(), check `predictions.isEmpty()` → show error state instead of decision.

#### MEDIUM — shoot_count has no confidence filter (inconsistent with leaf_count)
`FeatureExtractor.kt:54-59` — `leaf_count` uses `confidence >= 0.5` threshold (line 54) but `shoot_count` counts all "plant"/"shoot" predictions regardless of confidence (line 58). This inconsistency means low-confidence plant detections inflate shoot count.  
**Recommendation**: Apply the same `confidence >= 0.5` (or `>= thesis.0`) to shoot_count.

#### MEDIUM — Gap zone 0.70–0.80 coverage_ratio defaults to WAIT
`DecisionEngine.kt:31` — `coverage in 0.35f..0.70f` for SUBCULTURE. Coverage 0.75 (between 0.70–0.80) falls to `else → WAIT`. The design in subculture_criteria.md also has this gap (line 41: "subculture: 0.35-0.70 / transplant-overdue: > 0.80") but does not specify what to do in the buffer zone.  
**Recommendation**: Either (a) extend SUBCULTURE range to 0.35–0.80, or (b) make it SUBCULTURE with reduced confidence, or (c) explicitly document and show "grey zone" in UI.

#### MEDIUM — No unit tests for DecisionEngine or FeatureExtractor
Neither `DecisionEngine.kt` nor `FeatureExtractor.kt` has any tests. The threshold logic (21, 45, 60 days; 0.35, 0.70, 0.80 ratios) is entirely untested.  
**Recommendation**: Add JVM unit tests parametrized for each decision boundary.

#### MEDIUM — Unused string resource `no_predictions`
`strings.xml:11` defines `"ไม่พบต้นพืชในภาพ"` but no Activity or View references this string. Either the feature is incomplete or the string is dead code.

#### MEDIUM — Hardcoded Thai strings in XML layouts (not using @string)
- `activity_main.xml:32` — `android:text="ระบบคัดกรองความพร้อมตัดย้ายเนื้อเยื่อ"` (should be `@string/app_subtitle` or similar)
- `activity_camera.xml:20` — `android:text="ยกเลิก"` (should be `@string/cancel`)
- `activity_result.xml:37` — `android:text="ค่าที่วัดได้"` (should be `@string/feature_section_title`)  
**Recommendation**: Extract all hardcoded strings to `strings.xml` for maintainability and future localization.

#### LOW — `setupOverrideButtons()` called before `triageResult` is assigned
`ResultActivity.kt:47` — `setupOverrideButtons()` is called from `onCreate`, but `triageResult` is only assigned in `loadAndProcess()` -> `displayResult()`. If user taps an override button before processing completes, `triageResult?.confidence ?: 0f` passes 0.  
**Recommendation**: Disable override buttons until processing finishes, or guard with `triageResult != null` check.

#### LOW — Override button labels inconsistent with decision labels
`strings.xml:25` — `override_subculture = "ย้าย"` but `decision_subculture = "ย้ายได้"` (strings.xml:20). Similarly `ResultActivity.kt:131` uses `"ย้าย"` in override dialog vs `"ย้ายได้"` in main display. Minor UX inconsistency.

#### LOW — `parseDays()` called redundantly in `onClick` and `launchCamera()`
`MainActivity.kt:46` and `MainActivity.kt:75` — Both call `parseDays()`; the second call is redundant and exposes a race condition (theoretical).

---

## 4. Language / Thai Compliance

| Check | Result |
|---|---|
| UI strings in Thai | ✅ PASS |
| Research/proposal prose in Thai | ✅ PASS |
| Diagrams to be in English (as specified) | ✅ Not yet created |
| Language level appropriate for YSC | ✅ PASS |

### Issues
None critical. One observation: the hardcoded strings mentioned in section 3 are all in Thai as required.

---

## 5. Gap Analysis

### 5.1 Decisions still needing project owner (4 points from orchestration.md)

| # | Question | Status |
|---|---|---|
| 1 | ภาพขวดจริงเพิ่ม (high-density / ชนิดพืชอื่น) | ❌ **ยังไม่ได้** — ไม่มีรูปตัวอย่างใน repo |
| 2 | เกณฑ์ subculture ต้องยืนยันกับคนแล็บจริง | ❌ **ยังไม่ได้** — subculture_criteria.md เป็น rough threshold ล้วนๆ |
| 3 | ยืนยัน target = YSC 2027 | ⚠️ **ไม่แน่ชัด** — citation_gate.md:143 ระบุว่า "ยังไม่พบปฏิทิน YSC 2027" |
| 4 | ทดสอบแอปจริงในแล็บด้วย Samsung S24 FE | ❌ **ยังไม่ได้** |

### 5.2 What is missing for complete deliverable

1. **Plant species identification** — ไม่ทราบชนิดพืชจริงที่แล็บมี → ไม่สามารถ calibrate threshold ได้
2. **Ground-truth dataset** — ไม่มี pair (ภาพ + manual measurement) แม้แต่ชุดเดียว
3. **Inter-rater reliability baseline** — ไม่มีข้อมูลว่าคนแล็บตัดสินตรงกันแค่ไหน
4. **Roboflow SAM3 PCS endpoint verification** — ไม่สามารถยืนยันจาก code ว่า Roboflow endpoint จริงๆ ใช้ SAM3 PCS หรือโมเดลอื่น
5. **Offline mode / error handling** — App ใช้ได้เฉพาะตอนมี internet ถ้า Roboflow API ล่ม = app ใช้ไม่ได้
6. **ROI detection** — ไม่มี bottle/ROI cropping
7. **YSC 2027 deadline confirmation** — ต้องไปเช็ค nstda.or.th ใกล้เวลาสมัคร

### 5.3 Risks identified

| Risk | Severity | Mitigation |
|---|---|---|
| Roboflow endpoint ≠ SAM3 PCS underneath | **HIGH** | Test with a known SAM3 PCS query; request API documentation from Roboflow |
| Refraction through glass distorts 2D metrics | **MEDIUM** | Compare coverage_ratio with manual measurement in spike test |
| No ground truth → thresholds are guesses | **HIGH** | Must collect lab data before finalizing thresholds |
| False negative when SAM3 detects nothing | **HIGH** | Add zero-prediction guard (code fix possible now) |
| Leaf count threshold unusable from literature | **MEDIUM** | Document as "secondary feature only" (already done) |
| YSC 2027 deadline unknown → scheduling risk | **MEDIUM** | Monitor nstda.or.th for new cycle announcement |

---

## 6. Final Verdict

### Summary
| Section | Verdict |
|---|---|
| 1. Orchestration Compliance | ✅ PASS with notes |
| 2. Citation Verification | ✅ PASS (flags documented in citation_gate.md) |
| 3. Code Audit | ⚠️ **CONDITIONAL PASS** — 2 HIGH issues found |
| 4. Language/Thai | ✅ PASS |
| 5. Gap Analysis | ❌ **3 out of 4 owner decisions pending** |

### รายการ "รอเจ้าของโครงการตัดสินใจ"

1. **ชนิดพืชจริงในแล็บคืออะไร?** → Researcher หา threshold ต่อไม่ได้จนกว่าจะรู้
2. **ส่งภาพขวดจริง** (high-density, multiple species) — เพื่อ calibrate coverage_ratio + ทดสอบ SAM3
3. **ทดสอบ Samsung S24 FE** ถ่ายในแล็บ — ตรวจ refraction/glare จริง
4. **ยืนยัน YSC 2027** + deadline จริง — citation_gate.md ระบุว่ายังไม่เจอปฏิทิน
5. **ตัดสินใจว่าจะใช้ citation style อะไร** (APA7 vs Vancouver-style ตามเทมเพลต YSC) — citation_gate.md:13

### สิ่งที่ต้องทำต่อ

**Priority 1 (HIGH — code fix):**
- แก้ `FeatureExtractor` ให้เช็ค `predictions.isEmpty()` → แสดง error state (ใช้ string ที่มีอยู่แล้ว)
- เพิ่ม ROI cropping หรือกำหนดสัดส่วน ROI ในภาพ

**Priority 2 (MEDIUM — code fix):**
- เพิ่ม confidence filter ให้ shoot_count เหมือน leaf_count
- ย้าย hardcoded strings ทั้งหมดไป `strings.xml`
- เพิ่ม unit tests สำหรับ DecisionEngine boundaries
- ปิด override buttons จนกว่าประมวลผลเสร็จ

**Priority 3 (Research — ก่อนเขียน proposal):**
- ยืนยัน citation Thammasiri (2015) ผ่าน Consensus หรือตัดออก
- verify Bethge et al. (2023) author list จาก full text
- เช็คปฏิทิน YSC 2027
- ตัดสินใจ citation style

**Priority 4 (Lab — ก่อน submit):**
- เก็บ ground truth (ภาพ + manual measurement) อย่างน้อย 1 รอบ subculture
- calibrate thresholds
- ทดสอบ Samsung S24 FE ในแล็บจริง
