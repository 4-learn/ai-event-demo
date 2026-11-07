# 11 長期回顧與 PDF 報告

沿用 10 的 Agent，只增加 `save_report()`，把結果排成一頁 PDF。

```sh
pip install -r requirements.txt
python 11_report/main.py
```

直接按 Enter 使用預設問題；會實際呼叫 OpenAI API，終端機顯示工具選擇。

- `main.py`：詢問、執行 Agent、呼叫 save_report()。
- `agent.py`、`tools.py`：沿用 10。
- `report.py`：數字直接取 Python 統計，LLM 提供觀察與兩項附來源的建議。
- `output/weekly_report.pdf`：一頁報告。
- `output/weekly_report.json`：工具選擇、統計、檢索原文與 API 用量，方便核對。

不呼叫 API 也可以先看 [已產生的範例 PDF](example/weekly_report.pdf)，以及旁邊同名 JSON 的實際工具紀錄。

PDF 使用可嵌入的中文字型；4-learn 已有文泉驛正黑，其他 Linux 可安裝 fonts-wqy-zenhei，或以 REPORT_FONT 指定 TrueType 中文字型。

資料固定為七天、兩區域的虛構 sample_events.csv，清楚標示為教學模擬，不能當成實際工廠改善或歸責依據。若文字太長，一頁模板會提示錯誤，不縮到難以閱讀。輸出目錄已忽略，不隨 Git 上傳。
