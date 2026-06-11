# 09 — Methods Misc: Active Learning, ArUco, Kruskal-Wallis

> รวบรวมเอกสารอ้างอิงสำหรับ 3 method หลักของโปรเจกต์ VitroVision  
> ค้นด้วย Consensus + PubMed — วันที่: 2026-06-11

---

## 1. Active Learning — Uncertainty Sampling & MC Dropout

### แนวคิดหลัก

Active Learning (AL) คือกลยุทธ์เลือกตัวอย่างให้ human annotator label เฉพาะภาพที่ model "ไม่มั่นใจ" มากที่สุด แทนการ label ทุกภาพ ผลลัพธ์คือประหยัด annotation cost อย่างมีนัยสำคัญ

**Least-Confidence Sampling** เป็น uncertainty sampling แบบง่ายที่สุด: เลือกตัวอย่างที่ค่า max predicted probability ต่ำที่สุด ซึ่งงาน benchmark พบว่าให้ผลไม่ต่างจาก state-of-the-art BADGE เมื่อใช้ data augmentation ร่วมด้วย [2]

**MC Dropout (Monte Carlo Dropout)** — Gal & Ghahramani (2015/2016) พิสูจน์ว่า neural network ที่เปิด dropout ระหว่าง inference หลายรอบ (T forward passes) มีความเท่าเทียมทางคณิตศาสตร์กับ approximate Bayesian inference ใน deep Gaussian process [4] ผลที่ได้คือ uncertainty estimate โดยไม่ต้องเพิ่ม computational cost หรือลด test accuracy — paper นี้ได้รับการอ้างอิงมากกว่า **11,600 ครั้ง** ยืนยันว่าเป็น foundational work ที่ verified แล้ว

### Label Efficiency ที่วัดได้

- Uncertainty Sampling และ Margin Sampling บรรลุ 90% accuracy ด้วยตัวอย่าง label **น้อยกว่า Random Sampling ~33%** (MNIST benchmark) [1]
- เมื่อใช้ data augmentation ร่วม: AL มี label efficiency สูงกว่า random sampling **2x–4x** [2]
- Cost-Effective AL (CEAL) รวม pseudo-labeling สำหรับ high-confidence samples เข้ากับ uncertainty sampling — ลด manual annotation ลงอีกในงาน face recognition และ object categorization [3]

### ความเหมาะสมกับ VitroVision

VitroVision มีภาพขวดเพาะเลี้ยง ~100 ขวด × 5 สูตร MS ซึ่งเป็น small-scale dataset ทั่วไปใน lab setting โดย AL + MC Dropout ช่วยให้ train model ได้คุณภาพสูงโดยไม่ต้อง label ทุกภาพ ซึ่งตรงกับข้อจำกัดด้านเวลาของโครงงานระดับ YSC

---

## 2. ArUco / Fiducial Markers ใน Plant & Lab Setting

### มี Precedent ไหม?

**มี** — fiducial markers รวมถึง ArUco ถูกใช้ในงาน lab automation และ specimen tracking แล้ว:

- ArUco markers ถูกใช้ใน **robotic arm laboratory automation** สำหรับ bioanalytical research โดยตรง [6] ระบบใช้ OpenCV + ArUco ร่วมกับ Python เพื่อสร้าง 3D digital model ของสภาพแวดล้อม robot และ automate การอ่านค่า — error rate เพียง 1.69% ซึ่งสำคัญมากเพราะแสดงว่า ArUco ในบริบท lab + Python + OpenCV เป็น established workflow
- งาน customizable fiducial markers [5] แสดงว่า marker system สามารถ encode unique identifier สำหรับแต่ละ object ได้ ตรงกับการ track `bottle_id` ของ VitroVision
- ArUco บน HoloLens 2 [7] แสดง translation error ต่ำถึง **1.36 mm** ยืนยัน precision ที่เพียงพอสำหรับ lab use

### การประยุกต์กับ VitroVision

การติด ArUco marker (DICT_4X4_100) ข้างขวดเพาะเลี้ยงเนื้อเยื่อเพื่อ encode `bottle_id` มี precedent ชัดเจนในวรรณกรรม โดยเฉพาะงาน Wienbruch et al. (2025) [6] ที่ใช้ ArUco + OpenCV ใน bioanalytical lab workflow ตรงกับ tech stack ของโปรเจกต์ (Python + OpenCV)

---

## 3. Kruskal-Wallis ใน Plant Experiments — Small Sample / Non-Normal

### เหตุผลที่เลือก Non-Parametric

Kruskal-Wallis เป็น non-parametric counterpart ของ one-way ANOVA สำหรับเปรียบเทียบ **มากกว่า 2 กลุ่มอิสระ** โดยไม่ต้องสมมติ normality ของ error term — ต้องการเพียง independence ของ random error [8]

### ความเหมาะสมกับ Small Sample

- งาน Ostertagová et al. (2014) [8] ยืนยันว่า Kruskal-Wallis เป็น powerful alternative ต่อ one-way ANOVA และใช้ต่อด้วย nonparametric multiple comparison เมื่อ statistic มีนัยสำคัญ
- Dwivedi et al. (2017) [9] พบว่า nonparametric tests เหมาะสมกับ small sample size ในงาน biomedical โดยเฉพาะเมื่อข้อมูลไม่เป็น normal distribution — เป็น scenario ตรงกับ tissue culture ที่มีขวดจำนวนจำกัดต่อ treatment
- Jan et al. (2025) [10] เสนอ F-transformation ของ Kruskal-Wallis H เพื่อแก้ปัญหา chi-square approximation ที่ conservative มากใน small sample — เป็น refinement ล่าสุดที่ควรพิจารณา

### การประยุกต์กับ VitroVision

VitroVision เปรียบเทียบ 5 สูตร MS (treatment groups) บน phenotype metrics (shoot height, leaf count, chlorophyll proxy จาก SPAD proxy ใน image) ด้วย sample size ต่อ group ที่อาจไม่เป็น normal distribution Kruskal-Wallis จึงเป็นตัวเลือกที่ defendable ทั้งใน YSC abstract และ methodology section

---

## References

[1] [Comparative Analysis of Active Learning Algorithms for Data-Efficient Image Classification](https://consensus.app/papers/details/8f7a6be18e6d5e3481b72dc7f83f4e57/?utm_source=claude_code) (Prof. Valarmathi, 2025, International Journal of Innovative Research in Information Security, 0 citations)

[2] [Effective Evaluation of Deep Active Learning on Image Classification Tasks](https://consensus.app/papers/details/6aaa829916b15404ad06f3c06a08d77f/?utm_source=claude_code) (Nathan Beck et al., 2021, ArXiv, 48 citations)

[3] [Cost-Effective Active Learning for Deep Image Classification](https://consensus.app/papers/details/ae04b197642b5ab3bb1c10bde2e6df46/?utm_source=claude_code) (Keze Wang et al., 2017, IEEE Transactions on Circuits and Systems for Video Technology, 741 citations)

[4] [Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning](https://consensus.app/papers/details/93e51bd77c8c54e291d7ef8dc0bb8815/?utm_source=claude_code) (Y. Gal & Z. Ghahramani, 2015, 11,672 citations) — **verified foundational paper สำหรับ MC Dropout**

[5] [Design, Detection, and Tracking of Customized Fiducial Markers](https://consensus.app/papers/details/6bac5cd4f229508e865cb737c83b0a44/?utm_source=claude_code) (David Jurado-Rodríguez et al., 2021, IEEE Access, 34 citations)

[6] [Facilitating laboratory automation using a robot with a simple and inexpensive camera detection system](https://consensus.app/papers/details/d5f932accbc657b7a4da3f8a72f86058/?utm_source=claude_code) (Rebecca Wienbruch et al., 2025, Scientific Reports, 3 citations) — **ArUco + OpenCV ใน bioanalytical lab — precedent ตรงที่สุด**

[7] [Assessment of Multiple Fiducial Marker Trackers on Hololens 2](https://consensus.app/papers/details/3c0f7c58a4ca5befb59db79e44b3c813/?utm_source=claude_code) (G. M. Costa et al., 2024, IEEE Access, 20 citations)

[8] [Methodology and Application of the Kruskal-Wallis Test](https://consensus.app/papers/details/b895d786c826511f9c75cdd3dedd483c/?utm_source=claude_code) (E. Ostertagová et al., 2014, Applied Mechanics and Materials, 696 citations)

[9] [Analysis of small sample size studies using nonparametric bootstrap test with pooled resampling method](https://consensus.app/papers/details/26187e4e7b515093b53fde02fce0daccf/?utm_source=claude_code) (A. Dwivedi et al., 2017, Statistics in Medicine, 288 citations)

[10] [Alternative Nonparametric Test and Sample Size Procedures for the Comparison of Several Location Shifts](https://consensus.app/papers/details/71cd653c7e8859d2af1aafddc20daccf/?utm_source=claude_code) (S. Jan et al., 2025, Journal of Statistical Theory and Applications, 2 citations)

---

*Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code*
