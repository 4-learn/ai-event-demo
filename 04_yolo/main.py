from pathlib import Path
from detector import detect_chair

VIDEO_PATH = Path(__file__).parent / "assets" / "aisle-chair-demo.mp4"
ALERT_THRESHOLD = 3

state = "正常"
blocked_count = 0

for detected in detect_chair(VIDEO_PATH, sample_seconds=1):
    previous_state = state

    if detected == "0":
        if state == "占用中":
            print("✓ 通道已清空，事件結束")

        blocked_count = 0
        state = "正常"

    elif state in ("正常", "待確認"):
        blocked_count += 1
        state = "待確認"

        print(f"占用確認：{blocked_count}/{ALERT_THRESHOLD}")

        if blocked_count >= ALERT_THRESHOLD:
            state = "占用中"
            print("⚠ 通道占用！發出一次告警")

    print(f"{previous_state} → {state}")
