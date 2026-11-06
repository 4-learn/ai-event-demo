# 07 事件儲存

06 讓人收到通知；07 用 Python 內建 csv 留下事件紀錄，不需要 pandas。

- `main.py`：沿用 06，在已告警事件解除時呼叫 `save_event()`。
- `event_logger.py`：產生事件 ID、計算秒數，追加寫入 CSV；首次寫入才建立表頭。
- `detector.py`、`notifier.py`：沿用 06。

在 repo 根目錄執行（沿用 config.env 與既有套件）：

```sh
python 07_logging/main.py
cat 07_logging/events.csv
```

程式會實際發送一次 LINE 通知。原影片在第 2 秒開始占用，第 5 秒告警，第 7 秒解除；最後追加一筆約 5 秒的事件。

`started_at` 是本次 demo 的起始時間加上影片中的首次占用時間，不是告警時間；日期時間固定使用台北時區。影片可加速處理，因此 CSV 日期時間是教學用的影片時間軸換算，不是實際送出 LINE 的時刻。

## 兩份資料

| 檔案 | 用途 |
| --- | --- |
| `events.csv` | 執行程式產生，已忽略、不上傳 GitHub |
| `sample_events.csv` | 明確為模擬資料：2026-10-30 至 2026-11-05、兩區域、30 筆，供後續統計與 Agent 使用 |

兩份欄位一致：event_id、zone、started_at、ended_at、duration_seconds。不要把模擬資料當作實際工廠紀錄。

本章只存「已達三秒門檻且已解除」的事件。影片結束不代表解除；未解除或程式中斷時，該事件尚未存檔。單一程式追加寫入，不支援多個程序同時寫入。
