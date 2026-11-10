"""讀取有缺值的事件紀錄，刪掉不完整的列，再存成新的 CSV。"""
from pathlib import Path

import pandas as pd

FOLDER = Path(__file__).parent
RAW_PATH = FOLDER / "raw_events.csv"
CLEAN_PATH = FOLDER / "clean_events.csv"

df = pd.read_csv(RAW_PATH)
print(f"讀入 {len(df)} 筆")

print("各欄缺值數：")
print(df.isna().sum())

print("有缺值的列：")
print(df[df.isna().any(axis=1)][["event_id", "zone", "duration_seconds"]])

clean = df.dropna()
print(f"刪掉 {len(df) - len(clean)} 筆，剩下 {len(clean)} 筆")

# 有缺值時 pandas 會把整數欄存成小數（120 變 120.0），刪完缺值後轉回整數。
clean = clean.astype({"duration_seconds": int})

clean.to_csv(CLEAN_PATH, index=False)
print(f"已存成 {CLEAN_PATH.name}")
