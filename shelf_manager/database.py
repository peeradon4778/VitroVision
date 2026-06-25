import sqlite3
from contextlib import contextmanager
from datetime import datetime, date

DB_PATH = "vitroshelf.db"

ROWS = ["A", "B", "C", "D", "E"]
COLS = list(range(1, 11))
SHELVES = ["S01", "S02"]

STATUS_CHOICES = ["healthy", "contaminated", "dead", "unknown"]


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS batches (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                round_type  TEXT NOT NULL DEFAULT 'training',
                start_date  TEXT NOT NULL,
                notes       TEXT DEFAULT '',
                created_at  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bottles (
                bottle_id   TEXT PRIMARY KEY,
                shelf       TEXT NOT NULL,
                row         TEXT NOT NULL,
                col         INTEGER NOT NULL,
                batch_id    INTEGER DEFAULT NULL,
                species     TEXT DEFAULT '',
                treatment   TEXT DEFAULT '',
                date_planted TEXT DEFAULT '',
                notes       TEXT DEFAULT '',
                FOREIGN KEY (batch_id) REFERENCES batches(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                bottle_id       TEXT NOT NULL,
                batch_id        INTEGER DEFAULT NULL,
                day_point       INTEGER NOT NULL,
                date_taken      TEXT NOT NULL,
                status          TEXT NOT NULL DEFAULT 'unknown',
                drive_file_id   TEXT DEFAULT '',
                drive_url       TEXT DEFAULT '',
                local_path      TEXT DEFAULT '',
                shoot_count     INTEGER DEFAULT -1,
                media_color     TEXT DEFAULT 'normal',
                hyperhydricity  INTEGER DEFAULT 0,
                has_roots       INTEGER DEFAULT 0,
                ai_status       TEXT DEFAULT '',
                ai_confidence   REAL DEFAULT 0.0,
                FOREIGN KEY (bottle_id) REFERENCES bottles(bottle_id),
                FOREIGN KEY (batch_id)  REFERENCES batches(id)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_images_bottle
                ON images(bottle_id)
        """)
        conn.commit()
        _seed_bottles(conn)
    _migrate_db()


def _migrate_db():
    """เพิ่ม columns ให้ DB เดิมที่สร้างก่อน schema นี้"""
    images_cols = [
        ("local_path",     "TEXT    DEFAULT ''"),
        ("shoot_count",    "INTEGER DEFAULT -1"),
        ("media_color",    "TEXT    DEFAULT 'normal'"),
        ("hyperhydricity", "INTEGER DEFAULT 0"),
        ("has_roots",      "INTEGER DEFAULT 0"),
        ("ai_status",      "TEXT    DEFAULT ''"),
        ("ai_confidence",  "REAL    DEFAULT 0.0"),
        ("batch_id",       "INTEGER DEFAULT NULL"),
    ]
    bottles_cols = [
        ("batch_id", "INTEGER DEFAULT NULL"),
    ]
    with get_conn() as conn:
        existing_img = {row[1] for row in conn.execute("PRAGMA table_info(images)")}
        for col_name, col_def in images_cols:
            if col_name not in existing_img:
                conn.execute(f"ALTER TABLE images ADD COLUMN {col_name} {col_def}")

        existing_btl = {row[1] for row in conn.execute("PRAGMA table_info(bottles)")}
        for col_name, col_def in bottles_cols:
            if col_name not in existing_btl:
                conn.execute(f"ALTER TABLE bottles ADD COLUMN {col_name} {col_def}")

        new_images_growth = [
            ("shoot_height_class",  "TEXT    DEFAULT ''"),
            ("root_density",        "TEXT    DEFAULT 'none'"),
            ("callus_present",      "INTEGER DEFAULT 0"),
            ("dev_stage",           "TEXT    DEFAULT ''"),
            ("vigor_score",         "REAL    DEFAULT 0"),
            ("green_coverage_pct",  "REAL    DEFAULT NULL"),
            ("leaf_color_index",    "REAL    DEFAULT NULL"),
            ("shoot_count_cv",      "INTEGER DEFAULT NULL"),
            ("media_color_cv",      "TEXT    DEFAULT ''"),
            ("texture_entropy",     "REAL    DEFAULT NULL"),
            ("brown_coverage_pct",  "REAL    DEFAULT NULL"),
            ("phenotype_method",    "TEXT    DEFAULT ''"),
            ("convex_hull_ratio",   "REAL    DEFAULT NULL"),
            ("exg_mean",            "REAL    DEFAULT NULL"),
            ("vari_mean",           "REAL    DEFAULT NULL"),
            ("glcm_contrast",       "REAL    DEFAULT NULL"),
            ("glcm_homogeneity",    "REAL    DEFAULT NULL"),
            ("specular_fraction",   "REAL    DEFAULT NULL"),
            ("ngrdi_mean",          "REAL    DEFAULT NULL"),
            ("cive_mean",           "REAL    DEFAULT NULL"),
        ]
        for col_name, col_def in new_images_growth:
            if col_name not in existing_img:
                conn.execute(f"ALTER TABLE images ADD COLUMN {col_name} {col_def}")

        new_bottles_growth = [
            ("cultivar",        "TEXT    DEFAULT ''"),
            ("media_formula",   "TEXT    DEFAULT ''"),
            ("pgr_detail",      "TEXT    DEFAULT ''"),
            ("passage_number",  "INTEGER DEFAULT 1"),
            ("emergence_date",  "TEXT    DEFAULT ''"),  # GAP-3: วันงอก (per-bottle)
        ]
        for col_name, col_def in new_bottles_growth:
            if col_name not in existing_btl:
                conn.execute(f"ALTER TABLE bottles ADD COLUMN {col_name} {col_def}")

        # GAP-3: sow_date ที่ระดับ batch
        existing_bat = {row[1] for row in conn.execute("PRAGMA table_info(batches)")}
        if "sow_date" not in existing_bat:
            conn.execute("ALTER TABLE batches ADD COLUMN sow_date TEXT DEFAULT ''")

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_images_batch ON images(batch_id)
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expert_scores (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id         INTEGER NOT NULL,
                rater_id         TEXT    NOT NULL,
                vigor_grade      INTEGER NOT NULL,
                hyperhydric_flag INTEGER DEFAULT 0,
                dev_stage_check  TEXT    DEFAULT '',
                notes            TEXT    DEFAULT '',
                ts               TEXT    NOT NULL,
                FOREIGN KEY (image_id) REFERENCES images(id)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_expert_image ON expert_scores(image_id)
        """)

        # TEMPO V3 — L5 temporal feature store
        conn.execute("""
            CREATE TABLE IF NOT EXISTS phenotype_series (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                bottle_id       TEXT    NOT NULL,
                batch_id        INTEGER DEFAULT NULL,
                day_point       INTEGER NOT NULL,
                feature_vector  TEXT    NOT NULL,
                mask_url        TEXT    DEFAULT '',
                prompt_method   TEXT    DEFAULT 'hsv_fallback',
                ts              TEXT    NOT NULL,
                FOREIGN KEY (bottle_id) REFERENCES bottles(bottle_id)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_series_bottle
                ON phenotype_series(bottle_id, day_point)
        """)
        conn.commit()


# --- Batch functions ---

def create_batch(name, round_type, start_date, notes="", sow_date=""):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO batches(name, round_type, start_date, notes, created_at, sow_date) VALUES (?,?,?,?,?,?)",
            (name, round_type, start_date, notes, created_at, sow_date)
        )
        conn.commit()
        return cur.lastrowid


def get_active_batch():
    """รอบล่าสุด = รอบที่กำลังใช้งาน"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM batches ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def get_active_batch_id() -> int | None:
    b = get_active_batch()
    return b['id'] if b else None


def get_all_batches():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM batches ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


def start_new_round(batch_id):
    """ผูกขวดทั้ง 100 ใบกับ batch ใหม่ และล้าง metadata รอบเก่า"""
    with get_conn() as conn:
        conn.execute("""
            UPDATE bottles SET batch_id=?, species='', treatment='', date_planted='',
                               notes='', emergence_date=''
        """, (batch_id,))
        conn.commit()


def get_batch_stats(batch_id):
    with get_conn() as conn:
        photos = conn.execute(
            "SELECT COUNT(*) FROM images WHERE batch_id=?", (batch_id,)
        ).fetchone()[0]
        status_counts = conn.execute("""
            SELECT i.status, COUNT(*) as cnt
            FROM images i
            INNER JOIN (
                SELECT bottle_id, MAX(day_point) as max_day
                FROM images WHERE batch_id=? GROUP BY bottle_id
            ) latest ON i.bottle_id = latest.bottle_id AND i.day_point = latest.max_day
            WHERE i.batch_id=?
            GROUP BY i.status
        """, (batch_id, batch_id)).fetchall()
    return {
        "total_photos": photos,
        "status_counts": {r["status"]: r["cnt"] for r in status_counts},
    }


# --- Bottle/Seed functions ---

def _seed_bottles(conn):
    existing = conn.execute("SELECT COUNT(*) FROM bottles").fetchone()[0]
    if existing > 0:
        return
    rows_to_insert = []
    for shelf in SHELVES:
        for row in ROWS:
            for col in COLS:
                bottle_id = f"{shelf}-{row}-{col:02d}"
                rows_to_insert.append((bottle_id, shelf, row, col))
    conn.executemany(
        "INSERT INTO bottles(bottle_id, shelf, row, col) VALUES (?,?,?,?)",
        rows_to_insert
    )
    conn.commit()


def get_shelf_grid(shelf, batch_id=None):
    batch = get_active_batch() if batch_id is None else {"id": batch_id}
    bid = batch["id"] if batch else None
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT b.bottle_id, b.row, b.col, b.species, b.treatment, b.date_planted,
                   COALESCE((
                       SELECT status FROM images
                       WHERE bottle_id = b.bottle_id AND (? IS NULL OR batch_id = ?)
                       ORDER BY day_point DESC LIMIT 1
                   ), 'unknown') as latest_status,
                   (SELECT COUNT(*) FROM images
                    WHERE bottle_id = b.bottle_id AND (? IS NULL OR batch_id = ?)) as photo_count
            FROM bottles b
            WHERE b.shelf = ?
            ORDER BY b.row, b.col
        """, (bid, bid, bid, bid, shelf)).fetchall()
    grid = {}
    for r in ROWS:
        grid[r] = {}
        for c in COLS:
            grid[r][c] = None
    for row in rows:
        grid[row["row"]][row["col"]] = dict(row)
    return grid


def get_bottle(bottle_id):
    with get_conn() as conn:
        bottle = conn.execute(
            "SELECT * FROM bottles WHERE bottle_id = ?", (bottle_id,)
        ).fetchone()
        images = conn.execute(
            """SELECT id, day_point, date_taken, status, drive_url, local_path,
                      shoot_count, media_color, hyperhydricity, has_roots,
                      ai_status, ai_confidence,
                      green_coverage_pct, leaf_color_index,
                      shoot_count_cv, media_color_cv, phenotype_method
               FROM images WHERE bottle_id = ? ORDER BY day_point""",
            (bottle_id,)
        ).fetchall()
    return dict(bottle) if bottle else None, [dict(i) for i in images]


def update_bottle_info(bottle_id, species, treatment, date_planted, notes,
                       cultivar="", media_formula="", pgr_detail="", passage_number=1):
    with get_conn() as conn:
        conn.execute("""
            UPDATE bottles SET species=?, treatment=?, date_planted=?, notes=?,
                               cultivar=?, media_formula=?, pgr_detail=?, passage_number=?
            WHERE bottle_id=?
        """, (species, treatment, date_planted, notes,
              cultivar, media_formula, pgr_detail, passage_number, bottle_id))
        conn.commit()


def add_image(bottle_id, day_point, status, drive_file_id="", drive_url="",
              local_path="", shoot_count=-1, media_color="normal",
              hyperhydricity=False, has_roots=False, batch_id=None,
              shoot_height_class="", root_density="none",
              callus_present=False, dev_stage="", vigor_score=0):
    if batch_id is None:
        active = get_active_batch()
        batch_id = active["id"] if active else None
    date_taken = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO images(bottle_id, batch_id, day_point, date_taken, status,
                               drive_file_id, drive_url, local_path,
                               shoot_count, media_color, hyperhydricity, has_roots,
                               shoot_height_class, root_density, callus_present,
                               dev_stage, vigor_score)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (bottle_id, batch_id, day_point, date_taken, status,
              drive_file_id, drive_url, local_path,
              shoot_count, media_color, int(hyperhydricity), int(has_roots),
              shoot_height_class, root_density, int(callus_present),
              dev_stage, vigor_score))
        conn.commit()
        return cur.lastrowid


def update_image_cv(image_id, shoot_count=-1, media_color="normal",
                    hyperhydricity=False, has_roots=False,
                    ai_status="", ai_confidence=0.0):
    with get_conn() as conn:
        conn.execute("""
            UPDATE images SET shoot_count=?, media_color=?, hyperhydricity=?,
                              has_roots=?, ai_status=?, ai_confidence=?
            WHERE id=?
        """, (shoot_count, media_color, int(hyperhydricity), int(has_roots),
              ai_status, ai_confidence, image_id))
        conn.commit()


def update_image_phenotype(image_id, green_coverage_pct, leaf_color_index,
                           shoot_count_cv, media_color_cv, phenotype_method,
                           texture_entropy=None, brown_coverage_pct=None,
                           vigor_score=None, convex_hull_ratio=None,
                           exg_mean=None, vari_mean=None,
                           glcm_contrast=None, glcm_homogeneity=None,
                           specular_fraction=None, ngrdi_mean=None, cive_mean=None):
    with get_conn() as conn:
        conn.execute("""
            UPDATE images SET green_coverage_pct=?, leaf_color_index=?,
                              shoot_count_cv=?, media_color_cv=?, phenotype_method=?,
                              texture_entropy=?, brown_coverage_pct=?, vigor_score=?,
                              convex_hull_ratio=?, exg_mean=?, vari_mean=?,
                              glcm_contrast=?, glcm_homogeneity=?,
                              specular_fraction=?, ngrdi_mean=?, cive_mean=?
            WHERE id=?
        """, (green_coverage_pct, leaf_color_index,
              shoot_count_cv, media_color_cv, phenotype_method,
              texture_entropy, brown_coverage_pct, vigor_score,
              convex_hull_ratio, exg_mean, vari_mean,
              glcm_contrast, glcm_homogeneity,
              specular_fraction, ngrdi_mean, cive_mean, image_id))
        conn.commit()


def get_phenotype_series(bottle_id):
    """คืน time series ของ phenotyping data สำหรับ growth chart"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT day_point, date_taken, green_coverage_pct, leaf_color_index,
                   shoot_count_cv, media_color_cv, texture_entropy, brown_coverage_pct,
                   vigor_score, convex_hull_ratio, exg_mean, vari_mean,
                   glcm_contrast, glcm_homogeneity, phenotype_method, status
            FROM images
            WHERE bottle_id=? AND green_coverage_pct IS NOT NULL
            ORDER BY day_point
        """, (bottle_id,)).fetchall()
    return [dict(r) for r in rows]


def get_formulation_series(batch_id=None):
    """คืน phenotype time series ทุกขวด grouped by media_formula — ใช้สำหรับ CSBI analysis"""
    filter_sql = "WHERE b.batch_id=? AND i.green_coverage_pct IS NOT NULL" if batch_id else "WHERE i.green_coverage_pct IS NOT NULL"
    params = (batch_id,) if batch_id else ()
    with get_conn() as conn:
        rows = conn.execute(f"""
            SELECT i.bottle_id, b.media_formula, b.pgr_detail,
                   i.day_point, i.date_taken, i.status,
                   i.green_coverage_pct, i.leaf_color_index, i.shoot_count_cv,
                   i.texture_entropy, i.brown_coverage_pct, i.vigor_score,
                   i.convex_hull_ratio, i.exg_mean, i.vari_mean,
                   i.glcm_contrast, i.glcm_homogeneity,
                   i.media_color_cv, i.phenotype_method,
                   i.ngrdi_mean, i.cive_mean, i.specular_fraction
            FROM images i
            JOIN bottles b ON i.bottle_id = b.bottle_id
            {filter_sql}
            ORDER BY b.media_formula, i.bottle_id, i.day_point
        """, params).fetchall()
    return [dict(r) for r in rows]


def get_bottle_timeline(bottle_id):
    """คืน time series ทุก record ของขวด — ใช้สำหรับ growth timeline chart"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT day_point, date_taken, status,
                   shoot_count, vigor_score, shoot_height_class,
                   root_density, callus_present, dev_stage, hyperhydricity,
                   green_coverage_pct, leaf_color_index,
                   shoot_count_cv, media_color_cv,
                   texture_entropy, brown_coverage_pct,
                   convex_hull_ratio, exg_mean, vari_mean,
                   glcm_contrast, glcm_homogeneity,
                   ai_status, ai_confidence, phenotype_method,
                   ngrdi_mean, cive_mean, specular_fraction
            FROM images
            WHERE bottle_id=?
            ORDER BY day_point, date_taken
        """, (bottle_id,)).fetchall()
    return [dict(r) for r in rows]


def update_image_local_path(image_id, local_path):
    with get_conn() as conn:
        conn.execute("UPDATE images SET local_path=? WHERE id=?", (local_path, image_id))
        conn.commit()


def update_image_drive(image_id, drive_file_id, drive_url):
    with get_conn() as conn:
        conn.execute(
            "UPDATE images SET drive_file_id=?, drive_url=? WHERE id=?",
            (drive_file_id, drive_url, image_id)
        )
        conn.commit()


def get_image_url(image_id):
    with get_conn() as conn:
        row = conn.execute("SELECT drive_url FROM images WHERE id=?", (image_id,)).fetchone()
    return row["drive_url"] if row else None


def get_image_sources(image_id):
    # คืนทั้ง drive_url และ local_path ของภาพ เพื่อให้ route ทำ fallback ได้
    # (drive_url ว่าง = ยังไม่ได้อัป Drive → ใช้ไฟล์ local แทน)
    with get_conn() as conn:
        row = conn.execute(
            "SELECT drive_url, local_path FROM images WHERE id=?", (image_id,)
        ).fetchone()
    if not row:
        return None
    return {"drive_url": row["drive_url"], "local_path": row["local_path"]}


def add_expert_score(image_id, rater_id, vigor_grade,
                     hyperhydric_flag=0, dev_stage_check='', notes=''):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO expert_scores(image_id, rater_id, vigor_grade,
                                      hyperhydric_flag, dev_stage_check, notes, ts)
            VALUES (?,?,?,?,?,?,?)
        """, (image_id, rater_id, vigor_grade,
              int(hyperhydric_flag), dev_stage_check, notes, ts))
        conn.commit()
        return cur.lastrowid


def get_expert_scores_by_image(image_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM expert_scores WHERE image_id=? ORDER BY ts",
            (image_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_expert_score_count():
    with get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM expert_scores").fetchone()[0]
        raters = conn.execute(
            "SELECT COUNT(DISTINCT rater_id) FROM expert_scores"
        ).fetchone()[0]
    return {"count": count, "rater_count": raters}


def get_next_bottle_id(bottle_id):
    parts = bottle_id.split('-')
    shelf, row, col = parts[0], parts[1], int(parts[2])
    col_idx = COLS.index(col)
    row_idx = ROWS.index(row)
    shelf_idx = SHELVES.index(shelf)
    if col_idx + 1 < len(COLS):
        return f"{shelf}-{row}-{COLS[col_idx+1]:02d}"
    elif row_idx + 1 < len(ROWS):
        return f"{shelf}-{ROWS[row_idx+1]}-{COLS[0]:02d}"
    elif shelf_idx + 1 < len(SHELVES):
        return f"{SHELVES[shelf_idx+1]}-{ROWS[0]}-{COLS[0]:02d}"
    else:
        return f"{SHELVES[0]}-{ROWS[0]}-{COLS[0]:02d}"


def get_stats():
    active = get_active_batch()
    bid = active["id"] if active else None
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM bottles").fetchone()[0]
        photos = conn.execute(
            "SELECT COUNT(*) FROM images WHERE (? IS NULL OR batch_id=?)", (bid, bid)
        ).fetchone()[0]
        status_counts = conn.execute("""
            SELECT i.status, COUNT(*) as cnt
            FROM images i
            INNER JOIN (
                SELECT bottle_id, MAX(day_point) as max_day
                FROM images WHERE (? IS NULL OR batch_id=?) GROUP BY bottle_id
            ) latest ON i.bottle_id = latest.bottle_id AND i.day_point = latest.max_day
            WHERE (? IS NULL OR i.batch_id=?)
            GROUP BY i.status
        """, (bid, bid, bid, bid)).fetchall()
    return {
        "total_bottles": total,
        "total_photos": photos,
        "status_counts": {r["status"]: r["cnt"] for r in status_counts},
        "active_batch": active,
    }


def get_today_capture_count():
    """จำนวนขวด (distinct) ที่มีภาพถ่าย 'วันนี้' ใน batch ปัจจุบัน + total bottles"""
    active = get_active_batch()
    bid = active["id"] if active else None
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM bottles").fetchone()[0]
        today = conn.execute("""
            SELECT COUNT(DISTINCT bottle_id) FROM images
            WHERE date(date_taken) = date('now','localtime')
              AND (? IS NULL OR batch_id = ?)
        """, (bid, bid)).fetchone()[0]
    return {"today": today, "total": total}


# ── GAP-3: sow_date / emergence_date ──────────────────────────────────────────

def update_batch_sow_date(batch_id, sow_date):
    with get_conn() as conn:
        conn.execute("UPDATE batches SET sow_date=? WHERE id=?", (sow_date, batch_id))
        conn.commit()


def update_bottle_emergence(bottle_id, emergence_date):
    """บันทึกวันงอกของขวด — emergence_date='YYYY-MM-DD' หรือ '' เพื่อล้าง"""
    with get_conn() as conn:
        conn.execute("UPDATE bottles SET emergence_date=? WHERE bottle_id=?",
                     (emergence_date, bottle_id))
        conn.commit()


def get_day_from_emergence(bottle_id):
    """คืนจำนวนวันนับจากวันงอก หรือ None ถ้ายังไม่ได้บันทึก emergence_date"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT emergence_date FROM bottles WHERE bottle_id=?", (bottle_id,)
        ).fetchone()
    if not row or not row["emergence_date"]:
        return None
    try:
        em = date.fromisoformat(row["emergence_date"])
        return (date.today() - em).days
    except ValueError:
        return None


def get_germination_stats(batch_id=None):
    """สถิติการงอก: จำนวนขวดที่มี emergence_date / ทั้งหมด"""
    bid = batch_id
    if bid is None:
        active = get_active_batch()
        bid = active["id"] if active else None
    with get_conn() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM bottles WHERE (? IS NULL OR batch_id=?)", (bid, bid)
        ).fetchone()[0]
        emerged = conn.execute(
            "SELECT COUNT(*) FROM bottles WHERE emergence_date != '' AND emergence_date IS NOT NULL"
            " AND (? IS NULL OR batch_id=?)", (bid, bid)
        ).fetchone()[0]
    pct = round(emerged / total * 100, 1) if total else 0
    return {"emerged": emerged, "total": total, "germination_pct": pct}


def suggest_day_point(batch_id=None):
    """แนะนำ day_point วันนี้ = วันนี้ - sow_date ของ batch (fallback ถ้าไม่มี emergence)"""
    if batch_id is not None:
        with get_conn() as conn:
            row = conn.execute("SELECT sow_date FROM batches WHERE id=?", (batch_id,)).fetchone()
            sow = row["sow_date"] if row else ""
    else:
        active = get_active_batch()
        sow = (active or {}).get("sow_date", "")
    if not sow:
        return None
    try:
        sow_d = date.fromisoformat(sow)
        return (date.today() - sow_d).days
    except ValueError:
        return None


# --- TEMPO V3 — phenotype_series (L5 temporal store) ---

def add_phenotype_series_record(bottle_id, day_point, feature_vector: dict,
                                 batch_id=None, mask_url='', prompt_method='hsv_fallback'):
    """บันทึก feature vector 1 time-point สำหรับ CNN-LSTM temporal model"""
    import json
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO phenotype_series
               (bottle_id, batch_id, day_point, feature_vector, mask_url, prompt_method, ts)
               VALUES (?,?,?,?,?,?,?)""",
            (bottle_id, batch_id, day_point, json.dumps(feature_vector),
             mask_url, prompt_method, ts)
        )
        conn.commit()
        return cur.lastrowid


def get_temporal_series(bottle_id):
    """คืน feature vector time-series ต่อขวด สำหรับ CNN-LSTM — ordered by day_point"""
    import json
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT day_point, feature_vector, mask_url, prompt_method, ts
               FROM phenotype_series
               WHERE bottle_id=?
               ORDER BY day_point""",
            (bottle_id,)
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d['feature_vector'] = json.loads(d['feature_vector'])
        result.append(d)
    return result


def get_batch_temporal_series(batch_id):
    """คืน feature vector time-series ทุกขวดใน batch — ใช้ train CNN-LSTM"""
    import json
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT ps.bottle_id, b.media_formula, ps.day_point,
                      ps.feature_vector, ps.mask_url, ps.prompt_method
               FROM phenotype_series ps
               JOIN bottles b ON ps.bottle_id = b.bottle_id
               WHERE ps.batch_id=?
               ORDER BY ps.bottle_id, ps.day_point""",
            (batch_id,)
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d['feature_vector'] = json.loads(d['feature_vector'])
        result.append(d)
    return result


def get_unlabeled_bottles():
    """คืนขวดที่มี status='unknown' และมีภาพ local — image ล่าสุดต่อขวด สำหรับ AL query"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT b.bottle_id, b.shelf, b.row, b.col,
                   i.id AS image_id, i.local_path
            FROM images i
            JOIN bottles b ON i.bottle_id = b.bottle_id
            INNER JOIN (
                SELECT bottle_id, MAX(id) AS max_id
                FROM images
                WHERE status = 'unknown'
                  AND local_path IS NOT NULL
                  AND local_path != ''
                GROUP BY bottle_id
            ) latest ON i.bottle_id = latest.bottle_id AND i.id = latest.max_id
            ORDER BY b.shelf, b.row, b.col
        """).fetchall()
    return [dict(r) for r in rows]
