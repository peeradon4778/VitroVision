# 02 — Media Formulations Review: PGR สำหรับ Capsicum annuum Tissue Culture

**โครงงาน:** VitroVision — Computational Phenotyping ของพริกเพาะเลี้ยงเนื้อเยื่อ
**เป้าหมาย:** YSC 2027 (CSBI) → ISEF
**วันที่:** 2026-06-11
**ขอบเขต:** ทบทวน literature เรื่องผลของสูตร MS + PGR ต่อการเจริญ และวิจารณ์การออกแบบ 5 สูตร × 20 ขวด

---

> ## ⚠️ หมายเหตุสำคัญ — ไฟล์นี้เขียน **ก่อน** lock design (อ่านก่อน)
> ไฟล์นี้เขียนวันเดียวกับการตัดสินใจ แต่ **ก่อน** Research Design v1 ถูก lock (2026-06-11). ข้อเสนอ "เปลี่ยน design" ทั้งหมดในไฟล์นี้ถูกพิจารณาแล้วและ **ตัดสินใจไม่นำมาใช้** ใน v1:
> - **5 สูตร A–E ตายตัว** — ไม่เพิ่ม BAP กลาง 2–3 mg/L (§2.2 ข้อ 2, §2.4 ข้อ 2), ไม่ยก NAA เป็น 0.1–0.5 (§2.2 ข้อ 3, §2.4 ข้อ 3), ไม่เพิ่มแขน TDZ/kinetin (§2.2 ข้อ 4, §2.4 ข้อ 4)
> - **n:** "20 ขวด/สูตร" ในไฟล์นี้ = **ต่อ batch** ไม่ใช่ total; decision v1 = **pool ≥2 batch → n≈40/สูตร** (over-sow ~24–25/สูตร/batch). ตัวเลข "100 ขวด" = ต่อ batch ไม่ใช่ total → power analysis §2.3 อ้าง assumption n=20 จึงเป็น **lower bound; ดู `10_methods_draft.md` §1.4 สำหรับ power analysis ฉบับสมบูรณ์ที่ n≈40**
> - **Post-hoc:** ข้อเสนอ "Dunn + Holm/BH" ในไฟล์นี้ถูก supersede — source of truth = `10_methods_draft.md`: **primary = LMM (ถ้า normal) หรือ ART-ANOVA + ART-C (ถ้าไม่ normal); Dunn + Bonferroni = secondary/preliminary เท่านั้น**
> - ข้อ critique เรื่อง confound (E คนละ stage, dose-response 2 จุด) ยังใช้ได้ → ระบุเป็น acknowledged limitation ในรายงาน
>
> *(ดู `_decisions_pending.md` §1 สำหรับ decision ที่ lock ครบ)*

---

## TL;DR (สรุปสั้น)

1. **BAP คือ cytokinin หลักสำหรับ shoot multiplication ในพริก** — literature ส่วนใหญ่ใช้ BAP 5 mg/L ขึ้นไป (บางสูตรถึง 8 mg/L) ในขั้น shoot induction [1][3][6][7][8][9].
2. **BAP สูง (5 mg/L) เพิ่ม "จำนวน" ยอด แต่ "ไม่ทำให้ยอดยืด" (elongation)** — ที่ 5 mg/L BAP ใน cv. mathania ยอดเพิ่มจำนวนแต่ไม่ elongate ต้องย้ายไป auxin ต่ำเพื่อยืด [3]. นี่คือ diminishing return รูปแบบหนึ่ง: ได้ปริมาณแต่เสียคุณภาพ.
3. **BAP ทำให้เกิด morphophysiological disorder เมื่อความเข้มข้นสูง** — underdeveloped leaves, shoot-tip necrosis, hyperhydricity, pigment ลด [13][14][15]. ในพริก/พืชใกล้เคียง topolin (mT) ให้ proliferation สูงกว่าและ hyperhydricity ต่ำกว่า BAP [10][11].
4. **C:A ratio (BAP:NAA) กำหนดทิศทาง**: BAP สูง + NAA ต่ำมาก → shoot; BAP กลาง + NAA → callus; auxin เด่น → root. ใน C. annuum, 2 mg/L BAP + 0.1 mg/L NAA เหมาะกับ **callus**, ส่วน BAP + IAA ต่ำเหมาะกับ shoot bud [6].
5. **IBA คือ auxin มาตรฐานสำหรับ rooting ในพริก** (0.5–1 mg/L) [1][6][7]; NAA/IBA สูงเร่ง root initiation แต่เสี่ยง callus ที่โคน [4][5].
6. **การออกแบบ 5 สูตรของเรา: โครงดี แต่มี confound ที่ต้องระวัง** — E (auxin เดี่ยว) เป็นคนละ stage กับ A–D (multiplication) ทำให้เปรียบเทียบตรงๆ ใน Kruskal-Wallis เดียวกันได้ไม่สะอาด และ dose-response ของ BAP มีแค่ 2 จุด (1 → 5 mg/L) ขาดจุดกลาง.
7. **n=20/สูตร เพียงพอสำหรับ Kruskal-Wallis** ในระดับ effect ปานกลาง-ใหญ่ที่ TC ทั่วไปเห็น แต่ contamination/missing จะลด effective n — ควรวางแผนเผื่อ.

---

## ส่วนที่ 1 — สูตร/PGR แบบไหนเร่งอะไรได้ดี (Capsicum + พืชใกล้เคียง)

### 1.1 BAP กับ shoot multiplication
ในพริก BAP เป็น cytokinin ที่ใช้บ่อยที่สุดสำหรับชักนำ multiple shoot. งานคลาสสิกใน *C. annuum* cv. mathania พบว่า **BAP 5.0 mg/L เป็นตัวที่ดีที่สุดสำหรับ shoot bud differentiation** [3]. ใน cv. Meiteimorok/Haomorok จำนวน shoot bud สูงสุดที่ BAP 22.2 µM (~5 mg/L) หรือ 44.4 µM (~10 mg/L) [2]. โปรโตคอลล่าสุดของ sweet pepper หลายงานดันไปถึง **BAP 8 mg/L + NAA 0.02 + IAA** สำหรับ shoot induction [1][8]. โปรโตคอล transformation ของ chili 7 พันธุ์ก็ optimize ที่ **BAP 5 mg/L (+ AgNO₃)** สำหรับ shoot formation [7].

> สรุป: **ช่วง optimal ของ BAP สำหรับ multiplication ในพริก = ~3–8 mg/L** ขึ้นกับพันธุ์และ explant. 5 mg/L เป็นจุดที่ literature ใช้บ่อยและสมเหตุสมผล.

### 1.2 BAP สูง (5) vs ต่ำ (1): diminishing return / vitrification?
- **Elongation ถูกกด:** ที่ BAP 5 mg/L ยอด "เพิ่มจำนวนแต่ไม่ยืด" — ต้องย้ายไป IBA/NAA 0.1 mg/L เพื่อให้ได้ plantlet สมบูรณ์ [3]. นี่คือ trade-off ปริมาณ↔ความยาวยอดที่คาดได้.
- **Morphophysiological disorder:** BAP สูงเหนี่ยวนำ underdeveloped leaves, **shoot-tip necrosis**, ผนังเซลล์บาง, phenolic/pigment ลด [13]; กลไกระดับเซลล์ — BAP รบกวน actin dynamics และ cytokinesis ที่ความเข้มข้นสูง [14]; ผล BAP ตกค้างกระทบ anatomy/pigment ระยะยาว และ NAA ช่วยกลบบางส่วน [15].
- **Hyperhydricity:** ในพืชเนื้อแข็ง BAP สัมพันธ์กับ hyperhydricity สูงกว่า cytokinin ทางเลือก (topolin) — mT ให้ proliferation สูงกว่า BAP ~6 เท่า และ hyperhydric shoot น้อยกว่า [10]; ในระบบ MS การลด BAP/ปรับ NH₄NO₃-CaCl₂ ลด hyperhydricity ได้ [11].

> สรุป: BAP 1 → 5 mg/L คาดว่าจะ **เพิ่มจำนวนยอด แต่เริ่มเห็นสัญญาณ diminishing return** (ยอดสั้นลง, callus ที่โคน, อาจมี hyperhydricity/necrosis). นี่คือ phenotype ที่ CV ของเราควรจับให้ได้ — เป็นจุดขายของโครงงาน.

### 1.3 BAP:NAA ratio → shoot vs callus vs root
ทิศทางการเจริญถูกกำหนดโดย cytokinin:auxin ratio:
- **Cytokinin เด่นมาก (BAP สูง, auxin ต่ำมาก ~0.02–0.1):** ไป shoot/bud [1][6].
- **Cytokinin:auxin ใกล้กันขึ้น (BAP 2 + NAA 0.1):** เริ่มไป **callus** ใน *C. annuum* [6]; ในแซฟฟรอน BAP 1 + NAA 1 ให้ shoot regeneration และ rooting สูงสุด ส่วน BAP สูงขึ้นกด callus [9].
- **Auxin เด่น:** ไป root [4][5].

> สูตร D ของเรา (BAP 5 + NAA 0.05) คือ cytokinin เด่นมาก + auxin แตะเบาๆ — ตาม literature น่าจะยังเป็น regime **shoot-dominant** แต่ NAA จะช่วยลด apical dominance/กระตุ้น basal callus เล็กน้อย เทียบกับ C (BAP 5 เดี่ยว) ได้ผล ratio ที่สะอาด.

### 1.4 Auxin (IBA/NAA) สำหรับ rooting ในพริก
- **IBA 0.5–1 mg/L** เป็นมาตรฐาน rooting ในพริกหลายงาน [1][6][7].
- ในพืชอื่น IBA เด่นเรื่อง root elongation; NAA เด่นเรื่อง root number/shoot girth; ความเข้มข้นสูงเร่ง initiation แต่เพิ่ม callus ที่โคน [4][5].

> สูตร E (IBA 1 mg/L) ตรงกับ rooting protocol มาตรฐานของพริก — เป็น auxin เดี่ยวระดับที่เหมาะสำหรับ root induction.

---

## ส่วนที่ 2 — วิจารณ์การออกแบบ 5 สูตร (ตรงไปตรงมา)

| สูตร | Treatment | บทบาทในดีไซน์ | คำถามที่ตอบได้ |
|------|-----------|----------------|----------------|
| A | MS (control) | baseline ไม่มี PGR | growth พื้นฐาน |
| B | MS + 1 mg/L BAP | BAP ต่ำ | จุดต่ำของ dose-response |
| C | MS + 5 mg/L BAP | BAP สูง | จุดสูงของ dose-response |
| D | MS + 5 BAP + 0.05 NAA | เพิ่ม auxin บน BAP 5 | ผลของ NAA (เทียบ C) |
| E | MS + 1 mg/L IBA | auxin เดี่ยว | rooting |

### 2.1 จุดแข็งของดีไซน์
1. **มี control ที่สะอาด (A)** — เทียบ baseline ได้.
2. **B→C เป็น dose-response ของ BAP ที่ confound ต่ำ** — เปลี่ยนแค่ขนาด BAP (1→5) เป็นการเทียบ dose ที่ตีความได้ตรง [2][3].
3. **C→D เป็นการเทียบ ratio ที่ดี** — คุม BAP=5 คงที่ เพิ่มเฉพาะ NAA 0.05 → แยกผล "เติม auxin บน cytokinin สูง" ได้สะอาด (เป็น single-factor contrast) [6].
4. **ครอบคลุม regime หลัก** — control / cytokinin dose / cytokinin+auxin / auxin เดี่ยว.

### 2.2 จุดอ่อน / confound ที่ต้องบอกตรงๆ
1. **E อยู่คนละ developmental stage กับ A–D (confound ใหญ่ที่สุด).**
   A–D คือ **multiplication stage** (cytokinin-driven); E (IBA เดี่ยว) คือ **rooting stage** [1][6][7]. ถ้าเอา explant แบบเดียวกัน เริ่มพร้อมกัน แล้ววัด "จำนวนยอด" เทียบ E กับ C ในตารางเดียว — E จะแพ้โดยอัตโนมัติเพราะมันไม่ได้ออกแบบมาให้แตกยอด ไม่ใช่เพราะ "ด้อยกว่า". **การเทียบ E กับ A–D ใน Kruskal-Wallis เดียวด้วย endpoint เดียว (เช่น shoot count) จึงตีความผิดได้.**
   → **คำแนะนำ:** แยก response variable ตาม stage — ใช้ shoot count/length สำหรับ A–D, ใช้ root count/length/% rooting สำหรับ E (และอาจ D). หรือกำหนดให้ E เป็น "rooting arm" แยกจาก "multiplication arm" ในการวิเคราะห์.

2. **Dose-response ของ BAP มีแค่ 2 จุด (1 และ 5 mg/L) — มองไม่เห็นรูปโค้ง.**
   ด้วย 2 จุดจะรู้แค่ "ขึ้นหรือลง" บอกไม่ได้ว่ามี optimum/plateau/diminishing return ตรงไหน ทั้งที่ literature ชี้ว่าโซน 3–8 mg/L เป็นที่ที่ response เริ่ม saturate และ disorder เริ่มโผล่ [3][13][14].
   → **คำแนะนำ:** เพิ่ม **BAP ระดับกลาง 2–3 mg/L** (เช่นสูตร B2 = MS + 2.5 BAP) ให้เป็น dose-response 3 จุด (1 / 2.5 / 5) จะเห็นรูปโค้งและจุด diminishing return ชัด — เป็น biological question ที่คมขึ้นและขายได้ใน YSC.

3. **D เปลี่ยน "ปัจจัยเดียว" เทียบ C จริง แต่ NAA 0.05 อาจเบาเกินจะเห็นผล.**
   NAA 0.05 mg/L ต่ำมาก (ในพริก callus เริ่มที่ ~NAA 0.1 บน BAP 2 [6]). บน BAP 5 ที่ cytokinin ครอบงำอยู่แล้ว ผลของ NAA 0.05 อาจจมหายในความแปรปรวน.
   → **คำแนะนำ:** ถ้าต้องการเห็น ratio effect ชัด พิจารณายก NAA เป็น 0.1–0.5 หรือเพิ่มอีกระดับ เพื่อให้ contrast C→D มี signal.

4. **ไม่มีแขนเทียบ cytokinin ชนิดอื่น.**
   จุดอ่อนที่ literature ชี้ตรงๆ คือ BAP ทำให้ necrosis/hyperhydricity และ **TDZ ให้จำนวนยอดสูงกว่า BAP มากใน 4 Capsicum species (4.2–22.4 ยอด)** [12], ส่วน topolin ลด hyperhydricity [10]. ถ้าจะให้โครงงานมี novelty เชิงชีววิทยา การเพิ่มแขน TDZ หรือ kinetin จะตอบคำถาม "BAP เป็นทางเลือกที่ดีที่สุดจริงไหม".
   → **คำแนะนำ (optional, ถ้างบ/พื้นที่พอ):** เพิ่ม 1 แขน **TDZ 0.5–1 mg/L** หรือ **kinetin** เป็น cytokinin-type contrast. ถ้าเพิ่มไม่ได้ ให้ระบุใน limitation ว่าดีไซน์ fix ที่ BAP โดยตั้งใจ.

5. **GA3 สำหรับ elongation ไม่มีในดีไซน์.**
   เนื่องจาก BAP 5 กดการยืดยอด [3] ถ้า endpoint รวมถึง shoot length ผลของ C/D จะดู "สั้น" โดยธรรมชาติ. ไม่จำเป็นต้องแก้ดีไซน์ แต่ควร**บันทึกว่า length ใน C/D สะท้อน cytokinin effect ไม่ใช่ความด้อย** และพิจารณา GA3 ในขั้น elongation แยก [8].

### 2.3 n=20/สูตร เพียงพอทางสถิติไหม (Kruskal-Wallis)
- หลักการทั่วไป: sample size ที่ต้องการเพิ่มตาม variance และลดตาม effect size; การเพิ่ม n ในกลุ่มที่ variance สูงคุ้มกว่าเพิ่ม n รวม [16][18]. Kruskal-Wallis ต้องการ n ใกล้เคียงหรือมากกว่า ANOVA เล็กน้อยเมื่อข้อมูล non-normal [18].
- **ประเมินสำหรับเรา:** TC phenotype (shoot count) มักให้ effect ขนาดกลาง-ใหญ่ระหว่าง control กับ BAP สูง. ที่ k=5 กลุ่ม, **n=20/กลุ่ม (รวม 100)** ให้ power เพียงพอ (โดยทั่วไป >0.8) สำหรับตรวจ effect ปานกลางขึ้นไป — ถือว่า **เพียงพอ**.
- **ข้อควรระวัง:** contamination/วิตริฟิเคชัน/ตายของขวด จะลด effective n; ถ้าเหลือ ~12–15/กลุ่มยังพอ แต่ใกล้ขอบ. variance ใน TC สูง (จุดอ่อนของ KW เมื่อ variance ไม่เท่ากันระหว่างกลุ่ม [16]).
  → **คำแนะนำ:** (a) วางแผนเผื่อ loss ~20% (ตั้งใจไว้ที่ 20 จึงดี), (b) วัด **หลาย endpoint ต่อขวด** (shoot count, length, leaf count, callus area, hyperhydricity score) เพื่อเพิ่มข้อมูลโดยไม่เพิ่มขวด, (c) post-hoc — *(⚠️ superseded: ดู `10_methods_draft.md` — primary = ART-C/LMM, secondary = Dunn + **Bonferroni** ไม่ใช่ Holm/BH)*, (d) รายงาน effect size (epsilon² หรือ rank-biserial) ไม่ใช่แค่ p-value.

> **หมายเหตุ power analysis (§2.3):** วิเคราะห์บน assumption n=20/สูตร (ต่อ batch) ซึ่งเป็น lower bound. **ฉบับสมบูรณ์ที่ n≈40/สูตร (pool 2 batch) อยู่ที่ `10_methods_draft.md` §1.4** ซึ่งพิสูจน์ว่าต้องการ n≈40 สำหรับ medium effect (f=0.25)

### 2.4 ข้อเสนอแนะ — สรุปเป็นข้อ
1. **แยกการวิเคราะห์ตาม stage:** A–D = multiplication arm (วัด shoot count/length/hyperhydricity); E (+อาจ D) = rooting arm (วัด % rooting, root number/length). อย่าเทียบ E กับ C ด้วย endpoint เดียวกัน.
2. **เพิ่มจุด BAP กลาง (2–3 mg/L)** เพื่อให้ dose-response 3 จุด เห็น diminishing return/optimum ชัด — น้ำหนัก priority สูงสุดถ้าเพิ่มได้ 1 สูตร.
3. **ยก NAA ใน D เป็น 0.1–0.5 mg/L** (หรือเพิ่มอีกระดับ) เพื่อให้ ratio contrast C→D มี signal พอ.
4. **(Optional) เพิ่มแขน TDZ หรือ kinetin** เป็น cytokinin-type contrast เพื่อ novelty; ถ้าไม่เพิ่ม ให้ระบุเป็น limitation ที่ตั้งใจ.
5. **วัดหลาย endpoint/ขวด + บันทึก hyperhydricity/necrosis เป็น categorical score** — ตรงกับจุดขาย CV phenotyping และเพิ่มข้อมูลโดยไม่เพิ่มขวด.
6. **สถิติ:** *(⚠️ superseded by `10_methods_draft.md`)* — primary = LMM/ART-ANOVA + ART-C บน per-bottle growth params; KW + Dunn + **Bonferroni** = secondary/preliminary เท่านั้น; รายงาน effect size; วางแผนเผื่อ loss; ถ้า variance ต่างกันมาก พิจารณา Brunner-Munzel/permutation.
7. **บันทึกว่า shoot length สั้นใน C/D เป็นผล BAP กดการยืด ไม่ใช่ความด้อย** [3]; แยก elongation (GA3) เป็นขั้นถ้าจำเป็น.

---

## ตารางคัดกรอง paper

| # | Paper | พืช | สาระสำคัญต่อเรา | น้ำหนัก |
|---|-------|-----|------------------|---------|
| 1 | Nadim 2024 [1] | C. annuum (sweet) | BAP 8 + NAA 0.02 + IAA = shoot ดีที่สุด; IBA 1 = rooting | สูง |
| 2 | Sanatombi 2006 [2] | C. annuum | shoot bud สูงสุด BAP 22.2/44.4 µM; IBA/IAA rooting | สูง |
| 3 | Agrawal 1989 [3] | C. annuum mathania | **BAP 5 ดีสุดสำหรับ bud แต่ไม่ elongate**; IBA/NAA 0.1 ทำ plantlet | สูงมาก |
| 4 | Indrachapa 2025 [4] | coconut | IBA เด่น root elongation; NAA เด่น root number/girth | กลาง |
| 5 | Song 2024 [5] | pear | IBA+NAA สูงเร่ง root induction; control rooting ต่ำ | กลาง |
| 6 | Swamy 2014 [6] | C. annuum (5 พันธุ์) | **BAP 2 + NAA 0.1 → callus; BAP+IAA → shoot** (ratio) | สูงมาก |
| 7 | Shams 2024 [7] | chili (7 พันธุ์) | optimal BAP 5 + AgNO₃ shoot; IBA 1 rooting; GA3 elongation | สูง |
| 8 | Akther 2020 [8] | C. annuum (bell) | BAP 8 + NAA shoot; IBA 0.5 rooting | กลาง |
| 9 | Ahmed 2025 [9] | saffron | BAP 1 + NAA 1 = shoot+root สูงสุด; BAP สูงกด callus | กลาง |
| 10 | Abdouli 2022 [10] | Pistacia | **topolin > BAP**: proliferation 6×, hyperhydricity ต่ำ | สูง |
| 11 | Ersali 2024 [11] | Pistacia | ลด BAP/ปรับ NH₄NO₃-CaCl₂ ลด hyperhydricity | กลาง |
| 12 | Peddaboina 2006 [12] | 4 Capsicum spp. | **TDZ ให้ยอดสูงสุด 4.2–22.4** > BA/Kn/zeatin | สูงมาก |
| 13 | Martins 2022 [13] | Quercus | **BAP สูง → underdeveloped leaf, tip necrosis**; KIN ช่วยกลบ | สูง |
| 14 | Ruan 2022 [14] | moss | BAP สูงรบกวน actin/cytokinesis → toxicity กลไก | กลาง |
| 15 | Martins 2020 [15] | Alcantarea | BAP ตกค้างกระทบ anatomy/pigment; NAA กลบบางส่วน | กลาง |
| 16 | Liang 2020 [16] | (สถิติ) | KW: เพิ่ม n ในกลุ่ม variance สูงคุ้มกว่าเพิ่ม n รวม | สูง |
| 17 | Ledolter 2020 [17] | (สถิติ) | หลัก power analysis: n ↑ ตาม variance, ↓ ตาม effect | กลาง |
| 18 | Clark 2023 [18] | (สถิติ) | KW power ใกล้ ANOVA เมื่อ assumption ใช้ไม่ได้ | กลาง |

---

## References

[1] [Development of In Vitro Regeneration Protocol for Sweet Pepper (Capsicum annuum L.) using Cotyledon as Explant](https://consensus.app/papers/details/3e2de8ef6ed052939014617cc97d1519/?utm_source=claude_code) (M. Nadim et al., 2024, J Bangladesh Agril Univ, 2 citations)
[2] [In vitro regeneration and mass multiplication of Capsicum annuum L](https://consensus.app/papers/details/3b9553e240fc5408a3bd185d45d46ac5/?utm_source=claude_code) (K. Sanatombi et al., 2006, Int. J. Food Agric. Environ., 27 citations)
[3] [Plant regeneration in tissue cultures of pepper (Capsicum annuum L. cv. mathania)](https://consensus.app/papers/details/9b63b169ea505a37a68d867af2c04f60/?utm_source=claude_code) (S. Agrawal et al., 1989, Plant Cell Tissue Organ Cult., 102 citations)
[4] [Optimizing pulse treatments for enhanced in vitro rooting in coconut micropropagation](https://consensus.app/papers/details/cf5d54982e9750e1890bdbf19bb36a36/?utm_source=claude_code) (M. Indrachapa et al., 2025, Technology in Horticulture, 0 citations)
[5] [High-Efficiency In Vitro Root Induction in Pear Microshoots (Pyrus spp.)](https://consensus.app/papers/details/638b0677babe5bbfa50652ad4623e324/?utm_source=claude_code) (Jae-Young Song et al., 2024, Plants, 5 citations)
[6] [Direct regeneration protocols of five Capsicum annuum L. varieties](https://consensus.app/papers/details/bd7de73261db528b8ef2000e2f801826/?utm_source=claude_code) (S. Swamy et al., 2014, African Journal of Biotechnology, 10 citations)
[7] [Developing an Optimized Protocol for Regeneration and Transformation in Pepper](https://consensus.app/papers/details/29feb87f470151a2b49fec839a03e40e/?utm_source=claude_code) (Shamsullah Shams et al., 2024, Genes, 6 citations)
[8] [Micropropagation of Two Varieties of Bell pepper (Capsicum annuum L.)](https://consensus.app/papers/details/92c4e6e4e78a55a8a444793368fd87a6/?utm_source=claude_code) (Shilpi Akther et al., 2020, Plant Tissue Culture and Biotechnology, 3 citations)
[9] [Optimizing micropropagation and microcorm induction in saffron (Crocus sativus L.) using PGRs (NAA and BAP) and elicitor salicylic acid](https://consensus.app/papers/details/1ddfb2f610835f76ada8c30bf6d6ca85/?utm_source=claude_code) (Z. Ahmed et al., 2025, BMC Plant Biology, 5 citations)
[10] [Topolin cytokinins enhanced shoot proliferation, reduced hyperhydricity and altered cytokinin metabolism in Pistacia vera L. seedling explants.](https://consensus.app/papers/details/6ab7f6a493d0560f9b9d96b991fb35f0/?utm_source=claude_code) (Dhekra Abdouli et al., 2022, Plant Science, 27 citations)
[11] [Control of hyperhydricity of Pistacia khinjuk stocks in vitro shoots](https://consensus.app/papers/details/38637b29cfc75e1b898f89da24f17880/?utm_source=claude_code) (Yusuf Ersali, 2024, BMC Biotechnology, 1 citation)
[12] [In vitro shoot multiplication and plant regeneration in four Capsicum species using thidiazuron](https://consensus.app/papers/details/e068be68558e549b9c2d4b70fb95361f/?utm_source=claude_code) (Venkataiah Peddaboina et al., 2006, Scientia Horticulturae, 69 citations)
[13] [6-Benzylaminopurine and kinetin modulations during in vitro propagation of Quercus robur (L.): an assessment of anatomical, biochemical, and physiological profiling of shoots](https://consensus.app/papers/details/e98247844367563c9c3c4ab910b4a68f/?utm_source=claude_code) (J. Martins et al., 2022, Plant Cell Tissue Organ Cult., 36 citations)
[14] [Exogenous 6-benzylaminopurine inhibits tip growth and cytokinesis via regulating actin dynamics in the moss Physcomitrium patens](https://consensus.app/papers/details/28266e67538b5ac4913c6e9c431b8e29/?utm_source=claude_code) (Jing-Hui Ruan et al., 2022, Planta, 6 citations)
[15] [Modulation of the anatomical and physiological responses of in vitro grown Alcantarea imperialis induced by NAA and residual effects of BAP](https://consensus.app/papers/details/7e83c131298f5d7eab1407ad369dc26f/?utm_source=claude_code) (J. Martins et al., 2020, Ornamental Horticulture, 22 citations)
[16] [[Influence of group sample size on statistical power of tests for quantitative data with an imbalanced design].](https://consensus.app/papers/details/6c361d9fff825fd7afc51316b8d02aa3/?utm_source=claude_code) (Qihong Liang et al., 2020, J Southern Medical University, 2 citations)
[17] [Focus on Data: Statistical Design of Experiments and Sample Size Selection Using Power Analysis](https://consensus.app/papers/details/164168f19fcc5198b7b1ea971d5874fc/?utm_source=claude_code) (J. Ledolter et al., 2020, Investigative Ophthalmology & Visual Science, 53 citations)
[18] [Empirical investigations into Kruskal-Wallis power studies utilizing Bernstein fits, simulations and medical study datasets](https://consensus.app/papers/details/d641a7a3c01757648f1e345a30a1c973/?utm_source=claude_code) (J. Clark et al., 2023, Scientific Reports, 22 citations)

---

## Consensus message (verbatim)

> Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
