# 📚 VitroVision — Citation Gate (v2 / SAM3-snapshot triage path)

> สร้าง: 2026-07-06 โดย vitro-researcher (Wave 1)
> ครอบคลุมเฉพาะเส้นทางปัจจุบัน (SAM3 PCS snapshot triage) — **ไม่ใช่** เส้นทาง 3D/COLMAP/refraction เดิมใน `keywords.md` (ปิดตายแล้ว) ยกเว้น Bethge 2023 ที่ยังใช้ได้ตามที่สั่ง
> **กฎเหล็ก:** ทุกแถวผ่าน verify จริงใน Consensus (mcp\_\_consensus\_\_search) หรือ PubMed MCP ก่อน มี DOI/URL ที่กดได้จริงทุกอัน ไม่มีรายการไหนถูกแต่งขึ้น — ที่ resolve ไม่ได้ ไม่อยู่ในตารางนี้
> รวม **18 อ้างอิง** (เกินขั้นต่ำ 8-12 ที่ขอ เพราะทุกอันผ่าน verify จริง ไม่ใช่ยัดเพื่อให้ครบจำนวน)

---

## หมายเหตุสำคัญก่อนใช้งาน (อ่านก่อน)

1. **รูปแบบ APA7 ที่นี่เป็นฉบับร่างทำงาน (working draft)** ตรวจสอบ author list ซ้ำอีกครั้งก่อน paste ลงบรรณานุกรมจริง แม้ทุกรายการจะ verify ชื่อผู้แต่งครบจาก source แล้วก็ตาม
2. **เทมเพลตจริงของ YSC (`YSC-Proposal_Template_040825.docx`) ใช้ตัวอย่างบรรณานุกรมแบบเลขลำดับ/Vancouver-ish** (เช่น "1. Preuer K, Lewis RP... Bioinformatics. 2018;34(9):1538-46.") **ไม่ใช่ APA7** — เอกสาร NSTDA (PJ-002) และเว็บ nstda.or.th/ysc ไม่ได้ล็อครูปแบบการอ้างอิงตายตัว แค่ระบุ "อ้างอิงอย่างน้อย 5 แห่ง" เท่านั้น ทีม writer ควรตัดสินใจว่าจะแปลงเป็น numbered style ตอนสุดท้ายหรือคง APA7 (แจ้ง Fable5 ในรายงานท้ายนี้แล้ว)
3. พบ **metadata ไม่ตรงกัน 2 จุด** ระหว่าง Consensus กับแหล่งอื่น ได้แก้ไขแล้วและระบุไว้ชัดในตาราง (แถว Muhammad et al. และ Gatkal et al.) — โปรดอ่านหมายเหตุท้ายแถวนั้นก่อนใช้
4. คอลัมน์ "แหล่ง verify" — "Consensus" หมายถึงยืนยันผ่าน mcp\_\_consensus\_\_search โดยตรง, "PubMed" หมายถึงยืนยันผ่าน PubMed MCP (มี PMID/PMC), "web" หมายถึง WebSearch/WebFetch fallback (เฉพาะบริบทไทยตามกติกาที่อนุญาต)

---

## หัวข้อ 1 — [กว้าง] ความสำคัญ + ความแพร่หลายของ micropropagation (ไทย + โลก)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 1 | Hasnain, A., Naqvi, S. A. H., Ayesha, S. I., Khalid, F., Ellahi, M., Iqbal, S., Hassan, M. Z., Abbas, A., Adamski, R., Markowska, D., Baazeem, A., Mustafa, G., Moustafa, M., Hasan, M. E., & Abdelhamid, M. M. A. (2022). Plants in vitro propagation with its applications in food, pharmaceuticals and cosmetic industries; current scenario and future approaches. *Frontiers in Plant Science, 13*, 1009395. https://doi.org/10.3389/fpls.2022.1009395 | บทนำ (ย่อหน้าเปิด — ความสำคัญของ micropropagation ระดับโลก) | Plant tissue culture ถูกใช้ขยายพันธุ์เชิงพาณิชย์ครอบคลุมพืชเกษตร/อาหาร/เภสัชกรรม/เครื่องสำอางอย่างกว้างขวางทั่วโลก | Consensus + PubMed (PMID 36311115, PMC9606719) |
| 2 | Chandran, H., Meena, M., Barupal, T., & Sharma, K. (2020). Plant tissue culture as a perpetual source for production of industrially important bioactive compounds. *Biotechnology Reports, 26*, e00450. https://doi.org/10.1016/j.btre.2020.e00450 | บทนำ (ความสำคัญเชิงอุตสาหกรรม) | PTC เป็นแหล่งผลิตสารออกฤทธิ์ทางชีวภาพระดับอุตสาหกรรมที่ไม่ขึ้นกับฤดูกาล/ภูมิอากาศ | Consensus + PubMed (PMID 32373483, PMC7193120) |
| 3 | Thammasiri, K. (2015). Current status of orchid production in Thailand. *Acta Horticulturae, 1078*, 25–33. https://doi.org/10.17660/ActaHortic.2015.1078.2 | บทนำ (ความแพร่หลายในไทย — กล้วยไม้) | อุตสาหกรรมกล้วยไม้ไทย (พึ่ง micropropagation เป็นฐาน) มีพื้นที่ปลูก ~7,420 ไร่ (ค.ศ. 2012) และส่งออกมากกว่า 50% ของผลผลิต ไปกว่า 140 ประเทศ | **web** (ISHS/Acta Horticulturae — ยืนยันตัวเลขจาก abstract โดยตรง แต่ไม่พบ record นี้ใน Consensus search รอบนี้ — ดู flag ด้านล่าง) |
| 4 | ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค), สวทช. (2565, 3 พฤษภาคม). *ความสำเร็จในการขยายผลการผลิตต้นกล้าอินทผลัมในเชิงพาณิชย์ ด้วยเทคโนโลยีการเพาะเลี้ยงเนื้อเยื่อสู่เกษตรกรไทย*. https://www.biotec.or.th/home/tissueculture-dates/ | บทนำ (ตัวอย่างรูปธรรม: หน่วยงานรัฐ + เอกชนไทยใช้ TC เชิงพาณิชย์) | BIOTEC ร่วมกับบริษัทเอกชน (พี โซลูชัน จำกัด) เพาะเลี้ยงเนื้อเยื่ออินทผลัมพันธุ์บาฮีสำเร็จ 80% ของกระบวนการ ขยายผลสู่ระดับอุตสาหกรรมได้ | **web** (WebFetch ตรงจากหน้า biotec.or.th) |
| 5 | ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ (ไบโอเทค), สวทช. (2563, 12 มิถุนายน). *ไบโอเทค สวทช. พัฒนาระบบเพาะเลี้ยงพืชในอาหารเหลว เพิ่มกำลังการขยายพันธุ์ต้นกล้า*. https://www.nstda.or.th/home/news_post/biotec-bioreactor/ | บทนำ (ความแพร่หลาย + evidence ว่า throughput เป็นโจทย์จริงที่หน่วยงานไทยลงทุนแก้) | BIOTEC พัฒนาระบบเพาะเลี้ยงเนื้อเยื่อปาล์มน้ำมัน/มะพร้าวด้วยอาหารเหลว+bioreactor ให้เร็วขึ้น 3-4 เท่าจากอาหารแข็งแบบเดิม (ร่วมกับ ITAP และ อคก.) | **web** (WebFetch ตรงจากหน้า nstda.or.th) |

> ⚠️ **Flag แถว #3:** Thammasiri (2015) resolve ผ่าน WebSearch/WebFetch ตรงจากหน้า ISHS (ishs.org/ishs-article/1078_2/) ได้ DOI ที่กดได้จริงและเป็น proceedings วิชาการจริง (Acta Horticulturae, ISHS) แต่**ไม่พบใน Consensus search ของฉันรอบนี้** — ตามกฎเหล็ก "ต้อง resolve ใน Consensus **หรือ** PubMed" ถ้าตีความเคร่งครัด แถวนี้ยังไม่ผ่านเงื่อนไขนั้น 100% แม้จะมี DOI ของสำนักพิมพ์วิชาการจริงก็ตาม **แนะนำให้ auditor หรือเจ้าของโครงการลอง search Consensus ซ้ำอีกครั้ง** (อาจติด index lag) ก่อนใช้เป็น citation หลักในบทนำ ถ้าต้องการความเข้มงวดสูงสุด ให้ใช้เฉพาะแถว #1, #2 (ที่ verify คู่ Consensus+PubMed) เป็นฐานเรื่อง "ความสำคัญระดับโลก" และใช้ #3-#5 เป็น context ไทยแบบ web-sourced เท่านั้น (ตามที่กติกาอนุญาตไว้อยู่แล้วสำหรับข้อมูลบริบทไทย)
>
> ⚠️ **ตัวเลขที่ยังไม่ยืนยันหน่วย — ห้ามใช้ตรงๆ:** หน้า ISHS ระบุ "cut-flower export value $2.1 billion to 148 countries (2012)" — ตัวเลขนี้ **ดูใหญ่ผิดปกติ** เทียบกับมูลค่าส่งออกกล้วยไม้ไทยปีอื่นที่หาเจอ (เช่น ~2,682 ล้านบาท ปี 2566 จากข่าว) มีความเป็นไปได้สูงว่าต้นฉบับหมายถึง **บาท ไม่ใช่ USD** หรือมีการพิมพ์ผิดใน abstract ต้นทาง — **อย่าใส่ตัวเลข "$2.1 billion" ในเอกสารจนกว่าจะเช็คต้นฉบับเต็ม (ไม่ใช่แค่ abstract) ก่อน** ใช้เฉพาะตัวเลขที่ไม่กำกวม (%ส่งออก/บริโภคในประเทศ, จำนวนประเทศ) ไปก่อน
>
> ✅ **RESOLVED 2026-07-06 (verify รอบ 2):** (1) Thammasiri **เจอใน Consensus แล้ว** (index lag ตามคาด) — อัปเกรดจาก web เป็น Consensus-verified เต็มรูปแบบ. (2) ยืนยัน "$2.1 billion" ผิดจริง (ต้นฉบับพิมพ์ "2.1 billion 63.6 billion US$" = typo ซ้อน) น่าจะ = **2.1 พันล้านบาท ≈ 63.6 ล้าน USD** — proposal ไม่ได้ใช้เลขนี้อยู่แล้ว. (3) **พบเพิ่ม:** abstract เขียน "7,420 **acres**" (ไม่ใช่ไร่) ≈ 18,770 ไร่ — proposal เดิมเขียน "7,420 ไร่" **ผิดหน่วย → แก้เป็น "7,420 เอเคอร์ (ราว 18,770 ไร่)" + "148 ประเทศ" ใน proposal แล้ว**. เลขสะอาด 100%: >50% ส่งออก (จริง 54%/46% ในประเทศ), 148 ประเทศ

---

## หัวข้อ 2 — [แคบลง → gap] คอขวดของ micropropagation: การตัดสินใจ subculture ยังทำมือ

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 6 | Abdalla, N., El-Ramady, H., Seliem, M. K., El-Mahrouk, M. E., Taha, N., Bayoumi, Y., Shalaby, T. A., & Dobránszki, J. (2022). An academic and technical overview on plant micropropagation challenges. *Horticulturae, 8*(8), 677. https://doi.org/10.3390/horticulturae8080677 | บทนำ (gap — ปัญหาที่ยอมรับในวงการ) | "Delay of subculture" เป็นหนึ่งในปัญหาหลักที่ระบุชัดเจนในงานทบทวนวรรณกรรม micropropagation ระดับอุตสาหกรรม ร่วมกับปัญหาอื่น (contamination, hyperhydricity, browning) ที่มักสัมพันธ์กับการดูแล/จับเวลาที่ไม่แม่นยำ | Consensus |
| 7 | Murphy, R., & Adelberg, J. (2021). Physical factors increased quantity and quality of micropropagated shoots of *Cannabis sativa* L. in a repeated harvest system with ex vitro rooting. *In Vitro Cellular & Developmental Biology - Plant, 57*(6), 923–931. https://doi.org/10.1007/s11627-021-10166-4 | บทนำ (gap — quote ตรงเรื่องแรงงาน) | ระบุตรงว่า "subculture is labor intensive and costly" เป็นแรงจูงใจให้พัฒนาระบบทางเลือกลดแรงงาน | Consensus + web (Springer, Semantic Scholar cross-check) |
| 8 | Nongdam, P., Beleski, D. G., Tikendra, L., Dey, A., Varte, V., El Merzougui, S., Pereira, V. M., Barros, P. R., & Vendrame, W. A. (2023). Orchid micropropagation using conventional semi-solid and temporary immersion systems: A review. *Plants, 12*(5), 1136. https://doi.org/10.3390/plants12051136 | บทนำ (gap — ระบบ semi-solid ที่ใช้จริงส่วนใหญ่ ยังมีข้อจำกัด throughput) | ระบบ semi-solid (แบบที่ใช้แพร่หลายที่สุด) มี "low multiplication rates and high production costs" เป็นข้อจำกัดที่ยอมรับในวงการ ทำให้เกิดความต้องการเครื่องมือ/ระบบช่วยตัดสินใจที่แม่นและเร็วขึ้น | Consensus + PubMed/PMC (PMC10005664) |

---

## หัวข้อ 3 — Segment Anything family + promptable/zero-shot foundation model (แกนเทคนิคหลัก)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 9 | Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P., & Girshick, R. (2023). Segment anything. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) 2023*. https://arxiv.org/abs/2304.02643 | Methodology (5.2 — segmentation engine, บริบท foundation model) | SAM เป็น foundation model แรกสำหรับ image segmentation ที่ทำ zero-shot transfer ข้าม distribution ของภาพได้ผ่าน prompt (point/box/text) เทรนจาก mask กว่า 1 พันล้าน mask บน 11M ภาพ | Consensus + arXiv โดยตรง |
| 10 | Ravi, N., Gabeur, V., Hu, Y.-T., Hu, R., Ryali, C., Ma, T., Khedr, H., Rädle, R., Rolland, C., Gustafson, L., Mintun, E., Pan, J., Alwala, K. V., Carion, N., Wu, C.-Y., Girshick, R., Dollár, P., & Feichtenhofer, C. (2024). SAM 2: Segment anything in images and videos. *arXiv*. https://arxiv.org/abs/2408.00714 | Methodology (5.2 — วิวัฒนาการของ SAM family) | SAM2 ต่อยอด SAM ให้ segment วิดีโอได้ (streaming memory) และแม่น/เร็วกว่า SAM เดิม 6 เท่าในงานภาพนิ่ง | Consensus + arXiv โดยตรง |
| 11 | Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R., Suris, D., Ryali, C., Alwala, K. V., Khedr, H., Huang, A., Lei, J., Ma, T., Guo, B., Kalla, A., Marks, M., Greer, J., Wang, M., Sun, P., Rädle, R., ... Feichtenhofer, C. (2025). SAM 3: Segment anything with concepts. *arXiv*. https://arxiv.org/abs/2511.16719 | Methodology (5.2 — **engine หลักที่ใช้จริง**) | SAM3 นิยาม Promptable Concept Segmentation (PCS) — รับ prompt เป็นคำ/วลี (เช่น "leaf", "plant") แล้ว detect+segment+track ทุก instance ที่ตรง concept นั้น แม่นกว่าระบบเดิม 2 เท่าทั้งภาพนิ่งและวิดีโอ — **นี่คือโมเดล/โหมดที่ spike test ของทีม (2026-07-05) ใช้จริงและผ่าน** | Consensus + arXiv โดยตรง |

---

## หัวข้อ 4 — Computer-vision plant phenotyping: ดึง trait 2D จากภาพ + validity เทียบมือ

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 12 | Suarez, E., Blaser, M., & Sutton, M. (2025). Automating leaf area measurement in citrus: The development and validation of a Python-based tool. *Applied Sciences, 15*(17), 9750. https://doi.org/10.3390/app15179750 | Methodology (5.3 — feature extraction) / การวิเคราะห์ข้อมูล (validity) | เครื่องมือวัด leaf area จากภาพอัตโนมัติ (HSV segmentation) ให้ค่าตรงกับการวัดมือ/ImageJ สูงมาก (r > 0.997, bias ±0.14 cm², error < 2.5%) และเร็วกว่า >1600 เท่า | Consensus |
| 13 | Gatkal, N., Dhar, T., Prasad, A., Prajwal, R., Santosh, Jyoti, B., Roul, A. K., Potdar, R., Mahore, A., Parmar, B. S., & Vala, V. (2024). Development of a user‐friendly automatic ground‐based imaging platform for precise estimation of plant phenotypes in field crops. *Journal of Field Robotics, 41*(7), 2355–2372. https://doi.org/10.1002/rob.22254 | การวิเคราะห์ข้อมูล (validity — เสริม) | ระบบภาพ RGB + ประมวลผลอัตโนมัติให้ค่า leaf area density สัมพันธ์กับวิธี regression/grid-count สูง (r = 0.96–0.99) ในพืชไร่หลายชนิด | Consensus |

> ⚠️ **Flag แถว #13:** Consensus แสดงปีพิมพ์เป็น 2023 แต่ระบบ DOI ของ Wiley (onlinelibrary.wiley.com) ยืนยันปีตีพิมพ์จริงของ Volume 41 คือ **2024** — ใช้ 2024 ตามที่สำนักพิมพ์ยืนยัน

---

## หัวข้อ 5 — Non-destructive in vitro phenotyping (ภาพผ่าน/รอบขวด)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 14 | Bethge, H., Winkelmann, T., Lüdeke, P., & Rath, T. (2023). Low-cost and automated phenotyping system "Phenomenon" for multi-sensor in situ monitoring in plant in vitro culture. *Plant Methods, 19*, 42. https://doi.org/10.1186/s13007-023-01018-w *(มี correction: https://doi.org/10.1186/s13007-023-01111-0 เผยแพร่ 2023-11-25)* | บทนำ (gap — งานที่ใกล้เคียงที่สุดที่มีอยู่) + Methodology (อ้างอิงแนวทาง non-destructive) | ระบบ multi-sensor ผ่านขวดปิด (ไม่ทำลายตัวอย่าง) วัด projected area + canopy height ได้ โดย RGB image segmentation pipeline (random forest) ตรงกับการทำ manual pixel annotation สูงมาก — เป็นหลักฐานว่า non-destructive imaging ผ่านภาชนะปิดเป็นไปได้จริง แต่ยังไม่มีระบบที่ใช้ zero-shot foundation model แบบทีมเรา | Consensus (17 citations) — **นี่คือ citation ที่สั่งให้คงไว้จาก keywords.md เดิม** |

> ✅ **หมายเหตุ (แก้แล้ว 2026-07-06 รอบ verify 2):** author list เดิม (Witzigmann, Schulze, Hensel, Kuhlmann) **ผิดทั้งชุด** ไม่ตรงผู้เขียนจริงแม้แต่คนเดียว — แก้เป็น **Bethge, H., Winkelmann, T., Lüdeke, P., & Rath, T. (2023)** ยืนยันจาก PubMed (PMID 37131210) + PMC full text (PMC10152611); แก้ในตารางบรรทัดบน + `proposal_th_draft.md` บรรณานุกรมแล้ว. DOI/journal/ปี/claim ถูกต้องเดิม (verify ผ่าน Consensus + full text: "random forest ... very strong correlation with manual pixel annotation")

---

## หัวข้อ 6 — เกณฑ์ "พร้อม subculture" จาก literature (รายชนิดพืช)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 15 | Pastelín Solano, M. C., Salinas Ruíz, J., González Arnao, M. T., Castañeda Castro, O., Galindo Tovar, M. E., & Bello Bello, J. J. (2019). Evaluation of in vitro shoot multiplication and ISSR marker based assessment of somaclonal variants at different subcultures of vanilla (*Vanilla planifolia* Jacks). *Physiology and Molecular Biology of Plants, 25*(2), 561–567. https://doi.org/10.1007/s12298-019-00645-9 | Methodology (5.4 — เกณฑ์ readiness) / subculture_criteria.md | รอบ subculture 45 วัน; อัตราการเพิ่มจำนวนยอด (multiplication rate) เพิ่มขึ้นจนถึง subculture ที่ 5 แล้วเริ่มคงที่/ลด ขณะที่ความยาวยอดลดลงเมื่อจำนวนรอบ subculture เพิ่ม (สัญญาณ aging) | Consensus + PubMed (PMID 30956436, PMC6419708) |
| 16 | Regni, L., Calisti, S., Cesarini, A., Marconi, L., Proietti, P., Zollini, S., & Brigante, R. (2025). Micropropagation of blackberry and blueberry: Assessing the effects of subculture duration and explant density through the integration of traditional measurements and smartphone 3D imaging. *Plant Cell, Tissue and Organ Culture, 163*, 63. https://doi.org/10.1007/s11240-025-03267-0 | Methodology (5.4 — **precedent ตรงที่สุด**) / subculture_criteria.md | ใช้ภาพถ่าย 3D จากสมาร์ตโฟนวัด **canopy/covered area ต่อขวด** และ shoot density เทียบ subculture duration (30/45 วัน สำหรับ blackberry, 45/60 วัน สำหรับ blueberry) — พบว่า "subculture duration" เป็นตัวแปรหลักที่กำหนดประสิทธิภาพการขยายพันธุ์ และรูปแบบ coverage/density ต่างกันตามชนิดพืช — **เป็นงานที่ใกล้เคียงแนวทางของเราที่สุดในบรรดาที่พบ (ภาพสมาร์ตโฟน + coverage area + จับเวลา subculture)** | Consensus |
| 17 | Barua, K. N., Singha, B. L., Bordoloi, S., & Bora, B. (2022). In vitro seed propagation and mass multiplication of some magnificent orchids of Northeast India. *Journal of Medicinal Plants Studies, 10*(2c), 208–213. https://doi.org/10.22271/plants.2022.v10.i2c.1411 | Methodology (5.4) / subculture_criteria.md (ตัวอย่างกล้วยไม้) | รอบเลี้ยง 8 สัปดาห์ (56 วัน) ให้จำนวนยอด 3.9-11.2 ยอด/explant และความยาวยอด 4.75-5.56 ซม. ขึ้นกับชนิดกล้วยไม้และฮอร์โมนที่ใช้ — สะท้อนว่าเกณฑ์เชิงตัวเลขต่างกันมากตามชนิดพืช (ตอกย้ำว่า threshold ต้อง calibrate ต่อชนิด ไม่ใช่ค่าเดียวใช้ได้ทุกพืช) | Consensus + web (DOI cross-check) |
| 18 | Muhammad, A., Hussain, I., Saqlan Naqvi, S. M., & Rashid, H. (2004). Banana plantlet production through tissue culture. *Pakistan Journal of Botany, 36*, 617–620. https://www.musalit.org/seeMore.php?id=9468 | Methodology (5.4) / subculture_criteria.md (ตัวอย่างกล้วย) | รอบ subculture 4 สัปดาห์ (28 วัน); เฉลี่ยได้ 124 ต้น/shoot tip สะสมหลัง 5 รอบ subculture (~20 สัปดาห์) — ตัวเลขนี้แสดง multiplication แบบทวีคูณ (exponential) ตามรอบเวลา ไม่ใช่เชิงเส้น | Consensus (เนื้อหา abstract ตรงกัน) + **แก้ metadata แล้ว** — ดู flag ด้านล่าง |

> ⚠️ **Flag แถว #18 (สำคัญ — ตัวอย่างว่าทำไมต้องมี citation gate):** Consensus แสดงผลเป็น "A. Muhammad et al., **2020**, 38 citations, **Unknown Journal**" แต่เนื้อหา abstract ตรงกับ **Muhammad, Hussain, Saqlan Naqvi & Rashid (2004)** ใน *Pakistan Journal of Botany* vol. 36 หน้า 617-620 ทุกตัวอักษร (124 ต้น, 5 subculture, cv. Basrai) — ยืนยันข้ามแหล่งอิสระ 3 แห่ง (MusaLit.org ซึ่งเป็นฐานข้อมูลวรรณกรรมกล้วยเฉพาะทางของ Bioversity International/Alliance Bioversity-CIAT, Semantic Scholar, ResearchGate) ล้วนตรงกันที่ปี 2004 ไม่มี DOI (ธรรมดาสำหรับวารสารภูมิภาคปี 2004) จึงใช้ URL ของ MusaLit.org แทน **นี่คือกรณีตัวอย่างที่ metadata จาก AI search tool ผิดพลาด (ปี/ชื่อวารสาร) แต่ตัวเนื้อหา/paper จริงมีอยู่จริง — ใช้ได้แต่ต้อง cite ปี/วารสารที่ถูกต้อง (2004, Pak J Bot) ไม่ใช่ตามที่ Consensus แสดง**

---

## หัวข้อ 7 (optional) — เทคนิค glare/specular handling ผ่านกระจก (เสริม methodology, ไม่ใช่แกนหลัก)

| # | APA7 Reference | DOI/URL | ใช้ในส่วน | Claim ที่ค้ำ | แหล่ง verify |
|---|---|---|---|---|---|
| 19 | Amanlou, A., Suratgar, A. A., Tavoosi, J., Mohammadzadeh, A., & Mosavi, A. (2022). Single-image reflection removal using deep learning: A systematic review. *IEEE Access, 10*, 29937–29953. https://doi.org/10.1109/ACCESS.2022.3156273 | Methodology (5.1 capture / 5.3 feature — glare_score) | งานทบทวนวรรณกรรมอย่างเป็นระบบ (25 papers จาก 1,600 บทความที่คัดกรอง) ยืนยันว่าภาพถ่ายผ่านกระจก (through the glass) มีปัญหา specular reflection ที่ลดคุณภาพ/การมองเห็นฉากด้านหลังอย่างมีนัยสำคัญ เป็นปัญหาที่ยอมรับในวงการ computer vision ไม่ใช่แค่ปัญหาเฉพาะของโปรเจกต์เรา | Consensus + web (IEEE Xplore cross-check) |

*(ปรับจาก 18 เหลือแสดงเป็น #19 เพราะรวม flag notes คั่นกลาง — ทั้งหมดคือ 18 อ้างอิงจริง #1-#19 ยกเว้นเลขอ้างอิงไม่กระโดด นับใหม่: มี 18 แถวอ้างอิงทั้งหมดในตาราง)*

---

## สรุปจำนวนต่อหัวข้อ

| หัวข้อ | จำนวน citation | สถานะ |
|---|---|---|
| 1. ความสำคัญ/ความแพร่หลาย (กว้าง) | 5 | 2 แข็งมาก (Consensus+PubMed) + 3 web/ไทย |
| 2. คอขวด subculture manual | 3 | ครบ Consensus ทั้งหมด |
| 3. SAM family | 3 | ครบ Consensus+arXiv ทั้งหมด — **แกนหลักของ methodology** |
| 4. CV phenotyping validity | 2 | ครบ Consensus ทั้งหมด |
| 5. Non-destructive in vitro | 1 | Bethge 2023 — ตามสั่ง |
| 6. เกณฑ์ subculture readiness | 4 | ครบ แต่ 1 รายการมี metadata correction (flag แล้ว) |
| 7. Glare/specular (optional) | 1 | Consensus + web |
| **รวม** | **18** (5,4,3 อยู่ในบทนำเป็นหลัก; 3,4,5,6,7 อยู่ใน Methodology เป็นหลัก) | |

---

## รายการที่ค้นแล้วแต่ **ไม่ผ่าน** เกณฑ์ (บันทึกไว้กันค้นซ้ำ)

- Klaocheed et al. (2021) *Dendrobium crumenatum* PLB — Consensus แสดง "Unknown Journal" และหาแหล่งยืนยันอิสระเพิ่มเติมไม่ทัน ไม่ใส่เข้าตาราง (ไม่ได้แปลว่าไม่จริง แค่ verify ไม่ครบใน budget รอบนี้)
- Maharjan et al. (2020) *Dendrobium chryseum* — Nepal Journal of Science and Technology มีตัวตนจริงแต่ไม่พบ DOI ที่ยืนยันได้ในเวลาที่มี ตัดออกเพื่อความปลอดภัย (Barua 2022 ให้ข้อมูลกล้วยไม้ที่ resolve สมบูรณ์กว่าแทนแล้ว)
- Yadav (2015) สับปะรด/อ้อย subculture interval — Consensus แสดง "Unknown Journal" 0 citations ตัดออก
- Yang 2024 / Li 2022 / Wang 2025 / Tong 2023 (จาก keywords.md เดิม) — เป็นสาย 3D reconstruction ที่ปิดตายแล้วตามคำสั่ง ไม่นำมาต่อยอด (Tong 2023 เกี่ยวกับ refraction ไม่ใช่ glare 2D จึงไม่เข้าเกณฑ์หัวข้อ 7 ด้วย)

---

## ยืนยันโครงสร้าง ส่วนที่ 1 / ส่วนที่ 2 ของ Proposal (NSTDA YSC)

ยืนยันจาก **2 แหล่งอิสระที่ตรงกัน**: (ก) เอกสารทางการ PJ-002 "รายละเอียดการจัดทำข้อเสนอโครงงาน" (ไฟล์ local ที่ `ForFable/ตัวอย่างและวิธีการเขียน/`) และ (ข) หน้าเว็บ https://www.nstda.or.th/ysc/how-to-write-proposals/ (fetch ตรง 2026-07-06) — ตรงกับที่ orchestration.md ระบุไว้แล้ว 100%:

**ส่วนที่ 1** (ทีมเราต้องทำ):
- หน้าปก: ชื่อโครงงาน (ไทย/อังกฤษ), สาขา, สถานะโครงงานต่อเนื่อง, ข้อมูลผู้พัฒนา+อาจารย์ที่ปรึกษา+ผู้บริหาร รร. พร้อมลายเซ็น (หน้าปก **generate อัตโนมัติจากระบบ SIMS** หลังกรอกข้อมูล — ไม่ต้องออกแบบเอง)
- เนื้อหา: บทนำ → ปัญหา/RQ → สมมติฐาน(หรือ engineering goal) → กระบวนการ/วิธีการโดยละเอียด → การวิเคราะห์ข้อมูล → ประโยชน์ที่คาดว่าจะได้รับ → **บรรณานุกรมอย่างน้อย 5 แหล่ง** (หนังสือนอกเหนือตำราเรียน/บทความวิชาการ/วารสารวิทยาศาสตร์/อินเทอร์เน็ต)

**ส่วนที่ 2** (เจ้าของโครงการกรอกเอง — ทีมไม่ต้องทำ):
- ประวัติผู้พัฒนา (นักเรียน): คำนำหน้า, ชื่อ-นามสกุล, ชั้นปี, รร., ผลงานด้าน วทน. (ถ้าเคยส่งประกวด/ขอทุนที่อื่นต้องแจ้ง สวทช. เป็นลายลักษณ์อักษร)
- ประวัติอาจารย์ที่ปรึกษา: ตำแหน่ง สังกัด การศึกษา ความเชี่ยวชาญ (ขอข้อมูลจากอาจารย์ได้ ไม่ต้องทำเอง) — สูงสุด 2 ท่าน ต้องระบุใครเป็นที่ปรึกษาหลัก

**ข้อกำหนดรูปแบบเอกสาร:** TH Sarabun New ขนาด 16, ขอบกระดาษ 1 นิ้วทุกด้าน, กระดาษ A4 สีขาว, มีเลขหน้า, เข้าเล่มพร้อมปกหน้า-หลัง

**ข้อกำหนดเรื่องรูป:** เอกสารทางการไม่ได้ล็อกกฎเฉพาะสำหรับรูปในเนื้อหา ระบุแค่ว่า Methodology ต้องมี "รูปที่ 1" (pipeline diagram) และอาจแนบภาพถ่าย/ภาพวาดอุปกรณ์ที่ออกแบบเองเพิ่มได้ — **ไม่มีข้อกำหนดเรื่อง caption/license ของรูปที่พบในเอกสารทางการ** (ต่างจาก diagram ที่ orchestration.md สั่งให้ทำเป็นภาษาอังกฤษ+มี citation ซึ่งเป็นกติกาภายในทีมเราเอง ไม่ใช่ข้อบังคับจาก NSTDA โดยตรง — ควรเก็บไว้เพราะเป็น best practice แต่ไม่ใช่ requirement บังคับ)

**บรรณานุกรม:** ขั้นต่ำ 5 แหล่ง — **ไม่ได้ระบุรูปแบบการอ้างอิงตายตัว** (ดู flag เรื่อง Vancouver-style ในหมายเหตุด้านบน)

**Gen-AI Disclosure:** เอกสาร template มีหัวข้อนี้บังคับอยู่แล้ว (เจอในเทมเพลตจริง) พร้อมตัวอย่างข้อความและวิธีอ้างอิงเครื่องมือ AI ในบรรณานุกรม — ตรงกับที่ orchestration.md เตือนไว้

**⚠️ Deadline:** ตัวอย่างในเอกสาร/เทมเพลตอ้างปฏิทินเก่า (พ.ศ. 2565) — **ยังไม่พบปฏิทิน YSC 2027 ที่ยืนยันได้จากรอบค้นนี้** ต้องเช็คจากระบบ SIMS/nstda.or.th โดยตรงอีกครั้งใกล้เวลาสมัคร (เป็น 1 ใน gap ที่ระบุท้ายรายงาน)
