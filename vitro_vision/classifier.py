"""โหลด model + run inference บนภาพขวด"""
import os
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms

from .config import MODEL_PATH, CONF_MIN

LABELS = ["healthy", "contaminated", "dead"]

_model = None
_model_loaded = False
_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_model():
    global _model, _model_loaded
    if _model_loaded:
        return _model
    if not os.path.exists(MODEL_PATH):
        _model_loaded = True
        _model = None
        return None
    try:
        _model = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
        _model.eval()
        print(f"โหลด model จาก {MODEL_PATH}")
    except Exception as e:
        print(f"[classifier] โหลด model ไม่ได้: {e}")
        _model = None
    _model_loaded = True
    return _model


def is_model_ready() -> bool:
    return load_model() is not None


def predict(image_bgr: np.ndarray) -> tuple[str, float]:
    """คืน (status_label, confidence) — ถ้าไม่มี model คืน ('unknown', 0.0)"""
    model = load_model()
    if model is None:
        return "unknown", 0.0
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    tensor = _transform(rgb).unsqueeze(0)
    with torch.no_grad():
        logits = model(tensor)
        probs  = F.softmax(logits, dim=1)[0]
    idx  = probs.argmax().item()
    conf = probs[idx].item()
    label = LABELS[idx] if conf >= CONF_MIN else "unknown"
    return label, conf
