---
name: run-vitrovision
description: Run, start, build, test, screenshot, verify, launch, check, smoke VitroVision / VitroShelf web app and ML pipeline. Use when asked to run VitroVision, start VitroShelf, test the app, or check if it works.
---

# run-vitrovision

VitroVision is a Flask web app (VitroShelf, port 5001) + Python ML pipeline for monitoring in-vitro tissue culture bottles. The web app lives in `shelf_manager/`, ML modules in `vitro_vision/` and `src/`. The agent path uses `smoke.ps1` to start, test, and stop the server via HTTP.

## Prerequisites

- Conda env `ml` (Python 3.11) must exist with Flask, OpenCV, PyTorch, etc.
- Python path: `C:\Users\User\miniconda3\envs\ml\python.exe`
- No extra install needed — all deps in the `ml` conda env.

## Run (agent path)

The driver is `.claude/skills/run-vitrovision/smoke.ps1`. Run from the VitroVision root:

```powershell
# Full smoke test: start -> test 9 endpoints -> stop
.\.claude\skills\run-vitrovision\smoke.ps1

# Individual commands
.\.claude\skills\run-vitrovision\smoke.ps1 start   # launch server (waits up to 30s for ML ready)
.\.claude\skills\run-vitrovision\smoke.ps1 test    # hit all 9 endpoints, exit 1 on any failure
.\.claude\skills\run-vitrovision\smoke.ps1 stop    # kill server
```

**Verified output (2026-06-17):**
```
[start] PID 13416
[ready] ML modules loaded

=== Smoke Tests ===
  [OK]   ml_status (all ready)
  [OK]   dashboard /
  [OK]   scan page
  [OK]   glass page
  [OK]   train page
  [OK]   analytics page
  [OK]   growth_data API
  [OK]   glass_state API
  [OK]   al_query API

Result: 9 passed, 0 failed
[stop] killed PID 13416
```

**Endpoints covered by smoke tests:**

| Endpoint | Purpose |
|---|---|
| `GET /api/ml_status` | All ML modules ready flag |
| `GET /` | Dashboard (batch list + bottle counts) |
| `GET /scan` | ArUco scan + AI classify UI |
| `GET /glass` | Live Glass Mode monitoring |
| `GET /train` | Active Learning training UI |
| `GET /analytics` | Growth analytics charts |
| `GET /api/growth_data` | JSON growth metrics |
| `GET /api/glass_state` | Live Glass Mode state |
| `GET /api/al_query` | Active Learning queue |

## Run (human path)

Double-click `VitroVision.bat` in the project root — starts the server and opens `http://localhost:5001` in the default browser. Use Ctrl+C to stop.

Or manually:

```powershell
cd shelf_manager
& "C:\Users\User\miniconda3\envs\ml\python.exe" main.py
```

## Run Jupyter (ML pipeline)

```powershell
cd "C:\Users\User\OneDrive\Desktop\Projects\Other\VitroVision"
& "C:\Users\User\miniconda3\envs\ml\Scripts\jupyter.exe" lab --no-browser --port 8888
```

Notebooks are in `notebooks/`:
- `01_explore_data.ipynb` — dataset exploration
- `02_train.ipynb` — model training
- `03_growth_analysis.ipynb` — growth curve analysis
- `05_kfold_eval.ipynb` — cross-validation
- `06_gradcam.ipynb` — GradCAM visualization

## Quick API test (no driver)

```powershell
Invoke-WebRequest -Uri http://localhost:5001/api/ml_status -UseBasicParsing | Select-Object -ExpandProperty Content
```

## Gotchas

- **ML takes ~15-20s to load** — `smoke.ps1 start` waits up to 30s polling `/api/ml_status` for `ready: true`. The web routes respond immediately even before ML is ready, but scan/classify won't work until ready.
- **Port conflict** — if something else runs on 5001, the server silently fails. Check with `netstat -ano | findstr 5001`.
- **Google OAuth / Drive** — `drive_uploader.py` uses `oauth_token.json`. Uploading images to Google Drive may prompt OAuth if the token is expired. The rest of the app works without it.
- **ArUco** — `ARUCO_OK` flag in `/api/ml_status`. If false, scan page shows bottles but ArUco detection is disabled. Requires OpenCV with contrib modules.
- **Database** — `vitroshelf.db` is in `shelf_manager/`. Fresh installs return `"empty": true` from `/api/growth_data`. Run `_inject_mock.py` to populate test data.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `[warn] server may not be fully ready after 30s` | ML modules still loading; smoke tests usually still pass since Flask is serving. Wait another 10s and retry `test`. |
| `[FAIL] ml_status (all ready)` | Check `shelf_manager/error.txt` for import errors. Common: missing `cv2` contrib or `ultralytics`. |
| Port 5001 already in use | `Get-Process -Name python \| Stop-Process` or find the PID via `netstat -ano \| findstr 5001`. |
| `smoke.ps1 stop` says "no pid file" | Server was started outside the driver; kill manually: `Get-Process -Name python \| Stop-Process`. |
