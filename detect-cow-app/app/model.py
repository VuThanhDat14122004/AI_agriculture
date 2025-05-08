import cv2
from ultralytics import YOLO
import torch
import ultralytics



torch.serialization.add_safe_globals([ultralytics.nn.tasks.DetectionModel])
torch.serialization.add_safe_globals([torch.nn.modules.container.Sequential])
torch.serialization.add_safe_globals([torch.nn.modules.module.Module])
torch.serialization.add_safe_globals([ultralytics.nn.modules.conv.Conv])


model = YOLO("best.pt")

def detect_and_count_cows(video_path, output_path):
    video = cv2.VideoCapture(video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_SIMPLEX

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        results = model(frame, conf=0.5)
        count = len(results[0].boxes)

        cv2.putText(frame, f"number of cow: {count}", (30, 30), font, 1, (0, 255, 0), 2)

        boxes = results[0].boxes.xyxy.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()

        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes[i]
            confidence = confidences[i]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'cow: {confidence:.2f}', (int(x1), int(y1) - 10),
                        font, 0.5, (0, 255, 0), 2)

        out.write(frame)

    video.release()
    out.release()
