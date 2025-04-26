import os
import cv2
import yaml
import glob
from ultralytics import YOLO
import matplotlib.pyplot as plt


model = YOLO("runs/detect/train/weights/best.pt")

video_path = 'cow_vid.mp4'
video = cv2.VideoCapture(video_path)
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    results = model(frame, conf=0.6)    
    count = len(results[0].boxes)
    print(f'Detected objects count: {count}')
    # Display the results
    for result in results:
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Get bounding box coordinates
        confidences = results[0].boxes.conf.cpu().numpy() # cpu to avoid cuda error 
        for i in range(len(boxes)):
            box = boxes[i]
            x1, y1, x2, y2 = box  # x_min, ymin, xmax, ymax = box
            confidence = confidences[i]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'Number: {i}, confidence: {confidence:.2f}',\
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
