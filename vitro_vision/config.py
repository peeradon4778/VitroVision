import os

SHELF_API   = os.getenv("SHELF_API", "http://localhost:5001")
MODEL_PATH  = os.path.join(os.path.dirname(__file__), "..", "models", "final", "classifier.pt")
ARUCO_DICT  = "DICT_4X4_100"   # ต้องตรงกับ generate_aruco.py + detector.py + aruco_map.py
CONF_MIN    = 0.70
GROWTH_CURVES = {}   # day → expected ranges (populate หลังมี dataset)
