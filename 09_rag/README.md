# 09 檢索增強生成

使用本機語意檢索找出三條規範，再由 gpt-6-luna 根據證據回答與引用原文。

- `main.py`：輸入問題，顯示回答、來源與逐字引文。
- `retriever.py`：E5 語意向量；短句索引、以最高相關分數選出完整條文。
- `prompt.txt`：只依據檢索證據回答、資訊不足時明說，回傳條文 ID 與逐字引文。
- `answer_check.py`：拒絕未檢索的 ID 與不存在的原文，不能代替語意核對。
- `llm.py`：讀取金鑰，透過 Responses API 取得 JSON 回答與 token 用量；不自動重試。
- `evaluation/`：固定測試題與逐題結果，保留失敗案例。

本原型不使用向量資料庫；八條規範在記憶體中即可。模型首次執行需要下載，應在上課前準備好。

在根目錄的 config.env 加入 OPENAI_API_KEY，選用 LLM_MODEL（預設 gpt-6-luna）。保留原本 LINE 設定，設定檔已忽略、不上傳 GitHub。

```sh
pip install -r requirements.txt
python 09_rag/main.py
```

使用既有 CPU PyTorch，執行前先安裝套件、預先下載 embedding 模型。規範更新後，先執行 `python 08_crawler/main.py`。

## 已知測試結果

修正一處模擬資料範圍的過度概括後，最終 28 題的引用格式與逐字原文檢查通過；人工核對 26 題有充分依據，另 2 題仍缺少完整依據，保留為待改善，不宣稱全部問題都能回答。

詳見 evaluation/validated_results.json 與 evaluation/README.md。需要重新測 20 題時執行 `python 09_rag/evaluation/run.py`，會呼叫 API 並產生費用；這是驗證工具，不是學生需要逐行理解的主程式。
