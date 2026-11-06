from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO


def detect_chair(video_path, roi, sample_seconds=1):
    if sample_seconds <= 0:
        raise ValueError("取樣間隔必須大於 0")

    # 沿用 04 的模型，不必再下載一份。
    model_path = Path(__file__).parent.parent / "04_yolo" / "models" / "yolo11n.pt"
    model_path.parent.mkdir(exist_ok=True)
    model = YOLO(str(model_path))
    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        video.release()
        raise RuntimeError("無法開啟影片")

    fps = video.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        video.release()
        raise RuntimeError("無法取得影片 FPS")

    sample_every = max(1, round(fps * sample_seconds))
    frame_count = 0
    roi_polygon = np.array(roi, dtype=np.int32)

    try:
        while True:
            success, frame = video.read()
            if not success:
                break

            # 依影片時間抽幀，不是讓程式等待一秒。
            if frame_count % sample_every == 0:
                result = model.predict(
                    frame,
                    classes=[56],  # COCO 的 chair 類別
                    conf=0.25,
                    imgsz=640,
                    verbose=False,
                )[0]
                blocked = False
                for x1, y1, x2, y2 in result.boxes.xyxy.tolist():
                    bottom_center = ((x1 + x2) / 2, y2)
                    # 在多邊形內或邊界上，都算占用。
                    if cv2.pointPolygonTest(roi_polygon, bottom_center, False) >= 0:
                        blocked = True
                        break

                video_time = frame_count / fps
                yield video_time, blocked

            frame_count += 1
    finally:
        video.release()
