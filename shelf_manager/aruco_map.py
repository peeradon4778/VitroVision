"""ArUco marker map — ID 0-99 ต่อขวด 100 ใบ"""
ROWS    = ['A', 'B', 'C', 'D', 'E']
COLS    = [f'{i:02d}' for i in range(1, 11)]
SHELVES = ['S01', 'S02']

# marker_id (0-99) → bottle_id
MARKER_MAP: dict[int, str] = {}
_mid = 0
for _shelf in SHELVES:
    for _row in ROWS:
        for _col in COLS:
            MARKER_MAP[_mid] = f'{_shelf}-{_row}-{_col}'
            _mid += 1

# bottle_id → marker_id (reverse)
BOTTLE_MAP: dict[str, int] = {v: k for k, v in MARKER_MAP.items()}

try:
    import cv2
    import numpy as np

    _dict   = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    _params = cv2.aruco.DetectorParameters()
    _det    = cv2.aruco.ArucoDetector(_dict, _params)

    def detect(image_bytes: bytes) -> list[dict]:
        """คืน list ของ {bottle_id, corners [[x,y]×4], frame_w, frame_h}"""
        arr = np.frombuffer(image_bytes, np.uint8)
        bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if bgr is None:
            return []
        h, w = bgr.shape[:2]
        corners_list, ids, _ = _det.detectMarkers(bgr)
        if ids is None:
            return []
        found = []
        for i in range(len(ids)):
            mid = int(ids[i][0])
            if mid in MARKER_MAP:
                found.append({
                    'bottle_id': MARKER_MAP[mid],
                    'corners':   corners_list[i][0].tolist(),
                    'frame_w':   w,
                    'frame_h':   h,
                })
        return found

    def calc_clarity(corners) -> int:
        """วัดความชัดของ marker จาก corners [[x,y]×4]"""
        c = np.array(corners)
        d1 = np.linalg.norm(c[0] - c[2])
        d2 = np.linalg.norm(c[1] - c[3])
        size_score = min((d1 + d2) / 2 / 80.0, 1.0)
        sides = [np.linalg.norm(c[i] - c[(i+1)%4]) for i in range(4)]
        mean_s = float(np.mean(sides))
        shape_score = max(0.0, 1 - float(np.std(sides)) / mean_s) if mean_s > 0 else 0.0
        return round((size_score * 0.7 + shape_score * 0.3) * 100)

    ARUCO_OK = True

except Exception:
    def detect(image_bytes: bytes) -> list[dict]:
        return []
    def calc_clarity(corners) -> int:
        return 0
    ARUCO_OK = False
