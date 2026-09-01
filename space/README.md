---
title: VitroVision - Scan Plant
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
license: mit
suggested_hardware: cpu-basic
---

# VitroVision — Non-destructive scan of tissue-culture plants

A Gradio web app that uses the **camera (or an uploaded photo)** to segment a plant inside a
tissue-culture bottle and estimate its acclimatization readiness — **non-destructively**.

## 📱 How to use
- Click the camera button (📷) to **scan a plant in a bottle**, or upload an image.
- The app segments the plant (green) and returns measured traits: coverage, height proxy,
  plant regions, color health, glare/condensation, plus a readiness verdict (Ready / Not ready).

## 🧠 Model
- **Our model:** **U-Net + MobileNetV3-Small** (~3.6M params) — replaces SAM3 at the segmentation
  step of the pipeline. Trained on `Project-AgML/greenhouse_leafy_segmentation` (public greenhouse
  dataset, 1200 image/mask pairs). Weights are pulled from the HF model repo
  `peeradon4778/vitrovision-unet-small`.
- **Fallback:** while the trained model is not available, the app uses a **classical-green**
  segmentation so the demo is fully usable.

## ⚠️ Honesty / limits
- Trained on a **public greenhouse dataset** (human-annotated masks; not SAM3-pseudo, not our 100-bottle
  labels) → the 100-bottle set is used for **test/eval only**; it is a **prototype**, not yet a "production" grader.
- Displayed values use the **whole frame as ROI** (no separate bottle ROI) → **demo-scale numbers**,
  not yet calibrated to the 100-bottle validation set.
- Data: 1 species (bird's-eye chili / *Capsicum*) × 100 images → cross-species generalisation
  is not yet shown.

## 🔬 Project
[VitroVision](https://github.com/peeradon4778/VitroVision) — AI-based computer vision for analyzing
and predicting the growth of tissue-cultured plants (research project).

```
Author: Peeradon Duangthong (PCSHSBR)
```
