# 08 網路爬蟲與資料處理

抓取 [GitHub Pages 教學規範](https://4-learn.github.io/ai-event-demo/)，把每一條規範存成可引用的資料。網頁由 main 分支的 docs/ 發布，內容為虛構教學文件，並非正式法規。

```sh
pip install -r requirements.txt
python 08_crawler/main.py
```

- `main.py`：呼叫爬蟲，寫入 regulations.json。
- `crawler.py`：取得 HTML，用 Beautiful Soup 找出每一條規範。
- `regulations.json`：條文 ID、文件名稱、版本、標題、原文、條文連結與擷取時間。

每條規範各自是一個完整的檢索單位，不把條號與原文切開。09 會先從這八條中找出證據，再交給 LLM 回答。
