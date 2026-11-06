import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "config.env")


def send_alert(message):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    if not token or not user_id:
        raise ValueError("請在 config.env 設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_USER_ID")

    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}],
    }
    request = Request(
        "https://api.line.me/v2/bot/message/push",
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=10):
            print("LINE API 已接受通知請求")
    except HTTPError as error:
        print(f"LINE 通知失敗：HTTP {error.code}")
    except (URLError, TimeoutError):
        print("LINE 通知失敗：連線異常或逾時")
