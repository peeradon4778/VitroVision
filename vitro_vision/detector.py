"""ArUco marker detection — อ่าน bottle_id จาก marker ID"""
import cv2
import numpy as np

# DICT_4X4_100 รองรับ 100 ขวด (ID 0–99) — ต้องตรงกับ export_aruco_png.py
_aruco_dict   = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
_aruco_params = cv2.aruco.DetectorParameters()
# ปรับ params สำหรับ marker ติดข้างขวด (เห็นเป็นมุมเฉียง + แสงไม่สม่ำเสมอ)
_aruco_params.adaptiveThreshConstant = 7
_aruco_params.perspectiveRemovePixelPerCell = 8
_aruco_params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
_detector     = cv2.aruco.ArucoDetector(_aruco_dict, _aruco_params)

# map marker_id → bottle_id (สร้างตอน label printing)
# เช่น {0: "S01-A-01", 1: "S01-A-02", ...}
MARKER_MAP: dict[int, str] = {}


def detect_markers(frame: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """คืน list ของ (marker_id, corners) ที่พบในภาพ"""
    corners, ids, _ = _detector.detectMarkers(frame)
    if ids is None:
        return []
    return [(int(ids[i][0]), corners[i]) for i in range(len(ids))]


def marker_to_bottle(marker_id: int) -> str | None:
    return MARKER_MAP.get(marker_id)


def draw_markers(frame: np.ndarray, detections: list) -> np.ndarray:
    """วาด overlay ArUco + label บนภาพ (สำหรับ preview)"""
    out = frame.copy()
    for mid, corners in detections:
        cv2.aruco.drawDetectedMarkers(out, [corners])
        bottle_id = marker_to_bottle(mid) or f"#{mid}"
        pt = corners[0][0].astype(int)
        cv2.putText(out, bottle_id, tuple(pt), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 0), 2)
    return out
