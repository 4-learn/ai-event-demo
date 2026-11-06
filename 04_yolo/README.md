# 04 影像辨識 × 有限狀態機

本分支從 `03_fsm` 接續，用 YOLO 的辨識結果取代鍵盤輸入。

## 執行

在專案根目錄執行：

```bash
source .env/bin/activate
python -m pip install -r requirements.txt
python 04_yolo/main.py
```

尚未建立環境時，先執行 `python3 -m venv .env`。第一次執行會下載模型到 `04_yolo/models/`。

- `detector.py`：按影片時間每秒取樣一次，只辨識 chair，交出 `"1"` 或 `"0"`。
- `main.py`：連續三個取樣結果有椅子才告警，持續占用不重複告警，沒椅子就立即解除。

預期九次取樣結果為 `0、0、1、1、1、1、1、0、0`，告警一次、解除一次。每秒取樣不代表程式真的等待一秒；影片結束只停止讀取，不會自動解除。

YOLO 使用預訓練模型，不需要自行訓練。ESP32-CAM 串流與 ROI 留待後續版本。

## 素材

- `assets/aisle-empty.png`：空通道。
- `assets/aisle-chair.png`：同一鏡位的通道加入工作椅。
- `results/`：YOLO 原始辨識框圖片與 JSON 測試紀錄。

圖片以 OpenAI 影像工具生成與編輯，屬於合成教學素材，非工廠實拍。先生成空通道，再以該圖加入黑色工作椅，保持相同場景與鏡位。

## 初步驗證

在 4-learn 使用 YOLO11n（yolo11n.pt）、CPU、imgsz=640、conf=0.25，Ultralytics 8.4.203。

| 圖片 | 椅子辨識 |
| --- | --- |
| 空通道 | 無 |
| 通道＋椅子 | chair，信心分數 0.9351 |

兩張圖均將遠處的門誤判為 refrigerator，後續事件判斷將只採用 chair 類別。信心分數不代表準確率。

原圖辨識已通過這次測試，ESP32-CAM 翻拍效果尚待驗證。

## 測試影片

[下載 aisle-chair-demo.mp4](assets/aisle-chair-demo.mp4)

由上述兩張合成圖片組成，無聲、1280×720、25 FPS、9 秒，沒有搬運動作。

- 0～2 秒：空通道。
- 2～7 秒：工作椅占用通道。
- 7～9 秒：回到空通道。

若要對照每秒一次的九次輸入，辨識程式需每秒取樣一次；影片本身是 25 FPS，逐幀處理時「連續 3 次」並不等於 3 秒。
