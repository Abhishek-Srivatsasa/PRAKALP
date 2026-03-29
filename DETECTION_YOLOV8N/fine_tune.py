from ultralytics import YOLO

# 1. Load your existing pre-trained weights
model = YOLO('best.pt')

# 2. Fine-tune the model on your new dataset
# Using the configured coco.yaml file
# You can adjust the epochs (e.g., 10-50) depending on how much new data you have
results = model.train(data='coco.yaml', epochs=2, imgsz=640)