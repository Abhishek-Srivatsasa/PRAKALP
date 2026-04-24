import cv2
from ultralytics import YOLO
import time

# --- CONFIGURATION ---
MODEL_PATH = 'best.onnx'  # POINTING TO THE NEW ONNX FILE
CONF_LEVEL = 0.45
IMG_SIZE = 320            # CRITICAL: Keep this at 320 for speed

print("🚀 Garuda Linux Core: Loading ONNX Engine...")

# 1. Load ONNX Model
try:
    # Ultralytics automatically detects the ONNX format and uses the fastest available provider
    model = YOLO(MODEL_PATH, task='detect')
    print("✅ ONNX Engine LIVE")
except Exception as e:
    print(f"❌ Load Error: {e}")
    exit()

cap = cv2.VideoCapture(0)
# Set low resolution for the camera buffer to prevent "Old Frame" lag
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("🟢 STREAM STARTING...")

while True:
    success, frame = cap.read()
    if not success: break

    # --- THE "ZERO LAG" INFERENCE ---
    # verbose=False removes the slow print-to-console lag
    results = model.predict(source=frame, imgsz=IMG_SIZE, conf=CONF_LEVEL, verbose=False)

    # Simple display
    annotated_frame = results[0].plot()
    cv2.imshow("Garuda - ONNX Vision", annotated_frame)

    # Coordinates for Turret Logic
    for box in results[0].boxes:
        x_c, y_c, _, _ = box.xywh[0]
        # Only print if you NEED it for debugging, otherwise it slows the loop
        # print(f"X: {int(x_c)} Y: {int(y_c)}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()