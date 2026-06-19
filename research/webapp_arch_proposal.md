# Web App Architecture Proposal — VitroVision
> วางแผนจาก 5 Consensus research agents · 2026-06-19
> ตอบคำถาม: คนยังใช้ web app ไหม / ตัดอะไร / เพิ่มอะไร / ทำ continuous ได้อย่างไร

## คำถาม 1: Web app ยังนิยมไหม?
ใช่ — papers ปี 2022–2026 ทุก paper เลือก web-based สำหรับ plant phenotyping
เหตุผล: cross-platform ทันที, no install, update ง่าย, democratize สำหรับ nonexpert

## คำถาม 2: ทำให้ทันสมัยกว่านี้
| ลำดับ | เปลี่ยน | ยาก | evidence |
|---|---|---|---|
| 1 | **PWA** (manifest.json + Service Worker) | ต่ำมาก | Kim 2022, Koysawat 2021 (-45% time) |
| 2 | **Module layout** 4 โมดูล | กลาง | IHUP 2024 (14 cit.) |
| 3 | **FastAPI** แยก ML endpoint | กลาง | Haitan 2025 |

## Architecture เป้าหมาย
```
Flask (UI, port 5001)    ← คงไว้, เป็น web UI + dashboard
FastAPI (ML, port 8000)  ← เพิ่มใหม่, serve inference endpoint
PWA layer                ← manifest.json + SW บน Flask เดิม

4 Modules:
  📷 Capture  — scan.html (ArUco + camera optimize)
  🔬 Analysis — batch_analyze, pseudo_labeler
  📊 Data     — DB viewer, expert scoring
  📈 Reports  — growth curves, 5-formula comparison
```

## ตัดออก
- Free-text input → dropdown/tap ทุกจุด
- หน้าที่ hit rate ต่ำ (ดู server log ก่อน)

## เพิ่ม (จาก LIMS literature)
- `subculture_passage` field ใน DB
- Media lot tracking (MS formulation batch)
- Rate-of-change alert แทน absolute threshold

## Design Patterns สำคัญ (UX evidence)
| pattern | paper | implement |
|---|---|---|
| Interaction point ไม่ตัด flow | Pohl 2024, Elfaramawy 2022 | Flag ขวดได้ขณะถ่าย |
| ลด keystrokes | Waloszek 2020, Myka 2019 | QR scan + EXIF timestamp |
| Tablet-first (feel like clipboard) | Cole 2006 (53 cit.) | Swipe per bottle |
| Linked view: timeline ↔ ภาพ | Cruz-García 2019 (DevX, 28 cit.) | Hover graph = ดูภาพ |
| Gap transparency | Belda 2020 (84 cit.) | ทึบ = จริง, ประ = interpolated |
| Rate of change alert | Zhou 2026 (PVR) | +X/วัน แทน threshold |
| Dynamic context ตาม role | Davronova 2025 | Scientist vs Supervisor view |

## Implementation Phases

### Phase A — สัปดาห์นี้ (low-hanging)
- [ ] เพิ่ม `manifest.json` + `sw.js` → installable PWA
- [ ] ลด free-text form fields → dropdown/tap
- [ ] เพิ่ม rate-of-change column ใน dashboard table

### Phase B — ก.ค.
- [ ] Module nav (Capture / Analysis / Data / Reports)
- [ ] Linked view: timeline + photo hover
- [ ] Flag button ใน scan.html ไม่ตัด flow
- [ ] `subculture_passage` field ใน DB

### Phase C — ส.ค.
- [ ] FastAPI endpoint (port 8000) สำหรับ ML inference
- [ ] Media lot tracking
- [ ] Role-based view (scientist vs supervisor)

## Open-source อ้างอิง
- **Leaf LIMS** (MIT + Docker) — adaptable สำหรับ TC workflow
- **GridScore** (Raubach 2022) — plant phenotyping PWA มี barcode + image tagging
- **PlantCV** — white balance correction pipeline

## Papers สำคัญ (cite ใน proposal ได้)
- Kim 2022: PWA + Transfer Learning + plant disease (offline CNN)
- Koysawat 2021: PWA crop field data -45.28% time
- Raubach 2022: GridScore plant phenotyping PWA (BMC Bioinformatics)
- Bethge 2023: Phenomenon — in vitro TC automated phenotyping (16 cit.)
- Barburiceanu 2021: hybrid DL+classical CV pipeline (101 cit.)
