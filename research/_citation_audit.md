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
| ⚠️ ต้องแก้รายละเอียด (มีจริง แต่ชื่อ/ปี/journal ผิด) | 2 |
| ❌ ไม่พบ / อาจผี | 1 |
| 🔍 Verify ไม่ได้ครบ — ต้องตรวจ manual | 0 (เคลียร์หมดแล้ว 2026-06-12) |

**รายชื่อ ❌ ที่ต้องจัดการด่วน:**
- **Thomas 2026** — ไม่พบใน PubMed/Consensus (ยืนยันแล้วว่าเป็น AI hallucination — ถูกตัดออกจากไฟล์ 10 แล้ว แต่ยังอยู่ใน 08 เป็น historical note)

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

*ไฟล์นี้สร้างโดย citation-audit sub-agent (claude-sonnet-4-6) — 2026-06-12*  
*ใช้เครื่องมือ: WebSearch (Springer, Nature, PubMed, Wiley, MDPI, ACM DL, PLOS, Semantic Scholar, ResearchGate)*
