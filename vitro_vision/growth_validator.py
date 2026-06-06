"""ตรวจสอบว่าการเจริญที่วัดได้สมเหตุสมผลกับ day_point หรือไม่"""
from .config import GROWTH_CURVES


def validate(day_point: int, shoot_count: int = -1,
             vigor_score: int = 0) -> dict:
    """
    คืน dict:
      ok       — True ถ้า growth อยู่ในช่วงที่คาดไว้
      warnings — list ของข้อสังเกตุ
    growth_curves ยังว่างอยู่ ระหว่างเก็บ dataset —
    ฟังก์ชันนี้จะถูก populate หลังวิเคราะห์ข้อมูล Phase 2
    """
    warnings = []

    if not GROWTH_CURVES:
        return {"ok": True, "warnings": ["ยังไม่มี growth curve — ข้ามการ validate"]}

    curve = GROWTH_CURVES.get(day_point)
    if curve is None:
        return {"ok": True, "warnings": [f"ไม่มีข้อมูล curve สำหรับ Day {day_point}"]}

    if shoot_count >= 0:
        lo, hi = curve.get("shoot_count", (0, 999))
        if not (lo <= shoot_count <= hi):
            warnings.append(f"ยอด {shoot_count} ผิดปกติ (คาด {lo}–{hi} ที่ Day {day_point})")

    if vigor_score > 0:
        lo, hi = curve.get("vigor", (1, 5))
        if not (lo <= vigor_score <= hi):
            warnings.append(f"Vigor {vigor_score} ผิดปกติ (คาด {lo}–{hi} ที่ Day {day_point})")

    return {"ok": len(warnings) == 0, "warnings": warnings}
