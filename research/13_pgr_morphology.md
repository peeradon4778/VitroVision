# 13 — ผลของ Plant Growth Regulator (PGR) ต่อ Morphology ของพริกในหลอดทดลอง
> **วัตถุประสงค์:** คาดการณ์ phenotype ที่แตกต่างกันใน 5 สูตร MS (A–E) เพื่อเป็น ground truth ให้ระบบ CV ของ VitroVision จับความแตกต่างได้

---

## 1. สรุป — คาดการณ์ความต่าง Morphology ของ 5 สูตร

| สูตร | ส่วนผสมหลัก | ยอดต่อ explant | ความสูง/ปล้อง | ราก | ลักษณะใบ | ความเสี่ยง Hyperhydricity |
|------|------------|---------------|--------------|-----|----------|--------------------------|
| A — MS Control | ไม่มี PGR | ต่ำ (1–2) | ปกติ–ยาวกว่า | มีราก (endogenous auxin) | ปกติ สีเขียวเข้ม | ต่ำมาก |
| B — BAP 1 mg/L | cytokinin ต่ำ | ปานกลาง (2–4) | ปกติ–ค่อนข้างสั้น | น้อยลง | ปกติ–สมบูรณ์ดี | ต่ำ |
| C — BAP 5 mg/L | cytokinin สูง | สูง (3–8+) | สั้น ปล้องถี่ | น้อยมาก | เล็ก บิดงอ หรือ glassy ได้ | สูง |
| D — BAP 5 + NAA 0.05 | cytokinin สูง + auxin ต่ำ | สูง (3–6) | สั้น–ปานกลาง | ปานกลาง | เล็ก–ปกติ อาจมี callus โคนต้น | ปานกลาง |
| E — IBA 1 mg/L | auxin เด่น ไม่มี cytokinin | ต่ำ (1–2) | ปกติ–สูง | สูง รากยาว หนา | ปกติ–สีเขียวสม่ำเสมอ | ต่ำมาก |

**ความต่างที่เด่นที่สุดสำหรับ CV:**
- **C vs A/E:** ยอดเยอะ ต้นเตี้ย ใบเล็ก — ต่างชัดเจนทาง morphology
- **E vs B/C:** รากชัดเจน ไม่มียอดหลายยอด
- **C (รุนแรง) → Hyperhydricity:** ใบโปร่งแสง/glassy สีซีด — phenotype พิเศษสำหรับ CV class

---

## 2. Cytokinin Effects — BAP ต่อ Morphology ของ Capsicum in vitro

### 2.1 Multiple Shoot Induction
BAP เป็น cytokinin สังเคราะห์ที่นิยมใช้มากที่สุดใน Capsicum tissue culture [3] การศึกษาของ Ebida & Hu (1993) พบว่าใน *Capsicum annuum* cv. Early California Wonder — BAP 5.0 mg/L ± NAA 0.1 mg/L ให้ multiple shoot-buds จาก cotyledon, shoot-tip และ hypocotyl explants ได้ดีที่สุด และ 70% ของ shoot-buds สามารถออกรากได้เมื่อย้ายไปสูตรที่มี IAA หรือ NAA [3]

งานของ Martínez-López et al. (2021) ยืนยันว่า BAP 5 mg/L (สูตร Pep1) ให้ผล shoot regeneration ดีที่สุดใน *C. annuum* และ *C. baccatum* ในลักษณะ direct organogenesis [2] และ Renfiyeni et al. (2026) พบว่าใน *Capsicum frutescens* สูตร MS + 2 mg/L BAP + 1 mg/L NAA ให้ค่าเฉลี่ย 5.29 shoots/explant [1]

### 2.2 Shoot Elongation และ Internode Length
cytokinin สูง (BAP ≥ 3 mg/L) มีแนวโน้มลด shoot elongation และทำให้ปล้องสั้นลง (stunted internodes) งานกับ *Humulus lupulus* แสดงว่า BAP ≥ 1 mg/L ลดการเจริญเติบโตโดยรวมและเพิ่ม callus formation และ hyperhydricity [C1] ใน *Quercus robur*, BAP ทำให้เกิด underdeveloped leaf anatomy, shoot-tip necrosis และลดปริมาณ phenolic compounds [C2] — ผลนี้น่าจะเกิดขึ้นใน Capsicum ด้วย โดยเฉพาะสูตร C (BAP 5 mg/L)

### 2.3 Leaf Morphology
- ใบมีแนวโน้มเล็กลง บิดงอ หรือ underdeveloped เมื่อ BAP สูง [C2]
- สีใบอาจซีดลง (ลด chlorophyll/phenolic) ต่างกับ control ที่ใบเขียวเข้ม
- ที่ BAP สูงมาก (สูตร C) อาจเกิด hyperhydric leaves (ดูหัวข้อ 4)

### 2.4 Apical Dominance
cytokinin ทำลาย apical dominance → กระตุ้น axillary bud break → multiple shoots [Skoog & Miller, 1957 revisited by Melnyk 2023] [S1] ดังนั้น:
- **สูตร A (control):** apical dominance เต็มที่ → ต้นเดี่ยว ยืดสูง
- **สูตร B (BAP 1):** apical dominance ลดลง → 2–4 shoots
- **สูตร C (BAP 5):** apical dominance ถูก suppress อย่างมาก → multiple shoots cluster

---

## 3. Auxin Effects — NAA และ IBA ต่อ Morphology ของ Capsicum in vitro

### 3.1 Root Induction
auxin เป็นตัวกระตุ้นหลักสำหรับ root initiation การศึกษา Gunay & Rao (1978) พบว่า root regeneration ใน Capsicum เกิดในสูตรที่มี IAA หรือ NAA แต่ไม่เกิดในสูตร 2,4-D สูง [R1] IBA เป็น auxin ที่นิยมใช้สำหรับ rooting เพราะ stable และ lipophilic — ช่วยให้รากยาวและหนา

สูตร **E (IBA 1 mg/L):** คาดว่าจะเห็น root system ที่ชัดเจน รากยาว อาจมีหลายราก — phenotype ที่โดดเด่นมากเมื่อดูผ่านขวด

### 3.2 Callus Formation
auxin สูง (NAA ≥ 0.5–1 mg/L) หรือ 2,4-D กระตุ้น callus มากกว่า shoot Rakshit et al. (2008) รายงานว่า NAA 2.0 mg/L + 2,4-D ให้ callus ดีที่สุดใน *C. annuum* [R2] สำหรับสูตร **D (BAP 5 + NAA 0.05)** — NAA ต่ำมาก (0.05 mg/L) ไม่น่าทำให้เกิด callus มาก แต่ช่วย balance auxin:cytokinin ratio ให้ shoot regeneration ดีขึ้นและลดความเสี่ยง hyperhydricity เมื่อเทียบกับสูตร C

### 3.3 Shoot-Root Balance
| auxin level | cytokinin level | ผลที่คาด |
|-------------|-----------------|----------|
| ต่ำ/ไม่มี | สูง (BAP 5) | multiple shoots, ไม่มีราก (สูตร C) |
| ต่ำ (NAA 0.05) | สูง (BAP 5) | multiple shoots + ราก บ้าง (สูตร D) |
| ต่ำ/ไม่มี | ต่ำ (BAP 1) | 2–4 shoots + ราก บ้าง (สูตร B) |
| สูง (IBA 1) | ไม่มี | 1–2 shoots + ราก ชัดเจน (สูตร E) |
| endogenous เท่านั้น | endogenous | ต้นปกติ + ราก (สูตร A) |

---

## 4. Hyperhydricity = Phenotype สำคัญที่ CV ควรจับ

### 4.1 ความหมายและสาเหตุ
Hyperhydricity (เดิมเรียก vitrification) คือความผิดปกติทาง physiological ที่พบบ่อยที่สุดใน plant tissue culture [H1] เกิดจาก waterlogging ของ apoplast → hypoxia → oxidative stress [H3] ปัจจัยสำคัญคือ:
- **cytokinin สูงเกินไป** (เช่น BAP 5 mg/L โดยไม่มี balance) [H1, H2]
- การระบายอากาศในขวดไม่ดี
- ความชื้นสูงในขวด

### 4.2 ลักษณะภายนอกที่ CV สามารถตรวจจับได้ (External Visual Phenotype)

| ลักษณะ | รายละเอียด | ตรวจได้ผ่านขวด |
|--------|-----------|----------------|
| ใบ glassy/translucent | ใบโปร่งแสง คล้ายแก้ว เนื่องจากน้ำสะสมใน mesophyll | ใช่ — ความแตกต่าง texture/brightness ชัด |
| ใบสีซีด/เหลือง | chlorophyll ลด pigmentation ลด | ใช่ — color analysis โดย CV |
| ใบบวมน้ำ / succulent | เนื้อใบหนา ฉ่ำน้ำ ผิวไม่เรียบ | ใช่ — texture feature |
| ลำต้นบวม / กลม | internode พองขึ้น | ใช่ — shape feature |
| ใบม้วน/บิด (wrinkled) | ผิวใบไม่เรียบ ขอบม้วน | ใช่ — edge/contour feature |
| ขนาดใบเล็กมาก | leaf area ลดลงอย่างมาก | ใช่ — size metric |
| shoot cluster แน่น | ยอดหลายยอดแออัด ไม่ยืดตัว | ใช่ — density/count feature |

Bethge et al. (2023) พิสูจน์ว่า ML สามารถ classify hyperhydricity จาก visual/spectral features ได้แม่นยำ 85% โดยใช้ reflectance spectra — เป็น precedent สำคัญสำหรับ VitroVision [H2]

### 4.3 ความเสี่ยงของแต่ละสูตร
- **สูตร C (BAP 5):** ความเสี่ยง **สูงที่สุด** — cytokinin เด่น ไม่มี auxin balance
- **สูตร D (BAP 5 + NAA 0.05):** ความเสี่ยง **ปานกลาง** — NAA เล็กน้อยช่วย balance
- **สูตร B (BAP 1):** ความเสี่ยง **ต่ำ** — cytokinin พอประมาณ
- **สูตร A, E:** ความเสี่ยง **ต่ำมาก** — ไม่มีหรือมี cytokinin น้อยมาก

---

## 5. External vs Internal Differences — CV เห็นแค่ External

### 5.1 สิ่งที่ CV มองเห็นผ่านขวดแก้ว
- **ใบ:** ขนาด สี texture (glassy vs matte) รูปร่าง การม้วน
- **ยอด:** จำนวน shoot ขนาด การเรียงตัว ความหนาแน่น
- **ลำต้น:** ความสูง ปล้อง ความตรง ขนาดเส้นผ่านศูนย์กลาง
- **ราก:** การมีอยู่/ไม่มี ความยาว ความหนา สี ปริมาณ
- **สี:** เขียวเข้ม vs ซีด vs เหลือง vs โปร่งแสง
- **Callus:** ก้อนสีเหลือง/ขาว/น้ำตาลที่โคนต้น

### 5.2 สิ่งที่ CV ไม่เห็น (Internal — ต้องใช้ microscopy/biochemistry)
- stomata density, stomata opening/closing
- mesophyll cell structure, cell wall thickness
- cuticle layer development (ลดใน hyperhydric plants)
- chloroplast ultrastructure
- xylem/phloem differentiation
- endogenous hormone levels

**นัยสำคัญ:** CV ของ VitroVision ต้องอาศัย external proxy ของ internal disorder — เช่น ความ glassy ของใบ เป็น proxy ของ excess apoplastic water [H3] ซึ่งงานของ Bethge et al. (2023) พิสูจน์ว่าทำได้จริง [H2]

---

## 6. References

### Capsicum Tissue Culture & PGR
[1] [In Vitro Somatic Embryogenesis and Regeneration of Cayenne Pepper (Capsicum frutescens) from West Sumatra](https://consensus.app/papers/details/7dba885853c45105a45cab1a013d8c11/?utm_source=claude_code) (R. Renfiyeni et al., 2026, AGRIVITA Journal of Agricultural Science)

[2] [Screening of Suitable Plant Regeneration Protocols for Several Capsicum spp. through Direct Organogenesis](https://consensus.app/papers/details/d61b54c194a75d598fb47ee91e8d1dcf/?utm_source=claude_code) (Marina Martínez-López et al., 2021, 11 citations, Horticulturae)

[3] [In vitro morphogenetic responses and plant regeneration from pepper (Capsicum annuum L. cv. Early California Wonder) seedling explants](https://consensus.app/papers/details/7780cdc7cf725fafb4701cf189f9ee4e/?utm_source=claude_code) (Aly I. A. Ebida & Hu, 1993, 68 citations, Plant Cell Reports)

[R1] [In vitro plant regeneration from hypocotyl and cotyledon explants of red pepper (capsicum)](https://consensus.app/papers/details/3079f5835e6e5f5c819637558dcd475b/?utm_source=claude_code) (A. Gunay & Rao, 1978, 133 citations, Plant Science Letters)

[R2] [Effect of different explant and hormones on in vitro callus induction and regeneration of pepper (Capsicum annuum L.)](https://consensus.app/papers/details/82097077f26c5c4cb0365138aaf4ca45/?utm_source=claude_code) (A. Rakshit et al., 2008, AGRIS)

### Cytokinin Effects (General — ใช้กับ Capsicum โดย analogy)
[C1] [Effect of different cytokinin concentrations on establishing an in vitro micropropagation system for hop (Humulus lupulus L.)](https://consensus.app/papers/details/195ba156a74c51648fae63a8643e5569/?utm_source=claude_code) (E. Carloni et al., 2025, 2 citations, New Zealand Journal of Crop and Horticultural Science)

[C2] [6-Benzylaminopurine and kinetin modulations during in vitro propagation of Quercus robur (L.): an assessment of anatomical, biochemical, and physiological profiling of shoots](https://consensus.app/papers/details/e98247844367563c9c3c4ab910b4a68f/?utm_source=claude_code) (J. Martins et al., 2022, 36 citations, Plant Cell, Tissue and Organ Culture (PCTOC))

[C3] [Pluripotency acquisition in the middle cell layer of callus is required for organ regeneration](https://consensus.app/papers/details/11113e4c7ddd5ee79e27c3a401bf353a/?utm_source=claude_code) (Ning Zhai et al., 2021, 167 citations, Nature Plants)

### Skoog-Miller Principle
[S1] [Quantitative regeneration: Skoog and Miller revisited](https://consensus.app/papers/details/ff29e00fdee05ae190f0f9301d313ba4/?utm_source=claude_code) (Charles W. Melnyk, 2023, 14 citations, Quantitative Plant Biology)

### Hyperhydricity
[H1] [Hyperhydricity in Plant Tissue Culture](https://consensus.app/papers/details/7ba487e729365e3bb751a4a7cb57b0e1/?utm_source=claude_code) (O. Polivanova et al., 2022, 102 citations, Plants)

[H2] [Towards automated detection of hyperhydricity in plant in vitro culture](https://consensus.app/papers/details/5a5eb58a215a52a9bdc3e5314635467b/?utm_source=claude_code) (Hans Bethge et al., 2023, 12 citations, Plant Cell, Tissue and Organ Culture (PCTOC))

[H3] [The hyperhydricity syndrome: waterlogging of plant tissues as a major cause](https://consensus.app/papers/details/382b398d67f9544598ccd0ba2f28ce59/?utm_source=claude_code) (L. Martinez et al., 2010, 72 citations, Propagation of Ornamental Plants)

[H4] [Hyperhydricity Syndrome in In Vitro Plants: Mechanisms, Physiology, and Control](https://consensus.app/papers/details/f52f85cf6c6e5c809e48296ea825f5f7/?utm_source=claude_code) (Rajesh Barua et al., 2025, Plants)

---

*สร้างโดย VitroVision research sub-agent — 2026-06-11*
*ใช้ข้อมูลจาก Consensus Academic Search และ PubMed*

---

> **Create or connect a free Consensus account to return more than 3 results per search in Claude Code.:** https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
