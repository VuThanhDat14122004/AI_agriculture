import cv2
from ultralytics import YOLO
import os

# Kiểm tra file mô hình
if not os.path.exists("best.pt"):
    raise FileNotFoundError("Model file best.pt not found")
model = YOLO("best.pt")

def detect_and_count_cows(video_path, output_path):
    # Kiểm tra file đầu vào
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Mở video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    # Lấy thông số video và giảm độ phân giải
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
    fps = video.get(cv2.CAP_PROP_FPS)

    # Thiết lập video đầu ra với codec XVID
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        video.release()
        raise ValueError(f"Cannot write to output file: {output_path}")

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame_count = 0

    # Xử lý từng frame
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_count += 1
        frame = cv2.resize(frame, (width, height))

        # Bỏ qua mỗi frame thứ 2 để giảm tải
        if frame_count % 2 != 0:
            out.write(frame)
            continue

        # Dự đoán với YOLO
        results = model(frame, conf=0.5)
        count = len(results[0].boxes)

        # Vẽ số lượng bò
        cv2.putText(frame, f"Number of cows: {count}", (30, 30), font, 1, (0, 255, 0), 2)

        # Vẽ bounding boxes
        boxes = results[0].boxes.xyxy.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()

        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes[i]
            confidence = confidences[i]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'cow: {confidence:.2f}', (int(x1), int(y1) - 10),
                        font, 0.5, (0, 255, 0), 2)

        # Ghi frame vào video đầu ra
        out.write(frame)

    # Giải phóng tài nguyên
    video.release()
    out.release()