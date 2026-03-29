from ultralytics import YOLO
import time 
import os
import cv2

# 1. Load your fine-tuned model
model = YOLO('best.pt')

# 2. Run prediction using the default webcam (source=0)
# stream=True is essential for live camera feeds
results = model.predict(source="http://192.168.29.131:8080/video", conf=0.8, stream=True) 
# To use the IP Webcam app from phone to laptop -- "http://192.168.29.131:8080/video"
# TO use the Laptop camera put the source = 0 

# Create Detections folder if it doesn't exist
os.makedirs("Detections", exist_ok=True)

last_capture_time = 0

for r in results:
    # Grab the frame with the AI's boxes drawn on it
    annotated_frame = r.plot()
    # Display it in a custom window
    cv2.imshow("Turret Vision", annotated_frame)

    # Loop through detected drones to get their exact center coordinates
    for box in r.boxes:
        # xywh gives us a list of [x_center, y_center, width, height]
        x_center, y_center, width, height = box.xywh[0]
        
        x, y = int(x_center), int(y_center)
        print(f"🎯 Target Locked! Aiming Turret at X:{x} Y:{y}")

    if len(r.boxes) > 0 :
        current_time = time.time()
        # Check if 5 seconds have passed since the last photo
        if current_time - last_capture_time >= 5:
            f_name = f"detected_Webcam_file_{int(current_time)}.jpg"
            save_path = os.path.join("Detections", f_name)
            r.save(filename=save_path) 
            print(f"📸 Snapshot saved of webcam file: {save_path}")
            
            # Reset the stopwatch!
            last_capture_time = current_time

    # Press 'q' to close the window safely
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
