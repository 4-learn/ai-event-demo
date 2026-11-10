"""讀取事件紀錄，刪掉有缺值的列，再存回同一個 CSV。"""
from pathlib import Path

import pandas as pd

CSV_PATH = Path(__file__).parent / "sample_events.csv"

df = pd.read_csv(CSV_PATH)
print(f"讀入 {len(df)} 筆")

print("各欄缺值數：")
print(df.isna().sum())

print("有缺值的列：")
print(df[df.isna().any(axis=1)][["event_id", "zone", "duration_seconds"]])

clean = df.dropna()
print(f"刪掉 {len(df) - len(clean)} 筆，剩下 {len(clean)} 筆")

# 有缺值時 pandas 會把整數欄存成小數（120 變 120.0），刪完缺值後轉回整數。
clean = clean.astype({"duration_seconds": int})

clean.to_csv(CSV_PATH, index=False)
print(f"已存回 {CSV_PATH.name}")
