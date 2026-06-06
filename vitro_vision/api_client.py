"""ส่งผล inference ไปยัง VitroShelf REST API"""
import requests
from .config import SHELF_API


def get_bottle(bottle_id: str) -> dict:
    r = requests.get(f"{SHELF_API}/api/bottle/{bottle_id}", timeout=5)
    r.raise_for_status()
    return r.json()


def post_observation(bottle_id: str, day_point: int, status: str,
                     shoot_count: int = -1, media_color: str = "normal",
                     hyperhydricity: bool = False, has_roots: bool = False,
                     ai_status: str = "", ai_confidence: float = 0.0) -> dict:
    payload = {
        "day_point": day_point, "status": status,
        "shoot_count": shoot_count, "media_color": media_color,
        "hyperhydricity": hyperhydricity, "has_roots": has_roots,
        "ai_status": ai_status, "ai_confidence": ai_confidence,
    }
    r = requests.post(f"{SHELF_API}/api/bottle/{bottle_id}/observation",
                      json=payload, timeout=5)
    r.raise_for_status()
    return r.json()
