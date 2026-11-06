import json
from pathlib import Path

from crawler import fetch_regulations

regulations = fetch_regulations()
output = Path(__file__).parent / "regulations.json"
output.write_text(
    json.dumps(regulations, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(f"取得 {len(regulations)} 條規範，已儲存至 {output.name}")
for rule in regulations:
    print(rule["section"], rule["source"])
