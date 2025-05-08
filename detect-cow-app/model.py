import cv2
from ultralytics import YOLO
import os
import gdown

MODEL_PATH = "best.pt"
url = "https://drive.google.com/file/d/1-fn96rROeiwnvBcHjV-N6xMfgoSC8eht/view?usp=sharing"

gdown.download(url, MODEL_PATH, quiet=False)

model = YOLO(MODEL_PATH)

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"Cow {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        yield frame
    cap.release()
