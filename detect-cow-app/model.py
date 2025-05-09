import cv2
from ultralytics import YOLO
import os
import time
import gdown
from ultralytics import settings


url_model = "https://drive.google.com/uc?id=1-fn96rROeiwnvBcHjV-N6xMfgoSC8eht"
# model = YOLO("best.pt")
if not os.path.exists("best.pt"):
    gdown.download(url_model, "best.pt", quiet=False)
model = YOLO("best.pt")

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=0.5)
        count = len(results[0].boxes)
        cv2.putText(frame, f"Number of cows: {count}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Get bounding box coordinates
        confidences = results[0].boxes.conf.cpu().numpy() # cpu to avoid cuda error 
        for i in range(len(boxes)):
            box = boxes[i]                                                                                                                                                                                                                                                                                                                                                                                                  
            x1, y1, x2, y2 = box  # x_min, ymin, xmax, ymax = box
            confidence = confidences[i]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'cow, confidence: {confidence:.2f}',\
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)
        time.sleep(0.5)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
