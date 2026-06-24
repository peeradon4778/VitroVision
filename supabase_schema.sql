-- VitroVision — Supabase Schema (PostgreSQL)
-- วิธีใช้: เปิด Supabase Dashboard → SQL Editor → New query → paste → Run

-- ── batches ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS batches (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    round_type  TEXT NOT NULL DEFAULT 'training',
    start_date  TEXT NOT NULL,
    sow_date    TEXT DEFAULT '',
    notes       TEXT DEFAULT '',
    created_at  TEXT NOT NULL
);

-- ── bottles ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bottles (
    bottle_id       TEXT PRIMARY KEY,
    shelf           TEXT NOT NULL,
    row             TEXT NOT NULL,
    col             INTEGER NOT NULL,
    batch_id        INTEGER REFERENCES batches(id),
    species         TEXT DEFAULT '',
    treatment       TEXT DEFAULT '',
    date_planted    TEXT DEFAULT '',
    notes           TEXT DEFAULT '',
    cultivar        TEXT DEFAULT '',
    media_formula   TEXT DEFAULT '',
    pgr_detail      TEXT DEFAULT '',
    passage_number  INTEGER DEFAULT 1,
    emergence_date  TEXT DEFAULT ''
);

-- ── images ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS images (
    id                  BIGSERIAL PRIMARY KEY,
    bottle_id           TEXT NOT NULL REFERENCES bottles(bottle_id),
    batch_id            INTEGER REFERENCES batches(id),
    day_point           INTEGER NOT NULL,
    date_taken          TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'unknown',
    source              TEXT DEFAULT 'desktop',   -- 'mobile' | 'desktop'
    storage_path        TEXT DEFAULT '',           -- Supabase Storage path
    drive_file_id       TEXT DEFAULT '',
    drive_url           TEXT DEFAULT '',
    local_path          TEXT DEFAULT '',
    shoot_count         INTEGER DEFAULT -1,
    media_color         TEXT DEFAULT 'normal',
    hyperhydricity      INTEGER DEFAULT 0,
    has_roots           INTEGER DEFAULT 0,
    ai_status           TEXT DEFAULT '',
    ai_confidence       REAL DEFAULT 0.0,
    shoot_height_class  TEXT DEFAULT '',
    root_density        TEXT DEFAULT 'none',
    callus_present      INTEGER DEFAULT 0,
    dev_stage           TEXT DEFAULT '',
    vigor_score         REAL DEFAULT 0,
    green_coverage_pct  REAL,
    leaf_color_index    REAL,
    shoot_count_cv      INTEGER,
    media_color_cv      TEXT DEFAULT '',
    phenotype_method    TEXT DEFAULT '',
    texture_entropy     REAL,
    brown_coverage_pct  REAL,
    convex_hull_ratio   REAL,
    exg_mean            REAL,
    vari_mean           REAL,
    glcm_contrast       REAL,
    glcm_homogeneity    REAL,
    specular_fraction   REAL,
    ngrdi_mean          REAL,
    cive_mean           REAL,
    phenotyped          BOOLEAN DEFAULT FALSE,
    synced_local        BOOLEAN DEFAULT FALSE
);

-- ── expert_scores ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS expert_scores (
    id               BIGSERIAL PRIMARY KEY,
    image_id         INTEGER NOT NULL REFERENCES images(id),
    rater_id         TEXT NOT NULL,
    vigor_grade      INTEGER NOT NULL,
    hyperhydric_flag INTEGER DEFAULT 0,
    dev_stage_check  TEXT DEFAULT '',
    notes            TEXT DEFAULT '',
    ts               TEXT NOT NULL
);

-- ── Indexes ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_images_bottle  ON images(bottle_id);
CREATE INDEX IF NOT EXISTS idx_images_batch   ON images(batch_id);
CREATE INDEX IF NOT EXISTS idx_images_source  ON images(source, synced_local);
CREATE INDEX IF NOT EXISTS idx_expert_image   ON expert_scores(image_id);

-- ── Seed 100 bottles (S01/S02 × A-E × 01-10) ─────────────────────────────────
INSERT INTO bottles (bottle_id, shelf, row, col)
SELECT
    s.shelf || '-' || r.row_letter || '-' || LPAD(c.col_num::text, 2, '0'),
    s.shelf, r.row_letter, c.col_num
FROM
    (VALUES ('S01'),('S02')) AS s(shelf),
    (VALUES ('A'),('B'),('C'),('D'),('E')) AS r(row_letter),
    generate_series(1, 10) AS c(col_num)
ON CONFLICT (bottle_id) DO NOTHING;

-- ── Seed Batch 1 ──────────────────────────────────────────────────────────────
INSERT INTO batches (name, round_type, start_date, sow_date, notes, created_at)
VALUES (
    'Batch 1', 'training', '2026-06-22', '2026-06-22',
    'Capsicum frutescens cv.Phrik Jinda | A=MS B=BAP1 C=BAP5 D=BAP5+NAA E=IBA1 | 20 bottles/formula | 125mL jar',
    '2026-06-24 16:00'
)
ON CONFLICT DO NOTHING;

-- ── Link bottles to batch 1 ───────────────────────────────────────────────────
UPDATE bottles SET batch_id = (SELECT id FROM batches WHERE name = 'Batch 1' LIMIT 1);

-- ── Storage bucket (run separately if needed) ─────────────────────────────────
-- ไปที่ Storage → New bucket → ชื่อ "photos" → Public: ON
-- (ทำใน Dashboard ไม่ใช่ SQL)

-- ── Row Level Security (ปิดไว้ก่อนสำหรับการพัฒนา) ──────────────────────────
ALTER TABLE bottles       DISABLE ROW LEVEL SECURITY;
ALTER TABLE batches       DISABLE ROW LEVEL SECURITY;
ALTER TABLE images        DISABLE ROW LEVEL SECURITY;
ALTER TABLE expert_scores DISABLE ROW LEVEL SECURITY;
