-- VitroVision — Row Level Security
-- วิธีใช้: Supabase Dashboard → SQL Editor → New query → paste → Run

-- เปิด RLS ทุก table
ALTER TABLE bottles       ENABLE ROW LEVEL SECURITY;
ALTER TABLE batches       ENABLE ROW LEVEL SECURITY;
ALTER TABLE images        ENABLE ROW LEVEL SECURITY;
ALTER TABLE expert_scores ENABLE ROW LEVEL SECURITY;

-- bottles: อ่านได้ ห้ามแก้/ลบ
CREATE POLICY "anon_read_bottles"  ON bottles FOR SELECT USING (true);

-- batches: อ่านได้ ห้ามแก้/ลบ
CREATE POLICY "anon_read_batches"  ON batches FOR SELECT USING (true);

-- images: อ่านได้ + เพิ่มได้ (mobile capture) + แก้ได้ (update phenotype)
CREATE POLICY "anon_read_images"   ON images FOR SELECT USING (true);
CREATE POLICY "anon_insert_images" ON images FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_images" ON images FOR UPDATE USING (true);

-- expert_scores: อ่านได้ + เพิ่มได้
CREATE POLICY "anon_read_scores"   ON expert_scores FOR SELECT USING (true);
CREATE POLICY "anon_insert_scores" ON expert_scores FOR INSERT WITH CHECK (true);
