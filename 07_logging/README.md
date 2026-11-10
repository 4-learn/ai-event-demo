# 07 事件儲存

06 讓人收到通知；07 用 Python 內建 csv 留下事件紀錄，再用 pandas 清理有缺值的紀錄。

- `main.py`：沿用 06，在已告警事件解除時呼叫 `save_event()`。
- `event_logger.py`：產生事件 ID、計算秒數，追加寫入 CSV；首次寫入才建立表頭。
- `clean_events.py`：用 pandas 讀取 `sample_events.csv`，刪掉有缺值的列，存回同一個檔案。
- `detector.py`、`notifier.py`：沿用 06。

在 repo 根目錄執行（沿用 config.env 與既有套件）：

```sh
python 07_logging/main.py
cat 07_logging/events.csv
```

程式會實際發送一次 LINE 通知。原影片在第 2 秒開始占用，第 5 秒告警，第 7 秒解除；最後追加一筆約 5 秒的事件。

`started_at` 是本次 demo 的起始時間加上影片中的首次占用時間，不是告警時間；日期時間固定使用台北時區。影片可加速處理，因此 CSV 日期時間是教學用的影片時間軸換算，不是實際送出 LINE 的時刻。

## 用 pandas 清理缺值

實際紀錄常有不完整的列，例如程式中斷、事件沒有解除，就沒有結束時間與秒數。`sample_events.csv` 共 34 筆，其中 4 筆不完整：

| event_id | 缺少的欄位 | 可能的原因（教學設定） |
| --- | --- | --- |
| sample_031 | zone | 沒記到區域 |
| sample_032 | ended_at、duration_seconds | 程式中斷，事件未解除 |
| sample_033 | started_at、duration_seconds | 沒記到開始時間 |
| sample_034 | duration_seconds | 沒算出秒數 |

```sh
python 07_logging/clean_events.py
```

輸出：

```text
讀入 34 筆
各欄缺值數：
event_id            0
zone                1
started_at          1
ended_at            1
duration_seconds    3
dtype: int64
有缺值的列：
      event_id      zone  duration_seconds
15  sample_031       NaN              60.0
16  sample_032  aisle_01               NaN
32  sample_033  aisle_02               NaN
33  sample_034  aisle_01               NaN
刪掉 4 筆，剩下 30 筆
已存回 sample_events.csv
```

1. `pd.read_csv()`：讀進 DataFrame，空白的格子會變成 `NaN`。
2. `df.isna().sum()`：每一欄有幾個缺值。
3. `df.dropna()`：只要有一欄是缺值，就刪掉整列。
4. `astype({"duration_seconds": int})`：有缺值時 pandas 會把整數存成小數（`120` 變 `120.0`），刪完後轉回整數。
5. `to_csv(..., index=False)`：存回同一個 CSV，不寫入左邊的 index。

清理後剩下 30 筆完整紀錄，**10、11 的統計就是讀這份清好的資料**，所以要先跑完這一步。再執行一次會顯示「刪掉 0 筆」，不會重複刪資料。

刪掉的 4 筆不代表現場沒發生事件，只是紀錄不完整、這次不列入統計。

### 想重新練習

`clean_events.py` 會直接改寫 `sample_events.csv`。要回到 34 筆、含缺值的原始版本：

```sh
git checkout -- 07_logging/sample_events.csv
```

## 資料檔

| 檔案 | 用途 |
| --- | --- |
| `events.csv` | 執行 `main.py` 產生，已忽略、不上傳 GitHub |
| `sample_events.csv` | 模擬資料：2026-10-30 至 2026-11-05、兩區域。版本控制中是 34 筆（含 4 筆缺值）；執行 `clean_events.py` 後剩 30 筆，供 10、11 統計 |

欄位一致：event_id、zone、started_at、ended_at、duration_seconds。不要把模擬資料當作實際工廠紀錄。

本章只存「已達三秒門檻且已解除」的事件。影片結束不代表解除；未解除或程式中斷時，該事件尚未存檔。單一程式追加寫入，不支援多個程序同時寫入。
