# 💻 รายการ Software ของ VitroVision — แยกหมวด + แหล่งที่มา

> สร้าง 2026-09 · ใช้ประกอบมาตรา 4.1 วัสดุอุปกรณ์ (ฝั่ง software) และการเปิดเผยการใช้งานซอฟต์แวร์
> ลำดับ: **Environment / Library / Model / Dataset / Service** (แยกชัด แล้วระบุที่มาแต่ละตัว)

---

## 🧰 Environment — เครื่องมือพัฒนา/รัน
| ซอฟต์แวร์ | ใช้ทำอะไร | แหล่งที่มา (ผู้สร้าง/เจ้าของ) |
|-----------|-----------|------------------------------|
| **Python 3** | ภาษาหลักของทั้งโปรเจกต์ | Python Software Foundation (open-source, https://python.org) |
| **Jupyter / Colab notebook** | สคริปต์แบบ cells รันบนคลาวด์ | Project Jupyter · Google Colab |
| **Git / GitHub** | ควบคุมเวอร์ชัน + เก็บโค้ด | Git (open-source) · GitHub, Inc. |

## 📚 Library — โค้ดที่เรา import (จาก `requirements.txt`)
| Library | ใช้ทำอะไร | แหล่งที่มา |
|---------|-----------|-----------|
| **PyTorch (`torch>=2.1`)** | เทรน/รันโมเดล deep learning | Meta AI (open-source, pytorch.org) |
| **torchvision** | utilities สำหรับ vision | Meta AI / PyTorch team |
| **transformers** | โหลด SAM3 (Sam3Processor/Sam3Model) | Hugging Face (github.com/huggingface/transformers) |
| **accelerate** | ประมวลผลหลายอุปกรณ์ GPU | Hugging Face |
| **huggingface_hub** | ดาวน์โหลดโมเดล/ชุดข้อมูลจาก HF | Hugging Face |
| **segmentation-models-pytorch (smp)** | **สร้าง U-Net** (encoder MobileNetV3) | Pavel Yakubovskiy (github.com/qubvel) |
| **timm** | โหลด MobileNetV3 backbone | Ross Wightman (github.com/huggingface/pytorch-image-models) |
| **opencv-python** | ประมวลผลภาพ (ROI, mask, overlay) | OpenCV Team |
| **numpy** | คณิตศาสตร์/array | NumPy developers |
| **pillow (PIL)** | จัดการภาพ | Python Imaging Library |
| **gradio (`>=4.44`)** | สร้างเว็บแอป (HF Space) | Gradio, Hugging Face |
| **pandas** | จัดการตารางข้อมูล (CSV/XLSX) | pandas developers |
| **matplotlib / seaborn** | สร้างกราฟ/ภาพ | Matplotlib · seaborn |
| **tabulate** | จัดตารางข้อความ | open-source |
| **openpyxl** | อ่าน/เขียน Excel | openpyxl developers |

## 🧠 Model — แบบจำลอง AI ที่ใช้
| Model | ขนาด | ใช้ทำอะไร | แหล่งที่มา |
|-------|------|-----------|-----------|
| **SAM3 (facebook/sam3)** — teacher | ~848M params | สร้าง pseudo-labels (ต้นแบบ) | Meta AI (Carion et al. 2025) · HuggingFace |
| **U-Net + MobileNetV3-Small** — โมเดลเรา | ~3.6M params | ตัวแบ่งส่วนภาพจริง (distilled) | สร้างเองจาก smp (ใช้ใน repo) |
| **MobileNetV3-Small** — backbone | เบา | encoder ของ U-Net | Howard et al. 2019 (timm, ImageNet weights) |

## 📊 Dataset — ชุดข้อมูลที่ใช้ฝึก/ทดสอบ
| ชุดข้อมูล | รายละเอียด | แหล่งที่มา |
|-----------|-----------|-----------|
| **`greenhouse_leafy_segmentation`** | 1,200 ภาพ/มาสก์ ฝึกโมเดล | Project-AgML (HuggingFace, public) |
| **ชุดภาพ 100 ขวดพริกจินดา** | ภาพถ่ายจริง + ground truth จากผู้เชี่ยวชาญ (test/eval only) | สร้างโดยทีม VitroVision (ห้องแล็บ) |

## ☁️ Service — บริการคลาวด์/เผยแพร่
| Service | ใช้ทำอะไร | แหล่งที่มา (เจ้าของ) |
|---------|-----------|---------------------|
| **Google Colab** | ประมวลผล/เทรนโมเดลบน GPU T4 | Google |
| **Hugging Face Model Hub** | เผยแพร่โมเดล `vitrovision-unet-small` | Hugging Face, Inc. |
| **Hugging Face Space** | โฮสต์เว็บแอป Gradio | Hugging Face, Inc. |

---

## 🧾 สรุปภาพรวม software-centric
- **เขียนเอง:** U-Net + MobileNetV3 (โค้ดใน `src/`), pipeline, แอป Gradio
- **ใช้ของ open-source:** PyTorch, smp, timm, OpenCV, numpy, pandas ฯลฯ
- **ใช้ของ third-party (บริการ):** Google Colab, Hugging Face
- **ใช้โมเดลสำเร็จรูป:** SAM3 (Meta AI) เป็น teacher
- **ใบอนุญาตต้องเช็ค:** SAM3 ใช้ **SAM License** (ไม่ใช่ MIT/Apache) — ระวังก่อนตีพิมพ์
