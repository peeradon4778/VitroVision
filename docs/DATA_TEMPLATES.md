# แม่แบบไฟล์ข้อมูลเสริม (ใส่ใน /content/data ก่อนรัน Colab)

> ไฟล์จริงวางที่ `/content/data` (data/raw หรือ data/processed ไม่ push GitHub)
> ถ้าไม่มีไฟล์เหล่านี้ pipeline รันได้ตามปกติ — ใส่เมื่อมีข้อมูลจริงเท่านั้น

## 1) ground_truth.csv — ค่าที่วัดมือ (ใช้คำนวณ Pearson/MAE/RMSE)

คอลัมน์: `image,leaf_count,shoot_count,root_count,height_cm,width_cm,area_cm2`

```csv
image,leaf_count,shoot_count,root_count,height_cm,width_cm,area_cm2
20260716_165222.jpg,8,1,0,4.2,2.1,6.8
20260716_165223.jpg,6,1,0,3.8,2.0,6.1
```

- `image` = ชื่อไฟล์ตรงกับในโฟลเดอร์เป๊ะ (รวม .jpg)
- `height_cm/width_cm/area_cm2` = วัดจริงด้วยไม้บรรทัด/กระดาษกราฟ
- วิธีวัดมือ (แนะนำ): นับใบทั้งหมดที่มองเห็นผ่านขวด + วัดความสูงจากโคนถึงยอด

## 2) species_map.csv — ระบุชนิดต่อภาพ (คอลัมน์ข้อมูลเท่านั้น ยังไม่เปลี่ยน verdict)

คอลัมน์: `image,species`

```csv
image,species
20260716_165222.jpg,กล้วย
20260716_165233.jpg,กล้วยไม้
```

- เปิด `USE_SPECIES_THRESHOLDS=True` ใน config เมื่ออยากให้ verdict ใช้ threshold ต่อชนิด
- ชนิดที่รองรับในตาราง threshold: กล้วย, กล้วยไม้, มันฝรั่ง (เพิ่มเองได้ใน cell config)

## 3) ground_truth_masks/ — masks กำกับด้วยมือ (ใช้ benchmark คำนวณ mIoU/Dice)

โฟลเดอร์ `ground_truth_masks/` (วางข้าง data/) มีไฟล์ `<ชื่อภาพ>.png` (binary: ขาว = ต้นพืช):

```
ground_truth_masks/
├── 001.png   ← ตรงกับ 001.jpg (ขาว = plant, ดำ = พื้นหลัง)
├── 002.png
└── ...
```

**วิธี annotate (แนะนำ):**
- เปิดภาพในโปรแกรมระบาย mask เช่น Label Studio / CVAT / GIMP / Photoshop (หรือแม้แต่ Paint)
- ระบายพื้นที่ "ต้นพืช" ทั้งหมด (ใบ + ลำต้น ที่มองเห็นผ่านขวด) เป็นสีขาว พื้นหลังสีดำ
- บันทึกเป็น PNG ขนาดเท่าภาพต้นฉบับ (หรือสัดส่วนเดียวกัน — script resize ให้อัตโนมัติ)
- จำนวนแนะนำ: ≥ 30 ภาพ ครอบคลุม 3 คลาส (wait / subculture / transplant-overdue)
- ถ้าทำได้ ให้ annotate ≥ 2 คน แล้วรายงาน inter-rater agreement (เช่น Cohen's kappa)

**รัน benchmark:**
```
python benchmark_colab.py --data <โฟลเดอร์ภาพ> --gt ground_truth_masks --out <ผลลัพธ์>
```
