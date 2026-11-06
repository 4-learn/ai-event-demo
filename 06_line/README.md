# 06 即時通知

延續 05，只在事件進入「占用中」時，傳送一次 LINE 文字通知。

- `main.py`：ROI、三秒計時、有限狀態機，並呼叫通知。
- `detector.py`：沿用 05 的辨識流程。
- `notifier.py`：讀取設定並呼叫 LINE Messaging API。

在 repo 根目錄建立 `config.env`（已加入忽略清單）：

```dotenv
LINE_CHANNEL_ACCESS_TOKEN=你的token
LINE_USER_ID=你的user_id
```

收件人需先加入該 LINE 官方帳號好友。從 repo 根目錄執行：

```sh
pip install -r requirements.txt
python 06_line/main.py
```

沿用 04 的合成影片與模型；通知失敗會顯示原因，不自動重試。
API 接受請求不代表手機已收到通知，實際收到仍需在 LINE 確認。
