"""โหลด classifier.pt และ predict — auto-reload เมื่อ model อัปเดต"""
import cv2, numpy as np, torch, torch.nn.functional as F
from pathlib import Path
from torchvision import transforms

LABELS     = ['healthy', 'contaminated', 'dead']
CONF_MIN   = 0.55
MODEL_PATH = Path(__file__).parent.parent / 'models' / 'final' / 'classifier.pt'

_model = None
_mtime = 0.0

_tf = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def _reload():
    global _model, _mtime
    if not MODEL_PATH.exists():
        _model = None
        return
    t = MODEL_PATH.stat().st_mtime
    if t == _mtime:
        return
    try:
        _model = torch.load(str(MODEL_PATH), map_location='cpu', weights_only=False)
        _model.eval()
        _mtime = t
        print(f'[inference] โหลด model ใหม่ ({MODEL_PATH.name})')
    except Exception as e:
        print(f'[inference] โหลดไม่ได้: {e}')
        _model = None


def ready() -> bool:
    _reload()
    return _model is not None


def predict_bytes(image_bytes: bytes) -> tuple[str, float]:
    """รับ bytes ของภาพ คืน (label, confidence) — ('unknown', 0.0) ถ้าไม่มี model"""
    _reload()
    if _model is None:
        return 'unknown', 0.0
    arr = np.frombuffer(image_bytes, np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        return 'unknown', 0.0
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    tensor = _tf(rgb).unsqueeze(0)
    with torch.no_grad():
        probs = F.softmax(_model(tensor), dim=1)[0]
    idx  = probs.argmax().item()
    conf = probs[idx].item()
    return (LABELS[idx] if conf >= CONF_MIN else 'unknown'), round(conf, 4)


def predict_mc_dropout(image_bytes: bytes, n_passes: int = 10) -> dict:
    """MC Dropout inference — คืน uncertainty จาก variance ระหว่าง n_passes forward pass"""
    _reload()
    if _model is None:
        return {'label': 'unknown', 'confidence': 0.0, 'uncertainty': 1.0,
                'probs': {l: 0.0 for l in LABELS}}
    arr = np.frombuffer(image_bytes, np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        return {'label': 'unknown', 'confidence': 0.0, 'uncertainty': 1.0,
                'probs': {l: 0.0 for l in LABELS}}
    rgb    = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    tensor = _tf(rgb).unsqueeze(0)
    _model.train()
    try:
        probs_list = []
        with torch.no_grad():
            for _ in range(n_passes):
                probs_list.append(F.softmax(_model(tensor), dim=1)[0])
        mean_probs  = torch.stack(probs_list).mean(0)
        idx         = mean_probs.argmax().item()
        confidence  = mean_probs[idx].item()
        uncertainty = 1 - confidence
        return {
            'label':       LABELS[idx] if confidence >= CONF_MIN else 'unknown',
            'confidence':  round(confidence,  4),
            'uncertainty': round(uncertainty, 4),
            'probs':       {LABELS[i]: round(mean_probs[i].item(), 4) for i in range(len(LABELS))},
        }
    finally:
        _model.eval()
