from ultralytics import YOLO
import time
import os

# 1. Load your fine-tuned model
model = YOLO('best.pt')

# 2. Specify the image path (replace with your actual image name)
image_path = 'test_image5.png' # Or test_image(1/2).jpg

# Create Detections folder if it doesn't exist
os.makedirs("Detections", exist_ok=True)

# 3. Run prediction
# show=True displays the image
results = model.predict(source="http://192.168.29.131:8080/video", show=True, conf=0.5)

for r in results:
    if len(r.boxes) > 0:
        f_name = f"detected_Image_file_{int(time.time())}.jpg"
        save_path = os.path.join("Detections", f_name)
        r.save(filename=save_path)
        print(f"📸 Snapshot saved of Image file: {save_path}")