ALERT_THRESHOLD = 3

state = "正常"
blocked_count = 0

print("1：有物品｜0：沒物品｜q：結束")

while True:
    detected = input("\n請輸入：").strip()

    if detected == "q":
        break

    if detected not in ("0", "1"):
        print("請輸入 0、1 或 q")
        continue

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
