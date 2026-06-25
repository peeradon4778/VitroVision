# VitroVision — Architecture V3: TEMPO

> **TEMPO** — **T**emporal-phenomics **E**ngine for **M**ulti-trait **P**rofiling in vitr**O**
> สร้าง: 2026-06-25 · อิงจาก V2 final (`_architecture_v2_final.md`) + Consensus gap analysis
> **กฎ:** V3 นี้ = research direction spec — ยังไม่ใช่ implementation order (ดู Phase plan ท้ายไฟล์)
> V2 ยังเป็น source of truth สำหรับโค้ดที่ implement แล้ว — V3 override เฉพาะ L4–L7

---

## 🔬 Research Positioning

### Gap ที่ TEMPO fill (จาก Consensus meta-analysis)

| Gap (Consensus 2024–2026) | Layer ที่ fill | Evidence |
|---|---|---|
| AutoML / foundation / zero-shot — **In vitro (1 paper)** | L4 | Bethge 2024: ทำได้แค่ fluorescence ไม่ใช่ RGB |
| Temporal Modeling — **GAP (0 papers in vitro)** | L5 | Yasrab 2021: Arabidopsis ex vitro เท่านั้น |
| Functional Integration — **In vitro (1 paper)** | L6 | Pasternak 2024: empirical เท่านั้น ไม่มี quantitative profile |
| Generalization / Benchmark Dataset — weak | L7 | ไม่มี in vitro TC benchmark dataset |

### Research claim ของ TEMPO
> *"TEMPO เป็น pipeline แรกที่รวม zero-shot foundation model segmentation (MobileSAM) + temporal sequence modeling (CNN-LSTM) + automated multi-trait phenotype profiling สำหรับ in vitro glass-vessel plant phenomics — ไม่ต้องใช้ pixel-level annotation, วัด growth trajectory, และแยก formula response ได้"*

---

## ⚡ CHANGE SUMMARY (V2 → V3 TEMPO)

| Layer | V2 | V3 TEMPO | เหตุผล |
|---|---|---|---|
| **L0** | Physical rig spec | **ตัดออก** — ไม่ใช่ software layer | ไม่เกี่ยวกับ ML pipeline |
| **L1** | Capture scan.html | **ไม่เปลี่ยน** (งานใหญ่ ไว้ทีหลัง) | — |
| **L2** | SQLite + Drive | **Supabase cloud** ✅ เสร็จแล้ว | migrate ไปแล้ว |
| **L3** | Color Correction | **ไม่เปลี่ยน** (CCM pipeline เดิม) | V2 ถูกแล้ว |
| **L4** | MobileSAM box-prompt | **MobileSAM zero-shot** (framing ใหม่) | fills foundation/zero-shot gap |
| **L5** | Feature Extraction (static) | **CNN-LSTM Temporal Sequence** | fills temporal gap — layer ใหม่ |
| **L6** | 3-class classifier + Gemini qual | **Phenotype Profiling Engine** | fills functional integration gap |
| **L7** | Stats validation (κ/ICC/ART) | **Multi-level Phenomics Validation** | upgraded: V1 trait + V2 formula discrim + V3 predictive |

---

## 🏗️ TEMPO — FULL ARCHITECTURE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L1 — DATA CAPTURE  [ไม่เปลี่ยน จาก V2]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  shelf_manager/templates/scan.html
  ArUco clarity gate ≥75% · Pro mode lock · 17:00 ทุกวัน
  FormData: bottle_id · day_point · dev_stage · hyperhydricity
  C3 gates (pending): Laplacian sharpness · glare · torch · grid

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L2 — STORAGE  [Supabase — ✅ done]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Supabase cloud (แทน SQLite)
  Tables: batches · bottles · images · expert_scores · phenotype_series
  phenotype_series: เพิ่มใหม่ใน V3
    (bottle_id, day_point, feature_vector JSON, mask_url, ts)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L3 — PREPROCESSING  [ไม่เปลี่ยน จาก V2]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ลำดับบังคับ (V2 ยังคงถูก):
    [1] Glare mask   → specular_fraction
    [2] Flat-field   → แก้ non-uniform illumination
    [3] CCM 3×3      → PlantCV affine color correction
    → เข้า L4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L4 — FOUNDATION SEGMENTATION  [V3 — fills Gap 1]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Research gap: AutoML/foundation/zero-shot × In vitro = 1 paper
  Bethge 2024: fluorescence เท่านั้น — RGB pipeline = novel

  Engine: MobileSAM (zero-shot, CPU-capable)
  ← SAM2-tiny หนักเกิน RAM 8GB (V2 Q2) → MobileSAM = foundation model
     ที่ยังนับเป็น SAM-family / zero-shot ได้

  Prompt strategy (สำคัญ — fills "in vitro glass vessel" gap):
    [1] ArUco crop: ตัด ROI จาก marker position
    [2] Adaptive box-prompt: ขยาย/หด box ตาม ArUco px size
    [3] Instance seg 3-class: leaf / shoot / stem
    [4] Fallback: HSV green threshold (ถ้า MobileSAM fail)

  Output: binary mask per class → เข้า L5 โดยตรง
  ⚠️ Bridge study ยังต้องทำ (T1): HSV vs MobileSAM Bland-Altman

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L5 — CNN-LSTM TEMPORAL SEQUENCE  [V3 NEW — fills Gap 2]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Research gap: Temporal Modeling × AutoML/foundation = GAP (0 papers)
  Yasrab 2021 (79 citations): ทำบน Arabidopsis ex vitro เท่านั้น

  Input: time-series feature vectors per bottle
    X = [f_day0, f_day1, ..., f_dayN]  shape: (N_days, n_features=16)

  Architecture:
    CNN encoder:  Conv1D layers → per-timestep spatial embeddings
    LSTM decoder: hidden state → temporal context per bottle
    Output head:  growth trajectory vector (ต่อ L6)

  Phase dependency: ต้องมีข้อมูล ≥7 day-points ก่อน train
    → Phase A (ตอนนี้): เก็บ phenotype_series ไว้ก่อน
    → Phase B (ก.ค.+): train CNN-LSTM เมื่อ batch 1 มี ≥7 days

  ⚠️ ก่อนใช้ temporal: ต้องมี consistent pipeline (bridge study ผ่าน)
     เพราะ feature vector ต้องมาจาก engine เดียวกันทุก day-point

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L6 — PHENOTYPE PROFILING ENGINE  [V3 — fills Gap 3]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Research gap: Functional Integration = 1–2 papers เท่านั้น
  Alsanie 2025: BAP เปลี่ยน phenotype วัดได้จริงในภาพ
  Pasternak 2024 (176 citations): data-driven TC model ยังใหม่

  เปลี่ยนจาก V2: ไม่ classify เป็น 3-class อีกต่อไป
  → Output = Phenotype Profile per bottle per timepoint

  Profile 1 — Growth Kinetics:
    Gompertz fit: K (asymptote), k (growth rate), tm (inflection day)
    Derived: AGRmax, AUC_28days, lag_period, early_vigor_index
    source: CNN-LSTM trajectory → fit NLS per bottle

  Profile 2 — Developmental Trajectory:
    stage_progression_velocity: วันที่ถึงแต่ละ stage
    stage_duration: จำนวนวันใน radicle/hypocotyl/cotyledon/true-leaf
    → ไม่ใช่แค่บอก stage ณ วันนั้น แต่บอก velocity ของ progression

  Profile 3 — Morphological Phenotype Vector:
    [green_coverage, NGRDI, ExG, VARI, LCI, brown_coverage,
     GLCM_contrast, GLCM_homogeneity, LBP, shoot_count,
     plant_area_cm², convex_hull_ratio, hyperhydricity_index,
     specular_fraction]
    → 14-dim vector ต่อ day-point (ดู L5 V2 feature set)

  Profile 4 — Formula Response Fingerprint:
    deviation_from_expected: Mahalanobis distance จาก formula-mean trajectory
    formula_cluster_membership: soft assignment A/B/C/D/E
    → ตอบ: "ขวดนี้ respond ตาม BAP5 expectation ไหม?"
    → evidence: Alsanie 2025, Grzegorczyk-Karolak 2021

  [Gemini VLM — คงไว้ qualitative เหมือน V2]
    vigor_description: string (ไม่ออกเลข)
    contamination_signs: string
    → feed เป็น metadata เสริม ไม่ใช่ primary output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  L7 — MULTI-LEVEL PHENOMICS VALIDATION  [V3 upgraded]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Research gap: Generalization + Benchmark dataset — weak evidence

  [V1] Trait Validity  (V2 มีอยู่แล้ว — คง)
    Spearman ρ: AI phenotype vector vs expert vigor score
    ICC(2,1): inter-rater human reliability ≥0.75
    QWK: vigor rubric ≥0.61
    Bland-Altman: bias + LoA (CV vs expert)
    → ตอบ: "AI วัด trait ตรงกับ expert ไหม?"

  [V2] Formula Discrimination Power  (V3 ใหม่)
    PERMANOVA บน phenotype profile vector (5 กลุ่ม A–E)
    ART-ANOVA: Gompertz parameters K/k/tm เทียบสูตร
    Effect size: ε²p (ไม่ใช่ η²)
    → ตอบ: "phenotype profile แยก A/B/C/D/E ออกได้ไหม?"
    fills: Generalization gap

  [V3] Predictive Validity  (V3 ใหม่ — fills temporal gap in validation)
    Input: day 3–7 features
    Predict: day 21 green_coverage + survival
    Metric: MAE, Spearman ρ (early vs late)
    Benchmark: Yasrab 2021 (Arabidopsis ex vitro) — baseline to beat
    → ตอบ: "เห็นปัญหาก่อนตาเห็นได้ไหม?"

  Threshold ทั้งหมด (ไม่เปลี่ยนจาก V2):
    ICC(2,1) human IRR ≥ 0.75
    QWK vigor ≥ 0.61
    Spearman CV vs expert ≥ 0.80
    [V3 เพิ่ม] Predictive ρ day3–7 vs day21 ≥ 0.70
```

---

## 📦 Data Contract (JSON Schema)

```json
{
  "bottle_id": "string",
  "formula": "A|B|C|D|E",
  "day_point": "integer",
  "timestamp": "ISO8601",

  "l4_masks": {
    "leaf_mask_url": "string",
    "shoot_mask_url": "string",
    "stem_mask_url": "string",
    "prompt_method": "mobilesam_box|hsv_fallback"
  },

  "l5_feature_vector": {
    "green_coverage_pct": "float",
    "ngrdi_mean": "float",
    "exg_mean": "float",
    "exr_mean": "float",
    "cive_mean": "float",
    "vari_mean": "float",
    "lci_mean": "float",
    "brown_coverage_pct": "float",
    "glcm_contrast": "float",
    "glcm_homogeneity": "float",
    "lbp_hist": "[float×10]",
    "shoot_count": "integer",
    "plant_area_cm2": "float",
    "convex_hull_ratio": "float",
    "hyperhydricity_index": "float",
    "specular_fraction": "float"
  },

  "l6_phenotype_profile": {
    "growth_kinetics": {
      "gompertz_K": "float",
      "gompertz_k": "float",
      "gompertz_tm": "float",
      "AGRmax": "float",
      "AUC_28days": "float",
      "lag_period_days": "float"
    },
    "developmental_trajectory": {
      "stage_current": "radicle|hypocotyl|cotyledon|true_leaf",
      "stage_velocity": "float",
      "days_to_cotyledon": "float|null"
    },
    "formula_response": {
      "deviation_from_expected": "float",
      "formula_cluster": "A|B|C|D|E",
      "cluster_confidence": "float"
    }
  },

  "l7_validation": {
    "spearman_rho_vs_expert": "float|null",
    "predictive_rho_early_late": "float|null"
  }
}
```

---

## 🚀 Implementation Phases

### Phase A — Foundation (ตอนนี้ — batch 1 day 0–28)
> เป้า: เก็บข้อมูลครบ + MobileSAM แทน HSV + สร้าง phenotype_series table

| Task | Layer | ความซับซ้อน |
|---|---|---|
| Bridge study: HSV vs MobileSAM Bland-Altman (T1) | L4 | M |
| สร้าง `phenotype_series` table ใน Supabase | L2 | S |
| เก็บ feature_vector ต่อ day-point (ทุกวัน) | L5 | S |
| Gompertz NLS fit per bottle (เมื่อมี ≥7 points) | L6 | M |

### Phase B — Temporal (ก.ค.+ เมื่อมีข้อมูล ≥7 days)
> เป้า: train CNN-LSTM + formula fingerprint

| Task | Layer | ความซับซ้อน |
|---|---|---|
| CNN-LSTM trainer + inference module | L5 | L |
| Formula Response Fingerprint (Mahalanobis) | L6 | M |
| Developmental trajectory velocity calculation | L6 | M |

### Phase C — Validation (ส.ค.–ต.ค.)
> เป้า: V1/V2/V3 validation ครบก่อนส่งรายงาน

| Task | Layer | ความซับซ้อน |
|---|---|---|
| PERMANOVA formula discrimination (V2) | L7 | M |
| Predictive validity day3–7 vs day21 (V3) | L7 | M |
| DINOv2 upgrade classifier (optional) | L6 | L |

---

## 📚 Citation Anchors

| Claim | Paper | DOI / URL |
|---|---|---|
| MobileSAM = foundation model zero-shot viable | Zhao 2025 | (verify PubMed ก่อนใช้) |
| SAM for label-efficient plant phenotyping | Zhang 2024 | (verify PubMed) |
| Automated in vitro phenotyping gap (fluorescence only) | Bethge 2024 | Consensus verified |
| CNN-LSTM temporal plant growth | Taghavi Namin 2018 | DOI: 10.1186/s13007-018-0333-4 · PMID 30087695 ✅ |
| Predictive growth deep learning baseline | Yasrab 2021 | Remote Sens. verified |
| BAP phenotype response quantifiable | Alsanie 2025 | BMC Plant Biology verified |
| TC data-driven models gap | Pasternak 2024 | Plants (176 citations) verified |

⚠️ ยืนยัน Zhao 2025 + Zhang 2024 + Namin 2017 ใน PubMed ก่อนใส่รายงาน
   (กฎ citation: ทุก cite ต้องผ่าน `_citation_audit.md`)

---

## 🔁 V2 → V3 ที่ยังใช้ได้เหมือนเดิม (ห้ามลบ)

- L1 Capture + scan.html ทั้งหมด
- L3 Color Correction pipeline (glare → flat-field → CCM)
- L5 Feature set 16 features (ใช้เป็น input ของ CNN-LSTM)
- L7 Module 1 inter-rater (ICC/QWK/Spearman/Bland-Altman)
- Stats: ART-ANOVA + ART-C + KM/CIF (V2 Module 3/4/5)
- Decision log Q1–Q11 ทั้งหมด

---

*สร้าง: 2026-06-25 | V3 TEMPO | อิง V2 final + Consensus gap analysis (Bethge 2024, Yasrab 2021, Alsanie 2025, Pasternak 2024)*
