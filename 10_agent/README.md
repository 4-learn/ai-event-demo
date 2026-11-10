# 10 AI Agent

09 是規範問答；10 讓模型實際選擇工具，讀七天事件統計、查規範，再提出建議。

```sh
python 10_agent/main.py
```

問題可直接按 Enter，使用預設的七天回顧。終端機會顯示模型選了哪個工具。

- `main.py`：接收問題、顯示結果。
- `agent.py`：最多六次模型回合、四次工具呼叫，無自動重試。
- `tools.py`：summarize_events() 用 Python 內建 csv 統計；search_regulations(query) 沿用 09 的檢索。

資料固定為 07 的 sample_events.csv（先執行 `python 07_logging/clean_events.py` 清掉缺值；還沒清理時，程式會提示這一步。），涵蓋 2026-10-30 至 2026-11-05，是虛構教學資料。不是目前現場，也不能任意更換查詢期間。

模型必須取得統計與規範才產生報告；Python 驗證引用原文是否存在，但仍須核對建議是否受到原文支持。沿用既有 config.env 與 requirements.txt，會呼叫 OpenAI API。
