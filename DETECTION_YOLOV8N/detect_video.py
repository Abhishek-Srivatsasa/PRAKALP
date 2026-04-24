from ultralytics import YOLO
import time
import os

# 1. Load your fine-tuned model
model = YOLO('best.pt')

# 2. Specify the video path (replace with your actual video name)
video_path = 'Gemini.mp4' # or test_video(1/2).mp4

# 3. Run prediction with stream=True for memory efficiency
results = model.predict(source=video_path, show=True, conf=0.5, stream=True)

# Create Detections folder if it doesn't exist
os.makedirs("Detections", exist_ok=True)

last_capture_time = 0

# Loop through the video frames to keep the window updating
for r in results:
    if len(r.boxes) > 0:
        current_time = time.time()
        # Check if 5 seconds have passed since the last photo
        if current_time - last_capture_time >= 5:
            f_name = f"detected_Video_file_{int(current_time)}.jpg"
            save_path = os.path.join("Detections", f_name)
            r.save(filename=save_path) 
            print(f"📸 Snapshot saved of Video file: {save_path}")
            
            # Reset the stopwatch!
            last_capture_time = current_time