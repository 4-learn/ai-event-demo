# 04 影像辨識（素材驗證）

本分支從 `03_fsm` 接續，目前先加入測試素材，尚未新增 YOLO 與 FSM 串接程式。

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
