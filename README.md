# AI 事件管理系統

給 Python 初學者的課程示範：從通道占用的故事，逐步串起事件判斷、影像辨識、LINE 通知與 AI 報告。

## 章節分支

每一章從上一章接續，只增加少量功能。請切換到對應分支查看程式。

| 分支 | 內容 |
| --- | --- |
| [03_fsm](https://github.com/4-learn/ai-event-demo/tree/03_fsm) | 用鍵盤輸入，理解有限狀態機、計數與告警門檻。 |
| [04_yolo](https://github.com/4-learn/ai-event-demo/tree/04_yolo) | 每秒取樣，用 YOLO 辨識工作椅。 |
| [05_roi](https://github.com/4-learn/ai-event-demo/tree/05_roi) | 限定通道範圍，持續三秒才告警。 |
| [06_line](https://github.com/4-learn/ai-event-demo/tree/06_line) | 事件成立後推播 LINE。 |
| [07_logging](https://github.com/4-learn/ai-event-demo/tree/07_logging) | 解除後寫入 CSV，附七天模擬紀錄。 |
| [08_crawler](https://github.com/4-learn/ai-event-demo/tree/08_crawler) | 擷取教學規範，保留條文與來源。 |
| [09_rag](https://github.com/4-learn/ai-event-demo/tree/09_rag) | 語意檢索、依證據回答與引用檢查。 |
| [10_agent](https://github.com/4-learn/ai-event-demo/tree/10_agent) | 讓模型選擇事件統計與規範工具。 |
| [11_report](https://github.com/4-learn/ai-event-demo/tree/11_report) | 用 Python 輸出一頁 PDF，附可直接查看的範例。 |

```bash
git clone https://github.com/4-learn/ai-event-demo.git
cd ai-event-demo
git switch 03_fsm
```

`main` 目前作為課程入口，日後放置總成果。其他章節會依進度加入。

[通道管理辦法（教學模擬）](https://4-learn.github.io/ai-event-demo/)：由本分支 docs/ 發布，供爬蟲與 RAG 使用，並非正式法規。
