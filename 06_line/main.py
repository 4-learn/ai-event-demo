from pathlib import Path
from detector import detect_chair
from notifier import send_alert

VIDEO_PATH = Path(__file__).parent.parent / "04_yolo" / "assets" / "aisle-chair-demo.mp4"
# 對應 1280 × 720 影片：左上、右上、右下、左下。
ROI = [(559, 199), (674, 199), (1072, 716), (245, 716)]
ALERT_SECONDS = 3

state = "正常"
blocked_since = None

for video_time, blocked in detect_chair(VIDEO_PATH, ROI):
    if not blocked:
        if state == "占用中":
            print("✓ 通道已清空，事件結束")
        state = "正常"
        blocked_since = None
        continue

    if state == "正常":
        state = "待確認"
        blocked_since = video_time
        print("發現通道占用，開始計時")

    if state == "待確認":
        duration = video_time - blocked_since
        print(f"持續占用：{duration:.1f} 秒")
        if duration >= ALERT_SECONDS:
            state = "占用中"
            print("⚠ 通道占用！發出一次告警")
            send_alert("⚠ 通道占用已持續 3 秒，請安排人員確認。")
