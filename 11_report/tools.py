import csv
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV_PATH = ROOT / "07_logging" / "sample_events.csv"
sys.path.insert(0, str(ROOT / "09_rag"))

_retriever = None


def summarize_events():
    """讀取固定的七天模擬檔，由 Python 計算，不能由模型指定任意檔案。"""
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        events = list(csv.DictReader(file))
    if not events:
        raise ValueError("事件資料為空")

    zones = {}
    hours = Counter()
    dates = []
    for event in events:
        start = datetime.fromisoformat(event["started_at"])
        end = datetime.fromisoformat(event["ended_at"])
        duration = float(event["duration_seconds"])
        if duration < 0 or abs((end - start).total_seconds() - duration) > 0.001:
            raise ValueError("CSV 的時間與持續秒數不一致")
        zone = zones.setdefault(event["zone"], {"event_count": 0, "total_seconds": 0, "longest_seconds": 0})
        zone["event_count"] += 1
        zone["total_seconds"] += duration
        zone["longest_seconds"] = max(zone["longest_seconds"], duration)
        hours[f"{start.hour:02d}:00"] += 1
        dates.extend([start.date(), end.date()])

    return {
        "dataset": CSV_PATH.name,
        "is_simulated": True,
        "period_start": str(min(dates)),
        "period_end": str(max(dates)),
        "timezone": "Asia/Taipei",
        "event_count": len(events),
        "total_seconds": sum(zone["total_seconds"] for zone in zones.values()),
        "zones": zones,
        "events_by_start_hour": dict(sorted(hours.items())),
    }


def search_regulations(query):
    """沿用 09 的語意檢索，回傳三條完整原文與來源，不額外呼叫問答 LLM。"""
    global _retriever
    if _retriever is None:
        from retriever import Retriever
        rules = json.loads((ROOT / "08_crawler" / "regulations.json").read_text(encoding="utf-8"))
        _retriever = Retriever(rules)
    return _retriever.search(query)


TOOL_FUNCTIONS = {"summarize_events": summarize_events, "search_regulations": search_regulations}
TOOL_DEFINITIONS = [
    {
        "type": "function", "name": "summarize_events", "strict": True,
        "description": "統計固定七天的 sample_events.csv 模擬紀錄，取得各區次數、總占用秒數、最長秒數與開始時段。",
        "parameters": {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
    },
    {
        "type": "function", "name": "search_regulations", "strict": True,
        "description": "搜尋教學規範，取得可支持改善建議的原文、條文 ID 與來源。",
        "parameters": {
            "type": "object", "properties": {"query": {"type": "string"}},
            "required": ["query"], "additionalProperties": False,
        },
    },
]
