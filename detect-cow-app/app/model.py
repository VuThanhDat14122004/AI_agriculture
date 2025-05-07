import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

def detect_and_count_cows(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(" Không mở được video:", video_path)
        return

    font = cv2.FONT_HERSHEY_SIMPLEX

    try:
        while True:
            ret, frame = video.read()
            if not ret:
                break

            results = model(frame, conf=0.5)
            boxes = results[0].boxes.xyxy.cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
            count = len(boxes)

            cv2.putText(frame, f"number of cow: {count}", (30, 30), font, 1, (0, 255, 0), 2, cv2.LINE_4)

            for i in range(len(boxes)):
                x1, y1, x2, y2 = boxes[i]
                confidence = confidences[i]
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f'cow, confidence: {confidence:.2f}',
                            (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(" Lỗi trong xử lý video:", str(e))
    finally:
        video.release()
        cv2.destroyAllWindows()
