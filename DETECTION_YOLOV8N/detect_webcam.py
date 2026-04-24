import cv2
from ultralytics import YOLO as yl
import os 
import time

try :
	model = yl('best.onnx', task = 'detect')
	print("ONNX loaded for CPU")
except Exception as e :
	print(f"Error: Couldn't find the onnx module")
	exit()

SAVE_DIR = "Detections"
os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

last_save_time = 0 
prev_frame_time = 0
print("TURRET ACTIVE ::::::: ")

while True :
	success, frame = cap.read() 
	if not success:
		break

	results = model(frame, imgsz=320, conf=0.5, verbose=False, device="cpu")
	for r in results:
		annotated_frame = r.plot() 
		
		new_frame_time = time.time()
		fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
		prev_frame_time = new_frame_time
		
		cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
		
		cv2.imshow("GARUDA TURRET",annotated_frame)
		
		if len(r.boxes) >0 :
			current_time = time.time()
			if current_time - last_save_time > 3:
				timestamp = int(current_time)

				file_path = os.path.join(SAVE_DIR, f"Drone_detected_{timestamp}.jpg")
				cv2.imwrite(file_path, annotated_frame)
				
				# Mirror to the website
				website_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PRAKALP_WHITE_BG')
				os.makedirs(website_dir, exist_ok=True)
				cv2.imwrite(os.path.join(website_dir, 'latest_detection.jpg'), annotated_frame)

				print(f"TARGET IMAGE CAPTURED : {file_path}")
				last_save_time = current_time
	if cv2.waitKey(1) & 0xFF == ord('q') :
		break
cap.release()
cv2.destroyAllWindows()
print("GARUDA STOPPED")