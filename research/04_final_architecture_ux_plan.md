# VitroVision — แผน Final Architecture + UX/UI

> เอกสารแผน (ไม่ใช่การลงมือแก้โค้ด) สำหรับยกระดับ VitroVision ให้เป็นเวอร์ชัน Final
> ที่ **reproduce ใหม่ได้ง่าย, ใช้งานง่าย, สถาปัตยกรรม + UX/UI ระดับดีเยี่ยม**
> เป้าหมาย: YSC 2027 (CSBI) → ISEF
>
> ผู้จัดทำแผน: AI architect/UX review · วันที่: 2026-06-11
> ขอบเขต: นักเรียน ม.ปลาย ทำคนเดียว → แผนต้อง **realistic, ไม่ over-engineer**

---

## 0. สรุปผู้บริหาร (อ่านอันเดียวพอ)

VitroVision วันนี้ทำงาน **ได้จริงและฟีเจอร์ครบ** (classifier κ=0.627, phenotyper 7 ฟีเจอร์,
analytics, active learning, ArUco tracking) แต่โครงสร้างมีปัญหาที่จะทำให้ **กรรมการหรือคนอื่น
reproduce ยาก** และมี **ความเสี่ยงด้านความปลอดภัย** ที่ต้องแก้ก่อนเผยแพร่/นำเสนอ

3 ปัญหาที่ critical ที่สุด:
1. **Secret/credential อยู่บนดิสก์ในโฟลเดอร์โปรเจกต์** (`oauth_token.json`, `gdrive_key.json`,
   `oauth_client.json`, `vitroshelf.db`) — *ข่าวดี:* ถูก `.gitignore` แล้ว และ **ไม่อยู่ใน git history**
   (ตรวจแล้ว 0 ไฟล์ tracked) แต่ token ตัวจริงยังอยู่ในเครื่อง ถ้าซิป/แชร์โฟลเดอร์เมื่อไหร่หลุดทันที
2. **โค้ดซ้ำซ้อน 2 ชุด** — มี trainer 2 ไฟล์ และ Flask app 2 ตัว (port 5001 + 5002) ที่ drift กัน
3. **รันได้เฉพาะบนเครื่องตัวเอง** — hard-coded path (`C:\Users\User\miniconda3\...`),
   flat import (`import database`), ไม่มี `.env`, ไม่มี `environment.yml` lock

ทิศทางแก้: รวมโค้ดเป็น package เดียว, ย้าย config ไป `.env`, pin dependency,
ทำ CLI/Makefile รันคำสั่งเดียว, แล้วค่อย redesign UX. เริ่มที่ **P0 (security + reproducibility)** ก่อน

---

## 1. Reproducibility Audit

### 1.1 สรุปสภาพปัจจุบัน (จากการสำรวจจริง)

```
VitroVision/
├── vitro_vision/         ← ML package (CLI) — มี config.py ใช้ env var แล้ว ✅
│   ├── classifier.py  scanner.py  detector.py  api_client.py
│   ├── trainer.py (267 บรรทัด)  train_app.py (Flask port 5002) ⚠️ ซ้ำ
│   ├── transforms.py  growth_validator.py  batch_analyze.py  config.py
├── shelf_manager/        ← Flask "VitroShelf" (port 5001) — flat module ⚠️
│   ├── main.py (713 บรรทัด, 32 routes)  database.py (DB_PATH="vitroshelf.db") ⚠️
│   ├── trainer.py (394 บรรทัด) ⚠️ ซ้ำกับ vitro_vision/trainer.py
│   ├── inference.py  phenotyper.py  drive_uploader.py  auth_google.py
│   ├── templates/ (8 ไฟล์ Jinja2, Tailwind CDN, ไม่มี static/)
│   ├── oauth_token.json  gdrive_key.json  oauth_client.json  🔴 SECRET บนดิสก์
│   ├── cert.pem  key.pem  vitroshelf.db  🔴 บนดิสก์
│   └── al_config.json
├── notebooks/ (01–06)   models/  results/  wandb/
├── VitroVision.bat (hard-coded python path) ⚠️
├── requirements.txt (ใช้ >= ทั้งหมด ไม่ pin) ⚠️
└── _inject_mock.py  _migrate_db.py  reset.py  insert_test_images.py ... (สคริปต์เกลื่อน root)
```

### 1.2 ตารางปัญหา → วิธีแก้

| # | ปัญหา | ระดับ | หลักฐาน | วิธีแก้ |
|---|-------|-------|---------|---------|
| R1 | **Credential อยู่บนดิสก์** | 🔴 P0 | `oauth_token.json` มี refresh_token, `gdrive_key.json` service-account key อยู่ใน `shelf_manager/` | ย้ายออกนอก repo → `~/.vitrovision/secrets/` หรือชี้ผ่าน env var `GOOGLE_TOKEN_PATH`; เก็บ `*.example` แทน; **revoke + ออก token ใหม่** เพราะตัวเก่าเคยอยู่บนดิสก์ที่ sync OneDrive |
| R2 | git history สะอาดจริงไหม | 🟢 ตรวจแล้ว | `git ls-files \| grep secret` = 0; `git log -- oauth_token.json` = ว่าง | ไม่ต้อง rewrite history ✅ แค่ระวังอย่าให้หลุดในอนาคต |
| R3 | **OneDrive sync secret** | 🟠 P0 | repo อยู่ใน `OneDrive/Desktop/Projects/` → token sync ขึ้น cloud | ย้าย secret ออกนอก OneDrive (ดู R1) |
| R4 | **Hard-coded path** | 🟠 P1 | `VitroVision.bat:3` = `C:\Users\User\miniconda3\envs\ml\python.exe` | ใช้ `conda run -n ml python -m ...` หรือ resolve จาก env |
| R5 | **DB path relative กับ CWD** | 🟠 P1 | `database.py:5` `DB_PATH="vitroshelf.db"`, `drive_uploader.py:12` `TOKEN_FILE="oauth_token.json"` → รันได้เฉพาะตอน `cd shelf_manager` | ย้ายเป็น path จาก config/env, resolve absolute |
| R6 | **Flat import ไม่เป็น package** | 🟠 P1 | `main.py` `import database`, `import trainer` (ไม่มี `.`) | ทำเป็น package `from shelf_manager import ...` หรือรวมเข้า `vitro_vision` |
| R7 | **โค้ด trainer ซ้ำ 2 ชุด** | 🟠 P1 | `shelf_manager/trainer.py` (394) vs `vitro_vision/trainer.py` (267) docstring เดียวกัน drift กัน | รวมเป็นไฟล์เดียวใน package กลาง ทั้งสองฝั่ง import ตัวเดียว |
| R8 | **Flask app ซ้ำ 2 ตัว** | 🟡 P2 | `main.py` (5001) + `train_app.py` (5002) มี training UI ทั้งคู่ | ตัด `train_app.py` ทิ้ง (main.py มี `/train` อยู่แล้ว) |
| R9 | **Dependency ไม่ pin** | 🟠 P1 | `requirements.txt` ใช้ `>=` หมด → `numpy>=2.0`, `torch>=2.0` อาจได้คนละเวอร์ชัน | สร้าง `environment.yml` + `requirements.lock` (pin exact) จาก env `ml` ที่ใช้จริง |
| R10 | **ไม่มี global seed** | 🟡 P2 | มีแค่ `random_state=42` ใน split; ไม่มี `torch.manual_seed`/`np.random.seed`/`cudnn.deterministic` | เพิ่ม `set_seed(42)` รวมศูนย์ เรียกต้น train — สำคัญต่อการอ้าง κ=0.627 ซ้ำได้ |
| R11 | **Data ไม่ track** | 🟡 P2 | `data/raw` gitignore (ถูกต้อง) แต่ไม่มี manifest/checksum ว่าใช้ภาพชุดไหน train | เพิ่ม `data/README` + `dataset_manifest.csv` (ชื่อไฟล์+label+hash) เพื่อ trace metric |
| R12 | **ขั้นตอน manual เยอะ** | 🟡 P2 | `auth_google.py`, `_migrate_db.py`, `reset.py`, `gen_ssl.py` ต้องรันมือทีละตัว | รวมเป็น `python -m vitrovision setup` / `make setup` |
| R13 | **สคริปต์เกลื่อน root** | 🟢 P3 | `_inject_mock.py`, `_migrate_db.py`, `export_aruco_png.py` ฯลฯ ปนกับโค้ดหลัก | ย้ายเข้า `scripts/` |
| R14 | **README quickstart รันไม่ผ่านจริง** | 🟠 P1 | README บอก `python shelf_manager/main.py` แต่ flat import จะ error ถ้าไม่ `cd` เข้าไปก่อน | แก้ quickstart ให้ตรงกับ entry point ใหม่ (ดูข้อ 4) |
| R15 | **metrics ไม่ผูกกับ commit/seed** | 🟡 P2 | `models/final/metrics.json` ไม่มี field commit hash / seed / dataset hash | เพิ่ม metadata block (git sha, seed, n_images, timestamp) ตอน save |

> **หมายเหตุสำคัญ (ข่าวดี):** การตรวจ git history ยืนยันว่า secret **ไม่เคยถูก commit** —
> `.gitignore` ทำงานถูกตั้งแต่แรก งาน P0 จึงเป็นแค่ "ย้ายไฟล์ออกจากดิสก์ในโฟลเดอร์ + revoke เผื่อไว้"
> ไม่ต้องทำ `git filter-repo` ซึ่งซับซ้อนและเสี่ยง

---

## 2. สถาปัตยกรรมเป้าหมาย (Target Architecture)

### 2.1 หลักการ
- **One package, one source of truth** — รวม ML logic ที่ซ้ำให้เหลือชุดเดียว
- **Config out of code** — ทุก path/secret/พอร์ต อ่านจาก `.env` ผ่าน layer เดียว
- **Run with one command** — `make <target>` หรือ `python -m vitrovision <cmd>`
- **Secret ไม่อยู่ใน repo เด็ดขาด** — มีแต่ `.example`
- **ไม่ over-engineer** — ไม่ทำ Docker/k8s/CI หนัก ๆ เกินจำเป็นสำหรับโปรเจกต์เดี่ยว

### 2.2 โครงสร้างเป้าหมาย

```
VitroVision/
├── vitrovision/                 ← package เดียว (รวม vitro_vision + shelf_manager)
│   ├── __init__.py
│   ├── __main__.py              ← CLI entry: python -m vitrovision <cmd>
│   ├── config.py                ← โหลด .env, resolve path ทั้งหมด (ที่เดียว)
│   ├── core/                    ← ML logic ที่ใช้ร่วมกัน (ไม่มีโค้ดซ้ำอีก)
│   │   ├── classifier.py        ← รวม inference (เดิม shelf_manager/inference.py)
│   │   ├── trainer.py           ← รวม trainer 2 ตัวเป็น 1  [แก้ R7]
│   │   ├── phenotyper.py
│   │   ├── detector.py  transforms.py  growth_validator.py
│   │   └── seed.py              ← set_seed() รวมศูนย์  [แก้ R10]
│   ├── data/                    ← data layer
│   │   ├── db.py                ← เดิม database.py, path จาก config  [แก้ R5]
│   │   └── registry.py          ← model registry: เลือก/โหลด model + metadata
│   ├── web/                     ← Flask app เดียว (port 5001)  [แก้ R8]
│   │   ├── app.py               ← เดิม main.py, import แบบ package  [แก้ R6]
│   │   ├── drive.py             ← เดิม drive_uploader.py
│   │   ├── templates/
│   │   └── static/              ← ★ ใหม่: design-system.css + app.js (ดูข้อ 3)
│   └── cli/                     ← scanner, batch_analyze, setup
├── models/
│   ├── final/classifier.pt + metrics.json (มี git sha+seed+hash)  [แก้ R15]
│   └── registry.json            ← index ของ model + metric + วันที่
├── data/
│   ├── README.md  +  dataset_manifest.csv  [แก้ R11]
├── notebooks/  results/
├── scripts/                     ← _inject_mock, _migrate_db, gen_ssl ...  [แก้ R13]
├── secrets.example/             ← *.json.example เท่านั้น (ไม่มีของจริง)  [แก้ R1]
├── .env.example                 ← template ตัวแปรทั้งหมด
├── environment.yml              ← conda env lock  [แก้ R9]
├── requirements.lock            ← pip pin exact
├── Makefile                     ← setup/run/train/scan/test  [แก้ R12]
├── pyproject.toml               ← ทำให้ pip install -e . ได้
├── README.md (quickstart ใหม่)  CHANGELOG.md  .gitignore
```

> **กลยุทธ์ realistic:** ไม่ต้องรื้อทุกอย่างวันเดียว. เริ่มจาก "วาง `config.py` กลาง + ย้าย secret"
> ก่อน แล้วค่อย ๆ ย้ายโมดูลเข้าโครงใหม่ทีละไฟล์ การ "รวม trainer" คือ refactor ที่คุ้มสุดเพราะ
> ตัด 400 บรรทัดซ้ำทิ้งได้

### 2.3 Config layer (หัวใจของ reproducibility)

```python
# vitrovision/config.py  (แนวคิด — ยังไม่ลงมือเขียน)
from pathlib import Path
import os
from dotenv import load_dotenv          # เพิ่ม python-dotenv ใน deps

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SECRETS_DIR  = Path(os.getenv("VV_SECRETS_DIR", Path.home()/".vitrovision"/"secrets"))
DB_PATH      = Path(os.getenv("VV_DB_PATH",  ROOT/"data"/"vitroshelf.db"))
MODEL_PATH   = Path(os.getenv("VV_MODEL_PATH", ROOT/"models"/"final"/"classifier.pt"))
GOOGLE_TOKEN = SECRETS_DIR / "oauth_token.json"      # อยู่นอก repo เสมอ
WEB_PORT     = int(os.getenv("VV_PORT", 5001))
SEED         = int(os.getenv("VV_SEED", 42))
```

`.env.example` (commit ได้ เพราะไม่มีความลับ):
```
VV_PORT=5001
VV_SEED=42
VV_SECRETS_DIR=~/.vitrovision/secrets
VV_DB_PATH=data/vitroshelf.db
GDRIVE_ROOT_FOLDER_ID=                # ใส่เอง
WANDB_MODE=offline                    # ปิด wandb เวลา demo ก็ได้
```

### 2.4 Model registry (เล่าให้กรรมการเชื่อ metric ได้)

`models/registry.json` เก็บประวัติ model: `{id, path, created, git_sha, seed, n_train, n_val,
weighted_f1, cohen_kappa, dataset_hash}`. ทำให้ตอบได้ว่า "κ=0.627 มาจาก model ตัวไหน ภาพชุดไหน
commit ไหน" — จุดนี้กรรมการ ISEF ชอบมาก

---

## 3. UX/UI Redesign (สไตล์ Claude Fable 5 — clean / scientific / minimal)

### 3.1 ปัญหา UX ปัจจุบัน
- ใช้ Tailwind CDN + inline style ปนกัน, ไม่มี `static/`, ไม่มี design token ที่เดียว
- ธีม dark `gray-950` + emoji เยอะ (🌱🧠📷📈🔬) → ดู playful มากกว่า scientific
- `train.html` 1155 บรรทัด, `bottle.html` 789 บรรทัด — หน้าใหญ่ ทำ data-viz ไม่ consistent
- nav ใช้สีต่างกันทุกลิงก์ (เขียว/ม่วง/ฟ้า/เขียวมรกต/เทา) → ไม่มี hierarchy

### 3.2 Design System (tokens)

โทน: **"lab notebook ดิจิทัล"** — พื้นสว่าง/นวล, accent เขียวพืชเดียว, ตัวเลขเด่นคม

```
COLOR
  --bg          #FAFAF9   (warm white — พื้นหลัก)
  --surface     #FFFFFF   (การ์ด)
  --border      #E7E5E4
  --text        #1C1917   (เกือบดำ)
  --text-muted  #78716C
  --accent      #15803D   (เขียวพืช — ใช้ที่เดียวพอ)
  --accent-soft #DCFCE7
  // status (semantic, ห้ามใช้นอกบริบทสถานะ)
  --healthy     #16A34A   --contaminated #EA580C   --dead #DC2626   --unknown #A8A29E

TYPE   (Inter / IBM Plex Sans Thai — ฟอนต์เดียวทั้งระบบ)
  display 28/600   h1 22/600   h2 17/600   body 14/400   caption 12/500
  numeric: tabular-nums (ตัวเลข metric เรียงตรง)

SPACE  4 · 8 · 12 · 16 · 24 · 32 · 48   (8px grid)
RADIUS 8 (การ์ด) · 6 (ปุ่ม) · 999 (badge)
SHADOW sm: 0 1 2 rgba(0,0,0,.05)   card: 0 1 3 rgba(0,0,0,.08)
```

> เลือก **light theme** แทน dark เพราะภาพถ่ายขวด/ใบไม้สีจริงอ่านง่ายกว่าบนพื้นสว่าง
> และดู "ตำราวิทยาศาสตร์" มากกว่า. ลด emoji ใน nav เหลือไอคอนเส้น (lucide) สีเดียว

### 3.3 Layout หลัก (sidebar ซ้าย + content)

```
┌──────────────────────────────────────────────────────────────────────┐
│  VitroVision                                      🔍 ค้นหาขวด   ● Model:Ready │  ← topbar
├────────────┬─────────────────────────────────────────────────────────┤
│ ◇ Dashboard │   Dashboard                                              │
│ ▣ Shelves   │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│ ⊕ Scan      │   │ 100     │ │  82%    │ │  κ 0.63 │ │  Day 14 │        │
│ ⚗ Phenotype │   │ ขวด     │ │ healthy │ │  model  │ │ รอบนี้  │        │  ← stat cards
│ ⌧ Compare   │   └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
│ 🧠 Train    │                                                          │
│ 📊 Analytics│   Growth by Formula            Status Distribution       │
│             │   ┌──────────────────────┐    ┌─────────────────────┐    │
│             │   │   vigor↑              │    │ ███████░░ A 18/20    │    │
│             │   │   A╱  B╱  C─  D╲  E╱  │    │ ██████░░░ B 16/20    │    │  ← data-viz
│ ───────     │   │  ╱  ╱                 │    │ ████████░ C 19/20    │    │
│ ● ml ready  │   │ day→                  │    │ ...                  │    │
└────────────┴───┴──────────────────────┴────┴─────────────────────┴────┘
```

### 3.4 User flow หลัก: สแกน → phenotype → เทียบสูตร → export

```
[1 SCAN]                [2 PHENOTYPE]            [3 COMPARE]            [4 EXPORT]
┌─────────────┐         ┌─────────────┐          ┌──────────────┐       ┌──────────┐
│ 📷 live cam │         │ S01-A3      │          │ สูตร A vs B  │       │ CSV /PNG │
│ ┌─────────┐ │  ArUco  │ ┌─────────┐ │  บันทึก   │ ┌──┬──┬──┐    │  เลือก  │ phenotype│
│ │ [bottle]│ │ ──ตรวจ→ │ │ overlay │ │ ──ลง DB→ │ │A │B │C │    │ ──ช่วง→ │ summary  │
│ │ #A3  ●  │ │  id+AI  │ │ green82%│ │          │ │██│██│██│    │  วัน    │ report   │
│ └─────────┘ │         │ vigor 7.4 │ │          │ Kruskal-     │       │ + กราฟ   │
│ healthy 0.91│         │ [✓ บันทึก] │ │          │ Wallis p<.05 │       │          │
└─────────────┘         └─────────────┘          └──────────────┘       └──────────┘
   1 หน้า                  panel ขวา                หน้า Analytics         ปุ่มเดียว
```

### 3.5 Component spec (ที่ใช้ซ้ำทั้งระบบ)

| Component | สเปก |
|-----------|------|
| **StatCard** | ตัวเลขใหญ่ `tabular-nums` + label เล็กด้านล่าง + เส้น sparkline จาง; border 1px ไม่มีเงาหนา |
| **StatusBadge** | pill กลม สีตาม semantic token + จุดนำ `●`; ใช้ที่เดียวทั่วระบบ |
| **BottleCard** | thumbnail 1:1 + id + status badge + วัน; hover ยกเงาเบา ๆ |
| **PhenotypePanel** | ภาพ + overlay mask + ตาราง 7 ค่า (numeric ขวา) + vigor gauge 0–10 |
| **ComparisonChart** | bar/line ต่อสูตร A–E ใช้สี accent เดียว ไล่เฉด ไม่ใช่สีรุ้ง; แสดง p-value ใต้กราฟ |
| **ConfidenceBar** | แถบ AI confidence + เส้น threshold (0.70) ให้เห็นว่าเข้าเกณฑ์ไหม |

### 3.6 หลักการ data-viz (สำคัญต่อการแข่ง)
- **สีรุ้งออก, เฉดเดียวเข้า** — สูตร A–E ใช้เขียวไล่อ่อน→เข้ม + ป้ายกำกับ (ไม่พึ่งสีอย่างเดียว = a11y)
- ทุกกราฟเปรียบเทียบ **โชว์ค่าสถิติ** (p-value, n, error bar) ใต้กราฟ — ดูเป็นงานวิจัย
- กราฟ growth curve มี **error band** ไม่ใช่เส้นเปล่า

---

## 4. Reproduction Quickstart (เป้าหมาย — README ในอุดมคติ)

```bash
# 1. Clone
git clone https://github.com/peeradon4778/VitroVision.git
cd VitroVision

# 2. สร้าง env จาก lock (ได้เวอร์ชันเป๊ะตามที่ผู้ทำใช้)
conda env create -f environment.yml      # สร้าง env ชื่อ ml
conda activate ml
pip install -e .                          # ติดตั้ง package vitrovision

# 3. ตั้งค่า (คัดลอก template — ยังไม่มีความลับ)
cp .env.example .env
cp -r secrets.example ~/.vitrovision/secrets   # แล้วเติม credential ของตัวเอง

# 4. (ครั้งแรกเท่านั้น) auth Google Drive + สร้าง DB
python -m vitrovision setup               # auth + init db + migrate รวบทีเดียว

# 5. รัน web app
python -m vitrovision web                 # → http://localhost:5001
#   หรือ:  make run

# --- งานอื่น ---
python -m vitrovision scan --day 14       # live scanner
python -m vitrovision train               # train classifier (seed=42, reproducible)
make test                                 # smoke test ว่า import/route ผ่าน
```

`Makefile` (เป้าหมาย):
```
setup:  python -m vitrovision setup
run:    python -m vitrovision web
train:  python -m vitrovision train
scan:   python -m vitrovision scan --day $(DAY)
lock:   conda env export --no-builds > environment.yml
test:   python -m pytest -q
```

> ผลที่ได้: กรรมการ/เพื่อน clone แล้วถึงหน้าเว็บได้ใน 5 คำสั่ง โดยไม่ต้องรู้ path เครื่องคุณ

---

## 5. Roadmap แบ่งเฟส

### P0 — Security + กันพังก่อน (½–1 วัน) 🔴 ทำก่อนสุด
| งาน | effort | เสี่ยง |
|-----|--------|-------|
| ย้าย `oauth_token.json`, `gdrive_key.json`, `oauth_client.json`, `*.pem`, `vitroshelf.db` ออกไป `~/.vitrovision/secrets/` (นอก OneDrive) | ต่ำ | ต่ำ — แค่ระวัง drive_uploader/database หา path ไม่เจอ → แก้ให้ชี้ env |
| **Revoke + ออก Google token ใหม่** (เพราะตัวเก่าเคย sync OneDrive) | ต่ำ | ต่ำ |
| commit `*.example` แทนไฟล์จริง; ยืนยัน `.gitignore` ครอบครบ | ต่ำ | ต่ำ |
| ตรวจ git history ซ้ำ (ทำแล้ว = สะอาด ✅ ไม่ต้อง filter-repo) | — | — |

> P0 ปลดล็อกให้ "ซิปส่ง/ขึ้น public repo ได้โดยไม่หลุดความลับ"

### P1 — Architecture + Reproducibility (2–4 วัน) 🟠
| งาน | effort | เสี่ยง |
|-----|--------|-------|
| วาง `vitrovision/config.py` กลาง + `.env` (R4, R5) | กลาง | ต่ำ |
| **รวม trainer 2 ไฟล์ → 1** (R7) | กลาง | กลาง — ต้องทดสอบ train ยังได้ κ เดิม |
| ตัด `train_app.py` (port 5002) ทิ้ง (R8) | ต่ำ | ต่ำ |
| ทำ `pyproject.toml` + แก้ flat import เป็น package (R6) | กลาง | กลาง — กระทบ import หลายไฟล์ |
| `environment.yml` + `requirements.lock` pin จาก env จริง (R9) | ต่ำ | ต่ำ |
| `set_seed(42)` รวมศูนย์ + บันทึก seed/git_sha ใน metrics (R10, R15) | ต่ำ | ต่ำ — เพิ่มความน่าเชื่อถือ metric |
| CLI `python -m vitrovision <cmd>` + Makefile (R12) | กลาง | ต่ำ |
| ย้ายสคริปต์เข้า `scripts/`, เขียน quickstart ใหม่ (R13, R14) | ต่ำ | ต่ำ |

### P2 — UX/UI Redesign (3–5 วัน) 🟡
| งาน | effort | เสี่ยง |
|-----|--------|-------|
| สร้าง `static/design-system.css` + tokens (เลิก inline style) | กลาง | ต่ำ |
| ทำ component ร่วม (StatCard, StatusBadge, BottleCard) | กลาง | ต่ำ |
| redesign Dashboard + layout sidebar (light theme) | กลาง | ต่ำ |
| รวม data-viz ให้ consistent (เฉดเดียว + p-value + error band) | กลาง | กลาง |
| ปรับ flow scan→phenotype→compare→export ให้ลื่น | กลาง | ต่ำ |

### P3 — Polish (1–2 วัน) 🟢
- `dataset_manifest.csv` + data/README (R11) · model registry.json · pytest smoke test
- a11y pass (contrast, ป้ายกำกับกราฟ) · screenshot ชุดสำหรับโปสเตอร์ YSC

**รวมประมาณ 8–14 วันทำงาน** กระจายได้หลายสัปดาห์ · เริ่ม P0 ทันที (ครึ่งวันก็เสร็จ)

---

## 6. สิ่งที่ "อย่าทำ" (กัน over-engineer)
- ❌ อย่าทำ Docker/CI/CD pipeline เต็มรูป — เกินความจำเป็นสำหรับโปรเจกต์เดี่ยว
- ❌ อย่าเปลี่ยนไป React/SPA — Flask+Jinja+Tailwind พอแล้ว แค่จัด design system
- ❌ อย่า `git filter-repo` — history สะอาดอยู่แล้ว เสี่ยงพังเปล่า ๆ
- ❌ อย่ารื้อ DB schema — แค่ย้าย path; schema ทำงานได้ดี
- ✅ โฟกัส: ย้าย secret · รวมโค้ดซ้ำ · pin env · design system เดียว
```
