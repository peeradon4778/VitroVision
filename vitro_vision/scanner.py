"""
VitroVision — Live Scanner
รัน: conda activate ml && python -m vitro_vision.scanner --day 14

กด Q เพื่อออก | SPACE เพื่อ capture ขวดปัจจุบัน
"""
import argparse
import sys
import cv2
from . import detector, classifier, growth_validator, api_client

# สีสำหรับ status
STATUS_COLOR = {
    "healthy":      (0, 200, 0),
    "contaminated": (0, 60, 255),
    "dead":         (100, 100, 100),
    "unknown":      (0, 200, 255),
}

def _put_text(img, text, pos, color=(255, 255, 255), scale=0.7, thickness=2):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness + 2)
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)


def run(day_point: int, cam_index: int = 0):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        sys.exit(f"ไม่สามารถเปิดกล้อง index={cam_index}")

    model_ok = classifier.is_model_ready()
    mode_label = "RESEARCH TRACKING" if model_ok else "SCREENING (no model)"
    print(f"VitroVision Scanner — Day {day_point} | {mode_label}")
    print("SPACE = capture | Q = ออก")

    current_bottle = None
    last_result = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_markers(frame)
        preview = detector.draw_markers(frame, detections)

        if detections:
            current_bottle = detector.marker_to_bottle(detections[0][0])

        h = preview.shape[0]

        # แถบข้อมูลล่าง
        cv2.rectangle(preview, (0, h - 80), (preview.shape[1], h), (30, 30, 30), -1)

        if current_bottle:
            _put_text(preview, f"Bottle: {current_bottle}", (10, h - 55), (0, 255, 120))
        else:
            _put_text(preview, "ไม่พบ marker", (10, h - 55), (0, 200, 255))

        _put_text(preview, f"Day {day_point} | SPACE=capture  Q=ออก", (10, h - 20))

        if not model_ok:
            _put_text(preview, "NO MODEL", (preview.shape[1] - 150, 30), (0, 60, 255))

        if last_result:
            _put_text(preview, last_result, (10, 35), (255, 255, 100))

        cv2.imshow("VitroVision", preview)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        if key == ord(' ') and current_bottle:
            status, conf = classifier.predict(frame)
            growth = growth_validator.validate(day_point)

            last_result = f"{current_bottle}: {status} {conf:.0%}"
            if growth["warnings"]:
                last_result += f" [{growth['warnings'][0]}]"

            print(f"  {last_result}")

            try:
                api_client.post_observation(
                    current_bottle, day_point, status,
                    ai_status=status, ai_confidence=conf,
                )
                print(f"  → บันทึกแล้ว")
            except Exception as e:
                print(f"  → API error: {e}")

            current_bottle = None

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--day", type=int, required=True, help="Day point ปัจจุบัน")
    p.add_argument("--cam", type=int, default=0, help="Camera index")
    args = p.parse_args()
    run(args.day, args.cam)
