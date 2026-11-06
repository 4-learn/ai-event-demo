from pathlib import Path

import cv2
from ultralytics import YOLO


def detect_chair(video_path, sample_seconds=1):
    if sample_seconds <= 0:
        raise ValueError("取樣間隔必須大於 0")

    model_path = Path(__file__).parent / "models" / "yolo11n.pt"
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
                has_chair = len(result.boxes) > 0
                yield "1" if has_chair else "0"

            frame_count += 1
    finally:
        video.release()
