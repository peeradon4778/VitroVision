import sqlite3
from contextlib import contextmanager
from datetime import datetime

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
            ("vigor_score",         "INTEGER DEFAULT 0"),
            ("green_coverage_pct",  "REAL    DEFAULT NULL"),
            ("leaf_color_index",    "REAL    DEFAULT NULL"),
            ("shoot_count_cv",      "INTEGER DEFAULT NULL"),
            ("media_color_cv",      "TEXT    DEFAULT ''"),
            ("phenotype_method",    "TEXT    DEFAULT ''"),
        ]
        for col_name, col_def in new_images_growth:
            if col_name not in existing_img:
                conn.execute(f"ALTER TABLE images ADD COLUMN {col_name} {col_def}")

        new_bottles_growth = [
            ("cultivar",        "TEXT    DEFAULT ''"),
            ("media_formula",   "TEXT    DEFAULT ''"),
            ("pgr_detail",      "TEXT    DEFAULT ''"),
            ("passage_number",  "INTEGER DEFAULT 1"),
        ]
        for col_name, col_def in new_bottles_growth:
            if col_name not in existing_btl:
                conn.execute(f"ALTER TABLE bottles ADD COLUMN {col_name} {col_def}")

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_images_batch ON images(batch_id)
        """)
        conn.commit()


# --- Batch functions ---

def create_batch(name, round_type, start_date, notes=""):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO batches(name, round_type, start_date, notes, created_at) VALUES (?,?,?,?,?)",
            (name, round_type, start_date, notes, created_at)
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


def get_all_batches():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM batches ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


def start_new_round(batch_id):
    """ผูกขวดทั้ง 100 ใบกับ batch ใหม่ และล้าง metadata รอบเก่า"""
    with get_conn() as conn:
        conn.execute("""
            UPDATE bottles SET batch_id=?, species='', treatment='', date_planted='', notes=''
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
              callus_present=False, vigor_score=0):
    if batch_id is None:
        active = get_active_batch()
        batch_id = active["id"] if active else None
    date_taken = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO images(bottle_id, batch_id, day_point, date_taken, status,
                               drive_file_id, drive_url, local_path,
                               shoot_count, media_color, hyperhydricity, has_roots,
                               shoot_height_class, root_density, callus_present, vigor_score)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (bottle_id, batch_id, day_point, date_taken, status,
              drive_file_id, drive_url, local_path,
              shoot_count, media_color, int(hyperhydricity), int(has_roots),
              shoot_height_class, root_density, int(callus_present), vigor_score))
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
                           shoot_count_cv, media_color_cv, phenotype_method):
    with get_conn() as conn:
        conn.execute("""
            UPDATE images SET green_coverage_pct=?, leaf_color_index=?,
                              shoot_count_cv=?, media_color_cv=?, phenotype_method=?
            WHERE id=?
        """, (green_coverage_pct, leaf_color_index,
              shoot_count_cv, media_color_cv, phenotype_method, image_id))
        conn.commit()


def get_phenotype_series(bottle_id):
    """คืน time series ของ phenotyping data สำหรับ growth chart"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT day_point, date_taken, green_coverage_pct, leaf_color_index,
                   shoot_count_cv, media_color_cv, phenotype_method, status
            FROM images
            WHERE bottle_id=? AND green_coverage_pct IS NOT NULL
            ORDER BY day_point
        """, (bottle_id,)).fetchall()
    return [dict(r) for r in rows]


def get_bottle_timeline(bottle_id):
    """คืน time series ทุก record ของขวด — ใช้สำหรับ growth timeline chart"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT day_point, date_taken, status,
                   shoot_count, vigor_score, shoot_height_class,
                   root_density, callus_present,
                   green_coverage_pct, leaf_color_index,
                   shoot_count_cv, media_color_cv,
                   ai_status, ai_confidence
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
