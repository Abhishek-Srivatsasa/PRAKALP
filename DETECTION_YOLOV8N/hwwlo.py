from ultralytics import YOLO

# Download best.pt from the HuggingFace repo manually
# Then load it like this
model = YOLO('best.pt')

# Use stream=True and a loop to keep the webcam feed running and visible
# Replace 'test_video.mp4' with the actual name of your downloaded video file
video_path = 'test_video2.mp4' 
results = model.predict(source=video_path, show=True, conf=0.5, stream=True)

for r in results:
    pass