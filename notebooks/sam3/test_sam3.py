import os
import sys
import numpy as np
from PIL import Image
import cv2

# ตรวจสอบ device
try:
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] device = {device}")
    if device == "cpu":
        print("[WARN] SAM3 0.9B params on CPU จะช้ามาก (แนะนำ Colab/Kaggle GPU)")
except ImportError:
    device = "cpu"
    print("[WARN] torch not installed")

HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    print("[WARN] ยังไม่มี HF_TOKEN ใน environment variables")
    print("       ตั้งค่า: $env:HF_TOKEN='hf_...' (PowerShell)")
    print("       หรือ login: huggingface-cli login")

print(f"\nกำลังโหลด SAM3 (facebook/sam3)...")
print("(ครั้งแรกจะ download weights ~2GB)")

from transformers import pipeline

pipe = pipeline(
    "mask-generation",
    model="facebook/sam3",
    trust_remote_code=True,
    device=device,
    token=HF_TOKEN,
)

print("โหลดเสร็จ!")

IMG_PATH = None
for p in ["test_plant.jpg", "test.jpg", "sample.jpg"]:
    if os.path.exists(p):
        IMG_PATH = p
        break

if not IMG_PATH:
    print("\nไม่พบรูปตัวอย่าง — สร้างรูปเทียมสำหรับทดสอบ")
    img = Image.new("RGB", (640, 480), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    draw.ellipse([200, 100, 400, 300], fill=(34, 139, 34))
    draw.ellipse([280, 180, 340, 240], fill=(50, 50, 200))
    img.save("test_plant.jpg")
    IMG_PATH = "test_plant.jpg"

img = Image.open(IMG_PATH).convert("RGB")
print(f"รูป: {IMG_PATH} ({img.size})")

print("\n--- SAM3 PCS: Promptable Concept Segmentation ---")
text_prompts = ["plant", "leaf", "shoot"]

for prompt in text_prompts:
    print(f'\n>> prompt = "{prompt}"')
    try:
        outputs = pipe(
            img,
            text_prompts=[prompt],
            points_per_batch=32,
        )
        masks = outputs.get("masks", [])
        scores = outputs.get("scores", [])
        print(f"   found {len(masks)} masks")

        # visualize
        vis = np.array(img).copy()
        for i, (mask, score) in enumerate(zip(masks, scores)):
            if score and score < 0.5:
                continue
            mask_np = np.array(mask, dtype=np.uint8) * 255
            contours, _ = cv2.findContours(mask_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(vis, contours, -1, (0, 255, 0), 2)

        out_path = f"sam3_{prompt}.png"
        Image.fromarray(vis).save(out_path)
        print(f"   saved -> {out_path}")

    except Exception as e:
        print(f"   ERROR: {e}")

print("\n✅ เสร็จ!")
