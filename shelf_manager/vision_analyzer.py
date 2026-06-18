import io
import json
import os
from pathlib import Path

import PIL.Image
from google import genai
from google.genai import types

_client = None


def _load_env():
    if os.environ.get("GOOGLE_API_KEY"):
        return
    for candidate in [
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env",
    ]:
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                    os.environ["GOOGLE_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return


def _get_client():
    global _client
    if _client is None:
        _load_env()
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


PROMPT = """\
วิเคราะห์สภาพพืช Capsicum annuum (พริก) ในขวดแยมแก้ว 240mL บนอาหาร MS ถ่ายผ่านกระจกปิดผนึก

ตอบ JSON เท่านั้น ห้ามมี ``` ห้ามมีคำอธิบายอื่น:
{"status":"","vigor":0,"dev_stage":"","contamination_signs":"","notes":""}

กฎ:
- status: "healthy"=เขียวสด | "contaminated"=มีรา/แบคทีเรีย ขุ่น/ดำ/น้ำตาล | "dead"=ตาย ซีด | "unknown"=มองไม่ชัด
- vigor: 1–5 (1=แย่มาก, 3=ปกติ, 5=ดีมาก); 0 ถ้า unknown/dead
- dev_stage: "radicle"|"hypocotyl"|"cotyledon"|"true_leaf"|"" ถ้าไม่แน่ใจ
- contamination_signs: อธิบายถ้าเห็น หรือ ""
- notes: ข้อสังเกต ≤50 ตัวอักษร หรือ ""
"""


def analyze_plant_image(image_bytes: bytes) -> dict:
    client = _get_client()
    img = PIL.Image.open(io.BytesIO(image_bytes))
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[img, PROMPT],
    )
    text = response.text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    result = json.loads(text)
    result.setdefault("status", "unknown")
    result.setdefault("vigor", 0)
    result.setdefault("dev_stage", "")
    result.setdefault("contamination_signs", "")
    result.setdefault("notes", "")
    if result["status"] not in ("healthy", "contaminated", "dead", "unknown"):
        result["status"] = "unknown"
    return result
