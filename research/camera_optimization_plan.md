# Camera Optimization Plan — scan.html (C3)
> วางแผนจาก 5 Consensus research agents · 2026-06-19
> implement ใน `shelf_manager/templates/scan.html` + `vitro_vision/scanner.py`

## Evidence Summary (papers สำคัญ)

| feature | paper | นำมาใช้ |
|---|---|---|
| Laplacian variance sharpness | Pham 2024 (RF classifier, 95%) | JS Canvas convolution |
| Patch-based blur (lower = condensation) | Agent 5 synthesis | แบ่ง frame 3×3 วัดแยก |
| Color calibration 3×3 matrix | Sunoj 2018 (74 cit.) | `cv2.transform()` server-side |
| White reference card ทุกเฟรม | Berry 2018 (PlantCV), Chopin 2018 | Macbeth mini card ในเฟรม |
| CLAHE ลด glare | Jiang 2020 (318 cit.) | `cv2.createCLAHE(clipLimit=2.0, tile=(8,8))` |
| Torch = supplementary เท่านั้น | Sun 2025, Heinemeyer 2025 | auto-on แต่ + diffuser |
| Angle check DeviceOrientation | Liu 2021 | DeviceOrientationEvent |
| Metadata (bottle ID, timestamp, lighting) | Röckel 2022, Di 2025 | append ใน FormData |

## Implementation Plan

### 1. Laplacian Sharpness Gate (JS)
```javascript
// Patch-based: แบ่ง frame เป็น lower/mid/upper
// คำนวณ Laplacian variance แต่ละ patch
// pass เมื่อ lower_patch_score >= 80 (condensation zone)
// threshold กลาง: ~100-200 (calibrate กับขวดจริง)
// แสดง sharpness % แยกจาก clarity ArUco
```

### 2. Glare Detection (JS)
```javascript
// patch-based: scan 5x5 patches
// ถ้า luminance > 240 ใน patch area > 5% → glare warning
// overlay สีแดง semi-transparent บน patch ที่ glare
```

### 3. Torch Auto-On
```javascript
// ImageCapture API: torch constraint
// auto-on เมื่อ เปิด scanner, auto-off เมื่อ leave
// note: iOS Safari ไม่รองรับ torch ผ่าน browser
```

### 4. Grid Overlay
```javascript
// วาด 3×3 grid บน canvas overlay (rule of thirds)
// ช่วย frame ขวดให้อยู่ตรงกลาง
// toggle ได้จากปุ่ม
```

### 5. Orientation Check
```javascript
// DeviceOrientationEvent: beta (tilt front/back)
// เตือนถ้า beta > 15° (กล้องเอียงเกิน)
// แสดงไอคอนเตือนใน topbar
```

### 6. White Balance Lock
```javascript
// ImageCapture.getPhotoCapabilities() → whiteBalanceMode
// lock เมื่อเห็น white card (WB_CARD_CORNER)
// fallback: auto WB ปกติ
```

### 7. Metadata ใน FormData
```javascript
// เพิ่มใน scan_save POST:
// - device_orientation (beta, gamma)
// - torch_on (bool)
// - sharpness_score (Laplacian variance)
// - glare_detected (bool)
// - timestamp_iso (ไม่ใช้แค่ day_point)
```

## Server-side (scanner.py / phenotyper.py)
- รับ metadata ใหม่ใน `/api/scan_save`
- บันทึก sharpness + glare ลง DB (ใช้ audit trail ภายหลัง)
- apply CLAHE ก่อน ArUco detect (ลด false negative กรณีแสงน้อย)

## Priority
1. Laplacian patch-based gate (ต้องทำก่อน — กระทบ data quality ตรง)
2. Glare detection overlay
3. Grid overlay + orientation check
4. Torch auto-on
5. WB lock (รอ white card จาก rig จริง)
