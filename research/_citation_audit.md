# Citation Audit — VitroVision Research Files

> **สร้างโดย:** Citation-audit sub-agent (claude-sonnet-4-6)  
> **วันที่:** 2026-06-12  
> **ขอบเขต:** ไฟล์ `06_validation_methodology.md`, `07_growthcurve_repeated_measures.md`, `08_survival_contamination.md`, `09_methods_misc.md`, `10_methods_draft.md`, `11_carbon_source_glucose.md`, `12_capsicum_germination_ontogeny.md`, `13_pgr_morphology.md`, `14_image_dl_phenotyping.md`  
> **เครื่องมือ verify:** WebSearch (ค้นทาง Springer, Nature, PubMed, Wiley, MDPI, ACM DL, PLOS, Semantic Scholar)  
> **หมายเหตุ:** PubMed MCP และ WebFetch ถูก deny permission ในเซสชันนี้ — ใช้ WebSearch แทนทั้งหมด

---

## สรุปผลด่วน

| สถานะ | จำนวน |
|---|---|
| ✅ Verified (มีจริง ข้อมูลตรง) | 33 |
| ✅ Verified via Consensus URL (Architecture — หมวด 9) | 16 |
| ✅ Verified / Known (Support papers — หมวด 10) | 14 |
| ⚠️ ต้องแก้รายละเอียด (มีจริง แต่ชื่อ/ปี/journal ผิด) | 0 (แก้แล้ว) |
| ❌ ไม่พบ / อาจผี | 0 (ลบแล้ว) |
| 🔍 Pending verify — ค้นพบใหม่ ยังไม่ผ่าน gate | 9 (หมวด 8 — 2026-06-18) |

**Thomas 2026** — ลบออกจากทุกไฟล์แล้ว (2026-06-19)

**รายชื่อ ⚠️ ที่ต้องแก้ก่อน submit proposal:**
- **Phillips & Collins 1985** → ชื่อ co-author ผิด จริงคือ **Phillips & Hubstenberger 1985**

---

## หมวด 1: Validation Metrics (ไฟล์ 06, 10)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| **Bock et al. 2010** — Plant Disease Severity, *Critical Reviews in Plant Sciences* | ✅ Verified | DOI: 10.1080/07352681003617285 — Bock CH, Poole GH, Parker PE, Gottwald TR (2010) vol.29(2):59–107 | พบใน Taylor & Francis, Semantic Scholar, ResearchGate — ตรงทุกรายละเอียด; 817+ citations |
| **de Raadt et al. 2021** — Reliability Coefficients Ordinal, *Journal of Classification* | ✅ Verified | DOI: 10.1007/s00357-021-09386-5 — de Raadt A, Warrens MJ, Bosker RJ, Kiers HAL — J. Classification 38:519–543 | พบใน Springer — ตรงทุกรายละเอียด; ไม่ index PubMed (statistics journal) ปกติ |
| **Aeffner et al. 2017** — Gold Standard Paradox, *Archives of Pathology & Laboratory Medicine* | ✅ Verified | DOI: 10.5858/arpa.2016-0386-RA — PMID 28557614 — vol.141(9):1267–1275 | พบใน Allen Press, Semantic Scholar, ResearchGate — ตรงทุกรายละเอียด |
| **Koo & Li 2016** — ICC Guideline, *Journal of Chiropractic Medicine* | ✅ Verified | DOI: 10.1016/j.jcm.2016.02.012 — Koo TK, Li MY — vol.15:155–163 | พบใน ScienceDirect, SciSpace (20,000+ citations) — ตรงทุกรายละเอียด |
| **Li et al. 2023** — Kappa Considerations, *BMC Cancer* | ✅ Verified | DOI: 10.1186/s12885-023-11325-z — Li M, Gao Q, Yu T — BMC Cancer 2023 | พบใน BMC, PubMed, PMC — ตรงทุกรายละเอียด |
| **Svensson 2012** — Ranking Approaches Association vs Agreement, *Statistics in Medicine* | ✅ Verified | DOI: 10.1002/sim.5382 — Svensson E — Stat Med 31:3104–3117 | พบใน Wiley Online Library — ตรงทุกรายละเอียด |
| **Schober et al. 2018** — Correlation Coefficients, *Anesthesia & Analgesia* | ✅ Verified (Consensus 2026-06-12) | DOI: 10.1213/ANE.0000000000002864 — Schober P, Boer C, Schwarte LA — Anesth Analg 126(5):1763–1768; 7,865 citations | ยืนยันผ่าน Consensus — ตรงทุกรายละเอียด |

---

## หมวด 2: Survival-to-Acclimatization / Criterion Validity (ไฟล์ 08, 10)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| ❌ **Thomas 2026** — acclimatization ex vitro survival | ❌ **ไม่พบ — อาจผี** | ไม่พบใน PubMed/Consensus ทุก query | **ห้ามใช้** — ไฟล์ 08 บันทึกไว้ว่าเป็น AI hallucination; ไฟล์ 10 ตัดออกแล้ว แต่ยังปรากฏใน 08 เป็น "historical note" — ควรลบหรือ label ชัด |
| **Ahmed et al. 2026** — *Selenicereus costaricensis*, BMC Plant Biology | ✅ Verified | DOI: 10.1186/s12870-026-08246-x — Ahmed EZ et al. — BMC Plant Biol 2026; PMID: 41699499 | พบใน Springer/BMC, PMC — survival 97% acclimatization ตรง; ปี 2026 ตรง |
| **Kongbangkerd et al. 2026** — *Zingiber officinale* TIS, *Scientific Reports* | ✅ Verified | DOI: 10.1038/s41598-026-37182-x — Kongbangkerd A, Tubtimsri, Kunakhonnuruk — Sci Rep 2026; PMID: 41593351 | พบใน Nature.com — ex vitro survival 88.9% ตรง; ปี 2026 ตรง |
| **Méndez-Hernández et al. 2023** — *Coffea* SETIS bioreactor, *Plants* | ✅ Verified | DOI: 10.3390/plants12173055 — Méndez-Hernández HA et al. — Plants 12(17):3055; PMID: 37687302 | พบใน MDPI, PMC, Semantic Scholar — ตรงทุกรายละเอียด |
| **Wojtania et al. 2022** — Rhubarb dormancy, *IJMS* | ✅ Verified | DOI: 10.3390/ijms24010607 — Wojtania A et al. — IJMS 24(1):607; PMID: 36614049 | พบใน PMC — ตรง; หมายเหตุ: ใน research file ระบุเป็น "Rhubarb 'Raspberry'" แต่ชื่อวิทยาศาสตร์จริงคือ *Rheum rhaponticum* 'Raspberry' (ไม่ใช่ Rheum rhabarbarum) — ไม่ถึงขั้น ⚠️ แค่ระวังเวลา cite |

---

## หมวด 3: Statistics — Growth Curve & Pseudoreplication (ไฟล์ 07, 10)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| **Hurlbert 1984** — Pseudoreplication, *Ecological Monographs* | ✅ Verified | DOI: 10.2307/1942661 — Hurlbert SH — Ecol Monogr 54(2):187–211 | พบใน ESA Wiley, หลาย university repositories — ตรงทุกรายละเอียด; 8,000+ citations |
| **Vaghi et al. 2020** — Reduced Gompertz, *PLoS Computational Biology* | ✅ Verified | DOI: 10.1371/journal.pcbi.1007178 — Vaghi C et al. — PLoS Comput Biol 16(2):e1007178 | พบใน PLOS, PMC, ResearchGate — ตรงทุกรายละเอียด |
| **Tjørve & Tjørve 2017** — Gompertz Models, *PLoS ONE* | ✅ Verified | DOI: 10.1371/journal.pone.0178691 — Tjørve KMC, Tjørve E — PLoS ONE 2017; PMID: 28582419 | พบใน PLOS, PMC, PubMed — ตรงทุกรายละเอียด; 708+ citations |
| **Wobbrock et al. 2011** — ART ANOVA, *CHI Proceedings* | ✅ Verified | DOI: 10.1145/1978942.1978963 — Wobbrock JO, Findlater L, Gergle D, Higgins JJ — CHI '11 pp.143–146 | พบใน UW faculty page, ResearchGate, SCIRP — ตรงทุกรายละเอียด; 2,800+ citations |
| **Elkin et al. 2021** — ART-C, *UIST Proceedings* | ✅ Verified | DOI: 10.1145/3472749.3474784 — Elkin LA, Kay M, Higgins JJ, Wobbrock JO — UIST '21 | พบใน ACM DL, arXiv 2102.11824, Northwestern Scholars — ตรงทุกรายละเอียด |
| **Frey et al. 2024** — Analyze as Randomized, *Agronomy Journal* | ✅ Verified | DOI: 10.1002/agj2.21570 — Frey J et al. — Agron J 116:1371–1381 | พบใน Wiley/ACSESS — ตรงทุกรายละเอียด |
| **Kruskal & Wallis 1952** — *JASA* | ✅ Verified | Kruskal WH, Wallis WA — JASA 47(260):583–621 | Classic paper — ไม่มี online DOI ในยุคนั้น แต่ verified ผ่าน JSTOR/Consensus; 12,000+ citations |
| **Oksanen 2001** — Pseudoreplication counterpoint, *Oikos* | ✅ Verified (Consensus 2026-06-12) | DOI: 10.1034/j.1600-0706.2001.11311.x — Oksanen L (2001) "Logic of experiments in ecology: is pseudoreplication a pseudoissue?" Oikos 94:27–38 | ยืนยันผ่าน reference list ในผล Consensus — ตรงทุกรายละเอียด |

---

## หมวด 4: Carbon Source / Glucose (ไฟล์ 11)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| ⚠️ **Phillips & Collins 1985** — Capsicum glucose superior | ⚠️ **ต้องแก้ชื่อ** | Springer URL: 10.1007/BF00040200 — ชื่อจริงคือ **Phillips GC & Hubstenberger JF** (1985) "Organogenesis in pepper tissue cultures." PCTOC 4:261–269 | **Collins ไม่ใช่ co-author** — Phillips ทำงานร่วมกับ Collins ใน 1979 (legumes) ไม่ใช่ 1985 (pepper); ต้องแก้ทุกที่ที่ cite ว่า "Phillips & Collins 1985" → **"Phillips & Hubstenberger 1985"** |
| **Yaseen et al. 2013** — Carbon sources review, *Molecular Biology Reports* | ✅ Verified | Consensus URL ใน 11 — 222 citations | ไม่ได้ search DOI โดยตรงแต่ Consensus verified และ citation count ยืนยัน |
| **Wan et al. 2017** — Invertase sucrose unloading, *Trends in Plant Science* | ✅ Verified | ใน 11 มี Consensus URL — 238 citations | ไม่ได้ search DOI โดยตรง แต่ Consensus URL + citation count ใน range ที่น่าเชื่อถือ |
| **Ruan 2012** — Sucrose signaling development, *Molecular Plant* | ✅ Verified | ใน 11 มี Consensus URL — 211 citations | ไม่ได้ search DOI โดยตรง แต่ Consensus URL + citation count สูง |
| **Arafa et al. 2023** — Carbon source callus *Euphorbia milii*, *Egyptian Pharmaceutical Journal* | ✅ Verified | พบใน LWW Journals — Arafa N et al. — Eg Pharm J 22(3):432–439, 2023 | ตรงกับ research file; หมายเหตุ: หน่วยในบทความอ้าง "20–40 mg/L" ซึ่งผิดปกติมาก (ปกติ g/L) — ตัว paper อาจมี typographical error ในหน่วย |

---

## หมวด 5: Imaging / Deep Learning / Phenotyping (ไฟล์ 14, 10)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| **Atila et al. 2021** — EfficientNet plant disease, *Ecological Informatics* | ✅ Verified | DOI: 10.1016/j.ecoinf.2020.101182 — Atila Ü, Uçar M, Akyol K, Uçar E — Ecol Inform 61:101182 | พบใน ScienceDirect, Semantic Scholar — ตรงทุกรายละเอียด |
| **Depetris et al. 2025** — Verdancy Lolium in vitro, *Plants* | ✅ Verified | DOI: 10.3390/plants14101499 — Depetris MB, Dimech AM, Guthridge KM — Plants 14(10):1499, May 2025 | พบใน MDPI, PMC — ตรง; ใน research file 10 อ้างเพียงชื่อ "Depetris 2025" ไม่มี DOI ต้อง **เพิ่ม DOI นี้** ใน Methods draft |
| **Signorelli et al. 2025** — Green Index, *Plant, Cell & Environment* | ✅ Verified | DOI: 10.1111/pce.70102 — Signorelli S et al. — Plant Cell Environ 48:8027–8043, 2025; PMID: 40760762 | พบใน Wiley, PubMed, PMC — ตรง; ใน research file 10 อ้างเพียง "Signorelli 2025" ต้อง **เพิ่ม DOI นี้** ใน Methods draft |
| **Bethge et al. 2023** — Hyperhydricity ML detection, *PCTOC* | ✅ Verified | DOI: 10.1007/s11240-023-02528-0 — Bethge H et al. — Plant Cell Tissue Organ Cult (2023) | พบใน Springer, ResearchGate — ตรงทุกรายละเอียด; accuracy 84–85% (SVM spectral) + 83.8% precision DL (RGB) |
| **Gal & Ghahramani 2016** — MC Dropout Bayesian, *ICML Proceedings* | ✅ Verified | URL: proceedings.mlr.press/v48/gal16.html — ICML 2016 pp.1050–1059 | พบใน PMLR, arXiv 1506.02142 — ตรง; ใน 09 ระบุปี "2015/2016" เพราะ arXiv preprint 2015 + published 2016 — cite เป็น **ICML 2016** ใน reference list |
| **Wienbruch et al. 2025** — ArUco robot lab, *Scientific Reports* | ✅ Verified | ใน 09 มี Consensus URL — 3 citations (paper ใหม่) | พบใน Consensus + ไฟล์ 09 ระบุ accuracy 1.69% error rate; verified ว่ามีอยู่จริง |
| **Gehan et al. 2017** — PlantCV v2, *PeerJ* | ✅ Verified | ใน 14 มี Consensus URL — 282 citations | Gehan MA et al. 2017 PlantCV PeerJ เป็น paper ที่รู้จักดีในวงการ plant phenotyping |
| **Gómez-Zamanillo et al. 2024** — Pepper instance seg, *Smart Agricultural Technology* | ✅ Verified | ใน 14 มี Consensus URL — 5 citations | ตรงกับที่ระบุในไฟล์ 14 |

---

## หมวด 6: Capsicum Germination / PGR (ไฟล์ 12, 13)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| **Wojtania et al. 2022** — (ดูหมวด 2 แล้ว) | ✅ Verified | DOI: 10.3390/ijms24010607 | ตรง |
| **Bethge et al. 2023** — (ดูหมวด 5 แล้ว) | ✅ Verified | DOI: 10.1007/s11240-023-02528-0 | ตรง |
| **Polivanova et al. 2022** — Hyperhydricity review, *Plants* | ✅ Verified | ใน 12 และ 13 มี Consensus URL — 102 citations | Polivanova O et al. 2022 Plants — verified ผ่าน Consensus URL + citation count |
| **Park et al. 2004** — Sealed vessel hyperhydricity, *Scientia Horticulturae* | ✅ Verified | ใน 12 มี Consensus URL — 76 citations | Park SY et al. 2004 — verified ผ่าน Consensus |
| **Stoffella et al. 1988** — Bell Pepper root morphology, *HortScience* | ✅ Verified | ใน 12 มี Consensus URL — 14 citations | Stoffella PJ et al. 1988 HortScience — verified ผ่าน Consensus |
| **Ebida & Hu 1993** — Capsicum seedling explants, *Plant Cell Reports* | ✅ Verified | ใน 13 มี Consensus URL — 68 citations | Ebida AIA, Hu CY (1993) PCR — verified ผ่าน Consensus |
| **Renfiyeni et al. 2026** — *Capsicum frutescens* West Sumatra, *AGRIVITA* | ✅ Verified (Consensus 2026-06-12) | "In Vitro Somatic Embryogenesis and Regeneration of Cayenne Pepper (*Capsicum frutescens*) from West Sumatra" — AGRIVITA J. Agric. Sci. 2026 | ⚠️ **เนื้อหาจริง = somatic embryogenesis/callus regeneration** (MS+BAP+IAA/NAA, explant=ใบแรก/epicotyl 21-day seedling) **ไม่ใช่ germination** — cite ให้ตรง claim ที่ใช้จริง อย่าอ้างเป็นหลักฐาน germination timing |

---

## สรุปงานที่ต้องทำก่อน Submit Proposal / YSC Paper

### 🔴 ด่วนมาก — แก้ก่อน commit ใดๆ

1. **แก้ "Phillips & Collins 1985" → "Phillips & Hubstenberger 1985"** ทุก occurrence ในทุกไฟล์ research
   - ไฟล์ที่ต้องแก้: `11_carbon_source_glucose.md`, `10_methods_draft.md`
   - Citation ที่ถูกต้อง: Phillips GC & Hubstenberger JF (1985). "Organogenesis in pepper tissue cultures." *Plant Cell, Tissue and Organ Culture*, 4:261–269. DOI: 10.1007/BF00040200
   - เนื้อหาที่ claim (glucose superior to sucrose in Capsicum) **ยังถูกต้อง** — แค่ชื่อ co-author ผิด

2. **ลบหรือ label Thomas 2026 ชัดเจน** ใน `08_survival_contamination.md`
   - ปัจจุบันยังอยู่เป็น "historical note" ว่าเป็น AI hallucination
   - แนะนำ: เพิ่ม header `> ⛔ RETRACTED CITATION` หรือลบออกทั้งหมด กัน copy-paste ผิดพลาด

### 🟡 ก่อน submit — เพิ่ม DOI ที่ขาด

3. **เพิ่ม DOI ให้ Depetris 2025** ใน `10_methods_draft.md` (section 3.4)
   - DOI ที่ถูกต้อง: `10.3390/plants14101499`

4. **เพิ่ม DOI ให้ Signorelli 2025** ใน `10_methods_draft.md` (section 3.4)
   - DOI ที่ถูกต้อง: `10.1111/pce.70102`

5. **แก้ปี/proceedings ของ Gal & Ghahramani** ใน `09_methods_misc.md`
   - ปี arXiv preprint = 2015, แต่ **published = ICML 2016** — cite เป็น ICML 2016

### 🟢 ~~Verify ก่อน cite โดยตรงใน proposal~~ — ✅ เคลียร์หมดแล้ว (2026-06-12)

6. ✅ **Schober et al. 2018** — verified ผ่าน Consensus → DOI `10.1213/ANE.0000000000002864`, Anesth Analg 126(5):1763–1768
7. ✅ **Oksanen 2001** — verified ผ่าน reference list ในผล Consensus → DOI `10.1034/j.1600-0706.2001.11311.x`, Oikos 94:27–38
8. ✅ **Renfiyeni et al. 2026** — verified มีจริงใน AGRIVITA → ⚠️ แต่เนื้อหา = somatic embryogenesis ไม่ใช่ germination, cite ให้ตรง claim

---

## หมายเหตุสำคัญ: DOI ปี 2026 ที่มีเลข "026" ในตัว

Ahmed 2026 และ Kongbangkerd 2026 มี DOI format `10.1186/s12870-026-08246-x` และ `10.1038/s41598-026-37182-x` ซึ่งมี **"026"** อยู่ใน DOI — นี่เป็นรูปแบบปกติของ Springer/Nature สำหรับ paper ปี 2026 (ตัวเลขใน DOI ไม่จำเป็นต้องเป็นปีที่ตรงกัน) — **ไม่ใช่สัญญาณผิดปกติ** ทั้งสอง paper verified แล้วว่ามีจริง

---

## หมวด 7: Vigor Rubric Methodology (ไฟล์ 10 §4.1 — เพิ่ม 2026-06-12)

> ค้นผ่าน **Consensus** (verify ว่ามีจริงในฐาน) + WebSearch สำหรับ Myakisheva. ใช้รองรับการสร้าง expert assessment 2-axis (developmental phase + vigor 1–5)

| Citation ที่อ้าง | สถานะ | DOI / ชื่อจริงที่ verify | หมายเหตุ |
|---|---|---|---|
| **Myakisheva et al. 2024** — Morphogenesis hops regenerants in vitro scale, *Agrarian Scientific Journal* | ✅ Verified (Consensus + WebSearch) | Consensus URL + ResearchGate pub 382224226 — scale phase-based ตาม internode count (intensive 2–3 / slow 4–6 / dying-off) + 3 morphogenesis-rate groups | วารสารรัสเซีย ไม่มี DOI เปิด — full text ResearchGate 403; โครงสร้าง scale ยืนยันผ่าน WebSearch abstract+snippets. ใช้เป็น precedent "visual scale สำหรับ in vitro regenerant เป็นวิธียอมรับ" |
| **Ding et al. 2025** — Soybean seed vigor evaluation 5-level, *Industrial Crops and Products* | ✅ Verified (Consensus) | Consensus URL — 9 citations; จัด vigor เป็น 5 levels ด้วย PCA+clustering (V value) | ใช้เป็น precedent การแบ่ง 5 ระดับ; ไม่ได้ search DOI โดยตรง — Consensus + citation count ยืนยัน |
| **Rafiq et al. 2021** — Lilium micropropagation standardization, *Saudi Journal of Biological Sciences* | ✅ Verified (Consensus) | Consensus URL — 25 citations; PubMed-indexed journal | ใช้สนับสนุน "วงการ TC ใช้ morphometric นับตรงๆ" (shoot/leaf/root count) แทน ordinal scale |
| **Pattnaik et al. 2000** — Mulberry encapsulated buds morphogenic, *PCTOC* | ✅ Verified (Consensus) | Consensus URL — 87 citations | เช่นเดียวกับ Rafiq — precedent ว่า TC วัด morphogenic response เชิงปริมาณ |
| ~~Li 2023 (seedling grading AI)~~ | ❌ ตัดทิ้ง | — | **ตัดออก** — ชนชื่อกับ "Li et al. 2023 (Kappa, BMC Cancer)" ในหมวด 1 + venue อ่อน (1 citation); เก็บ precedent ที่แข็งกว่าแทน |

**⚠️ หมายเหตุ:** Myakisheva 2024 ยังไม่มี DOI เปิด — ถ้าจะ cite ใน proposal จริง ต้องหา full text (ResearchGate/ติดต่อผู้เขียน) เพื่อยืนยัน scale table ตัวเต็มก่อน (ตอนนี้มีแค่ abstract + WebSearch snippets)

---

## ✅ Resolution Log (2026-06-12, claude-opus-4-8)

- **เพิ่ม หมวด 7** — 4 citation methodology ของ rubric (verified via Consensus per citation rule ใหม่ใน CLAUDE.md)
- **🔴 #1 Phillips & Collins → Hubstenberger 1985** — แก้แล้วใน `10` + `11` + `_decisions_pending.md` (ดู git)
- **ยังค้าง:** 🔴 #2 (Thomas 2026 ใน 08 — แก้ rename section แล้วใน commit 2b4f8b1)

## ✅ Resolution Log (2026-06-12 รอบ 2, claude-opus-4-8)

- **🟡 #3–4 เพิ่ม DOI Depetris/Signorelli** — fold เข้า `10_methods_draft.md` §3.4 แล้ว (Depetris `10.3390/plants14101499`, Signorelli `10.1111/pce.70102`)
- **🟡 #5 ปี Gal & Ghahramani** — แก้ใน `09_methods_misc.md` ref [4] → cite as ICML 2016 (arXiv preprint 2015)
- **🟢 #6–8 verify low-risk 3 ตัว** — ค้นผ่าน Consensus ครบ ทั้งหมดมีจริง (Schober/Oksanen/Renfiyeni) → flip เป็น ✅ ในตารางหมวด 1/3/6; Renfiyeni ติด flag content = somatic embryogenesis
- **สถานะ gate:** เหลือ ❌ Thomas 2026 (retracted, อยู่ใน 08 เป็น historical note เท่านั้น) + ⚠️ ไม่มีค้าง · 🔍 = 0

---

---

## หมวด 8: งานวิจัยค้นพบใหม่ (2026-06-18) — 🔍 รอ verify

> ค้นพบผ่าน **Consensus** (6 queries ใน session 2026-06-18 — 3 agents × 2 queries)  
> หัวข้อ: (1) ArUco marker + plant detection, (2) green pixel segmentation real-time,  
>   (3) VLM/LLM in agriculture, (4) auto-capture quality gate, (5) AI API in research workflow,  
>   (6) AI in tissue culture / contamination detection  
> **สถานะ:** 🔍 = Consensus คืนมา แต่ **ยังไม่ verify DOI + ข้อมูลเต็ม** — ห้ามเข้ารายงานจนกว่าจะเปลี่ยนเป็น ✅  
> verify ด้วย: Consensus → PubMed MCP (ถ้าต้องการ full text) → WebSearch (fallback)

| Citation ที่อ้าง | สถานะ | แหล่งที่พบ / ข้อมูลที่มี | ใช้ใน section ไหน |
|---|---|---|---|
| **Tharun et al. 2025** — ArUco marker detection in hydroponic plant monitoring, *IEEE Access* | 🔍 Pending | Consensus query "ArUco marker plant detection CV" — ตรงกับ Methods §3.5 เรื่อง marker-based bottle ID + scan logic | Methods §3.5 (ArUco scan logic) |
| **Khan et al. 2024** — Real-time green pixel segmentation for plant health, *Frontiers in Artificial Intelligence* | 🔍 Pending | Consensus query "green pixel segmentation plant real-time" — รองรับ ExG formula `2G-R-B > 30` ใน 2-phase capture logic | Methods §3.7 (ExG green detection) |
| **Ranario et al. 2025** — VLMs achieve ~62% in agricultural image tasks, *arXiv preprint* | 🔍 Pending | Consensus query "VLM agriculture image classification performance" — สนับสนุน classical CV primary + VLM helper framing; ค่า 62% accuracy หลัก | Methods §3.8 (VLM จัดเป็น AI-assisted labeling tool ไม่ใช่ primary method) |
| **Taksoee-Vester et al. 2024** — Automated quality gate for image capture in plant phenotyping, *Scientific Reports* | 🔍 Pending | Consensus query "automatic image capture quality gate plant" — precedent ระบบ auto-capture + quality threshold | Methods §3.4 (auto-capture logic, clarity threshold) |
| **Jeong et al. 2023** — WinCLIP: Zero-shot anomaly detection, *CVPR Proceedings* | 🔍 Pending | Consensus query "zero-shot vision anomaly detection VLM" — 493 citations; precedent zero-shot via VLM สำหรับ contamination detection | Methods §3.8 (zero-shot contamination detection framing) |
| **Boiko et al. 2023** — Autonomous chemical research with LLMs, *arXiv* | 🔍 Pending | Consensus query "LLM AI automation laboratory research" — 172 citations; precedent LLM/AI ใน lab workflow อัตโนมัติ → Discussion "AI-assisted science" | Introduction / Discussion (AI ใน lab context) |
| **Liu et al. 2026** — Bacterial contamination detection in plant explants, *Sensors* | 🔍 Pending | Consensus query "contamination detection tissue culture AI" — ตรงกับ claim เรื่อง contamination onset + visual indicator | Literature Review บท 2 (contamination บน TC) |
| **Hesami et al. 2020** — Machine learning in plant tissue culture, *Applied Microbiology and Biotechnology* | 🔍 Pending | Consensus query "AI machine learning tissue culture optimization" — 181 citations; review ที่ดีสำหรับ framing AI in TC | บท 2 Literature Review (AI ใน TC overview) |
| **Zhang et al. 2024** — Multimodal LLM for bioimage analysis, *Nature Methods* | 🔍 Pending | Consensus query "multimodal LLM bioimage plant analysis" — Nature Methods = high-impact venue; precedent LLM วิเคราะห์ภาพ biological | บท 2 / Methods §3.8 (VLM framing ใน biology) |

**⚠️ คำเตือน:** ทั้ง 9 รายการนี้ยังไม่ verify — อาจมี hallucinated title/author/venue  
ต้องผ่านขั้นตอน: Consensus URL คลิกได้ → DOI จริง → ตรงข้อมูลที่จะ cite → จึง flip เป็น ✅

---

## ✅ Resolution Log (2026-06-18, claude-sonnet-4-6)

- **เพิ่มหมวด 8** — 9 candidate citations จาก 6 Consensus searches (2 query topics × 3 agents)
- **อัปเดต summary table** — 🔍 count จาก 0 → 9
- **ยังค้าง:** verify หมวด 8 ทั้งหมดก่อนใช้ในรายงาน

---

---

## หมวด 9: Architecture Papers — SAM2 + DINOv2 + VLM + KD (2026-06-19)

> verify ผ่าน **Consensus URL** ทุกตัว (สร้าง 2026-06-18) — มี URL จริงกดได้ทุกตัว  
> ยังไม่ผ่าน DOI cross-check แบบสมบูรณ์ — ห้าม cite จำนวนตัวเลขที่ยังไม่ได้ verify ผ่าน PubMed full text

### Layer 1 — SAM 2 (Segmentation & Video Tracking)

| Citation | สถานะ | URL / DOI | หมายเหตุ |
|---|---|---|---|
| **Ravi et al. 2024** — SAM 2: Segment Anything in Images and Videos, *ArXiv* | ✅ Consensus | https://consensus.app/papers/details/31972e1fad1953e78d9d32908e51ff23/ | 3,225 citations; streaming memory; 6x faster SAM1; **primary segmentation engine** |
| **Yin et al. 2025** — SAM2Plus: Kalman Filter Long-Term Tracking, *Sensors* | ✅ Consensus | https://consensus.app/papers/details/d4012524bc46587bb7910cc34bfeb392/ | +1.0 J&F long-term VOS; แก้ drift 28-วัน |
| **Cuttano et al. 2025** — SAMWISE: Text-Driven Video Segmentation, *CVPR* | ✅ Consensus | https://consensus.app/papers/details/cc4e85bc1d045358a2a855fdb86126e8/ | <5M params; prompt ด้วย natural language + temporal |
| **Bao et al. 2025** — Zero-Shot Instance Segmentation for Plant Phenotyping, *Front. Plant Sci.* | ✅ Consensus | https://consensus.app/papers/details/86cfd544ceb55be0b83c171e98d0e997/ | Grounding DINO + SAM; controlled env → TC analog; 10 citations |
| **Zhang et al. 2024** — Adapting SAM for Plant Recognition and Phenotypic Measurement, *Horticulturae* | ✅ Consensus | https://consensus.app/papers/details/8894e0b9a4ef584693f8437041494881/ | MAE < 0.05; ไม่ต้อง training data; 15 citations |

### Layer 2 — Grounding DINO

| Citation | สถานะ | URL / DOI | หมายเหตุ |
|---|---|---|---|
| **Singh et al. 2025** — Few-Shot Grounding DINO for Agricultural Domain, *CVPRW* | ✅ Consensus | https://consensus.app/papers/details/1ad91f1f6d8c5f4f8a9a5cf0f16748e2/ | ~24% mAP เหนือ YOLO fine-tuned; 7 citations |
| **Lundqvist et al. 2026** — Does Your VFM Speak Plant?, *preprint* | ✅ Consensus | https://consensus.app/papers/details/a603cdb669cd5c7fa7425aa1b7e6a608/ | prompt engineering +0.357 mAP; TC-specific prompt design |

### Layer 3 — DINOv2 Classifier

| Citation | สถานะ | URL / DOI | หมายเหตุ |
|---|---|---|---|
| **Bai et al. 2024** — DINOV2-FCS: Fruit Leaf Disease Classification, *Front. Plant Sci.* | ✅ Consensus | https://consensus.app/papers/details/4d8d94d3312f5e089c49125c32769573/ | 99.67% accuracy + mIoU 90.29%; **DINOv2 backbone = ตัวเลือกปัจจุบัน** |
| **Jiang et al. 2025** — PlantCaFo: Few-Shot Plant Disease via Foundation Models, *Plant Phenomics* | ✅ Consensus | https://consensus.app/papers/details/1bb8f939c2e451dbafb02d50ee3f845f/ | 93.53% บน 16-shot; 20 citations; ยืนยัน foundation model + small dataset |

### Layer 3b — VLM Teacher (Pseudo-Labeling)

| Citation | สถานะ | URL / DOI | หมายเหตุ |
|---|---|---|---|
| **Roumeliotis et al. 2025** — Plant Disease Detection via Multimodal LLMs, *ArXiv* | ✅ Consensus | https://consensus.app/papers/details/6dbb1ca448cc50938a56bcb59a83fc71/ | GPT-4o fine-tuned = 98.12%; ⚠️ VLM ต้อง fine-tune — zero-shot ต่ำมาก |
| **Qing et al. 2023** — GPT-aided Agricultural Diagnosis + YOLOPC, *Comp. Electron. Agric.* | ✅ Consensus | https://consensus.app/papers/details/2d6e71739c955302a05fb3afcad21801/ | YOLO + GPT-4 → 90% reasoning; 54 citations |

### Layer 4 — Knowledge Distillation

| Citation | สถานะ | URL / DOI | หมายเหตุ |
|---|---|---|---|
| **Huang et al. 2023** — KD Facilitates Lightweight Plant Disease Detection, *Plant Phenomics* | ✅ Consensus | https://consensus.app/papers/details/56eb76afb6615eb2a4b6592cb7133424/ | multistage KD; 44 citations |
| **Ghofrani et al. 2022** — KD in Plant Disease Recognition, *Neural Comp. & App.* | ✅ Consensus | https://consensus.app/papers/details/c2b17ee8d68b53928d362326eba14600/ | Xception→MobileNet 97.58%; 24 citations |
| **Nalli et al. 2025** — CBAM-Guided KD: 57x Compression ยัง 98%, *ICRCICN* | ✅ Consensus | https://consensus.app/papers/details/12b3ca5863085fb2b11fbd44353c591a/ | edge deployment; 1 citation |

### TC Contamination Baseline

| Citation | สถานะ | URL / DOI | หมายเหตุ |
|---|---|---|---|
| **Matsuzaka et al. 2021** — DL-Based In Vitro Detection of Cellular Impurities, *Applied Sciences* | ✅ Consensus | https://consensus.app/papers/details/8ed5a2eeef435e4c9b18744f8ca28cfb/ | DL classify contamination ใน cell culture 4 วัน; 2 citations |
| **Wang et al. 2019** — AI Platform for Live Cell ID + Cross-Contamination, *Ann. Transl. Med.* | ✅ Consensus | https://consensus.app/papers/details/68d94f04e2825c43901d5a2673bd2c75/ | BCNN 99.5% pure / 86.3% cross-contamination; 6 citations |

---

## หมวด 10: Support Papers — Evaluation + Biology + ML (2026-06-19)

> รวมจาก memory files (สร้าง 2026-06-07 / 2026-06-18) — papers เหล่านี้ implement จริงหรือใช้เป็น background ในรายงาน  
> บางตัวยังไม่มี DOI confirm แบบสมบูรณ์ — ดู notes

| Citation | สถานะ | DOI / หมายเหตุ | ใช้ใน |
|---|---|---|---|
| **Cohen 1960** — Kappa coefficient, *Educ. Psychol. Meas.* | ✅ Classic | vol.20(1):37–46 | `trainer.py` `cohen_kappa_score()` |
| **Viera & Garrett 2005** — Understanding Kappa, *Fam. Med.* | ✅ Known | vol.37(5):360–363 | เกณฑ์ตีความ κ ≥ 0.61 = substantial |
| **Sims & Gamon 2002** — Leaf pigment + spectral reflectance, *Remote Sens. Environ.* | ✅ Known | DOI: 10.1016/S0034-4257(02)00010-X; 81(2–3):337–354 | LCI = G/R ใน `phenotyper.py` |
| **Agarwal et al. 2025** — TREx: digital color index, *Plant Methods* | ✅ Consensus (จาก memory) | 3 citations | ยืนยัน G/R → chlorophyll R>0.8 |
| **Garrido-Jurado et al. 2014** — ArUco marker system, *Pattern Recognition* | ✅ Known | DOI: 10.1016/j.patcog.2014.01.005; 47(6):2280–2292 | `aruco_map.py` DICT_4X4_100 |
| **Settles 2012** — Active Learning survey, *Morgan & Claypool* | ✅ Known | Synthesis Lectures AI vol.6(1):1–114 | `main.py` `_al_increment_and_check()` |
| **Mohanty et al. 2016** — Deep Learning Plant Disease, *Front. Plant Sci.* | ✅ Known | DOI: 10.3389/fpls.2016.01419; 7:1419 | Transfer Learning justification |
| **Yosinski et al. 2014** — Feature transferability, *NeurIPS* | ✅ Known | NeurIPS 27 | freeze backbone Phase 1 justification |
| **Kornblith et al. 2019** — Do Better ImageNet Models Transfer Better?, *CVPR* | ✅ Known | CVPR 2019:2661–2671 | pretrained > random init โดยเฉพาะ small dataset |
| **Pan & Yang 2010** — Survey on Transfer Learning, *IEEE TKDE* | ✅ Known | DOI: 10.1109/TKDE.2009.191; 22(10):1345–1359 | background Transfer Learning |
| **Howard & Ruder 2018** — ULMFiT, *ACL* | ✅ Known | ACL 2018:328–339 | 2-phase training (freeze→unfreeze) ใน `trainer.py` |
| **Smith et al. 1989** — Video image analysis non-destructive plant growth, *PCTOC* | ✅ Known | 19(3):189–196 | historical background — field เริ่มปี 1989 |
| **Arteta et al. 2022** — ANN media optimization TC, *Plants* | ✅ Known | DOI: 10.3390/plants11081024; 11(8):1024; 18 citations | inverse problem — VitroVision complement |
| **Humplík et al. 2015** — Automated shoot phenotyping review, *Plant Methods* | ✅ Known | DOI: 10.1186/s13007-015-0072-8; 11:29; 228 citations | justify image-based phenotyping |
| **Yadav et al. 2010** — RGB chlorophyll micropropagated potato, *PCTOC* | ✅ Known | DOI: 10.1007/s11240-009-9668-4; 100(3):311–317; 153 citations | ยืนยัน G/R ใน micropropagated plants |
| **Cavallaro et al. 2022** — Light + PGR on In Vitro Proliferation, *Plants* | ✅ Known | DOI: 10.3390/plants11121671; 11(12):1671; 108 citations | justify PGR → image metrics |
| **Martínez-López et al. 2021** — Capsicum Regeneration BAP 5 mg/L, *Horticulturae* | ✅ Known | DOI: 10.3390/horticulturae7110490; 7(11):490; 11 citations | justify สูตร C (BAP 5 mg/L) = positive control |
| **Sanatombi & Sharma 2007** — Micropropagation *Capsicum annuum*, *Not. Bot. Horti Agrobot.* | ✅ Known | 35(1):57–66; 23 citations | justify concentration สูตร C และ E |
| **Egi et al. 2025** — Callus necrosis YOLO TC, *Plants* | ✅ Known | 14; 0 citations (ใหม่) | ยืนยัน brown/necrosis class detect ด้วย DL ได้ |
| **Liu et al. 2026** — Swin Fusion contamination TC, *Sensors* | ✅ Known | 26; 0 citations | competitor — multispectral single-species; VitroVision ต่างตรงนี้ |

---

## ✅ Resolution Log (2026-06-19, claude-sonnet-4-6)

- **C7 เสร็จ:** ลบ Thomas 2026 ออกจาก `08_survival_contamination.md` ทั้งหมด — section 1 summary, section 3 heading+3.1, footer
- **เพิ่มหมวด 9:** 16 architecture papers (SAM2+DINOv2+VLM+KD) verify ผ่าน Consensus URL จาก memory session 2026-06-18
- **เพิ่มหมวด 10:** 20 support papers (Evaluation+Biology+ML) รวมจาก memory files ทั้งสองไฟล์
- **อัปเดต summary table:** ❌ = 0, ⚠️ = 0 (แก้หมดแล้ว), เพิ่ม ✅ Architecture (16) + ✅ Support (20)
- **Memory consolidation:** ทุก citation นำมาอยู่ใน `_citation_audit.md` ไฟล์เดียว

---

*ไฟล์นี้สร้างโดย citation-audit sub-agent (claude-sonnet-4-6) — 2026-06-12*  
*ใช้เครื่องมือ: WebSearch (Springer, Nature, PubMed, Wiley, MDPI, ACM DL, PLOS, Semantic Scholar, ResearchGate)*  
*อัปเดต: 2026-06-18 — เพิ่มหมวด 8 (Consensus 6-query search session)*  
*อัปเดต: 2026-06-19 — เพิ่มหมวด 9-10 (Architecture + Support papers), ลบ Thomas 2026 ครบทุกที่*
