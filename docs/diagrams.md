# VitroVision — Architecture & Design Diagrams

> Publication-quality diagrams in Mermaid syntax.
> All labels in English per YSC publication requirement.
> Thai annotations in `%%` comments where design context is needed.

---

## 1. System Architecture Diagram

```mermaid
%% สถาปัตยกรรม cloud-primary: Android app → Roboflow SAM3 PCS API → on-device processing
graph TD
    subgraph Android["📱 Android App (On-Device)"]
        A["Camera Module<br/><small>Capture TC bottle photo</small>"]
        B["Image Preprocessor<br/><small>Resize → Base64 encode</small>"]
        C["Feature Extractor<br/><small>Coverage ratio · Height proxy<br/>Leaf count · Shoot count · Glare score</small>"]
        D["Decision Engine<br/><small>Rule-based triage<br/>3-class + confidence</small>"]
        E["UI Layer<br/><small>Result display · Manual override</small>"]
    end

    subgraph Cloud["☁️ Roboflow Cloud (API)"]
        F["SAM3 PCS Endpoint<br/><small>text_prompts: ['plant', 'leaf']</small>"]
        G["Zero-Shot Segmentation<br/><small>Mask generation</small>"]
    end

    A -->|"Capture"| B
    B -->|"POST /sam3/pcs<br/>image base64 + prompts"| F
    F --> G
    G -->|"JSON predictions<br/>masks · bbox · confidence"| C
    C -->|"FeatureMetrics"| D
    D -->|"TriageResult<br/>Wait / Subculture / Transplant-overdue"| E
    E -->|"Manual override"| D

    style A fill:#e3f2fd,stroke:#1565c0,color:#000
    style B fill:#e3f2fd,stroke:#1565c0,color:#000
    style C fill:#e8f5e9,stroke:#2e7d32,color:#000
    style D fill:#fff3e0,stroke:#e65100,color:#000
    style E fill:#f3e5f5,stroke:#6a1b9a,color:#000
    style F fill:#fce4ec,stroke:#c62828,color:#000
    style G fill:#fce4ec,stroke:#c62828,color:#000
```

**Data Flow Summary:**

| Step | Component | Direction | Payload |
|------|-----------|-----------|---------|
| 1 | Camera → Image Preprocessor | local | Raw JPEG/PNG |
| 2 | Image Preprocessor → SAM3 API | HTTP POST | Base64 image + `["plant","leaf"]` |
| 3 | SAM3 API → Feature Extractor | HTTP Response | JSON: predictions, masks (RLE), bbox, confidence |
| 4 | Feature Extractor → Decision Engine | in-memory | FeatureMetrics object |
| 5 | Decision Engine → UI | in-memory | TriageResult with decision class + confidence |

---

## 2. Pipeline / Flowchart

```mermaid
%% ขั้นตอนจาก capture → result สอดคล้องกับ orchestration.md
flowchart TD
    S1["📷 Capture Photo<br/><small>Android Camera API</small>"]
    S2["✂️ Resize + Base64 Encode<br/><small>Maintain aspect ratio</small>"]
    S3["🌐 POST to Roboflow SAM3 PCS<br/><small>text_prompts: ['plant', 'leaf']</small>"]
    S4["📦 Parse Predictions<br/><small>Masks · BBox · Confidence per instance</small>"]

    subgraph FE["Feature Extraction"]
        F1["coverage_ratio =<br/>area(mask) / area(ROI)"]
        F2["height_proxy =<br/>bbox_h(plant) / ROI_h"]
        F3["leaf_count =<br/>#instance with class='leaf'"]
        F4["shoot_count =<br/>#instance with class='plant'"]
        F5["glare_score =<br/>pixel HSV: V>0.95 & S<0.2"]
    end

    subgraph DE["Decision Engine (Rule-Based)"]
        D1["Apply subculture criteria<br/><small>days + coverage + shoot growth</small>"]
        D2["Compute confidence<br/><small>base * (1 - glare_score * 0.5)</small>"]
        D3["Apply glare penalty"]
    end

    S4 --> F1
    S4 --> F2
    S4 --> F3
    S4 --> F4
    S4 --> F5

    F1 & F2 & F3 & F4 & F5 --> D1
    D1 --> D2
    D2 --> D3

    D3 --> R1["📊 Display Result<br/><small>Mask overlay · Feature table · Decision badge</small>"]
    R1 --> R2["✋ Manual Override Option<br/><small>User can change decision</small>"]
    R2 --> R1

    style S1 fill:#e3f2fd,stroke:#1565c0,color:#000
    style S2 fill:#e3f2fd,stroke:#1565c0,color:#000
    style S3 fill:#fce4ec,stroke:#c62828,color:#000
    style S4 fill:#e8f5e9,stroke:#2e7d32,color:#000
    style FE fill:#e8f5e9,stroke:#2e7d32,color:#000,stroke-dasharray: 5 5
    style DE fill:#fff3e0,stroke:#e65100,color:#000,stroke-dasharray: 5 5
    style R1 fill:#f3e5f5,stroke:#6a1b9a,color:#000
    style R2 fill:#f3e5f5,stroke:#6a1b9a,color:#000
```

---

## 3. Decision Tree

```mermaid
%% ตรรกะ rule-based triage ตาม subculture_criteria.md
%% threshold เป็นค่าเริ่มต้น cross-species — รอ lab validate
flowchart TD
    START(["📥 Input: FeatureMetrics + days"]) --> Q1{"days < 21?"}

    Q1 -->|"Yes"| WAIT["WAIT<br/><small>Not enough time elapsed</small>"]

    Q1 -->|"No"| Q2{"coverage > 0.80<br/>OR<br/>days > 60?"}

    Q2 -->|"Yes"| OVERDUE1["TRANSPLANT-OVERDUE<br/><small>Overcrowding / time exceeded</small>"]

    Q2 -->|"No"| Q3{"shoot_count_growth < 1.2×<br/>AND<br/>days > 45?"}

    Q3 -->|"Yes"| OVERDUE2["TRANSPLANT-OVERDUE<br/><small>Stagnant growth + long duration</small>"]

    Q3 -->|"No"| Q4{"0.35 ≤ coverage ≤ 0.70<br/>AND<br/>21 ≤ days ≤ 45?"}

    Q4 -->|"Yes"| SUBCULTURE["SUBCULTURE<br/><small>Optimal window for transfer</small>"]

    Q4 -->|"No"| WAIT2["WAIT<br/><small>Outside productive band</small>"]

    WAIT --> CONF["⚙️ confidence = base × (1 − glare_score × 0.5)"]
    OVERDUE1 --> CONF
    OVERDUE2 --> CONF
    SUBCULTURE --> CONF
    WAIT2 --> CONF

    CONF --> FINAL(["📊 TriageResult + Manual Override"])

    style START fill:#e8f5e9,stroke:#2e7d32,color:#000
    style WAIT fill:#fff9c4,stroke:#f9a825,color:#000
    style WAIT2 fill:#fff9c4,stroke:#f9a825,color:#000
    style OVERDUE1 fill:#ffcdd2,stroke:#c62828,color:#000
    style OVERDUE2 fill:#ffcdd2,stroke:#c62828,color:#000
    style SUBCULTURE fill:#c8e6c9,stroke:#2e7d32,color:#000
    style CONF fill:#e0f7fa,stroke:#00838f,color:#000
    style FINAL fill:#f3e5f5,stroke:#6a1b9a,color:#000
```

### Decision Table

| Condition | Decision Class | Color |
|-----------|----------------|-------|
| days < 21 | WAIT | 🟡 Yellow |
| coverage > 0.80 OR days > 60 | TRANSPLANT-OVERDUE | 🔴 Red |
| shoot_count_growth < 1.2× AND days > 45 | TRANSPLANT-OVERDUE | 🔴 Red |
| 0.35 ≤ coverage ≤ 0.70 AND 21 ≤ days ≤ 45 | SUBCULTURE | 🟢 Green |
| Else | WAIT | 🟡 Yellow |

**Confidence Formula:**
```
confidence = base_confidence × (1 − glare_score × 0.5)
```
where `base_confidence` is the model confidence from SAM3 averaged across instances, and `glare_score` ∈ [0, 1] reduces confidence by up to 50%.

---

## 4. Wireframe UI (ASCII Mockup)

### Screen 1 — Main Screen

```
┌────────────────────────────────────┐
│  📱 VitroVision                     │  ← Status bar
│────────────────────────────────────│
│                                    │
│          ┌──────────────┐          │
│          │  VitroVision  │          │  ← App title
│          │   🌱 v2.0    │          │
│          └──────────────┘          │
│                                    │
│    Days since last subculture      │
│    ┌──────────────────────────┐    │
│    │  [  28  ]                │    │  ← Numeric input field
│    └──────────────────────────┘    │
│                                    │
│         ┌──────────────────┐       │
│         │    📸 ถ่ายภาพ     │       │  ← Primary CTA (Thai per UX)
│         └──────────────────┘       │
│                                    │
│    [ℹ] ถ่ายภาพขวดด้านข้าง         │
│        ระยะ 15-20 ซม.              │  ← Instruction text
│                                    │
│    ────── Recent Results ──────    │
│    │ 2026-07-05 → SUBCULTURE  │    │
│    │ 2026-06-28 → WAIT        │    │  ← History (collapsed)
│    └──────────────────────────┘    │
└────────────────────────────────────┘
```

### Screen 2 — Camera

```
┌────────────────────────────────────┐
│  ← Back        VitroVision         │
│────────────────────────────────────│
│                                    │
│    ┌──────────────────────────┐    │
│    │                          │    │
│    │   ┌────────────────┐   ░░░│   │
│    │   │  TC Bottle     │   ░░░│   │  ← Viewfinder with
│    │   │  (live feed)   │      │   │     guide overlay
│    │   │                │      │   │
│    │   └────────────────┘      │   │
│    │                  ░░░░░░░  │   │
│    └──────────────────────────┘    │
│                                    │
│         ┌──────────────────┐       │
│         │   ⭕ ถ่ายภาพ     │       │  ← Capture button
│         └──────────────────┘       │
│                                    │
│    [i] จัดให้ขวดอยู่ในกรอบ        │
├────────────────────────────────────┤
│  Confirm Capture?                  │
│  ┌──────────┐  ┌──────────┐       │  ← Confirm dialog
│  │  Retake  │  │   Use    │       │
│  └──────────┘  └──────────┘       │
└────────────────────────────────────┘
```

### Screen 3 — Result

```
┌────────────────────────────────────┐
│  ← Back        VitroVision         │
│────────────────────────────────────│
│  ┌───── Image with Mask Overlay ─┐ │
│  │                               │ │
│  │   ┌──────────────────┐        │ │
│  │   │  ▓▓▓▓▓▓▓▓░░░░░░  │        │ │  ← Plant mask (green)
│  │   │  ▓▓▓▓▓▓▓█████░  │        │ │     + glare (white)
│  │   │  ░░███████████   │        │ │
│  │   └──────────────────┘        │ │
│  │                               │ │
│  └───────────────────────────────┘ │
│                                    │
│  📊 Feature Values                 │
│  ┌──────────────────────────────┐  │
│  │ Coverage Ratio   0.52  ✅   │  │
│  │ Height Proxy     0.61  ✅   │  │  ← Feature table
│  │ Leaf Count       14    ✅   │  │
│  │ Shoot Count       3    ✅   │  │
│  │ Glare Score      0.08  ✅   │  │
│  └──────────────────────────────┘  │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  🟢 SUBCULTURE               │  │  ← Decision badge
│  │  Confidence: 87%             │  │     (green/yellow/red)
│  └──────────────────────────────┘  │
│                                    │
│  Manual Override:                  │
│  ┌──────────┐ ┌──────────┐ ┌───┐  │
│  │  WAIT    │ │SUBCULTURE│ │TO │  │  ← Override buttons
│  └──────────┘ └──────────┘ └───┘  │
│     [💾 Save Result]              │
└────────────────────────────────────┘
```

---

## 5. Feature Definition Diagram

```mermaid
%% แสดงความหมายทางเรขาคณิตของแต่ละ feature บนภาพขวด TC
block-beta
    columns 1
    block["ROI (Bottle Region)"]
        columns 1
        block["Plant Mask Region"]
            columns 2
            space
            block["Leaf instance 1"]
            end
            block["Leaf instance 2"]
            end
            space
            block["Shoot (plant) instance"]
            end
        end
    end

    space

    block:Legend["Legend"]
        columns 3
        L1["🟩 coverage_ratio<br/>= area(mask) / area(ROI)"]
        L2["📏 height_proxy<br/>= bbox_h / ROI_h"]
        L3["🍃 leaf_count<br/>= #leaf instances (conf≥0.5)"]
        L4["🌱 shoot_count<br/>= #plant instances"]
        L5["✨ glare_score<br/>= pixels with V>0.95 & S<0.2"]
    end
```

### Feature Definitions (from `_orchestration.md`)

| Feature | Formula | Unit | Range | Purpose |
|---------|---------|------|-------|---------|
| **coverage_ratio** | `area(plant ∪ leaf masks) / area(ROI)` | Ratio [0, 1] | 0–1 (typically 0–0.9) | Primary decision metric — correlates with explant density (Regni 2025) |
| **height_proxy** | `bbox_height(plant mask) / ROI_height` | Ratio [0, 1] | 0–1 | Secondary signal — height stagnation + high coverage = transplant-overdue |
| **leaf_count** | `# instances with class="leaf", conf ≥ 0.5` | Count | 0–N | Supplementary metric — no validated threshold yet |
| **shoot_count** | `# instances with class="plant"` | Count | 0–N | Used as **relative growth ratio** between subculture cycles |
| **glare_score** | `pixel fraction in ROI: V(HSV) > 0.95 & S < 0.2` | Ratio [0, 1] | 0–1 | Engineering safeguard — reduces confidence, never used for class decision |

**ROI Definition:** The bottle region extracted via fixed-distance capture (15–20 cm) or automated bottle detection. All ratio features are relative to ROI dimensions, making them capture-distance invariant.

---

## 6. Data Model Diagram

```mermaid
%% โมเดลข้อมูลตั้งแต่ request → response → feature → triage
classDiagram
    class RoboflowRequest {
        +String image_base64
        +List~String~ text_prompts
        +String model_id
        +int max_detections
        +float confidence_threshold
    }

    class RoboflowResponse {
        +List~Prediction~ predictions
        +String time_ms
        +String status
    }

    class Prediction {
        +String class_name
        +float confidence
        +BBox bbox
        +List~float~ points
        +String mask_rle
        +int mask_width
        +int mask_height
    }

    class BBox {
        +float x
        +float y
        +float width
        +float height
    }

    class FeatureMetrics {
        +float coverage_ratio
        +float height_proxy
        +int leaf_count
        +int shoot_count
        +float glare_score
        +int days_since_last_subculture
        +float avg_confidence
    }

    class TriageResult {
        +DecisionClass decision
        +float confidence
        +float glare_penalty
        +boolean manual_override
        +String override_reason
        +datetime timestamp
    }

    class DecisionClass {
        <<enumeration>>
        +WAIT
        +SUBCULTURE
        +TRANSPLANT_OVERDUE
    }

    RoboflowRequest --> RoboflowResponse : POST /sam3/pcs
    RoboflowResponse --> "*" Prediction : contains
    Prediction --> BBox : has
    Prediction --> FeatureMetrics : extracted from
    FeatureMetrics --> TriageResult : input for
    DecisionClass --> TriageResult : classifies

    %% หมายเหตุ: override_reason ใช้เก็บคำอธิบายเมื่อ user เลือก override
```

### Serialization Example (JSON)

**Request:**
```json
{
  "image_base64": "/9j/4AAQSkZJRg...",
  "text_prompts": ["plant", "leaf"],
  "model_id": "sam3-pcs",
  "max_detections": 50,
  "confidence_threshold": 0.3
}
```

**Response (abbreviated):**
```json
{
  "predictions": [
    {
      "class_name": "plant",
      "confidence": 0.89,
      "bbox": { "x": 120, "y": 80, "width": 200, "height": 300 },
      "mask_rle": "1;2;3;...",
      "mask_width": 640,
      "mask_height": 480
    },
    {
      "class_name": "leaf",
      "confidence": 0.76,
      "bbox": { "x": 180, "y": 150, "width": 60, "height": 80 },
      "mask_rle": "4;5;6;...",
      "mask_width": 640,
      "mask_height": 480
    }
  ],
  "time_ms": 2340,
  "status": "success"
}
```

**Triage Result (output):**
```json
{
  "decision": "SUBCULTURE",
  "confidence": 0.87,
  "glare_penalty": 0.13,
  "manual_override": false,
  "override_reason": null,
  "timestamp": "2026-07-06T14:30:00Z",
  "features": {
    "coverage_ratio": 0.52,
    "height_proxy": 0.61,
    "leaf_count": 14,
    "shoot_count": 3,
    "glare_score": 0.08,
    "days_since_last_subculture": 28,
    "avg_confidence": 0.92
  }
}
```

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-07-06 | v1.0 | Initial diagrams from Designer (Wave 1). Matches `_orchestration.md` v2026-07-06 and `subculture_criteria.md` thresholds. |
