import cv2
from ultralytics import YOLO

model = YOLO("app/best.pt")

def detect_and_count_cows(video_path):
    cap = cv2.VideoCapture(video_path)
    width, height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out_path = "/tmp/output.mp4"
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        confidences = results[0].boxes.conf.cpu().numpy()
        boxes = results[0].boxes.xyxy.cpu().numpy()
        for box, confidence in zip(boxes, confidences):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'cow, confidence: {confidence:.2f}',\
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)

    cap.release()
    out.release()
    return out_path
